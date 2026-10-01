"""Testy warstwy kryptograficznej."""

from __future__ import annotations

import os
import time

import pytest

from cleanvault import crypto
from cleanvault.crypto import (
    IntegrityError,
    KdfParams,
    PasswordKeyring,
    UnsupportedFormatError,
)


@pytest.fixture()
def keyring() -> PasswordKeyring:
    # PBKDF2 z małą liczbą iteracji, żeby testy nie trwały minutami.
    return PasswordKeyring("Poprawne-Hasło-123", KdfParams(crypto.KDF_PBKDF2_SHA256, b"0" * 16, 1000))


def test_roundtrip_preserves_bytes(tmp_path, keyring):
    src = tmp_path / "dane.bin"
    payload = os.urandom(3 * 1024 * 1024 + 17)  # kilka porcji + reszta
    src.write_bytes(payload)

    enc = tmp_path / "dane.cvlt"
    dec = tmp_path / "odzyskane.bin"
    crypto.encrypt_file(src, enc, keyring)
    crypto.decrypt_file(enc, dec, keyring)

    assert dec.read_bytes() == payload


def test_empty_file_roundtrip(tmp_path, keyring):
    src = tmp_path / "pusty.txt"
    src.write_bytes(b"")
    enc, dec = tmp_path / "p.cvlt", tmp_path / "p.out"
    crypto.encrypt_file(src, enc, keyring)
    crypto.decrypt_file(enc, dec, keyring)
    assert dec.read_bytes() == b""


def test_container_is_not_bloated(tmp_path, keyring):
    """Stary format (JSON + base64) puchł o ~33%. Nowy dokłada stały narzut."""
    src = tmp_path / "dane.bin"
    src.write_bytes(os.urandom(1_000_000))
    enc = tmp_path / "dane.cvlt"
    written = crypto.encrypt_file(src, enc, keyring)
    overhead = written - 1_000_000
    assert 0 < overhead < 128, f"narzut kontenera wynosi {overhead} B"


def test_wrong_password_is_rejected(tmp_path, keyring):
    src = tmp_path / "tajne.txt"
    src.write_bytes(b"zawartosc")
    enc = tmp_path / "tajne.cvlt"
    crypto.encrypt_file(src, enc, keyring)

    wrong = PasswordKeyring("Złe-Hasło", KdfParams(crypto.KDF_PBKDF2_SHA256, b"0" * 16, 1000))
    with pytest.raises(IntegrityError):
        crypto.decrypt_file(enc, tmp_path / "out.txt", wrong)


def test_failed_decryption_leaves_no_plaintext(tmp_path, keyring):
    """Niezweryfikowany plaintext nie może trafić pod docelową nazwę."""
    src = tmp_path / "tajne.txt"
    src.write_bytes(b"x" * 200_000)
    enc = tmp_path / "tajne.cvlt"
    crypto.encrypt_file(src, enc, keyring)

    wrong = PasswordKeyring("Złe-Hasło", KdfParams(crypto.KDF_PBKDF2_SHA256, b"0" * 16, 1000))
    out = tmp_path / "wyciek.txt"
    with pytest.raises(IntegrityError):
        crypto.decrypt_file(enc, out, wrong)

    assert not out.exists(), "plik docelowy powstał mimo nieudanej weryfikacji"
    assert not (tmp_path / "wyciek.txt.part").exists(), "plik tymczasowy nie został posprzątany"


def test_tampered_ciphertext_is_detected(tmp_path, keyring):
    src = tmp_path / "dane.bin"
    src.write_bytes(os.urandom(50_000))
    enc = tmp_path / "dane.cvlt"
    crypto.encrypt_file(src, enc, keyring)

    blob = bytearray(enc.read_bytes())
    blob[len(blob) // 2] ^= 0xFF
    enc.write_bytes(bytes(blob))

    with pytest.raises(IntegrityError):
        crypto.decrypt_file(enc, tmp_path / "out.bin", keyring)


def test_tampered_header_is_detected(tmp_path, keyring):
    """Nagłówek jest uwierzytelniony jako AAD — podmiana musi unieważnić tag."""
    src = tmp_path / "dane.bin"
    src.write_bytes(os.urandom(10_000))
    enc = tmp_path / "dane.cvlt"
    crypto.encrypt_file(src, enc, keyring)

    blob = bytearray(enc.read_bytes())
    header = crypto.peek_header(enc)
    blob[header.size - 1] ^= 0x01  # ostatni bajt nagłówka: deklarowany rozmiar
    enc.write_bytes(bytes(blob))

    with pytest.raises((IntegrityError, UnsupportedFormatError)):
        crypto.decrypt_file(enc, tmp_path / "out.bin", keyring)


def test_foreign_file_is_rejected(tmp_path, keyring):
    alien = tmp_path / "zwykly.txt"
    alien.write_bytes(b"to nie jest kontener CleanVault")
    with pytest.raises(UnsupportedFormatError):
        crypto.decrypt_file(alien, tmp_path / "out", keyring)


def test_detects_container_by_signature_not_extension(tmp_path, keyring):
    src = tmp_path / "a.txt"
    src.write_bytes(b"tresc")
    enc = tmp_path / "bez_rozszerzenia"
    crypto.encrypt_file(src, enc, keyring)
    assert crypto.is_encrypted_file(enc)
    assert not crypto.is_encrypted_file(src)


def test_verify_file_accepts_good_and_rejects_bad(tmp_path, keyring):
    src = tmp_path / "a.bin"
    src.write_bytes(os.urandom(20_000))
    enc = tmp_path / "a.cvlt"
    crypto.encrypt_file(src, enc, keyring)
    assert crypto.verify_file(enc, keyring) == 20_000

    blob = bytearray(enc.read_bytes())
    blob[-1] ^= 0xFF  # psujemy tag
    enc.write_bytes(bytes(blob))
    with pytest.raises(IntegrityError):
        crypto.verify_file(enc, keyring)


def test_each_file_gets_unique_nonce(tmp_path, keyring):
    """Powtórzony nonce przy współdzielonym kluczu łamie GCM całkowicie."""
    src = tmp_path / "a.txt"
    src.write_bytes(b"identyczna tresc")
    nonces = set()
    for i in range(25):
        out = tmp_path / f"{i}.cvlt"
        crypto.encrypt_file(src, out, keyring)
        nonces.add(crypto.peek_header(out).nonce)
    assert len(nonces) == 25


def test_key_is_derived_once_per_session():
    """Regresja wydajności: 1.x liczyło KDF osobno dla każdego pliku.

    Przy 10 000 plików i 100 000 iteracjach oznaczało to godziny samego KDF.
    """
    params = KdfParams(crypto.KDF_PBKDF2_SHA256, os.urandom(16), 200_000)
    ring = PasswordKeyring("hasło", params)

    first_start = time.perf_counter()
    key_a = ring.key_for(params)
    first = time.perf_counter() - first_start

    cached_start = time.perf_counter()
    for _ in range(50):
        key_b = ring.key_for(params)
    cached = time.perf_counter() - cached_start

    assert key_a == key_b
    assert cached < first, "50 odczytów z cache musi być tańsze niż jedno wyprowadzenie klucza"


def test_argon2_is_the_default_when_available():
    if not crypto.ARGON2_AVAILABLE:
        pytest.skip("argon2-cffi niedostępne w tym środowisku")
    params = KdfParams.new_default()
    assert params.kdf_id == crypto.KDF_ARGON2ID
    assert params.b >= 19 * 1024, "pamięć Argon2 poniżej rekomendacji OWASP"


def test_pbkdf2_fallback_uses_sha256_and_strong_count():
    """1.x używało PBKDF2 z domyślnym PRF = HMAC-SHA1 i 100k iteracji."""
    assert crypto.PBKDF2_ITERATIONS >= 600_000
    params = KdfParams(crypto.KDF_PBKDF2_SHA256, b"s" * 16, crypto.PBKDF2_ITERATIONS)
    assert "SHA256" in params.algorithm_name


def test_empty_password_is_refused():
    with pytest.raises(ValueError):
        PasswordKeyring("")


def test_cancel_stops_encryption_and_cleans_up(tmp_path, keyring):
    src = tmp_path / "duzy.bin"
    src.write_bytes(os.urandom(5 * 1024 * 1024))
    enc = tmp_path / "duzy.cvlt"

    calls = {"n": 0}

    def cancel() -> bool:
        calls["n"] += 1
        return calls["n"] > 2

    with pytest.raises(crypto.OperationCancelled):
        crypto.encrypt_file(src, enc, keyring, cancel=cancel)
    assert not enc.exists()
    assert not (tmp_path / "duzy.cvlt.part").exists()
