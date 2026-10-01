"""Uruchamianie programu w tle przy logowaniu do Windows.

Bez tego harmonogram działałby tylko wtedy, gdy ktoś pamięta, by otworzyć
program — a o kopii zapasowej z definicji się nie pamięta.

Dwa przypadki:

* **zwykły plik EXE** — wpis w ``HKCU\\...\\Run`` (bez uprawnień administratora,
  tylko dla bieżącego użytkownika), z parametrem ``--background``;
* **pakiet MSIX ze Sklepu** — zapis pakietu do ``HKCU`` trafia do jego
  prywatnej kopii rejestru, której system przy logowaniu nie czyta. Start
  deklaruje manifest pakietu (``windows.startupTask`` z parametrem
  ``--background``), a program włącza i wyłącza to zadanie przez API
  ``StartupTask``. Jeśli użytkownik wyłączył je w Ustawieniach Windows
  (Aplikacje → Uruchamianie), program nie może go włączyć z powrotem sam —
  tak działa ta zgoda w Windows; program tylko o tym mówi.

W trybie deweloperskim (uruchomienie ze źródeł) wpisu nie zakładamy: wskazywałby
na interpreter Pythona i katalog roboczy, które za tydzień mogą nie istnieć.
"""

from __future__ import annotations

import asyncio
import contextlib
import os
import sys

from .log import get_logger
from .paths import is_frozen, package_family_name

log = get_logger("autostart")

RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
VALUE_NAME = "Sigelith Backup"
#: Wpisy z poprzednich nazw programu. Wskazują stary plik EXE — zostawione,
#: uruchamiałyby przy logowaniu dawny program obok nowego.
LEGACY_VALUE_NAMES = ("Time Vault Backup",)
BACKGROUND_FLAG = "--background"

#: Identyfikator zadania startowego — ten sam co ``TaskId`` w ``packaging/msix/AppxManifest.xml``.
STARTUP_TASK_ID = "SigelithBackupStartup"

# Wartości ``Windows.ApplicationModel.StartupTaskState``.
TASK_DISABLED = 0
TASK_DISABLED_BY_USER = 1
TASK_ENABLED = 2
TASK_DISABLED_BY_POLICY = 3
TASK_ENABLED_BY_POLICY = 4


def packaged() -> bool:
    """Czy program działa z pakietu MSIX (ma tożsamość pakietu)."""
    return package_family_name() is not None


def _wait(operation):
    """Wynik operacji asynchronicznej WinRT — trwa milisekundy, więc czekamy w miejscu."""

    async def result():
        return await operation

    return asyncio.run(result())


def _startup_task():
    """Zadanie startowe pakietu (``StartupTask``) albo ``None``, gdy go nie ma."""
    try:
        # winrt ma w sobie starszą bibliotekę MSVCP140 (14.29) niż Qt (14.44). Której proces
        # użyje, decyduje ta, która załaduje się pierwsza — a Qt ze starszą się wywraca.
        # W programie Qt jest zawsze pierwsze; ten import pilnuje kolejności także w testach.
        import PySide6.QtCore  # noqa: F401
        from winrt.windows.applicationmodel import StartupTask
    except ImportError:
        log.warning("Brak modułu winrt — start przy logowaniu w pakiecie jest niedostępny.")
        return None
    try:
        return _wait(StartupTask.get_async(STARTUP_TASK_ID))
    except OSError as exc:
        log.warning("Nie znaleziono zadania startowego pakietu %s: %s", STARTUP_TASK_ID, exc)
        return None


def _task_state() -> int | None:
    task = _startup_task()
    return None if task is None else int(task.state)


def supported() -> bool:
    """Czy program sam może włączyć start przy logowaniu."""
    if os.name != "nt" or not is_frozen():
        return False
    if packaged():
        return _startup_task() is not None
    return True


def blocked_in_windows() -> bool:
    """Start wyłączony w Ustawieniach Windows (albo zasadami firmy) — program go nie włączy."""
    return packaged() and _task_state() in (TASK_DISABLED_BY_USER, TASK_DISABLED_BY_POLICY)


def command() -> str:
    return f'"{sys.executable}" {BACKGROUND_FLAG}'


def is_enabled() -> bool:
    if not supported():
        return False
    if packaged():
        return _task_state() in (TASK_ENABLED, TASK_ENABLED_BY_POLICY)
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY) as key:
            value, _kind = winreg.QueryValueEx(key, VALUE_NAME)
    except OSError:
        return False
    return str(value).strip().lower() == command().lower()


def set_enabled(enabled: bool) -> bool:
    """Włącza albo wyłącza start przy logowaniu; ``True`` = stan zgodny z żądaniem."""
    if not supported():
        return False
    if packaged():
        return _set_task(enabled)
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE) as key:
            if enabled:
                winreg.SetValueEx(key, VALUE_NAME, 0, winreg.REG_SZ, command())
            else:
                with contextlib.suppress(FileNotFoundError):
                    winreg.DeleteValue(key, VALUE_NAME)
            for name in LEGACY_VALUE_NAMES:
                with contextlib.suppress(FileNotFoundError):
                    winreg.DeleteValue(key, name)
    except OSError as exc:
        log.warning("Nie udało się zmienić startu przy logowaniu: %s", exc)
        return False
    log.info("Start przy logowaniu: %s", "włączony" if enabled else "wyłączony")
    return True


def migrate_legacy() -> bool:
    """Przenosi start przy logowaniu spod poprzedniej nazwy programu (tylko wersja EXE).

    Zwraca ``True``, gdy był stary wpis: zostaje usunięty, a start włączony pod
    obecną nazwą i dla obecnego pliku EXE — użytkownik, który go włączył, dalej
    ma kopie planowe po zalogowaniu.
    """
    if not supported() or packaged():
        return False
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY) as key:
            found = []
            for name in LEGACY_VALUE_NAMES:
                with contextlib.suppress(FileNotFoundError):
                    winreg.QueryValueEx(key, name)
                    found.append(name)
    except OSError:
        return False
    if not found:
        return False
    log.info("Start przy logowaniu przeniesiony spod dawnej nazwy: %s", ", ".join(found))
    return set_enabled(True)


def _set_task(enabled: bool) -> bool:
    task = _startup_task()
    if task is None:
        return False
    try:
        if enabled:
            state = int(_wait(task.request_enable_async()))
        else:
            task.disable()
            state = int(task.state)
    except OSError as exc:
        log.warning("Nie udało się zmienić zadania startowego pakietu: %s", exc)
        return False
    log.info("Start przy logowaniu (pakiet): stan zadania %s", state)
    if enabled:
        return state in (TASK_ENABLED, TASK_ENABLED_BY_POLICY)
    return state in (TASK_DISABLED, TASK_DISABLED_BY_USER, TASK_DISABLED_BY_POLICY)
