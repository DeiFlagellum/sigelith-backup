"""Komponenty interfejsu wielokrotnego użytku.

Każdy element niosący decyzję użytkownika ma tu przypisany tekst pomocniczy
i podpowiedź (tooltip). To celowe: w wersji 1.x okno składało się z surowych
kontrolek bez jednego zdania wyjaśnienia, przez co opcje takie jak „tryb
przywracania" nie znaczyły dla użytkownika nic konkretnego.
"""

from __future__ import annotations

import html
import re
from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import QRect, QSize, Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLayoutItem,
    QLineEdit,
    QListWidget,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ..i18n import tr
from . import icons

# --------------------------------------------------------------- typografia


def page_title(text: str, subtitle: str = "") -> QWidget:
    box = QWidget()
    layout = QVBoxLayout(box)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(3)
    title = QLabel(text)
    title.setObjectName("PageTitle")
    layout.addWidget(title)
    if subtitle:
        sub = QLabel(subtitle)
        sub.setObjectName("PageSubtitle")
        sub.setWordWrap(True)
        layout.addWidget(sub)
    return box


def field_help(text: str) -> QLabel:
    label = QLabel(text)
    label.setObjectName("FieldHelp")
    label.setWordWrap(True)
    return label


class Hint(QLabel):
    """Pasek podpowiedzi — wyjaśnia *dlaczego*, a nie tylko *co*."""

    def __init__(self, text: str, icon: str = "info-circle") -> None:
        super().__init__()
        self.setObjectName("Hint")
        self.setWordWrap(True)
        self.setTextFormat(Qt.TextFormat.RichText)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self._icon_name = icon
        self._plain_text = text
        self.refresh_icon()

    def refresh_icon(self) -> None:
        """Składa treść z ikoną w bieżącym kolorze motywu."""
        source = icons.data_uri(self._icon_name, icons.current_color(), 14)
        self.setText(f'<img src="{source}">&nbsp;&nbsp;{html.escape(self._plain_text)}')


class Card(QFrame):
    """Sekcja z tytułem, opisem i własnym układem treści."""

    def __init__(self, title: str = "", subtitle: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Card")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(18, 16, 18, 16)
        outer.setSpacing(12)

        if title:
            header = QVBoxLayout()
            header.setSpacing(2)
            label = QLabel(title)
            label.setObjectName("CardTitle")
            header.addWidget(label)
            if subtitle:
                sub = QLabel(subtitle)
                sub.setObjectName("CardSubtitle")
                sub.setWordWrap(True)
                header.addWidget(sub)
            outer.addLayout(header)

        self.body = QVBoxLayout()
        self.body.setSpacing(10)
        outer.addLayout(self.body)

    def add(self, widget: QWidget) -> QWidget:
        self.body.addWidget(widget)
        return widget

    def add_layout(self, layout) -> None:
        self.body.addLayout(layout)


class StatTile(QFrame):
    """Kafelek z liczbą — używany w podsumowaniu planu kopii."""

    def __init__(self, label: str, value: str = "—", tooltip: str = "") -> None:
        super().__init__()
        self.setObjectName("Card")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 11, 14, 11)
        layout.setSpacing(1)
        self._value = QLabel(value)
        self._value.setObjectName("StatValue")
        self._label = QLabel(label)
        self._label.setObjectName("StatLabel")
        layout.addWidget(self._value)
        layout.addWidget(self._label)
        if tooltip:
            self.setToolTip(tooltip)

    def set_value(self, value: str) -> None:
        self._value.setText(value)


def checkbox(text: str, tooltip: str, checked: bool = False) -> QCheckBox:
    box = QCheckBox(text)
    box.setChecked(checked)
    box.setToolTip(tooltip)
    return box


# ------------------------------------------------------------------ ścieżki


class PathPicker(QWidget):
    """Pole wyboru katalogu z przyciskiem przeglądania i podglądem w Eksploratorze."""

    changed = Signal(str)

    def __init__(
        self,
        placeholder: str = "",
        button_text: str = "",
        dialog_title: str = "",
        tooltip: str = "",
    ) -> None:
        super().__init__()
        placeholder = placeholder or tr("Nie wybrano katalogu")
        button_text = button_text or tr("Wybierz…")
        dialog_title = dialog_title or tr("Wybierz katalog")
        self._dialog_title = dialog_title
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.edit = QLineEdit()
        self.edit.setPlaceholderText(placeholder)
        self.edit.setClearButtonEnabled(True)
        if tooltip:
            self.edit.setToolTip(tooltip)
        self.edit.textChanged.connect(self.changed.emit)

        self.browse_btn = QPushButton(button_text)
        self.browse_btn.setToolTip(tr("Otwórz okno wyboru katalogu"))
        self.browse_btn.clicked.connect(self._browse)

        layout.addWidget(self.edit, 1)
        layout.addWidget(self.browse_btn)

    def _browse(self) -> None:
        start = self.edit.text() or str(Path.home())
        chosen = QFileDialog.getExistingDirectory(self, self._dialog_title, start)
        if chosen:
            self.edit.setText(chosen)

    def path(self) -> str:
        return self.edit.text().strip()

    def set_path(self, value: str) -> None:
        self.edit.setText(value or "")


class SourceList(QListWidget):
    """Lista katalogów źródłowych z obsługą przeciągnij-i-upuść."""

    changed = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setAcceptDrops(True)
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.setMinimumHeight(104)
        self.setToolTip(
            tr("Katalogi objęte kopią.\n"
               "Możesz przeciągnąć foldery z Eksploratora Windows wprost na tę listę.")
        )

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        added = False
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path and Path(path).is_dir():
                added |= self.add_path(path)
        if added:
            event.acceptProposedAction()
            self.changed.emit()

    def add_path(self, path: str) -> bool:
        normalised = str(Path(path).resolve())
        if normalised in self.paths():
            return False
        self.addItem(normalised)
        self.changed.emit()
        return True

    def remove_selected(self) -> None:
        for item in self.selectedItems():
            self.takeItem(self.row(item))
        self.changed.emit()

    def paths(self) -> list[str]:
        return [self.item(i).text() for i in range(self.count())]

    def set_paths(self, values: list[str]) -> None:
        self.clear()
        for value in values:
            self.addItem(value)
        self.changed.emit()


# -------------------------------------------------------------------- hasło

_COMMON = {
    "haslo", "hasło", "password", "qwerty", "123456", "12345678", "admin",
    "zaq12wsx", "iloveyou", "letmein", "monkey", "dragon", "111111", "polska",
}


def estimate_strength(password: str) -> tuple[int, str, str]:
    """Zwraca ``(wynik 0-4, etykieta, nazwa roli koloru)``.

    Świadomie prosta heurystyka: długość, różnorodność znaków i kara za
    oczywiste wzorce. Nie zastępuje zxcvbn, ale uczciwie odróżnia
    „Lato2024" od hasła generowanego losowo.
    """
    if not password:
        return 0, "—", "Muted"

    lowered = password.lower()
    classes = sum(
        bool(pattern.search(password))
        for pattern in (
            re.compile(r"[a-ząćęłńóśźż]"),
            re.compile(r"[A-ZĄĆĘŁŃÓŚŹŻ]"),
            re.compile(r"\d"),
            re.compile(r"[^\w\s]"),
        )
    )
    score = 0
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1
    if classes >= 3:
        score += 1
    if classes == 4 and len(password) >= 12:
        score += 1

    if any(word in lowered for word in _COMMON):
        score = min(score, 1)
    if len(set(password)) <= max(2, len(password) // 4):
        score = min(score, 1)
    if re.fullmatch(r"\d+", password):
        score = min(score, 1)

    score = max(0, min(4, score))
    labels = [
        (tr("Bardzo słabe"), "Danger"),
        (tr("Słabe"), "Danger"),
        (tr("Przeciętne"), "Warning"),
        (tr("Dobre"), "Success"),
        (tr("Bardzo dobre"), "Success"),
    ]
    label, role = labels[score]
    return score, label, role


class PasswordField(QWidget):
    """Pole hasła z podglądem treści i oceną siły.

    Ocena siły ma znaczenie praktyczne: hasło jest **jedynym** sekretem
    chroniącym kopię. Przy AES-256-GCM i Argon2id to ono, a nie algorytm,
    jest najsłabszym ogniwem.
    """

    changed = Signal(str)

    def __init__(self, placeholder: str = "", show_strength: bool = True) -> None:
        super().__init__()
        placeholder = placeholder or tr("Hasło do kopii")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        row = QHBoxLayout()
        row.setSpacing(8)
        self.edit = QLineEdit()
        self.edit.setPlaceholderText(placeholder)
        self.edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.edit.textChanged.connect(self._on_changed)
        self.edit.setToolTip(
            tr("Hasło nie jest nigdzie zapisywane w postaci jawnej.\n"
               "Bez niego nie da się odzyskać danych — nie istnieje żadna furtka serwisowa.")
        )

        self.reveal_btn = QPushButton()
        icons.set_icon(self.reveal_btn, "eye")
        self.reveal_btn.setObjectName("Ghost")
        self.reveal_btn.setCheckable(True)
        self.reveal_btn.setFixedWidth(42)
        self.reveal_btn.setToolTip(tr("Pokaż / ukryj wpisane hasło"))
        self.reveal_btn.toggled.connect(self._toggle_reveal)

        row.addWidget(self.edit, 1)
        row.addWidget(self.reveal_btn)
        layout.addLayout(row)

        self._show_strength = show_strength
        if show_strength:
            meter_row = QHBoxLayout()
            meter_row.setSpacing(9)
            self.meter = QProgressBar()
            self.meter.setRange(0, 4)
            self.meter.setValue(0)
            self.meter.setTextVisible(False)
            self.meter.setFixedHeight(6)
            self.meter.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.strength_label = QLabel(tr("—"))
            self.strength_label.setObjectName("Muted")
            self.strength_label.setMinimumWidth(96)
            meter_row.addWidget(self.meter, 1)
            meter_row.addWidget(self.strength_label)
            layout.addLayout(meter_row)

    def _toggle_reveal(self, shown: bool) -> None:
        self.edit.setEchoMode(
            QLineEdit.EchoMode.Normal if shown else QLineEdit.EchoMode.Password
        )
        icons.set_icon(self.reveal_btn, "eye-slash" if shown else "eye")

    def _on_changed(self, text: str) -> None:
        if self._show_strength:
            score, label, role = estimate_strength(text)
            self.meter.setValue(score)
            self.strength_label.setText(label)
            self.strength_label.setObjectName(role)
            self.strength_label.style().unpolish(self.strength_label)
            self.strength_label.style().polish(self.strength_label)
        self.changed.emit(text)

    def password(self) -> str:
        return self.edit.text()

    def set_password(self, value: str) -> None:
        self.edit.setText(value)

    def clear(self) -> None:
        self.edit.clear()

    def set_enabled(self, enabled: bool) -> None:
        self.setEnabled(enabled)
        if not enabled:
            self.clear()


# ------------------------------------------------------------------ pomocnicze


class FlowLayout(QLayout):
    """Rząd przycisków, który zawija się do następnego wiersza, gdy brakuje szerokości.

    Na stronie przywracania jest osiem przycisków — po polsku to ok. 1450 px, więcej niż
    okno na laptopie (1920×1080 przy skali 150% to 1280 px). Zwykły QHBoxLayout chował
    wtedy „Przywróć pliki” za poziomym przewijaniem; tu przyciski przechodzą niżej.
    """

    def __init__(self, parent: QWidget | None = None, spacing: int = 10) -> None:
        super().__init__(parent)
        self._items: list[QLayoutItem] = []
        self._gap = spacing
        self.setContentsMargins(0, 0, 0, 0)

    def addItem(self, item: QLayoutItem) -> None:
        self._items.append(item)

    def count(self) -> int:
        return len(self._items)

    def itemAt(self, index: int) -> QLayoutItem | None:
        return self._items[index] if 0 <= index < len(self._items) else None

    def takeAt(self, index: int) -> QLayoutItem | None:
        return self._items.pop(index) if 0 <= index < len(self._items) else None

    def expandingDirections(self) -> Qt.Orientation:
        return Qt.Orientation(0)

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, width: int) -> int:
        return self._arrange(QRect(0, 0, width, 0), apply=False)

    def setGeometry(self, rect: QRect) -> None:
        super().setGeometry(rect)
        self._arrange(rect, apply=True)

    def sizeHint(self) -> QSize:
        return self.minimumSize()

    def minimumSize(self) -> QSize:
        size = QSize()
        for item in self._items:
            if not item.isEmpty():
                size = size.expandedTo(item.minimumSize())
        margins = self.contentsMargins()
        return size + QSize(margins.left() + margins.right(), margins.top() + margins.bottom())

    def _arrange(self, rect: QRect, apply: bool) -> int:
        margins = self.contentsMargins()
        area = rect.adjusted(margins.left(), margins.top(), -margins.right(), -margins.bottom())
        x, y, row = area.x(), area.y(), 0
        for item in self._items:
            if item.isEmpty():  # ukryty przycisk (np. „Dowody Sigelith…”) nie zajmuje miejsca
                continue
            hint = item.sizeHint()
            if x > area.x() and x + hint.width() > area.right() + 1:
                x, y, row = area.x(), y + row + self._gap, 0
            if apply:
                item.setGeometry(QRect(x, y, hint.width(), hint.height()))
            x += hint.width() + self._gap
            row = max(row, hint.height())
        return y + row - rect.y() + margins.bottom()


def horizontal_line() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFixedHeight(1)
    return line


def button(
    text: str,
    tooltip: str = "",
    on_click: Callable[[], None] | None = None,
    object_name: str = "",
    icon: str = "",
) -> QPushButton:
    # odstęp, bo Qt stawia ikonę tuż przy napisie, a arkusz stylów tego nie reguluje
    btn = QPushButton(f"  {text}" if icon else text)
    icons.set_icon(btn, icon)
    if tooltip:
        btn.setToolTip(tooltip)
    if object_name:
        btn.setObjectName(object_name)
    if on_click is not None:
        btn.clicked.connect(on_click)
    return btn
