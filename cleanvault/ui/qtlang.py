"""Tłumaczenie tekstów samego Qt — przycisków okien standardowych („Tak”, „Nie”, „Anuluj”).

Bez tego polski interfejs pokazywał w oknach pytań angielskie „Yes” i „No”, bo te
napisy dostarcza Qt, a nie nasz katalog tłumaczeń. Plik ``qtbase_pl.qm`` przychodzi
z PySide6 (do paczki trafia tylko on — patrz ``cleanvault.spec``).
"""

from __future__ import annotations

from pathlib import Path

import PySide6
from PySide6.QtCore import QCoreApplication, QTranslator

_installed: QTranslator | None = None


def apply(language: str) -> bool:
    """Ustawia tłumaczenie Qt dla języka interfejsu; ``True``, gdy teksty Qt są w tym języku."""
    global _installed
    app = QCoreApplication.instance()
    if app is None:
        return False
    if _installed is not None:
        app.removeTranslator(_installed)
        _installed = None
    if language == "en":
        return True  # Qt mówi po angielsku bez tłumaczenia
    translator = QTranslator(app)
    if not translator.load(f"qtbase_{language}", str(Path(PySide6.__file__).parent / "translations")):
        return False
    app.installTranslator(translator)
    _installed = translator
    return True
