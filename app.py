"""Punkt wejścia Sigelith Backup.

Uruchomienie w trybie deweloperskim::

    .venv\\Scripts\\python.exe app.py

Po zbudowaniu (PyInstaller) ten sam kod startuje z ``SigelithBackup.exe``.
"""

from __future__ import annotations

import sys


def _log_environment(logger) -> None:
    """Zapisuje w dzienniku stan środowiska.

    Ma to znaczenie praktyczne w wersji zamrożonej: ``keyring`` i ``argon2-cffi``
    ładują się dynamicznie, więc brak któregoś w pakiecie EXE objawiłby się
    dopiero cichym wyłączeniem funkcji. Dziennik od razu mówi, co jest dostępne.
    """
    from cleanvault import crypto, paths, secrets_store

    logger.info("Tryb: %s", "EXE (PyInstaller)" if paths.is_frozen() else "źródła")
    logger.info("Pakiet MSIX (Sklep): %s", paths.package_family_name() or "nie")
    logger.info("Katalog danych: %s", paths.data_dir())
    logger.info(
        "Wyprowadzanie klucza: %s",
        "Argon2id" if crypto.ARGON2_AVAILABLE else f"PBKDF2-SHA256 ({crypto.PBKDF2_ITERATIONS})",
    )
    logger.info(
        "Magazyn haseł: %s (bezpieczny: %s)",
        secrets_store.backend_name(),
        "tak" if secrets_store.is_available() else "nie",
    )
    from cleanvault import chunks

    logger.info(
        "Zapis różnicowy dużych plików: %s",
        "dostępny (FastCDC)" if chunks.AVAILABLE else "niedostępny — duże pliki kopiowane w całości",
    )


def main() -> int:
    from cleanvault import __app_name__, __publisher__, __version__, i18n, log
    from cleanvault.i18n import tr
    from cleanvault.state import StateStore

    log.setup()
    # Język ustawiamy przed zbudowaniem okna: teksty powstają przy budowie,
    # a wybór użytkownika ma pierwszeństwo przed językiem systemu.
    store = StateStore()
    language = i18n.set_language(store.setting("language", "auto"))
    logger = log.get_logger("app")
    logger.info("Start %s %s (Python %s)", __app_name__, __version__, sys.version.split()[0])
    logger.info("Język interfejsu: %s", language)
    _log_environment(logger)

    try:
        from PySide6.QtCore import QTimer
        from PySide6.QtWidgets import QApplication

        from cleanvault.ui.main_window import MainWindow
    except ImportError as exc:  # pragma: no cover - brakująca zależność
        logger.critical("Brak wymaganej biblioteki: %s", exc)
        print(
            tr("Nie udało się uruchomić programu — brakuje biblioteki: {error}\n"
               "Zainstaluj zależności poleceniem:  pip install -r requirements.txt").format(error=exc),
            file=sys.stderr,
        )
        return 2

    app = QApplication(sys.argv)
    app.setApplicationName(__app_name__)
    app.setApplicationVersion(__version__)
    app.setOrganizationName(__publisher__)
    from cleanvault.ui import qtlang

    if not qtlang.apply(language):
        logger.warning("Brak tłumaczenia tekstów Qt dla języka %s — przyciski okien po angielsku.", language)

    # Jeden egzemplarz na użytkownika: program działający w tle pilnuje
    # harmonogramu, więc drugi egzemplarz uruchomiłby te same kopie drugi raz.
    # Drugie uruchomienie (np. z menu Start) tylko przywołuje okno pierwszego.
    from cleanvault.ui.background import MSG_BACKGROUND, MSG_SHOW, SingleInstance

    background = "--background" in sys.argv[1:]
    instance = SingleInstance()
    if instance.forward_to_primary(MSG_BACKGROUND if background else MSG_SHOW):
        logger.info("Program już działa — przekazano prośbę do działającego egzemplarza.")
        return 0
    instance.become_primary()
    # Start przy logowaniu włączony jeszcze pod dawną nazwą programu wskazywałby stary
    # plik EXE — przenosimy go na obecny, zanim okno pokaże stan tej opcji.
    from cleanvault import autostart

    autostart.migrate_legacy()
    # Okno bywa ukryte (praca w tle), więc o końcu programu decyduje okno główne
    # przy prawdziwym zamknięciu, a nie Qt po zamknięciu ostatniego okna.
    app.setQuitOnLastWindowClosed(False)

    try:
        window = MainWindow(store, background=background)
    except Exception as exc:
        logger.exception("Nie udało się zbudować okna głównego")
        from PySide6.QtWidgets import QMessageBox

        QMessageBox.critical(
            None,
            tr("Błąd uruchamiania"),
            tr("Program nie mógł się uruchomić:\n\n{error}\n\n"
               "Szczegóły zapisano w dzienniku aplikacji.").format(error=exc),
        )
        return 1

    instance.message_received.connect(window.handle_instance_message)
    if background:
        logger.info("Start w tle — okno ukryte, harmonogram aktywny.")
    else:
        window.show()
        # Kreator i ekran powitalny pojawiają się nad widocznym już oknem —
        # inaczej użytkownik zobaczyłby najpierw puste tło, a potem okno dialogowe.
        QTimer.singleShot(0, window.greet)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
