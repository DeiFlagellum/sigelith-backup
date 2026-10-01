"""Ekran przeglądania: drzewo wersji, historia pliku, wyszukiwarka i odtworzenie jednego pliku."""

from __future__ import annotations

import os
import time
from pathlib import Path

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication, QFileDialog, QInputDialog

from cleanvault import crypto, engine
from cleanvault.crypto import KdfParams, PasswordKeyring
from cleanvault.engine import BackupConfig, Reporter
from cleanvault.state import StateStore
from cleanvault.ui import browser as browser_module
from cleanvault.ui.browser import BrowserPage
from cleanvault.ui.main_window import MainWindow

PASSWORD = "Hasło-podglądu"


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture()
def source(tmp_path):
    root = tmp_path / "Dane"
    (root / "Umowy").mkdir(parents=True)
    (root / "Umowy" / "najem.txt").write_text("wersja 1", encoding="utf-8")
    (root / "notatka.txt").write_text("notatka", encoding="utf-8")
    return root


@pytest.fixture()
def page(qapp):
    widget = BrowserPage()
    yield widget
    widget.shutdown()


def _backup(source, destination, password=None):
    config = BackupConfig(sources=[str(source)], destination=str(destination), structure="dated", excludes=[],
                          stamp_updates=False, catchup_passes=0, encrypt=password is not None)
    key = PasswordKeyring(password, KdfParams(crypto.KDF_PBKDF2_SHA256, b"b" * 16, 1000)) if password else None
    plan = engine.plan_backup(config, Reporter())
    result = engine.run_backup(plan, key, Reporter())
    assert result.ok, result.errors
    return plan


def _wait(qapp, page):
    """Czeka na wątek roboczy i dostarcza jego sygnały do ekranu."""
    assert page._worker is not None
    assert page._worker.wait(30_000)
    for _ in range(5):
        qapp.processEvents()


def _open_tree(page, *names):
    """Rozwija kolejne foldery drzewa i zwraca węzeł ostatniej nazwy."""
    parent = page.tree.invisibleRootItem()
    node = None
    for name in names:
        node = next(parent.child(i) for i in range(parent.childCount()) if parent.child(i).text(0) == name)
        page.tree.expandItem(node)
        parent = node
    return node


def test_tree_shows_versions_and_saves_a_single_file(qapp, page, tmp_path, source, monkeypatch):
    destination = tmp_path / "kopia"
    _backup(source, destination)
    time.sleep(0.05)
    (source / "Umowy" / "najem.txt").write_text("wersja 2, dłuższa", encoding="utf-8")
    newest = _backup(source, destination)

    page.open_backup(str(destination))
    assert page.version_combo.count() == 2
    assert page.version_combo.currentData() == newest.version
    assert [page.tree.topLevelItem(i).text(0) for i in range(page.tree.topLevelItemCount())] == ["Dane"]
    assert not page.open_btn.isEnabled(), "nic nie zaznaczono"
    page.tree.setCurrentItem(_open_tree(page, "Dane", "Umowy"))
    assert not page.open_btn.isEnabled(), "folderu się nie otwiera"
    page.tree.setCurrentItem(_open_tree(page, "Dane", "Umowy", "najem.txt"))
    assert page.open_btn.isEnabled() and page.save_btn.isEnabled() and page.history_btn.isEnabled()

    target = tmp_path / "zapisany.txt"
    monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *args, **kwargs: (str(target), ""))
    page._save_copy()
    _wait(qapp, page)
    assert target.read_text(encoding="utf-8") == "wersja 2, dłuższa"

    page._show_history()
    assert page.history.count() == 2 and not page.history.isHidden()
    opened = []
    monkeypatch.setattr(browser_module.QDesktopServices, "openUrl", lambda url: opened.append(url.toLocalFile()))
    page._open_from_history(page.history.item(1))
    _wait(qapp, page)
    assert Path(opened[0]).read_text(encoding="utf-8") == "wersja 1"
    temp = page._temp
    page.shutdown()
    assert not Path(temp).exists(), "podgląd nie zostaje na dysku po zamknięciu"


def test_encrypted_copy_asks_for_the_password_until_it_is_right(qapp, page, tmp_path, source, monkeypatch):
    destination = tmp_path / "kopia"
    _backup(source, destination, PASSWORD)
    page.open_backup(str(destination))
    page.tree.setCurrentItem(_open_tree(page, "Dane", "notatka.txt"))
    answers = iter([("złe hasło", True), (PASSWORD, True)])
    asked = []

    def ask(*args, **kwargs):
        asked.append(1)
        return next(answers)

    monkeypatch.setattr(QInputDialog, "getText", ask)
    target = tmp_path / "odszyfrowana.txt"
    monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *args, **kwargs: (str(target), ""))
    page._save_copy()
    _wait(qapp, page)
    assert not target.exists(), "złe hasło nie zostawia niczego pod docelową nazwą"
    page._save_copy()
    _wait(qapp, page)
    assert target.read_text(encoding="utf-8") == "notatka"
    page._save_copy()  # hasło już znane — bez pytania
    _wait(qapp, page)
    assert len(asked) == 2


def test_search_results_open_the_newest_copy(qapp, page, tmp_path, source, monkeypatch):
    destination = tmp_path / "kopia"
    _backup(source, destination)
    page.open_backup(str(destination))
    page.search_edit.setText("NAJEM")
    page._search()
    _wait(qapp, page)
    assert [page.tree.topLevelItem(i).text(0) for i in range(page.tree.topLevelItemCount())] == [
        "Dane/Umowy/najem.txt"
    ]
    page.tree.setCurrentItem(page.tree.topLevelItem(0))
    opened = []
    monkeypatch.setattr(browser_module.QDesktopServices, "openUrl", lambda url: opened.append(url.toLocalFile()))
    page._open_copy()
    _wait(qapp, page)
    assert Path(opened[0]).read_text(encoding="utf-8") == "wersja 1"
    page._load_version()  # „Pokaż foldery” wraca do drzewa
    assert page.tree.topLevelItem(0).text(0) == "Dane"


def test_restore_screen_leads_to_the_browser(qapp, tmp_path, source, monkeypatch):
    destination = tmp_path / "kopia"
    _backup(source, destination)
    monkeypatch.setattr("cleanvault.state.state_file", lambda: tmp_path / "state.msgpack")
    window = MainWindow(StateStore(tmp_path / "state.msgpack"))
    try:
        assert not window.browse_btn.isEnabled()
        window.restore_src.set_path(str(destination))
        assert window.browse_btn.isEnabled()
        window.browse_btn.click()
        assert window.stack.currentIndex() == MainWindow.PAGE_BROWSE
        assert window.browser.version_combo.count() == 1
        assert window.browser.tree.topLevelItem(0).text(0) == "Dane"
    finally:
        window.close()
