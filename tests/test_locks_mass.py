"""Pliki zablokowane przez inne programy i wykrywanie masowych zmian (ransomware)."""

from __future__ import annotations

import ctypes
import os

import pytest

from cleanvault import engine, locks
from cleanvault.engine import BackupConfig, MassChangeDetected, Reporter


@pytest.fixture(autouse=True)
def no_retry_pause(monkeypatch):
    monkeypatch.setattr(engine, "LOCK_RETRY_DELAY", 0.0)


def _config(source, destination, **kwargs):
    params = dict(
        sources=[str(source)],
        destination=str(destination),
        structure="dated",
        excludes=[],
        stamp_updates=False,
        catchup_passes=0,
        workers=1,
    )
    params.update(kwargs)
    return BackupConfig(**params)


def _run(config):
    reporter = Reporter()
    plan = engine.plan_backup(config, reporter)
    return plan, engine.run_backup(plan, None, reporter)


def _sharing_violation():
    return OSError(None, "Proces nie może uzyskać dostępu do pliku", None, 32)


# ------------------------------------------------------------ pliki zablokowane


@pytest.mark.skipif(os.name != "nt", reason="blokady plików Windows")
def test_really_locked_file_is_reported_with_the_program(tmp_path):
    source = tmp_path / "Poczta"
    source.mkdir()
    (source / "list.txt").write_text("zwykły plik", encoding="utf-8")
    archive = source / "archiwum.pst"
    archive.write_bytes(b"x" * 4096)

    from ctypes import wintypes

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateFileW.restype = wintypes.HANDLE
    handle = kernel32.CreateFileW(str(archive), 0x80000000, 0, None, 3, 0x80, None)  # bez współdzielenia
    try:
        plan, result = _run(_config(source, tmp_path / "kopia"))
    finally:
        kernel32.CloseHandle(handle)

    assert result.ok, result.errors  # zablokowany plik to nie błąd kopii
    key = f"{source.name}/archiwum.pst"
    assert list(result.locked) == [key]
    assert result.locked[key], "nie ustalono programu, który trzyma plik"
    assert "Pominięto 1 plik otwarty w innym programie." in result.summary
    assert any("archiwum.pst" in note for note in result.notes)
    run = result.versions[plan.version]
    assert run.complete and run.locked_files == 1


def test_file_released_before_retry_is_backed_up(tmp_path, monkeypatch):
    source = tmp_path / "dane"
    source.mkdir()
    (source / "a.txt").write_text("a", encoding="utf-8")
    (source / "b.txt").write_text("b", encoding="utf-8")
    real = engine._store_one
    attempts = {"n": 0}

    def locked_once(item, ctx):
        if item.key.endswith("b.txt") and attempts["n"] == 0:
            attempts["n"] += 1
            raise _sharing_violation()
        return real(item, ctx)

    monkeypatch.setattr(engine, "_store_one", locked_once)
    _plan, result = _run(_config(source, tmp_path / "kopia"))
    assert result.ok and not result.locked
    assert result.files_done == 2


def test_locked_file_goes_in_on_the_next_run(tmp_path, monkeypatch):
    source = tmp_path / "dane"
    source.mkdir()
    (source / "baza.db").write_bytes(b"dane" * 100)
    real = engine._store_one

    def always_locked(item, ctx):
        raise _sharing_violation()

    monkeypatch.setattr(engine, "_store_one", always_locked)
    monkeypatch.setattr(locks, "who_locks", lambda path: ["Baza danych"])
    _plan, first = _run(_config(source, tmp_path / "kopia"))
    assert list(first.locked.values()) == [["Baza danych"]]
    assert "Baza danych (baza.db)" in " ".join(first.notes)

    monkeypatch.setattr(engine, "_store_one", real)
    plan, second = _run(_config(source, tmp_path / "kopia"))
    assert [item.key for item in plan.to_copy] == [f"{source.name}/baza.db"]
    assert second.ok and not second.locked


def test_permission_problem_is_not_mistaken_for_a_lock(tmp_path):
    missing = tmp_path / "nie-ma.txt"
    assert not locks.is_lock_error(PermissionError(13, "Odmowa dostępu"), missing)
    assert locks.is_lock_error(_sharing_violation())
    assert not locks.is_lock_error(ValueError("coś innego"))


def test_describe_lists_programs_and_the_rest():
    text = locks.describe({f"x/plik{i}.pst": ["Outlook"] for i in range(7)}, limit=3)
    assert text.startswith("Outlook (plik0.pst)")
    assert text.endswith("… +4")


# ------------------------------------------------------------- masowe zmiany


@pytest.fixture()
def big_source(tmp_path):
    source = tmp_path / "Dokumenty"
    source.mkdir()
    for index in range(300):
        (source / f"notatka{index:03}.txt").write_text(
            f"Notatka numer {index}. " * 60, encoding="utf-8"
        )
    return source


def _backup_then(tmp_path, source, change):
    destination = tmp_path / "kopia"
    _run(_config(source, destination))
    change(source)
    return engine.plan_backup(_config(source, destination), Reporter())


def test_encrypted_looking_files_stop_the_backup(tmp_path, big_source):
    def encrypt(source):
        for path in sorted(source.glob("*.txt"))[:150]:
            path.write_bytes(os.urandom(path.stat().st_size + 7))

    plan = _backup_then(tmp_path, big_source, encrypt)
    assert plan.suspicion, "150 z 300 plików tekstowych zamienionych w szum musi wzbudzić alarm"
    with pytest.raises(MassChangeDetected) as caught:
        engine.run_backup(plan, None, Reporter())
    assert caught.value.reasons == plan.suspicion
    assert any("wygląda na zaszyfrowaną" in reason for reason in caught.value.reasons)
    assert not (tmp_path / "kopia" / plan.version).exists(), "nic nie może trafić do kopii przed decyzją"


def test_confirmed_mass_change_runs(tmp_path, big_source):
    def encrypt(source):
        for path in sorted(source.glob("*.txt"))[:150]:
            path.write_bytes(os.urandom(4096))

    destination = tmp_path / "kopia"
    _run(_config(big_source, destination))
    encrypt(big_source)
    config = _config(big_source, destination, allow_mass_change=True)
    plan = engine.plan_backup(config, Reporter())
    assert plan.suspicion
    result = engine.run_backup(plan, None, Reporter())
    assert result.ok


def test_ordinary_mass_edit_is_not_an_alarm(tmp_path, big_source):
    """Przełączenie gałęzi, masowa zmiana formatowania — dużo zmian, ale treść wciąż tekstowa."""

    def rewrite(source):
        for path in sorted(source.glob("*.txt"))[:200]:
            path.write_text(path.read_text(encoding="utf-8").upper(), encoding="utf-8")

    plan = _backup_then(tmp_path, big_source, rewrite)
    assert plan.suspicion == []


def test_renamed_with_extra_extension_is_an_alarm(tmp_path, big_source):
    def rename(source):
        for path in sorted(source.glob("*.txt"))[:80]:
            path.rename(path.with_name(path.name + ".locked"))
            (path.parent / (path.name + ".locked")).write_bytes(os.urandom(2048))

    plan = _backup_then(tmp_path, big_source, rename)
    assert any("końcówką" in reason for reason in plan.suspicion)


def test_document_without_its_signature_counts_as_encrypted(tmp_path):
    good = tmp_path / "raport.docx"
    good.write_bytes(b"PK\x03\x04" + b"\x00" * 200)
    bad = tmp_path / "zaszyfrowany.docx"
    bad.write_bytes(os.urandom(200))
    text = tmp_path / "zwykly.txt"
    text.write_text("zwykły tekst " * 50, encoding="utf-8")
    photo = tmp_path / "zdjecie.raw"
    photo.write_bytes(os.urandom(200))

    def planned(path):
        return engine.PlannedFile(key=path.name, source=path, meta=None, reason="zmieniony")

    assert engine._content_looks_encrypted(planned(good)) is False
    assert engine._content_looks_encrypted(planned(bad)) is True
    assert engine._content_looks_encrypted(planned(text)) is False
    assert engine._content_looks_encrypted(planned(photo)) is None  # nieznany typ — bez oceny


def test_entropy_separates_text_from_noise():
    assert engine._entropy(("zwykły polski tekst " * 100).encode("utf-8")) < 5.5
    assert engine._entropy(os.urandom(64 * 1024)) > 7.9


def test_small_folders_never_trigger_the_scale_rule(tmp_path):
    source = tmp_path / "male"
    source.mkdir()
    for index in range(50):
        (source / f"{index}.txt").write_text("tekst", encoding="utf-8")
    plan = _backup_then(tmp_path, source, lambda s: [p.write_text("inny", encoding="utf-8") for p in s.glob("*.txt")])
    assert plan.suspicion == []
