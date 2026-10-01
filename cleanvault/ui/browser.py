"""Ekran przeglądania kopii: foldery, wersje, historia pliku i wyszukiwarka.

Otwarcie pliku z kopii nie wymaga przywracania całości: plik jest odtwarzany do
katalogu tymczasowego i otwierany w domyślnym programie. Przy kopii szyfrowanej
to jawna treść na dysku, więc katalog tymczasowy znika przy zamknięciu programu.
"""

from __future__ import annotations

import atexit
import json
import shutil
import tempfile
import time
from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .. import browse, crypto, fileproof, i18n, sigelith
from ..engine import human_size
from ..i18n import tr
from ..log import get_logger
from ..paths import package_family_name
from .widgets import Card, Hint, PathPicker, button, field_help, page_title
from .workers import EngineWorker

log = get_logger("ui.browser")

_ROLE = Qt.ItemDataRole.UserRole
_PLACEHOLDER = "…"


class BrowserPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._root = ""
        self._version = ""
        self._keyring: crypto.PasswordKeyring | None = None
        self._temp: str | None = None
        self._worker: EngineWorker | None = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(14)
        layout.addWidget(page_title(tr("Przeglądanie"), tr("Pliki i wersje wprost z kopii — bez przywracania całości.")))
        layout.addWidget(
            Hint(tr("Zaznacz plik i wybierz „Otwórz kopię”, żeby zajrzeć do niego w zwykłym programie, "
                    "albo „Historia pliku”, żeby zobaczyć, w których wersjach się zmieniał."), icon="folder2-open")
        )

        source = Card(tr("Kopia"))
        row = QHBoxLayout()
        self.picker = PathPicker(tr("Główny folder kopii"), dialog_title=tr("Wybierz folder kopii"))
        row.addWidget(self.picker, 1)
        row.addWidget(button(tr("Otwórz"), tr("Wczytuje wersje z tego folderu kopii"), self._open, icon="folder2-open"))
        source.add_layout(row)
        filters = QHBoxLayout()
        self.version_combo = QComboBox()
        self.version_combo.setToolTip(tr("Wersja kopii, której zawartość widzisz poniżej."))
        self.version_combo.currentIndexChanged.connect(lambda _i: self._load_version())
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText(tr("Szukaj pliku w najnowszym stanie kopii…"))
        self.search_edit.setToolTip(tr("Fragment nazwy albo ścieżki, bez rozróżniania wielkości liter."))
        self.search_edit.returnPressed.connect(self._search)
        filters.addWidget(self.version_combo)
        filters.addWidget(self.search_edit, 1)
        filters.addWidget(button(tr("Szukaj"), tr("Przeszukuje spis treści kopii"), self._search, icon="search"))
        filters.addWidget(button(tr("Pokaż foldery"), tr("Wraca z wyników wyszukiwania do drzewa folderów"),
                                 self._load_version))
        source.add_layout(filters)
        layout.addWidget(source)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels([tr("Nazwa"), tr("Rozmiar"), tr("Zmieniono")])
        self.tree.setColumnWidth(0, 420)
        self.tree.setMinimumHeight(300)
        self.tree.itemExpanded.connect(self._expand)
        self.tree.currentItemChanged.connect(lambda current, _previous: self._selected_changed(current))
        self.tree.itemDoubleClicked.connect(lambda item, _col: self._open_copy())
        layout.addWidget(self.tree, 1)

        self.details = field_help(tr("Wskaż folder kopii i kliknij „Otwórz”."))
        layout.addWidget(self.details)
        actions = QHBoxLayout()
        self.open_btn = button(tr("Otwórz kopię"), tr("Odtwarza plik do katalogu tymczasowego i otwiera go"),
                               self._open_copy, icon="eye")
        self.save_btn = button(tr("Zapisz jako…"), tr("Odtwarza plik w wybranym miejscu"), self._save_copy,
                               icon="box-arrow-down")
        self.history_btn = button(tr("Historia pliku"), tr("W których wersjach jest ten plik i kiedy się zmieniał"),
                                  self._show_history, icon="clock-history")
        self.proof_btn = button(tr("Dowód czasu…"), tr("Zapisuje dowód, że ten plik był w kopii w chwili jej "
                                                     "oznakowania — bez ujawniania innych plików"),
                                self._export_proof, icon="patch-check")
        self.handover_btn = button(tr("Przekaż…"), tr("Zapisuje tę wersję pliku i otwiera ją w Sigelith Handover — "
                                                   "odbiorca potwierdzi odbiór własnym kluczem"),
                                   self._hand_over, icon="send")
        for widget in (self.open_btn, self.save_btn, self.history_btn, self.proof_btn, self.handover_btn):
            actions.addWidget(widget)
        actions.addStretch(1)
        layout.addLayout(actions)
        self.history = QListWidget()
        self.history.setMaximumHeight(150)
        self.history.itemDoubleClicked.connect(self._open_from_history)
        self.history.hide()
        layout.addWidget(self.history)
        self._selected_changed(None)

    # ---------------------------------------------------------------- wersje

    def open_backup(self, path: str) -> None:
        """Wywoływane z innych ekranów — np. „Przeglądaj” przy przywracaniu."""
        self.picker.set_path(path)
        self._open()

    def _open(self) -> None:
        root = self.picker.path()
        if not root or not Path(root).is_dir():
            self.details.setText(tr("Wskaż folder kopii, aby zobaczyć jej zawartość."))
            return
        self._root = root
        self._keyring = None
        self.version_combo.blockSignals(True)
        self.version_combo.clear()
        for version in browse.versions(root):
            label = version.label + ("" if version.complete is not False else tr(" (niedokończona)"))
            self.version_combo.addItem(label, version.name)
        self.version_combo.blockSignals(False)
        if not self.version_combo.count():
            self.tree.clear()
            self.details.setText(tr("W tym folderze nie ma wersji kopii."))
            return
        self._load_version()

    def _load_version(self) -> None:
        if not self._root or self.version_combo.currentIndex() < 0:
            return
        self._version = self.version_combo.currentData() or ""
        self.tree.clear()
        for item in browse.list_folder(self._root, self._version):
            self._add(self.tree.invisibleRootItem(), item)
        self.details.setText(tr("Wersja: {version}").format(version=self.version_combo.currentText()))

    def _add(self, parent: QTreeWidgetItem, item: browse.Item) -> None:
        size = "" if item.is_dir else (human_size(item.size) if item.size is not None else "—")
        # data folderu w kopii to chwila zapisu kopii, a nie zmiany w oryginale — nie mylmy
        when = time.strftime(tr("%d.%m.%Y %H:%M"), time.localtime(item.mtime)) if not item.is_dir else ""
        node = QTreeWidgetItem([item.name, size, when])
        node.setData(0, _ROLE, item)
        node.setTextAlignment(1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        if item.is_dir:
            node.addChild(QTreeWidgetItem([_PLACEHOLDER]))  # strzałka rozwijania przed wczytaniem
        parent.addChild(node)

    def _expand(self, node: QTreeWidgetItem) -> None:
        if node.childCount() != 1 or node.child(0).text(0) != _PLACEHOLDER:
            return
        node.takeChild(0)
        item: browse.Item = node.data(0, _ROLE)
        for child in browse.list_folder(self._root, self._version, item.key):
            self._add(node, child)

    # ----------------------------------------------------------- wyszukiwanie

    def _search(self) -> None:
        text = self.search_edit.text()
        if not self._root or not text.strip():
            return
        self.details.setText(tr("Szukam…"))
        self._run(
            lambda _r: browse.search(self._root, text),
            self._show_results,
        )

    def _show_results(self, rows: list[tuple[str, int, float]]) -> None:
        self.tree.clear()
        for key, size, mtime in rows:
            node = QTreeWidgetItem([key, human_size(size), time.strftime(tr("%d.%m.%Y %H:%M"), time.localtime(mtime))])
            node.setData(0, _ROLE, key)
            self.tree.addTopLevelItem(node)
        self.details.setText(
            tr("Znalezione pliki: {count}. Wyniki pochodzą z najnowszego stanu kopii.").format(count=len(rows))
            if rows else tr("Nic nie znaleziono.")
        )

    # -------------------------------------------------------------- zaznaczenie

    def _selected(self) -> browse.Item | None:
        node = self.tree.currentItem()
        if node is None:
            return None
        data = node.data(0, _ROLE)
        if isinstance(data, str):  # wynik wyszukiwania — plik w najnowszej wersji, która go ma
            found = browse.locate(self._root, data)
            return found[1] if found else None
        return data if isinstance(data, browse.Item) and not data.is_dir else None

    def _selected_changed(self, node: QTreeWidgetItem | None) -> None:
        is_file = node is not None and (
            isinstance(node.data(0, _ROLE), str)
            or (isinstance(node.data(0, _ROLE), browse.Item) and not node.data(0, _ROLE).is_dir)
        )
        for widget in (self.open_btn, self.save_btn, self.history_btn, self.proof_btn, self.handover_btn):
            widget.setEnabled(is_file)
        self.history.clear()
        self.history.hide()

    # ---------------------------------------------------------------- akcje

    def _password_for(self, item: browse.Item) -> bool:
        if not browse.needs_password(item) or self._keyring is not None:
            return True
        password, accepted = QInputDialog.getText(
            self, tr("Hasło do kopii"), tr("Kopia jest zaszyfrowana — podaj hasło użyte przy jej tworzeniu."),
            QLineEdit.EchoMode.Password,
        )
        if not accepted or not password:
            return False
        self._keyring = crypto.PasswordKeyring(password)
        return True

    def _extract(self, item: browse.Item, target: Path, then) -> None:
        if not self._password_for(item):
            return
        self.details.setText(tr("Odtwarzam „{name}”…").format(name=item.name))
        root, keyring = self._root, self._keyring
        self._run(lambda _r: browse.extract(root, item, target, keyring), then)

    def _open_copy(self) -> None:
        item = self._selected()
        if item is None:
            return
        if self._temp is None:
            self._temp = tempfile.mkdtemp(prefix="tvb-podglad-")
            atexit.register(shutil.rmtree, self._temp, True)
        target = Path(self._temp) / f"{int(time.time() * 1000)}" / item.name

        def opened(path: Path) -> None:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))
            self.details.setText(tr("Otwarto kopię „{name}” (plik tymczasowy, zniknie po zamknięciu programu).").format(
                name=item.name))

        self._extract(item, target, opened)

    def _save_copy(self) -> None:
        item = self._selected()
        if item is None:
            return
        chosen, _filter = QFileDialog.getSaveFileName(self, tr("Zapisz kopię pliku"), str(Path.home() / item.name))
        if chosen:
            self._extract(item, Path(chosen), lambda path: self.details.setText(
                tr("Zapisano: {path}").format(path=path)))

    def _show_history(self) -> None:
        item = self._selected()
        if item is None:
            return
        self.history.clear()
        rows = browse.history(self._root, item.key)
        for index, row in enumerate(rows):
            size = human_size(row.item.size) if row.item.size is not None else "—"
            if index == len(rows) - 1:
                state = tr("najstarsza zachowana kopia")
            else:
                state = tr("zmieniony") if row.changed else tr("bez zmian")
            entry = QListWidgetItem(f"{row.version.label}  •  {size}  •  {state}")
            entry.setData(_ROLE, row.item)
            self.history.addItem(entry)
        self.history.setVisible(bool(rows))
        self.details.setText(tr("Wersje z tym plikiem: {count}. Dwuklik otwiera kopię z danej wersji.").format(
            count=len(rows)))

    def _export_proof(self) -> None:
        """Dowód czasu dla zaznaczonego pliku — z pieczęci wersji, w której leży jego kopia."""
        item = self._selected()
        if item is None:
            return
        answer = QMessageBox.question(
            self, tr("Dowód czasu"),
            tr("Dołączyć do dowodu ścieżkę pliku w kopii („{path}”)?\n\nBez niej dowód dalej potwierdza plik "
               "i chwilę oznakowania, ale nie mówi, gdzie plik leżał.").format(path=item.key),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Yes,
        )
        if answer == QMessageBox.StandardButton.Cancel:
            return
        folder = browse.seal_folder(self._root, item)
        include_path = answer == QMessageBox.StandardButton.Yes
        self.details.setText(tr("Przygotowuję dowód dla „{name}”…").format(name=item.name))
        self._run(lambda _r: fileproof.build(folder, item.key, include_path=include_path),
                  lambda doc: self._save_proof(item, doc))

    def _save_proof(self, item: browse.Item, doc: dict) -> None:
        from .proof_pdf import write_certificate

        chosen, _filter = QFileDialog.getSaveFileName(
            self, tr("Zapisz dowód czasu"), str(Path.home() / (item.name + fileproof.SUFFIX)),
            tr("Dowód pliku Sigelith (*{suffix})").format(suffix=fileproof.SUFFIX),
        )
        if not chosen:
            self.details.setText("")
            return
        target = Path(chosen)
        target.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        certificate = write_certificate(doc, target.with_name(target.name + ".pdf"), target.name)
        self.details.setText(tr("Zapisano dowód i certyfikat PDF: {path}. Sprawdzi go Sigelith Desktop albo "
                                "strona sigelith.org/verify/.").format(path=f"{target} · {certificate.name}"))

    def _hand_over(self) -> None:
        """Wersja pliku z kopii do Sigelith Handover: zapis w wybranym miejscu, potem okno wysyłki."""
        item = self._selected()
        if item is None:
            return
        if sigelith.desktop_launcher() is None:
            answer = QMessageBox.question(
                self, tr("Przekazanie z dowodem doręczenia"),
                tr("Przekazanie z dowodem doręczenia robi Sigelith Desktop (od wersji 3.0.1): odbiorca "
                   "potwierdza odbiór własnym kluczem, a chwila doręczenia trafia do publicznego dziennika. "
                   "Na tym komputerze go nie ma albo jest w starszej wersji. Otworzyć stronę programu?"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes,
            )
            if answer == QMessageBox.StandardButton.Yes:
                QDesktopServices.openUrl(QUrl(sigelith.product_url(
                    i18n.language(), packaged=package_family_name() is not None)))
            return
        chosen, _filter = QFileDialog.getSaveFileName(
            self, tr("Zapisz plik do przekazania"), str(Path.home() / item.name))
        if chosen:
            self._extract(item, Path(chosen), self._handed_over)

    def _handed_over(self, path: Path) -> None:
        if sigelith.hand_over(path):
            self.details.setText(tr("Otwieram Sigelith Handover z plikiem „{name}” — wybierz odbiorcę.").format(
                name=path.name))
        else:
            self.details.setText(tr("Zapisano: {path}").format(path=path))

    def _open_from_history(self, entry: QListWidgetItem) -> None:
        item: browse.Item = entry.data(_ROLE)
        if self._temp is None:
            self._temp = tempfile.mkdtemp(prefix="tvb-podglad-")
            atexit.register(shutil.rmtree, self._temp, True)
        target = Path(self._temp) / f"{int(time.time() * 1000)}" / item.name
        self._extract(item, target, lambda path: QDesktopServices.openUrl(QUrl.fromLocalFile(str(path))))

    # ------------------------------------------------------------------ wątek

    def _run(self, job, on_success) -> None:
        if self._worker is not None and self._worker.isRunning():
            return
        self._worker = EngineWorker(job, tr("przeglądanie kopii"))
        self._worker.succeeded.connect(on_success)
        self._worker.error.connect(self._failed)
        self._worker.start()

    def _failed(self, exc: Exception) -> None:
        if isinstance(exc, crypto.CryptoError):
            self._keyring = None  # np. złe hasło — zapytamy ponownie przy następnej próbie
        self.details.setText(tr("Nie udało się: {error}").format(error=exc))

    def shutdown(self) -> None:
        """Przed zamknięciem okna — wątek nie może przeżyć swojego widgetu."""
        if self._worker is not None and self._worker.isRunning():
            self._worker.wait(30_000)
        if self._temp is not None:
            shutil.rmtree(self._temp, ignore_errors=True)
