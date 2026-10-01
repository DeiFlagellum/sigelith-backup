"""Konfiguracja logowania.

Stara wersja gubiła wszystkie tracebacki (``except Exception as e: return str(e)``),
przez co błąd typu ``'sources'`` był nie do zdiagnozowania. Tutaj każdy wyjątek
trafia do pliku z pełnym stosem, a użytkownik dostaje czytelny komunikat.
"""

from __future__ import annotations

import contextlib
import logging
import logging.handlers
import sys
from pathlib import Path

from .paths import log_dir

_LOG_FORMAT = "%(asctime)s %(levelname)-8s [%(name)s] %(message)s"
_configured = False


class QtLogBridge(logging.Handler):
    """Przekazuje rekordy logu do GUI (panel „Dziennik")."""

    def __init__(self) -> None:
        super().__init__()
        self._sink = None
        self.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-7s  %(message)s", "%H:%M:%S"))

    def set_sink(self, sink) -> None:
        self._sink = sink

    def emit(self, record: logging.LogRecord) -> None:
        sink = self._sink
        if sink is None:
            return
        # Awaria kanału logowania nie może wywrócić aplikacji ani zapętlić
        # logowania błędu o błędzie logowania.
        with contextlib.suppress(Exception):
            sink(self.format(record), record.levelno)


bridge = QtLogBridge()


def setup(verbose: bool = False) -> Path:
    """Ustawia logowanie do pliku rotowanego i na konsolę. Zwraca ścieżkę pliku."""
    global _configured
    log_file = log_dir() / "cleanvault.log"
    if _configured:
        return log_file

    root = logging.getLogger()
    root.setLevel(logging.DEBUG if verbose else logging.INFO)

    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=2_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(_LOG_FORMAT))
    file_handler.setLevel(logging.DEBUG)
    root.addHandler(file_handler)

    # W zamrożonym EXE (console=False) stdout bywa None — wtedy pomijamy konsolę.
    if sys.stderr is not None:
        # Polska konsola Windows używa cp1252/cp852 — bez tego każdy komunikat
        # ze znakiem diakrytycznym kończy się UnicodeEncodeError wewnątrz logging.
        with contextlib.suppress(AttributeError, ValueError):
            sys.stderr.reconfigure(errors="replace")
        stream = logging.StreamHandler(sys.stderr)
        stream.setFormatter(logging.Formatter(_LOG_FORMAT))
        stream.setLevel(logging.INFO)
        root.addHandler(stream)

    bridge.setLevel(logging.INFO)
    root.addHandler(bridge)

    def _hook(exc_type, exc_value, exc_tb):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_tb)
            return
        logging.getLogger("cleanvault").critical(
            "Nieobsłużony wyjątek", exc_info=(exc_type, exc_value, exc_tb)
        )

    sys.excepthook = _hook
    _configured = True
    logging.getLogger("cleanvault").info("Logowanie uruchomione: %s", log_file)
    return log_file


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"cleanvault.{name}")
