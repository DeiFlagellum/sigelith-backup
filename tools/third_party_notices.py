"""Plik z licencjami składników programu: ``assets/legal/THIRD-PARTY-NOTICES.txt``.

Licencje MIT, BSD, Apache i pozostałe wymagają dołączenia do programu informacji
o prawach autorskich i tekstu licencji, a zasady Microsoft Store (10.2) — wszystkich
informacji wymaganych prawem. Plik powstaje z:

* metadanych zainstalowanych bibliotek Pythona — od zależności z ``requirements.txt``
  w dół, bez tych, które nie trafiają do programu (``NOT_BUNDLED``);
* wycinka atrybucji ze źródeł Qt 6.11.2 (``packaging/legal``) — składniki wbudowane
  w moduły Core, Gui, Network i Svg, bez składników innych systemów;
* opisów poniżej: Python, Qt i PySide6 na LGPL, ikony, biblioteki Microsoft.

Użycie::

    .venv/Scripts/python.exe tools/third_party_notices.py          # zapisuje plik
    .venv/Scripts/python.exe tools/third_party_notices.py --check  # czy plik jest aktualny
    .venv/Scripts/python.exe tools/third_party_notices.py --bundle <PYZ-00.toc> <katalog programu>
        # czy każda biblioteka, która trafiła do zbudowanego programu, jest wykazana
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from importlib import metadata
from pathlib import Path

from packaging.requirements import Requirement

ROOT = Path(__file__).resolve().parent.parent
LEGAL = ROOT / "assets" / "legal"
OUTPUT = LEGAL / "THIRD-PARTY-NOTICES.txt"
#: Licencja Pythona z interpretera, którym budujemy — obejmuje też biblioteki wbudowane
#: w Pythona dla Windows (OpenSSL, libffi, bzip2, xz, zlib, expat, mpdecimal).
PYTHON_LICENSE = LEGAL / "PYTHON-LICENSE.txt"
PACKAGING = ROOT / "packaging" / "legal"
QT_ATTRIBUTIONS = PACKAGING / "qt-6.11.2-attributions.json"
QT_VERSION = "6.11.2"

#: Zależności, które są zainstalowane, ale do programu nie trafiają (patrz ``cleanvault.spec``).
NOT_BUNDLED = {
    "pyside6-addons": "moduły dodatkowe Qt — program z nich nie korzysta",
    # py_ecc wymaga ich tylko w podpakiecie py_ecc.bls, którego program nie importuje
    # (hash do G1 i kompresję punktów ma cleanvault/ibe.py) — razem z pydantic
    "eth-utils": "tylko dla py_ecc.bls — program go nie importuje",
    "eth-typing": "tylko dla py_ecc.bls — program go nie importuje",
}
#: Biblioteki Qt for Python — licencja LGPL-3.0 opisana osobno, z tekstem w LGPL-3.0.txt.
QT_DISTRIBUTIONS = {"pyside6", "pyside6-essentials", "shiboken6"}
#: Teksty licencji, których pakiet nie dołącza do swoich metadanych.
EXTRA_LICENSES = {
    "winrt-runtime": ["pywinrt.txt"],
    "winrt-windows-applicationmodel": ["pywinrt.txt"],
    "winrt-windows-foundation": ["pywinrt.txt"],
    "argon2-cffi-bindings": ["phc-winner-argon2.txt"],
}
_LICENSE_FILE = re.compile(r"^(LICEN[CS]E|COPYING|NOTICE|AUTHORS)", re.IGNORECASE)


def normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def runtime_distributions() -> dict[str, metadata.Distribution]:
    """Biblioteki wymagane w działającym programie: ``requirements.txt`` i ich zależności."""
    roots = []
    for line in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines():
        spec = line.split("#", 1)[0].strip()
        if spec:
            roots.append(Requirement(spec))
    found: dict[str, metadata.Distribution] = {}
    todo = [req for req in roots if req.marker is None or req.marker.evaluate()]
    while todo:
        req = todo.pop()
        key = normalize(req.name)
        if key in found or key in NOT_BUNDLED:
            continue
        try:
            dist = metadata.distribution(req.name)
        except metadata.PackageNotFoundError:
            continue  # zależność opcjonalna, której nie instalujemy (np. narzędzia fastcdc)
        found[key] = dist
        for requirement in dist.requires or []:
            sub = Requirement(requirement)
            if sub.marker is None or sub.marker.evaluate({"extra": ""}):
                todo.append(sub)
    return dict(sorted(found.items()))


def _license_name(dist: metadata.Distribution) -> str:
    expression = dist.metadata.get("License-Expression")
    if expression:
        return expression
    text = (dist.metadata.get("License") or "").strip()
    if text and "\n" not in text and len(text) < 80:
        return text
    classifiers = [c.split("::")[-1].strip() for c in dist.metadata.get_all("Classifier") or []
                   if c.startswith("License ::")]
    return ", ".join(classifiers) or "zob. tekst licencji / see license text"


def _homepage(dist: metadata.Distribution) -> str:
    home = dist.metadata.get("Home-page")
    if home:
        return home
    for url in dist.metadata.get_all("Project-URL") or []:
        label, _, address = url.partition(",")
        if label.strip().lower() in ("homepage", "home", "source", "repository", "source code"):
            return address.strip()
    urls = dist.metadata.get_all("Project-URL") or []
    return urls[0].partition(",")[2].strip() if urls else ""


def _license_texts(key: str, dist: metadata.Distribution) -> list[tuple[str, str]]:
    names = list(dict.fromkeys(dist.metadata.get_all("License-File") or []))
    if not names:
        names = sorted({Path(str(f)).name for f in dist.files or []
                        if _LICENSE_FILE.match(Path(str(f)).name) and ".dist-info" in str(f)})
    texts = []
    for name in names:
        for candidate in (f"licenses/{name}", name):
            text = dist.read_text(candidate)
            if text:
                texts.append((name, text.strip()))
                break
    for extra in EXTRA_LICENSES.get(key, []):
        texts.append((extra, (PACKAGING / "extra-licenses" / extra).read_text(encoding="utf-8").strip()))
    return texts


def _heading(text: str, char: str = "=") -> str:
    return f"{text}\n{char * len(text)}\n"


def render() -> str:
    dists = runtime_distributions()
    qt = json.loads(QT_ATTRIBUTIONS.read_text(encoding="utf-8"))
    pyside = dists["pyside6"].version
    python = ".".join(map(str, sys.version_info[:3]))
    out: list[str] = []
    out.append(_heading("Sigelith Backup — third-party notices / informacje o licencjach składników"))
    out.append(
        "PL: Sigelith Backup zawiera oprogramowanie osób trzecich wymienione niżej. Każdy\n"
        "składnik podlega własnej licencji; teksty licencji są w tym pliku albo w plikach obok\n"
        "(LGPL-3.0.txt, GPL-3.0.txt, PYTHON-LICENSE.txt). Na ekranie „O programie” jest ta sama treść.\n\n"
        "EN: Sigelith Backup includes the third-party software listed below. Each component is\n"
        "subject to its own license; the license texts are in this file or in the files next to it\n"
        "(LGPL-3.0.txt, GPL-3.0.txt, PYTHON-LICENSE.txt).\n"
    )

    out.append(_heading(f"1. Qt {QT_VERSION} and Qt for Python (PySide6, Shiboken6) {pyside}", "-"))
    out.append(
        f"The program uses Qt {QT_VERSION} and Qt for Python {pyside} by The Qt Company Ltd. under the\n"
        "GNU Lesser General Public License version 3 (LGPL-3.0-only, chosen from the offered\n"
        "LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only). Full texts: LGPL-3.0.txt and GPL-3.0.txt.\n\n"
        "* Qt and PySide6 are used unmodified, as dynamically loaded libraries (Qt6*.dll, the\n"
        "  PySide6 and shiboken6 modules). In the Microsoft Store (MSIX) version they are separate\n"
        "  files in the program folder and can be replaced with interface-compatible versions\n"
        "  built from modified sources.\n"
        "* Source code of the exact versions used:\n"
        f"    Qt {QT_VERSION}:      https://download.qt.io/official_releases/qt/6.11/{QT_VERSION}/\n"
        f"    PySide6 {pyside}: https://download.qt.io/official_releases/QtForPython/pyside6/"
        f"PySide6-{pyside}-src/\n"
        "* Qt is a registered trademark of The Qt Company Ltd. and its subsidiaries.\n"
        "* Qt itself contains third-party components — see section 4.\n"
    )

    out.append(_heading(f"2. Python {python}", "-"))
    out.append(
        "The program runs on the Python interpreter and standard library by the Python Software\n"
        "Foundation under the PSF License Version 2. PYTHON-LICENSE.txt contains that license\n"
        "together with the licenses of the libraries built into Python for Windows (among them\n"
        "OpenSSL, libffi, bzip2, xz, zlib, expat and mpdecimal).\n"
    )

    out.append(_heading("3. Python libraries / biblioteki Pythona", "-"))
    for key, dist in dists.items():
        name = dist.metadata["Name"]
        license_name = _license_name(dist)
        if key in QT_DISTRIBUTIONS:
            license_name = "LGPL-3.0-only (see section 1)"
        out.append(f"{name} {dist.version}\n    License: {license_name}\n    {_homepage(dist)}\n")

    out.append(_heading(f"4. Components built into Qt {QT_VERSION} (Core, Gui, Network, Svg)", "-"))
    out.append(
        "Listed from the qt_attribution.json files of the Qt sources. Where a component is offered\n"
        "under alternative licenses, the license used by this program is given in brackets.\n"
        "License texts: section 7.\n"
    )
    for entry in qt:
        license_line = entry["license"]
        if entry["elected"] != entry["license"]:
            license_line += f"  [{entry['elected']}]"
        lines = [f"{entry['name']}" + (f" {entry['version']}" if entry["version"] else ""),
                 f"    Qt module: {entry['module']}", f"    License: {license_line}"]
        if entry["copyright"]:
            lines += ["    " + line for line in entry["copyright"].splitlines()]
        if entry["homepage"]:
            lines.append(f"    {entry['homepage']}")
        out.append("\n".join(lines) + "\n")

    out.append(_heading("5. Other components / pozostałe składniki", "-"))
    out.append(
        "Bootstrap Icons 1.13.1 — Copyright (c) 2019-2024 The Bootstrap Authors — MIT License\n"
        "    https://icons.getbootstrap.com/ (full text: section 6, Bootstrap Icons)\n\n"
        "Microsoft Visual C++ Runtime and Universal C Runtime (vcruntime140*.dll, msvcp140*.dll,\n"
        "ucrtbase.dll, api-ms-win-*.dll) — Microsoft Distributable Code, redistributed under the\n"
        "Microsoft Visual Studio license terms. Copyright (c) Microsoft Corporation.\n\n"
        "PyInstaller bootloader — GPL-2.0-or-later with the PyInstaller bootloader exception, which\n"
        "allows distributing programs built with it under any license. https://pyinstaller.org\n"
    )

    out.append(_heading("6. License texts of Python libraries / teksty licencji bibliotek", "-"))
    for key, dist in dists.items():
        if key in QT_DISTRIBUTIONS:
            continue
        for file_name, text in _license_texts(key, dist):
            out.append(f"--- {dist.metadata['Name']} {dist.version} — {file_name} ---\n\n{text}\n")
    icons = (ROOT / "assets" / "icons" / "LICENSE").read_text(encoding="utf-8").strip()
    out.append(f"--- Bootstrap Icons 1.13.1 — LICENSE ---\n\n{icons}\n")

    out.append(_heading(f"7. License texts for components built into Qt {QT_VERSION}", "-"))
    used = sorted({part.strip() for entry in qt for part in entry["elected"].split(" AND ")})
    for license_id in used:
        text = (PACKAGING / "qt-licenses" / f"{license_id}.txt").read_text(encoding="utf-8").strip()
        out.append(f"--- {license_id} ---\n\n{text}\n")
    return "\n".join(out).replace("\r\n", "\n")


def unlisted(top_level_names: set[str]) -> list[str]:
    """Biblioteki, z których pochodzą podane moduły najwyższego poziomu, a których nie wykazano.

    ``cleanvault.spec`` woła to przy każdym budowaniu z listą modułów i plików binarnych,
    które PyInstaller zebrał do programu.
    """
    mapping = metadata.packages_distributions()
    found = {normalize(dist) for top in top_level_names for dist in mapping.get(top, [])}
    # NOT_BUNDLED: np. PySide6_Addons dzieli katalog PySide6 z Essentials, więc samo
    # „PySide6” wskazuje na oba pakiety; narzędzia PyInstallera to nie kod programu
    ignored = set(NOT_BUNDLED) | {"pyinstaller", "pyinstaller-hooks-contrib"}
    return sorted(found - set(runtime_distributions()) - ignored)


def python_license_text() -> str:
    return (Path(sys.base_prefix) / "LICENSE.txt").read_text(encoding="utf-8").replace("\r\n", "\n")


def stale_files() -> list[str]:
    """Pliki w ``assets/legal``, które nie odpowiadają temu, co wygenerowałoby narzędzie."""
    wanted = ((OUTPUT, render()), (PYTHON_LICENSE, python_license_text()))
    return [path.name for path, text in wanted
            if not path.exists() or path.read_text(encoding="utf-8") != text]


def bundled_names(pyz_toc: Path, app_dir: Path) -> set[str]:
    """Moduły najwyższego poziomu w zbudowanym programie (spis PYZ i katalog ``_internal``)."""
    toc = ast.literal_eval(pyz_toc.read_text(encoding="utf-8"))
    tops = {entry[0].split(".")[0] for entry in toc[1]}
    internal = app_dir / "_internal"
    if internal.is_dir():
        tops |= {path.name.split(".")[0] for path in internal.iterdir()}
    return tops


def main() -> int:
    sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="tylko sprawdza, czy plik jest aktualny")
    parser.add_argument("--bundle", nargs=2, metavar=("PYZ_TOC", "APP_DIR"),
                        help="sprawdza, czy każda spakowana biblioteka jest wykazana")
    args = parser.parse_args()
    if args.bundle:
        missing = unlisted(bundled_names(Path(args.bundle[0]), Path(args.bundle[1])))
        if missing:
            print("Spakowane, a niewykazane w informacjach o licencjach:", ", ".join(missing))
            return 1
        print("Wszystkie spakowane biblioteki są wykazane w informacjach o licencjach.")
        return 0
    text = render()
    python_license = python_license_text()
    if args.check:
        stale = stale_files()
        if stale:
            print("Nieaktualne:", ", ".join(stale), "— uruchom tools/third_party_notices.py")
            return 1
        print("Informacje o licencjach są aktualne.")
        return 0
    OUTPUT.write_text(text, encoding="utf-8", newline="\n")
    PYTHON_LICENSE.write_text(python_license, encoding="utf-8", newline="\n")
    print(f"Zapisano {OUTPUT} ({len(text) // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
