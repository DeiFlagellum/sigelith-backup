"""IBE Boneh-Franklina na BLS12-381 — zgodne co do bitu z tlock-js 0.9.0 (drand/tlock).

Kapsuła czasu (capsule.py, format ``beattime-seal-v1``) szyfruje udziały sekretu
„do przyszłości”: do tożsamości rundy drand i do tożsamości @beatu na serwerze
kluczy Sigelith. Klucz prywatny takiej tożsamości (podpis BLS) powstaje dopiero
w tamtej chwili, więc wcześniej nikt — także wydawca — udziału nie odszyfruje.

Schemat ``bls-unchained-g1-rfc9380`` (drand quicknet, beat-key): tożsamość
i podpisy na G1, klucz publiczny na G2. Odpowiednik ``encryptOnG2RFC9380``
i ``decryptOnG2`` z tlock-js — nazwa mówi, gdzie leży U, nie tożsamość.

Arytmetykę krzywej robi py_ecc (Ethereum Foundation, MIT) — tej części nie
piszemy sami. Z jego podpakietu ``py_ecc.bls`` przenieśliśmy tylko hash do G1
(RFC 9380) i kompresję punktów, dosłownie: ``py_ecc.bls`` ciągnie przy imporcie
eth-utils i pydantic (pół sekundy i kilka megabajtów w pakiecie), a nam potrzebny
jest wyłącznie rdzeń ``py_ecc.optimized_bls12_381``.

Dwie rzeczy trzeba było dopasować do tlock-js (noble-curves), bo obie
biblioteki liczą POPRAWNE, ale różne parowania; sprawdzone na żywo w obie
strony z apps/web/static/web/seal/ibe.js (tests/test_capsule.py):

* ``pairing_gt`` = sprzężenie(py_ecc.pairing(Q, P) ** 3): noble sprzęga wynik
  pętli Millera (ujemny parametr x krzywej) i liczy trudną część końcowego
  potęgowania dla 3·(p⁴−p²+1)/r;
* ``gt_bytes`` — serializacja jak ``fp12ToBytes``: wieża Fp2/Fp6/Fp12, w każdym
  poziomie najpierw wyższy współczynnik. py_ecc trzyma Fp12 płasko
  (w¹², w⁶ = 1 + u), więc współczynniki są przeliczane.
"""

from __future__ import annotations

import functools
import hashlib
import os

from py_ecc.optimized_bls12_381 import (
    FQ,
    FQ2,
    G2,
    Z1,
    Z2,
    add,
    b,
    b2,
    curve_order,
    eq,
    field_modulus,
    is_inf,
    is_on_curve,
    iso_map_G1,
    multiply,
    multiply_clear_cofactor_G1,
    normalize,
    optimized_swu_G1,
    pairing,
)

SCHEME = "bls-unchained-g1-rfc9380"
DST_G1 = b"BLS_SIG_BLS12381G1_XMD:SHA-256_SSWU_RO_NUL_"
U_LEN = 96  # punkt G2, postać skompresowana


_P = field_modulus
_POW_2_381 = 1 << 381
_C_FLAG = 1 << 383  # postać skompresowana
_B_FLAG = 1 << 382  # punkt w nieskończoności
_A_FLAG = 1 << 381  # „większe” y


class IbeError(ValueError):
    """Szyfrogram nie pasuje do podpisu (kontrola rP == U) albo zły punkt."""


# ------------------------------------------------------------------ z py_ecc.bls (MIT)


def _expand_message_xmd(message: bytes, dst: bytes, length: int) -> bytes:
    """RFC 9380 §5.3.1 z SHA-256."""
    dst_prime = dst + bytes([len(dst)])
    b0 = hashlib.sha256(bytes(64) + message + length.to_bytes(2, "big") + b"\x00" + dst_prime).digest()
    blocks = [hashlib.sha256(b0 + b"\x01" + dst_prime).digest()]
    for i in range(2, -(-length // 32) + 1):
        blocks.append(hashlib.sha256(_xor(b0, blocks[-1]) + bytes([i]) + dst_prime).digest())
    return b"".join(blocks)[:length]


def hash_to_g1(message: bytes, dst: bytes = DST_G1):
    """RFC 9380 hash_to_curve, zestaw BLS12381G1_XMD:SHA-256_SSWU_RO_."""
    raw = _expand_message_xmd(message, dst, 128)
    u0, u1 = (FQ(int.from_bytes(raw[i:i + 64], "big") % _P) for i in (0, 64))
    return multiply_clear_cofactor_G1(add(iso_map_G1(*optimized_swu_G1(u0)), iso_map_G1(*optimized_swu_G1(u1))))


def _g1_decompress(z: int):
    if not z & _C_FLAG:
        raise IbeError("a compressed G1 point needs the C flag")
    x = z % _POW_2_381
    if z & _B_FLAG:
        if x or z & _A_FLAG:
            raise IbeError("malformed G1 point at infinity")
        return Z1
    if x >= _P:
        raise IbeError("G1 x coordinate out of range")
    rhs = (x**3 + b.n) % _P
    y = pow(rhs, (_P + 1) // 4, _P)
    if pow(y, 2, _P) != rhs:
        raise IbeError("the point is not on G1")
    if (y * 2) // _P != bool(z & _A_FLAG):
        y = _P - y
    return (FQ(x), FQ(y), FQ(1))


def _g1_compress(point) -> int:
    if is_inf(point):
        return _C_FLAG | _B_FLAG
    x, y = normalize(point)
    return x.n | _C_FLAG | (_A_FLAG if (y.n * 2) // _P else 0)


@functools.cache
def _eighth_roots() -> tuple:
    order = _P**2 - 1
    return tuple(FQ2([1, 1]) ** ((order * k) // 8) for k in range(8))


def _fq2_sqrt(value):
    roots = _eighth_roots()
    candidate = value ** ((_P**2 - 1 + 8) // 16)
    check = candidate**2 / value
    if check not in roots[::2]:
        return None
    x1 = candidate / roots[roots.index(check) // 2]
    x2 = -x1
    (re1, im1), (re2, im2) = x1.coeffs, x2.coeffs
    return x1 if (im1 > im2 or (im1 == im2 and re1 > re2)) else x2


def _g2_decompress(z1: int, z2: int):
    if not z1 & _C_FLAG:
        raise IbeError("a compressed G2 point needs the C flag")
    x1 = z1 % _POW_2_381
    if z1 & _B_FLAG:
        if x1 or z2 or z1 & _A_FLAG:
            raise IbeError("malformed G2 point at infinity")
        return Z2
    if x1 >= _P or z2 >= _P:
        raise IbeError("G2 x coordinate out of range")
    x = FQ2([z2, x1])
    y = _fq2_sqrt(x**3 + b2)
    if y is None:
        raise IbeError("the point is not on G2")
    y_re, y_im = (int(c) for c in y.coeffs)
    if (y_im * 2 if y_im else y_re * 2) // _P != bool(z1 & _A_FLAG):
        y = -y
    point = (x, y, FQ2([1, 0]))
    if not is_on_curve(point, b2):
        raise IbeError("the point is not on G2")
    return point


def _g2_compress(point) -> tuple[int, int]:
    if is_inf(point):
        return _C_FLAG | _B_FLAG, 0
    x, y = normalize(point)
    x_re, x_im = (int(c) for c in x.coeffs)
    y_re, y_im = (int(c) for c in y.coeffs)
    a_flag = (y_im * 2 if y_im else y_re * 2) // _P
    return x_im | _C_FLAG | (_A_FLAG if a_flag else 0), x_re


# ------------------------------------------------------------------ IBE


def g2_from_bytes(raw: bytes):
    if len(raw) != 96:
        raise IbeError("a G2 point must be 96 bytes")
    return _g2_decompress(int.from_bytes(raw[:48], "big"), int.from_bytes(raw[48:], "big"))


def g2_to_bytes(point) -> bytes:
    z1, z2 = _g2_compress(point)
    return z1.to_bytes(48, "big") + z2.to_bytes(48, "big")


def g1_from_bytes(raw: bytes):
    if len(raw) != 48:
        raise IbeError("a G1 point must be 48 bytes")
    return _g1_decompress(int.from_bytes(raw, "big"))


def g1_to_bytes(point) -> bytes:
    return _g1_compress(point).to_bytes(48, "big")


def _conjugate(x):
    c = list(x.coeffs)
    return type(x)([(-c[i]) % field_modulus if i % 2 else c[i] for i in range(12)])


def pairing_gt(q_g2, p_g1):
    """Parowanie e(P, Q) w konwencji noble-curves / tlock-js (patrz opis modułu)."""
    return _conjugate(pairing(q_g2, p_g1) ** 3)


def gt_bytes(x) -> bytes:
    """``fp12ToBytes`` z tlock-js: 576 bajtów, wieża Fp2/Fp6/Fp12, wyższe współczynniki najpierw."""
    f = [int(c) % field_modulus for c in x.coeffs]  # baza 1, w, …, w¹¹ nad Fp; w⁶ = 1 + u
    parts = {k: ((f[k] + f[k + 6]) % field_modulus, f[k + 6]) for k in range(6)}
    out = bytearray()
    # c1 (Fp6: w¹, w³, w⁵), potem c0 (w⁰, w², w⁴); w Fp6 kolejność c2, c1, c0; w Fp2 najpierw u.
    for k in (5, 3, 1, 4, 2, 0):
        real, imag = parts[k]
        out += imag.to_bytes(48, "big") + real.to_bytes(48, "big")
    return bytes(out)


def _h2(gt, n: int) -> bytes:
    return hashlib.sha256(b"IBE-H2" + gt_bytes(gt)).digest()[:n]


def _h3(sigma: bytes, msg: bytes) -> int:
    h = hashlib.sha256(b"IBE-H3" + sigma + msg).digest()
    for n in range(1, 65535):
        candidate = bytearray(hashlib.sha256(n.to_bytes(2, "little") + h).digest())
        candidate[0] >>= 1
        value = int.from_bytes(candidate, "big")
        if value < curve_order:
            return value
    raise IbeError("H3 found no value")  # praktycznie nieosiągalne


def _h4(sigma: bytes, n: int) -> bytes:
    return hashlib.sha256(b"IBE-H4" + sigma).digest()[:n]


def _xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b, strict=True))


def encrypt(public_key: bytes, identity: bytes, message: bytes, sigma: bytes | None = None) -> bytes:
    """Szyfruje do 32 bajtów; wynik U‖V‖W (treść stanzy tlock), jak ``sealShare`` w beacons.js."""
    if not 0 < len(message) <= 32:
        raise IbeError("IBE encrypts 1 to 32 bytes")
    point = hash_to_g1(identity)
    gid = pairing_gt(g2_from_bytes(public_key), point)
    sigma = sigma if sigma is not None else os.urandom(len(message))
    r = _h3(sigma, message)
    u = multiply(G2, r)
    v = _xor(sigma, _h2(gid ** r, len(message)))
    w = _xor(message, _h4(sigma, len(message)))
    return g2_to_bytes(u) + v + w


def decrypt(signature: bytes, ciphertext: bytes) -> bytes:
    """Odszyfrowuje U‖V‖W podpisem BLS tożsamości (G1). ``IbeError`` = podpis nie pasuje."""
    rest = len(ciphertext) - U_LEN
    if rest <= 0 or rest % 2:
        raise IbeError(f"unexpected share ciphertext length: {len(ciphertext)} B")
    half = rest // 2
    u_raw, v, w = ciphertext[:U_LEN], ciphertext[U_LEN:U_LEN + half], ciphertext[U_LEN + half:]
    u = g2_from_bytes(u_raw)
    sigma = _xor(_h2(pairing_gt(u, g1_from_bytes(signature)), len(w)), v)
    message = _xor(_h4(sigma, len(w)), w)
    if not eq(multiply(G2, _h3(sigma, message)), u):
        raise IbeError("the share does not match the signature (rP == U check failed)")
    return message


def identity_signature(secret: int, identity: bytes) -> bytes:
    """Podpis BLS tożsamości kluczem ``secret`` — tylko do testów (tak liczy serwer kluczy)."""
    return g1_to_bytes(multiply(hash_to_g1(identity), secret % curve_order))


def public_key_for(secret: int) -> bytes:
    """Klucz publiczny G2 dla ``secret`` — tylko do testów."""
    return g2_to_bytes(multiply(G2, secret % curve_order))
