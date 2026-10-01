"""Testy kopii równoległej, punktów kontrolnych i weryfikacji odroczonej.

Najważniejsze są testy przerwania: kopia wielu plików naraz nie może zostawić
na nośniku pliku, który wygląda na kompletny, a nim nie jest, ani zgubić
informacji o plikach zapisanych do końca.
"""

from __future__ import annotations

import os
import stat
import threading
import time

import pytest

from cleanvault import crypto, engine, snapshot
from cleanvault.crypto import KdfParams, PasswordKeyring
from cleanvault.engine import BackupConfig, EngineError, Reporter
from cleanvault.parallel import DirectoryCache, resolve_workers, unordered_map
from cleanvault.paths import JOURNAL_NAME, MANIFEST_NAME, supports_hardlinks
from cleanvault.snapshot import (
    Manifest,
    ManifestJournal,
    ManifestSummary,
    SourceRoot,
    is_excluded,
    scan_sources,
)


def make_tree(root, name="Dane", dirs=12, per_dir=25):
    source = root / name
    for d in range(dirs):
        folder = source / f"kat{d:02d}" / "pod"
        folder.mkdir(parents=True)
        for i in range(per_dir):
            (folder / f"plik{i:03d}.bin").write_bytes(os.urandom(512 + (d * 37 + i * 101) % 6000))
    return source


def config_for(source, dest, **kwargs) -> BackupConfig:
    params = dict(
        sources=[str(source)],
        destination=str(dest),
        structure="dated",
        verify_after_write=False,
        excludes=[],
        catchup_passes=0,
        workers=8,
        # Dopisywanie daty uzupełnienia do nazwy wersji sprawdza test_version_names.py.
        stamp_updates=False,
    )
    params.update(kwargs)
    return BackupConfig(**params)


def run(config, reporter=None, keyring=None):
    plan = engine.plan_backup(config, Reporter())
    return plan, engine.run_backup(plan, keyring, reporter or Reporter())


class CancelAfterFiles:
    """Przerywa kopię po rozpoczęciu ``n`` plików — w trybie równoległym moment jest losowy."""

    def __init__(self, n: int) -> None:
        self.n = n
        self.count = 0
        self.lock = threading.Lock()
        self.event = threading.Event()

    def reporter(self) -> Reporter:
        def on_file(_name, _index, _total):
            with self.lock:
                self.count += 1
                if self.count >= self.n:
                    self.event.set()

        return Reporter(on_file=on_file, is_cancelled=self.event.is_set)


def stored_files(dest, version):
    return {p.relative_to(dest / version).as_posix(): p for p in (dest / version).rglob("*") if p.is_file()}


# -------------------------------------------------------------- narzędzia


def test_unordered_map_returns_every_result_and_error():
    def work(n):
        if n % 7 == 0:
            raise ValueError(f"zły {n}")
        return n * 2

    results = list(unordered_map(work, range(100), 8, lambda: False))
    assert len(results) == 100
    errors = [item for item, _res, err in results if err is not None]
    assert sorted(errors) == [n for n in range(100) if n % 7 == 0]
    assert all(res == item * 2 for item, res, err in results if err is None)


def test_unordered_map_stops_submitting_but_returns_started_work():
    started = []
    stop = threading.Event()

    def work(n):
        started.append(n)
        if len(started) >= 20:
            stop.set()
        time.sleep(0.002)
        return n

    results = list(unordered_map(work, range(10_000), 4, stop.is_set))
    assert len(results) == len(started), "wynik zadania, które ruszyło, zginął"
    assert len(started) < 200, "po przerwaniu nadal wysyłano nowe zadania"


def test_unordered_map_single_worker_keeps_order():
    assert [item for item, _r, _e in unordered_map(lambda n: n, range(50), 1, lambda: False)] == list(range(50))


def test_resolve_workers_bounds():
    assert resolve_workers(0) >= 4
    assert resolve_workers(1) == 1
    assert resolve_workers(10_000) == 64


def test_directory_cache_creates_once(tmp_path):
    cache = DirectoryCache()
    target = tmp_path / "a" / "b" / "c"
    cache.ensure(target)
    cache.ensure(target)
    assert target.is_dir()


# ------------------------------------------------------------ kopia równoległa


def test_parallel_backup_copies_everything_exactly(tmp_path):
    source = make_tree(tmp_path)
    dest = tmp_path / "cel"
    plan, result = run(config_for(source, dest))

    assert result.ok and result.files_done == 300
    stored = stored_files(dest, plan.version)
    assert len(stored) == 300
    assert not [name for name in stored if name.endswith(".part")]
    for rel, path in stored.items():
        original = source / rel.partition("/")[2]
        assert path.read_bytes() == original.read_bytes()
        # Czas modyfikacji źródła jest znakiem „plik kompletny” dla wznawiania.
        assert abs(path.stat().st_mtime - original.stat().st_mtime) < 0.01
    manifest = Manifest.load(dest)
    assert len(manifest.entries) == 300
    assert manifest.runs[plan.version].complete
    assert not (dest / JOURNAL_NAME).exists(), "dziennik po ukończonej kopii powinien zostać wchłonięty"


def test_parallel_and_sequential_backups_agree(tmp_path):
    source = make_tree(tmp_path, dirs=5, per_dir=10)
    _, par = run(config_for(source, tmp_path / "rownolegle", workers=16))
    _, seq = run(config_for(source, tmp_path / "sekwencyjnie", workers=1))
    a = Manifest.load(tmp_path / "rownolegle").entries
    b = Manifest.load(tmp_path / "sekwencyjnie").entries
    assert set(a) == set(b)
    assert all(a[k].sha256 == b[k].sha256 for k in a)
    assert par.files_done == seq.files_done == 50


@pytest.mark.parametrize("stop_after", [1, 37, 150, 299])
def test_parallel_interruption_never_leaves_a_fake_complete_file(tmp_path, stop_after):
    """Po przerwaniu w dowolnym momencie: plik z czasem modyfikacji źródła ma pełną treść,
    dziennik zna tylko pliki faktycznie zapisane, a wznowienie domyka kopię bajt w bajt."""
    source = make_tree(tmp_path)
    dest = tmp_path / "cel"
    config = config_for(source, dest, workers=8)
    plan = engine.plan_backup(config, Reporter())
    result = engine.run_backup(plan, None, CancelAfterFiles(stop_after).reporter())
    assert result.cancelled

    stored = stored_files(dest, plan.version)
    assert not [name for name in stored if name.endswith(".part")], "zostały pliki tymczasowe"
    for rel, path in stored.items():
        original = source / rel.partition("/")[2]
        if abs(path.stat().st_mtime - original.stat().st_mtime) < 0.01:
            assert path.read_bytes() == original.read_bytes(), f"{rel}: wygląda na kompletny, a nie jest"

    manifest = Manifest.load(dest)
    assert len(manifest.entries) == result.files_done
    for entry in manifest.entries.values():
        assert (dest / entry.stored).exists()

    resume = engine.plan_backup(config_for(source, dest, target_version=plan.version), Reporter())
    assert len(resume.adopted) + len(resume.to_copy) == 300
    finished = engine.run_backup(resume, None, Reporter())
    assert finished.ok
    final = Manifest.load(dest)
    assert len(final.entries) == 300 and final.runs[plan.version].complete
    for rel, path in stored_files(dest, plan.version).items():
        assert path.read_bytes() == (source / rel.partition("/")[2]).read_bytes()


# ------------------------------------------------------ punkty kontrolne


def test_cancelled_first_backup_lives_in_journal(tmp_path, monkeypatch):
    """Przerwanie nie zapisuje pełnego manifestu — stan odtwarza się z dziennika."""
    monkeypatch.setattr(engine, "CHECKPOINT_FILES", 10)
    source = make_tree(tmp_path, dirs=4, per_dir=25)
    dest = tmp_path / "cel"
    plan = engine.plan_backup(config_for(source, dest, workers=1), Reporter())
    result = engine.run_backup(plan, None, CancelAfterFiles(40).reporter())
    assert result.cancelled and result.files_done > 0

    assert not (dest / MANIFEST_NAME).exists()
    frames = list(ManifestJournal(dest).frames())
    assert len(frames) >= 3, "punkty kontrolne powinny zapisywać się w trakcie kopii"

    summary = ManifestSummary.load(dest)
    assert summary is not None
    run_state = summary.runs[plan.version]
    assert not run_state.complete and run_state.done_files == result.files_done

    manifest = Manifest.load(dest)
    assert len(manifest.entries) == result.files_done
    assert all(entry.sha256 for entry in manifest.entries.values())


def test_torn_journal_tail_is_ignored(tmp_path):
    source = make_tree(tmp_path, dirs=2, per_dir=10)
    dest = tmp_path / "cel"
    plan = engine.plan_backup(config_for(source, dest, workers=1), Reporter())
    result = engine.run_backup(plan, None, CancelAfterFiles(8).reporter())
    before = len(Manifest.load(dest).entries)
    assert before == result.files_done

    with open(dest / JOURNAL_NAME, "ab") as handle:
        handle.write(snapshot.JOURNAL_MAGIC + b"\x00" * 20)  # urwana paczka po wyłączeniu zasilania
    assert len(Manifest.load(dest).entries) == before


def test_journal_older_than_manifest_is_skipped(tmp_path):
    manifest = Manifest.load(tmp_path)
    manifest.entries["a/x"] = snapshot.ManifestEntry(1, 1.0, "abc", "a/x")
    ManifestJournal(tmp_path).append([{"t": "del", "k": "a/x"}])
    time.sleep(0.01)
    manifest.save()
    # Dziennik z usunięciem powstał przed zapisem manifestu — nie może go cofnąć.
    ManifestJournal(tmp_path).append([{"t": "set", "k": "a/y", "e": snapshot.ManifestEntry(2, 2.0, "", "a/y").to_dict()}])
    reloaded = Manifest.load(tmp_path)
    assert set(reloaded.entries) == {"a/x", "a/y"}


# ------------------------------------------------------ bezpieczeństwo zapisu


@pytest.mark.skipif(os.name != "nt", reason="dowiązania testujemy na NTFS")
def test_rewriting_file_in_version_does_not_touch_older_version(tmp_path):
    """Plik w nowej wersji bywa twardym dowiązaniem do starszej — zapis w miejscu zmieniłby obie."""
    if not supports_hardlinks(tmp_path):
        pytest.skip("brak twardych dowiązań")
    source = make_tree(tmp_path, dirs=1, per_dir=3)
    dest = tmp_path / "cel"
    first, _ = run(config_for(source, dest))
    (source / "kat00" / "pod" / "nowy.bin").write_bytes(b"wymusza nowa wersje")
    second, _ = run(config_for(source, dest))
    shared = "Dane/kat00/pod/plik000.bin"
    old_copy = dest / first.version / shared
    new_copy = dest / second.version / shared
    assert os.stat(new_copy).st_nlink == 2, "plik niezmieniony powinien być dowiązaniem"
    original = old_copy.read_bytes()

    changed = source / "kat00" / "pod" / "plik000.bin"
    changed.write_bytes(b"NOWA TRESC " * 100)
    later = changed.stat().st_mtime + 60
    os.utime(changed, (later, later))
    run(config_for(source, dest, target_version=second.version))

    assert new_copy.read_bytes() == changed.read_bytes()
    assert old_copy.read_bytes() == original, "nadpisanie w nowej wersji zmieniło starszą wersję"


def test_read_only_source_does_not_make_backup_read_only(tmp_path):
    source = make_tree(tmp_path, dirs=1, per_dir=2)
    target = source / "kat00" / "pod" / "plik000.bin"
    os.chmod(target, stat.S_IREAD)
    try:
        plan, result = run(config_for(source, tmp_path / "cel"))
        copy = tmp_path / "cel" / plan.version / "Dane" / "kat00" / "pod" / "plik000.bin"
        assert result.ok and os.access(copy, os.W_OK)
    finally:
        os.chmod(target, stat.S_IWRITE | stat.S_IREAD)


def test_retention_removes_version_with_read_only_files(tmp_path, monkeypatch):
    """Kopie ze starszej wersji programu miały pliki „tylko do odczytu” — retencja musi je usunąć."""
    stamps = iter(["2026-01-01_@416", "2026-01-02_@416", "2026-01-03_@416"])
    monkeypatch.setattr(engine.beat, "stamp", lambda *a: next(stamps))
    source = make_tree(tmp_path, dirs=1, per_dir=2)
    dest = tmp_path / "cel"
    first, _ = run(config_for(source, dest, retention=1))
    for path in (dest / first.version).rglob("*.bin"):
        os.chmod(path, stat.S_IREAD)
    (source / "kat00" / "pod" / "plik000.bin").write_bytes(b"zmiana")
    run(config_for(source, dest, retention=1))
    assert not (dest / first.version).exists(), "wersja z plikami tylko do odczytu nie została usunięta"


# -------------------------------------------------------------- wykluczenia


@pytest.mark.parametrize(
    ("rel", "is_dir", "expected"),
    [
        ("proj/node_modules", True, True),
        ("proj/node_modules/pkg/index.js", False, True),
        ("a/b/.venv/Lib/site.py", False, True),
        ("proj/src/__pycache__", True, True),
        ("proj/build", False, False),  # plik o nazwie „build” to nie katalog „build/”
        ("proj/build", True, True),
        ("proj/src/main.py", False, False),
    ],
)
def test_single_name_directory_patterns_match_at_any_depth(rel, is_dir, expected):
    patterns = ["node_modules/*", ".venv/*", "__pycache__/*", "build/*"]
    assert is_excluded(rel, rel.rpartition("/")[2], patterns, is_dir=is_dir) is expected


def test_multi_part_patterns_stay_anchored():
    assert is_excluded("docs/stare/plik.txt", "plik.txt", ["docs/stare/*"])
    assert not is_excluded("inny/docs/stare/plik.txt", "plik.txt", ["docs/stare/*"])


def test_scan_skips_nested_regenerable_directories(tmp_path):
    source = tmp_path / "Repo"
    for folder in ("proj/src", "proj/.venv/Lib", "proj/web/node_modules/pkg"):
        (source / folder).mkdir(parents=True)
    (source / "proj/src/main.py").write_text("x", encoding="utf-8")
    (source / "proj/.venv/Lib/site.py").write_text("x", encoding="utf-8")
    (source / "proj/web/node_modules/pkg/i.js").write_text("x", encoding="utf-8")
    result = scan_sources([SourceRoot.make(source)], [".venv/*", "node_modules/*"])
    assert set(result) == {"Repo/proj/src/main.py"}


def test_parallel_scan_matches_sequential(tmp_path):
    source = make_tree(tmp_path, dirs=20, per_dir=7)
    roots = [SourceRoot.make(source)]
    assert scan_sources(roots, [], workers=1) == scan_sources(roots, [], workers=16)


# ------------------------------------------------------- szacunek miejsca


def test_directories_are_counted_in_physical_size(tmp_path, monkeypatch):
    monkeypatch.setattr(engine, "cluster_size", lambda _p: 262144)
    monkeypatch.setattr(engine, "supports_hardlinks", lambda _p: True)
    source = make_tree(tmp_path, dirs=3, per_dir=1)
    plan = engine.plan_backup(config_for(source, tmp_path / "cel"), Reporter())
    # Dane, 3× katNN, 3× katNN/pod = 7 katalogów, każdy po klastrze.
    assert plan.directories == 7
    assert plan.physical_bytes == 3 * 262144 + 7 * 262144


# --------------------------------------------------- weryfikacja odroczona


def test_verify_backup_passes_for_intact_copy(tmp_path):
    source = make_tree(tmp_path, dirs=3, per_dir=5)
    dest = tmp_path / "cel"
    run(config_for(source, dest))
    report = engine.verify_backup(dest, None, Reporter(), workers=4)
    assert report.ok and report.files_done == 15 and not report.errors


def test_verify_backup_detects_damage_and_missing_files(tmp_path):
    source = make_tree(tmp_path, dirs=2, per_dir=5)
    dest = tmp_path / "cel"
    plan, _ = run(config_for(source, dest))
    files = sorted(stored_files(dest, plan.version).values())
    damaged, missing = files[0], files[1]
    data = bytearray(damaged.read_bytes())
    data[0] ^= 0xFF
    damaged.write_bytes(bytes(data))
    missing.unlink()

    report = engine.verify_backup(dest, None, Reporter())
    assert not report.ok
    assert len(report.errors) == 2
    assert any("sumy kontrolnej" in e for e in report.errors)
    assert any("brak pliku" in e for e in report.errors)


def test_verify_backup_fills_missing_checksums_from_source(tmp_path):
    """Pliki rozpoznane przy wznawianiu nie mają sumy — weryfikacja porównuje je ze źródłem."""
    source = make_tree(tmp_path, dirs=1, per_dir=6)
    dest = tmp_path / "cel"
    run(config_for(source, dest))
    manifest = Manifest.load(dest)
    for key in sorted(manifest.entries)[:4]:  # plik000–003; plik000 zmienimy w źródle
        entry = manifest.entries[key]
        manifest.entries[key] = snapshot.ManifestEntry(entry.size, entry.mtime, "", entry.stored, entry.stored_size)
    manifest.save()
    changed = source / "kat00" / "pod" / "plik000.bin"
    changed.write_bytes(b"zmienione po kopii")

    report = engine.verify_backup(dest, None, Reporter())
    assert report.ok, report.errors
    assert any("uzupełnione w spisie treści" in note for note in report.notes)
    assert any("tylko co do rozmiaru" in note for note in report.notes)
    filled = [e for e in Manifest.load(dest).entries.values() if e.sha256]
    assert len(filled) == 5  # 2 z sumą od początku + 3 uzupełnione; 1 ma zmienione źródło


def test_verify_encrypted_backup_needs_password(tmp_path):
    keyring = PasswordKeyring("Hasło-Testowe", KdfParams(crypto.KDF_PBKDF2_SHA256, b"s" * 16, 1000))
    source = make_tree(tmp_path, dirs=1, per_dir=3)
    dest = tmp_path / "cel"
    run(config_for(source, dest, encrypt=True), keyring=keyring)
    with pytest.raises(EngineError, match="hasło"):
        engine.verify_backup(dest, None, Reporter())
    assert engine.verify_backup(dest, keyring, Reporter()).ok
