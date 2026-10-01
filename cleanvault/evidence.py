"""Magazyn dowodów Sigelith w katalogu kopii: dokładne bajty oznakowanych dokumentów.

Stempel Sigelith zawiera tylko sumę SHA-256 dokumentu. Wystarczy, że ktoś otworzy
i zapisze umowę, a dowód przestaje do niej pasować; wystarczy, że historia Sigelith
dojdzie do sufitu, a najstarsze dowody z niej znikną. Magazyn trzyma więc po jednym
folderze na stempel — dokument zweryfikowany sumą i plik ``.beatproof`` — obok wersji
kopii, a nie w nich: sprzątanie wersji (retencja) nigdy go nie dotyka.

Układ::

    <katalog kopii>/Sigelith Evidence/
        2026-09-27 Umowa najmu.pdf [3fa9c1d2e4b5a6f7]/
            Umowa najmu.pdf
            Umowa najmu.pdf.beatproof

W kopii szyfrowanej dokument i dowód leżą jako kontenery ``.cvlt`` — ten sam format
co reszta kopii (nazwy plików są widoczne, treść nie).

Skąd bajty: z oryginału, jeśli jego suma wciąż się zgadza; jeśli dokument zmienił
się po stemplu — ze starszych wersji tej kopii (ta sama ścieżka albo ten sam plik
pod inną nazwą). Dowód bez dokumentu też trafia do magazynu, a dokument dochodzi,
gdy tylko się znajdzie.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from . import crypto, sigelith
from .crypto import ENCRYPTED_SUFFIX, PasswordKeyring
from .i18n import plural, tr
from .log import get_logger
from .paths import long_path

log = get_logger("evidence")

EVIDENCE_DIR = "Sigelith Evidence"
_STAGING = ".cleanvault-staging"
_FOLDER = re.compile(r"\[([0-9a-f]{16})\]$")
_UNSAFE = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_CHUNK = 1024 * 1024

#: Pliki folderu danych Sigelith, których nie kopiujemy (ustalone z projektem beattime):
#: dzienniki i blokada są otwarte przez działający program, ``witness/log.jsonl`` to
#: dopisywana na bieżąco kopia publicznego dziennika (da się ją pobrać od nowa),
#: ``.proba-zapisu`` to próba zapisu. Wzorce liczą się od katalogu głównego źródła.
SIGELITH_EXCLUDES = (
    "sigelith.log",
    "sigelith.log.*",
    "sigelith-crash.log",
    "beatstamp.lock",
    ".proba-zapisu",
    "witness/log.jsonl",
)


@dataclass
class Summary:
    stamps: int = 0
    protected: int = 0  # dokument już był w magazynie
    added: list[str] = field(default_factory=list)  # nazwy dokumentów wziętych z oryginału
    recovered: list[str] = field(default_factory=list)  # odtworzonych ze starszych wersji kopii
    missing: list[str] = field(default_factory=list)  # dowód jest, dokumentu nie ma nigdzie
    pending: int = 0  # tydzień stempla jeszcze niepodpisany
    proofs_completed: int = 0

    @property
    def documents(self) -> int:
        return self.protected + len(self.added) + len(self.recovered)

    def describe(self) -> str:
        text = tr("Dowody Sigelith: zabezpieczone dokumenty {count} z {total}").format(
            count=self.documents, total=self.stamps)
        details = []
        if self.added:
            details.append(tr("nowe: {count}").format(count=len(self.added)))
        if self.recovered:
            details.append(tr("odtworzone ze starszych wersji kopii: {count}").format(count=len(self.recovered)))
        if self.proofs_completed:
            details.append(tr("dowody uzupełnione o podpis tygodnia: {count}").format(count=self.proofs_completed))
        if self.pending:
            details.append(tr("czekają na podpis tygodnia: {count}").format(count=self.pending))
        if details:
            text += " (" + ", ".join(details) + ")"
        text += "."
        if self.missing:
            names = ", ".join(self.missing[:5]) + (" …" if len(self.missing) > 5 else "")
            text += " " + tr(
                "Bez dokumentu: {count} {stamps} — plik zmienił się po stemplu albo zniknął i nie ma "
                "go w żadnej wersji tej kopii ({names}). Sam dowód jest zachowany."
            ).format(count=len(self.missing), stamps=plural(len(self.missing), "stempel", "stemple", "stempli"),
                     names=names)
        return text


@dataclass
class Item:
    """Jeden folder magazynu: dowód i — jeśli jest — dokument."""

    folder: Path
    digest16: str
    date: str
    document: Path | None
    proof_file: Path | None

    @property
    def encrypted(self) -> bool:
        return any(p is not None and p.name.endswith(ENCRYPTED_SUFFIX) for p in (self.document, self.proof_file))

    @property
    def name(self) -> str:
        """Nazwa dokumentu (w kopii szyfrowanej — z pliku dowodu, po odszyfrowaniu)."""
        source = self.document or self.proof_file
        if source is None:
            return ""
        name = source.name
        for suffix in (ENCRYPTED_SUFFIX, sigelith.BEATPROOF_SUFFIX):
            name = name[: -len(suffix)] if name.endswith(suffix) else name
        return name


# ------------------------------------------------------------------ zabezpieczanie


def protect(
    destination: str | os.PathLike[str],
    stamps: list[sigelith.Stamp],
    roots: list,
    keyring: PasswordKeyring | None,
    reporter=None,
) -> Summary:
    """Dokłada do magazynu dowody i dokumenty, których w nim jeszcze nie ma.

    ``keyring`` różny od ``None`` = kopia szyfrowana: nowe foldery dostają kontenery.
    """
    destination = Path(destination)
    vault = destination / EVIDENCE_DIR
    summary = Summary(stamps=len(stamps))
    if not stamps:
        return summary
    existing = {item.digest16: item for item in list_items(destination)}
    staging = vault / _STAGING
    shutil.rmtree(long_path(staging), ignore_errors=True)
    manifest_index: dict[str, list[str]] | None = None
    try:
        for stamp in stamps:
            if reporter is not None:
                reporter.check_cancel()
            item = existing.get(stamp.digest[:16])
            first_time = item is None
            if item is None:
                folder = vault / _folder_name(stamp)
                folder.mkdir(parents=True, exist_ok=True)
                _write_proof(folder, stamp, keyring)
                item = Item(folder, stamp.digest[:16], stamp.date, None, _find_proof(folder))
            elif _refresh_proof(item, stamp, keyring):
                summary.proofs_completed += 1
            if not stamp.complete:
                summary.pending += 1
            if item.document is not None:
                summary.protected += 1
                continue
            label = stamp.file_name or stamp.digest[:16]
            staged = _from_original(stamp, staging)
            if staged is not None:
                _store_document(item.folder, stamp, staged, keyring)
                summary.added.append(label)
                continue
            if first_time and manifest_index is None:
                manifest_index = _manifest_index(destination)
            staged = _from_backups(destination, stamp, roots, keyring, staging,
                                   manifest_index.get(stamp.digest, []) if first_time and manifest_index else [])
            if staged is not None:
                _store_document(item.folder, stamp, staged, keyring)
                summary.recovered.append(label)
            else:
                summary.missing.append(label)
    finally:
        shutil.rmtree(long_path(staging), ignore_errors=True)
    return summary


def _safe_name(name: str) -> str:
    cleaned = _UNSAFE.sub("_", Path(name).name).strip(" .")
    return cleaned[:120] or "dokument"


def _folder_name(stamp: sigelith.Stamp) -> str:
    # Nazwa dokumentu jest widoczna jak w całej kopii (także szyfrowanej: „nazwa.cvlt”);
    # treść dowodu — z notatką — w kopii szyfrowanej leży w kontenerze.
    return f"{stamp.date or '0000-00-00'} {_safe_name(stamp.file_name)} [{stamp.digest[:16]}]"


def _write_atomic(path: Path, data: bytes) -> None:
    tmp = path.with_name(path.name + ".part")
    with open(long_path(tmp), "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(long_path(tmp), long_path(path))


def _write_proof(folder: Path, stamp: sigelith.Stamp, keyring: PasswordKeyring | None,
                 encrypted: bool | None = None) -> None:
    data = json.dumps(sigelith.beatproof(stamp), indent=2, ensure_ascii=False).encode("utf-8")
    name = _safe_name(stamp.file_name) + sigelith.BEATPROOF_SUFFIX
    encrypt = keyring is not None if encrypted is None else encrypted
    if encrypt:
        _write_atomic(folder / (name + ENCRYPTED_SUFFIX), crypto.encrypt_bytes(data, keyring))
    else:
        _write_atomic(folder / name, data)


def _find_proof(folder: Path) -> Path | None:
    for path in sorted(folder.iterdir()):
        if path.name.endswith((sigelith.BEATPROOF_SUFFIX, sigelith.BEATPROOF_SUFFIX + ENCRYPTED_SUFFIX)):
            return path
    return None


def read_proof(item: Item, keyring: PasswordKeyring | None) -> dict | None:
    """Treść ``.beatproof``; ``None`` — brak pliku albo zaszyfrowany bez hasła."""
    if item.proof_file is None:
        return None
    raw = Path(long_path(item.proof_file)).read_bytes()
    if item.proof_file.name.endswith(ENCRYPTED_SUFFIX):
        if keyring is None:
            return None
        raw = crypto.decrypt_bytes(raw, keyring)
    return json.loads(raw.decode("utf-8"))


def _refresh_proof(item: Item, stamp: sigelith.Stamp, keyring: PasswordKeyring | None) -> bool:
    """Dowód zapisany przed zamknięciem tygodnia dostaje podpis, gdy Sigelith już go ma."""
    if not stamp.complete or item.proof_file is None:
        return False
    encrypted = item.proof_file.name.endswith(ENCRYPTED_SUFFIX)
    if encrypted and keyring is None:
        return False  # kopia była szyfrowana, a ten przebieg nie zna hasła — następnym razem
    try:
        current = read_proof(item, keyring)
    except (OSError, ValueError, crypto.CryptoError) as exc:
        log.warning("Nie da się odczytać dowodu %s: %s", item.proof_file, exc)
        return False
    if current and current.get("week_closed") and current.get("root_signature"):
        return False
    _write_proof(item.folder, stamp, keyring, encrypted=encrypted)
    return True


def _copy_verified(source: Path, staging: Path, digest: str, open_source=None) -> Path | None:
    """Kopiuje plik do strefy roboczej, licząc sumę w tym samym przebiegu; zła suma = ``None``."""
    staging.mkdir(parents=True, exist_ok=True)
    target = staging / f"{digest[:16]}.part"
    hasher = hashlib.sha256()
    try:
        with open(long_path(source), "rb") as src, open(long_path(target), "wb") as dst:
            while block := src.read(_CHUNK):
                hasher.update(block)
                dst.write(block)
    except OSError as exc:
        log.info("Nie da się odczytać %s: %s", source, exc)
        with contextlib.suppress(OSError):
            os.unlink(long_path(target))
        return None
    if hasher.hexdigest() != digest:
        os.unlink(long_path(target))
        return None
    with contextlib.suppress(OSError):
        mtime = os.stat(long_path(source)).st_mtime
        os.utime(long_path(target), (mtime, mtime))
    return target


def _from_original(stamp: sigelith.Stamp, staging: Path) -> Path | None:
    if not stamp.file_path:
        return None
    path = Path(stamp.file_path)
    try:
        st = os.stat(long_path(path))
    except OSError:
        return None
    if not os.path.isfile(long_path(path)) or (stamp.file_size and st.st_size != stamp.file_size):
        return None
    return _copy_verified(path, staging, stamp.digest)


def _manifest_index(destination: Path) -> dict[str, list[str]]:
    """Suma → klucze plików w spisie treści kopii (stan najnowszy)."""
    from .snapshot import Manifest

    index: dict[str, list[str]] = {}
    try:
        manifest = Manifest.load(destination)
    except (OSError, ValueError) as exc:
        log.warning("Nie da się wczytać spisu treści %s: %s", destination, exc)
        return index
    for key, entry in manifest.entries.items():
        if entry.sha256:
            index.setdefault(entry.sha256, []).append(key)
    return index


def _keys_for_path(file_path: str, roots: list) -> list[str]:
    if not file_path:
        return []
    path = Path(file_path)
    keys = []
    for root in roots:
        try:
            rel = path.relative_to(root.path)
        except ValueError:
            continue
        keys.append(f"{root.label}/{rel.as_posix()}")
    return keys


def _from_backups(destination: Path, stamp: sigelith.Stamp, roots: list, keyring: PasswordKeyring | None,
                  staging: Path, same_content_keys: list[str]) -> Path | None:
    """Szuka dokładnych bajtów dokumentu w wersjach tej kopii (od najnowszej)."""
    from . import browse

    for key in dict.fromkeys(_keys_for_path(stamp.file_path, roots) + same_content_keys):
        for row in browse.history(destination, key):
            item = row.item
            if item.size is not None and stamp.file_size and item.size != stamp.file_size:
                continue
            if browse.needs_password(item) and keyring is None:
                continue
            staging.mkdir(parents=True, exist_ok=True)
            candidate = staging / f"{stamp.digest[:16]}.candidate"
            try:
                browse.extract(destination, item, candidate, keyring)
            except (OSError, crypto.CryptoError) as exc:
                log.info("Nie da się odtworzyć %s z %s: %s", key, row.version.name, exc)
                continue
            found = _copy_verified(candidate, staging, stamp.digest)
            with contextlib.suppress(OSError):
                os.unlink(long_path(candidate))
            if found is not None:
                return found
    return None


def _store_document(folder: Path, stamp: sigelith.Stamp, staged: Path, keyring: PasswordKeyring | None) -> None:
    name = _safe_name(stamp.file_name)
    if keyring is not None:
        crypto.encrypt_file(staged, folder / (name + ENCRYPTED_SUFFIX), keyring)
        os.unlink(long_path(staged))
    else:
        os.replace(long_path(staged), long_path(folder / name))


# ------------------------------------------------------------ przeglądanie i odzysk


def list_items(destination: str | os.PathLike[str]) -> list[Item]:
    """Foldery magazynu, od najnowszego stempla."""
    vault = Path(destination) / EVIDENCE_DIR
    try:
        folders = [p for p in vault.iterdir() if p.is_dir() and _FOLDER.search(p.name)]
    except OSError:
        return []
    items = []
    for folder in folders:
        digest16 = _FOLDER.search(folder.name).group(1)
        proof_file, document = None, None
        for path in sorted(folder.iterdir()):
            if path.name.endswith((".part", ".tmp")):
                continue
            if path.name.endswith((sigelith.BEATPROOF_SUFFIX, sigelith.BEATPROOF_SUFFIX + ENCRYPTED_SUFFIX)):
                proof_file = path
            elif path.is_file():
                document = path
        items.append(Item(folder, digest16, folder.name[:10], document, proof_file))
    items.sort(key=lambda item: (item.date, item.folder.name), reverse=True)
    return items


def has_vault(destination: str | os.PathLike[str]) -> bool:
    return bool(list_items(destination))


def _document_digest(item: Item, keyring: PasswordKeyring | None) -> str:
    hasher = hashlib.sha256()
    if item.document.name.endswith(ENCRYPTED_SUFFIX) and crypto.is_encrypted_file(item.document):
        if keyring is None:
            raise crypto.CryptoError(tr("Kopia jest zaszyfrowana — podaj hasło, aby ją przywrócić."))
        tmp = item.folder / (item.document.name + ".check")
        try:
            crypto.decrypt_file(item.document, tmp, keyring)
            with open(long_path(tmp), "rb") as handle:
                while block := handle.read(_CHUNK):
                    hasher.update(block)
        finally:
            with contextlib.suppress(OSError):
                os.unlink(long_path(tmp))
    else:
        with open(long_path(item.document), "rb") as handle:
            while block := handle.read(_CHUNK):
                hasher.update(block)
    return hasher.hexdigest()


def verify_item(item: Item, keyring: PasswordKeyring | None) -> list[str]:
    """Problemy z dowodem i dokumentem; pusta lista = dowód pasuje do dokumentu i jest podpisany."""
    data = read_proof(item, keyring)
    if data is None:
        return [tr("Brak pliku dowodu albo dowód jest zaszyfrowany.")]
    problems = sigelith.proof_problems(data)
    if item.document is None:
        problems.append(tr("W magazynie nie ma dokumentu do tego dowodu."))
    elif _document_digest(item, keyring) != data.get("digest"):
        problems.append(tr("Suma dokumentu nie zgadza się z dowodem."))
    return problems


def restore_item(item: Item, target: str | os.PathLike[str], keyring: PasswordKeyring | None) -> list[Path]:
    """Odtwarza dokument i jego ``.beatproof`` (jawne) do wskazanego folderu."""
    target = Path(target)
    target.mkdir(parents=True, exist_ok=True)
    written = []
    for path in (item.document, item.proof_file):
        if path is None:
            continue
        name = path.name[: -len(ENCRYPTED_SUFFIX)] if path.name.endswith(ENCRYPTED_SUFFIX) else path.name
        out = target / name
        if path.name.endswith(ENCRYPTED_SUFFIX) and crypto.is_encrypted_file(path):
            if keyring is None:
                raise crypto.CryptoError(tr("Kopia jest zaszyfrowana — podaj hasło, aby ją przywrócić."))
            crypto.decrypt_file(path, out, keyring)
        else:
            shutil.copy2(long_path(path), long_path(out))
        written.append(out)
    return written
