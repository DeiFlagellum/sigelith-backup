"""Wersja ze Sklepu (pakiet MSIX): start przy logowaniu, katalog danych, manifest."""

from __future__ import annotations

import importlib.util
import os
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from cleanvault import __version__, autostart, engine, paths

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_msix

NS = {
    "m": "http://schemas.microsoft.com/appx/manifest/foundation/windows10",
    "uap": "http://schemas.microsoft.com/appx/manifest/uap/windows10",
    "uap5": "http://schemas.microsoft.com/appx/manifest/uap/windows10/5",
    "uap10": "http://schemas.microsoft.com/appx/manifest/uap/windows10/10",
    "rescap": "http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities",
}


class FakeTask:
    """Zachowuje się jak ``Windows.ApplicationModel.StartupTask``."""

    def __init__(self, state: int) -> None:
        self.state = state

    def request_enable_async(self):
        async def operation():
            # wyłączonego przez użytkownika albo zasady firmy program nie włączy
            if self.state == autostart.TASK_DISABLED:
                self.state = autostart.TASK_ENABLED
            return self.state

        return operation()

    def disable(self) -> None:
        if self.state == autostart.TASK_ENABLED:
            self.state = autostart.TASK_DISABLED


@pytest.fixture()
def in_package(monkeypatch):
    monkeypatch.setattr(autostart, "packaged", lambda: True)
    monkeypatch.setattr(autostart, "is_frozen", lambda: True)
    task = FakeTask(autostart.TASK_DISABLED)
    monkeypatch.setattr(autostart, "_startup_task", lambda: task)
    return task


@pytest.mark.skipif(sys.platform != "win32", reason="Windows")
def test_packaged_autostart_switches_the_startup_task(in_package):
    assert autostart.supported()
    assert not autostart.is_enabled()
    assert autostart.set_enabled(True)
    assert autostart.is_enabled() and in_package.state == autostart.TASK_ENABLED
    assert autostart.set_enabled(False)
    assert not autostart.is_enabled()
    assert not autostart.blocked_in_windows()


@pytest.mark.skipif(sys.platform != "win32", reason="Windows")
def test_startup_disabled_in_windows_settings_is_reported_not_overridden(in_package):
    in_package.state = autostart.TASK_DISABLED_BY_USER
    assert not autostart.set_enabled(True)
    assert in_package.state == autostart.TASK_DISABLED_BY_USER
    assert autostart.blocked_in_windows()


@pytest.mark.skipif(sys.platform != "win32", reason="Windows")
def test_package_without_startup_task_is_not_supported(monkeypatch):
    monkeypatch.setattr(autostart, "packaged", lambda: True)
    monkeypatch.setattr(autostart, "is_frozen", lambda: True)
    monkeypatch.setattr(autostart, "_startup_task", lambda: None)
    assert not autostart.supported()
    assert not autostart.set_enabled(True)


def test_real_startup_task_lookup_fails_quietly_outside_a_package():
    # bez importu: winrt zaimportowany przed Qt wywraca proces (patrz autostart._startup_task)
    if importlib.util.find_spec("winrt") is None:
        pytest.skip("brak modułu winrt")
    assert paths.package_family_name() is None, "testy nie działają z pakietu"
    assert autostart._startup_task() is None


@pytest.mark.skipif(sys.platform != "win32", reason="Windows")
def test_store_version_keeps_data_in_local_state_and_adopts_exe_state(tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(paths, "package_family_name", lambda: "SigelithBackup.Test_abc123")
    exe_data = tmp_path / paths.APP_DIR_NAME
    exe_data.mkdir()
    (exe_data / "state.msgpack").write_bytes(b"stan z wersji EXE")

    folder = paths.data_dir()
    assert folder == tmp_path / "Packages" / "SigelithBackup.Test_abc123" / "LocalState"
    assert (folder / "state.msgpack").read_bytes() == b"stan z wersji EXE"
    assert (exe_data / "state.msgpack").exists(), "wersja EXE zachowuje swoje dane"

    (exe_data / "state.msgpack").write_bytes(b"nowszy stan wersji EXE")
    assert (paths.data_dir() / "state.msgpack").read_bytes() == b"stan z wersji EXE", "przejęcie tylko raz"


@pytest.mark.skipif(sys.platform != "win32", reason="Windows")
def test_store_version_adopts_state_from_the_old_program_name(tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    monkeypatch.setattr(paths, "package_family_name", lambda: "Rodzina_x")
    for name in paths.LEGACY_APP_DIR_NAMES:
        legacy = tmp_path / name
        legacy.mkdir()
        (legacy / "state.msgpack").write_bytes(name.encode())
    # Najnowsza wcześniejsza nazwa ma pierwszeństwo przed najstarszą.
    assert (paths.data_dir() / "state.msgpack").read_bytes() == b"Time Vault Backup"


def test_package_version_has_four_numbers_ending_with_zero():
    assert build_msix.package_version("2.0.0") == "2.0.0.0"
    assert build_msix.package_version("2.1") == "2.1.0.0"
    assert build_msix.package_version(__version__).endswith(".0")


def test_manifest_matches_the_program(tmp_path):
    build_msix.write_manifest(tmp_path, "Wydawca.SigelithBackup", 'CN="Firma & Syn", O=Test', "Firma & Syn",
                              "2.0.0.0")
    root = ET.parse(tmp_path / "AppxManifest.xml").getroot()
    identity = root.find("m:Identity", NS)
    assert identity.get("Name") == "Wydawca.SigelithBackup"
    assert identity.get("Publisher") == 'CN="Firma & Syn", O=Test'
    assert identity.get("Version") == "2.0.0.0"
    assert root.find("m:Properties/m:PublisherDisplayName", NS).text == "Firma & Syn"

    app = root.find("m:Applications/m:Application", NS)
    assert app.get("Executable") == "SigelithBackup.exe"
    assert app.get("EntryPoint") == "Windows.FullTrustApplication"
    startup = app.find("m:Extensions/uap5:Extension", NS)
    assert startup.get("Category") == "windows.startupTask"
    assert startup.get(f"{{{NS['uap10']}}}Parameters") == autostart.BACKGROUND_FLAG
    task = startup.find("uap5:StartupTask", NS)
    assert task.get("TaskId") == autostart.STARTUP_TASK_ID
    assert task.get("Enabled") == "false", "start przy logowaniu włącza użytkownik, nie instalator"

    capabilities = [c.get("Name") for c in root.find("m:Capabilities", NS)]
    assert capabilities == ["runFullTrust"], "żadnych innych uprawnień do uzasadniania w Sklepie"
    logos = [app.find("uap:VisualElements", NS).get(name) for name in ("Square150x150Logo", "Square44x44Logo")]
    assert all(logo.startswith("Assets") for logo in logos)


@pytest.fixture()
def appdata(tmp_path, monkeypatch):
    local, roaming = tmp_path / "Local", tmp_path / "Roaming"
    (local / "Microsoft").mkdir(parents=True)
    (roaming / "Microsoft" / "Windows" / "Start Menu" / "Programs").mkdir(parents=True)
    (roaming / "Thunderbird").mkdir()  # program, który już działał na tym komputerze
    monkeypatch.setenv("LOCALAPPDATA", str(local))
    monkeypatch.setenv("APPDATA", str(roaming))
    return local, roaming


@pytest.mark.skipif(sys.platform != "win32", reason="Windows")
def test_only_new_folders_directly_in_appdata_are_private_to_the_package(appdata, tmp_path, monkeypatch):
    local, roaming = appdata
    targets = [
        roaming / "Thunderbird" / "Profiles",  # folder istnieje — zapis prawdziwy
        roaming / "Nowy program" / "dane",  # nowy folder prosto w Roaming
        local / "Microsoft" / "Nowość",  # nowy folder w Local/Microsoft
        tmp_path / "Dokumenty" / "Raporty",  # poza AppData
    ]
    monkeypatch.setattr(paths, "package_family_name", lambda: None)
    assert paths.private_appdata_folders(targets) == [], "poza pakietem nic nie jest przekierowane"
    monkeypatch.setattr(paths, "package_family_name", lambda: "Rodzina_x")
    assert paths.private_appdata_folders(targets) == [roaming / "Nowy program", local / "Microsoft" / "Nowość"]
    assert paths.private_appdata_folders([roaming]) == [roaming], "pliki prosto w Roaming też"


def test_restore_roots_follow_the_layout(tmp_path):
    documents = "C:/Users/U/Documents"
    items = [
        engine.RestoreItem("Dokumenty/a.txt", tmp_path / "a", 1, False, original_root=documents),
        engine.RestoreItem("Dokumenty/b/c.txt", tmp_path / "c", 1, False, original_root=documents),
        engine.RestoreItem("Thunderbird/prefs.js", tmp_path / "p", 1, False),
    ]
    plan = engine.RestorePlan(tmp_path, items, tmp_path / "cel", layout="tree")
    assert engine.restore_roots(plan) == {tmp_path / "cel" / "Dokumenty", tmp_path / "cel" / "Thunderbird"}
    plan.layout = "flat"
    assert engine.restore_roots(plan) == {tmp_path / "cel"}
    plan.layout = "original"
    plan.roots = {"Thunderbird": "C:/Users/U/AppData/Roaming/Thunderbird"}
    assert engine.restore_roots(plan) == {Path(documents), Path("C:/Users/U/AppData/Roaming/Thunderbird")}


def _wait_for_window(qapp, window, timeout=60.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        qapp.processEvents()
        if window.worker is None and window._after_worker is None:
            qapp.processEvents()
            if window.worker is None:
                return
        time.sleep(0.02)
    pytest.fail("operacja nie zakończyła się w czasie")


@pytest.mark.skipif(sys.platform != "win32", reason="Windows")
def test_window_asks_before_restoring_into_a_private_appdata_folder(tmp_path, monkeypatch, appdata):
    pytest.importorskip("PySide6")
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication, QMessageBox

    from cleanvault.state import StateStore
    from cleanvault.ui.main_window import MainWindow

    qapp = QApplication.instance() or QApplication([])
    _local, roaming = appdata
    source = tmp_path / "Nowy program"
    source.mkdir()
    (source / "ustawienia.ini").write_text("[konto]", encoding="utf-8")
    config = engine.BackupConfig(sources=[str(source)], destination=str(tmp_path / "kopia"), structure="mirror",
                                 excludes=[], stamp_updates=False, catchup_passes=0)
    assert engine.run_backup(engine.plan_backup(config, engine.Reporter()), None, engine.Reporter()).ok

    answers = []

    def answer(box):
        wanted = answers.pop(0)
        next(b for b in box.buttons() if b.text() == wanted).click()
        return 0

    monkeypatch.setattr(QMessageBox, "exec", answer)
    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: None)
    monkeypatch.setattr("cleanvault.state.state_file", lambda: tmp_path / "state.msgpack")
    window = MainWindow(StateStore(tmp_path / "state.msgpack"))
    try:
        monkeypatch.setattr(paths, "package_family_name", lambda: "Rodzina_x")
        window.restore_src.set_path(str(tmp_path / "kopia"))
        window.restore_dst.set_path(str(roaming))
        window.layout_combo.setCurrentIndex(window.layout_combo.findData("tree"))
        window.collision_combo.setCurrentIndex(window.collision_combo.findData("rename"))

        answers.append("Anuluj")
        window._start_restore()
        _wait_for_window(qapp, window)
        assert not answers, "program zapytał"
        assert not (roaming / "Nowy program").exists(), "po odmowie nic nie zapisano"

        answers.append("Przywróć mimo to")
        window._start_restore()
        _wait_for_window(qapp, window)
        assert (roaming / "Nowy program" / "ustawienia.ini").read_text(encoding="utf-8") == "[konto]"
    finally:
        window.close()


def test_contained_path_is_decided_without_touching_the_disk(tmp_path):
    base = tmp_path / "cel"  # jeszcze nie istnieje — tak jest na początku przywracania
    assert paths.contained_path(base, "Dokumenty/a.txt") == base / "Dokumenty" / "a.txt"
    assert paths.contained_path(base, "") == base
    assert paths.contained_path(str(base).upper(), "x.txt") is not None, "wielkość liter bez znaczenia"
    for evil in ("../obok.txt", "a/../../obok.txt", "C:/Windows/zly.dll", "/Windows/zly.dll", "D:zly.txt"):
        assert paths.contained_path(base, evil) is None, evil
    assert paths.contained_path(base, "a/../b.txt") == base / "b.txt", "wewnątrz celu wolno"
    assert not base.exists(), "nic nie powstało na dysku"
