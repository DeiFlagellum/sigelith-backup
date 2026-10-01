"""Dowód czasu dla pojedynczego pliku z kopii (format ``sigelith-file-proof-v1``).

Po co: pieczęć wersji (proof.py) obejmuje spis wszystkich plików wersji naraz.
Żeby udowodnić istnienie jednego pliku, trzeba by pokazać cały spis — nazwy
i sumy wszystkich innych plików. Tu pieczęć obejmuje korzeń drzewa Merkle'a
nad plikami wersji, więc dowód jednego pliku to jego liść i kilkadziesiąt
skrótów po drodze do korzenia — reszta kopii zostaje nieujawniona.

Budowa (opis dla każdego, kto chce sprawdzić dowód bez tego programu):

* liść pliku = SHA-256(0x00 ‖ sól ‖ SHA-256 pliku ‖ rozmiar (8 bajtów, big-endian)
  ‖ SHA-256 ścieżki w kopii (UTF-8)) — pola o stałej długości, więc zapis jest
  jednoznaczny;
* sól = HMAC-SHA256(ziarno wersji, ścieżka) — losowe ziarno leży tylko w folderze
  wersji; bez soli ze skrótów sąsiadów w dowodzie dałoby się zgadywać, czy
  w kopii był plik o znanej treści;
* węzeł = SHA-256(0x01 ‖ lewy ‖ prawy); liście w kolejności spisu wersji,
  łączone parami poziom po poziomie, nieparzysty ostatni węzeł przechodzi wyżej
  bez zmian — ta sama reguła 0x00/0x01 co w drzewach tygodni Sigelith;
* oświadczenie pieczęci — cztery wiersze tekstu (``SIGELITH-BACKUP-SEAL 1``,
  suma spisu wersji, korzeń drzewa plików, liczba plików); do Sigelith trafia
  wyłącznie SHA-256 oświadczenia, a jego potwierdzenie to zwykły ``beatproof-v1``.
"""

from __future__ import annotations

import hashlib
import hmac
import time
from collections.abc import Iterable, Sequence
from pathlib import Path

FORMAT = "sigelith-file-proof-v1"
SUFFIX = ".sigelith-proof"
STATEMENT_HEADER = "SIGELITH-BACKUP-SEAL 1"
HOW_TO_VERIFY = (
    '1) SHA-256 of the file must equal file.sha256 and its length file.size. 2) If file.path is '
    'present, SHA-256 of its UTF-8 bytes must equal leaf.path_sha256. 3) leaf = SHA-256(0x00 || '
    'leaf.salt || file.sha256 || size as 8-byte big-endian || leaf.path_sha256); fold merkle_path '
    'with SHA-256(0x01 || left || right) ("side" is the side of the sibling) — the result must '
    'equal files_root. 4) statement must say "files-root <files_root>" and "files <files>". '
    '5) SHA-256 of statement (UTF-8) must equal beatproof.digest, and the beatproof must verify '
    'as described in its own how_to_verify. Spec: https://sigelith.org/spec/#file-proof'
)


# ----------------------------------------------------------------- drzewo


def file_salt(seed: bytes, key: str) -> bytes:
    return hmac.new(seed, key.encode("utf-8"), hashlib.sha256).digest()


def path_digest(key: str) -> bytes:
    return hashlib.sha256(key.encode("utf-8")).digest()


def leaf(salt: bytes, sha256_hex: str, size: int, path_sha: bytes) -> bytes:
    if len(salt) != 32 or len(path_sha) != 32 or size < 0:
        raise ValueError("bad leaf")
    return hashlib.sha256(
        b"\x00" + salt + bytes.fromhex(sha256_hex) + size.to_bytes(8, "big") + path_sha
    ).digest()


def node(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(b"\x01" + left + right).digest()


def _next_level(level: Sequence[bytes]) -> list[bytes]:
    parents = [node(level[i], level[i + 1]) for i in range(0, len(level) - 1, 2)]
    if len(level) % 2:
        parents.append(level[-1])
    return parents


def merkle_root(leaves: Sequence[bytes]) -> bytes:
    if not leaves:
        raise ValueError("empty tree")
    level = list(leaves)
    while len(level) > 1:
        level = _next_level(level)
    return level[0]


def merkle_path(leaves: Sequence[bytes], index: int) -> list[dict[str, str]]:
    """Skróty sąsiadów od liścia do korzenia; ``side`` mówi, po której stronie stoi sąsiad."""
    if not 0 <= index < len(leaves):
        raise IndexError(index)
    path: list[dict[str, str]] = []
    level, position = list(leaves), index
    while len(level) > 1:
        sibling = position ^ 1
        if sibling < len(level):  # ostatni nieparzysty węzeł przechodzi wyżej bez kroku
            path.append({"side": "L" if sibling < position else "R", "hash": level[sibling].hex()})
        level, position = _next_level(level), position // 2
    return path


def fold(start: bytes, path: Iterable[dict | Sequence[str]]) -> bytes:
    current = start
    for step in path:
        side, sibling_hex = (step["side"], step["hash"]) if isinstance(step, dict) else step
        sibling = bytes.fromhex(sibling_hex)
        if len(sibling) != 32 or side not in ("L", "R"):
            raise ValueError("bad path step")
        current = node(sibling, current) if side == "L" else node(current, sibling)
    return current


def leaves_for(entries: Iterable[tuple[str, int, str]], seed: bytes) -> tuple[list[str], list[bytes]]:
    """Klucze i liście w kolejności spisu wersji (posortowane jak w ``version_index``)."""
    keys: list[str] = []
    leaves: list[bytes] = []
    for key, size, sha in sorted(entries):
        keys.append(key)
        leaves.append(leaf(file_salt(seed, key), sha, int(size), path_digest(key)))
    return keys, leaves


def files_root(entries: Iterable[tuple[str, int, str]], seed: bytes) -> str:
    return merkle_root(leaves_for(entries, seed)[1]).hex()


# ----------------------------------------------------------- oświadczenie


def statement(index_sha256: str, root_hex: str, count: int) -> bytes:
    return (
        f"{STATEMENT_HEADER}\nindex-sha256 {index_sha256}\nfiles-root {root_hex}\nfiles {count}\n"
    ).encode()


def parse_statement(data: bytes | str) -> dict | None:
    text = data.decode("utf-8") if isinstance(data, bytes) else data
    lines = text.split("\n")
    if len(lines) != 5 or lines[0] != STATEMENT_HEADER or lines[4] != "":
        return None
    try:
        tag_index, index_sha = lines[1].split(" ")
        tag_root, root = lines[2].split(" ")
        tag_files, count = lines[3].split(" ")
        files = int(count)
    except ValueError:
        return None
    if (tag_index, tag_root, tag_files) != ("index-sha256", "files-root", "files"):
        return None
    if not (_is_hex64(index_sha) and _is_hex64(root)) or files < 1 or str(files) != count:
        return None
    return {"index": index_sha, "root": root, "files": files}


def _is_hex64(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


# ------------------------------------------------------- dowód jednego pliku


class FileProofError(Exception):
    """Dowodu dla pliku nie da się wystawić."""


def read_index(folder: Path) -> list[tuple[str, int, str]]:
    """Spis wersji (``.cleanvault-index.txt``) jako krotki (klucz, rozmiar, SHA-256)."""
    from . import proof
    from .i18n import tr
    from .paths import long_path

    raw = Path(long_path(folder / proof.INDEX_NAME)).read_bytes()
    lines = raw.decode("utf-8").split("\n")
    if not lines or lines[0] != proof.INDEX_HEADER:
        raise FileProofError(tr("Nieznany format spisu wersji."))
    entries = []
    for line in lines[1:]:
        if not line:
            continue
        key, size, sha = line.rsplit("\t", 2)
        entries.append((key, int(size), sha))
    return entries


def beatproof_from_receipt(digest: str, receipt: dict, generator: str, file_name: str = "") -> dict:
    """Potwierdzenie Sigelith w formacie ``beatproof-v1`` (te same pola co sigelith.beatproof)."""
    from .sigelith import AUTHORITY, BEATPROOF_FORMAT

    level = receipt.get("level", "")
    return {
        "format": BEATPROOF_FORMAT,
        "generator": generator,
        "authority": AUTHORITY,
        "digest": digest,
        "beat": str(receipt.get("beat") or ""),
        "utc": str(receipt.get("utc") or ""),
        "seq": receipt.get("seq"),
        "week": str(receipt.get("week") or ""),
        "week_closed": bool(receipt.get("week_closed", bool(receipt.get("root_signature")))),
        "week_root": str(receipt.get("week_root") or ""),
        "inclusion_proof": list(receipt.get("inclusion_proof") or []),
        "root_signature": str(receipt.get("root_signature") or ""),
        "public_key": str(receipt.get("public_key") or ""),
        "chain_hash": str(receipt.get("chain_hash") or ""),
        "ots_status": str(receipt.get("ots_status") or "none"),
        "ots_bitcoin_height": receipt.get("ots_height"),
        "anchors": list(receipt.get("anchors") or []),
        "level": level if isinstance(level, str) else str(level),
        "file_name": file_name,
        "note": "",
        "time": dict(receipt.get("time_bounds") or {}),
    }


def build(folder: Path, key: str, *, include_path: bool = True) -> dict:
    """Dowód dla pliku ``key`` z wersji w ``folder`` — wyłącznie z danych w folderze wersji."""
    from . import __app_name__, __version__, proof
    from .i18n import tr
    from .paths import long_path

    seal = proof.read_seal(folder)
    if seal is None or not seal.salt_seed:
        raise FileProofError(tr("Ta wersja nie ma pieczęci dla pojedynczych plików (kopia sprzed wersji 3.0 "
                                "albo bez znaczników czasu)."))
    if seal.status != "signed" or not seal.receipt.get("root_signature"):
        raise FileProofError(tr("Pieczęć tej wersji czeka jeszcze na podpis tygodnia Sigelith — dowód "
                                "będzie gotowy po poniedziałku 00:00 UTC i kolejnej kopii."))
    try:
        text = Path(long_path(folder / proof.STATEMENT_NAME)).read_bytes()
    except OSError as exc:
        raise FileProofError(tr("Brak oświadczenia pieczęci w folderze wersji.")) from exc
    parsed = parse_statement(text)
    if parsed is None or proof.digest_of(text) != seal.digest:
        raise FileProofError(tr("Oświadczenie pieczęci nie zgadza się z pieczęcią wersji."))
    entries = read_index(folder)
    index_bytes = proof.version_index(entries)
    if proof.digest_of(index_bytes) != parsed["index"]:
        raise FileProofError(tr("Spis wersji został zmieniony po oznakowaniu."))
    keys, leaves = leaves_for(entries, bytes.fromhex(seal.salt_seed))
    if merkle_root(leaves).hex() != parsed["root"] or len(leaves) != parsed["files"]:
        raise FileProofError(tr("Drzewo plików wersji nie zgadza się z pieczęcią."))
    try:
        position = keys.index(key)
    except ValueError as exc:
        raise FileProofError(tr("Tego pliku nie ma w spisie tej wersji.")) from exc
    _key, size, sha = sorted(entries)[position]
    generator = f"{__app_name__} {__version__}"
    file_info = {"name": key.rsplit("/", 1)[-1], "size": size, "sha256": sha}
    if include_path:
        file_info["path"] = key
    return {
        "format": FORMAT,
        "generator": generator,
        "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "file": file_info,
        "leaf": {
            "salt": file_salt(bytes.fromhex(seal.salt_seed), key).hex(),
            "path_sha256": path_digest(key).hex(),
        },
        "files_root": parsed["root"],
        "files": parsed["files"],
        "merkle_path": merkle_path(leaves, position),
        "statement": text.decode("utf-8"),
        "beatproof": beatproof_from_receipt(seal.digest, seal.receipt, generator),
        "how_to_verify": HOW_TO_VERIFY,
    }


def problems(doc: dict, file_sha256: str | None = None, file_size: int | None = None) -> list[str]:
    """Sprawdza dowód bez sieci; pusta lista = dowód poprawny.

    ``file_sha256``/``file_size`` — gdy podane, dowód musi dotyczyć właśnie tego pliku.
    """
    from . import sigelith
    from .i18n import tr

    if not isinstance(doc, dict) or doc.get("format") != FORMAT:
        return [tr("To nie jest dowód pliku z kopii Sigelith Backup ({format}).").format(format=FORMAT)]
    found: list[str] = []
    try:
        info, leaf_info = doc["file"], doc["leaf"]
        sha, size = str(info["sha256"]).lower(), int(info["size"])
        salt, path_sha = bytes.fromhex(leaf_info["salt"]), bytes.fromhex(leaf_info["path_sha256"])
        root = str(doc["files_root"]).lower()
        start = leaf(salt, sha, size, path_sha)
        reached = fold(start, doc["merkle_path"]).hex()
    except (KeyError, TypeError, ValueError):
        return [tr("Dowód jest uszkodzony — brakuje pól albo mają zły format.")]
    if file_sha256 is not None and (file_sha256.lower() != sha or (file_size is not None and file_size != size)):
        found.append(tr("Ten plik nie jest plikiem, którego dotyczy dowód."))
    path = info.get("path")
    if path is not None and path_digest(str(path)) != path_sha:
        found.append(tr("Ścieżka pliku w dowodzie nie zgadza się z liściem drzewa."))
    if reached != root:
        found.append(tr("Droga w drzewie plików nie prowadzi do korzenia z pieczęci."))
    statement_text = str(doc.get("statement") or "")
    parsed = parse_statement(statement_text)
    if parsed is None or parsed["root"] != root or parsed["files"] != doc.get("files"):
        found.append(tr("Oświadczenie pieczęci nie potwierdza tego drzewa plików."))
    beatproof = doc.get("beatproof")
    if not isinstance(beatproof, dict) or beatproof.get("digest") != hashlib.sha256(
        statement_text.encode("utf-8")
    ).hexdigest():
        found.append(tr("Potwierdzenie Sigelith nie dotyczy tej pieczęci."))
    else:
        found.extend(sigelith.proof_problems(beatproof))
    return found
