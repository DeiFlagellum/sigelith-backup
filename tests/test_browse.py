"""Przeglądanie kopii, historia pliku i wyszukiwarka."""

from __future__ import annotations

import os
import random
import time

import pytest

from cleanvault import browse, chunks, crypto, engine, rescue
from cleanvault.crypto import KdfParams, PasswordKeyring
from cleanvault.engine import BackupConfig, Reporter


@pytest.fixture(autouse=True)
def small_chunks(monkeypatch):
    monkeypatch.setattr(chunks, "DELTA_MIN_SIZE", 1024 * 1024)
    monkeypatch.setattr(chunks, "MIN_CHUNK", 16 * 1024)
    monkeypatch.setattr(chunks, "AVG_CHUNK", 64 * 1024)
    monkeypatch.setattr(chunks, "MAX_CHUNK", 256 * 1024)
    monkeypatch.setattr(chunks, "WINDOW", 1024 * 1024)


@pytest.fixture()
def source(tmp_path):
    root = tmp_path / "Dokumenty"
    (root / "Umowy" / "2026").mkdir(parents=True)
    (root / "Umowy" / "2026" / "Najem.txt").write_text("umowa najmu", encoding="utf-8")
    (root / "Zestawienie.CSV").write_text("a;b\n1;2\n", encoding="utf-8")
    (root / "obraz.vhdx").write_bytes(random.Random(2).randbytes(2 * 1024 * 1024))
    return root


def keyring():
    return PasswordKeyring("Hasło-przeglądania", KdfParams(crypto.KDF_PBKDF2_SHA256, b"p" * 16, 1000))


def _backup(source, destination, key=None, **kwargs):
    config = BackupConfig(sources=[str(source)], destination=str(destination), structure="dated",
                          excludes=[], stamp_updates=False, catchup_passes=0, encrypt=key is not None, **kwargs)
    plan = engine.plan_backup(config, Reporter())
    result = engine.run_backup(plan, key, Reporter())
    assert result.ok, result.errors
    return plan


def test_versions_are_listed_newest_first(tmp_path, source):
    destination = tmp_path / "kopia"
    first = _backup(source, destination)
    time.sleep(0.05)
    (source / "Zestawienie.CSV").write_text("zmienione", encoding="utf-8")
    second = _backup(source, destination)
    names = [v.name for v in browse.versions(destination)]
    assert names[:2] == [second.version, first.version]
    assert all(v.complete for v in browse.versions(destination))


def test_folder_listing_hides_program_files_and_storage_suffixes(tmp_path, source):
    destination = tmp_path / "kopia"
    plan = _backup(source, destination)
    top = browse.list_folder(destination, plan.version)
    assert [i.name for i in top] == ["Dokumenty"]
    inside = browse.list_folder(destination, plan.version, "Dokumenty")
    assert [i.name for i in inside] == ["Umowy", "obraz.vhdx", "Zestawienie.CSV"]
    big = next(i for i in inside if i.name == "obraz.vhdx")
    assert big.kind == browse.CHUNKED and big.size == 2 * 1024 * 1024
    names_everywhere = {i.name for i in browse.list_folder(destination, "")}
    assert not names_everywhere & ({".cleanvault-manifest", chunks.CHUNK_DIR} | set(rescue.RESCUE_FILES))


def test_encrypted_listing_knows_sizes_without_the_password(tmp_path, source):
    destination = tmp_path / "kopia"
    plan = _backup(source, destination, key=keyring())
    inside = browse.list_folder(destination, plan.version, "Dokumenty")
    small = next(i for i in inside if i.name == "Zestawienie.CSV")
    assert small.kind == browse.ENCRYPTED and small.size == (source / "Zestawienie.CSV").stat().st_size
    big = next(i for i in inside if i.name == "obraz.vhdx")
    assert big.kind == browse.CHUNKED_ENCRYPTED and big.size is None


@pytest.mark.parametrize("encrypted", [False, True])
def test_single_file_extraction(tmp_path, source, encrypted):
    destination = tmp_path / "kopia"
    key = keyring() if encrypted else None
    plan = _backup(source, destination, key=key)
    items = {i.name: i for i in browse.list_folder(destination, plan.version, "Dokumenty")}
    for name in ("Zestawienie.CSV", "obraz.vhdx"):
        target = browse.extract(destination, items[name], tmp_path / "podglad" / name, key)
        assert target.read_bytes() == (source / name).read_bytes()
    if encrypted:
        with pytest.raises(crypto.CryptoError):
            browse.extract(destination, items["Zestawienie.CSV"], tmp_path / "x", None)


def test_history_shows_where_a_file_changed(tmp_path, source):
    destination = tmp_path / "kopia"
    first = _backup(source, destination)
    time.sleep(0.05)
    second = _backup(source, destination)  # bez zmian
    time.sleep(0.05)
    (source / "Zestawienie.CSV").write_text("nowe liczby", encoding="utf-8")
    third = _backup(source, destination)

    rows = browse.history(destination, "Dokumenty/Zestawienie.CSV")
    assert [r.version.name for r in rows] == [third.version, second.version, first.version]
    assert [r.changed for r in rows] == [True, False, True], "druga wersja to ten sam plik co pierwsza"


def test_search_finds_paths_case_insensitively(tmp_path, source):
    destination = tmp_path / "kopia"
    _backup(source, destination)
    assert [row[0] for row in browse.search(destination, "najem")] == ["Dokumenty/Umowy/2026/Najem.txt"]
    assert len(browse.search(destination, "dokumenty")) == 3
    assert browse.search(destination, "   ") == []
    assert len(browse.search(destination, "dokumenty", limit=2)) == 2


def test_locate_returns_the_newest_copy(tmp_path, source):
    destination = tmp_path / "kopia"
    _backup(source, destination)
    time.sleep(0.05)
    second = _backup(source, destination)
    version, item = browse.locate(destination, "Dokumenty/Umowy/2026/Najem.txt")
    assert version.name == second.version and item.size == len(b"umowa najmu")


def test_user_file_ending_in_cvlt_is_not_mistaken_for_a_container(tmp_path):
    destination = tmp_path / "kopia"
    folder = destination / "2026-09-27_@500" / "Dane"
    folder.mkdir(parents=True)
    (folder / "notatki.cvlt").write_text("zwykły tekst", encoding="utf-8")
    item = browse.list_folder(destination, "2026-09-27_@500", "Dane")[0]
    assert item.name == "notatki.cvlt" and item.kind == browse.PLAIN
    assert os.path.getsize(item.stored) == item.size
