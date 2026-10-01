"""Audyt kopii względem pieczęci w publicznym dzienniku (audit.py).

Najważniejsze: podmiana pliku jest wykryta, NAWET gdy podmieniono też spis
treści kopii (manifest) — wzorcem jest spis oznakowany w dzienniku; podmieniony
oznakowany spis nie daje fałszywego „nietknięta”; zaszyfrowana kopia jest
sprawdzana po odszyfrowaniu (suma treści), a uszkodzony szyfrogram — wykryty.
"""

from __future__ import annotations

import os
import shutil
import stat
import time
from pathlib import Path

import pytest
from test_proof import FakeBeatTime

from cleanvault import audit, engine, proof
from cleanvault.crypto import ENCRYPTED_SUFFIX, PasswordKeyring
from cleanvault.engine import BackupConfig, Reporter

PASSWORD = "Bardzo-dlugie-haslo-kopii-2026!"


@pytest.fixture()
def beattime(monkeypatch):
    fake = FakeBeatTime()
    monkeypatch.setattr(proof, "BASE_URL", fake.url)
    monkeypatch.setattr(proof, "PINNED_KEYS", ({"public_key": fake.public_b64, "active_from": "2026-09-21"},))
    yield fake
    fake.server.shutdown()


def _source(tmp_path: Path) -> Path:
    source = tmp_path / "Dokumenty"
    (source / "Umowy").mkdir(parents=True)
    (source / "Umowy" / "umowa.txt").write_text("treść umowy", encoding="utf-8")
    (source / "faktura.txt").write_text("faktura 2026/09", encoding="utf-8")
    (source / "notatka.txt").write_text("notatka", encoding="utf-8")
    return source


def _backup(source: Path, destination: Path, keyring=None):
    config = BackupConfig(sources=[str(source)], destination=str(destination), structure="dated",
                          excludes=[], stamp_updates=False, catchup_passes=0, timestamp=True,
                          encrypt=keyring is not None)
    plan = engine.plan_backup(config, Reporter())
    result = engine.run_backup(plan, keyring, Reporter())
    assert result.ok, result.errors
    return plan.version


def _sign(beattime, destination: Path) -> None:
    beattime.close_week()
    for version in audit.sealed_versions(destination):
        assert proof.refresh(audit.version_folder(destination, version), proof.BeatTimeClient()).status == "signed"


def _open_next_week(fake) -> None:
    """Jak prawdziwy Sigelith: zamknięty tydzień jest zamrożony, nowe znaczniki idą do następnego."""
    closed = list(fake.digests)
    original = fake.payload

    def payload(digest):
        if digest in closed:
            current, fake.digests = fake.digests, closed
            try:
                return original(digest)
            finally:
                fake.digests = current
        return {"found": True, "digest": digest, "beat": "@512.34", "utc": "2026-10-01T12:17:00Z",
                "seq": len(fake.digests), "week": "2026-W40", "week_closed": False}

    fake.payload = payload


def test_untouched_backup_is_intact(tmp_path, beattime):
    destination = tmp_path / "kopia"
    version = _backup(_source(tmp_path), destination)
    _sign(beattime, destination)
    result = audit.audit_version(destination, version, None, Reporter())
    assert result.intact, result.describe()
    assert result.checked == result.listed == 3 and not result.sampled
    assert "Nietknięta" in result.describe()


def test_changed_file_is_caught_even_with_a_forged_manifest(tmp_path, beattime):
    destination = tmp_path / "kopia"
    version = _backup(_source(tmp_path), destination)
    _sign(beattime, destination)
    stored = destination / version / "Dokumenty" / "Umowy" / "umowa.txt"
    stored.write_text("treść umowy — podmieniona", encoding="utf-8")
    # Atakujący niszczy (albo „poprawia”) spis treści kopii — bez znaczenia: wzorcem
    # audytu jest spis oznakowany w publicznym dzienniku, nie manifest obok plików.
    for manifest in destination.glob(".cleanvault-manifest*"):
        if manifest.is_dir():
            shutil.rmtree(manifest, onerror=lambda f, p, _e: (os.chmod(p, stat.S_IWRITE), f(p)))
        else:
            os.chmod(manifest, stat.S_IWRITE | stat.S_IREAD)
            manifest.unlink()
    assert not list(destination.glob(".cleanvault-manifest*"))
    result = audit.audit_version(destination, version, None, Reporter())
    assert not result.intact
    assert result.changed == ["Dokumenty/Umowy/umowa.txt"]
    assert "PODMIENIONA" in result.describe()


def test_deleted_file_is_missing(tmp_path, beattime):
    destination = tmp_path / "kopia"
    version = _backup(_source(tmp_path), destination)
    _sign(beattime, destination)
    (destination / version / "Dokumenty" / "notatka.txt").unlink()
    result = audit.audit_version(destination, version, None, Reporter())
    assert result.missing == ["Dokumenty/notatka.txt"] and not result.intact


def test_forged_sealed_index_gives_no_false_all_clear(tmp_path, beattime):
    destination = tmp_path / "kopia"
    version = _backup(_source(tmp_path), destination)
    _sign(beattime, destination)
    folder = destination / version
    index = folder / proof.INDEX_NAME
    index.write_bytes(index.read_bytes().replace(b"\t", b"\t0", 1))
    result = audit.audit_version(destination, version, None, Reporter())
    assert result.sealed and not result.seal_proven and result.checked == 0
    assert not result.intact


def test_encrypted_backup_is_checked_after_decryption(tmp_path, beattime):
    destination = tmp_path / "kopia"
    keyring = PasswordKeyring(PASSWORD)
    version = _backup(_source(tmp_path), destination, keyring)
    _sign(beattime, destination)
    with pytest.raises(audit.AuditNeedsPassword):
        audit.audit_version(destination, version, None, Reporter())
    assert audit.audit_version(destination, version, PasswordKeyring(PASSWORD), Reporter()).intact

    stored = destination / version / "Dokumenty" / ("faktura.txt" + ENCRYPTED_SUFFIX)
    blob = bytearray(stored.read_bytes())
    blob[-20] ^= 0x01  # jeden bit szyfrogramu
    stored.write_bytes(bytes(blob))
    result = audit.audit_version(destination, version, PasswordKeyring(PASSWORD), Reporter())
    assert result.unreadable == ["Dokumenty/faktura.txt"] and not result.intact


def test_sample_audit(tmp_path, beattime):
    destination = tmp_path / "kopia"
    version = _backup(_source(tmp_path), destination)
    _sign(beattime, destination)
    result = audit.audit_version(destination, version, None, Reporter(), sample=2, seed=7)
    assert result.sampled and result.checked == 2 and result.listed == 3 and result.intact


def test_last_intact_version_skips_the_tampered_newest(tmp_path, beattime):
    source = _source(tmp_path)
    destination = tmp_path / "kopia"
    older = _backup(source, destination)
    time.sleep(0.05)
    (source / "notatka.txt").write_text("notatka — wersja 2", encoding="utf-8")
    newer = _backup(source, destination)
    assert newer != older
    _sign(beattime, destination)
    stored = destination / newer / "Dokumenty" / "notatka.txt"
    stored.write_text("zaszyfrowane przez ransomware", encoding="utf-8")
    audits, intact = audit.last_intact(destination, None, Reporter())
    assert [a.version for a in audits][:1] == [newer] and not audits[0].intact
    assert intact == older


def test_unsealed_version_is_reported_as_such(tmp_path):
    result = audit.audit_version(tmp_path, "", None, Reporter())
    assert not result.sealed and not result.intact
    assert "nie ma pieczęci" in result.describe()


def test_every_backup_audits_a_sample_of_an_older_signed_version(tmp_path, beattime):
    source = _source(tmp_path)
    destination = tmp_path / "kopia"
    older = _backup(source, destination)
    _sign(beattime, destination)
    _open_next_week(beattime)

    def next_backup():
        time.sleep(0.05)
        (source / "notatka.txt").write_text(f"notatka {time.time()}", encoding="utf-8")
        config = BackupConfig(sources=[str(source)], destination=str(destination), structure="dated",
                              excludes=[], stamp_updates=False, catchup_passes=0, timestamp=True)
        return engine.run_backup(engine.plan_backup(config, Reporter()), None, Reporter())

    result = next_backup()
    assert any("próbka wersji" in note and "zgodna" in note for note in result.notes), result.notes

    (destination / older / "Dokumenty" / "faktura.txt").write_text("podmieniona", encoding="utf-8")
    result = next_backup()
    assert result.ok, "podmiana starszej wersji nie psuje bieżącej kopii"
    warnings = [note for note in result.notes if note.startswith("UWAGA — audyt z pieczęcią")]
    assert warnings and "Dokumenty/faktura.txt" in warnings[0], result.notes
