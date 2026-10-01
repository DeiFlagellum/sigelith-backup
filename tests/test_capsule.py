"""Kapsuła czasu (capsule.py + ibe.py) — koperta beattime-seal-v1 ze strony sigelith.org/capsule/.

Najważniejszy test: kapsułę zapieczętowaną przez Sigelith Backup otwiera KOD
STRONY (apps/web/static/web/seal/core.js + beacons.js + ibe.js z repozytorium
Sigelith) — udziałami beaconów i kodem odzyskiwania. Klucze łańcucha i operatora
są testowe (znamy sekret, więc liczymy podpisy tożsamości), budowa koperty — ta
sama co przy prawdziwym drand quicknet i serwerze kluczy Sigelith.
"""

from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from cleanvault import browse, capsule, engine, ibe, rescue
from cleanvault.engine import BackupConfig, Reporter
from cleanvault.paths import CAPSULES_DIR

#: Moduły strony kapsuły z repozytorium Sigelith — domyślnie katalog obok tego repozytorium.
SIGELITH_REPO = Path(os.environ.get("SIGELITH_REPO", Path(__file__).resolve().parents[2] / "beattime"))
SEAL_JS = SIGELITH_REPO / "apps" / "web" / "static" / "web" / "seal"
CHAIN_SECRET = 0x1D2C3B4A59687786
OPERATOR_SECRET = 0x7A6B5C4D3E2F1001


@pytest.fixture(scope="module")
def keys():
    chain = capsule.Chain(name="test", chain_hash="ab" * 32, scheme=ibe.SCHEME, period=3,
                          genesis_time=1692803367, public_key=ibe.public_key_for(CHAIN_SECRET).hex())
    operator = {"op": "test-op", "pub": base64.b64encode(ibe.public_key_for(OPERATOR_SECRET)).decode(),
                "scheme": ibe.SCHEME, "url": "https://example.invalid/share/"}
    return chain, operator


def _signatures(envelope: dict) -> tuple[bytes, bytes]:
    drand = next(s for s in envelope["shares"] if s["kind"] == "drand")
    return (ibe.identity_signature(CHAIN_SECRET, capsule.drand_identity(drand["round"])),
            ibe.identity_signature(OPERATOR_SECRET, capsule.beat_identity(envelope["beat"])))


def _seal(keys, payload: bytes, detached: bool):
    chain, operator = keys
    escrow = capsule.EscrowSealer()
    blob = __import__("io").BytesIO() if detached else None
    index = capsule.beat_index(datetime.now(UTC)) + 5000
    envelope = capsule.seal(payload, index=index, t=2, blob_out=blob,
                            sealers=[capsule.DrandSealer(chain), capsule.BeatSealer(operator), escrow])
    code = capsule.recovery_code(capsule.envelope_id(envelope), escrow.x, escrow.share)
    return envelope, (blob.getvalue() if blob else None), code, (escrow.x, escrow.share)


def test_shamir_any_two_of_three():
    secret = bytes(range(32))
    parts = capsule.shamir_split(secret, 2, 3)
    for pair in ((0, 1), (0, 2), (1, 2)):
        assert capsule.shamir_combine([parts[pair[0]], parts[pair[1]]]) == secret
    assert capsule.shamir_combine(parts[:1]) != secret or len(parts[0][1]) != 32
    with pytest.raises(ValueError):
        capsule.shamir_split(secret, 1, 3)


def test_round_never_before_the_beat():
    chain = capsule.QUICKNET
    for index in (20726724, 20726725, 21_000_000, 25_000_000):
        round_number = capsule.round_for_beat(chain, index)
        round_time = chain.genesis_time + (round_number - 1) * chain.period
        assert round_time * 1_000_000 >= index * capsule.MICROSECONDS_PER_BEAT
        assert (round_time - chain.period) * 1_000_000 < index * capsule.MICROSECONDS_PER_BEAT


def test_ibe_round_trip_and_wrong_signature():
    identity = capsule.beat_identity(12345678)
    ct = ibe.encrypt(ibe.public_key_for(OPERATOR_SECRET), identity, b"u" * 32)
    assert ibe.decrypt(ibe.identity_signature(OPERATOR_SECRET, identity), ct) == b"u" * 32
    with pytest.raises(ibe.IbeError):
        ibe.decrypt(ibe.identity_signature(OPERATOR_SECRET, capsule.beat_identity(12345679)), ct)


@pytest.mark.parametrize("detached", [False, True])
def test_python_seals_and_opens(keys, detached):
    payload = capsule.pack_payload({"kind": "file", "name": "list do rodziny.zip", "type": "application/zip"},
                                   b"PK" + bytes(300_000 if detached else 1000))
    envelope, blob, _code, escrow = _seal(keys, payload, detached)
    drand_sig, beat_sig = _signatures(envelope)
    drand_share = ibe.decrypt(drand_sig, base64.b64decode(envelope["shares"][0]["ct"]))
    beat_share = ibe.decrypt(beat_sig, base64.b64decode(envelope["shares"][1]["ct"]))
    for shares in ([(1, drand_share), (2, beat_share)], [(1, drand_share), escrow], [(2, beat_share), escrow]):
        assert capsule.open_payload(envelope, list(shares), blob) == payload
    assert envelope["payload"]["mode"] == ("detached" if detached else "inline")
    assert "ct" not in envelope["shares"][2] and envelope["shares"][2]["kind"] == "escrow"


def test_envelope_carries_no_secret(keys):
    envelope, _blob, _code, escrow = _seal(keys, b"x" * 10, False)
    text = json.dumps(envelope)
    assert escrow[1].hex() not in text and base64.b64encode(escrow[1]).decode() not in text


@pytest.mark.skipif(shutil.which("node") is None or not (SEAL_JS / "core.js").exists(),
                    reason="Node albo repozytorium Sigelith niedostępne")
@pytest.mark.parametrize("detached", [False, True])
def test_the_capsule_page_opens_a_capsule_sealed_by_sigelith_backup(keys, detached, tmp_path):
    """Kod strony sigelith.org/capsule/ otwiera kapsułę z programu — beaconami i kodem odzyskiwania."""
    body = b"PK\x03\x04" + bytes(range(256)) * (1200 if detached else 4)
    payload = capsule.pack_payload({"kind": "file", "name": "dokumenty — 2036.zip", "type": "application/zip"}, body)
    envelope, blob, code, _escrow = _seal(keys, payload, detached)
    drand_sig, beat_sig = _signatures(envelope)
    script = """
import * as S from 'CORE_JS';
import * as B from 'BEACONS_JS';
import { readFileSync } from 'node:fs';
const a = JSON.parse(readFileSync(process.argv[1], 'utf8'));
const env = a.envelope;
const blob = a.blob ? Uint8Array.from(Buffer.from(a.blob, 'base64')) : null;
const open = (shares) => env.payload.mode === 'detached' ? S.openDetached(env, blob, shares) : S.openInline(env, shares);
const out = {};
out.id = await S.envelopeId(env);
if (blob) await S.checkCiphertext(env, blob);
const d = await B.openShare(env.shares[0], a.drand);
const b = await B.openShare(env.shares[1], a.beat);
const r = await S.decodeRecovery(a.code);
const hex = (raw) => { const p = S.unpackPayload(raw); return JSON.stringify(p.meta) + '|' + Buffer.from(p.body).toString('hex'); };
out.beacons = hex(await open([{ x: env.shares[0].x, y: d }, { x: env.shares[1].x, y: b }]));
out.recovery = hex(await open([{ x: env.shares[0].x, y: d }, { x: r.x, y: r.y }]));
console.log(JSON.stringify(out));
""".replace("CORE_JS", (SEAL_JS / "core.js").as_uri()).replace("BEACONS_JS", (SEAL_JS / "beacons.js").as_uri())
    args = {"envelope": envelope, "blob": base64.b64encode(blob).decode() if blob else None,
            "drand": drand_sig.hex(), "beat": beat_sig.hex(), "code": code}
    args_file = tmp_path / "kapsula.json"
    args_file.write_text(json.dumps(args), encoding="utf-8")
    run = subprocess.run(["node", "--input-type=module", "-e", script, str(args_file)],
                         capture_output=True, encoding="utf-8", timeout=300)
    assert run.returncode == 0, run.stderr[-2000:]
    result = json.loads(run.stdout.strip().splitlines()[-1])
    meta, raw = capsule.unpack_payload(payload)
    expected = json.dumps(meta, separators=(",", ":"), ensure_ascii=False) + "|" + raw.hex()
    assert result["id"] == capsule.envelope_id(envelope)
    assert json.loads(result["beacons"].split("|")[0]) == meta and result["beacons"].split("|")[1] == raw.hex()
    assert result["recovery"] == result["beacons"]
    assert expected.split("|")[1] == raw.hex()


def test_seal_files_writes_the_capsule_pair_and_the_code(keys, tmp_path, monkeypatch):
    chain, operator = keys
    monkeypatch.setattr(capsule, "QUICKNET", chain)
    source = tmp_path / "Dla rodziny"
    (source / "listy").mkdir(parents=True)
    (source / "listy" / "list.txt").write_text("Otworzyć w 2036.", encoding="utf-8")
    (source / "hasla.kdbx").write_bytes(os.urandom(400_000))  # nie do skompresowania
    when = datetime.now(UTC) + timedelta(days=3650)
    sealed = capsule.seal_files([source], when, tmp_path / "Sigelith Capsules", "Dla rodziny", operator)
    assert sealed.opens_at >= when and sealed.opens_at - when < timedelta(seconds=87)
    assert sealed.envelope_path.name == f"capsule-{sealed.envelope_id}.beatseal.json"
    assert sealed.blob_path is not None and sealed.blob_path.exists()
    envelope = json.loads(sealed.envelope_path.read_bytes())
    assert envelope["hint"].endswith("Z") and envelope["t"] == 2 and len(envelope["shares"]) == 3
    assert sealed.recovery_code.startswith(sealed.envelope_id[:4].upper() + "-")

    drand_sig, beat_sig = _signatures(envelope)
    shares = [(1, ibe.decrypt(drand_sig, base64.b64decode(envelope["shares"][0]["ct"]))),
              (2, ibe.decrypt(beat_sig, base64.b64decode(envelope["shares"][1]["ct"])))]
    meta, body = capsule.unpack_payload(capsule.open_payload(envelope, shares, sealed.blob_path.read_bytes()))
    assert meta == {"kind": "file", "name": "Dla rodziny.zip", "type": "application/zip"}
    import io
    import zipfile
    names = sorted(zipfile.ZipFile(io.BytesIO(body)).namelist())
    assert names == ["Dla rodziny/hasla.kdbx", "Dla rodziny/listy/list.txt"]


def test_past_moment_is_refused(keys, tmp_path):
    with pytest.raises(ValueError):
        capsule.seal_files([tmp_path], datetime.now(UTC) - timedelta(days=1), tmp_path / "k", "x",
                           keys[1])


@pytest.fixture()
def offline(monkeypatch):
    """Każda próba połączenia kończy test — pieczętowanie ma działać bez sieci."""
    import socket

    def refuse(*_args, **_kwargs):
        raise AssertionError("kapsuła próbowała połączyć się z siecią")

    monkeypatch.setattr(socket.socket, "connect", refuse)
    monkeypatch.setattr(socket, "create_connection", refuse)


def test_sealing_never_touches_the_network(offline, tmp_path):
    source = tmp_path / "Dla rodziny"
    source.mkdir()
    (source / "list.txt").write_text("Otworzyć w 2036.", encoding="utf-8")
    sealed = capsule.seal_files([source], datetime.now(UTC) + timedelta(days=30), tmp_path / "k", "Dla rodziny")
    envelope = json.loads(sealed.envelope_path.read_bytes())
    beat = next(s for s in envelope["shares"] if s["kind"] == "beat")
    drand = next(s for s in envelope["shares"] if s["kind"] == "drand")
    assert beat["op"] == "beattime" and beat["pub"] == capsule.BUILTIN_OPERATOR["pub"]
    assert len(base64.b64decode(beat["pub"])) == 96
    assert drand["chain_hash"] == capsule.QUICKNET.chain_hash


def test_capsule_note_is_bilingual_and_names_the_files():
    when = datetime(2036, 10, 1, 12, 0, tzinfo=UTC)
    note = rescue.capsule_note("Dla rodziny", "ABCD-EFGH", when, ["capsule-x.beatseal.json", "capsule-x.bin"])
    assert "ABCD-EFGH" in note and "2036-10-01 12:00 UTC" in note
    assert "capsule-x.beatseal.json + capsule-x.bin" in note
    assert "PL:" in note and "EN:" in note and "sigelith.org/capsule/" in note


def test_backups_leave_the_capsule_folder_alone_and_the_note_describes_it(tmp_path):
    source = tmp_path / "Dokumenty"
    source.mkdir()
    (source / "notatki.txt").write_text("zwykły plik", encoding="utf-8")
    destination = tmp_path / "kopia"
    kept = destination / CAPSULES_DIR / "Dla rodziny 2036-10-01" / "capsule-0123456789abcdef.beatseal.json"
    kept.parent.mkdir(parents=True)
    kept.write_text("{}", encoding="utf-8")
    for _ in range(3):
        config = BackupConfig(sources=[str(source)], destination=str(destination), structure="dated", excludes=[],
                              stamp_updates=False, catchup_passes=0, retention=1)
        assert engine.run_backup(engine.plan_backup(config, Reporter()), None, Reporter()).ok
        time.sleep(0.05)
    assert kept.exists(), "sprzątanie starych wersji nie rusza kapsuł"
    assert all(v.name for v in browse.versions(destination)), "folder kapsuł to nie kopia lustrzana"
    note = (destination / rescue.NOTE_NAME).read_text(encoding="utf-8-sig")
    assert note.count(CAPSULES_DIR) >= 2 and "sigelith.org/capsule/" in note

    mirror = tmp_path / "lustro"
    (mirror / CAPSULES_DIR).mkdir(parents=True)
    config = BackupConfig(sources=[str(source)], destination=str(mirror), structure="mirror", excludes=[],
                          stamp_updates=False, catchup_passes=0, delete_removed=True)
    assert engine.run_backup(engine.plan_backup(config, Reporter()), None, Reporter()).ok
    names = [item.name for item in browse.list_folder(mirror, "")]
    assert CAPSULES_DIR not in names and "Dokumenty" in names
    assert (mirror / CAPSULES_DIR).is_dir()


def test_capsule_dialog_seals_a_folder_into_the_backup(keys, offline, tmp_path, monkeypatch):
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    pytest.importorskip("PySide6")
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox

    from cleanvault.ui import capsule_dialog

    qapp = QApplication.instance() or QApplication([])
    chain, operator = keys
    monkeypatch.setattr(capsule, "QUICKNET", chain)
    monkeypatch.setattr(capsule, "BUILTIN_OPERATOR", operator)
    source = tmp_path / "Dla rodziny"
    source.mkdir()
    (source / "list.txt").write_text("Otworzyć w 2036.", encoding="utf-8")
    when = datetime.now(UTC) + timedelta(days=3650)

    class Settings:
        def __init__(self, *_args):
            pass

        def exec(self):
            return QDialog.DialogCode.Accepted

        def values(self):
            return "Dla rodziny", when

    monkeypatch.setattr(QFileDialog, "getExistingDirectory", lambda *args, **kwargs: str(source))
    monkeypatch.setattr(capsule_dialog, "_NewCapsule", Settings)
    shown = []
    monkeypatch.setattr(QMessageBox, "information", lambda *args: shown.append(args[2]))

    backup = tmp_path / "kopia"
    backup.mkdir()
    dialog = capsule_dialog.CapsuleDialog(str(backup))
    assert dialog.list.count() == 0
    dialog._new()
    assert dialog._worker.wait(120_000)
    for _ in range(5):
        qapp.processEvents()

    assert dialog.list.count() == 1 and shown
    code = QGuiApplication.clipboard().text()
    notes = list((backup / CAPSULES_DIR).glob(f"*/{rescue.CAPSULE_NOTE_NAME}"))
    assert len(notes) == 1 and code and code in notes[0].read_text(encoding="utf-8-sig")
    assert not dialog.open_btn.isEnabled() or dialog.list.currentRow() < 0, "zamkniętej nie otwiera się na stronie"
