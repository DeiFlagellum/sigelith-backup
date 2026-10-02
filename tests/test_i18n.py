"""Testy warstwy tłumaczeń.

Sedno: interfejs ma być w całości przetłumaczalny, a katalog — zgodny z kodem.
Najgorszy możliwy błąd to angielskie okno z polskim zdaniem w środku, więc
większość testów porównuje **zbiór tekstów w kodzie** ze **zbiorem kluczy
katalogu** i pilnuje, by nowy napis nie wśliznął się poza ``tr()``.
"""

from __future__ import annotations

import ast
import importlib
import os
import re
from pathlib import Path

import pytest

from cleanvault import i18n
from cleanvault.locale.en import TEXTS

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ROOT / "app.py",
    # katalogi tłumaczeń to same teksty źródłowe, ``theme.py`` to arkusz stylów
    # z polskimi komentarzami, a notatka ratunkowa (``rescue.py``) i certyfikat PDF
    # dowodu czasu (``proof_pdf.py``) są z założenia dwujęzyczne niezależnie od języka
    # interfejsu — czyta je ktoś bez programu
    *[
        p
        for p in sorted((ROOT / "cleanvault").rglob("*.py"))
        if p.parent.name != "locale" and p.name not in {"theme.py", "rescue.py", "proof_pdf.py"}
    ],
]
FIELD = re.compile(r"\{(\w+)\}")
DIRECTIVE = re.compile(r"%[A-Za-z]")
POLISH = set("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ")

#: Teksty, które celowo zostają po polsku i nie są tłumaczone.
ALLOWED_RAW = {
    # klucze porównywane w kodzie, nie napisy dla użytkownika
    "brak w kopii",
    # wzorzec wykluczeń: nazwa katalogu Windows, ta sama w każdej wersji językowej
    "System Volume Information/*",
    # nazwa usługi w Menedżerze poświadczeń — zmiana odcięłaby zapisane hasła
    "TVS CleanVault",
    # domyślna nazwa szablonu w danych; ekran podaje własną, tłumaczoną
    "Nowy szablon",
    # etykieta pliku zapasowego stanu w dzienniku
    "kopia zapasowa stanu",
    # klasy znaków w wyrażeniach regularnych oceniających hasło
    "[a-ząćęłńóśźż]",
    "[A-ZĄĆĘŁŃÓŚŹŻ]",
    # fragment HTML podpowiedzi
    '<img src="',
    # nazwa pola hasła w słowniku popularnych haseł
    "hasło",
    # błąd programisty przy złym wywołaniu funkcji, nie komunikat dla użytkownika
    "decimals musi być >= 0",
}


def _literal(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _texts_in_code() -> dict[str, list[str]]:
    """Teksty przekazane do ``tr``/``mark``/``plural`` wraz z miejscem użycia."""
    found: dict[str, list[str]] = {}
    for path in SOURCES:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
                continue
            if node.func.id in {"tr", "mark"}:
                args = node.args[:1]
            elif node.func.id == "plural":
                args = node.args[1:]
            else:
                continue
            for arg in args:
                text = _literal(arg)
                if text:
                    found.setdefault(text, []).append(f"{path.name}:{node.lineno}")
    return found


@pytest.fixture(scope="module")
def code_texts() -> dict[str, list[str]]:
    texts = _texts_in_code()
    assert len(texts) > 300, "ekstrakcja tekstów przestała działać"
    return texts


def test_every_text_has_an_english_translation(code_texts):
    missing = sorted(set(code_texts) - set(TEXTS))
    assert not missing, "brak tłumaczeń: " + "; ".join(
        f"{text[:40]!r} ({code_texts[text][0]})" for text in missing[:10]
    )


def test_catalog_has_no_stale_entries(code_texts):
    stale = sorted(set(TEXTS) - set(code_texts))
    assert not stale, f"tłumaczenia bez odpowiednika w kodzie: {[t[:40] for t in stale[:10]]}"


def test_placeholders_survive_translation():
    """Pole ``{count}`` zgubione w tłumaczeniu to wyjątek przy formatowaniu."""
    mismatched = [
        source for source, target in TEXTS.items()
        if set(FIELD.findall(source)) != set(FIELD.findall(target))
    ]
    assert not mismatched, [text[:50] for text in mismatched]


def test_date_formats_keep_their_directives():
    mismatched = [
        source for source, target in TEXTS.items()
        if "%" in source and set(DIRECTIVE.findall(source)) != set(DIRECTIVE.findall(target))
    ]
    assert not mismatched, mismatched


#: katalogi wszystkich języków poza źródłowym — te same języki co Sigelith Desktop i strona
CATALOG_CODES = [code for code in i18n.LANGUAGES if code != i18n.SOURCE_LANGUAGE]
#: litery, które występują tylko po polsku — w obcym katalogu znaczą nieprzetłumaczony tekst
POLISH_ONLY = set("ąćęłńśźżĄĆĘŁŃŚŹŻ")


def _texts_of(code: str) -> dict[str, str]:
    return importlib.import_module(f"cleanvault.locale.{code}").TEXTS


def test_languages_match_sigelith_desktop_and_the_website():
    assert list(i18n.LANGUAGES) == ["pl", "en", "de", "es", "fr", "ru", "tr", "ja", "ko", "zh", "ar"]


@pytest.mark.parametrize("code", CATALOG_CODES)
def test_every_language_has_every_text(code, code_texts):
    texts = _texts_of(code)
    missing = sorted(set(code_texts) - set(texts))
    stale = sorted(set(texts) - set(code_texts))
    assert not missing, f"[{code}] brak tłumaczeń: {[t[:40] for t in missing[:10]]}"
    assert not stale, f"[{code}] tłumaczenia bez odpowiednika w kodzie: {[t[:40] for t in stale[:10]]}"


@pytest.mark.parametrize("code", CATALOG_CODES)
def test_placeholders_and_dates_survive_in_every_language(code):
    texts = _texts_of(code)
    fields = [s for s, t in texts.items() if set(FIELD.findall(s)) != set(FIELD.findall(t))]
    dates = [s for s, t in texts.items() if "%" in s and set(DIRECTIVE.findall(s)) != set(DIRECTIVE.findall(t))]
    assert not fields, f"[{code}] zgubione pola: {[t[:50] for t in fields[:10]]}"
    assert not dates, f"[{code}] zepsute formaty dat: {dates}"


@pytest.mark.parametrize("code", [code for code in CATALOG_CODES if code != "en"])
def test_no_polish_left_in_foreign_catalogs(code):
    left = [
        source for source, target in _texts_of(code).items()
        if set(target) & POLISH_ONLY and not set(TEXTS[source]) & POLISH_ONLY
    ]
    assert not left, f"[{code}] polskie teksty w katalogu: {[t[:40] for t in left[:10]]}"


@pytest.mark.parametrize(
    ("code", "numbers", "forms"),
    [
        ("de", (0, 1, 2, 21), (1, 0, 1, 1)),
        ("fr", (0, 1, 2, 21), (0, 0, 1, 1)),
        ("ru", (1, 2, 5, 11, 12, 21, 22, 25, 112), (0, 1, 2, 2, 2, 0, 1, 2, 2)),
        ("ar", (0, 1, 2, 3, 10, 11, 99, 100, 103), (2, 0, 1, 1, 1, 2, 2, 2, 1)),
        ("ja", (0, 1, 2, 5), (0, 0, 0, 0)),
        ("zh", (1, 7), (0, 0)),
    ],
)
def test_plural_rules_follow_each_language(code, numbers, forms):
    try:
        i18n.set_language(code)
        assert tuple(i18n._form_index(n) for n in numbers) == forms
    finally:
        i18n.set_language("pl")


def test_arabic_turns_the_window_right_to_left():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication

    from cleanvault.ui import qtlang

    app = QApplication.instance() or QApplication([])
    try:
        assert i18n.is_rtl("ar") and not i18n.is_rtl("pl")
        assert qtlang.apply("ar")
        assert app.layoutDirection() == Qt.LayoutDirection.RightToLeft
        assert qtlang.apply("zh")  # plik Qt nazywa się qtbase_zh_CN
        assert app.layoutDirection() == Qt.LayoutDirection.LeftToRight
    finally:
        qtlang.apply("pl")


def test_translation_switches_with_language():
    try:
        i18n.set_language("pl")
        assert i18n.tr("Uruchom kopię") == "Uruchom kopię"
        i18n.set_language("en")
        assert i18n.tr("Uruchom kopię") == "Run backup"
        # tekst spoza katalogu wraca bez zmian, zamiast znikać
        assert i18n.tr("czegoś takiego nie ma") == "czegoś takiego nie ma"
    finally:
        i18n.set_language("pl")


def test_polish_plural_follows_grammar():
    i18n.set_language("pl")
    forms = ("plik", "pliki", "plików")
    assert [i18n.plural(n, *forms) for n in (1, 2, 5, 22, 25, 112)] == [
        "plik", "pliki", "plików", "pliki", "plików", "plików",
    ]


def test_english_plural_uses_two_forms():
    try:
        i18n.set_language("en")
        forms = ("plik", "pliki", "plików")
        assert i18n.plural(1, *forms) == "file"
        assert i18n.plural(2, *forms) == "files"
        assert i18n.plural(112, *forms) == "files"
    finally:
        i18n.set_language("pl")


def test_unknown_language_falls_back_to_the_system_language(monkeypatch):
    """Ustawienie z językiem, którego ta wersja nie zna (np. z nowszej), nie psuje programu."""
    monkeypatch.setenv("TVB_LANG", "pl_PL")
    try:
        assert i18n.set_language("kl") == "pl"
        assert i18n.tr("Uruchom kopię") == "Uruchom kopię"
    finally:
        i18n.set_language("pl")


def test_system_language_reads_the_environment(monkeypatch):
    monkeypatch.setenv("TVB_LANG", "en_US.UTF-8")
    assert i18n.system_language() == "en"
    monkeypatch.setenv("TVB_LANG", "pl_PL")
    assert i18n.system_language() == "pl"
    monkeypatch.setenv("TVB_LANG", "de_DE")
    assert i18n.system_language() == "de"
    monkeypatch.setenv("TVB_LANG", "zh-Hans-CN")
    assert i18n.system_language() == "zh"


def test_system_language_follows_the_windows_interface_and_defaults_to_english(monkeypatch):
    """Liczy się język interfejsu Windows; języka spoza listy nie zastępujemy polskim."""
    for name in ("TVB_LANG", "LANGUAGE", "LC_ALL", "LANG"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(i18n, "_system_languages", lambda: ["it", "ko", "pl"])
    assert i18n.system_language() == "ko"
    monkeypatch.setattr(i18n, "_system_languages", lambda: ["it", "nl"])
    assert i18n.system_language() == "en"


def _polish_outside_tr(source: str, name: str = "kod.py") -> list[str]:
    """Polskie napisy, które nie przechodzą przez warstwę tłumaczeń."""
    tree = ast.parse(source)
    skip = _docstrings(tree) | _protected(tree)
    offenders: list[str] = []
    for node in ast.walk(tree):
        key = (getattr(node, "lineno", 0), getattr(node, "col_offset", 0))
        if key in skip:
            continue
        text = _literal(node)
        if isinstance(node, ast.JoinedStr):
            text = "".join(v.value for v in node.values if isinstance(v, ast.Constant))
        if not text or text in ALLOWED_RAW or len(text) < 4:
            continue
        if set(text) & POLISH and any(c.isalpha() for c in text):
            offenders.append(f"{name}:{node.lineno}: {text[:60]!r}")
    return offenders


def test_no_polish_text_escapes_the_translation_layer():
    """Nowy napis dla użytkownika musi przejść przez ``tr`` — inaczej zostanie po polsku."""
    offenders: list[str] = []
    for path in SOURCES:
        offenders += _polish_outside_tr(path.read_text(encoding="utf-8"), path.name)
    assert not offenders, "teksty poza tr(): " + "; ".join(offenders[:10])


def test_guard_catches_a_forgotten_message_box():
    """Sam strażnik też bywa zepsuty — sprawdzamy, że łapie typowe przeoczenie."""
    forgotten = 'QMessageBox.critical(self, "Błąd zapisu", "Nie udało się zapisać pliku.")'
    assert len(_polish_outside_tr(forgotten)) == 2

    translated = 'QMessageBox.critical(self, tr("Błąd zapisu"), tr("Nie udało się zapisać pliku."))'
    assert _polish_outside_tr(translated) == []

    logged = 'logging.getLogger("x").critical("Nieobsłużony wyjątek")'
    assert _polish_outside_tr(logged) == []


def _docstrings(tree: ast.AST) -> set[tuple[int, int]]:
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            first = node.body[0] if node.body else None
            if isinstance(first, ast.Expr) and isinstance(getattr(first.value, "value", None), str):
                out.add((first.value.lineno, first.value.col_offset))
    return out


def _protected(tree: ast.AST) -> set[tuple[int, int]]:
    """Miejsca, w których polski tekst jest w porządku: tłumaczenia i dziennik."""
    out = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.id if isinstance(func, ast.Name) else getattr(func, "attr", "")
        owner = func.value.id if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) else ""
        # Dziennik jest dla diagnostyki, nie dla użytkownika. Sama nazwa metody nie
        # wystarczy: ``QMessageBox.critical`` też nazywa się „critical”, a jego treść
        # widzi użytkownik — dlatego patrzymy, do czego metoda należy.
        logging_call = (
            name in {"debug", "info", "warning", "error", "critical", "exception"}
            and "log" in ast.unparse(func.value).lower()
        )
        if (
            name in {"tr", "plural", "mark", "setStyleSheet"}
            or owner in {"log", "logger"}
            or logging_call
        ):
            for child in ast.walk(node):
                if isinstance(child, (ast.Constant, ast.JoinedStr)):
                    out.add((child.lineno, child.col_offset))
    return out
