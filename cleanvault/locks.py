"""Pliki zablokowane przez inne programy.

Bez migawek VSS (wycofanych z projektu — patrz plan rozwoju) pliku otwartego na
wyłączność przez inny program nie da się skopiować: skrzynki Outlooka, działającej
bazy danych, dysku uruchomionej maszyny wirtualnej. Zamiast udawać, że to zwykły
błąd, mówimy wprost, **który program trzyma który plik** — użytkownik wie wtedy,
co zamknąć, żeby następna kopia go objęła.

Program trzymający plik ustala Menedżer ponownego uruchamiania Windows (Restart
Manager, ``rstrtmgr.dll``) — ten sam, z którego korzystają instalatory, pytając
„zamknij te programy”. Działa bez uprawnień administratora; o procesach innych
użytkowników może nie wiedzieć nic i wtedy po prostu nie podajemy nazwy.
"""

from __future__ import annotations

import os

from .log import get_logger
from .paths import long_path

log = get_logger("locks")

#: ERROR_SHARING_VIOLATION i ERROR_LOCK_VIOLATION z WinAPI.
_LOCK_ERRORS = {32, 33}
_ERROR_MORE_DATA = 234
_CCH_RM_SESSION_KEY = 32
_CCH_RM_MAX_APP_NAME = 255
_CCH_RM_MAX_SVC_NAME = 63


def is_lock_error(exc: BaseException, path: str | os.PathLike[str] | None = None) -> bool:
    """Czy błąd oznacza plik otwarty na wyłączność przez inny proces.

    ``open()`` w Pythonie przechodzi przez bibliotekę C, która zamienia
    „naruszenie udostępniania” na zwykłe ``EACCES`` i gubi kod błędu Windows —
    blokada wygląda wtedy jak brak uprawnień. Dlatego przy ``PermissionError``
    sprawdzamy plik sami, otwierając go przez ``CreateFileW``.
    """
    if not isinstance(exc, OSError):
        return False
    if getattr(exc, "winerror", None) in _LOCK_ERRORS:
        return True
    return isinstance(exc, PermissionError) and path is not None and _probe_lock(path)


def _probe_lock(path: str | os.PathLike[str]) -> bool:
    if os.name != "nt":
        return False
    import ctypes
    from ctypes import wintypes

    generic_read = 0x80000000
    share_all = 0x7  # odczyt, zapis i usuwanie — sami niczego nie blokujemy
    open_existing = 3
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateFileW.restype = wintypes.HANDLE
    kernel32.CreateFileW.argtypes = [
        wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
        wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE,
    ]
    handle = kernel32.CreateFileW(str(long_path(path)), generic_read, share_all, None, open_existing, 0, None)
    if handle in (None, wintypes.HANDLE(-1).value):
        return ctypes.get_last_error() in _LOCK_ERRORS
    kernel32.CloseHandle(handle)
    return False


def who_locks(path: str | os.PathLike[str]) -> list[str]:
    """Nazwy programów, które trzymają plik otwarty; pusta lista, gdy nie wiadomo."""
    if os.name != "nt":
        return []
    try:
        return _restart_manager_list(str(long_path(path)))
    except Exception as exc:  # noqa: BLE001 - brak nazwy programu nie może wywrócić kopii
        log.debug("Nie udało się ustalić, kto blokuje %s: %s", path, exc)
        return []


def _restart_manager_list(path: str) -> list[str]:
    import ctypes
    from ctypes import wintypes

    class RmUniqueProcess(ctypes.Structure):
        _fields_ = [("dwProcessId", wintypes.DWORD), ("ProcessStartTime", wintypes.FILETIME)]

    class RmProcessInfo(ctypes.Structure):
        _fields_ = [
            ("Process", RmUniqueProcess),
            ("strAppName", wintypes.WCHAR * (_CCH_RM_MAX_APP_NAME + 1)),
            ("strServiceShortName", wintypes.WCHAR * (_CCH_RM_MAX_SVC_NAME + 1)),
            ("ApplicationType", ctypes.c_int),
            ("AppStatus", wintypes.ULONG),
            ("TSSessionId", wintypes.DWORD),
            ("bRestartable", wintypes.BOOL),
        ]

    rm = ctypes.WinDLL("rstrtmgr")
    session = wintypes.DWORD(0)
    key = ctypes.create_unicode_buffer(_CCH_RM_SESSION_KEY + 1)
    if rm.RmStartSession(ctypes.byref(session), 0, key) != 0:
        return []
    try:
        files = (wintypes.LPCWSTR * 1)(path)
        if rm.RmRegisterResources(session, 1, files, 0, None, 0, None) != 0:
            return []
        needed = wintypes.UINT(0)
        count = wintypes.UINT(0)
        reasons = wintypes.DWORD(0)
        code = rm.RmGetList(session, ctypes.byref(needed), ctypes.byref(count), None, ctypes.byref(reasons))
        if code not in (0, _ERROR_MORE_DATA) or needed.value == 0:
            return []
        infos = (RmProcessInfo * needed.value)()
        count = wintypes.UINT(needed.value)
        if rm.RmGetList(session, ctypes.byref(needed), ctypes.byref(count), infos, ctypes.byref(reasons)) != 0:
            return []
        names: list[str] = []
        for info in infos[: count.value]:
            name = info.strAppName or _process_name(info.Process.dwProcessId)
            if name and name not in names:
                names.append(name)
        return names
    finally:
        rm.RmEndSession(session)


def _process_name(pid: int) -> str:
    """Nazwa pliku programu po numerze procesu — gdy Restart Manager nie podał nazwy."""
    import ctypes
    from ctypes import wintypes

    process_query_limited_information = 0x1000
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    handle = kernel32.OpenProcess(process_query_limited_information, False, pid)
    if not handle:
        return ""
    try:
        size = wintypes.DWORD(1024)
        buffer = ctypes.create_unicode_buffer(size.value)
        if kernel32.QueryFullProcessImageNameW(handle, 0, buffer, ctypes.byref(size)):
            return os.path.basename(buffer.value)
        return ""
    finally:
        kernel32.CloseHandle(handle)


def describe(locked: dict[str, list[str]], limit: int = 5) -> str:
    """„Outlook (archiwum.pst), baza.db” — krótka lista do komunikatu."""
    parts = []
    for key, programs in list(locked.items())[:limit]:
        name = key.rpartition("/")[2]
        parts.append(f"{', '.join(programs)} ({name})" if programs else name)
    rest = len(locked) - limit
    if rest > 0:
        parts.append(f"… +{rest}")
    return "; ".join(parts)
