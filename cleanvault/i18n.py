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

#: kody i nazwy własne języków, w kolejności wyświetlania w ustawieniach — te same
#: języki i ta sama kolejność co w Sigelith Desktop i na sigelith.org
LANGUAGES: dict[str, str] = {
    "pl": "Polski",
    "en": "English",
    "de": "Deutsch",
    "es": "Español",
    "fr": "Français",
    "ru": "Русский",
    "tr": "Türkçe",
    "ja": "日本語",
    "ko": "한국어",
    "zh": "简体中文",
    "ar": "العربية",
}

#: języki pisane od prawej do lewej — okno dostaje układ od prawej (``ui/qtlang.py``)
RTL = frozenset({"ar"})

#: język, gdy żadnego języka systemu nie obsługujemy: angielski, bo wersja ze Sklepu
#: trafia też do ludzi, którzy polskiego nie znają (tak samo robi Sigelith Desktop)
FALLBACK_LANGUAGE = "en"

#: nazwy języków, które Windows podaje w ``locale.getlocale()`` („Polish_Poland”)
_WINDOWS_NAMES = {
    "polish": "pl", "english": "en", "german": "de", "spanish": "es", "french": "fr",
    "russian": "ru", "turkish": "tr", "japanese": "ja", "korean": "ko", "chinese": "zh",
    "arabic": "ar",
}

_language = SOURCE_LANGUAGE
_catalog: dict[str, str] = {}


def _bare(value: str) -> str:
    """``pl_PL.UTF-8`` / ``zh-Hans-CN`` → ``pl`` / ``zh``."""
    return value.replace("_", "-").split(".")[0].split("-")[0].strip().lower()


def system_language() -> str:
    """Język interfejsu systemu sprowadzony do obsługiwanego kodu; angielski, gdy żadnego nie znamy.

    Zmienne środowiskowe mają pierwszeństwo przed ustawieniem systemowym, bo
    tak działa reszta narzędzi wiersza poleceń i tak testuje się tę funkcję.
    Na Windows liczy się język INTERFEJSU, a nie format regionalny: ``locale``
    przy polskim interfejsie i niemieckim formacie dat zwraca ``de`` — program
    mówiłby po niemiecku do kogoś, kto ma Windows po polsku.
    """
    for name in ("TVB_LANG", "LANGUAGE", "LC_ALL", "LANG"):
        value = os.environ.get(name)
        if value and _bare(value) in LANGUAGES:
            return _bare(value)
    for candidate in _system_languages():
        if candidate in LANGUAGES:
            return candidate
    return FALLBACK_LANGUAGE


def _system_languages() -> list[str]:
    """Języki interfejsu systemu w kolejności preferencji, jako gołe kody."""
    codes = [_bare(name) for name in _windows_ui_languages()]
    try:
        system = _locale.getlocale()[0] or ""
    except ValueError:  # pragma: no cover - zepsute ustawienia regionalne
        system = ""
    codes.append(_WINDOWS_NAMES.get(system.split("_")[0].lower(), _bare(system)))
    return [code for code in codes if code]


def _windows_ui_languages() -> list[str]:
    """``GetUserPreferredUILanguages`` — lista języków interfejsu Windows (``pl-PL``, ``en-US``…)."""
    try:
        import ctypes
        from ctypes import wintypes

        mui_language_name = 0x8
        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        count, size = wintypes.ULONG(), wintypes.ULONG()
        if not kernel32.GetUserPreferredUILanguages(mui_language_name, ctypes.byref(count), None,
                                                    ctypes.byref(size)):
            return []
        buffer = ctypes.create_unicode_buffer(size.value)
        if not kernel32.GetUserPreferredUILanguages(mui_language_name, ctypes.byref(count), buffer,
                                                    ctypes.byref(size)):
            return []
        raw = buffer[:size.value]
    except (AttributeError, OSError, ValueError):  # poza Windows albo stary system
        return []
    return [part for part in raw.split("\x00") if part]


def set_language(code: str | None) -> str:
    """Ustawia język; ``auto``/pusty oznacza język systemu. Zwraca kod użyty."""
    global _language, _catalog
    wanted = (code or "auto").lower()
    if wanted in ("", "auto", "system"):
        wanted = system_language()
    if wanted not in LANGUAGES:
        # np. ustawienie z nowszej wersji z językiem, którego ta jeszcze nie zna
        fallback = system_language()
        log.warning("Nieznany język %s — biorę język systemu (%s)", code, fallback)
        wanted = fallback
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
    jedzie osobno przez :func:`tr`, a wybór robi reguła języka docelowego
    (:func:`_form_index`) — np. angielski ma tylko dwie formy, więc dostaje
    pierwszą i drugą.
    """
    forms = [tr(one), tr(few), tr(many or few)]
    return forms[_form_index(number)]


def _form_index(number: int) -> int:
    """Która z trzech form pasuje do liczby w bieżącym języku.

    Reguły jak w katalogach Sigelith Desktop (nagłówki ``Plural-Forms``), sprowadzone
    do trzech miejsc: japoński, koreański i chiński nie odmieniają rzeczownika po
    liczebniku, francuski ma liczbę pojedynczą także dla zera, rosyjski ma trzy formy
    jak polski, ale liczone inaczej (21 → „one”), a z sześciu kategorii arabskich
    zostają trzy: 1 — pojedyncza, 2–10 — mnoga, reszta — forma po liczebnikach 11–99.
    """
    n = abs(number)
    if _language == "pl":
        return _polish_form(n)
    if _language == "ru":
        if n % 10 == 1 and n % 100 != 11:
            return 0
        if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
            return 1
        return 2
    if _language in ("ja", "ko", "zh"):
        return 0
    if _language == "fr":
        return 0 if n <= 1 else 1
    if _language == "ar":
        if n == 1:
            return 0
        return 1 if n == 2 or 3 <= n % 100 <= 10 else 2
    return 0 if n == 1 else 1


def is_rtl(code: str | None = None) -> bool:
    """Czy język (domyślnie bieżący) pisze się od prawej do lewej."""
    return (code or _language) in RTL


def isolate(text: str) -> str:
    """Wstawka pisana od lewej (rozmiar, @beat) w tekście od prawej do lewej.

    Po arabsku „4.0 KB” obok tekstu arabskiego czyta się jako „KB 4.0”, a „@921”
    jako „921@” — znaki LRI … PDI zamykają wstawkę w osobnym akapicie od lewej.
    W pozostałych językach tekst wraca bez zmian.
    """
    return f"\u2066{text}\u2069" if is_rtl() else text


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
