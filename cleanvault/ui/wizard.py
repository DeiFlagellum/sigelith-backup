"""Kreator: ekran powitalny i ustawienia pierwszej kopii.

Zasada, na której stoi cały ten plik: **pytamy o cel, nie o ustawienia.**
Ekran „Kopia zapasowa” zostaje bez zmian dla tych, którzy wiedzą, czego chcą;
kreator prowadzi resztę i na końcu zapisuje zwykły szablon — czyli dokładnie to
samo, co użytkownik ustawiłby ręcznie. Dzięki temu nie ma drugiego, równoległego
modelu konfiguracji, który trzeba by utrzymywać.

Kreator ma dwie role:

* **przy pierwszym uruchomieniu** — pięć kroków: co chronić, gdzie, jak mocno,
  kiedy i podsumowanie skutków (nie listy ustawień, tylko tego, co się wydarzy);
* **przy każdym kolejnym** — ekran powitalny z pytaniem, co teraz zrobić.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QStandardPaths, QStorageInfo, Qt, QTime, QUrl
from PySide6.QtGui import QDesktopServices, QGuiApplication
from PySide6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QRadioButton,
    QScrollArea,
    QStackedWidget,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

from .. import engine, i18n, scheduler, secrets_store, sigelith
from ..engine import human_size
from ..i18n import plural, tr
from ..log import get_logger
from ..paths import (
    DRIVE_NETWORK,
    DRIVE_OPTICAL,
    MANIFEST_NAME,
    drive_kind,
    is_system_drive,
    package_family_name,
)
from ..state import DEFAULT_EXCLUDES, StateStore, Template
from . import icons
from .widgets import Card, Hint, PasswordField, button, checkbox, field_help, page_title

log = get_logger("ui.wizard")

#: Nazwa katalogu zakładanego na wybranym nośniku. Sama mówi, co zawiera —
#: użytkownik znajdzie kopię nawet po latach i na cudzym komputerze.
BACKUP_FOLDER_NAME = "Sigelith Backup"
#: Katalogi zakładane pod poprzednimi nazwami programu. Kopia, która już na nośniku
#: jest, ma być kontynuowana — nie zaczynana od zera w katalogu o nowej nazwie.
LEGACY_BACKUP_FOLDER_NAMES = ("Time Vault Backup",)


def backup_folder_on(root: str | os.PathLike[str]) -> Path:
    """Katalog kopii na wybranym nośniku: istniejąca kopia spod dawnej nazwy albo nowy."""
    for name in LEGACY_BACKUP_FOLDER_NAMES:
        candidate = Path(root) / name
        if (candidate / MANIFEST_NAME).is_file():
            return candidate
    return Path(root) / BACKUP_FOLDER_NAME

#: Wykluczenia dokładane przy wyborze „projekty i kod”. To katalogi, które
#: odtwarza się jednym poleceniem, a potrafią być większe niż sam projekt.
PROJECT_EXCLUDES = [
    "node_modules/*",
    "venv/*",
    ".venv/*",
    "__pycache__/*",
    "build/*",
    "dist/*",
    "target/*",
    ".mypy_cache/*",
    ".pytest_cache/*",
]

@dataclass
class Choice:
    """Wynik kreatora: gotowy szablon i to, czy od razu ruszamy z kopią."""

    template: Template
    start_now: bool = False


# --------------------------------------------------------------- ekran powitalny


class WelcomeDialog(QDialog):
    """Cztery duże przyciski zamiast formularza — ekran przy każdym starcie."""

    BACKUP = "backup"
    RESTORE = "restore"
    VERIFY = "verify"
    SETTINGS = "settings"
    WIZARD = "wizard"

    def __init__(self, store: StateStore, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.store = store
        self.choice: str | None = None
        self.setWindowTitle(tr("Co chcesz teraz zrobić?"))
        self.setMinimumWidth(620)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 24, 26, 20)
        layout.setSpacing(14)
        layout.addWidget(page_title(tr("Co chcesz teraz zrobić?"), self._last_backup_line()))

        for key, icon, title, description in (
            (self.BACKUP, "play-circle", tr("Zrób kopię"),
             tr("Zapisuje nowe i zmienione pliki. Pierwszy raz trwa najdłużej.")),
            (self.RESTORE, "box-arrow-down", tr("Przywróć pliki"),
             tr("Odtwarza pliki z kopii — całość albo wybrany folder.")),
            (self.VERIFY, "shield-check", tr("Sprawdź kopię"),
             tr("Czyta kopię z nośnika i porównuje ją z zapisanymi sumami kontrolnymi.")),
            (self.SETTINGS, "gear", tr("Ustawienia"),
             tr("Język, motyw, domyślne wykluczenia i informacje o środowisku.")),
        ):
            layout.addWidget(self._action(key, icon, title, description))

        layout.addSpacing(4)
        self.hide_cb = checkbox(
            tr("Nie pokazuj tego ekranu przy starcie"),
            tr("Ekran powitalny wrócisz w ustawieniach, gdy zmienisz zdanie."),
            checked=not store.setting("show_welcome", True),
        )
        layout.addWidget(self.hide_cb)
        row = QHBoxLayout()
        row.setSpacing(10)
        row.addStretch(1)
        row.addWidget(button(tr("Ustawienia pierwszej kopii…"),
                             tr("Uruchamia kreator, który ustawi kopię krok po kroku"),
                             lambda: self._pick(self.WIZARD), icon="stars"))
        row.addWidget(button(tr("Zamknij"), tr("Przechodzi do pełnego okna programu"), self.reject))
        layout.addLayout(row)

    def _action(self, key: str, icon: str, title: str, description: str) -> QWidget:
        card = Card()
        row = QHBoxLayout()
        row.setSpacing(14)
        glyph = QLabel()
        glyph.setPixmap(icons.pixmap(icon, icons.current_color(), 34))
        glyph.setFixedWidth(40)
        glyph.setAlignment(Qt.AlignmentFlag.AlignTop)
        texts = QVBoxLayout()
        texts.setSpacing(2)
        name = QLabel(title)
        name.setObjectName("CardTitle")
        texts.addWidget(name)
        texts.addWidget(field_help(description))
        row.addWidget(glyph)
        row.addLayout(texts, 1)
        go = button(tr("Wybierz"), description, lambda: self._pick(key), object_name="Primary")
        row.addWidget(go, 0, Qt.AlignmentFlag.AlignVCenter)
        card.add_layout(row)
        return card

    def _last_backup_line(self) -> str:
        """Jedno zdanie o stanie ochrony — to jest powód, dla którego tu jesteśmy."""
        for entry in self.store.history(25):
            if entry.get("action") != "backup":
                continue
            when = time.strftime(tr("%d.%m.%Y %H:%M"), time.localtime(entry.get("at", 0)))
            count = int(entry.get("files", 0))
            return tr("Ostatnia kopia: {when} • {count} {files}.").format(
                when=when, count=count, files=plural(count, "plik", "pliki", "plików")
            )
        return tr("Nie było jeszcze żadnej kopii. Zacznij od „Zrób kopię”.")

    def _pick(self, key: str) -> None:
        self.choice = key
        self.store.set_setting("show_welcome", not self.hide_cb.isChecked())
        self.accept()

    def reject(self) -> None:
        """Zamknięcie krzyżykiem też zapamiętuje „nie pokazuj przy starcie”."""
        self.store.set_setting("show_welcome", not self.hide_cb.isChecked())
        super().reject()


# ---------------------------------------------------------------------- kreator


class SetupWizard(QDialog):
    """Cztery kroki od zera do gotowego szablonu kopii."""

    def __init__(self, store: StateStore, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.store = store
        self.result_choice: Choice | None = None
        self._sources: list[str] = []
        self._destination = ""
        # Kroki reagują na zmiany już w trakcie budowy (np. domyślny profil),
        # a pasek nawigacji powstaje po nich — do tego czasu nie ma czego odświeżać.
        self._ready = False

        self.setWindowTitle(tr("Ustawienia pierwszej kopii"))
        self.setMinimumSize(820, 640)
        # Na zwykłym monitorze cały krok mieści się bez przewijania (także karta Sigelith
        # na dole pierwszego kroku); na małym laptopie zostaje minimum i przewijanie.
        screen = QGuiApplication.primaryScreen()
        if screen is not None:
            available = screen.availableGeometry()
            self.resize(min(900, max(820, available.width() - 120)), min(880, max(640, available.height() - 100)))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 24, 26, 20)
        layout.setSpacing(14)

        self.header = page_title(tr("Ustawienia pierwszej kopii"), "")
        layout.addWidget(self.header)

        self.steps = QStackedWidget()
        # Kroki przewijają się, zamiast ściskać karty na małych ekranach (laptop 1366×768).
        for build in (self._build_sources_step, self._build_destination_step, self._build_protection_step,
                      self._build_when_step, self._build_summary_step):
            area = QScrollArea()
            area.setWidgetResizable(True)
            area.setFrameShape(QFrame.Shape.NoFrame)
            area.setWidget(build())
            self.steps.addWidget(area)
        layout.addWidget(self.steps, 1)

        nav = QHBoxLayout()
        nav.setSpacing(10)
        self.step_label = QLabel()
        self.step_label.setObjectName("FieldHelp")
        nav.addWidget(self.step_label)
        nav.addStretch(1)
        self.back_btn = button(tr("Wstecz"), tr("Wraca do poprzedniego kroku"), self._back)
        self.next_btn = button(tr("Dalej"), tr("Przechodzi do następnego kroku"),
                               self._next, object_name="Primary")
        self.save_btn = button(tr("Zapisz ustawienia"), tr("Zapisuje szablon bez uruchamiania kopii"),
                               lambda: self._finish(start_now=False), icon="bookmark-plus")
        self.run_btn = button(tr("Zapisz i zrób kopię"), tr("Zapisuje szablon i od razu uruchamia kopię"),
                              lambda: self._finish(start_now=True), object_name="Primary",
                              icon="play-fill")
        nav.addWidget(button(tr("Anuluj"), tr("Zamyka kreator bez zapisywania"), self.reject))
        nav.addWidget(self.back_btn)
        nav.addWidget(self.next_btn)
        nav.addWidget(self.save_btn)
        nav.addWidget(self.run_btn)
        layout.addLayout(nav)

        self._ready = True
        self._show_step(0)

    # ------------------------------------------------------------ krok 1: źródła

    def _build_sources_step(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        card = Card(tr("Co chcesz chronić?"),
                    tr("Wybierz to, co najbliższe. Dokładną listę folderów poprawisz niżej."))
        self.purpose_group = QButtonGroup(self)
        self.purpose_group.setExclusive(True)
        for index, (title, description) in enumerate((
            (tr("Dokumenty i zdjęcia"),
             tr("Twoje pliki osobiste z folderów użytkownika. Najczęstszy wybór.")),
            (tr("Projekty i kod"),
             tr("Foldery z pracą. Kreator pominie katalogi, które odtwarza się "
                "jednym poleceniem (node_modules, venv, build).")),
            (tr("Wybrane foldery"),
             tr("Sam wskażesz, co ma trafić do kopii.")),
        )):
            radio = QRadioButton(title)
            radio.setToolTip(description)
            self.purpose_group.addButton(radio, index)
            card.add(radio)
            card.add(field_help(description))
        self.purpose_group.button(0).setChecked(True)
        self.purpose_group.idToggled.connect(self._purpose_changed)
        layout.addWidget(card)

        folders = Card(tr("Foldery objęte kopią"),
                       tr("Podfoldery są uwzględniane automatycznie."))
        self.source_view = QListWidget()
        self.source_view.setMinimumHeight(110)
        self.source_view.setMaximumHeight(150)  # zwykle 3–5 folderów; reszta miejsca dla karty Sigelith
        folders.add(self.source_view)
        row = QHBoxLayout()
        row.addWidget(button(tr("Dodaj folder"), tr("Wybierz kolejny folder do kopii"),
                             self._add_source, icon="folder-plus"))
        row.addWidget(button(tr("Usuń zaznaczone"), tr("Usuwa pozycję z listy. Nie kasuje żadnych plików."),
                             self._remove_source, icon="dash-circle"))
        row.addStretch(1)
        folders.add_layout(row)
        layout.addWidget(folders)
        layout.addWidget(self._build_sigelith_card())
        layout.addStretch(1)

        self._purpose_changed(0, True)
        return page

    def _build_sigelith_card(self) -> QWidget:
        """Dowody czasu z Sigelith Desktop (ten sam wydawca) — karta dla każdego.

        Kto ma Sigelith, włącza ochronę jego dowodów jednym zaznaczeniem. Kto nie ma,
        dowiaduje się, co zyskałyby jego ważne dokumenty, i może włączyć ochronę na zapas:
        zacznie działać sama, gdy Sigelith Desktop pojawi się na komputerze.
        """
        self._sigelith_dir = sigelith.find_data_dir()
        if self._sigelith_dir is not None:
            count = len(sigelith.load_stamps(self._sigelith_dir))
            card = Card(tr("Dowody czasu dla ważnych dokumentów"),
                        tr("Na tym komputerze jest Sigelith Desktop: {count} {stamps}.").format(
                            count=count, stamps=plural(count, "stempel", "stemple", "stempli")))
            card.add(field_help(tr(
                "Kopia zachowa każdy dokument oznakowany w Sigelith Desktop dokładnie w tej postaci, "
                "którą oznakowano, razem z dowodem — nawet gdy oryginał później się zmieni.")))
            self.sigelith_cb = checkbox(
                tr("Chroń też dowody Sigelith"),
                tr("Historia stempli Sigelith Desktop i dokładne bajty oznakowanych dokumentów, "
                   "z plikami .beatproof — w osobnym magazynie, którego retencja nie sprząta."),
                checked=True,
            )
            card.add(self.sigelith_cb)
            return card
        card = Card(tr("Dowody czasu dla ważnych dokumentów"),
                    tr("Umowy, faktury, projekty — czasem trzeba wykazać, że dokument istniał danego dnia."))
        card.add(field_help(tr(
            "Sigelith Desktop, program tego samego wydawcy, oznakuje dokument czasem: to podpisany "
            "dowód, że plik w tej postaci istniał w danej chwili, sprawdzalny bez udziału kogokolwiek. "
            "Sigelith Backup przechowa potem każdy oznakowany dokument razem z dowodem.")))
        row = QHBoxLayout()
        row.addWidget(button(tr("Poznaj Sigelith Desktop"), tr("Otwiera stronę programu Sigelith Desktop"),
                             self._open_sigelith, icon="patch-check"))
        self.sigelith_cb = checkbox(
            tr("Chroń dowody Sigelith, gdy go zainstaluję"),
            tr("Ochrona zacznie działać sama, gdy na komputerze pojawi się Sigelith Desktop."),
            checked=False,
        )
        row.addWidget(self.sigelith_cb)
        row.addStretch(1)
        card.add_layout(row)
        return card

    @staticmethod
    def _open_sigelith() -> None:
        url = sigelith.product_url(i18n.language(), packaged=package_family_name() is not None)
        QDesktopServices.openUrl(QUrl(url))

    def _purpose_changed(self, index: int, checked: bool) -> None:
        if not checked:
            return
        if index == 0:
            self._set_sources(_personal_folders())
        elif index == 1:
            self._set_sources([])
        else:
            self._set_sources([])

    def _set_sources(self, paths: list[str]) -> None:
        self._sources = [p for p in paths if p]
        self.source_view.clear()
        for path in self._sources:
            self.source_view.addItem(QListWidgetItem(path))
        self._update_nav()

    def _add_source(self) -> None:
        chosen = QFileDialog.getExistingDirectory(self, tr("Wybierz folder do kopii"), str(Path.home()))
        if chosen and chosen not in self._sources:
            self._set_sources([*self._sources, chosen])

    def _remove_source(self) -> None:
        for item in self.source_view.selectedItems():
            self._sources.remove(item.text())
        self._set_sources(self._sources)

    # --------------------------------------------------------- krok 2: nośnik

    def _build_destination_step(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        card = Card(tr("Gdzie zapisać kopię?"),
                    tr("Najlepiej na innym dysku fizycznym niż ten, który chronisz — "
                       "kopia obok oryginału ginie razem z nim."))
        self.volume_view = QListWidget()
        self.volume_view.setMinimumHeight(300)
        self.volume_view.setWordWrap(True)
        self.volume_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.volume_view.setSpacing(3)
        self.volume_view.currentRowChanged.connect(lambda _row: self._volume_chosen())
        card.add(self.volume_view)
        row = QHBoxLayout()
        row.addWidget(button(tr("Wybierz inny folder…"), tr("Wskaż dowolny katalog docelowy"),
                             self._choose_folder, icon="folder"))
        row.addWidget(button(tr("Odśwież listę"), tr("Ponownie sprawdza podłączone nośniki"),
                             self._refresh_volumes, icon="arrow-counterclockwise"))
        row.addStretch(1)
        card.add_layout(row)
        layout.addWidget(card)

        self.destination_note = field_help("")
        layout.addWidget(self.destination_note)
        layout.addStretch(1)
        return page

    def _refresh_volumes(self) -> None:
        self.volume_view.clear()
        self._volumes = detect_volumes()
        for volume in self._volumes:
            item = QListWidgetItem(volume.describe())
            item.setIcon(icons.icon("usb-drive" if volume.removable else "device-hdd"))
            item.setData(Qt.ItemDataRole.UserRole, volume.root)
            self.volume_view.addItem(item)
        if self._volumes:
            self.volume_view.setCurrentRow(0)

    def _volume_chosen(self) -> None:
        item = self.volume_view.currentItem()
        if item is None:
            return
        root = item.data(Qt.ItemDataRole.UserRole)
        self._set_destination(str(backup_folder_on(root)))

    def _choose_folder(self) -> None:
        chosen = QFileDialog.getExistingDirectory(self, tr("Wybierz katalog docelowy kopii"), str(Path.home()))
        if chosen:
            self.volume_view.setCurrentRow(-1)
            self._set_destination(chosen)

    def _set_destination(self, path: str) -> None:
        self._destination = path
        self.destination_note.setText(self._destination_warning(path))
        self._update_nav()

    def _destination_warning(self, path: str) -> str:
        parts = [tr("Kopia trafi do: {path}").format(path=path)]
        if is_system_drive(path):
            parts.append(tr("To dysk systemowy — kopia nie przetrwa jego awarii. "
                            "Jeśli masz drugi dysk albo pendrive, wybierz jego."))
        for source in self._sources:
            if _inside(path, source):
                parts.append(tr("Ten katalog leży wewnątrz folderu źródłowego — wybierz inny."))
                break
        return "\n".join(parts)

    # ------------------------------------------------------ krok 3: ochrona

    def _build_protection_step(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        card = Card(tr("Jak bardzo chcesz się zabezpieczyć?"),
                    tr("Trzy gotowe zestawy zamiast kilkunastu przełączników."))
        self.profile_group = QButtonGroup(self)
        self.profile_group.setExclusive(True)
        for index, (title, description) in enumerate((
            (tr("Jedna aktualna kopia"),
             tr("Najszybsza i najmniejsza. Kopia odpowiada temu, co masz teraz — "
                "bez historii wcześniejszych wersji.")),
            (tr("Historia zmian (zalecane)"),
             tr("Każdy przebieg tworzy folder z datą. Pliki niezmienione są podpinane "
                "dowiązaniem, więc historia kosztuje tyle, ile realnie się zmieniło.")),
            (tr("Historia i szyfrowanie"),
             tr("Jak wyżej, a dodatkowo każdy plik trafia do kopii zaszyfrowany "
                "(AES-256-GCM). Potrzebne przy kopii wożonej poza dom.")),
        )):
            radio = QRadioButton(title)
            radio.setToolTip(description)
            self.profile_group.addButton(radio, index)
            card.add(radio)
            card.add(field_help(description))
        self.profile_group.button(1).setChecked(True)
        self.profile_group.idToggled.connect(lambda _i, _c: self._profile_changed())
        layout.addWidget(card)

        self.password_card = Card(tr("Hasło do kopii"),
                                  tr("Bez hasła nie da się odczytać ani jednego pliku z kopii."))
        self.password = PasswordField(tr("Hasło do kopii"))
        self.password_confirm = PasswordField(tr("Powtórz hasło"), show_strength=False)
        self.password.changed.connect(lambda _t: self._update_nav())
        self.password_confirm.changed.connect(lambda _t: self._update_nav())
        self.password_card.add(self.password)
        self.password_card.add(self.password_confirm)
        self.remember_cb = checkbox(
            tr("Zapamiętaj hasło w Menedżerze poświadczeń Windows"),
            tr("Potrzebne, żeby kopie planowe ruszały bez Twojego udziału. Hasło trafia do "
               "magazynu systemowego powiązanego z Twoim kontem, nie do plików programu."),
            checked=secrets_store.is_available(),
        )
        self.remember_cb.setEnabled(secrets_store.is_available())
        self.password_card.add(self.remember_cb)
        self.password_card.add(
            Hint(tr("Hasła nie da się odzyskać ani zresetować. Jeśli je zgubisz, dane z kopii "
                    "zaszyfrowanej są bezpowrotnie stracone — tak działa poprawne szyfrowanie."),
                 icon="exclamation-triangle")
        )
        layout.addWidget(self.password_card)
        layout.addStretch(1)
        self._profile_changed()
        return page

    def _profile_changed(self) -> None:
        self.password_card.setVisible(self.profile_group.checkedId() == 2)
        self._update_nav()

    def _password_problem(self) -> str:
        if self.profile_group.checkedId() != 2:
            return ""
        password = self.password.password()
        if not password:
            return tr("Podaj hasło — bez niego nie można zaszyfrować kopii.")
        if password != self.password_confirm.password():
            return tr("Hasła w obu polach różnią się.")
        if len(password) < 8:
            return tr("Hasło powinno mieć co najmniej 8 znaków.")
        return ""

    # --------------------------------------------------------- krok 4: kiedy

    def _build_when_step(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        card = Card(tr("Kiedy robić kopię?"),
                    tr("Kopia sprzed miesiąca nie chroni tego, co zmieniło się od tamtej pory."))
        self.when_group = QButtonGroup(self)
        self.when_group.setExclusive(True)
        self._when_values = [scheduler.DAILY, scheduler.LIVE, scheduler.ON_CONNECT, scheduler.MANUAL]
        options = (
            (tr("Codziennie o wybranej godzinie (zalecane)"),
             tr("Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.")),
            (tr("Na bieżąco — po każdej zmianie i po podłączeniu dysku"),
             tr("Dla dysku podłączonego na stałe albo często: zmiany trafiają do kopii kilka minut "
                "po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje.")),
            (tr("Po podłączeniu dysku z kopią"),
             tr("Dla dysku USB podłączanego od czasu do czasu. Najwyżej jedna kopia na 12 godzin.")),
            (tr("Ręcznie — kiedy zechcę"),
             tr("Kopię uruchamiasz przyciskiem. Najprostsze, ale łatwo o niej zapomnieć.")),
        )
        for index, (title, description) in enumerate(options):
            radio = QRadioButton(title)
            radio.setToolTip(description)
            self.when_group.addButton(radio, index)
            if index == 0:
                row = QHBoxLayout()
                row.addWidget(radio)
                self.when_time = QTimeEdit(QTime(20, 0))
                self.when_time.setDisplayFormat("HH:mm")
                self.when_time.setToolTip(tr("Godzina kopii codziennej (czas tego komputera)."))
                row.addWidget(self.when_time)
                row.addStretch(1)
                card.add_layout(row)
            else:
                card.add(radio)
            card.add(field_help(description))
        self.when_group.button(0).setChecked(True)
        self.when_group.idToggled.connect(
            lambda _i, _c: self.when_time.setEnabled(self.when_group.checkedId() == 0)
        )
        layout.addWidget(card)
        layout.addWidget(
            Hint(tr("Kopie planowe działają, gdy działa program: po zamknięciu okna zostaje ikona "
                    "przy zegarze, a przy logowaniu do Windows program uruchamia się w tle."))
        )
        layout.addStretch(1)
        return page

    def schedule_choice(self) -> tuple[str, str]:
        """Wybrany harmonogram i godzina („GG:MM”)."""
        return self._when_values[self.when_group.checkedId()], self.when_time.time().toString("HH:mm")

    # --------------------------------------------------- krok 5: podsumowanie

    def _build_summary_step(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.summary_card = Card(tr("To się wydarzy"),
                                 tr("Nie lista ustawień, tylko ich skutki."))
        self.summary_text = field_help("")
        self.summary_card.add(self.summary_text)
        layout.addWidget(self.summary_card)

        self.medium_card = Card(tr("Nośnik docelowy"))
        self.medium_text = field_help("")
        self.medium_card.add(self.medium_text)
        layout.addWidget(self.medium_card)

        layout.addStretch(1)
        return page

    def _fill_summary(self) -> None:
        profile = self.profile_group.checkedId()
        lines = [
            tr("Foldery objęte kopią ({count}): {list}").format(
                count=len(self._sources),
                list=", ".join(self._sources),
            ),
            tr("Kopia powstanie w: {path}").format(path=self._destination),
        ]
        if profile == 0:
            lines.append(tr("Program będzie utrzymywał jeden folder zgodny ze źródłem. "
                            "Każdy kolejny przebieg dopisze tylko to, co się zmieniło."))
        else:
            lines.append(tr("Każdy przebieg utworzy folder z datą. Pierwszy zajmie tyle, ile dane; "
                            "kolejne — tyle, ile realnie się zmieniło."))
        if profile == 2:
            lines.append(tr("Pliki w kopii będą zaszyfrowane; bez hasła nie da się ich odczytać."))
        if self.sigelith_cb.isChecked() and self._sigelith_dir is not None:
            lines.append(tr("Dowody Sigelith: historia stempli i dokładne kopie oznakowanych dokumentów "
                            "z plikami .beatproof trafią do magazynu dowodów w katalogu kopii."))
        elif self.sigelith_cb.isChecked():
            lines.append(tr("Dowody Sigelith: ochrona zacznie działać sama, gdy zainstalujesz Sigelith Desktop."))
        lines.append(tr("Pierwszy przebieg jest najdłuższy — kolejne porównują rozmiar i datę "
                        "modyfikacji, więc zwykle trwają sekundy."))
        schedule, at = self.schedule_choice()
        if schedule == scheduler.DAILY:
            lines.append(tr("Kopia będzie robiona codziennie o {time}; termin przegapiony przy "
                            "wyłączonym komputerze program nadrobi po jego włączeniu.").format(time=at))
        elif schedule == scheduler.ON_CONNECT:
            lines.append(tr("Kopia ruszy po podłączeniu dysku docelowego (najwyżej raz na 12 godzin)."))
        elif schedule == scheduler.LIVE:
            lines.append(tr("Kopia będzie na bieżąco: zmiany trafią do dzisiejszej wersji kilka minut "
                            "po zapisie, a po podłączeniu dysku kopia od razu się zsynchronizuje."))
        else:
            lines.append(tr("Kopię uruchamiasz sam — przyciskiem w programie albo z menu ikony "
                            "przy zegarze."))
        self.summary_text.setText("\n\n".join(lines))
        self.medium_text.setText(self._medium_description())

    def _medium_description(self) -> str:
        # Kreator proponuje katalog, którego jeszcze nie ma — o nośniku mówi
        # wtedy najbliższy istniejący katalog nadrzędny (zwykle korzeń dysku).
        # Bez tego ocena pokazywała „0 B z 0 B” i żadnych ostrzeżeń.
        try:
            info = engine.inspect_destination(_nearest_existing(self._destination))
            if Path(self._destination).is_dir():
                info.entry_count = engine.inspect_destination(self._destination).entry_count
            else:
                info.entry_count = None
        except OSError as exc:
            return tr("Nie można odczytać informacji o dysku: {error}").format(error=exc)
        lines = [
            tr("Wolne miejsce: {free} z {total}").format(
                free=human_size(info.free), total=human_size(info.total)
            )
        ]
        if info.filesystem:
            lines.append(tr("System plików: {filesystem}, klaster {cluster}").format(
                filesystem=info.filesystem, cluster=human_size(info.cluster)
            ))
        if not info.hardlinks_likely:
            lines.append(tr("Ten nośnik nie obsługuje twardych dowiązań, więc każda wersja z datą "
                            "zajmie tyle miejsca co pełna kopia. Przy tym nośniku rozważ "
                            "„jedną aktualną kopię”."))
        if info.entry_count:
            lines.append(tr("W tym katalogu jest już kopia ({count} {files}) — program ją uzupełni, "
                            "a nie nadpisze.").format(
                count=info.entry_count, files=plural(info.entry_count, "plik", "pliki", "plików")
            ))
        return "\n".join(lines)

    # ------------------------------------------------------------- nawigacja

    def _show_step(self, index: int) -> None:
        if index == 1 and not getattr(self, "_volumes", None):
            self._refresh_volumes()
        if index == self.steps.count() - 1:
            self._fill_summary()
        self.steps.setCurrentIndex(index)
        self._update_nav()

    def _update_nav(self) -> None:
        if not self._ready:
            return
        index = self.steps.currentIndex()
        last = self.steps.count() - 1
        self.step_label.setText(tr("Krok {number} z {total}").format(number=index + 1, total=last + 1))
        self.back_btn.setEnabled(index > 0)
        self.next_btn.setVisible(index < last)
        self.save_btn.setVisible(index == last)
        self.run_btn.setVisible(index == last)
        self.next_btn.setEnabled(not self._step_problem(index))
        self.next_btn.setToolTip(self._step_problem(index) or tr("Przechodzi do następnego kroku"))

    def _step_problem(self, index: int) -> str:
        """Czego brakuje, by przejść dalej — także treść podpowiedzi przycisku."""
        if index == 0 and not self._sources:
            return tr("Dodaj przynajmniej jeden folder źródłowy.")
        if index == 1:
            if not self._destination:
                return tr("Wskaż katalog docelowy kopii.")
            if any(_inside(self._destination, source) for source in self._sources):
                return tr("Katalog docelowy leży wewnątrz źródła — wybierz inny.")
        if index == 2:
            return self._password_problem()
        return ""

    def _next(self) -> None:
        if self._step_problem(self.steps.currentIndex()):
            return
        self._show_step(min(self.steps.currentIndex() + 1, self.steps.count() - 1))

    def _back(self) -> None:
        self._show_step(max(self.steps.currentIndex() - 1, 0))

    def _finish(self, start_now: bool) -> None:
        profile = self.profile_group.checkedId()
        excludes = list(self.store.setting("default_excludes", DEFAULT_EXCLUDES))
        if self.purpose_group.checkedId() == 1:
            excludes += [pattern for pattern in PROJECT_EXCLUDES if pattern not in excludes]
        schedule, at = self.schedule_choice()
        template = Template(
            name=self._template_name(),
            sources=list(self._sources),
            destination=self._destination,
            structure="mirror" if profile == 0 else "dated",
            encrypt=profile == 2,
            excludes=excludes,
            schedule=schedule,
            schedule_time=at,
            sigelith=self.sigelith_cb.isChecked(),
        )
        if template.structure == "dated":
            # „Historia zmian” = kalendarz: gęsto dla świeżych zmian, rzadko dla dawnych
            template.gfs_daily, template.gfs_weekly, template.gfs_monthly = 7, 4, 12
        scheduler.arm(template)
        if template.encrypt and self.remember_cb.isChecked():
            template.remember_password = secrets_store.save_password(template.id, self.password.password())
        self.store.put_template(template)
        self.store.set_setting("wizard_done", True)
        self.result_choice = Choice(template=template, start_now=start_now)
        log.info("Kreator zapisał szablon %s (uruchomienie: %s)", template.name, start_now)
        self.accept()

    def _template_name(self) -> str:
        names = {tr("Dokumenty i zdjęcia"), tr("Projekty i kod")}
        chosen = self.purpose_group.checkedButton()
        if chosen is not None and chosen.text() in names:
            return tr("Kopia: {what}").format(what=chosen.text().lower())
        first = Path(self._sources[0]).name if self._sources else ""
        return tr("Kopia {folder}").format(folder=first) if first else tr("Nowy szablon")

    def password_value(self) -> str:
        """Hasło wpisane w kreatorze — okno główne potrzebuje go do uruchomienia kopii."""
        return self.password.password() if self.profile_group.checkedId() == 2 else ""


# ------------------------------------------------------------------- pomocnicze


@dataclass
class Volume:
    """Nośnik widziany przez system, opisany tak, by dało się go ocenić."""

    root: str
    name: str
    filesystem: str
    free: int
    total: int
    removable: bool
    system: bool

    def describe(self) -> str:
        """Dwa wiersze: czym jest nośnik i czy się nadaje."""
        title = f"{self.root}  {self.name}".rstrip()
        details = [tr("wolne {free} z {total}").format(
            free=human_size(self.free), total=human_size(self.total)
        )]
        if self.filesystem:
            details.append(self.filesystem)
        if self.system:
            details.append(tr("dysk systemowy"))
        return title + "\n" + "  •  ".join(details)


def detect_volumes() -> list[Volume]:
    """Podłączone nośniki, od najlepszego kandydata na kopię.

    Kolejność ustala :func:`rank_volumes`: kopia obok oryginału nie chroni przed
    awarią dysku, więc dysk systemowy trafia na koniec. Napędy sieciowe
    i optyczne pomijamy.
    """
    volumes: list[Volume] = []
    for storage in QStorageInfo.mountedVolumes():
        if not storage.isValid() or not storage.isReady() or storage.isReadOnly():
            continue
        root = storage.rootPath()
        kind = drive_kind(root)
        if kind in {DRIVE_NETWORK, DRIVE_OPTICAL}:
            continue
        if storage.bytesTotal() <= 0:
            continue
        volumes.append(
            Volume(
                root=root,
                name=storage.name(),
                filesystem=bytes(storage.fileSystemType()).decode("ascii", "replace").upper(),
                free=storage.bytesAvailable(),
                total=storage.bytesTotal(),
                removable=kind == "removable",
                system=is_system_drive(root),
            )
        )
    return rank_volumes(volumes)


def rank_volumes(volumes: list[Volume]) -> list[Volume]:
    """Najpierw nośniki spoza dysku systemowego, wśród nich te z większym zapasem miejsca."""
    return sorted(volumes, key=lambda v: (v.system, -v.free))


def _nearest_existing(path: str) -> str:
    """Najbliższy istniejący katalog na drodze do ``path`` (sam ``path``, gdy istnieje)."""
    candidate = Path(path)
    for folder in (candidate, *candidate.parents):
        if folder.is_dir():
            return str(folder)
    return path


def _personal_folders() -> list[str]:
    """Foldery osobiste użytkownika, które faktycznie istnieją."""
    wanted = (
        QStandardPaths.StandardLocation.DocumentsLocation,
        QStandardPaths.StandardLocation.PicturesLocation,
        QStandardPaths.StandardLocation.DesktopLocation,
    )
    found = []
    for location in wanted:
        path = QStandardPaths.writableLocation(location)
        # Qt podaje ukośniki „/”; w Windows użytkownik zna ścieżki z „\”
        path = os.path.normpath(path) if path else ""
        if path and Path(path).is_dir() and path not in found:
            found.append(path)
    return found


def _inside(candidate: str, folder: str) -> bool:
    """Czy ``candidate`` leży w ``folder`` — bez rzucania wyjątkiem na dziwnych ścieżkach."""
    try:
        return os.path.commonpath([Path(candidate).resolve(), Path(folder).resolve()]) == str(
            Path(folder).resolve()
        )
    except (OSError, ValueError):
        return False
