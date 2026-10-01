"""Sigelith Desktop: odnajdywanie jego danych i odczyt historii stempli (tylko odczyt).

Sigelith Desktop (dawniej BeatStamp, ten sam wydawca) znakuje dokumenty czasem:
w swojej historii trzyma sumę SHA-256 dokumentu, drogę w drzewie Merkle'a tygodnia
i podpis Ed25519. Sam dokument zostaje tam, gdzie był — a dowód bez **dokładnie
tych samych bajtów** niczego nie dowodzi. Do tego folderu danych Sigelith nie
obejmuje ani OneDrive, ani Kopia zapasowa Windows, a historia ma sufit i obcina
najstarsze wpisy. Sigelith Backup kopiuje więc folder danych jak zwykłe źródło,
a oznakowane dokumenty zabezpiecza w osobnym magazynie (patrz :mod:`cleanvault.evidence`).

Kontrakt z Sigelith Desktop (uzgodniony z projektem beattime, desktop/ROZWOJ.md):

* folder danych: zmienna ``SIGELITH_DATA_DIR`` (albo dawna ``BEATSTAMP_DATA_DIR``),
  inaczej wskaźnik ``%LOCALAPPDATA%\\Sigelith\\katalog-danych.json`` ``{"katalog": …}``
  (dawniej ``…\\BeatStamp\\``), inaczej ``%USERPROFILE%\\Sigelith`` (dawniej ``BeatStamp``);
* ``history.json``: lista wpisów (albo słownik z kluczem ``entries``) z polami
  ``digest``, ``file_name``, ``file_path``, ``file_size``, ``utc``, ``beat``, ``week``,
  ``week_closed``, ``week_root``, ``inclusion_proof``, ``root_signature``,
  ``public_key`` i dalszymi, które przepisujemy do ``.beatproof``.

Program niczego w folderze Sigelith nie zapisuje.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from . import __app_name__, __version__, proof
from .log import get_logger

log = get_logger("sigelith")

DATA_DIR_NAMES = ("Sigelith", "BeatStamp")  # nowa nazwa, potem sprzed 3.0
DATA_DIR_ENVS = ("SIGELITH_DATA_DIR", "BEATSTAMP_DATA_DIR")
POINTER_NAME = "katalog-danych.json"
HISTORY_NAME = "history.json"
#: Rodziny pakietów MSIX Sigelith Desktop. Spakowana aplikacja, która tworzy nowy
#: folder prosto w ``%LOCALAPPDATA%``, dostaje go w prywatnej kopii pakietu
#: (``Packages\\<rodzina>\\LocalCache\\Local``) — tam też szukamy wskaźnika.
PACKAGE_PREFIXES = ("AdamKoch.SigelithDesktop_", "AdamKoch.BeatStamp_")
#: Format pliku dowodu — ten sam, który wystawia Sigelith Desktop (bundle.py).
BEATPROOF_FORMAT = "beatproof-v1"
BEATPROOF_SUFFIX = ".beatproof"
AUTHORITY = "https://sigelith.org"
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
#: Sigelith Desktop w Microsoft Store (Store ID z Partner Center, sprawdzony 2026-09-30) i na stronie.
STORE_PRODUCT_ID = "9N5XK65GTF33"
WEB_PAGES = {"pl": "https://sigelith.org/pl/desktop/", "de": "https://sigelith.org/de/desktop/"}
WEB_PAGE = "https://sigelith.org/desktop/"
#: Wpisy przeniesione ze starego TVS nie mają dowodu — to tylko archiwum.
_LEGACY_SOURCE = "tvs-legacy"


@dataclass
class Stamp:
    """Jeden stempel z historii Sigelith — to, co potrzebne do zabezpieczenia dokumentu."""

    digest: str
    file_name: str = ""
    file_path: str = ""
    file_size: int = 0
    utc: str = ""
    week: str = ""
    raw: dict = field(default_factory=dict)

    @property
    def complete(self) -> bool:
        """Tydzień zamknięty i korzeń podpisany — dowód da się sprawdzić bez sieci."""
        return bool(self.raw.get("week_closed") and self.raw.get("root_signature")
                    and self.raw.get("week_root") and self.raw.get("inclusion_proof") is not None)

    @property
    def date(self) -> str:
        return self.utc[:10] if len(self.utc) >= 10 else ""


def product_url(language: str, packaged: bool) -> str:
    """Gdzie poznać i zdobyć Sigelith Desktop.

    Wersja ze Sklepu prowadzi wyłącznie do karty w Sklepie: zasada 10.1.5 pozwala polecać
    własne produkty tylko wtedy, gdy zdobywa się je przez Sklep. Poza Sklepem — strona
    programu w języku interfejsu.
    """
    if packaged:
        return f"ms-windows-store://pdp/?productid={STORE_PRODUCT_ID}"
    return WEB_PAGES.get(language, WEB_PAGE)


#: Alias Sigelith Desktop (od 3.0.1, manifest paczki): ``sigelith-desktop.exe --handover <plik>``
#: otwiera okno wysyłki Sigelith Handover z tym plikiem — odbiorca potwierdza odbiór
#: własnym kluczem, a chwila doręczenia trafia do publicznego dziennika.
DESKTOP_ALIAS = "sigelith-desktop.exe"
HANDOVER_FLAG = "--handover"


def desktop_launcher() -> str | None:
    """Ścieżka aliasu Sigelith Desktop albo ``None`` (brak programu albo wersja sprzed 3.0.1)."""
    if os.name != "nt":
        return None
    return shutil.which(DESKTOP_ALIAS)


def hand_over(path: Path) -> bool:
    """Otwiera w Sigelith Desktop okno wysyłki Handover z plikiem; ``False`` = nie ma czym."""
    launcher = desktop_launcher()
    if launcher is None:
        return False
    subprocess.Popen([launcher, HANDOVER_FLAG, str(path)], close_fds=True)
    return True


def _pointed_dir(pointer: Path) -> tuple[bool, Path | None]:
    """(czy wskaźnik istnieje, wskazany folder albo ``None`` = domyślny)."""
    try:
        if not pointer.is_file():
            return False, None
        raw = json.loads(pointer.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return True, None
    value = raw.get("katalog") if isinstance(raw, dict) else None
    if not isinstance(value, str) or not value.strip():
        return True, None
    chosen = Path(value.strip()).expanduser()
    return True, (chosen if chosen.is_absolute() else None)


def _pointer_locations(local: Path) -> list[Path]:
    """Wskaźniki w kolejności ważności: nowy, spakowany nowy, dawny, spakowany dawny."""
    found: list[Path] = []
    for index, name in enumerate(DATA_DIR_NAMES):
        found.append(local / name / POINTER_NAME)
        packages = local / "Packages"
        try:
            families = sorted(p for p in packages.iterdir() if p.name.startswith(PACKAGE_PREFIXES[index]))
        except OSError:
            families = []
        found += [family / "LocalCache" / "Local" / name / POINTER_NAME for family in families]
    return found


def candidate_dirs(env: Mapping[str, str] | None = None) -> list[Path]:
    """Miejsca, w których może leżeć folder danych — w kolejności, w jakiej wybiera je Sigelith."""
    env = os.environ if env is None else env
    for name in DATA_DIR_ENVS:
        value = (env.get(name) or "").strip()
        if value:
            return [Path(value).expanduser()]  # wymuszony — Sigelith nie patrzy wtedy nigdzie indziej
    local = Path(env.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local")
    profile = Path(env.get("USERPROFILE") or Path.home())
    candidates: list[Path] = []
    for pointer in _pointer_locations(local):
        exists, chosen = _pointed_dir(pointer)
        if chosen is not None:
            candidates.append(chosen)
        if exists:
            break  # pierwszy istniejący wskaźnik rozstrzyga (pusty = folder domyślny)
    candidates += [profile / name for name in DATA_DIR_NAMES]
    return list(dict.fromkeys(candidates))


def find_data_dir(env: Mapping[str, str] | None = None) -> Path | None:
    """Folder danych Sigelith Desktop z historią stempli albo ``None``, gdy go nie ma."""
    for folder in candidate_dirs(env):
        try:
            if (folder / HISTORY_NAME).is_file():
                return folder
        except OSError:
            continue
    return None


def load_stamps(data_dir: Path) -> list[Stamp]:
    """Stemple z historii Sigelith, bez duplikatów sumy; wpisy bez dowodu są pomijane."""
    try:
        raw = json.loads((data_dir / HISTORY_NAME).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        log.warning("Nie da się odczytać historii Sigelith w %s: %s", data_dir, exc)
        return []
    items = raw if isinstance(raw, list) else raw.get("entries") if isinstance(raw, dict) else None
    by_digest: dict[str, Stamp] = {}
    for item in items or []:
        if not isinstance(item, dict) or item.get("source") == _LEGACY_SOURCE:
            continue
        digest = str(item.get("digest") or "").strip().lower()
        if not _DIGEST.match(digest):
            continue
        try:
            size = int(item.get("file_size") or 0)
        except (TypeError, ValueError):
            size = 0
        stamp = Stamp(digest, str(item.get("file_name") or ""), str(item.get("file_path") or ""), size,
                      str(item.get("utc") or ""), str(item.get("week") or ""), dict(item))
        previous = by_digest.get(digest)
        # ten sam dokument oznakowany kilka razy: wygrywa wpis z kompletnym dowodem i ścieżką
        if previous is None or (stamp.complete, bool(stamp.file_path)) > (previous.complete, bool(previous.file_path)):
            by_digest[digest] = stamp
    return list(by_digest.values())


def beatproof(stamp: Stamp) -> dict:
    """Plik dowodu ``beatproof-v1`` — te same pola, które zapisuje Sigelith Desktop.

    Bez sekcji ``checkpoint``: jej plik leży w katalogu świadka Sigelith, a format
    traktuje ją jako opcjonalną. Dowód z samej drogi w drzewie i podpisu tygodnia
    sprawdza się w całości bez sieci.
    """
    raw = stamp.raw
    level = raw.get("level", "")
    return {
        "format": BEATPROOF_FORMAT,
        "generator": f"{__app_name__} {__version__}",
        "authority": AUTHORITY,
        "digest": stamp.digest,
        "beat": str(raw.get("beat") or ""),
        "utc": stamp.utc,
        "seq": raw.get("seq"),
        "week": stamp.week,
        "week_closed": bool(raw.get("week_closed", False)),
        "week_root": str(raw.get("week_root") or ""),
        "inclusion_proof": list(raw.get("inclusion_proof") or []),
        "root_signature": str(raw.get("root_signature") or ""),
        "public_key": str(raw.get("public_key") or ""),
        "chain_hash": str(raw.get("chain_hash") or ""),
        "ots_status": str(raw.get("ots_status") or "none"),
        "ots_bitcoin_height": raw.get("ots_height"),
        "anchors": list(raw.get("anchors") or []),
        "level": level if isinstance(level, str) else str(level),
        "file_name": stamp.file_name,
        "note": str(raw.get("note") or ""),
        "time": dict(raw.get("time_bounds") or {}),
        "how_to_verify": (
            '1) Compute the SHA-256 of the document and compare it with "digest". 2) Fold '
            '"inclusion_proof" from the leaf SHA-256(0x00||digest), computing '
            'SHA-256(0x01||left||right) at every step — the result must equal "week_root". '
            '3) Check the Ed25519 signature "root_signature" over the text '
            '"beattime-proof-v1|<week>|<week_root>" with the key "public_key". 4) Compare '
            '"public_key" with the Sigelith key history: https://sigelith.org/spec/#keys. '
            '5) The signature covers the week: "utc" must lie within the ISO week "week"; '
            "what is confirmed is that the document existed no later than the end of that week."
        ),
    }


def proof_problems(data: Mapping[str, object]) -> list[str]:
    """Sprawdza dowód ``.beatproof`` bez sieci; pusta lista = dowód poprawny.

    Nie sprawdza samego dokumentu — to robi wywołujący, porównując sumę.
    """
    from .i18n import tr

    if data.get("format") != BEATPROOF_FORMAT:
        return [tr("To nie jest plik dowodu Sigelith (beatproof-v1).")]
    digest = str(data.get("digest") or "")
    week, root = str(data.get("week") or ""), str(data.get("week_root") or "")
    signature = str(data.get("root_signature") or "")
    if not (data.get("week_closed") and root and signature):
        return [tr("Tydzień stempla jeszcze się nie zamknął — podpis dojdzie przy kolejnej kopii.")]
    problems = []
    if not proof.verify_inclusion(digest, list(data.get("inclusion_proof") or []), root):
        problems.append(tr("Droga w drzewie Merkle'a nie prowadzi do podpisanego korzenia tygodnia."))
    if not proof.verify_signature(week, root, signature):
        problems.append(tr("Podpis tygodnia nie zgadza się z kluczem Sigelith zapisanym w programie."))
    return problems
