# -*- mode: python ; coding: utf-8 -*-
"""Konfiguracja budowania Sigelith Backup: pojedynczy plik EXE albo katalog pod MSIX.

Budowanie::

    .venv\\Scripts\\pyinstaller.exe cleanvault.spec --noconfirm --clean

Uwagi względem starego ``qt_gui.spec``:

* ``datas`` było puste, więc ``QIcon("icon.png")`` w zbudowanej aplikacji
  nie znajdowało pliku i ikony po prostu znikały — teraz zasoby są dołączane,
  a kod sięga po nie przez ``cleanvault.paths.resource_path``;
* backendy ``keyring`` są ładowane dynamicznie, więc PyInstaller ich nie wykrywa —
  trzeba je wymienić w ``hiddenimports``, inaczej zapamiętywanie haseł działa
  w trybie deweloperskim, a w EXE cicho przestaje;
* moduły Qt, których nie używamy (WebEngine, Quick, 3D, multimedia), potrafią
  dołożyć kilkaset MB — dlatego trafiają do ``excludes``.
"""

import os
import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules, copy_metadata

#: ``TVB_ONEDIR=1`` — katalog zamiast jednego pliku. Tak budujemy pakiet MSIX:
#: EXE jednoplikowy rozpakowuje się przy każdym starcie do katalogu tymczasowego,
#: a w pakiecie pliki i tak leżą już rozpakowane w katalogu instalacji.
ONEDIR = os.environ.get("TVB_ONEDIR") == "1"

hidden = [
    # keyring wybiera backend w czasie działania — statyczna analiza go nie widzi.
    "keyring.backends.Windows",
    "keyring.backends.null",
    "win32ctypes.core",
    "win32ctypes.core.ctypes",
    # argon2-cffi opiera się na rozszerzeniu ładowanym dynamicznie.
    "_cffi_backend",
]
# Katalogi tłumaczeń ładuje ``importlib`` po kodzie języka — analiza statyczna
# ich nie widzi, a bez nich wersja EXE po cichu zostałaby wyłącznie po polsku.
# Wyliczamy je z plików, a nie przez ``collect_submodules``: ten importuje pakiet
# w osobnym procesie, który nie widzi katalogu projektu, i zwraca pustą listę
# bez żadnego błędu — tak właśnie zniknęło tłumaczenie z pierwszej kompilacji.
_locale_dir = Path(SPECPATH) / "cleanvault" / "locale"  # noqa: F821 - zmienna PyInstallera
hidden += ["cleanvault.locale"] + [
    f"cleanvault.locale.{module.stem}"
    for module in sorted(_locale_dir.glob("*.py"))
    if module.stem != "__init__"
]
hidden += collect_submodules("Cryptodome.Cipher")
hidden += collect_submodules("Cryptodome.Hash")
hidden += collect_submodules("Cryptodome.Protocol")
# Start przy logowaniu w pakiecie MSIX (StartupTask) — import wewnątrz funkcji.
hidden += collect_submodules("winrt.windows.applicationmodel")
hidden += collect_submodules("winrt.windows.foundation")
hidden += collect_submodules("winrt.system")
# Kopia „na bieżąco”: watchdog wybiera obserwatora systemu w czasie działania
# (w Windows ReadDirectoryChangesW) — analiza statyczna go nie widzi.
hidden += ["watchdog.observers.read_directory_changes", "watchdog.observers.winapi",
           "watchdog.observers.polling"]

excluded = [
    "tkinter",
    "unittest",
    "pydoc_data",
    # cffi sięga po setuptools tylko przy kompilacji rozszerzeń (ffi.compile) — program
    # używa gotowego, skompilowanego modułu argon2, więc setuptools zbędnie pęczniałoby paczkę
    "setuptools",
    "_distutils_hack",
    "pkg_resources",
    "pytest",
    "PySide6.QtWebEngineCore",
    "PySide6.QtWebEngineWidgets",
    "PySide6.QtWebEngineQuick",
    "PySide6.QtQuick",
    "PySide6.QtQuick3D",
    "PySide6.QtQml",
    "PySide6.Qt3DCore",
    "PySide6.Qt3DRender",
    "PySide6.QtMultimedia",
    "PySide6.QtMultimediaWidgets",
    "PySide6.QtCharts",
    "PySide6.QtDataVisualization",
    "PySide6.QtBluetooth",
    "PySide6.QtPositioning",
    "PySide6.QtSerialPort",
    "PySide6.QtTest",
    "PySide6.QtSql",
    "PySide6.QtPdf",
    "PySide6.QtPdfWidgets",
    "PySide6.QtNetworkAuth",
    "PySide6.QtDesigner",
    "PySide6.QtHelp",
    "PySide6.QtOpenGL",
    "PySide6.QtOpenGLWidgets",
    # zależności py_ecc.bls — kapsuła czasu używa tylko rdzenia py_ecc.optimized_bls12_381
    "py_ecc.bls",
    "eth_utils",
    "eth_typing",
    "eth_hash",
    "pydantic",
    "pydantic_core",
    "cytoolz",
    "toolz",
]

a = Analysis(
    ["app.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("assets/icon.png", "assets"),
        ("assets/icon.ico", "assets"),
        # cały katalog: pliki SVG oraz licencja MIT zestawu Bootstrap Icons
        ("assets/icons", "assets/icons"),
        # skrypt ratunkowy kopiowany do katalogu kopii — jako tekst, nie moduł
        ("assets/recovery", "assets/recovery"),
        # licencja programu, informacje o licencjach składników i pełne teksty licencji
        ("assets/legal", "assets/legal"),
        # py_ecc przy imporcie czyta własną wersję z metadanych pakietu
        *copy_metadata("py_ecc"),
    ],
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excluded,
    noarchive=False,
    optimize=0,
)

# winrt przynosi starszą bibliotekę MSVCP140 (14.29) niż Qt (14.44). Zostaje tylko ta
# z Qt: proces używa jednej, tej załadowanej pierwszej, a Qt ze starszą się wywraca.
a.binaries = [
    entry for entry in a.binaries
    if not (entry[0].lower().startswith("winrt") and "msvcp140" in entry[0].lower())
]

# Części Qt, których program nie używa, a które hak PySide6 zbiera hurtem. Klawiatura
# ekranowa Qt (Qt Virtual Keyboard) jest w wersji otwartej wyłącznie na GPL-3.0 — reszta
# Qt jest na LGPL-3.0 — więc w programie o zamkniętej licencji nie może się znaleźć.
# Reszta to megabajty bez pożytku: PDF, QML/Quick (ciągnięte przez klawiaturę), programowy
# OpenGL, TLS Qt z własną kopią OpenSSL (połączenia sieciowe robi Python) i wtyczki
# formatów obrazów, których program nie wyświetla. Każdy wycięty składnik to też jedna
# licencja mniej do wykazania w informacjach o licencjach.
QT_KEEP_PLUGINS = {
    "pyside6/plugins/platforms/qwindows.dll",
    "pyside6/plugins/styles/qmodernwindowsstyle.dll",
    "pyside6/plugins/iconengines/qsvgicon.dll",
    "pyside6/plugins/imageformats/qsvg.dll",
    "pyside6/plugins/imageformats/qico.dll",
}
QT_UNUSED_LIBRARIES = ("qt6virtualkeyboard", "qt6pdf", "qt6qml", "qt6quick", "qt6opengl", "opengl32sw")
#: Tłumaczenia Qt: przyciski okien standardowych („Tak”, „Nie”, „Anuluj”) w językach
#: programu (cleanvault/i18n.py, LANGUAGES). Wersja angielska tłumaczenia nie potrzebuje.
QT_KEEP_TRANSLATIONS = {
    f"pyside6/translations/qtbase_{name}.qm"
    for name in ("pl", "de", "es", "fr", "ru", "tr", "ja", "ko", "zh_cn", "ar")
}


def _unused_qt(entry) -> bool:
    name = entry[0].replace(chr(92), "/").lower()
    if name in ("libcrypto-3-x64.dll", "libssl-3-x64.dll"):
        return True  # OpenSSL dla wtyczek TLS Qt; Python ma własne libcrypto-3/libssl-3
    if not name.startswith("pyside6/"):
        return False
    if name.startswith("pyside6/translations/"):
        return name not in QT_KEEP_TRANSLATIONS
    if name.startswith("pyside6/plugins/"):
        return name not in QT_KEEP_PLUGINS
    return any(part in name for part in QT_UNUSED_LIBRARIES)


a.binaries = [entry for entry in a.binaries if not _unused_qt(entry)]
a.datas = [entry for entry in a.datas if not _unused_qt(entry)]
if any("virtualkeyboard" in entry[0].lower() for entry in a.binaries):
    raise SystemExit("Qt Virtual Keyboard (tylko GPL-3.0) nie może trafić do programu — popraw QT_KEEP_PLUGINS.")

# Informacje o licencjach (assets/legal/THIRD-PARTY-NOTICES.txt) muszą być aktualne i obejmować
# każdą bibliotekę, która trafia do programu — licencje MIT, BSD, Apache i LGPL tego wymagają.
sys.path.insert(0, str(Path(SPECPATH) / "tools"))  # noqa: F821 - zmienna PyInstallera
import third_party_notices  # noqa: E402

_stale = third_party_notices.stale_files()
if _stale:
    raise SystemExit(f"Nieaktualne pliki licencji w assets/legal: {', '.join(_stale)} — uruchom tools/third_party_notices.py")
_tops = {name.split(".")[0] for name, *_rest in a.pure}
_tops |= {entry[0].replace(chr(92), "/").split("/")[0].split(".")[0] for entry in a.binaries}
_unlisted = third_party_notices.unlisted(_tops)
if _unlisted:
    raise SystemExit("Do programu trafiają biblioteki bez informacji o licencji: " + ", ".join(_unlisted))

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    *([] if ONEDIR else [a.binaries, a.datas]),
    [],
    exclude_binaries=ONEDIR,
    name="SigelithBackup",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    # UPX bywa fałszywie wykrywany przez programy antywirusowe i potrafi uszkodzić
    # biblioteki Qt — świadomie rezygnujemy z kompresji.
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="assets/icon.ico",
)

if ONEDIR:
    coll = COLLECT(  # noqa: F821 - klasa PyInstallera
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=False,
        name="SigelithBackup",
    )
