"""Okno magazynu dowodów Sigelith: przegląd, sprawdzenie bez sieci i odzyskanie dokumentu."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLineEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .. import crypto, evidence
from ..i18n import tr
from .widgets import button, field_help, page_title
from .workers import EngineWorker

_ROLE = Qt.ItemDataRole.UserRole


class EvidenceDialog(QDialog):
    """Dokumenty oznakowane w Sigelith, zabezpieczone w katalogu kopii."""

    def __init__(self, root: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.root = Path(root)
        self._keyring: crypto.PasswordKeyring | None = None
        self._worker: EngineWorker | None = None
        self._results: dict[str, list[str]] = {}
        self.setWindowTitle(tr("Dowody Sigelith"))
        self.resize(900, 600)
        layout = QVBoxLayout(self)
        layout.addWidget(page_title(tr("Dowody Sigelith"), str(self.root / evidence.EVIDENCE_DIR)))
        layout.addWidget(field_help(
            tr("Każdy stempel ma tu swój folder z dokładnie tym dokumentem, który oznakowano, i plikiem "
               ".beatproof. „Sprawdź” liczy sumę każdego dokumentu i sprawdza podpis tygodnia bez "
               "łączenia się z siecią.")
        ))
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels([tr("Oznakowano"), tr("Dokument"), tr("Stan")])
        self.tree.setColumnWidth(0, 110)
        self.tree.setColumnWidth(1, 380)
        self.tree.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)
        layout.addWidget(self.tree, 1)
        self.status = field_help("")
        layout.addWidget(self.status)
        row = QHBoxLayout()
        self.verify_btn = button(tr("Sprawdź"), tr("Sprawdza każdy dokument i jego dowód bez łączenia z siecią"),
                                 self._verify, icon="shield-check")
        self.restore_btn = button(tr("Przywróć zaznaczone…"),
                                  tr("Zapisuje dokumenty razem z plikami .beatproof we wskazanym folderze"),
                                  self._restore, icon="box-arrow-down")
        row.addWidget(self.verify_btn)
        row.addWidget(self.restore_btn)
        row.addWidget(button(tr("Otwórz folder dowodów"), tr("Pokazuje magazyn dowodów w Eksploratorze"),
                             lambda: QDesktopServices.openUrl(
                                 QUrl.fromLocalFile(str(self.root / evidence.EVIDENCE_DIR)))))
        row.addStretch(1)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        row.addWidget(buttons)
        layout.addLayout(row)
        self.items = evidence.list_items(self.root)
        self._fill()

    # ------------------------------------------------------------------ lista

    def _state(self, item: evidence.Item) -> str:
        if item.folder.name in self._results:
            problems = self._results[item.folder.name]
            return tr("sprawdzony: dokument i dowód się zgadzają") if not problems else problems[0]
        if item.document is None:
            return tr("bez dokumentu — dowód zachowany")
        try:
            data = evidence.read_proof(item, self._keyring)
        except (OSError, ValueError, crypto.CryptoError):
            return tr("dowodu nie da się odczytać")
        if data is None:
            return tr("zaszyfrowany — podaj hasło, żeby sprawdzić")
        if not (data.get("week_closed") and data.get("root_signature")):
            return tr("dokument jest; dowód czeka na podpis tygodnia")
        return tr("dokument i dowód są w kopii")

    def _fill(self) -> None:
        self.tree.clear()
        for item in self.items:
            node = QTreeWidgetItem([item.date, item.name or item.digest16, self._state(item)])
            node.setData(0, _ROLE, item.folder.name)
            self.tree.addTopLevelItem(node)
        documents = sum(1 for item in self.items if item.document is not None)
        self.status.setText(tr("Stemple w magazynie: {count}, z dokumentem: {documents}.").format(
            count=len(self.items), documents=documents) if self.items else tr("Magazyn dowodów jest pusty."))
        for widget in (self.verify_btn, self.restore_btn):
            widget.setEnabled(bool(self.items))

    def _selected(self) -> list[evidence.Item]:
        chosen = {node.data(0, _ROLE) for node in self.tree.selectedItems()}
        return [item for item in self.items if item.folder.name in chosen]

    # ----------------------------------------------------------------- akcje

    def _password(self) -> bool:
        if self._keyring is not None or not any(item.encrypted for item in self.items):
            return True
        password, accepted = QInputDialog.getText(
            self, tr("Hasło do kopii"), tr("Kopia jest zaszyfrowana — podaj hasło użyte przy jej tworzeniu."),
            QLineEdit.EchoMode.Password,
        )
        if not accepted or not password:
            return False
        self._keyring = crypto.PasswordKeyring(password)
        return True

    def _run(self, job, on_success) -> None:
        if self._worker is not None and self._worker.isRunning():
            return
        self._worker = EngineWorker(job, tr("dowody Sigelith"))
        self._worker.succeeded.connect(on_success)
        self._worker.error.connect(self._failed)
        self._worker.start()

    def _failed(self, exc: Exception) -> None:
        if isinstance(exc, crypto.CryptoError):
            self._keyring = None
        self.status.setText(tr("Nie udało się: {error}").format(error=exc))

    def _verify(self) -> None:
        if not self._password():
            return
        items, keyring = list(self.items), self._keyring
        self.status.setText(tr("Sprawdzam dowody…"))

        def job(_reporter):
            return {item.folder.name: evidence.verify_item(item, keyring) for item in items}

        self._run(job, self._verified)

    def _verified(self, results: dict[str, list[str]]) -> None:
        self._results = results
        self._fill()
        bad = sum(1 for problems in results.values() if problems)
        self.status.setText(
            tr("Wszystkie dowody pasują do dokumentów i mają poprawny podpis.") if not bad
            else tr("Dowody z problemem: {count} — szczegóły w kolumnie „Stan”.").format(count=bad)
        )

    def _restore(self) -> None:
        items = self._selected() or list(self.items)
        if not items or not self._password():
            return
        target = QFileDialog.getExistingDirectory(self, tr("Gdzie zapisać dokumenty i dowody"), str(Path.home()))
        if not target:
            return
        keyring = self._keyring

        def job(_reporter):
            written = []
            for item in items:
                written += evidence.restore_item(item, Path(target) / item.folder.name, keyring)
            return written

        self._run(job, lambda written: self.status.setText(
            tr("Zapisano pliki: {count} w {path}.").format(count=len(written), path=target)))

    def done(self, result: int) -> None:
        if self._worker is not None and self._worker.isRunning():
            self._worker.wait(30_000)
        super().done(result)
