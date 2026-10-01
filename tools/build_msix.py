"""Buduje pakiet MSIX programu Sigelith Backup.

Kroki: PyInstaller w trybie katalogu (``TVB_ONEDIR=1``) → układ pakietu
z grafikami i manifestem → indeks zasobów (makepri) → ``makeappx pack``.
Opcjonalnie podpis (signtool) albo rejestracja układu do testów
(``Add-AppxPackage -Register`` — wymaga trybu dewelopera w Windows, ale nie
uprawnień administratora ani certyfikatu).

Użycie::

    .venv/Scripts/python.exe tools/build_msix.py                # pakiet testowy
    .venv/Scripts/python.exe tools/build_msix.py --register     # + rejestracja układu
    .venv/Scripts/python.exe tools/build_msix.py --identity-name AdamKoch.SigelithBackup  # do Sklepu

Do Sklepu pakietu nie podpisujemy — po certyfikacji podpisuje go Microsoft.
Nazwa, wydawca i jego nazwa wyświetlana muszą być dokładnie takie jak na stronie
„Tożsamość produktu” w Partner Center.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from string import Template
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from cleanvault import __version__  # noqa: E402

BUILD = ROOT / "build" / "msix"
LAYOUT = BUILD / "layout"
DIST = ROOT / "dist"
TEMPLATE = ROOT / "packaging" / "msix" / "AppxManifest.xml"

#: Konto wydawcy w Partner Center (firmowe, zweryfikowane 2026-09-26) — wspólne dla wszystkich
#: produktów konta; te same wartości ma Sigelith Desktop (Product identity, 2026-09-27).
PUBLISHER = "CN=322BC472-4859-4579-991B-25EE879D3796"
PUBLISHER_NAME = "Adam Koch"
#: Nazwa pakietu nadana przy rezerwacji „Sigelith Backup” (Product identity 2026-09-30,
#: Store ID 9P403GRSV1TX) — do Sklepu podajemy ją w ``--identity-name``.
STORE_IDENTITY = "AdamKoch.SigelithBackup"
#: Bez ``--identity-name`` pakiet ma nazwę testową i nadaje się tylko do prób na własnym komputerze.
TEST_IDENTITY = "AdamKoch.SigelithBackup.Test"

#: Grafiki z manifestu: nazwa, rozmiar w skali 100% i jaką część kafelka zajmuje ikona.
TILES = (
    ("Square44x44Logo", 44, 44, 1.0),
    ("StoreLogo", 50, 50, 1.0),
    ("Square150x150Logo", 150, 150, 0.6),
    ("Wide310x150Logo", 310, 150, 0.6),
)
SCALES = (100, 125, 150, 200, 400)
#: Ikona listy aplikacji i paska zadań w rozmiarach dokładnych (bez skalowania).
TARGET_SIZES = (16, 20, 24, 30, 32, 36, 40, 48, 60, 64, 72, 80, 96, 256)


def sdk_tool(name: str) -> Path:
    """Najnowsze narzędzie z Windows SDK (makeappx, makepri, signtool)."""
    base = Path(os.environ.get("PROGRAMFILES(X86)", "C:/Program Files (x86)")) / "Windows Kits" / "10" / "bin"
    found = sorted(
        base.glob(f"10.*/x64/{name}"),
        key=lambda path: tuple(int(part) for part in path.parent.parent.name.split(".")),
    )
    if not found:
        raise SystemExit(f"Nie znaleziono {name} — potrzebny jest Windows SDK.")
    return found[-1]


def package_version(version: str) -> str:
    """Wersja pakietu ma cztery liczby, a Sklep wymaga zera na ostatnim miejscu."""
    parts = [int(part) for part in version.split(".")][:3]
    parts += [0] * (3 - len(parts))
    return ".".join(str(part) for part in (*parts, 0))


def run(command: list[object], **kwargs) -> None:
    print(">", " ".join(str(part) for part in command), flush=True)
    subprocess.run([str(part) for part in command], check=True, **kwargs)


def build_app() -> Path:
    # --clean: bez tego PyInstaller potrafi uznać archiwum modułów za aktualne, bo lista
    # modułów się nie zmieniła, i zostawić w pakiecie stary kod (tak było 2026-09-29)
    env = dict(os.environ, TVB_ONEDIR="1")
    run(
        [sys.executable, "-m", "PyInstaller", ROOT / "cleanvault.spec", "--noconfirm", "--clean",
         "--distpath", BUILD / "dist", "--workpath", BUILD / "work"],
        env=env, cwd=ROOT,
    )
    return BUILD / "dist" / "SigelithBackup"


def write_assets(folder: Path) -> None:
    """Kafelki i ikony pakietu, rysowane od zera w każdym rozmiarze — bez rozmycia."""
    import make_icon
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QImage, QPainter
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication([])  # noqa: F841 - QPainter wymaga aplikacji Qt
    folder.mkdir(parents=True, exist_ok=True)
    for name, width, height, fill in TILES:
        for scale in SCALES:
            w, h = round(width * scale / 100), round(height * scale / 100)
            image = QImage(w, h, QImage.Format.Format_ARGB32)
            image.fill(Qt.GlobalColor.transparent)
            side = round(min(w, h) * fill)
            painter = QPainter(image)
            painter.drawImage((w - side) // 2, (h - side) // 2, make_icon.render(side))
            painter.end()
            image.save(str(folder / f"{name}.scale-{scale}.png"))
    for size in TARGET_SIZES:
        icon = make_icon.render(size)
        for variant in ("", "_altform-unplated", "_altform-lightunplated"):
            icon.save(str(folder / f"Square44x44Logo.targetsize-{size}{variant}.png"))


def write_manifest(layout: Path, identity: str, publisher: str, publisher_name: str, version: str) -> None:
    text = Template(TEMPLATE.read_text(encoding="utf-8")).substitute(
        identity_name=escape(identity),
        publisher=escape(publisher, {'"': "&quot;"}),
        publisher_display_name=escape(publisher_name),
        version=version,
    )
    (layout / "AppxManifest.xml").write_text(text, encoding="utf-8")


def make_pri(layout: Path) -> None:
    """Indeks zasobów: dzięki niemu Windows wybiera grafikę w rozmiarze ekranu.

    Indeksujemy osobny katalog z samymi grafikami i manifestem — cały układ to
    tysiące plików Qt, których indeks zasobów nie potrzebuje.
    """
    stage = BUILD / "pri"
    shutil.rmtree(stage, ignore_errors=True)
    shutil.copytree(layout / "Assets", stage / "Assets")
    shutil.copy2(layout / "AppxManifest.xml", stage / "AppxManifest.xml")
    makepri = sdk_tool("makepri.exe")
    config = BUILD / "priconfig.xml"
    run([makepri, "createconfig", "/cf", config, "/dq", "en-US", "/o"])
    # Bez podziału na pakiety zasobów (skale, języki): ten jest jeden, nie pakiet zbiorczy,
    # a grafiki z osobnych plików .pri nie byłyby w nim nigdy wczytane.
    text = config.read_text(encoding="utf-8")
    start, end = text.find("<packaging>"), text.find("</packaging>")
    if start != -1 and end != -1:
        config.write_text(text[:start] + text[end + len("</packaging>"):], encoding="utf-8")
    run([makepri, "new", "/pr", stage, "/cf", config, "/mn", stage / "AppxManifest.xml",
         "/of", layout / "resources.pri", "/o"])


def main() -> int:
    sys.stdout.reconfigure(errors="replace")  # polskie znaki w konsoli z inną stroną kodową
    parser = argparse.ArgumentParser(description="Buduje pakiet MSIX Sigelith Backup.")
    parser.add_argument("--skip-app", action="store_true",
                        help="bez PyInstallera — katalog programu z poprzedniego budowania")
    parser.add_argument("--identity-name", default=TEST_IDENTITY)
    parser.add_argument("--publisher", default=PUBLISHER)
    parser.add_argument("--publisher-display-name", default=PUBLISHER_NAME)
    parser.add_argument("--pfx", help="certyfikat do podpisu (instalacja poza Sklepem)")
    parser.add_argument("--pfx-password", default="")
    parser.add_argument("--register", action="store_true", help="rejestruje układ do testów (tryb dewelopera)")
    args = parser.parse_args()

    app_dir = BUILD / "dist" / "SigelithBackup" if args.skip_app else build_app()
    if not (app_dir / "SigelithBackup.exe").is_file():
        raise SystemExit(f"Brak zbudowanego programu w {app_dir}")
    shutil.rmtree(LAYOUT, ignore_errors=True)
    if LAYOUT.exists():
        raise SystemExit(f"Nie da się wyczyścić {LAYOUT} — czy program z tego układu jest uruchomiony?")
    shutil.copytree(app_dir, LAYOUT)
    write_assets(LAYOUT / "Assets")
    version = package_version(__version__)
    write_manifest(LAYOUT, args.identity_name, args.publisher, args.publisher_display_name, version)
    make_pri(LAYOUT)

    DIST.mkdir(exist_ok=True)
    package = DIST / f"SigelithBackup_{version}_x64.msix"
    run([sdk_tool("makeappx.exe"), "pack", "/d", LAYOUT, "/p", package, "/o"])
    if args.pfx:
        run([sdk_tool("signtool.exe"), "sign", "/fd", "SHA256", "/f", args.pfx, "/p", args.pfx_password, package])
    if args.register:
        manifest = LAYOUT / "AppxManifest.xml"
        run(["powershell", "-NoProfile", "-Command", f"Add-AppxPackage -Register '{manifest}'"])
    print(f"Pakiet: {package} ({package.stat().st_size / 1024 / 1024:.1f} MB)")
    if args.identity_name == TEST_IDENTITY:
        print("Uwaga: nazwa pakietu testowa — do Sklepu podaj "
              f"--identity-name {STORE_IDENTITY} (Product identity w Partner Center).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
