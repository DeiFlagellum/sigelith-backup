"""Audyt kopii względem pieczęci w publicznym dzienniku Sigelith (od 3.0).

Po co: spis treści kopii (manifest) leży obok plików. Kto podmieni pliki —
ransomware, włamanie do chmury, psujący się dysk, ktoś z dostępem do nośnika —
może podmienić i spis, a zwykła weryfikacja (verify_backup) porównuje pliki
właśnie z tym spisem. Pieczęć wersji leży w publicznym dzienniku Sigelith,
którego stan potwierdzają niezależni świadkowie (GitHub, Internet Archive,
Zenodo, Bitcoin), a podpis tygodnia sprawdzamy kluczem wpisanym w program —
jej po cichu zmienić się nie da.

Audyt:
1. sprawdza pieczęć wersji bez sieci (proof.check: oświadczenie, spis, droga
   w drzewie tygodnia, podpis) — tylko spis zgodny z pieczęcią jest wzorcem;
2. czyta z nośnika każdy plik tego spisu (albo losową próbkę), liczy SHA-256
   TREŚCI — po odszyfrowaniu z kontrolą tagu GCM i po złożeniu fragmentów —
   i porównuje z sumą oznakowaną w dzienniku.

„Ostatnia nietknięta wersja” to najnowsza wersja, której pieczęć jest
potwierdzona, a wszystkie pliki zgadzają się z oznakowanymi — z niej warto
przywracać, gdy nowsze okazały się podmienione.
"""

from __future__ import annotations

import os
import random
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

from . import chunks, crypto, fileproof, proof
from .crypto import ENCRYPTED_SUFFIX, PasswordKeyring
from .i18n import tr
from .log import get_logger
from .paths import long_path
from .snapshot import hash_file

log = get_logger("audit")

#: Możliwe postaci zapisanego pliku w folderze wersji — ta sama kolejność co w browse.
_STORED_FORMS = (
    ("", "plain"),
    (ENCRYPTED_SUFFIX, "encrypted"),
    (chunks.RECIPE_SUFFIX, "chunked"),
    (chunks.RECIPE_SUFFIX + ENCRYPTED_SUFFIX, "chunked"),
)
#: Próbka audytu automatycznego po kopii planowej: minuty, nie godziny.
SAMPLE_FILES = 24


class AuditNeedsPassword(Exception):
    """Kopia jest zaszyfrowana — audyt treści wymaga hasła."""


@dataclass
class VersionAudit:
    version: str                      # "" = kopia lustrzana
    sealed: bool = False
    seal_proven: bool = False
    seal_problems: list[str] = field(default_factory=list)
    checked: int = 0
    listed: int = 0
    changed: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    unreadable: list[str] = field(default_factory=list)
    cancelled: bool = False
    sampled: bool = False

    @property
    def intact(self) -> bool:
        """Pieczęć potwierdzona i każdy sprawdzony plik zgodny z oznakowanym."""
        return (self.seal_proven and not self.cancelled and self.checked > 0
                and not (self.changed or self.missing or self.unreadable))

    def describe(self) -> str:
        if not self.sealed:
            return tr("Ta wersja nie ma pieczęci — nie ma z czym porównać plików.")
        if not self.seal_proven:
            return tr("Pieczęć wersji się nie potwierdza: {problems}").format(
                problems="; ".join(self.seal_problems) or tr("brak podpisu tygodnia"))
        if self.cancelled:
            return tr("Audyt przerwany.")
        scope = (tr("próbka {checked} z {listed} plików").format(checked=self.checked, listed=self.listed)
                 if self.sampled else tr("wszystkie pliki ({count})").format(count=self.checked))
        if self.intact:
            return tr("Nietknięta: sprawdzono {scope}, wszystko zgodne z pieczęcią w publicznym dzienniku.").format(
                scope=scope)
        parts = []
        if self.changed:
            parts.append(tr("zmienione: {files}").format(files=_names(self.changed)))
        if self.missing:
            parts.append(tr("brakujące: {files}").format(files=_names(self.missing)))
        if self.unreadable:
            parts.append(tr("nieczytelne albo uszkodzone: {files}").format(files=_names(self.unreadable)))
        return tr("PODMIENIONA albo uszkodzona ({scope}) — {details}.").format(
            scope=scope, details="; ".join(parts))


def _names(keys: list[str], limit: int = 5) -> str:
    shown = ", ".join(keys[:limit])
    return shown + (f" (+{len(keys) - limit})" if len(keys) > limit else "")


def version_folder(root: Path, version: str) -> Path:
    return root / version if version else root


def _stored(folder: Path, key: str) -> tuple[Path, str] | None:
    base = folder / key.replace("/", os.sep)
    for suffix, kind in _STORED_FORMS:
        candidate = Path(str(base) + suffix)
        if Path(long_path(candidate)).is_file():
            return candidate, kind
    return None


def _content_digest(path: Path, kind: str, keyring: PasswordKeyring | None,
                    store: chunks.ChunkStore | None, cancel) -> tuple[str, int]:
    if kind == "plain":
        return hash_file(path, cancel=cancel), os.stat(long_path(path)).st_size
    if keyring is None and (kind == "encrypted" or path.name.endswith(ENCRYPTED_SUFFIX)):
        raise AuditNeedsPassword(tr("Kopia jest zaszyfrowana — podaj hasło, aby ją sprawdzić."))
    if kind == "encrypted":
        return crypto.plaintext_sha256(path, keyring, cancel=cancel)  # type: ignore[arg-type]
    recipe = chunks.read_recipe(path, keyring)
    digest = chunks.verify_recipe(recipe, store, cancel=cancel)  # type: ignore[arg-type]
    return digest, sum(length for _cid, length in recipe.chunks)


def audit_version(
    root: str | os.PathLike[str],
    version: str,
    keyring: PasswordKeyring | None,
    reporter,
    sample: int | None = None,
    seed: int | None = None,
) -> VersionAudit:
    """Porównuje pliki wersji z sumami oznakowanymi w publicznym dzienniku."""
    base = Path(root)
    folder = version_folder(base, version)
    result = VersionAudit(version)
    if proof.read_seal(folder) is None:
        return result
    result.sealed = True
    check = proof.check(folder)
    result.seal_problems = list(check.problems)
    result.seal_proven = check.proven
    if not check.index_matches:
        return result  # spis podmieniony: nie ma wzorca, z którym uczciwie porównać pliki
    entries = fileproof.read_index(folder)
    result.listed = len(entries)
    chosen: Iterable[tuple[str, int, str]] = entries
    if sample is not None and sample < len(entries):
        chosen = random.Random(seed).sample(entries, sample)
        result.sampled = True
    store = chunks.ChunkStore(base, keyring) if (base / chunks.CHUNK_DIR).is_dir() else None
    chosen = list(chosen)
    for number, (key, size, sha) in enumerate(chosen, 1):
        if reporter.cancelled:
            result.cancelled = True
            break
        reporter.file(key, number, len(chosen))
        found = _stored(folder, key)
        if found is None:
            result.missing.append(key)
            continue
        path, kind = found
        try:
            digest, actual = _content_digest(path, kind, keyring, store, lambda: reporter.cancelled)
        except AuditNeedsPassword:
            raise
        except crypto.OperationCancelled:
            result.cancelled = True
            break
        except (OSError, crypto.CryptoError, ValueError) as exc:
            log.warning("Audyt: %s nieczytelny: %s", key, exc)
            result.unreadable.append(key)
            continue
        result.checked += 1
        if digest != sha or actual != size:
            result.changed.append(key)
    log.info("Audyt wersji %s: %s", version or "(lustro)", result.describe())
    return result


def sealed_versions(root: str | os.PathLike[str]) -> list[str]:
    """Wersje z pieczęcią, najnowsze najpierw; kopia lustrzana ("") na końcu."""
    from .engine import _version_dirs  # import tutaj: engine importuje ten moduł

    base = Path(root)
    names = [n for n in sorted(_version_dirs(base), reverse=True)
             if (base / n / proof.SEAL_NAME).is_file()]
    if (base / proof.SEAL_NAME).is_file():
        names.append("")
    return names


def last_intact(
    root: str | os.PathLike[str],
    keyring: PasswordKeyring | None,
    reporter,
) -> tuple[list[VersionAudit], str | None]:
    """Audytuje wersje od najnowszej, aż trafi na nietkniętą. Zwraca raporty i jej nazwę."""
    audits: list[VersionAudit] = []
    for version in sealed_versions(root):
        audit = audit_version(root, version, keyring, reporter)
        audits.append(audit)
        if audit.cancelled:
            return audits, None
        if audit.intact:
            return audits, version
    return audits, None
