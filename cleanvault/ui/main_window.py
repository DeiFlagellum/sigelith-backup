"""Główne okno aplikacji.

Układ: stała nawigacja boczna + przełączane ekrany. Wersja 1.x upychała
wszystko w jednej zakładce (tryb, szyfrowanie, ścieżki, szablony, śledzone
pliki i reguły jedno pod drugim), przez co okno wymagało przewijania,
a żadna kontrolka nie miała opisu ani podpowiedzi.

Zasady przyjęte w tym pliku:

* nic, co dotyka dysku, nie wykonuje się w wątku GUI — patrz :mod:`.workers`;
* każda operacja ma tryb podglądu, więc użytkownik widzi skutki przed zapisem;
* każda opcja ma tooltip i zdanie wyjaśniające, co realnie zmienia;
* komunikaty mówią, co zrobić dalej, a nie tylko że „wystąpił błąd".
"""

from __future__ import annotations

import contextlib
import itertools
import time
from collections.abc import Callable
from dataclasses import replace
from pathlib import Path
from typing import ClassVar

from PySide6.QtCore import QEventLoop, QObject, Qt, QTime, QTimer, QUrl, Signal
from PySide6.QtGui import QColor, QDesktopServices, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QColorDialog,
    QComboBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSpinBox,
    QStackedWidget,
    QStatusBar,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

from .. import (
    __app_name__,
    __publisher__,
    __source__,
    __version__,
    autostart,
    beat,
    crypto,
    engine,
    evidence,
    i18n,
    offsite,
    paths,
    scheduler,
    secrets_store,
    sigelith,
)
from ..engine import BackupConfig, human_size
from ..i18n import mark, plural, tr
from ..live import plan_live_run
from ..log import bridge, get_logger
from ..paths import data_dir, is_admin, log_dir, resource_path
from ..s3 import S3Client, S3Target
from ..snapshot import Manifest, ManifestSummary, SourceRoot
from ..state import DEFAULT_EXCLUDES, StateStore, Template
from . import cloud, icons, qtlang
from .background import MSG_SHOW, SchedulerService, Tray
from .browser import BrowserPage
from .evidence_dialog import EvidenceDialog
from .legal import LegalDialog, PrivacyDialog
from .template_dialog import TemplateDialog
from .theme import build_stylesheet, effective_accent, palette_for
from .widgets import (
    Card,
    FlowLayout,
    Hint,
    PasswordField,
    PathPicker,
    SourceList,
    StatTile,
    button,
    checkbox,
    field_help,
    horizontal_line,
    page_title,
)
from .wizard import SetupWizard, WelcomeDialog
from .workers import EngineWorker, ProgressTracker

log = get_logger("ui")

#: Jak długo przy zamykaniu okna czekamy, aż przerwana kopia zapisze spis
#: treści. Manifest dużej kopii na wolnym dysku USB zapisuje się dłużej niż
#: kilka sekund — ubicie procesu w trakcie to utrata stanu przebiegu.
CLOSE_WAIT_SECONDS = 300

#: Ile czekamy na utrwalenie stanu kopii, gdy Windows się wyłącza. Dzięki
#: punktom kontrolnym to zwykle 1–2 sekundy; dłużej system i tak nie poczeka.
SESSION_END_WAIT_SECONDS = 25

#: Opóźnienie odczytu stanu katalogu docelowego po zmianie ścieżki. Pole
#: zmienia się przy każdym wciśniętym klawiszu.
DESTINATION_DEBOUNCE_MS = 350


class LogRelay(QObject):
    """Most między logowaniem a widgetem — sygnał bezpiecznie przekracza wątki."""

    message = Signal(str, int)


class OperationPanel(QWidget):
    """Wspólny panel postępu: etap, bieżący plik, pasek, prędkość, anulowanie."""

    cancel_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.stage_label = QLabel(tr("Gotowe do pracy."))
        self.stage_label.setObjectName("CardTitle")

        self.file_label = QLabel("")
        self.file_label.setObjectName("FieldHelp")
        self.file_label.setWordWrap(True)

        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setValue(0)

        row = QHBoxLayout()
        self.stats_label = QLabel("")
        self.stats_label.setObjectName("FieldHelp")
        self.cancel_btn = button(tr("Przerwij"), tr("Zatrzymuje operację. Pliki już zapisane pozostają nienaruszone."), object_name="Danger")
        self.cancel_btn.clicked.connect(self.cancel_requested.emit)
        row.addWidget(self.stats_label, 1)
        row.addWidget(self.cancel_btn)

        layout.addWidget(self.stage_label)
        layout.addWidget(self.file_label)
        layout.addWidget(self.bar)
        layout.addLayout(row)
        self.set_busy(False)

    def set_busy(self, busy: bool) -> None:
        self.bar.setVisible(busy)
        self.cancel_btn.setVisible(busy)
        self.file_label.setVisible(busy)
        self.stats_label.setVisible(busy)
        if not busy:
            self.bar.setValue(0)

    def set_stage(self, text: str) -> None:
        self.stage_label.setText(text)

    def set_file(self, name: str, index: int, total: int) -> None:
        self.file_label.setText(f"[{index}/{total}] {name}" if total else name)

    def set_progress(self, percent: int, stats: str) -> None:
        self.bar.setValue(percent)
        self.stats_label.setText(stats)


class MainWindow(QMainWindow):
    PAGES: ClassVar[list[tuple[str, str, str]]] = [
        # teksty powstają przy imporcie, więc tłumaczy je dopiero ``tr`` przy budowie menu
        ("archive", mark("Kopia zapasowa"), mark("Utwórz lub zaktualizuj kopię wybranych folderów")),
        ("arrow-counterclockwise", mark("Przywracanie"), mark("Odtwórz pliki z istniejącej kopii")),
        ("folder2-open", mark("Przeglądanie"), mark("Pliki i wersje wprost z kopii — bez przywracania")),
        ("bookmarks", mark("Szablony"), mark("Zapisane konfiguracje do ponownego użycia")),
        ("gear", mark("Ustawienia"), mark("Wygląd, wykluczenia i magazyn haseł")),
        ("journal-text", mark("Dziennik"), mark("Przebieg operacji i diagnostyka")),
        ("info-circle", mark("O programie"), mark("Wersja, licencja i użyta kryptografia")),
    ]
    PAGE_BACKUP, PAGE_RESTORE, PAGE_BROWSE, PAGE_TEMPLATES, PAGE_SETTINGS, PAGE_LOG, PAGE_ABOUT = range(7)

    def __init__(self, store: StateStore | None = None, background: bool = False) -> None:
        super().__init__()
        #: start z parametrem --background: okno ukryte, działa harmonogram
        self.started_in_background = background
        #: prawdziwe zakończenie programu (z menu w zasobniku), a nie ukrycie okna
        self._quitting = False
        #: bieżąca operacja uruchomiona przez harmonogram — bez okien dialogowych
        self._unattended = False
        #: id szablonu „na bieżąco”, którego kopia właśnie trwa (dla ChangeTracker)
        self._live_run: str | None = None
        self.tray: Tray | None = None
        # Start programu wczytuje stan wcześniej (potrzebuje języka przed
        # zbudowaniem okna) i przekazuje go tutaj — jeden odczyt zamiast dwóch.
        self.store = store if store is not None else StateStore()
        self.worker: EngineWorker | None = None
        self.tracker: ProgressTracker | None = None
        self.current_plan: engine.BackupPlan | None = None
        self.selected_template_id: str | None = None
        #: krok do wykonania po zakończeniu bieżącego wątku roboczego
        self._after_worker: Callable[[], None] | None = None
        self._closing = False
        self._dest_timer = QTimer(self)
        self._dest_timer.setSingleShot(True)
        self._dest_timer.setInterval(DESTINATION_DEBOUNCE_MS)
        self._dest_timer.timeout.connect(self._inspect_destination_now)
        app = QApplication.instance()
        if app is not None and hasattr(app, "commitDataRequest"):
            app.commitDataRequest.connect(self._on_session_ending)

        self.setWindowTitle(f"{__app_name__} {__version__}")
        self.setMinimumSize(1060, 720)
        self.resize(1180, 820)
        icon_path = resource_path("assets", "icon.png")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self._build_ui()
        self._apply_theme()
        self._connect_logging()
        self._setup_background()
        self._refresh_templates()
        self._update_backup_readiness()

    # ------------------------------------------------------------------ szkielet

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_sidebar())

        content = QVBoxLayout()
        content.setContentsMargins(0, 0, 0, 0)
        content.setSpacing(0)
        if is_admin():
            self.admin_banner = Hint(
                tr("Program działa z uprawnieniami administratora. Nie są mu potrzebne — kopia "
                   "i przywracanie działają bez nich, a pliki zapisane przez administratora "
                   "mogą później nie dać się zmienić ze zwykłego konta."),
                icon="exclamation-triangle",
            )
            self.admin_banner.setObjectName("AdminBanner")
            content.addWidget(self.admin_banner)

        self.stack = QStackedWidget()
        self.stack.addWidget(self._wrap_scroll(self._build_backup_page()))
        self.stack.addWidget(self._wrap_scroll(self._build_restore_page()))
        if getattr(self, "browser", None) is not None:
            self.browser.shutdown()  # przebudowa okna po zmianie języka
        self.browser = BrowserPage()
        self.stack.addWidget(self._wrap_scroll(self.browser))
        self.stack.addWidget(self._wrap_scroll(self._build_templates_page()))
        self.stack.addWidget(self._wrap_scroll(self._build_settings_page()))
        self.stack.addWidget(self._wrap_scroll(self._build_log_page()))
        self.stack.addWidget(self._wrap_scroll(self._build_about_page()))
        content.addWidget(self.stack, 1)
        root.addLayout(content, 1)

        status = QStatusBar()
        status.setObjectName("StatusBar")
        self.setStatusBar(status)
        self._set_status(tr("Gotowe. Wybierz foldery do kopii."))

    def _build_sidebar(self) -> QWidget:
        side = QWidget()
        side.setObjectName("Sidebar")
        side.setFixedWidth(228)
        layout = QVBoxLayout(side)
        layout.setContentsMargins(14, 18, 14, 16)
        layout.setSpacing(5)

        title = QLabel(__app_name__)
        title.setObjectName("SidebarTitle")
        subtitle = QLabel(tr("wersja {version}").format(version=__version__))
        subtitle.setObjectName("SidebarSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(14)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        for index, (icon_name, name, tip) in enumerate(self.PAGES):
            btn = QPushButton(f"  {tr(name)}")
            btn.setObjectName("NavButton")
            icons.set_icon(btn, icon_name)
            btn.setCheckable(True)
            btn.setToolTip(tr(tip))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _checked, i=index: self._go_to(i))
            self.nav_group.addButton(btn, index)
            layout.addWidget(btn)
        self.nav_group.button(0).setChecked(True)

        layout.addStretch(1)
        self.sidebar_note = QLabel("")
        self.sidebar_note.setObjectName("FieldHelp")
        self.sidebar_note.setWordWrap(True)
        layout.addWidget(self.sidebar_note)
        self._refresh_sidebar_note()
        return side

    @staticmethod
    def _wrap_scroll(page: QWidget) -> QScrollArea:
        area = QScrollArea()
        area.setWidgetResizable(True)
        area.setWidget(page)
        return area

    def _go_to(self, index: int) -> None:
        self.stack.setCurrentIndex(index)
        self.nav_group.button(index).setChecked(True)
        if index == self.PAGE_TEMPLATES:
            self._refresh_templates()
        elif index == self.PAGE_BROWSE and not self.browser.picker.path():
            # od razu ta kopia, o której właśnie mowa: z przywracania albo z formularza kopii
            for candidate in (self.restore_src.path(), self.dest_picker.path()):
                if candidate and Path(candidate).is_dir():
                    self.browser.open_backup(candidate)
                    break

    def _set_status(self, text: str) -> None:
        self.statusBar().showMessage(text)

    def _refresh_sidebar_note(self) -> None:
        count = len(self.store.templates())
        kdf = "Argon2id" if crypto.ARGON2_AVAILABLE else "PBKDF2-SHA256"
        self.sidebar_note.setText(
            tr("Szablony: {count}\nSzyfrowanie: AES-256-GCM\nKlucz: {kdf}").format(count=count, kdf=kdf)
        )

    # -------------------------------------------------------------- ekran kopii

    def _build_backup_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(16)

        layout.addWidget(
            page_title(
                tr("Kopia zapasowa"),
                tr("Kopiowane są wyłącznie pliki nowe i zmienione od ostatniego przebiegu."),
            )
        )
        layout.addWidget(
            Hint(
                tr("Pierwszy przebieg kopiuje wszystko i trwa najdłużej. Kolejne porównują "
                   "rozmiar i datę modyfikacji, więc zwykle kończą się w kilka sekund.")
            )
        )
        wizard_row = QHBoxLayout()
        wizard_row.addWidget(self._wizard_button())
        wizard_row.addStretch(1)
        layout.addLayout(wizard_row)

        # --- źródła ---
        sources_card = Card(
            tr("Co kopiujemy"),
            tr("Wskaż foldery objęte kopią. Podfoldery są uwzględniane automatycznie."),
        )
        self.source_list = SourceList()
        self.source_list.changed.connect(self._update_backup_readiness)
        sources_card.add(self.source_list)
        row = QHBoxLayout()
        row.addWidget(button(tr("Dodaj folder"), tr("Wybierz kolejny folder do kopii"), self._add_source, icon="folder-plus"))
        row.addWidget(
            button(
                tr("Usuń zaznaczone"),
                tr("Usuwa pozycję z listy. Nie kasuje żadnych plików."),
                self.source_list.remove_selected,
                icon="dash-circle",
            )
        )
        row.addStretch(1)
        sources_card.add_layout(row)
        sources_card.add(
            field_help(tr("Możesz też przeciągnąć foldery z Eksploratora Windows wprost na listę."))
        )
        self.sigelith_cb = checkbox(
            tr("Chroń dowody Sigelith"),
            tr("Kopia obejmie folder danych Sigelith Desktop (historię stempli), a każdy oznakowany\n"
               "dokument trafi — dokładnie w tej postaci, którą oznakowano — do magazynu dowodów\n"
               "w katalogu kopii, razem z plikiem .beatproof. Starych wersji magazyn nie dotyczy:\n"
               "retencja go nie sprząta."),
        )
        sources_card.add(self.sigelith_cb)
        self.sigelith_status = field_help("")
        sources_card.add(self.sigelith_status)
        self._refresh_sigelith_status()
        layout.addWidget(sources_card)

        # --- cel ---
        dest_card = Card(tr("Gdzie zapisujemy"), tr("Folder docelowy kopii — najlepiej na innym dysku fizycznym."))
        self.dest_picker = PathPicker(
            placeholder=tr("np. E:\\Kopie zapasowe"),
            dialog_title=tr("Wybierz katalog docelowy kopii"),
            tooltip=tr("Katalog, w którym powstanie kopia. Nie może leżeć wewnątrz folderu źródłowego."),
        )
        self.dest_picker.changed.connect(self._on_destination_changed)
        dest_card.add(self.dest_picker)
        self.dest_info = field_help(tr("Wybierz katalog, aby zobaczyć dostępne miejsce."))
        dest_card.add(self.dest_info)
        layout.addWidget(dest_card)

        # --- struktura ---
        struct_card = Card(tr("Układ kopii"), tr("Decyduje, czy zachowujemy historię wersji."))
        self.structure_dated = QRadioButton(tr("Wersje z datą (zalecane)"))
        self.structure_dated.setChecked(True)
        self.structure_dated.setToolTip(
            tr("Każdy przebieg tworzy osobny folder z datą i godziną.\n"
               "Pliki niezmienione są podpinane twardym dowiązaniem, więc historia\n"
               "zajmuje tyle miejsca, ile realnie się zmieniło.")
        )
        self.structure_mirror = QRadioButton(tr("Kopia lustrzana"))
        self.structure_mirror.setToolTip(
            tr("Jeden folder utrzymywany w zgodzie ze źródłem. Brak historii wersji,\n"
               "za to najprostsza struktura i najmniejsze zużycie miejsca.")
        )
        self.structure_dated.toggled.connect(self._on_structure_changed)
        struct_card.add(self.structure_dated)
        struct_card.add(
            field_help(tr("Każdy folder z datą jest kompletny — przywracanie nie wymaga sklejania wersji."))
        )
        struct_card.add(self.structure_mirror)
        struct_card.add(
            field_help(tr("Odpowiednik synchronizacji folderu. Wcześniejsze wersje plików nie są zachowywane."))
        )

        retention_row = QHBoxLayout()
        self.retention_mode = QComboBox()
        self.retention_mode.addItem(tr("wszystkie wersje"), "all")
        self.retention_mode.addItem(tr("ostatnie wersje"), "last")
        self.retention_mode.addItem(tr("kalendarz: dni, tygodnie, miesiące"), "gfs")
        self.retention_mode.setToolTip(
            tr("Kalendarz zostawia najnowszą wersję z każdego z ostatnich dni, tygodni\n"
               "i miesięcy — gęsto dla świeżych zmian, rzadko dla dawnych. Nadmiar jest\n"
               "kasowany po udanym przebiegu; wersje niedokończone nigdy.")
        )
        self.retention_spin = QSpinBox()
        self.retention_spin.setRange(1, 999)
        self.retention_spin.setValue(10)
        self.retention_spin.setSuffix(tr(" wersji"))
        self.gfs_daily_spin = QSpinBox()
        self.gfs_daily_spin.setRange(0, 366)
        self.gfs_daily_spin.setValue(7)
        self.gfs_daily_spin.setSuffix(tr(" dni"))
        self.gfs_weekly_spin = QSpinBox()
        self.gfs_weekly_spin.setRange(0, 260)
        self.gfs_weekly_spin.setValue(4)
        self.gfs_weekly_spin.setSuffix(tr(" tyg."))
        self.gfs_monthly_spin = QSpinBox()
        self.gfs_monthly_spin.setRange(0, 600)
        self.gfs_monthly_spin.setValue(12)
        self.gfs_monthly_spin.setSuffix(tr(" mies."))
        self.retention_spin.setToolTip(tr("Ile ostatnich wersji zachować. Starsze są kasowane po udanym przebiegu."))
        self.gfs_daily_spin.setToolTip(tr("Z ilu ostatnich dni zachować po jednej, najnowszej wersji."))
        self.gfs_weekly_spin.setToolTip(tr("Z ilu ostatnich tygodni zachować po jednej, najnowszej wersji."))
        self.gfs_monthly_spin.setToolTip(tr("Z ilu ostatnich miesięcy zachować po jednej, najnowszej wersji."))
        retention_row.addWidget(QLabel(tr("Zachowuj:")))
        retention_row.addWidget(self.retention_mode)
        for spin in (self.retention_spin, self.gfs_daily_spin, self.gfs_weekly_spin, self.gfs_monthly_spin):
            retention_row.addWidget(spin)
        retention_row.addStretch(1)
        struct_card.add_layout(retention_row)
        self.retention_mode.currentIndexChanged.connect(lambda _i: self._retention_mode_changed())
        self._retention_mode_changed()

        target_row = QHBoxLayout()
        self.version_combo = QComboBox()
        self.version_combo.setToolTip(
            tr("Nowa wersja z datą — kopia do nowego folderu.\n"
               "Wybrana istniejąca wersja — dogrywa do niej tylko brakujące i zmienione\n"
               "pliki, a pliki różniące się od źródła nadpisuje. Tak dokończysz przerwaną\n"
               "kopię albo uzupełnisz ją o dane, które powstały w trakcie jej wykonywania.")
        )
        self.version_combo.addItem(tr("Nowa wersja z datą"), "")
        target_row.addWidget(QLabel(tr("Zapisz do:")))
        target_row.addWidget(self.version_combo, 1)
        struct_card.add_layout(target_row)
        struct_card.add(
            field_help(
                tr("Uzupełnienie istniejącej wersji nie kopiuje ponownie tego, co już w niej jest — "
                   "dokończysz przerwaną kopię bez tworzenia kolejnej pełnej wersji.")
            )
        )

        self.stamp_updates_cb = checkbox(
            tr("Dopisuj do nazwy katalogu datę ostatniego uzupełnienia"),
            tr("Po uzupełnieniu istniejącej wersji jej katalog nazywa się np.\n"
               "  2026-09-17_@687--2026-09-24_@921\n"
               "czyli: data utworzenia kopii i data ostatniego uzupełnienia.\n\n"
               "Data utworzenia zostaje z przodu, więc katalogi nadal układają się\n"
               "chronologicznie. Widać to w Eksploratorze bez uruchamiania programu."),
            checked=True,
        )
        struct_card.add(self.stamp_updates_cb)
        struct_card.add(
            field_help(
                tr("Czas w nazwie to BeatTime — 1000 beatów na dobę, kotwica w UTC, ten sam "
                   "moment na całym świecie. Data jest datą UTC, więc zgadza się z zegarem.")
            )
        )

        self.delete_removed_cb = checkbox(
            tr("Usuwaj z kopii pliki skasowane w źródle"),
            tr("Domyślnie wyłączone. Przy włączonej opcji skasowanie pliku w źródle\n"
               "usuwa też jego jedyną kopię zapasową — operacja nieodwracalna."),
        )
        self.delete_removed_cb.setEnabled(False)
        struct_card.add(self.delete_removed_cb)
        layout.addWidget(struct_card)

        # --- ochrona ---
        crypto_card = Card(tr("Ochrona danych"), tr("Szyfrowanie i kontrola poprawności zapisu."))
        self.encrypt_cb = checkbox(
            tr("Szyfruj kopię (AES-256-GCM)"),
            tr("Każdy plik trafia do kopii jako zaszyfrowany kontener .cvlt.\n"
               "Klucz powstaje z hasła przez Argon2id."),
        )
        self.encrypt_cb.toggled.connect(self._on_encrypt_toggled)
        crypto_card.add(self.encrypt_cb)

        self.password_field = PasswordField(tr("Hasło do kopii"))
        self.password_field.changed.connect(lambda _: self._update_backup_readiness())
        self.password_field.setEnabled(False)
        crypto_card.add(self.password_field)

        self.password_confirm = QLineEdit()
        self.password_confirm.setPlaceholderText(tr("Powtórz hasło"))
        self.password_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_confirm.setEnabled(False)
        self.password_confirm.textChanged.connect(lambda _: self._update_backup_readiness())
        self.password_confirm.setToolTip(tr("Zabezpieczenie przed literówką — hasła nie da się odzyskać."))
        crypto_card.add(self.password_confirm)

        self.password_warning = field_help("")
        crypto_card.add(self.password_warning)

        self.remember_cb = checkbox(
            tr("Zapamiętaj hasło w Menedżerze poświadczeń Windows"),
            tr("Hasło trafia do magazynu systemowego powiązanego z Twoim kontem.\n"
               "Nigdy nie jest zapisywane w plikach programu."),
        )
        self.remember_cb.setEnabled(False)
        crypto_card.add(self.remember_cb)
        crypto_card.add(field_help(tr("Magazyn haseł: {backend}").format(backend=secrets_store.describe())))

        crypto_card.add(horizontal_line())
        self.verify_cb = checkbox(
            tr("Weryfikuj natychmiast po zapisie (spowalnia kopię)"),
            tr("Każdy plik jest czytany ponownie zaraz po zapisaniu. Dane pochodzą wtedy\n"
               "zwykle z pamięci podręcznej systemu, więc niewiele mówi to o nośniku,\n"
               "a wydłuża kopię nawet dwukrotnie.\n\n"
               "Skuteczniejsza jest weryfikacja odroczona: ekran „Przywracanie” →\n"
               "„Sprawdź kopię”, najlepiej po ponownym podłączeniu dysku."),
            checked=bool(self.store.setting("verify_after_write", True)),
        )
        crypto_card.add(self.verify_cb)
        self.thorough_cb = checkbox(
            tr("Tryb dokładny — licz sumę kontrolną każdego pliku"),
            tr("Wolniejszy, ale wykrywa zmiany, które nie zmieniły rozmiaru ani daty\n"
               "(np. po przywróceniu pliku z innego nośnika)."),
        )
        crypto_card.add(self.thorough_cb)
        self.delta_cb = checkbox(
            tr("Duże pliki zapisuj różnicowo (od 256 MB)"),
            tr("Kolejna wersja dużego pliku — maszyny wirtualnej, skrzynki pocztowej, bazy —\n"
               "zapisuje tylko zmienione fragmenty zamiast całego pliku. W kopii taki plik\n"
               "leży jako przepis + fragmenty; złoży go program albo skrypt ratunkowy."),
            checked=True,
        )
        crypto_card.add(self.delta_cb)
        self.timestamp_cb = checkbox(
            tr("Znakuj wersję czasem Sigelith"),
            tr("Dowód, że kopia w tym kształcie istniała danego dnia (podpis Ed25519, kotwica\n"
               "w Bitcoinie). Do sigelith.org trafia wyłącznie suma kontrolna spisu wersji —\n"
               "żadne nazwy plików ani ich treść."),
        )
        crypto_card.add(self.timestamp_cb)

        catchup_row = QHBoxLayout()
        self.catchup_spin = QSpinBox()
        self.catchup_spin.setRange(0, 5)
        self.catchup_spin.setValue(1)
        self.catchup_spin.setSuffix(tr(" ×"))
        self.catchup_spin.setSpecialValueText(tr("wyłączona"))
        self.catchup_spin.setToolTip(
            tr("Po zakończeniu kopii program ponownie skanuje źródło i dogrywa do tej samej\n"
               "wersji pliki, które w międzyczasie powstały lub się zmieniły.\n"
               "Przydatne, gdy pracujesz na danych w trakcie wielogodzinnej kopii.\n"
               "Plik zmieniony w trakcie własnego kopiowania nigdy nie jest uznawany za zapisany.")
        )
        catchup_row.addWidget(QLabel(tr("Dogrywka zmian z czasu kopii:")))
        catchup_row.addWidget(self.catchup_spin)
        catchup_row.addSpacing(24)
        self.workers_spin = QSpinBox()
        self.workers_spin.setRange(0, 64)
        self.workers_spin.setValue(0)
        self.workers_spin.setSpecialValueText(tr("automatycznie"))
        self.workers_spin.setToolTip(
            tr("Ile plików kopia przetwarza jednocześnie. Przy setkach tysięcy małych plików\n"
               "czas kopii to głównie opóźnienia na każdy plik (otwarcie, skanowanie\n"
               "antywirusowe, zapis na nośnik), a nie przesył danych — praca równoległa\n"
               "skraca go kilkukrotnie.\n\n"
               "„automatycznie” dobiera liczbę do procesora (do 32). Na wolnym dysku\n"
               "talerzowym mniejsza wartość (2–4) bywa szybsza.")
        )
        catchup_row.addWidget(QLabel(tr("Równoległe operacje:")))
        catchup_row.addWidget(self.workers_spin)
        catchup_row.addStretch(1)
        crypto_card.add_layout(catchup_row)
        layout.addWidget(crypto_card)

        # --- wykluczenia ---
        excl_card = Card(tr("Wykluczenia"), tr("Wzorce plików i folderów pomijanych w kopii — po jednym w wierszu."))
        self.excludes_edit = QPlainTextEdit("\n".join(self.store.setting("default_excludes", DEFAULT_EXCLUDES)))
        self.excludes_edit.setFixedHeight(118)
        self.excludes_edit.setToolTip(
            tr("Obsługiwane są wzorce w stylu Windows:\n"
               "  *.tmp          — wszystkie pliki tymczasowe\n"
               "  Thumbs.db      — konkretna nazwa\n"
               "  node_modules/* — cały folder wraz z zawartością")
        )
        excl_card.add(self.excludes_edit)
        excl_row = QHBoxLayout()
        excl_row.addWidget(
            button(tr("Przywróć domyślne"), tr("Wstawia zalecaną listę wykluczeń"), lambda: self.excludes_edit.setPlainText("\n".join(DEFAULT_EXCLUDES)))
        )
        excl_row.addStretch(1)
        excl_card.add_layout(excl_row)
        layout.addWidget(excl_card)

        # --- podsumowanie planu ---
        self.plan_card = Card(tr("Podgląd zmian"), tr("Co dokładnie zostanie zapisane przy najbliższym przebiegu."))
        tiles = QHBoxLayout()
        tiles.setSpacing(10)
        self.tile_new = StatTile(tr("nowych plików"), "—", tr("Pliki, których jeszcze nie ma w kopii"))
        self.tile_changed = StatTile(tr("zmienionych"), "—", tr("Pliki zmienione od ostatniego przebiegu"))
        self.tile_unchanged = StatTile(tr("bez zmian"), "—", tr("Pliki pominięte — kopia jest aktualna"))
        self.tile_size = StatTile(tr("do zapisania"), "—", tr("Łączny rozmiar danych do przesłania"))
        for tile in (self.tile_new, self.tile_changed, self.tile_unchanged, self.tile_size):
            tiles.addWidget(tile)
        self.plan_card.add_layout(tiles)
        self.plan_details = field_help(tr("Kliknij „Podgląd zmian”, aby sprawdzić plan bez zapisywania czegokolwiek."))
        self.plan_card.add(self.plan_details)
        layout.addWidget(self.plan_card)

        # --- akcje ---
        actions = QHBoxLayout()
        actions.setSpacing(10)
        self.preview_btn = button(
            tr("Podgląd zmian"), tr("Analizuje pliki i pokazuje plan. Nic nie zapisuje."),
            self._preview_backup, icon="search",
        )
        self.run_btn = button(
            tr("Uruchom kopię"), tr("Wykonuje kopię zgodnie z powyższymi ustawieniami"),
            self._start_backup, object_name="Primary", icon="play-fill",
        )
        self.save_template_btn = button(
            tr("Zapisz jako szablon"), tr("Zapamiętuje te ustawienia do ponownego użycia"),
            self._save_as_template, icon="bookmark-plus",
        )
        actions.addWidget(self.preview_btn)
        actions.addWidget(self.run_btn)
        actions.addWidget(self.save_template_btn)
        actions.addStretch(1)
        layout.addLayout(actions)

        self.backup_panel = OperationPanel()
        self.backup_panel.cancel_requested.connect(self._cancel_operation)
        layout.addWidget(self.backup_panel)
        layout.addStretch(1)
        return page

    # ------------------------------------------------------- logika ekranu kopii

    def _add_source(self) -> None:
        chosen = QFileDialog.getExistingDirectory(self, tr("Wybierz folder do kopii"), str(Path.home()))
        if chosen and not self.source_list.add_path(chosen):
            self._set_status(tr("Ten folder jest już na liście."))

    def _on_destination_changed(self, _path: str) -> None:
        self._update_backup_readiness()
        self._dest_timer.start()

    def _inspect_destination_now(self) -> None:
        """Pokazuje stan katalogu docelowego i wypełnia listę wersji.

        Korzysta wyłącznie z małego podsumowania manifestu — wcześniej przy
        każdym wciśniętym klawiszu w polu ścieżki wczytywany był cały manifest,
        który przy dużej kopii waży setki megabajtów i zamrażał okno.
        """
        path = self.dest_picker.path()
        previous = self.version_combo.currentData()
        self.version_combo.blockSignals(True)
        self.version_combo.clear()
        self.version_combo.addItem(tr("Nowa wersja z datą"), "")
        self.version_combo.blockSignals(False)

        if not path or not Path(path).exists():
            self.dest_info.setText(tr("Katalog jeszcze nie istnieje — zostanie utworzony."))
            return
        try:
            info = engine.inspect_destination(path)
        except OSError as exc:
            self.dest_info.setText(tr("Nie można odczytać informacji o dysku: {error}").format(error=exc))
            return

        parts = [
            tr("Wolne miejsce: {free} z {total}").format(
                free=human_size(info.free), total=human_size(info.total)
            )
        ]
        if info.filesystem:
            medium = info.filesystem
            if info.cluster:
                medium += tr(", klaster {size}").format(size=human_size(info.cluster))
            parts.append(medium)
        if info.entry_count:
            when = time.strftime(tr("%d.%m.%Y %H:%M"), time.localtime(info.updated))
            parts.append(
                tr("istniejąca kopia: {count} {files}, ostatnio {when}").format(
                    count=info.entry_count,
                    files=plural(info.entry_count, "plik", "pliki", "plików"),
                    when=when,
                )
            )
        text = " • ".join(parts)
        if not info.hardlinks_likely:
            text += tr(
                "\nUwaga: {filesystem} nie obsługuje twardych dowiązań — każda wersja z datą "
                "zajmuje tyle miejsca co pełna kopia."
            ).format(filesystem=info.filesystem)
        if info.cluster >= 64 * 1024:
            text += tr(
                "\nUwaga: duży klaster ({size}): każdy mały plik zajmuje co najmniej "
                "tyle miejsca. Przy wielu małych plikach kopia zajmie wielokrotnie więcej niż dane."
            ).format(size=human_size(info.cluster))
        pending = [run for run in info.runs if not run.complete]
        if pending:
            text += tr(
                "\nDo uzupełnienia: niedokończone kopie: {count} — możesz je uzupełnić, "
                "wybierając wersję poniżej."
            ).format(count=len(pending))
        self.dest_info.setText(text)

        for run in info.runs:
            labels = ", ".join(run.labels) if run.labels else "—"
            self.version_combo.addItem(
                tr("Uzupełnij: {version} • {labels}").format(
                    version=engine.describe_version(run), labels=labels
                ),
                run.name,
            )
        index = self.version_combo.findData(previous)
        if index > 0:
            self.version_combo.setCurrentIndex(index)

    def _retention_mode_changed(self) -> None:
        mode = self.retention_mode.currentData()
        self.retention_spin.setVisible(mode == "last")
        for spin in (self.gfs_daily_spin, self.gfs_weekly_spin, self.gfs_monthly_spin):
            spin.setVisible(mode == "gfs")

    def _retention_values(self) -> dict[str, int]:
        mode = self.retention_mode.currentData()
        return {
            "retention": self.retention_spin.value() if mode == "last" else 0,
            "gfs_daily": self.gfs_daily_spin.value() if mode == "gfs" else 0,
            "gfs_weekly": self.gfs_weekly_spin.value() if mode == "gfs" else 0,
            "gfs_monthly": self.gfs_monthly_spin.value() if mode == "gfs" else 0,
        }

    def _set_retention(self, retention: int, daily: int, weekly: int, monthly: int) -> None:
        if daily or weekly or monthly:
            mode = "gfs"
            self.gfs_daily_spin.setValue(daily)
            self.gfs_weekly_spin.setValue(weekly)
            self.gfs_monthly_spin.setValue(monthly)
        elif retention:
            mode = "last"
            self.retention_spin.setValue(retention)
        else:
            mode = "all"
        self.retention_mode.setCurrentIndex(max(0, self.retention_mode.findData(mode)))
        self._retention_mode_changed()

    def _on_structure_changed(self, dated: bool) -> None:
        for widget in (
            self.retention_mode, self.retention_spin, self.gfs_daily_spin,
            self.gfs_weekly_spin, self.gfs_monthly_spin,
        ):
            widget.setEnabled(dated)
        self.version_combo.setEnabled(dated)
        self.delete_removed_cb.setEnabled(not dated)
        if dated:
            self.delete_removed_cb.setChecked(False)

    def _on_encrypt_toggled(self, enabled: bool) -> None:
        self.password_field.setEnabled(enabled)
        self.password_confirm.setEnabled(enabled)
        self.remember_cb.setEnabled(enabled and secrets_store.is_available())
        if not enabled:
            self.password_field.clear()
            self.password_confirm.clear()
            self.remember_cb.setChecked(False)
        self._update_backup_readiness()

    def _password_problem(self) -> str | None:
        if not self.encrypt_cb.isChecked():
            return None
        password = self.password_field.password()
        if not password:
            return tr("Podaj hasło — bez niego nie można zaszyfrować kopii.")
        if password != self.password_confirm.text():
            return tr("Hasła w obu polach różnią się.")
        if len(password) < 8:
            return tr("Hasło powinno mieć co najmniej 8 znaków.")
        return None

    def _update_backup_readiness(self) -> None:
        problem = self._password_problem()
        self.password_warning.setText(problem or "")
        self.password_warning.setObjectName("Danger" if problem else "FieldHelp")
        self.password_warning.style().unpolish(self.password_warning)
        self.password_warning.style().polish(self.password_warning)

        ready = bool(self.source_list.paths()) and bool(self.dest_picker.path()) and problem is None
        busy = self.worker is not None and self.worker.isRunning()
        self.run_btn.setEnabled(ready and not busy)
        self.preview_btn.setEnabled(ready and not busy)
        self.save_template_btn.setEnabled(bool(self.source_list.paths()) and bool(self.dest_picker.path()))

        if busy:
            self.run_btn.setToolTip(tr("Trwa inna operacja — poczekaj na jej zakończenie."))
        elif not self.source_list.paths():
            self.run_btn.setToolTip(tr("Dodaj przynajmniej jeden folder źródłowy."))
        elif not self.dest_picker.path():
            self.run_btn.setToolTip(tr("Wskaż katalog docelowy kopii."))
        elif problem:
            self.run_btn.setToolTip(problem)
        else:
            self.run_btn.setToolTip(tr("Wykonuje kopię zgodnie z powyższymi ustawieniami"))

    def _refresh_sigelith_status(self) -> None:
        data_dir = sigelith.find_data_dir()
        if data_dir is None:
            self.sigelith_status.setText(tr("Na tym komputerze nie ma danych Sigelith Desktop."))
            return
        count = len(sigelith.load_stamps(data_dir))
        self.sigelith_status.setText(tr("Sigelith Desktop: {count} {stamps} w folderze {path}.").format(
            count=count, stamps=plural(count, "stempel", "stemple", "stempli"), path=data_dir))

    def _current_config(self) -> BackupConfig:
        excludes = [line.strip() for line in self.excludes_edit.toPlainText().splitlines() if line.strip()]
        return BackupConfig(
            sources=self.source_list.paths(),
            destination=self.dest_picker.path(),
            structure="dated" if self.structure_dated.isChecked() else "mirror",
            encrypt=self.encrypt_cb.isChecked(),
            verify_after_write=self.verify_cb.isChecked(),
            excludes=excludes,
            **self._retention_values(),
            thorough=self.thorough_cb.isChecked(),
            delete_removed=self.delete_removed_cb.isChecked(),
            target_version=(self.version_combo.currentData() or "") if self.structure_dated.isChecked() else "",
            catchup_passes=self.catchup_spin.value(),
            workers=self.workers_spin.value(),
            stamp_updates=self.stamp_updates_cb.isChecked(),
            delta=self.delta_cb.isChecked(),
            timestamp=self.timestamp_cb.isChecked(),
            sigelith=self.sigelith_cb.isChecked(),
        )

    def _preview_backup(self) -> None:
        config = self._current_config()
        self._run_job(
            lambda reporter: engine.plan_backup(config, reporter),
            panel=self.backup_panel,
            on_success=self._show_plan,
            description=tr("podgląd kopii"),
            total_bytes=0,
        )

    def _show_plan(self, plan: engine.BackupPlan) -> None:
        self.current_plan = plan
        new = sum(1 for item in plan.to_copy if item.reason == "nowy")
        changed = sum(1 for item in plan.to_copy if item.reason == "zmieniony")
        missing = sum(1 for item in plan.to_copy if item.reason == "brak w kopii")

        self.tile_new.set_value(str(new))
        self.tile_changed.set_value(str(changed + missing))
        self.tile_unchanged.set_value(str(len(plan.unchanged) + len(plan.adopted)))
        self.tile_size.set_value(human_size(plan.total_bytes))

        parts = [
            tr("Przeskanowano {count} {files}.").format(
                count=plan.scanned, files=plural(plan.scanned, "plik", "pliki", "plików")
            )
        ]
        if plan.resuming and plan.version:
            parts.append(
                tr("Uzupełnianie wersji {version} — pliki już zapisane, które zostaną "
                   "pominięte: {count}.").format(version=plan.version, count=len(plan.adopted))
            )
        if plan.physical_bytes and plan.physical_bytes != plan.total_bytes:
            parts.append(
                tr("Na nośniku docelowym zajmie to ok. {size}.").format(
                    size=human_size(plan.physical_bytes)
                )
            )
        if missing:
            parts.append(
                tr("Pliki, których brakuje w kopii i które zostaną zapisane ponownie: {count}.").format(
                    count=missing
                )
            )
        if plan.removed:
            action = (
                tr("zostaną usunięte z kopii") if plan.config.delete_removed
                else tr("pozostaną w kopii")
            )
            parts.append(
                tr("Pliki skasowane w źródle: {count} — {action}.").format(
                    count=len(plan.removed),
                    action=action,
                )
            )
        if plan.warnings:
            parts.extend(tr(warning) for warning in plan.warnings)
        if not plan.to_copy:
            parts.append(tr("Kopia jest aktualna — nie ma czego zapisywać."))
        self.plan_details.setText(" ".join(parts))
        self._set_status(
            tr("Plan gotowy: {count} {files} do zapisania.").format(
                count=len(plan.to_copy), files=plural(len(plan.to_copy), "plik", "pliki", "plików")
            )
        )

    def _start_backup(self) -> None:
        problem = self._password_problem()
        if problem:
            QMessageBox.warning(self, tr("Sprawdź hasło"), problem)
            return
        config = self._current_config()
        keyring = self._make_keyring(self.password_field.password()) if config.encrypt else None

        if config.delete_removed:
            answer = QMessageBox.question(
                self,
                tr("Potwierdź usuwanie"),
                tr("Włączono usuwanie z kopii plików skasowanych w źródle.\n\n"
                   "Pliki usunięte w źródle stracą swoją jedyną kopię zapasową. "
                   "Czy na pewno kontynuować?"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if answer != QMessageBox.StandardButton.Yes:
                return

        if config.encrypt and self.remember_cb.isChecked():
            self._pending_password = self.password_field.password()

        self._launch_backup(
            config, keyring, self.backup_panel, self._backup_finished, tr("kopia zapasowa")
        )

    def _launch_backup(
        self,
        config: BackupConfig,
        keyring,
        panel,
        on_success,
        description: str,
        unattended: bool = False,
        live: bool = False,
    ) -> None:
        """Uruchamia kopię, najpierw sprawdzając, czy nie ma czego dokończyć.

        Tu leżał sedno problemu z przerwaną kopią: program zawsze zaczynał nową,
        pełną wersję — nawet gdy użytkownik chciał tylko dokończyć poprzednią,
        a na nową zabrakło miejsca. Teraz, jeśli najnowsza wersja tych samych
        folderów jest niedokończona (albo jej stanu nie znamy), użytkownik
        dostaje wybór, zanim cokolwiek zostanie zapisane.
        """
        self._unattended = unattended
        if config.structure != "dated" or config.target_version:
            self._start_backup_job(config, keyring, panel, on_success, description)
            return

        def inspect(reporter):
            reporter.stage(tr("Sprawdzam, czy w katalogu docelowym jest kopia do dokończenia…"))
            return engine.inspect_destination(config.destination, load_manifest=True)

        def inspected(info: engine.DestinationInfo) -> None:
            if live:
                # „Na bieżąco”: do dzisiejszej wersji; opieczętowanej nie ruszamy, a wczorajszą
                # przy włączonych znacznikach zamykamy pieczęcią (cleanvault/live.py).
                plan = plan_live_run(info.runs_for(engine.source_labels(config.sources)),
                                     config.destination, time.time(), config.timestamp)
                adjusted = replace(config, target_version=plan.target_version, timestamp=plan.seal,
                                   stamp_updates=False, catchup_passes=0)
                self._after_worker = lambda: self._start_backup_job(
                    adjusted, keyring, panel, on_success, description
                )
                return
            self._after_worker = lambda: self._continue_launch(
                config, keyring, panel, on_success, description, info
            )

        self._run_job(
            inspect, panel=panel, on_success=inspected, description=tr("sprawdzanie kopii"), total_bytes=0
        )

    def _continue_launch(self, config, keyring, panel, on_success, description, info) -> None:
        suggestion = engine.suggest_continuation(info, engine.source_labels(config.sources))
        if suggestion is not None:
            # Bez człowieka przy komputerze wybieramy bezpiecznie: uzupełnienie
            # niedokończonej wersji nie kopiuje ponownie tego, co już zapisane.
            choice = True if self._unattended else self._ask_continuation(suggestion, info)
            if choice is None:
                panel.set_stage(tr("Anulowano przed rozpoczęciem kopii."))
                self._set_status(tr("Kopia nie została uruchomiona."))
                return
            if choice:
                config = replace(config, target_version=suggestion.name)
        self._start_backup_job(config, keyring, panel, on_success, description)

    def _ask_continuation(self, run, info) -> bool | None:
        """``True`` = uzupełnij wersję, ``False`` = nowa wersja, ``None`` = anuluj."""
        described = engine.describe_version(run)
        if run.known:
            intro = tr("W katalogu docelowym jest niedokończona kopia tych samych folderów:")
            detail = tr("Można ją dokończyć — zostaną dograne tylko brakujące i zmienione pliki.")
        else:
            intro = tr(
                "W katalogu docelowym jest kopia tych samych folderów zapisana starszą wersją programu:"
            )
            detail = tr(
                "Program nie wie, czy ta kopia została dokończona. Uzupełnienie jej dogra tylko "
                "brakujące i zmienione pliki, a tego, co już jest zapisane, nie kopiuje ponownie."
            )
        cost = tr("Nowa wersja z datą to kopia od początku do osobnego folderu")
        if not info.hardlinks_likely:
            cost += tr(
                " — a ponieważ {filesystem} nie obsługuje twardych dowiązań, zapisze ponownie "
                "wszystkie pliki i zajmie tyle miejsca co cała kopia"
            ).format(filesystem=info.filesystem)
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Question)
        box.setWindowTitle(tr("Kopia do dokończenia"))
        box.setText(f"{intro}\n\n    {described}\n\n{detail}\n\n{cost}.")
        resume_btn = box.addButton(tr("Uzupełnij tę wersję"), QMessageBox.ButtonRole.AcceptRole)
        new_btn = box.addButton(tr("Utwórz nową wersję"), QMessageBox.ButtonRole.ActionRole)
        box.addButton(tr("Anuluj"), QMessageBox.ButtonRole.RejectRole)
        box.setDefaultButton(resume_btn)
        box.exec()
        clicked = box.clickedButton()
        if clicked is resume_btn:
            return True
        if clicked is new_btn:
            return False
        return None

    def _remember_error(self, error: object) -> None:
        self._last_error = error

    def _handle_mass_change(self, panel: OperationPanel, error: engine.MassChangeDetected) -> None:
        """Kopia wstrzymana przed zapisem, bo w źródle zmieniło się podejrzanie dużo.

        Przy kopii planowej nikt nie może tego potwierdzić, więc kopia czeka na
        człowieka; przy ręcznej pytamy wprost. Wcześniejsze wersje kopii są w obu
        przypadkach nietknięte — nic jeszcze nie zostało zapisane.
        """
        panel.set_stage(tr("Kopia wstrzymana — w źródle zmieniło się podejrzanie dużo plików."))
        self._set_status(tr("Kopia wstrzymana do decyzji."))
        reasons = " ".join(error.reasons)
        if self._unattended:
            self._notify(
                tr("Kopia planowa wstrzymana"),
                tr("{reasons} To może być działanie złośliwego oprogramowania szyfrującego pliki. "
                   "Otwórz program, sprawdź pliki i uruchom kopię ręcznie.").format(reasons=reasons),
                warning=True,
            )
            return
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Warning)
        box.setWindowTitle(tr("Podejrzanie dużo zmian"))
        box.setText(
            tr("{reasons}\n\nJeśli to spodziewane — aktualizacja programu, przeniesienie albo "
               "przerobienie wielu plików — kontynuuj.\n\nJeśli nie, NIE kontynuuj: tak wygląda "
               "działanie oprogramowania szyfrującego pliki (ransomware). Sprawdź najpierw, czy "
               "Twoje pliki dają się otworzyć. Wcześniejsze wersje w kopii pozostają "
               "nietknięte.").format(reasons=reasons)
        )
        go = box.addButton(tr("Kontynuuj mimo to"), QMessageBox.ButtonRole.AcceptRole)
        stop = box.addButton(tr("Wstrzymaj kopię"), QMessageBox.ButtonRole.RejectRole)
        box.setDefaultButton(stop)
        box.exec()
        if box.clickedButton() is not go or getattr(self, "_last_launch", None) is None:
            return
        config, keyring, launch_panel, on_success, description = self._last_launch
        confirmed = replace(config, allow_mass_change=True)
        # wątek poprzedniej próby jeszcze się kończy — nową kopię uruchamiamy po nim
        self._after_worker = lambda: self._start_backup_job(
            confirmed, keyring, launch_panel, on_success, description
        )

    def _start_backup_job(self, config: BackupConfig, keyring, panel, on_success, description: str) -> None:
        # zapamiętane, by po potwierdzeniu masowych zmian uruchomić tę samą kopię jeszcze raz
        self._last_launch = (config, keyring, panel, on_success, description)
        def job(reporter):
            plan = engine.plan_backup(config, reporter)
            self.tracker = ProgressTracker(plan.transfer_bytes)
            return engine.run_backup(plan, keyring, reporter)

        self._run_job(job, panel=panel, on_success=on_success, description=description, total_bytes=None)

    def _backup_finished(self, result: engine.OperationResult) -> None:
        self.store.add_history(
            {
                "action": "backup",
                "ok": result.ok,
                "files": result.files_done,
                "bytes": result.bytes_done,
                "path": result.output_path,
            }
        )
        hint = ""
        if result.ok and not self.verify_cb.isChecked():
            hint = tr(
                "Kopię możesz sprawdzić później: ekran „Przywracanie” → „Sprawdź kopię”. "
                "Najlepiej po ponownym podłączeniu dysku — wtedy dane są czytane z nośnika."
            )
        self._report_result(result, tr("Kopia zapasowa"), hint)
        self._preview_after_run()
        self._dest_timer.start()

    def _preview_after_run(self) -> None:
        self.tile_new.set_value("0")
        self.tile_changed.set_value("0")
        self.plan_details.setText(tr("Kopia wykonana. Uruchom podgląd ponownie, aby sprawdzić stan."))

    # -------------------------------------------------------- ekran przywracania

    def _build_restore_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(16)

        layout.addWidget(
            page_title(tr("Przywracanie"), tr("Odtwarza pliki z kopii — również z kopii zaszyfrowanej."))
        )
        layout.addWidget(
            Hint(
                tr("Wskaż główny folder kopii (ten, który wybrałeś jako cel), a nie pojedynczy "
                   "folder z datą. Program sam odczyta spis treści kopii.")
            )
        )

        source_card = Card(
            tr("Skąd przywracamy"),
            tr("Folder zawierający kopię utworzoną przez {app}.").format(app=__app_name__),
        )
        self.restore_src = PathPicker(
            placeholder=tr("np. E:\\Kopie zapasowe"),
            dialog_title=tr("Wybierz folder kopii"),
            tooltip=tr("Główny folder kopii. Zawiera spis treści (.cleanvault-manifest)."),
        )
        self.restore_src.changed.connect(self._inspect_backup)
        source_card.add(self.restore_src)
        self.restore_info = field_help(tr("Wskaż folder kopii, aby zobaczyć jej zawartość."))
        source_card.add(self.restore_info)
        layout.addWidget(source_card)

        dest_card = Card(tr("Dokąd przywracamy"), tr("Miejsce i układ odtwarzanych plików."))
        self.restore_dst = PathPicker(
            placeholder=tr("np. C:\\Odzyskane"),
            dialog_title=tr("Wybierz katalog docelowy"),
            tooltip=tr("Katalog, w którym pojawią się odtworzone pliki."),
        )
        self.restore_dst.changed.connect(lambda _: self._update_restore_readiness())
        dest_card.add(self.restore_dst)

        self.layout_combo = QComboBox()
        self.layout_combo.addItem(tr("Odtwórz pełną strukturę folderów"), "tree")
        self.layout_combo.addItem(tr("Wszystko do jednego folderu"), "flat")
        self.layout_combo.addItem(tr("Przywróć do pierwotnych lokalizacji"), "original")
        self.layout_combo.setToolTip(
            tr("Pełna struktura — układ jak w źródle, wewnątrz wskazanego katalogu.\n"
               "Jeden folder — wygodne, gdy szukasz kilku plików.\n"
               "Pierwotne lokalizacje — zapisuje pliki tam, skąd zostały pobrane.")
        )
        self.layout_combo.currentIndexChanged.connect(self._on_restore_layout_changed)
        dest_card.add(QLabel(tr("Układ plików:")))
        dest_card.add(self.layout_combo)
        self.layout_help = field_help(tr("Pliki trafią do wskazanego katalogu z zachowaniem struktury folderów."))
        dest_card.add(self.layout_help)

        self.collision_combo = QComboBox()
        self.collision_combo.addItem(tr("Zachowaj oba — dopisz numer do nazwy"), "rename")
        self.collision_combo.addItem(tr("Pomiń istniejące pliki"), "skip")
        self.collision_combo.addItem(tr("Nadpisz istniejące pliki"), "overwrite")
        self.collision_combo.setToolTip(tr("Co zrobić, gdy plik o tej nazwie już istnieje w katalogu docelowym."))
        dest_card.add(QLabel(tr("Gdy plik już istnieje:")))
        dest_card.add(self.collision_combo)
        layout.addWidget(dest_card)

        pass_card = Card(tr("Hasło"), tr("Wymagane wyłącznie dla kopii zaszyfrowanych."))
        self.restore_password = PasswordField(tr("Hasło użyte przy tworzeniu kopii"), show_strength=False)
        self.restore_password.changed.connect(lambda _: self._update_restore_readiness())
        self.restore_password.setEnabled(False)
        pass_card.add(self.restore_password)
        self.restore_pass_help = field_help(tr("Program sam wykryje, czy kopia jest zaszyfrowana."))
        pass_card.add(self.restore_pass_help)
        layout.addWidget(pass_card)

        actions = FlowLayout(spacing=10)  # osiem przycisków: na laptopie w dwóch wierszach
        self.verify_btn = button(
            tr("Sprawdź kopię"),
            tr("Odczytuje wszystkie pliki kopii i weryfikuje ich poprawność.\nNic nie zapisuje na dysku."),
            self._verify_backup,
            icon="shield-check",
        )
        self.trial_btn = button(
            tr("Próbne przywrócenie"),
            tr("Przywraca losową próbkę plików do katalogu tymczasowego i porównuje je ze źródłem.\n"
               "Sprawdza całą drogę odzyskiwania, a trwa minuty. Nic nie zostaje na dysku."),
            self._trial_restore,
            icon="patch-check",
        )
        self.restore_btn = button(
            tr("Przywróć pliki"), tr("Odtwarza pliki zgodnie z ustawieniami powyżej"),
            self._start_restore, object_name="Primary", icon="box-arrow-down",
        )
        self.proof_btn = button(
            tr("Znaczniki czasu…"),
            tr("Znaczniki Sigelith wersji w tym katalogu kopii: sprawdzenie i certyfikat"),
            self._show_proofs,
            icon="clock-history",
        )
        self.browse_btn = button(
            tr("Przeglądaj…"),
            tr("Pokazuje pliki i wersje tej kopii — pojedynczy plik otworzysz bez przywracania całości"),
            self._browse_restore_source,
            icon="folder2-open",
        )
        self.evidence_btn = button(
            tr("Dowody Sigelith…"),
            tr("Dokumenty oznakowane w Sigelith, zabezpieczone w tej kopii: sprawdzenie i odzyskanie"),
            self._show_evidence,
            icon="patch-check",
        )
        self.evidence_btn.hide()  # pokazuje się, gdy w katalogu kopii jest magazyn dowodów
        cloud_btn = button(
            tr("Z kopii poza domem…"),
            tr("Przywraca pliki z zaszyfrowanej kopii w usłudze S3 — także na nowym komputerze"),
            self._restore_offsite,
            icon="cloud-arrow-down",
        )
        actions.addWidget(self.verify_btn)
        actions.addWidget(self.trial_btn)
        actions.addWidget(self.proof_btn)
        actions.addWidget(self.browse_btn)
        actions.addWidget(self.evidence_btn)
        capsule_btn = button(
            tr("Kapsuły czasu…"),
            tr("Pliki zapieczętowane w tej kopii do daty — klucze wydają dopiero po niej sieć drand "
               "i serwer kluczy Sigelith"),
            self._show_capsules,
            icon="shield-lock",
        )
        actions.addWidget(capsule_btn)
        actions.addWidget(cloud_btn)
        actions.addWidget(self.restore_btn)
        layout.addLayout(actions)

        self.restore_panel = OperationPanel()
        self.restore_panel.cancel_requested.connect(self._cancel_operation)
        layout.addWidget(self.restore_panel)
        layout.addStretch(1)

        self._restore_encrypted = False
        self._update_restore_readiness()
        return page

    def _on_restore_layout_changed(self) -> None:
        mode = self.layout_combo.currentData()
        texts = {
            "tree": tr("Pliki trafią do wskazanego katalogu z zachowaniem struktury folderów."),
            "flat": tr("Wszystkie pliki wylądują bezpośrednio w katalogu docelowym, bez podfolderów."),
            "original": tr("Pliki wrócą dokładnie tam, skąd pochodzą. Katalog docelowy zostanie zignorowany."),
        }
        self.layout_help.setText(texts.get(mode, ""))
        self.restore_dst.setEnabled(mode != "original")
        self._update_restore_readiness()

    def _inspect_backup(self, path: str) -> None:
        self._restore_encrypted = False
        if not path or not Path(path).is_dir():
            self.restore_info.setText(tr("Wskaż folder kopii, aby zobaczyć jej zawartość."))
            self._update_restore_readiness()
            return
        # Najpierw lekkie podsumowanie; pełny manifest tylko dla kopii zapisanych
        # starszą wersją programu, która podsumowania nie tworzyła.
        summary = ManifestSummary.load(Path(path))
        if summary is None:
            manifest = Manifest.load(Path(path))
            if manifest.entries:
                summary = ManifestSummary(
                    updated=manifest.updated,
                    encrypted=manifest.encrypted,
                    entry_count=len(manifest.entries),
                    total_bytes=sum(entry.size for entry in manifest.entries.values()),
                    roots=manifest.roots,
                    versions=manifest.versions,
                    runs=manifest.runs,
                )
        if summary is not None and summary.entry_count:
            when = time.strftime(tr("%d.%m.%Y %H:%M"), time.localtime(summary.updated))
            self._restore_encrypted = summary.encrypted
            kind = tr("zaszyfrowana (AES-256-GCM)") if summary.encrypted else tr("niezaszyfrowana")
            roots = ", ".join(summary.roots.values()) or tr("brak danych")
            text = tr(
                "Kopia {kind} • {count} {files} • {size} • "
                "ostatnia aktualizacja {when}\nŹródła: {roots}"
            ).format(
                kind=kind,
                count=summary.entry_count,
                files=plural(summary.entry_count, "plik", "pliki", "plików"),
                size=human_size(summary.total_bytes),
                when=when,
                roots=roots,
            )
            pending = [run for run in summary.runs.values() if run.known and not run.complete]
            if pending:
                names = ", ".join(engine.describe_version(run) for run in pending)
                text += tr(
                    "\nUwaga: niedokończone wersje (nie zawierają wszystkich plików): {names}"
                ).format(names=names)
            self.restore_info.setText(text)
        else:
            # ``rglob`` jest leniwy — ``list(...)[:50]`` przechodził najpierw całe
            # drzewo, co przy kopii z milionem plików zamrażało okno na minuty.
            sample = itertools.islice((p for p in Path(path).rglob("*") if p.is_file()), 50)
            encrypted_found = any(crypto.is_encrypted_file(p) for p in sample)
            self._restore_encrypted = encrypted_found
            self.restore_info.setText(
                tr("Nie znaleziono spisu treści kopii — program przeskanuje folder i rozpozna "
                   "pliki po ich zawartości.")
            )
        self.restore_password.setEnabled(self._restore_encrypted)
        self.restore_pass_help.setText(
            tr("Kopia jest zaszyfrowana — podaj hasło użyte przy jej tworzeniu.")
            if self._restore_encrypted
            else tr("Ta kopia nie jest zaszyfrowana — hasło nie jest potrzebne.")
        )
        self._update_restore_readiness()

    def _show_evidence(self) -> None:
        EvidenceDialog(self.restore_src.path(), self).exec()

    def _show_capsules(self) -> None:
        root = self.restore_src.path()
        if not root or not Path(root).is_dir():
            self._set_status(tr("Wskaż najpierw folder kopii — kapsuła leży w kopii."))
            return
        # Import dopiero tutaj: krzywa eliptyczna (py_ecc) ładuje się pół sekundy,
        # a większość uruchomień programu kapsuł nie otwiera.
        from .capsule_dialog import CapsuleDialog

        CapsuleDialog(root, self).exec()

    def _browse_restore_source(self) -> None:
        self.browser.open_backup(self.restore_src.path())
        self._go_to(self.PAGE_BROWSE)

    def _update_restore_readiness(self) -> None:
        busy = self.worker is not None and self.worker.isRunning()
        has_source = bool(self.restore_src.path())
        needs_dest = self.layout_combo.currentData() != "original"
        has_dest = bool(self.restore_dst.path()) or not needs_dest
        has_password = (not self._restore_encrypted) or bool(self.restore_password.password())
        ready = has_source and has_dest and has_password and not busy
        self.restore_btn.setEnabled(ready)
        self.verify_btn.setEnabled(has_source and has_password and not busy)
        self.trial_btn.setEnabled(has_source and has_password and not busy)
        self.proof_btn.setEnabled(has_source)
        self.browse_btn.setEnabled(has_source)
        self.evidence_btn.setVisible(has_source and evidence.has_vault(self.restore_src.path()))

        if not has_source:
            self.restore_btn.setToolTip(tr("Wskaż folder kopii."))
        elif not has_dest:
            self.restore_btn.setToolTip(tr("Wskaż katalog docelowy."))
        elif not has_password:
            self.restore_btn.setToolTip(tr("Kopia jest zaszyfrowana — podaj hasło."))
        else:
            self.restore_btn.setToolTip(tr("Odtwarza pliki zgodnie z ustawieniami powyżej"))

    def _verify_backup(self) -> None:
        source = self.restore_src.path()
        keyring = self._make_keyring(self.restore_password.password()) if self._restore_encrypted else None

        def job(reporter):
            # Wcześniej ten przycisk dla kopii niezaszyfrowanej niczego nie
            # czytał i zawsze zgłaszał sukces. Teraz każdy plik jest porównywany
            # z sumą kontrolną zapisaną w spisie treści podczas kopii.
            summary = ManifestSummary.load(Path(source))
            self.tracker = ProgressTracker(summary.total_bytes if summary else 0)
            return engine.verify_backup(source, keyring, reporter, workers=self.workers_spin.value())

        self._run_job(
            job,
            panel=self.restore_panel,
            on_success=lambda r: self._report_result(r, tr("Weryfikacja kopii")),
            description=tr("weryfikacja"),
            total_bytes=None,
        )

    def _show_proofs(self) -> None:
        cloud.ProofDialog(self.restore_src.path(), self).exec()

    def _restore_offsite(self) -> None:
        dialog = cloud.OffsiteRestoreDialog(self.store, self)
        if dialog.exec() != QDialog.DialogCode.Accepted or dialog.choice is None:
            return
        target, secret, password, stamp, destination = dialog.choice

        def job(reporter):
            restored, errors = offsite.restore(
                S3Client(target, secret), cloud.keyring_for(password), stamp, destination,
                reporter.stage, reporter.advance, lambda: reporter.cancelled,
            )
            return engine.OperationResult(
                ok=not errors and not reporter.cancelled, files_done=restored, errors=errors,
                cancelled=reporter.cancelled, output_path=destination,
            )

        self._run_job(
            job,
            panel=self.restore_panel,
            on_success=lambda r: self._report_result(r, tr("Przywracanie z kopii poza domem")),
            description=tr("przywracanie z kopii poza domem"),
            total_bytes=None,
        )

    def _configure_offsite(self) -> None:
        if not self._require_template():
            return
        template = self.store.get_template(self.selected_template_id)
        if cloud.OffsiteDialog(self.store, template, self).exec() == QDialog.DialogCode.Accepted:
            self._refresh_templates()
            self._set_status(tr("Kopia poza domem dla szablonu „{name}” zapisana.").format(name=template.name))

    def _run_offsite(self, template_id: str, unattended: bool = False) -> None:
        """Wysyła migawkę szablonu poza dom — po kopii lokalnej albo na żądanie."""
        template = self.store.get_template(template_id)
        if template is None or not template.offsite:
            return
        secret, password = cloud.secrets_for(template.id)
        if not secret or not password:
            self._notify(
                tr("Kopia poza domem nie ruszyła"),
                tr("Brak klucza albo hasła w Menedżerze poświadczeń Windows — zapisz ustawienia "
                   "kopii poza domem jeszcze raz."),
                warning=True,
            )
            return
        config = BackupConfig(sources=template.sources, destination=template.destination,
                              excludes=template.excludes, sigelith=template.sigelith)
        try:
            roots = engine.source_roots(config)
        except engine.EngineError as exc:
            self._notify(tr("Kopia poza domem nie ruszyła"), str(exc), warning=True)
            return
        vault = Path(template.destination) / evidence.EVIDENCE_DIR
        if template.sigelith and vault.is_dir():
            # magazyn dowodów leży w katalogu kopii, a nie w źródłach — poza dom idzie osobno
            roots.append(SourceRoot(path=vault, label=evidence.EVIDENCE_DIR))
        excludes = engine.effective_excludes(config)
        target = S3Target.from_dict(template.offsite)
        keep = template.offsite_keep

        def job(reporter):
            client = S3Client(target, secret)
            keyring = cloud.keyring_for(password)
            sent = offsite.upload(
                roots, excludes, client, keyring, reporter.stage, reporter.advance,
                lambda: reporter.cancelled, workers=template.workers,
            )
            notes = []
            if sent.ok and keep and len(offsite.list_snapshots(client)) > keep + 5:
                # nadmiar usuwamy partiami — sprzątanie czyta wszystkie migawki, więc nie codziennie
                removed, chunks_removed = offsite.prune(client, keyring, keep, reporter.stage)
                notes.append(tr("Usunięto starsze migawki: {count}, nieużywane fragmenty: {chunks}.").format(
                    count=removed, chunks=chunks_removed))
            notes.insert(0, tr("Migawka {stamp}: plików bez zmian {reused}, wysłanych {files}, "
                               "nowych fragmentów {chunks} ({size}).").format(
                stamp=beat.describe(sent.stamp) if sent.stamp else "—", reused=sent.reused,
                files=sent.files, chunks=sent.uploaded_chunks, size=engine.human_size(sent.uploaded_bytes)))
            if sent.skipped:
                notes.append(tr("Pominięte (otwarte w innych programach albo zmienione w trakcie): {count}.").format(
                    count=len(sent.skipped)))
            return engine.OperationResult(
                ok=sent.ok, files_done=sent.files, bytes_done=sent.uploaded_bytes, errors=sent.errors,
                cancelled=sent.cancelled, notes=notes,
            )

        def done(result: engine.OperationResult) -> None:
            current = self.store.get_template(template_id) or template
            current.offsite_last = time.time()
            current.offsite_last_result = result.summary
            self.store.put_template(current)
            self.store.add_history(
                {"action": "offsite", "ok": result.ok, "files": result.files_done,
                 "template": current.name, "scheduled": unattended}
            )
            self._refresh_templates()
            self._report_result(result, tr("Kopia poza domem „{name}”").format(name=current.name),
                                unattended=unattended)

        self._unattended = unattended
        self._run_job(
            job, panel=self.template_panel, on_success=done,
            description=tr("kopia poza domem"), total_bytes=None,
        )

    def _trial_restore(self) -> None:
        source = self.restore_src.path()
        keyring = self._make_keyring(self.restore_password.password()) if self._restore_encrypted else None
        self._run_job(
            lambda reporter: engine.trial_restore(source, keyring, reporter),
            panel=self.restore_panel,
            on_success=lambda r: self._report_result(r, tr("Próbne przywrócenie")),
            description=tr("próbne przywrócenie"),
            total_bytes=engine.TRIAL_BYTE_BUDGET,
        )

    def _start_restore(self) -> None:
        source = self.restore_src.path()
        destination = self.restore_dst.path() or source
        mode = self.layout_combo.currentData()
        collision = self.collision_combo.currentData()
        keyring = self._make_keyring(self.restore_password.password()) if self._restore_encrypted else None

        if mode == "original":
            answer = QMessageBox.question(
                self,
                tr("Przywracanie do pierwotnych lokalizacji"),
                tr("Pliki zostaną zapisane dokładnie tam, skąd pochodzą.\n\n"
                   "Konflikty nazw: {collision}.\n\n"
                   "Czy kontynuować?").format(collision=self.collision_combo.currentText().lower()),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if answer != QMessageBox.StandardButton.Yes:
                return
        if collision == "overwrite":
            answer = QMessageBox.warning(
                self,
                tr("Nadpisywanie plików"),
                tr("Wybrano nadpisywanie istniejących plików. Ich obecna zawartość "
                   "zostanie bezpowrotnie zastąpiona.\n\nCzy kontynuować?"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if answer != QMessageBox.StandardButton.Yes:
                return

        self._launch_restore(source, destination, mode, collision, keyring)

    def _launch_restore(self, source: str, destination: str, mode: str, collision: str,
                        keyring: crypto.PasswordKeyring | None, private_ok: bool = False) -> None:
        self._last_restore = (source, destination, mode, collision, keyring)

        def job(reporter):
            plan = engine.plan_restore(source, destination, layout=mode, collision=collision, reporter=reporter)
            hidden = [] if private_ok else paths.private_appdata_folders(engine.restore_roots(plan))
            if hidden:
                raise engine.PrivateAppDataTargets(hidden)
            self.tracker = ProgressTracker(plan.total_bytes)
            return engine.run_restore(plan, keyring, reporter)

        self._run_job(
            job,
            panel=self.restore_panel,
            on_success=lambda r: (self.store.add_history({"action": "restore", "ok": r.ok, "files": r.files_done}), self._report_result(r, tr("Przywracanie"))),
            description=tr("przywracanie"),
            total_bytes=None,
        )

    def _handle_private_appdata(self, panel: OperationPanel, error: engine.PrivateAppDataTargets) -> None:
        """Wersja ze Sklepu nie utworzy prawdziwego folderu prosto w AppData — mówimy o tym przed zapisem."""
        panel.set_stage(tr("Przywracanie wstrzymane do decyzji."))
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Warning)
        box.setWindowTitle(tr("Foldery w AppData"))
        box.setText(
            tr("Przywracanie utworzy nowe foldery bezpośrednio w AppData:\n\n{folders}\n\n"
               "Windows pozwala wersji programu ze Sklepu tworzyć je tylko w jej prywatnej kopii — "
               "pliki będą widoczne w tym programie, ale nie w programie, do którego należą.\n\n"
               "Najprościej: zainstaluj i raz uruchom tamten program (utworzy swój folder), "
               "a potem przywróć jeszcze raz. Albo przywróć do zwykłego folderu i przenieś "
               "pliki Eksploratorem.").format(folders="\n".join(str(folder) for folder in error.folders))
        )
        go = box.addButton(tr("Przywróć mimo to"), QMessageBox.ButtonRole.AcceptRole)
        stop = box.addButton(tr("Anuluj"), QMessageBox.ButtonRole.RejectRole)
        box.setDefaultButton(stop)
        box.exec()
        if box.clickedButton() is not go:
            return
        source, destination, mode, collision, keyring = self._last_restore
        # wątek poprzedniej próby jeszcze się kończy — przywracanie ruszy po nim
        self._after_worker = lambda: self._launch_restore(source, destination, mode, collision, keyring,
                                                          private_ok=True)

    # ------------------------------------------------------------ ekran szablonów

    def _build_templates_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(16)

        layout.addWidget(
            page_title(tr("Szablony"), tr("Zapisane konfiguracje — uruchamiasz je jednym kliknięciem."))
        )
        layout.addWidget(
            Hint(
                tr("Szablon przechowuje foldery, opcje i wykluczenia. Hasło nigdy nie trafia "
                   "do szablonu — jest przechowywane w Menedżerze poświadczeń Windows albo "
                   "wpisywane przy każdym uruchomieniu.")
            )
        )

        card = Card(tr("Zapisane szablony"))
        self.template_list = QListWidget()
        self.template_list.setMinimumHeight(190)
        self.template_list.currentItemChanged.connect(self._on_template_selected)
        self.template_list.setToolTip(tr("Kliknij szablon, aby zobaczyć jego szczegóły."))
        card.add(self.template_list)

        self.template_details = field_help(tr("Wybierz szablon z listy."))
        card.add(self.template_details)

        schedule_row = QHBoxLayout()
        schedule_row.setSpacing(10)
        schedule_row.addWidget(QLabel(tr("Harmonogram:")))
        self.schedule_combo = QComboBox()
        self.schedule_combo.addItem(tr("Ręcznie"), scheduler.MANUAL)
        self.schedule_combo.addItem(tr("Codziennie o godzinie"), scheduler.DAILY)
        self.schedule_combo.addItem(tr("Po podłączeniu dysku docelowego"), scheduler.ON_CONNECT)
        self.schedule_combo.addItem(tr("Na bieżąco"), scheduler.LIVE)
        self.schedule_combo.setToolTip(tr("Kiedy kopia z tego szablonu ma ruszać sama."))
        self.schedule_time = QTimeEdit()
        self.schedule_time.setDisplayFormat("HH:mm")
        self.schedule_time.setToolTip(tr("Godzina kopii codziennej (czas tego komputera)."))
        schedule_row.addWidget(self.schedule_combo)
        schedule_row.addWidget(self.schedule_time)
        schedule_row.addStretch(1)
        card.add_layout(schedule_row)
        self.schedule_note = field_help("")
        card.add(self.schedule_note)
        self.schedule_combo.currentIndexChanged.connect(self._schedule_changed)
        self.schedule_time.timeChanged.connect(self._schedule_changed)
        self._set_schedule_controls(None)

        rename_row = QHBoxLayout()
        self.template_name_edit = QLineEdit()
        self.template_name_edit.setPlaceholderText(tr("Nazwa szablonu"))
        self.template_name_edit.setToolTip(tr("Zmień nazwę, aby łatwiej rozpoznawać szablon."))
        rename_row.addWidget(self.template_name_edit, 1)
        rename_row.addWidget(button(tr("Zapisz nazwę"), tr("Zapisuje nową nazwę szablonu"), self._rename_template))
        card.add_layout(rename_row)

        actions = FlowLayout(spacing=10)
        actions.addWidget(self._wizard_button())
        actions.addWidget(button(
            tr("Uruchom kopię"), tr("Wykonuje kopię według tego szablonu"),
            self._run_template, object_name="Primary", icon="play-fill",
        ))
        actions.addWidget(button(
            tr("Przywróć z tej kopii"), tr("Otwiera ekran przywracania z wypełnionymi ścieżkami"),
            self._restore_from_template, icon="arrow-counterclockwise",
        ))
        actions.addWidget(button(
            tr("Wczytaj do formularza"), tr("Kopiuje ustawienia szablonu na ekran „Kopia zapasowa”"),
            self._load_template_to_form, icon="pencil-square",
        ))
        actions.addWidget(button(
            tr("Kopia poza domem…"), tr("Druga, zaszyfrowana kopia w usłudze zgodnej z S3 (np. Backblaze B2)"),
            self._configure_offsite, icon="cloud-arrow-up",
        ))
        actions.addWidget(button(
            tr("Usuń"), tr("Usuwa szablon. Nie kasuje żadnych plików kopii."),
            self._delete_template, object_name="Danger", icon="trash",
        ))
        card.add_layout(actions)
        layout.addWidget(card)

        self.template_panel = OperationPanel()
        self.template_panel.cancel_requested.connect(self._cancel_operation)
        layout.addWidget(self.template_panel)

        history_card = Card(tr("Ostatnie operacje"), tr("Skrót z dziennika — pełny zapis znajdziesz w zakładce „Dziennik”."))
        self.history_list = QListWidget()
        self.history_list.setMaximumHeight(170)
        history_card.add(self.history_list)
        layout.addWidget(history_card)
        layout.addStretch(1)
        return page

    def _refresh_templates(self) -> None:
        self.template_list.clear()
        for template in sorted(self.store.templates().values(), key=lambda t: t.created, reverse=True):
            item = QListWidgetItem(template.name)
            # Identyfikator trzymamy w danych elementu. W 1.x odzyskiwano go przez
            # split(" — ") na etykiecie, co psuło się przy nazwie z myślnikiem.
            item.setData(Qt.ItemDataRole.UserRole, template.id)
            self.template_list.addItem(item)
        self._refresh_history()
        self._refresh_sidebar_note()
        self._refresh_tray()

    def _refresh_history(self) -> None:
        self.history_list.clear()
        for entry in self.store.history(25):
            when = time.strftime(tr("%d.%m %H:%M"), time.localtime(entry.get("at", 0)))
            action = {
                "backup": tr("Kopia"),
                "offsite": tr("Poza dom"),
            }.get(entry.get("action"), tr("Przywracanie"))
            files = entry.get("files", 0)
            item = QListWidgetItem(
                tr("{when}  •  {action}  •  {count} {files}").format(
                    when=when, action=action, count=files,
                    files=plural(files, "plik", "pliki", "plików"),
                )
            )
            item.setIcon(icons.icon("check-circle" if entry.get("ok") else "exclamation-triangle"))
            self.history_list.addItem(item)

    def _on_template_selected(self, current: QListWidgetItem | None) -> None:
        if current is None:
            self.selected_template_id = None
            self.template_details.setText(tr("Wybierz szablon z listy."))
            self._set_schedule_controls(None)
            return
        self.selected_template_id = current.data(Qt.ItemDataRole.UserRole)
        template = self.store.get_template(self.selected_template_id)
        if template is None:
            return
        self._set_schedule_controls(template)
        self.template_name_edit.setText(template.name)
        created = time.strftime(tr("%d.%m.%Y"), time.localtime(template.created))
        last = (
            time.strftime(tr("%d.%m.%Y %H:%M"), time.localtime(template.last_run))
            if template.last_run
            else tr("jeszcze nie uruchamiany")
        )
        yes, no = tr("tak"), tr("nie")
        self.template_details.setText(
            tr("Źródła: {sources}\n"
               "Cel: {destination}\n"
               "Układ: {structure} • Szyfrowanie: {encrypt} • "
               "Weryfikacja: {verify} • "
               "Dogrywka: {catchup} • "
               "Równolegle: {workers} • "
               "Data uzupełnienia w nazwie: {stamp}\n"
               "Utworzony: {created} • Ostatni przebieg: {last}").format(
                sources=", ".join(template.sources) or "—",
                destination=template.destination or "—",
                structure=tr("wersje z datą") if template.structure == "dated" else tr("kopia lustrzana"),
                encrypt=yes if template.encrypt else no,
                verify=yes if template.verify_after_write else no,
                catchup=template.catchup_passes or tr("wyłączona"),
                workers=template.workers or tr("automatycznie"),
                stamp=yes if template.stamp_updates else no,
                created=created,
                last=last,
            )
        )
        if template.sigelith:
            self.template_details.setText(
                self.template_details.text() + "\n"
                + tr("Chroni dowody Sigelith: historię stempli i oznakowane dokumenty.")
            )

    def _set_schedule_controls(self, template: Template | None) -> None:
        """Pokazuje harmonogram zaznaczonego szablonu — bez wywołania zapisu."""
        for widget in (self.schedule_combo, self.schedule_time):
            widget.blockSignals(True)
        try:
            enabled = template is not None
            self.schedule_combo.setEnabled(enabled)
            self.schedule_time.setEnabled(enabled)
            schedule = template.schedule if template else scheduler.MANUAL
            self.schedule_combo.setCurrentIndex(max(0, self.schedule_combo.findData(schedule)))
            hours, minutes = scheduler.parse_time(template.schedule_time if template else scheduler.DEFAULT_TIME)
            self.schedule_time.setTime(QTime(hours, minutes))
            self.schedule_time.setVisible(schedule == scheduler.DAILY)
            self.schedule_note.setText(self._schedule_description(template) if template else "")
        finally:
            for widget in (self.schedule_combo, self.schedule_time):
                widget.blockSignals(False)

    def _schedule_description(self, template: Template) -> str:
        if template.schedule == scheduler.DAILY:
            when = time.strftime(
                tr("%d.%m.%Y %H:%M"), time.localtime(scheduler.next_slot(time.time(), template.schedule_time))
            )
            text = tr("Następna kopia: {when}. Jeśli komputer będzie wtedy wyłączony, kopia ruszy "
                      "po jego włączeniu.").format(when=when)
        elif template.schedule == scheduler.ON_CONNECT:
            text = tr("Kopia ruszy po podłączeniu dysku docelowego — najwyżej raz na 12 godzin.")
        elif template.schedule == scheduler.LIVE:
            text = tr("Zmiany w folderach źródłowych trafiają do dzisiejszej wersji kopii kilka minut "
                      "po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje. Jedna "
                      "wersja na dzień; ze znacznikami czasu zamyka ją pieczęć następnego dnia.")
        else:
            return tr("Kopia rusza tylko wtedy, gdy ją uruchomisz.")
        return text + " " + self._background_status()

    def _background_status(self) -> str:
        if autostart.is_enabled():
            return tr("Program uruchamia się w tle przy logowaniu, więc terminy nie przepadną.")
        if autostart.blocked_in_windows():
            return tr("Start przy logowaniu wyłączono w Ustawieniach Windows → Aplikacje → Uruchamianie; "
                      "dopóki go tam nie włączysz, kopie planowe działają tylko przy otwartym programie.")
        return tr("Kopie planowe działają, gdy działa program (także ukryty przy zegarze).")

    def _schedule_changed(self) -> None:
        template = self.store.get_template(self.selected_template_id) if self.selected_template_id else None
        if template is None:
            return
        template.schedule = self.schedule_combo.currentData()
        template.schedule_time = self.schedule_time.time().toString("HH:mm")
        scheduler.arm(template)
        self.store.put_template(template)
        if template.schedule != scheduler.MANUAL:
            self._ensure_autostart()
        self._set_schedule_controls(template)
        self._set_status(tr("Harmonogram szablonu „{name}” zapisany.").format(name=template.name))

    def _ensure_autostart(self) -> None:
        """Kopie planowe bez startu przy logowaniu przepadałyby po każdym restarcie."""
        if autostart.supported() and not autostart.is_enabled() and autostart.set_enabled(True):
            if hasattr(self, "autostart_cb"):
                self.autostart_cb.blockSignals(True)
                self.autostart_cb.setChecked(True)
                self.autostart_cb.blockSignals(False)
            self._notify(
                tr("Start przy logowaniu włączony"),
                tr("Sigelith Backup będzie uruchamiał się w tle, żeby wykonywać kopie planowe. "
                   "Wyłączysz to w ustawieniach programu."),
            )

    def _ask_template_settings(self, suggested: str) -> tuple[str, str, str] | None:
        """Nazwa szablonu i kopia automatyczna; ``None`` po rezygnacji (w testach podmieniane)."""
        dialog = TemplateDialog(list(self.store.templates().values()), suggested, self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return None
        name, schedule, schedule_time = dialog.values()
        return (name, schedule, schedule_time) if name else None

    def _save_as_template(self) -> None:
        answer = self._ask_template_settings(
            tr("Kopia {folder}").format(folder=Path(self.source_list.paths()[0]).name)
            if self.source_list.paths()
            else tr("Nowy szablon")
        )
        if answer is None:
            return
        name, schedule, schedule_time = answer
        # Szablon o tej nazwie już istnieje: zastępujemy go (za zgodą), zamiast
        # tworzyć drugi o tej samej nazwie. Inaczej zmienionych ustawień nie
        # dało się wprowadzić do istniejącego szablonu.
        existing = next((t for t in self.store.templates().values() if t.name == name), None)
        if existing is not None:
            answer = QMessageBox.question(
                self,
                tr("Zastąpić szablon?"),
                tr("Szablon „{name}” już istnieje.\n\n"
                   "Zastąpić go bieżącymi ustawieniami z formularza?").format(name=existing.name),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if answer != QMessageBox.StandardButton.Yes:
                return
        config = self._current_config()
        from_form = {
            "name": name,
            "sources": config.sources,
            "destination": config.destination,
            "structure": config.structure,
            "encrypt": config.encrypt,
            "verify_after_write": config.verify_after_write,
            "excludes": config.excludes,
            "retention": config.retention,
            "gfs_daily": config.gfs_daily,
            "gfs_weekly": config.gfs_weekly,
            "gfs_monthly": config.gfs_monthly,
            "catchup_passes": config.catchup_passes,
            "workers": config.workers,
            "stamp_updates": config.stamp_updates,
            "delta": config.delta,
            "timestamp": config.timestamp,
            "sigelith": config.sigelith,
            "remember_password": self.remember_cb.isChecked(),
        }
        if existing is not None:
            # Z formularza przychodzi tylko to, co formularz pokazuje. Kopia poza domem
            # i historia przebiegów zostają z zastępowanego szablonu; harmonogram okno
            # zapisu podpowiada z niego (TemplateDialog), więc też go nie kasuje.
            template = replace(existing, **from_form)
            if existing.remember_password and not template.remember_password:
                secrets_store.delete_password(existing.id)
        else:
            template = Template(**from_form)
        template.schedule = schedule
        template.schedule_time = schedule_time
        scheduler.arm(template)
        self.store.put_template(template)
        if schedule != scheduler.MANUAL:
            self._ensure_autostart()
        if template.encrypt and template.remember_password:
            saved = secrets_store.save_password(template.id, self.password_field.password())
            if not saved:
                template.remember_password = False
                self.store.put_template(template)
                QMessageBox.information(
                    self,
                    tr("Hasło niezapisane"),
                    tr("Nie udało się zapisać hasła w magazynie systemowym.\n"
                       "Szablon działa normalnie — program poprosi o hasło przy uruchomieniu."),
                )
        self._refresh_templates()
        self._set_status(tr("Zapisano szablon „{name}”.").format(name=template.name))

    def _rename_template(self) -> None:
        if not self._require_template():
            return
        template = self.store.get_template(self.selected_template_id)
        name = self.template_name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, tr("Pusta nazwa"), tr("Nazwa szablonu nie może być pusta."))
            return
        template.name = name
        self.store.put_template(template)
        self._refresh_templates()
        self._set_status(tr("Nazwa szablonu zapisana."))

    def _delete_template(self) -> None:
        if not self._require_template():
            return
        template = self.store.get_template(self.selected_template_id)
        answer = QMessageBox.question(
            self,
            tr("Usunąć szablon?"),
            tr("Szablon „{name}” zostanie usunięty.\n\n"
               "Pliki kopii zapasowej pozostaną nienaruszone.").format(name=template.name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        secrets_store.delete_password(template.id)
        secrets_store.delete_password(cloud.OFFSITE_KEY.format(template.id))
        secrets_store.delete_password(cloud.OFFSITE_PASSWORD.format(template.id))
        self.store.delete_template(template.id)
        self.selected_template_id = None
        self._refresh_templates()
        self._set_status(tr("Szablon usunięty."))

    def _apply_template_to_form(self, template: Template) -> None:
        """Przenosi szablon do formularza kopii — wspólne dla listy szablonów i kreatora."""
        self.source_list.set_paths(template.sources)
        self.dest_picker.set_path(template.destination)
        self.structure_dated.setChecked(template.structure == "dated")
        self.structure_mirror.setChecked(template.structure != "dated")
        self.encrypt_cb.setChecked(template.encrypt)
        self.verify_cb.setChecked(template.verify_after_write)
        self._set_retention(template.retention, template.gfs_daily, template.gfs_weekly, template.gfs_monthly)
        self.catchup_spin.setValue(template.catchup_passes)
        self.workers_spin.setValue(template.workers)
        self.stamp_updates_cb.setChecked(template.stamp_updates)
        self.delta_cb.setChecked(template.delta)
        self.timestamp_cb.setChecked(template.timestamp)
        self.sigelith_cb.setChecked(template.sigelith)
        self.excludes_edit.setPlainText("\n".join(template.excludes))
        self._go_to(self.PAGE_BACKUP)

    def _load_template_to_form(self) -> None:
        if not self._require_template():
            return
        template = self.store.get_template(self.selected_template_id)
        self._apply_template_to_form(template)
        self._set_status(tr("Wczytano szablon „{name}” do formularza.").format(name=template.name))

    def _restore_from_template(self) -> None:
        if not self._require_template():
            return
        template = self.store.get_template(self.selected_template_id)
        self.restore_src.set_path(template.destination)
        self._go_to(self.PAGE_RESTORE)
        self._set_status(tr("Ekran przywracania wypełniony danymi szablonu."))

    def _run_template(self) -> None:
        if not self._require_template():
            return
        self._run_template_now(self.store.get_template(self.selected_template_id))

    def _run_template_now(self, template: Template, unattended: bool = False, live: bool = False) -> None:
        """Uruchamia kopię z szablonu — z ekranu szablonów, z zasobnika albo z harmonogramu.

        ``unattended``: nikt nie siedzi przy komputerze, więc żadnych okien
        dialogowych — brak zapamiętanego hasła kończy się powiadomieniem,
        niedokończona wersja jest uzupełniana, a wynik trafia do powiadomienia.
        ``live``: dogrywka trybu „na bieżąco” — do dzisiejszej wersji, bez powiadomienia
        o sukcesie (byłoby co kilka minut).
        """
        keyring = None
        if template.encrypt:
            password = secrets_store.load_password(template.id) if template.remember_password else None
            if not password and unattended:
                self._notify(
                    tr("Kopia „{name}” nie ruszyła").format(name=template.name),
                    tr("Szablon jest zaszyfrowany, a hasło nie jest zapamiętane. Kopie planowe "
                       "potrzebują hasła zapisanego w Menedżerze poświadczeń Windows."),
                    warning=True,
                )
                return
            if not password:
                password, accepted = QInputDialog.getText(
                    self,
                    tr("Hasło do kopii"),
                    tr("Podaj hasło dla szablonu „{name}”:").format(name=template.name),
                    QLineEdit.EchoMode.Password,
                )
                if not accepted or not password:
                    return
            keyring = self._make_keyring(password)

        config = BackupConfig(
            sources=template.sources,
            destination=template.destination,
            structure=template.structure,
            encrypt=template.encrypt,
            verify_after_write=template.verify_after_write,
            excludes=template.excludes,
            retention=template.retention,
            gfs_daily=template.gfs_daily,
            gfs_weekly=template.gfs_weekly,
            gfs_monthly=template.gfs_monthly,
            catchup_passes=template.catchup_passes,
            workers=template.workers,
            stamp_updates=template.stamp_updates,
            delta=template.delta,
            timestamp=template.timestamp,
            sigelith=template.sigelith,
        )

        service = getattr(self, "scheduler_service", None)
        tracked = service is not None and template.schedule == scheduler.LIVE
        if tracked:
            service.live_tracker.started(template.id)
            self._live_run = template.id

        def done(result: engine.OperationResult) -> None:
            if tracked:
                service.live_tracker.finished(template.id, result.ok)
                if result.ok and not live:
                    service.live_tracker.release(template.id)  # człowiek uruchomił kopię sam
                self._live_run = None
            # Szablon mógł zostać zmieniony w trakcie wielogodzinnej kopii (np. inny
            # harmonogram) — zapisujemy wynik na świeżo wczytanym, nie na starej kopii.
            current = self.store.get_template(template.id) or template
            current.last_run = time.time()
            current.last_result = result.summary
            if result.ok:
                current.last_success = current.last_run
            self.store.put_template(current)
            self.store.add_history(
                {
                    "action": "backup",
                    "ok": result.ok,
                    "files": result.files_done,
                    "template": current.name,
                    "scheduled": unattended,
                }
            )
            self._refresh_templates()
            self._report_result(
                result, tr("Szablon „{name}”").format(name=current.name), unattended=unattended,
                quiet=live,
            )
            if result.ok and current.offsite_enabled and current.offsite:
                # po lokalnej kopii — ten sam łańcuch co inspekcja → kopia
                self._after_worker = lambda: self._run_offsite(current.id, unattended)

        self._launch_backup(
            config,
            keyring,
            self.template_panel,
            done,
            tr("szablon {name}").format(name=template.name),
            unattended=unattended,
            live=live,
        )

    def _require_template(self) -> bool:
        if not self.selected_template_id:
            QMessageBox.information(self, tr("Nie wybrano szablonu"), tr("Zaznacz szablon na liście."))
            return False
        return True

    # ------------------------------------------------------------ ekran ustawień

    def _build_settings_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(16)

        layout.addWidget(page_title(tr("Ustawienia"), tr("Wygląd, wykluczenia domyślne i informacje o środowisku.")))

        look = Card(tr("Wygląd"))
        self.language_combo = QComboBox()
        self.language_combo.addItem(tr("Automatycznie (język systemu)"), "auto")
        for code, name in i18n.LANGUAGES.items():
            # nazwy języków zostają w ich własnym brzmieniu — tak się je poznaje
            self.language_combo.addItem(name, code)
        chosen = self.store.setting("language", "auto")
        self.language_combo.setCurrentIndex(max(0, self.language_combo.findData(chosen)))
        self.language_combo.setToolTip(tr("Zmiana języka przebudowuje okno; wypełnione ścieżki zostają."))
        self.language_combo.currentIndexChanged.connect(self._change_language)
        look.add(QLabel(tr("Język:")))
        look.add(self.language_combo)

        self.theme_combo = QComboBox()
        self.theme_combo.addItem(tr("Ciemny"), "dark")
        self.theme_combo.addItem(tr("Jasny"), "light")
        current_theme = self.store.setting("theme", "dark")
        self.theme_combo.setCurrentIndex(0 if current_theme == "dark" else 1)
        self.theme_combo.currentIndexChanged.connect(self._change_theme)
        self.theme_combo.setToolTip(tr("Zmiana motywu działa natychmiast."))
        look.add(QLabel(tr("Motyw:")))
        look.add(self.theme_combo)

        self.welcome_cb = checkbox(
            tr("Pokazuj ekran powitalny przy starcie"),
            tr("Ekran z pytaniem, co chcesz teraz zrobić: kopia, przywracanie, sprawdzenie."),
            checked=bool(self.store.setting("show_welcome", True)),
        )
        self.welcome_cb.toggled.connect(
            lambda on: self.store.set_setting("show_welcome", bool(on))
        )
        look.add(self.welcome_cb)

        accent_row = QHBoxLayout()
        accent_row.addWidget(button(tr("Kolor wyróżnienia…"), tr("Zmienia kolor przycisków i zaznaczeń"), self._pick_accent))
        self.accent_preview = QLabel("     ")
        self.accent_preview.setFixedWidth(46)
        accent_row.addWidget(self.accent_preview)
        accent_row.addStretch(1)
        look.add_layout(accent_row)
        layout.addWidget(look)

        layout.addWidget(self._build_background_card())

        excl = Card(tr("Domyślne wykluczenia"), tr("Lista podpowiadana przy tworzeniu nowej kopii."))
        self.default_excludes_edit = QPlainTextEdit(
            "\n".join(self.store.setting("default_excludes", DEFAULT_EXCLUDES))
        )
        self.default_excludes_edit.setFixedHeight(140)
        excl.add(self.default_excludes_edit)
        excl_row = QHBoxLayout()
        excl_row.addWidget(button(tr("Zapisz"), tr("Zapisuje listę jako domyślną"), self._save_default_excludes, object_name="Primary"))
        excl_row.addWidget(button(tr("Przywróć fabryczne"), tr("Wraca do listy wbudowanej w program"), lambda: self.default_excludes_edit.setPlainText("\n".join(DEFAULT_EXCLUDES))))
        excl_row.addStretch(1)
        excl.add_layout(excl_row)
        layout.addWidget(excl)

        env = Card(tr("Środowisko"), tr("Informacje przydatne przy zgłaszaniu problemu."))
        kdf = (
            tr("Argon2id — {passes} przebiegi, {memory} MiB, {threads} wątki").format(
                passes=crypto.ARGON2_TIME_COST,
                memory=crypto.ARGON2_MEMORY_KIB // 1024,
                threads=crypto.ARGON2_PARALLELISM,
            )
            if crypto.ARGON2_AVAILABLE
            else tr("PBKDF2-HMAC-SHA256 — {count} iteracji").format(
                count=f"{crypto.PBKDF2_ITERATIONS:,}".replace(",", " ")
            )
        )
        env.add(field_help(
            tr("Szyfrowanie: AES-256-GCM (uwierzytelnione)\nWyprowadzanie klucza: {kdf}").format(kdf=kdf)
        ))
        env.add(field_help(tr("Magazyn haseł: {backend}").format(backend=secrets_store.describe())))
        env.add(field_help(tr("Dane aplikacji: {path}").format(path=data_dir())))
        env.add(field_help(tr("Dziennik: {path}").format(path=log_dir())))
        env_row = QHBoxLayout()
        env_row.addWidget(button(tr("Otwórz katalog danych"), tr("Pokazuje folder z ustawieniami i szablonami"), lambda: self._open_path(data_dir())))
        env_row.addWidget(button(tr("Otwórz katalog dziennika"), tr("Pokazuje folder z plikami dziennika"), lambda: self._open_path(log_dir())))
        env_row.addWidget(button(
            tr("Usuń zapamiętane hasła…"),
            tr("Usuwa z Menedżera poświadczeń Windows wszystkie hasła zapamiętane przez program — "
               "na przykład przed odinstalowaniem"),
            self._forget_all_passwords,
        ))
        env_row.addStretch(1)
        env.add_layout(env_row)
        layout.addWidget(env)
        layout.addStretch(1)
        return page

    def _build_background_card(self) -> QWidget:
        card = Card(
            tr("Kopie planowe i praca w tle"),
            tr("Harmonogram działa wtedy, gdy działa program — także ukryty przy zegarze."),
        )
        self.autostart_cb = checkbox(
            tr("Uruchamiaj program w tle przy logowaniu do Windows"),
            tr("Bez tego kopia planowa ruszy dopiero wtedy, gdy sam otworzysz program."),
            checked=autostart.is_enabled(),
        )
        self.autostart_cb.setEnabled(autostart.supported())
        self.autostart_cb.toggled.connect(self._toggle_autostart)
        card.add(self.autostart_cb)
        if autostart.packaged():
            card.add(field_help(tr("Ten sam przełącznik jest w Ustawieniach Windows → Aplikacje → "
                                   "Uruchamianie. Wyłączony tam da się włączyć tylko tam.")))
        elif not autostart.supported():
            card.add(field_help(tr("Dostępne w zainstalowanej wersji programu (plik EXE).")))

        self.background_cb = checkbox(
            tr("Po zamknięciu okna działaj dalej przy zegarze, gdy są kopie planowe"),
            tr("Zamknięcie okna chowa je, a harmonogram pilnuje terminów. Program zamkniesz "
               "z menu ikony przy zegarze."),
            checked=bool(self.store.setting("run_in_background", True)),
        )
        self.background_cb.toggled.connect(lambda on: self.store.set_setting("run_in_background", bool(on)))
        card.add(self.background_cb)

        self.pause_cb = checkbox(
            tr("Wstrzymaj kopie planowe"),
            tr("Harmonogram nie uruchamia kopii, dopóki tego nie odznaczysz. Ręczne kopie działają."),
            checked=bool(self.store.setting("schedule_paused", False)),
        )
        self.pause_cb.toggled.connect(self._set_schedule_paused)
        card.add(self.pause_cb)
        return card

    def _forget_all_passwords(self) -> None:
        """Hasła w Menedżerze poświadczeń przeżywają odinstalowanie programu — tu da się je usunąć."""
        answer = QMessageBox.question(
            self,
            tr("Usuń zapamiętane hasła"),
            tr("Program usunie z Menedżera poświadczeń Windows wszystkie hasła, które zapamiętał: "
               "hasła kopii i dane dostępu do kopii poza domem. Kopie planowe szablonów "
               "zaszyfrowanych będą potem czekać, aż podasz hasło.\n\nUsunąć?"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        removed = 0
        for template in self.store.templates().values():
            for name in (template.id, cloud.OFFSITE_KEY.format(template.id), cloud.OFFSITE_PASSWORD.format(template.id)):
                removed += bool(secrets_store.delete_password(name))
            if template.remember_password:
                template.remember_password = False
                self.store.put_template(template)
        self._set_status(tr("Usunięte zapamiętane hasła: {count}.").format(count=removed))

    def _toggle_autostart(self, enabled: bool) -> None:
        if not autostart.set_enabled(enabled):
            self.autostart_cb.blockSignals(True)
            self.autostart_cb.setChecked(autostart.is_enabled())
            self.autostart_cb.blockSignals(False)
            if enabled and autostart.blocked_in_windows():
                QMessageBox.information(
                    self,
                    tr("Start przy logowaniu"),
                    tr("Start programu przy logowaniu wyłączono w Ustawieniach Windows. Włączysz go "
                       "tam: Ustawienia → Aplikacje → Uruchamianie → Sigelith Backup."),
                )
                return
            self._set_status(tr("Nie udało się zmienić startu przy logowaniu — szczegóły w dzienniku."))

    def _wizard_button(self) -> QPushButton:
        """Kreator kopii — na ekranie kopii i na liście szablonów, bo tworzy kopię, a nie ustawia program."""
        return button(
            tr("Nowa kopia krok po kroku…"),
            tr("Ustawia kopię krok po kroku i zapisuje ją jako szablon"),
            self.run_setup_wizard,
            icon="stars",
        )

    def _change_theme(self) -> None:
        theme = self.theme_combo.currentData()
        self.store.set_setting("theme", theme)
        self._apply_theme()
        self._set_status(
            tr("Motyw zmieniony na {theme}.").format(theme=self.theme_combo.currentText().lower())
        )

    def _change_language(self) -> None:
        """Przełącza język i przebudowuje okno — teksty powstają przy budowie."""
        code = self.language_combo.currentData()
        if code == self.store.setting("language", "auto"):
            return
        if self.worker is not None and self.worker.isRunning():
            QMessageBox.information(
                self,
                tr("Trwa operacja"),
                tr("Język zmienisz po zakończeniu bieżącej operacji."),
            )
            previous = self.store.setting("language", "auto")
            self.language_combo.setCurrentIndex(max(0, self.language_combo.findData(previous)))
            return
        self.store.set_setting("language", code)
        qtlang.apply(i18n.set_language(code))
        self._rebuild_ui()
        self._set_status(tr("Język interfejsu zmieniony."))

    def _form_state(self) -> dict[str, object]:
        """Zapamiętuje to, co użytkownik wpisał — przebudowa okna ma tego nie zgubić.

        Haseł celowo nie przenosimy: trzymanie ich w dodatkowym miejscu pamięci
        nie jest warte oszczędzenia jednego wpisania.
        """
        return {
            "sources": self.source_list.paths(),
            "destination": self.dest_picker.path(),
            "dated": self.structure_dated.isChecked(),
            "encrypt": self.encrypt_cb.isChecked(),
            "verify": self.verify_cb.isChecked(),
            "thorough": self.thorough_cb.isChecked(),
            "delta": self.delta_cb.isChecked(),
            "timestamp": self.timestamp_cb.isChecked(),
            "sigelith": self.sigelith_cb.isChecked(),
            "delete_removed": self.delete_removed_cb.isChecked(),
            "stamp_updates": self.stamp_updates_cb.isChecked(),
            "retention": self._retention_values(),
            "catchup": self.catchup_spin.value(),
            "workers": self.workers_spin.value(),
            "excludes": self.excludes_edit.toPlainText(),
            "restore_src": self.restore_src.path(),
            "restore_dst": self.restore_dst.path(),
            "browse_root": self.browser.picker.path(),
            "page": self.stack.currentIndex(),
        }

    def _apply_form_state(self, state: dict[str, object]) -> None:
        self.source_list.set_paths(list(state["sources"]))
        self.dest_picker.set_path(str(state["destination"]))
        self.structure_dated.setChecked(bool(state["dated"]))
        self.structure_mirror.setChecked(not state["dated"])
        self.encrypt_cb.setChecked(bool(state["encrypt"]))
        self.verify_cb.setChecked(bool(state["verify"]))
        self.thorough_cb.setChecked(bool(state["thorough"]))
        self.delta_cb.setChecked(bool(state["delta"]))
        self.timestamp_cb.setChecked(bool(state["timestamp"]))
        self.sigelith_cb.setChecked(bool(state["sigelith"]))
        self.delete_removed_cb.setChecked(bool(state["delete_removed"]))
        self.stamp_updates_cb.setChecked(bool(state["stamp_updates"]))
        values = dict(state["retention"])
        self._set_retention(values["retention"], values["gfs_daily"], values["gfs_weekly"], values["gfs_monthly"])
        self.catchup_spin.setValue(int(state["catchup"]))
        self.workers_spin.setValue(int(state["workers"]))
        self.excludes_edit.setPlainText(str(state["excludes"]))
        self.restore_src.set_path(str(state["restore_src"]))
        self.restore_dst.set_path(str(state["restore_dst"]))
        if state["browse_root"]:
            self.browser.open_backup(str(state["browse_root"]))
        self._go_to(int(state["page"]))

    def _rebuild_ui(self) -> None:
        state = self._form_state()
        self._build_ui()
        self._apply_theme()
        self._connect_logging()
        if self.tray is not None:
            self.tray.rebuild_menu()
        self._refresh_templates()
        self._apply_form_state(state)
        self._update_backup_readiness()

    def _pick_accent(self) -> None:
        current = QColor(effective_accent(self.store.setting("accent")))
        chosen = QColorDialog.getColor(current, self, tr("Kolor wyróżnienia"))
        if chosen.isValid():
            self.store.set_setting("accent", chosen.name())
            self._apply_theme()

    def _save_default_excludes(self) -> None:
        patterns = [line.strip() for line in self.default_excludes_edit.toPlainText().splitlines() if line.strip()]
        self.store.set_setting("default_excludes", patterns)
        self._set_status(tr("Domyślne wykluczenia zapisane."))

    def _apply_theme(self) -> None:
        theme = self.store.setting("theme", "dark")
        accent = effective_accent(self.store.setting("accent"))
        self.setStyleSheet(build_stylesheet(theme, accent))
        palette = palette_for(theme, accent)
        icons.repaint_all(self, palette)
        for hint in self.findChildren(Hint):
            hint.refresh_icon()
        self._refresh_history()
        if hasattr(self, "accent_preview"):
            self.accent_preview.setStyleSheet(f"background:{accent}; border-radius:5px;")

    @staticmethod
    def _open_path(path: Path) -> None:
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

    # ------------------------------------------------------------ ekran dziennika

    def _build_log_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(16)

        layout.addWidget(
            page_title(tr("Dziennik"), tr("Przebieg operacji na żywo. Pełna historia trafia do pliku."))
        )
        layout.addWidget(
            Hint(
                tr("Jeśli operacja zakończy się błędem, skopiuj stąd ostatnie wiersze — "
                   "zawierają dokładną przyczynę, a nie tylko komunikat ogólny.")
            )
        )

        card = Card(tr("Zapis bieżącej sesji"))
        self.log_view = QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setMinimumHeight(400)
        self.log_view.setMaximumBlockCount(3000)
        card.add(self.log_view)
        row = QHBoxLayout()
        row.addWidget(button(tr("Otwórz plik dziennika"), tr("Otwiera pełny dziennik w domyślnym edytorze"), lambda: self._open_path(log_dir() / "cleanvault.log")))
        row.addWidget(button(tr("Wyczyść widok"), tr("Czyści tylko okno — plik dziennika pozostaje"), self.log_view.clear))
        row.addStretch(1)
        card.add_layout(row)
        layout.addWidget(card)
        layout.addStretch(1)
        return page

    def _connect_logging(self) -> None:
        self._log_relay = LogRelay()
        self._log_relay.message.connect(self._append_log)
        bridge.set_sink(lambda text, level: self._log_relay.message.emit(text, level))

    def _append_log(self, text: str, level: int) -> None:
        self.log_view.appendPlainText(text)

    # ---------------------------------------------------------- ekran o programie

    def _build_about_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(16)

        layout.addWidget(page_title(tr("O programie"), f"{__app_name__} {__version__}"))

        about = Card(tr("Czym jest {app}").format(app=__app_name__))
        about.add(
            field_help(
                tr("Kopie zapasowe folderów na dysk zewnętrzny, z historią wersji i szyfrowaniem. "
                   "Wszystko dzieje się na Twoim komputerze, bez konta i bez telemetrii. Z internetem "
                   "program łączy się tylko wtedy, gdy sam włączysz kopię poza domem albo znaczniki "
                   "czasu Sigelith.")
            )
        )
        layout.addWidget(about)

        features = Card(tr("Jak to działa"))
        features.add(
            field_help(
                tr("• Kopia przyrostowa — zapisywane są wyłącznie pliki nowe i zmienione.\n"
                   "  Porównanie opiera się na spisie treści kopii, rozmiarze i dacie modyfikacji;\n"
                   "  przy różnicy liczona jest suma kontrolna SHA-256.\n\n"
                   "• Wersje z datą — każdy przebieg tworzy kompletny folder z datą, a pliki\n"
                   "  niezmienione są podpinane twardym dowiązaniem, więc nie zajmują miejsca dwa razy.\n\n"
                   "• Weryfikacja po zapisie — zapisany plik jest odczytywany z powrotem\n"
                   "  i porównywany ze źródłem.\n\n"
                   "• Odporność na przerwania — pliki powstają pod nazwą tymczasową i są\n"
                   "  podmieniane dopiero po pełnym zapisie.")
            )
        )
        layout.addWidget(features)

        security = Card(tr("Kryptografia"), tr("Dokładnie to, co program realnie stosuje."))
        kdf_line = (
            tr("Argon2id (t={passes}, {memory} MiB, p={threads})").format(
                passes=crypto.ARGON2_TIME_COST,
                memory=crypto.ARGON2_MEMORY_KIB // 1024,
                threads=crypto.ARGON2_PARALLELISM,
            )
            if crypto.ARGON2_AVAILABLE
            else tr("PBKDF2-HMAC-SHA256, {count} iteracji").format(
                count=f"{crypto.PBKDF2_ITERATIONS:,}".replace(",", " ")
            )
        )
        security.add(
            field_help(
                tr("• Szyfr: AES-256 w trybie GCM (szyfrowanie z uwierzytelnieniem).\n"
                   "• Wyprowadzanie klucza z hasła: {kdf}.\n"
                   "• Nagłówek każdego pliku jest uwierzytelniony jako AAD — podmiana parametrów\n"
                   "  unieważnia tag.\n"
                   "• Każdy plik dostaje losowy, niepowtarzalny nonce.\n"
                   "• Odszyfrowany plik powstaje dopiero po pomyślnej weryfikacji tagu.\n"
                   "• Hasła nie są zapisywane w plikach programu. Opcjonalnie trafiają do\n"
                   "  Menedżera poświadczeń Windows.").format(kdf=kdf_line)
            )
        )
        security.add(
            Hint(
                tr("Hasła nie da się odzyskać ani zresetować. Jeśli je zgubisz, dane z kopii "
                   "zaszyfrowanej są bezpowrotnie stracone — tak działa poprawne szyfrowanie."),
                icon="exclamation-triangle",
            )
        )
        layout.addWidget(security)

        credits = Card(tr("Licencje i prywatność"))
        credits.add(field_help(tr("© {years} {publisher}. Wolne oprogramowanie na licencji GNU GPL "
                                  "w wersji 3 lub nowszej.").format(years="2025–2026", publisher=__publisher__)))
        credits.add(
            field_help(
                tr("Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0, z Pythona i z innych "
                   "składników na licencjach otwartych (m.in. MIT, BSD, Apache 2.0); ikony: Bootstrap "
                   "Icons (MIT). Wykaz, prawa autorskie, pełne teksty licencji i adresy kodu źródłowego "
                   "Qt są pod przyciskiem „Licencje”.")
            )
        )
        legal_row = QHBoxLayout()
        legal_row.addWidget(button(tr("Licencje…"), tr("Licencja programu i licencje użytych składników"),
                                   lambda: LegalDialog(self).exec(), icon="journal-text"))
        legal_row.addWidget(button(tr("Polityka prywatności…"), tr("Jakie dane program przetwarza i gdzie"),
                                   lambda: PrivacyDialog(self).exec(), icon="shield-check"))
        legal_row.addWidget(button(tr("Kod źródłowy"), tr("Kod źródłowy programu w serwisie GitHub"),
                                   lambda: QDesktopServices.openUrl(QUrl(__source__)), icon="code-slash"))
        legal_row.addStretch(1)
        credits.add_layout(legal_row)
        layout.addWidget(credits)
        layout.addStretch(1)
        return page

    # ------------------------------------------------------- wspólna obsługa zadań

    def _make_keyring(self, password: str) -> crypto.PasswordKeyring:
        return crypto.PasswordKeyring(password)

    def _run_job(self, job, panel: OperationPanel, on_success, description: str, total_bytes: int | None) -> None:
        if self.worker is not None and self.worker.isRunning():
            QMessageBox.information(self, tr("Operacja w toku"), tr("Poczekaj na zakończenie bieżącej operacji."))
            return

        self.tracker = ProgressTracker(total_bytes or 0)
        self._active_panel = panel
        panel.set_busy(True)
        panel.set_stage(tr("Przygotowanie…"))
        panel.set_progress(0, "")

        worker = EngineWorker(job, description)
        self.worker = worker
        worker.stage_changed.connect(panel.set_stage)
        worker.file_changed.connect(panel.set_file)
        worker.bytes_advanced.connect(self._on_bytes)
        worker.succeeded.connect(lambda result: self._on_job_done(panel, on_success, result))
        self._last_error = None
        worker.error.connect(self._remember_error)
        worker.failed.connect(lambda message: self._on_job_failed(panel, message))
        worker.finished.connect(self._on_worker_finished)
        worker.start()

        self._update_backup_readiness()
        self._update_restore_readiness()
        self._set_status(tr("Trwa: {description}…").format(description=description))

    def _on_bytes(self, delta: int) -> None:
        if self.tracker is None:
            return
        self.tracker.advance(delta)
        self._active_panel.set_progress(self.tracker.percent, self.tracker.describe())

    def _on_job_done(self, panel: OperationPanel, on_success, result) -> None:
        panel.set_busy(False)
        panel.set_stage(tr("Zakończono."))
        on_success(result)

    def _on_job_failed(self, panel: OperationPanel, message: str) -> None:
        self._after_worker = None
        panel.set_busy(False)
        live_id, self._live_run = self._live_run, None
        service = getattr(self, "scheduler_service", None)
        if live_id and service is not None:
            if isinstance(self._last_error, engine.MassChangeDetected):
                # nie ponawiamy co kilka minut — czekamy na człowieka (ręczna kopia zwalnia)
                service.live_tracker.hold(live_id)
            else:
                service.live_tracker.finished(live_id, False)
        if isinstance(self._last_error, engine.MassChangeDetected):
            self._handle_mass_change(panel, self._last_error)
            return
        if isinstance(self._last_error, engine.PrivateAppDataTargets):
            self._handle_private_appdata(panel, self._last_error)
            return
        panel.set_stage(tr("Operacja nie powiodła się."))
        self._set_status(tr("Operacja zakończona błędem."))
        if self._unattended:
            self._notify(tr("Kopia planowa nie powiodła się"), message, warning=True)
            return
        QMessageBox.critical(
            self,
            tr("Nie udało się wykonać operacji"),
            tr("{message}\n\nSzczegóły techniczne znajdziesz w zakładce „Dziennik”.").format(
                message=message
            ),
        )

    def _on_worker_finished(self) -> None:
        worker, self.worker = self.worker, None
        if worker is not None:
            worker.wait(2000)
        self._update_backup_readiness()
        self._update_restore_readiness()
        self._refresh_history()
        follow_up, self._after_worker = self._after_worker, None
        if follow_up is not None and not self._closing:
            QTimer.singleShot(0, follow_up)
        elif follow_up is None:
            self._unattended = False

    def _cancel_operation(self) -> None:
        if self.worker is not None and self.worker.isRunning():
            self.worker.cancel()
            self._set_status(tr("Przerywanie operacji…"))

    def _report_result(
        self, result: engine.OperationResult, title: str, hint: str = "", unattended: bool = False,
        quiet: bool = False,
    ) -> None:
        self._set_status(result.summary)
        if self._closing:
            return
        if unattended:
            if result.cancelled:
                return  # przerwanie (np. wyłączanie komputera) — kopia dokończy się później
            if result.ok and quiet:
                return  # dogrywka „na bieżąco” — powiadomienie co kilka minut byłoby szumem
            if result.ok:
                self._notify(tr("{title} — gotowe").format(title=title), result.summary)
            else:
                self._notify(
                    tr("{title} — zakończono z błędami").format(title=title),
                    tr("{summary} Szczegóły znajdziesz w programie, w zakładce „Dziennik”.").format(
                        summary=result.summary
                    ),
                    warning=True,
                )
            return
        notes = "".join(f"\n\n{note}" for note in result.notes)
        if hint:
            notes += f"\n\n{hint}"
        if result.cancelled:
            QMessageBox.information(
                self,
                tr("{title} — przerwano").format(title=title),
                tr("{summary}{notes}\n\nPliki zapisane przed przerwaniem są kompletne "
                   "i zostały odnotowane w spisie treści kopii.\n\n"
                   "Aby dokończyć kopię, uruchom ją ponownie — program zaproponuje uzupełnienie "
                   "tej wersji zamiast tworzenia nowej.").format(summary=result.summary, notes=notes),
            )
            return
        if result.ok:
            extra = (
                tr("\n\nLokalizacja:\n{path}").format(path=result.output_path)
                if result.output_path
                else ""
            )
            QMessageBox.information(
                self,
                tr("{title} — gotowe").format(title=title),
                f"{result.summary}{extra}{notes}",
            )
            return

        preview = "\n".join(f"• {line}" for line in result.errors[:8])
        more = (
            tr("\n\n…i kolejne: {count}.").format(count=len(result.errors) - 8)
            if len(result.errors) > 8
            else ""
        )
        QMessageBox.warning(
            self,
            tr("{title} — zakończono z błędami").format(title=title),
            tr("{summary}\n\nProblemy:\n{problems}\n\n"
               "Pełna lista znajduje się w zakładce „Dziennik”.").format(
                summary=result.summary, problems=f"{preview}{more}{notes}"
            ),
        )

    # ----------------------------------------------------------- praca w tle

    def _setup_background(self) -> None:
        self.scheduler_service = SchedulerService(self.store, self)
        self.scheduler_service.due.connect(self._run_scheduled)
        self.scheduler_service.overdue.connect(self._remind_overdue)
        if Tray.available():
            self.tray = Tray(self.windowIcon(), self)
            self.tray.show_requested.connect(self.bring_to_front)
            self.tray.backup_requested.connect(self._backup_from_tray)
            self.tray.pause_toggled.connect(self._set_schedule_paused)
            self.tray.quit_requested.connect(self.quit_from_tray)
            self.tray.set_paused(self.scheduler_service.paused)
            self.tray.show()
        self.scheduler_service.start()

    def _refresh_tray(self) -> None:
        if self.tray is None:
            return
        names = sorted(
            ((t.id, t.name) for t in self.store.templates().values()), key=lambda pair: pair[1].lower()
        )
        self.tray.set_templates(names)

    def _should_hide_to_tray(self) -> bool:
        return (
            not self._quitting
            and self.tray is not None
            and bool(self.store.setting("run_in_background", True))
            and self.scheduler_service.has_schedules()
        )

    def _notify(self, title: str, text: str, warning: bool = False) -> None:
        if self.tray is not None:
            self.tray.notify(title, text, warning)
        else:
            log.info("Powiadomienie (brak zasobnika): %s — %s", title, text)

    def _run_scheduled(self, template_id: str, reason: str) -> None:
        template = self.store.get_template(template_id)
        if template is None:
            return
        if self.worker is not None and self.worker.isRunning():
            log.info("Termin kopii „%s” — trwa inna operacja, sprawdzę ponownie.", template.name)
            return
        template.last_attempt = time.time()
        self.store.put_template(template)
        log.info("Kopia planowa „%s” (%s).", template.name, reason)
        # „Na bieżąco”: każda kopia z harmonogramu (zmiany albo podłączenie dysku)
        # dogrywa do dzisiejszej wersji zamiast tworzyć nową (cleanvault/live.py).
        self._run_template_now(template, unattended=True, live=template.schedule == scheduler.LIVE)

    def _backup_from_tray(self, template_id: str) -> None:
        template = self.store.get_template(template_id)
        if template is None:
            return
        if self.worker is not None and self.worker.isRunning():
            self._notify(tr("Trwa operacja"), tr("Poczekaj na zakończenie bieżącej operacji."))
            return
        # Z zasobnika bez okna: zachowujemy się jak kopia planowa, ale wynik i tak
        # trafia do powiadomienia — okno mogło pozostać ukryte.
        self._run_template_now(template, unattended=not self.isVisible())

    def _remind_overdue(self, template_id: str) -> None:
        template = self.store.get_template(template_id)
        if template is None:
            return
        reference = template.last_success or template.created
        days = int((time.time() - reference) // 86400)
        self._notify(
            tr("Kopia „{name}” czeka").format(name=template.name),
            tr("Od {days} dni nie było udanej kopii. Podłącz dysk docelowy albo otwórz "
               "program, żeby sprawdzić, co się dzieje.").format(days=days),
            warning=True,
        )

    def _set_schedule_paused(self, paused: bool) -> None:
        self.scheduler_service.set_paused(paused)
        if self.tray is not None:
            self.tray.set_paused(paused)
        if hasattr(self, "pause_cb"):
            self.pause_cb.blockSignals(True)
            self.pause_cb.setChecked(paused)
            self.pause_cb.blockSignals(False)

    def bring_to_front(self) -> None:
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def quit_from_tray(self) -> None:
        self._quitting = True
        if not self.isVisible() and self.worker is not None and self.worker.isRunning():
            # pytanie o przerwanie kopii ma być widoczne, a nie ukryte za niewidocznym oknem
            self.bring_to_front()
        self.close()
        if self.isVisible() or (self.worker is not None and self.worker.isRunning()):
            self._quitting = False  # użytkownik zrezygnował z zamykania

    def handle_instance_message(self, message: str) -> None:
        """Druga instancja programu prosi o pokazanie okna (np. start z menu Start)."""
        if message == MSG_SHOW:
            self.bring_to_front()

    # -------------------------------------------------------- kreator i powitanie

    def greet(self) -> None:
        """Pierwszy kontakt z programem: kreator albo ekran powitalny.

        Wołane po ``show()``, a nie w konstruktorze — okno ma być już widoczne,
        zanim pojawi się nad nim cokolwiek modalnego. Przy pierwszym
        uruchomieniu (brak szablonów i brak śladu po kreatorze) prowadzimy przez
        ustawienia; później pytamy tylko, co użytkownik chce teraz zrobić.
        """
        if not self.store.templates() and not self.store.setting("wizard_done", False):
            self.run_setup_wizard()
            return
        if self.store.setting("show_welcome", True):
            self.show_welcome()

    def show_welcome(self) -> None:
        dialog = WelcomeDialog(self.store, self)
        dialog.exec()
        choice = dialog.choice
        if choice == WelcomeDialog.WIZARD:
            self.run_setup_wizard()
        elif choice == WelcomeDialog.BACKUP:
            self._go_to(self.PAGE_BACKUP)
        elif choice == WelcomeDialog.RESTORE:
            self._go_to(self.PAGE_RESTORE)
        elif choice == WelcomeDialog.VERIFY:
            self._go_to(self.PAGE_RESTORE)
            self.verify_btn.setFocus()
            self._set_status(tr("Wskaż folder kopii i kliknij „Sprawdź kopię”."))
        elif choice == WelcomeDialog.SETTINGS:
            self._go_to(self.PAGE_SETTINGS)

    def run_setup_wizard(self) -> None:
        wizard = SetupWizard(self.store, self)
        wizard.exec()
        outcome = wizard.result_choice
        self._refresh_templates()
        if outcome is None:
            # Rezygnacja z kreatora nie może go przywoływać przy każdym starcie.
            self.store.set_setting("wizard_done", True)
            return
        if outcome.template.schedule != scheduler.MANUAL:
            self._ensure_autostart()
        self._apply_template_to_form(outcome.template)
        password = wizard.password_value()
        if password:
            self.password_field.set_password(password)
            self.password_confirm.setText(password)
        self._update_backup_readiness()
        self._set_status(tr("Zapisano szablon „{name}”.").format(name=outcome.template.name))
        if outcome.start_now:
            self._start_backup()

    # ------------------------------------------------------------------ zamykanie

    def closeEvent(self, event) -> None:
        if self._should_hide_to_tray():
            # Kopie planowe działają tylko wtedy, gdy działa program — zamknięcie
            # okna go chowa, a trwająca kopia biegnie dalej. Koniec: menu w zasobniku.
            event.ignore()
            self.hide()
            if not self.store.setting("tray_hint_shown", False):
                self.store.set_setting("tray_hint_shown", True)
                self._notify(
                    tr("Sigelith Backup działa w tle"),
                    tr("Kopie planowe wykonają się o czasie. Program zamkniesz z menu ikony "
                       "przy zegarze."),
                )
            return
        if self.worker is not None and self.worker.isRunning():
            answer = QMessageBox.question(
                self,
                tr("Operacja w toku"),
                tr("Trwa operacja na plikach. Zamknięcie programu ją przerwie.\n\n"
                   "Pliki zapisane do tej chwili zostaną zachowane, a kopię będzie można "
                   "później dokończyć.\n\nZamknąć mimo to?"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if answer != QMessageBox.StandardButton.Yes:
                event.ignore()
                return
            self._closing = True
            self._wait_for_worker_to_stop()
        try:
            self.store.save()
        except OSError as exc:
            log.error("Nie udało się zapisać stanu przy zamykaniu: %s", exc)
        log.info("Zamykanie aplikacji.")
        if self.tray is not None:
            self.tray.hide()
        self.scheduler_service.stop()
        self.browser.shutdown()
        event.accept()
        app = QApplication.instance()
        if app is not None and not app.quitOnLastWindowClosed():
            app.quit()

    def _on_session_ending(self, _manager) -> None:
        """Wyłączanie komputera albo wylogowanie w trakcie kopii.

        Nie pytamy o nic — użytkownik już zdecydował. Przerywamy operację,
        a silnik utrwala punkt kontrolny; przy następnym uruchomieniu kopię
        da się dokończyć.
        """
        if self.worker is None or not self.worker.isRunning():
            return
        log.info("System kończy sesję w trakcie operacji — przerywam i utrwalam stan kopii.")
        self._closing = True
        self._wait_for_worker_to_stop(SESSION_END_WAIT_SECONDS)
        with contextlib.suppress(OSError):
            self.store.save()

    def _wait_for_worker_to_stop(self, timeout: float = CLOSE_WAIT_SECONDS) -> None:
        """Przerywa operację i czeka, aż silnik zapisze spis treści kopii.

        Wcześniej okno czekało 5 sekund i zamykało się niezależnie od wyniku.
        Zapis manifestu dużej kopii na dysk USB trwa dłużej, więc proces ginął
        w trakcie — a wraz z nim informacja o tym, co zdążyło się skopiować.
        """
        worker = self.worker
        if worker is None:
            return
        worker.cancel()
        self._set_status(tr("Przerywanie — zapisuję spis treści kopii, nie wyłączaj komputera…"))
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            deadline = time.monotonic() + timeout
            while worker.isRunning() and time.monotonic() < deadline:
                QApplication.processEvents(QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents, 100)
                worker.wait(100)
            if worker.isRunning():
                log.error(
                    "Operacja nie zakończyła się w %d s od przerwania — zamykam mimo to.",
                    timeout,
                )
        finally:
            QApplication.restoreOverrideCursor()
