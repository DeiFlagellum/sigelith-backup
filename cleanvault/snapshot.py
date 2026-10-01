"""Skanowanie drzewa plików i manifest kopii zapasowej.

Tu mieszka najważniejsza poprawka merytoryczna całej wersji 2.0.

Wersja 1.x porównywała źródło z celem tak::

    rel = os.path.relpath(path, start=list(snap.keys())[0].split(os.sep)[0])

czyli liczyła ścieżkę względną wobec *litery dysku* pierwszego napotkanego
klucza. Dla źródła na ``D:`` i celu na ``C:`` te ścieżki nie miały szans się
zrównać, więc **każdy plik przy każdym uruchomieniu był uznawany za zmieniony** —
„kopia przyrostowa" była w rzeczywistości pełną kopią. Dodatkowo porównanie
działało w złożoności ``O(N×M)`` (lista składana po całym celu dla każdego pliku
źródła), a snapshot liczył SHA-256 całego drzewa źródła *i* celu przy każdym
przebiegu.

Wersja 2.0 rozwiązuje to strukturalnie:

* klucze są ścieżkami **względnymi wobec katalogu źródłowego**, więc porównanie
  jest zwykłym odpytaniem słownika — ``O(N+M)``;
* stan poprzedniej kopii trzyma **manifest zapisany w katalogu docelowym**,
  a nie snapshot celu. Dzięki temu porównanie działa identycznie dla kopii
  jawnych i zaszyfrowanych (hash zaszyfrowanego pliku z natury nie równa się
  hashowi źródła, więc stare podejście i tak nie mogło działać z szyfrowaniem);
* SHA-256 liczymy **leniwie** — tylko gdy rozmiar lub czas modyfikacji różni się
  od zapisanego w manifeście. Typowy kolejny backup nie czyta zawartości plików
  w ogóle, tylko metadane.
"""

from __future__ import annotations

import contextlib
import fnmatch
import functools
import hashlib
import os
import queue
import re
import struct
import threading
import time
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from pathlib import Path

import msgpack

from .i18n import tr
from .log import get_logger
from .parallel import resolve_workers
from .paths import JOURNAL_NAME, MANIFEST_NAME, SUMMARY_NAME, long_path

log = get_logger("snapshot")

HASH_CHUNK = 1024 * 1024
MANIFEST_MAGIC = b"CVMF"
MANIFEST_VERSION = 1
#: Domyślna liczba wątków skanu. Pomiar na 1,1 mln plików (NVMe, dane
#: w pamięci podręcznej systemu): 1 wątek 25 s, 4–32 wątki 38–39 s. Skan to
#: w większości praca Pythona na każdym wpisie, a CPython zwalnia i odzyskuje
#: GIL przy każdym kolejnym wpisie katalogu — wątki przepychają się o blokadę.
#: Równoległość opłaca się tam, gdzie czeka się na samo listowanie katalogów
#: (np. udziały sieciowe), dlatego zostaje dostępna jako opcja.
SCAN_WORKERS = 1
JOURNAL_MAGIC = b"CVJ1"
#: magia, znacznik czasu zapisu paczki, długość, SHA-256 treści
_JOURNAL_HEADER = struct.Struct(">4sdI32s")

ProgressFn = Callable[[str, int], None]
CancelFn = Callable[[], bool]


class ScanCancelled(Exception):
    """Skanowanie przerwane przez użytkownika."""


@dataclass(frozen=True)
class FileMeta:
    """Metadane pojedynczego pliku źródłowego."""

    size: int
    mtime: float
    sha256: str = ""

    def same_stat_as(self, other: FileMeta | None, tolerance: float = 2.0) -> bool:
        """Czy rozmiar i czas modyfikacji wskazują na brak zmian.

        Domyślna tolerancja 2 s obsługuje czasy odczytane z nośników FAT, które
        zapisują je z dokładnością do dwóch sekund. Silnik porównuje jednak
        źródło z czasem zapamiętanym **z tego samego źródła** i podaje dużo
        mniejszą tolerancję — inaczej plik zapisany sekundę po skopiowaniu,
        z tym samym rozmiarem, uchodziłby za niezmieniony na zawsze.
        """
        if other is None:
            return False
        return self.size == other.size and abs(self.mtime - other.mtime) <= tolerance


@dataclass
class SourceRoot:
    """Katalog źródłowy wraz z etykietą, pod którą trafia do kopii."""

    path: Path
    label: str

    @staticmethod
    def make(raw: str | os.PathLike[str]) -> SourceRoot:
        path = Path(raw).resolve()
        label = path.name
        if not label:  # katalog główny dysku, np. "D:\\"
            label = path.drive.replace(":", "").replace("\\", "") or "dysk"
            label = f"{label}_dysk"
        return SourceRoot(path=path, label=_sanitise(label))


def _sanitise(name: str) -> str:
    """Usuwa z etykiety znaki niedozwolone w nazwach plików Windows."""
    bad = '<>:"/\\|?*'
    cleaned = "".join("_" if ch in bad or ord(ch) < 32 else ch for ch in name).strip(" .")
    return cleaned or "zrodlo"


def compile_excludes(patterns: list[str]) -> list[str]:
    """Normalizuje wzorce wykluczeń do porównań na ścieżkach z ukośnikiem."""
    return [p.replace("\\", "/").strip() for p in patterns if p and p.strip()]


class ExcludeMatcher:
    """Skompilowany zestaw wzorców wykluczeń.

    Skan sprawdza wykluczenia dla każdego z milionów wpisów. Dopasowanie wzorzec
    po wzorcu przez ``fnmatch`` kosztowało ~34–66 µs na wpis, czyli ponad minutę
    samego porównywania napisów przy 1,7 mln plików — i to pod blokadą GIL, więc
    hamowało także skan wielowątkowy. Jedno wyrażenie regularne na wszystkie
    wzorce robi to kilkanaście razy szybciej.
    """

    def __init__(self, patterns: tuple[str, ...]) -> None:
        lowered = [p.lower() for p in patterns]
        self._any = _alternation(lowered)
        bases = [p[:-2] for p in lowered if p.endswith("/*")]
        self._anchored = tuple(bases)
        self._single_name = _alternation([b for b in bases if "/" not in b])

    def matches(self, rel_lower: str, name_lower: str, is_dir: bool, check_ancestors: bool) -> bool:
        if self._any is not None and (self._any.match(name_lower) or self._any.match(rel_lower)):
            return True
        for base in self._anchored:
            # Sam katalog i jego wnętrze, licząc od katalogu głównego źródła.
            if rel_lower == base or rel_lower.startswith(base + "/"):
                return True
        if self._single_name is None:
            return False
        # Katalog o tej nazwie gdziekolwiek na ścieżce. Ostatni człon liczy się
        # tylko dla katalogu — plik o nazwie „build” nie jest katalogiem „build/”.
        if is_dir and self._single_name.match(name_lower):
            return True
        if check_ancestors:
            return any(self._single_name.match(part) for part in rel_lower.split("/")[:-1])
        return False


def _alternation(patterns: list[str]) -> re.Pattern[str] | None:
    if not patterns:
        return None
    return re.compile("|".join(f"(?:{fnmatch.translate(p)})" for p in patterns))


@functools.lru_cache(maxsize=64)
def exclude_matcher(patterns: tuple[str, ...]) -> ExcludeMatcher:
    return ExcludeMatcher(patterns)


def is_excluded(
    rel_path: str,
    name: str,
    patterns: list[str],
    is_dir: bool = False,
    check_ancestors: bool = True,
) -> bool:
    """Dopasowuje wzorzec do nazwy pliku i do pełnej ścieżki względnej.

    Wzorzec katalogowy z jedną nazwą (``node_modules/*``) działa na **każdej
    głębokości**, tak jak ``node_modules/`` w ``.gitignore``. Wcześniej działał
    wyłącznie w katalogu głównym źródła, więc zagnieżdżone ``venv``,
    ``__pycache__`` i ``node_modules`` projektów trafiały do kopii — u jednego
    użytkownika była to jedna trzecia z 1,7 mln plików. Wzorzec z kilkoma
    członami (``a/b/*``) pozostaje zakotwiczony w katalogu głównym źródła.

    ``check_ancestors=False`` stosuje skan: katalogi nadrzędne zostały już
    sprawdzone, gdy do nich wchodził.
    """
    return exclude_matcher(tuple(patterns)).matches(rel_path.lower(), name.lower(), is_dir, check_ancestors)


def hash_file(path: str | os.PathLike[str], cancel: CancelFn | None = None) -> str:
    digest = hashlib.sha256()
    with open(long_path(path), "rb") as handle:
        while True:
            if cancel is not None and cancel():
                raise ScanCancelled(tr("Przerwano liczenie sumy kontrolnej."))
            chunk = handle.read(HASH_CHUNK)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def iter_tree(root: Path, excludes: list[str], cancel: CancelFn | None = None) -> Iterator[tuple[str, Path, os.stat_result]]:
    """Przechodzi drzewo katalogów, zwracając ``(ścieżka względna, ścieżka, stat)``.

    Używamy ``os.scandir`` zamiast ``os.walk``: ``DirEntry`` niesie już wynik
    ``stat`` z systemu plików, więc unikamy osobnego wywołania na każdy plik.
    Dowiązania i punkty ponownej analizy (junction) pomijamy — inaczej
    junction wskazujący na przodka zapętliłby skanowanie.
    """
    stack: list[Path] = [root]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(long_path(current)) as entries:
                for entry in entries:
                    if cancel is not None and cancel():
                        raise ScanCancelled(tr("Przerwano skanowanie."))
                    entry_path = Path(current) / entry.name
                    try:
                        rel = entry_path.relative_to(root).as_posix()
                    except ValueError:  # pragma: no cover - zabezpieczenie
                        continue
                    try:
                        is_dir = entry.is_dir(follow_symlinks=False) and not _is_junction(entry)
                        if is_excluded(rel, entry.name, excludes, is_dir=is_dir, check_ancestors=False):
                            continue
                        if is_dir:
                            stack.append(entry_path)
                            continue
                        if not entry.is_file(follow_symlinks=False):
                            continue
                        yield rel, entry_path, entry.stat(follow_symlinks=False)
                    except OSError as exc:
                        log.warning("Pomijam %s: %s", entry_path, exc)
        except PermissionError as exc:
            log.warning("Brak dostępu do katalogu %s: %s", current, exc)
        except OSError as exc:
            log.warning("Nie można odczytać katalogu %s: %s", current, exc)


def _is_junction(entry: os.DirEntry) -> bool:
    """Punkt połączenia (junction) — traktujemy jak dowiązanie i nie wchodzimy do środka."""
    checker = getattr(entry, "is_junction", None)
    try:
        return bool(checker()) if checker is not None else False
    except OSError:
        return False


def _scan_directory(
    root: Path, rel_dir: str, patterns: list[str], cancel: CancelFn | None
) -> tuple[list[tuple[str, int, float]], list[str]]:
    """Jeden katalog: pliki ``(ścieżka względna, rozmiar, mtime)`` i podkatalogi do odwiedzenia."""
    folder = root / rel_dir if rel_dir else root
    matcher = exclude_matcher(tuple(patterns))
    files: list[tuple[str, int, float]] = []
    subdirs: list[str] = []
    try:
        with os.scandir(long_path(folder)) as entries:
            for entry in entries:
                if cancel is not None and cancel():
                    raise ScanCancelled(tr("Przerwano skanowanie."))
                rel = f"{rel_dir}/{entry.name}" if rel_dir else entry.name
                try:
                    is_dir = entry.is_dir(follow_symlinks=False) and not _is_junction(entry)
                    if matcher.matches(rel.lower(), entry.name.lower(), is_dir, False):
                        continue
                    if is_dir:
                        subdirs.append(rel)
                        continue
                    if not entry.is_file(follow_symlinks=False):
                        continue
                    st = entry.stat(follow_symlinks=False)
                    files.append((rel, st.st_size, st.st_mtime))
                except OSError as exc:
                    log.warning("Pomijam %s: %s", folder / entry.name, exc)
    except PermissionError as exc:
        log.warning("Brak dostępu do katalogu %s: %s", folder, exc)
    except OSError as exc:
        log.warning("Nie można odczytać katalogu %s: %s", folder, exc)
    return files, subdirs


def _walk_source(
    root: Path, patterns: list[str], cancel: CancelFn | None, workers: int
) -> Iterator[tuple[str, int, float]]:
    """Przechodzi drzewo źródła; przy ``workers > 1`` czyta wiele katalogów naraz.

    Tryb wielowątkowy pomaga, gdy czeka się na samo listowanie katalogów
    (np. udział sieciowy). Na lokalnym NVMe jest wolniejszy — patrz
    ``SCAN_WORKERS``. Kolejka zadań zamiast listy ``Future`` pozwala obsłużyć
    setki tysięcy katalogów bez kosztu kwadratowego.
    """
    if workers <= 1:
        pending = [""]
        while pending:
            files, subdirs = _scan_directory(root, pending.pop(), patterns, cancel)
            yield from files
            pending.extend(subdirs)
        return

    tasks: queue.Queue[str | None] = queue.Queue()
    results: queue.Queue[tuple[list, list, BaseException | None]] = queue.Queue()

    def worker() -> None:
        while True:
            rel = tasks.get()
            if rel is None:
                return
            try:
                files, subdirs = _scan_directory(root, rel, patterns, cancel)
                results.put((files, subdirs, None))
            except BaseException as exc:  # noqa: BLE001 - przekazujemy do wątku głównego
                results.put(([], [], exc))

    threads = [threading.Thread(target=worker, name="cleanvault-scan", daemon=True) for _ in range(workers)]
    for thread in threads:
        thread.start()
    tasks.put("")
    outstanding = 1
    try:
        while outstanding:
            files, subdirs, error = results.get()
            outstanding -= 1
            if error is not None:
                raise error
            yield from files
            for rel in subdirs:
                tasks.put(rel)
                outstanding += 1
    finally:
        with contextlib.suppress(queue.Empty):
            while True:
                tasks.get_nowait()
        for _ in threads:
            tasks.put(None)


def scan_sources(
    roots: list[SourceRoot],
    excludes: list[str],
    progress: ProgressFn | None = None,
    cancel: CancelFn | None = None,
    workers: int = SCAN_WORKERS,
) -> dict[str, FileMeta]:
    """Skanuje wszystkie katalogi źródłowe.

    Klucz wyniku to ``<etykieta źródła>/<ścieżka względna>``. Etykieta jest
    zawsze obecna, dzięki czemu kilka źródeł nie miesza się w celu, a układ
    kopii jest jednoznaczny przy przywracaniu. Stara wersja używała
    ``os.path.commonpath(sources)``, co przy źródłach na różnych dyskach
    rzucało ``ValueError`` i wywracało cały backup.

    Wynik jest posortowany po kluczu: skan równoległy zwraca pliki w dowolnej
    kolejności, a kopia plików z tego samego katalogu jeden po drugim jest
    szybsza i daje powtarzalny plan.
    """
    result: dict[str, FileMeta] = {}
    patterns = compile_excludes(excludes)
    threads = resolve_workers(workers)
    for root in roots:
        if not root.path.is_dir():
            log.warning("Pomijam nieistniejące źródło: %s", root.path)
            continue
        count = 0
        for rel, size, mtime in _walk_source(root.path, patterns, cancel, threads):
            result[f"{root.label}/{rel}"] = FileMeta(size=size, mtime=mtime)
            count += 1
            if progress is not None and count % 2000 == 0:
                progress(root.label, count)
        log.info("Źródło %s: %d plików.", root.path, count)
    return dict(sorted(result.items()))


@dataclass
class ManifestEntry:
    size: int
    mtime: float
    sha256: str
    stored: str  # nazwa pliku w katalogu docelowym (z sufiksem .cvlt dla kopii szyfrowanych)
    stored_size: int = 0
    #: plik zapisany fragmentami: ``stored`` wskazuje przepis (.cvrecipe), a treść
    #: leży w magazynie fragmentów (patrz :mod:`cleanvault.chunks`)
    chunked: bool = False

    def to_dict(self) -> dict:
        raw = {
            "size": self.size,
            "mtime": self.mtime,
            "sha256": self.sha256,
            "stored": self.stored,
            "stored_size": self.stored_size,
        }
        if self.chunked:  # tylko gdy prawda — spis treści ma miliony wpisów
            raw["chunked"] = True
        return raw

    @classmethod
    def from_dict(cls, raw: dict) -> ManifestEntry:
        return cls(
            size=int(raw.get("size", 0)),
            mtime=float(raw.get("mtime", 0.0)),
            sha256=str(raw.get("sha256", "")),
            stored=str(raw.get("stored", "")),
            stored_size=int(raw.get("stored_size", 0)),
            chunked=bool(raw.get("chunked", False)),
        )


@dataclass
class VersionState:
    """Stan jednego katalogu wersji kopii.

    Bez tego manifest wiedział tylko, że katalog wersji *istnieje* — nie, czy
    kopia do niego dobiegła końca. Przerwany przebieg wyglądał więc dokładnie
    tak samo jak ukończony, a „wznawianie" nie miało się o co oprzeć.
    """

    name: str
    started: float = 0.0
    finished: float = 0.0  # 0.0 = przebieg nigdy się nie domknął
    complete: bool = False
    #: etykiety katalogów źródłowych, których dotyczył ten przebieg — pozwalają
    #: odróżnić niedokończoną kopię *tego* zadania od kopii innego zadania
    #: piszącego do tego samego katalogu docelowego.
    labels: list[str] = field(default_factory=list)
    encrypted: bool = False
    structure: str = "dated"
    planned_files: int = 0
    planned_bytes: int = 0
    done_files: int = 0
    done_bytes: int = 0
    #: pliki pominięte, bo trzymał je otwarte inny program — wersja jest mimo to
    #: kompletna (użytkownik wie, co zamknąć), ale nie wolno tego przemilczeć
    locked_files: int = 0
    #: ``False`` dla wersji odtworzonej z manifestu sprzed zapisywania stanu
    #: przebiegów. O takiej wersji **nie wiemy**, czy jest kompletna — i tak
    #: musi ją opisywać interfejs, zamiast twierdzić, że jest pełna.
    known: bool = True

    @property
    def missing_files(self) -> int:
        return max(0, self.planned_files - self.done_files)

    @property
    def missing_bytes(self) -> int:
        return max(0, self.planned_bytes - self.done_bytes)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "started": self.started,
            "finished": self.finished,
            "complete": self.complete,
            "labels": list(self.labels),
            "encrypted": self.encrypted,
            "structure": self.structure,
            "planned_files": self.planned_files,
            "planned_bytes": self.planned_bytes,
            "done_files": self.done_files,
            "done_bytes": self.done_bytes,
            "locked_files": self.locked_files,
            "known": self.known,
        }

    @classmethod
    def from_dict(cls, raw: dict) -> VersionState:
        return cls(
            name=str(raw.get("name", "")),
            started=float(raw.get("started", 0.0)),
            finished=float(raw.get("finished", 0.0)),
            complete=bool(raw.get("complete", False)),
            labels=[str(x) for x in (raw.get("labels") or [])],
            encrypted=bool(raw.get("encrypted", False)),
            structure=str(raw.get("structure", "dated")),
            planned_files=int(raw.get("planned_files", 0)),
            planned_bytes=int(raw.get("planned_bytes", 0)),
            done_files=int(raw.get("done_files", 0)),
            done_bytes=int(raw.get("done_bytes", 0)),
            locked_files=int(raw.get("locked_files", 0)),
            known=bool(raw.get("known", True)),
        )


@dataclass
class Manifest:
    """Spis treści kopii zapasowej, zapisywany w katalogu docelowym.

    To on — a nie ponowne skanowanie celu — jest podstawą kopii przyrostowej.
    Zapis jest atomowy i opatrzony sumą kontrolną, tak samo jak stan aplikacji.
    """

    path: Path
    encrypted: bool = False
    created: float = field(default_factory=time.time)
    updated: float = field(default_factory=time.time)
    entries: dict[str, ManifestEntry] = field(default_factory=dict)
    #: etykieta źródła -> oryginalna ścieżka absolutna; potrzebne, by umieć
    #: przywrócić pliki dokładnie tam, skąd zostały pobrane.
    roots: dict[str, str] = field(default_factory=dict)
    #: katalogi wersji utworzone przez ten manifest, chronologicznie.
    #: Czyszczenie historii działa wyłącznie na tej liście — nigdy nie kasujemy
    #: katalogu tylko dlatego, że jego nazwa wygląda jak data.
    versions: list[str] = field(default_factory=list)
    #: stan każdego przebiegu, po nazwie katalogu wersji. To stąd wiadomo,
    #: która kopia nie dobiegła końca i nadaje się do wznowienia.
    runs: dict[str, VersionState] = field(default_factory=dict)

    @classmethod
    def load(cls, folder: Path) -> Manifest:
        path = Path(folder) / MANIFEST_NAME
        manifest = cls(path=path)
        data: dict = {}
        if path.exists():
            try:
                data = _read_envelope(path)
            except Exception as exc:  # noqa: BLE001
                log.error("Manifest %s jest nieczytelny (%s) — kopia będzie pełna.", path, exc)
                data = {}
        if not data:
            # Bez pełnego manifestu (pierwsza kopia jeszcze się nie domknęła albo
            # manifest jest uszkodzony) każda paczka dziennika jest nowsza od
            # „ostatniego zapisu” — inaczej wznowienie pominęłoby cały dziennik.
            manifest.updated = 0.0
        manifest._apply_data(data)
        manifest._replay_journal()
        manifest._synthesise_legacy_runs()
        log.info(
            "Wczytano manifest: %d wpisów, %d wersji (%d niedokończonych), szyfrowany=%s",
            len(manifest.entries),
            len(manifest.runs),
            sum(1 for r in manifest.runs.values() if not r.complete),
            manifest.encrypted,
        )
        return manifest

    def _apply_data(self, data: dict) -> None:
        if not data:
            return
        manifest = self
        manifest.encrypted = bool(data.get("encrypted", False))
        manifest.created = float(data.get("created", time.time()))
        manifest.updated = float(data.get("updated", time.time()))
        manifest.entries = {
            key: ManifestEntry.from_dict(raw) for key, raw in (data.get("entries") or {}).items()
        }
        manifest.roots = {str(k): str(v) for k, v in (data.get("roots") or {}).items()}
        manifest.versions = [str(v) for v in (data.get("versions") or [])]
        manifest.runs = {
            str(name): VersionState.from_dict(raw)
            for name, raw in (data.get("runs") or {}).items()
        }

    def _replay_journal(self) -> None:
        """Nakłada na manifest zmiany zapisane w dzienniku punktów kontrolnych.

        Paczki starsze niż ostatni pełny zapis manifestu pomijamy: jeśli
        program padł między zapisem manifestu a usunięciem dziennika, stare
        wpisy nie mogą cofnąć nowszego stanu.
        """
        applied = 0
        for stamp, records in ManifestJournal(self.path.parent).frames():
            if stamp <= self.updated:
                continue
            for record in records:
                kind = record.get("t")
                if kind == "set":
                    self.entries[str(record["k"])] = ManifestEntry.from_dict(record["e"])
                elif kind == "del":
                    self.entries.pop(str(record["k"]), None)
                elif kind == "run":
                    run = VersionState.from_dict(record["run"])
                    self.runs[run.name] = run
                    if run.name and run.structure == "dated" and run.name not in self.versions:
                        self.versions.append(run.name)
                elif kind == "rename":
                    self._replay_rename(str(record["from"]), str(record["to"]))
                elif kind == "meta":
                    self.encrypted = bool(record.get("encrypted", self.encrypted))
                    self.roots.update({str(k): str(v) for k, v in (record.get("roots") or {}).items()})
                    for version in record.get("versions") or []:
                        if version not in self.versions:
                            self.versions.append(str(version))
                applied += 1
        if applied:
            log.info("Odtworzono %d zmian z dziennika punktów kontrolnych.", applied)

    def _synthesise_legacy_runs(self) -> None:
        manifest = self
        # Manifest sprzed wprowadzenia stanu przebiegów nie wie nic o tym, czy
        # kopia się domknęła. Dla logiki programu (np. czyszczenia historii)
        # traktujemy taką wersję jak kompletną, ale oznaczamy ją jako „stan
        # nieznany” — interfejs nie może twierdzić, że jest pełna, bo dokładnie
        # tak wyglądała przerwana kopia, od której zaczął się ten problem.
        for name in manifest.versions:
            if name not in manifest.runs:
                manifest.runs[name] = VersionState(
                    name=name, complete=True, structure="dated", known=False
                )

    def incomplete_runs(self, labels: set[str] | None = None) -> list[VersionState]:
        """Niedokończone przebiegi, najnowsze najpierw.

        ``labels`` zawęża wynik do przebiegów dotyczących tych samych katalogów
        źródłowych — do jednego katalogu docelowego potrafi pisać kilka zadań
        i nie wolno zaproponować wznowienia cudzej kopii.
        """
        found = [run for run in self.runs.values() if not run.complete]
        if labels is not None:
            found = [run for run in found if not run.labels or set(run.labels) & labels]
        return sorted(found, key=lambda r: r.started, reverse=True)

    def save(self) -> None:
        self.updated = time.time()
        common = {
            "version": MANIFEST_VERSION,
            "encrypted": self.encrypted,
            "created": self.created,
            "updated": self.updated,
            "roots": self.roots,
            "versions": self.versions,
            "runs": {k: v.to_dict() for k, v in self.runs.items()},
        }
        _write_envelope(
            self.path, {**common, "entries": {k: v.to_dict() for k, v in self.entries.items()}}
        )
        # Podsumowanie zapisujemy **po** manifeście. Gdy zapis zostanie przerwany
        # pomiędzy nimi, podsumowanie jest starsze od manifestu
        # i ``ManifestSummary.load`` je odrzuci — nigdy odwrotnie.
        self.write_summary(len(self.entries), sum(e.size for e in self.entries.values()))
        # Dziennik jest już wchłonięty przez pełny manifest.
        ManifestJournal(self.path.parent).remove()
        self.hide_on_windows()

    def rename_version(self, old: str, new: str) -> int:
        """Przepisuje nazwę katalogu wersji w całym spisie treści.

        Nazwa wersji jest prefiksem ścieżki **każdego** wpisu, więc zmiana
        nazwy katalogu na dysku musi iść w parze z tym przepisaniem — inaczej
        spis treści wskazywałby na katalog, którego już nie ma, a następny
        przebieg skopiowałby całą kopię od nowa.
        """
        prefix, replacement = old + "/", new + "/"
        changed = 0
        for entry in self.entries.values():
            if entry.stored.startswith(prefix):
                entry.stored = replacement + entry.stored[len(prefix) :]
                changed += 1
        self.versions = [new if version == old else version for version in self.versions]
        run = self.runs.pop(old, None)
        if run is not None:
            run.name = new
            self.runs[new] = run
        return changed

    def _replay_rename(self, old: str, new: str) -> None:
        """Zmiana nazwy wersji odtwarzana z dziennika — tylko zgodnie ze stanem dysku.

        Rekord trafia do dziennika **przed** zmianą nazwy katalogu. Jeśli program
        zginął przed nią, katalogu ``new`` nie ma i wpisy muszą dalej wskazywać
        na ``old``; jeśli zginął po niej, katalog ``new`` istnieje i dopiero
        wtedy wolno przepisać wpisy.
        """
        folder = self.path.parent
        if not (folder / new).is_dir() or (folder / old).is_dir():
            return
        changed = self.rename_version(old, new)
        log.info("Odtworzono zmianę nazwy wersji %s -> %s (%d wpisów).", old, new, changed)

    def meta_record(self) -> dict:
        """Rekord dziennika z danymi ogólnymi manifestu."""
        return {"t": "meta", "encrypted": self.encrypted, "roots": dict(self.roots), "versions": list(self.versions)}

    def write_summary(self, entry_count: int, total_bytes: int) -> None:
        """Zapisuje lekkie podsumowanie — także w trakcie kopii, przy punktach kontrolnych."""
        try:
            _write_envelope(
                self.path.with_name(SUMMARY_NAME),
                {
                    "version": MANIFEST_VERSION,
                    "encrypted": self.encrypted,
                    "created": self.created,
                    "updated": time.time(),
                    "roots": self.roots,
                    "versions": self.versions,
                    "runs": {k: v.to_dict() for k, v in self.runs.items()},
                    "entry_count": entry_count,
                    "total_bytes": total_bytes,
                },
            )
        except OSError as exc:
            log.warning("Nie udało się zapisać podsumowania manifestu: %s", exc)

    def hide_on_windows(self) -> None:
        """Oznacza manifest i podsumowanie jako ukryte, żeby nie zaśmiecały widoku kopii."""
        if os.name != "nt":
            return
        for path in (self.path, self.path.with_name(SUMMARY_NAME), self.path.with_name(JOURNAL_NAME)):
            if not path.exists():
                continue
            try:
                import ctypes

                ctypes.windll.kernel32.SetFileAttributesW(str(path), 0x02)  # FILE_ATTRIBUTE_HIDDEN
            except Exception as exc:  # noqa: BLE001 - kosmetyka, nie może przerwać backupu
                log.debug("Nie udało się ukryć %s: %s", path.name, exc)


@dataclass
class ManifestSummary:
    """Lekki odpowiednik manifestu: stan wersji bez listy plików.

    Wczytuje się w milisekundach niezależnie od wielkości kopii, więc interfejs
    może go czytać przy każdej zmianie katalogu docelowego. Manifest dużej kopii
    waży setki megabajtów i jego wczytanie w wątku interfejsu zamrażało okno.
    """

    updated: float = 0.0
    encrypted: bool = False
    entry_count: int = 0
    total_bytes: int = 0
    roots: dict[str, str] = field(default_factory=dict)
    versions: list[str] = field(default_factory=list)
    runs: dict[str, VersionState] = field(default_factory=dict)

    @classmethod
    def load(cls, folder: Path) -> ManifestSummary | None:
        """Podsumowanie albo ``None``, gdy go brak albo jest starsze od manifestu.

        Manifest mógł zostać zapisany przez starszą wersję programu, która
        o podsumowaniu nie wie — wtedy podsumowanie opisuje stan sprzed tego
        zapisu i nie wolno mu wierzyć.
        """
        folder = Path(folder)
        summary_path = folder / SUMMARY_NAME
        try:
            summary_mtime = os.stat(long_path(summary_path)).st_mtime
        except OSError:
            return None
        try:
            manifest_mtime = os.stat(long_path(folder / MANIFEST_NAME)).st_mtime
        except OSError:
            # Pierwsza kopia jeszcze się nie domknęła: pełnego manifestu nie ma,
            # stan żyje w dzienniku i w podsumowaniu zapisanym razem z nim.
            manifest_mtime = 0.0
        if manifest_mtime > summary_mtime + 2.0:
            return None
        try:
            data = _read_envelope(summary_path)
        except Exception as exc:  # noqa: BLE001
            log.warning("Podsumowanie manifestu %s jest nieczytelne: %s", summary_path, exc)
            return None
        return cls(
            updated=float(data.get("updated", 0.0)),
            encrypted=bool(data.get("encrypted", False)),
            entry_count=int(data.get("entry_count", 0)),
            total_bytes=int(data.get("total_bytes", 0)),
            roots={str(k): str(v) for k, v in (data.get("roots") or {}).items()},
            versions=[str(v) for v in (data.get("versions") or [])],
            runs={str(k): VersionState.from_dict(v) for k, v in (data.get("runs") or {}).items()},
        )


class ManifestJournal:
    """Dziennik punktów kontrolnych manifestu — plik wyłącznie dopisywany.

    Każdy punkt kontrolny to jedna paczka rekordów z własną sumą SHA-256
    i znacznikiem czasu, zapisana i utrwalona (``fsync``) w całości. Paczka
    urwana przez wyłączenie komputera jest wykrywana po długości albo sumie
    kontrolnej i wraz ze wszystkim po niej pomijana. Do dziennika trafiają
    wyłącznie pliki już utrwalone na nośniku, więc odtworzenie go nigdy nie
    wpisze do spisu treści pliku, którego nie ma.
    """

    def __init__(self, folder: Path) -> None:
        self.path = Path(folder) / JOURNAL_NAME

    def append(self, records: list[dict]) -> None:
        if not records:
            return
        payload = msgpack.packb(records, use_bin_type=True)
        header = _JOURNAL_HEADER.pack(JOURNAL_MAGIC, time.time(), len(payload), hashlib.sha256(payload).digest())
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(long_path(self.path), "ab") as handle:
            handle.write(header + payload)
            handle.flush()
            os.fsync(handle.fileno())

    def frames(self) -> Iterator[tuple[float, list[dict]]]:
        """Kolejne kompletne paczki ``(czas zapisu, rekordy)``."""
        try:
            handle = open(long_path(self.path), "rb")  # noqa: SIM115 - zamykane w finally
        except FileNotFoundError:
            return
        except OSError as exc:
            log.warning("Nie można odczytać dziennika %s: %s", self.path, exc)
            return
        try:
            while True:
                header = handle.read(_JOURNAL_HEADER.size)
                if len(header) < _JOURNAL_HEADER.size:
                    return
                magic, stamp, size, digest = _JOURNAL_HEADER.unpack(header)
                if magic != JOURNAL_MAGIC:
                    log.warning("Dziennik %s: nieznany nagłówek paczki — pomijam resztę.", self.path)
                    return
                payload = handle.read(size)
                if len(payload) < size:
                    log.info("Dziennik %s: ostatnia paczka niedokończona — pomijam ją.", self.path)
                    return
                if hashlib.sha256(payload).digest() != digest:
                    log.warning("Dziennik %s: uszkodzona paczka — pomijam resztę.", self.path)
                    return
                try:
                    records = msgpack.unpackb(payload, raw=False)
                except Exception as exc:  # noqa: BLE001
                    log.warning("Dziennik %s: nieczytelna paczka (%s) — pomijam resztę.", self.path, exc)
                    return
                yield stamp, records
        finally:
            handle.close()

    def remove(self) -> None:
        with contextlib.suppress(FileNotFoundError):
            try:
                os.unlink(long_path(self.path))
            except PermissionError:
                os.chmod(long_path(self.path), 0o600)
                os.unlink(long_path(self.path))


def _write_envelope(path: Path, data: dict) -> None:
    """Zapis atomowy: magia, wersja formatu, SHA-256 treści, treść msgpack."""
    payload = msgpack.packb(data, use_bin_type=True)
    envelope = (
        MANIFEST_MAGIC + bytes([MANIFEST_VERSION]) + hashlib.sha256(payload).digest() + payload
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with open(long_path(tmp), "wb") as handle:
        handle.write(envelope)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(long_path(tmp), long_path(path))


def _read_envelope(path: Path) -> dict:
    blob = Path(long_path(path)).read_bytes()
    if blob[: len(MANIFEST_MAGIC)] != MANIFEST_MAGIC:
        raise ValueError(tr("nieznany format manifestu"))
    digest = blob[len(MANIFEST_MAGIC) + 1 : len(MANIFEST_MAGIC) + 33]
    payload = blob[len(MANIFEST_MAGIC) + 33 :]
    if hashlib.sha256(payload).digest() != digest:
        raise ValueError(tr("suma kontrolna manifestu się nie zgadza"))
    return msgpack.unpackb(payload, raw=False)
