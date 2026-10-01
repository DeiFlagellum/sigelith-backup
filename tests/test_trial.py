"""Próbne przywrócenie — losowa próbka przez prawdziwą ścieżkę przywracania."""

from __future__ import annotations

import os
import tempfile

import pytest

from cleanvault import crypto, engine
from cleanvault.crypto import KdfParams, PasswordKeyring
from cleanvault.engine import BackupConfig, EngineError, Reporter


@pytest.fixture()
def source(tmp_path):
    root = tmp_path / "Projekty"
    (root / "a").mkdir(parents=True)
    for index in range(6):
        (root / "a" / f"plik{index}.txt").write_text(f"treść {index} " * 50, encoding="utf-8")
    (root / "duzy.bin").write_bytes(os.urandom(256 * 1024))
    return root


def _backup(source, destination, encrypt=False, keyring=None):
    config = BackupConfig(
        sources=[str(source)],
        destination=str(destination),
        structure="dated",
        encrypt=encrypt,
        excludes=[],
        stamp_updates=False,
        catchup_passes=0,
    )
    reporter = Reporter()
    plan = engine.plan_backup(config, reporter)
    result = engine.run_backup(plan, keyring, reporter)
    assert result.ok
    return plan


def test_trial_restore_compares_with_the_source(tmp_path, source):
    destination = tmp_path / "kopia"
    _backup(source, destination)
    result = engine.trial_restore(destination, None, Reporter(), seed=1)
    assert result.ok, result.errors
    assert result.files_done == 7
    assert "Porównano ze źródłem: 7" in result.notes[0]


def test_trial_restore_finds_a_damaged_copy(tmp_path, source):
    destination = tmp_path / "kopia"
    plan = _backup(source, destination)
    damaged = destination / plan.version / source.name / "a" / "plik3.txt"
    damaged.write_text("to nie jest ta treść", encoding="utf-8")
    os.utime(damaged, (1, 1))

    result = engine.trial_restore(destination, None, Reporter(), seed=1)
    assert not result.ok
    assert any("plik3.txt" in error for error in result.errors)


def test_changed_source_falls_back_to_the_checksum(tmp_path, source):
    destination = tmp_path / "kopia"
    _backup(source, destination)
    (source / "a" / "plik0.txt").write_text("zmieniony po kopii", encoding="utf-8")

    result = engine.trial_restore(destination, None, Reporter(), seed=1)
    assert result.ok, result.errors  # kopia jest dobra — zmieniło się tylko źródło
    assert "tylko z sumą kontrolną (źródło zmieniło się albo jest niedostępne): 1" in result.notes[0]


def test_encrypted_backup_needs_the_password(tmp_path, source):
    keyring = PasswordKeyring("Hasło-próby-1", KdfParams(crypto.KDF_PBKDF2_SHA256, b"s" * 16, 1000))
    destination = tmp_path / "kopia"
    _backup(source, destination, encrypt=True, keyring=keyring)

    with pytest.raises(EngineError):
        engine.trial_restore(destination, None, Reporter())
    result = engine.trial_restore(destination, keyring, Reporter(), seed=2)
    assert result.ok, result.errors
    assert result.files_done == 7


def test_scratch_folder_is_removed(tmp_path, source, monkeypatch):
    destination = tmp_path / "kopia"
    _backup(source, destination)
    scratch = tmp_path / "proba"
    monkeypatch.setattr(tempfile, "mkdtemp", lambda prefix="": (scratch.mkdir(), str(scratch))[1])

    engine.trial_restore(destination, None, Reporter(), seed=3)
    assert not scratch.exists()


def test_sample_respects_the_byte_budget(tmp_path, source):
    destination = tmp_path / "kopia"
    _backup(source, destination)
    result = engine.trial_restore(destination, None, Reporter(), byte_budget=100 * 1024, seed=4)
    assert result.ok
    assert result.bytes_done <= 100 * 1024
    assert result.files_done == 6  # duży plik nie mieści się w limicie


def test_sample_size_is_respected(tmp_path, source):
    destination = tmp_path / "kopia"
    _backup(source, destination)
    result = engine.trial_restore(destination, None, Reporter(), sample=3, seed=5)
    assert result.files_done == 3


def test_empty_backup_folder_is_refused(tmp_path):
    (tmp_path / "pusto").mkdir()
    with pytest.raises(EngineError):
        engine.trial_restore(tmp_path / "pusto", None, Reporter())
