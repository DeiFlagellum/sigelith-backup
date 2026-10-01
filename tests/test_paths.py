"""Testy budowania ścieżek — w tym nazw, których Windows sam z siebie nie obsłuży."""

from __future__ import annotations

import contextlib
import os
import shutil

import pytest

from cleanvault import engine
from cleanvault.engine import BackupConfig, Reporter
from cleanvault.paths import long_path
from cleanvault.snapshot import Manifest

WINDOWS = os.name == "nt"
pytestmark = pytest.mark.skipif(not WINDOWS, reason="prefiks \\\\?\\ dotyczy wyłącznie Windows")


def test_reserved_device_name_stays_a_file_path():
    """Plik o nazwie ``nul`` nie może zamienić się w ścieżkę urządzenia.

    Regresja z prawdziwej kopii: ``os.path.abspath`` zamieniał
    ``O:\\Repo\\laborbuch\\nul`` na ``\\\\.\\nul``, a stąd powstawało
    ``\\\\?\\UNC\\.\\nul`` — każdy przebieg kopii kończył się błędem, więc
    wersja nigdy nie dostawała statusu „kompletna”.
    """
    for name in ("nul", "con", "aux", "prn", "com1", "lpt1"):
        result = long_path(rf"O:\Repo\projekt\{name}")
        assert result == rf"\\?\O:\Repo\projekt\{name}"
        assert "\\\\.\\" not in result


def test_trailing_dot_and_space_are_preserved():
    """Nazwy z kropką lub spacją na końcu tworzy Linux; Windows je obcina."""
    assert long_path(r"O:\dane\kropka.") == "\\\\?\\O:\\dane\\kropka."
    assert long_path(r"O:\dane\spacja ") == "\\\\?\\O:\\dane\\spacja "


def test_paths_are_still_normalised_and_unc_is_handled():
    assert long_path(r"O:\a\..\b\plik.txt") == "\\\\?\\O:\\b\\plik.txt"
    assert long_path(r"\\serwer\udzial\plik") == "\\\\?\\UNC\\serwer\\udzial\\plik"
    assert long_path("\\\\?\\O:\\gotowe") == "\\\\?\\O:\\gotowe"
    assert long_path("wzgledny.txt").startswith("\\\\?\\")


def _write_odd_file(folder, name: str, data: bytes) -> str:
    """Tworzy plik o nazwie, której zwykłe API Windows nie przyjmie."""
    path = long_path(os.path.join(str(folder), name))
    with open(path, "wb") as handle:
        handle.write(data)
    return path


def test_backup_copies_files_windows_cannot_name(tmp_path):
    """Kopia ma przenieść także pliki o nazwach zarezerwowanych i z kropką na końcu."""
    source = tmp_path / "zrodlo"
    source.mkdir()
    (source / "zwykly.txt").write_text("zwykła treść", encoding="utf-8")
    odd = {"nul": b"tresc pliku nul", "kropka.": b"tresc z kropka"}
    created = [_write_odd_file(source, name, data) for name, data in odd.items()]
    dest = tmp_path / "kopia"

    try:
        config = BackupConfig(
            sources=[str(source)], destination=str(dest), structure="dated",
            verify_after_write=True, excludes=[], catchup_passes=0,
        )
        plan = engine.plan_backup(config, Reporter())
        result = engine.run_backup(plan, None, Reporter())

        assert result.ok, result.errors
        assert result.files_done == 3
        manifest = Manifest.load(dest)
        for name, data in odd.items():
            entry = manifest.entries[f"zrodlo/{name}"]
            with open(long_path(dest / entry.stored), "rb") as handle:
                assert handle.read() == data
        assert manifest.runs[plan.version].complete, "kopia z takim plikiem musi być kompletna"
    finally:
        # Ani shutil.rmtree, ani pytest nie usuną pliku o nazwie "nul".
        for path in created:
            with contextlib.suppress(OSError):
                os.unlink(path)
        for stored in (dest.rglob("*") if dest.exists() else []):
            if stored.is_file():
                with contextlib.suppress(OSError):
                    os.unlink(long_path(stored))
        shutil.rmtree(dest, ignore_errors=True)



def test_data_dir_prefers_new_name_but_keeps_using_the_old_one(tmp_path, monkeypatch):
    """Zmiana nazwy produktu nie może odciąć użytkownika od jego szablonów i historii."""
    from cleanvault import paths

    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))

    oldest = tmp_path / "CleanVault"
    oldest.mkdir()
    (oldest / "state.msgpack").write_bytes(b"stan")
    assert paths.data_dir() == oldest, "program przestał widzieć dotychczasowy stan"

    # Druga zmiana nazwy (Time Vault Backup → Sigelith Backup): nowszy stary katalog wygrywa.
    previous = tmp_path / "Time Vault Backup"
    previous.mkdir()
    assert paths.data_dir() == previous

    (tmp_path / paths.APP_DIR_NAME).mkdir()
    assert paths.data_dir() == tmp_path / paths.APP_DIR_NAME == tmp_path / "Sigelith Backup"


def test_data_dir_creates_the_new_directory_when_there_is_no_history(tmp_path, monkeypatch):
    from cleanvault import paths

    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    created = paths.data_dir()
    assert created == tmp_path / paths.APP_DIR_NAME and created.is_dir()
