"""Licencje i prywatność: pliki dołączone do programu, ich aktualność i ekran „O programie”."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

pytest.importorskip("PySide6")

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

from cleanvault.state import StateStore
from cleanvault.ui import legal, qtlang
from cleanvault.ui.main_window import MainWindow

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import third_party_notices

LEGAL_FILES = ("LICENSE.txt", "THIRD-PARTY-NOTICES.txt", "LGPL-3.0.txt", "GPL-3.0.txt",
               "PYTHON-LICENSE.txt", "polityka-prywatnosci.md")


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


def test_legal_files_are_present_and_bundled():
    for name in LEGAL_FILES:
        assert legal.legal_path(name).stat().st_size > 500, name
    spec = (ROOT / "cleanvault.spec").read_text(encoding="utf-8")
    assert '("assets/legal", "assets/legal")' in spec
    assert "GNU LESSER GENERAL PUBLIC LICENSE" in legal.read_legal("LGPL-3.0.txt")
    assert "do użytku wewnętrznego" not in legal.read_legal("LICENSE.txt")


def test_notices_are_up_to_date_with_installed_libraries():
    assert third_party_notices.stale_files() == [], "uruchom tools/third_party_notices.py"


def test_every_runtime_library_is_listed_with_its_license_text():
    notices = legal.read_legal("THIRD-PARTY-NOTICES.txt")
    for key, dist in third_party_notices.runtime_distributions().items():
        name = dist.metadata["Name"]
        assert f"{name} {dist.version}" in notices, name
        if key not in third_party_notices.QT_DISTRIBUTIONS:
            assert f"--- {name} {dist.version} —" in notices, f"brak tekstu licencji: {name}"
    assert "pyside6-addons" not in third_party_notices.runtime_distributions()


def test_qt_is_attributed_with_lgpl_and_sources():
    notices = legal.read_legal("THIRD-PARTY-NOTICES.txt")
    assert "LGPL-3.0-only" in notices
    assert legal.QT_SOURCES in notices and legal.PYSIDE_SOURCES in notices
    for component in ("HarfBuzz-NG", "LibPNG", "PCRE2", "The Public Suffix List", "XSVG"):
        assert component in notices, component
    assert "Qt Virtual Keyboard" not in notices


def test_build_check_flags_an_unlisted_library():
    assert third_party_notices.unlisted({"PySide6", "Cryptodome", "msgpack", "winrt"}) == []
    assert third_party_notices.unlisted({"pytest"}) == ["pytest"], "biblioteka spoza wykazu jest wskazana"


def test_about_page_offers_licenses_and_privacy(qapp, tmp_path, monkeypatch):
    monkeypatch.setattr("cleanvault.state.state_file", lambda: tmp_path / "state.msgpack")
    window = MainWindow(StateStore(tmp_path / "state.msgpack"))
    try:
        dialog = legal.LegalDialog(window)
        assert dialog.tabs.count() == len(legal.LegalDialog.TABS)
        texts = [dialog.tabs.widget(i).toPlainText() for i in range(dialog.tabs.count())]
        assert all(len(text) > 500 for text in texts)
        privacy = legal.PrivacyDialog(window)
        assert "Sigelith" in privacy.view.toPlainText()
        assert "Menedżer" in privacy.view.toPlainText(), "polityka mówi, jak usunąć zapamiętane hasła"
    finally:
        window.close()


def test_qt_buttons_speak_polish(qapp):
    try:
        assert qtlang.apply("pl")
        assert QCoreApplication.translate("QPlatformTheme", "&Yes") == "&Tak"
    finally:
        qtlang.apply("en")
    assert QCoreApplication.translate("QPlatformTheme", "&Yes") == "&Yes"


def test_forgetting_passwords_clears_every_template_secret(qapp, tmp_path, monkeypatch):
    from PySide6.QtWidgets import QMessageBox

    from cleanvault import secrets_store
    from cleanvault.state import Template

    deleted = []
    monkeypatch.setattr(secrets_store, "delete_password", lambda name: deleted.append(name) or True)
    monkeypatch.setattr(QMessageBox, "question", lambda *args, **kwargs: QMessageBox.StandardButton.Yes)
    monkeypatch.setattr("cleanvault.state.state_file", lambda: tmp_path / "state.msgpack")
    store = StateStore(tmp_path / "state.msgpack")
    template = Template(name="Zaszyfrowana", remember_password=True)
    store.put_template(template)
    window = MainWindow(store)
    try:
        window._forget_all_passwords()
        assert set(deleted) == {template.id, f"offsite-key:{template.id}", f"offsite-password:{template.id}"}
        assert not store.get_template(template.id).remember_password
    finally:
        window.close()
