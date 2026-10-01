"""Kopia „na bieżąco”: zmiany w źródłach dogrywane do dzisiejszej wersji kopii.

Pierwsza kopia jest pełna, każda następna dogrywa tylko to, co się zmieniło —
tak działa każdy przebieg tego programu. Tryb „na bieżąco” dokłada dwie rzeczy:

* **kiedy** — program w tle obserwuje foldery źródłowe (``watchdog``, w Windows
  ReadDirectoryChangesW) i po serii zmian, gdy zrobi się cicho, uruchamia
  dogrywkę. Po podłączeniu dysku z kopią synchronizuje od razu (harmonogram,
  :mod:`cleanvault.scheduler`);
* **dokąd** — do dzisiejszej wersji z datą, a nie do nowej przy każdej zmianie:
  historia zostaje czytelna (jedna wersja na dzień), a kopia jest aktualna
  co do minut.

Wersji opieczętowanej w publicznym dzienniku Sigelith nigdy nie uzupełniamy —
audyt (:mod:`cleanvault.audit`) słusznie uznałby ją za zmienioną. Dlatego przy
włączonych znacznikach czasu pierwsza dogrywka nowego dnia **zamyka** wczorajszą
wersję pieczęcią, a dalsze zmiany trafiają już do nowej, dzisiejszej.

Moduł nie zna Qt: zegar i uruchamianie kopii należą do interfejsu
(:class:`cleanvault.ui.background.SchedulerService`).
"""

from __future__ import annotations

import threading
import time
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from . import proof
from .log import get_logger
from .snapshot import VersionState
from .state import Template

log = get_logger("live")

#: Tyle sekund ciszy po ostatniej zmianie, zanim dogramy — zapis dużego pliku albo
#: seria zapisów (zapis dokumentu, rozpakowanie archiwum) kończy się w jednej kopii.
QUIET_SECONDS = 90
#: Najkrótszy odstęp między dogrywkami tego samego szablonu.
MIN_INTERVAL = 5 * 60
#: Przy nieustających zmianach (np. dziennik programu) dogrywamy najpóźniej po tylu
#: sekundach od pierwszej z nich — inaczej cisza mogłaby nie nadejść nigdy.
MAX_DELAY = 15 * 60
#: Po nieudanej dogrywce kolejna próba dopiero po tylu sekundach.
RETRY_AFTER = 30 * 60
#: Gdy obserwowanie folderu się nie udało (brak biblioteki, dysk sieciowy), dogrywka
#: rusza po prostu co tyle sekund — kopia przyrostowa bez zmian trwa chwilę.
FALLBACK_INTERVAL = 15 * 60


@dataclass
class _State:
    first_change: float = 0.0
    last_change: float = 0.0
    last_run: float = 0.0
    retry_at: float = 0.0
    running_since: float = 0.0
    held: bool = False


class ChangeTracker:
    """Zmiany zgłoszone dla szablonów i decyzja, czy pora na dogrywkę.

    Zgłoszenia przychodzą z wątku obserwatora, decyzje zapadają w wątku
    interfejsu — stąd blokada.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._states: dict[str, _State] = {}

    def _state(self, template_id: str) -> _State:
        return self._states.setdefault(template_id, _State())

    def note(self, template_id: str, when: float | None = None) -> None:
        moment = time.time() if when is None else when
        with self._lock:
            state = self._state(template_id)
            if not state.first_change:
                state.first_change = moment
            state.last_change = max(state.last_change, moment)

    def pending(self, template_id: str) -> bool:
        with self._lock:
            state = self._states.get(template_id)
            return bool(state and state.first_change)

    def held(self, template_id: str) -> bool:
        with self._lock:
            state = self._states.get(template_id)
            return bool(state and state.held)

    def last_run(self, template_id: str) -> float:
        with self._lock:
            state = self._states.get(template_id)
            return state.last_run if state else 0.0

    def ready(self, template_id: str, now: float) -> bool:
        with self._lock:
            state = self._states.get(template_id)
            if state is None or not state.first_change or state.held or state.running_since:
                return False
            if now < state.retry_at or now - state.last_run < MIN_INTERVAL:
                return False
            return now - state.last_change >= QUIET_SECONDS or now - state.first_change >= MAX_DELAY

    def started(self, template_id: str, when: float | None = None) -> None:
        with self._lock:
            self._state(template_id).running_since = time.time() if when is None else when

    def finished(self, template_id: str, ok: bool, when: float | None = None) -> None:
        """Koniec dogrywki: zmiany sprzed jej startu są w kopii, późniejsze czekają."""
        moment = time.time() if when is None else when
        with self._lock:
            state = self._state(template_id)
            started = state.running_since or moment
            state.running_since = 0.0
            state.last_run = moment
            if not ok:
                state.retry_at = moment + RETRY_AFTER
                return
            state.retry_at = 0.0
            if state.last_change <= started:
                state.first_change = state.last_change = 0.0
            else:
                state.first_change = max(state.first_change, started)

    def hold(self, template_id: str) -> None:
        """Wstrzymanie do decyzji człowieka — np. podejrzanie dużo zmian (ransomware?)."""
        with self._lock:
            state = self._state(template_id)
            state.held = True
            state.running_since = 0.0

    def release(self, template_id: str) -> None:
        with self._lock:
            state = self._states.get(template_id)
            if state is not None:
                state.held = False
                state.retry_at = 0.0

    def forget(self, template_id: str) -> None:
        with self._lock:
            self._states.pop(template_id, None)


# ------------------------------------------------------------------ dokąd dogrywać


@dataclass(frozen=True)
class LivePlan:
    """Wersja do uzupełnienia (``""`` = nowa wersja z datą) i czy ją przy tym zamknąć pieczęcią."""

    target_version: str
    seal: bool


def _created_day(version_name: str) -> str:
    """``2026-10-01_@523--2026-10-02_@100`` → ``2026-10-01`` (data UTC utworzenia)."""
    return version_name.partition("--")[0].partition("_")[0]


def plan_live_run(runs: Sequence[VersionState], destination: str | Path, now: float,
                  timestamp: bool) -> LivePlan:
    """Dokąd dograć zmiany: ``runs`` to wersje tych samych źródeł, najnowsze najpierw."""
    if not runs:
        return LivePlan("", False)
    newest = runs[0]
    if (Path(destination) / newest.name / proof.SEAL_NAME).exists():
        return LivePlan("", False)  # opieczętowanej wersji nie ruszamy — nowa wersja
    today = datetime.fromtimestamp(now, UTC).strftime("%Y-%m-%d")
    older = _created_day(newest.name) != today
    if not older or not newest.complete or not newest.known:
        # dzisiejsza albo niedokończona: uzupełniamy; starszą przy okazji zamykamy pieczęcią
        return LivePlan(newest.name, timestamp and older)
    if timestamp:
        return LivePlan(newest.name, True)  # wczorajsza: dogrywka zamykająca z pieczęcią
    return LivePlan("", False)


# ------------------------------------------------------------------ obserwowanie folderów


def watchdog_available() -> bool:
    try:
        import watchdog.observers  # noqa: F401
    except ImportError:
        return False
    return True


def _inside(path: Path, folder: Path) -> bool:
    try:
        path.relative_to(folder)
    except ValueError:
        return False
    return True


class LiveWatcher:
    """Obserwuje foldery źródłowe szablonów „na bieżąco” i zgłasza zmiany trackerowi."""

    def __init__(self, tracker: ChangeTracker) -> None:
        self.tracker = tracker
        self.available = watchdog_available()
        self._observer = None
        self._wanted: dict[str, tuple[tuple[str, ...], str]] = {}
        #: szablony, których nie udało się obserwować — dla nich dogrywka co FALLBACK_INTERVAL
        self.unwatched: set[str] = set()

    def update(self, templates: Iterable[Template]) -> None:
        wanted = {t.id: (tuple(t.sources), t.destination) for t in templates}
        if wanted == self._wanted:
            return
        self.stop()
        self._wanted = wanted
        self.unwatched = set(wanted) if not self.available else set()
        if not wanted or not self.available:
            return
        from watchdog.observers import Observer

        observer = Observer()
        for template_id, (sources, destination) in wanted.items():
            handler = _Handler(self.tracker, template_id, destination)
            for source in sources:
                path = Path(source)
                try:
                    if path.is_dir():
                        observer.schedule(handler, str(path), recursive=True)
                    elif path.parent.is_dir():
                        observer.schedule(handler, str(path.parent), recursive=False)
                    else:
                        self.unwatched.add(template_id)
                except OSError as exc:
                    log.warning("Nie obserwuję %s (%s) — dogrywka co %d min.", source, exc,
                                FALLBACK_INTERVAL // 60)
                    self.unwatched.add(template_id)
        observer.daemon = True
        try:
            observer.start()
        except OSError as exc:
            log.warning("Obserwowanie folderów nie ruszyło (%s) — dogrywka co %d min.", exc,
                        FALLBACK_INTERVAL // 60)
            self.unwatched = set(wanted)
            return
        self._observer = observer
        log.info("Na bieżąco: obserwuję %d szablon(ów).", len(wanted))

    def stop(self) -> None:
        observer, self._observer = self._observer, None
        if observer is not None:
            observer.stop()
            observer.join(timeout=5)


try:  # obsługa zdarzeń potrzebuje klasy bazowej z biblioteki — bez niej tylko tryb zapasowy
    from watchdog.events import FileSystemEventHandler as _HandlerBase
except ImportError:  # pragma: no cover - środowisko bez watchdog
    _HandlerBase = object  # type: ignore[assignment,misc]


class _Handler(_HandlerBase):  # type: ignore[misc,valid-type]
    def __init__(self, tracker: ChangeTracker, template_id: str, destination: str) -> None:
        super().__init__()
        self.tracker = tracker
        self.template_id = template_id
        self.destination = Path(destination) if destination else None

    def on_any_event(self, event) -> None:
        if event.event_type in ("opened", "closed_no_write"):
            return
        if event.is_directory and event.event_type == "modified":
            return  # „katalog zmieniony” towarzyszy każdej zmianie pliku w nim
        if self.destination is not None:
            for raw in (event.src_path, getattr(event, "dest_path", "")):
                if raw and _inside(Path(raw), self.destination):
                    return  # zapis samej kopii (katalog docelowy wewnątrz źródła)
        self.tracker.note(self.template_id)
