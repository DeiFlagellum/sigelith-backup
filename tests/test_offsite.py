"""Kopia poza domem: migawki w usłudze zgodnej z S3."""

from __future__ import annotations

import datetime
import hashlib
import os
import random
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))

from fake_s3 import FakeS3

from cleanvault import chunks, crypto, offsite, s3
from cleanvault.crypto import KdfParams, PasswordKeyring
from cleanvault.snapshot import SourceRoot

pytestmark = pytest.mark.skipif(not chunks.AVAILABLE, reason="brak skompilowanego FastCDC")

PASSWORD = "Hasło-chmury-2026"
SECRET = "sekret-dostępu"


@pytest.fixture(autouse=True)
def small_pieces(monkeypatch):
    monkeypatch.setattr(offsite, "SINGLE_CHUNK_LIMIT", 256 * 1024)
    monkeypatch.setattr(chunks, "MIN_CHUNK", 16 * 1024)
    monkeypatch.setattr(chunks, "AVG_CHUNK", 64 * 1024)
    monkeypatch.setattr(chunks, "MAX_CHUNK", 256 * 1024)
    monkeypatch.setattr(chunks, "WINDOW", 1024 * 1024)


@pytest.fixture()
def server():
    with FakeS3() as fake:
        yield fake


@pytest.fixture()
def client(server):
    target = s3.S3Target(endpoint=server.endpoint, region="eu-central-003", bucket="kubel",
                         access_key="AKIATEST", prefix="dom")
    return s3.S3Client(target, SECRET)


@pytest.fixture()
def source(tmp_path):
    root = tmp_path / "Dokumenty"
    (root / "pod").mkdir(parents=True)
    (root / "list.txt").write_text("Poufna treść listu — zażółć gęślą jaźń", encoding="utf-8")
    (root / "pod" / "duzy.bin").write_bytes(random.Random(1).randbytes(2 * 1024 * 1024))
    (root / "pusty.txt").write_bytes(b"")
    return root


def keyring(password: str = PASSWORD) -> PasswordKeyring:
    return PasswordKeyring(password, KdfParams(crypto.KDF_PBKDF2_SHA256, os.urandom(16), 1000))


def roots_of(source):
    return [SourceRoot.make(str(source))]


def _files(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}


def test_upload_and_restore_round_trip(tmp_path, source, client):
    result = offsite.upload(roots_of(source), [], client, keyring())
    assert result.ok and result.files == 3 and result.stamp

    target = tmp_path / "z-chmury"
    restored, errors = offsite.restore(client, keyring(), result.stamp, target)
    assert not errors and restored == 3
    assert _files(target / source.name) == _files(source)


def test_nothing_readable_is_stored_in_the_cloud(source, client, server):
    offsite.upload(roots_of(source), [], client, keyring())
    secret_text = "Poufna treść listu".encode()
    big_start = (source / "pod" / "duzy.bin").read_bytes()[:4096]
    plain_by_design = ("config.json", "HOW TO RECOVER.txt", "odzyskaj.py")  # bez danych użytkownika
    for key, (data, _when) in server.objects.items():
        if key.endswith(plain_by_design):
            assert secret_text not in data and b"list.txt" not in data
            continue
        assert data[:4] == crypto.MAGIC, f"{key} nie jest zaszyfrowany"
        assert secret_text not in data and big_start not in data
        assert "list.txt" not in key and "Dokumenty" not in key
    plain_ids = {hashlib.sha256((source / "list.txt").read_bytes()).hexdigest()}
    assert not any(key.rsplit("/", 1)[-1] in plain_ids for key in server.objects)


def test_second_upload_sends_only_changes(source, client):
    offsite.upload(roots_of(source), [], client, keyring())
    (source / "list.txt").write_text("Zmieniona treść listu", encoding="utf-8")
    second = offsite.upload(roots_of(source), [], client, keyring(), now=first_time_plus(60))
    assert second.ok
    assert second.files == 1 and second.reused == 2
    assert second.uploaded_chunks <= 3, "wysłano więcej niż zmieniony plik i fragment spisu"
    assert len(offsite.list_snapshots(client)) == 2


def first_time_plus(seconds: float) -> float:
    import time

    return time.time() + seconds


def test_wrong_password_is_refused(source, client):
    offsite.upload(roots_of(source), [], client, keyring())
    with pytest.raises(offsite.OffsiteError):
        offsite.RemoteStore(client, keyring("zupełnie inne hasło"))


def test_prune_keeps_recent_snapshots_and_shared_chunks(tmp_path, source, client, server):
    stamps = []
    rng = random.Random(4)
    for index in range(3):
        (source / "pod" / "duzy.bin").write_bytes(rng.randbytes(1024 * 1024))
        result = offsite.upload(roots_of(source), [], client, keyring(), now=first_time_plus(index * 100))
        stamps.append(result.stamp)
    before = {k for k in server.objects if "/chunks/" in k}

    deleted, removed = offsite.prune(client, keyring(), keep=1, now=first_time_plus(3 * 86400))
    assert deleted == 2 and removed > 0
    assert offsite.list_snapshots(client) == [stamps[-1]]
    after = {k for k in server.objects if "/chunks/" in k}
    assert after < before

    target = tmp_path / "z-chmury"
    restored, errors = offsite.restore(client, keyring(), stamps[-1], target)
    assert not errors and restored == 3
    assert _files(target / source.name) == _files(source)


def test_prune_never_removes_fresh_chunks(source, client):
    for index in range(2):
        (source / "list.txt").write_text(f"wersja {index}", encoding="utf-8")
        offsite.upload(roots_of(source), [], client, keyring(), now=first_time_plus(index * 100))
    _deleted, removed = offsite.prune(client, keyring(), keep=1)
    assert removed == 0, "fragmenty młodsze niż doba mogą należeć do migawki w drodze"


def test_client_retries_when_the_service_is_busy(source, client, server, monkeypatch):
    monkeypatch.setattr(s3.time, "sleep", lambda _s: None)
    server.fail_next = 2
    result = offsite.upload(roots_of(source), [], client, keyring())
    assert result.ok


def test_listing_follows_continuation_tokens(client, server):
    server.page_size = 3
    for index in range(10):
        client.put(f"lista/{index:02}", b"x")
    names = [name for name, _size in client.list("lista/")]
    assert names == [f"lista/{index:02}" for index in range(10)]


def test_rejected_credentials_are_reported(server):
    target = s3.S3Target(endpoint=server.endpoint, region="x", bucket="kubel", access_key="INNY")
    with pytest.raises(s3.S3Error) as caught:
        s3.S3Client(target, SECRET).get("cokolwiek")
    assert caught.value.status == 403 and caught.value.code == "InvalidAccessKeyId"


def test_check_writes_reads_and_removes_a_probe(client, server):
    client.check()
    assert not server.objects


def test_restore_refuses_paths_outside_the_target(tmp_path, source, client):
    key = keyring()
    store = offsite.RemoteStore(client, key, create=True)
    snapshot = offsite.Snapshot(stamp="2026-09-27_@500", created=0.0, roots={})
    data = b"zlosliwy plik"
    cid = store.chunk_id(data)
    store.put(cid, data)
    snapshot.files["../poza.txt"] = offsite.FileRecord(len(data), 0.0, hashlib.sha256(data).hexdigest(), [(cid, len(data))])
    offsite._save_snapshot(client, store, snapshot, set())

    restored, errors = offsite.restore(client, key, "2026-09-27_@500", tmp_path / "cel")
    assert restored == 0 and errors
    assert not (tmp_path / "poza.txt").exists()


def test_signature_matches_botocore():
    """Podpis SigV4 porównany z oficjalną biblioteką AWS dla tych samych żądań."""
    botocore_auth = pytest.importorskip("botocore.auth")
    from urllib.parse import quote

    from botocore.awsrequest import AWSRequest
    from botocore.credentials import Credentials

    original = botocore_auth.get_current_datetime
    botocore_auth.get_current_datetime = lambda: datetime.datetime(2026, 9, 27, 10, 15, 0)
    try:
        creds = Credentials("AKIAIOSFODNN7EXAMPLE", "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY")
        host = "s3.eu-central-003.backblazeb2.com"
        cases = [
            ("PUT", "/kubel/dom/chunks/ab/abcdef", {}, b"tresc fragmentu"),
            ("GET", "/kubel/", {"list-type": "2", "prefix": "dom/chunks/", "continuation-token": "1a/b+c=="}, b""),
            ("DELETE", "/kubel/dom/plik ze spacją+ąę.txt", {}, b""),
            ("HEAD", "/kubel/dom/a~b_c-d.e", {}, b""),
        ]
        for method, path, query, body in cases:
            payload = hashlib.sha256(body).hexdigest()
            mine = s3.sign(method, host, path, query,
                           {"x-amz-content-sha256": payload, "x-amz-date": "20260927T101500Z"},
                           payload, creds.access_key, creds.secret_key, "eu-central-003", "20260927T101500Z")
            url = f"https://{host}{quote(path, safe='/-_.~')}"
            if query:
                url += "?" + "&".join(f"{quote(k, safe='-_.~')}={quote(v, safe='-_.~')}" for k, v in sorted(query.items()))
            request = AWSRequest(method=method, url=url, data=body, headers={"x-amz-content-sha256": payload})
            botocore_auth.S3SigV4Auth(creds, "s3", "eu-central-003").add_auth(request)
            assert mine == request.headers["Authorization"], (method, path)
    finally:
        botocore_auth.get_current_datetime = original


def test_downloaded_bucket_is_recoverable_without_the_program(tmp_path, source, client, server):
    """Scenariusz, dla którego ta kopia istnieje: dysk i komputer przepadły.

    Kubełek pobrany dowolnym narzędziem S3 do folderu, a potem sam skrypt
    ratunkowy z tego folderu — osobny proces, bez modułów programu.
    """
    import subprocess

    from cleanvault import rescue

    result = offsite.upload(roots_of(source), [], client, keyring())
    downloaded = tmp_path / "pobrane"
    for key, (data, _when) in server.objects.items():
        rel = key.split("/", 1)[1]  # bez folderu w kubełku („dom/…”)
        target = downloaded / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    assert (downloaded / rescue.SCRIPT_NAME).is_file(), "skrypt ratunkowy musi leżeć w kubełku"
    assert "pip install pycryptodomex" in (downloaded / "JAK ODZYSKAC DANE - HOW TO RECOVER.txt").read_text(
        encoding="utf-8")

    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH",)}
    env["TVB_PASSWORD"] = PASSWORD
    done = subprocess.run(
        [sys.executable, "-I", str(downloaded / rescue.SCRIPT_NAME), str(downloaded), str(tmp_path / "cel")],
        capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=120,
    )
    assert done.returncode == 0, done.stdout + done.stderr
    assert result.stamp in done.stdout
    assert _files(tmp_path / "cel" / source.name) == _files(source)

