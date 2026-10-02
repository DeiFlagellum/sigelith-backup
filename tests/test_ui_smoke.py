"""Testy dymne interfejsu.

Uruchamiają się na platformie ``offscreen``, więc działają też w CI bez pulpitu.
Sprawdzają, że okno daje się zbudować, wszystkie ekrany się renderują,
a logika włączania/wyłączania kontrolek zachowuje się zgodnie z opisem.
"""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication, QPushButton, QWidget

from cleanvault import __publisher__, i18n
from cleanvault.state import StateStore
from cleanvault.ui.main_window import MainWindow
from cleanvault.ui.widgets import FlowLayout, estimate_strength


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture()
def window(qapp, tmp_path, monkeypatch):
    monkeypatch.setattr("cleanvault.state.state_file", lambda: tmp_path / "state.msgpack")
    monkeypatch.setattr("cleanvault.ui.main_window.StateStore", lambda: StateStore(tmp_path / "state.msgpack"))
    win = MainWindow()
    yield win
    win.close()


def test_admin_banner_only_when_elevated(qapp, tmp_path, monkeypatch):
    monkeypatch.setattr("cleanvault.state.state_file", lambda: tmp_path / "state.msgpack")
    monkeypatch.setattr("cleanvault.ui.main_window.is_admin", lambda: True)
    elevated = MainWindow(StateStore(tmp_path / "state.msgpack"))
    assert "administratora" in elevated.admin_banner.text()
    elevated.close()

    monkeypatch.setattr("cleanvault.ui.main_window.is_admin", lambda: False)
    normal = MainWindow(StateStore(tmp_path / "state.msgpack"))
    assert not hasattr(normal, "admin_banner")
    normal.close()


def test_window_builds_all_pages(window):
    assert window.stack.count() == len(MainWindow.PAGES) == 7
    for index in range(window.stack.count()):
        window._go_to(index)
        assert window.stack.currentIndex() == index


def test_button_rows_wrap_instead_of_scrolling_sideways(qapp):
    """1920×1080 przy skali 150% to 1280 px logicznych — rząd ośmiu przycisków na stronie
    przywracania się nie mieścił i chował „Przywróć pliki” za poziomym przewijaniem
    (2026-09-30). FlowLayout przenosi przyciski do następnego wiersza."""
    host = QWidget()
    flow = FlowLayout(host, spacing=10)
    buttons = [QPushButton(f"Przycisk {i}") for i in range(8)]
    for btn in buttons:
        btn.setFixedSize(150, 36)
        flow.addWidget(btn)
    assert flow.heightForWidth(8 * 160) == 36  # jeden wiersz
    assert flow.heightForWidth(4 * 160) == 2 * 36 + 10  # dwa wiersze po cztery
    assert flow.heightForWidth(150) == 8 * 36 + 7 * 10  # wąsko: jeden pod drugim
    assert flow.minimumSize().width() == 150  # nigdy szerzej niż najszerszy przycisk
    buttons[0].hide()
    assert flow.heightForWidth(7 * 160) == 36  # ukryty przycisk nie zajmuje miejsca


def _layout_holding(widget: QWidget):
    def search(layout):
        for index in range(layout.count()):
            item = layout.itemAt(index)
            if item.widget() is widget:
                return layout
            if item.layout() is not None and (found := search(item.layout())) is not None:
                return found
        return None

    parent = widget.parentWidget()
    while parent is not None:
        if parent.layout() is not None and (found := search(parent.layout())) is not None:
            return found
        parent = parent.parentWidget()
    return None


def test_restore_and_template_buttons_use_the_wrapping_row(window):
    assert isinstance(_layout_holding(window.restore_btn), FlowLayout)
    run = next(b for b in window.findChildren(QPushButton) if b.text().strip() == "Uruchom kopię")
    assert isinstance(_layout_holding(run), FlowLayout)


def test_run_button_disabled_without_paths(window):
    assert not window.run_btn.isEnabled()
    assert "folder źródłowy" in window.run_btn.toolTip()


def test_run_button_enables_when_form_is_complete(window, tmp_path):
    source = tmp_path / "dane"
    source.mkdir()
    window.source_list.add_path(str(source))
    window.dest_picker.set_path(str(tmp_path / "kopia"))
    assert window.run_btn.isEnabled()


def test_encryption_requires_matching_passwords(window, tmp_path):
    source = tmp_path / "dane"
    source.mkdir()
    window.source_list.add_path(str(source))
    window.dest_picker.set_path(str(tmp_path / "kopia"))

    window.encrypt_cb.setChecked(True)
    assert not window.run_btn.isEnabled(), "puste hasło nie może pozwalać na start"

    window.password_field.edit.setText("Tajne-Hasło-123")
    window.password_confirm.setText("Tajne-Hasło-124")
    assert not window.run_btn.isEnabled()
    assert "różnią" in window.password_warning.text()

    window.password_confirm.setText("Tajne-Hasło-123")
    assert window.run_btn.isEnabled()
    assert window.password_warning.text() == ""


def test_password_fields_clear_when_encryption_disabled(window):
    window.encrypt_cb.setChecked(True)
    window.password_field.edit.setText("cokolwiek")
    window.encrypt_cb.setChecked(False)
    assert window.password_field.password() == ""
    assert not window.password_field.isEnabled()


def test_structure_switch_toggles_related_options(window):
    window.structure_mirror.setChecked(True)
    assert window.delete_removed_cb.isEnabled()
    assert not window.retention_spin.isEnabled()

    assert not window.version_combo.isEnabled(), "kopia lustrzana nie ma wersji do uzupełniania"

    window.structure_dated.setChecked(True)
    assert not window.delete_removed_cb.isEnabled()
    assert not window.delete_removed_cb.isChecked()
    assert window.retention_spin.isEnabled()
    assert window.version_combo.isEnabled()


def test_restore_layout_original_disables_destination(window):
    index = window.layout_combo.findData("original")
    window.layout_combo.setCurrentIndex(index)
    assert not window.restore_dst.isEnabled()
    assert "pierwotnych" in window.layout_help.text().lower() or "pochodz" in window.layout_help.text()


def test_template_id_survives_name_with_dash(window):
    """Regresja: 1.x odzyskiwało identyfikator przez split(" — ") na etykiecie."""
    from cleanvault.state import Template

    template = Template(name="Backup — dokumenty — wersja 2")
    window.store.put_template(template)
    window._refresh_templates()

    window.template_list.setCurrentRow(0)
    assert window.selected_template_id == template.id


def test_theme_switch_applies_stylesheet(window):
    window.theme_combo.setCurrentIndex(1)  # jasny
    assert window.store.setting("theme") == "light"
    assert window.styleSheet()
    window.theme_combo.setCurrentIndex(0)
    assert window.store.setting("theme") == "dark"


def test_all_interactive_controls_have_tooltips(window):
    """UX: każdy element decyzyjny musi tłumaczyć, co robi."""
    controls = [
        window.encrypt_cb,
        window.verify_cb,
        window.thorough_cb,
        window.delete_removed_cb,
        window.retention_spin,
        window.version_combo,
        window.catchup_spin,
        window.workers_spin,
        window.stamp_updates_cb,
        window.structure_dated,
        window.structure_mirror,
        window.layout_combo,
        window.collision_combo,
        window.excludes_edit,
        window.source_list,
    ]
    missing = [c for c in controls if not c.toolTip()]
    assert not missing, f"brak podpowiedzi dla: {missing}"


@pytest.mark.parametrize(
    ("password", "minimum", "maximum"),
    [
        ("", 0, 0),
        ("haslo", 0, 1),
        ("12345678", 0, 1),
        ("aaaaaaaaaaaa", 0, 1),
        ("Lato2024!", 2, 3),
        ("K7#mQ9x!Lp2@Rv5w", 4, 4),
    ],
)
def test_password_strength_scoring(password, minimum, maximum):
    score, label, _role = estimate_strength(password)
    assert minimum <= score <= maximum, f"{password!r} -> {score} ({label})"


def test_status_bar_starts_with_guidance(window):
    assert window.statusBar().currentMessage()


# ----------------------------------------------------- wznawianie przerwanej kopii


def _interrupted_backup(tmp_path):
    """Katalog docelowy z przerwaną kopią folderu ``dane``."""
    from cleanvault import engine

    source = tmp_path / "dane"
    source.mkdir()
    for i in range(6):
        (source / f"plik{i}.bin").write_bytes(bytes([i]) * 256)
    dest = tmp_path / "kopia"
    config = engine.BackupConfig(
        sources=[str(source)], destination=str(dest), verify_after_write=False, catchup_passes=0, workers=1
    )
    plan = engine.plan_backup(config, engine.Reporter())
    seen = []
    reporter = engine.Reporter(
        on_file=lambda *_: seen.append(1), is_cancelled=lambda: len(seen) >= 3
    )
    engine.run_backup(plan, None, reporter)
    return source, dest, plan.version


def test_destination_lists_versions_and_flags_incomplete(window, tmp_path):
    _source, dest, version = _interrupted_backup(tmp_path)
    window.dest_picker.set_path(str(dest))
    window._inspect_destination_now()

    assert "niedokończone kopie: 1" in window.dest_info.text()
    index = window.version_combo.findData(version)
    assert index > 0, "niedokończona wersja nie trafiła na listę"
    assert "niedokończona" in window.version_combo.itemText(index)


def test_selected_version_goes_into_config(window, tmp_path):
    source, dest, version = _interrupted_backup(tmp_path)
    window.source_list.add_path(str(source))
    window.dest_picker.set_path(str(dest))
    window._inspect_destination_now()
    window.version_combo.setCurrentIndex(window.version_combo.findData(version))
    window.catchup_spin.setValue(2)

    config = window._current_config()
    assert config.target_version == version
    assert config.catchup_passes == 2

    window.structure_mirror.setChecked(True)
    assert window._current_config().target_version == ""


def test_start_offers_to_finish_interrupted_backup(window, tmp_path, monkeypatch):
    """Sedno zgłoszenia: ponowne uruchomienie ma zaproponować dokończenie,
    a nie po cichu zaczynać nową, pełną wersję."""
    from cleanvault import engine

    source, dest, version = _interrupted_backup(tmp_path)
    config = engine.BackupConfig(sources=[str(source)], destination=str(dest))
    info = engine.inspect_destination(dest, load_manifest=True)

    asked, started = [], []
    monkeypatch.setattr(window, "_ask_continuation", lambda run, _info: asked.append(run.name) or True)
    monkeypatch.setattr(window, "_start_backup_job", lambda cfg, *_a: started.append(cfg))

    window._continue_launch(config, None, window.backup_panel, lambda _r: None, "kopia", info)
    assert asked == [version]
    assert started[0].target_version == version


def test_choosing_new_version_keeps_default_behaviour(window, tmp_path, monkeypatch):
    from cleanvault import engine

    source, dest, _version = _interrupted_backup(tmp_path)
    config = engine.BackupConfig(sources=[str(source)], destination=str(dest))
    info = engine.inspect_destination(dest, load_manifest=True)
    started = []
    monkeypatch.setattr(window, "_ask_continuation", lambda *_a: False)
    monkeypatch.setattr(window, "_start_backup_job", lambda cfg, *_a: started.append(cfg))

    window._continue_launch(config, None, window.backup_panel, lambda _r: None, "kopia", info)
    assert started[0].target_version == ""


def test_cancel_in_dialog_starts_nothing(window, tmp_path, monkeypatch):
    from cleanvault import engine

    source, dest, _version = _interrupted_backup(tmp_path)
    config = engine.BackupConfig(sources=[str(source)], destination=str(dest))
    info = engine.inspect_destination(dest, load_manifest=True)
    started = []
    monkeypatch.setattr(window, "_ask_continuation", lambda *_a: None)
    monkeypatch.setattr(window, "_start_backup_job", lambda cfg, *_a: started.append(cfg))

    window._continue_launch(config, None, window.backup_panel, lambda _r: None, "kopia", info)
    assert started == []


def test_template_remembers_catchup_passes(window, tmp_path, monkeypatch):
    from cleanvault.state import Template

    template = Template(name="Duża kopia", catchup_passes=3)
    window.store.put_template(template)
    window._refresh_templates()
    window.template_list.setCurrentRow(0)
    assert "Dogrywka: 3" in window.template_details.text()
    window._load_template_to_form()
    assert window.catchup_spin.value() == 3


def test_closing_waits_for_worker_to_save_state(window):
    """Zamknięcie okna czeka na zapis spisu treści, zamiast ubijać wątek po 5 s."""

    class SlowWorker:
        def __init__(self):
            self.cancelled = False
            self.polls = 0

        def cancel(self):
            self.cancelled = True

        def isRunning(self):
            return self.polls < 30  # zapis spisu treści trwa wiele kolejnych prób oczekiwania

        def wait(self, _ms):
            self.polls += 1
            return not self.isRunning()

    worker = SlowWorker()
    window.worker = worker
    window._wait_for_worker_to_stop()
    window.worker = None
    assert worker.cancelled
    assert not worker.isRunning(), "okno przestało czekać, zanim wątek zakończył zapis"


def test_windows_shutdown_stops_backup_without_asking(window, monkeypatch):
    """Wyłączanie komputera w trakcie kopii: bez pytań, przerwanie i utrwalenie stanu."""
    from PySide6.QtWidgets import QMessageBox

    asked = []
    monkeypatch.setattr(QMessageBox, "question", lambda *a, **k: asked.append(a) or QMessageBox.StandardButton.No)

    class RunningWorker:
        def __init__(self):
            self.cancelled = False

        def cancel(self):
            self.cancelled = True

        def isRunning(self):
            return not self.cancelled

        def wait(self, _ms):
            return True

    worker = RunningWorker()
    window.worker = worker
    window._on_session_ending(None)
    window.worker = None
    assert worker.cancelled, "kopia nie została przerwana przy wyłączaniu systemu"
    assert window._closing, "okno pokazałoby jeszcze raporty i pytania"
    assert not asked, "przy wyłączaniu systemu nie wolno o nic pytać"


def test_saving_template_with_existing_name_replaces_it(window, tmp_path, monkeypatch):
    """Zmienione ustawienia muszą dać się wprowadzić do istniejącego szablonu."""
    from PySide6.QtWidgets import QMessageBox

    source = tmp_path / "dane"
    source.mkdir()
    window.source_list.add_path(str(source))
    window.dest_picker.set_path(str(tmp_path / "kopia"))
    monkeypatch.setattr(window, "_ask_template_settings", lambda _suggested: ("Kopia Repo+Privat", "manual", "20:00"))
    monkeypatch.setattr(QMessageBox, "question", lambda *a, **k: QMessageBox.StandardButton.Yes)

    window.verify_cb.setChecked(True)
    window._save_as_template()
    first = next(iter(window.store.templates().values()))
    assert first.verify_after_write

    window.verify_cb.setChecked(False)
    window.workers_spin.setValue(12)
    window._save_as_template()
    templates = list(window.store.templates().values())
    assert len(templates) == 1, "zamiast zastąpić, powstał drugi szablon"
    assert templates[0].id == first.id
    assert not templates[0].verify_after_write and templates[0].workers == 12


def test_default_excludes_keep_git_history_but_skip_environments():
    from cleanvault.state import DEFAULT_EXCLUDES

    assert ".git/*" not in DEFAULT_EXCLUDES
    assert {".venv/*", "venv/*", "__pycache__/*", "node_modules/*"} <= set(DEFAULT_EXCLUDES)


def test_update_stamp_switch_reaches_config_and_template(window, tmp_path, monkeypatch):
    """Przełącznik daty uzupełnienia w nazwie katalogu trafia do ustawień i do szablonu."""
    from PySide6.QtWidgets import QMessageBox

    source = tmp_path / "dane"
    source.mkdir()
    window.source_list.add_path(str(source))
    window.dest_picker.set_path(str(tmp_path / "kopia"))

    assert window.stamp_updates_cb.isChecked(), "domyślnie włączone"
    assert window._current_config().stamp_updates is True
    window.stamp_updates_cb.setChecked(False)
    assert window._current_config().stamp_updates is False

    monkeypatch.setattr(window, "_ask_template_settings", lambda _suggested: ("Bez stempla", "manual", "20:00"))
    monkeypatch.setattr(QMessageBox, "question", lambda *a, **k: QMessageBox.StandardButton.Yes)
    window._save_as_template()
    template = next(iter(window.store.templates().values()))
    assert template.stamp_updates is False

    # Wczytanie do formularza wymaga zaznaczonego szablonu — bez tego program
    # pokazuje modalne okienko, które w teście nie miałoby kto zamknąć.
    window._refresh_templates()
    window.template_list.setCurrentRow(0)
    window.stamp_updates_cb.setChecked(True)
    window._load_template_to_form()
    assert window.stamp_updates_cb.isChecked() is False, "szablon ma wrócić do formularza ze swoim ustawieniem"


def test_english_window_shows_no_polish_text(qapp, tmp_path, monkeypatch):
    """Sprawdzian końcowy: w gotowym oknie po angielsku nie zostaje polskie zdanie.

    Skan kodu (``tests/test_i18n.py``) pilnuje napisów w źródłach, ale dopiero
    zbudowane okno pokazuje, czy tekst faktycznie przeszedł przez tłumaczenie —
    np. etykiety składane przy starcie albo podpowiedzi ustawiane później.
    """
    polish = set("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ")
    monkeypatch.setattr("cleanvault.state.state_file", lambda: tmp_path / "state.msgpack")
    monkeypatch.setattr(
        "cleanvault.ui.main_window.StateStore", lambda: StateStore(tmp_path / "state.msgpack")
    )
    i18n.set_language("en")
    try:
        window = MainWindow()
        leftovers = []
        for widget in window.findChildren(QWidget):
            for attribute in ("text", "toolTip", "placeholderText", "title", "specialValueText"):
                getter = getattr(widget, attribute, None)
                if not callable(getter):
                    continue
                try:
                    value = getter()
                except TypeError:  # metoda wymaga argumentu — to nie nasz przypadek
                    continue
                if isinstance(value, str) and set(value.replace(__publisher__, "")) & polish:
                    leftovers.append(f"{type(widget).__name__}.{attribute}: {value[:60]!r}")
        window.close()
    finally:
        i18n.set_language("pl")
    assert not leftovers, leftovers


def test_language_switch_rebuilds_window_and_keeps_the_form(window, tmp_path):
    source = tmp_path / "dane"
    source.mkdir()
    window.source_list.add_path(str(source))
    window.dest_picker.set_path(str(tmp_path / "kopia"))
    window.structure_mirror.setChecked(True)
    window.catchup_spin.setValue(3)
    window._go_to(MainWindow.PAGE_SETTINGS)
    try:
        window.language_combo.setCurrentIndex(window.language_combo.findData("en"))
        assert window.run_btn.text().strip() == "Run backup"
        assert window.nav_group.button(0).text().strip() == "Backup"
        # wpisane dane i bieżący ekran przetrwały przebudowę
        assert window.source_list.paths() == [str(source)]
        assert window.dest_picker.path() == str(tmp_path / "kopia")
        assert window.structure_mirror.isChecked()
        assert window.catchup_spin.value() == 3
        assert window.stack.currentIndex() == MainWindow.PAGE_SETTINGS
        assert window.store.setting("language") == "en"
        # przebudowane okno nadal działa: przyciski reagują na formularz
        assert window.run_btn.isEnabled()
    finally:
        window.language_combo.setCurrentIndex(window.language_combo.findData("pl"))
    assert window.run_btn.text().strip() == "Uruchom kopię"


def test_wizard_is_offered_where_backups_are_made_not_in_settings(window):
    """Kreator zakłada kopię — jest na ekranie kopii i na liście szablonów, nie w Ustawieniach."""

    def wizard_buttons(page_index):
        page = window.stack.widget(page_index)
        return [b for b in page.findChildren(QPushButton) if b.text().strip() == "Nowa kopia krok po kroku…"]

    assert wizard_buttons(MainWindow.PAGE_BACKUP)
    assert wizard_buttons(MainWindow.PAGE_TEMPLATES)
    assert not wizard_buttons(MainWindow.PAGE_SETTINGS)


def test_template_dialog_offers_the_schedule_of_the_template_it_replaces(qapp):
    """Zapis pod nazwą istniejącego szablonu nie kasuje jego harmonogramu."""
    from cleanvault import scheduler
    from cleanvault.state import Template
    from cleanvault.ui.template_dialog import TemplateDialog

    existing = Template(name="Dom", schedule=scheduler.DAILY, schedule_time="06:30")
    dialog = TemplateDialog([existing], "Kopia dokumentów")
    assert dialog.values() == ("Kopia dokumentów", scheduler.MANUAL, "20:00")
    assert not dialog.time_edit.isEnabled(), "godzina tylko przy kopii codziennej"
    dialog.name_edit.setText("Dom")
    assert dialog.values() == ("Dom", scheduler.DAILY, "06:30")
    assert dialog.time_edit.isEnabled()
    dialog.close()


def test_saving_a_template_sets_its_automatic_backup(window, tmp_path, monkeypatch):
    """Harmonogram wybiera się w oknie zapisu — bez szukania go na liście szablonów."""
    from cleanvault import scheduler

    source = tmp_path / "dane"
    source.mkdir()
    window.source_list.add_path(str(source))
    window.dest_picker.set_path(str(tmp_path / "kopia"))
    autostart = []
    monkeypatch.setattr(window, "_ensure_autostart", lambda: autostart.append(True))
    monkeypatch.setattr(window, "_ask_template_settings", lambda _suggested: ("Codzienna", scheduler.DAILY, "07:15"))
    window._save_as_template()
    template = next(iter(window.store.templates().values()))
    assert (template.name, template.schedule, template.schedule_time) == ("Codzienna", scheduler.DAILY, "07:15")
    assert autostart, "kopie planowe potrzebują startu przy logowaniu"

