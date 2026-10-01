"""Przeglądanie kopii bez przywracania: wersje, foldery, historia pliku, wyszukiwanie.

Daje to, po co w innych programach montuje się kopię jako dysk — bez żadnych
wymagań wobec systemu (montowanie przez ProjFS/WinFsp wymagałoby uprawnień
administratora i wypadło z projektu). Foldery są czytane leniwie, po jednym
poziomie, więc otwarcie wersji z milionem plików jest natychmiastowe.

Nazwy pokazujemy bez przyrostków zapisu (``.cvlt``, ``.cvrecipe``) — użytkownik
widzi swoje pliki, a nie sposób, w jaki program je przechowuje.
"""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path

from . import beat, chunks, crypto
from .crypto import ENCRYPTED_SUFFIX, PasswordKeyring
from .engine import _VERSION_NAME, inspect_destination
from .evidence import EVIDENCE_DIR
from .i18n import tr
from .paths import CAPSULES_DIR, long_path
from .rescue import RESCUE_FILES
from .snapshot import Manifest

PLAIN = "plain"
ENCRYPTED = "encrypted"
CHUNKED = "chunked"
CHUNKED_ENCRYPTED = "chunked-encrypted"
_SUFFIXES = (
    (chunks.RECIPE_SUFFIX + ENCRYPTED_SUFFIX, CHUNKED_ENCRYPTED),
    (chunks.RECIPE_SUFFIX, CHUNKED),
    (ENCRYPTED_SUFFIX, ENCRYPTED),
)


@dataclass
class Version:
    name: str  # "" = kopia lustrzana
    label: str
    complete: bool | None


@dataclass
class Item:
    name: str
    key: str  # ścieżka względem wersji, z „/” — jak klucz w spisie treści
    is_dir: bool
    stored: Path | None = None
    kind: str = PLAIN
    size: int | None = None
    mtime: float = 0.0


def versions(root: str | os.PathLike[str]) -> list[Version]:
    """Wersje w katalogu kopii, najnowsze najpierw; kopia lustrzana na końcu."""
    info = inspect_destination(root)
    result = [
        Version(run.name, beat.describe(run.name), run.complete if run.known else None) for run in info.runs
    ]
    base = Path(root)
    if _mirror_folders(base):
        mirror = info.mirror
        result.append(Version("", tr("kopia lustrzana"), mirror.complete if mirror else None))
    return result


def _is_program_file(name: str) -> bool:
    return name.startswith(".cleanvault-") or name in RESCUE_FILES


def _mirror_folders(root: Path) -> list[str]:
    try:
        with os.scandir(long_path(root)) as entries:
            return [
                e.name for e in entries
                if e.is_dir() and not _VERSION_NAME.match(e.name) and not _is_program_file(e.name)
                and e.name not in (EVIDENCE_DIR, CAPSULES_DIR)  # dowody i kapsuły to nie kopia lustrzana
            ]
    except OSError:
        return []


def classify(name: str) -> tuple[str, str]:
    """(nazwa bez przyrostka zapisu, rodzaj zapisu)."""
    for suffix, kind in _SUFFIXES:
        if name.endswith(suffix) and len(name) > len(suffix):
            return name[: -len(suffix)], kind
    return name, PLAIN


def list_folder(root: str | os.PathLike[str], version: str, rel: str = "") -> list[Item]:
    """Jeden poziom folderu wersji: najpierw foldery, potem pliki, alfabetycznie."""
    base = Path(root) / version if version else Path(root)
    folder = base / rel.replace("/", os.sep) if rel else base
    items: list[Item] = []
    try:
        with os.scandir(long_path(folder)) as iterator:
            entries = list(iterator)
    except OSError:
        return []
    at_top = not rel
    for entry in entries:
        if _is_program_file(entry.name) or entry.name.endswith((".part", ".tmp")):
            continue
        if at_top and not version and (_VERSION_NAME.match(entry.name)
                                       or entry.name in (EVIDENCE_DIR, CAPSULES_DIR)):
            continue  # w kopii lustrzanej katalogi wersji, magazyn dowodów i kapsuły to nie są dane
        key = f"{rel}/{entry.name}" if rel else entry.name
        path = Path(folder) / entry.name
        try:
            st = entry.stat()
        except OSError:
            continue
        if entry.is_dir():
            items.append(Item(entry.name, key, True, path, mtime=st.st_mtime))
            continue
        items.append(_stored_item(path, rel, entry.name, st))
    items.sort(key=lambda i: (not i.is_dir, i.name.casefold()))
    return items


def _stored_item(path: Path, rel: str, stored_name: str, st: os.stat_result) -> Item:
    """Plik kopii widziany oczami użytkownika: jego nazwa i rozmiar po odtworzeniu.

    Rozmiar znamy bez hasła wszędzie poza zaszyfrowanym przepisem. Kontener
    rozpoznajemy po zawartości (jedno otwarcie pliku) — plik użytkownika, który
    po prostu kończy się na ``.cvlt``, zostaje zwykłym plikiem.
    """
    name, kind = classify(stored_name)
    size: int | None = None
    if kind == PLAIN:
        size = st.st_size
    elif kind == ENCRYPTED:
        try:
            with open(long_path(path), "rb") as handle:
                if handle.read(len(crypto.MAGIC)) != crypto.MAGIC:
                    name, kind, size = stored_name, PLAIN, st.st_size
                else:
                    handle.seek(0)
                    size = crypto.read_header(handle).plain_size
        except (OSError, crypto.CryptoError):
            size = None
    elif kind == CHUNKED:
        try:
            size = chunks.read_recipe(path, None).size
        except (OSError, crypto.CryptoError):
            size = None
    key = f"{rel}/{name}" if rel else name
    return Item(name, key, False, path, kind, size, st.st_mtime)


@dataclass
class HistoryEntry:
    version: Version
    item: Item
    changed: bool  # treść inna niż w starszej wersji (inny plik na dysku)


def history(root: str | os.PathLike[str], key: str) -> list[HistoryEntry]:
    """W których wersjach jest plik i w których się zmienił — od najnowszej.

    Plik niezmieniony jest w kolejnych wersjach twardym dowiązaniem, więc to ten
    sam plik na dysku: zmiana tożsamości pliku między wersjami = zmiana treści.
    """
    base = Path(root)
    found: list[tuple[Version, Item, tuple[int, int] | None]] = []
    for version in versions(root):
        folder = base / version.name if version.name else base
        for suffix, _kind in (*_SUFFIXES, ("", PLAIN)):
            path = folder / (key.replace("/", os.sep) + suffix)
            try:
                st = os.stat(long_path(path))
            except OSError:
                continue
            rel, _sep, stored_name = f"{key}{suffix}".rpartition("/")
            item = _stored_item(path, rel, stored_name, st)
            if item.key != key:
                continue  # np. zwykły plik „x.cvlt” obok szukanego „x”
            identity = (st.st_dev, st.st_ino) if st.st_ino else None
            found.append((version, item, identity))
            break
    entries: list[HistoryEntry] = []
    for index, (version, item, identity) in enumerate(found):
        older = found[index + 1] if index + 1 < len(found) else None
        changed = older is None or not _same_file(identity, item, older[2], older[1])
        entries.append(HistoryEntry(version, item, changed))
    return entries


def _same_file(identity, item: Item, older_identity, older: Item) -> bool:
    """Czy dwie wersje trzymają tę samą treść pliku.

    Na NTFS niezmieniony plik jest w nowej wersji twardym dowiązaniem — ten sam
    plik na dysku. Gdzie dowiązań nie ma (np. kopia przeniesiona na inny dysk),
    o braku zmiany świadczy ten sam rozmiar i ta sama data modyfikacji.
    """
    if identity is not None and identity == older_identity:
        return True
    return (
        item.kind == older.kind
        and item.size is not None
        and item.size == older.size
        and abs(item.mtime - older.mtime) < 0.001
    )


def search(root: str | os.PathLike[str], text: str, limit: int = 500) -> list[tuple[str, int, float]]:
    """Pliki z aktualnego spisu treści, których ścieżka zawiera szukany tekst."""
    needle = text.strip().casefold()
    if not needle:
        return []
    found: list[tuple[str, int, float]] = []
    for key, entry in Manifest.load(Path(root)).entries.items():
        if needle in key.casefold():
            found.append((key, entry.size, entry.mtime))
            if len(found) >= limit:
                break
    found.sort(key=lambda row: row[0].casefold())
    return found


def locate(root: str | os.PathLike[str], key: str) -> tuple[Version, Item] | None:
    """Najnowsza wersja, w której leży plik o danym kluczu."""
    entries = history(root, key)
    return (entries[0].version, entries[0].item) if entries else None


def seal_folder(root: str | os.PathLike[str], item: Item) -> Path:
    """Folder wersji, której pieczęć obejmuje plik — ten, w którym leży jego zapisana kopia.

    Pieczęć wersji obejmuje pliki zapisane w tej wersji; plik niezmieniony od dawna
    leży (i jest oznakowany) w starszej wersji — to nawet lepiej: wcześniejsza chwila.
    """
    base = Path(root)
    if item.stored is not None:
        try:
            first = Path(item.stored).relative_to(base).parts[0]
        except (ValueError, IndexError):
            first = ""
        if _VERSION_NAME.match(first):
            return base / first
    return base


def extract(root: str | os.PathLike[str], item: Item, target: str | os.PathLike[str],
            keyring: PasswordKeyring | None) -> Path:
    """Odtwarza jeden plik kopii pod wskazaną ścieżką (odszyfrowany i złożony)."""
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    assert item.stored is not None
    if item.kind in (ENCRYPTED, CHUNKED_ENCRYPTED) and keyring is None:
        raise crypto.CryptoError(tr("Kopia jest zaszyfrowana — podaj hasło, aby ją przywrócić."))
    if item.kind in (CHUNKED, CHUNKED_ENCRYPTED):
        recipe = chunks.read_recipe(item.stored, keyring)
        chunks.restore_file(recipe, chunks.ChunkStore(root, keyring), target)
    elif item.kind == ENCRYPTED:
        crypto.decrypt_file(item.stored, target, keyring)  # type: ignore[arg-type]
    else:
        shutil.copyfile(long_path(item.stored), long_path(target))
    os.utime(long_path(target), (item.mtime, item.mtime))
    return target


def needs_password(item: Item) -> bool:
    return item.kind in (ENCRYPTED, CHUNKED_ENCRYPTED)
