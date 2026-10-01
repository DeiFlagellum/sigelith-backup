"""Okna kopii poza domem (S3/B2) i znaczników czasu Sigelith.

Operacje sieciowe idą w wątku roboczym — okno nie może zamarzać na czas łączenia
z usługą. Każde okno czeka przy zamknięciu, aż jego wątek skończy: zniszczenie
działającego wątku Qt wywraca cały program.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from .. import audit, beat, offsite, proof, secrets_store
from ..crypto import PasswordKeyring
from ..i18n import mark, tr
from ..s3 import S3Client, S3Target
from ..state import StateStore, Template
from .widgets import Card, Hint, PasswordField, PathPicker, button, checkbox, field_help, page_title
from .workers import EngineWorker

OFFSITE_KEY = "offsite-key:{}"
OFFSITE_PASSWORD = "offsite-password:{}"

#: Gotowe ustawienia popularnych usług — użytkownik zmienia tylko region.
PRESETS = (
    ("Backblaze B2", "https://s3.eu-central-003.backblazeb2.com", "eu-central-003"),
    ("Amazon S3", "https://s3.eu-central-1.amazonaws.com", "eu-central-1"),
    (mark("MinIO / Wasabi / inna zgodna z S3"), "", ""),
)


def secrets_for(template_id: str) -> tuple[str, str]:
    key = secrets_store.load_password(OFFSITE_KEY.format(template_id)) or ""
    password = secrets_store.load_password(OFFSITE_PASSWORD.format(template_id)) or ""
    return key, password


class _Busy:
    """Wątek roboczy okna z pewnym zakończeniem przy zamykaniu."""

    def __init__(self) -> None:
        self.worker: EngineWorker | None = None

    def start(self, job, on_success, on_failure) -> bool:
        if self.worker is not None and self.worker.isRunning():
            return False
        self.worker = EngineWorker(job)
        self.worker.succeeded.connect(on_success)
        self.worker.failed.connect(on_failure)
        self.worker.start()
        return True

    def wait(self) -> None:
        if self.worker is not None and self.worker.isRunning():
            self.worker.cancel()
            self.worker.wait(30_000)


class OffsiteForm(QWidget):
    """Dane usługi, klucze i hasło kopii poza domem."""

    def __init__(self, new_password: bool = True) -> None:
        super().__init__()
        layout = QFormLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.preset = QComboBox()
        for name, _endpoint, _region in PRESETS:
            self.preset.addItem(tr(name))
        self.preset.currentIndexChanged.connect(self._preset_changed)
        self.endpoint = QLineEdit()
        self.endpoint.setPlaceholderText("https://s3.eu-central-003.backblazeb2.com")
        self.region = QLineEdit()
        self.bucket = QLineEdit()
        self.prefix = QLineEdit()
        self.prefix.setPlaceholderText(tr("np. komputer-domowy"))
        self.access_key = QLineEdit()
        self.secret = PasswordField(tr("Klucz tajny"), show_strength=False)
        self.password = PasswordField(tr("Hasło kopii poza domem"), show_strength=new_password)
        self.password_confirm = QLineEdit()
        self.password_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_confirm.setPlaceholderText(tr("Powtórz hasło"))
        self.password_confirm.setVisible(new_password)

        layout.addRow(tr("Usługa:"), self.preset)
        layout.addRow(tr("Adres usługi:"), self.endpoint)
        layout.addRow(tr("Region:"), self.region)
        layout.addRow(tr("Kubełek (bucket):"), self.bucket)
        layout.addRow(tr("Folder w kubełku:"), self.prefix)
        layout.addRow(tr("Identyfikator klucza:"), self.access_key)
        layout.addRow(tr("Klucz tajny:"), self.secret)
        layout.addRow(tr("Hasło szyfrowania:"), self.password)
        if new_password:
            layout.addRow("", self.password_confirm)
        self._new_password = new_password
        self._preset_changed(0)

    def _preset_changed(self, index: int) -> None:
        _name, endpoint, region = PRESETS[index]
        if endpoint and not self.endpoint.text():
            self.endpoint.setText(endpoint)
            self.region.setText(region)

    def load(self, target: S3Target, secret: str, password: str) -> None:
        self.endpoint.setText(target.endpoint)
        self.region.setText(target.region)
        self.bucket.setText(target.bucket)
        self.prefix.setText(target.prefix)
        self.access_key.setText(target.access_key)
        self.secret.set_password(secret)
        self.password.set_password(password)
        self.password_confirm.setText(password)

    def target(self) -> S3Target:
        return S3Target(
            endpoint=self.endpoint.text().strip(),
            region=self.region.text().strip(),
            bucket=self.bucket.text().strip(),
            access_key=self.access_key.text().strip(),
            prefix=self.prefix.text().strip().strip("/"),
        )

    def problem(self) -> str:
        target = self.target()
        if not (target.endpoint and target.region and target.bucket and target.access_key):
            return tr("Uzupełnij adres usługi, region, kubełek i identyfikator klucza.")
        if not self.secret.password():
            return tr("Podaj klucz tajny usługi.")
        if not self.password.password():
            return tr("Podaj hasło szyfrowania kopii poza domem.")
        if self._new_password and self.password.password() != self.password_confirm.text():
            return tr("Hasła w obu polach różnią się.")
        if self._new_password and len(self.password.password()) < 10:
            return tr("Hasło kopii poza domem powinno mieć co najmniej 10 znaków.")
        return ""


class OffsiteDialog(QDialog):
    """Kopia poza domem dla jednego szablonu."""

    def __init__(self, store: StateStore, template: Template, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.store = store
        self.template = template
        self.busy = _Busy()
        self.setWindowTitle(tr("Kopia poza domem"))
        self.setMinimumWidth(640)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 18)
        layout.setSpacing(12)
        layout.addWidget(page_title(tr("Kopia poza domem"), template.name))
        layout.addWidget(
            Hint(tr("Kopia na dysku obok komputera nie przetrwa pożaru ani kradzieży. Tu ustawisz "
                    "drugą kopię w usłudze zgodnej z S3 (np. Backblaze B2). Pliki są szyfrowane "
                    "na tym komputerze osobnym hasłem — usługa widzi tylko nieczytelne fragmenty."),
                 icon="shield-lock")
        )
        card = Card(tr("Usługa przechowywania"))
        self.form = OffsiteForm(new_password=not template.offsite)
        card.add(self.form)
        options = QHBoxLayout()
        options.addWidget(QLabel(tr("Zachowuj migawek:")))
        self.keep = QSpinBox()
        self.keep.setRange(1, 3650)
        self.keep.setValue(template.offsite_keep or 30)
        self.keep.setToolTip(tr("Starsze migawki są usuwane, gdy nadmiar sięgnie kilku — co kilka dni."))
        options.addWidget(self.keep)
        options.addStretch(1)
        card.add_layout(options)
        self.enabled = checkbox(
            tr("Wysyłaj poza dom po każdej udanej kopii z tego szablonu"),
            tr("Także po kopiach planowych. Wysyłane są tylko pliki nowe i zmienione."),
            checked=template.offsite_enabled or not template.offsite,
        )
        card.add(self.enabled)
        layout.addWidget(card)

        self.status = field_help("")
        layout.addWidget(self.status)
        row = QHBoxLayout()
        row.addWidget(button(tr("Sprawdź połączenie"), tr("Zapisuje, odczytuje i usuwa mały plik próbny"),
                             self._check, icon="search"))
        row.addStretch(1)
        row.addWidget(button(tr("Anuluj"), "", self.reject))
        row.addWidget(button(tr("Zapisz"), tr("Zapisuje ustawienia; klucz i hasło trafiają do Menedżera "
                                               "poświadczeń Windows"), self._save, object_name="Primary"))
        layout.addLayout(row)

        if template.offsite:
            secret, password = secrets_for(template.id)
            self.form.load(S3Target.from_dict(template.offsite), secret, password)

    def _check(self) -> None:
        problem = self.form.problem()
        if problem:
            self.status.setText(problem)
            return
        target, secret = self.form.target(), self.form.secret.password()
        self.status.setText(tr("Sprawdzam połączenie…"))
        self.busy.start(
            lambda _reporter: S3Client(target, secret, timeout=15, retries=1).check(),
            lambda _result: self.status.setText(tr("Połączenie działa: zapis, odczyt i usuwanie się udały.")),
            lambda message: self.status.setText(tr("Połączenie nie działa: {error}").format(error=message)),
        )

    def _save(self) -> None:
        problem = self.form.problem()
        if problem:
            self.status.setText(problem)
            return
        if not secrets_store.is_available():
            self.status.setText(tr("Kopia poza domem potrzebuje Menedżera poświadczeń Windows, "
                                   "a jest on niedostępny."))
            return
        saved_key = secrets_store.save_password(OFFSITE_KEY.format(self.template.id), self.form.secret.password())
        saved_password = secrets_store.save_password(
            OFFSITE_PASSWORD.format(self.template.id), self.form.password.password()
        )
        if not (saved_key and saved_password):
            self.status.setText(tr("Nie udało się zapisać klucza albo hasła w magazynie systemowym."))
            return
        current = self.store.get_template(self.template.id) or self.template
        current.offsite = self.form.target().to_dict()
        current.offsite_keep = self.keep.value()
        current.offsite_enabled = self.enabled.isChecked()
        self.store.put_template(current)
        self.accept()

    def done(self, result: int) -> None:
        self.busy.wait()
        super().done(result)


class OffsiteRestoreDialog(QDialog):
    """Przywracanie z kopii poza domem — z szablonu albo z danymi wpisanymi ręcznie.

    Ręczne dane to scenariusz, dla którego ta kopia istnieje: komputer przepadł,
    na nowym nie ma szablonów, jest tylko to, co użytkownik zapisał gdzie indziej.
    """

    def __init__(self, store: StateStore, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.store = store
        self.busy = _Busy()
        self.choice: tuple[S3Target, str, str, str, str] | None = None
        self.setWindowTitle(tr("Przywracanie z kopii poza domem"))
        self.setMinimumWidth(680)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 18)
        layout.setSpacing(12)
        layout.addWidget(page_title(tr("Przywracanie z kopii poza domem"),
                                    tr("Wybierz migawkę i katalog, do którego trafią pliki.")))
        source = Card(tr("Skąd"))
        self.templates = QComboBox()
        self._with_offsite = [t for t in store.templates().values() if t.offsite]
        for template in self._with_offsite:
            self.templates.addItem(template.name, template.id)
        self.templates.addItem(tr("Podam dane ręcznie"), "")
        self.templates.currentIndexChanged.connect(self._template_changed)
        source.add(self.templates)
        self.form = OffsiteForm(new_password=False)
        source.add(self.form)
        load_row = QHBoxLayout()
        load_row.addWidget(button(tr("Wczytaj migawki"), tr("Pobiera listę migawek z usługi"),
                                  self._load, icon="arrow-counterclockwise"))
        load_row.addStretch(1)
        source.add_layout(load_row)
        layout.addWidget(source)

        pick = Card(tr("Migawka i cel"))
        self.snapshots = QListWidget()
        self.snapshots.setMinimumHeight(140)
        pick.add(self.snapshots)
        self.destination = PathPicker(tr("Katalog, do którego trafią pliki"))
        pick.add(self.destination)
        layout.addWidget(pick)

        self.status = field_help("")
        layout.addWidget(self.status)
        row = QHBoxLayout()
        row.addStretch(1)
        row.addWidget(button(tr("Anuluj"), "", self.reject))
        row.addWidget(button(tr("Przywróć"), tr("Pobiera i odszyfrowuje pliki wybranej migawki"),
                             self._accept, object_name="Primary", icon="box-arrow-down"))
        layout.addLayout(row)
        self._template_changed(0)

    def _template_changed(self, _index: int) -> None:
        template_id = self.templates.currentData()
        template = self.store.get_template(template_id) if template_id else None
        self.form.setVisible(template is None)
        if template is not None:
            secret, password = secrets_for(template.id)
            self.form.load(S3Target.from_dict(template.offsite), secret, password)

    def _load(self) -> None:
        problem = self.form.problem()
        if problem:
            self.status.setText(problem)
            return
        target, secret = self.form.target(), self.form.secret.password()
        self.status.setText(tr("Łączę się z usługą…"))
        self.busy.start(
            lambda _reporter: offsite.list_snapshots(S3Client(target, secret, timeout=20, retries=2)),
            self._show,
            lambda message: self.status.setText(tr("Nie udało się wczytać migawek: {error}").format(error=message)),
        )

    def _show(self, stamps: list[str]) -> None:
        self.snapshots.clear()
        for stamp in reversed(stamps):
            item = QListWidgetItem(beat.describe(stamp))
            item.setData(Qt.ItemDataRole.UserRole, stamp)
            self.snapshots.addItem(item)
        if stamps:
            self.snapshots.setCurrentRow(0)
            self.status.setText(tr("Migawek w usłudze: {count}.").format(count=len(stamps)))
        else:
            self.status.setText(tr("W tym miejscu nie ma jeszcze kopii poza domem."))

    def _accept(self) -> None:
        item = self.snapshots.currentItem()
        if item is None:
            self.status.setText(tr("Wczytaj migawki i wybierz jedną z listy."))
            return
        if not self.destination.path():
            self.status.setText(tr("Wskaż katalog docelowy."))
            return
        self.choice = (
            self.form.target(),
            self.form.secret.password(),
            self.form.password.password(),
            item.data(Qt.ItemDataRole.UserRole),
            self.destination.path(),
        )
        self.accept()

    def done(self, result: int) -> None:
        self.busy.wait()
        super().done(result)


class ProofDialog(QDialog):
    """Znaczniki czasu wersji w jednym katalogu kopii."""

    def __init__(self, backup_root: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.root = Path(backup_root)
        self.busy = _Busy()
        self._keyring: PasswordKeyring | None = None
        self.setWindowTitle(tr("Znaczniki czasu"))
        self.setMinimumSize(700, 480)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 18)
        layout.setSpacing(12)
        layout.addWidget(page_title(tr("Znaczniki czasu Sigelith"), str(self.root)))
        layout.addWidget(
            Hint(tr("Znacznik dowodzi, że wersja kopii w dokładnie tym kształcie istniała w podanej "
                    "chwili. Podpis tygodnia pojawia się po jego zamknięciu (poniedziałek 00:00 UTC), "
                    "a kotwica w Bitcoinie — zwykle kilka godzin później."), icon="clock-history")
        )
        self.list = QListWidget()
        layout.addWidget(self.list, 1)
        self.details = field_help(tr("Wybierz wersję z listy."))
        layout.addWidget(self.details)
        row = QHBoxLayout()
        row.addWidget(button(tr("Sprawdź"), tr("Sprawdza spis wersji, drogę w drzewie tygodnia i podpis — bez sieci"),
                             self._check, icon="shield-check"))
        row.addWidget(button(tr("Odśwież z sieci"), tr("Pobiera podpis tygodnia i stan kotwicy w Bitcoinie"),
                             self._refresh, icon="arrow-counterclockwise"))
        row.addWidget(button(tr("Certyfikat PDF"), tr("Otwiera certyfikat znacznika na stronie Sigelith"),
                             self._certificate, icon="file-earmark-text"))
        row.addWidget(button(tr("Audyt treści"), tr("Czyta z nośnika każdy plik tej wersji i porównuje go z sumą "
                                                     "oznakowaną w publicznym dzienniku"),
                             self._audit, icon="search"))
        row.addWidget(button(tr("Ostatnia nietknięta"), tr("Sprawdza wersje od najnowszej i wskazuje ostatnią "
                                                            "zgodną z pieczęcią — z niej przywracaj"),
                             self._last_intact, icon="shield-check"))
        row.addStretch(1)
        row.addWidget(button(tr("Zamknij"), "", self.reject))
        layout.addLayout(row)
        self.list.currentRowChanged.connect(lambda _row: self._check())
        self._fill()

    def _folders(self) -> list[Path]:
        folders = [self.root] if (self.root / proof.SEAL_NAME).exists() else []
        if self.root.is_dir():
            folders += sorted(
                (p for p in self.root.iterdir() if p.is_dir() and (p / proof.SEAL_NAME).exists()),
                reverse=True,
            )
        return folders

    def _fill(self) -> None:
        self.list.clear()
        for folder in self._folders():
            seal = proof.read_seal(folder)
            if seal is None:
                continue
            label = beat.describe(folder.name) if folder != self.root else tr("kopia lustrzana")
            item = QListWidgetItem(f"{label}  •  {self._status_text(seal)}")
            item.setData(Qt.ItemDataRole.UserRole, str(folder))
            self.list.addItem(item)
        if not self.list.count():
            self.details.setText(tr("W tym katalogu kopii nie ma jeszcze znaczników czasu."))

    @staticmethod
    def _status_text(seal: proof.Seal) -> str:
        if seal.status == "pending":
            return tr("czeka na połączenie z Sigelith")
        if seal.status == "stamped":
            return tr("oznakowana {when} — podpis po zamknięciu tygodnia").format(
                when=seal.receipt.get("utc", "")[:16].replace("T", " ")
            )
        bitcoin = tr(", zakotwiczona w Bitcoinie") if seal.receipt.get("ots_status") == "bitcoin" else ""
        return tr("podpisana (tydzień {week}){bitcoin}").format(week=seal.receipt.get("week", ""), bitcoin=bitcoin)

    def _selected(self) -> Path | None:
        item = self.list.currentItem()
        return Path(item.data(Qt.ItemDataRole.UserRole)) if item is not None else None

    def _check(self) -> None:
        folder = self._selected()
        if folder is None:
            return
        result = proof.check(folder)
        lines = [
            (tr("Spis wersji zgodny ze znacznikiem: {answer}")).format(answer=tr("tak") if result.index_matches else tr("nie")),
        ]
        if result.stamped:
            lines.append(tr("Oznakowana: {utc} (BeatTime {beat})").format(utc=result.utc, beat=result.beat))
        if result.inclusion_ok is not None:
            lines.append(tr("Suma w drzewie tygodnia: {answer}").format(
                answer=tr("tak") if result.inclusion_ok else tr("nie")))
        if result.signature_ok is not None:
            lines.append(tr("Podpis Sigelith: {answer}").format(
                answer=tr("poprawny") if result.signature_ok else tr("NIEPOPRAWNY")))
        if result.bitcoin:
            lines.append(tr("Korzeń tygodnia zakotwiczony w łańcuchu Bitcoina."))
        lines += result.problems
        self.details.setText("\n".join(lines))

    def _refresh(self) -> None:
        folders = self._folders()
        self.details.setText(tr("Pobieram potwierdzenia…"))
        client = proof.BeatTimeClient()
        self.busy.start(
            lambda _reporter: [proof.refresh(folder, client) for folder in folders],
            lambda _result: (self._fill(), self.details.setText(tr("Potwierdzenia odświeżone."))),
            lambda message: self.details.setText(message),
        )

    def _label(self, version: str | None) -> str:
        return beat.describe(version) if version else tr("kopia lustrzana")

    def _audit(self) -> None:
        folder = self._selected()
        if folder is None:
            return
        version = "" if folder == self.root else folder.name
        self._run_audit(lambda reporter, keyring: audit.audit_version(self.root, version, keyring, reporter),
                        lambda result: self.details.setText(
                            f"{self._label(version)}: {result.describe()}"))

    def _last_intact(self) -> None:
        def show(outcome) -> None:
            audits, intact = outcome
            lines = [f"{self._label(item.version)}: {item.describe()}" for item in audits]
            if intact is not None:
                lines.append(tr("Ostatnia nietknięta wersja: {label} — z niej przywracaj.").format(
                    label=self._label(intact)))
            elif audits and not audits[-1].cancelled:
                lines.append(tr("Żadna wersja z pieczęcią nie jest nietknięta."))
            self.details.setText("\n".join(lines) or tr("W tym katalogu kopii nie ma jeszcze znaczników czasu."))

        self._run_audit(lambda reporter, keyring: audit.last_intact(self.root, keyring, reporter), show)

    def _run_audit(self, job, show) -> None:
        """Audyt w wątku; przy kopii zaszyfrowanej pyta o hasło i zaczyna od nowa."""
        keyring = self._keyring

        def work(reporter):
            try:
                return "done", job(reporter, keyring)
            except audit.AuditNeedsPassword:
                return "password", None

        def done(outcome) -> None:
            kind, value = outcome
            if kind == "done":
                show(value)
                return
            password, accepted = QInputDialog.getText(
                self, tr("Hasło do kopii"),
                tr("Kopia jest zaszyfrowana — podaj hasło użyte przy jej tworzeniu."), QLineEdit.EchoMode.Password)
            if accepted and password:
                self._keyring = PasswordKeyring(password)
                self._run_audit(job, show)
            else:
                self.details.setText("")

        self.details.setText(tr("Czytam pliki kopii i porównuję je z pieczęcią w publicznym dzienniku…"))
        self.busy.start(work, done, lambda message: self.details.setText(message))

    def _certificate(self) -> None:
        folder = self._selected()
        seal = proof.read_seal(folder) if folder else None
        if seal is not None and seal.status != "pending":
            QDesktopServices.openUrl(QUrl(proof.BeatTimeClient().cert_url(seal.digest)))

    def done(self, result: int) -> None:
        self.busy.wait()
        super().done(result)


def keyring_for(password: str) -> PasswordKeyring:
    return PasswordKeyring(password)
