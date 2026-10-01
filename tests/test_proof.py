"""Znakowanie wersji czasem przez BeatTime.

Lokalny serwer odtwarza zachowanie prawdziwego API (sprawdzone w kodzie usługi):
znacznik zapisuje się od razu, a korzeń drzewa Merkle'a tygodnia z podpisem
Ed25519 pojawia się dopiero po zamknięciu tygodnia. Osobny test sprawdza nasz
kod na prawdziwym, opublikowanym podpisie BeatTime — bez łączenia się z siecią.
"""

from __future__ import annotations

import base64
import hashlib
import json
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
from Cryptodome.PublicKey import ECC
from Cryptodome.Signature import eddsa

from cleanvault import engine, proof
from cleanvault.engine import BackupConfig, Reporter

#: Publiczne dane z https://beattime.live/api/proof/root/latest (tydzień 2026-W38).
REAL_WEEK = "2026-W38"
REAL_ROOT = "731921cf38dd24474ddd4719489c969999334761ddaa4c60c2534cab674b5c3e"
REAL_SIGNATURE = "4LPISwR0HVVr0aPS0hUDZAXODdapISPKCI4PQ8dvXj9dsaDpl5b9yKFwr92mOng0Z6AV+hJsKzJ/L18b8dqyAw=="


class FakeBeatTime:
    """Serwer z tym samym kształtem odpowiedzi co apps/tsa/views.py:_payload."""

    def __init__(self) -> None:
        self.key = ECC.generate(curve="ed25519")
        self.public_b64 = base64.b64encode(self.key.public_key().export_key(format="raw")).decode()
        self.digests: list[str] = []
        self.closed = False
        self.root = ""
        self.signature = ""
        fake = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args):
                pass

            def _json(self, status, body):
                data = json.dumps(body).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                digest = str(body.get("digest", "")).lower()
                created = digest not in fake.digests
                if created:
                    fake.digests.append(digest)
                self._json(201 if created else 200, {**fake.payload(digest), "created": created})

            def do_GET(self):
                query = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
                digest = query.get("digest", [""])[0]
                if digest not in fake.digests:
                    self._json(200, {"found": False, "digest": digest})
                else:
                    self._json(200, fake.payload(digest))

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.server.server_address[1]}"

    def leaves(self):
        return [hashlib.sha256(b"\x00" + bytes.fromhex(d)).digest() for d in self.digests]

    def close_week(self) -> None:
        level = self.leaves()
        while len(level) > 1:
            level = [
                hashlib.sha256(b"\x01" + level[i] + level[i + 1]).digest() if i + 1 < len(level) else level[i]
                for i in range(0, len(level), 2)
            ]
        self.root = level[0].hex()
        message = f"beattime-proof-v1|2026-W39|{self.root}".encode()
        self.signature = base64.b64encode(eddsa.new(self.key, "rfc8032").sign(message)).decode()
        self.closed = True

    def proof_for(self, digest):
        level, index, path = self.leaves(), self.digests.index(digest), []
        while len(level) > 1:
            nxt = []
            for i in range(0, len(level), 2):
                if i + 1 < len(level):
                    if i == index:
                        path.append({"side": "R", "hash": level[i + 1].hex()})
                    elif i + 1 == index:
                        path.append({"side": "L", "hash": level[i].hex()})
                    nxt.append(hashlib.sha256(b"\x01" + level[i] + level[i + 1]).digest())
                else:
                    nxt.append(level[i])
            index //= 2
            level = nxt
        return path

    def payload(self, digest):
        body = {"found": True, "digest": digest, "beat": "@512.34", "utc": "2026-09-27T12:17:00Z",
                "seq": self.digests.index(digest) + 1, "week": "2026-W39", "week_closed": self.closed}
        if self.closed:
            body.update(week_root=self.root, root_signature=self.signature, public_key=self.public_b64,
                        inclusion_proof=self.proof_for(digest), ots_status="pending")
        return body


@pytest.fixture()
def beattime(monkeypatch):
    fake = FakeBeatTime()
    monkeypatch.setattr(proof, "BASE_URL", fake.url)
    monkeypatch.setattr(proof, "PINNED_KEYS", ({"public_key": fake.public_b64, "active_from": "2026-09-21"},))
    yield fake
    fake.server.shutdown()


ENTRIES = [("Dokumenty/b.txt", 3, "b" * 64), ("Dokumenty/a.txt", 5, "a" * 64)]


def test_real_beattime_signature_is_accepted():
    """Prawdziwy podpis korzenia tygodnia 2026-W38 i klucz przypięty w programie."""
    assert proof.verify_signature(REAL_WEEK, REAL_ROOT, REAL_SIGNATURE)
    assert not proof.verify_signature(REAL_WEEK, "0" * 64, REAL_SIGNATURE)
    assert not proof.verify_signature("2026-W37", REAL_ROOT, REAL_SIGNATURE)


def test_index_is_canonical():
    assert proof.version_index(ENTRIES) == proof.version_index(list(reversed(ENTRIES)))
    assert proof.version_index(ENTRIES).decode().splitlines()[1].startswith("Dokumenty/a.txt\t5\t")


def test_seal_then_signature_after_the_week_closes(tmp_path, beattime):
    seal = proof.seal_version(tmp_path, ENTRIES, proof.BeatTimeClient())
    assert seal.status == "stamped"
    # Od 3.0 oznakowane jest oświadczenie pieczęci: suma spisu wersji + korzeń drzewa plików.
    statement = (tmp_path / proof.STATEMENT_NAME).read_bytes()
    assert seal.digest == hashlib.sha256(statement).hexdigest()
    assert statement.decode().splitlines()[1] == (
        "index-sha256 " + hashlib.sha256((tmp_path / proof.INDEX_NAME).read_bytes()).hexdigest())
    early = proof.check(tmp_path, ENTRIES)
    assert early.index_matches and early.stamped and not early.proven  # podpis jeszcze nie istnieje

    for other in range(4):  # inne znaczniki tego tygodnia — drzewo ma kilka poziomów
        beattime.digests.append(hashlib.sha256(bytes([other])).hexdigest())
    beattime.close_week()
    refreshed = proof.refresh(tmp_path, proof.BeatTimeClient())
    assert refreshed.status == "signed"
    final = proof.check(tmp_path, ENTRIES)
    assert final.inclusion_ok and final.signature_ok and final.proven, final.problems


def test_tampering_is_detected(tmp_path, beattime):
    proof.seal_version(tmp_path, ENTRIES, proof.BeatTimeClient())
    beattime.close_week()
    proof.refresh(tmp_path, proof.BeatTimeClient())

    changed = [*ENTRIES[:1], ("Dokumenty/a.txt", 5, "c" * 64)]
    assert not proof.check(tmp_path, changed).proven
    index = tmp_path / proof.INDEX_NAME
    index.write_bytes(index.read_bytes().replace(b"aaaa", b"dddd", 1))
    assert not proof.check(tmp_path).index_matches


def test_signature_by_another_key_is_rejected(tmp_path, beattime, monkeypatch):
    proof.seal_version(tmp_path, ENTRIES, proof.BeatTimeClient())
    beattime.close_week()
    proof.refresh(tmp_path, proof.BeatTimeClient())
    stranger = base64.b64encode(ECC.generate(curve="ed25519").public_key().export_key(format="raw")).decode()
    monkeypatch.setattr(proof, "PINNED_KEYS", ({"public_key": stranger, "active_from": "2026-09-21"},))
    result = proof.check(tmp_path, ENTRIES)
    assert result.signature_ok is False and not result.proven


def test_no_network_leaves_a_pending_seal(tmp_path, monkeypatch):
    monkeypatch.setattr(proof, "BASE_URL", "http://127.0.0.1:9")  # nic tu nie słucha
    seal = proof.seal_version(tmp_path, ENTRIES, proof.BeatTimeClient(timeout=2))
    assert seal.status == "pending" and seal.error
    assert "czeka" in proof.check(tmp_path).problems[0]


def test_backup_seals_the_version_and_refreshes_older_ones(tmp_path, beattime):
    source = tmp_path / "Dokumenty"
    source.mkdir()
    (source / "umowa.txt").write_text("treść umowy", encoding="utf-8")
    destination = tmp_path / "kopia"

    def backup():
        config = BackupConfig(sources=[str(source)], destination=str(destination), structure="dated",
                              excludes=[], stamp_updates=False, catchup_passes=0, timestamp=True)
        plan = engine.plan_backup(config, Reporter())
        return plan, engine.run_backup(plan, None, Reporter())

    first, result = backup()
    assert result.ok
    folder = destination / first.version
    entries = [(f"{source.name}/umowa.txt", 13, hashlib.sha256("treść umowy".encode()).hexdigest())]
    assert proof.check(folder, entries).stamped

    beattime.close_week()
    (source / "umowa.txt").write_text("treść umowy, wersja 2", encoding="utf-8")
    import time

    time.sleep(0.05)
    second, _ = backup()
    assert second.version != first.version
    assert proof.read_seal(folder).status == "signed", "starsza wersja dostała podpis tygodnia"


def test_pending_seal_is_sent_with_the_next_backup(tmp_path, beattime, monkeypatch):
    working_url = proof.BASE_URL
    monkeypatch.setattr(proof, "BASE_URL", "http://127.0.0.1:9")
    proof.seal_version(tmp_path, ENTRIES, proof.BeatTimeClient(timeout=2))
    monkeypatch.setattr(proof, "BASE_URL", working_url)
    assert proof.refresh(tmp_path, proof.BeatTimeClient()).status == "stamped"
