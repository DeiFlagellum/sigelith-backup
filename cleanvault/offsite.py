"""Kopia poza domem (zasada 3-2-1): zaszyfrowane migawki w usłudze zgodnej z S3.

Kopia na dysku USB obok komputera nie przetrwa pożaru, kradzieży ani zalania.
Ten moduł wysyła do chmury (AWS S3, Backblaze B2, MinIO…) **migawkę** stanu
źródeł, zaszyfrowaną po stronie komputera osobnym hasłem — usługa widzi tylko
nieczytelne fragmenty.

Układ w kubełku (pod wybranym prefiksem)::

    config.json                  sól identyfikatorów i wartość kontrolna hasła
    chunks/ab/<id>               fragment: kontener CVLT (jak lokalnie .cvlt)
    snapshots/<znacznik>.cvsnap  migawka: zaszyfrowany przepis spisu treści

Treść plików dzielimy tak samo jak lokalny zapis różnicowy (FastCDC), a nazwą
fragmentu jest HMAC z kluczem z hasła, więc powtarzająca się treść — w tym samym
pliku, w innych plikach i w kolejnych migawkach — jest wysyłana raz. Spis treści
migawki (jeden wiersz na plik, posortowany) też jest dzielony na fragmenty:
kolejne migawki różnią się o kilka wierszy, więc kosztują kilka fragmentów,
a nie cały spis.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import threading
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from pathlib import Path

from . import beat, chunks, crypto
from .crypto import KdfParams, PasswordKeyring
from .i18n import plural, tr
from .locks import is_lock_error
from .log import get_logger
from .parallel import resolve_workers, unordered_map
from .paths import contained_path, long_path
from .s3 import NotFound, S3Client, S3Error
from .snapshot import ScanCancelled, SourceRoot, scan_sources

log = get_logger("offsite")

CONFIG = "config.json"
CHUNKS = "chunks/"
SNAPSHOTS = "snapshots/"
SNAPSHOT_SUFFIX = ".cvsnap"
INDEX_HEADER = b"TVB-SNAPSHOT 1\n"
#: Pliki do tej wielkości to jeden fragment; większe dzielimy jak lokalnie.
SINGLE_CHUNK_LIMIT = 8 * 1024 * 1024
#: Sprzątanie nie usuwa fragmentów młodszych niż doba — mógł je właśnie wysłać
#: drugi komputer, który zapisze swoją migawkę za chwilę.
GC_GRACE_SECONDS = 24 * 3600
_ID_CONTEXT = b"cleanvault chunk id"


class OffsiteError(Exception):
    """Kopia poza domem nie powiodła się albo jej zawartość jest niespójna."""


# ------------------------------------------------------------- magazyn zdalny


class RemoteStore:
    """Fragmenty w kubełku — ten sam schemat co lokalny :class:`chunks.ChunkStore`."""

    def __init__(self, client: S3Client, keyring: PasswordKeyring, create: bool = False) -> None:
        self.client = client
        self.keyring = keyring
        self._id_key = self._load_id_key(create)

    def _load_id_key(self, create: bool) -> bytes:
        try:
            raw = json.loads(self.client.get(CONFIG).decode("utf-8"))
        except NotFound:
            raw = None
        except (ValueError, UnicodeDecodeError) as exc:
            raise OffsiteError(tr("Opis kopii poza domem jest uszkodzony.")) from exc
        if raw is None:
            if not create:
                raise OffsiteError(tr("W tym miejscu nie ma jeszcze kopii poza domem."))
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
                "check": hmac.new(key, b"check", hashlib.sha256).hexdigest(),
            }
            self.client.put(CONFIG, json.dumps(config, indent=1).encode("utf-8"))
            return key
        try:
            params = KdfParams(int(raw["kdf"]), bytes.fromhex(raw["salt"]), int(raw["a"]), int(raw["b"]), int(raw["c"]))
            check = str(raw["check"])
        except (KeyError, ValueError) as exc:
            raise OffsiteError(tr("Opis kopii poza domem jest uszkodzony.")) from exc
        key = self._derive(params)
        if not hmac.compare_digest(hmac.new(key, b"check", hashlib.sha256).hexdigest(), check):
            raise OffsiteError(tr("Hasło kopii poza domem nie pasuje do danych zapisanych w tym miejscu."))
        return key

    def _derive(self, params: KdfParams) -> bytes:
        return hmac.new(self.keyring.key_for(params), _ID_CONTEXT, hashlib.sha256).digest()

    def chunk_id(self, data: bytes) -> str:
        return hmac.new(self._id_key, data, hashlib.sha256).hexdigest()

    @staticmethod
    def name_for(cid: str) -> str:
        return f"{CHUNKS}{cid[:2]}/{cid}"

    def put(self, cid: str, data: bytes) -> int:
        payload = crypto.encrypt_bytes(data, self.keyring)
        self.client.put(self.name_for(cid), payload)
        return len(payload)

    def get(self, cid: str) -> bytes:
        try:
            payload = self.client.get(self.name_for(cid))
        except NotFound as exc:
            raise OffsiteError(tr("Brak fragmentu {cid} w kopii poza domem.").format(cid=cid[:16])) from exc
        data = crypto.decrypt_bytes(payload, self.keyring)
        if not hmac.compare_digest(self.chunk_id(data), cid):
            raise OffsiteError(tr("Fragment {cid} jest uszkodzony.").format(cid=cid[:16]))
        return data


# ------------------------------------------------------------------ migawka


@dataclass
class FileRecord:
    size: int
    mtime: float
    sha256: str
    chunks: list[tuple[str, int]]


@dataclass
class Snapshot:
    stamp: str
    created: float
    roots: dict[str, str]
    files: dict[str, FileRecord] = field(default_factory=dict)

    def to_bytes(self) -> bytes:
        """Spis treści — jeden wiersz na plik, posortowany, żeby kolejne migawki
        różniły się w jak najmniejszej liczbie fragmentów."""
        head = json.dumps({"stamp": self.stamp, "created": self.created, "roots": self.roots}, sort_keys=True)
        lines = [INDEX_HEADER.decode("ascii").rstrip("\n"), head]
        for key in sorted(self.files):
            record = self.files[key]
            lines.append(
                json.dumps([key, record.size, record.mtime, record.sha256, [[c, n] for c, n in record.chunks]],
                           ensure_ascii=False, separators=(",", ":"))
            )
        return ("\n".join(lines) + "\n").encode("utf-8")

    @classmethod
    def from_bytes(cls, data: bytes) -> Snapshot:
        if not data.startswith(INDEX_HEADER):
            raise OffsiteError(tr("Migawka kopii poza domem jest uszkodzona."))
        lines = data.decode("utf-8").splitlines()
        try:
            head = json.loads(lines[1])
            snapshot = cls(stamp=head["stamp"], created=float(head["created"]), roots=dict(head["roots"]))
            for line in lines[2:]:
                if not line:
                    continue
                key, size, mtime, sha, parts = json.loads(line)
                snapshot.files[key] = FileRecord(int(size), float(mtime), str(sha), [(c, int(n)) for c, n in parts])
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise OffsiteError(tr("Migawka kopii poza domem jest uszkodzona.")) from exc
        return snapshot

    def chunk_ids(self) -> set[str]:
        return {cid for record in self.files.values() for cid, _n in record.chunks}


def list_snapshots(client: S3Client) -> list[str]:
    """Znaczniki migawek od najstarszej do najnowszej."""
    names = [name[len(SNAPSHOTS) : -len(SNAPSHOT_SUFFIX)] for name, _size in client.list(SNAPSHOTS)
             if name.endswith(SNAPSHOT_SUFFIX)]
    return sorted(names)


def load_snapshot(client: S3Client, store: RemoteStore, stamp: str, cache: dict[str, bytes] | None = None) -> Snapshot:
    """Wczytuje migawkę: przepis spisu treści, a z niego fragmenty samego spisu."""
    try:
        blob = client.get(f"{SNAPSHOTS}{stamp}{SNAPSHOT_SUFFIX}")
    except NotFound as exc:
        raise OffsiteError(tr("Nie ma migawki {stamp} w kopii poza domem.").format(stamp=stamp)) from exc
    recipe = chunks.Recipe.from_bytes(crypto.decrypt_bytes(blob, store.keyring))
    parts = []
    for cid, _length in recipe.chunks:
        if cache is not None and cid in cache:
            parts.append(cache[cid])
            continue
        data = store.get(cid)
        if cache is not None:
            cache[cid] = data
        parts.append(data)
    index = b"".join(parts)
    if hashlib.sha256(index).hexdigest() != recipe.sha256:
        raise OffsiteError(tr("Migawka kopii poza domem jest uszkodzona."))
    snapshot = Snapshot.from_bytes(index)
    snapshot.index_ids = recipe.ids  # type: ignore[attr-defined]
    return snapshot


def _save_snapshot(client: S3Client, store: RemoteStore, snapshot: Snapshot, known: set[str]) -> int:
    index = snapshot.to_bytes()
    parts: list[tuple[str, int]] = []
    sent = 0
    for data in _split(index):
        cid = store.chunk_id(data)
        if cid not in known:
            sent += store.put(cid, data)
            known.add(cid)
        parts.append((cid, len(data)))
    recipe = chunks.Recipe(size=len(index), sha256=hashlib.sha256(index).hexdigest(), chunks=parts)
    client.put(f"{SNAPSHOTS}{snapshot.stamp}{SNAPSHOT_SUFFIX}", crypto.encrypt_bytes(recipe.to_bytes(), store.keyring))
    return sent


def _split(data: bytes) -> Iterable[bytes]:
    if len(data) <= SINGLE_CHUNK_LIMIT:
        return [data]
    import io

    return list(chunks.iter_chunks(io.BytesIO(data)))


# ------------------------------------------------------------------- wysyłka


@dataclass
class UploadResult:
    stamp: str = ""
    files: int = 0
    reused: int = 0
    uploaded_chunks: int = 0
    uploaded_bytes: int = 0
    errors: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    cancelled: bool = False

    @property
    def ok(self) -> bool:
        return not self.errors and not self.cancelled


def upload(
    roots: list[SourceRoot],
    excludes: list[str],
    client: S3Client,
    keyring: PasswordKeyring,
    progress_stage: Callable[[str], None] = lambda _t: None,
    progress_bytes: Callable[[int], None] = lambda _n: None,
    cancel: Callable[[], bool] = lambda: False,
    workers: int = 0,
    now: float | None = None,
) -> UploadResult:
    """Wysyła nową migawkę: pliki bez zmian od poprzedniej migawki nie są nawet czytane."""
    result = UploadResult()
    store = RemoteStore(client, keyring, create=True)
    existing = list_snapshots(client)
    previous: Snapshot | None = None
    if existing:
        progress_stage(tr("Wczytuję poprzednią migawkę kopii poza domem…"))
        previous = load_snapshot(client, store, existing[-1])
    known: set[str] = previous.chunk_ids() | getattr(previous, "index_ids", set()) if previous else set()
    lock = threading.Lock()

    progress_stage(tr("Skanowanie plików źródłowych…"))
    try:
        scanned = scan_sources(roots, excludes, cancel=cancel)
    except ScanCancelled:
        result.cancelled = True
        return result

    moment = time.time() if now is None else now
    stamp = beat.stamp(moment)
    if stamp in existing:
        stamp = f"{stamp}_{int(moment)}"
    snapshot = Snapshot(stamp=stamp, created=moment, roots={r.label: str(r.path) for r in roots})
    by_label = {root.label: root for root in roots}
    todo: list[tuple[str, Path]] = []
    for key, meta in scanned.items():
        old = previous.files.get(key) if previous else None
        if old is not None and old.size == meta.size and abs(old.mtime - meta.mtime) <= 0.01:
            snapshot.files[key] = old
            result.reused += 1
            continue
        label, _, rel = key.partition("/")
        todo.append((key, by_label[label].path / rel.replace("/", os.sep)))

    progress_stage(
        tr("Wysyłam poza dom pliki nowe i zmienione: {count}…").format(count=len(todo))
    )

    def send(item: tuple[str, Path]) -> FileRecord | None:
        _key, path = item
        if cancel():
            raise crypto.OperationCancelled(tr("Operacja przerwana przez użytkownika."))
        before = _fingerprint(path)
        digest = hashlib.sha256()
        parts: list[tuple[str, int]] = []
        with open(long_path(path), "rb") as handle:
            pieces = [handle.read()] if (before and before[0] <= SINGLE_CHUNK_LIMIT) else chunks.iter_chunks(handle, cancel)
            for data in pieces:
                digest.update(data)
                cid = store.chunk_id(data)
                with lock:
                    fresh = cid not in known
                    if fresh:
                        known.add(cid)
                if fresh:
                    try:
                        sent = store.put(cid, data)
                    except BaseException:
                        with lock:
                            known.discard(cid)
                        raise
                    with lock:
                        result.uploaded_chunks += 1
                        result.uploaded_bytes += sent
                parts.append((cid, len(data)))
                progress_bytes(len(data))
        after = _fingerprint(path)
        if before is None or before != after:
            return None  # zmieniony w trakcie — trafi do następnej migawki
        return FileRecord(size=after[0], mtime=after[1], sha256=digest.hexdigest(), chunks=parts)

    for (key, path), record, error in unordered_map(send, todo, resolve_workers(workers), cancel):
        if error is not None:
            if isinstance(error, (crypto.OperationCancelled, ScanCancelled)):
                result.cancelled = True
                continue
            old = previous.files.get(key) if previous else None
            if old is not None:
                snapshot.files[key] = old  # lepsza wczorajsza wersja niż żadna
            if is_lock_error(error, path):
                result.skipped.append(key)
            else:
                result.errors.append(f"{key}: {error}")
            continue
        if record is None:
            result.skipped.append(key)
            old = previous.files.get(key) if previous else None
            if old is not None:
                snapshot.files[key] = old
            continue
        snapshot.files[key] = record
        result.files += 1

    if result.cancelled or cancel():
        result.cancelled = True
        return result
    progress_stage(tr("Zapisuję migawkę {stamp}…").format(stamp=beat.describe(stamp)))
    result.uploaded_bytes += _save_snapshot(client, store, snapshot, known)
    _leave_rescue_files(client)
    result.stamp = stamp
    log.info(
        "Migawka poza domem %s: %d plików wysłanych, %d bez zmian, %d fragmentów (%d B).",
        stamp, result.files, result.reused, result.uploaded_chunks, result.uploaded_bytes,
    )
    return result


def _leave_rescue_files(client: S3Client) -> None:
    """Kubełek też opisuje się sam: notatka i skrypt ratunkowy obok migawek.

    Gdy przepada dysk lokalny, przepada też leżący na nim skrypt — a kopia poza
    domem istnieje właśnie na taką okazję. Oba pliki są jawne: nie zawierają
    żadnej tajemnicy, a bez nich nikt nie odczyta reszty.
    """
    from .paths import resource_path
    from .rescue import SCRIPT_NAME, offsite_note

    note = offsite_note()
    try:
        client.put("JAK ODZYSKAC DANE - HOW TO RECOVER.txt", note.encode("utf-8"))
        client.put(SCRIPT_NAME, resource_path("assets", "recovery", SCRIPT_NAME).read_bytes())
    except (OSError, S3Error) as exc:
        log.warning("Nie udało się zostawić notatki ratunkowej w kubełku: %s", exc)


def _fingerprint(path: Path) -> tuple[int, float] | None:
    try:
        st = os.stat(long_path(path))
    except OSError:
        return None
    return st.st_size, st.st_mtime


# --------------------------------------------------------------- przywracanie


def restore(
    client: S3Client,
    keyring: PasswordKeyring,
    stamp: str,
    destination: str | os.PathLike[str],
    progress_stage: Callable[[str], None] = lambda _t: None,
    progress_bytes: Callable[[int], None] = lambda _n: None,
    cancel: Callable[[], bool] = lambda: False,
    workers: int = 0,
    only: Callable[[str], bool] | None = None,
) -> tuple[int, list[str]]:
    """Odtwarza migawkę do katalogu; zwraca (liczba plików, błędy)."""
    store = RemoteStore(client, keyring)
    progress_stage(tr("Wczytuję migawkę {stamp}…").format(stamp=beat.describe(stamp)))
    snapshot = load_snapshot(client, store, stamp)
    target_root = Path(destination)
    items = [(key, record) for key, record in snapshot.files.items() if only is None or only(key)]
    progress_stage(
        tr("Przywracanie {count} {files} z kopii poza domem…").format(
            count=len(items), files=plural(len(items), "pliku", "plików", "plików")
        )
    )

    def fetch(item: tuple[str, FileRecord]) -> None:
        key, record = item
        target = contained_path(target_root, key)
        if target is None:
            raise OffsiteError(tr("Wpis {key} w spisie treści kopii wskazuje poza katalog docelowy — "
                                  "pomijam go.").format(key=repr(key)))
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_name(target.name + ".part")
        digest = hashlib.sha256()
        try:
            with open(long_path(tmp), "wb") as out:
                for cid, length in record.chunks:
                    if cancel():
                        raise crypto.OperationCancelled(tr("Operacja przerwana przez użytkownika."))
                    data = store.get(cid)
                    if len(data) != length:
                        raise OffsiteError(tr("Fragment {cid} jest uszkodzony.").format(cid=cid[:16]))
                    out.write(data)
                    digest.update(data)
                    progress_bytes(length)
            if digest.hexdigest() != record.sha256:
                raise OffsiteError(tr("Plik złożony z fragmentów różni się od zapisanego w przepisie."))
            os.replace(long_path(tmp), long_path(target))
            os.utime(long_path(target), (record.mtime, record.mtime))
        except BaseException:
            if Path(long_path(tmp)).exists():
                os.remove(long_path(tmp))
            raise

    restored = 0
    errors: list[str] = []
    for (key, _record), _none, error in unordered_map(fetch, items, resolve_workers(workers), cancel):
        if error is not None:
            if isinstance(error, crypto.OperationCancelled):
                break
            errors.append(f"{key}: {error}")
            continue
        restored += 1
    return restored, errors


# ---------------------------------------------------------------- sprzątanie


def prune(
    client: S3Client,
    keyring: PasswordKeyring,
    keep: int,
    progress_stage: Callable[[str], None] = lambda _t: None,
    now: float | None = None,
) -> tuple[int, int]:
    """Zostawia ``keep`` najnowszych migawek i usuwa fragmenty, których żadna nie używa.

    Zwraca (usunięte migawki, usunięte fragmenty). Jak lokalnie: jeśli któraś
    z zostających migawek nie daje się wczytać, nie usuwamy żadnego fragmentu.
    """
    if keep <= 0:
        return 0, 0
    store = RemoteStore(client, keyring)
    stamps = list_snapshots(client)
    doomed = stamps[: max(0, len(stamps) - keep)]
    for stamp in doomed:
        client.delete(f"{SNAPSHOTS}{stamp}{SNAPSHOT_SUFFIX}")
    if not doomed:
        return 0, 0
    progress_stage(tr("Porządkowanie kopii poza domem…"))
    referenced: set[str] = set()
    cache: dict[str, bytes] = {}
    try:
        for stamp in stamps[len(doomed) :]:
            snapshot = load_snapshot(client, store, stamp, cache)
            referenced |= snapshot.chunk_ids() | snapshot.index_ids  # type: ignore[attr-defined]
    except (OffsiteError, S3Error, crypto.CryptoError) as exc:
        log.warning("Sprzątanie kopii poza domem wstrzymane — nieczytelna migawka: %s", exc)
        return len(doomed), 0
    moment = time.time() if now is None else now
    removed = 0
    for name, _size, modified in client.list_detailed(CHUNKS):
        cid = name.rsplit("/", 1)[-1]
        if cid in referenced or moment - modified < GC_GRACE_SECONDS:
            continue
        client.delete(name)
        removed += 1
    log.info("Kopia poza domem: usunięto %d migawek i %d fragmentów.", len(doomed), removed)
    return len(doomed), removed
