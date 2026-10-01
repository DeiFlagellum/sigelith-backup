"""Logika harmonogramu: terminy, zaległości, podłączenie dysku.

Czas jest podawany wprost (``now``), więc testy nie zależą od zegara ani od
strefy czasowej komputera, na którym się uruchamiają — poza samym przeliczeniem
„GG:MM” na czas lokalny, które sprawdzamy na dniu bez zmiany czasu.
"""

from __future__ import annotations

import time

import pytest

from cleanvault import scheduler
from cleanvault.state import Template


def local(year, month, day, hour, minute=0):
    return time.mktime((year, month, day, hour, minute, 0, 0, 0, -1))


def always(_path):
    return True


def never(_path):
    return False


def daily(at="20:00", **kwargs):
    return Template(name="Codzienna", schedule=scheduler.DAILY, schedule_time=at, destination="X:/k", **kwargs)


@pytest.mark.parametrize(
    ("text", "expected"),
    [("20:00", (20, 0)), ("7:05", (7, 5)), ("25:00", (20, 0)), ("abc", (20, 0)), ("2000", (20, 0))],
)
def test_parse_time_is_forgiving(text, expected):
    assert scheduler.parse_time(text) == expected


def test_last_and_next_slot():
    now = local(2026, 9, 15, 21, 30)
    assert scheduler.last_slot(now, "20:00") == local(2026, 9, 15, 20)
    assert scheduler.next_slot(now, "20:00") == local(2026, 9, 16, 20)
    morning = local(2026, 9, 15, 8)
    assert scheduler.last_slot(morning, "20:00") == local(2026, 9, 14, 20)
    assert scheduler.next_slot(morning, "20:00") == local(2026, 9, 15, 20)


def test_daily_runs_once_per_slot():
    template = daily(last_attempt=local(2026, 9, 14, 20, 1))
    now = local(2026, 9, 15, 20, 0, ) + 30
    due = scheduler.due_templates([template], now, always)
    assert [d.template_id for d in due] == [template.id]
    assert due[0].reason == "daily"

    template.last_attempt = now  # próba zrobiona — także nieudana liczy się jako próba
    assert scheduler.due_templates([template], now + 60, always) == []
    assert scheduler.due_templates([template], local(2026, 9, 16, 19, 59), always) == []
    assert scheduler.due_templates([template], local(2026, 9, 16, 20, 0), always)


def test_missed_slot_is_caught_up_after_power_on():
    """Komputer wyłączony o 20:00 — kopia rusza po włączeniu następnego ranka."""
    template = daily(last_attempt=local(2026, 9, 14, 20, 0))
    due = scheduler.due_templates([template], local(2026, 9, 16, 8, 0), always)
    assert due and due[0].reason == "missed"


def test_new_schedule_waits_for_the_next_slot():
    template = daily()
    scheduler.arm(template, now=local(2026, 9, 15, 21, 0))
    assert scheduler.due_templates([template], local(2026, 9, 15, 21, 1), always) == []
    assert scheduler.due_templates([template], local(2026, 9, 16, 20, 0), always)


def test_daily_waits_for_the_drive():
    template = daily(last_attempt=local(2026, 9, 14, 20, 1))
    now = local(2026, 9, 15, 20, 5)
    assert scheduler.due_templates([template], now, never) == []
    # dysk podłączony godzinę później — zaległy termin wciąż czeka na wykonanie
    assert scheduler.due_templates([template], now + 3600, always)


def test_on_connect_fires_when_the_drive_appears():
    template = Template(name="USB", schedule=scheduler.ON_CONNECT, destination="E:/kopia")
    now = local(2026, 9, 15, 10)
    assert scheduler.due_templates([template], now, never, seen={template.id: False}) == []
    due = scheduler.due_templates([template], now, always, seen={template.id: False})
    assert due and due[0].reason == "connected"
    # dysk cały czas podłączony — nie ma nowego zdarzenia
    assert scheduler.due_templates([template], now + 60, always, seen={template.id: True}) == []


def test_on_connect_is_limited_to_once_per_twelve_hours():
    now = local(2026, 9, 15, 10)
    template = Template(name="USB", schedule=scheduler.ON_CONNECT, destination="E:/k", last_attempt=now - 3600)
    assert scheduler.due_templates([template], now, always, seen={template.id: False}) == []
    template.last_attempt = now - scheduler.ON_CONNECT_MIN_GAP - 1
    assert scheduler.due_templates([template], now, always, seen={template.id: False})


def test_first_check_after_start_counts_as_connection():
    template = Template(name="USB", schedule=scheduler.ON_CONNECT, destination="E:/k")
    assert scheduler.due_templates([template], local(2026, 9, 15, 10), always, seen={})


def test_manual_templates_never_run_by_themselves():
    template = Template(name="Ręczna", destination="E:/k")
    assert template.schedule == scheduler.MANUAL
    assert scheduler.due_templates([template], time.time(), always) == []


def test_overdue_reminder():
    now = local(2026, 9, 30, 12)
    fresh = daily(last_success=now - 3600)
    stale = daily(last_success=now - 8 * 86400)
    never_ran = daily(created=now - 10 * 86400)
    manual = Template(name="Ręczna", last_success=0, created=now - 30 * 86400)
    late = scheduler.overdue_templates([fresh, stale, never_ran, manual], now)
    assert [t.id for t in late] == [stale.id, never_ran.id]


def test_destination_available_checks_the_drive(tmp_path):
    assert scheduler.destination_available(str(tmp_path / "jeszcze-nie-ma"))
    assert not scheduler.destination_available(str(tmp_path / "a" / "b" / "c"))
    assert not scheduler.destination_available("")


def test_old_state_files_load_with_manual_schedule():
    raw = {"id": "abc", "name": "Stara", "sources": ["C:/x"], "destination": "E:/k"}
    template = Template.from_dict(raw)
    assert template.schedule == scheduler.MANUAL
    assert template.last_success == 0.0
