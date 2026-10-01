"""Działanie w tle: jedna instancja, ikona w zasobniku i zegar harmonogramu.

Harmonogram działa tylko wtedy, gdy program działa — aplikacja ze Sklepu nie
może oddać tej pracy Harmonogramowi Windows. Stąd trzy elementy:

* :class:`SingleInstance` — drugie uruchomienie programu (np. z menu Start,
  gdy pierwszy działa w tle) nie może postawić drugiego harmonogramu, bo ta
  sama kopia ruszyłaby dwa razy. Drugi proces przekazuje prośbę pierwszemu
  i kończy się;
* :class:`Tray` — ikona przy zegarze z menu i powiadomieniami;
* :class:`SchedulerService` — co pół minuty pyta :mod:`cleanvault.scheduler`,
  czy coś trzeba uruchomić, a dla szablonów „na bieżąco” także
  :mod:`cleanvault.live` (zmiany w źródłach). Samego uruchomienia nie robi:
  zgłasza to oknu.
"""

from __future__ import annotations

import getpass
import time

from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtGui import QAction, QIcon
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from PySide6.QtWidgets import QMenu, QSystemTrayIcon

from .. import live, scheduler
from ..i18n import tr
from ..log import get_logger
from ..state import StateStore
from . import icons

log = get_logger("ui.background")

#: Co ile milisekund harmonogram sprawdza terminy.
TICK_MS = 30_000
#: Wiadomości przekazywane przez drugą instancję pierwszej.
MSG_SHOW = "show"
MSG_BACKGROUND = "background"
#: Potwierdzenie odbioru wiadomości przez działający egzemplarz.
ACK = b"ok"


def instance_name() -> str:
    """Nazwa kanału jednej instancji — osobna dla każdego użytkownika systemu."""
    try:
        user = getpass.getuser()
    except Exception:  # noqa: BLE001 - brak nazwy użytkownika nie może zablokować startu
        user = "user"
    safe = "".join(ch for ch in user if ch.isalnum()) or "user"
    # Nazwa kanału zostaje sprzed zmiany nazwy programu (Time Vault Backup → Sigelith
    # Backup): stary i nowy egzemplarz muszą się widzieć, inaczej zaraz po aktualizacji
    # działałyby dwa harmonogramy na tym samym stanie i robiły te same kopie dwa razy.
    return f"TimeVaultBackup-{safe}"


class SingleInstance(QObject):
    """Pilnuje, by program działał w jednym egzemplarzu na użytkownika."""

    message_received = Signal(str)

    def __init__(self, name: str | None = None, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.name = name or instance_name()
        self._server: QLocalServer | None = None

    def forward_to_primary(self, message: str, timeout_ms: int = 2000) -> bool:
        """Przekazuje wiadomość działającej instancji; ``True`` = taka instancja jest.

        Klient czeka na potwierdzenie „ok”: w Windows zapis do nazwanego potoku
        bywa asynchroniczny i rozłączenie tuż po nim potrafi go anulować — bez
        potwierdzenia wiadomość (np. „pokaż okno”) potrafiła po prostu zniknąć.
        """
        socket = QLocalSocket()
        socket.connectToServer(self.name)
        if not socket.waitForConnected(400):
            return False
        socket.write(message.encode("utf-8"))
        socket.waitForBytesWritten(timeout_ms)
        # Krótkie odpytywanie zamiast jednego długiego czekania: w Windows pojedyncze
        # waitForReadyRead potrafi wrócić przed czasem, choć odpowiedź już płynie.
        reply = b""
        deadline = time.monotonic() + timeout_ms / 1000
        while not reply.startswith(ACK) and time.monotonic() < deadline:
            if socket.waitForReadyRead(100) or socket.bytesAvailable():
                reply += bytes(socket.readAll())
        acknowledged = reply.startswith(ACK)
        if not acknowledged:
            # Instancja istnieje, ale nie odpowiada. Drugiej i tak nie uruchamiamy —
            # dwa harmonogramy zrobiłyby tę samą kopię dwa razy.
            log.warning("Działający egzemplarz programu nie potwierdził wiadomości „%s”.", message)
        socket.disconnectFromServer()
        return True

    def become_primary(self) -> bool:
        """Zajmuje kanał; po awarii poprzedniego procesu sprząta jego pozostałość."""
        server = QLocalServer(self)
        if not server.listen(self.name):
            QLocalServer.removeServer(self.name)
            if not server.listen(self.name):
                log.warning("Nie udało się zająć kanału jednej instancji: %s", server.errorString())
                return False
        server.newConnection.connect(self._on_connection)
        self._server = server
        return True

    def _on_connection(self) -> None:
        while self._server is not None and self._server.hasPendingConnections():
            socket = self._server.nextPendingConnection()
            socket.readyRead.connect(lambda s=socket: self._read(s))
            socket.disconnected.connect(socket.deleteLater)
            if socket.bytesAvailable():
                self._read(socket)

    def _read(self, socket: QLocalSocket) -> None:
        message = bytes(socket.readAll()).decode("utf-8", "replace").strip()
        if not message:
            return
        socket.write(ACK)
        socket.waitForBytesWritten(500)
        self.message_received.emit(message)


class Tray(QObject):
    """Ikona przy zegarze: przywołanie okna, kopia teraz, wstrzymanie, zakończenie."""

    show_requested = Signal()
    backup_requested = Signal(str)
    pause_toggled = Signal(bool)
    quit_requested = Signal()

    def __init__(self, window_icon: QIcon, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.icon = QSystemTrayIcon(window_icon, self)
        self.icon.setToolTip("Sigelith Backup")
        self.menu = QMenu()
        self.icon.setContextMenu(self.menu)
        self.icon.activated.connect(self._on_activated)
        self._templates: list[tuple[str, str]] = []
        self._paused = False
        self.rebuild_menu()

    @staticmethod
    def available() -> bool:
        return QSystemTrayIcon.isSystemTrayAvailable()

    def show(self) -> None:
        self.icon.show()

    def hide(self) -> None:
        self.icon.hide()

    def set_templates(self, templates: list[tuple[str, str]]) -> None:
        """Lista (id, nazwa) szablonów do podmenu „Zrób kopię teraz”."""
        self._templates = templates
        self.rebuild_menu()

    def set_paused(self, paused: bool) -> None:
        self._paused = paused
        self.rebuild_menu()

    def rebuild_menu(self) -> None:
        self.menu.clear()
        open_action = QAction(tr("Otwórz Sigelith Backup"), self.menu)
        open_action.triggered.connect(self.show_requested.emit)
        self.menu.addAction(open_action)

        backups = self.menu.addMenu(icons.icon("play-circle"), tr("Zrób kopię teraz"))
        if not self._templates:
            empty = QAction(tr("(brak zapisanych szablonów)"), backups)
            empty.setEnabled(False)
            backups.addAction(empty)
        for template_id, name in self._templates:
            action = QAction(name, backups)
            action.triggered.connect(lambda _checked=False, tid=template_id: self.backup_requested.emit(tid))
            backups.addAction(action)

        self.menu.addSeparator()
        pause = QAction(tr("Wstrzymaj kopie planowe"), self.menu)
        pause.setCheckable(True)
        pause.setChecked(self._paused)
        pause.toggled.connect(self.pause_toggled.emit)
        self.menu.addAction(pause)
        self.menu.addSeparator()
        quit_action = QAction(tr("Zakończ"), self.menu)
        quit_action.triggered.connect(self.quit_requested.emit)
        self.menu.addAction(quit_action)

    def notify(self, title: str, text: str, warning: bool = False) -> None:
        kind = QSystemTrayIcon.MessageIcon.Warning if warning else QSystemTrayIcon.MessageIcon.Information
        if self.icon.isVisible():
            self.icon.showMessage(title, text, kind, 12_000)
        log.info("Powiadomienie: %s — %s", title, text)

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            self.show_requested.emit()


class SchedulerService(QObject):
    """Odmierza czas i zgłasza szablony, których termin nadszedł."""

    due = Signal(str, str)  # id szablonu, powód
    overdue = Signal(str)  # id szablonu

    def __init__(self, store: StateStore, parent: QObject | None = None, tick_ms: int = TICK_MS) -> None:
        super().__init__(parent)
        self.store = store
        self._seen: dict[str, bool] = {}
        self._reminded: dict[str, float] = {}
        #: „na bieżąco”: zgłoszone zmiany i decyzja, kiedy dograć; obserwator folderów
        self.live_tracker = live.ChangeTracker()
        self.live_watcher = live.LiveWatcher(self.live_tracker)
        self._timer = QTimer(self)
        self._timer.setInterval(tick_ms)
        self._timer.timeout.connect(self.check)
        # Pierwsze sprawdzenie chwilę po starcie — na własnym zegarze, a nie przez
        # statyczne QTimer.singleShot: tamto przeżywa zamknięcie okna i odpala
        # potem na zniszczonym obiekcie Qt, co kończyło się wywrotką procesu.
        self._first = QTimer(self)
        self._first.setSingleShot(True)
        self._first.setInterval(5_000)
        self._first.timeout.connect(self.check)

    @property
    def paused(self) -> bool:
        return bool(self.store.setting("schedule_paused", False))

    def set_paused(self, paused: bool) -> None:
        self.store.set_setting("schedule_paused", bool(paused))
        log.info("Kopie planowe %s.", "wstrzymane" if paused else "wznowione")

    def start(self) -> None:
        self._timer.start()
        self._first.start()

    def stop(self) -> None:
        self._timer.stop()
        self._first.stop()
        self.live_watcher.stop()

    def has_schedules(self) -> bool:
        return any(t.schedule != scheduler.MANUAL for t in self.store.templates().values())

    def check(self, now: float | None = None) -> list[scheduler.Due]:
        moment = time.time() if now is None else now
        templates = list(self.store.templates().values())
        found = [] if self.paused else scheduler.due_templates(templates, moment, seen=self._seen)
        for template in templates:
            if template.schedule in (scheduler.ON_CONNECT, scheduler.LIVE):
                self._seen[template.id] = scheduler.destination_available(template.destination)
        found += self._live_due(templates, moment, {item.template_id for item in found})
        for item in found:
            log.info("Termin kopii: %s (%s)", item.template_id, item.reason)
            self.due.emit(item.template_id, item.reason)
        for template in scheduler.overdue_templates(templates, moment):
            # jedno przypomnienie na dobę — nie przy każdym tyknięciu zegara
            if moment - self._reminded.get(template.id, 0.0) > 86400:
                self._reminded[template.id] = moment
                self.overdue.emit(template.id)
        return found

    def _live_due(self, templates: list, moment: float, already: set[str]) -> list[scheduler.Due]:
        """Szablony „na bieżąco”, w których źródłach zmiany zdążyły się uspokoić."""
        current = [t for t in templates if t.schedule == scheduler.LIVE]
        self.live_watcher.update(current)
        if self.paused:
            return []
        due = []
        for template in current:
            if template.id in already:
                continue
            if template.id in self.live_watcher.unwatched:
                # bez obserwatora (dysk sieciowy, brak biblioteki): dogrywka co kwadrans
                last = max(self.live_tracker.last_run(template.id), template.last_attempt or 0.0)
                if moment - last >= live.FALLBACK_INTERVAL:
                    self.live_tracker.note(template.id, moment - live.QUIET_SECONDS)
            if self.live_tracker.ready(template.id, moment) and scheduler.destination_available(
                template.destination
            ):
                log.info("Na bieżąco: dogrywka „%s”.", template.name)
                due.append(scheduler.Due(template.id, "live"))
        return due
