"""Dowody Sigelith: odnajdywanie danych, magazyn dokumentów w kopii, sprawdzanie i odzysk."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import time
from pathlib import Path

import pytest

from cleanvault import browse, crypto, engine, evidence, proof, rescue, sigelith
from cleanvault.crypto import KdfParams, PasswordKeyring
from cleanvault.engine import BackupConfig, Reporter
from cleanvault.snapshot import Manifest

WEEK = "2026-W39"


@pytest.fixture()
def signer(monkeypatch):
    """Klucz Ed25519 udający klucz Sigelith — wpięty jako przypięty klucz programu."""
    from Cryptodome.PublicKey import ECC
    from Cryptodome.Signature import eddsa

    key = ECC.generate(curve="ed25519")
    public = base64.b64encode(key.public_key().export_key(format="raw")).decode()
    monkeypatch.setattr(proof, "PINNED_KEYS", ({"public_key": public, "active_from": "2026-01-01"},))

    def sign(week: str, root: str) -> str:
        message = f"beattime-proof-v1|{week}|{root}".encode()
        return base64.b64encode(eddsa.new(key, "rfc8032").sign(message)).decode()

    sign.public = public
    return sign


def _entry(path: Path, sign=None, content: bytes | None = None, **extra) -> dict:
    """Wpis historii Sigelith dla pliku — z prawdziwym drzewem tygodnia (dwa liście)."""
    data = content if content is not None else path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    other = hashlib.sha256(b"inny dokument tego tygodnia").hexdigest()
    leaf = hashlib.sha256(b"\x00" + bytes.fromhex(digest)).digest()
    sibling = hashlib.sha256(b"\x00" + bytes.fromhex(other)).digest()
    root = hashlib.sha256(b"\x01" + leaf + sibling).hexdigest()
    entry = {
        "digest": digest, "file_name": path.name, "file_path": str(path), "file_size": len(data),
        "note": "dla notariusza", "beat": "@500", "utc": "2026-09-27T10:00:00+00:00", "seq": 7,
        "week": WEEK, "week_closed": sign is not None, "week_root": root if sign else "",
        "inclusion_proof": [{"side": "R", "hash": sibling.hex()}] if sign else [],
        "root_signature": sign(WEEK, root) if sign else "", "public_key": getattr(sign, "public", ""),
        "level": "signed" if sign else "recorded", "source": "beattime",
    }
    entry.update(extra)
    return entry


def _sigelith_dir(tmp_path: Path, entries: list[dict], monkeypatch=None) -> Path:
    data_dir = tmp_path / "Sigelith"
    (data_dir / "witness").mkdir(parents=True, exist_ok=True)
    (data_dir / "history.json").write_text(json.dumps(entries, ensure_ascii=False), encoding="utf-8")
    (data_dir / "settings.json").write_text("{}", encoding="utf-8")
    (data_dir / "witness" / "log.jsonl").write_text('{"n": 1}\n', encoding="utf-8")
    (data_dir / "sigelith.log").write_text("dziennik", encoding="utf-8")
    if monkeypatch is not None:
        monkeypatch.setattr(sigelith, "find_data_dir", lambda env=None: data_dir)
    return data_dir


def keyring():
    return PasswordKeyring("Hasło-dowodów", KdfParams(crypto.KDF_PBKDF2_SHA256, b"e" * 16, 1000))


def _backup(source: Path, destination: Path, key=None, **kwargs):
    config = BackupConfig(sources=[str(source)], destination=str(destination), structure="dated", excludes=[],
                          stamp_updates=False, catchup_passes=0, encrypt=key is not None, **kwargs)
    plan = engine.plan_backup(config, Reporter())
    result = engine.run_backup(plan, key, Reporter())
    assert result.ok, result.errors
    return plan, result


@pytest.fixture()
def documents(tmp_path):
    root = tmp_path / "Dokumenty"
    (root / "Umowy").mkdir(parents=True)
    (root / "Umowy" / "Umowa najmu.pdf").write_bytes(b"%PDF umowa najmu, wersja podpisana")
    (root / "notatki.txt").write_text("zwykły plik", encoding="utf-8")
    return root


# ------------------------------------------------------------------ odnajdywanie


def test_data_dir_is_found_like_sigelith_finds_it(tmp_path):
    local, profile = tmp_path / "Local", tmp_path / "Profil"
    env = {"LOCALAPPDATA": str(local), "USERPROFILE": str(profile)}
    assert sigelith.find_data_dir(env) is None

    legacy = profile / "BeatStamp"
    legacy.mkdir(parents=True)
    (legacy / "history.json").write_text("[]", encoding="utf-8")
    assert sigelith.find_data_dir(env) == legacy, "dane sprzed zmiany nazwy"

    default = profile / "Sigelith"
    default.mkdir()
    (default / "history.json").write_text("[]", encoding="utf-8")
    assert sigelith.find_data_dir(env) == default, "nowa nazwa ma pierwszeństwo"

    chosen = tmp_path / "Dowody gdzie indziej"
    chosen.mkdir()
    (chosen / "history.json").write_text("[]", encoding="utf-8")
    packaged = local / "Packages" / "AdamKoch.SigelithDesktop_rwa3tvtpxc2q6" / "LocalCache" / "Local" / "Sigelith"
    packaged.mkdir(parents=True)
    (packaged / sigelith.POINTER_NAME).write_text(json.dumps({"katalog": str(chosen)}), encoding="utf-8")
    assert sigelith.find_data_dir(env) == chosen, "wskaźnik z prywatnej kopii pakietu MSIX"

    real_pointer = local / "Sigelith" / sigelith.POINTER_NAME
    real_pointer.parent.mkdir(parents=True)
    real_pointer.write_text(json.dumps({"katalog": ""}), encoding="utf-8")
    assert sigelith.find_data_dir(env) == default, "pusty wskaźnik = folder domyślny"

    forced = tmp_path / "wymuszony"
    forced.mkdir()
    (forced / "history.json").write_text("[]", encoding="utf-8")
    assert sigelith.find_data_dir({**env, "SIGELITH_DATA_DIR": str(forced)}) == forced


def test_history_is_read_tolerantly(tmp_path, documents, signer):
    doc = documents / "Umowy" / "Umowa najmu.pdf"
    good = _entry(doc, signer)
    pending = _entry(doc)  # ten sam dokument, dowód jeszcze niepodpisany — wygrywa kompletny
    legacy = {"digest": "ab" * 32, "source": "tvs-legacy"}
    broken = {"digest": "to nie jest suma"}
    data_dir = _sigelith_dir(tmp_path, [pending, good, legacy, broken, "śmieć"])
    stamps = sigelith.load_stamps(data_dir)
    assert [s.digest for s in stamps] == [good["digest"]] and stamps[0].complete

    (data_dir / "history.json").write_text(json.dumps({"entries": [good]}), encoding="utf-8")
    assert len(sigelith.load_stamps(data_dir)) == 1, "także postać ze słownikiem"
    (data_dir / "history.json").write_text("{uszkodzony", encoding="utf-8")
    assert sigelith.load_stamps(data_dir) == []


def test_beatproof_matches_the_sigelith_format_and_verifies_offline(tmp_path, documents, signer):
    stamp = sigelith.load_stamps(_sigelith_dir(tmp_path, [_entry(documents / "Umowy" / "Umowa najmu.pdf",
                                                                  signer)]))[0]
    data = sigelith.beatproof(stamp)
    assert data["format"] == "beatproof-v1" and data["digest"] == stamp.digest
    assert data["generator"].startswith("Sigelith Backup") and data["authority"] == "https://sigelith.org"
    required = {"digest", "week", "week_root", "inclusion_proof", "root_signature", "public_key", "utc", "beat"}
    assert required <= set(data)
    assert sigelith.proof_problems(data) == []
    tampered = dict(data, root_signature=signer(WEEK, "00" * 32))
    assert sigelith.proof_problems(tampered)


# ------------------------------------------------------------------ magazyn w kopii


def test_backup_safeguards_the_exact_stamped_document(tmp_path, documents, signer, monkeypatch):
    doc = documents / "Umowy" / "Umowa najmu.pdf"
    data_dir = _sigelith_dir(tmp_path, [_entry(doc, signer)], monkeypatch)
    destination = tmp_path / "kopia"
    _, result = _backup(documents, destination, sigelith=True)

    items = evidence.list_items(destination)
    assert len(items) == 1 and items[0].document.read_bytes() == doc.read_bytes()
    assert "Umowa najmu.pdf" in items[0].folder.name
    assert json.loads(items[0].proof_file.read_text(encoding="utf-8"))["digest"] == hashlib.sha256(
        doc.read_bytes()).hexdigest()
    assert evidence.verify_item(items[0], None) == []
    assert any("Dowody Sigelith" in note for note in result.notes)

    keys = set(Manifest.load(destination).entries)
    assert f"{data_dir.name}/history.json" in keys, "folder danych Sigelith jest źródłem kopii"
    assert f"{data_dir.name}/witness/log.jsonl" not in keys and f"{data_dir.name}/sigelith.log" not in keys

    # dokument zmienia się po stemplu — magazyn trzyma bajty, które oznakowano
    doc.write_bytes(b"%PDF umowa najmu, poprawiona po podpisie")
    time.sleep(0.05)
    _backup(documents, destination, sigelith=True)
    kept = evidence.list_items(destination)
    assert len(kept) == 1 and kept[0].document.read_bytes() == b"%PDF umowa najmu, wersja podpisana"
    assert evidence.verify_item(kept[0], None) == []


def test_document_changed_before_protection_is_recovered_from_older_versions(tmp_path, documents, signer,
                                                                             monkeypatch):
    doc = documents / "Umowy" / "Umowa najmu.pdf"
    signed = doc.read_bytes()
    _backup(documents, tmp_path / "kopia")  # zwykła kopia, bez ochrony dowodów
    doc.write_bytes(b"%PDF inna wersja")
    _sigelith_dir(tmp_path, [_entry(doc, signer, content=signed)], monkeypatch)
    time.sleep(0.05)
    _, result = _backup(documents, tmp_path / "kopia", sigelith=True)
    items = evidence.list_items(tmp_path / "kopia")
    assert items[0].document.read_bytes() == signed
    assert any("odtworzone ze starszych wersji kopii: 1" in note for note in result.notes)


def test_stamp_without_any_copy_keeps_the_proof_and_reports_it(tmp_path, documents, signer, monkeypatch):
    lost = tmp_path / "zniknal.docx"
    lost.write_bytes(b"dokument, ktorego juz nie ma")
    entry = _entry(lost, signer)
    lost.unlink()
    _sigelith_dir(tmp_path, [entry], monkeypatch)
    _, result = _backup(documents, tmp_path / "kopia", sigelith=True)
    item = evidence.list_items(tmp_path / "kopia")[0]
    assert item.document is None and item.proof_file is not None
    assert any("Bez dokumentu: 1 stempel" in note for note in result.notes)
    assert evidence.verify_item(item, None) == ["W magazynie nie ma dokumentu do tego dowodu."]


def test_pending_proof_gets_the_week_signature_later(tmp_path, documents, signer, monkeypatch):
    doc = documents / "Umowy" / "Umowa najmu.pdf"
    data_dir = _sigelith_dir(tmp_path, [_entry(doc)], monkeypatch)
    _backup(documents, tmp_path / "kopia", sigelith=True)
    item = evidence.list_items(tmp_path / "kopia")[0]
    assert not json.loads(item.proof_file.read_text(encoding="utf-8"))["week_closed"]
    assert evidence.verify_item(item, None)[0].startswith("Tydzień stempla")

    (data_dir / "history.json").write_text(json.dumps([_entry(doc, signer)]), encoding="utf-8")
    time.sleep(0.05)
    _, second = _backup(documents, tmp_path / "kopia", sigelith=True)
    assert any("uzupełnione o podpis tygodnia: 1" in note for note in second.notes)
    assert evidence.verify_item(evidence.list_items(tmp_path / "kopia")[0], None) == []


def test_encrypted_backup_keeps_evidence_in_containers(tmp_path, documents, signer, monkeypatch):
    doc = documents / "Umowy" / "Umowa najmu.pdf"
    _sigelith_dir(tmp_path, [_entry(doc, signer)], monkeypatch)
    key = keyring()
    _backup(documents, tmp_path / "kopia", key=key, sigelith=True)
    item = evidence.list_items(tmp_path / "kopia")[0]
    assert item.encrypted and item.document.name.endswith(".cvlt") and item.proof_file.name.endswith(".cvlt")
    assert b"notariusza" not in item.proof_file.read_bytes(), "notatka ze stempla nie leży jawnie"
    assert evidence.verify_item(item, key) == []
    with pytest.raises(crypto.CryptoError):
        evidence.restore_item(item, tmp_path / "bez-hasla", None)
    written = evidence.restore_item(item, tmp_path / "odzysk", key)
    assert {p.name for p in written} == {"Umowa najmu.pdf", "Umowa najmu.pdf.beatproof"}
    assert (tmp_path / "odzysk" / "Umowa najmu.pdf").read_bytes() == doc.read_bytes()


def test_retention_and_browsing_leave_the_evidence_store_alone(tmp_path, documents, signer, monkeypatch):
    _sigelith_dir(tmp_path, [_entry(documents / "Umowy" / "Umowa najmu.pdf", signer)], monkeypatch)
    destination = tmp_path / "kopia"
    for _ in range(3):
        _backup(documents, destination, sigelith=True, retention=1)
        time.sleep(0.05)
    assert len([v for v in browse.versions(destination) if v.name]) == 1, "retencja działa"
    assert len(evidence.list_items(destination)) == 1, "…ale magazynu dowodów nie rusza"
    assert all(v.name for v in browse.versions(destination)), "magazyn to nie kopia lustrzana"

    mirror = tmp_path / "lustro"
    config = BackupConfig(sources=[str(documents)], destination=str(mirror), structure="mirror", excludes=[],
                          stamp_updates=False, catchup_passes=0, delete_removed=True, sigelith=True)
    assert engine.run_backup(engine.plan_backup(config, Reporter()), None, Reporter()).ok
    names = [item.name for item in browse.list_folder(mirror, "")]
    assert evidence.EVIDENCE_DIR not in names and "Dokumenty" in names
    assert len(evidence.list_items(mirror)) == 1


def test_rescue_note_describes_the_evidence_store(tmp_path, documents, signer, monkeypatch):
    _sigelith_dir(tmp_path, [_entry(documents / "Umowy" / "Umowa najmu.pdf", signer)], monkeypatch)
    _backup(documents, tmp_path / "kopia", sigelith=True)
    note = (tmp_path / "kopia" / rescue.NOTE_NAME).read_text(encoding="utf-8-sig")
    assert note.count(evidence.EVIDENCE_DIR) >= 2 and ".beatproof" in note


def test_missing_sigelith_is_a_note_not_an_error(tmp_path, documents, monkeypatch):
    monkeypatch.setattr(sigelith, "find_data_dir", lambda env=None: None)
    _, result = _backup(documents, tmp_path / "kopia", sigelith=True)
    assert any("nie ma jeszcze Sigelith Desktop" in note for note in result.notes)
    assert not os.path.exists(tmp_path / "kopia" / evidence.EVIDENCE_DIR)


# ------------------------------------------------------------------ okno


def test_evidence_dialog_checks_and_restores(tmp_path, documents, signer, monkeypatch):
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    pytest.importorskip("PySide6")
    from PySide6.QtWidgets import QApplication, QFileDialog

    from cleanvault.ui.evidence_dialog import EvidenceDialog

    qapp = QApplication.instance() or QApplication([])
    doc = documents / "Umowy" / "Umowa najmu.pdf"
    _sigelith_dir(tmp_path, [_entry(doc, signer)], monkeypatch)
    _backup(documents, tmp_path / "kopia", sigelith=True)

    dialog = EvidenceDialog(str(tmp_path / "kopia"))
    assert dialog.tree.topLevelItemCount() == 1
    assert dialog.tree.topLevelItem(0).text(1) == "Umowa najmu.pdf"

    def wait():
        assert dialog._worker.wait(30_000)
        for _ in range(5):
            qapp.processEvents()

    dialog._verify()
    wait()
    assert "zgadzają" in dialog.tree.topLevelItem(0).text(2)

    target = tmp_path / "przywrocone"
    monkeypatch.setattr(QFileDialog, "getExistingDirectory", lambda *args, **kwargs: str(target))
    dialog._restore()
    wait()
    restored = list(target.rglob("Umowa najmu.pdf"))
    assert restored and restored[0].read_bytes() == doc.read_bytes()
    dialog.done(0)
