"""Testy jednolitego zestawu ikon.

Program używał emoji, których kształt zależał od czcionki systemowej i których
nie da się dopasować kolorem do motywu. Zestąpił je zestaw Bootstrap Icons (MIT)
rysowany z plików SVG. Te testy pilnują trzech rzeczy, które łatwo zepsuć:

* każda nazwa użyta w kodzie ma swój plik — literówka nie objawia się wtedy
  dopiero na ekranie użytkownika jako znak zapytania,
* ikona faktycznie się rysuje i zmienia kolor razem z motywem,
* emoji nie wracają do kodu interfejsu.
"""

from __future__ import annotations

import os
import re
import unicodedata
from pathlib import Path

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

pytest.importorskip("PySide6")

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QPushButton

from cleanvault.ui import icons
from cleanvault.ui.main_window import MainWindow
from cleanvault.ui.theme import palette_for
from cleanvault.ui.widgets import Hint

ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / "assets" / "icons"
UI_DIR = ROOT / "cleanvault" / "ui"

#: nazwy ikon wypisane w kodzie: icon="...", icons.icon("..."), set_icon(w, "...")
USES = re.compile(r'''(?:icon\s*=\s*|icons\.icon\(\s*|set_icon\([^,]+,\s*)"([a-z0-9-]+)"''')


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


def _names_used() -> set[str]:
    """Nazwy ikon z kodu: podane wprost w wywołaniach oraz spis pozycji menu."""
    found = {name for name, _label, _tip in MainWindow.PAGES}
    for path in UI_DIR.rglob("*.py"):
        found.update(USES.findall(path.read_text(encoding="utf-8")))
    return found


def test_icon_set_ships_with_its_licence():
    licence = (ICON_DIR / "LICENSE").read_text(encoding="utf-8")
    assert "MIT" in licence
    assert "The Bootstrap Authors" in licence


def test_every_name_used_in_code_has_a_file():
    used = _names_used()
    assert len(used) > 15, "test przestał znajdować nazwy ikon w kodzie"
    missing = sorted(name for name in used if not (ICON_DIR / f"{name}.svg").exists())
    assert not missing, f"brak plików SVG: {missing}"


def test_icons_are_single_colour_so_theme_can_repaint_them():
    for path in sorted(ICON_DIR.glob("*.svg")):
        assert b"currentColor" in path.read_bytes(), path.name


def test_pixmap_uses_requested_colour(qapp):
    red = icons.pixmap("gear", "#ff0000", 32).toImage()
    blue = icons.pixmap("gear", "#0000ff", 32).toImage()
    colours = {red.pixelColor(x, y).name() for x in range(32) for y in range(32)
               if red.pixelColor(x, y).alpha() > 200}
    assert "#ff0000" in colours
    assert red.constBits() != blue.constBits()


def test_unknown_name_falls_back_instead_of_crashing(qapp):
    fallback = icons.pixmap("nie-ma-takiej-ikony", "#ffffff", 16)
    assert not fallback.isNull()


def test_button_icons_follow_the_colour_of_their_background():
    palette = palette_for("dark")
    assert icons.color_for("Primary", palette).normal == palette.accent_text
    danger = icons.color_for("Danger", palette)
    assert (danger.normal, danger.active) == (palette.danger, "#ffffff")
    nav = icons.color_for("NavButton", palette)
    assert (nav.normal, nav.checked, nav.active) == (palette.muted, palette.accent_text, palette.text)
    assert icons.color_for("", palette) == icons.IconColors(palette.text)


def test_checked_navigation_icon_differs_from_the_resting_one(qapp):
    palette = palette_for("dark")
    built = icons.icon("gear", icons.color_for("NavButton", palette), 24)
    resting = built.pixmap(24, 24, QIcon.Mode.Normal, QIcon.State.Off).toImage()
    chosen = built.pixmap(24, 24, QIcon.Mode.Normal, QIcon.State.On).toImage()
    assert resting != chosen


def test_repaint_all_follows_the_theme(qapp):
    parent = QPushButton()
    child = QPushButton(parent)
    icons.set_icon(child, "gear")
    light = palette_for("light")
    assert icons.repaint_all(parent, light) == 1
    assert icons.current_color() == light.text
    dark = palette_for("dark")
    icons.repaint_all(parent, dark)
    assert icons.current_color() == dark.text


def test_hint_embeds_its_icon_in_the_text(qapp):
    hint = Hint("Kopia nie usuwa plików ze źródła.", icon="shield-check")
    assert "<img src=\"data:image/png;base64," in hint.text()
    assert "Kopia nie usuwa" in hint.text()
    icons.set_color("#123456")
    before = hint.text()
    icons.set_color("#abcdef")
    hint.refresh_icon()
    assert hint.text() != before


def test_no_emoji_left_in_the_interface_code():
    symbols = {0x2713, 0x2714, 0x25b6, 0x267b, 0x2699, 0x23f8}
    offenders = []
    for path in sorted(UI_DIR.rglob("*.py")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if any((ord(c) > 0x2000 and unicodedata.category(c) in {"So", "Sk"}) or ord(c) in symbols
                   for c in line):
                offenders.append(f"{path.name}:{number}")
    assert not offenders, f"emoji zamiast ikon: {offenders}"
