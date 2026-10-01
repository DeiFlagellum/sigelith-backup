"""Zapis różnicowy dużych plików: przepisy, magazyn fragmentów, sprzątanie, odzyskiwanie.

Progi są zmniejszone (plik „duży” od 1 MB, fragment ~64 KB), żeby testy trwały
sekundy — ale cała ścieżka jest ta sama co w programie: plan, zapis, dowiązania,
wznawianie, sprawdzanie, przywracanie i skrypt ratunkowy uruchamiany osobno.
"""

from __future__ import annotations

import os
import random
import subprocess
import sys
from pathlib import Path

import pytest

from cleanvault import chunks, crypto, engine, rescue
from cleanvault.crypto import KdfParams, PasswordKeyring
from cleanvault.engine import BackupConfig, Reporter
from cleanvault.paths import resource_path

pytestmark = pytest.mark.skipif(not chunks.AVAILABLE, reason="brak skompilowanego FastCDC")

PASSWORD = "Hasło-fragmentów-1"


@pytest.fixture(autouse=True)
def small_chunks(monkeypatch):
    monkeypatch.setattr(chunks, "DELTA_MIN_SIZE", 1024 * 1024)
    monkeypatch.setattr(chunks, "MIN_CHUNK", 16 * 1024)
    monkeypatch.setattr(chunks, "AVG_CHUNK", 64 * 1024)
    monkeypatch.setattr(chunks, "MAX_CHUNK", 256 * 1024)
    monkeypatch.setattr(chunks, "WINDOW", 1024 * 1024)


@pytest.fixture()
def source(tmp_path):
    root = tmp_path / "Maszyny"
    root.mkdir()
    rng = random.Random(3)
    (root / "dysk.vhdx").write_bytes(rng.randbytes(3 * 1024 * 1024))
    (root / "notatka.txt").write_text("mały plik", encoding="utf-8")
    return root


def keyring() -> PasswordKeyring:
    return PasswordKeyring(PASSWORD, KdfParams(crypto.KDF_PBKDF2_SHA256, b"s" * 16, 1000))


def _run(source, destination, key=None, **kwargs):
    params = dict(
        sources=[str(source)],
        destination=str(destination),
        structure="dated",
        encrypt=key is not None,
        excludes=[],
        stamp_updates=False,
        catchup_passes=0,
        verify_after_write=True,
    )
    params.update(kwargs)
    reporter = Reporter()
    plan = engine.plan_backup(BackupConfig(**params), reporter)
    return plan, engine.run_backup(plan, key, reporter)


def _chunk_files(destination: Path) -> set[str]:
    store = destination / chunks.CHUNK_DIR
    return {p.name for p in store.rglob("*") if p.is_file() and p.parent.parent.parent == store}


def _edit_middle(path: Path, data: bytes) -> None:
    content = bytearray(path.read_bytes())
    middle = len(content) // 2
    content[middle : middle + len(data)] = data
    path.write_bytes(bytes(content))


def test_large_file_goes_to_the_chunk_store(tmp_path, source):
    destination = tmp_path / "kopia"
    plan, result = _run(source, destination)
    assert result.ok, result.errors

    version = destination / plan.version / source.name
    assert (version / ("dysk.vhdx" + chunks.RECIPE_SUFFIX)).is_file()
    assert not (version / "dysk.vhdx").exists()
    assert (version / "notatka.txt").read_text(encoding="utf-8") == "mały plik"
    assert len(_chunk_files(destination)) > 10
    entry = engine.Manifest.load(destination).entries[f"{source.name}/dysk.vhdx"]
    assert entry.chunked and entry.size == 3 * 1024 * 1024


def test_changed_large_file_writes_only_new_chunks(tmp_path, source):
    destination = tmp_path / "kopia"
    _run(source, destination)
    before = _chunk_files(destination)

    _edit_middle(source / "dysk.vhdx", b"ZMIANA" * 10)
    _run(source, destination)
    new = _chunk_files(destination) - before
    assert 1 <= len(new) <= 3, f"zmiana 60 bajtów zapisała {len(new)} nowych fragmentów"


def test_insertion_in_the_middle_keeps_later_chunks(tmp_path, source):
    destination = tmp_path / "kopia"
    _run(source, destination)
    before = _chunk_files(destination)
    content = (source / "dysk.vhdx").read_bytes()
    (source / "dysk.vhdx").write_bytes(content[:1_500_000] + b"WSTAWKA" * 50 + content[1_500_000:])

    _run(source, destination)
    new = _chunk_files(destination) - before
    assert len(new) <= 3, "wstawka przesunęła dalszą treść, ale fragmenty mają zostać rozpoznane"


def test_unchanged_large_file_costs_nothing(tmp_path, source):
    destination = tmp_path / "kopia"
    _run(source, destination)
    before = _chunk_files(destination)
    second, result = _run(source, destination)
    assert result.ok
    assert _chunk_files(destination) == before
    recipe = Path(second.version) / source.name / ("dysk.vhdx" + chunks.RECIPE_SUFFIX)
    assert (destination / recipe).is_file()


def test_restore_and_verify_rebuild_the_file(tmp_path, source):
    destination = tmp_path / "kopia"
    _run(source, destination)
    assert engine.verify_backup(destination, None, Reporter()).ok

    plan = engine.plan_restore(str(destination), str(tmp_path / "cel"), reporter=Reporter())
    result = engine.run_restore(plan, None, Reporter())
    assert result.ok, result.errors
    restored = tmp_path / "cel" / source.name / "dysk.vhdx"
    assert restored.read_bytes() == (source / "dysk.vhdx").read_bytes()
    assert abs(restored.stat().st_mtime - (source / "dysk.vhdx").stat().st_mtime) < 2


def test_damaged_chunk_is_found_by_verification(tmp_path, source):
    destination = tmp_path / "kopia"
    _run(source, destination)
    victim = next((destination / chunks.CHUNK_DIR).rglob("*"))
    while victim.is_dir():
        victim = next(victim.iterdir())
    victim.write_bytes(b"uszkodzony fragment")

    report = engine.verify_backup(destination, None, Reporter())
    assert not report.ok
    assert any("dysk.vhdx" in error for error in report.errors)


def test_encrypted_chunks_hide_their_content(tmp_path, source):
    destination = tmp_path / "kopia"
    key = keyring()
    plan, result = _run(source, destination, key=key)
    assert result.ok, result.errors

    recipe = destination / plan.version / source.name / ("dysk.vhdx" + chunks.RECIPE_SUFFIX + ".cvlt")
    assert recipe.read_bytes()[:4] == crypto.MAGIC
    names = _chunk_files(destination)
    assert names and all(name.endswith(".cvlt") for name in names)
    plain_ids = {
        __import__("hashlib").sha256(c).hexdigest()
        for c in chunks.iter_chunks(open(source / "dysk.vhdx", "rb"))  # noqa: SIM115
    }
    assert not {name[:-5] for name in names} & plain_ids, "nazwy fragmentów zdradzają treść"

    plan_restore = engine.plan_restore(str(destination), str(tmp_path / "cel"), reporter=Reporter())
    assert engine.run_restore(plan_restore, key, Reporter()).ok
    assert (tmp_path / "cel" / source.name / "dysk.vhdx").read_bytes() == (source / "dysk.vhdx").read_bytes()


def test_other_password_is_refused_by_the_chunk_store(tmp_path, source):
    destination = tmp_path / "kopia"
    _run(source, destination, key=keyring())
    other = PasswordKeyring("zupełnie inne hasło", KdfParams(crypto.KDF_PBKDF2_SHA256, b"t" * 16, 1000))
    with pytest.raises(chunks.ChunkError):
        chunks.ChunkStore(destination, other)


def test_resume_reuses_chunks_written_before_the_stop(tmp_path, source, monkeypatch):
    destination = tmp_path / "kopia"
    real_put = chunks.ChunkStore.put
    writes = {"n": 0}

    def put_then_stop(self, cid, data):
        writes["n"] += 1
        if writes["n"] > 20:
            raise crypto.OperationCancelled("stop")
        return real_put(self, cid, data)

    monkeypatch.setattr(chunks.ChunkStore, "put", put_then_stop)
    plan, first = _run(source, destination, workers=1)
    assert first.cancelled
    kept = len(_chunk_files(destination))
    assert kept == 20

    written = []
    monkeypatch.setattr(
        chunks.ChunkStore, "put", lambda self, cid, data: written.append(real_put(self, cid, data)) or written[-1]
    )
    _plan, second = _run(source, destination, target_version=plan.version, workers=1)
    assert second.ok, second.errors
    assert sum(1 for size in written if size) == len(_chunk_files(destination)) - kept


def test_mirror_replaces_recipe_and_collects_old_chunks(tmp_path, source):
    destination = tmp_path / "kopia"
    _run(source, destination, structure="mirror")
    first = _chunk_files(destination)
    (source / "dysk.vhdx").write_bytes(random.Random(9).randbytes(3 * 1024 * 1024))  # zupełnie nowa treść
    _plan, result = _run(source, destination, structure="mirror")
    assert result.ok
    assert not (first & _chunk_files(destination)), "stare fragmenty kopii lustrzanej powinny zniknąć"
    assert engine.verify_backup(destination, None, Reporter()).ok


def test_file_crossing_the_threshold_leaves_no_stale_copy(tmp_path, source):
    destination = tmp_path / "kopia"
    small = source / "rosnie.bin"
    small.write_bytes(os.urandom(200 * 1024))
    _run(source, destination, structure="mirror")
    assert (destination / source.name / "rosnie.bin").is_file()

    small.write_bytes(os.urandom(2 * 1024 * 1024))
    _run(source, destination, structure="mirror")
    assert not (destination / source.name / "rosnie.bin").exists(), "stara postać pliku została obok przepisu"
    assert (destination / source.name / ("rosnie.bin" + chunks.RECIPE_SUFFIX)).is_file()


def test_retention_removes_only_unreferenced_chunks(tmp_path, source):
    destination = tmp_path / "kopia"
    rng = random.Random(11)
    shared = rng.randbytes(1024 * 1024)
    for index in range(3):
        (source / "dysk.vhdx").write_bytes(shared + rng.randbytes(2 * 1024 * 1024))
        _run(source, destination, retention=1)
        if index < 2:
            # kolejne wersje muszą mieć inną nazwę katalogu
            import time as _time

            _time.sleep(0.01)
    manifest = engine.Manifest.load(destination)
    assert len([v for v in manifest.versions if (destination / v).is_dir()]) == 1
    assert engine.verify_backup(destination, None, Reporter()).ok
    total = sum(p.stat().st_size for p in (destination / chunks.CHUNK_DIR).rglob("*") if p.is_file())
    assert total < 5 * 1024 * 1024, "fragmenty usuniętych wersji powinny zostać sprzątnięte"


def test_unreadable_recipe_stops_garbage_collection(tmp_path, source):
    destination = tmp_path / "kopia"
    plan, _ = _run(source, destination)
    before = _chunk_files(destination)
    recipe = destination / plan.version / source.name / ("dysk.vhdx" + chunks.RECIPE_SUFFIX)
    recipe.write_bytes(b"to nie jest przepis")

    store = chunks.ChunkStore(destination, None)
    assert chunks.collect_garbage(store, [plan.version, ""]) == (0, 0)
    assert _chunk_files(destination) == before


def test_trial_restore_handles_chunked_files(tmp_path, source):
    destination = tmp_path / "kopia"
    _run(source, destination)
    result = engine.trial_restore(destination, None, Reporter(), seed=1)
    assert result.ok, result.errors
    assert result.files_done == 2


def test_restore_without_manifest_understands_recipes(tmp_path, source):
    destination = tmp_path / "kopia"
    plan, _ = _run(source, destination)
    for leftover in destination.glob(".cleanvault-manifest*"):
        leftover.unlink()
    restore = engine.plan_restore(str(destination / plan.version), str(tmp_path / "cel"), reporter=Reporter())
    keys = {item.key for item in restore.items}
    assert f"{source.name}/dysk.vhdx" in keys
    assert not any(chunks.CHUNK_DIR in key for key in keys)


def test_delta_can_be_switched_off(tmp_path, source):
    destination = tmp_path / "kopia"
    plan, _ = _run(source, destination, delta=False)
    assert (destination / plan.version / source.name / "dysk.vhdx").is_file()
    assert not (destination / chunks.CHUNK_DIR).exists()


@pytest.mark.parametrize("encrypted", [False, True])
def test_rescue_script_rebuilds_chunked_files(tmp_path, source, encrypted):
    destination = tmp_path / "kopia"
    key = keyring() if encrypted else None
    plan, _ = _run(source, destination, key=key)
    note = (destination / rescue.NOTE_NAME).read_text(encoding="utf-8-sig")
    assert "FRAGMENTAMI" in note and "IN CHUNKS" in note

    target = tmp_path / "odzyskane"
    env = {k: v for k, v in os.environ.items() if k not in ("TVB_PASSWORD", "PYTHONPATH")}
    if encrypted:
        env["TVB_PASSWORD"] = PASSWORD
    done = subprocess.run(
        [sys.executable, "-I", str(resource_path("assets", "recovery", rescue.SCRIPT_NAME)),
         str(destination / plan.version), str(target)],
        capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=120,
    )
    assert done.returncode == 0, done.stdout + done.stderr
    assert (target / source.name / "dysk.vhdx").read_bytes() == (source / "dysk.vhdx").read_bytes()
    assert (target / source.name / "notatka.txt").read_text(encoding="utf-8") == "mały plik"
