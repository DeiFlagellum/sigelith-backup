"""Trwały stan aplikacji: szablony, ustawienia, historia.

Poprawki względem 1.x:

* **Zapis atomowy** (plik tymczasowy + ``fsync`` + ``os.replace``). Stara wersja
  otwierała plik docelowy w trybie ``wb`` i pisała w miejscu — przerwanie zapisu
  zostawiało obcięty plik, a wczytanie go wywalało aplikację przy starcie.
  W narzędziu do backupu utrata wszystkich szablonów przez jeden zanik zasilania
  była realnym scenariuszem.
* **Suma kontrolna SHA-256** w kopercie pliku — wykrywa obcięcie i uszkodzenie
  nośnika, zanim msgpack wyprodukuje niejasny wyjątek.
* **Kopia zapasowa poprzedniego stanu** (``.bak``) i automatyczne odzyskiwanie.
* **Brak twardych indeksów** (``data["files"]``) — każdy odczyt ma wartość
  domyślną, więc niepełny plik stanu nie blokuje uruchomienia programu.
* **Hasła nigdy nie trafiają do stanu.** Wcześniej ``perform_backup`` zapisywał
  je otwartym tekstem obok listy plików, co całkowicie unieważniało szyfrowanie.
"""

from __future__ import annotations

import hashlib
import os
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import msgpack

from .i18n import tr
from .log import get_logger
from .paths import legacy_state_file, long_path, state_file

log = get_logger("state")

STATE_MAGIC = b"CVST"
STATE_VERSION = 2

DEFAULT_EXCLUDES = [
    "Thumbs.db",
    "desktop.ini",
    ".DS_Store",
    "~$*",
    "*.tmp",
    "*.part",
    "*.crdownload",
    "System Volume Information/*",
    "$RECYCLE.BIN/*",
    # Celowo bez ".git/*": wzorce katalogowe działają na każdej głębokości, więc
    # wykluczałby historię wszystkich repozytoriów — a tej nie da się odtworzyć,
    # jeśli nie była wypchnięta na serwer.
    "__pycache__/*",
    "node_modules/*",
    # Środowiska Pythona da się odtworzyć poleceniem instalacji zależności,
    # a potrafią stanowić jedną trzecią wszystkich plików kopii.
    ".venv/*",
    "venv/*",
]


@dataclass
class Template:
    """Zapamiętana konfiguracja kopii zapasowej.

    Uwaga: pole ``password`` nie istnieje celowo. Jeśli użytkownik włączy
    ``remember_password``, hasło ląduje w Menedżerze poświadczeń Windows
    (patrz :mod:`cleanvault.secrets_store`), a tutaj zostaje tylko flaga.
    """

    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    name: str = "Nowy szablon"
    sources: list[str] = field(default_factory=list)
    destination: str = ""
    structure: str = "dated"  # "dated" | "mirror"
    encrypt: bool = False
    remember_password: bool = False
    verify_after_write: bool = False
    excludes: list[str] = field(default_factory=lambda: list(DEFAULT_EXCLUDES))
    retention: int = 0  # ile wersji zachować przy strukturze "dated"; 0 = wszystkie
    #: retencja kalendarzowa (GFS): najnowsza wersja z każdego z tylu ostatnich
    #: dni, tygodni i miesięcy; 0 wyłącza daną zasadę
    gfs_daily: int = 0
    gfs_weekly: int = 0
    gfs_monthly: int = 0
    #: ile przebiegów uzupełniających po kopii (dogrywka zmian powstałych w jej
    #: trakcie); 0 = wyłączone
    catchup_passes: int = 1
    #: ile plików przetwarzać równocześnie; 0 = dobór automatyczny
    workers: int = 0
    #: czy dopisywać do nazwy katalogu wersji datę jej ostatniego uzupełnienia
    stamp_updates: bool = True
    #: duże pliki zapisuj fragmentami (nowa wersja zapisuje tylko zmienione fragmenty)
    delta: bool = True
    #: znakuj wersje czasem Sigelith (do usługi trafia tylko suma kontrolna spisu)
    timestamp: bool = False
    #: chroń dowody Sigelith Desktop: jego folder danych i oznakowane dokumenty
    sigelith: bool = False
    #: kopia poza domem: ustawienia usługi S3 — bez sekretów, które leżą
    #: w Menedżerze poświadczeń Windows (patrz :mod:`cleanvault.ui.cloud`)
    offsite: dict = field(default_factory=dict)
    offsite_enabled: bool = False
    offsite_keep: int = 30
    offsite_last: float = 0.0
    offsite_last_result: str = ""
    created: float = field(default_factory=time.time)
    last_run: float | None = None
    last_result: str | None = None
    #: kiedy kopia uruchamia się sama: "manual" | "daily" | "on_connect"
    #: (logika terminów: :mod:`cleanvault.scheduler`)
    schedule: str = "manual"
    #: godzina kopii codziennej, "GG:MM" czasu lokalnego
    schedule_time: str = "20:00"
    #: ostatnia próba uruchomienia z harmonogramu, także nieudana — jedna próba
    #: na termin, inaczej wywracająca się kopia ponawiałaby się co pół minuty
    last_attempt: float = 0.0
    #: ostatnia kopia zakończona bez błędów — podstawa przypomnień o zaległości
    last_success: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Template:
        """Tolerancyjna deserializacja: nieznane pola ignorujemy, brakujące
        dostają wartości domyślne. Dzięki temu starszy plik stanu nigdy nie
        wywraca wczytywania."""
        known = {f for f in cls.__dataclass_fields__}
        data = {k: v for k, v in raw.items() if k in known}
        # Migracja z 1.x: klucz nazywał się "source" przy zapisie, a był czytany
        # jako "sources" — przez co przywracanie z szablonu nigdy nie działało.
        if "sources" not in data and "source" in raw:
            legacy = raw["source"]
            data["sources"] = list(legacy) if isinstance(legacy, (list, tuple)) else [legacy]
        if "structure" not in data and "auto_structure" in raw:
            data["structure"] = "dated" if raw["auto_structure"] else "mirror"
        data.setdefault("id", uuid.uuid4().hex[:12])
        return cls(**data)


def _default_state() -> dict[str, Any]:
    return {
        "version": STATE_VERSION,
        "templates": {},
        "settings": {
            "theme": "dark",
            "accent": "#f59e0b",
            "confirm_before_overwrite": True,
            "verify_after_write": False,
            "show_hints": True,
        },
        "history": [],
    }


class StateStore:
    """Magazyn stanu z zapisem atomowym i odzyskiwaniem po uszkodzeniu."""

    MAX_HISTORY = 200

    def __init__(self, path: Path | None = None) -> None:
        # Import stanu 1.x dotyczy wyłącznie domyślnej lokalizacji. Magazyn
        # utworzony ze wskazaną ścieżką (testy, eksport) musi być niezależny
        # od tego, co akurat leży w katalogu roboczym.
        self._uses_default_location = path is None
        self.path = Path(path) if path else state_file()
        self.backup_path = self.path.with_suffix(self.path.suffix + ".bak")
        self.data: dict[str, Any] = self._load()

    # ------------------------------------------------------------------ I/O

    def _load(self) -> dict[str, Any]:
        for candidate, label in ((self.path, "stan"), (self.backup_path, "kopia zapasowa stanu")):
            if not candidate.exists():
                continue
            try:
                data = self._read_envelope(candidate)
            except Exception as exc:  # noqa: BLE001 - chcemy przeżyć każdy rodzaj uszkodzenia
                log.error("Nie udało się wczytać %s (%s): %s", label, candidate, exc)
                if candidate is self.path:
                    self._quarantine(candidate)
                continue
            log.info("Wczytano %s: %d szablonów", label, len(data.get("templates", {})))
            return self._normalise(data)

        # Jednorazowy import stanu z 1.x, który leżał w katalogu roboczym.
        # Szablony przenosimy (z poprawionym kluczem "sources"), hasła — nie.
        legacy = legacy_state_file()
        if self._uses_default_location and legacy.exists():
            try:
                data = self._read_envelope(legacy)
                log.info("Znaleziono stan wersji 1.x (%s) — migruję szablony.", legacy)
                return self._normalise(data)
            except Exception as exc:  # noqa: BLE001
                log.error("Nie udało się zaimportować stanu 1.x: %s", exc)

        log.info("Brak zapisanego stanu — startuję z konfiguracją domyślną.")
        return _default_state()

    @staticmethod
    def _read_envelope(path: Path) -> dict[str, Any]:
        blob = Path(long_path(path)).read_bytes()
        if len(blob) < len(STATE_MAGIC) + 1 + 32:
            raise ValueError(tr("plik stanu jest za krótki"))
        if blob[: len(STATE_MAGIC)] != STATE_MAGIC:
            # Plik z 1.x: goły msgpack bez koperty.
            return msgpack.unpackb(blob, raw=False)
        offset = len(STATE_MAGIC)
        version = blob[offset]
        offset += 1
        digest = blob[offset : offset + 32]
        offset += 32
        payload = blob[offset:]
        if hashlib.sha256(payload).digest() != digest:
            raise ValueError(tr("suma kontrolna się nie zgadza — plik uszkodzony"))
        if version > STATE_VERSION:
            raise ValueError(
                tr("plik stanu w wersji {found}, obsługiwana: {supported}").format(
                    found=version, supported=STATE_VERSION
                )
            )
        return msgpack.unpackb(payload, raw=False)

    @staticmethod
    def _normalise(data: dict[str, Any]) -> dict[str, Any]:
        """Uzupełnia brakujące sekcje i migruje układ z 1.x."""
        base = _default_state()
        if not isinstance(data, dict):
            return base

        if int(data.get("version", 1)) >= 2:
            base["settings"].update(data.get("settings") or {})
            templates = data.get("templates") or {}
        else:
            # 1.x trzymało szablony pod kluczem "settings", wymieszane z ustawieniami.
            templates = {
                k: v
                for k, v in (data.get("settings") or {}).items()
                if isinstance(v, dict) and ("source" in v or "sources" in v)
            }
            if templates:
                log.info("Migruję %d szablonów z formatu 1.x.", len(templates))
        for key, raw in (templates or {}).items():
            if not isinstance(raw, dict):
                continue
            template = Template.from_dict({**raw, "id": raw.get("id", str(key))})
            if raw.get("password"):
                # Hasło z 1.x leżało tu otwartym tekstem. Nie przenosimy go.
                log.warning(
                    "Szablon %r zawierał hasło zapisane jawnie — zostało usunięte "
                    "przy migracji. Włącz opcję zapamiętywania hasła, aby trzymać je "
                    "w Menedżerze poświadczeń Windows.",
                    template.name,
                )
            base["templates"][template.id] = template.to_dict()

        history = data.get("history")
        if isinstance(history, list):
            base["history"] = history[-StateStore.MAX_HISTORY :]
        return base

    def _quarantine(self, path: Path) -> None:
        target = path.with_name(f"{path.name}.corrupt-{int(time.time())}")
        try:
            os.replace(long_path(path), long_path(target))
            log.warning("Uszkodzony plik stanu odłożony na bok: %s", target)
        except OSError as exc:
            log.error("Nie udało się odłożyć uszkodzonego pliku stanu: %s", exc)

    def save(self) -> None:
        """Zapisuje stan atomowo, zachowując poprzednią wersję jako ``.bak``."""
        payload = msgpack.packb(self.data, use_bin_type=True)
        envelope = STATE_MAGIC + bytes([STATE_VERSION]) + hashlib.sha256(payload).digest() + payload

        tmp = self.path.with_name(self.path.name + ".tmp")
        with open(long_path(tmp), "wb") as handle:
            handle.write(envelope)
            handle.flush()
            os.fsync(handle.fileno())
        if self.path.exists():
            try:
                os.replace(long_path(self.path), long_path(self.backup_path))
            except OSError as exc:
                log.warning("Nie udało się odświeżyć kopii zapasowej stanu: %s", exc)
        os.replace(long_path(tmp), long_path(self.path))
        log.debug("Stan zapisany (%d B).", len(envelope))

    # ------------------------------------------------------------- szablony

    def templates(self) -> dict[str, Template]:
        return {tid: Template.from_dict(raw) for tid, raw in self.data["templates"].items()}

    def get_template(self, template_id: str) -> Template | None:
        raw = self.data["templates"].get(template_id)
        return Template.from_dict(raw) if raw else None

    def put_template(self, template: Template) -> Template:
        self.data["templates"][template.id] = template.to_dict()
        self.save()
        return template

    def delete_template(self, template_id: str) -> bool:
        if template_id in self.data["templates"]:
            del self.data["templates"][template_id]
            self.save()
            return True
        return False

    # ------------------------------------------------------------ ustawienia

    def setting(self, key: str, default: Any = None) -> Any:
        return self.data["settings"].get(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        self.data["settings"][key] = value
        self.save()

    # -------------------------------------------------------------- historia

    def add_history(self, entry: dict[str, Any]) -> None:
        entry.setdefault("at", time.time())
        self.data["history"].append(entry)
        del self.data["history"][: -self.MAX_HISTORY]
        self.save()

    def history(self, limit: int = 50) -> list[dict[str, Any]]:
        return list(reversed(self.data["history"][-limit:]))
