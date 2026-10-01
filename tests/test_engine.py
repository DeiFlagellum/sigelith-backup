"""Testy silnika kopii i przywracania.

Najważniejszy test w całym pakiecie to :func:`test_second_backup_copies_nothing`
— pilnuje błędu, przez który „kopia przyrostowa" w 1.x kopiowała za każdym razem
wszystko od nowa.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from cleanvault import crypto, engine, rescue
from cleanvault.crypto import KdfParams, PasswordKeyring
from cleanvault.engine import BackupConfig, EngineError, Reporter
from cleanvault.snapshot import Manifest


@pytest.fixture()
def keyring() -> PasswordKeyring:
    return PasswordKeyring("Test-Hasło", KdfParams(crypto.KDF_PBKDF2_SHA256, b"s" * 16, 1000))


@pytest.fixture()
def tree(tmp_path):
    """Drzewo źródłowe: 3 pliki, w tym jeden w podkatalogu."""
    src = tmp_path / "zrodlo"
    (src / "pod").mkdir(parents=True)
    (src / "a.txt").write_text("alfa", encoding="utf-8")
    (src / "b.bin").write_bytes(os.urandom(4096))
    (src / "pod" / "c.txt").write_text("gamma", encoding="utf-8")
    return src


def make_config(src, dst, **kwargs) -> BackupConfig:
    params = dict(
        sources=[str(src)],
        destination=str(dst),
        structure="mirror",
        encrypt=False,
        verify_after_write=True,
        excludes=[],
        retention=0,
        stamp_updates=False,
    )
    params.update(kwargs)
    return BackupConfig(**params)


def run(config) -> tuple[engine.BackupPlan, engine.OperationResult]:
    reporter = Reporter()
    plan = engine.plan_backup(config, reporter)
    result = engine.run_backup(plan, None, reporter)
    return plan, result


# --------------------------------------------------------- regresja z 1.x


def test_second_backup_copies_nothing(tree, tmp_path):
    """Regresja: w 1.x każdy przebieg kopiował całość, bo porównanie ścieżek
    liczyło ścieżkę względną wobec litery dysku i nigdy się nie zgadzało."""
    dst = tmp_path / "kopia"
    config = make_config(tree, dst)

    first_plan, first = run(config)
    assert first.ok
    assert len(first_plan.to_copy) == 3
    assert first.files_done == 3

    second_plan, second = run(config)
    assert second.ok
    assert second_plan.to_copy == [], "drugi przebieg nie może kopiować niezmienionych plików"
    assert len(second_plan.unchanged) == 3
    assert second.files_done == 0


def test_changed_file_is_detected(tree, tmp_path):
    dst = tmp_path / "kopia"
    config = make_config(tree, dst)
    run(config)

    (tree / "a.txt").write_text("alfa zmieniona", encoding="utf-8")
    plan, result = run(config)

    assert [p.key for p in plan.to_copy] == ["zrodlo/a.txt"]
    assert plan.to_copy[0].reason == "zmieniony"
    assert result.files_done == 1


def test_same_size_different_content_is_detected(tree, tmp_path):
    """Zmiana bez zmiany rozmiaru musi zostać złapana przez SHA-256."""
    dst = tmp_path / "kopia"
    config = make_config(tree, dst, thorough=True)
    run(config)

    target = tree / "a.txt"
    os.utime(target, (1_600_000_000, 1_600_000_000))
    run(config)
    target.write_text("beta", encoding="utf-8")  # ta sama długość co "alfa"
    os.utime(target, (1_600_000_000, 1_600_000_000))  # ten sam mtime!

    plan, _ = run(config)
    assert [p.key for p in plan.to_copy] == ["zrodlo/a.txt"]


def test_file_missing_from_backup_is_recopied(tree, tmp_path):
    dst = tmp_path / "kopia"
    config = make_config(tree, dst)
    run(config)

    (dst / "zrodlo" / "a.txt").unlink()
    plan, _ = run(config)

    assert [p.key for p in plan.to_copy] == ["zrodlo/a.txt"]
    assert plan.to_copy[0].reason == "brak w kopii"


# ------------------------------------------------------------ bezpieczeństwo


def test_destination_inside_source_is_rejected(tree):
    """1.x pozwalało zrobić kopię do podkatalogu źródła — kopia kopiowała samą siebie."""
    config = make_config(tree, tree / "kopia_w_srodku")
    with pytest.raises(EngineError, match="wewnątrz źródła"):
        engine.plan_backup(config, Reporter())


def test_destination_equal_to_source_is_rejected(tree):
    config = make_config(tree, tree)
    with pytest.raises(EngineError):
        engine.plan_backup(config, Reporter())


def test_missing_source_is_rejected(tmp_path):
    config = make_config(tmp_path / "nie_ma", tmp_path / "cel")
    with pytest.raises(EngineError, match="nie istnieje"):
        engine.plan_backup(config, Reporter())


def test_encryption_without_password_is_refused(tree, tmp_path):
    config = make_config(tree, tmp_path / "kopia", encrypt=True)
    plan = engine.plan_backup(config, Reporter())
    with pytest.raises(EngineError, match="hasła"):
        engine.run_backup(plan, None, Reporter())


def test_plan_does_not_write_anything(tree, tmp_path):
    """Podgląd planu musi być bezpieczny — to podstawa trybu „co się stanie"."""
    dst = tmp_path / "kopia"
    engine.plan_backup(make_config(tree, dst), Reporter())
    assert list(dst.iterdir()) == []


# ------------------------------------------------------------------ szyfrowanie


def test_encrypted_backup_and_restore_roundtrip(tree, tmp_path, keyring):
    dst = tmp_path / "kopia"
    config = make_config(tree, dst, encrypt=True)
    reporter = Reporter()
    plan = engine.plan_backup(config, reporter)
    result = engine.run_backup(plan, keyring, reporter)
    assert result.ok and result.files_done == 3

    stored = list(dst.rglob("*.cvlt"))
    assert len(stored) == 3
    assert crypto.is_encrypted_file(stored[0])

    out = tmp_path / "przywrocone"
    rplan = engine.plan_restore(dst, out, layout="tree")
    rresult = engine.run_restore(rplan, keyring, Reporter())

    assert rresult.ok, rresult.errors
    assert (out / "zrodlo" / "a.txt").read_text(encoding="utf-8") == "alfa"
    assert (out / "zrodlo" / "pod" / "c.txt").read_text(encoding="utf-8") == "gamma"
    assert (out / "zrodlo" / "b.bin").read_bytes() == (tree / "b.bin").read_bytes()


def test_encrypted_incremental_also_works(tree, tmp_path, keyring):
    """1.x nie mógł porównywać kopii szyfrowanych — hash celu nigdy nie
    równa się hashowi źródła. Manifest rozwiązuje to bez czytania kopii."""
    dst = tmp_path / "kopia"
    config = make_config(tree, dst, encrypt=True)
    reporter = Reporter()
    engine.run_backup(engine.plan_backup(config, reporter), keyring, reporter)

    plan = engine.plan_backup(config, reporter)
    assert plan.to_copy == []


def test_restore_needs_password_for_encrypted_backup(tree, tmp_path, keyring):
    dst = tmp_path / "kopia"
    config = make_config(tree, dst, encrypt=True)
    engine.run_backup(engine.plan_backup(config, Reporter()), keyring, Reporter())

    rplan = engine.plan_restore(dst, tmp_path / "out")
    with pytest.raises(EngineError, match="hasło"):
        engine.run_restore(rplan, None, Reporter())


# -------------------------------------------------------------- przywracanie


def test_restore_plain_backup_roundtrip(tree, tmp_path):
    dst = tmp_path / "kopia"
    run(make_config(tree, dst))
    out = tmp_path / "przywrocone"

    plan = engine.plan_restore(dst, out)
    result = engine.run_restore(plan, None, Reporter())

    assert result.ok and result.files_done == 3
    assert (out / "zrodlo" / "a.txt").read_text(encoding="utf-8") == "alfa"


def test_restore_flat_layout(tree, tmp_path):
    dst = tmp_path / "kopia"
    run(make_config(tree, dst))
    out = tmp_path / "plasko"

    plan = engine.plan_restore(dst, out, layout="flat")
    engine.run_restore(plan, None, Reporter())

    names = sorted(p.name for p in out.iterdir())
    assert names == ["a.txt", "b.bin", "c.txt"]


def test_restore_to_original_location(tree, tmp_path):
    """1.x nie zapisywał oryginalnych katalogów, więc ta opcja nie mogła działać."""
    dst = tmp_path / "kopia"
    run(make_config(tree, dst))

    (tree / "a.txt").unlink()
    plan = engine.plan_restore(dst, tmp_path / "nieistotne", layout="original")
    result = engine.run_restore(plan, None, Reporter())

    assert result.ok, result.errors
    assert (tree / "a.txt").read_text(encoding="utf-8") == "alfa"


def test_collision_policy_rename_keeps_existing(tree, tmp_path):
    dst = tmp_path / "kopia"
    run(make_config(tree, dst))
    out = tmp_path / "out"
    (out / "zrodlo").mkdir(parents=True)
    (out / "zrodlo" / "a.txt").write_text("STARE", encoding="utf-8")

    plan = engine.plan_restore(dst, out, collision="rename")
    engine.run_restore(plan, None, Reporter())

    assert (out / "zrodlo" / "a.txt").read_text(encoding="utf-8") == "STARE"
    assert (out / "zrodlo" / "a (1).txt").read_text(encoding="utf-8") == "alfa"


def test_collision_policy_skip(tree, tmp_path):
    dst = tmp_path / "kopia"
    run(make_config(tree, dst))
    out = tmp_path / "out"
    (out / "zrodlo").mkdir(parents=True)
    (out / "zrodlo" / "a.txt").write_text("STARE", encoding="utf-8")

    plan = engine.plan_restore(dst, out, collision="skip")
    result = engine.run_restore(plan, None, Reporter())

    assert (out / "zrodlo" / "a.txt").read_text(encoding="utf-8") == "STARE"
    assert result.skipped == 1


def test_restore_without_manifest_falls_back_to_scan(tree, tmp_path):
    dst = tmp_path / "kopia"
    run(make_config(tree, dst))
    for leftover in dst.glob(".cleanvault-manifest*"):
        leftover.unlink()

    plan = engine.plan_restore(dst, tmp_path / "out")
    assert not plan.from_manifest
    assert len(plan.items) == 3
    assert engine.run_restore(plan, None, Reporter()).ok


# ------------------------------------------------------------------ struktura


def test_multiple_sources_with_same_name_do_not_collide(tmp_path):
    a = tmp_path / "dysk1" / "Foto"
    b = tmp_path / "dysk2" / "Foto"
    a.mkdir(parents=True)
    b.mkdir(parents=True)
    (a / "jeden.txt").write_text("1", encoding="utf-8")
    (b / "dwa.txt").write_text("2", encoding="utf-8")

    dst = tmp_path / "kopia"
    config = make_config(a, dst, sources=[str(a), str(b)])
    plan, result = run(config)

    assert result.ok and result.files_done == 2
    labels = {p.key.split("/")[0] for p in plan.to_copy}
    assert labels == {"Foto", "Foto_2"}


def test_excludes_are_respected(tree, tmp_path):
    (tree / "Thumbs.db").write_text("smiec", encoding="utf-8")
    (tree / "notatka.tmp").write_text("smiec", encoding="utf-8")
    dst = tmp_path / "kopia"

    plan, _ = run(make_config(tree, dst, excludes=["Thumbs.db", "*.tmp"]))
    keys = {p.key for p in plan.to_copy}

    assert "zrodlo/Thumbs.db" not in keys
    assert "zrodlo/notatka.tmp" not in keys
    assert len(keys) == 3


def test_dated_structure_creates_versions_and_shares_data(tree, tmp_path):
    """Niezmienione pliki trafiają do nowej wersji twardym dowiązaniem,
    więc historia nie kosztuje podwójnego miejsca."""
    dst = tmp_path / "kopia"
    config = make_config(tree, dst, structure="dated")

    run(config)
    (tree / "a.txt").write_text("alfa v2", encoding="utf-8")
    run(config)

    versions = sorted(p for p in dst.iterdir() if p.is_dir())
    assert len(versions) == 2
    # Każda wersja jest kompletna — przywracanie nie wymaga sklejania wersji.
    for version in versions:
        assert (version / "zrodlo" / "a.txt").exists()
        assert (version / "zrodlo" / "b.bin").exists()
        assert (version / "zrodlo" / "pod" / "c.txt").exists()

    old_b = versions[0] / "zrodlo" / "b.bin"
    new_b = versions[1] / "zrodlo" / "b.bin"
    if os.name == "nt":
        assert old_b.stat().st_nlink >= 2 or old_b.read_bytes() == new_b.read_bytes()
    assert old_b.read_bytes() == new_b.read_bytes()


def test_retention_removes_oldest_versions(tree, tmp_path, monkeypatch):
    dst = tmp_path / "kopia"
    config = make_config(tree, dst, structure="dated", retention=2)

    stamps = iter(["2026-01-01_@416", "2026-01-02_@416", "2026-01-03_@416"])
    monkeypatch.setattr(engine.beat, "stamp", lambda *a: next(stamps))

    for i in range(3):
        (tree / "a.txt").write_text(f"wersja {i}", encoding="utf-8")
        run(config)

    versions = sorted(p.name for p in dst.iterdir() if p.is_dir())
    assert versions == ["2026-01-02_@416", "2026-01-03_@416"]


def test_removed_source_file_is_kept_by_default(tree, tmp_path):
    """Domyślnie kopia nie kasuje — usunięcie pliku w źródle nie może
    po cichu usunąć jedynej kopii zapasowej."""
    dst = tmp_path / "kopia"
    config = make_config(tree, dst)
    run(config)

    (tree / "a.txt").unlink()
    plan, _ = run(config)

    assert plan.removed == ["zrodlo/a.txt"]
    assert (dst / "zrodlo" / "a.txt").exists()


def test_delete_removed_when_explicitly_enabled(tree, tmp_path):
    dst = tmp_path / "kopia"
    config = make_config(tree, dst, delete_removed=True)
    run(config)

    (tree / "a.txt").unlink()
    run(config)

    assert not (dst / "zrodlo" / "a.txt").exists()
    assert (dst / "zrodlo" / "b.bin").exists()


def test_manifest_survives_reload(tree, tmp_path):
    dst = tmp_path / "kopia"
    run(make_config(tree, dst))

    manifest = Manifest.load(dst)
    assert len(manifest.entries) == 3
    assert manifest.roots == {"zrodlo": str(tree.resolve())}


def test_corrupted_manifest_falls_back_to_full_backup(tree, tmp_path):
    dst = tmp_path / "kopia"
    run(make_config(tree, dst))

    manifest_file = dst / ".cleanvault-manifest"
    blob = bytearray(manifest_file.read_bytes())
    blob[-1] ^= 0xFF
    # Manifest ma atrybut "ukryty", więc podmieniamy go tak jak robi to aplikacja.
    tmp = dst / "uszkodzony.tmp"
    tmp.write_bytes(bytes(blob))
    os.replace(tmp, manifest_file)

    # Uszkodzony manifest nie może wywrócić programu. Nie może też wymusić
    # przepisania całej kopii: pliki leżące już w kopii lustrzanej i zgodne ze
    # źródłem są rozpoznawane z nośnika, a manifest odbudowywany.
    (tree / "a.txt").write_text("zmienione po uszkodzeniu", encoding="utf-8")
    plan, result = run(make_config(tree, dst))
    assert [item.key for item in plan.to_copy] == ["zrodlo/a.txt"]
    assert set(plan.adopted) == {"zrodlo/b.bin", "zrodlo/pod/c.txt"}
    assert result.ok
    rebuilt = Manifest.load(dst)
    assert len(rebuilt.entries) == 3
    assert (dst / "zrodlo" / "a.txt").read_text(encoding="utf-8") == "zmienione po uszkodzeniu"


def test_verify_after_write_detects_bad_write(tree, tmp_path, monkeypatch):
    """Symulujemy nośnik, który zapisuje śmieci — weryfikacja musi to złapać."""
    dst = tmp_path / "kopia"

    real_write = engine._write_stored

    def broken_write(src, target, reporter):
        """Suma kontrolna źródła się zgadza, ale na nośniku lądują śmieci — tak
        zachowuje się nośnik, który przyjął zapis i przekłamał dane."""
        pending = real_write(src, target, reporter)
        os.lseek(pending.fd, 0, os.SEEK_SET)
        os.write(pending.fd, b"USZKODZONE DANE")
        os.ftruncate(pending.fd, 15)
        return pending

    monkeypatch.setattr(engine, "_write_stored", broken_write)
    _, result = run(make_config(tree, dst, verify_after_write=True, catchup_passes=0))

    assert not result.ok
    assert len(result.errors) == 3
    assert "Weryfikacja" in result.errors[0]
    # Plik z czasem modyfikacji źródła, ale złą treścią, zostałby przy
    # wznowieniu uznany za poprawny — nie może zostać na nośniku. Notatka
    # ratunkowa w korzeniu kopii to nie dane, więc jej nie liczymy.
    leftovers = [
        path for path in [*dst.rglob("*.txt"), *dst.rglob("*.bin")]
        if not (path.parent == dst and path.name in rescue.RESCUE_FILES)
    ]
    assert not leftovers


def test_catchup_retries_files_that_failed(tree, tmp_path, monkeypatch):
    """Plik, którego nie udało się zapisać, dostaje drugą szansę w przebiegu
    uzupełniającym — a nie czeka do następnej kopii."""
    dst = tmp_path / "kopia"
    attempts: list[str] = []
    real_write = engine._write_stored

    def flaky(src, target, reporter):
        attempts.append(str(src))
        if len(attempts) <= 3:
            raise OSError("nośnik chwilowo niedostępny")
        return real_write(src, target, reporter)

    monkeypatch.setattr(engine, "_write_stored", flaky)
    _, result = run(make_config(tree, dst, verify_after_write=False, catchup_passes=1, workers=1))

    assert result.files_done == 3, "przebieg uzupełniający nie ponowił nieudanych plików"
    assert result.ok
    assert len(Manifest.load(dst).entries) == 3


def test_result_summary_is_human_readable(tree, tmp_path):
    _, result = run(make_config(tree, tmp_path / "kopia"))
    assert "Gotowe" in result.summary
    assert result.duration >= 0


# ----------------------------------------------------- bezpieczeństwo przywracania


def test_restore_rejects_path_escaping_destination(tree, tmp_path):
    """Manifest z cudzego nośnika nie może zapisać pliku poza katalogiem docelowym.

    Odpowiednik podatności „zip slip": wpis ze ścieżką ``../..`` wyprowadzałby
    zapis do dowolnego miejsca na dysku.
    """
    dst = tmp_path / "kopia"
    run(make_config(tree, dst))

    manifest = Manifest.load(dst)
    entry = next(iter(manifest.entries.values()))
    manifest.entries["../../wyciek.txt"] = entry
    manifest.save()

    out = tmp_path / "out"
    plan = engine.plan_restore(dst, out)
    result = engine.run_restore(plan, None, Reporter())

    assert not (tmp_path.parent / "wyciek.txt").exists()
    assert not (tmp_path / "wyciek.txt").exists()
    assert any("poza katalog" in err for err in result.errors), result.errors


def test_restore_flat_layout_cannot_escape(tree, tmp_path):
    dst = tmp_path / "kopia"
    run(make_config(tree, dst))

    manifest = Manifest.load(dst)
    entry = next(iter(manifest.entries.values()))
    manifest.entries["../../zly.txt"] = entry
    manifest.save()

    out = tmp_path / "plasko"
    engine.run_restore(engine.plan_restore(dst, out, layout="flat"), None, Reporter())

    assert sorted(p.name for p in out.iterdir()) == ["a.txt", "b.bin", "c.txt", "zly.txt"]
    assert not (tmp_path.parent / "zly.txt").exists()


# ------------------------------------------------------ bezpieczeństwo retencji


def test_retention_never_touches_foreign_folders(tree, tmp_path, monkeypatch):
    """Czyszczenie historii nie może skasować katalogu, którego nie utworzyliśmy,
    nawet jeśli jego nazwa wygląda jak nasza data."""
    dst = tmp_path / "kopia"
    dst.mkdir(parents=True)
    intruder = dst / "2020-01-01_00-00-00"
    intruder.mkdir()
    (intruder / "cenne-dane.txt").write_text("nie kasuj mnie", encoding="utf-8")

    config = make_config(tree, dst, structure="dated", retention=1)
    stamps = iter(["2026-05-01_@416", "2026-05-02_@416"])
    monkeypatch.setattr(engine.beat, "stamp", lambda *a: next(stamps))
    run(config)
    (tree / "a.txt").write_text("zmiana", encoding="utf-8")
    run(config)

    assert intruder.exists(), "usunięto katalog spoza manifestu"
    assert (intruder / "cenne-dane.txt").read_text(encoding="utf-8") == "nie kasuj mnie"


def test_retention_keeps_versions_still_referenced(tree, tmp_path, monkeypatch):
    """Wersja, na którą wciąż wskazuje spis treści, nie może zniknąć —
    inaczej kopia straciłaby pliki, które uważa za zapisane."""
    dst = tmp_path / "kopia"
    config = make_config(tree, dst, structure="dated", retention=1)

    stamps = iter(["2026-06-01_@416", "2026-06-02_@416"])
    monkeypatch.setattr(engine.beat, "stamp", lambda *a: next(stamps))

    # Twarde dowiązania zawodzą (np. FAT) -> wpisy zostają przy starej wersji.
    def failing_link(*_args, **_kwargs):
        raise OSError("system plików nie wspiera twardych dowiązań")

    run(config)
    monkeypatch.setattr(engine.os, "link", failing_link)
    monkeypatch.setattr(engine, "_duplicate_file", failing_link)
    (tree / "a.txt").write_text("zmiana", encoding="utf-8")
    run(config)

    manifest = Manifest.load(dst)
    for entry in manifest.entries.values():
        assert (dst / entry.stored).exists(), f"brak pliku {entry.stored} wskazywanego przez manifest"


def test_manifest_tracks_versions(tree, tmp_path):
    dst = tmp_path / "kopia"
    config = make_config(tree, dst, structure="dated")
    run(config)
    (tree / "a.txt").write_text("v2", encoding="utf-8")
    run(config)

    manifest = Manifest.load(dst)
    assert len(manifest.versions) == 2
    assert manifest.versions == sorted(manifest.versions)


def test_end_to_end_with_production_argon2(tmp_path):
    """Pełny obieg na domyślnych parametrach produkcyjnych.

    Pozostałe testy używają szybkiego PBKDF2, żeby nie trwać minutami. Ten jeden
    przechodzi realną ścieżką (Argon2id, 64 MiB) i pilnuje, że klucz wyprowadza
    się raz na sesję — inaczej ten test sam stałby się nieznośnie wolny.
    """
    src = tmp_path / "dane"
    src.mkdir()
    for i in range(12):
        (src / f"plik{i}.txt").write_text(f"zawartość {i}", encoding="utf-8")

    dst = tmp_path / "kopia"
    config = make_config(src, dst, encrypt=True, structure="dated")
    keyring = crypto.PasswordKeyring("Prawdziwe-Hasło-Produkcyjne-2026")

    result = engine.run_backup(engine.plan_backup(config, Reporter()), keyring, Reporter())
    assert result.ok and result.files_done == 12, result.errors

    out = tmp_path / "odzyskane"
    restore = engine.run_restore(engine.plan_restore(dst, out), keyring, Reporter())
    assert restore.ok, restore.errors

    for i in range(12):
        assert (out / "dane" / f"plik{i}.txt").read_text(encoding="utf-8") == f"zawartość {i}"

    # Złe hasło nie może odzyskać niczego.
    zly = crypto.PasswordKeyring("Nieprawidłowe-Hasło")
    bad = engine.run_restore(engine.plan_restore(dst, tmp_path / "nic"), zly, Reporter())
    assert not bad.ok
    assert bad.files_done == 0


# ------------------------------------------- regresja: przerwana kopia a manifest


class CancelAfter:
    """Reporter zgłaszający przerwanie po ``n`` plikach.

    Odwzorowuje realny scenariusz: użytkownik zatrzymuje wielogodzinną kopię
    w połowie.
    """

    def __init__(self, n: int) -> None:
        self.n = n
        self.seen = 0

    def reporter(self) -> Reporter:
        def on_file(_name, _index, _total):
            self.seen += 1

        return Reporter(on_file=on_file, is_cancelled=lambda: self.seen >= self.n)


def test_cancelled_backup_keeps_entries_of_other_job(tmp_path):
    """Przerwanie kopii zadania B nie może skasować z manifestu wpisów zadania A.

    Realny incydent: dwa zadania pisały do jednego katalogu na dysku N. Przerwanie
    drugiego wyczyściło manifest pierwszego, więc jego 360 GB przestało być
    widoczne dla programu i kolejny przebieg chciał skopiować wszystko od nowa.
    """
    job_a = tmp_path / "JobA"
    job_b = tmp_path / "JobB"
    dest = tmp_path / "Cel"
    job_a.mkdir()
    job_b.mkdir()
    for i in range(3):
        (job_a / f"a{i}.bin").write_bytes(b"A" * 512)
    for i in range(8):
        (job_b / f"b{i}.bin").write_bytes(b"B" * 512)

    config_a = make_config(job_a, dest, structure="dated", verify_after_write=False)
    run(config_a)
    assert len(Manifest.load(dest).entries) == 3

    config_b = make_config(job_b, dest, structure="dated", verify_after_write=False, workers=1)
    canceller = CancelAfter(3)
    plan_b = engine.plan_backup(config_b, Reporter())
    result = engine.run_backup(plan_b, None, canceller.reporter())
    assert result.cancelled

    manifest = Manifest.load(dest)
    kept = [key for key in manifest.entries if key.startswith("JobA/")]
    assert len(kept) == 3, "przerwana kopia skasowała wpisy drugiego zadania"
    assert "JobA" in manifest.roots, "przerwana kopia skasowała mapowanie katalogów źródłowych"

    # I najważniejsze: powtórka zadania A nie kopiuje niczego od nowa.
    plan_a2 = engine.plan_backup(config_a, Reporter())
    assert plan_a2.to_copy == [], "zadanie A chce skopiować wszystko ponownie"


def test_cancelled_backup_keeps_unchanged_entries(tree, tmp_path):
    """Przerwanie w pętli kopiowania zachowuje wpisy plików niezmienionych."""
    dest = tmp_path / "cel"
    config = make_config(tree, dest, structure="dated", verify_after_write=False, workers=1)
    run(config)
    before = len(Manifest.load(dest).entries)
    assert before == 3

    (tree / "nowy1.txt").write_text("x", encoding="utf-8")
    (tree / "nowy2.txt").write_text("y", encoding="utf-8")
    canceller = CancelAfter(1)
    plan = engine.plan_backup(config, Reporter())
    result = engine.run_backup(plan, None, canceller.reporter())
    assert result.cancelled

    manifest = Manifest.load(dest)
    assert len(manifest.entries) >= before, "przerwanie zgubiło wpisy plików niezmienionych"
    for entry in manifest.entries.values():
        assert (dest / entry.stored).exists(), f"manifest wskazuje na nieistniejący plik {entry.stored}"


# ------------------------------------------- realny koszt kopii na nośniku


def test_plan_counts_cluster_slack(tree, tmp_path, monkeypatch):
    """Plan podaje miejsce zajęte naprawdę, z zaokrągleniem do klastrów.

    Na nośniku z klastrem 256 KB trzy małe pliki zajmują 768 KB, a nie ~4 KB.
    Bez tego kontrola wolnego miejsca przepuszczała kopie, które się nie mieszczą.
    """
    monkeypatch.setattr(engine, "cluster_size", lambda _p: 262144)
    monkeypatch.setattr(engine, "supports_hardlinks", lambda _p: True)
    plan = engine.plan_backup(make_config(tree, tmp_path / "cel"), Reporter())
    assert plan.cluster == 262144
    assert plan.physical_bytes == 3 * 262144
    assert plan.physical_bytes > plan.total_bytes


def test_plan_warns_when_medium_has_no_hardlinks(tree, tmp_path, monkeypatch):
    """Bez twardych dowiązań każda wersja z datą jest pełną kopią — i plan to mówi."""
    monkeypatch.setattr(engine, "cluster_size", lambda _p: 4096)
    monkeypatch.setattr(engine, "supports_hardlinks", lambda _p: False)
    monkeypatch.setattr(engine, "filesystem_name", lambda _p: "exFAT")
    dest = tmp_path / "cel"

    config = make_config(tree, dest, structure="dated", verify_after_write=False)
    run(config)

    plan = engine.plan_backup(config, Reporter())
    assert plan.unchanged and not plan.to_copy
    assert plan.physical_bytes > 0, "powielenie niezmienionych plików musi być policzone"
    assert any("twardych dowiązań" in w for w in plan.warnings)


def test_free_space_check_uses_physical_size(tree, tmp_path, monkeypatch):
    """Kopia, która logicznie się mieści, ale fizycznie nie, jest odrzucana."""
    import shutil as _shutil

    monkeypatch.setattr(engine, "cluster_size", lambda _p: 1024 * 1024)
    monkeypatch.setattr(engine, "supports_hardlinks", lambda _p: True)
    monkeypatch.setattr(
        engine.shutil, "disk_usage", lambda _p: _shutil._ntuple_diskusage(100, 50, 1024 * 1024)
    )
    with pytest.raises(EngineError, match="Za mało miejsca"):
        engine.plan_backup(make_config(tree, tmp_path / "cel"), Reporter())


# ------------------------------------------------- wznawianie przerwanej kopii


@pytest.fixture()
def big_tree(tmp_path):
    """Dwanaście plików — na tyle dużo, by przerwać kopię w połowie."""
    src = tmp_path / "dane"
    src.mkdir()
    for i in range(12):
        (src / f"plik{i:02d}.bin").write_bytes(bytes([i]) * 2048)
    return src


def _incomplete(dest):
    return [r for r in Manifest.load(dest).runs.values() if not r.complete]


def test_interrupted_version_is_marked_incomplete(big_tree, tmp_path):
    """Przerwana kopia zostaje oznaczona jako niedokończona, a nie jako zwykła wersja."""
    dest = tmp_path / "cel"
    config = make_config(big_tree, dest, structure="dated", verify_after_write=False, workers=1)
    plan = engine.plan_backup(config, Reporter())
    result = engine.run_backup(plan, None, CancelAfter(5).reporter())
    assert result.cancelled

    pending = _incomplete(dest)
    assert len(pending) == 1
    assert pending[0].name == plan.version
    assert pending[0].missing_files > 0


def test_resume_adopts_already_copied_files(big_tree, tmp_path):
    """Wznowienie dogrywa wyłącznie brakujące pliki — reszty nie tyka."""
    dest = tmp_path / "cel"
    config = make_config(big_tree, dest, structure="dated", verify_after_write=False, workers=1)
    first = engine.plan_backup(config, Reporter())
    interrupted = engine.run_backup(first, None, CancelAfter(5).reporter())
    assert interrupted.cancelled
    done_before = interrupted.files_done
    assert 0 < done_before < 12

    resume_config = make_config(
        big_tree, dest, structure="dated", verify_after_write=False,
        target_version=first.version,
    )
    plan = engine.plan_backup(resume_config, Reporter())
    assert plan.resuming
    assert plan.version == first.version
    assert len(plan.adopted) == done_before, "wznowienie nie rozpoznało zapisanych plików"
    assert len(plan.to_copy) == 12 - done_before

    result = engine.run_backup(plan, None, Reporter())
    assert result.ok and not result.cancelled
    assert result.files_done == 12 - done_before, "wznowienie skopiowało coś po raz drugi"

    manifest = Manifest.load(dest)
    assert len(manifest.entries) == 12
    assert manifest.runs[first.version].complete
    assert _incomplete(dest) == []
    for entry in manifest.entries.values():
        assert entry.stored.startswith(first.version + "/")
        assert (dest / entry.stored).exists()


def test_resume_works_without_any_manifest(big_tree, tmp_path):
    """Po twardym zabiciu procesu manifest może nie istnieć — wznowienie i tak działa.

    Wznawianie pyta nośnik, a nie manifest: plik leżący pod docelową nazwą jest
    kompletny, bo zapis idzie przez plik tymczasowy i atomową podmianę.
    """
    dest = tmp_path / "cel"
    config = make_config(big_tree, dest, structure="dated", verify_after_write=False, workers=1)
    first = engine.plan_backup(config, Reporter())
    engine.run_backup(first, None, CancelAfter(6).reporter())
    saved = len(list((dest / first.version).rglob("*.bin")))
    assert saved > 0

    # Symulacja zaniku zasilania: żaden ślad stanu kopii nie trafił na dysk —
    # ani manifest, ani podsumowanie, ani dziennik punktów kontrolnych.
    for name in (".cleanvault-manifest", ".cleanvault-manifest.summary", ".cleanvault-manifest.journal"):
        (dest / name).unlink(missing_ok=True)

    resume_config = make_config(
        big_tree, dest, structure="dated", verify_after_write=False,
        target_version=first.version,
    )
    plan = engine.plan_backup(resume_config, Reporter())
    assert len(plan.adopted) == saved, "bez manifestu wznowienie kopiowałoby wszystko od nowa"
    result = engine.run_backup(plan, None, Reporter())
    assert result.ok
    assert result.files_done == 12 - saved
    assert len(Manifest.load(dest).entries) == 12


def test_resume_recopies_file_changed_since_interruption(big_tree, tmp_path):
    """Plik zmieniony po zapisaniu musi zostać dograny ponownie, nie zaadoptowany."""
    dest = tmp_path / "cel"
    config = make_config(big_tree, dest, structure="dated", verify_after_write=False, workers=1)
    first = engine.plan_backup(config, Reporter())
    engine.run_backup(first, None, CancelAfter(5).reporter())

    stored = sorted((dest / first.version).rglob("*.bin"))
    victim = big_tree / stored[0].name
    victim.write_bytes(b"CALKIEM NOWA TRESC" * 200)

    resume_config = make_config(
        big_tree, dest, structure="dated", verify_after_write=False,
        target_version=first.version,
    )
    plan = engine.plan_backup(resume_config, Reporter())
    assert victim.name not in {Path(k).name for k in plan.adopted}, "zmieniony plik został uznany za gotowy"
    engine.run_backup(plan, None, Reporter())
    copied = (dest / first.version / big_tree.name / victim.name)
    assert copied.read_bytes() == victim.read_bytes()


def test_resume_of_unknown_version_is_rejected(big_tree, tmp_path):
    config = make_config(big_tree, tmp_path / "cel", structure="dated", target_version="nie-ma-takiej")
    with pytest.raises(EngineError, match="Nie ma wersji kopii"):
        engine.plan_backup(config, Reporter())


# ------------------------------ źródło żyjące w trakcie kopii (dogrywka)


def test_file_changed_during_copy_is_not_trusted(tree, tmp_path, monkeypatch):
    """Plik zmieniony w trakcie własnego kopiowania nie trafia do spisu treści.

    Zapisane bajty mogą być sklejką starej i nowej treści. Wpis w manifeście
    mówiłby, że kopia jest aktualna — i plik nigdy nie zostałby poprawiony.
    """
    dst = tmp_path / "kopia"
    real_write = engine._write_stored
    touched: list[str] = []

    def copy_then_mutate(src, target, reporter):
        out = real_write(src, target, reporter)
        if src.name == "b.bin" and src.name not in touched:
            touched.append(src.name)
            # Użytkownik zapisuje plik dokładnie w chwili, gdy go kopiujemy.
            src.write_bytes(os.urandom(9000))
        return out

    monkeypatch.setattr(engine, "_write_stored", copy_then_mutate)
    _, result = run(make_config(tree, dst, verify_after_write=False, catchup_passes=0))

    manifest = Manifest.load(dst)
    assert "zrodlo/b.bin" not in manifest.entries, "niepewny plik został uznany za zapisany"
    assert result.skipped == 1
    assert not manifest.runs[""].complete if "" in manifest.runs else True


def test_catchup_repairs_file_changed_during_copy(tree, tmp_path, monkeypatch):
    """Przebieg uzupełniający dogrywa plik, który zmienił się w trakcie kopiowania."""
    dst = tmp_path / "kopia"
    real_write = engine._write_stored
    touched: list[str] = []

    def copy_then_mutate(src, target, reporter):
        out = real_write(src, target, reporter)
        if src.name == "b.bin" and src.name not in touched:
            touched.append(src.name)
            src.write_bytes(b"TRESC PO ZMIANIE" * 500)
        return out

    monkeypatch.setattr(engine, "_write_stored", copy_then_mutate)
    _, result = run(make_config(tree, dst, verify_after_write=True, catchup_passes=1))

    manifest = Manifest.load(dst)
    assert "zrodlo/b.bin" in manifest.entries, "dogrywka nie naprawiła niepewnego pliku"
    stored = dst / manifest.entries["zrodlo/b.bin"].stored
    assert stored.read_bytes() == (tree / "b.bin").read_bytes()
    assert result.ok


def test_catchup_saves_files_created_during_backup(tree, tmp_path, monkeypatch):
    """Pliki, które powstały w źródle w trakcie kopii, trafiają do tej samej wersji.

    Bez tego użytkownik pracujący na danych przez kilkanaście godzin kopiowania
    dostawał kopię niekompletną już w chwili jej zakończenia.
    """
    dst = tmp_path / "kopia"
    real_write = engine._write_stored
    created: list[str] = []

    def copy_then_create(src, target, reporter):
        out = real_write(src, target, reporter)
        if not created:
            created.append("tak")
            (src.parent / "powstal_w_trakcie.txt").write_text("nowe dane", encoding="utf-8")
        return out

    monkeypatch.setattr(engine, "_write_stored", copy_then_create)
    plan, result = run(
        make_config(tree, dst, structure="dated", verify_after_write=False, catchup_passes=1)
    )

    manifest = Manifest.load(dst)
    assert "zrodlo/powstal_w_trakcie.txt" in manifest.entries, "dogrywka pominęła nowy plik"
    assert (dst / manifest.entries["zrodlo/powstal_w_trakcie.txt"].stored).exists()
    assert manifest.runs[plan.version].complete
    assert result.files_done == 4


def test_catchup_can_be_switched_off(tree, tmp_path):
    """catchup_passes=0 zachowuje stare zachowanie: jeden przebieg i koniec."""
    dst = tmp_path / "kopia"
    _, result = run(make_config(tree, dst, catchup_passes=0))
    assert result.ok and result.files_done == 3
