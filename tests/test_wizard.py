"""Testy kreatora i ekranu powitalnego.

Kreator jest sterowany tak, jak zrobiłby to użytkownik — wybór opcji, „Dalej”,
„Zapisz” — ale bez ``exec()``: okno modalne zatrzymałoby test. Liczy się to, co
kreator zostawia po sobie: szablon, ustawienia i stan formularza w oknie głównym.
"""

from __future__ import annotations

import os
import time

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication, QDialog, QLabel, QWidget

from cleanvault import i18n, paths, scheduler
from cleanvault.state import StateStore, Template
from cleanvault.ui import wizard as wizard_module
from cleanvault.ui.main_window import MainWindow
from cleanvault.ui.wizard import PROJECT_EXCLUDES, SetupWizard, Volume, WelcomeDialog


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


@pytest.fixture()
def store(tmp_path):
    return StateStore(tmp_path / "state.msgpack")


@pytest.fixture()
def folders(tmp_path):
    source = tmp_path / "dane"
    source.mkdir()
    (source / "plik.txt").write_text("treść", encoding="utf-8")
    return source, tmp_path / "kopia"


def _walk_to_summary(wizard: SetupWizard, source, destination, profile: int = 1) -> None:
    wizard.purpose_group.button(2).setChecked(True)  # „wybrane foldery”
    wizard._set_sources([str(source)])
    wizard._next()
    wizard._set_destination(str(destination))
    wizard._next()
    wizard.profile_group.button(profile).setChecked(True)
    wizard._next()
    wizard._next()  # „Kiedy?” — zostaje domyślne: codziennie o 20:00


def test_wizard_cannot_move_on_without_sources(qapp, store):
    wizard = SetupWizard(store)
    wizard.purpose_group.button(2).setChecked(True)
    wizard._set_sources([])
    assert not wizard.next_btn.isEnabled()
    assert "folder" in wizard.next_btn.toolTip().lower()
    wizard._next()
    assert wizard.steps.currentIndex() == 0


def test_destination_inside_source_is_refused(qapp, store, folders):
    source, _ = folders
    wizard = SetupWizard(store)
    wizard.purpose_group.button(2).setChecked(True)
    wizard._set_sources([str(source)])
    wizard._next()
    wizard._set_destination(str(source / "kopia"))
    assert not wizard.next_btn.isEnabled()
    assert "wewnątrz" in wizard.destination_note.text()


def test_encryption_requires_a_matching_password(qapp, store, folders):
    source, destination = folders
    wizard = SetupWizard(store)
    wizard.purpose_group.button(2).setChecked(True)
    wizard._set_sources([str(source)])
    wizard._next()
    wizard._set_destination(str(destination))
    wizard._next()
    wizard.profile_group.button(2).setChecked(True)
    assert not wizard.password_card.isHidden()
    assert not wizard.next_btn.isEnabled()
    wizard.password.set_password("długie-hasło-1")
    wizard.password_confirm.set_password("inne-hasło-12")
    assert not wizard.next_btn.isEnabled()
    wizard.password_confirm.set_password("długie-hasło-1")
    assert wizard.next_btn.isEnabled()


@pytest.mark.parametrize(
    ("profile", "structure", "encrypt"),
    [(0, "mirror", False), (1, "dated", False), (2, "dated", True)],
)
def test_profiles_become_template_settings(qapp, store, folders, profile, structure, encrypt):
    source, destination = folders
    wizard = SetupWizard(store)
    _walk_to_summary(wizard, source, destination, profile=0 if profile == 2 else profile)
    if profile == 2:
        # profil z szyfrowaniem wymaga hasła, zanim da się przejść dalej
        wizard._back()
        wizard.profile_group.button(2).setChecked(True)
        wizard.password.set_password("długie-hasło-1")
        wizard.password_confirm.set_password("długie-hasło-1")
        wizard._next()
        wizard._next()
    assert wizard.steps.currentIndex() == 4
    wizard._finish(start_now=False)

    choice = wizard.result_choice
    assert choice is not None and not choice.start_now
    saved = store.get_template(choice.template.id)
    assert saved is not None
    assert (saved.structure, saved.encrypt) == (structure, encrypt)
    assert saved.sources == [str(source)]
    assert saved.destination == str(destination)
    assert store.setting("wizard_done") is True
    # hasła nie ma w szablonie — kreator oddaje je oknu głównemu tylko na chwilę
    assert (wizard.password_value() != "") == encrypt


def test_projects_add_rebuildable_folders_to_exclusions(qapp, store, folders):
    source, destination = folders
    wizard = SetupWizard(store)
    wizard.purpose_group.button(1).setChecked(True)  # „projekty i kod”
    wizard._set_sources([str(source)])
    wizard._next()
    wizard._set_destination(str(destination))
    wizard._next()
    wizard._next()
    wizard._next()
    wizard._finish(start_now=True)
    template = wizard.result_choice.template
    assert set(PROJECT_EXCLUDES) <= set(template.excludes)
    assert wizard.result_choice.start_now


def test_summary_speaks_about_consequences(qapp, store, folders):
    source, destination = folders
    wizard = SetupWizard(store)
    _walk_to_summary(wizard, source, destination, profile=1)
    text = wizard.summary_text.text()
    assert str(source) in text
    assert str(destination) in text
    assert "folder z datą" in text
    assert wizard.medium_text.text()  # ocena nośnika zawsze coś mówi


def test_system_drive_gets_a_warning(qapp, store, folders, monkeypatch):
    source, destination = folders
    monkeypatch.setattr(wizard_module, "is_system_drive", lambda _path: True)
    wizard = SetupWizard(store)
    wizard._set_sources([str(source)])
    wizard._set_destination(str(destination))
    assert "systemowy" in wizard.destination_note.text()


def test_volumes_put_the_system_drive_last(monkeypatch):
    fake = [
        Volume("C:/", "System", "NTFS", free=900, total=1000, removable=False, system=True),
        Volume("E:/", "Mały", "EXFAT", free=10, total=64, removable=True, system=False),
        Volume("N:/", "Duży", "NTFS", free=500, total=1000, removable=False, system=False),
    ]
    ranked = wizard_module.rank_volumes(fake)
    assert [v.root for v in ranked] == ["N:/", "E:/", "C:/"]
    assert "dysk systemowy" in ranked[-1].describe()


def test_welcome_remembers_do_not_show(qapp, store):
    dialog = WelcomeDialog(store)
    dialog.hide_cb.setChecked(True)
    dialog._pick(WelcomeDialog.RESTORE)
    assert dialog.choice == WelcomeDialog.RESTORE
    assert store.setting("show_welcome") is False


def test_welcome_mentions_the_last_backup(qapp, store):
    assert "Nie było jeszcze" in WelcomeDialog(store)._last_backup_line()
    store.add_history({"action": "backup", "ok": True, "files": 3})
    assert "3 pliki" in WelcomeDialog(store)._last_backup_line()


@pytest.fixture()
def window(qapp, tmp_path, monkeypatch):
    monkeypatch.setattr("cleanvault.state.state_file", lambda: tmp_path / "state.msgpack")
    monkeypatch.setattr(
        "cleanvault.ui.main_window.StateStore", lambda: StateStore(tmp_path / "state.msgpack")
    )
    win = MainWindow()
    yield win
    win.close()


def test_first_start_opens_the_wizard(window, monkeypatch):
    opened = []
    monkeypatch.setattr(SetupWizard, "exec", lambda self: opened.append("wizard") or QDialog.DialogCode.Rejected)
    monkeypatch.setattr(WelcomeDialog, "exec", lambda self: opened.append("welcome") or 0)
    window.greet()
    assert opened == ["wizard"]
    # rezygnacja z kreatora nie może go przywoływać przy każdym starcie
    assert window.store.setting("wizard_done") is True


def test_later_starts_show_the_welcome_screen(window, monkeypatch):
    window.store.put_template(Template(name="Moja kopia"))
    opened = []
    monkeypatch.setattr(SetupWizard, "exec", lambda self: opened.append("wizard") or 0)

    def choose_settings(self):
        opened.append("welcome")
        self.choice = WelcomeDialog.SETTINGS
        return QDialog.DialogCode.Accepted

    monkeypatch.setattr(WelcomeDialog, "exec", choose_settings)
    window.greet()
    assert opened == ["welcome"]
    assert window.stack.currentIndex() == MainWindow.PAGE_SETTINGS


def test_welcome_can_be_switched_off(window, monkeypatch):
    window.store.put_template(Template(name="Moja kopia"))
    window.store.set_setting("show_welcome", False)
    monkeypatch.setattr(WelcomeDialog, "exec", lambda self: pytest.fail("ekran powitalny wyłączony"))
    window.greet()


def test_wizard_result_fills_the_backup_form(window, folders, monkeypatch):
    source, destination = folders

    def finish(self):
        _walk_to_summary(self, source, destination, profile=0)
        self._finish(start_now=False)
        return QDialog.DialogCode.Accepted

    monkeypatch.setattr(SetupWizard, "exec", finish)
    window.run_setup_wizard()
    assert window.source_list.paths() == [str(source)]
    assert window.dest_picker.path() == str(destination)
    assert window.structure_mirror.isChecked()
    assert window.stack.currentIndex() == MainWindow.PAGE_BACKUP


def test_drive_helpers_do_not_fail_on_odd_paths():
    assert paths.drive_kind("Z:/nie/istnieje") in {
        paths.DRIVE_REMOVABLE, paths.DRIVE_FIXED, paths.DRIVE_NETWORK,
        paths.DRIVE_OPTICAL, paths.DRIVE_UNKNOWN,
    }
    assert isinstance(paths.is_system_drive("Z:/nie/istnieje"), bool)


def test_dialogs_speak_english_when_asked(qapp, store):
    """Kreator buduje wszystkie kroki od razu, więc jedno sprawdzenie obejmuje całość."""
    polish = set("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ")
    i18n.set_language("en")
    try:
        leftovers = []
        for dialog in (WelcomeDialog(store), SetupWizard(store)):
            for widget in [dialog, *dialog.findChildren(QWidget)]:
                for attribute in ("text", "toolTip", "windowTitle", "title"):
                    getter = getattr(widget, attribute, None)
                    if not callable(getter):
                        continue
                    try:
                        value = getter()
                    except TypeError:
                        continue
                    # ścieżki folderów użytkownika mogą mieć polskie litery — to nie tekst programu
                    if isinstance(value, str) and set(value) & polish and ":" + chr(92) not in value:
                        leftovers.append(f"{type(widget).__name__}.{attribute}: {value[:60]!r}")
    finally:
        i18n.set_language("pl")
    assert not leftovers, leftovers


def test_schedule_step_goes_into_the_template(qapp, store, folders):
    source, destination = folders
    wizard = SetupWizard(store)
    _walk_to_summary(wizard, source, destination, profile=1)
    before = time.time()
    wizard._finish(start_now=False)
    template = wizard.result_choice.template
    assert template.schedule == scheduler.DAILY and template.schedule_time == "20:00"
    # uzbrojony harmonogram: bieżący termin uznany za obsłużony, pierwsza kopia o czasie
    assert template.last_attempt >= before


def test_manual_choice_means_no_schedule(qapp, store, folders):
    source, destination = folders
    wizard = SetupWizard(store)
    wizard.purpose_group.button(2).setChecked(True)
    wizard._set_sources([str(source)])
    wizard._next()
    wizard._set_destination(str(destination))
    wizard._next()
    wizard._next()
    wizard.when_group.button(2).setChecked(True)  # „ręcznie”
    wizard._next()
    wizard._finish(start_now=False)
    assert wizard.result_choice.template.schedule == scheduler.MANUAL


def test_encrypted_schedule_remembers_the_password(qapp, store, folders, monkeypatch):
    source, destination = folders
    saved = {}
    monkeypatch.setattr(wizard_module.secrets_store, "is_available", lambda: True)
    monkeypatch.setattr(
        wizard_module.secrets_store, "save_password", lambda tid, pw: saved.setdefault(tid, pw) is not None
    )
    wizard = SetupWizard(store)
    wizard.purpose_group.button(2).setChecked(True)
    wizard._set_sources([str(source)])
    wizard._next()
    wizard._set_destination(str(destination))
    wizard._next()
    wizard.profile_group.button(2).setChecked(True)
    wizard.password.set_password("długie-hasło-1")
    wizard.password_confirm.set_password("długie-hasło-1")
    wizard.remember_cb.setChecked(True)
    wizard._next()
    wizard._next()
    wizard._finish(start_now=False)
    template = wizard.result_choice.template
    assert saved == {template.id: "długie-hasło-1"}
    assert template.remember_password



def test_wizard_offers_sigelith_evidence_also_without_sigelith(qapp, store, folders, monkeypatch):
    """Karta dowodów czasu jest dla każdego: kto nie ma Sigelith, może ją włączyć na zapas."""
    from cleanvault import sigelith

    monkeypatch.setattr(sigelith, "find_data_dir", lambda env=None: None)
    source, destination = folders
    wizard = SetupWizard(store)
    assert not wizard.sigelith_cb.isChecked(), "bez Sigelith nic się nie włącza samo"
    opened = []
    monkeypatch.setattr(wizard_module.QDesktopServices, "openUrl", lambda url: opened.append(url.toString()))
    monkeypatch.setattr(wizard_module, "package_family_name", lambda: None)
    wizard._open_sigelith()
    monkeypatch.setattr(wizard_module, "package_family_name", lambda: "AdamKoch.SigelithBackup_x")
    wizard._open_sigelith()
    assert opened[0].startswith("https://sigelith.org/") and opened[0].endswith("/desktop/")
    assert opened[1] == "ms-windows-store://pdp/?productid=9N5XK65GTF33", "wersja ze Sklepu — tylko przez Sklep"

    wizard.sigelith_cb.setChecked(True)
    _walk_to_summary(wizard, source, destination)
    assert "gdy zainstalujesz Sigelith Desktop" in wizard.summary_text.text()
    wizard._finish(start_now=False)
    assert wizard.result_choice.template.sigelith


def test_wizard_protects_existing_sigelith_evidence_by_default(qapp, store, folders, tmp_path, monkeypatch):
    from cleanvault import sigelith

    data_dir = tmp_path / "Sigelith"
    data_dir.mkdir()
    (data_dir / "history.json").write_text('[{"digest": "' + "ab" * 32 + '", "file_name": "umowa.pdf"}]',
                                           encoding="utf-8")
    monkeypatch.setattr(sigelith, "find_data_dir", lambda env=None: data_dir)
    source, destination = folders
    wizard = SetupWizard(store)
    assert wizard.sigelith_cb.isChecked()
    texts = " ".join(label.text() for label in wizard.findChildren(QLabel))
    assert "1 stempel" in texts
    _walk_to_summary(wizard, source, destination)
    assert "magazynu dowodów" in wizard.summary_text.text()
    wizard._finish(start_now=False)
    assert wizard.result_choice.template.sigelith


def test_backup_folder_continues_the_copy_made_under_the_previous_name(tmp_path):
    """Kopia założona jako „Time Vault Backup” jest kontynuowana, nie zaczynana od zera."""
    assert wizard_module.backup_folder_on(tmp_path) == tmp_path / "Sigelith Backup"
    old = tmp_path / "Time Vault Backup"
    old.mkdir()
    assert wizard_module.backup_folder_on(tmp_path) == tmp_path / "Sigelith Backup", "pusty katalog to nie kopia"
    (old / paths.MANIFEST_NAME).write_bytes(b"manifest")
    assert wizard_module.backup_folder_on(tmp_path) == old
