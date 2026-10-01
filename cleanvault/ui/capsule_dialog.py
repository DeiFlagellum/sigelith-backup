"""Okno „Kapsuły czasu”: pieczętowanie folderu do daty i lista kapsuł w katalogu kopii.

Kapsułę otwiera strona sigelith.org/capsule/ — po dacie otwarcia; program
pieczętuje (capsule.py) i przechowuje kapsułę w kopii, obok magazynu dowodów.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from PySide6.QtCore import QDateTime, Qt, QUrl
from PySide6.QtGui import QDesktopServices, QGuiApplication
from PySide6.QtWidgets import (
    QDateTimeEdit,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from .. import capsule, rescue
from ..i18n import tr
from ..paths import CAPSULES_DIR
from .widgets import Hint, button, field_help, page_title
from .workers import EngineWorker


class CapsuleDialog(QDialog):
    def __init__(self, backup_root: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.root = Path(backup_root)
        self._worker: EngineWorker | None = None
        self.setWindowTitle(tr("Kapsuły czasu"))
        self.setMinimumSize(720, 480)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 18)
        layout.setSpacing(12)
        layout.addWidget(page_title(tr("Kapsuły czasu"), str(self.root / CAPSULES_DIR)))
        layout.addWidget(Hint(
            tr("Kapsuła pieczętuje wybrany folder do chwili, którą wskażesz. Otwierają ją dowolne dwie z trzech "
               "części: runda sieci drand z tej chwili, udział serwera kluczy Sigelith (wydawany dopiero po tej "
               "chwili — to zasada operatora, nie kryptografia) i kod odzyskiwania zapisany obok kapsuły. Kto ma "
               "tę kopię, ma więc i kod: do wcześniejszego otwarcia wystarczy mu, że operator złamie swoją "
               "zasadę. Po tej chwili otworzy ją każdy, kto ma jej pliki. Kapsuła leży w tej kopii, nie na "
               "serwerze; otwiera ją strona sigelith.org/capsule/."), icon="clock-history"))
        self.list = QListWidget()
        layout.addWidget(self.list, 1)
        self.details = field_help(tr("Wybierz kapsułę z listy albo utwórz nową."))
        layout.addWidget(self.details)
        row = QHBoxLayout()
        self.new_btn = button(tr("Nowa kapsuła…"), tr("Pieczętuje wybrany folder do daty"), self._new,
                              icon="shield-lock")
        row.addWidget(self.new_btn)
        row.addWidget(button(tr("Pokaż w folderze"), tr("Otwiera folder kapsuły w Eksploratorze"),
                             self._show_folder, icon="folder2-open"))
        self.open_btn = button(tr("Otwórz na stronie"), tr("Strona sigelith.org/capsule/ otwiera kapsułę po jej dacie"),
                               lambda: QDesktopServices.openUrl(QUrl(capsule.CAPSULE_PAGE)), icon="play-circle")
        row.addWidget(self.open_btn)
        row.addStretch(1)
        row.addWidget(button(tr("Zamknij"), "", self.reject))
        layout.addLayout(row)
        self.list.currentRowChanged.connect(lambda _row: self._selected_changed())
        self._fill()

    # ------------------------------------------------------------ lista

    def _capsules(self) -> list[tuple[Path, dict]]:
        found = []
        base = self.root / CAPSULES_DIR
        if base.is_dir():
            for envelope in sorted(base.glob(f"*/capsule-*{capsule.ENVELOPE_SUFFIX}")):
                try:
                    found.append((envelope, json.loads(envelope.read_text(encoding="utf-8"))))
                except (OSError, ValueError):
                    continue
        return found

    def _fill(self) -> None:
        self.list.clear()
        now = datetime.now(UTC)
        for path, envelope in self._capsules():
            opens = capsule.beat_moment(int(envelope.get("beat", 0)))
            state = tr("można otworzyć") if opens <= now else tr("zamknięta")
            item = QListWidgetItem(f"{path.parent.name}  •  {opens.astimezone().strftime('%Y-%m-%d %H:%M')}  •  {state}")
            item.setData(Qt.ItemDataRole.UserRole, (str(path), opens <= now))
            self.list.addItem(item)
        if not self.list.count():
            self.details.setText(tr("W tej kopii nie ma jeszcze kapsuł czasu."))
        self._selected_changed()

    def _selected(self) -> tuple[Path, bool] | None:
        item = self.list.currentItem()
        if item is None:
            return None
        path, openable = item.data(Qt.ItemDataRole.UserRole)
        return Path(path), bool(openable)

    def _selected_changed(self) -> None:
        chosen = self._selected()
        self.open_btn.setEnabled(bool(chosen and chosen[1]))
        if chosen:
            self.details.setText(
                tr("Ta kapsuła da się otworzyć na stronie sigelith.org/capsule/ — wskaż jej pliki.") if chosen[1]
                else tr("Kapsuła jest zamknięta do daty z listy. Kod odzyskiwania leży w pliku obok niej."))

    def _show_folder(self) -> None:
        chosen = self._selected()
        folder = chosen[0].parent if chosen else self.root / CAPSULES_DIR
        if folder.is_dir():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))

    # ------------------------------------------------------------ nowa

    def _new(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, tr("Wybierz folder do zapieczętowania"), str(Path.home()))
        if not folder:
            return
        settings = _NewCapsule(Path(folder).name, self)
        if settings.exec() != QDialog.DialogCode.Accepted:
            return
        name, when = settings.values()
        target = self.root / CAPSULES_DIR / capsule.capsule_dir_name(name, when)
        self.new_btn.setEnabled(False)
        self.details.setText(tr("Pieczętuję „{name}” — kilka sekund na krzywej eliptycznej…").format(name=name))

        def job(_reporter):
            sealed = capsule.seal_files([Path(folder)], when, target, name)
            files = [sealed.envelope_path.name] + ([sealed.blob_path.name] if sealed.blob_path else [])
            note = rescue.capsule_note(name, sealed.recovery_code, sealed.opens_at, files)
            (target / rescue.CAPSULE_NOTE_NAME).write_text(note, encoding="utf-8-sig")
            return sealed

        self._worker = EngineWorker(job, tr("kapsuła czasu"))
        self._worker.succeeded.connect(lambda sealed: self._sealed(sealed, name))
        self._worker.failed.connect(self._failed)
        self._worker.start()

    def _sealed(self, sealed: capsule.SealedCapsule, name: str) -> None:
        self.new_btn.setEnabled(True)
        self._fill()
        QGuiApplication.clipboard().setText(sealed.recovery_code)
        QMessageBox.information(
            self, tr("Kapsuła zapieczętowana"),
            tr("„{name}” otworzy się najwcześniej {when}.\n\nKod odzyskiwania (skopiowany do schowka, zapisany też "
               "obok kapsuły):\n\n{code}\n\nZapisz go w bezpiecznym miejscu. Przed datą otwarcia sam niczego nie "
               "otwiera; po niej zastępuje jeden z kluczy, gdyby był niedostępny.").format(
                name=name, when=sealed.opens_at.astimezone().strftime("%Y-%m-%d %H:%M"), code=sealed.recovery_code))

    def _failed(self, message: str) -> None:
        self.new_btn.setEnabled(True)
        self.details.setText(tr("Nie udało się zapieczętować: {error}").format(error=message))

    def done(self, result: int) -> None:
        if self._worker is not None and self._worker.isRunning():
            self._worker.wait(60_000)
        super().done(result)


class _NewCapsule(QDialog):
    """Nazwa i chwila otwarcia nowej kapsuły."""

    def __init__(self, name: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("Nowa kapsuła czasu"))
        form = QFormLayout(self)
        self.name = QLineEdit(name)
        form.addRow(tr("Nazwa"), self.name)
        self.when = QDateTimeEdit(QDateTime.currentDateTime().addYears(10))
        self.when.setCalendarPopup(True)
        self.when.setMinimumDateTime(QDateTime.currentDateTime().addSecs(3600))
        self.when.setDisplayFormat("yyyy-MM-dd HH:mm")
        form.addRow(tr("Otworzy się najwcześniej"), self.when)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def values(self) -> tuple[str, datetime]:
        moment = self.when.dateTime().toPython().astimezone()  # czas lokalny → strefa systemu
        return (self.name.text().strip() or tr("kapsuła")), moment.astimezone(UTC)
