"""Testy czasu BeatTime — muszą zgadzać się z apps/beat/core.py z beattime.live."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta, timezone

import pytest

from cleanvault import beat


def unix(hour: int, minute: int = 0, second: int = 0, microsecond: int = 0) -> float:
    return datetime(2026, 9, 24, hour, minute, second, microsecond, tzinfo=UTC).timestamp()


@pytest.mark.parametrize(
    ("moment", "expected"),
    [
        (unix(0, 0, 0), "@000"),
        (unix(0, 21, 36), "@015"),  # granica, na której dzielenie przez 86.4 schodzi o jeden
        (unix(12, 0, 0), "@500"),
        (unix(14, 30, 0), "@604"),
        (unix(23, 59, 59, 999999), "@999"),
    ],
)
def test_beat_matches_reference_values(moment, expected):
    assert beat.format_beat(beat.beats_from_unix(moment)) == expected


def test_centibeats_truncate_not_round():
    assert beat.format_beat(999.6) == "@999", "zaokrąglenie dałoby @1000, czyli wartość spoza zakresu"
    assert beat.format_beat(beat.beats_from_unix(unix(14, 30, 0)), decimals=2) == "@604.16"


def test_beat_wraps_within_a_day():
    assert beat.format_beat(1000.0) == "@000"
    assert beat.beats_from_unix(unix(0, 0, 0)) == 0.0


def test_stamp_uses_utc_date_not_local():
    """01:30 czasu letniego w Polsce to jeszcze poprzednia doba BeatTime."""
    moment = datetime(2026, 9, 25, 1, 30, tzinfo=timezone(timedelta(hours=2)))
    assert beat.stamp(moment.timestamp()) == "2026-09-24_@979"


def test_stamp_without_argument_uses_now():
    now = beat.stamp()
    assert len(now) == len("2026-09-24_@921")
    assert now[10] == "_" and now[11] == "@"


def test_describe_handles_beat_and_clock_names():
    assert beat.describe("2026-09-24_@921") == "24.09.2026 @921"
    assert beat.describe("2026-09-17_16-30-11") == "17.09.2026 16:30"
    assert beat.describe("cokolwiek") == "cokolwiek"
