"""Praca w tle: kopie planowe bez okien dialogowych, zasobnik, jedna instancja, autostart.

Najważniejsza zasada tego pliku: kopia uruchomiona przez harmonogram **nie może
otworzyć żadnego okna dialogowego** — nikt nie siedzi przy komputerze, a modalne
okno zatrzymałoby kopię do rana. Testy podmieniają wszystkie okna dialogowe na
pułapki, które od razu kończą test niepowodzeniem.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication, QInputDialog, QMessageBox

from cleanvault import autostart, scheduler
from cleanvault.state import StateStore, Template
from cleanvault.ui.background import SchedulerService, SingleInstance
from cleanvault.ui.main_window import MainWindow


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


@pytest.fixture()
def window(qapp, tmp_path, monkeypatch):
    monkeypatch.setattr("cleanvault.state.state_file", lambda: tmp_path / "state.msgpack")
    win = MainWindow(StateStore(tmp_path / "state.msgpack"))
    yield win
    win._quitting = True
    win.close()


@pytest.fixture()
def no_dialogs(monkeypatch):
    def trap(*_args, **_kwargs):
        pytest.fail("kopia planowa otworzyła okno dialogowe")

    for name in ("information", "warning", "critical", "question"):
        monkeypatch.setattr(QMessageBox, name, trap)
    monkeypatch.setattr(QMessageBox, "exec", trap)
    monkeypatch.setattr(QInputDialog, "getText", trap)


class FakeTray:
    def __init__(self):
        self.messages: list[tuple[str, str, bool]] = []
        self.hidden = False

    def notify(self, title, text, warning=False):
        self.messages.append((title, text, warning))

    def hide(self):
        self.hidden = True

    def rebuild_menu(self):
        pass

    def set_templates(self, _templates):
        pass

    def set_paused(self, _paused):
        pass


def _wait_for_worker(qapp, window, timeout=60.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        qapp.processEvents()
        if window.worker is None and window._after_worker is None:
            # dokończenie łańcucha (inspekcja → kopia) idzie przez QTimer.singleShot(0)
            qapp.processEvents()
            if window.worker is None:
                return
        time.sleep(0.02)
    pytest.fail("operacja nie zakończyła się w czasie")


def _scheduled_template(tmp_path, **kwargs) -> Template:
    source = tmp_path / "Dokumenty"
    source.mkdir(exist_ok=True)
    (source / "raport.txt").write_text("treść raportu", encoding="utf-8")
    return Template(
        name="Codzienna",
        sources=[str(source)],
        destination=str(tmp_path / "kopia"),
        schedule=scheduler.DAILY,
        schedule_time="20:00",
        catchup_passes=0,
        **kwargs,
    )


def test_scheduled_backup_runs_without_any_dialog(qapp, window, tmp_path, no_dialogs):
    tray = FakeTray()
    window.tray = tray
    template = _scheduled_template(tmp_path)
    window.store.put_template(template)

    window._run_scheduled(template.id, "daily")
    _wait_for_worker(qapp, window)

    saved = window.store.get_template(template.id)
    assert saved.last_attempt > 0
    assert saved.last_success > 0, saved.last_result
    assert (tmp_path / "kopia").is_dir()
    history = window.store.history(5)
    assert history[0]["scheduled"] is True and history[0]["ok"] is True
    assert tray.messages and not tray.messages[-1][2], "po udanej kopii — zwykłe powiadomienie"


def test_unfinished_version_is_resumed_without_asking(qapp, window, tmp_path, no_dialogs, monkeypatch):
    template = _scheduled_template(tmp_path)
    window.store.put_template(template)
    asked = []
    monkeypatch.setattr(window, "_ask_continuation", lambda *a: asked.append(a) or False)
    # pierwsza kopia, a potem udajemy, że jej wersja jest niedokończona
    window._run_scheduled(template.id, "daily")
    _wait_for_worker(qapp, window)
    monkeypatch.setattr("cleanvault.engine.suggest_continuation", lambda info, labels: info.runs[0])

    window._run_scheduled(template.id, "missed")
    _wait_for_worker(qapp, window)
    assert asked == [], "harmonogram zapytał o dokończenie wersji"


def test_encrypted_template_without_saved_password_only_notifies(window, tmp_path, no_dialogs):
    tray = FakeTray()
    window.tray = tray
    template = _scheduled_template(tmp_path, encrypt=True, remember_password=False)
    window.store.put_template(template)

    window._run_scheduled(template.id, "daily")
    assert window.worker is None
    assert tray.messages and tray.messages[-1][2], "brak hasła to ostrzeżenie w powiadomieniu"


def test_busy_program_postpones_the_slot(window, tmp_path, no_dialogs):
    template = _scheduled_template(tmp_path)
    window.store.put_template(template)

    class Busy:
        def isRunning(self):
            return True

    window.worker = Busy()
    try:
        window._run_scheduled(template.id, "daily")
    finally:
        window.worker = None
    assert window.store.get_template(template.id).last_attempt == 0.0, "termin nie może przepaść"


def test_closing_hides_to_tray_when_backups_are_scheduled(window, tmp_path):
    tray = FakeTray()
    window.tray = tray
    window.store.put_template(_scheduled_template(tmp_path))
    window.show()

    window.close()
    assert not window.isVisible(), "okno powinno schować się do zasobnika"
    assert tray.messages, "pierwsze schowanie wyjaśnia, gdzie jest program"
    window.close()
    assert len(tray.messages) == 1, "wyjaśnienie tylko raz"

    window.quit_from_tray()
    assert tray.hidden


def test_closing_quits_without_schedules(window):
    window.tray = FakeTray()
    window.show()
    window.close()
    assert window.tray.hidden, "bez harmonogramu zamknięcie okna kończy program"


def test_scheduler_service_emits_due_and_respects_pause(qapp, tmp_path):
    store = StateStore(tmp_path / "state.msgpack")
    template = _scheduled_template(tmp_path, last_attempt=1.0)
    store.put_template(template)
    service = SchedulerService(store)
    fired = []
    service.due.connect(lambda tid, reason: fired.append((tid, reason)))

    service.check(now=time.time())
    assert [tid for tid, _ in fired] == [template.id]

    fired.clear()
    service.set_paused(True)
    service.check(now=time.time())
    assert fired == []


def test_overdue_reminder_once_a_day(qapp, tmp_path):
    store = StateStore(tmp_path / "state.msgpack")
    now = time.time()
    store.put_template(_scheduled_template(tmp_path, created=now - 30 * 86400, last_attempt=now))
    service = SchedulerService(store)
    reminded = []
    service.overdue.connect(reminded.append)
    service.check(now=now)
    service.check(now=now + 60)
    assert len(reminded) == 1
    service.check(now=now + 86400 + 1)
    assert len(reminded) == 2


SECOND_INSTANCE = """
import sys
from PySide6.QtCore import QCoreApplication
app = QCoreApplication([])
from cleanvault.ui.background import SingleInstance
print("forwarded" if SingleInstance(sys.argv[1]).forward_to_primary("show") else "alone")
"""


def test_second_instance_forwards_to_the_first(qapp):
    """Drugi egzemplarz jest osobnym procesem — dokładnie jak przy starcie z menu Start.

    (Wcześniej w wątku: gniazdo Qt z wątku, który potem znika, zostawiało
    oczekujące operacje, które wywracały proces testów kilkadziesiąt testów dalej.)
    """
    name = f"SigelithBackup-test-{uuid.uuid4().hex[:8]}"
    first = SingleInstance(name)
    assert first.become_primary()
    received = []
    first.message_received.connect(received.append)

    second = subprocess.Popen(
        [sys.executable, "-c", SECOND_INSTANCE, name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(Path(__file__).resolve().parents[1]),
    )
    deadline = time.monotonic() + 30
    while second.poll() is None and time.monotonic() < deadline:
        qapp.processEvents()
        time.sleep(0.01)
    qapp.processEvents()
    output, errors = second.communicate(timeout=5)
    assert output.strip() == "forwarded", errors
    assert received == ["show"]
    assert "nie potwierdził" not in errors, "wiadomość dotarła bez potwierdzenia"


def test_no_primary_means_nothing_to_forward(qapp):
    lonely = SingleInstance(f"SigelithBackup-test-{uuid.uuid4().hex[:8]}")
    assert not lonely.forward_to_primary("show")


@pytest.mark.skipif(os.name != "nt", reason="rejestr Windows")
def test_autostart_writes_and_removes_its_entry(monkeypatch):
    import winreg

    test_key = r"Software\SigelithBackupTests\Run"
    winreg.CreateKey(winreg.HKEY_CURRENT_USER, test_key).Close()
    monkeypatch.setattr(autostart, "RUN_KEY", test_key)
    monkeypatch.setattr(autostart, "supported", lambda: True)
    try:
        assert autostart.set_enabled(True)
        assert autostart.is_enabled()
        assert autostart.set_enabled(False)
        assert not autostart.is_enabled()
        assert autostart.set_enabled(False), "wyłączenie wyłączonego nie jest błędem"
    finally:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, test_key)
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\SigelithBackupTests")


@pytest.mark.skipif(os.name != "nt", reason="rejestr Windows")
def test_autostart_moves_from_the_previous_program_name(monkeypatch):
    """Wpis „Time Vault Backup” wskazuje stary EXE — po zmianie nazwy uruchamiałby dawny program."""
    import winreg

    test_key = r"Software\SigelithBackupTests\Run"
    winreg.CreateKey(winreg.HKEY_CURRENT_USER, test_key).Close()
    monkeypatch.setattr(autostart, "RUN_KEY", test_key)
    monkeypatch.setattr(autostart, "supported", lambda: True)
    monkeypatch.setattr(autostart, "packaged", lambda: False)
    try:
        assert not autostart.migrate_legacy(), "bez starego wpisu nic się nie dzieje"
        assert not autostart.is_enabled(), "start nie włącza się sam"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, test_key, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "Time Vault Backup", 0, winreg.REG_SZ,
                              r'"C:\Stary\TimeVaultBackup.exe" --background')
        assert autostart.migrate_legacy()
        assert autostart.is_enabled(), "start przeniesiony na obecny program"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, test_key) as key, pytest.raises(FileNotFoundError):
            winreg.QueryValueEx(key, "Time Vault Backup")
        assert not autostart.migrate_legacy(), "przeniesienie tylko raz"
    finally:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, test_key)
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\SigelithBackupTests")


def test_autostart_is_off_when_running_from_sources():
    assert not autostart.supported()
    assert not autostart.set_enabled(True)


def _encrypted_looking_source(tmp_path, window):
    """Źródło z pierwszą kopią, potem połowa plików „zaszyfrowana” szumem."""
    template = _scheduled_template(tmp_path)
    source = Path(template.sources[0])
    for index in range(300):
        (source / f"notatka{index:03}.txt").write_text(f"Notatka {index}. " * 60, encoding="utf-8")
    window.store.put_template(template)
    window._run_scheduled(template.id, "daily")
    return template, source


def test_scheduled_backup_pauses_on_mass_change(qapp, window, tmp_path, no_dialogs):
    tray = FakeTray()
    window.tray = tray
    template, source = _encrypted_looking_source(tmp_path, window)
    _wait_for_worker(qapp, window)
    versions_before = sorted(p.name for p in (tmp_path / "kopia").iterdir() if p.is_dir())
    for path in sorted(source.glob("notatka*.txt"))[:150]:
        path.write_bytes(os.urandom(4096))

    template = window.store.get_template(template.id)
    template.last_attempt = 0.0
    window.store.put_template(template)
    window._run_scheduled(template.id, "daily")
    _wait_for_worker(qapp, window)

    title, text, warning = tray.messages[-1]
    assert warning and "wstrzymana" in title
    assert "sprawdź pliki" in text
    versions_after = sorted(p.name for p in (tmp_path / "kopia").iterdir() if p.is_dir())
    assert versions_after == versions_before, "przed decyzją nic nie może trafić do kopii"


def test_manual_backup_asks_and_continues_after_confirmation(qapp, window, tmp_path, monkeypatch):
    template, source = _encrypted_looking_source(tmp_path, window)
    _wait_for_worker(qapp, window)
    for path in sorted(source.glob("notatka*.txt"))[:150]:
        path.write_bytes(os.urandom(4096))

    asked = []

    def choose_continue(box):
        asked.append(box.text())
        next(b for b in box.buttons() if "Kontynuuj" in b.text()).click()
        return 0

    monkeypatch.setattr(QMessageBox, "exec", choose_continue)
    monkeypatch.setattr(QMessageBox, "information", lambda *a, **k: None)
    monkeypatch.setattr(window, "_ask_continuation", lambda *a: False)  # nowa wersja
    window._run_template_now(window.store.get_template(template.id))
    _wait_for_worker(qapp, window)

    assert asked and "ransomware" in asked[0]
    saved = window.store.get_template(template.id)
    assert window.store.history(1)[0]["ok"], saved.last_result


def test_replacing_a_template_keeps_its_schedule_and_cloud(window, tmp_path, monkeypatch):
    """Regresja: „Zapisz jako szablon” pod istniejącą nazwą kasowało harmonogram."""
    template = _scheduled_template(tmp_path, offsite={"endpoint": "https://x", "bucket": "b"},
                                   offsite_enabled=True, last_success=123.0)
    window.store.put_template(template)
    window._apply_template_to_form(template)
    monkeypatch.setattr(QInputDialog, "getText", lambda *a, **k: (template.name, True))
    monkeypatch.setattr(QMessageBox, "question", lambda *a, **k: QMessageBox.StandardButton.Yes)
    window.catchup_spin.setValue(3)
    window._save_as_template()

    saved = window.store.get_template(template.id)
    assert saved.catchup_passes == 3, "zmiana z formularza weszła"
    assert saved.schedule == scheduler.DAILY and saved.schedule_time == "20:00"
    assert saved.offsite_enabled and saved.offsite["bucket"] == "b"
    assert saved.last_success == 123.0


def test_successful_backup_is_followed_by_the_offsite_snapshot(qapp, window, tmp_path, no_dialogs, monkeypatch):
    from fake_s3 import FakeS3

    from cleanvault import offsite
    from cleanvault.s3 import S3Client, S3Target
    from cleanvault.ui import cloud

    with FakeS3() as server:
        tray = FakeTray()
        window.tray = tray
        target = S3Target(endpoint=server.endpoint, region="x", bucket="kubel", access_key="AKIATEST")
        template = _scheduled_template(tmp_path, offsite=target.to_dict(), offsite_enabled=True)
        window.store.put_template(template)
        monkeypatch.setattr(cloud, "secrets_for", lambda _tid: ("sekret", "hasło-chmury-2026"))

        window._run_scheduled(template.id, "daily")
        _wait_for_worker(qapp, window)

        stamps = offsite.list_snapshots(S3Client(target, "sekret"))
        assert len(stamps) == 1, "po udanej kopii lokalnej powinna powstać migawka poza domem"
        assert window.store.history(1)[0]["action"] == "offsite"
        assert window.store.get_template(template.id).offsite_last > 0

