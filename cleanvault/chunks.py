"""Zapis różnicowy dużych plików — fragmenty wyznaczane treścią (FastCDC).

Dlaczego: 117 plików większych niż 256 MB to u użytkownika 57% bajtów kopii.
Zmiana jednego bajtu w maszynie wirtualnej albo skrzynce PST kopiowała dotąd
cały plik do nowej wersji. Teraz duży plik trafia do kopii jako mały **przepis**
(lista fragmentów), a treść — do wspólnego **magazynu fragmentów**. Nowa wersja
zmienionego pliku zapisuje tylko fragmenty, których w magazynie jeszcze nie ma.

Granice fragmentów wyznacza treść (FastCDC), a nie stały rozmiar: wstawienie
kilku bajtów w środek pliku przesuwa dalszą treść, ale nie zmienia jej
podziału, więc wszystkie dalsze fragmenty pozostają rozpoznawalne.

Układ na nośniku (opisany też w notatce ratunkowej i w ``odzyskaj.py``)::

    .cleanvault-chunks/config.json          sól identyfikatorów (kopia szyfrowana)
    .cleanvault-chunks/ab/cd/abcd…          fragment (``.cvlt`` przy szyfrowaniu)
    .cleanvault-chunks/versions/<wersja>.list  przepisy danej wersji (do sprzątania)
    <wersja>/<źródło>/<ścieżka>.cvrecipe    przepis (``.cvrecipe.cvlt`` przy szyfrowaniu)

Przepis to ``CVRECIPE 1`` w pierwszym wierszu i JSON: rozmiar, SHA-256 całości
i lista ``[identyfikator, długość]``. Identyfikator fragmentu to SHA-256 jego
treści; w kopii szyfrowanej — HMAC-SHA256 z kluczem z hasła, żeby nazwy plików
nie zdradzały, jakie znane treści są w kopii.
"""

from __future__ import annotations

import contextlib
import hashlib
import hmac
import json
import os
import threading
import uuid
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass, field
from pathlib import Path

from . import crypto
from .crypto import ENCRYPTED_SUFFIX, KdfParams, PasswordKeyring
from .i18n import tr
from .log import get_logger
from .paths import long_path

log = get_logger("chunks")

CHUNK_DIR = ".cleanvault-chunks"
RECIPE_SUFFIX = ".cvrecipe"
RECIPE_HEADER = b"CVRECIPE 1\n"
RECIPE_FORMAT = "cvrecipe/1"
#: Pliki od tej wielkości idą do magazynu fragmentów. Mniejsze kopiujemy w całości:
#: każdy fragment to osobny plik na nośniku, a dla małych plików zysk jest znikomy.
DELTA_MIN_SIZE = 256 * 1024 * 1024
MIN_CHUNK = 512 * 1024
AVG_CHUNK = 2 * 1024 * 1024
MAX_CHUNK = 8 * 1024 * 1024
#: Plik czytamy zwykłym odczytem w oknach tej wielkości — mapowanie całego pliku
#: w pamięć (mmap) wywracało proces, gdy inny program zmieniał plik w trakcie.
WINDOW = 64 * 1024 * 1024
_CONFIG = "config.json"
_LISTS = "versions"
_ID_CONTEXT = b"cleanvault chunk id"

try:  # skompilowany FastCDC; bez niego zapis różnicowy się po prostu wyłącza
    from fastcdc.fastcdc_cy import fastcdc_cy as _fastcdc

    AVAILABLE = True
except ImportError:  # pragma: no cover - zależne od instalacji
    _fastcdc = None
    AVAILABLE = False
    log.warning("Brak skompilowanego FastCDC — duże pliki będą kopiowane w całości.")


class ChunkError(crypto.CryptoError):
    """Przepis albo fragment jest uszkodzony lub nie pasuje do hasła."""


def iter_chunks(handle, cancel: Callable[[], bool] | None = None) -> Iterator[bytes]:
    """Fragmenty strumienia w granicach wyznaczonych przez treść.

    Okno kończy się zwykle w środku fragmentu, więc ostatni fragment okna
    odkładamy i dzielimy od nowa razem z dalszą treścią. FastCDC zaczyna liczyć
    od zera na początku każdego fragmentu, więc granice wychodzą dokładnie takie
    same, jakby cały plik podzielić naraz.
    """
    pending = bytearray()
    eof = False
    while True:
        while not eof and len(pending) < WINDOW:
            block = handle.read(WINDOW)
            if not block:
                eof = True
                break
            pending += block
        if not pending:
            return
        data = bytes(pending)
        cuts = list(_fastcdc(data, MIN_CHUNK, AVG_CHUNK, MAX_CHUNK))
        emit = cuts if eof or len(cuts) == 1 else cuts[:-1]
        consumed = 0
        for cut in emit:
            yield data[cut.offset : cut.offset + cut.length]
            consumed = cut.offset + cut.length
        del pending[:consumed]
        if cancel is not None and cancel():
            raise crypto.OperationCancelled(tr("Operacja przerwana przez użytkownika."))
        if eof and not pending:
            return


@dataclass
class Recipe:
    """Przepis na odtworzenie dużego pliku z fragmentów."""

    size: int
    sha256: str
    chunks: list[tuple[str, int]] = field(default_factory=list)

    def to_bytes(self) -> bytes:
        body = {
            "format": RECIPE_FORMAT,
            "size": self.size,
            "sha256": self.sha256,
            "chunks": [[cid, length] for cid, length in self.chunks],
        }
        return RECIPE_HEADER + json.dumps(body, separators=(",", ":")).encode("utf-8")

    @classmethod
    def from_bytes(cls, data: bytes) -> Recipe:
        if not data.startswith(RECIPE_HEADER):
            raise ChunkError(tr("To nie jest przepis pliku zapisanego fragmentami."))
        try:
            body = json.loads(data[len(RECIPE_HEADER) :].decode("utf-8"))
            chunks = [(str(cid), int(length)) for cid, length in body["chunks"]]
            recipe = cls(size=int(body["size"]), sha256=str(body["sha256"]), chunks=chunks)
        except (ValueError, KeyError, TypeError) as exc:
            raise ChunkError(tr("Przepis pliku jest uszkodzony.")) from exc
        if sum(length for _cid, length in recipe.chunks) != recipe.size:
            raise ChunkError(tr("Przepis pliku jest uszkodzony."))
        return recipe

    @property
    def ids(self) -> set[str]:
        return {cid for cid, _length in self.chunks}


class ChunkStore:
    """Magazyn fragmentów jednego katalogu kopii."""

    def __init__(
        self, root: str | os.PathLike[str], keyring: PasswordKeyring | None, create: bool = False
    ) -> None:
        self.root = Path(root)
        self.dir = self.root / CHUNK_DIR
        self.keyring = keyring
        self._create = create
        self._known: set[str] = set()
        self._lock = threading.Lock()
        self._id_key: bytes | None = self._load_id_key() if keyring is not None else None

    @property
    def encrypted(self) -> bool:
        return self.keyring is not None

    # ------------------------------------------------------------ identyfikatory

    def _load_id_key(self) -> bytes:
        """Klucz identyfikatorów: stały dla katalogu kopii, wyprowadzony z hasła.

        Sól leży w ``config.json`` — bez stałej soli ten sam fragment dostawałby
        przy każdej kopii inną nazwę i nic by się nie deduplikowało. Obok soli
        leży wartość kontrolna, żeby inne hasło wykryć od razu, a nie po cichu
        zacząć drugi, równoległy zestaw fragmentów.
        """
        config_path = self.dir / _CONFIG
        assert self.keyring is not None
        if Path(long_path(config_path)).exists():
            try:
                raw = json.loads(Path(long_path(config_path)).read_text(encoding="utf-8"))
                params = KdfParams(
                    int(raw["kdf"]), bytes.fromhex(raw["salt"]), int(raw["a"]), int(raw["b"]), int(raw["c"])
                )
                check = str(raw["check"])
            except (OSError, ValueError, KeyError) as exc:
                raise ChunkError(tr("Opis magazynu fragmentów jest uszkodzony.")) from exc
            key = self._derive(params)
            if not hmac.compare_digest(self._check_value(key), check):
                raise ChunkError(
                    tr("Podane hasło nie pasuje do fragmentów zapisanych wcześniej w tej kopii.")
                )
            return key
        if not self._create:
            # Przywracanie i sprawdzanie tylko czytają — bez opisu magazynu nie da
            # się wyliczyć nazw fragmentów, a nowy opis dałby nazwy niepasujące.
            raise ChunkError(tr("Brak opisu magazynu fragmentów w katalogu kopii."))
        session = self.keyring.session_params
        params = KdfParams(session.kdf_id, os.urandom(16), session.a, session.b, session.c)
        key = self._derive(params)
        config = {
            "format": 1,
            "kdf": params.kdf_id,
            "salt": params.salt.hex(),
            "a": params.a,
            "b": params.b,
            "c": params.c,
            "check": self._check_value(key),
        }
        self.dir.mkdir(parents=True, exist_ok=True)
        _write_atomic(config_path, json.dumps(config, indent=1).encode("utf-8"))
        return key

    def _derive(self, params: KdfParams) -> bytes:
        assert self.keyring is not None
        return hmac.new(self.keyring.key_for(params), _ID_CONTEXT, hashlib.sha256).digest()

    @staticmethod
    def _check_value(key: bytes) -> str:
        return hmac.new(key, b"check", hashlib.sha256).hexdigest()

    def chunk_id(self, data: bytes) -> str:
        if self._id_key is None:
            return hashlib.sha256(data).hexdigest()
        return hmac.new(self._id_key, data, hashlib.sha256).hexdigest()

    # ------------------------------------------------------------------ zapis

    def path_for(self, cid: str) -> Path:
        name = cid + (ENCRYPTED_SUFFIX if self.encrypted else "")
        return self.dir / cid[:2] / cid[2:4] / name

    def has(self, cid: str) -> bool:
        with self._lock:
            if cid in self._known:
                return True
        present = Path(long_path(self.path_for(cid))).exists()
        if present:
            with self._lock:
                self._known.add(cid)
        return present

    def put(self, cid: str, data: bytes) -> int:
        """Zapisuje fragment, jeśli go jeszcze nie ma. Zwraca liczbę zapisanych bajtów."""
        if self.has(cid):
            return 0
        payload = crypto.encrypt_bytes(data, self.keyring) if self.keyring is not None else data
        target = self.path_for(cid)
        target.parent.mkdir(parents=True, exist_ok=True)
        _write_atomic(target, payload)
        with self._lock:
            self._known.add(cid)
        return len(payload)

    def get(self, cid: str) -> bytes:
        """Treść fragmentu — sprawdzona: identyfikator musi się zgadzać z treścią."""
        try:
            payload = Path(long_path(self.path_for(cid))).read_bytes()
        except FileNotFoundError as exc:
            raise ChunkError(tr("Brak fragmentu {cid} w magazynie kopii.").format(cid=cid[:16])) from exc
        data = crypto.decrypt_bytes(payload, self.keyring) if self.keyring is not None else payload
        if not hmac.compare_digest(self.chunk_id(data), cid):
            raise ChunkError(tr("Fragment {cid} jest uszkodzony.").format(cid=cid[:16]))
        return data

    def all_ids(self) -> Iterator[tuple[str, Path]]:
        if not Path(long_path(self.dir)).is_dir():
            return
        suffix = ENCRYPTED_SUFFIX if self.encrypted else ""
        for first in _subdirs(self.dir):
            for second in _subdirs(first):
                with os.scandir(long_path(second)) as entries:
                    names = [e.name for e in entries if e.is_file()]
                for name in names:
                    if name.endswith(suffix) and not name.endswith(".tmp"):
                        cid = name[: len(name) - len(suffix)] if suffix else name
                        yield cid, Path(second) / name


_HEX = set("0123456789abcdef")


def _subdirs(folder: Path) -> Iterable[Path]:
    """Katalogi rozkładu fragmentów: dokładnie dwa znaki szesnastkowe."""
    with os.scandir(long_path(folder)) as entries:
        return [
            Path(folder) / entry.name
            for entry in entries
            if entry.is_dir() and len(entry.name) == 2 and set(entry.name) <= _HEX
        ]


def _write_atomic(path: Path, data: bytes) -> None:
    tmp = path.with_name(f"{path.name}.{uuid.uuid4().hex[:8]}.tmp")
    try:
        with open(long_path(tmp), "wb") as handle:
            handle.write(data)
        os.replace(long_path(tmp), long_path(path))
    except BaseException:
        with contextlib.suppress(OSError):
            os.remove(long_path(tmp))
        raise


# ---------------------------------------------------------------- pliki


def store_file(
    source: str | os.PathLike[str],
    store: ChunkStore,
    progress: Callable[[int], None] | None = None,
    cancel: Callable[[], bool] | None = None,
) -> tuple[Recipe, int]:
    """Dzieli plik na fragmenty i zapisuje brakujące. Zwraca przepis i bajty zapisane."""
    digest = hashlib.sha256()
    chunks: list[tuple[str, int]] = []
    written = 0
    size = 0
    with open(long_path(source), "rb") as handle:
        for data in iter_chunks(handle, cancel):
            digest.update(data)
            cid = store.chunk_id(data)
            written += store.put(cid, data)
            chunks.append((cid, len(data)))
            size += len(data)
            if progress is not None:
                progress(len(data))
    return Recipe(size=size, sha256=digest.hexdigest(), chunks=chunks), written


def write_recipe(path: str | os.PathLike[str], recipe: Recipe, keyring: PasswordKeyring | None) -> int:
    payload = recipe.to_bytes()
    if keyring is not None:
        payload = crypto.encrypt_bytes(payload, keyring)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    _write_atomic(Path(path), payload)
    return len(payload)


def read_recipe(path: str | os.PathLike[str], keyring: PasswordKeyring | None) -> Recipe:
    payload = Path(long_path(path)).read_bytes()
    if payload.startswith(crypto.MAGIC):
        if keyring is None:
            raise ChunkError(tr("Kopia jest zaszyfrowana — podaj hasło, aby ją przywrócić."))
        payload = crypto.decrypt_bytes(payload, keyring)
    return Recipe.from_bytes(payload)


def restore_file(
    recipe: Recipe,
    store: ChunkStore,
    target: str | os.PathLike[str],
    progress: Callable[[int], None] | None = None,
    cancel: Callable[[], bool] | None = None,
) -> int:
    """Składa plik z fragmentów; wynik trafia pod docelową nazwę dopiero po sprawdzeniu."""
    target = Path(target)
    tmp = target.with_name(target.name + ".part")
    digest = hashlib.sha256()
    written = 0
    try:
        with open(long_path(tmp), "wb") as out:
            for cid, length in recipe.chunks:
                if cancel is not None and cancel():
                    raise crypto.OperationCancelled(tr("Operacja przerwana przez użytkownika."))
                data = store.get(cid)
                if len(data) != length:
                    raise ChunkError(tr("Fragment {cid} jest uszkodzony.").format(cid=cid[:16]))
                out.write(data)
                digest.update(data)
                written += length
                if progress is not None:
                    progress(length)
        if written != recipe.size or digest.hexdigest() != recipe.sha256:
            raise ChunkError(tr("Plik złożony z fragmentów różni się od zapisanego w przepisie."))
        os.replace(long_path(tmp), long_path(target))
    except BaseException:
        with contextlib.suppress(OSError):
            os.remove(long_path(tmp))
        raise
    return written


def verify_recipe(
    recipe: Recipe,
    store: ChunkStore,
    progress: Callable[[int], None] | None = None,
    cancel: Callable[[], bool] | None = None,
) -> str:
    """Czyta wszystkie fragmenty i zwraca SHA-256 złożonego pliku (bez zapisu)."""
    digest = hashlib.sha256()
    for cid, length in recipe.chunks:
        if cancel is not None and cancel():
            raise crypto.OperationCancelled(tr("Operacja przerwana przez użytkownika."))
        data = store.get(cid)
        if len(data) != length:
            raise ChunkError(tr("Fragment {cid} jest uszkodzony.").format(cid=cid[:16]))
        digest.update(data)
        if progress is not None:
            progress(length)
    return digest.hexdigest()


# ------------------------------------------------------------- sprzątanie


def list_path(store: ChunkStore, version: str) -> Path:
    return store.dir / _LISTS / f"{version or '_mirror'}.list"


def write_version_list(store: ChunkStore, version: str, recipes: Iterable[str]) -> None:
    """Zapisuje, które przepisy należą do wersji — sprzątanie nie musi przeglądać drzewa."""
    target = list_path(store, version)
    target.parent.mkdir(parents=True, exist_ok=True)
    _write_atomic(target, "\n".join(sorted(set(recipes))).encode("utf-8"))


def remove_version_list(store: ChunkStore, version: str) -> None:
    with contextlib.suppress(OSError):
        os.remove(long_path(list_path(store, version)))


def collect_garbage(
    store: ChunkStore,
    versions: Iterable[str],
    cancel: Callable[[], bool] | None = None,
) -> tuple[int, int]:
    """Patrz niżej — ``versions`` to nazwy katalogów wersji z datą plus ``""`` (kopia lustrzana)."""
    versions = list(versions)
    return _collect(store, versions, cancel)


def _collect(
    store: ChunkStore,
    versions: list[str],
    cancel: Callable[[], bool] | None,
) -> tuple[int, int]:
    """Usuwa fragmenty, do których nie odwołuje się żaden przepis. Zwraca (liczba, bajty).

    Zasada bezpieczeństwa: jeśli którykolwiek przepis nie daje się przeczytać,
    nie usuwamy **niczego** — lepiej zostawić śmieci niż skasować fragment
    potrzebny do odtworzenia pliku. Wersja bez listy przepisów (np. przerwana
    tak, że lista nie powstała) jest przeglądana w całości.
    """
    referenced: set[str] = set()
    seen: set[tuple[int, int]] = set()
    dated = {version for version in versions if version}
    for version in versions:
        for rel in _recipes_of(store, version, dated):
            path = store.root / rel
            try:
                st = os.stat(long_path(path))
            except FileNotFoundError:
                continue  # przepis usunięty razem z wersją albo podmieniony
            inode = (st.st_dev, st.st_ino)
            if st.st_ino and inode in seen:
                continue  # ten sam przepis podpięty dowiązaniem do wielu wersji
            seen.add(inode)
            try:
                referenced |= read_recipe(path, store.keyring).ids
            except (OSError, crypto.CryptoError) as exc:
                log.warning("Sprzątanie fragmentów wstrzymane — nieczytelny przepis %s: %s", path, exc)
                return 0, 0
            if cancel is not None and cancel():
                return 0, 0
    removed = freed = 0
    for cid, path in list(store.all_ids()):
        if cid in referenced:
            continue
        with contextlib.suppress(OSError):
            size = os.stat(long_path(path)).st_size
            os.remove(long_path(path))
            removed += 1
            freed += size
    if removed:
        log.info("Usunięto %d nieużywanych fragmentów (%d B).", removed, freed)
    return removed, freed


def _recipes_of(store: ChunkStore, version: str, dated: set[str]) -> Iterable[str]:
    listing = list_path(store, version)
    if Path(long_path(listing)).exists():
        text = Path(long_path(listing)).read_text(encoding="utf-8")
        return [line for line in text.splitlines() if line]
    found = list(_scan_for_recipes(store.root, version, dated))
    if version:
        # Wersja sprzed zapisu różnicowego (albo przerwana bez listy) — przegląd
        # drzewa zapamiętujemy, żeby następne sprzątanie go nie powtarzało.
        # Kopia lustrzana i tak dostaje świeżą listę przy każdym przebiegu.
        with contextlib.suppress(OSError):
            write_version_list(store, version, found)
    return found


def _scan_for_recipes(root: Path, version: str, dated: set[str]) -> Iterator[str]:
    """Przepisy wersji odczytane z drzewa katalogów, gdy brakuje listy.

    Dla kopii lustrzanej pomijamy wyłącznie **znane** katalogi wersji — zgadywanie
    po nazwie uznałoby folder użytkownika „2024-01-01 zdjęcia” za wersję, a jego
    fragmenty za nieużywane.
    """
    base = root / version if version else root
    top = True
    for folder, dirs, names in os.walk(long_path(base)):
        dirs[:] = [d for d in dirs if d != CHUNK_DIR and not (top and not version and d in dated)]
        top = False
        for name in names:
            if name.endswith(RECIPE_SUFFIX) or name.endswith(RECIPE_SUFFIX + ENCRYPTED_SUFFIX):
                full = Path(folder) / name
                yield os.path.relpath(full, long_path(root)).replace(os.sep, "/")
