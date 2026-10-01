#!/usr/bin/env python3
"""Odzyskiwanie danych z kopii Sigelith Backup — bez samego programu.

Recover files from a Sigelith Backup copy — without the program itself.

Ten plik leży w katalogu kopii celowo: program może kiedyś zniknąć, komputer
może się zepsuć, a kopia ma dać się odczytać mimo to. Skrypt potrzebuje tylko
Pythona 3.8+ i — dla kopii zaszyfrowanej — dwóch bibliotek:

    pip install pycryptodomex argon2-cffi

(zamiast pycryptodomex zadziała też biblioteka ``cryptography``).

Użycie / usage::

    python odzyskaj.py KATALOG_KOPII KATALOG_DOCELOWY

KATALOG_KOPII to folder wersji (np. ``2026-09-27_@512``), dowolny jego podfolder
albo pojedynczy plik ``.cvlt``. Pliki niezaszyfrowane są kopiowane bez zmian,
zaszyfrowane — odszyfrowywane (hasło padnie raz, na początku). Żaden plik
w kopii nie jest zmieniany. Hasło można też podać w zmiennej środowiskowej
``TVB_PASSWORD`` (np. przy odzyskiwaniu skryptem) / the password may also be
given in the ``TVB_PASSWORD`` environment variable.

Format pliku .cvlt (liczby big-endian)::

    magic 4B "CVLT" | wersja 1B (=1) | kdf 1B (1=Argon2id, 2=PBKDF2-SHA256)
    flagi 1B | dł. soli 1B | sól | dł. nonce 1B | nonce | kdf_a 4B | kdf_b 4B
    kdf_c 4B | rozmiar jawny 8B | szyfrogram (rozmiar jawny B) | tag GCM 16B

Klucz (32 B): Argon2id(hasło, sól, t=kdf_a, pamięć=kdf_b KiB, p=kdf_c) albo
PBKDF2-HMAC-SHA256(hasło, sól, iteracje=kdf_a). Szyfr: AES-256-GCM, a cały
nagłówek (od "CVLT" do rozmiaru jawnego) jest danymi uwierzytelnianymi (AAD).

Duże pliki (od 256 MB) mogą być zapisane fragmentami. W folderze wersji leży
wtedy przepis ``nazwa.cvrecipe`` (``nazwa.cvrecipe.cvlt`` w kopii szyfrowanej):
pierwszy wiersz ``CVRECIPE 1``, dalej JSON z rozmiarem, SHA-256 całości i listą
``[identyfikator, długość]``. Fragmenty leżą w ``.cleanvault-chunks`` w katalogu
głównym kopii, w ścieżce ``ab/cd/<identyfikator>`` (``.cvlt`` przy szyfrowaniu,
w tym samym formacie co wyżej). Plik to fragmenty sklejone po kolei.

Kopia poza domem (chmura S3/B2): pobierz cały folder kopii z usługi dowolnym
narzędziem (rclone, AWS CLI, strona Backblaze) i wskaż go skryptowi:

    python odzyskaj.py POBRANY_FOLDER KATALOG_DOCELOWY [ZNACZNIK_MIGAWKI]

Bez znacznika odtwarzana jest najnowsza migawka. Hasło to hasło kopii poza domem.
"""

from __future__ import annotations

import contextlib
import getpass
import hashlib
import os
import shutil
import struct
import sys

MAGIC = b"CVLT"
SUFFIX = ".cvlt"
RECIPE_SUFFIX = ".cvrecipe"
RECIPE_HEADER = b"CVRECIPE 1\n"
CHUNK_DIR = ".cleanvault-chunks"
TAG_BYTES = 16
CHUNK = 1024 * 1024
KDF_ARGON2ID = 1
KDF_PBKDF2_SHA256 = 2

# Pliki programu leżące w katalogu kopii — nie są danymi użytkownika.
SKIP_PREFIXES = (".cleanvault-",)
SKIP_NAMES = ("odzyskaj.py", "JAK ODZYSKAC DANE - HOW TO RECOVER.txt")


class RecoveryError(Exception):
    pass


def read_header(handle):
    """Zwraca (surowy nagłówek, id kdf, sól, nonce, a, b, c, rozmiar jawny)."""
    fixed = handle.read(8)
    if len(fixed) < 8 or fixed[:4] != MAGIC:
        raise RecoveryError("to nie jest plik .cvlt / not a .cvlt file")
    version, kdf_id, _flags, salt_len = fixed[4], fixed[5], fixed[6], fixed[7]
    if version != 1:
        raise RecoveryError(f"nieznana wersja formatu / unknown format version: {version}")
    salt = handle.read(salt_len)
    nonce_len = handle.read(1)
    if len(salt) != salt_len or not nonce_len:
        raise RecoveryError("uszkodzony nagłówek / damaged header")
    nonce = handle.read(nonce_len[0])
    tail = handle.read(20)
    if len(nonce) != nonce_len[0] or len(tail) != 20:
        raise RecoveryError("uszkodzony nagłówek / damaged header")
    a, b, c, plain_size = struct.unpack(">IIIQ", tail)
    raw = fixed + salt + nonce_len + nonce + tail
    return raw, kdf_id, salt, nonce, a, b, c, plain_size


def derive_key(password, kdf_id, salt, a, b, c):
    secret = password.encode("utf-8")
    if kdf_id == KDF_PBKDF2_SHA256:
        return hashlib.pbkdf2_hmac("sha256", secret, salt, a, dklen=32)
    if kdf_id == KDF_ARGON2ID:
        try:
            from argon2.low_level import Type, hash_secret_raw
        except ImportError as exc:
            raise RecoveryError("brak biblioteki argon2-cffi: pip install argon2-cffi") from exc
        return hash_secret_raw(
            secret=secret, salt=salt, time_cost=a, memory_cost=b,
            parallelism=c, hash_len=32, type=Type.ID,
        )
    raise RecoveryError(f"nieznany algorytm klucza / unknown key algorithm: {kdf_id}")


class _Decryptor:
    """AES-256-GCM strumieniowo — z pycryptodomex albo z cryptography."""

    def __init__(self, key, nonce, aad, tag):
        self._tag = tag
        try:
            from Cryptodome.Cipher import AES

            self._cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            self._cipher.update(aad)
            self._kind = "pycryptodome"
        except ImportError:
            try:
                from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
            except ImportError as exc:
                raise RecoveryError(
                    "brak biblioteki do AES-GCM: pip install pycryptodomex"
                ) from exc
            self._cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag)).decryptor()
            self._cipher.authenticate_additional_data(aad)
            self._kind = "cryptography"

    def update(self, data):
        if self._kind == "pycryptodome":
            return self._cipher.decrypt(data)
        return self._cipher.update(data)

    def finish(self):
        try:
            if self._kind == "pycryptodome":
                self._cipher.verify(self._tag)
                return b""
            return self._cipher.finalize()
        except Exception as exc:
            raise RecoveryError("złe hasło albo uszkodzony plik / wrong password or damaged file") from exc


def decrypt(source, target, password, keys):
    with open(source, "rb") as handle:
        raw, kdf_id, salt, nonce, a, b, c, plain_size = read_header(handle)
        body_start = handle.tell()
        handle.seek(0, os.SEEK_END)
        if handle.tell() != body_start + plain_size + TAG_BYTES:
            raise RecoveryError("plik jest obcięty / file is truncated")
        handle.seek(body_start + plain_size)
        tag = handle.read(TAG_BYTES)
        handle.seek(body_start)

        cache_key = (kdf_id, salt, a, b, c)
        if cache_key not in keys:
            keys[cache_key] = derive_key(password, kdf_id, salt, a, b, c)
        cipher = _Decryptor(keys[cache_key], nonce, raw, tag)

        part = target + ".part"
        try:
            with open(part, "wb") as out:
                remaining = plain_size
                while remaining:
                    block = handle.read(min(CHUNK, remaining))
                    if not block:
                        raise RecoveryError("plik jest obcięty / file is truncated")
                    remaining -= len(block)
                    out.write(cipher.update(block))
                out.write(cipher.finish())
            os.replace(part, target)
        except BaseException:
            if os.path.exists(part):
                os.remove(part)
            raise


def decrypt_blob(blob, password, keys):
    """Kontener .cvlt z pamięci (przepis albo fragment)."""
    import io

    raw, kdf_id, salt, nonce, a, b, c, plain_size = read_header(io.BytesIO(blob))
    start = len(raw)
    if len(blob) != start + plain_size + TAG_BYTES:
        raise RecoveryError("plik jest obcięty / file is truncated")
    cache_key = (kdf_id, salt, a, b, c)
    if cache_key not in keys:
        keys[cache_key] = derive_key(password, kdf_id, salt, a, b, c)
    cipher = _Decryptor(keys[cache_key], nonce, raw, blob[start + plain_size :])
    return cipher.update(blob[start : start + plain_size]) + cipher.finish()


def find_chunk_store(folder):
    """Katalog .cleanvault-chunks — szukany od folderu przepisu w górę."""
    current = os.path.abspath(folder)
    while True:
        candidate = os.path.join(current, CHUNK_DIR)
        if os.path.isdir(candidate):
            return candidate
        parent = os.path.dirname(current)
        if parent == current:
            raise RecoveryError("nie znaleziono katalogu " + CHUNK_DIR + " / chunk store not found")
        current = parent


def rebuild(recipe_path, target, password, keys):
    """Składa duży plik z fragmentów według przepisu i sprawdza sumę SHA-256."""
    import json

    with open(recipe_path, "rb") as handle:
        blob = handle.read()
    encrypted = blob[:4] == MAGIC
    if encrypted:
        blob = decrypt_blob(blob, password, keys)
    if not blob.startswith(RECIPE_HEADER):
        raise RecoveryError("uszkodzony przepis / damaged recipe")
    recipe = json.loads(blob[len(RECIPE_HEADER) :].decode("utf-8"))
    store = find_chunk_store(os.path.dirname(recipe_path))
    digest = hashlib.sha256()
    part = target + ".part"
    try:
        with open(part, "wb") as out:
            for cid, length in recipe["chunks"]:
                name = cid + (SUFFIX if encrypted else "")
                with open(os.path.join(store, cid[:2], cid[2:4], name), "rb") as handle:
                    data = handle.read()
                if encrypted:
                    data = decrypt_blob(data, password, keys)
                elif hashlib.sha256(data).hexdigest() != cid:
                    raise RecoveryError("uszkodzony fragment / damaged chunk " + cid[:16])
                if len(data) != length:
                    raise RecoveryError("uszkodzony fragment / damaged chunk " + cid[:16])
                out.write(data)
                digest.update(data)
        if digest.hexdigest() != recipe["sha256"]:
            raise RecoveryError("suma pliku się nie zgadza / file checksum mismatch")
        os.replace(part, target)
    except BaseException:
        if os.path.exists(part):
            os.remove(part)
        raise


def recipe_kind(path):
    """0 — zwykły plik, 1 — przepis jawny, 2 — przepis zaszyfrowany."""
    if path.endswith(RECIPE_SUFFIX + SUFFIX):
        return 2
    if path.endswith(RECIPE_SUFFIX):
        return 1
    return 0


def restore_offsite(folder, target, password, wanted=None):
    """Migawka kopii poza domem: przepis spisu → spis → pliki z fragmentów."""
    import json

    keys = {}
    snapshots = sorted(n[: -len(".cvsnap")] for n in os.listdir(os.path.join(folder, "snapshots"))
                       if n.endswith(".cvsnap"))
    if not snapshots:
        raise RecoveryError("brak migawek w folderze / no snapshots in the folder")
    stamp = wanted or snapshots[-1]
    print("Migawka / snapshot:", stamp)

    def chunk(cid):
        with open(os.path.join(folder, "chunks", cid[:2], cid), "rb") as handle:
            return decrypt_blob(handle.read(), password, keys)

    with open(os.path.join(folder, "snapshots", stamp + ".cvsnap"), "rb") as handle:
        recipe_bytes = decrypt_blob(handle.read(), password, keys)
    if not recipe_bytes.startswith(RECIPE_HEADER):
        raise RecoveryError("uszkodzona migawka / damaged snapshot")
    recipe = json.loads(recipe_bytes[len(RECIPE_HEADER) :].decode("utf-8"))
    index = b"".join(chunk(cid) for cid, _length in recipe["chunks"])
    if hashlib.sha256(index).hexdigest() != recipe["sha256"]:
        raise RecoveryError("uszkodzona migawka / damaged snapshot")
    lines = index.decode("utf-8").splitlines()[2:]
    done = failed = 0
    root = os.path.abspath(target)
    for line in lines:
        if not line:
            continue
        key, _size, mtime, sha, parts = json.loads(line)
        out = os.path.abspath(os.path.join(root, *key.split("/")))
        if not out.startswith(root + os.sep):
            print("POMINIĘTO / SKIPPED:", key)
            failed += 1
            continue
        os.makedirs(os.path.dirname(out), exist_ok=True)
        try:
            digest = hashlib.sha256()
            with open(out + ".part", "wb") as handle:
                for cid, length in parts:
                    data = chunk(cid)
                    if len(data) != length:
                        raise RecoveryError("uszkodzony fragment / damaged chunk " + cid[:16])
                    handle.write(data)
                    digest.update(data)
            if digest.hexdigest() != sha:
                raise RecoveryError("suma pliku się nie zgadza / file checksum mismatch")
            os.replace(out + ".part", out)
            os.utime(out, (mtime, mtime))
            done += 1
        except (OSError, RecoveryError) as exc:
            failed += 1
            if os.path.exists(out + ".part"):
                os.remove(out + ".part")
            print("BŁĄD / ERROR:", key, "—", exc)
    print(f"Odzyskano plików / files recovered: {done}, błędów / errors: {failed}")
    return 1 if failed else 0


def is_encrypted(path):
    if not path.endswith(SUFFIX):
        return False
    with open(path, "rb") as handle:
        return handle.read(4) == MAGIC


def files_under(source):
    if os.path.isfile(source):
        yield source, os.path.basename(source)
        return
    for folder, dirs, names in os.walk(source):
        dirs[:] = sorted(d for d in dirs if not d.startswith(SKIP_PREFIXES))
        for name in sorted(names):
            if name in SKIP_NAMES or name.startswith(SKIP_PREFIXES) or name.endswith(".part"):
                continue
            full = os.path.join(folder, name)
            yield full, os.path.relpath(full, source)


def _safe_console():
    """Konsola Windows bywa w kodowaniu cp1252 albo cp852 — polski znak w komunikacie
    nie może przerwać odzyskiwania. Znak, którego nie da się wypisać, staje się „?”;
    każdy komunikat ma też wersję angielską, więc pozostaje czytelny."""
    for stream in (sys.stdout, sys.stderr):
        with contextlib.suppress(AttributeError, ValueError):
            stream.reconfigure(errors="replace")


def main(argv):
    _safe_console()
    if len(argv) == 4 or (len(argv) == 3 and os.path.isdir(os.path.join(argv[1], "snapshots"))):
        folder, target = os.path.abspath(argv[1]), os.path.abspath(argv[2])
        password = os.environ.get("TVB_PASSWORD") or getpass.getpass("Hasło kopii poza domem / password: ")
        try:
            return restore_offsite(folder, target, password, argv[3] if len(argv) == 4 else None)
        except (OSError, RecoveryError) as exc:
            print("BŁĄD / ERROR:", exc)
            return 1
    if len(argv) != 3:
        print(__doc__.split("Użycie / usage::")[1].split("KATALOG_KOPII to")[0].strip())
        return 2
    source, target = os.path.abspath(argv[1]), os.path.abspath(argv[2])
    if not os.path.exists(source):
        print("Nie ma takiego katalogu / no such folder:", source)
        return 2

    items = list(files_under(source))
    needs_password = any(is_encrypted(path) or recipe_kind(path) == 2 for path, _rel in items)
    password = ""
    if needs_password:
        password = os.environ.get("TVB_PASSWORD") or getpass.getpass("Hasło do kopii / backup password: ")

    keys = {}
    done = failed = 0
    for path, rel in items:
        kind = recipe_kind(path)
        encrypted = kind == 0 and is_encrypted(path)
        if kind == 2:
            name = rel[: -len(RECIPE_SUFFIX + SUFFIX)]
        elif kind == 1:
            name = rel[: -len(RECIPE_SUFFIX)]
        else:
            name = rel[: -len(SUFFIX)] if encrypted else rel
        out = os.path.join(target, name)
        os.makedirs(os.path.dirname(out) or target, exist_ok=True)
        try:
            if kind:
                rebuild(path, out, password, keys)
            elif encrypted:
                decrypt(path, out, password, keys)
            else:
                shutil.copy2(path, out)
            done += 1
        except (OSError, RecoveryError) as exc:
            failed += 1
            print("BŁĄD / ERROR:", rel, "—", exc)
    print(f"Odzyskano plików / files recovered: {done}, błędów / errors: {failed}")
    print("Cel / target:", target)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
