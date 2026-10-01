"""Testy skanowania drzewa i wykluczeń."""

from __future__ import annotations

import os

import pytest

from cleanvault.snapshot import (
    FileMeta,
    Manifest,
    ManifestEntry,
    SourceRoot,
    is_excluded,
    scan_sources,
)


def test_source_root_label_from_directory_name(tmp_path):
    folder = tmp_path / "Moje Zdjęcia"
    folder.mkdir()
    root = SourceRoot.make(folder)
    assert root.label == "Moje Zdjęcia"


def test_source_root_label_sanitises_forbidden_characters(tmp_path):
    SourceRoot(path=tmp_path, label="a")
    assert SourceRoot.make(tmp_path).label  # nie pusty
    from cleanvault.snapshot import _sanitise

    assert _sanitise('zły:znak?') == "zły_znak_"
    assert _sanitise("...") == "zrodlo"


def test_scan_uses_relative_keys(tmp_path):
    """Klucze muszą być względne wobec źródła — to sedno poprawki A1."""
    src = tmp_path / "dane"
    (src / "pod").mkdir(parents=True)
    (src / "plik.txt").write_text("x", encoding="utf-8")
    (src / "pod" / "glebiej.txt").write_text("y", encoding="utf-8")

    result = scan_sources([SourceRoot.make(src)], [])

    assert set(result) == {"dane/plik.txt", "dane/pod/glebiej.txt"}
    assert all(not os.path.isabs(k) for k in result)


def test_scan_skips_missing_source(tmp_path):
    assert scan_sources([SourceRoot.make(tmp_path)], []) == {}


def test_scan_ignores_directories_matching_exclude(tmp_path):
    src = tmp_path / "projekt"
    (src / ".git").mkdir(parents=True)
    (src / ".git" / "HEAD").write_text("ref", encoding="utf-8")
    (src / "kod.py").write_text("print()", encoding="utf-8")

    result = scan_sources([SourceRoot.make(src)], [".git/*"])
    assert set(result) == {"projekt/kod.py"}


@pytest.mark.parametrize(
    ("rel", "name", "pattern", "expected"),
    [
        ("a/Thumbs.db", "Thumbs.db", "Thumbs.db", True),
        ("a/notatka.tmp", "notatka.tmp", "*.tmp", True),
        ("a/notatka.txt", "notatka.txt", "*.tmp", False),
        ("node_modules/x/y.js", "y.js", "node_modules/*", True),
        ("node_modules", "node_modules", "node_modules/*", True),
        ("src/kod.py", "kod.py", "node_modules/*", False),
        ("a/THUMBS.DB", "THUMBS.DB", "thumbs.db", True),
    ],
)
def test_exclude_matching(rel, name, pattern, expected):
    assert is_excluded(rel, name, [pattern]) is expected


def test_file_meta_tolerates_fat_timestamp_granularity():
    """FAT/exFAT zapisuje czas z dokładnością do 2 s — bez tolerancji każdy
    backup na pendrive wykrywałby zmiany, których nie ma."""
    a = FileMeta(size=100, mtime=1_700_000_000.0)
    b = FileMeta(size=100, mtime=1_700_000_001.0)
    c = FileMeta(size=100, mtime=1_700_000_010.0)
    d = FileMeta(size=200, mtime=1_700_000_000.0)

    assert a.same_stat_as(b)
    assert not a.same_stat_as(c)
    assert not a.same_stat_as(d)
    assert not a.same_stat_as(None)


def test_manifest_roundtrip(tmp_path):
    manifest = Manifest.load(tmp_path)
    manifest.encrypted = True
    manifest.roots = {"dane": "D:/Dane"}
    manifest.entries["dane/a.txt"] = ManifestEntry(
        size=10, mtime=1.0, sha256="abc", stored="dane/a.txt.cvlt", stored_size=83
    )
    manifest.save()

    reloaded = Manifest.load(tmp_path)
    assert reloaded.encrypted is True
    assert reloaded.roots == {"dane": "D:/Dane"}
    assert reloaded.entries["dane/a.txt"].sha256 == "abc"
    assert reloaded.entries["dane/a.txt"].stored_size == 83


def test_manifest_detects_corruption(tmp_path):
    manifest = Manifest.load(tmp_path)
    manifest.entries["a"] = ManifestEntry(1, 1.0, "x", "a")
    manifest.save()

    blob = bytearray(manifest.path.read_bytes())
    blob[-1] ^= 0xFF
    tmp = tmp_path / "x.tmp"
    tmp.write_bytes(bytes(blob))
    os.replace(tmp, manifest.path)

    assert Manifest.load(tmp_path).entries == {}, "uszkodzony manifest musi dać pustą listę, nie wyjątek"


def test_manifest_missing_file_is_not_an_error(tmp_path):
    assert Manifest.load(tmp_path / "nie_ma").entries == {}
