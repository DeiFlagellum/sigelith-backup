"""Harmonogram kopii — sama logika terminów, bez Qt.

Aplikacja ze Sklepu Microsoft nie może zakładać zadań w Harmonogramie Windows
tak jak zwykły program, więc terminy pilnuje sam program działający w tle
(ikona przy zegarze, start przy logowaniu). Ten moduł odpowiada wyłącznie na
pytanie „które szablony należy teraz uruchomić” — odmierzanie czasu i samo
uruchamianie kopii należą do interfejsu.

Zasady, które łatwo zepsuć i które pilnują testy:

* **jedna próba na termin.** Po próbie (także nieudanej) szablon czeka na
  następny termin — inaczej kopia, która się wywraca, ponawiałaby się co pół
  minuty i zajeżdżała dysk;
* **zaległy termin nadrabiamy.** Komputer wyłączony o 20:00 zrobi kopię po
  włączeniu, a nie dopiero następnego dnia;
* **nowy harmonogram nie strzela od razu.** Ustawienie „codziennie o 20:00”
  o 21:00 oznacza pierwszą kopię jutro o 20:00 — dlatego przy zmianie
  harmonogramu ``last_attempt`` dostaje bieżący czas (patrz :func:`arm`).
"""

from __future__ import annotations

import os
import time
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path

from .state import Template

MANUAL = "manual"
DAILY = "daily"
ON_CONNECT = "on_connect"
#: „Na bieżąco”: zmiany w źródłach dogrywane kilka minut po zapisie, a po podłączeniu
#: dysku z kopią — od razu (patrz :mod:`cleanvault.live`).
LIVE = "live"
SCHEDULES = (MANUAL, DAILY, ON_CONNECT, LIVE)

DEFAULT_TIME = "20:00"
_DEFAULT_CLOCK = (20, 0)
#: „Po podłączeniu dysku” — najwyżej raz na tyle sekund. Dysk odłączony
#: i podłączony po godzinie nie powinien wywoływać drugiej pełnej kopii.
ON_CONNECT_MIN_GAP = 12 * 3600
#: „Na bieżąco” po podłączeniu dysku — najwyżej raz na tyle sekund.
LIVE_CONNECT_GAP = 10 * 60
#: Po tylu dniach bez udanej kopii program przypomina o zaległości.
OVERDUE_AFTER = 7 * 24 * 3600


@dataclass(frozen=True)
class Due:
    """Szablon do uruchomienia i powód — powód trafia do dziennika i powiadomienia."""

    template_id: str
    reason: str  # "daily" | "missed" | "connected"


def parse_time(text: str) -> tuple[int, int]:
    """``"20:00"`` → ``(20, 0)``; zapis niepoprawny daje godzinę domyślną."""
    try:
        hours, minutes = (int(part) for part in str(text).split(":", 1))
    except ValueError:
        return _DEFAULT_CLOCK
    if not (0 <= hours < 24 and 0 <= minutes < 60):
        return _DEFAULT_CLOCK
    return hours, minutes


def last_slot(now: float, hhmm: str) -> float:
    """Ostatni termin „GG:MM” czasu lokalnego, który już minął (albo trwa)."""
    hours, minutes = parse_time(hhmm)
    today = time.localtime(now)
    candidate = time.mktime((today.tm_year, today.tm_mon, today.tm_mday, hours, minutes, 0, 0, 0, -1))
    if candidate <= now:
        return candidate
    yesterday = time.localtime(now - 86400)
    return time.mktime(
        (yesterday.tm_year, yesterday.tm_mon, yesterday.tm_mday, hours, minutes, 0, 0, 0, -1)
    )


def next_slot(now: float, hhmm: str) -> float:
    """Najbliższy przyszły termin — do opisu „następna kopia: …” w interfejsie."""
    hours, minutes = parse_time(hhmm)
    day = time.localtime(now)
    candidate = time.mktime((day.tm_year, day.tm_mon, day.tm_mday, hours, minutes, 0, 0, 0, -1))
    if candidate > now:
        return candidate
    tomorrow = time.localtime(now + 86400)
    return time.mktime((tomorrow.tm_year, tomorrow.tm_mon, tomorrow.tm_mday, hours, minutes, 0, 0, 0, -1))


def destination_available(destination: str) -> bool:
    """Czy nośnik docelowy jest podłączony — sam katalog kopii może jeszcze nie istnieć."""
    if not destination:
        return False
    path = Path(destination)
    anchor = path.anchor or os.sep
    try:
        return Path(anchor).exists() and (path.exists() or path.parent.exists())
    except OSError:
        return False


def arm(template: Template, now: float | None = None) -> None:
    """Uzbraja harmonogram po jego zmianie: bieżący termin uznajemy za obsłużony."""
    template.last_attempt = time.time() if now is None else now


def due_templates(
    templates: Iterable[Template],
    now: float,
    available: Callable[[str], bool] = destination_available,
    seen: Mapping[str, bool] | None = None,
) -> list[Due]:
    """Szablony, które trzeba uruchomić teraz.

    ``seen`` to dostępność nośnika przy poprzednim sprawdzeniu (klucz: id
    szablonu). Dla „po podłączeniu dysku” liczy się przejście z „niedostępny”
    do „dostępny”; brak wpisu (pierwsze sprawdzenie po starcie programu) też
    jest takim przejściem — dysk podłączony na stałe dostanie kopię po starcie.
    """
    seen = seen or {}
    result: list[Due] = []
    for template in templates:
        if template.schedule == DAILY:
            slot = last_slot(now, template.schedule_time)
            if (template.last_attempt or 0.0) < slot and available(template.destination):
                late = now - slot > 15 * 60
                result.append(Due(template.id, "missed" if late else "daily"))
        elif template.schedule in (ON_CONNECT, LIVE):
            connected_now = available(template.destination)
            was_connected = seen.get(template.id)
            appeared = connected_now and was_connected is not True
            # „na bieżąco” synchronizuje po każdym podłączeniu — dogrywka jest tania
            gap = LIVE_CONNECT_GAP if template.schedule == LIVE else ON_CONNECT_MIN_GAP
            if appeared and now - (template.last_attempt or 0.0) >= gap:
                result.append(Due(template.id, "connected"))
    return result


def overdue_templates(templates: Iterable[Template], now: float) -> list[Template]:
    """Szablony z harmonogramem, które od dawna nie dały udanej kopii."""
    late = []
    for template in templates:
        if template.schedule == MANUAL:
            continue
        reference = template.last_success or template.created
        if now - reference > OVERDUE_AFTER:
            late.append(template)
    return late
