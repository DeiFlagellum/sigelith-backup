"""Tłumaczenia interfejsu.

Językiem źródłowym jest polski: w kodzie stoją zwykłe polskie napisy owinięte
w :func:`tr`, a tłumaczenie to słownik „polski tekst → obcy tekst”. Dzięki temu
kod czyta się tak samo jak wcześniej i nie trzeba wymyślać kluczy dla kilkuset
zdań, a brak tłumaczenia nigdy nie kończy się pustym ekranem — najwyżej zdaniem
po polsku. Test ``tests/test_i18n.py`` pilnuje, by takich braków nie było.

Katalogi są zwykłymi modułami Pythona (``cleanvault/locale/en.py``), a nie
plikami danych: PyInstaller dołącza je sam, bez wpisów w ``datas``, więc wersja
EXE nie może zgubić tłumaczeń.
"""

from __future__ import annotations

import importlib
import locale as _locale
import os

from .log import get_logger

log = get_logger("i18n")

#: język źródłowy — w nim napisane są teksty w kodzie
SOURCE_LANGUAGE = "pl"

#: kody i nazwy własne języków, w kolejności wyświetlania w ustawieniach
LANGUAGES: dict[str, str] = {
    "pl": "Polski",
    "en": "English",
}

_language = SOURCE_LANGUAGE
_catalog: dict[str, str] = {}


def system_language() -> str:
    """Język systemu sprowadzony do obsługiwanego kodu; ``pl`` gdy nie wiadomo.

    Zmienne środowiskowe mają pierwszeństwo przed ustawieniem systemowym, bo
    tak działa reszta narzędzi wiersza poleceń i tak testuje się tę funkcję.
    """
    for name in ("TVB_LANG", "LANGUAGE", "LC_ALL", "LANG"):
        value = os.environ.get(name)
        if value:
            code = value.split(".")[0].split("_")[0].lower()
            if code in LANGUAGES:
                return code
    try:
        system = _locale.getlocale()[0] or ""
    except ValueError:  # pragma: no cover - zepsute ustawienia regionalne
        system = ""
    code = system.split("_")[0].lower()
    if code in LANGUAGES:
        return code
    # Windows zwraca nazwy w rodzaju „Polish_Poland”; sprawdzamy też je.
    for candidate, name in {"pl": "polish", "en": "english"}.items():
        if system.lower().startswith(name):
            return candidate
    return SOURCE_LANGUAGE


def set_language(code: str | None) -> str:
    """Ustawia język; ``auto``/pusty oznacza język systemu. Zwraca kod użyty."""
    global _language, _catalog
    wanted = (code or "auto").lower()
    if wanted in ("", "auto", "system"):
        wanted = system_language()
    if wanted not in LANGUAGES:
        log.warning("Nieznany język %s — zostaje %s", code, SOURCE_LANGUAGE)
        wanted = SOURCE_LANGUAGE
    _language = wanted
    _catalog = {} if wanted == SOURCE_LANGUAGE else _load(wanted)
    return wanted


def _load(code: str) -> dict[str, str]:
    try:
        module = importlib.import_module(f".locale.{code}", __package__)
    except ImportError:
        log.warning("Brak katalogu tłumaczeń dla języka %s", code)
        return {}
    return dict(getattr(module, "TEXTS", {}))


def language() -> str:
    return _language


def tr(text: str) -> str:
    """Tłumaczy tekst na bieżący język; nieprzetłumaczony zwraca bez zmian."""
    if not _catalog:
        return text
    return _catalog.get(text, text)


def mark(text: str) -> str:
    """Znaczy tekst do tłumaczenia bez tłumaczenia go tu i teraz.

    Potrzebne tam, gdzie napis powstaje przy imporcie modułu (stałe klasowe,
    słowniki), a język bywa ustawiany później: taki tekst przechodzi przez
    :func:`tr` dopiero w miejscu użycia. Katalog tłumaczeń wypełnia się na
    podstawie obu wywołań, więc nic się nie gubi.
    """
    return text


def plural(number: int, one: str, few: str, many: str = "") -> str:
    """Wybiera formę liczby mnogiej właściwą dla języka wyniku.

    Formy podaje się po polsku (``1 plik``, ``2 pliki``, ``5 plików``); każda
    jedzie osobno przez :func:`tr`, a wybór robi reguła języka docelowego —
    angielski ma tylko dwie formy, więc dostaje pierwszą i drugą.
    """
    forms = [tr(one), tr(few), tr(many or few)]
    return forms[_form_index(number)]


def _form_index(number: int) -> int:
    if _language == "pl":
        return _polish_form(number)
    return 0 if abs(number) == 1 else 1


def _polish_form(number: int) -> int:
    number = abs(number)
    if number == 1:
        return 0
    rest = number % 10
    if 2 <= rest <= 4 and not 12 <= number % 100 <= 14:
        return 1
    return 2


def catalog() -> dict[str, str]:
    """Kopia bieżącego katalogu — do testów i podglądu."""
    return dict(_catalog)
