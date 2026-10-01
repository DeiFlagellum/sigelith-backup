"""Testy rozpoznawania plików przeniesionych i przemianowanych w źródle.

Przeniesienie katalogu wyglądało dla programu jak skasowanie jednych plików
i pojawienie się drugich, więc kosztowało tyle, co kopiowanie od nowa. Teraz
taki plik trafia do kopii samym dowiązaniem — pod warunkiem, że **suma
kontrolna** potwierdzi, że to naprawdę ten sam plik.
"""

from __future__ import annotations

import os

import pytest

from cleanvault import engine
from cleanvault.engine import BackupConfig, Reporter
from cleanvault.paths import supports_hardlinks
from cleanvault.snapshot import Manifest


def make_source(tmp_path):
    source = tmp_path / "Dane"
    (source / "stary").mkdir(parents=True)
    (source / "stary" / "duzy.bin").write_bytes(os.urandom(2 * 1024 * 1024))
    (source / "stary" / "maly.txt").write_text("treść", encoding="utf-8")
    (source / "inny.bin").write_bytes(os.urandom(4096))
    return source


def config_for(source, dest, **kwargs) -> BackupConfig:
    params = dict(
        sources=[str(source)], destination=str(dest), structure="dated",
        verify_after_write=False, excludes=[], catchup_passes=0, workers=1,
        stamp_updates=False,
    )
    params.update(kwargs)
    return BackupConfig(**params)


def run(config):
    plan = engine.plan_backup(config, Reporter())
    return plan, engine.run_backup(plan, None, Reporter())


def test_moved_file_is_linked_instead_of_copied(tmp_path):
    source = make_source(tmp_path)
    dest = tmp_path / "cel"
    run(config_for(source, dest))
    original = (source / "stary" / "duzy.bin").read_bytes()

    (source / "nowy").mkdir()
    (source / "stary" / "duzy.bin").rename(source / "nowy" / "duzy.bin")

    plan, result = run(config_for(source, dest))
    assert plan.moved == 1
    assert result.files_done == 0, "przeniesiony plik został skopiowany od nowa"
    assert result.bytes_done == 0

    stored = dest / plan.version / "Dane" / "nowy" / "duzy.bin"
    assert stored.read_bytes() == original
    if supports_hardlinks(tmp_path):
        assert os.stat(stored).st_nlink >= 2, "powinno powstać dowiązanie, a nie kopia"

    manifest = Manifest.load(dest)
    assert manifest.entries["Dane/nowy/duzy.bin"].sha256
    assert (dest / manifest.entries["Dane/nowy/duzy.bin"].stored).exists()


def test_renamed_directory_moves_all_its_files(tmp_path):
    source = make_source(tmp_path)
    dest = tmp_path / "cel"
    run(config_for(source, dest))

    (source / "stary").rename(source / "przeniesiony")

    plan, result = run(config_for(source, dest))
    assert plan.moved == 2 and result.files_done == 0
    for name in ("duzy.bin", "maly.txt"):
        assert (dest / plan.version / "Dane" / "przeniesiony" / name).exists()


def test_same_size_and_time_but_different_content_is_not_confused(tmp_path):
    """Dwa pliki o identycznym rozmiarze i czasie — decyduje suma kontrolna."""
    source = tmp_path / "Dane"
    source.mkdir()
    first_content = b"A" * 4096
    second_content = b"B" * 4096
    (source / "pierwszy.bin").write_bytes(first_content)
    (source / "drugi.bin").write_bytes(second_content)
    moment = 1_700_000_000
    for name in ("pierwszy.bin", "drugi.bin"):
        os.utime(source / name, (moment, moment))
    dest = tmp_path / "cel"
    run(config_for(source, dest))

    # Oba znikają ze starych miejsc, więc oba są kandydatami dla nowego pliku.
    (source / "drugi.bin").unlink()
    (source / "pierwszy.bin").rename(source / "przeniesiony.bin")

    plan, _ = run(config_for(source, dest))
    assert plan.moved == 1
    stored = dest / plan.version / "Dane" / "przeniesiony.bin"
    assert stored.read_bytes() == first_content, "do kopii trafiła treść innego pliku"


def test_entry_without_checksum_is_copied_not_guessed(tmp_path):
    """Wpisy bez sumy kontrolnej (rozpoznane przy wznawianiu) nie są kandydatami."""
    source = make_source(tmp_path)
    dest = tmp_path / "cel"
    run(config_for(source, dest))

    manifest = Manifest.load(dest)
    entry = manifest.entries["Dane/stary/duzy.bin"]
    manifest.entries["Dane/stary/duzy.bin"] = type(entry)(
        entry.size, entry.mtime, "", entry.stored, entry.stored_size
    )
    manifest.save()

    (source / "nowy").mkdir()
    (source / "stary" / "duzy.bin").rename(source / "nowy" / "duzy.bin")

    plan, result = run(config_for(source, dest))
    assert plan.moved == 0
    assert result.files_done == 1, "bez sumy kontrolnej plik musi zostać skopiowany"


def test_moved_file_in_mirror_structure_lands_in_the_new_place(tmp_path):
    source = make_source(tmp_path)
    dest = tmp_path / "cel"
    run(config_for(source, dest, structure="mirror"))
    original = (source / "stary" / "duzy.bin").read_bytes()

    (source / "nowy").mkdir()
    (source / "stary" / "duzy.bin").rename(source / "nowy" / "duzy.bin")

    plan, result = run(config_for(source, dest, structure="mirror"))
    assert plan.moved == 1 and result.files_done == 0
    assert (dest / "Dane" / "nowy" / "duzy.bin").read_bytes() == original


def test_move_detection_works_while_resuming_a_version(tmp_path):
    source = make_source(tmp_path)
    dest = tmp_path / "cel"
    first, _ = run(config_for(source, dest))

    (source / "nowy").mkdir()
    (source / "stary" / "duzy.bin").rename(source / "nowy" / "duzy.bin")

    plan, result = run(config_for(source, dest, target_version=first.version))
    assert plan.moved == 1 and result.files_done == 0
    assert (dest / first.version / "Dane" / "nowy" / "duzy.bin").exists()
    assert (dest / first.version / "Dane" / "stary" / "duzy.bin").exists(), (
        "stara ścieżka zostaje w kopii — plik usunięty ze źródła nie znika z kopii"
    )


def test_copy_without_hardlinks_reads_from_the_backup_not_the_source(tmp_path, monkeypatch):
    """Bez twardych dowiązań plik jest powielany w obrębie kopii, a nie ciągnięty ze źródła."""
    monkeypatch.setattr(engine, "supports_hardlinks", lambda _p: False)
    source = make_source(tmp_path)
    dest = tmp_path / "cel"
    run(config_for(source, dest))
    original = (source / "stary" / "duzy.bin").read_bytes()

    (source / "nowy").mkdir()
    (source / "stary" / "duzy.bin").rename(source / "nowy" / "duzy.bin")

    duplicated: list[tuple[str, str]] = []
    real_duplicate = engine._duplicate_file

    def watch(src, dst, reporter):
        duplicated.append((str(src), str(dst)))
        return real_duplicate(src, dst, reporter)

    monkeypatch.setattr(engine, "_duplicate_file", watch)
    plan, result = run(config_for(source, dest))

    assert plan.moved == 1 and result.files_done == 0
    assert (dest / plan.version / "Dane" / "nowy" / "duzy.bin").read_bytes() == original
    sources_read = [src for src, _dst in duplicated if "duzy.bin" in src]
    assert sources_read, "plik nie został powielony w kopii"
    assert all(str(dest) in src for src in sources_read), "dane czytano ze źródła zamiast z kopii"


@pytest.mark.parametrize("size", [0, 1])
def test_tiny_files_are_handled_without_crashing(tmp_path, size):
    source = tmp_path / "Dane"
    source.mkdir()
    (source / "a.bin").write_bytes(b"x" * size)
    dest = tmp_path / "cel"
    run(config_for(source, dest))
    (source / "a.bin").rename(source / "b.bin")
    plan, result = run(config_for(source, dest))
    assert result.ok
    assert (dest / plan.version / "Dane" / "b.bin").exists()
