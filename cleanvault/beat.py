"""Czas BeatTime — znaczniki używane w nazwach katalogów wersji kopii.

Doba to 1000 beatów (1 beat = 86,4 s), kotwica w **UTC**. To standard
z projektu użytkownika (``beattime.live``); wzorcowa implementacja mieszka
w ``apps/beat/core.py`` tamtego repozytorium i ten moduł musi liczyć dokładnie
to samo — inaczej nazwa katalogu kopii kłóciłaby się z zegarem.

Dwie rzeczy, w których łatwo się pomylić i które są tu celowo zrobione inaczej,
niż podpowiada intuicja:

* beat liczymy z **całkowitych mikrosekund doby dzielonych przez 86 400 000**,
  a nie przez dzielenie sekund przez ``86.4``. Ta wartość nie ma dokładnej
  reprezentacji binarnej, więc zaokrąglenie w dół potrafi zejść o jeden na
  granicy (00:21:36 to dokładnie ``@015``, a nie ``@014``);
* formatujemy przez **obcięcie**, nie zaokrąglenie — ``999.6`` zaokrąglone
  dałoby ``@1000``, czyli wartość spoza zakresu.

Data w znaczniku jest **datą UTC**. Skoro beat jest kotwiczony w UTC, to data
liczona lokalnie rozjeżdżałaby się z nim co noc: o 01:30 czasu letniego
w Polsce zegar BeatTime pokazuje jeszcze poprzednią dobę.
"""

from __future__ import annotations

import math
import time
from datetime import UTC, datetime

from .i18n import isolate, tr

SECONDS_PER_DAY = 86_400
BEATS_PER_DAY = 1_000
#: 86 400 000 000 mikrosekund doby / 1000 beatów — liczba całkowita, bez błędu binarnego.
MICROSECONDS_PER_BEAT = 86_400_000


def beats_from_unix(unix_seconds: float) -> float:
    """Dokładny czas beat w zakresie [0, 1000) dla znacznika uniksowego."""
    microseconds_of_day = round((unix_seconds % SECONDS_PER_DAY) * 1_000_000)
    return (microseconds_of_day / MICROSECONDS_PER_BEAT) % BEATS_PER_DAY


def format_beat(beats: float, decimals: int = 0) -> str:
    """Formatuje do ``@NNN`` (albo ``@NNN.dd`` dla setnych beata)."""
    if decimals < 0:
        raise ValueError("decimals musi być >= 0")
    beats = beats % BEATS_PER_DAY
    factor = 10**decimals
    truncated = math.floor(beats * factor) / factor
    width = 3 + (decimals + 1 if decimals else 0)
    return f"@{truncated:0{width}.{decimals}f}"


def stamp(unix_seconds: float | None = None) -> str:
    """Znacznik do nazwy katalogu wersji: ``RRRR-MM-DD_@NNN`` w UTC."""
    moment = time.time() if unix_seconds is None else unix_seconds
    day = datetime.fromtimestamp(moment, tz=UTC).strftime("%Y-%m-%d")
    return f"{day}_{format_beat(beats_from_unix(moment))}"


def unix_from_stamp(stamp_text: str) -> float | None:
    """Chwila utworzenia wersji z nazwy katalogu (``RRRR-MM-DD_@NNN`` w UTC).

    Obsługuje też stary zapis zegarowy (``RRRR-MM-DD_GG-MM-SS``, czas lokalny)
    oraz przyrostki: ``_2`` (unikalność) i ``--…`` (data uzupełnienia).
    """
    created = stamp_text.partition("--")[0]
    day, _, clock = created.partition("_")
    clock = clock.partition("_")[0]
    try:
        midnight = datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=UTC).timestamp()
    except ValueError:
        return None
    if clock.startswith("@"):
        try:
            return midnight + float(clock[1:]) * SECONDS_PER_DAY / BEATS_PER_DAY
        except ValueError:
            return midnight
    try:
        return time.mktime(time.strptime(f"{day} {clock}", "%Y-%m-%d %H-%M-%S"))
    except ValueError:
        return midnight


def describe(stamp_text: str) -> str:
    """Znacznik w postaci czytelnej dla człowieka: ``24.09.2026 @921``.

    Obsługuje też stary format zegarowy (``2026-09-17_16-30-11``), bo takie
    katalogi leżą już na dyskach użytkowników.
    """
    day, _, clock = stamp_text.partition("_")
    # Przyrostek unikalności („_2” przy dwóch kopiach w tym samym beacie)
    # jest szczegółem technicznym i nie ma czego szukać w opisie dla człowieka.
    clock = clock.partition("_")[0]
    try:
        readable = time.strftime(tr("%d.%m.%Y"), time.strptime(day, "%Y-%m-%d"))
    except ValueError:
        return stamp_text
    if clock.startswith("@"):
        # po arabsku „@921” obok daty czytałby się jako „921@” (i18n.isolate)
        return f"{readable} {isolate(clock)}"
    try:
        return f"{readable} {time.strftime('%H:%M', time.strptime(clock, '%H-%M-%S'))}"
    except ValueError:
        return readable
