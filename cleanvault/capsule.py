"""Kapsuła czasu w kopii — koperta ``beattime-seal-v1`` (ta sama co sigelith.org/capsule/).

Po co: wybrane pliki zapieczętowane do daty tak, że żaden pojedynczy posiadacz
klucza nie otworzy ich wcześniej, a kapsuła leży w kopii użytkownika, nie na
serwerze („minimum odpowiedzialności”). Np. dokumenty dla rodziny „do otwarcia w 2036”.

Jak (profil „standard” strony kapsuły, SEAL.md): sekret 32 B dzielony Shamirem
2 z 3 — udział dla sieci drand (runda wypadająca na zadany @beat), udział dla
serwera kluczy Sigelith (tożsamość tego @beatu) i udział dla użytkownika (kod
odzyskiwania). Udziały beaconów są zaszyfrowane IBE (ibe.py) do tożsamości,
których klucze wydają dopiero w tamtej chwili sieć drand (podpis progowy) i serwer
kluczy — ten z zasady, bo kluczem głównym mógłby je policzyć wcześniej. Przed nią
sam kod odzyskiwania nie wystarcza, ale leży obok kapsuły (rescue.capsule_note),
więc kto ma kopię, temu do wcześniejszego otwarcia wystarczy złamanie tej zasady
przez operatora. Po tej chwili wystarczą dowolne dwa udziały — więc zniknięcie
jednego operatora nie zamyka kapsuły na zawsze.

Treść: pakiet ZIP wybranych plików (``meta``: kind=file, name, type), jak plik
wybrany na stronie kapsuły; szyfrowanie AES-256-GCM segmentami po 64 KiB. Wynik
to para plików ``capsule-<id>.beatseal.json`` + ``capsule-<id>.bin`` —
otwiera je strona sigelith.org/capsule/ (w dniu otwarcia).

Warstwy przeniesione z serwera Sigelith (apps/seal: envelope, shamir, stream,
recovery, drand) bez zmian formatu; szyfr przez pycryptodomex zamiast
cryptography. Zgodność z przeglądarkowym otwieraniem sprawdzają testy
(tests/test_capsule.py) na tych samych modułach JS co strona.
"""

from __future__ import annotations

import base64
import hashlib
import io
import json
import secrets
import zipfile
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import BinaryIO

from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
from Cryptodome.Protocol.KDF import HKDF

from . import ibe
from .i18n import tr

VERSION = "beattime-seal-v1"
AEAD = "AES-256-GCM-STREAM"
SEGMENT = 65_536
NONCE_PREFIX_LEN = 7
TAG_LEN = 16
MASTER_LEN = 32
HKDF_INFO = b"beattime-seal-v1|aead"
MICROSECONDS_PER_BEAT = 86_400_000
BEACON_KINDS = ("drand", "beat")
#: Powyżej tej wielkości ładunek idzie do osobnego pliku — ta sama granica co na stronie.
INLINE_MAX = 262_144
ENVELOPE_SUFFIX = ".beatseal.json"
BLOB_SUFFIX = ".bin"
CAPSULE_PAGE = "https://sigelith.org/capsule/"


# ------------------------------------------------------------------ czas


def beat_index(moment: datetime) -> int:
    """Absolutny indeks @beatu (całkowite mikrosekundy od 1970, bez dzielenia przez 86,4)."""
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=UTC)
    micros = int(moment.astimezone(UTC).timestamp() * 1_000_000)
    return micros // MICROSECONDS_PER_BEAT


def beat_moment(index: int) -> datetime:
    return datetime.fromtimestamp(index * MICROSECONDS_PER_BEAT / 1_000_000, tz=UTC)


@dataclass(frozen=True)
class Chain:
    name: str
    chain_hash: str
    scheme: str
    period: int
    genesis_time: int
    public_key: str


#: drand quicknet — parametry łańcucha są niezmienne dla danego chain_hash (apps/seal/drand.py).
QUICKNET = Chain(
    name="quicknet",
    chain_hash="52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971",
    scheme="bls-unchained-g1-rfc9380",
    period=3,
    genesis_time=1692803367,
    public_key=(
        "83cf0f2896adee7eb8b5f01fcad3912212c437e0073e911fb90022d3e760183c"
        "8c4b450b6a0a6c3ac6a5776a2d1064510d1fec758c921cc22b0e17e63aaf4bcb"
        "5ed66304de9cf809bd274ca73bab4af5a6e9c76a4bc09e76eae8991ef5ece45a"
    ),
)


def round_for_beat(chain: Chain, index: int) -> int:
    """Pierwsza runda drand nie wcześniej niż początek @beatu — liczone całkowicie, jak beacons.js."""
    if index < 0:
        raise ValueError("beat index must not be negative")
    delta = index * MICROSECONDS_PER_BEAT - chain.genesis_time * 1_000_000
    if delta <= 0:
        return 1
    step = chain.period * 1_000_000
    return -(-delta // step) + 1


def drand_identity(round_number: int) -> bytes:
    return hashlib.sha256(round_number.to_bytes(8, "big")).digest()


def beat_identity(index: int) -> bytes:
    return hashlib.sha256(f"beattime-beat-v1|{index}".encode("ascii")).digest()


# ---------------------------------------------------------- Shamir GF(256)

_EXP = [0] * 512
_LOG = [0] * 256


def _tables() -> None:
    x = 1
    for i in range(255):
        _EXP[i] = x
        _LOG[x] = i
        x = ((x << 1) ^ (0x11B if x & 0x80 else 0) ^ x) & 0xFF
    for i in range(255, 512):
        _EXP[i] = _EXP[i - 255]


_tables()


def _mul(a: int, b: int) -> int:
    return 0 if a == 0 or b == 0 else _EXP[_LOG[a] + _LOG[b]]


def _div(a: int, b: int) -> int:
    if b == 0:
        raise ZeroDivisionError("division by zero in GF(256)")
    return 0 if a == 0 else _EXP[_LOG[a] - _LOG[b] + 255]


def shamir_split(secret: bytes, t: int, n: int) -> list[tuple[int, bytes]]:
    if not secret or t < 2 or n < t or n > 255:
        raise ValueError("invalid Shamir split")
    ys = [bytearray(len(secret)) for _ in range(n)]
    for pos, byte in enumerate(secret):
        coeffs = [byte, *secrets.token_bytes(t - 1)]
        for i in range(n):
            acc = 0
            for c in reversed(coeffs):
                acc = _mul(acc, i + 1) ^ c
            ys[i][pos] = acc
    return [(i + 1, bytes(y)) for i, y in enumerate(ys)]


def shamir_combine(shares: list[tuple[int, bytes]]) -> bytes:
    xs = [x for x, _ in shares]
    if not shares or len(set(xs)) != len(xs) or 0 in xs:
        raise ValueError("invalid shares")
    out = bytearray(len(shares[0][1]))
    for pos in range(len(out)):
        acc = 0
        for i, (xi, yi) in enumerate(shares):
            num, den = 1, 1
            for j, (xj, _) in enumerate(shares):
                if i != j:
                    num = _mul(num, xj)
                    den = _mul(den, xi ^ xj)
            acc ^= _mul(yi[pos], _div(num, den))
        out[pos] = acc
    return bytes(out)


# -------------------------------------------------------- kod odzyskiwania

_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def share_sum(x: int, y: bytes) -> str:
    return hashlib.sha256(f"beattime-seal-v1|share|{x:02x}{y.hex()}".encode("ascii")).hexdigest()[:4]


def recovery_code(envelope_id_hex: str, x: int, y: bytes) -> str:
    payload = bytes([x]) + y + bytes.fromhex(share_sum(x, y))
    bits, width = int.from_bytes(payload, "big"), len(payload) * 8
    body = "".join(_ALPHABET[(bits >> shift) & 0x1F] for shift in range(width - 5, -1, -5))
    return "-".join([envelope_id_hex[:4].upper()] + [body[i:i + 4] for i in range(0, len(body), 4)])


# --------------------------------------------------- AES-256-GCM-STREAM


def _nonce(prefix: bytes, counter: int, last: bool) -> bytes:
    return prefix + counter.to_bytes(4, "big") + (b"\x01" if last else b"\x00")


def _segments(src: BinaryIO, size: int):
    def read() -> bytes:
        chunks, remaining = [], size
        while remaining > 0:
            chunk = src.read(remaining)
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        return b"".join(chunks)

    current = read()
    while True:
        following = read()
        if not following:
            yield current, True
            return
        yield current, False
        current = following


def stream_encrypt(key: bytes, prefix: bytes, aad: bytes, src: BinaryIO, dst: BinaryIO) -> int:
    written = 0
    for counter, (chunk, last) in enumerate(_segments(src, SEGMENT)):
        cipher = AES.new(key, AES.MODE_GCM, nonce=_nonce(prefix, counter, last), mac_len=TAG_LEN)
        cipher.update(aad)
        body, tag = cipher.encrypt_and_digest(chunk)
        dst.write(body + tag)
        written += len(body) + TAG_LEN
    return written


def stream_decrypt(key: bytes, prefix: bytes, aad: bytes, src: BinaryIO, dst: BinaryIO) -> int:
    written, saw_last = 0, False
    for counter, (blob, last) in enumerate(_segments(src, SEGMENT + TAG_LEN)):
        if len(blob) < TAG_LEN:
            raise ValueError("truncated ciphertext")
        cipher = AES.new(key, AES.MODE_GCM, nonce=_nonce(prefix, counter, last), mac_len=TAG_LEN)
        cipher.update(aad)
        chunk = cipher.decrypt_and_verify(blob[:-TAG_LEN], blob[-TAG_LEN:])
        dst.write(chunk)
        written += len(chunk)
        saw_last = last
    if not saw_last:
        raise ValueError("ciphertext has no final segment")
    return written


# ---------------------------------------------------------------- koperta


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def header(envelope: dict) -> dict:
    out = {k: v for k, v in envelope.items() if k != "payload"}
    out["payload"] = {k: v for k, v in envelope.get("payload", {}).items() if k == "mode"}
    return out


def envelope_id(envelope: dict) -> str:
    return hashlib.sha256(canonical(header(envelope))).hexdigest()[:16]


def _aad(envelope: dict) -> bytes:
    return hashlib.sha256(canonical(header(envelope))).digest()


def derive_key(master: bytes) -> bytes:
    return HKDF(master, 32, b"", SHA256, context=HKDF_INFO)


class DrandSealer:
    kind = "drand"

    def __init__(self, chain: Chain = QUICKNET) -> None:
        self.chain = chain

    def seal(self, x: int, share: bytes, index: int) -> dict:
        round_number = round_for_beat(self.chain, index)
        ct = ibe.encrypt(bytes.fromhex(self.chain.public_key), drand_identity(round_number), share)
        return {"kind": "drand", "x": x, "chain_hash": self.chain.chain_hash, "round": round_number,
                "scheme": self.chain.scheme, "ct": base64.b64encode(ct).decode()}


class BeatSealer:
    kind = "beat"

    def __init__(self, operator: dict) -> None:
        self.operator = operator

    def seal(self, x: int, share: bytes, index: int) -> dict:
        ct = ibe.encrypt(base64.b64decode(self.operator["pub"]), beat_identity(index), share)
        out = {"kind": "beat", "x": x, "op": self.operator["op"], "pub": self.operator["pub"],
               "scheme": self.operator["scheme"], "ct": base64.b64encode(ct).decode()}
        if self.operator.get("url"):
            out["url"] = self.operator["url"]
        return out


class EscrowSealer:
    """Udział dla użytkownika — do koperty trafia tylko jego suma kontrolna."""

    kind = "escrow"

    def __init__(self) -> None:
        self.x: int | None = None
        self.share: bytes | None = None

    def seal(self, x: int, share: bytes, index: int) -> dict:
        self.x, self.share = x, share
        return {"kind": "escrow", "x": x, "sum": share_sum(x, share)}


def _build(master: bytes, prefix: bytes, index: int, sealers: list, t: int, hint: str | None,
           mode: str) -> dict:
    parts = shamir_split(master, t, len(sealers))
    shares = [sealer.seal(x, y, index) for sealer, (x, y) in zip(sealers, parts, strict=True)]
    envelope = {"v": VERSION, "t": t, "beat": index, "aead": AEAD, "chunk": SEGMENT,
                "nonce": base64.b64encode(prefix).decode(), "payload": {"mode": mode}, "shares": shares}
    if hint:
        envelope["hint"] = hint
    return envelope


def seal(plaintext: bytes, *, index: int, sealers: list, t: int, hint: str | None = None,
         blob_out: BinaryIO | None = None) -> dict:
    """Pieczętuje ładunek; duży (``blob_out`` podany) trafia do osobnego pliku szyfrogramu."""
    master, prefix = secrets.token_bytes(MASTER_LEN), secrets.token_bytes(NONCE_PREFIX_LEN)
    mode = "detached" if blob_out is not None else "inline"
    envelope = _build(master, prefix, index, sealers, t, hint, mode)
    key = derive_key(master)
    if blob_out is None:
        out = io.BytesIO()
        stream_encrypt(key, prefix, _aad(envelope), io.BytesIO(plaintext), out)
        envelope["payload"]["data"] = base64.b64encode(out.getvalue()).decode()
        return envelope

    class _Digest:
        def __init__(self) -> None:
            self.hash = hashlib.sha256()

        def write(self, data: bytes) -> int:
            self.hash.update(data)
            return blob_out.write(data)

    sink = _Digest()
    size = stream_encrypt(key, prefix, _aad(envelope), io.BytesIO(plaintext), sink)
    envelope["payload"]["digest"] = sink.hash.hexdigest()
    envelope["payload"]["size"] = size
    return envelope


def open_payload(envelope: dict, shares: list[tuple[int, bytes]], blob: bytes | None = None) -> bytes:
    """Otwiera kopertę z ``t`` udziałów (do testów i do przyszłego otwierania w programie)."""
    if envelope.get("v") != VERSION:
        raise ValueError("not a beattime-seal-v1 envelope")
    key = derive_key(shamir_combine(shares[: envelope["t"]]))
    prefix = base64.b64decode(envelope["nonce"])
    data = blob if envelope["payload"]["mode"] == "detached" else base64.b64decode(envelope["payload"]["data"])
    out = io.BytesIO()
    stream_decrypt(key, prefix, _aad(envelope), io.BytesIO(data), out)
    return out.getvalue()


def pack_payload(meta: dict, body: bytes) -> bytes:
    return canonical(meta) + b"\n" + body


def unpack_payload(raw: bytes) -> tuple[dict, bytes]:
    cut = raw.index(b"\n")
    return json.loads(raw[:cut].decode("utf-8")), raw[cut + 1:]


# ------------------------------------------------------------ operatorzy

#: Serwer kluczy Sigelith — ten sam wpis co w rejestrze
#: https://sigelith.org/.well-known/beat-key-operators.json (profil „standard” strony
#: kapsuły). Wbudowany, a nie pobierany: pieczętowanie nie łączy się z siecią, bo program
#: poza dwiema włączanymi funkcjami niczego nie wysyła (polityka prywatności). Nowy klucz
#: operatora = aktualizacja programu. Źródłem prawdy o kluczu jest ``pub`` w kopercie.
BUILTIN_OPERATOR = {
    "op": "beattime",
    "pub": "jN8nAWDv7kfa7qXX8LvxBniOi3EksnRr6YA474t8VtYzrIHEttBwikf+0RWwutscBhukGwik6kjOumfo27iT7VXjPytmIOBAVFcO4538Vy3SIfewNy0LhuEGCERv3baD",
    "scheme": ibe.SCHEME,
    "url": "https://beattime.live/api/seal/share/",
}


# ------------------------------------------------------------- całość


@dataclass
class SealedCapsule:
    envelope_path: Path
    blob_path: Path | None
    envelope_id: str
    recovery_code: str
    opens_at: datetime


def zip_paths(paths: Iterable[Path]) -> bytes:
    """ZIP wybranych plików i folderów (ścieżki względem ich folderu nadrzędnego)."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in paths:
            path = Path(path)
            if path.is_dir():
                for item in sorted(path.rglob("*")):
                    if item.is_file():
                        archive.write(item, item.relative_to(path.parent).as_posix())
            elif path.is_file():
                archive.write(path, path.name)
    return buffer.getvalue()


def seal_files(paths: list[Path], opens_at: datetime, target_dir: Path, name: str,
               operator: dict | None = None) -> SealedCapsule:
    """Pieczętuje pliki do chwili ``opens_at`` i zapisuje kapsułę w ``target_dir``."""
    index = beat_index(opens_at)
    if beat_moment(index) < opens_at.astimezone(UTC):
        index += 1  # kapsuła nie może się otworzyć ANI chwili przed zadanym czasem
    if index <= beat_index(datetime.now(UTC)):
        raise ValueError(tr("Chwila otwarcia musi być w przyszłości."))
    body = zip_paths(paths)
    payload = pack_payload({"kind": "file", "name": f"{name}.zip", "type": "application/zip"}, body)
    escrow = EscrowSealer()
    sealers = [DrandSealer(QUICKNET), BeatSealer(operator or dict(BUILTIN_OPERATOR)), escrow]
    hint = beat_moment(index).strftime("%Y-%m-%dT%H:%M:%S.") + f"{beat_moment(index).microsecond // 1000:03d}Z"
    target_dir.mkdir(parents=True, exist_ok=True)
    blob = io.BytesIO() if len(payload) > INLINE_MAX else None
    envelope = seal(payload, index=index, sealers=sealers, t=2, hint=hint, blob_out=blob)
    ident = envelope_id(envelope)
    envelope_path = target_dir / f"capsule-{ident}{ENVELOPE_SUFFIX}"
    envelope_path.write_bytes(canonical(envelope))
    blob_path = None
    if blob is not None:
        blob_path = target_dir / f"capsule-{ident}{BLOB_SUFFIX}"
        blob_path.write_bytes(blob.getvalue())
    code = recovery_code(ident, escrow.x, escrow.share)  # type: ignore[arg-type]
    escrow.x = escrow.share = None
    return SealedCapsule(envelope_path, blob_path, ident, code, beat_moment(index))


def capsule_dir_name(name: str, opens_at: datetime) -> str:
    safe = "".join(ch for ch in name if ch.isalnum() or ch in " -_.").strip() or "kapsula"
    return f"{safe} — {opens_at.astimezone().strftime('%Y-%m-%d')}"


__all__ = ["QUICKNET", "SealedCapsule", "beat_index", "beat_moment", "open_payload", "seal", "seal_files",
           "unpack_payload"]
