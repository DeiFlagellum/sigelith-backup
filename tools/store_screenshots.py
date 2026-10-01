"""Zrzuty ekranu do strony w Microsoft Store — po polsku i po angielsku.

Rysuje okno programu poza ekranem (Qt ``offscreen`` z czcionkami systemu) na
przykładowych danych z ``build/store-screens`` i zapisuje pliki PNG 1600×1000
(Sklep wymaga co najmniej 1366×768) do ``dist/store-screens/<język>/``.

Ścieżki widoczne na zrzutach są podmieniane na neutralne (dysk D: i E:), żeby
na stronie w Sklepie nie było nazwy konta ani katalogów autora.

Użycie::

    .venv/Scripts/python.exe tools/store_screenshots.py
"""

from __future__ import annotations

import os
import random
import shutil
import sys
import time
from pathlib import Path, PureWindowsPath

os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ.setdefault("QT_QPA_FONTDIR", str(Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"))

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

WORK = ROOT / "build" / "store-screens"
OUT = ROOT / "dist" / "store-screens"
SIZE = (1600, 1000)

#: Przykładowe dane: foldery i pliki w obu językach.
SAMPLES = {
    "pl": {
        "Dokumenty": ["Umowy/2026/Umowa najmu.pdf", "Umowy/Aneks do umowy.pdf", "Faktury/FV-2026-09.pdf",
                      "Faktury/FV-2026-08.pdf", "Budżet domowy.xlsx", "Notatki ze spotkania.docx"],
        "Zdjęcia": ["Wakacje 2026/IMG_0412.jpg", "Wakacje 2026/IMG_0413.jpg", "Urodziny/IMG_0102.jpg"],
        "template": "Dokumenty i zdjęcia",
        "changed": "Budżet domowy.xlsx",
        "destination": "E:/Kopie",
        "restored": "D:/Przywrócone",
    },
    "en": {
        "Documents": ["Contracts/2026/Lease agreement.pdf", "Contracts/Amendment.pdf", "Invoices/INV-2026-09.pdf",
                      "Invoices/INV-2026-08.pdf", "Home budget.xlsx", "Meeting notes.docx"],
        "Photos": ["Holiday 2026/IMG_0412.jpg", "Holiday 2026/IMG_0413.jpg", "Birthday/IMG_0102.jpg"],
        "template": "Documents and photos",
        "changed": "Home budget.xlsx",
        "destination": "E:/Backups",
        "restored": "D:/Restored",
    },
}


def _sample_data(language: str) -> tuple[list[Path], Path, str]:
    base = WORK / language
    shutil.rmtree(base, ignore_errors=True)
    rng = random.Random(7)
    sample = SAMPLES[language]
    sources = []
    for folder, files in sample.items():
        if not isinstance(files, list):
            continue
        root = base / folder
        for name in files:
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(rng.randbytes(rng.randint(20_000, 400_000)))
        sources.append(root)
    return sources, base / "Backup", sample["changed"]


def _backups(sources: list[Path], destination: Path, changed: str) -> None:
    from cleanvault import engine

    config = engine.BackupConfig(sources=[str(s) for s in sources], destination=str(destination),
                                 structure="dated", excludes=[], stamp_updates=False, catchup_passes=0)
    for round_ in range(2):
        plan = engine.plan_backup(config, engine.Reporter())
        assert engine.run_backup(plan, None, engine.Reporter()).ok
        if round_ == 0:
            time.sleep(1.0)  # druga wersja w innym beacie
            target = sources[0] / changed
            target.write_bytes(target.read_bytes() + b"-zmiana")
            time.sleep(90)  # beat to 86,4 s — nazwa następnej wersji musi się różnić


def _neutral(language: str) -> dict[str, str]:
    folders = [name for name, files in SAMPLES[language].items() if isinstance(files, list)]
    return {
        "sources": [str(PureWindowsPath("D:/", name)) for name in folders],
        "destination": str(PureWindowsPath(SAMPLES[language]["destination"])),
    }


def _mask(picker, text: str) -> None:
    picker.edit.blockSignals(True)
    picker.edit.setText(str(PureWindowsPath(text)))
    picker.edit.blockSignals(False)


def _settle(app, seconds: float = 1.0) -> None:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.02)


def shoot(language: str) -> list[Path]:
    from PySide6.QtGui import QColor, QPainter
    from PySide6.QtWidgets import QApplication

    from cleanvault import i18n, scheduler
    from cleanvault.state import StateStore, Template
    from cleanvault.ui.main_window import MainWindow
    from cleanvault.ui.wizard import SetupWizard

    sources, destination, changed = _sample_data(language)
    _backups(sources, destination, changed)
    shown = _neutral(language)

    app = QApplication.instance() or QApplication([])
    store = StateStore(WORK / language / "state.msgpack")
    store.set_setting("language", language)
    store.set_setting("wizard_done", True)
    store.set_setting("show_welcome", False)
    template = Template(name=SAMPLES[language]["template"], sources=shown["sources"],
                        destination=shown["destination"], schedule=scheduler.DAILY, schedule_time="20:00",
                        gfs_daily=7, gfs_weekly=4, gfs_monthly=12, retention=0, encrypt=True)
    now = time.time()
    template.last_attempt = template.last_success = now - 86400
    scheduler.arm(template)  # termin dziś już „widziany” — harmonogram nie ruszy kopii w trakcie zrzutów
    store.put_template(template)
    for days, files in ((3, 1240), (2, 17), (1, 42)):  # kilka wpisów w „Ostatnich operacjach”
        store.add_history({"action": "backup", "ok": True, "files": files, "at": now - days * 86400})
    i18n.set_language(language)
    window = MainWindow(store)
    window.resize(*SIZE)
    window.show()
    folder = OUT / language
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    saved: list[Path] = []

    def save(name: str, widget) -> None:
        _settle(app, 0.5)
        path = folder / f"{name}.png"
        widget.grab().save(str(path))
        saved.append(path)

    # 1. kopia: formularz z dwoma folderami i dyskiem docelowym
    window.source_list.set_paths([str(s) for s in sources])
    window.dest_picker.set_path(str(destination))
    window._go_to(MainWindow.PAGE_BACKUP)
    _settle(app, 2.0)  # ocena nośnika po zmianie katalogu docelowego
    window._set_retention(0, 7, 4, 12)
    for index, text in enumerate(shown["sources"]):
        window.source_list.item(index).setText(text)
    _mask(window.dest_picker, shown["destination"])
    save("1-backup", window)

    # 2. przeglądanie: drzewo wersji i historia pliku
    browser = window.browser
    browser.open_backup(str(destination))
    window._go_to(MainWindow.PAGE_BROWSE)
    top = browser.tree.topLevelItem(0)
    browser.tree.expandItem(top)
    for i in range(top.childCount()):
        child = top.child(i)
        if child.childCount():
            browser.tree.expandItem(child)
        if child.text(0) == changed:
            browser.tree.setCurrentItem(child)
    browser._show_history()
    _mask(browser.picker, shown["destination"])
    save("2-browse", window)

    # 3. przywracanie
    window.restore_src.set_path(str(destination))
    window._go_to(MainWindow.PAGE_RESTORE)
    _settle(app, 1.5)
    _mask(window.restore_src, shown["destination"])
    _mask(window.restore_dst, SAMPLES[language]["restored"])
    save("3-restore", window)

    # 4. szablony z harmonogramem
    window._go_to(MainWindow.PAGE_TEMPLATES)
    window.template_list.setCurrentRow(0)
    save("4-templates", window)

    # 5. kreator („jak bardzo chcesz się zabezpieczyć”) nad przyciemnionym oknem —
    # sam kreator jest mniejszy niż minimum Sklepu (1366×768)
    window._go_to(MainWindow.PAGE_BACKUP)
    wizard = SetupWizard(store, window)
    wizard.resize(900, 700)
    wizard.show()
    wizard._show_step(2)
    _settle(app, 0.5)
    canvas = window.grab()
    painter = QPainter(canvas)
    painter.fillRect(canvas.rect(), QColor(0, 0, 0, 120))
    dialog = wizard.grab()
    painter.drawPixmap((canvas.width() - dialog.width()) // 2, (canvas.height() - dialog.height()) // 2, dialog)
    painter.end()
    path = folder / "5-wizard.png"
    canvas.save(str(path))
    saved.append(path)
    wizard.close()

    window.browser.shutdown()
    window.close()
    return saved


def main() -> int:
    sys.stdout.reconfigure(errors="replace")
    language = sys.argv[1] if len(sys.argv) > 1 else None
    for code in [language] if language else list(SAMPLES):
        for path in shoot(code):
            print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
