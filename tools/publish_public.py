"""Publikacja do publicznego repozytorium DeiFlagellum/sigelith-backup (migawka wydania).

Model jak przy Sigelith Desktop: to repozytorium (prywatne) jest ŹRÓDŁEM PRAWDY,
publiczne jest lustrem — jeden commit na publikację, bez historii roboczej
(dawne nazwy, notatki, adresy w metadanych starych commitów zostają tutaj).

Dlaczego `git archive`, a nie kopiowanie katalogu: kopiowanie nie respektuje
.gitignore — w katalogu roboczym leżą `dist/`, `build/` i `.venv/` (paczki
z bibliotekami Qt, stan programu z prywatnymi ścieżkami). `git archive` bierze
wyłącznie pliki ŚLEDZONE w HEAD i honoruje `export-ignore` z `.gitattributes`
(wewnętrzne `docs/`). Kontrola niżej sprawdza migawkę jeszcze raz, niezależnie.

Użycie::

    .venv/Scripts/python.exe tools/publish_public.py --dry-run   # tylko zbuduj i skontroluj
    .venv/Scripts/python.exe tools/publish_public.py             # wyślij
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = "DeiFlagellum/sigelith-backup"

FORBIDDEN_SUFFIXES = {".pfx", ".p12", ".pem", ".key", ".jks", ".keystore", ".cer", ".crt", ".env",
                      ".msgpack", ".msix", ".exe"}
FORBIDDEN_DIRS = {"dist", "build", ".venv", "venv", "__pycache__", "secrets", "docs"}
REQUIRED = ("LICENSE", "README.md", "README.pl.md", "assets/legal/LICENSE.txt",
            "assets/legal/THIRD-PARTY-NOTICES.txt", "requirements.txt")
#: Wzorce sklejane z kawałków, żeby ten plik (też w migawce) nie zgłaszał sam siebie.
FORBIDDEN_PATTERNS = [
    re.compile(b"-----BEGIN " + rb"[A-Z ]*" + b"PRIVATE KEY-----"),
    re.compile(b"gh" + rb"[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(b"github" + rb"_pat_[A-Za-z0-9_]{20,}"),
    re.compile(b"sk" + rb"_live_[A-Za-z0-9]{10,}"),
    re.compile(b"xox" + rb"[baprs]-[A-Za-z0-9-]{10,}"),
    # prywatne ścieżki z komputera autora
    re.compile(b"vers" + b"ace", re.IGNORECASE),
    re.compile(b"O:[/\\\\]Repo[/\\\\]" + b"beattime", re.IGNORECASE),
]
TEXT = {".py", ".md", ".txt", ".json", ".toml", ".spec", ".xml", ".cfg", ".ini", ".yml", ".yaml",
        ".gitignore", ".gitattributes", ".ps1"}


def run(command: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(command, cwd=cwd or ROOT, capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
    if result.returncode != 0:
        raise SystemExit(f"polecenie nie powiodło się: {' '.join(command)}\n{result.stdout}\n{result.stderr}")
    return result.stdout


def version() -> str:
    text = (ROOT / "cleanvault" / "__init__.py").read_text(encoding="utf-8")
    match = re.search(r'__version__\s*=\s*"([^"]+)"', text)
    if not match:
        raise SystemExit("nie znalazłem __version__ w cleanvault/__init__.py")
    return match.group(1)


def require_clean_tree() -> None:
    """Publikujemy z HEAD — niezapisane zmiany śledzonych plików to prawie na pewno pomyłka."""
    dirty = run(["git", "status", "--porcelain", "--untracked-files=no"]).strip()
    if dirty:
        raise SystemExit("niezacommitowane zmiany — najpierw commit:\n" + dirty)


def snapshot(target: Path) -> None:
    with tempfile.NamedTemporaryFile(suffix=".tar", delete=False) as handle:
        tar_path = Path(handle.name)
    try:
        with open(tar_path, "wb") as out:
            result = subprocess.run(["git", "archive", "--format=tar", "HEAD"], cwd=ROOT, stdout=out,
                                    stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise SystemExit("git archive nie powiodło się: " + result.stderr.decode("utf-8", "replace"))
        with tarfile.open(tar_path) as tar:
            tar.extractall(target, filter="data")
    finally:
        tar_path.unlink(missing_ok=True)


def check(folder: Path) -> list[str]:
    problems = []
    for path in sorted(folder.rglob("*")):
        relative = path.relative_to(folder)
        if any(part.lower() in FORBIDDEN_DIRS for part in relative.parts[:-1 if path.is_file() else None]):
            problems.append(f"zakazany katalog: {relative}")
            continue
        if path.is_dir():
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            problems.append(f"zakazany typ pliku: {relative}")
        if path.suffix.lower() in TEXT or path.name in {".gitignore", ".gitattributes"}:
            data = path.read_bytes()
            for pattern in FORBIDDEN_PATTERNS:
                if pattern.search(data):
                    problems.append(f"podejrzana treść ({pattern.pattern[:24]!r}…): {relative}")
    for required in REQUIRED:
        if not (folder / required).is_file():
            problems.append(f"brak wymaganego pliku: {required}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true", help="tylko zbuduj i skontroluj migawkę")
    parser.add_argument("--message", default="", help="treść commita (domyślnie: Sigelith Backup <wersja>)")
    args = parser.parse_args()
    sys.stdout.reconfigure(errors="replace")
    require_clean_tree()
    v = version()
    with tempfile.TemporaryDirectory() as tmp:
        snap = Path(tmp) / "snapshot"
        snap.mkdir()
        snapshot(snap)
        files = [p for p in snap.rglob("*") if p.is_file()]
        print(f"Sigelith Backup {v} — migawka z HEAD: {len(files)} plików")
        problems = check(snap)
        if problems:
            print("KONTROLA NIE PRZESZŁA:")
            for problem in problems:
                print("  -", problem)
            return 1
        print("kontrola: czysto (bez kluczy, paczek, stanu programu, notatek docs/ i prywatnych ścieżek)")
        if args.dry_run:
            print("--dry-run: nic nie wysłano")
            return 0
        work = Path(tmp) / "repo"
        run(["git", "clone", "--depth", "1", f"https://github.com/{REPO}.git", str(work)])
        empty = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=work,
                               capture_output=True).returncode != 0
        if empty:
            run(["git", "checkout", "-b", "main"], cwd=work)
        for item in work.iterdir():
            if item.name != ".git":
                shutil.rmtree(item) if item.is_dir() else item.unlink()
        for item in snap.iterdir():
            shutil.copytree(item, work / item.name) if item.is_dir() else shutil.copy2(item, work / item.name)
        run(["git", "add", "-A"], cwd=work)
        if not run(["git", "status", "--porcelain"], cwd=work).strip():
            print("publiczne repozytorium jest już aktualne — nic do wysłania")
            return 0
        run(["git", "commit", "-m", args.message or f"Sigelith Backup {v}"], cwd=work)
        run(["git", "push", "origin", "HEAD"], cwd=work)
        print(f"wysłano do https://github.com/{REPO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
