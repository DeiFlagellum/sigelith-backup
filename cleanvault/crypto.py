"""Szyfrowanie plików — AES-256-GCM ze strumieniowaniem i KDF Argon2id.

Co zmieniono względem wersji 1.x i dlaczego:

* **Strumieniowanie zamiast wczytywania całego pliku do RAM.** Stara wersja robiła
  ``f.read()`` na całym pliku, kodowała base64 i pakowała w JSON — plik 2 GB
  potrafił zająć ~6 GB pamięci. Teraz przetwarzamy porcjami po 1 MiB
  przy stałym zużyciu pamięci.
* **Format binarny zamiast JSON+base64.** Base64 puchł o 33%; kontener binarny
  zajmuje tyle co dane wejściowe + 57 bajtów nagłówka + 16 bajtów tagu.
* **Klucz wyprowadzany raz na sesję, nie raz na plik.** Stara wersja liczyła
  PBKDF2 (100k iteracji) osobno dla każdego pliku — dla 10 000 plików to godziny
  samego KDF. :class:`PasswordKeyring` cache'uje klucz per (sól, parametry).
* **Argon2id zamiast PBKDF2-HMAC-SHA1.** Domyślny PRF w PyCryptodome to SHA-1;
  aplikacja deklarowała w oknie „O programie" Argon2, którego w ogóle nie było.
* **Nagłówek uwierzytelniony jako AAD.** Bez tego dałoby się podmienić parametry
  KDF albo deklarowany rozmiar pliku bez unieważnienia tagu.
* **Odszyfrowanie zapisuje do pliku tymczasowego i dopiero po weryfikacji tagu
  podmienia cel.** Inaczej wypuszczalibyśmy na dysk niezweryfikowany plaintext.

Format kontenera ``CVLT`` v1 (wszystkie liczby big-endian)::

    magic        4B   b"CVLT"
    version      1B   1
    kdf_id       1B   1 = Argon2id, 2 = PBKDF2-HMAC-SHA256
    flags        1B   zarezerwowane (0)
    salt_len     1B   16
    salt        16B
    nonce_len    1B   12
    nonce       12B
    kdf_a        4B   Argon2: time_cost      | PBKDF2: liczba iteracji
    kdf_b        4B   Argon2: pamięć w KiB   | PBKDF2: 0
    kdf_c        4B   Argon2: równoległość   | PBKDF2: 0
    plain_size   8B   rozmiar jawnego pliku (do paska postępu i kontroli spójności)
    -------------------------------------------------- koniec nagłówka (AAD)
    ciphertext   NB   dokładnie plain_size bajtów
    tag         16B   GCM
"""

from __future__ import annotations

import contextlib
import hashlib
import os
import struct
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Random import get_random_bytes

from .i18n import tr
from .log import get_logger
from .paths import long_path

log = get_logger("crypto")

MAGIC = b"CVLT"
FORMAT_VERSION = 1
ENCRYPTED_SUFFIX = ".cvlt"

KDF_ARGON2ID = 1
KDF_PBKDF2_SHA256 = 2

SALT_BYTES = 16
NONCE_BYTES = 12
TAG_BYTES = 16
KEY_BYTES = 32
CHUNK_SIZE = 1024 * 1024

_HEADER_STRUCT = struct.Struct(">4sBBBB")  # magic, version, kdf_id, flags, salt_len
_TAIL_STRUCT = struct.Struct(">IIIQ")  # kdf_a, kdf_b, kdf_c, plain_size

# Parametry Argon2id zgodne z rekomendacją OWASP (64 MiB / t=3 / p=4).
ARGON2_TIME_COST = 3
ARGON2_MEMORY_KIB = 64 * 1024
ARGON2_PARALLELISM = 4
# Fallback PBKDF2 — 600 000 iteracji SHA-256 (rekomendacja OWASP 2023).
PBKDF2_ITERATIONS = 600_000

try:  # argon2-cffi jest zalecane, ale nie jest twardym wymogiem
    from argon2.low_level import Type as _Argon2Type
    from argon2.low_level import hash_secret_raw as _argon2_raw

    ARGON2_AVAILABLE = True
except ImportError:  # pragma: no cover - zależne od środowiska
    ARGON2_AVAILABLE = False
    log.warning("argon2-cffi niedostępne — używam PBKDF2-HMAC-SHA256 %d iteracji", PBKDF2_ITERATIONS)


class CryptoError(Exception):
    """Bazowy błąd warstwy kryptograficznej."""


class UnsupportedFormatError(CryptoError):
    """Plik nie jest kontenerem programu albo pochodzi z nowszej wersji."""


class IntegrityError(CryptoError):
    """Tag GCM się nie zgadza: złe hasło albo uszkodzony/zmodyfikowany plik."""


class OperationCancelled(CryptoError):
    """Użytkownik przerwał operację."""


ProgressFn = Callable[[int], None]
CancelFn = Callable[[], bool]


@dataclass(frozen=True)
class KdfParams:
    """Parametry wyprowadzania klucza zapisane w nagłówku pliku."""

    kdf_id: int
    salt: bytes
    a: int = 0
    b: int = 0
    c: int = 0

    @staticmethod
    def new_default() -> KdfParams:
        salt = get_random_bytes(SALT_BYTES)
        if ARGON2_AVAILABLE:
            return KdfParams(KDF_ARGON2ID, salt, ARGON2_TIME_COST, ARGON2_MEMORY_KIB, ARGON2_PARALLELISM)
        return KdfParams(KDF_PBKDF2_SHA256, salt, PBKDF2_ITERATIONS)

    @property
    def algorithm_name(self) -> str:
        if self.kdf_id == KDF_ARGON2ID:
            return tr("Argon2id (t={passes}, {memory} MiB, p={threads})").format(
                passes=self.a, memory=self.b // 1024, threads=self.c
            )
        return tr("PBKDF2-HMAC-SHA256 ({count} iteracji)").format(
            count=f"{self.a:,}".replace(",", " ")
        )


@dataclass(frozen=True)
class Header:
    params: KdfParams
    nonce: bytes
    plain_size: int
    raw: bytes  # dokładne bajty nagłówka — uwierzytelniane jako AAD

    @property
    def size(self) -> int:
        return len(self.raw)


def _derive_key(password: str, params: KdfParams) -> bytes:
    secret = password.encode("utf-8")
    if params.kdf_id == KDF_ARGON2ID:
        if not ARGON2_AVAILABLE:
            raise UnsupportedFormatError(
                tr("Plik wymaga Argon2id, a biblioteka argon2-cffi jest niedostępna.")
            )
        return _argon2_raw(
            secret=secret,
            salt=params.salt,
            time_cost=params.a,
            memory_cost=params.b,
            parallelism=params.c,
            hash_len=KEY_BYTES,
            type=_Argon2Type.ID,
        )
    if params.kdf_id == KDF_PBKDF2_SHA256:
        return PBKDF2(secret, params.salt, dkLen=KEY_BYTES, count=params.a, hmac_hash_module=SHA256)
    raise UnsupportedFormatError(
        tr("Nieznany algorytm wyprowadzania klucza: {name}").format(name=params.kdf_id)
    )


class PasswordKeyring:
    """Hasło + cache wyprowadzonych kluczy.

    Jeden obiekt obsługuje całą sesję backupu/przywracania. Wszystkie pliki
    jednej kopii dzielą sól, więc kosztowny KDF liczy się dokładnie raz,
    a nie raz na plik. Każdy plik dostaje własny losowy nonce, co jest
    warunkiem bezpieczeństwa GCM przy współdzielonym kluczu.
    """

    def __init__(self, password: str, params: KdfParams | None = None) -> None:
        if not password:
            raise ValueError(tr("Hasło nie może być puste."))
        self._password = password
        self._session_params = params or KdfParams.new_default()
        self._cache: dict[tuple, bytes] = {}

    @property
    def session_params(self) -> KdfParams:
        """Parametry używane przy szyfrowaniu nowych plików."""
        return self._session_params

    def key_for(self, params: KdfParams) -> bytes:
        cache_key = (params.kdf_id, params.salt, params.a, params.b, params.c)
        key = self._cache.get(cache_key)
        if key is None:
            key = _derive_key(self._password, params)
            self._cache[cache_key] = key
            log.debug("Wyprowadzono klucz: %s", params.algorithm_name)
        return key

    def wipe(self) -> None:
        """Porzuca hasło i klucze. Python nie gwarantuje wymazania pamięci,
        ale skracamy czas życia sekretu i zwalniamy referencje."""
        self._password = ""
        self._cache.clear()


def _pack_header(params: KdfParams, nonce: bytes, plain_size: int) -> bytes:
    return (
        _HEADER_STRUCT.pack(MAGIC, FORMAT_VERSION, params.kdf_id, 0, len(params.salt))
        + params.salt
        + bytes([len(nonce)])
        + nonce
        + _TAIL_STRUCT.pack(params.a, params.b, params.c, plain_size)
    )


def read_header(stream) -> Header:
    """Czyta i waliduje nagłówek z otwartego strumienia binarnego."""
    fixed = stream.read(_HEADER_STRUCT.size)
    if len(fixed) < _HEADER_STRUCT.size:
        raise UnsupportedFormatError(tr("Plik jest za krótki, by być kontenerem tego programu."))
    magic, version, kdf_id, _flags, salt_len = _HEADER_STRUCT.unpack(fixed)
    if magic != MAGIC:
        raise UnsupportedFormatError(tr("To nie jest plik zaszyfrowany przez ten program."))
    if version != FORMAT_VERSION:
        raise UnsupportedFormatError(
            tr("Plik w formacie w wersji {found}; ta wersja programu obsługuje {supported}.").format(
                found=version, supported=FORMAT_VERSION
            )
        )
    salt = stream.read(salt_len)
    nonce_len_raw = stream.read(1)
    if len(salt) != salt_len or not nonce_len_raw:
        raise UnsupportedFormatError(tr("Uszkodzony nagłówek pliku."))
    nonce = stream.read(nonce_len_raw[0])
    tail = stream.read(_TAIL_STRUCT.size)
    if len(nonce) != nonce_len_raw[0] or len(tail) != _TAIL_STRUCT.size:
        raise UnsupportedFormatError(tr("Uszkodzony nagłówek pliku."))
    a, b, c, plain_size = _TAIL_STRUCT.unpack(tail)
    params = KdfParams(kdf_id, salt, a, b, c)
    raw = fixed + salt + nonce_len_raw + nonce + tail
    return Header(params=params, nonce=nonce, plain_size=plain_size, raw=raw)


def peek_header(path: str | os.PathLike[str]) -> Header:
    """Odczytuje nagłówek bez deszyfrowania — do podglądu i walidacji w GUI."""
    with open(long_path(path), "rb") as handle:
        return read_header(handle)


def is_encrypted_file(path: str | os.PathLike[str]) -> bool:
    """Rozpoznaje kontener po zawartości, nie po rozszerzeniu."""
    try:
        with open(long_path(path), "rb") as handle:
            return handle.read(4) == MAGIC
    except OSError:
        return False


def _chunks(stream, total: int, cancel: CancelFn | None) -> Iterator[bytes]:
    remaining = total
    while remaining > 0:
        if cancel is not None and cancel():
            raise OperationCancelled(tr("Operacja przerwana przez użytkownika."))
        chunk = stream.read(min(CHUNK_SIZE, remaining))
        if not chunk:
            raise IntegrityError(tr("Plik skończył się wcześniej, niż deklaruje nagłówek."))
        remaining -= len(chunk)
        yield chunk


def encrypt_file(
    src: str | os.PathLike[str],
    dst: str | os.PathLike[str],
    keyring: PasswordKeyring,
    progress: ProgressFn | None = None,
    cancel: CancelFn | None = None,
    plain_digest: Any | None = None,
) -> int:
    """Szyfruje ``src`` do ``dst``. Zwraca rozmiar zapisanego kontenera.

    Zapis idzie do pliku tymczasowego i jest podmieniany atomowo, więc
    przerwana operacja nie zostawia w kopii uszkodzonego pliku wyglądającego
    na kompletny.

    ``plain_digest`` (obiekt w stylu ``hashlib.sha256()``) jest aktualizowany
    jawnym tekstem w locie. Dzięki temu suma kontrolna źródła powstaje podczas
    tego samego odczytu co szyfrowanie — bez niej silnik musiałby przeczytać
    każdy plik drugi raz, a przy kopii setek gigabajtów to podwaja pracę dysku
    i otwiera okno, w którym plik zmienia się między odczytami.
    """
    params = keyring.session_params
    key = keyring.key_for(params)
    nonce = get_random_bytes(NONCE_BYTES)
    src_path = long_path(src)
    plain_size = os.path.getsize(src_path)
    header = _pack_header(params, nonce, plain_size)

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    cipher.update(header)  # nagłówek uwierzytelniony, ale niezaszyfrowany

    tmp = Path(str(dst) + ".part")
    written = 0
    try:
        with open(src_path, "rb") as fin, open(long_path(tmp), "wb") as fout:
            fout.write(header)
            written += len(header)
            for chunk in _chunks(fin, plain_size, cancel):
                if plain_digest is not None:
                    plain_digest.update(chunk)
                block = cipher.encrypt(chunk)
                fout.write(block)
                written += len(block)
                if progress is not None:
                    progress(len(chunk))
            tag = cipher.digest()
            fout.write(tag)
            written += len(tag)
            fout.flush()
            os.fsync(fout.fileno())
        os.replace(long_path(tmp), long_path(dst))
    except BaseException:
        _unlink_quiet(tmp)
        raise
    return written


def encrypt_bytes(data: bytes, keyring: PasswordKeyring) -> bytes:
    """Kontener CVLT w pamięci — dla małych porcji: fragmentów dużych plików i przepisów.

    Format jest identyczny z plikowym (:func:`encrypt_file`), więc ten sam kod —
    także skrypt ratunkowy w katalogu kopii — odszyfrowuje jedno i drugie.
    """
    params = keyring.session_params
    key = keyring.key_for(params)
    nonce = get_random_bytes(NONCE_BYTES)
    header = _pack_header(params, nonce, len(data))
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    cipher.update(header)
    body, tag = cipher.encrypt_and_digest(data)
    return header + body + tag


def decrypt_bytes(blob: bytes, keyring: PasswordKeyring) -> bytes:
    """Odszyfrowuje kontener CVLT z pamięci; zły tag albo obcięcie to :class:`IntegrityError`."""
    import io

    header = read_header(io.BytesIO(blob))
    end = header.size + header.plain_size
    if len(blob) != end + TAG_BYTES:
        raise IntegrityError(tr("Brakuje tagu uwierzytelniającego — plik jest obcięty."))
    cipher = AES.new(keyring.key_for(header.params), AES.MODE_GCM, nonce=header.nonce)
    cipher.update(header.raw)
    try:
        return cipher.decrypt_and_verify(blob[header.size : end], blob[end:])
    except ValueError as exc:
        raise IntegrityError(
            tr("Weryfikacja nie powiodła się: nieprawidłowe hasło lub uszkodzony plik.")
        ) from exc


def decrypt_file(
    src: str | os.PathLike[str],
    dst: str | os.PathLike[str],
    keyring: PasswordKeyring,
    progress: ProgressFn | None = None,
    cancel: CancelFn | None = None,
) -> int:
    """Odszyfrowuje ``src`` do ``dst``. Zwraca rozmiar odtworzonego pliku.

    Plik docelowy powstaje dopiero po pomyślnej weryfikacji tagu GCM —
    niezweryfikowany plaintext nigdy nie trafia pod docelową nazwę.
    """
    src_path = long_path(src)
    tmp = Path(str(dst) + ".part")
    try:
        with open(src_path, "rb") as fin:
            header = read_header(fin)
            key = keyring.key_for(header.params)
            cipher = AES.new(key, AES.MODE_GCM, nonce=header.nonce)
            cipher.update(header.raw)

            with open(long_path(tmp), "wb") as fout:
                for chunk in _chunks(fin, header.plain_size, cancel):
                    fout.write(cipher.decrypt(chunk))
                    if progress is not None:
                        progress(len(chunk))
                tag = fin.read(TAG_BYTES)
                if len(tag) != TAG_BYTES:
                    raise IntegrityError(tr("Brakuje tagu uwierzytelniającego — plik jest obcięty."))
                try:
                    cipher.verify(tag)
                except ValueError as exc:
                    raise IntegrityError(
                        tr("Weryfikacja nie powiodła się: nieprawidłowe hasło lub uszkodzony plik.")
                    ) from exc
                fout.flush()
                os.fsync(fout.fileno())
        os.replace(long_path(tmp), long_path(dst))
    except BaseException:
        _unlink_quiet(tmp)
        raise
    return header.plain_size


def verify_file(
    path: str | os.PathLike[str],
    keyring: PasswordKeyring,
    cancel: CancelFn | None = None,
) -> int:
    """Sprawdza, czy kontener da się odszyfrować i czy tag się zgadza.

    Nic nie zapisuje na dysk — służy do opcji „Weryfikuj kopię po zapisie"
    oraz do testu poprawności hasła przed masowym przywracaniem.
    """
    with open(long_path(path), "rb") as fin:
        header = read_header(fin)
        key = keyring.key_for(header.params)
        cipher = AES.new(key, AES.MODE_GCM, nonce=header.nonce)
        cipher.update(header.raw)
        for chunk in _chunks(fin, header.plain_size, cancel):
            cipher.decrypt(chunk)
        tag = fin.read(TAG_BYTES)
        if len(tag) != TAG_BYTES:
            raise IntegrityError(tr("Brakuje tagu uwierzytelniającego — plik jest obcięty."))
        try:
            cipher.verify(tag)
        except ValueError as exc:
            raise IntegrityError(
                tr("Weryfikacja nie powiodła się: nieprawidłowe hasło lub uszkodzony plik.")
            ) from exc
    return header.plain_size


def plaintext_sha256(
    path: str | os.PathLike[str],
    keyring: PasswordKeyring,
    cancel: CancelFn | None = None,
) -> tuple[str, int]:
    """SHA-256 i rozmiar treści jawnej kontenera — bez zapisu na dysk.

    Suma liczy się tylko wtedy, gdy tag GCM się zgadza: treść podmieniona albo
    uszkodzona daje ``IntegrityError``, nie „inną sumę". Służy audytowi kopii
    względem pieczęci w publicznym dzienniku (audit.py), która obejmuje sumy
    plików przed zaszyfrowaniem.
    """
    digest = hashlib.sha256()
    with open(long_path(path), "rb") as fin:
        header = read_header(fin)
        key = keyring.key_for(header.params)
        cipher = AES.new(key, AES.MODE_GCM, nonce=header.nonce)
        cipher.update(header.raw)
        for chunk in _chunks(fin, header.plain_size, cancel):
            digest.update(cipher.decrypt(chunk))
        tag = fin.read(TAG_BYTES)
        if len(tag) != TAG_BYTES:
            raise IntegrityError(tr("Brakuje tagu uwierzytelniającego — plik jest obcięty."))
        try:
            cipher.verify(tag)
        except ValueError as exc:
            raise IntegrityError(
                tr("Weryfikacja nie powiodła się: nieprawidłowe hasło lub uszkodzony plik.")
            ) from exc
    return digest.hexdigest(), header.plain_size


def _unlink_quiet(path: Path) -> None:
    with contextlib.suppress(OSError):
        os.unlink(long_path(path))
