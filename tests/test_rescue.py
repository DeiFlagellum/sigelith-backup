"""Notatka ratunkowa i skrypt ``odzyskaj.py``.

Najważniejszy test w tym pliku uruchamia skrypt ratunkowy **jako osobny proces**
na kopii zaszyfrowanej przez silnik i porównuje wynik bajt w bajt ze źródłem.
To jedyny uczciwy dowód, że kopię da się odczytać bez tego programu.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from cleanvault import crypto, engine, rescue
from cleanvault.crypto import KdfParams, PasswordKeyring
from cleanvault.engine import BackupConfig, Reporter
from cleanvault.paths import resource_path
from cleanvault.snapshot import VersionState

SCRIPT = resource_path("assets", "recovery", rescue.SCRIPT_NAME)
PASSWORD = "Hasło-do-odzysku-1"


@pytest.fixture()
def source(tmp_path):
    root = tmp_path / "Dokumenty"
    (root / "pod").mkdir(parents=True)
    (root / "list.txt").write_text("Treść listu — zażółć gęślą jaźń", encoding="utf-8")
    (root / "pod" / "dane.bin").write_bytes(os.urandom(3 * 1024 * 1024 + 17))  # > porcja 1 MiB
    (root / "pusty.txt").write_bytes(b"")
    return root


def _backup(source: Path, destination: Path, encrypt: bool, keyring=None, **kwargs):
    config = BackupConfig(
        sources=[str(source)],
        destination=str(destination),
        structure="dated",
        encrypt=encrypt,
        excludes=[],
        stamp_updates=False,
        catchup_passes=0,
        **kwargs,
    )
    reporter = Reporter()
    plan = engine.plan_backup(config, reporter)
    return plan, engine.run_backup(plan, keyring, reporter)


def _files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _run_script(*args: str, password: str | None = None) -> subprocess.CompletedProcess:
    env = {**os.environ}
    env.pop("TVB_PASSWORD", None)
    if password is not None:
        env["TVB_PASSWORD"] = password
    # Czysty interpreter bez ścieżek projektu: skrypt nie może po cichu korzystać
    # z modułów programu, bo u użytkownika bez programu ich nie będzie.
    env.pop("PYTHONPATH", None)
    return subprocess.run(
        [sys.executable, "-I", str(SCRIPT), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        timeout=120,
        cwd=str(Path(args[0]).parent),
    )


def test_backup_leaves_note_and_script(tmp_path, source):
    destination = tmp_path / "kopia"
    plan, result = _backup(source, destination, encrypt=False)
    assert result.ok

    note = (destination / rescue.NOTE_NAME).read_text(encoding="utf-8-sig")
    assert plan.version in note
    assert "kompletna / complete" in note
    assert "NIE jest zaszyfrowana" in note and "NOT encrypted" in note
    assert (destination / rescue.SCRIPT_NAME).read_bytes() == SCRIPT.read_bytes()


def test_note_marks_an_interrupted_version(tmp_path, source, monkeypatch):
    destination = tmp_path / "kopia"
    real = engine._store_one
    calls = {"n": 0}

    def store_then_stop(item, ctx):
        calls["n"] += 1
        if calls["n"] > 1:
            raise crypto.OperationCancelled("stop")
        return real(item, ctx)

    monkeypatch.setattr(engine, "_store_one", store_then_stop)
    _plan, result = _backup(source, destination, encrypt=False, workers=1)
    assert result.cancelled

    note = (destination / rescue.NOTE_NAME).read_text(encoding="utf-8-sig")
    assert "NIEDOKOŃCZONA / INCOMPLETE" in note


def test_note_text_describes_mirror_and_unknown_state():
    versions = {
        "": VersionState(name="", complete=True, done_files=12),
        "2026-09-17_16-30-11": VersionState(name="2026-09-17_16-30-11", known=False),
    }
    text = rescue.note_text(versions, encrypted=True, now=0)
    assert "kopia lustrzana / mirror copy" in text
    assert "stan nieznany / state unknown" in text
    assert "pip install pycryptodomex argon2-cffi" in text


def test_script_recovers_encrypted_backup_without_the_program(tmp_path, source):
    destination = tmp_path / "kopia"
    keyring = PasswordKeyring(PASSWORD, KdfParams(crypto.KDF_PBKDF2_SHA256, b"s" * 16, 1000))
    plan, result = _backup(source, destination, encrypt=True, keyring=keyring)
    assert result.ok
    assert list((destination / plan.version).rglob("*.cvlt")), "kopia miała być zaszyfrowana"

    target = tmp_path / "odzyskane"
    done = _run_script(str(destination / plan.version), str(target), password=PASSWORD)
    assert done.returncode == 0, done.stdout + done.stderr

    recovered = _files(target / source.name)
    assert recovered == _files(source)


def test_script_recovers_argon2_encrypted_file(tmp_path, source):
    """Domyślny KDF programu to Argon2id — skrypt musi wyprowadzić ten sam klucz."""
    pytest.importorskip("argon2")
    destination = tmp_path / "kopia"
    keyring = PasswordKeyring(
        PASSWORD, KdfParams(crypto.KDF_ARGON2ID, b"a" * 16, 1, 8 * 1024, 1)
    )
    plan, result = _backup(source, destination, encrypt=True, keyring=keyring)
    assert result.ok
    single = next((destination / plan.version).rglob("list.txt.cvlt"))

    target = tmp_path / "jeden"
    done = _run_script(str(single), str(target), password=PASSWORD)
    assert done.returncode == 0, done.stdout + done.stderr
    assert (target / "list.txt").read_text(encoding="utf-8") == "Treść listu — zażółć gęślą jaźń"


def test_wrong_password_recovers_nothing(tmp_path, source):
    destination = tmp_path / "kopia"
    keyring = PasswordKeyring(PASSWORD, KdfParams(crypto.KDF_PBKDF2_SHA256, b"s" * 16, 1000))
    plan, _result = _backup(source, destination, encrypt=True, keyring=keyring)

    target = tmp_path / "odzyskane"
    done = _run_script(str(destination / plan.version), str(target), password="złe hasło")
    assert done.returncode == 1
    assert "złe hasło" in done.stdout or "wrong password" in done.stdout
    # żaden niezweryfikowany plik nie może udawać odzyskanego
    assert not [p for p in target.rglob("*") if p.is_file()]


def test_script_copies_unencrypted_files_and_skips_program_files(tmp_path, source):
    destination = tmp_path / "kopia"
    _backup(source, destination, encrypt=False)

    target = tmp_path / "odzyskane"
    done = _run_script(str(destination), str(target))
    assert done.returncode == 0, done.stdout + done.stderr
    names = {p.name for p in target.rglob("*") if p.is_file()}
    assert "list.txt" in names
    assert not names & set(rescue.RESCUE_FILES)
    assert not any(name.startswith(".cleanvault-") for name in names)


def test_restore_without_manifest_ignores_rescue_files(tmp_path, source):
    destination = tmp_path / "kopia"
    _backup(source, destination, encrypt=False)
    for leftover in destination.glob(".cleanvault-*"):
        leftover.unlink()  # kopia bez spisu treści, np. po ręcznym przeniesieniu

    restore = engine.plan_restore(str(destination), str(tmp_path / "cel"), reporter=Reporter())
    keys = {item.key for item in restore.items}
    assert not restore.from_manifest
    assert not keys & set(rescue.RESCUE_FILES)
    assert any(key.endswith("list.txt") for key in keys)


def test_failed_note_does_not_break_the_backup(tmp_path, source, monkeypatch):
    def refuse(*_args, **_kwargs):
        raise OSError("nośnik tylko do odczytu")

    monkeypatch.setattr(rescue, "_write_atomic", refuse)
    _plan, result = _backup(source, tmp_path / "kopia", encrypt=False)
    assert result.ok
