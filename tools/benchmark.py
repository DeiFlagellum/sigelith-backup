"""Pomiar wydajności poprawek względem wersji 1.x.

Porównuje na tym samym zbiorze danych:

1. algorytm porównywania snapshotów z 1.x (``O(N×M)``, dopasowanie po literze dysku)
   z obecnym indeksem słownikowym (``O(N+M)``);
2. koszt wyprowadzania klucza per plik (1.x) z wyprowadzaniem raz na sesję (2.0);
3. czas pierwszej i kolejnej kopii przyrostowej — czyli to, co użytkownik
   faktycznie odczuwa.

Uruchomienie::

    .venv\\Scripts\\python.exe tools\\benchmark.py
"""

from __future__ import annotations

import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cleanvault import crypto, engine
from cleanvault.crypto import KdfParams, PasswordKeyring
from cleanvault.engine import BackupConfig, Reporter

FILES = 2_000
FILE_SIZE = 2 * 1024


# --------------------------------------------------------- algorytm z wersji 1.x


def legacy_compare(source_snap: dict, dest_snap: dict) -> list:
    """Dokładna kopia ``LBMA.compare_snapshots`` z wersji 1.x."""
    changed = []
    for path, meta in source_snap.items():
        rel_path = os.path.relpath(path, start=list(source_snap.keys())[0].split(os.sep)[0])  # noqa: RUF015
        dest_match = [
            p
            for p in dest_snap
            if rel_path == os.path.relpath(p, start=list(dest_snap.keys())[0].split(os.sep)[0])  # noqa: RUF015
        ]
        if not dest_match:
            changed.append(path)
        else:
            d_meta = dest_snap[dest_match[0]]
            if (
                meta["mtime"] > d_meta["mtime"]
                or meta["size"] != d_meta["size"]
                or meta["hash"] != d_meta["hash"]
            ):
                changed.append(path)
    return changed


def modern_compare(source_snap: dict, dest_index: dict) -> list:
    changed = []
    for key, meta in source_snap.items():
        previous = dest_index.get(key)
        if previous is None or meta["size"] != previous["size"] or meta["hash"] != previous["hash"]:
            changed.append(key)
    return changed


def bench_compare(count: int = 400) -> None:
    print(f"\n1) Porównywanie snapshotów — {count} plików po obu stronach")
    meta = {"mtime": 1_700_000_000.0, "size": 100, "hash": "a" * 64}
    src = {rf"D:\Dane\pod{i % 50}\plik{i}.txt": meta for i in range(count)}
    dst = {rf"E:\Kopia\pod{i % 50}\plik{i}.txt": meta for i in range(count)}
    src_idx = {f"Dane/pod{i % 50}/plik{i}.txt": meta for i in range(count)}
    dst_idx = dict(src_idx)

    start = time.perf_counter()
    legacy_changed = legacy_compare(src, dst)
    legacy_time = time.perf_counter() - start

    start = time.perf_counter()
    modern_changed = modern_compare(src_idx, dst_idx)
    modern_time = time.perf_counter() - start

    print(f"   1.x : {legacy_time:8.3f} s -> uznane za zmienione: {len(legacy_changed)}/{count}")
    print(f"   2.0 : {modern_time:8.3f} s -> uznane za zmienione: {len(modern_changed)}/{count}")
    print(f"   przyspieszenie: {legacy_time / max(modern_time, 1e-9):,.0f}x".replace(",", " "))
    print(f"   poprawnosc 1.x: {'BLAD - uznaje wszystko za zmienione' if legacy_changed else 'ok'}")
    # Algorytm 1.x jest kwadratowy, więc czas rośnie z kwadratem liczby plików.
    for scale in (10_000, 50_000):
        factor = (scale / count) ** 2
        print(f"   ekstrapolacja 1.x dla {scale:,} plikow: {legacy_time * factor / 60:,.0f} min".replace(",", " "))


def bench_kdf(files: int = 500) -> None:
    print(f"\n2) Wyprowadzanie klucza przy szyfrowaniu {files} plików")
    params = KdfParams(crypto.KDF_PBKDF2_SHA256, os.urandom(16), 100_000)

    start = time.perf_counter()
    for _ in range(5):
        PasswordKeyring("hasło", params).key_for(params)
    per_derivation = (time.perf_counter() - start) / 5

    ring = PasswordKeyring("hasło", params)
    ring.key_for(params)
    start = time.perf_counter()
    for _ in range(files):
        ring.key_for(params)
    cached_total = time.perf_counter() - start

    legacy_total = per_derivation * files
    print(f"   jedno wyprowadzenie klucza (PBKDF2 100k): {per_derivation * 1000:.1f} ms")
    print(f"   1.x (raz na plik) : {legacy_total:8.2f} s")
    print(f"   2.0 (raz na sesję): {per_derivation + cached_total:8.2f} s")
    print(f"   przyspieszenie: {legacy_total / max(per_derivation + cached_total, 1e-9):,.0f}x".replace(",", " "))


def bench_backup() -> None:
    print(f"\n3) Realny przebieg kopii — {FILES} plików po {FILE_SIZE} B")
    root = Path(tempfile.mkdtemp(prefix="cv-bench-"))
    try:
        src = root / "zrodlo"
        for i in range(FILES):
            folder = src / f"katalog{i % 40}"
            folder.mkdir(parents=True, exist_ok=True)
            (folder / f"plik{i}.bin").write_bytes(os.urandom(FILE_SIZE))

        def timed_backup(destination: Path, verify: bool):
            config = BackupConfig(
                sources=[str(src)],
                destination=str(destination),
                structure="mirror",
                verify_after_write=verify,
                excludes=[],
            )
            start = time.perf_counter()
            plan = engine.plan_backup(config, Reporter())
            result = engine.run_backup(plan, None, Reporter())
            return time.perf_counter() - start, result, config

        # Przebieg rozgrzewający. Bez niego pierwszy mierzony wynik obejmuje
        # zimny cache systemu plików i skanowanie przez program antywirusowy,
        # co potrafi odwrócić kolejność wyników.
        timed_backup(root / "rozgrzewka", verify=False)
        shutil.rmtree(root / "rozgrzewka", ignore_errors=True)

        first, result, config = timed_backup(root / "kopia", verify=False)
        print(f"   pierwsza kopia (bez weryfikacji): {first:6.2f} s ({result.files_done} plików)")

        verified, _, _ = timed_backup(root / "kopia-w", verify=True)
        print(f"   pierwsza kopia (z weryfikacją)  : {verified:6.2f} s "
              f"({(verified / first - 1) * 100:+.0f}% względem powyższej)")

        start = time.perf_counter()
        plan2 = engine.plan_backup(config, Reporter())
        result2 = engine.run_backup(plan2, None, Reporter())
        second = time.perf_counter() - start
        print(f"   druga, przyrostowa              : {second:6.2f} s "
              f"({result2.files_done} plików skopiowanych)")
        print(f"   przyspieszenie kolejnego przebiegu: {first / max(second, 1e-9):.1f}x")
        if result2.files_done:
            print("   UWAGA: drugi przebieg nie powinien kopiować niczego!")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def bench_encryption() -> None:
    print("\n4) Przepustowość szyfrowania AES-256-GCM")
    root = Path(tempfile.mkdtemp(prefix="cv-crypt-"))
    try:
        size = 64 * 1024 * 1024
        src = root / "duzy.bin"
        src.write_bytes(os.urandom(size))
        ring = PasswordKeyring("hasło", KdfParams(crypto.KDF_PBKDF2_SHA256, b"s" * 16, 1000))

        start = time.perf_counter()
        written = crypto.encrypt_file(src, root / "duzy.cvlt", ring)
        enc_time = time.perf_counter() - start

        start = time.perf_counter()
        crypto.decrypt_file(root / "duzy.cvlt", root / "odzyskany.bin", ring)
        dec_time = time.perf_counter() - start

        mb = size / 1024 / 1024
        print(f"   szyfrowanie   : {mb / enc_time:6.0f} MB/s")
        print(f"   odszyfrowanie : {mb / dec_time:6.0f} MB/s")
        print(f"   narzut rozmiaru: {written - size} B (1.x przez base64+JSON: ~{int(size * 0.33):,} B)".replace(",", " "))
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main() -> int:
    print("=" * 74)
    print("Sigelith Backup — pomiar skuteczności poprawek")
    print("=" * 74)
    bench_compare()
    bench_kdf()
    bench_backup()
    bench_encryption()
    print("\n" + "=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
