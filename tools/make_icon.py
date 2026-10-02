"""Generator ikony aplikacji.

Rysuje ikonę proceduralnie i zapisuje ``assets/icon.png`` oraz ``assets/icon.ico``.
Dzięki temu ikona jest odtwarzalna i nie trzeba trzymać w repozytorium binariów,
których nikt nie umie już odtworzyć.

Uruchomienie::

    .venv\\Scripts\\python.exe tools\\make_icon.py
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

from PySide6.QtCore import QBuffer, QByteArray, QPointF, QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QImage, QPainter, QPainterPath
from PySide6.QtWidgets import QApplication

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
#: Kafelek jak w Sigelith Desktop: akcent marki (ten sam co motyw programu, certyfikat
#: i strona) i biały znak — obie aplikacje mają wyglądać jak jedna rodzina.
ACCENT = QColor("#ff5c39")
GLYPH = QColor("#ffffff")

#: Rozmiary umieszczane w pliku .ico — Windows dobiera właściwy zależnie od widoku.
ICO_SIZES = (16, 24, 32, 48, 64, 128, 256)


def render(size: int) -> QImage:
    image = QImage(size, size, QImage.Format.Format_ARGB32)
    image.fill(Qt.GlobalColor.transparent)

    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    s = size / 256.0  # wszystkie wymiary liczone dla kanwy 256 px

    # Tło: kafelek w kolorze marki w proporcjach kafelka Sigelith Desktop
    # (kwadrat 32..992 z 1024, promień rogów 204 — tu w jednostkach 256).
    painter.setBrush(QBrush(ACCENT))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(QRectF(8 * s, 8 * s, 240 * s, 240 * s), 51 * s, 51 * s)

    # Tarcza — symbol ochrony danych.
    shield = QPainterPath()
    shield.moveTo(128 * s, 46 * s)
    shield.lineTo(206 * s, 78 * s)
    shield.lineTo(206 * s, 132 * s)
    shield.cubicTo(206 * s, 176 * s, 174 * s, 202 * s, 128 * s, 216 * s)
    shield.cubicTo(82 * s, 202 * s, 50 * s, 176 * s, 50 * s, 132 * s)
    shield.lineTo(50 * s, 78 * s)
    shield.closeSubpath()

    painter.setBrush(QBrush(GLYPH))
    painter.drawPath(shield)

    # Dziurka od klucza w kolorze tła. Celowo NIE wycinamy jej trybem Clear —
    # przezroczysty otwór prześwitywałby paskiem zadań i tracił czytelność.
    keyhole = QPainterPath()
    radius = 23 * s
    keyhole.addEllipse(QPointF(128 * s, 118 * s), radius, radius)
    stem = QPainterPath()
    stem.moveTo(118 * s, 130 * s)
    stem.lineTo(138 * s, 130 * s)
    stem.lineTo(133 * s, 174 * s)
    stem.lineTo(123 * s, 174 * s)
    stem.closeSubpath()
    painter.fillPath(keyhole.united(stem), QBrush(ACCENT))

    painter.end()
    return image


def png_bytes(image: QImage) -> bytes:
    # QByteArray musi żyć dłużej niż QBuffer — przekazany jako obiekt tymczasowy
    # zostaje zwolniony przez Pythona i Qt sięga po zwolnioną pamięć
    # (awaria 0xC0000409 zamiast czytelnego wyjątku).
    data = QByteArray()
    buffer = QBuffer(data)
    buffer.open(QBuffer.OpenModeFlag.WriteOnly)
    image.save(buffer, "PNG")
    buffer.close()
    return bytes(data)


def write_ico(path: Path, images: list[QImage]) -> None:
    """Składa plik .ico z obrazów PNG (format obsługiwany od Windows Vista)."""
    blobs = [png_bytes(img) for img in images]
    offset = 6 + 16 * len(blobs)
    header = struct.pack("<HHH", 0, 1, len(blobs))
    entries = b""
    for image, blob in zip(images, blobs, strict=True):
        dimension = 0 if image.width() >= 256 else image.width()
        entries += struct.pack(
            "<BBBBHHII", dimension, dimension, 0, 0, 1, 32, len(blob), offset
        )
        offset += len(blob)
    path.write_bytes(header + entries + b"".join(blobs))


def main() -> int:
    app = QApplication.instance() or QApplication(sys.argv)  # noqa: F841 - QPainter wymaga QApplication
    ASSETS.mkdir(parents=True, exist_ok=True)

    render(256).save(str(ASSETS / "icon.png"), "PNG")
    write_ico(ASSETS / "icon.ico", [render(size) for size in ICO_SIZES])

    print(f"Zapisano {ASSETS / 'icon.png'}")
    print(f"Zapisano {ASSETS / 'icon.ico'} ({len(ICO_SIZES)} rozmiarów)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
