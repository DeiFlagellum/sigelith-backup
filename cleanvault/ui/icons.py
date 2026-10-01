"""Ikony interfejsu — jeden zestaw dla całego programu.

Zestaw: [Bootstrap Icons](https://icons.getbootstrap.com/) 1.13.1 na licencji
MIT; treść licencji leży obok plików w ``assets/icons/LICENSE``. Nową ikonę
dokłada się z tej samej wersji zestawu, żeby kreska i proporcje były wszędzie
takie same: ``https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/icons/<nazwa>.svg``. Wcześniej program
używał emoji, których wygląd zależał od czcionki systemowej i które nie dają
się dopasować kolorem do motywu.

Ikony są jednobarwne (``fill="currentColor"``), więc kolor podstawiamy przed
narysowaniem. Dzięki temu ten sam plik obsługuje motyw ciemny i jasny.
"""

from __future__ import annotations

import base64
import functools
from typing import NamedTuple

from PySide6.QtCore import QBuffer, QByteArray, QIODevice, QRectF, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QWidget

from ..log import get_logger
from ..paths import resource_path

log = get_logger("ui.icons")

#: Nazwa właściwości, pod którą widget pamięta swoją ikonę. Dzięki niej po
#: zmianie motywu wystarczy przejść po widgetach i przemalować ikony.
ICON_PROPERTY = "cleanvaultIcon"

DEFAULT_SIZE = 18
#: Kolor używany, zanim motyw zdąży się zgłosić (np. w testach bez okna).
_color = "#e7e9ee"


def set_color(color: str) -> None:
    """Ustawia kolor, którym rysowane są kolejne ikony."""
    global _color
    _color = color


@functools.lru_cache(maxsize=128)
def _source(name: str) -> bytes | None:
    path = resource_path("assets", "icons", f"{name}.svg")
    try:
        return path.read_bytes()
    except OSError:
        log.warning("Brak ikony %s (%s)", name, path)
        return None


@functools.lru_cache(maxsize=512)
def pixmap(name: str, color: str, size: int) -> QPixmap:
    source = _source(name) or _source("question-circle")
    canvas = QPixmap(size, size)
    canvas.fill(Qt.GlobalColor.transparent)
    if source is None:
        return canvas
    renderer = QSvgRenderer(QByteArray(source.replace(b"currentColor", color.encode("ascii"))))
    painter = QPainter(canvas)
    try:
        renderer.render(painter, QRectF(0, 0, size, size))
    finally:
        painter.end()
    return canvas


class IconColors(NamedTuple):
    """Kolory ikony w kolejnych stanach przycisku."""

    normal: str
    #: przycisk przełączany po wciśnięciu (np. wybrana pozycja menu)
    checked: str | None = None
    #: kursor nad przyciskiem, gdy zmienia się wtedy także tło
    active: str | None = None


def icon(name: str, colors: IconColors | str | None = None, size: int = DEFAULT_SIZE) -> QIcon:
    """Ikona gotowa dla widgetu, z wariantami na stany, w których zmienia się tło."""
    if colors is None:
        colors = IconColors(_color)
    elif isinstance(colors, str):
        colors = IconColors(colors)
    result = QIcon(pixmap(name, colors.normal, size))
    if colors.checked:
        checked = pixmap(name, colors.checked, size)
        result.addPixmap(checked, QIcon.Mode.Normal, QIcon.State.On)
        result.addPixmap(checked, QIcon.Mode.Active, QIcon.State.On)
    if colors.active:
        result.addPixmap(pixmap(name, colors.active, size), QIcon.Mode.Active, QIcon.State.Off)
    return result


def set_icon(widget, name: str, size: int = DEFAULT_SIZE) -> None:
    """Nadaje widgetowi ikonę i zapamiętuje jej nazwę do późniejszego przemalowania."""
    if not name:
        return
    widget.setProperty(ICON_PROPERTY, name)
    widget.setIcon(icon(name, size=size))


def color_for(object_name: str, palette) -> IconColors:
    """Kolory ikony dobrane do tła danego przycisku.

    Ikona przycisku głównego leży na tle akcentu; w pozycji menu dopiero po
    zaznaczeniu, a na przycisku niebezpiecznym dopiero pod kursorem — w każdym
    z tych stanów musi zmienić kolor razem z tekstem, inaczej znika w tle.
    """
    if object_name == "Primary":
        return IconColors(palette.accent_text)
    if object_name == "Danger":
        return IconColors(palette.danger, active="#ffffff")
    if object_name == "NavButton":
        return IconColors(palette.muted, checked=palette.accent_text, active=palette.text)
    return IconColors(palette.text)


def repaint_all(root, palette, size: int = DEFAULT_SIZE) -> int:
    """Przemalowuje ikony wszystkich widgetów pod ``root`` — po zmianie motywu."""
    set_color(palette.text)
    painted = 0
    for widget in root.findChildren(QWidget):
        name = widget.property(ICON_PROPERTY)
        if not name or not hasattr(widget, "setIcon"):
            continue
        widget.setIcon(icon(str(name), color_for(widget.objectName(), palette), size))
        painted += 1
    return painted


@functools.lru_cache(maxsize=128)
def data_uri(name: str, color: str, size: int) -> str:
    """Ikona jako adres ``data:`` — do osadzenia w tekście z formatowaniem.

    Podpowiedzi są etykietami z zawijanym tekstem; wstawienie obok nich osobnego
    widgetu z ikoną psułoby zawijanie i styl, więc ikona jedzie w treści.
    """
    image = pixmap(name, color, size).toImage()
    buffer = QBuffer()
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    image.save(buffer, "PNG")
    return "data:image/png;base64," + base64.b64encode(bytes(buffer.data())).decode("ascii")


def current_color() -> str:
    return _color
