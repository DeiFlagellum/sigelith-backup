"""Tłumaczenie tekstów samego Qt — przycisków okien standardowych („Tak”, „Nie”, „Anuluj”).

Bez tego polski interfejs pokazywał w oknach pytań angielskie „Yes” i „No”, bo te
napisy dostarcza Qt, a nie nasz katalog tłumaczeń. Pliki ``qtbase_<język>.qm``
przychodzą z PySide6 (do paczki trafiają tylko te dla języków programu — patrz
``cleanvault.spec``). Tu też ustawiamy kierunek okien: po arabsku układ idzie od
prawej do lewej.
"""

from __future__ import annotations

from pathlib import Path

import PySide6
from PySide6.QtCore import QCoreApplication, Qt, QTranslator
from PySide6.QtGui import QGuiApplication

from cleanvault import i18n

#: nazwa pliku Qt różni się od naszego kodu tylko dla chińskiego (uproszczony = zh_CN)
QT_NAMES = {"zh": "zh_CN"}

_installed: QTranslator | None = None


def apply(language: str) -> bool:
    """Ustawia tłumaczenie Qt i kierunek okien dla języka; ``True``, gdy teksty Qt są w tym języku."""
    global _installed
    app = QCoreApplication.instance()
    if app is None:
        return False
    if isinstance(app, QGuiApplication):
        app.setLayoutDirection(
            Qt.LayoutDirection.RightToLeft if i18n.is_rtl(language) else Qt.LayoutDirection.LeftToRight
        )
    if _installed is not None:
        app.removeTranslator(_installed)
        _installed = None
    if language == "en":
        return True  # Qt mówi po angielsku bez tłumaczenia
    translator = QTranslator(app)
    name = f"qtbase_{QT_NAMES.get(language, language)}"
    if not translator.load(name, str(Path(PySide6.__file__).parent / "translations")):
        return False
    app.installTranslator(translator)
    _installed = translator
    return True
