"""Silnik kopii zapasowych i przywracania.

Zastępuje klasę ``Api`` z ``backend.py`` (1.x), w której:

* ``perform_template_backup`` zawsze kończył się błędem ``'sources'`` — szablon
  zapisywał klucz ``source``, a odczyt szukał ``sources``;
* ``perform_template_restore`` traktował katalogi jak pliki, więc albo kończył
  się ``SameFileError``, albo zwracał „sukces" nie przywróciwszy niczego;
* ``update_file_record`` wpisywał ścieżkę **źródłową** do snapshotu **celu**,
  trwale zanieczyszczając stan;
* zapis snapshotu wykonywał się po **każdym** pliku (złożoność ``O(N²)`` operacji
  wejścia-wyjścia);
* nie istniała żadna kontrola bezpieczeństwa: cel wewnątrz źródła powodował
  rekurencyjne kopiowanie kopii do samej siebie.

Cała warstwa jest niezależna od Qt — komunikuje się przez :class:`Reporter`,
dzięki czemu da się ją testować bez GUI i uruchamiać z wątku roboczego.
"""

from __future__ import annotations

import contextlib
import datetime
import hashlib
import itertools
import os
import re
import shutil
import sys
import threading
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field, replace
from pathlib import Path

from . import beat, chunks, crypto, evidence, locks, proof, rescue, sigelith
from .crypto import ENCRYPTED_SUFFIX, OperationCancelled, PasswordKeyring
from .i18n import isolate, plural, tr
from .log import get_logger
from .parallel import DirectoryCache, resolve_workers, unordered_map
from .paths import (
    MANIFEST_NAME,
    cluster_size,
    contained_path,
    filesystem_name,
    hardlinks_expected,
    long_path,
    make_writable,
    mtime_tolerance,
    on_disk_size,
    set_file_mtime,
    supports_hardlinks,
)
from .snapshot import (
    FileMeta,
    Manifest,
    ManifestEntry,
    ManifestJournal,
    ManifestSummary,
    ScanCancelled,
    SourceRoot,
    VersionState,
    hash_file,
    iter_tree,
    scan_sources,
)

log = get_logger("engine")

COPY_CHUNK = 1024 * 1024
#: Zapas miejsca ponad rozmiar danych, jakiego wymagamy na dysku docelowym.
FREE_SPACE_MARGIN = 1.05
#: Tolerancja przy porównaniu czasu modyfikacji źródła z czasem zapamiętanym
#: w manifeście. Oba pochodzą z tego samego systemu plików, więc wystarczy
#: margines na zaokrąglenia; zbyt ostra wartość kosztuje co najwyżej policzenie
#: sumy kontrolnej, nigdy zbędne kopiowanie.
SOURCE_MTIME_TOLERANCE = 0.01
#: Punkt kontrolny co tyle zapisanych plików albo co tyle sekund — co nastąpi
#: wcześniej. Przy przerwaniu kopii (także wyłączeniu komputera) tracimy
#: najwyżej tyle postępu, a i on zostanie rozpoznany z nośnika przy wznowieniu.
CHECKPOINT_FILES = 2000
CHECKPOINT_SECONDS = 10.0


#: Pauza przed ponowieniem plików zablokowanych — krótkie blokady (skan
#: antywirusowy, klient synchronizacji) zdążą w tym czasie minąć.
LOCK_RETRY_DELAY = 2.0

#: Progi wykrywania masowych zmian (możliwe działanie ransomware). Dobrane tak,
#: by nie reagować na zwykłą pracę: przełączenie gałęzi w repozytorium zmienia
#: setki plików tekstowych, ale ich treść dalej wygląda jak tekst.
MASS_MIN_PREVIOUS = 200
MASS_MIN_CHANGED = 100
MASS_RATIO = 0.20
MASS_SAMPLE = 40
MASS_MIN_EVALUATED = 10
MASS_CONTENT_RATIO = 0.5
MASS_MIN_RENAMED = 50
#: Rozszerzenia, których treść zaczyna się od stałej sygnatury — zaszyfrowany
#: plik ją traci. Dokumenty Office w nowym formacie to archiwa ZIP („PK”).
_MAGIC = {
    ".docx": (b"PK",), ".xlsx": (b"PK",), ".pptx": (b"PK",), ".odt": (b"PK",), ".ods": (b"PK",),
    ".zip": (b"PK",), ".jar": (b"PK",), ".pdf": (b"%PDF",), ".png": (b"\x89PNG",),
    ".jpg": (b"\xff\xd8\xff",), ".jpeg": (b"\xff\xd8\xff",), ".gif": (b"GIF8",),
    ".7z": (b"7z\xbc\xaf",), ".rar": (b"Rar!",), ".bmp": (b"BM",),
    ".doc": (b"\xd0\xcf\x11\xe0",), ".xls": (b"\xd0\xcf\x11\xe0",), ".ppt": (b"\xd0\xcf\x11\xe0",),
}
#: Rozszerzenia z treścią zwykle daleką od losowej — wysoka entropia oznacza
#: zaszyfrowanie albo kompresję, której tu być nie powinno.
_LOW_ENTROPY = {
    ".txt", ".csv", ".md", ".json", ".xml", ".html", ".htm", ".log", ".ini", ".cfg", ".sql",
    ".py", ".js", ".ts", ".java", ".c", ".cpp", ".h", ".cs", ".php", ".rtf", ".tex", ".yaml",
    ".yml", ".svg", ".bat", ".ps1", ".sh", ".wav", ".tif", ".tiff",
}


class EngineError(Exception):
    """Błąd uniemożliwiający wykonanie operacji (walidacja, brak miejsca itp.)."""


class PrivateAppDataTargets(EngineError):
    """Wersja ze Sklepu: przywracanie utworzyłoby nowe foldery prosto w AppData.

    Windows trzyma je w prywatnej kopii pakietu, więc przywrócone pliki widziałby
    tylko ten program — dlatego pytamy, zanim cokolwiek zapiszemy.
    """

    def __init__(self, folders: list[Path]) -> None:
        super().__init__(
            tr("Przywracanie utworzyłoby w AppData nowe foldery, których inne programy nie zobaczą: "
               "{folders}").format(folders=", ".join(str(folder) for folder in folders))
        )
        self.folders = folders


class MassChangeDetected(EngineError):
    """W źródle zmieniło się podejrzanie dużo — kopia wstrzymana do decyzji użytkownika.

    Program widzi cały obraz zmian, zanim cokolwiek zapisze. Gdyby dopisał
    do kopii pliki zaszyfrowane przez ransomware, kopia lustrzana straciłaby
    jedyny dobry egzemplarz, a porządkowanie historii skasowałoby dobre wersje.
    """

    def __init__(self, reasons: list[str]) -> None:
        super().__init__(
            tr("Wstrzymano kopię: w źródle zmieniło się podejrzanie dużo plików. {reasons}").format(
                reasons=" ".join(reasons)
            )
        )
        self.reasons = reasons


class Reporter:
    """Kanał raportowania postępu — celowo bez zależności od Qt."""

    def __init__(
        self,
        on_stage: Callable[[str], None] | None = None,
        on_file: Callable[[str, int, int], None] | None = None,
        on_bytes: Callable[[int], None] | None = None,
        is_cancelled: Callable[[], bool] | None = None,
    ) -> None:
        self._on_stage = on_stage
        self._on_file = on_file
        self._on_bytes = on_bytes
        self._is_cancelled = is_cancelled or (lambda: False)

    def stage(self, text: str) -> None:
        log.info("%s", text)
        if self._on_stage:
            self._on_stage(text)

    def file(self, name: str, index: int, total: int) -> None:
        if self._on_file:
            self._on_file(name, index, total)

    def advance(self, delta: int) -> None:
        if self._on_bytes:
            self._on_bytes(delta)

    @property
    def cancelled(self) -> bool:
        return self._is_cancelled()

    def check_cancel(self) -> None:
        if self.cancelled:
            raise OperationCancelled(tr("Operacja przerwana przez użytkownika."))


@dataclass
class BackupConfig:
    """Parametry pojedynczego przebiegu kopii."""

    sources: list[str]
    destination: str
    structure: str = "dated"  # "dated" = wersje z datą, "mirror" = kopia lustrzana
    encrypt: bool = False
    verify_after_write: bool = True
    excludes: list[str] = field(default_factory=list)
    retention: int = 0
    #: Retencja „kalendarzowa” (GFS): zachowaj najnowszą wersję z każdego z tylu
    #: ostatnich dni, tygodni i miesięcy. Łączy się z ``retention`` — wersja
    #: zostaje, jeśli zatrzymuje ją którakolwiek z zasad. 0 = zasada wyłączona.
    gfs_daily: int = 0
    gfs_weekly: int = 0
    gfs_monthly: int = 0
    thorough: bool = False  # liczy SHA-256 każdego pliku, ignorując mtime
    delete_removed: bool = False  # tylko dla "mirror"
    #: Nazwa istniejącego katalogu wersji, do którego ma trafić ten przebieg.
    #: Pusty napis = utwórz nową wersję z datą. Wskazanie istniejącej wersji
    #: obsługuje trzy rzeczy naraz, bo to ten sam problem: **wznowienie**
    #: przerwanej kopii, **uzupełnienie** kopii o dane powstałe w trakcie jej
    #: wykonywania oraz **nadpisanie** tego, co się w niej rozjechało.
    target_version: str = ""
    #: Ile razy po głównym przebiegu ponowić skan źródła i dograć to, co w tym
    #: czasie przybyło lub się zmieniło. Kopia 500 GB trwa godzinami i źródło
    #: żyje przez cały ten czas. 0 wyłącza dogrywkę.
    catchup_passes: int = 1
    #: Ile plików przetwarzać równocześnie; 0 = dobór automatyczny.
    workers: int = 0
    #: Czy po uzupełnieniu istniejącej wersji dopisać do nazwy jej katalogu
    #: datę tego uzupełnienia (``…--RRRR-MM-DD_@NNN``).
    stamp_updates: bool = True
    #: Użytkownik obejrzał ostrzeżenie o masowych zmianach w źródle i potwierdził,
    #: że są spodziewane (np. aktualizacja programu, przeniesienie danych).
    allow_mass_change: bool = False
    #: Duże pliki zapisuj fragmentami — nowa wersja zapisuje tylko zmienione
    #: fragmenty (patrz :mod:`cleanvault.chunks`).
    delta: bool = True
    #: Oznakuj wersję czasem przez Sigelith — do usługi trafia wyłącznie suma
    #: kontrolna spisu wersji (patrz :mod:`cleanvault.proof`).
    timestamp: bool = False
    #: Chroń dowody Sigelith Desktop: folder danych Sigelith dochodzi do źródeł,
    #: a oznakowane dokumenty trafiają do magazynu dowodów (:mod:`cleanvault.evidence`).
    sigelith: bool = False


@dataclass
class PlannedFile:
    key: str
    source: Path
    meta: FileMeta
    reason: str  # "nowy" | "zmieniony" | "brak w kopii"


@dataclass
class BackupPlan:
    config: BackupConfig
    roots: list[SourceRoot]
    destination: Path
    to_copy: list[PlannedFile]
    unchanged: dict[str, ManifestEntry]
    removed: list[str]
    total_bytes: int
    scanned: int
    warnings: list[str] = field(default_factory=list)
    #: Rozmiar jednostki alokacji nośnika docelowego (0 = nieznany).
    cluster: int = 0
    #: Czy nośnik docelowy obsługuje twarde dowiązania. Gdy nie — każda wersja
    #: z datą jest pełną fizyczną kopią, a nie podpięciem istniejących danych.
    hardlinks: bool = True
    #: Ile miejsca kopia zajmie **naprawdę**: z zaokrągleniem każdego pliku do
    #: pełnych klastrów i z doliczeniem plików, które bez dowiązań trzeba
    #: fizycznie powielić. To ta liczba decyduje, czy kopia się zmieści.
    physical_bytes: int = 0
    #: Nazwa katalogu wersji, do którego pójdzie zapis ("" dla kopii lustrzanej).
    version: str = ""
    #: Czy piszemy do istniejącej już wersji (wznowienie/uzupełnienie).
    resuming: bool = False
    #: Pliki leżące już w docelowej wersji i zgodne ze źródłem — nie wymagają
    #: ani kopiowania, ani dowiązywania. To one sprawiają, że wznowienie nie
    #: przepisuje od nowa tego, co się udało przed przerwaniem.
    adopted: dict[str, ManifestEntry] = field(default_factory=dict)
    #: Dokładność zapisu czasu modyfikacji na nośniku docelowym (w sekundach).
    mtime_tolerance: float = 2.0
    #: Liczba katalogów, które powstaną w nowej wersji (szacunek miejsca).
    directories: int = 0
    #: Ile plików rozpoznano jako przeniesione albo przemianowane w źródle —
    #: trafiają do kopii bez przesyłania danych, samym dowiązaniem.
    moved: int = 0
    #: Powody podejrzenia masowych zmian (ransomware); pusta lista = spokój.
    suspicion: list[str] = field(default_factory=list)

    @property
    def version_prefix(self) -> str:
        return f"{self.version}/" if self.version else ""

    @property
    def transfer_bytes(self) -> int:
        """Ile bajtów faktycznie przepłynie przez dysk — do paska postępu.

        Bez twardych dowiązań niezmienione pliki są kopiowane do nowej wersji
        tak samo jak zmienione, więc muszą być wliczone w postęp. Inaczej pasek
        stałby na 100% przez wiele godzin „podpinania”.
        """
        extra = 0
        if self.config.structure == "dated" and not self.hardlinks:
            extra = sum(entry.size for entry in self.unchanged.values())
        return self.total_bytes + extra

    @property
    def is_empty(self) -> bool:
        return not self.to_copy and not self.removed


@dataclass
class OperationResult:
    ok: bool
    files_done: int = 0
    bytes_done: int = 0
    skipped: int = 0
    errors: list[str] = field(default_factory=list)
    duration: float = 0.0
    output_path: str = ""
    cancelled: bool = False
    #: uwagi, które nie są błędami (np. pliki bez sumy kontrolnej przy weryfikacji)
    notes: list[str] = field(default_factory=list)
    #: pliki pominięte, bo były otwarte na wyłączność w innym programie:
    #: klucz pliku → nazwy programów (pusta lista, gdy nie udało się ustalić)
    locked: dict[str, list[str]] = field(default_factory=dict)
    #: pliki wersji (klucz, rozmiar, SHA-256) — spis do znacznika czasu; tylko
    #: przy włączonym znakowaniu, bo przy milionie plików to niemała lista
    version_files: list[tuple[str, int, str]] = field(default_factory=list)
    #: stan wszystkich wersji w katalogu kopii po przebiegu (klucz "" = kopia
    #: lustrzana) — tabela w notatce ratunkowej ma pokazywać stan faktyczny,
    #: także po przerwaniu, gdy podsumowanie spisu treści jest jeszcze stare
    versions: dict[str, VersionState] = field(default_factory=dict)

    @property
    def summary(self) -> str:
        files = plural(self.files_done, "plik", "pliki", "plików")
        if self.cancelled:
            return tr("Przerwano. Zapisano {count} {files} ({size}).").format(
                count=self.files_done, files=files, size=human_size(self.bytes_done)
            )
        if not self.ok:
            return tr("Zakończono z błędami ({errors}). Zapisano {count} {files}.").format(
                errors=len(self.errors), count=self.files_done, files=files
            )
        text = tr("Gotowe: {count} {files}, {size}, {seconds} s.").format(
            count=self.files_done,
            files=files,
            size=human_size(self.bytes_done),
            seconds=f"{self.duration:.1f}",
        )
        if self.locked:
            text += " " + tr("Pominięto {count} {files}.").format(
                count=len(self.locked), files=open_elsewhere(len(self.locked))
            )
        return text


def open_elsewhere(count: int) -> str:
    """„plik otwarty w innym programie” w formie pasującej do liczby (mianownik/biernik)."""
    return plural(
        count,
        "plik otwarty w innym programie",
        "pliki otwarte w innych programach",
        "plików otwartych w innych programach",
    )


def human_size(num: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(num) < 1024.0 or unit == "TB":
            # po arabsku „4.0 KB” czytałoby się jako „KB 4.0” (i18n.isolate)
            return isolate(f"{num:.0f} {unit}" if unit == "B" else f"{num:.1f} {unit}")
        num /= 1024.0
    return isolate(f"{num:.1f} TB")


# --------------------------------------------------------------------- kopia


def source_roots(config: BackupConfig) -> list[SourceRoot]:
    """Katalogi źródłowe z etykietami — te same, których używa kopia na nośniku."""
    return _validate(config)


def effective_sources(config: BackupConfig) -> list[str]:
    """Źródła szablonu, a przy ochronie dowodów Sigelith — także folder danych Sigelith."""
    sources = list(config.sources)
    if config.sigelith:
        data_dir = sigelith.find_data_dir()
        if data_dir is not None and all(Path(raw).resolve() != data_dir.resolve() for raw in sources):
            sources.append(str(data_dir))
    return sources


def effective_excludes(config: BackupConfig) -> list[str]:
    """Wykluczenia szablonu i — przy ochronie dowodów — pliki Sigelith, których nie kopiujemy."""
    excludes = list(config.excludes)
    if config.sigelith:
        excludes += [pattern for pattern in evidence.SIGELITH_EXCLUDES if pattern not in excludes]
    return excludes


def _validate(config: BackupConfig) -> list[SourceRoot]:
    sources = effective_sources(config)
    if not sources:
        raise EngineError(tr("Nie wskazano żadnego katalogu źródłowego."))
    if not config.destination:
        raise EngineError(tr("Nie wskazano katalogu docelowego."))

    roots: list[SourceRoot] = []
    labels: set[str] = set()
    for raw in sources:
        root = SourceRoot.make(raw)
        if not root.path.is_dir():
            raise EngineError(tr("Katalog źródłowy nie istnieje: {path}").format(path=root.path))
        label = root.label
        suffix = 2
        while root.label in labels:
            # Dwa różne źródła o tej samej nazwie (np. D:\Foto i E:\Foto)
            # muszą trafić do osobnych podkatalogów kopii.
            root = SourceRoot(path=root.path, label=f"{label}_{suffix}")
            suffix += 1
        labels.add(root.label)
        roots.append(root)

    destination = Path(config.destination).resolve()
    for root in roots:
        if destination == root.path:
            raise EngineError(tr("Katalog docelowy nie może być tym samym katalogiem co źródłowy."))
        if _is_inside(destination, root.path):
            raise EngineError(
                tr("Katalog docelowy leży wewnątrz źródła ({path}). "
                   "Kopia kopiowałaby samą siebie w nieskończoność.").format(path=root.path)
            )
        if _is_inside(root.path, destination):
            log.warning("Źródło %s leży wewnątrz katalogu docelowego.", root.path)
    return roots


def _is_inside(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def plan_backup(config: BackupConfig, reporter: Reporter) -> BackupPlan:
    """Ustala, co trzeba skopiować — bez dotykania katalogu docelowego.

    Wynik służy zarówno do trybu podglądu („co się stanie"), jak i do
    właściwego wykonania, więc użytkownik zawsze widzi plan przed zapisem.
    """
    roots = _validate(config)
    destination = Path(config.destination).resolve()
    destination.mkdir(parents=True, exist_ok=True)

    reporter.stage(tr("Skanowanie plików źródłowych…"))
    workers = resolve_workers(config.workers)
    try:
        scanned = scan_sources(
            roots,
            effective_excludes(config),
            progress=lambda label, n: reporter.file(
                tr("{label}: {count} {files}").format(
                    label=label, count=n, files=plural(n, "plik", "pliki", "plików")
                ),
                0,
                0,
            ),
            cancel=lambda: reporter.cancelled,
        )
    except ScanCancelled:
        raise OperationCancelled(tr("Operacja przerwana przez użytkownika.")) from None
    reporter.stage(
        tr("Znaleziono {count} {files}. Porównuję z poprzednią kopią…").format(
            count=len(scanned), files=plural(len(scanned), "plik", "pliki", "plików")
        )
    )

    manifest = Manifest.load(destination)
    tolerance = mtime_tolerance(destination)
    version, resuming = _resolve_version(config, destination, manifest)
    version_prefix = f"{version}/" if version else ""

    to_copy: list[PlannedFile] = []
    unchanged: dict[str, ManifestEntry] = {}
    adopted: dict[str, ManifestEntry] = {}
    warnings: list[str] = []
    moved_count = 0
    roots_by_label = {r.label: r for r in roots}
    total_bytes = 0

    # Pliki, które zniknęły ze źródła, są kandydatami na „to samo, tylko gdzie
    # indziej”. Przeniesienie katalogu nie zmienia ani rozmiaru, ani czasu
    # modyfikacji plików, więc po tej parze znajdujemy kandydata natychmiast,
    # a dopiero potem potwierdzamy go sumą kontrolną.
    vanished = _moved_candidates(manifest, scanned, {root.label for root in roots})

    # Pliki rozstrzygalne bez dotykania dysku (nowe pliki w nowej wersji) idą
    # od razu do planu. Reszta wymaga zajrzenia na nośnik albo policzenia sumy
    # kontrolnej — to robimy równolegle, bo przy wznawianiu kopii setek tysięcy
    # plików jedno zapytanie do dysku USB na plik zajmowało minuty.
    needs_io: list[tuple[str, FileMeta, Path, ManifestEntry | None, bool]] = []
    for key, meta in scanned.items():
        source_path = _source_path(key, roots_by_label)
        if source_path is None:
            continue
        previous = manifest.entries.get(key)
        check_medium = resuming or (not version and previous is None)
        looks_moved = previous is None and _moved_key(meta.size, meta.mtime) in vanished
        if previous is None and not check_medium and not looks_moved:
            to_copy.append(PlannedFile(key=key, source=source_path, meta=meta, reason="nowy"))
            total_bytes += meta.size
            continue
        needs_io.append((key, meta, source_path, previous, check_medium))

    def classify(candidate: tuple[str, FileMeta, Path, ManifestEntry | None, bool]) -> tuple[str, object]:
        key, meta, source_path, previous, check_medium = candidate
        reporter.check_cancel()
        if check_medium:
            # Wznowienie nie ufa manifestowi — manifest mógł nie zostać zapisany
            # (twarde zabicie procesu, zanik zasilania). Pytamy sam nośnik:
            # czy plik leży już w docelowej wersji i czy zgadza się ze źródłem.
            # Kopia lustrzana ma zawsze jeden katalog, więc tam pytamy o każdy
            # plik nieznany manifestowi — to jest jej „wznowienie”.
            existing = _adoptable(
                destination, version_prefix + key + planned_suffix(config, meta.size),
                meta, config, previous, tolerance,
            )
            if existing is not None:
                return "adopted", existing
        if previous is None:
            moved = _recognise_moved(destination, vanished, meta, source_path, reporter)
            if moved is not None:
                return "moved", moved
            return "copy", PlannedFile(key=key, source=source_path, meta=meta, reason="nowy")
        if not _stored_exists(destination, previous):
            return "copy", PlannedFile(key=key, source=source_path, meta=meta, reason="brak w kopii")
        if config.thorough or not meta.same_stat_as(
            FileMeta(previous.size, previous.mtime, previous.sha256), SOURCE_MTIME_TOLERANCE
        ):
            # Metadane się różnią (albo wymuszono tryb dokładny) — dopiero teraz
            # liczymy SHA-256. To jest cały sekret szybkości kopii przyrostowej.
            try:
                digest = hash_file(source_path, cancel=lambda: reporter.cancelled)
            except ScanCancelled:
                raise OperationCancelled(tr("Operacja przerwana przez użytkownika.")) from None
            except OSError as exc:
                return "warning", tr("{name}: nie można odczytać ({error})").format(key=key, name=key, error=exc)
            if digest != previous.sha256:
                return "copy", PlannedFile(
                    key=key, source=source_path, meta=FileMeta(meta.size, meta.mtime, digest), reason="zmieniony"
                )
        return "unchanged", previous

    for candidate, outcome, error in unordered_map(classify, needs_io, workers, lambda: reporter.cancelled):
        if error is not None:
            raise error
        kind, value = outcome
        key = candidate[0]
        if kind == "adopted":
            adopted[key] = value
        elif kind == "moved":
            unchanged[key] = value
            moved_count += 1
        elif kind == "copy":
            to_copy.append(value)
            total_bytes += value.meta.size
        elif kind == "warning":
            warnings.append(value)
        else:
            unchanged[key] = value
    reporter.check_cancel()
    to_copy.sort(key=lambda item: item.key)

    own_labels = {root.label for root in roots}
    # Wpisy cudzych zadań piszących do tego samego katalogu nie są „usunięte ze
    # źródła" — po prostu nie należą do tego przebiegu i nic nam do nich.
    removed = [
        key
        for key in manifest.entries
        if key not in scanned and key.partition("/")[0] in own_labels
    ]

    if moved_count:
        reporter.stage(
            tr("Pliki przeniesione w źródle: {count} — trafią do kopii bez przesyłania danych.").format(
                count=moved_count
            )
        )
    if resuming:
        reporter.stage(
            tr("Wznawiam wersję {version} — już zapisane: {done}, do dogrania: {todo}.").format(
                version=version,
                done=len(adopted),
                todo=len(to_copy),
            )
        )

    plan = BackupPlan(
        config=config,
        roots=roots,
        destination=destination,
        to_copy=to_copy,
        unchanged=unchanged,
        removed=removed,
        total_bytes=total_bytes,
        scanned=len(scanned),
        warnings=warnings,
        version=version,
        resuming=resuming,
        adopted=adopted,
        mtime_tolerance=tolerance,
        moved=moved_count,
    )
    previous = sum(1 for key in manifest.entries if key.partition("/")[0] in own_labels)
    plan.suspicion = _mass_change_suspicion(plan, previous)
    if plan.suspicion:
        plan.warnings.append(
            tr("Uwaga: w źródle zmieniło się podejrzanie dużo plików — {reasons}").format(
                reasons=" ".join(plan.suspicion)
            )
        )
    _measure_medium(plan)
    _check_free_space(plan)
    return plan


def _mass_change_suspicion(plan: BackupPlan, previous: int) -> list[str]:
    """Czy zmiany w źródle wyglądają na działanie ransomware — lista powodów.

    Trzy sygnały, każdy tani, bo program i tak ma pełny obraz zmian:

    * **skala** — jaka część plików z poprzedniej kopii zmieniła się albo zniknęła;
    * **treść** — w próbce zmienionych plików: dokument, który przestał zaczynać
      się sygnaturą swojego formatu (``PK`` dla .docx), albo plik tekstowy
      o treści nieodróżnialnej od losowej;
    * **nazwy** — wiele plików zniknęło i pojawiło się z dopisaną końcówką
      (``raport.docx`` → ``raport.docx.locked``), co robi większość ransomware.

    Sama skala nie wystarcza (aktualizacja programu też zmienia tysiące plików),
    więc do alarmu potrzebna jest skala i treść albo nazwy — albo bardzo mocny
    sygnał treści.
    """
    changed = [item for item in plan.to_copy if item.reason == "zmieniony"]
    removed = set(plan.removed)
    touched = len(changed) + len(removed)
    scale = previous >= MASS_MIN_PREVIOUS and touched >= MASS_MIN_CHANGED and touched / previous >= MASS_RATIO

    evaluated = suspicious = 0
    for item in changed[:MASS_SAMPLE]:
        verdict = _content_looks_encrypted(item)
        if verdict is None:
            continue
        evaluated += 1
        suspicious += verdict
    content_ratio = suspicious / evaluated if evaluated else 0.0
    content = evaluated >= MASS_MIN_EVALUATED and content_ratio >= MASS_CONTENT_RATIO
    content_strong = evaluated >= 2 * MASS_MIN_EVALUATED and content_ratio >= 0.8

    renamed = sum(
        1 for item in plan.to_copy
        if item.reason == "nowy" and item.key.rpartition(".")[0] in removed
    )
    names = renamed >= MASS_MIN_RENAMED and renamed >= 0.5 * max(1, len(removed))

    if not ((scale and (content or names)) or content_strong or names):
        return []
    reasons = []
    if scale:
        reasons.append(
            tr("Zmieniło się albo zniknęło {count} z {previous} plików poprzedniej kopii.").format(
                count=touched, previous=previous
            )
        )
    if content or content_strong:
        reasons.append(
            tr("{suspicious} z {evaluated} sprawdzonych zmienionych plików ma treść, która nie "
               "pasuje do ich typu (wygląda na zaszyfrowaną).").format(
                suspicious=suspicious, evaluated=evaluated
            )
        )
    if names:
        reasons.append(
            tr("Pliki z końcówką dopisaną do nazwy, których oryginały zniknęły: {count}.").format(
                count=renamed
            )
        )
    return reasons


def _content_looks_encrypted(item: PlannedFile) -> bool | None:
    """Czy początek pliku wygląda na zaszyfrowany; ``None`` — nie da się ocenić."""
    suffix = item.source.suffix.lower()
    if suffix not in _MAGIC and suffix not in _LOW_ENTROPY:
        return None
    try:
        with open(long_path(item.source), "rb") as handle:
            head = handle.read(64 * 1024)
    except OSError:
        return None
    if len(head) < 64:
        return None
    if suffix in _MAGIC:
        return not head.startswith(_MAGIC[suffix])
    return _entropy(head) > 7.8


def _entropy(data: bytes) -> float:
    """Entropia Shannona w bitach na bajt: tekst ~4–5, dane zaszyfrowane ~8."""
    import math
    from collections import Counter

    total = len(data)
    return -sum(n / total * math.log2(n / total) for n in Counter(data).values())


def _resolve_version(
    config: BackupConfig, destination: Path, manifest: Manifest
) -> tuple[str, bool]:
    """Ustala katalog wersji dla tego przebiegu i czy jest to wznowienie.

    Zwraca ``("", False)`` dla kopii lustrzanej, która z definicji ma jeden
    katalog. Dla wersji z datą: albo świeży znacznik czasu, albo — gdy
    użytkownik wskazał ``target_version`` — istniejący katalog, do którego
    dopisujemy brakujące pliki.
    """
    if config.structure != "dated":
        return "", bool(config.target_version)

    if config.target_version:
        name = config.target_version
        if not (destination / name).is_dir() and name not in manifest.runs:
            raise EngineError(
                tr("Nie ma wersji kopii o nazwie {name} w katalogu {path}.").format(
                    name=repr(name), path=destination
                )
            )
        return name, True

    stamp = beat.stamp()
    # Dwie kopie w tym samym beacie (86,4 s) nie mogą wpaść do jednego katalogu —
    # druga nadpisałaby pliki pierwszej i zafałszowała historię wersji.
    unique, counter = stamp, 1
    while (destination / unique).exists():
        counter += 1
        unique = f"{stamp}_{counter}"
    return unique, False


def _moved_key(size: int, mtime: float) -> tuple[int, int]:
    """Klucz kandydata: rozmiar i czas modyfikacji z dokładnością do milisekundy."""
    return size, round(mtime * 1000)


def _moved_candidates(
    manifest: Manifest, scanned: dict[str, FileMeta], own_labels: set[str]
) -> dict[tuple[int, int], list[ManifestEntry]]:
    """Wpisy plików, które zniknęły ze źródła, pogrupowane po rozmiarze i czasie.

    Przeniesienie albo przemianowanie pliku wygląda dziś dla programu jak
    skasowanie jednego pliku i pojawienie się drugiego — a więc jak kopiowanie
    od nowa. Przeniesienie katalogu z gigabajtami danych kosztowało tyle, co
    pierwsza kopia. Kandydatów szukamy tylko wśród wpisów, które mają zapisaną
    sumę kontrolną: bez niej nie dałoby się potwierdzić, że to ten sam plik.
    """
    candidates: dict[tuple[int, int], list[ManifestEntry]] = {}
    for key, entry in manifest.entries.items():
        if key in scanned or not entry.sha256:
            continue
        if key.partition("/")[0] not in own_labels:
            continue
        candidates.setdefault(_moved_key(entry.size, entry.mtime), []).append(entry)
    return candidates


def _recognise_moved(
    destination: Path,
    candidates: dict[tuple[int, int], list[ManifestEntry]],
    meta: FileMeta,
    source_path: Path,
    reporter: Reporter,
) -> ManifestEntry | None:
    """Czy ten „nowy” plik to plik, który już jest w kopii, tylko pod inną ścieżką.

    Zgodność rozmiaru i czasu modyfikacji wskazuje kandydata, ale **decyduje
    suma kontrolna**: bez niej wystarczyłyby dwa pliki tej samej wielkości
    zapisane w tej samej milisekundzie, żeby do kopii trafiła treść zupełnie
    innego pliku.
    """
    possible = candidates.get(_moved_key(meta.size, meta.mtime))
    if not possible:
        return None
    try:
        digest = hash_file(source_path, cancel=lambda: reporter.cancelled)
    except ScanCancelled:
        raise OperationCancelled(tr("Operacja przerwana przez użytkownika.")) from None
    except OSError:
        return None
    for entry in possible:
        if entry.sha256 == digest and _stored_exists(destination, entry):
            return ManifestEntry(
                size=meta.size,
                mtime=meta.mtime,
                sha256=digest,
                stored=entry.stored,
                stored_size=entry.stored_size,
                chunked=entry.chunked,
            )
    return None


def _apply_update_stamp(plan: BackupPlan, manifest: Manifest, reporter: Reporter) -> None:
    """Dopisuje do nazwy katalogu wersji datę bieżącego uzupełnienia.

    ``2026-09-17_@687`` staje się ``2026-09-17_@687--2026-09-24_@921``: data
    utworzenia zostaje z przodu (więc sortowanie po nazwie dalej jest
    chronologiczne), a data uzupełnienia jest **podmieniana**, nie doklejana
    kolejny raz.

    Nazwa wersji jest prefiksem ścieżki każdego wpisu spisu treści, więc jest to
    najwrażliwsza operacja w programie. Kolejność jest taka, by po awarii dało
    się rozpoznać stan po samym dysku: najpierw zamiar do dziennika punktów
    kontrolnych, potem zmiana nazwy katalogu, na końcu przepisanie wpisów.
    """
    old = plan.version
    base = old.partition(VERSION_UPDATE_SEPARATOR)[0]
    now = beat.stamp()
    if base.startswith(now):
        # Uzupełnienie w tym samym beacie, w którym wersja powstała — dopisek
        # „--ten sam znacznik” niczego by nie mówił, a zaśmiecałby nazwę.
        return
    new = f"{base}{VERSION_UPDATE_SEPARATOR}{now}"
    if new == old:
        return
    destination = plan.destination
    if (destination / new).exists():
        log.warning("Nie zmieniam nazwy wersji — katalog %s już istnieje.", new)
        return

    ManifestJournal(destination).append([{"t": "rename", "from": old, "to": new}])
    try:
        os.rename(long_path(destination / old), long_path(destination / new))
    except OSError as exc:
        # Katalog bywa otwarty w Eksploratorze albo zajęty przez inny program.
        # To nie jest powód, żeby kopia się nie udała — zostaje stara nazwa,
        # a rekord z dziennika i tak nie zadziała, bo nowego katalogu nie ma.
        log.warning("Nie udało się zmienić nazwy wersji %s na %s: %s", old, new, exc)
        return

    manifest.rename_version(old, new)
    _rewrite_version_prefix(plan.adopted, old, new)
    _rewrite_version_prefix(plan.unchanged, old, new)
    plan.version = new
    reporter.stage(tr("Wersja kopii nosi teraz nazwę {name}.").format(name=new))


def _rewrite_version_prefix(entries: dict[str, ManifestEntry], old: str, new: str) -> None:
    prefix, replacement = old + "/", new + "/"
    for entry in entries.values():
        if entry.stored.startswith(prefix):
            entry.stored = replacement + entry.stored[len(prefix) :]


def _adoptable(
    destination: Path,
    stored_rel: str,
    meta: FileMeta,
    config: BackupConfig,
    previous: ManifestEntry | None,
    tolerance: float = 2.0,
) -> ManifestEntry | None:
    """Czy plik leży już w docelowej wersji i zgadza się z dzisiejszym źródłem.

    To jest serce wznawiania. Po przerwanej kopii dziesiątki tysięcy plików
    są już zapisane — pytanie tylko *które*. Odpowiedzi udziela nośnik, a nie
    manifest, bo manifest mógł w ogóle nie zostać zapisany.

    Rozstrzyga czas modyfikacji **zapisanego** pliku porównany ze źródłem:
    kopiowanie przenosi znacznik czasu ze źródła, więc plik zapisany, a potem
    zmieniony w źródle, ma inny ``mtime`` i zostanie dograny ponownie. Dzięki
    temu ta sama ścieżka kodu obsługuje też uzupełnianie kopii o zmiany
    powstałe w trakcie jej wykonywania.

    Zapis jest atomowy (``.part`` + ``os.replace``), więc plik pod nazwą
    docelową jest zawsze kompletny — nie ma ryzyka uznania obciętego pliku
    za gotowy.
    """
    path = Path(long_path(destination / stored_rel))
    try:
        st = path.stat()
    except OSError:
        return None

    if abs(st.st_mtime - meta.mtime) > tolerance:
        return None
    chunked = _is_recipe_path(stored_rel)
    sha = previous.sha256 if previous is not None and previous.stored == stored_rel else ""
    if chunked:
        if not config.encrypt:
            # Przepis jawny mówi, jak duży plik opisuje — i jaką ma sumę.
            try:
                recipe = chunks.read_recipe(path, None)
            except (OSError, crypto.CryptoError):
                return None
            if recipe.size != meta.size:
                return None
            sha = recipe.sha256
    elif not config.encrypt and st.st_size != meta.size:
        return None

    return ManifestEntry(
        size=meta.size,
        mtime=meta.mtime,
        sha256=sha,
        stored=stored_rel,
        stored_size=st.st_size,
        chunked=chunked,
    )


def _measure_medium(plan: BackupPlan) -> None:
    """Ustala realny koszt kopii na konkretnym nośniku docelowym.

    Sama suma rozmiarów plików jest złym oszacowaniem z dwóch powodów:

    * **klaster.** Każdy plik zajmuje wielokrotność jednostki alokacji.
      Nośnik sformatowany jako exFAT z klastrem 256 KB przy dziesiątkach
      tysięcy małych plików potrafi zająć dwa razy więcej, niż wynosi suma ich
      rozmiarów;
    * **twarde dowiązania.** Wersjonowanie z datą zakłada, że plik niezmieniony
      podpinamy do nowej wersji za darmo. Na exFAT/FAT dowiązań nie ma, więc
      ``_link_into_version`` po cichu kopiuje plik jeszcze raz — i każda wersja
      jest pełną kopią.
    """
    plan.cluster = cluster_size(plan.destination)
    plan.hardlinks = supports_hardlinks(plan.destination)

    needed = sum(on_disk_size(item.meta.size, plan.cluster) for item in plan.to_copy)
    if plan.resuming or not plan.version:
        # Plik zapisywany w miejsce już istniejącego (wznowienie, uzupełnienie,
        # kopia lustrzana) zwalnia miejsce poprzednika. Bez tego odliczenia
        # uzupełnienie wersji o kilka zmienionych dużych plików wymagało tyle
        # wolnego miejsca, jakby kopia powstawała od zera.
        for item in plan.to_copy:
            suffix = planned_suffix(plan.config, item.meta.size)
            try:
                st = os.stat(long_path(plan.destination / (plan.version_prefix + item.key + suffix)))
            except OSError:
                continue
            needed -= on_disk_size(st.st_size, plan.cluster)
        needed = max(0, needed)
    if plan.config.structure == "dated" and not plan.hardlinks and plan.unchanged:
        duplicated = sum(on_disk_size(entry.size, plan.cluster) for entry in plan.unchanged.values())
        needed += duplicated
        plan.warnings.append(
            tr("Nośnik docelowy ({filesystem}) nie obsługuje twardych dowiązań, więc każda "
               "wersja z datą jest pełną kopią. Te {count} niezmienionych plików zostanie "
               "powielone ({size}). Rozważ układ „kopia lustrzana” albo nośnik NTFS.").format(
                filesystem=filesystem_name(plan.destination) or tr("ten system plików"),
                count=len(plan.unchanged),
                size=human_size(duplicated),
            )
        )
    if plan.cluster > 0 and plan.version and not plan.resuming:
        # Każdy katalog nowej wersji to co najmniej jedna jednostka alokacji.
        # Na exFAT z klastrem 256 KB 400 tys. katalogów to prawie 100 GB,
        # których wcześniejszy szacunek w ogóle nie widział.
        folders: set[str] = set()
        for key in itertools.chain((item.key for item in plan.to_copy), plan.unchanged):
            parent = key.rpartition("/")[0]
            while parent and parent not in folders:
                folders.add(parent)
                parent = parent.rpartition("/")[0]
        plan.directories = len(folders)
        needed += len(folders) * plan.cluster
    plan.physical_bytes = needed

    if plan.cluster > 0 and plan.total_bytes:
        overhead = needed - plan.total_bytes
        if overhead > plan.total_bytes * 0.15:
            plan.warnings.append(
                tr("Klaster nośnika to {cluster} — pliki zajmą {actual} zamiast {logical} "
                   "(narzut {overhead}).").format(
                    cluster=human_size(plan.cluster),
                    actual=human_size(needed),
                    logical=human_size(plan.total_bytes),
                    overhead=human_size(overhead),
                )
            )


def _check_free_space(plan: BackupPlan) -> None:
    try:
        usage = shutil.disk_usage(plan.destination)
    except OSError as exc:  # pragma: no cover - zależne od nośnika
        log.warning("Nie udało się sprawdzić wolnego miejsca: %s", exc)
        return
    required = plan.physical_bytes or plan.total_bytes
    needed = int(required * FREE_SPACE_MARGIN)
    if usage.free < needed:
        raise EngineError(
            tr("Za mało miejsca w katalogu docelowym. Potrzeba ok. {needed}, dostępne {free}.").format(
                needed=human_size(needed), free=human_size(usage.free)
            )
        )
    if required and usage.free < required * 2:
        plan.warnings.append(
            tr("Po wykonaniu kopii zostanie mało wolnego miejsca ({free}).").format(
                free=human_size(usage.free)
            )
        )


def _source_path(key: str, roots_by_label: dict[str, SourceRoot]) -> Path | None:
    label, _, rel = key.partition("/")
    root = roots_by_label.get(label)
    if root is None:
        return None
    return root.path / rel.replace("/", os.sep)


def _stored_exists(destination: Path, entry: ManifestEntry) -> bool:
    if not entry.stored:
        return False
    return Path(long_path(destination / entry.stored)).exists()


def run_backup(plan: BackupPlan, keyring: PasswordKeyring | None, reporter: Reporter) -> OperationResult:
    """Wykonuje plan, a potem dogrywa to, co w międzyczasie zmieniło się w źródle.

    Kopia kilkuset gigabajtów trwa godzinami i przez cały ten czas użytkownik
    pracuje na tych samych plikach. Plan powstał na samym początku, więc w chwili
    zakończenia zapisu jest już nieaktualny: część plików przybyła, część
    zmieniła się po tym, jak je odczytaliśmy. Przebieg uzupełniający skanuje
    źródło ponownie i dogrywa różnicę **do tej samej wersji kopii**, zamiast
    zostawiać ją do następnego razu.
    """
    if plan.suspicion and not plan.config.allow_mass_change:
        raise MassChangeDetected(plan.suspicion)
    started_all = time.monotonic()
    result = _run_backup_pass(plan, keyring, reporter)
    if plan.config.catchup_passes > 0 and not result.cancelled:
        _run_catchup(plan, result, keyring, reporter)
    result.duration = time.monotonic() - started_all
    result.ok = not result.errors and not result.cancelled
    if result.locked:
        result.notes.append(
            tr("Pliki otwarte w innych programach nie trafiły do kopii: {files}. Zamknij te "
               "programy i uruchom kopię ponownie — dograne zostaną tylko te pliki.").format(
                files=locks.describe(result.locked)
            )
        )
    if plan.config.timestamp and not result.cancelled and result.version_files:
        _seal_version(plan, result, reporter, keyring)
    if plan.config.sigelith and not result.cancelled:
        _protect_evidence(plan, result, keyring, reporter)
    # Także po przerwaniu: notatka opisuje katalog i mówi wprost, która wersja
    # jest niedokończona — to najważniejsza informacja dla kogoś bez programu.
    encrypted = plan.config.encrypt or any(v.encrypted for v in result.versions.values())
    rescue.write_rescue_files(plan.destination, result.versions, encrypted)
    return result


def _protect_evidence(
    plan: BackupPlan, result: OperationResult, keyring: PasswordKeyring | None, reporter: Reporter
) -> None:
    """Zabezpiecza dokumenty oznakowane w Sigelith Desktop — nigdy nie psuje samej kopii."""
    data_dir = sigelith.find_data_dir()
    if data_dir is None:
        result.notes.append(tr("Dowody Sigelith: na tym komputerze nie ma jeszcze Sigelith Desktop — "
                               "ochrona zacznie działać sama, gdy się pojawi."))
        return
    reporter.stage(tr("Zabezpieczam dokumenty oznakowane w Sigelith…"))
    try:
        summary = evidence.protect(
            plan.destination, sigelith.load_stamps(data_dir), plan.roots,
            keyring if plan.config.encrypt else None, reporter,
        )
    except (OSError, crypto.CryptoError, EngineError) as exc:
        log.warning("Magazyn dowodów Sigelith: %s", exc)
        result.notes.append(tr("Dowodów Sigelith nie udało się zabezpieczyć: {error}").format(error=exc))
        return
    result.notes.append(summary.describe())


def _seal_version(
    plan: BackupPlan, result: OperationResult, reporter: Reporter,
    keyring: PasswordKeyring | None = None,
) -> None:
    """Znacznik czasu dla świeżej wersji i uzupełnienie potwierdzeń starszych.

    Sieć bywa niedostępna — wtedy pieczęć czeka i zostanie wysłana przy następnej
    kopii. Nigdy nie jest to błąd kopii: dane są bezpieczne i bez znacznika.
    """
    folder = plan.destination / plan.version if plan.version else plan.destination
    client = proof.BeatTimeClient()
    reporter.stage(tr("Znakuję wersję czasem Sigelith (wysyłana jest tylko suma kontrolna)…"))
    try:
        seal = proof.seal_version(folder, result.version_files, client)
    except (OSError, proof.ProofError) as exc:
        log.warning("Znacznik czasu pominięty: %s", exc)
        result.notes.append(tr("Znacznika czasu nie udało się zapisać: {error}").format(error=exc))
        return
    if seal.status == "pending":
        result.notes.append(
            tr("Znacznik czasu czeka na połączenie z Sigelith — zostanie wysłany przy następnej kopii.")
        )
    # Starsze wersje: odłożone znaczniki i podpisy tygodni, które się już zamknęły.
    for name in sorted(_version_dirs(plan.destination), reverse=True)[:8]:
        if name == plan.version:
            continue
        with contextlib.suppress(OSError, proof.ProofError):
            proof.refresh(plan.destination / name, client)
    _sample_audit(plan, result, reporter, keyring)


def _sample_audit(
    plan: BackupPlan, result: OperationResult, reporter: Reporter,
    keyring: PasswordKeyring | None,
) -> None:
    """Próbka plików jednej starszej, podpisanej wersji porównana z pieczęcią (audit.py).

    Kilkadziesiąt plików po każdej kopii: kto podmienia kopię (ransomware, włamanie do
    chmury, psujący się dysk), zostaje wykryty, zanim kopia będzie potrzebna — nawet
    jeśli poprawił też spis treści, bo wzorcem jest pieczęć w publicznym dzienniku.
    """
    import random

    from . import audit

    try:
        signed = [
            version for version in audit.sealed_versions(plan.destination)
            if version != plan.version
            and getattr(proof.read_seal(audit.version_folder(plan.destination, version)), "status", "") == "signed"
        ]
        if not signed:
            return
        version = random.choice(signed)
        reporter.stage(tr("Sprawdzam próbkę starszej wersji z pieczęcią w publicznym dzienniku…"))
        checked = audit.audit_version(plan.destination, version, keyring, reporter, sample=audit.SAMPLE_FILES)
    except (audit.AuditNeedsPassword, OSError, proof.ProofError, ValueError) as exc:
        log.info("Audyt próbki pominięty: %s", exc)
        return
    if checked.cancelled or not checked.sealed:
        return
    label = beat.describe(version) if version else tr("kopia lustrzana")
    if checked.intact:
        result.notes.append(tr("Audyt z pieczęcią: próbka wersji {label} zgodna z publicznym dziennikiem.").format(
            label=label))
    else:
        result.notes.append(tr("UWAGA — audyt z pieczęcią, wersja {label}: {details}").format(
            label=label, details=checked.describe()))


def _pause(seconds: float, reporter: Reporter) -> None:
    """Czeka, reagując na przerwanie co 0,1 s."""
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline and not reporter.cancelled:
        time.sleep(min(0.1, max(0.0, deadline - time.monotonic())))


def _run_catchup(
    plan: BackupPlan,
    result: OperationResult,
    keyring: PasswordKeyring | None,
    reporter: Reporter,
) -> None:
    """Skanuje źródło ponownie i dogrywa różnicę do tej samej wersji kopii.

    Przebiegów jest skończenie wiele — plik zapisywany bez przerwy (dziennik,
    baza danych, maszyna wirtualna) nigdy nie ustabilizuje się na tyle, by
    kolejny skan wyszedł pusty, a kopia nie może kręcić się w kółko.
    """
    config = plan.config
    passes = max(0, config.catchup_passes)
    for attempt in range(1, passes + 1):
        if reporter.cancelled:
            break
        reporter.stage(
            tr("Sprawdzam, co zmieniło się w źródle w trakcie kopii "
               "(przebieg uzupełniający {attempt} z {passes})…").format(
                attempt=attempt, passes=passes
            )
        )
        # Nazwę wersji zmienia wyłącznie przebieg główny; dogrywka pisze już
        # do katalogu pod nową nazwą.
        follow_config = replace(config, target_version=plan.version, catchup_passes=0, stamp_updates=False)
        try:
            follow_plan = plan_backup(follow_config, reporter)
        except OperationCancelled:
            result.cancelled = True
            break
        except EngineError as exc:
            result.errors.append(tr("Przebieg uzupełniający: {error}").format(error=exc))
            break

        if not follow_plan.to_copy:
            reporter.stage(tr("Źródło nie zmieniło się w trakcie kopii — nie ma czego uzupełniać."))
            break

        reporter.stage(
            tr("Uzupełniam kopię o pliki, które przybyły lub zmieniły się w trakcie: "
               "{count} ({size})…").format(
                count=len(follow_plan.to_copy),
                size=human_size(follow_plan.total_bytes),
            )
        )
        # Plik, który dostaje drugą szansę, nie może zostawić po sobie błędu
        # z pierwszego podejścia — liczy się stan końcowy kopii, a nie to, ile
        # razy nośnik po drodze odmówił.
        retried = {item.key for item in follow_plan.to_copy}
        stale = [msg for msg in result.errors if msg.partition(":")[0] in retried]
        if stale:
            result.errors = [msg for msg in result.errors if msg not in stale]
            result.skipped = max(0, result.skipped - len(stale))

        extra = _run_backup_pass(follow_plan, keyring, reporter)
        if extra.versions:
            result.versions = extra.versions
        if extra.version_files:
            result.version_files = extra.version_files
        for key in [key for key in result.locked if key in retried and key not in extra.locked]:
            del result.locked[key]  # plik zwolniony w międzyczasie — dogrywka go zapisała
        result.locked.update(extra.locked)
        result.files_done += extra.files_done
        result.bytes_done += extra.bytes_done
        result.skipped += extra.skipped
        result.errors.extend(extra.errors)
        if extra.cancelled:
            result.cancelled = True
            break
    else:
        if passes:
            log.info("Wyczerpano limit przebiegów uzupełniających (%d).", passes)


class _Checkpoints:
    """Utrwala postęp kopii w dzienniku manifestu co kilka tysięcy plików albo sekund.

    Pełny manifest dużej kopii waży setki megabajtów, więc zapisujemy go tylko
    po zakończeniu przebiegu. W trakcie — i przy przerwaniu, także przy
    wyłączaniu komputera — wystarczy dopisać do dziennika wpisy plików, które
    już leżą na nośniku. To trwa ułamek sekundy zamiast kilkudziesięciu.
    """

    def __init__(self, manifest: Manifest, run_state: VersionState) -> None:
        self.manifest = manifest
        self.run_state = run_state
        self.journal = ManifestJournal(manifest.path.parent)
        self.base = manifest.entries
        self.entry_count = len(manifest.entries)
        self.total_bytes = sum(entry.size for entry in manifest.entries.values())
        self.records: list[dict] = []
        self.last = time.monotonic()

    def start(self) -> None:
        self.journal.append([self.manifest.meta_record(), self._run_record()])
        self.manifest.write_summary(self.entry_count, self.total_bytes)
        self.manifest.hide_on_windows()
        self.last = time.monotonic()

    def set(self, key: str, entry: ManifestEntry) -> None:
        old = self.base.get(key)
        if old is None:
            self.entry_count += 1
            self.total_bytes += entry.size
        else:
            self.total_bytes += entry.size - old.size
        self.records.append({"t": "set", "k": key, "e": entry.to_dict()})

    def note(self, key: str, entry: ManifestEntry) -> None:
        """Uwzględnia wpis w licznikach podsumowania bez zapisu do dziennika.

        Dotyczy plików rozpoznanych na nośniku przy wznawianiu — ich stan
        i tak zostanie ponownie odczytany z dysku, a wrzucenie setek tysięcy
        takich wpisów do dziennika tylko opóźniałoby start kopii.
        """
        if self.base.get(key) is None:
            self.entry_count += 1
            self.total_bytes += entry.size

    def delete(self, key: str) -> None:
        old = self.base.get(key)
        if old is not None:
            self.entry_count -= 1
            self.total_bytes -= old.size
        self.records.append({"t": "del", "k": key})

    def maybe_flush(self) -> None:
        if len(self.records) >= CHECKPOINT_FILES or time.monotonic() - self.last >= CHECKPOINT_SECONDS:
            self.flush()

    def flush(self) -> None:
        self.journal.append([*self.records, self._run_record()])
        self.records = []
        self.manifest.write_summary(self.entry_count, self.total_bytes)
        self.last = time.monotonic()

    def _run_record(self) -> dict:
        return {"t": "run", "run": self.run_state.to_dict()}


@dataclass
class _PendingFile:
    """Plik zapisany i utrwalony na nośniku, jeszcze bez czasu modyfikacji źródła.

    Czas modyfikacji źródła jest znakiem „ten plik jest kompletny” — po nim
    wznawianie rozpoznaje zapisane pliki. Dlatego ustawiamy go dopiero po
    ``fsync`` i po sprawdzeniu, że źródło nie zmieniło się w trakcie odczytu.
    """

    fd: int
    final: Path
    temp: Path | None
    written: int = 0
    digest: str = ""

    def commit(self, mtime: float) -> None:
        try:
            set_file_mtime(self.fd, mtime)
        finally:
            os.close(self.fd)
            self.fd = -1
        if self.temp is not None:
            _replace(self.temp, self.final)

    def discard(self) -> None:
        if self.fd >= 0:
            with contextlib.suppress(OSError):
                os.close(self.fd)
            self.fd = -1
        _unlink_quiet(self.temp if self.temp is not None else self.final)


def _write_stored(src: Path, dst: Path, reporter: Reporter) -> _PendingFile:
    """Zapisuje dane pliku, licząc SHA-256 w locie, i utrwala je na nośniku.

    Plik, którego jeszcze nie ma w kopii, zapisujemy **od razu pod docelową
    nazwą** — bez pliku ``.part`` i zmiany nazwy, co przy setkach tysięcy
    małych plików na dysku USB jest zauważalną oszczędnością. Przerwany zapis
    zostawia wtedy plik z czasem modyfikacji „teraz”, którego wznowienie
    nie uzna za gotowy.

    Gdy plik docelowy **już istnieje**, zapis idzie przez ``.part``
    i ``os.replace``. Nadpisanie w miejscu byłoby niebezpieczne podwójnie:
    przerwanie zniszczyłoby jedyną poprzednią kopię, a plik bywa twardym
    dowiązaniem współdzielonym ze starszą wersją, którą zapis w miejscu
    by po cichu zmienił.
    """
    flags = os.O_WRONLY | os.O_CREAT | getattr(os, "O_BINARY", 0)
    temp: Path | None = None
    try:
        fd = os.open(long_path(dst), flags | os.O_EXCL)
    except FileExistsError:
        temp = Path(str(dst) + ".part")
        fd = os.open(long_path(temp), flags | os.O_TRUNC)
    pending = _PendingFile(fd=fd, final=dst, temp=temp)
    digest = hashlib.sha256()
    try:
        with open(long_path(src), "rb") as fin:
            while True:
                reporter.check_cancel()
                chunk = fin.read(COPY_CHUNK)
                if not chunk:
                    break
                digest.update(chunk)
                view = memoryview(chunk)
                while view:
                    view = view[os.write(fd, view) :]
                pending.written += len(chunk)
                reporter.advance(len(chunk))
        os.fsync(fd)
    except BaseException:
        pending.discard()
        raise
    pending.digest = digest.hexdigest()
    return pending


def _replace(temp: Path, final: Path) -> None:
    """``os.replace`` odporne na atrybut „tylko do odczytu” pliku docelowego."""
    try:
        os.replace(long_path(temp), long_path(final))
    except PermissionError:
        make_writable(final)
        os.replace(long_path(temp), long_path(final))


@dataclass
class _PassContext:
    config: BackupConfig
    destination: Path
    version_prefix: str
    keyring: PasswordKeyring | None
    reporter: Reporter
    dirs: DirectoryCache
    total: int
    counter: itertools.count = field(default_factory=lambda: itertools.count(1))
    _store: chunks.ChunkStore | None = None
    _store_lock: threading.Lock = field(default_factory=threading.Lock)

    def chunk_store(self) -> chunks.ChunkStore:
        """Magazyn fragmentów powstaje dopiero przy pierwszym dużym pliku."""
        with self._store_lock:
            if self._store is None:
                self._store = chunks.ChunkStore(self.destination, self.keyring, create=True)
            return self._store


def _store_one(item: PlannedFile, ctx: _PassContext) -> ManifestEntry | None:
    """Zapisuje jeden plik planu. ``None`` oznacza plik zmieniony w trakcie kopiowania."""
    config = ctx.config
    reporter = ctx.reporter
    reporter.check_cancel()
    reporter.file(item.key, next(ctx.counter), ctx.total)
    stored_rel = ctx.version_prefix + item.key + planned_suffix(config, item.meta.size)
    target = ctx.destination / stored_rel
    ctx.dirs.ensure(target.parent)
    if _is_recipe_path(stored_rel):
        return _store_chunked(item, ctx, stored_rel, target)

    # Kopia dużego zbioru trwa godzinami, a użytkownik przez ten czas pracuje
    # na plikach źródłowych. Stan pliku sprzed odczytu porównujemy ze stanem po
    # zapisie, żeby rozpoznać plik zmieniony nam pod ręką — jego bajty mogą być
    # sklejką starej i nowej treści i nie wolno wpisać go do spisu treści.
    before = _source_fingerprint(item.source)
    if config.encrypt:
        hasher = hashlib.sha256()
        stored_size = crypto.encrypt_file(
            item.source,
            target,
            ctx.keyring,  # type: ignore[arg-type]
            progress=reporter.advance,
            cancel=lambda: reporter.cancelled,
            plain_digest=hasher,
        )
        digest = hasher.hexdigest()
        after = _source_fingerprint(item.source)
        if not _stable(before, after):
            return None
        # Kontener .cvlt dostaje czas modyfikacji źródła, żeby wznawianie
        # rozpoznawało zapisane pliki tak samo jak w kopii jawnej.
        with contextlib.suppress(OSError):
            os.utime(long_path(target), (after[1], after[1]))  # type: ignore[index]
    else:
        pending = _write_stored(item.source, target, reporter)
        after = _source_fingerprint(item.source)
        if not _stable(before, after):
            pending.discard()
            return None
        try:
            pending.commit(after[1])  # type: ignore[index]
        except BaseException:
            pending.discard()
            raise
        stored_size, digest = pending.written, pending.digest

    if config.verify_after_write:
        try:
            _verify_stored(target, digest, config.encrypt, ctx.keyring, reporter)
        except EngineError:
            # Plik nie zgadza się ze źródłem, a ma już czas modyfikacji źródła —
            # zostawiony, zostałby przy wznowieniu uznany za poprawny.
            _unlink_quiet(target)
            raise

    return ManifestEntry(
        size=after[0],  # type: ignore[index]
        mtime=after[1],  # type: ignore[index]
        sha256=digest,
        stored=stored_rel,
        stored_size=stored_size,
    )


def planned_suffix(config: BackupConfig, size: int) -> str:
    """Przyrostek zapisu nowego pliku: przepis dla dużych, ``.cvlt`` przy szyfrowaniu."""
    chunked = config.delta and chunks.AVAILABLE and size >= chunks.DELTA_MIN_SIZE
    return (chunks.RECIPE_SUFFIX if chunked else "") + (ENCRYPTED_SUFFIX if config.encrypt else "")


def entry_suffix(entry: ManifestEntry, config: BackupConfig) -> str:
    """Przyrostek istniejącego wpisu — dowiązanie nie zmienia sposobu zapisu pliku."""
    return (chunks.RECIPE_SUFFIX if entry.chunked else "") + (ENCRYPTED_SUFFIX if config.encrypt else "")


def _is_recipe_path(stored: str) -> bool:
    return stored.endswith(chunks.RECIPE_SUFFIX) or stored.endswith(chunks.RECIPE_SUFFIX + ENCRYPTED_SUFFIX)


def _store_chunked(item: PlannedFile, ctx: _PassContext, stored_rel: str, target: Path) -> ManifestEntry | None:
    """Duży plik: brakujące fragmenty do magazynu, a do wersji — przepis.

    Te same zasady co przy zwykłym pliku: plik zmieniony w trakcie odczytu nie
    trafia do spisu treści, a przepis dostaje czas modyfikacji źródła, żeby
    wznawianie rozpoznawało go z nośnika. Fragmenty zapisane przed przerwaniem
    zostają w magazynie i przy wznowieniu nie są zapisywane drugi raz.
    """
    reporter = ctx.reporter
    store = ctx.chunk_store()
    before = _source_fingerprint(item.source)
    recipe, _written = chunks.store_file(
        item.source, store, progress=reporter.advance, cancel=lambda: reporter.cancelled
    )
    after = _source_fingerprint(item.source)
    if not _stable(before, after):
        return None
    stored_size = chunks.write_recipe(target, recipe, ctx.keyring)
    with contextlib.suppress(OSError):
        os.utime(long_path(target), (after[1], after[1]))  # type: ignore[index]
    if ctx.config.verify_after_write:
        check = chunks.verify_recipe(chunks.read_recipe(target, ctx.keyring), store)
        if check != recipe.sha256:
            _unlink_quiet(target)
            raise EngineError(
                tr("Weryfikacja po zapisie nie powiodła się — zapisane dane różnią się od źródła.")
            )
    return ManifestEntry(
        size=recipe.size,
        mtime=after[1],  # type: ignore[index]
        sha256=recipe.sha256,
        stored=stored_rel,
        stored_size=stored_size,
        chunked=True,
    )


def _same_space(stored: str, version_prefix: str, manifest: Manifest) -> bool:
    """Czy wpis leży w katalogu, do którego pisze bieżący przebieg (a nie w starszej wersji)."""
    if version_prefix:
        return stored.startswith(version_prefix)
    first = stored.split("/", 1)[0]
    return not (_VERSION_NAME.match(first) and first in manifest.runs)


def _version_dirs(destination: Path) -> list[str]:
    try:
        with os.scandir(long_path(destination)) as entries:
            return [e.name for e in entries if e.is_dir() and _VERSION_NAME.match(e.name)]
    except OSError:
        return []


def _finish_chunk_store(
    ctx: _PassContext, manifest: Manifest, stamp: str, pruned: list[str], cancelled: bool
) -> None:
    """Lista przepisów wersji i sprzątanie nieużywanych fragmentów.

    Listę zapisujemy także po przerwaniu — sprzątanie nie musi wtedy przeglądać
    drzewa wersji. Samo sprzątanie tylko po pełnym przebiegu i tylko wtedy, gdy
    coś mogło stać się zbędne: po usunięciu starych wersji albo w kopii
    lustrzanej, gdzie nowy przepis zastępuje stary.
    """
    store_dir = ctx.destination / chunks.CHUNK_DIR
    if ctx._store is None and not Path(long_path(store_dir)).is_dir():
        return
    try:
        store = ctx._store or chunks.ChunkStore(ctx.destination, ctx.keyring)
        prefix = f"{stamp}/" if stamp else ""
        recipes = [
            entry.stored
            for entry in manifest.entries.values()
            if entry.chunked and _same_space(entry.stored, prefix, manifest)
        ]
        chunks.write_version_list(store, stamp, recipes)
        for version in pruned:
            chunks.remove_version_list(store, version)
        if cancelled or not (pruned or not stamp):
            return
        removed, freed = chunks.collect_garbage(
            store, [*_version_dirs(ctx.destination), ""], cancel=lambda: ctx.reporter.cancelled
        )
    except (OSError, crypto.CryptoError) as exc:
        log.warning("Porządkowanie magazynu fragmentów pominięte: %s", exc)
        return
    if removed:
        ctx.reporter.stage(
            tr("Usunięto nieużywane fragmenty dużych plików: {count} ({size}).").format(
                count=removed, size=human_size(freed)
            )
        )


def _stable(before: tuple[int, float] | None, after: tuple[int, float] | None) -> bool:
    return before is not None and after is not None and before == after


def _is_cancellation(error: BaseException) -> bool:
    return isinstance(error, (OperationCancelled, ScanCancelled))


def _run_backup_pass(
    plan: BackupPlan, keyring: PasswordKeyring | None, reporter: Reporter
) -> OperationResult:
    """Wykonuje jeden przebieg wcześniej przygotowanego planu."""
    config = plan.config
    if config.encrypt and keyring is None:
        raise EngineError(tr("Włączono szyfrowanie, ale nie podano hasła."))
    if config.encrypt and keyring is not None:
        _check_password_matches(plan, keyring, reporter)
        # Klucz wyprowadzamy raz, zanim ruszą wątki. Inaczej kilkadziesiąt
        # wątków naraz liczyłoby Argon2id (po 64 MiB każdy) dla tej samej soli.
        keyring.key_for(keyring.session_params)

    started = time.monotonic()
    destination = plan.destination
    manifest = Manifest.load(destination)
    manifest.encrypted = config.encrypt
    if config.stamp_updates and plan.resuming and plan.version:
        _apply_update_stamp(plan, manifest, reporter)
    workers = resolve_workers(config.workers)

    # Do jednego katalogu docelowego potrafi pisać kilka różnych zadań (inne
    # katalogi źródłowe, ten sam dysk). Manifest jest wspólny, więc wpisy i
    # mapowania cudzych zadań wolno wyłącznie **dopisywać**. Podmiana całego
    # słownika kasowała poprzednie zadanie: jego pliki zostawały na dysku, ale
    # program przestawał o nich wiedzieć i przy kolejnym przebiegu chciał
    # skopiować wszystko od nowa.
    own_labels = {root.label for root in plan.roots}
    foreign_entries = {
        key: entry
        for key, entry in manifest.entries.items()
        if key.partition("/")[0] not in own_labels
    }
    manifest.roots.update({r.label: str(r.path) for r in plan.roots})

    # Katalog wersji wybrał już ``plan_backup`` — dzięki temu plan wie, gdzie
    # trafi zapis, potrafi rozpoznać pliki zapisane przed przerwaniem i pokazać
    # to użytkownikowi, zanim cokolwiek ruszy.
    stamp = plan.version
    version_prefix = plan.version_prefix

    # Stan przebiegu utrwalamy **zanim** cokolwiek skopiujemy. Po twardym
    # zabiciu procesu albo zaniku zasilania to jedyny ślad mówiący, że ta wersja
    # kopii jest niepełna i nadaje się do wznowienia.
    run_state = manifest.runs.get(stamp) or VersionState(name=stamp)
    run_state.name = stamp
    run_state.started = run_state.started or time.time()
    run_state.finished = 0.0
    run_state.complete = False
    run_state.labels = sorted(own_labels)
    run_state.encrypted = config.encrypt
    run_state.structure = config.structure
    # „Zaplanowane” to praca, która została do wykonania w tej wersji: pliki do
    # zapisania oraz — w wersji z datą — pliki do podpięcia. Pliki rozpoznane
    # jako już zapisane się nie liczą, więc po wznowieniu liczby pokazują
    # to, czego naprawdę brakuje.
    linked_needed = len(plan.unchanged) if config.structure == "dated" else 0
    run_state.planned_files = len(plan.to_copy) + linked_needed
    run_state.planned_bytes = plan.transfer_bytes
    run_state.done_files = 0
    run_state.done_bytes = 0
    manifest.runs[stamp] = run_state
    if stamp and stamp not in manifest.versions:
        manifest.versions.append(stamp)
    checkpoints = _Checkpoints(manifest, run_state)
    checkpoints.start()

    result = OperationResult(ok=True, output_path=str(destination / version_prefix.rstrip("/")))
    total = len(plan.to_copy)
    reporter.stage(
        tr("Zapisywanie {count} {files} ({size}), {workers} równolegle").format(
            count=total,
            files=plural(total, "pliku", "plików", "plików"),
            size=human_size(plan.total_bytes),
            workers=workers,
        )
        + (tr(" z szyfrowaniem AES-256-GCM…") if config.encrypt else "…")
    )

    linked_files = 0
    linked_bytes = 0
    new_entries: dict[str, ManifestEntry] = dict(foreign_entries)
    # Pliki rozpoznane jako już zapisane w tej wersji nie wymagają żadnej
    # operacji dyskowej — wchodzą do manifestu od razu.
    new_entries.update(plan.adopted)
    for key, entry in plan.adopted.items():
        checkpoints.note(key, entry)
    #: Pliki, które zmieniły się w trakcie własnego kopiowania. Dograwa je
    #: przebieg uzupełniający, a gdy go nie ma — następna kopia.
    unstable: list[str] = []
    if plan.adopted:
        reporter.stage(
            tr("Pomijam pliki, które już są w tej wersji kopii: {count}.").format(
                count=len(plan.adopted)
            )
        )
    dirs = DirectoryCache()
    ctx = _PassContext(
        config=config,
        destination=destination,
        version_prefix=version_prefix,
        keyring=keyring,
        reporter=reporter,
        dirs=dirs,
        total=total,
    )
    cancelled = lambda: reporter.cancelled  # noqa: E731

    locked_items: list[PlannedFile] = []

    def settle(item: PlannedFile, entry: ManifestEntry | None, error: BaseException | None, final: bool) -> None:
        if error is not None:
            if _is_cancellation(error):
                result.cancelled = True
                return
            if locks.is_lock_error(error, item.source):
                # Nie błąd, tylko plik otwarty w innym programie: ponawiamy go na
                # końcu, a jeśli dalej jest zajęty — mówimy, który program go trzyma.
                if final:
                    result.locked[item.key] = locks.who_locks(item.source)
                    log.warning("Plik %s jest otwarty w innym programie: %s", item.key, result.locked[item.key])
                else:
                    locked_items.append(item)
                return
            log.error("Błąd przy pliku %s: %s", item.source, error, exc_info=error)
            result.errors.append(f"{item.key}: {error}")  # klucz pliku i treść wyjątku
            result.skipped += 1
            return
        if entry is None:
            unstable.append(item.key)
            result.skipped += 1
            log.warning("Plik %s zmienił się w trakcie kopiowania.", item.key)
            return
        new_entries[item.key] = entry
        previous = manifest.entries.get(item.key)
        if (
            previous is not None
            and previous.stored != entry.stored
            and _same_space(previous.stored, version_prefix, manifest)
        ):
            # Plik przekroczył próg zapisu fragmentami (albo zmieniono szyfrowanie):
            # stara postać w tym samym katalogu zostałaby obok nowej na zawsze.
            _unlink_quiet(destination / previous.stored)
        checkpoints.set(item.key, entry)
        result.files_done += 1
        result.bytes_done += entry.size
        run_state.done_files = result.files_done + linked_files
        run_state.done_bytes = result.bytes_done + linked_bytes
        checkpoints.maybe_flush()

    try:
        for item, entry, error in unordered_map(lambda it: _store_one(it, ctx), plan.to_copy, workers, cancelled):
            settle(item, entry, error, final=False)
        if locked_items and not (result.cancelled or reporter.cancelled):
            reporter.stage(
                tr("Ponawiam {count} {files}…").format(
                    count=len(locked_items), files=open_elsewhere(len(locked_items))
                )
            )
            _pause(LOCK_RETRY_DELAY, reporter)
            for item in locked_items:
                if reporter.cancelled:
                    break
                try:
                    settle(item, _store_one(item, ctx), None, final=True)
                except Exception as exc:  # noqa: BLE001 - każdy błąd rozstrzyga settle
                    settle(item, None, exc, final=True)
        if result.cancelled or reporter.cancelled:
            raise OperationCancelled(tr("Operacja przerwana przez użytkownika."))

        # Pliki niezmienione: w trybie wersjonowanym podpinamy je do nowej wersji
        # twardym dowiązaniem, więc każdy katalog z datą jest kompletny,
        # a zajmuje tyle miejsca, ile faktycznie nowych danych.
        if plan.unchanged and (config.structure == "dated" or plan.moved):
            if config.structure != "dated":
                reporter.stage(
                    tr("Przenoszenie plików, które zmieniły miejsce w źródle: {count}…").format(
                        count=plan.moved
                    )
                )
            elif plan.hardlinks:
                reporter.stage(
                    tr("Podpinanie niezmienionych plików do nowej wersji: {count}…").format(
                        count=len(plan.unchanged)
                    )
                )
            else:
                reporter.stage(
                    tr("Nośnik nie obsługuje twardych dowiązań — kopiuję do nowej wersji "
                       "niezmienione pliki: {count} ({size})…").format(
                        count=len(plan.unchanged),
                        size=human_size(plan.transfer_bytes - plan.total_bytes),
                    )
                )
            link_counter = itertools.count(1)
            link_total = len(plan.unchanged)

            def link(pair: tuple[str, ManifestEntry]) -> ManifestEntry:
                key, entry = pair
                reporter.check_cancel()
                if not plan.hardlinks:
                    reporter.file(key, next(link_counter), link_total)
                return _link_into_version(
                    destination, key, entry, version_prefix, config, reporter,
                    plan.hardlinks, plan.mtime_tolerance, dirs,
                )

            for (key, entry), linked, error in unordered_map(link, list(plan.unchanged.items()), workers, cancelled):
                if error is not None:
                    if _is_cancellation(error):
                        result.cancelled = True
                        continue
                    log.error("Błąd podpinania %s: %s", key, error, exc_info=error)
                    result.errors.append(f"{key}: {error}")
                    result.skipped += 1
                    continue
                new_entries[key] = linked
                # Plik, który już leży w tej wersji (np. przebudowany artefakt
                # o tej samej treści, a nowym czasie modyfikacji), też jest
                # zrobiony — inaczej program pisał „brakuje N plików”, choć
                # nie brakowało żadnego.
                linked_files += 1
                run_state.done_files = result.files_done + linked_files
                if linked.stored != entry.stored:
                    if not plan.hardlinks:
                        linked_bytes += entry.size
                        run_state.done_bytes = result.bytes_done + linked_bytes
                    checkpoints.set(key, linked)
                    checkpoints.maybe_flush()
            if result.cancelled or reporter.cancelled:
                raise OperationCancelled(tr("Operacja przerwana przez użytkownika."))
        else:
            new_entries.update(plan.unchanged)

        if config.structure == "mirror" and config.delete_removed and plan.removed:
            reporter.stage(
                tr("Usuwanie z kopii plików skasowanych w źródle: {count}…").format(count=len(plan.removed))
            )
            for key in plan.removed:
                entry = manifest.entries.get(key)
                if entry:
                    _unlink_quiet(destination / entry.stored)
                    checkpoints.delete(key)

    except OperationCancelled:
        result.cancelled = True
        result.ok = False
        reporter.stage(tr("Operacja przerwana — utrwalam stan dotychczas zapisanych plików."))
    finally:
        # Wszystko, czego ten przebieg nie zdążył dotknąć, zachowuje wpis
        # z poprzedniej kopii — te pliki nadal leżą na dysku i nadal są
        # poprawne. Gdyby ich tu zabrakło, przerwanie kopii kasowałoby
        # z manifestu całą wcześniejszą kopię, a następny przebieg zaczynałby
        # od zera. Dla plików usuniętych ze źródła sprawdzamy nośnik, żeby nie
        # wskrzesić wpisu pliku skasowanego przed chwilą przez ``delete_removed``.
        carried = 0
        for key, entry in plan.unchanged.items():
            if key not in new_entries:
                new_entries[key] = entry
                carried += 1
        for key in plan.removed:
            entry = manifest.entries.get(key)
            if entry is not None and key not in new_entries and _stored_exists(destination, entry):
                new_entries[key] = entry
                carried += 1
        if result.cancelled and carried:
            log.info("Zachowano %d wpisów z poprzedniej kopii mimo przerwania.", carried)

        manifest.entries = new_entries

        # Wersja jest kompletna tylko wtedy, gdy przebieg przeszedł do końca
        # i nic nie zostało pominięte. Kopia z błędami albo przerwana zostaje
        # oznaczona jako niedokończona — i to ona zostanie zaproponowana do
        # wznowienia. Nigdy nie wolno uznać niepełnej kopii za pełną.
        if unstable:
            reporter.stage(
                tr("Pliki zmienione w trakcie kopiowania: {count} — zostaną zapisane "
                   "ponownie w przebiegu uzupełniającym.").format(count=len(unstable))
            )
        run_state.done_files = result.files_done + linked_files
        run_state.done_bytes = result.bytes_done + linked_bytes
        run_state.locked_files = len(result.locked)
        run_state.complete = not result.cancelled and not result.errors and not result.skipped
        run_state.finished = time.time() if run_state.complete else 0.0
        manifest.runs[stamp] = run_state
        if config.structure == "dated" and stamp not in manifest.versions:
            manifest.versions.append(stamp)

        pruned: list[str] = []
        if result.cancelled:
            # Przerwanie (także wyłączanie komputera) nie może czekać na zapis
            # wielusetmegabajtowego manifestu. Punkt kontrolny w dzienniku
            # wystarcza: przy następnym wczytaniu manifest odtworzy się z niego.
            checkpoints.flush()
        else:
            # Czyścimy historię tylko po pełnym, nieprzerwanym przebiegu — inaczej
            # skasowalibyśmy starą wersję, mając w zamian kopię niekompletną.
            if config.structure == "dated" and _retention_active(config):
                pruned = _prune_versions(destination, manifest, config, reporter, own_labels)
            manifest.save()
        _finish_chunk_store(ctx, manifest, stamp, pruned, result.cancelled)
        if config.timestamp and not result.cancelled:
            prefix = f"{stamp}/" if stamp else ""
            result.version_files = [
                (key, entry.size, entry.sha256)
                for key, entry in manifest.entries.items()
                if _same_space(entry.stored, prefix, manifest)
            ]
        result.duration = time.monotonic() - started
        result.versions = dict(manifest.runs)

    if result.errors:
        result.ok = False
    return result


def _link_into_version(
    destination: Path,
    key: str,
    entry: ManifestEntry,
    version_prefix: str,
    config: BackupConfig,
    reporter: Reporter,
    hardlinks: bool = True,
    tolerance: float = 2.0,
    dirs: DirectoryCache | None = None,
) -> ManifestEntry:
    """Podpina niezmieniony plik do wersji twardym dowiązaniem.

    Dowiązanie twarde nie zajmuje miejsca na dane, więc historia wersji
    kosztuje tyle, ile realnie się zmieniło. Gdy nośnik go nie zna (exFAT,
    FAT32), plik jest kopiowany — z postępem i reakcją na przerwanie, bo przy
    dużej kopii to może być większość całej pracy.
    """
    new_rel = version_prefix + key + entry_suffix(entry, config)
    old_path = destination / entry.stored
    new_path = destination / new_rel
    if entry.stored == new_rel:
        return entry
    if dirs is not None:
        dirs.ensure(new_path.parent)
    else:
        new_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        st = os.stat(long_path(new_path))
    except OSError:
        st = None
    if st is not None:
        expected_size = entry.stored_size or entry.size
        if st.st_size == expected_size and abs(st.st_mtime - entry.mtime) <= tolerance:
            return ManifestEntry(entry.size, entry.mtime, entry.sha256, new_rel, entry.stored_size, entry.chunked)
        # W docelowej wersji leży plik, który **nie** jest kopią tego wpisu —
        # pozostałość po przerwanym zapisie albo plik zmieniony w trakcie
        # kopiowania. Uznanie go za gotowy zapisałoby w manifeście kłamstwo.
        _unlink_quiet(new_path)

    if hardlinks:
        try:
            os.link(long_path(old_path), long_path(new_path))
            return ManifestEntry(entry.size, entry.mtime, entry.sha256, new_rel, entry.stored_size, entry.chunked)
        except OSError as exc:
            log.debug("Twarde dowiązanie nie powiodło się (%s) — kopiuję %s", exc, key)

    try:
        _duplicate_file(old_path, new_path, reporter)
    except OSError as exc:
        log.warning("Nie udało się przenieść %s do nowej wersji: %s", key, exc)
        return entry
    return ManifestEntry(entry.size, entry.mtime, entry.sha256, new_rel, entry.stored_size, entry.chunked)


def _duplicate_file(src: Path, dst: Path, reporter: Reporter) -> None:
    """Pełna kopia pliku z poprzedniej wersji — zamiennik twardego dowiązania.

    Przenosimy wyłącznie czas modyfikacji. ``shutil.copystat`` kopiowałby też
    atrybut „tylko do odczytu”, przez co takiej wersji nie dałoby się później
    usunąć przy czyszczeniu historii.
    """
    _copy_with_progress(src, dst, reporter)
    st = os.stat(long_path(src))
    os.utime(long_path(dst), (st.st_mtime, st.st_mtime))


def _version_labels(destination: Path, manifest: Manifest, version: str) -> set[str]:
    """Etykiety źródeł zapisanych w danej wersji.

    Wersje zapisane przez starszy program nie mają tej informacji w manifeście —
    wtedy odczytujemy ją z nazw podkatalogów, bo każde źródło ma w wersji
    własny katalog.
    """
    run = manifest.runs.get(version)
    if run is not None and run.labels:
        return set(run.labels)
    return _labels_on_disk(destination / version)


def _labels_on_disk(folder: Path) -> set[str]:
    try:
        with os.scandir(long_path(folder)) as entries:
            return {entry.name for entry in entries if entry.is_dir(follow_symlinks=False)}
    except OSError:
        return set()


def _retention_active(config: BackupConfig) -> bool:
    return any(n > 0 for n in (config.retention, config.gfs_daily, config.gfs_weekly, config.gfs_monthly))


def versions_to_keep(
    versions: list[str],
    times: dict[str, float],
    last: int = 0,
    daily: int = 0,
    weekly: int = 0,
    monthly: int = 0,
) -> set[str]:
    """Które wersje zostają według zasad „ostatnie N” i kalendarza (GFS).

    Z każdego dnia, tygodnia (ISO) i miesiąca zostaje **najnowsza** wersja,
    liczona dla tylu ostatnich okresów, ile ich podano — okresy bez żadnej
    wersji nie zużywają limitu. Najnowsza wersja zostaje zawsze.
    """
    ordered = sorted(versions, key=lambda v: times.get(v, 0.0), reverse=True)
    keep = set(ordered[:1])
    if last > 0:
        keep |= set(ordered[:last])

    def day(t: float):
        return time.localtime(t)[:3]

    def week(t: float):
        return tuple(datetime.date(*time.localtime(t)[:3]).isocalendar()[:2])

    def month(t: float):
        return time.localtime(t)[:2]

    for count, bucket in ((daily, day), (weekly, week), (monthly, month)):
        if count <= 0:
            continue
        seen: list = []
        for version in ordered:
            key = bucket(times.get(version, 0.0))
            if key in seen:
                continue
            seen.append(key)
            keep.add(version)
            if len(seen) >= count:
                break
    return keep


def _version_time(version: str, manifest: Manifest) -> float:
    run = manifest.runs.get(version)
    if run is not None and run.started:
        return run.started
    return beat.unix_from_stamp(version) or 0.0


def _prune_versions(
    destination: Path,
    manifest: Manifest,
    config: BackupConfig,
    reporter: Reporter,
    own_labels: set[str] | None = None,
) -> list[str]:
    """Usuwa wersje, których nie zatrzymuje żadna zasada przechowywania.

    Zasady: „ostatnie N wersji” oraz kalendarz (GFS) — patrz :func:`versions_to_keep`.
    Zwraca nazwy usuniętych wersji.

    Kasujemy wyłącznie katalogi wymienione w manifeście — katalog, który tylko
    *wygląda* jak data, może należeć do użytkownika. Dodatkowo pomijamy:

    * każdą wersję, do której odwołuje się aktualny spis treści;
    * wersje **innych zadań** piszących do tego samego katalogu — limit
      „zachowaj 2 wersje” w jednym zadaniu nie może skasować kopii drugiego;
    * wersje **niedokończone** — nie liczą się do limitu i nigdy nie są
      kasowane automatycznie. Inaczej udana kopia mogłaby usunąć ostatnią
      kompletną wersję, zostawiając w zamian niepełną.
    """
    referenced = {
        entry.stored.split("/", 1)[0] for entry in manifest.entries.values() if "/" in entry.stored
    }
    candidates: list[str] = []
    for version in manifest.versions:
        run = manifest.runs.get(version)
        if run is not None and not run.complete:
            continue
        if own_labels is not None and not (_version_labels(destination, manifest, version) & own_labels):
            continue
        candidates.append(version)

    times = {version: _version_time(version, manifest) for version in candidates}
    keep = versions_to_keep(
        candidates, times, config.retention, config.gfs_daily, config.gfs_weekly, config.gfs_monthly
    )
    doomed = [version for version in candidates if version not in keep]
    if not doomed:
        return []

    removed: list[str] = []
    for version in doomed:
        if version in referenced:
            continue
        folder = destination / version
        try:
            if folder.is_dir():
                _remove_tree(folder)
            removed.append(version)
            log.info("Usunięto starą wersję kopii: %s", version)
        except OSError as exc:
            log.warning("Nie udało się usunąć wersji %s: %s", version, exc)

    if removed:
        reporter.stage(
            tr("Porządkowanie historii — usunięte najstarsze wersje: {count}.").format(
                count=len(removed)
            )
        )
        gone = set(removed)
        manifest.versions = [v for v in manifest.versions if v not in gone]
        for version in gone:
            manifest.runs.pop(version, None)
    return removed


def _check_password_matches(plan: BackupPlan, keyring: PasswordKeyring, reporter: Reporter) -> None:
    """Sprawdza, czy hasło zgadza się z hasłem plików, które zostaną w kopii.

    Wznowienie i kopia przyrostowa zostawiają w wersji pliki zaszyfrowane
    wcześniej. Gdyby użytkownik wznowił kopię z innym hasłem, w jednej
    wersji wylądowałyby pliki pod dwoma hasłami — i część z nich okazałaby
    się nie do odczytania dopiero przy przywracaniu. Sprawdzamy najmniejszy
    z pozostających plików, więc koszt jest pomijalny.
    """
    kept = [
        entry
        for entry in list(plan.adopted.values()) + list(plan.unchanged.values())
        if entry.stored.endswith(ENCRYPTED_SUFFIX)
    ]
    if not kept:
        return
    sample = min(kept, key=lambda entry: entry.stored_size or entry.size)
    path = plan.destination / sample.stored
    reporter.stage(tr("Sprawdzam, czy hasło zgadza się z hasłem wcześniej zapisanych plików…"))
    try:
        crypto.verify_file(path, keyring, cancel=lambda: reporter.cancelled)
    except crypto.IntegrityError as exc:
        raise EngineError(
            tr("Podane hasło nie pasuje do plików zapisanych wcześniej w tej kopii. "
               "Wznowienie z innym hasłem zostawiłoby w jednej kopii pliki pod dwoma hasłami. "
               "Podaj hasło użyte przy poprzednim przebiegu albo utwórz kopię w nowym katalogu.")
        ) from exc
    except (OSError, crypto.UnsupportedFormatError) as exc:
        log.warning("Nie udało się sprawdzić hasła na pliku %s: %s", path, exc)


def _copy_with_progress(src: Path, dst: Path, reporter: Reporter) -> tuple[int, str]:
    """Kopiuje plik porcjami, zwracając ``(zapisane bajty, SHA-256 źródła)``.

    Suma kontrolna powstaje **podczas tego samego odczytu** co kopiowanie.
    Wcześniej silnik czytał każdy plik osobno do policzenia sumy i osobno do
    skopiowania: podwójna praca dysku, a między odczytami okno, w którym plik
    mógł się zmienić — i wtedy do spisu treści trafiała suma kontrolna
    nieodpowiadająca zapisanym bajtom.

    Zapis idzie przez plik tymczasowy, więc przerwana kopia nie zostawia
    w katalogu docelowym pliku, który wygląda na kompletny.
    """
    tmp = Path(str(dst) + ".part")
    digest = hashlib.sha256()
    written = 0
    try:
        with open(long_path(src), "rb") as fin, open(long_path(tmp), "wb") as fout:
            while True:
                reporter.check_cancel()
                chunk = fin.read(COPY_CHUNK)
                if not chunk:
                    break
                digest.update(chunk)
                fout.write(chunk)
                written += len(chunk)
                reporter.advance(len(chunk))
            fout.flush()
            os.fsync(fout.fileno())
        os.replace(long_path(tmp), long_path(dst))
    except BaseException:
        _unlink_quiet(tmp)
        raise
    return written, digest.hexdigest()


def _source_fingerprint(path: Path) -> tuple[int, float] | None:
    """Rozmiar i czas modyfikacji źródła — do wykrycia zmiany w trakcie kopiowania."""
    try:
        st = os.stat(long_path(path))
    except OSError:
        return None
    return st.st_size, st.st_mtime


def _verify_stored(
    target: Path,
    expected_sha: str,
    encrypted: bool,
    keyring: PasswordKeyring | None,
    reporter: Reporter,
) -> None:
    """Czyta zapisany plik z powrotem i sprawdza, czy dane są poprawne.

    Dla kopii jawnej porównujemy SHA-256 z sumą źródła; dla zaszyfrowanej
    weryfikujemy tag GCM, co jednocześnie potwierdza poprawność hasła.
    """
    if encrypted:
        if keyring is None:
            return
        crypto.verify_file(target, keyring, cancel=lambda: reporter.cancelled)
        return
    actual = hash_file(target, cancel=lambda: reporter.cancelled)
    if actual != expected_sha:
        raise EngineError(tr("Weryfikacja po zapisie nie powiodła się — zapisane dane różnią się od źródła."))


def _unlink_quiet(path: Path) -> None:
    try:
        os.unlink(long_path(path))
    except PermissionError:
        make_writable(path)
        with contextlib.suppress(OSError):
            os.unlink(long_path(path))
    except OSError:
        pass


def _remove_tree(folder: Path) -> None:
    """``shutil.rmtree`` radzący sobie z plikami „tylko do odczytu”.

    Kopie tworzone przez wcześniejsze wersje programu dziedziczyły ten atrybut
    ze źródła (np. obiekty repozytoriów Git), a Python na Windows takich plików
    nie usuwa — czyszczenie historii po cichu nie zwalniało miejsca.
    """

    def retry_writable(func, path, _exc):
        make_writable(path)
        func(path)

    if sys.version_info >= (3, 12):
        shutil.rmtree(long_path(folder), onexc=retry_writable)
    else:  # pragma: no cover - Python 3.11
        shutil.rmtree(long_path(folder), onerror=retry_writable)


# --------------------------------------------------------- weryfikacja odroczona


def _hash_with_progress(path: Path, reporter: Reporter) -> str:
    digest = hashlib.sha256()
    with open(long_path(path), "rb") as handle:
        while True:
            reporter.check_cancel()
            chunk = handle.read(COPY_CHUNK)
            if not chunk:
                break
            digest.update(chunk)
            reporter.advance(len(chunk))
    return digest.hexdigest()


def verify_backup(
    destination: str | os.PathLike[str],
    keyring: PasswordKeyring | None,
    reporter: Reporter,
    workers: int = 0,
) -> OperationResult:
    """Sprawdza pliki kopii z sumami kontrolnymi zapisanymi w spisie treści.

    To zastępuje weryfikację natychmiast po zapisie. Plik czytany zaraz po
    zapisaniu pochodzi zwykle z pamięci podręcznej systemu, więc niewiele mówi
    o nośniku, a kosztował ok. połowę czasu kopii. Uruchomiona później — najlepiej
    po ponownym podłączeniu dysku — weryfikacja czyta dane faktycznie z nośnika.

    Wpisy bez sumy kontrolnej (pliki rozpoznane przy wznawianiu kopii) porównujemy
    z plikiem źródłowym, o ile ten się od tamtej pory nie zmienił, i uzupełniamy
    w spisie treści brakującą sumę.
    """
    started = time.monotonic()
    root = Path(destination).resolve()
    manifest = Manifest.load(root)
    if not manifest.entries:
        raise EngineError(tr("W tym katalogu nie ma spisu treści kopii — nie ma z czym porównać plików."))
    items = list(manifest.entries.items())
    if keyring is None and any(entry.stored.endswith(ENCRYPTED_SUFFIX) for _, entry in items):
        raise EngineError(tr("Kopia jest zaszyfrowana — podaj hasło, aby ją zweryfikować."))
    if keyring is not None:
        keyring.key_for(keyring.session_params)

    total_bytes = sum(entry.size for _, entry in items)
    threads = resolve_workers(workers)
    reporter.stage(
        tr("Weryfikacja {count} {files} ({size}), {threads} równolegle…").format(
            count=len(items),
            files=plural(len(items), "pliku", "plików", "plików"),
            size=human_size(total_bytes),
            threads=threads,
        )
    )
    result = OperationResult(ok=True, output_path=str(root))
    counter = itertools.count(1)
    journal = ManifestJournal(root)
    filled_records: list[dict] = []
    unverified = 0
    filled = 0

    store = chunks.ChunkStore(root, keyring) if any(entry.chunked for _, entry in items) else None

    def check(pair: tuple[str, ManifestEntry]) -> tuple[str, str]:
        key, entry = pair
        reporter.check_cancel()
        reporter.file(key, next(counter), len(items))
        path = root / entry.stored
        if entry.chunked:
            try:
                recipe = chunks.read_recipe(path, keyring)
            except FileNotFoundError:
                return "bad", tr("brak pliku w kopii")
            digest = chunks.verify_recipe(recipe, store, reporter.advance, lambda: reporter.cancelled)  # type: ignore[arg-type]
            if digest != recipe.sha256 or (entry.sha256 and digest != entry.sha256):
                return "bad", tr("zawartość różni się od sumy kontrolnej zapisanej podczas kopii")
            return "ok", ""
        if entry.stored.endswith(ENCRYPTED_SUFFIX):
            crypto.verify_file(path, keyring, cancel=lambda: reporter.cancelled)  # type: ignore[arg-type]
            reporter.advance(entry.size)
            return "ok", ""
        try:
            st = os.stat(long_path(path))
        except FileNotFoundError:
            return "bad", tr("brak pliku w kopii")
        if st.st_size != entry.size:
            return "bad", tr("rozmiar w kopii {actual} B zamiast {expected} B").format(
                actual=st.st_size, expected=entry.size
            )
        digest = _hash_with_progress(path, reporter)
        if entry.sha256:
            if digest != entry.sha256:
                return "bad", tr("zawartość różni się od sumy kontrolnej zapisanej podczas kopii")
            return "ok", ""
        source = _source_for_key(manifest, key)
        fingerprint = _source_fingerprint(source) if source is not None else None
        if (
            fingerprint is None
            or fingerprint[0] != entry.size
            or abs(fingerprint[1] - entry.mtime) > SOURCE_MTIME_TOLERANCE
        ):
            return "unverified", ""
        if hash_file(source, cancel=lambda: reporter.cancelled) != digest:  # type: ignore[arg-type]
            return "bad", tr("zawartość różni się od pliku źródłowego")
        return "filled", digest

    try:
        for (key, entry), outcome, error in unordered_map(check, items, threads, lambda: reporter.cancelled):
            if error is not None:
                if _is_cancellation(error):
                    result.cancelled = True
                    continue
                result.errors.append(f"{key}: {error}")
                continue
            kind, detail = outcome
            if kind == "bad":
                result.errors.append(f"{key}: {detail}")
                continue
            result.files_done += 1
            result.bytes_done += entry.size
            if kind == "unverified":
                unverified += 1
            elif kind == "filled":
                filled += 1
                updated = ManifestEntry(
                    entry.size, entry.mtime, detail, entry.stored, entry.stored_size, entry.chunked
                )
                filled_records.append({"t": "set", "k": key, "e": updated.to_dict()})
                if len(filled_records) >= CHECKPOINT_FILES:
                    journal.append(filled_records)
                    filled_records = []
        if reporter.cancelled:
            result.cancelled = True
    finally:
        if filled_records:
            journal.append(filled_records)
        result.duration = time.monotonic() - started

    if filled:
        result.notes.append(
            tr("Pliki bez zapisanej sumy kontrolnej, porównane ze źródłem i uzupełnione "
               "w spisie treści: {count}.").format(count=filled)
        )
    if unverified:
        result.notes.append(
            tr("Pliki bez sumy kontrolnej sprawdzone tylko co do rozmiaru, bo ich źródło "
               "zmieniło się albo jest niedostępne: {count}.").format(count=unverified)
        )
    result.ok = not result.errors and not result.cancelled
    return result


#: Domyślna wielkość próbki i limit bajtów próbnego przywrócenia. Próba ma
#: trwać minuty, nie godziny — jeden plik maszyny wirtualnej nie może jej
#: zdominować, więc pliki większe niż pozostały limit są pomijane.
TRIAL_SAMPLE_FILES = 50
TRIAL_BYTE_BUDGET = 512 * 1024 * 1024


def trial_restore(
    destination: str | os.PathLike[str],
    keyring: PasswordKeyring | None,
    reporter: Reporter,
    sample: int = TRIAL_SAMPLE_FILES,
    byte_budget: int = TRIAL_BYTE_BUDGET,
    seed: int | None = None,
) -> OperationResult:
    """Przywraca losową próbkę plików do katalogu tymczasowego i sprawdza wynik.

    Różnica względem :func:`verify_backup`: tamta czyta kopię i porównuje sumy,
    a ta przechodzi **tę samą ścieżkę co prawdziwe przywracanie** — odszyfrowanie,
    zapis, nazwy, katalogi — i porównuje wynik ze źródłem, jeśli źródło się od
    kopii nie zmieniło, a w przeciwnym razie z sumą kontrolną ze spisu treści.
    Jedyny sposób, by wiedzieć, że kopia działa, zanim będzie potrzebna.

    Odtworzone pliki (przy kopii zaszyfrowanej — w postaci jawnej) leżą w katalogu
    tymczasowym tylko na czas porównania i są kasowane także przy przerwaniu.
    """
    import random
    import tempfile

    started = time.monotonic()
    root = Path(destination).resolve()
    manifest = Manifest.load(root)
    if not manifest.entries:
        raise EngineError(tr("W tym katalogu nie ma spisu treści kopii — nie ma z czym porównać plików."))

    chooser = random.Random(seed)
    candidates = [(key, entry) for key, entry in manifest.entries.items() if entry.sha256]
    chooser.shuffle(candidates)
    chosen: list[tuple[str, ManifestEntry]] = []
    budget = byte_budget
    for key, entry in candidates:
        if len(chosen) >= sample:
            break
        if entry.size > budget:
            continue
        chosen.append((key, entry))
        budget -= entry.size
    if not chosen:
        raise EngineError(tr("W kopii nie ma plików, które dałoby się sprawdzić próbnie."))

    items = [
        RestoreItem(
            key=key,
            stored=root / entry.stored,
            size=entry.size,
            encrypted=entry.stored.endswith(ENCRYPTED_SUFFIX),
            chunked=entry.chunked,
        )
        for key, entry in chosen
    ]
    if keyring is None and any(item.encrypted for item in items):
        raise EngineError(tr("Kopia jest zaszyfrowana — podaj hasło, aby ją zweryfikować."))

    reporter.stage(
        tr("Próbne przywrócenie losowo wybranych plików: {count}…").format(count=len(items))
    )
    scratch = Path(tempfile.mkdtemp(prefix="tvb-proba-"))
    try:
        plan = RestorePlan(
            backup_root=root,
            items=items,
            destination=scratch,
            layout="tree",
            collision="overwrite",
            total_bytes=sum(item.size for item in items),
        )
        restored = run_restore(plan, keyring, reporter)
        result = OperationResult(ok=True, output_path=str(root), cancelled=restored.cancelled)
        result.errors = list(restored.errors)
        if restored.cancelled:
            result.ok = False
            return result

        against_source = 0
        for key, entry in chosen:
            target = scratch / key.replace("/", os.sep)
            if not Path(long_path(target)).exists():
                continue  # błąd przywrócenia został już zapisany wyżej
            digest = hash_file(target, cancel=lambda: reporter.cancelled)
            source = _source_for_key(manifest, key)
            fingerprint = _source_fingerprint(source) if source is not None else None
            unchanged = (
                fingerprint is not None
                and fingerprint[0] == entry.size
                and abs(fingerprint[1] - entry.mtime) <= SOURCE_MTIME_TOLERANCE
            )
            if unchanged:
                expected = hash_file(source, cancel=lambda: reporter.cancelled)  # type: ignore[arg-type]
                against_source += 1
                problem = tr("przywrócony plik różni się od pliku źródłowego")
            else:
                expected = entry.sha256
                problem = tr("przywrócony plik różni się od sumy kontrolnej zapisanej podczas kopii")
            if digest != expected:
                result.errors.append(f"{key}: {problem}")
                continue
            result.files_done += 1
            result.bytes_done += entry.size

        result.notes.append(
            tr("Porównano ze źródłem: {source}; tylko z sumą kontrolną (źródło zmieniło się "
               "albo jest niedostępne): {checksum}.").format(
                source=against_source, checksum=result.files_done - against_source
            )
        )
        result.ok = not result.errors
        result.duration = time.monotonic() - started
        return result
    except OperationCancelled:
        return OperationResult(ok=False, output_path=str(root), cancelled=True)
    finally:
        # Odtworzone pliki kopii zaszyfrowanej są tu w postaci jawnej — nie mogą
        # przeżyć próby, także przerwanej.
        shutil.rmtree(scratch, ignore_errors=True)
        log.info("Próbne przywrócenie zakończone w %.1f s", time.monotonic() - started)


def _source_for_key(manifest: Manifest, key: str) -> Path | None:
    label, _, rel = key.partition("/")
    root = manifest.roots.get(label)
    if not root:
        return None
    return Path(root) / rel.replace("/", os.sep)


# ------------------------------------------------------ stan katalogu kopii

#: Nazwa katalogu wersji nadawana przez ``_resolve_version``.
#: Oddziela datę utworzenia wersji od daty jej ostatniego uzupełnienia.
VERSION_UPDATE_SEPARATOR = "--"

#: Nazwa katalogu wersji: znacznik BeatTime (``2026-09-24_@921``) albo starszy
#: zegarowy (``2026-09-17_16-30-11``), z opcjonalnym przyrostkiem unikalności
#: i opcjonalną datą ostatniego uzupełnienia.
_STAMP_PATTERN = r"\d{4}-\d{2}-\d{2}_(?:@\d{3}|\d{2}-\d{2}-\d{2})"
_VERSION_NAME = re.compile(
    rf"^{_STAMP_PATTERN}(?:_\d+)?(?:{VERSION_UPDATE_SEPARATOR}{_STAMP_PATTERN})?$"
)


def source_labels(sources: Iterable[str]) -> list[str]:
    """Etykiety, pod którymi źródła trafią do kopii — bez sprawdzania, czy istnieją.

    Ta sama reguła co w ``_validate``: dwa źródła o tej samej nazwie dostają
    przyrostek. Potrzebne, żeby rozpoznać wersje *tego* zadania w katalogu,
    do którego piszą też inne zadania.
    """
    labels: list[str] = []
    for raw in sources:
        base = SourceRoot.make(raw).label
        label, suffix = base, 2
        while label in labels:
            label = f"{base}_{suffix}"
            suffix += 1
        labels.append(label)
    return labels


@dataclass
class DestinationInfo:
    """Co wiadomo o katalogu docelowym, zanim zacznie się kopia."""

    path: Path
    exists: bool
    filesystem: str = ""
    cluster: int = 0
    hardlinks_likely: bool = True
    free: int = 0
    total: int = 0
    #: liczba plików w manifeście; ``None``, gdy jej nie znamy (stary manifest
    #: bez podsumowania, a nie pozwolono go wczytać)
    entry_count: int | None = None
    updated: float = 0.0
    #: wersje z datą, najnowsze najpierw
    runs: list[VersionState] = field(default_factory=list)
    #: stan kopii lustrzanej (katalog bez podziału na wersje), jeśli istnieje
    mirror: VersionState | None = None

    def runs_for(self, labels: Iterable[str]) -> list[VersionState]:
        wanted = set(labels)
        return [run for run in self.runs if set(run.labels) & wanted]


def inspect_destination(destination: str | os.PathLike[str], load_manifest: bool = False) -> DestinationInfo:
    """Ustala stan katalogu docelowego: nośnik, wolne miejsce, wersje i ich kompletność.

    Domyślnie korzysta wyłącznie z małego podsumowania manifestu i z listy
    katalogów, więc można to wołać z wątku interfejsu. ``load_manifest=True``
    wczytuje pełny manifest, gdy podsumowania brak — to może trwać długo
    i musi iść w wątku roboczym.
    """
    path = Path(destination)
    info = DestinationInfo(path=path, exists=path.is_dir())
    if not info.exists:
        return info

    info.filesystem = filesystem_name(path)
    info.cluster = cluster_size(path)
    info.hardlinks_likely = hardlinks_expected(info.filesystem) if info.filesystem else True
    try:
        usage = shutil.disk_usage(path)
        info.free, info.total = usage.free, usage.total
    except OSError as exc:
        log.warning("Nie udało się odczytać wolnego miejsca w %s: %s", path, exc)

    runs: dict[str, VersionState] = {}
    summary = ManifestSummary.load(path)
    if summary is not None:
        runs = dict(summary.runs)
        info.entry_count = summary.entry_count
        info.updated = summary.updated
    elif load_manifest and (path / MANIFEST_NAME).exists():
        manifest = Manifest.load(path)
        runs = dict(manifest.runs)
        info.entry_count = len(manifest.entries)
        info.updated = manifest.updated

    # Katalogi wersji leżące na dysku, a nieznane manifestowi — np. gdy
    # manifestu nie wczytano albo nigdy nie zdążył powstać. Ich stanu nie
    # znamy i dokładnie tak są opisywane.
    try:
        with os.scandir(long_path(path)) as entries:
            for entry in entries:
                if entry.is_dir(follow_symlinks=False) and _VERSION_NAME.match(entry.name):
                    runs.setdefault(entry.name, VersionState(name=entry.name, complete=True, known=False))
    except OSError as exc:
        log.warning("Nie udało się odczytać katalogu %s: %s", path, exc)

    for run in runs.values():
        if run.name and not run.labels:
            run.labels = sorted(_labels_on_disk(path / run.name))

    info.mirror = runs.pop("", None)
    info.runs = sorted(runs.values(), key=lambda run: run.name, reverse=True)
    return info


def suggest_continuation(info: DestinationInfo, labels: Iterable[str]) -> VersionState | None:
    """Wersja tego zadania, którą należy zaproponować do uzupełnienia.

    Bierzemy pod uwagę wyłącznie **najnowszą** wersję z tymi samymi źródłami.
    Proponujemy ją, gdy jest niedokończona albo jej stan jest nieznany —
    dokładnie w tej sytuacji program tworzył dotąd nową, pełną wersję, choć
    użytkownik chciał tylko dokończyć poprzednią. Kompletnej wersji nie
    proponujemy: dla niej właściwa jest nowa wersja z datą.
    """
    for run in info.runs_for(labels):
        if not run.complete or not run.known:
            return run
        return None
    return None


def describe_version(run: VersionState) -> str:
    """Opis wersji dla człowieka: data utworzenia, data uzupełnienia i stan."""
    created, _, updated = run.name.partition(VERSION_UPDATE_SEPARATOR)
    when = beat.describe(created) if created else tr("kopia lustrzana")
    if updated:
        when += tr(", uzupełniona {when}").format(when=beat.describe(updated))
    if not run.known:
        state = tr("stan nieznany (zapisana starszą wersją programu)")
    elif run.complete:
        state = tr("kompletna")
        if run.locked_files:
            state += tr(" (bez {count} {files})").format(
                count=run.locked_files,
                files=plural(
                    run.locked_files,
                    "pliku otwartego w innym programie",
                    "plików otwartych w innych programach",
                    "plików otwartych w innych programach",
                ),
            )
    elif run.missing_files:
        state = tr("niedokończona — brakuje ok. {count} {files} ({size})").format(
            count=run.missing_files,
            files=plural(run.missing_files, "pliku", "plików", "plików"),
            size=human_size(run.missing_bytes),
        )
    else:
        state = tr("niedokończona")
    return f"{when} — {state}"


# --------------------------------------------------------------- przywracanie


@dataclass
class RestoreItem:
    key: str
    stored: Path
    size: int
    encrypted: bool
    original_root: str = ""
    #: ``stored`` to przepis — treść składana z magazynu fragmentów
    chunked: bool = False


@dataclass
class RestorePlan:
    backup_root: Path
    items: list[RestoreItem]
    destination: Path
    layout: str = "tree"  # "tree" | "flat" | "original"
    collision: str = "rename"  # "skip" | "overwrite" | "rename"
    total_bytes: int = 0
    roots: dict[str, str] = field(default_factory=dict)
    from_manifest: bool = True


def plan_restore(
    backup_root: str | os.PathLike[str],
    destination: str | os.PathLike[str],
    layout: str = "tree",
    collision: str = "rename",
    reporter: Reporter | None = None,
) -> RestorePlan:
    """Buduje listę plików do przywrócenia.

    Preferujemy manifest (zna oryginalne nazwy, rozmiary i katalogi źródłowe).
    Jeśli go nie ma — bo katalog pochodzi z innego narzędzia albo został ręcznie
    okrojony — przechodzimy drzewo i rozpoznajemy kontenery po sygnaturze pliku,
    a nie po rozszerzeniu.
    """
    reporter = reporter or Reporter()
    root = Path(backup_root).resolve()
    if not root.is_dir():
        raise EngineError(tr("Katalog kopii nie istnieje: {path}").format(path=root))
    target = Path(destination).resolve()

    manifest = Manifest.load(root)
    items: list[RestoreItem] = []
    total = 0

    if manifest.entries:
        reporter.stage(
            tr("Wczytano manifest kopii: {count} {files}.").format(
                count=len(manifest.entries),
                files=plural(len(manifest.entries), "plik", "pliki", "plików"),
            )
        )
        for key, entry in manifest.entries.items():
            stored = root / entry.stored
            if not Path(long_path(stored)).exists():
                log.warning("Pominięto %s — brak pliku %s", key, stored)
                continue
            label = key.partition("/")[0]
            items.append(
                RestoreItem(
                    key=key,
                    stored=stored,
                    size=entry.size,
                    encrypted=manifest.encrypted or stored.suffix == ENCRYPTED_SUFFIX,
                    original_root=manifest.roots.get(label, ""),
                    chunked=entry.chunked,
                )
            )
            total += entry.size
        from_manifest = True
    else:
        reporter.stage(tr("Brak manifestu — skanuję katalog kopii."))
        for path in _iter_all_files(root):
            if path.name.startswith(MANIFEST_NAME):
                continue
            if path.parent == root and path.name in rescue.RESCUE_FILES:
                continue
            encrypted = crypto.is_encrypted_file(path)
            rel = path.relative_to(root).as_posix()
            if encrypted and rel.endswith(ENCRYPTED_SUFFIX):
                rel = rel[: -len(ENCRYPTED_SUFFIX)]
            chunked = rel.endswith(chunks.RECIPE_SUFFIX)
            if chunked:
                rel = rel[: -len(chunks.RECIPE_SUFFIX)]
            try:
                size = path.stat().st_size
            except OSError:
                size = 0
            items.append(RestoreItem(key=rel, stored=path, size=size, encrypted=encrypted, chunked=chunked))
            total += size
        from_manifest = False

    return RestorePlan(
        backup_root=root,
        items=items,
        destination=target,
        layout=layout,
        collision=collision,
        total_bytes=total,
        roots=dict(manifest.roots),
        from_manifest=from_manifest,
    )


def _iter_all_files(root: Path) -> Iterable[Path]:
    r"""Przechodzi katalog kopii, zwracając ścieżki bez prefiksu długich nazw.

    ``os.walk(long_path(root))`` zwracałby ścieżki z prefiksem ``\?\``,
    których nie da się potem odnieść do ``root`` przez ``relative_to``.
    """
    for _rel, path, _st in iter_tree(root, [chunks.CHUNK_DIR + "/*"], None):
        yield path


def run_restore(plan: RestorePlan, keyring: PasswordKeyring | None, reporter: Reporter) -> OperationResult:
    """Przywraca pliki zgodnie z planem."""
    started = time.monotonic()
    result = OperationResult(ok=True, output_path=str(plan.destination))
    total = len(plan.items)
    needs_password = any(item.encrypted for item in plan.items)
    if needs_password and keyring is None:
        raise EngineError(tr("Kopia jest zaszyfrowana — podaj hasło, aby ją przywrócić."))
    store = (
        chunks.ChunkStore(plan.backup_root, keyring) if any(item.chunked for item in plan.items) else None
    )

    reporter.stage(
        tr("Przywracanie {count} {files} ({size})…").format(
            count=total,
            files=plural(total, "pliku", "plików", "plików"),
            size=human_size(plan.total_bytes),
        )
    )
    try:
        for index, item in enumerate(plan.items, start=1):
            reporter.check_cancel()
            reporter.file(item.key, index, total)
            try:
                target = _restore_target(plan, item)
                target.parent.mkdir(parents=True, exist_ok=True)
                target = _apply_collision_policy(target, plan.collision)
                if target is None:
                    result.skipped += 1
                    continue
                if item.chunked:
                    recipe = chunks.read_recipe(item.stored, keyring)
                    written = chunks.restore_file(
                        recipe, store, target, reporter.advance, lambda: reporter.cancelled  # type: ignore[arg-type]
                    )
                    with contextlib.suppress(OSError):
                        stamp_time = os.stat(long_path(item.stored)).st_mtime
                        os.utime(long_path(target), (stamp_time, stamp_time))
                elif item.encrypted:
                    written = crypto.decrypt_file(
                        item.stored,
                        target,
                        keyring,  # type: ignore[arg-type]
                        progress=reporter.advance,
                        cancel=lambda: reporter.cancelled,
                    )
                else:
                    written, _ = _copy_with_progress(item.stored, target, reporter)
                    with contextlib.suppress(OSError):
                        shutil.copystat(long_path(item.stored), long_path(target))
                result.files_done += 1
                result.bytes_done += written
            except OperationCancelled:
                raise
            except Exception as exc:
                log.exception("Błąd przy przywracaniu %s", item.key)
                result.errors.append(f"{item.key}: {exc}")
                result.skipped += 1
    except OperationCancelled:
        result.cancelled = True
        result.ok = False
        reporter.stage(tr("Przywracanie przerwane."))
    finally:
        result.duration = time.monotonic() - started

    if result.errors:
        result.ok = False
    return result


def restore_roots(plan: RestorePlan) -> set[Path]:
    """Foldery najwyższego poziomu, w których przywracanie utworzy pliki."""
    if plan.layout == "flat":
        return {plan.destination}
    labels = {item.key.partition("/")[0]: item.original_root for item in plan.items}
    if plan.layout == "original":
        roots = (plan.roots.get(label) or root for label, root in labels.items())
        return {Path(root) for root in roots if root}
    return {plan.destination / label for label in labels}


def _restore_target(plan: RestorePlan, item: RestoreItem) -> Path:
    if plan.layout == "flat":
        return plan.destination / Path(item.key).name
    if plan.layout == "original":
        label, _, rel = item.key.partition("/")
        root = plan.roots.get(label) or item.original_root
        if not root:
            raise EngineError(
                tr("Nie znam oryginalnej lokalizacji dla {key} — wybierz inny układ "
                   "przywracania.").format(key=item.key)
            )
        # Ten układ z definicji zapisuje poza katalogiem docelowym, ale klucz
        # nadal nie może wyprowadzić zapisu ponad katalog źródłowy.
        return _contained(Path(root), rel, item.key)
    return _contained(plan.destination, item.key, item.key)


def _contained(base: Path, relative: str, key: str) -> Path:
    """Skleja ścieżkę i upewnia się, że wynik nie wychodzi poza ``base``.

    Manifest kopii to plik, który mógł powstać gdzie indziej — przywracanie
    z cudzego nośnika nie może zapisać pliku pod ścieżką w rodzaju
    ``../../Windows/System32``. Analogia do podatności „zip slip".
    """
    target = contained_path(base, relative)
    if target is None:
        raise EngineError(
            tr("Wpis {key} w spisie treści kopii wskazuje poza katalog docelowy — "
               "pomijam go.").format(key=repr(key))
        )
    return target


def _apply_collision_policy(target: Path, policy: str) -> Path | None:
    """Zwraca docelową ścieżkę albo ``None``, jeśli plik trzeba pominąć."""
    if not Path(long_path(target)).exists():
        return target
    if policy == "overwrite":
        return target
    if policy == "skip":
        return None
    stem, suffix = target.stem, target.suffix
    for counter in range(1, 10_000):
        candidate = target.with_name(f"{stem} ({counter}){suffix}")
        if not Path(long_path(candidate)).exists():
            return candidate
    raise EngineError(tr("Nie udało się znaleźć wolnej nazwy dla {path}").format(path=target))
