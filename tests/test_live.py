"""Kopia „na bieżąco” (cleanvault/live.py): kiedy dogrywać, dokąd i co obserwować."""

from __future__ import annotations

import os
import time
from datetime import UTC, datetime, timedelta

import pytest

from cleanvault import live, proof, scheduler
from cleanvault.snapshot import VersionState
from cleanvault.state import Template

T0 = 1_800_000_000.0


# ------------------------------------------------------------------ kiedy


def test_nothing_changed_nothing_to_do():
    tracker = live.ChangeTracker()
    assert not tracker.pending("a")
    assert not tracker.ready("a", T0)


def test_waits_for_quiet_after_the_last_change():
    tracker = live.ChangeTracker()
    tracker.note("a", T0)
    tracker.note("a", T0 + 30)
    assert not tracker.ready("a", T0 + 30 + live.QUIET_SECONDS - 1)
    assert tracker.ready("a", T0 + 30 + live.QUIET_SECONDS)


def test_never_ending_changes_still_get_backed_up():
    """Plik zapisywany co kilka sekund (dziennik) — cisza nie nadchodzi, a kopia ma ruszyć."""
    tracker = live.ChangeTracker()
    moment = T0
    while moment < T0 + live.MAX_DELAY:
        tracker.note("a", moment)
        assert not tracker.ready("a", moment) or moment - T0 >= live.MAX_DELAY
        moment += 10
    tracker.note("a", moment)
    assert tracker.ready("a", moment)


def test_minimum_gap_between_runs():
    tracker = live.ChangeTracker()
    tracker.note("a", T0)
    tracker.started("a", T0 + live.QUIET_SECONDS)
    tracker.finished("a", True, T0 + live.QUIET_SECONDS + 5)
    later = T0 + live.QUIET_SECONDS + 10
    tracker.note("a", later)
    assert not tracker.ready("a", later + live.QUIET_SECONDS)
    assert tracker.ready("a", T0 + live.QUIET_SECONDS + 5 + live.MIN_INTERVAL)


def test_changes_during_a_run_stay_pending_and_earlier_ones_are_done():
    tracker = live.ChangeTracker()
    tracker.note("a", T0)
    tracker.started("a", T0 + 100)
    assert not tracker.ready("a", T0 + 1000), "trwa dogrywka"
    tracker.finished("a", True, T0 + 200)
    assert not tracker.pending("a"), "zmiana sprzed startu jest już w kopii"

    tracker.note("b", T0)
    tracker.started("b", T0 + 100)
    tracker.note("b", T0 + 150)  # w trakcie kopii
    tracker.finished("b", True, T0 + 200)
    assert tracker.pending("b")


def test_failure_backs_off_and_hold_waits_for_a_human():
    tracker = live.ChangeTracker()
    tracker.note("a", T0)
    tracker.started("a", T0 + 100)
    tracker.finished("a", False, T0 + 120)
    assert tracker.pending("a")
    assert not tracker.ready("a", T0 + 120 + live.RETRY_AFTER - 1)
    assert tracker.ready("a", T0 + 120 + live.RETRY_AFTER)

    tracker.hold("a")  # np. podejrzanie dużo zmian — ransomware?
    assert not tracker.ready("a", T0 + 10 * live.RETRY_AFTER)
    tracker.release("a")
    assert tracker.ready("a", T0 + 10 * live.RETRY_AFTER)


# ------------------------------------------------------------------ dokąd


def _day(now: float, days_back: int = 0) -> str:
    return (datetime.fromtimestamp(now, UTC) - timedelta(days=days_back)).strftime("%Y-%m-%d")


def _run(name: str, complete: bool = True) -> VersionState:
    return VersionState(name=name, complete=complete, known=True)


def test_first_live_run_creates_a_version(tmp_path):
    assert live.plan_live_run([], tmp_path, T0, timestamp=True) == live.LivePlan("", False)


def test_todays_version_is_topped_up(tmp_path):
    name = f"{_day(T0)}_@100"
    (tmp_path / name).mkdir()
    assert live.plan_live_run([_run(name)], tmp_path, T0, timestamp=True) == live.LivePlan(name, False)


def test_a_sealed_version_is_never_touched_again(tmp_path):
    name = f"{_day(T0)}_@100"
    (tmp_path / name).mkdir()
    (tmp_path / name / proof.SEAL_NAME).write_text("{}", encoding="utf-8")
    assert live.plan_live_run([_run(name)], tmp_path, T0, timestamp=True) == live.LivePlan("", False)


def test_yesterdays_version_is_closed_with_a_seal_only_with_timestamps(tmp_path):
    name = f"{_day(T0, 1)}_@900"
    (tmp_path / name).mkdir()
    assert live.plan_live_run([_run(name)], tmp_path, T0, timestamp=True) == live.LivePlan(name, True)
    assert live.plan_live_run([_run(name)], tmp_path, T0, timestamp=False) == live.LivePlan("", False)


def test_an_interrupted_version_is_completed_first(tmp_path):
    name = f"{_day(T0, 2)}_@500"
    (tmp_path / name).mkdir()
    assert live.plan_live_run([_run(name, complete=False)], tmp_path, T0, timestamp=False) == \
        live.LivePlan(name, False)


def test_topped_up_name_counts_by_creation_day(tmp_path):
    name = f"{_day(T0)}_@100--{_day(T0)}_@700"
    (tmp_path / name).mkdir()
    assert live.plan_live_run([_run(name)], tmp_path, T0, timestamp=True).target_version == name


# ------------------------------------------------------------------ harmonogram


def test_live_syncs_on_every_connection_with_a_short_gap():
    template = Template(name="t", sources=["C:/x"], destination="E:/kopia", schedule=scheduler.LIVE)
    template.last_attempt = T0
    plugged = scheduler.due_templates([template], T0 + scheduler.LIVE_CONNECT_GAP + 1,
                                      available=lambda _d: True, seen={template.id: False})
    assert [d.reason for d in plugged] == ["connected"]
    too_soon = scheduler.due_templates([template], T0 + 60, available=lambda _d: True,
                                       seen={template.id: False})
    assert too_soon == []


# ------------------------------------------------------------------ obserwowanie


def _wait(condition, seconds: float = 8.0) -> bool:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if condition():
            return True
        time.sleep(0.05)
    return condition()


@pytest.mark.skipif(not live.watchdog_available(), reason="brak biblioteki watchdog")
def test_watcher_notes_changes_but_not_the_backup_itself(tmp_path):
    source = tmp_path / "Dokumenty"
    (source / "sub").mkdir(parents=True)
    destination = source / "Kopia"  # katalog kopii wewnątrz źródła — jej zapis nie może się liczyć
    destination.mkdir()
    template = Template(name="t", sources=[str(source)], destination=str(destination), schedule=scheduler.LIVE)
    tracker = live.ChangeTracker()
    watcher = live.LiveWatcher(tracker)
    try:
        watcher.update([template])
        assert template.id not in watcher.unwatched
        time.sleep(0.3)
        (destination / "plik.cvlt").write_bytes(os.urandom(64))
        time.sleep(1.0)
        assert not tracker.pending(template.id), "zapis kopii nie jest zmianą źródła"
        (source / "sub" / "umowa.txt").write_text("nowa umowa", encoding="utf-8")
        assert _wait(lambda: tracker.pending(template.id))
    finally:
        watcher.stop()


def test_without_a_watchable_folder_the_fallback_takes_over(tmp_path):
    template = Template(name="t", sources=[str(tmp_path / "nie-ma" / "ani-to")], destination=str(tmp_path / "k"),
                        schedule=scheduler.LIVE)
    watcher = live.LiveWatcher(live.ChangeTracker())
    try:
        watcher.update([template])
        assert template.id in watcher.unwatched
    finally:
        watcher.stop()
