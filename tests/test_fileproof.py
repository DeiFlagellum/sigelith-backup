"""Dowód czasu dla pojedynczego pliku z kopii (fileproof.py, format sigelith-file-proof-v1).

Najważniejsze właściwości: droga w drzewie prowadzi do korzenia dla każdego
rozmiaru drzewa i każdego liścia; dowód jednego pliku nie ujawnia innych;
każda zmiana w dowodzie albo w pliku jest wykryta; stare pieczęci (sprzed
3.0) dalej się sprawdzają.
"""

from __future__ import annotations

import hashlib
import json
import os

import pytest
from test_proof import FakeBeatTime

from cleanvault import browse, fileproof, proof

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ENTRIES = [
    ("Dokumenty/umowa.pdf", 1234, hashlib.sha256(b"umowa").hexdigest()),
    ("Dokumenty/faktura.pdf", 99, hashlib.sha256(b"faktura").hexdigest()),
    ("Zdjecia/2026/lato.jpg", 5_000_000, hashlib.sha256(b"lato").hexdigest()),
    ("Tajne/haslo-do-sejfu.txt", 12, hashlib.sha256(b"sekret").hexdigest()),
    ("notatka.txt", 7, hashlib.sha256(b"notatka").hexdigest()),
]


@pytest.fixture()
def beattime(monkeypatch):
    fake = FakeBeatTime()
    monkeypatch.setattr(proof, "BASE_URL", fake.url)
    monkeypatch.setattr(proof, "PINNED_KEYS", ({"public_key": fake.public_b64, "active_from": "2026-09-21"},))
    yield fake
    fake.server.shutdown()


def _sealed(folder, beattime):
    proof.seal_version(folder, ENTRIES, proof.BeatTimeClient())
    for other in range(5):  # inne znaczniki tygodnia — drzewo tygodnia ma kilka poziomów
        beattime.digests.append(hashlib.sha256(bytes([other])).hexdigest())
    beattime.close_week()
    assert proof.refresh(folder, proof.BeatTimeClient()).status == "signed"


# ------------------------------------------------------------------- drzewo


@pytest.mark.parametrize("count", [*range(1, 18), 64, 65, 1000])
def test_every_leaf_folds_to_the_root(count):
    leaves = [hashlib.sha256(str(i).encode()).digest() for i in range(count)]
    root = fileproof.merkle_root(leaves)
    for index in range(count):
        assert fileproof.fold(leaves[index], fileproof.merkle_path(leaves, index)) == root, (count, index)
    assert len(fileproof.merkle_path(leaves, count - 1)) <= count.bit_length()


def test_leaf_and_node_cannot_be_confused():
    leaf = fileproof.leaf(bytes(32), "a" * 64, 1, bytes(32))
    assert leaf != fileproof.node(bytes(32), bytes(32))
    with pytest.raises(ValueError):
        fileproof.leaf(bytes(31), "a" * 64, 1, bytes(32))


def test_salt_hides_files_between_versions():
    """Ta sama zawartość w dwóch wersjach daje inne liście — z dowodu nie da się zgadywać plików."""
    assert fileproof.files_root(ENTRIES, bytes(32)) != fileproof.files_root(ENTRIES, bytes([1]) * 32)
    assert fileproof.files_root(ENTRIES, bytes(32)) == fileproof.files_root(list(reversed(ENTRIES)), bytes(32))


def test_statement_round_trip_and_garbage():
    text = fileproof.statement("a" * 64, "b" * 64, 5)
    assert fileproof.parse_statement(text) == {"index": "a" * 64, "root": "b" * 64, "files": 5}
    for bad in (b"", text + b"x", text.replace(b"files 5", b"files 05"), text.replace(b"1\n", b"2\n", 1),
                text.replace(b"a" * 64, b"A" * 64), fileproof.statement("a" * 64, "b" * 64, 0)):
        assert fileproof.parse_statement(bad) is None, bad


# ------------------------------------------------------------ pieczęć wersji


def test_seal_covers_statement_with_index_and_tree(tmp_path, beattime):
    seal = proof.seal_version(tmp_path, ENTRIES, proof.BeatTimeClient())
    statement = (tmp_path / proof.STATEMENT_NAME).read_bytes()
    parsed = fileproof.parse_statement(statement)
    assert seal.digest == hashlib.sha256(statement).hexdigest(), "do Sigelith idzie skrót oświadczenia"
    assert parsed["index"] == hashlib.sha256((tmp_path / proof.INDEX_NAME).read_bytes()).hexdigest()
    assert parsed["root"] == seal.files_root and parsed["files"] == len(ENTRIES)
    assert beattime.digests == [seal.digest], "nazwy i sumy plików nie opuszczają komputera"
    assert json.loads((tmp_path / proof.SEAL_NAME).read_text(encoding="utf-8"))["format"] == "tvb-seal/2"
    assert proof.check(tmp_path, ENTRIES).index_matches


def test_check_catches_a_changed_file_behind_the_tree(tmp_path, beattime):
    _sealed(tmp_path, beattime)
    assert proof.check(tmp_path, ENTRIES).proven
    changed = [*ENTRIES[:-1], ("notatka.txt", 7, hashlib.sha256(b"inna").hexdigest())]
    assert not proof.check(tmp_path, changed).proven
    statement = tmp_path / proof.STATEMENT_NAME
    statement.write_bytes(statement.read_bytes().replace(b"files 5", b"files 6"))
    assert not proof.check(tmp_path).index_matches


def test_seals_from_before_3_0_still_check(tmp_path, beattime):
    """Wersje oznakowane przez Time Vault Backup 2.x: znacznik obejmuje sam spis."""
    index = proof.version_index(ENTRIES)
    (tmp_path / proof.INDEX_NAME).write_bytes(index)
    seal = proof.Seal(digest=proof.digest_of(index))
    proof._stamp(seal, proof.BeatTimeClient())
    raw = seal.to_dict()
    assert raw["format"] == "tvb-seal/1" and "salt_seed" not in raw
    (tmp_path / proof.SEAL_NAME).write_text(json.dumps(raw), encoding="utf-8")
    beattime.close_week()
    proof.refresh(tmp_path, proof.BeatTimeClient())
    assert proof.check(tmp_path, ENTRIES).proven
    with pytest.raises(fileproof.FileProofError, match=r"sprzed wersji 3.0"):
        fileproof.build(tmp_path, "notatka.txt")


# ------------------------------------------------------------ dowód pliku


def test_file_proof_verifies_and_reveals_nothing_else(tmp_path, beattime):
    _sealed(tmp_path, beattime)
    doc = fileproof.build(tmp_path, "Dokumenty/umowa.pdf")
    sha, size = hashlib.sha256(b"umowa").hexdigest(), 1234
    assert fileproof.problems(doc, sha, size) == []
    assert doc["file"] == {"name": "umowa.pdf", "size": size, "sha256": sha, "path": "Dokumenty/umowa.pdf"}
    text = json.dumps(doc)
    for key, _size, other_sha in ENTRIES[1:]:
        assert key not in text and other_sha not in text, key
    assert "salt_seed" not in text and json.loads(
        (tmp_path / proof.SEAL_NAME).read_text(encoding="utf-8"))["salt_seed"] not in text

    assert fileproof.problems(doc, hashlib.sha256(b"podmieniona").hexdigest(), size), "inny plik"
    assert fileproof.problems(doc, sha, size + 1), "inny rozmiar"


def test_file_proof_without_path(tmp_path, beattime):
    _sealed(tmp_path, beattime)
    doc = fileproof.build(tmp_path, "Tajne/haslo-do-sejfu.txt", include_path=False)
    assert "path" not in doc["file"] and "Tajne" not in json.dumps(doc)
    assert fileproof.problems(doc) == []


@pytest.mark.parametrize("damage", ["path", "step", "root", "statement", "beatproof", "salt", "format"])
def test_every_kind_of_tampering_is_detected(tmp_path, beattime, damage):
    _sealed(tmp_path, beattime)
    doc = fileproof.build(tmp_path, "Zdjecia/2026/lato.jpg")
    if damage == "path":
        doc["file"]["path"] = "Zdjecia/2025/lato.jpg"
    elif damage == "step":
        doc["merkle_path"][0]["hash"] = "0" * 64
    elif damage == "root":
        doc["files_root"] = "1" * 64
    elif damage == "statement":
        doc["statement"] = doc["statement"].replace("files 5", "files 4")
    elif damage == "beatproof":
        doc["beatproof"]["week_root"] = "2" * 64
    elif damage == "salt":
        doc["leaf"]["salt"] = "3" * 64
    else:
        doc["format"] = "beatproof-v1"
    assert fileproof.problems(doc), damage


def test_no_proof_before_the_week_is_signed(tmp_path, beattime):
    proof.seal_version(tmp_path, ENTRIES, proof.BeatTimeClient())
    with pytest.raises(fileproof.FileProofError, match="podpis tygodnia"):
        fileproof.build(tmp_path, "notatka.txt")


def test_unknown_file_is_refused(tmp_path, beattime):
    _sealed(tmp_path, beattime)
    with pytest.raises(fileproof.FileProofError, match="nie ma w spisie"):
        fileproof.build(tmp_path, "Dokumenty/nie-ma.pdf")


def test_seal_folder_is_where_the_stored_copy_lies(tmp_path):
    version = tmp_path / "2026-09-30_@521"  # nazwa wersji z engine._VERSION_NAME
    item = browse.Item("umowa.pdf", "Dokumenty/umowa.pdf", False, stored=version / "Dokumenty" / "umowa.pdf")
    assert browse.seal_folder(tmp_path, item) == version
    mirror = browse.Item("umowa.pdf", "Dokumenty/umowa.pdf", False, stored=tmp_path / "Dokumenty" / "umowa.pdf")
    assert browse.seal_folder(tmp_path, mirror) == tmp_path


def test_certificate_pdf_is_written(tmp_path, beattime):
    from PySide6.QtWidgets import QApplication

    from cleanvault.ui import proof_pdf

    QApplication.instance() or QApplication([])
    _sealed(tmp_path, beattime)
    doc = fileproof.build(tmp_path, "Dokumenty/umowa.pdf")
    html = proof_pdf.certificate_html(doc, "umowa.pdf.sigelith-proof")
    assert "umowa.pdf" in html and doc["file"]["sha256"] in html and "faktura" not in html
    target = proof_pdf.write_certificate(doc, tmp_path / "dowod.pdf", "umowa.pdf.sigelith-proof")
    assert target.read_bytes().startswith(b"%PDF") and target.stat().st_size > 5000
