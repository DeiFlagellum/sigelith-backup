"""Równoległe operacje na plikach.

Czas kopii dużego zbioru małych plików to suma opóźnień na każdy plik, a nie
przesył bajtów. Pomiar na sprzęcie docelowym (NVMe → SSD przez USB, aktywny
Microsoft Defender) pokazał:

* pierwsze otwarcie pliku źródłowego trwa ~16 ms, prawie w całości po stronie
  skanera przy dostępie — na 8 wątkach przepustowość rośnie 7×, na 32 wątkach 13×;
* zapis na NTFS przez USB: 92 pliki/s sekwencyjnie, 409 plików/s na 32 wątkach,
  bo równoczesne ``fsync`` nośnik łączy w jedno opróżnienie bufora.

Wątki Pythona w zupełności wystarczają: odczyt, zapis, ``fsync`` i SHA-256
(``hashlib``) zwalniają GIL.
"""

from __future__ import annotations

import os
import threading
from collections.abc import Callable, Iterable, Iterator
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from pathlib import Path
from typing import Any

#: Powyżej tej liczby wątków pomiar nie pokazał już zysku, a rośnie zużycie pamięci.
MAX_DEFAULT_WORKERS = 32
MAX_WORKERS = 64


def default_workers() -> int:
    return max(4, min(MAX_DEFAULT_WORKERS, os.cpu_count() or 4))


def resolve_workers(requested: int) -> int:
    """``0`` = dobór automatyczny, inaczej wartość przycięta do rozsądnego zakresu."""
    if requested <= 0:
        return default_workers()
    return max(1, min(MAX_WORKERS, requested))


def unordered_map(
    fn: Callable[[Any], Any],
    items: Iterable[Any],
    workers: int,
    cancelled: Callable[[], bool],
) -> Iterator[tuple[Any, Any, BaseException | None]]:
    """Wykonuje ``fn`` dla elementów, zwracając ``(element, wynik, wyjątek)`` w kolejności ukończenia.

    Zadania są wysyłane porcjami (okno ograniczone do kilku na wątek), więc
    lista miliona plików nie zamienia się w milion obiektów ``Future`` naraz.
    Po przerwaniu nie wysyłamy nowych zadań, ale **zawsze** oddajemy wyniki
    tych, które już ruszyły — plik zapisany do końca musi trafić do spisu
    treści, inaczej stan kopii rozjechałby się z zawartością nośnika.

    Przy ``workers == 1`` wszystko dzieje się w bieżącym wątku, dokładnie
    w kolejności elementów.
    """
    iterator = iter(items)
    if workers <= 1:
        for item in iterator:
            if cancelled():
                return
            try:
                yield item, fn(item), None
            except Exception as exc:  # noqa: BLE001 - wyjątek oddajemy wywołującemu
                yield item, None, exc
        return

    window = workers * 4
    pool = ThreadPoolExecutor(max_workers=workers, thread_name_prefix="cleanvault")
    pending: dict[Future, Any] = {}

    def fill() -> None:
        while len(pending) < window and not cancelled():
            try:
                item = next(iterator)
            except StopIteration:
                return
            pending[pool.submit(fn, item)] = item

    try:
        fill()
        while pending:
            done, _ = wait(pending, return_when=FIRST_COMPLETED)
            for future in done:
                item = pending.pop(future)
                exc = future.exception()
                yield item, (None if exc is not None else future.result()), exc
            fill()
    finally:
        # Generator porzucony w połowie (wyjątek po stronie wywołującego):
        # nie zostawiamy wiszących zadań.
        pool.shutdown(wait=True, cancel_futures=True)


class DirectoryCache:
    """Pamięć katalogów już utworzonych w kopii.

    ``mkdir(parents=True, exist_ok=True)`` na każdy plik to zbędne wywołanie
    systemowe dla setek tysięcy plików leżących w tych samych katalogach —
    a na dysku USB każde takie wywołanie kosztuje.
    """

    def __init__(self) -> None:
        self._known: set[str] = set()
        self._lock = threading.Lock()

    def ensure(self, folder: Path) -> None:
        key = str(folder)
        if key in self._known:
            return
        folder.mkdir(parents=True, exist_ok=True)
        with self._lock:
            self._known.add(key)
