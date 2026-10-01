"""Wątek roboczy dla operacji dyskowych.

W wersji 1.x ``perform_backup`` był wołany prosto z obsługi kliknięcia, czyli
w wątku GUI. Przy kopii kilku gigabajtów Windows oznaczał okno jako
„nie odpowiada", pasek postępu (utworzony, ale nigdy nieaktualizowany) stał
w miejscu, a przerwanie operacji było niemożliwe.

Tutaj każda operacja idzie do :class:`EngineWorker`, a komunikacja z GUI
odbywa się wyłącznie sygnałami — to jedyny bezpieczny sposób dotykania
widgetów Qt z innego wątku.
"""

from __future__ import annotations

import threading
import time
from collections.abc import Callable

from PySide6.QtCore import QThread, Signal

from ..engine import Reporter
from ..i18n import tr
from ..log import get_logger

log = get_logger("ui.worker")

#: Minimalny odstęp między aktualizacjami postępu. Bez throttlingu kopia
#: tysięcy małych plików zalewałaby pętlę zdarzeń sygnałami i sama się dławiła.
UPDATE_INTERVAL = 0.08


class EngineWorker(QThread):
    """Uruchamia dowolną operację silnika, raportując postęp sygnałami."""

    stage_changed = Signal(str)
    file_changed = Signal(str, int, int)
    bytes_advanced = Signal(int)
    succeeded = Signal(object)
    failed = Signal(str)
    #: sam wyjątek — przed ``failed``, żeby okno mogło rozpoznać jego rodzaj
    #: (np. wstrzymanie kopii przy podejrzanie masowych zmianach)
    error = Signal(object)

    def __init__(self, job: Callable[[Reporter], object], description: str = "") -> None:
        super().__init__()
        self._job = job
        self._description = description
        self._cancel_event = threading.Event()
        self._pending_bytes = 0
        self._last_emit = 0.0
        self._last_file_emit = 0.0
        self._lock = threading.Lock()

    # ------------------------------------------------------------ sterowanie

    def cancel(self) -> None:
        log.info("Zgłoszono przerwanie operacji: %s", self._description or "operacja")
        self._cancel_event.set()

    @property
    def is_cancelled(self) -> bool:
        return self._cancel_event.is_set()

    # --------------------------------------------------------------- przebieg

    def _emit_bytes(self, delta: int) -> None:
        """Zbiera przyrosty i wysyła je nie częściej niż co ``UPDATE_INTERVAL``."""
        with self._lock:
            self._pending_bytes += delta
            now = time.monotonic()
            if now - self._last_emit < UPDATE_INTERVAL:
                return
            pending, self._pending_bytes = self._pending_bytes, 0
            self._last_emit = now
        self.bytes_advanced.emit(pending)

    def _emit_file(self, name: str, index: int, total: int) -> None:
        """Nazwa bieżącego pliku, nie częściej niż co ``UPDATE_INTERVAL``.

        Kopia równoległa kończy setki plików na sekundę, i to z wielu wątków
        naraz — sygnał na każdy plik zalewałby pętlę zdarzeń okna.
        """
        with self._lock:
            now = time.monotonic()
            if index not in (0, 1, total) and now - self._last_file_emit < UPDATE_INTERVAL:
                return
            self._last_file_emit = now
        self.file_changed.emit(name, index, total)

    def _flush_bytes(self) -> None:
        with self._lock:
            pending, self._pending_bytes = self._pending_bytes, 0
        if pending:
            self.bytes_advanced.emit(pending)

    def run(self) -> None:
        reporter = Reporter(
            on_stage=self.stage_changed.emit,
            on_file=self._emit_file,
            on_bytes=self._emit_bytes,
            is_cancelled=self._cancel_event.is_set,
        )
        try:
            result = self._job(reporter)
            self._flush_bytes()
            self.succeeded.emit(result)
        except Exception as exc:
            self._flush_bytes()
            log.exception("Operacja zakończona błędem: %s", self._description or "operacja")
            self.error.emit(exc)
            self.failed.emit(str(exc))


class ProgressTracker:
    """Przelicza postęp na procenty, prędkość i szacowany czas zakończenia."""

    def __init__(self, total_bytes: int) -> None:
        self.total = max(0, total_bytes)
        self.done = 0
        self.started = time.monotonic()

    def advance(self, delta: int) -> None:
        self.done += delta

    @property
    def elapsed(self) -> float:
        return max(0.001, time.monotonic() - self.started)

    @property
    def percent(self) -> int:
        if self.total <= 0:
            return 0
        return min(100, int(self.done * 100 / self.total))

    @property
    def speed(self) -> float:
        """Bajty na sekundę."""
        return self.done / self.elapsed

    @property
    def eta_seconds(self) -> float:
        speed = self.speed
        if speed <= 0 or self.total <= 0 or self.done >= self.total:
            return 0.0
        return (self.total - self.done) / speed

    def describe(self) -> str:
        from ..engine import human_size

        if self.total <= 0:
            return tr("{done} • {speed}/s").format(
                done=human_size(self.done), speed=human_size(self.speed)
            )
        eta = self.eta_seconds
        eta_text = (
            tr(" • pozostało {time}").format(time=format_duration(eta)) if eta > 1 else ""
        )
        return tr("{done} z {total} • {speed}/s{eta}").format(
            done=human_size(self.done),
            total=human_size(self.total),
            speed=human_size(self.speed),
            eta=eta_text,
        )


def format_duration(seconds: float) -> str:
    seconds = int(max(0, seconds))
    if seconds < 60:
        return tr("{seconds} s").format(seconds=seconds)
    minutes, secs = divmod(seconds, 60)
    if minutes < 60:
        return tr("{minutes} min {seconds} s").format(minutes=minutes, seconds=secs)
    hours, minutes = divmod(minutes, 60)
    return tr("{hours} h {minutes} min").format(hours=hours, minutes=minutes)
