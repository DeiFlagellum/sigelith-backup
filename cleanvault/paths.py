"""Ścieżki aplikacji.

Stan aplikacji trzymamy w katalogu danych użytkownika
(%LOCALAPPDATA%\\Sigelith Backup), a nie w katalogu roboczym. Dzięki temu:
  * program działa tak samo uruchomiony z EXE, z IDE i z dowolnego CWD,
  * prywatne dane użytkownika nigdy nie lądują w repozytorium,
  * kilka instancji nie nadpisuje sobie stanu zależnie od tego, skąd je odpalono.
"""

from __future__ import annotations

import contextlib
import functools
import os
import shutil
import sys
from collections.abc import Iterable
from pathlib import Path

APP_DIR_NAME = "Sigelith Backup"

#: Katalogi danych sprzed zmian nazwy programu, od najnowszego („Time Vault Backup”
#: do 2026-09-30, wcześniej „CleanVault”). Jeśli któryś istnieje, a nowego nie ma,
#: pracujemy dalej na nim — szablony, historia i zapamiętane hasła użytkownika
#: zostają na miejscu i nic nie trzeba przenosić.
LEGACY_APP_DIR_NAMES = ("Time Vault Backup", "CleanVault")

#: Nazwa pliku manifestu zapisywanego w katalogu docelowym kopii.
MANIFEST_NAME = ".cleanvault-manifest"

#: Małe podsumowanie manifestu (stan wersji, liczba plików) zapisywane obok
#: niego. Manifest dużej kopii waży setki megabajtów — nie wolno go wczytywać
#: w wątku interfejsu tylko po to, żeby pokazać, czy kopia jest dokończona.
#: Nazwa zaczyna się od ``MANIFEST_NAME``, więc przywracanie bez manifestu
#: pomija ten plik tak samo jak sam manifest.
SUMMARY_NAME = MANIFEST_NAME + ".summary"

#: Dziennik punktów kontrolnych: wpisy plików zapisanych od ostatniego pełnego
#: zapisu manifestu. Dzięki niemu przerwanie kopii (także wyłączenie komputera)
#: nie wymaga przepisywania wielusetmegabajtowego manifestu.
JOURNAL_NAME = MANIFEST_NAME + ".journal"

#: Folder kapsuł czasu w katalogu kopii (:mod:`cleanvault.capsule`). Jak magazyn
#: dowodów: to nie dane kopii — przeglądanie go pomija, sprzątanie wersji go nie
#: dotyka, a notatka ratunkowa opisuje, czym jest.
CAPSULES_DIR = "Sigelith Capsules"


def contained_path(base: str | os.PathLike[str], relative: str) -> Path | None:
    """``base`` + ścieżka z kopii, jeśli wynik nie wychodzi poza ``base``; inaczej ``None``.

    Chroni przed wpisami w rodzaju ``../../Windows`` albo ``C:/Windows`` w spisie
    treści z obcego nośnika (analogia do „zip slip”). Porównanie jest czysto
    tekstowe: ``Path.resolve()`` pyta system plików i gdy inny wątek właśnie
    tworzy katalog, potrafi zwrócić ścieżkę z prefiksem długich nazw — plik
    w środku celu wyglądał wtedy na leżący poza nim.
    """
    root = os.path.normpath(os.fspath(base))
    if not os.path.isabs(root):
        root = os.path.normpath(os.path.join(os.getcwd(), root))
    joined = os.path.normpath(os.path.join(root, relative.replace("/", os.sep)))
    folded_root, folded = os.path.normcase(root), os.path.normcase(joined)
    if folded != folded_root and not folded.startswith(folded_root.rstrip(os.sep) + os.sep):
        return None
    return Path(joined)


def is_frozen() -> bool:
    """Czy działamy jako EXE zbudowane PyInstallerem."""
    return getattr(sys, "frozen", False)


def resource_path(*parts: str) -> Path:
    """Ścieżka do zasobu dołączonego do aplikacji (ikony itp.).

    W trybie zamrożonym PyInstaller rozpakowuje zasoby do ``sys._MEIPASS``.
    """
    base = getattr(sys, "_MEIPASS", None)
    root = Path(base) if base else Path(__file__).resolve().parent.parent
    return root.joinpath(*parts)


#: Kod błędu ``GetCurrentPackageFamilyName`` dla procesu bez tożsamości pakietu.
APPMODEL_ERROR_NO_PACKAGE = 15700


@functools.cache
def package_family_name() -> str | None:
    """Rodzina pakietu MSIX, z którego działa program (wersja ze Sklepu); poza pakietem ``None``."""
    if os.name != "nt":
        return None
    try:
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.windll.kernel32
        length = wintypes.UINT(0)
        if kernel32.GetCurrentPackageFamilyName(ctypes.byref(length), None) == APPMODEL_ERROR_NO_PACKAGE:
            return None
        buffer = ctypes.create_unicode_buffer(max(length.value, 1))
        if kernel32.GetCurrentPackageFamilyName(ctypes.byref(length), buffer) != 0:
            return None
        return buffer.value or None
    except (AttributeError, OSError):
        return None


def _package_data_dir(local: Path, family: str) -> Path:
    """Katalog danych wersji ze Sklepu: ``LocalState`` pakietu.

    Pakiet MSIX nie tworzy nowych folderów bezpośrednio w ``%LOCALAPPDATA%``
    naprawdę — system przekierowuje je do prywatnej kopii pakietu, więc
    Eksplorator i Notatnik nie znalazłyby tam dziennika ani ustawień.
    ``LocalState`` to zwykły folder, który system usuwa razem z aplikacją.
    Stan z wersji EXE przejmujemy przy pierwszym uruchomieniu — kopiując, nie
    przenosząc: wersja EXE nadal ma swoje dane.
    """
    path = local / "Packages" / family / "LocalState"
    path.mkdir(parents=True, exist_ok=True)
    state = path / "state.msgpack"
    if not state.exists():
        for old in (local / APP_DIR_NAME, *(local / name for name in LEGACY_APP_DIR_NAMES)):
            if (old / "state.msgpack").is_file():
                with contextlib.suppress(OSError):
                    shutil.copy2(old / "state.msgpack", state)
                break
    return path


def _virtualized_folders() -> list[Path]:
    """Foldery, w których pakiet MSIX tworzy nowe pliki tylko w swojej prywatnej kopii.

    Lista z dokumentacji Microsoftu, potwierdzona próbą w pakiecie: przekierowane
    są nowe pliki i foldery tworzone *bezpośrednio* w tych folderach; w istniejących
    podfolderach (np. profil programu, który już działał) zapis jest prawdziwy.
    """
    folders: list[Path] = []
    local, roaming = os.environ.get("LOCALAPPDATA"), os.environ.get("APPDATA")
    if local:
        folders += [Path(local), Path(local) / "Microsoft"]
    if roaming:
        folders += [
            Path(roaming),
            Path(roaming) / "Microsoft",
            Path(roaming) / "Microsoft" / "Windows" / "Start Menu" / "Programs",
        ]
    return folders


def private_appdata_folders(targets: Iterable[str | os.PathLike[str]]) -> list[Path]:
    """Nowe foldery w AppData, które wersja ze Sklepu utworzyłaby tylko dla siebie.

    Przywrócone tam pliki widziałby wyłącznie ten program — nie program, do którego
    należą (np. profil poczty przywracany na nowym komputerze). Poza pakietem MSIX
    zawsze pusta lista.
    """
    if package_family_name() is None:
        return []
    watched = sorted(_virtualized_folders(), key=lambda folder: len(folder.parts), reverse=True)
    found: list[Path] = []
    for target in targets:
        path = Path(os.path.normpath(os.fspath(target)))
        for folder in watched:  # najgłębszy pasujący, np. Roaming/Microsoft przed Roaming
            try:
                inside = path.relative_to(folder)
            except ValueError:
                continue
            created = folder / inside.parts[0] if inside.parts else folder
            if (created == folder or not created.exists()) and created not in found:
                found.append(created)
            break
    return found


def data_dir() -> Path:
    """Katalog na stan aplikacji, tworzony przy pierwszym użyciu."""
    if os.name == "nt":
        root = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local")
        family = package_family_name()
        if family:
            return _package_data_dir(root, family)
    elif sys.platform == "darwin":
        root = Path.home() / "Library" / "Application Support"
    else:
        root = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share")
    path = root / APP_DIR_NAME
    if not path.exists():
        for name in LEGACY_APP_DIR_NAMES:
            if (root / name).is_dir():
                return root / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def log_dir() -> Path:
    path = data_dir() / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def state_file() -> Path:
    return data_dir() / "state.msgpack"


def legacy_state_file() -> Path:
    """Stan ze starej wersji (1.x) leżący w katalogu roboczym — do jednorazowej migracji."""
    return Path.cwd() / "vault_state.msgpack"


def long_path(path: str | os.PathLike[str]) -> str:
    r"""Obejście limitu MAX_PATH (260 znaków) w Windows.

    Bez prefiksu ``\\?\`` operacje na plikach w głęboko zagnieżdżonych drzewach
    kończą się ``FileNotFoundError`` mimo że plik istnieje — typowa pułapka
    narzędzi backupowych. Prefiks działa wyłącznie na ścieżkach absolutnych
    i znormalizowanych, dlatego normalizujemy przed jego dodaniem.

    Normalizacja jest **czysto tekstowa** (``normpath``), a nie przez
    ``os.path.abspath``. ``abspath`` woła ``GetFullPathNameW``, które
    interpretuje zarezerwowane nazwy urządzeń DOS: plik ``nul`` (takie pliki
    tworzy np. przekierowanie powłoki w repozytorium) zamieniał się w ścieżkę
    urządzenia ``\\.\nul``, a stąd powstawało bezsensowne ``\\?\UNC\.\nul``
    i kopia kończyła się błędem przy każdym przebiegu. Ta sama funkcja obcina
    też końcowe kropki i spacje w nazwach — pliki utworzone na Linuksie
    przestawały być osiągalne. Prefiks ``\\?\`` wyłącza obie te interpretacje,
    więc wystarczy nie psuć ścieżki przed jego dodaniem.
    """
    text = os.fspath(path)
    if os.name != "nt":
        return text
    if text.startswith("\\\\?\\"):
        return text
    if os.path.isabs(text):
        absolute = os.path.normpath(text)
    else:
        absolute = os.path.normpath(os.path.join(os.getcwd(), text))
        if not os.path.isabs(absolute):  # np. ścieżka względna wobec dysku ("C:plik")
            absolute = os.path.abspath(absolute)
    if absolute.startswith("\\\\"):
        # Ścieżka UNC: \\serwer\udział -> \\?\UNC\serwer\udział
        return "\\\\?\\UNC\\" + absolute[2:]
    return "\\\\?\\" + absolute


# ----------------------------------------------------- właściwości nośnika

#: Systemy plików, które z definicji nie znają twardych dowiązań. Sprawdzamy je
#: po nazwie, żeby nie zakładać plików testowych na cudzym nośniku bez potrzeby.
_NO_HARDLINK_FS = {"FAT", "FAT12", "FAT16", "FAT32", "EXFAT"}

#: Nazwa pliku próbnego używanego do sprawdzenia twardych dowiązań.
_LINK_PROBE = ".cleanvault-linktest"


def filesystem_name(path: str | os.PathLike[str]) -> str:
    """Nazwa systemu plików wolumenu (``NTFS``, ``exFAT``…) albo pusty napis.

    Potrzebna, bo od systemu plików zależą dwie rzeczy, które decydują
    o zajętości kopii: obsługa twardych dowiązań i rozmiar klastra.
    """
    if os.name != "nt":
        return ""
    try:
        import ctypes
        from ctypes import wintypes

        root = _volume_root(path)
        buf = ctypes.create_unicode_buffer(256)
        ok = ctypes.windll.kernel32.GetVolumeInformationW(
            wintypes.LPCWSTR(root), None, 0, None, None, None, buf, ctypes.sizeof(buf) // 2
        )
        return buf.value if ok else ""
    except Exception:  # noqa: BLE001 - wykrywanie nośnika nie może wywrócić kopii
        return ""


def cluster_size(path: str | os.PathLike[str]) -> int:
    """Rozmiar jednostki alokacji w bajtach; 0 gdy nie da się ustalić.

    Każdy plik zajmuje wielokrotność klastra. Na nośnikach sformatowanych
    z dużym klastrem (exFAT bywa formatowany z 128–256 KB) kopia setek tysięcy
    małych plików zajmuje **wielokrotnie** więcej, niż wynosi suma ich
    rozmiarów — bez tej liczby kontrola wolnego miejsca kłamie.
    """
    if os.name != "nt":
        try:
            st = os.statvfs(path)  # type: ignore[attr-defined]
            return int(st.f_frsize)
        except (AttributeError, OSError):
            return 0
    try:
        import ctypes
        from ctypes import wintypes

        sectors = wintypes.DWORD()
        bytes_per_sector = wintypes.DWORD()
        free_clusters = wintypes.DWORD()
        total_clusters = wintypes.DWORD()
        ok = ctypes.windll.kernel32.GetDiskFreeSpaceW(
            wintypes.LPCWSTR(_volume_root(path)),
            ctypes.byref(sectors),
            ctypes.byref(bytes_per_sector),
            ctypes.byref(free_clusters),
            ctypes.byref(total_clusters),
        )
        if not ok:
            return 0
        return int(sectors.value) * int(bytes_per_sector.value)
    except Exception:  # noqa: BLE001
        return 0


def on_disk_size(size: int, cluster: int) -> int:
    """Ile miejsca zajmie plik o rozmiarze ``size`` przy danym klastrze.

    Plik pusty też zajmuje klaster — dlatego dolną granicą jest jeden klaster,
    a nie zero.
    """
    if cluster <= 0:
        return size
    return max(1, (size + cluster - 1) // cluster) * cluster


def hardlinks_expected(filesystem: str) -> bool:
    """Szybka ocena po samej nazwie systemu plików — bez zapisu na nośnik.

    Do podpowiedzi w interfejsie. Rozstrzygające sprawdzenie robi
    :func:`supports_hardlinks` przed właściwą kopią.
    """
    return filesystem.upper() not in _NO_HARDLINK_FS


#: Rodzaje nośników rozróżniane przez :func:`drive_kind`.
DRIVE_REMOVABLE = "removable"
DRIVE_FIXED = "fixed"
DRIVE_NETWORK = "network"
DRIVE_OPTICAL = "optical"
DRIVE_UNKNOWN = "unknown"

#: Odpowiedniki stałych ``DRIVE_*`` z WinAPI ``GetDriveTypeW``.
_DRIVE_TYPES = {
    2: DRIVE_REMOVABLE,
    3: DRIVE_FIXED,
    4: DRIVE_NETWORK,
    5: DRIVE_OPTICAL,
    6: DRIVE_FIXED,  # RAM-dysk — dla kreatora zachowuje się jak dysk stały
}


def drive_kind(path: str | os.PathLike[str]) -> str:
    """Rodzaj nośnika: wymienny, stały, sieciowy, optyczny albo nieznany.

    Kreator proponuje kopię **poza** dyskiem systemowym, a nośnik wymienny
    (pendrive, dysk USB) jest naturalnym wyborem — ale trzeba go odróżnić od
    dysku wewnętrznego, bo inaczej wybór sprowadza się do zgadywania po literze.
    """
    if os.name != "nt":
        return DRIVE_UNKNOWN
    try:
        import ctypes
        from ctypes import wintypes

        root = _volume_root(path)
        kind = ctypes.windll.kernel32.GetDriveTypeW(wintypes.LPCWSTR(root))
        return _DRIVE_TYPES.get(int(kind), DRIVE_UNKNOWN)
    except Exception:  # noqa: BLE001 - rozpoznanie nośnika nie może wywrócić programu
        return DRIVE_UNKNOWN


def is_admin() -> bool:
    """Czy proces działa z uprawnieniami administratora.

    Program ich nie potrzebuje i o nie nie prosi (aplikacja ze Sklepu nie może).
    Gdy ktoś uruchomi go jako administrator sam, pokazujemy to wprost — kopie
    zrobione wtedy mogą mieć uprawnienia plików, których zwykłe konto nie ruszy.
    """
    if os.name != "nt":
        return hasattr(os, "geteuid") and os.geteuid() == 0
    try:
        import ctypes

        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except (AttributeError, OSError):
        return False


def is_system_drive(path: str | os.PathLike[str]) -> bool:
    """Czy ścieżka leży na tym samym wolumenie co system operacyjny.

    Kopia na dysku systemowym nie chroni przed jego awarią — kreator musi to
    powiedzieć wprost, zamiast pozwolić użytkownikowi odkryć to po fakcie.
    """
    system = os.environ.get("SYSTEMDRIVE") or os.path.splitdrive(sys.executable)[0]
    if not system:
        return False
    return _volume_root(path).upper().startswith(system.rstrip("\\").upper())


def supports_hardlinks(folder: str | os.PathLike[str]) -> bool:
    """Czy w podanym katalogu da się tworzyć twarde dowiązania.

    Wersjonowanie z datą opiera się na dowiązaniach: plik niezmieniony jest
    podpinany do nowej wersji bez zajmowania miejsca. Gdy nośnik ich nie zna
    (exFAT, FAT32), **każda wersja jest pełną fizyczną kopią** — użytkownik
    musi to wiedzieć, zanim zabraknie mu miejsca.
    """
    name = filesystem_name(folder).upper()
    if name in _NO_HARDLINK_FS:
        return False
    probe = Path(folder) / _LINK_PROBE
    link = Path(folder) / (_LINK_PROBE + ".link")
    try:
        with open(long_path(probe), "wb") as handle:
            handle.write(b"cleanvault")
    except OSError:
        # Katalogu nie da się zapisać (np. korzeń dysku systemowego). O samych
        # dowiązaniach to nic nie mówi, więc ufamy nazwie systemu plików —
        # inaczej zwrócilibyśmy fałszywe „nie obsługuje" dla zwykłego NTFS.
        return name not in _NO_HARDLINK_FS and bool(name)
    try:
        os.link(long_path(probe), long_path(link))
        return True
    except (OSError, ValueError):
        return False
    finally:
        for leftover in (link, probe):
            with contextlib.suppress(OSError):
                os.unlink(long_path(leftover))


#: Tolerancja przyjmowana, gdy precyzji znaczników czasu nie da się zmierzyć.
#: FAT32 zapisuje czas modyfikacji z dokładnością do 2 sekund.
DEFAULT_MTIME_TOLERANCE = 2.0

_MTIME_PROBE = ".cleanvault-timetest"


def mtime_tolerance(folder: str | os.PathLike[str]) -> float:
    """Z jaką dokładnością nośnik przechowuje czas modyfikacji pliku.

    Wznawianie rozpoznaje zapisane pliki po czasie modyfikacji przeniesionym
    ze źródła. Za duża tolerancja przepuszcza plik zmieniony tuż po skopiowaniu
    (ten sam rozmiar, czas różny o ułamek sekundy); za mała sprawia, że na
    nośniku z grubszym zapisem czasu żaden plik nie zostanie rozpoznany i kopia
    zacznie się od zera. Zamiast zgadywać po nazwie systemu plików, mierzymy:
    ustawiamy na pliku próbnym dwa czasy dobrane tak, by zaokrąglenie w każdą
    stronę dało maksymalny błąd, i odczytujemy, co nośnik zapamiętał.
    """
    probe = Path(folder) / _MTIME_PROBE
    worst = 0.0
    try:
        with open(long_path(probe), "wb") as handle:
            handle.write(b"cleanvault")
        for wanted in (1_700_000_001.999, 1_700_000_002.001):
            os.utime(long_path(probe), (wanted, wanted))
            worst = max(worst, abs(os.stat(long_path(probe)).st_mtime - wanted))
    except OSError:
        return DEFAULT_MTIME_TOLERANCE
    finally:
        with contextlib.suppress(OSError):
            os.unlink(long_path(probe))
    return min(DEFAULT_MTIME_TOLERANCE, worst + 0.001)


def _volume_root(path: str | os.PathLike[str]) -> str:
    """Katalog główny wolumenu w postaci wymaganej przez API Windows."""
    absolute = os.path.abspath(os.fspath(path))
    drive, _ = os.path.splitdrive(absolute)
    if drive:
        return drive + os.sep
    return absolute


def set_file_mtime(fd: int, mtime: float) -> None:
    """Ustawia czas modyfikacji (i dostępu) na **otwartym** pliku.

    ``shutil.copystat`` i ``os.utime`` otwierają plik ponownie po ścieżce —
    przy setkach tysięcy plików na dysku USB to zauważalny koszt. Ponadto
    ``copystat`` przenosi atrybut „tylko do odczytu”, przez co kopii nie dało
    się później usunąć ani nadpisać (np. przy czyszczeniu starych wersji).

    Czas trzeba ustawić **po** ostatnim zapisie: NTFS nie nadpisuje jawnie
    ustawionego czasu przy zamknięciu uchwytu.
    """
    if os.name != "nt":
        os.utime(fd, (mtime, mtime))
        return
    import ctypes
    import msvcrt
    from ctypes import wintypes

    ticks = round((mtime + 11_644_473_600) * 10_000_000)
    filetime = wintypes.FILETIME(ticks & 0xFFFFFFFF, ticks >> 32)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.SetFileTime.argtypes = [
        wintypes.HANDLE,
        ctypes.c_void_p,
        ctypes.POINTER(wintypes.FILETIME),
        ctypes.POINTER(wintypes.FILETIME),
    ]
    kernel32.SetFileTime.restype = wintypes.BOOL
    handle = msvcrt.get_osfhandle(fd)
    if not kernel32.SetFileTime(handle, None, ctypes.byref(filetime), ctypes.byref(filetime)):
        raise ctypes.WinError(ctypes.get_last_error())


def make_writable(path: str | os.PathLike[str]) -> None:
    """Zdejmuje atrybut „tylko do odczytu”, jeśli jest ustawiony."""
    import stat

    with contextlib.suppress(OSError):
        os.chmod(long_path(path), stat.S_IWRITE | stat.S_IREAD)
