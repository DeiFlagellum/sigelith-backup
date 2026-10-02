"""Okno „Zapisz szablon”: nazwa i kopia automatyczna (harmonogram) w jednym miejscu.

Wcześniej zapis z ekranu kopii pytał tylko o nazwę, a harmonogram dało się ustawić
wyłącznie na liście szablonów. Teraz kopię automatyczną wybiera się od razu przy
zapisie — te same cztery możliwości co w kreatorze i na liście szablonów.
"""

from __future__ import annotations

from PySide6.QtCore import QTime
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QTimeEdit,
    QWidget,
)

from cleanvault import scheduler
from cleanvault.i18n import tr
from cleanvault.state import Template

DEFAULT_TIME = QTime(20, 0)


class TemplateDialog(QDialog):
    """Nazwa szablonu i harmonogram; nazwa istniejącego szablonu podpowiada jego harmonogram."""

    def __init__(self, templates: list[Template], suggested: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._templates = templates
        self.setWindowTitle(tr("Zapisz szablon"))
        self.setMinimumWidth(460)

        self.name_edit = QLineEdit(suggested)
        self.schedule_combo = QComboBox()
        self.schedule_combo.addItem(tr("Ręcznie"), scheduler.MANUAL)
        self.schedule_combo.addItem(tr("Codziennie o godzinie"), scheduler.DAILY)
        self.schedule_combo.addItem(tr("Po podłączeniu dysku docelowego"), scheduler.ON_CONNECT)
        self.schedule_combo.addItem(tr("Na bieżąco"), scheduler.LIVE)
        self.schedule_combo.setToolTip(tr("Kiedy kopia z tego szablonu ma ruszać sama."))
        self.time_edit = QTimeEdit(DEFAULT_TIME)
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setToolTip(tr("Godzina kopii codziennej (czas tego komputera)."))

        when = QHBoxLayout()
        when.addWidget(self.schedule_combo, 1)
        when.addWidget(self.time_edit)
        form = QFormLayout(self)
        form.addRow(tr("Nazwa szablonu:"), self.name_edit)
        form.addRow(tr("Harmonogram:"), when)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

        self.name_edit.textChanged.connect(self._follow_existing)
        self.schedule_combo.currentIndexChanged.connect(self._sync_time)
        self._follow_existing(suggested)
        self._sync_time()

    def _follow_existing(self, name: str) -> None:
        """Zastępowany szablon zachowuje swój harmonogram, jeśli użytkownik go nie zmieni."""
        existing = next((t for t in self._templates if t.name == name.strip()), None)
        if existing is None:
            return
        self.schedule_combo.setCurrentIndex(max(0, self.schedule_combo.findData(existing.schedule)))
        time = QTime.fromString(existing.schedule_time or "", "HH:mm")
        self.time_edit.setTime(time if time.isValid() else DEFAULT_TIME)

    def _sync_time(self) -> None:
        self.time_edit.setEnabled(self.schedule_combo.currentData() == scheduler.DAILY)

    def values(self) -> tuple[str, str, str]:
        """(nazwa, harmonogram, godzina „HH:mm”)."""
        return (
            self.name_edit.text().strip(),
            self.schedule_combo.currentData(),
            self.time_edit.time().toString("HH:mm"),
        )
