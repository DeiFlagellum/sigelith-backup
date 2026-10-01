"""Testy nazw katalogów wersji: znacznik BeatTime i data uzupełnienia.

Nazwa wersji jest prefiksem ścieżki każdego wpisu spisu treści, więc zmiana
nazwy katalogu jest najwrażliwszą operacją w programie. Największą wagę mają
tu testy awarii: po zabiciu programu w trakcie zmiany nazwy spis treści musi
wskazywać na katalog, który **faktycznie** leży na dysku.
"""

from __future__ import annotations

import os

import pytest

from cleanvault import beat, engine
from cleanvault.engine import BackupConfig, Reporter
from cleanvault.snapshot import Manifest, ManifestJournal


def make_source(tmp_path, count=6):
    source = tmp_path / "Dane"
    source.mkdir()
    for i in range(count):
        (source / f"plik{i:02d}.bin").write_bytes(bytes([i]) * 256)
    return source


def config_for(source, dest, **kwargs) -> BackupConfig:
    params = dict(
        sources=[str(source)], destination=str(dest), structure="dated",
        verify_after_write=False, excludes=[], catchup_passes=0, workers=1,
    )
    params.update(kwargs)
    return BackupConfig(**params)


def run(config):
    plan = engine.plan_backup(config, Reporter())
    return plan, engine.run_backup(plan, None, Reporter())


@pytest.fixture()
def stamps(monkeypatch):
    """Kolejne znaczniki BeatTime, żeby nazwy były przewidywalne."""
    prepared = iter(["2026-09-17_@687", "2026-09-24_@921", "2026-09-25_@015", "2026-09-26_@100"])
    monkeypatch.setattr(engine.beat, "stamp", lambda *a: next(prepared))
    return prepared


# --------------------------------------------------------------- nazwa wersji


def test_new_version_is_named_with_beat_stamp(tmp_path, monkeypatch):
    monkeypatch.setattr(engine.beat, "stamp", lambda *a: "2026-09-26_@100")
    plan, result = run(config_for(make_source(tmp_path), tmp_path / "cel"))
    assert plan.version == "2026-09-26_@100"
    assert result.ok and (tmp_path / "cel" / "2026-09-26_@100").is_dir()


def test_update_stamp_is_appended_then_replaced(tmp_path, stamps):
    source = make_source(tmp_path)
    dest = tmp_path / "cel"
    first, _ = run(config_for(source, dest))
    assert first.version == "2026-09-17_@687"

    (source / "plik00.bin").write_bytes(b"zmiana pierwsza")
    plan, result = run(config_for(source, dest, target_version=first.version))
    assert result.ok
    assert plan.version == "2026-09-17_@687--2026-09-24_@921"
    assert (dest / "2026-09-17_@687--2026-09-24_@921").is_dir()
    assert not (dest / "2026-09-17_@687").exists()

    (source / "plik01.bin").write_bytes(b"zmiana druga")
    plan, result = run(config_for(source, dest, target_version=plan.version))
    assert result.ok
    assert plan.version == "2026-09-17_@687--2026-09-25_@015", "data uzupełnienia ma być podmieniona, nie doklejona"
    assert plan.version.count("--") == 1


def test_manifest_follows_the_rename_and_nothing_is_copied_again(tmp_path, stamps):
    source = make_source(tmp_path)
    dest = tmp_path / "cel"
    first, _ = run(config_for(source, dest))
    plan, _ = run(config_for(source, dest, target_version=first.version))

    manifest = Manifest.load(dest)
    assert len(manifest.entries) == 6
    for entry in manifest.entries.values():
        assert entry.stored.startswith(plan.version + "/")
        assert (dest / entry.stored).exists()
    assert plan.version in manifest.runs and first.version not in manifest.runs
    assert manifest.versions == [plan.version]

    # Kolejne wznowienie rozpoznaje wszystko na nośniku i nie kopiuje nic.
    again = engine.plan_backup(config_for(source, dest, target_version=plan.version), Reporter())
    assert len(again.adopted) == 6 and again.to_copy == []


def test_old_clock_named_version_gets_the_update_stamp(tmp_path, monkeypatch):
    """Katalogi z poprzedniego formatu leżą już na dyskach — muszą działać dalej."""
    source = make_source(tmp_path)
    dest = tmp_path / "cel"
    monkeypatch.setattr(engine.beat, "stamp", lambda *a: "2026-09-17_16-30-11")
    first, _ = run(config_for(source, dest))
    assert first.version == "2026-09-17_16-30-11"

    monkeypatch.setattr(engine.beat, "stamp", lambda *a: "2026-09-26_@100")
    plan, result = run(config_for(source, dest, target_version=first.version))
    assert result.ok
    assert plan.version == "2026-09-17_16-30-11--2026-09-26_@100"
    info = engine.inspect_destination(dest)
    assert [run_state.name for run_state in info.runs] == [plan.version]
    assert engine.describe_version(info.runs[0]).startswith("17.09.2026 16:30, uzupełniona 26.09.2026 @100")


def test_stamping_can_be_switched_off(tmp_path, stamps):
    source = make_source(tmp_path)
    dest = tmp_path / "cel"
    first, _ = run(config_for(source, dest))
    plan, _ = run(config_for(source, dest, target_version=first.version, stamp_updates=False))
    assert plan.version == first.version
    assert (dest / first.version).is_dir()


def test_versions_stay_sorted_newest_first(tmp_path, stamps):
    source = make_source(tmp_path)
    dest = tmp_path / "cel"
    first, _ = run(config_for(source, dest))
    (source / "plik00.bin").write_bytes(b"zmiana")
    run(config_for(source, dest, target_version=first.version))
    (source / "nowy.bin").write_bytes(b"nowa wersja")
    second, _ = run(config_for(source, dest))

    names = [state.name for state in engine.inspect_destination(dest).runs]
    assert names == sorted(names, reverse=True)
    assert names[0] == second.version, "najnowsza wersja ma być pierwsza na liście"


# ------------------------------------------------------- awaria w trakcie zmiany


def test_crash_after_rename_is_recovered_from_journal(tmp_path, stamps):
    """Program zginął po zmianie nazwy katalogu, a przed zapisem spisu treści."""
    source = make_source(tmp_path)
    dest = tmp_path / "cel"
    first, _ = run(config_for(source, dest))
    old, new = first.version, first.version + "--2026-09-24_@921"

    # Dokładnie to, co robi silnik: zamiar do dziennika, potem zmiana nazwy.
    ManifestJournal(dest).append([{"t": "rename", "from": old, "to": new}])
    os.rename(dest / old, dest / new)

    manifest = Manifest.load(dest)
    assert manifest.versions == [new] and new in manifest.runs
    for entry in manifest.entries.values():
        assert entry.stored.startswith(new + "/")
        assert (dest / entry.stored).exists(), "spis treści wskazuje na nieistniejący plik"


def test_crash_before_rename_leaves_manifest_alone(tmp_path, stamps):
    """Program zginął po zapisie zamiaru, a przed zmianą nazwy katalogu."""
    source = make_source(tmp_path)
    dest = tmp_path / "cel"
    first, _ = run(config_for(source, dest))
    old, new = first.version, first.version + "--2026-09-24_@921"

    ManifestJournal(dest).append([{"t": "rename", "from": old, "to": new}])  # i nic więcej

    manifest = Manifest.load(dest)
    assert manifest.versions == [old], "przepisano wpisy na katalog, którego nie ma"
    for entry in manifest.entries.values():
        assert (dest / entry.stored).exists()

    # Kopia po takiej awarii dalej rozpoznaje wszystko na nośniku.
    plan = engine.plan_backup(config_for(source, dest, target_version=old, stamp_updates=False), Reporter())
    assert len(plan.adopted) == 6 and plan.to_copy == []


def test_locked_directory_does_not_break_the_backup(tmp_path, stamps, monkeypatch):
    """Katalog otwarty w Eksploratorze: zmiana nazwy się nie uda i to nie jest błąd kopii."""
    source = make_source(tmp_path)
    dest = tmp_path / "cel"
    first, _ = run(config_for(source, dest))

    def refuse(*_args, **_kwargs):
        raise PermissionError("katalog jest w użyciu")

    monkeypatch.setattr(engine.os, "rename", refuse)
    (source / "plik00.bin").write_bytes(b"zmiana")
    plan, result = run(config_for(source, dest, target_version=first.version))

    assert result.ok and plan.version == first.version
    manifest = Manifest.load(dest)
    assert manifest.versions == [first.version]
    for entry in manifest.entries.values():
        assert (dest / entry.stored).exists()


def test_stamp_is_not_applied_twice_by_catchup(tmp_path, stamps):
    """Przebieg uzupełniający pisze już do katalogu pod nową nazwą."""
    source = make_source(tmp_path)
    dest = tmp_path / "cel"
    first, _ = run(config_for(source, dest))
    (source / "plik00.bin").write_bytes(b"zmiana")
    plan, result = run(config_for(source, dest, target_version=first.version, catchup_passes=1))

    assert result.ok
    assert plan.version.count("--") == 1
    assert [p.name for p in dest.iterdir() if p.is_dir()] == [plan.version]


def test_beat_stamp_used_by_engine_matches_beat_module():
    assert engine.beat is beat
    assert engine.VERSION_UPDATE_SEPARATOR == "--"


def test_update_in_the_same_beat_does_not_duplicate_the_stamp(tmp_path, monkeypatch):
    """Uzupełnienie w tym samym beacie co utworzenie nie dopisuje niczego."""
    monkeypatch.setattr(engine.beat, "stamp", lambda *a: "2026-09-26_@768")
    source = make_source(tmp_path)
    dest = tmp_path / "cel"
    first, _ = run(config_for(source, dest))
    plan, result = run(config_for(source, dest, target_version=first.version))

    assert result.ok
    assert plan.version == "2026-09-26_@768", "nazwa nie może brzmieć …@768--…@768"
    assert [p.name for p in dest.iterdir() if p.is_dir()] == ["2026-09-26_@768"]


def test_rebuilt_file_with_same_content_does_not_look_like_missing(tmp_path, stamps):
    """Plik o tej samej treści, a nowym czasie modyfikacji, jest „zrobiony”.

    Tak wyglądają przebudowane artefakty (``build/``): treść identyczna, czas
    inny. Program liczy im sumę kontrolną, nie kopiuje ich ponownie — i nie może
    potem twierdzić, że w kopii ich brakuje.
    """
    source = make_source(tmp_path)
    dest = tmp_path / "cel"
    first, _ = run(config_for(source, dest))

    rebuilt = source / "plik00.bin"
    later = rebuilt.stat().st_mtime + 86_400
    os.utime(rebuilt, (later, later))  # ta sama treść, nowy czas

    plan, result = run(config_for(source, dest, target_version=first.version))
    assert result.ok
    state = Manifest.load(dest).runs[plan.version]
    assert state.complete
    assert state.missing_files == 0, "program twierdzi, że brakuje plików, choć wszystkie są"
