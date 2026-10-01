"""Znakowanie wersji kopii czasem przez Sigelith (sigelith.org, dawniej BeatTime — beattime.live).

Po co: dowód, że kopia **w tym kształcie** istniała danego dnia — np. przy sporze
o autorstwo dokumentu albo gdy trzeba wykazać, że plik nie został podmieniony
po fakcie. Do usługi trafia wyłącznie suma kontrolna (SHA-256) — ani nazwy
plików, ani ich treść nie opuszczają komputera.

Spis wersji to tekst: nagłówek i po jednym wierszu ``ścieżka⇥rozmiar⇥SHA-256``
na plik, posortowany po ścieżce. Leży w folderze wersji (``.cleanvault-index.txt``)
razem z potwierdzeniem (``.cleanvault-seal.json``), więc każdy może po latach
przeliczyć sumy plików, odtworzyć spis i porównać jego skrót ze znacznikiem.

Od 3.0 oznakowany jest nie sam spis, tylko czterowierszowe oświadczenie pieczęci
(``.cleanvault-seal-statement.txt``): suma spisu i korzeń drzewa Merkle'a nad
plikami wersji (fileproof.py). Pieczęć całości działa jak dotąd, a każdy plik
dostaje własny dowód bez ujawniania pozostałych. Pieczęci sprzed 3.0 (skrót
samego spisu, ``tvb-seal/1``) sprawdzamy dalej po staremu.

Jak działa Sigelith (sprawdzone w kodzie serwera): znacznik zapisuje się od razu,
ale **podpis Ed25519 obejmuje korzeń drzewa Merkle'a całego tygodnia** i powstaje
po zamknięciu tygodnia (poniedziałek 00:00 UTC); kotwica w Bitcoinie
(OpenTimestamps) dochodzi jeszcze później. Dlatego potwierdzenie jest
uzupełniane przy kolejnych kopiach, a podpis sprawdzamy kluczem wpisanym na sztywno
w program — klucz podany przez serwer w odpowiedzi niczego by nie dowodził.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

from . import __version__, fileproof
from .i18n import tr
from .log import get_logger
from .paths import long_path

log = get_logger("proof")

#: Usługa BeatTime nazywa się teraz Sigelith. Stary adres beattime.live nadal działa
#: (te same ścieżki API, ten sam klucz podpisu) — sprawdzone 2026-09-29.
BASE_URL = "https://sigelith.org"
SEAL_NAME = ".cleanvault-seal.json"
INDEX_NAME = ".cleanvault-index.txt"
#: Oświadczenie pieczęci (od 3.0): suma spisu + korzeń drzewa plików — to jego skrót trafia
#: do Sigelith, dzięki czemu każdy plik wersji ma własny dowód (fileproof.py).
STATEMENT_NAME = ".cleanvault-seal-statement.txt"
INDEX_HEADER = "TVB-INDEX 1"
_TIMEOUT = 15

#: Klucze, którymi Sigelith podpisuje korzenie tygodni — przepisane z kodu usługi
#: (desktop/beatstamp/keys.py). Klucz z odpowiedzi serwera nie wystarcza: kto
#: podrobiłby odpowiedź, podałby też własny klucz.
PINNED_KEYS: tuple[dict[str, str], ...] = (
    {"public_key": "e7y9THJIUKvNKOZHmdBjJ8E0bOKyBFVxxMpAJ8w574Y=", "active_from": "2026-09-21"},
)


class ProofError(Exception):
    """Znacznika nie udało się zapisać albo sprawdzić."""


# -------------------------------------------------------------------- spis


def version_index(entries: Iterable[tuple[str, int, str]]) -> bytes:
    """Kanoniczny spis wersji: ten sam zestaw plików daje zawsze te same bajty."""
    lines = [INDEX_HEADER]
    for key, size, sha in sorted(entries):
        lines.append(f"{key}\t{size}\t{sha}")
    return ("\n".join(lines) + "\n").encode("utf-8")


def digest_of(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ------------------------------------------------------------------- usługa


class BeatTimeClient:
    """Dwa wywołania publicznego API: zapisanie znacznika i pobranie potwierdzenia."""

    def __init__(self, base_url: str | None = None, timeout: float = _TIMEOUT) -> None:
        # adres czytany przy tworzeniu, nie przy definicji — testy podstawiają własny serwer
        self.base_url = (base_url or BASE_URL).rstrip("/")
        self.timeout = timeout

    def _call(self, method: str, path: str, body: dict | None = None) -> dict:
        data = json.dumps(body).encode("utf-8") if body is not None else None
        request = urllib.request.Request(
            self.base_url + path,
            data=data,
            method=method,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": f"SigelithBackup/{__version__}",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:200]
            raise ProofError(
                tr("Sigelith odrzucił żądanie ({status}): {detail}").format(status=exc.code, detail=detail)
            ) from exc
        except (urllib.error.URLError, OSError, ValueError) as exc:
            raise ProofError(tr("Nie udało się połączyć z Sigelith: {error}").format(error=exc)) from exc

    def stamp(self, digest: str) -> dict:
        return self._call("POST", "/api/proof/stamp", {"digest": digest})

    def verify(self, digest: str) -> dict:
        return self._call("GET", f"/api/proof/verify?digest={digest}")

    def cert_url(self, digest: str) -> str:
        return f"{self.base_url}/api/proof/cert/{digest}"

    def page_url(self, digest: str) -> str:
        return f"{self.base_url}/proof/?h={digest}"


# ---------------------------------------------------------------- pieczęć


@dataclass
class Seal:
    """Potwierdzenie znacznika zapisane w folderze wersji."""

    digest: str
    status: str = "pending"  # pending → stamped → signed (→ ots_status: bitcoin)
    receipt: dict = field(default_factory=dict)
    error: str = ""
    updated: float = 0.0
    #: Od 3.0: losowe ziarno soli liści (hex) i korzeń drzewa plików wersji.
    salt_seed: str = ""
    files_root: str = ""
    files: int = 0

    def to_dict(self) -> dict:
        data = {
            "format": "tvb-seal/2" if self.salt_seed else "tvb-seal/1",
            "service": BASE_URL,
            "digest": self.digest,
            "status": self.status,
            "receipt": self.receipt,
            "error": self.error,
            "updated": self.updated,
        }
        if self.salt_seed:
            data.update(salt_seed=self.salt_seed, files_root=self.files_root, files=self.files)
        return data

    @classmethod
    def from_dict(cls, raw: dict) -> Seal:
        return cls(
            digest=str(raw.get("digest", "")),
            status=str(raw.get("status", "pending")),
            receipt=dict(raw.get("receipt") or {}),
            error=str(raw.get("error", "")),
            updated=float(raw.get("updated", 0.0)),
            salt_seed=str(raw.get("salt_seed", "")),
            files_root=str(raw.get("files_root", "")),
            files=int(raw.get("files", 0) or 0),
        )


def read_seal(folder: Path) -> Seal | None:
    try:
        raw = json.loads(Path(long_path(folder / SEAL_NAME)).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return Seal.from_dict(raw)


def _write(folder: Path, name: str, data: bytes) -> None:
    target = folder / name
    tmp = target.with_name(name + ".tmp")
    with open(long_path(tmp), "wb") as handle:
        handle.write(data)
    os.replace(long_path(tmp), long_path(target))


def seal_version(folder: Path, entries: Iterable[tuple[str, int, str]], client: BeatTimeClient) -> Seal:
    """Zapisuje spis wersji i oświadczenie pieczęci, potem próbuje je oznakować.

    Brak sieci nie jest błędem kopii. Oznakowane jest oświadczenie (suma spisu +
    korzeń drzewa plików), więc wersja ma pieczęć całości i dowód dla każdego pliku.
    """
    entries = sorted(entries)
    index = version_index(entries)
    _write(folder, INDEX_NAME, index)
    seed = os.urandom(32)
    root = fileproof.files_root(entries, seed)
    text = fileproof.statement(digest_of(index), root, len(entries))
    _write(folder, STATEMENT_NAME, text)
    seal = Seal(digest=digest_of(text), salt_seed=seed.hex(), files_root=root, files=len(entries))
    _stamp(seal, client)
    _write(folder, SEAL_NAME, json.dumps(seal.to_dict(), indent=1, ensure_ascii=False).encode("utf-8"))
    return seal


def _stamp(seal: Seal, client: BeatTimeClient) -> None:
    try:
        receipt = client.stamp(seal.digest)
    except ProofError as exc:
        seal.error = str(exc)
        seal.updated = time.time()
        log.info("Znacznik czasu odłożony: %s", exc)
        return
    _apply(seal, receipt)


def _apply(seal: Seal, receipt: dict) -> None:
    if receipt.get("digest") and receipt.get("digest") != seal.digest:
        raise ProofError(tr("Sigelith odesłał potwierdzenie innej sumy kontrolnej."))
    seal.receipt = receipt
    seal.error = ""
    seal.updated = time.time()
    seal.status = "signed" if receipt.get("root_signature") else "stamped"


def refresh(folder: Path, client: BeatTimeClient) -> Seal | None:
    """Uzupełnia potwierdzenie: zapisuje odłożony znacznik albo dociąga podpis tygodnia."""
    seal = read_seal(folder)
    if seal is None:
        return None
    if seal.status == "pending":
        _stamp(seal, client)
    elif seal.status == "stamped" or seal.receipt.get("ots_status") not in (None, "bitcoin"):
        try:
            _apply(seal, client.verify(seal.digest))
        except ProofError as exc:
            seal.error = str(exc)
    else:
        return seal
    _write(folder, SEAL_NAME, json.dumps(seal.to_dict(), indent=1, ensure_ascii=False).encode("utf-8"))
    return seal


# ------------------------------------------------------------- sprawdzenie


@dataclass
class Check:
    """Wynik sprawdzenia pieczęci wersji — każdy punkt osobno, do pokazania człowiekowi."""

    index_matches: bool = False
    stamped: bool = False
    inclusion_ok: bool | None = None
    signature_ok: bool | None = None
    bitcoin: bool = False
    utc: str = ""
    beat: str = ""
    problems: list[str] = field(default_factory=list)

    @property
    def proven(self) -> bool:
        return self.index_matches and self.stamped and self.inclusion_ok is not False and bool(self.signature_ok)


def check(folder: Path, entries: Iterable[tuple[str, int, str]] | None = None) -> Check:
    """Sprawdza pieczęć bez sieci: spis, drogę w drzewie Merkle'a i podpis tygodnia.

    ``entries`` — gdy podane (np. ze spisu treści kopii po sprawdzeniu plików),
    spis wersji jest odtwarzany od nowa i porównywany z oznakowanym.
    """
    result = Check()
    seal = read_seal(folder)
    if seal is None:
        result.problems.append(tr("Ta wersja nie ma znacznika czasu."))
        return result
    try:
        index = Path(long_path(folder / INDEX_NAME)).read_bytes()
    except OSError:
        result.problems.append(tr("Brak spisu wersji, którego dotyczy znacznik."))
        return result
    parsed = None
    if seal.salt_seed:  # od 3.0 oznakowane jest oświadczenie: suma spisu + korzeń drzewa plików
        try:
            text = Path(long_path(folder / STATEMENT_NAME)).read_bytes()
        except OSError:
            text = b""
        parsed = fileproof.parse_statement(text) if text else None
        result.index_matches = (
            parsed is not None and digest_of(text) == seal.digest and parsed["index"] == digest_of(index)
        )
    else:
        result.index_matches = digest_of(index) == seal.digest
    listed = sorted(entries) if entries is not None else None
    if listed is not None and (
        version_index(listed) != index
        or (parsed is not None and fileproof.files_root(listed, bytes.fromhex(seal.salt_seed)) != parsed["root"])
    ):
        result.index_matches = False
        result.problems.append(tr("Pliki wersji różnią się od spisu, który został oznakowany."))
    elif not result.index_matches:
        result.problems.append(tr("Spis wersji został zmieniony po oznakowaniu."))

    receipt = seal.receipt
    result.stamped = seal.status in ("stamped", "signed") and receipt.get("digest") == seal.digest
    result.utc = str(receipt.get("utc", ""))
    result.beat = str(receipt.get("beat", ""))
    if not result.stamped:
        result.problems.append(tr("Znacznik czeka na połączenie z Sigelith."))
        return result

    root = str(receipt.get("week_root") or "")
    proof = receipt.get("inclusion_proof")
    if root and proof is not None:
        result.inclusion_ok = verify_inclusion(seal.digest, proof, root)
        if not result.inclusion_ok:
            result.problems.append(tr("Suma wersji nie należy do drzewa tygodnia podanego w potwierdzeniu."))

    signature = str(receipt.get("root_signature") or "")
    if signature and root:
        result.signature_ok = verify_signature(str(receipt.get("week", "")), root, signature)
        if not result.signature_ok:
            result.problems.append(tr("Podpis tygodnia nie zgadza się z kluczem Sigelith zapisanym w programie."))
    else:
        result.problems.append(tr("Tydzień jeszcze się nie zamknął — podpis pojawi się po poniedziałku 00:00 UTC."))
    result.bitcoin = receipt.get("ots_status") == "bitcoin"
    return result


def verify_inclusion(digest: str, proof: list, root_hex: str) -> bool:
    """Droga od liścia do korzenia: liść = SHA-256(0x00‖suma), węzeł = SHA-256(0x01‖L‖P)."""
    try:
        node = hashlib.sha256(b"\x00" + bytes.fromhex(digest)).digest()
        for step in proof:
            side, sibling_hex = (step["side"], step["hash"]) if isinstance(step, dict) else step
            sibling = bytes.fromhex(sibling_hex)
            pair = sibling + node if side == "L" else node + sibling
            node = hashlib.sha256(b"\x01" + pair).digest()
    except (ValueError, KeyError, TypeError):
        return False
    return node.hex() == root_hex.lower()


def verify_signature(week_key: str, root_hex: str, signature_b64: str) -> bool:
    """Podpis Ed25519 korzenia tygodnia, sprawdzany kluczami wpisanymi w program."""
    from Cryptodome.Signature import eddsa

    message = f"beattime-proof-v1|{week_key}|{root_hex}".encode()
    try:
        signature = base64.b64decode(signature_b64)
    except ValueError:
        return False
    for pinned in PINNED_KEYS:
        try:
            key = eddsa.import_public_key(base64.b64decode(pinned["public_key"]))
            eddsa.new(key, "rfc8032").verify(message, signature)
            return True
        except ValueError:
            continue
    return False
