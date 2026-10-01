"""Testy wznawiania, uzupełniania i stanu katalogu docelowego.

Tło: kopia ~500 GB na dysk exFAT została przerwana. Po ponownym uruchomieniu
program nie potrafił jej dokończyć — przerwanie skasowało z manifestu wpisy
innego zadania piszącego do tego samego dysku, a jedyną dostępną akcją było
utworzenie kolejnej pełnej wersji, na którą zabrakło miejsca.
"""

from __future__ import annotations

import os
import shutil

import pytest

from cleanvault import crypto, engine
from cleanvault.crypto import KdfParams, PasswordKeyring
from cleanvault.engine import BackupConfig, EngineError, Reporter
from cleanvault.paths import MANIFEST_NAME, SUMMARY_NAME
from cleanvault.snapshot import Manifest, ManifestSummary, VersionState


class CancelAfter:
    """Reporter zgłaszający przerwanie po ``n`` plikach."""

    def __init__(self, n: int) -> None:
        self.n = n
        self.seen = 0

    def reporter(self) -> Reporter:
        def on_file(_name, _index, _total):
            self.seen += 1

        return Reporter(on_file=on_file, is_cancelled=lambda: self.seen >= self.n)


def make_tree(root, name, count, size=1024):
    folder = root / name
    folder.mkdir(parents=True)
    for i in range(count):
        (folder / f"{name.lower()}{i:02d}.bin").write_bytes(bytes([i % 251]) * size)
    return folder


def config_for(sources, dest, **kwargs) -> BackupConfig:
    params = dict(
        sources=[str(s) for s in sources],
        destination=str(dest),
        structure="dated",
        verify_after_write=False,
        excludes=[],
        catchup_passes=0,
        # Przerywanie „po N plikach” musi być deterministyczne; tryb
        # równoległy ma własne testy w test_parallel.py.
        workers=1,
        # Dopisywanie daty uzupełnienia do nazwy wersji sprawdza test_version_names.py.
        stamp_updates=False,
    )
    params.update(kwargs)
    return BackupConfig(**params)


def run(config, keyring=None, reporter=None):
    plan = engine.plan_backup(config, Reporter())
    return plan, engine.run_backup(plan, keyring, reporter or Reporter())


@pytest.fixture()
def keyring() -> PasswordKeyring:
    return PasswordKeyring("Hasło-Testowe", KdfParams(crypto.KDF_PBKDF2_SHA256, b"s" * 16, 1000))


@pytest.fixture(autouse=True)
def stamps(monkeypatch):
    """Kolejne, różne znaczniki wersji — testy działają szybciej niż zegar BeatTime."""
    counter = iter(range(1, 1000))
    monkeypatch.setattr(engine.beat, "stamp", lambda *a: f"2026-09-{next(counter):02d}_@416")


# ----------------------------------------------------------- incydent z N:


def test_incident_two_jobs_one_disk_resume_copies_nothing(tmp_path):
    """Dokładny przebieg incydentu i to, jak ma się teraz zakończyć.

    Zadanie A (kilka źródeł) i zadanie B (jedno źródło) piszą na ten sam dysk.
    Kopia B zostaje przerwana. Uruchomienie A z uzupełnieniem jego ostatniej
    wersji nie może skopiować niczego, a dokończenie B — tylko to, czego brakuje.
    """
    muzyka = make_tree(tmp_path, "MUZYKA", 4)
    repo = make_tree(tmp_path, "Repo", 4)
    privat = make_tree(tmp_path, "Privat", 10)
    dest = tmp_path / "N"

    plan_a, result_a = run(config_for([muzyka, repo], dest))
    assert result_a.ok

    plan_b = engine.plan_backup(config_for([privat], dest), Reporter())
    result_b = engine.run_backup(plan_b, None, CancelAfter(4).reporter())
    assert result_b.cancelled

    info = engine.inspect_destination(dest)
    labels_a = engine.source_labels([str(muzyka), str(repo)])
    labels_b = engine.source_labels([str(privat)])

    # Zadanie A: najnowsza wersja kompletna — nic do proponowania, a pełny
    # przebieg uzupełniający nie kopiuje ani jednego pliku.
    assert engine.suggest_continuation(info, labels_a) is None
    plan_a2, result_a2 = run(config_for([muzyka, repo], dest, target_version=plan_a.version))
    assert plan_a2.to_copy == []
    assert result_a2.files_done == 0 and result_a2.ok

    # Zadanie B: program sam wskazuje niedokończoną wersję.
    suggestion = engine.suggest_continuation(info, labels_b)
    assert suggestion is not None and suggestion.name == plan_b.version
    assert not suggestion.complete

    plan_b2, result_b2 = run(config_for([privat], dest, target_version=suggestion.name))
    assert len(plan_b2.adopted) == result_b.files_done
    assert result_b2.files_done == 10 - result_b.files_done
    assert Manifest.load(dest).runs[plan_b.version].complete

    # Wpisy obu zadań są w manifeście i wskazują na istniejące pliki.
    manifest = Manifest.load(dest)
    assert len(manifest.entries) == 18
    assert {"MUZYKA", "Repo", "Privat"} <= set(manifest.roots)
    for entry in manifest.entries.values():
        assert (dest / entry.stored).exists()


def test_legacy_manifest_without_runs_reports_unknown_state(tmp_path):
    """Manifest zapisany starszym programem nie wie, czy kopia się domknęła —
    i program nie może udawać, że wie."""
    src = make_tree(tmp_path, "Privat", 3)
    dest = tmp_path / "N"
    plan, _ = run(config_for([src], dest))

    # Starszy program nie zapisywał ani stanu przebiegów, ani podsumowania.
    assert Manifest.load(dest).runs[plan.version].known
    (dest / SUMMARY_NAME).unlink()
    from cleanvault import snapshot

    blob = snapshot._read_envelope(dest / MANIFEST_NAME)
    blob.pop("runs")
    snapshot._write_envelope(dest / MANIFEST_NAME, blob)

    legacy = Manifest.load(dest)
    assert legacy.runs[plan.version].known is False
    info = engine.inspect_destination(dest)
    assert info.runs[0].known is False
    assert "stan nieznany" in engine.describe_version(info.runs[0])
    assert engine.suggest_continuation(info, ["Privat"]).name == plan.version


# ------------------------------------------------------------ podsumowanie


def test_summary_is_written_and_matches_manifest(tmp_path):
    src = make_tree(tmp_path, "Dane", 5, size=100)
    dest = tmp_path / "cel"
    plan, _ = run(config_for([src], dest))

    summary = ManifestSummary.load(dest)
    assert summary is not None
    assert summary.entry_count == 5
    assert summary.total_bytes == 500
    assert summary.runs[plan.version].complete


def test_stale_summary_is_ignored(tmp_path):
    """Podsumowanie starsze od manifestu (manifest zapisany starym programem) jest pomijane."""
    src = make_tree(tmp_path, "Dane", 2)
    dest = tmp_path / "cel"
    run(config_for([src], dest))
    old = (dest / MANIFEST_NAME).stat().st_mtime - 60
    os.utime(dest / SUMMARY_NAME, (old, old))
    assert ManifestSummary.load(dest) is None


def test_inspect_without_summary_lists_version_folders(tmp_path):
    """Bez podsumowania i bez wczytywania manifestu katalogi wersji i tak są widoczne."""
    dest = tmp_path / "cel"
    (dest / "2026-09-12_11-05-51" / "MUZYKA").mkdir(parents=True)
    (dest / "2026-09-15_07-38-26" / "Privat").mkdir(parents=True)
    (dest / "Moje zdjęcia").mkdir()

    info = engine.inspect_destination(dest)
    assert [run.name for run in info.runs] == ["2026-09-15_07-38-26", "2026-09-12_11-05-51"]
    assert info.runs[0].labels == ["Privat"]
    assert all(not run.known for run in info.runs)
    assert info.entry_count is None


def test_inspect_missing_destination(tmp_path):
    info = engine.inspect_destination(tmp_path / "nie-istnieje")
    assert not info.exists and info.runs == []


def test_source_labels_match_plan(tmp_path):
    a = make_tree(tmp_path / "d1", "Foto", 1)
    b = make_tree(tmp_path / "d2", "Foto", 1)
    plan = engine.plan_backup(config_for([a, b], tmp_path / "cel"), Reporter())
    assert engine.source_labels([str(a), str(b)]) == [root.label for root in plan.roots]


def test_complete_version_is_not_suggested(tmp_path):
    src = make_tree(tmp_path, "Dane", 2)
    dest = tmp_path / "cel"
    run(config_for([src], dest))
    assert engine.suggest_continuation(engine.inspect_destination(dest), ["Dane"]) is None


def test_other_jobs_incomplete_version_is_not_suggested(tmp_path):
    a = make_tree(tmp_path, "A", 6)
    b = make_tree(tmp_path, "B", 2)
    dest = tmp_path / "cel"
    plan = engine.plan_backup(config_for([a], dest), Reporter())
    engine.run_backup(plan, None, CancelAfter(2).reporter())
    info = engine.inspect_destination(dest)
    assert engine.suggest_continuation(info, ["A"]) is not None
    assert engine.suggest_continuation(info, engine.source_labels([str(b)])) is None


def test_describe_incomplete_version_shows_what_is_missing(tmp_path):
    src = make_tree(tmp_path, "Dane", 8)
    dest = tmp_path / "cel"
    plan = engine.plan_backup(config_for([src], dest), Reporter())
    engine.run_backup(plan, None, CancelAfter(3).reporter())
    run_state = engine.inspect_destination(dest).runs[0]
    text = engine.describe_version(run_state)
    assert "niedokończona" in text
    assert f"brakuje ok. {run_state.missing_files} plików" in text
    assert run_state.missing_files == 8 - run_state.done_files


# ------------------------------------------------------------- retencja


def test_retention_does_not_delete_other_jobs_versions(tmp_path):
    """Limit wersji jednego zadania nie może skasować kopii drugiego zadania."""
    a = make_tree(tmp_path, "A", 2)
    b = make_tree(tmp_path, "B", 2)
    dest = tmp_path / "cel"
    plan_b, _ = run(config_for([b], dest))

    # Symulacja stanu dysku N: — wpisy zadania B zniknęły z manifestu, więc
    # jego wersja nie jest już chroniona przez odwołania ze spisu treści.
    manifest = Manifest.load(dest)
    manifest.entries = {k: v for k, v in manifest.entries.items() if not k.startswith("B/")}
    manifest.save()

    for i in range(3):
        (a / "a00.bin").write_bytes(bytes([i]) * 50)
        run(config_for([a], dest, retention=1))

    assert (dest / plan_b.version).is_dir(), "retencja zadania A skasowała wersję zadania B"


def test_retention_never_deletes_or_counts_incomplete_versions(tmp_path):
    src = make_tree(tmp_path, "Dane", 6)
    dest = tmp_path / "cel"
    run(config_for([src], dest))

    (src / "dane00.bin").write_bytes(b"zmiana")
    broken = engine.plan_backup(config_for([src], dest), Reporter())
    engine.run_backup(broken, None, CancelAfter(1).reporter())
    assert not Manifest.load(dest).runs[broken.version].complete

    (src / "dane01.bin").write_bytes(b"kolejna zmiana")
    run(config_for([src], dest, retention=1))

    assert (dest / broken.version).is_dir(), "retencja skasowała niedokończoną wersję"


# ----------------------------------------------------- nośnik i dowiązania


def test_stale_file_in_target_version_is_not_trusted_when_linking(tmp_path):
    """W docelowej wersji leży plik, który nie jest kopią wpisu — trzeba go zastąpić."""
    src = make_tree(tmp_path, "Dane", 3)
    dest = tmp_path / "cel"
    run(config_for([src], dest))

    (src / "dane02.bin").write_bytes(b"nowy plik wymusza nowa wersje")
    second = engine.plan_backup(config_for([src], dest), Reporter())
    target = dest / second.version / "Dane" / "dane00.bin"
    target.parent.mkdir(parents=True)
    target.write_bytes(b"SMIECI Z PRZERWANEGO ZAPISU")

    engine.run_backup(second, None, Reporter())
    assert target.read_bytes() == (src / "dane00.bin").read_bytes()


def test_without_hardlinks_unchanged_files_are_copied_with_progress(tmp_path, monkeypatch):
    monkeypatch.setattr(engine, "supports_hardlinks", lambda _p: False)
    src = make_tree(tmp_path, "Dane", 4, size=2048)
    dest = tmp_path / "cel"
    run(config_for([src], dest))

    (src / "dane00.bin").write_bytes(b"x" * 10)
    plan = engine.plan_backup(config_for([src], dest), Reporter())
    assert plan.transfer_bytes == plan.total_bytes + 3 * 2048

    seen = []
    engine.run_backup(plan, None, Reporter(on_bytes=seen.append))
    assert sum(seen) >= 3 * 2048, "kopiowanie zamiast dowiązań nie raportuje postępu"
    for i in range(1, 4):
        copy = dest / plan.version / "Dane" / f"dane{i:02d}.bin"
        assert copy.exists() and os.stat(copy).st_nlink == 1


def test_resume_does_not_double_count_space_for_replaced_files(tmp_path, monkeypatch):
    monkeypatch.setattr(engine, "cluster_size", lambda _p: 4096)
    src = make_tree(tmp_path, "Dane", 3, size=8192)
    dest = tmp_path / "cel"
    first, _ = run(config_for([src], dest))
    changed = src / "dane00.bin"
    changed.write_bytes(b"y" * 8192)
    later = changed.stat().st_mtime + 30
    os.utime(changed, (later, later))

    plan = engine.plan_backup(config_for([src], dest, target_version=first.version), Reporter())
    assert [item.key for item in plan.to_copy] == ["Dane/dane00.bin"]
    assert plan.physical_bytes == 0, "plik zastępujący istniejący nie zajmuje dodatkowego miejsca"


def test_insufficient_space_message_is_truthful_for_resume(tmp_path, monkeypatch):
    """Wznowienie liczy tylko brakujące pliki, nie całą kopię."""
    src = make_tree(tmp_path, "Dane", 10, size=4096)
    dest = tmp_path / "cel"
    plan = engine.plan_backup(config_for([src], dest), Reporter())
    engine.run_backup(plan, None, CancelAfter(8).reporter())

    resume = engine.plan_backup(config_for([src], dest, target_version=plan.version), Reporter())
    missing = 10 - len(resume.adopted)
    assert resume.total_bytes == missing * 4096


# -------------------------------------------------------------- szyfrowanie


def test_encrypted_backup_can_be_resumed(tmp_path, keyring):
    src = make_tree(tmp_path, "Tajne", 8)
    dest = tmp_path / "cel"
    config = config_for([src], dest, encrypt=True)
    plan = engine.plan_backup(config, Reporter())
    interrupted = engine.run_backup(plan, keyring, CancelAfter(4).reporter())
    assert interrupted.cancelled

    resume = engine.plan_backup(config_for([src], dest, encrypt=True, target_version=plan.version), Reporter())
    assert len(resume.adopted) == interrupted.files_done
    result = engine.run_backup(resume, keyring, Reporter())
    assert result.ok and result.files_done == 8 - interrupted.files_done

    restore_to = tmp_path / "odzysk"
    restore = engine.plan_restore(dest, restore_to)
    assert engine.run_restore(restore, keyring, Reporter()).ok
    for original in src.iterdir():
        restored = next(restore_to.rglob(original.name))
        assert restored.read_bytes() == original.read_bytes()


def test_resume_with_different_password_is_refused(tmp_path, keyring):
    """Wznowienie z innym hasłem zostawiłoby w jednej kopii pliki pod dwoma hasłami."""
    src = make_tree(tmp_path, "Tajne", 6)
    dest = tmp_path / "cel"
    plan = engine.plan_backup(config_for([src], dest, encrypt=True), Reporter())
    engine.run_backup(plan, keyring, CancelAfter(3).reporter())

    other = PasswordKeyring("Inne-Hasło", KdfParams(crypto.KDF_PBKDF2_SHA256, b"t" * 16, 1000))
    resume = engine.plan_backup(config_for([src], dest, encrypt=True, target_version=plan.version), Reporter())
    with pytest.raises(EngineError, match="hasło nie pasuje"):
        engine.run_backup(resume, other, Reporter())


def test_version_state_roundtrip():
    state = VersionState(
        name="2026-09-15_07-38-26", started=1.0, labels=["Privat"], planned_files=10,
        done_files=4, planned_bytes=1000, done_bytes=400, known=True,
    )
    again = VersionState.from_dict(state.to_dict())
    assert again == state
    assert again.missing_files == 6 and again.missing_bytes == 600


def test_mirror_state_is_reported_separately(tmp_path):
    src = make_tree(tmp_path, "Dane", 2)
    dest = tmp_path / "cel"
    run(config_for([src], dest, structure="mirror"))
    info = engine.inspect_destination(dest)
    assert info.runs == []
    assert info.mirror is not None and info.mirror.complete
    shutil.rmtree(dest)


def test_file_saved_moments_after_copy_is_not_adopted(tmp_path):
    """Zapis sekundę po skopiowaniu, z tym samym rozmiarem, musi zostać wykryty.

    Stała tolerancja 2 s (potrzebna tylko dla FAT32) przepuszczała taki plik
    jako „już zapisany”. Tolerancja jest teraz mierzona na nośniku docelowym.
    """
    src = make_tree(tmp_path, "Dane", 2, size=64)
    dest = tmp_path / "cel"
    first, _ = run(config_for([src], dest))

    edited = src / "dane00.bin"
    before = edited.stat().st_mtime
    edited.write_bytes(b"z" * 64)
    os.utime(edited, (before + 0.5, before + 0.5))

    plan = engine.plan_backup(config_for([src], dest, target_version=first.version), Reporter())
    assert plan.mtime_tolerance < 0.5
    assert "Dane/dane00.bin" not in plan.adopted
    assert [item.key for item in plan.to_copy] == ["Dane/dane00.bin"]


def test_mtime_tolerance_falls_back_when_folder_is_not_writable(tmp_path):
    from cleanvault.paths import DEFAULT_MTIME_TOLERANCE, mtime_tolerance

    assert mtime_tolerance(tmp_path / "nie" / "istnieje") == DEFAULT_MTIME_TOLERANCE
    assert mtime_tolerance(tmp_path) < 0.1
    assert not list(tmp_path.iterdir()), "plik próbny został na nośniku"
