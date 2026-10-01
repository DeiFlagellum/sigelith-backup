"""Licencja programu, licencje składników i polityka prywatności — w samym programie.

Zasady Microsoft Store (10.2) wymagają, by program zawierał wszystkie informacje
wymagane prawem, a licencje MIT, BSD, Apache i LGPL — informacji o prawach
autorskich i tekstów licencji przy każdej kopii programu. Pliki leżą w
``assets/legal`` (zbiorczy wykaz tworzy ``tools/third_party_notices.py``).
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices, QFontDatabase
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QPlainTextEdit,
    QTabWidget,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from ..i18n import mark, tr
from ..paths import resource_path
from .widgets import button, field_help

LICENSE = "LICENSE.txt"
NOTICES = "THIRD-PARTY-NOTICES.txt"
PRIVACY = "polityka-prywatnosci.md"
#: Kod źródłowy bibliotek na LGPL w wersjach dołączonych do programu.
QT_SOURCES = "https://download.qt.io/official_releases/qt/6.11/6.11.2/"
PYSIDE_SOURCES = "https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-6.11.2-src/"


def legal_path(name: str) -> Path:
    return resource_path("assets", "legal", name)


def read_legal(name: str) -> str:
    try:
        return legal_path(name).read_text(encoding="utf-8")
    except OSError:
        return tr("Brak pliku {name} w katalogu programu.").format(name=name)


def _text_view(text: str) -> QPlainTextEdit:
    view = QPlainTextEdit()
    view.setReadOnly(True)
    view.setFont(QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont))
    view.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
    view.setPlainText(text)
    return view


class LegalDialog(QDialog):
    """Licencja programu i licencje składników, z pełnymi tekstami."""

    TABS = (
        (LICENSE, mark("Licencja programu")),
        (NOTICES, mark("Składniki i ich licencje")),
        ("LGPL-3.0.txt", "LGPL-3.0"),
        ("GPL-3.0.txt", "GPL-3.0"),
        ("PYTHON-LICENSE.txt", "Python"),
    )

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("Licencje"))
        self.resize(900, 640)
        layout = QVBoxLayout(self)
        layout.addWidget(field_help(
            tr("Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0 — to osobne pliki "
               "w katalogu programu, które można zastąpić zgodnymi wersjami. Kod źródłowy wersji "
               "dołączonych do programu: {qt} oraz {pyside}.").format(qt=QT_SOURCES, pyside=PYSIDE_SOURCES)
        ))
        self.tabs = QTabWidget()
        for name, title in self.TABS:
            self.tabs.addTab(_text_view(read_legal(name)), tr(title))
        layout.addWidget(self.tabs, 1)
        row = QHBoxLayout()
        row.addWidget(button(tr("Pokaż pliki licencji"), tr("Otwiera folder z plikami licencji w Eksploratorze"),
                             lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(str(legal_path(""))))))
        row.addWidget(button(tr("Kod źródłowy Qt"), tr("Strona z kodem źródłowym Qt w wersji użytej w programie"),
                             lambda: QDesktopServices.openUrl(QUrl(QT_SOURCES))))
        row.addStretch(1)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        row.addWidget(buttons)
        layout.addLayout(row)


class PrivacyDialog(QDialog):
    """Polityka prywatności — ten sam tekst, który wydawca publikuje pod adresem w Sklepie."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("Polityka prywatności"))
        self.resize(820, 640)
        layout = QVBoxLayout(self)
        self.view = QTextBrowser()
        self.view.setOpenExternalLinks(True)
        self.view.setMarkdown(read_legal(PRIVACY))
        layout.addWidget(self.view, 1)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
