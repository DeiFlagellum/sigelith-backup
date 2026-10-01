"""Retencja kalendarzowa (GFS): dzienne, tygodniowe, miesięczne."""

from __future__ import annotations

import time

from cleanvault import beat, engine
from cleanvault.engine import BackupConfig, Reporter
from cleanvault.snapshot import Manifest, VersionState

DAY = 86400


def local(year, month, day, hour=12):
    return time.mktime((year, month, day, hour, 0, 0, 0, 0, -1))


def daily_versions(start, days, per_day=1):
    times = {}
    for index in range(days):
        for extra in range(per_day):
            t = start + index * DAY + extra * 600
            times[f"v{index:03}_{extra}"] = t
    return times


def test_one_version_per_day_for_the_last_days():
    times = daily_versions(local(2026, 9, 1), 30)
    keep = engine.versions_to_keep(list(times), times, daily=7)
    assert keep == {f"v{index:03}_0" for index in range(23, 30)}


def test_only_the_newest_of_a_day_is_kept():
    times = daily_versions(local(2026, 9, 1), 3, per_day=4)
    keep = engine.versions_to_keep(list(times), times, daily=3)
    assert keep == {"v000_3", "v001_3", "v002_3"}


def test_empty_periods_do_not_use_up_the_limit():
    times = {"a": local(2026, 1, 5), "b": local(2026, 3, 9), "c": local(2026, 7, 14), "d": local(2026, 9, 20)}
    keep = engine.versions_to_keep(list(times), times, monthly=3)
    assert keep == {"b", "c", "d"}, "miesiące bez wersji nie liczą się do limitu"


def test_weekly_and_monthly_combine_with_daily():
    times = daily_versions(local(2026, 1, 1), 120)
    keep = engine.versions_to_keep(list(times), times, daily=7, weekly=4, monthly=4)
    newest_7 = {f"v{index:03}_0" for index in range(113, 120)}
    assert newest_7 <= keep
    assert len(keep) <= 7 + 4 + 4
    assert len(keep) >= 7 + 2, "tygodnie i miesiące dokładają starsze punkty"
    oldest_kept = min(times[v] for v in keep)
    assert times["v119_0"] - oldest_kept > 70 * DAY, "najstarsza zachowana sięga ok. 4 miesięcy wstecz"


def test_last_n_is_a_union_with_the_calendar():
    times = daily_versions(local(2026, 9, 1), 10, per_day=3)
    keep = engine.versions_to_keep(list(times), times, last=5, daily=2)
    assert {"v009_2", "v009_1", "v009_0", "v008_2", "v008_1"} <= keep
    assert "v008_2" in keep and "v007_2" not in keep


def test_newest_version_always_stays():
    times = {"stara": local(2020, 1, 1), "nowa": local(2026, 9, 27)}
    assert "nowa" in engine.versions_to_keep(list(times), times, monthly=1)


def test_version_time_from_its_name():
    assert beat.unix_from_stamp("2026-09-27_@500") == local(2026, 9, 27, 0) + 500 * 86.4 + _utc_offset(2026, 9, 27)
    assert beat.unix_from_stamp("2026-09-27_@500_2--2026-09-28_@100") == beat.unix_from_stamp("2026-09-27_@500")
    old = beat.unix_from_stamp("2026-09-17_16-30-11")
    assert time.localtime(old)[:6] == (2026, 9, 17, 16, 30, 11)
    assert beat.unix_from_stamp("nie-wersja") is None


def _utc_offset(year, month, day):
    """Różnica między północą lokalną a północą UTC tego dnia."""
    import calendar

    utc_midnight = calendar.timegm((year, month, day, 0, 0, 0))
    return utc_midnight - local(year, month, day, 0)


def test_pruning_applies_the_calendar_to_real_folders(tmp_path):
    destination = tmp_path / "kopia"
    destination.mkdir()
    manifest = Manifest.load(destination)
    start = local(2026, 6, 1)
    for index in range(60):
        name = beat.stamp(start + index * DAY)
        (destination / name / "Dokumenty").mkdir(parents=True)
        manifest.versions.append(name)
        manifest.runs[name] = VersionState(
            name=name, started=start + index * DAY, complete=True, labels=["Dokumenty"]
        )
    config = BackupConfig(sources=[], destination=str(destination), gfs_daily=7, gfs_weekly=4)

    removed = engine._prune_versions(destination, manifest, config, Reporter(), {"Dokumenty"})
    left = sorted(p.name for p in destination.iterdir())
    assert len(left) == len(manifest.versions) == 60 - len(removed)
    assert 7 <= len(left) <= 11
    assert left[-1] == beat.stamp(start + 59 * DAY), "najnowsza wersja zostaje"


def test_incomplete_versions_are_never_pruned(tmp_path):
    destination = tmp_path / "kopia"
    destination.mkdir()
    manifest = Manifest.load(destination)
    start = local(2026, 6, 1)
    names = []
    for index in range(5):
        name = beat.stamp(start + index * DAY)
        names.append(name)
        (destination / name / "Dokumenty").mkdir(parents=True)
        manifest.versions.append(name)
        manifest.runs[name] = VersionState(name=name, started=start + index * DAY,
                                           complete=index != 0, labels=["Dokumenty"])
    config = BackupConfig(sources=[], destination=str(destination), gfs_daily=1)
    engine._prune_versions(destination, manifest, config, Reporter(), {"Dokumenty"})
    assert (destination / names[0]).is_dir(), "niedokończona wersja nie może zniknąć automatycznie"
