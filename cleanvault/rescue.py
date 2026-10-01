"""Notatka ratunkowa w katalogu kopii — nośnik opisuje się sam.

Kopia ma dać się odczytać **bez tego programu**: na innym komputerze, za wiele
lat, w innym systemie, przez kogoś, kto programu nigdy nie widział. Dlatego po
każdym przebiegu w katalogu kopii leżą dwa pliki:

* notatka tekstowa — co jest w katalogu, która wersja jest kompletna i jak
  odzyskać pliki ręcznie;
* ``odzyskaj.py`` — samodzielny skrypt (Python + dwie biblioteki), który
  odszyfrowuje kopię zaszyfrowaną. Opis formatu jest w samym skrypcie.

Notatka jest z założenia **dwujęzyczna** (polski i angielski) niezależnie od
języka interfejsu: czyta ją ktoś, kogo języka program nie zna.
"""

from __future__ import annotations

import os
import time
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path

from . import beat
from .evidence import EVIDENCE_DIR
from .log import get_logger
from .paths import CAPSULES_DIR, long_path, resource_path
from .snapshot import VersionState

log = get_logger("rescue")

NOTE_NAME = "JAK ODZYSKAC DANE - HOW TO RECOVER.txt"
SCRIPT_NAME = "odzyskaj.py"
#: Pliki programu w katalogu kopii, które nie są danymi użytkownika — przywracanie
#: bez spisu treści i przeglądanie kopii muszą je pomijać.
RESCUE_FILES = frozenset({NOTE_NAME, SCRIPT_NAME})
#: Notatka z kodem odzyskiwania, zapisywana obok każdej kapsuły czasu.
CAPSULE_NOTE_NAME = "KOD ODZYSKIWANIA - RECOVERY CODE.txt"

_RULE = "=" * 72


def write_rescue_files(
    destination: str | os.PathLike[str],
    versions: Mapping[str, VersionState],
    encrypted: bool,
    now: float | None = None,
) -> None:
    """Zapisuje notatkę i skrypt ratunkowy. Nigdy nie przerywa kopii błędem."""
    root = Path(destination)
    chunked = Path(long_path(root / ".cleanvault-chunks")).is_dir()
    evidence = Path(long_path(root / EVIDENCE_DIR)).is_dir()
    capsules = Path(long_path(root / CAPSULES_DIR)).is_dir()
    try:
        text = note_text(versions, encrypted, now, chunked=chunked, evidence=evidence, capsules=capsules)
        _write_atomic(root / NOTE_NAME, text.encode("utf-8-sig"))
        script = resource_path("assets", "recovery", SCRIPT_NAME).read_bytes()
        target = root / SCRIPT_NAME
        current = Path(long_path(target)).read_bytes() if Path(long_path(target)).exists() else b""
        if current != script:
            _write_atomic(target, script)
    except OSError as exc:
        # Notatka pomaga, ale jej brak nie unieważnia kopii — dziennik wystarczy.
        log.warning("Nie udało się zapisać notatki ratunkowej w %s: %s", root, exc)


def _write_atomic(path: Path, data: bytes) -> None:
    tmp = path.with_name(path.name + ".tmp")
    with open(long_path(tmp), "wb") as handle:
        handle.write(data)
    os.replace(long_path(tmp), long_path(path))


def note_text(
    versions: Mapping[str, VersionState],
    encrypted: bool,
    now: float | None = None,
    chunked: bool = False,
    evidence: bool = False,
    capsules: bool = False,
) -> str:
    """Treść notatki: układ katalogu, sposób odzyskania i stan każdej wersji."""
    moment = time.time() if now is None else now
    updated = time.strftime("%Y-%m-%d %H:%M", time.localtime(moment))
    dated = sorted((name for name in versions if name), reverse=True)
    mirror = "" in versions
    table = _version_table(versions, dated)

    polish = [
        "SIGELITH BACKUP — JAK ODZYSKAĆ DANE",
        _RULE,
        "",
        "Ten katalog zawiera kopię zapasową wykonaną programem Sigelith Backup.",
        "Notatka jest po to, by dane dało się odzyskać także BEZ tego programu —",
        "na innym komputerze, za wiele lat, w innym systemie operacyjnym.",
        "",
        f"Stan na: {updated} (czas lokalny komputera, który robił kopię)",
        "",
        "1. CO TU JEST",
        "",
    ]
    if dated:
        polish += [
            "   • Każdy przebieg kopii ma własny folder z datą, np. 2026-09-27_@512.",
            "     Data to data UTC, a „@512” to godzina w BeatTime: doba dzieli się na",
            "     1000 beatów po 86,4 sekundy, liczonych od północy UTC",
            "     (@512 = 512 × 86,4 s ≈ 12:17 UTC). Folder uzupełniony później ma",
            "     w nazwie drugą datę po znakach „--”.",
            "   • Każdy folder z datą jest KOMPLETNY: zawiera wszystkie pliki z chwili",
            "     kopii, a nie tylko zmiany. Pliki, które się nie zmieniły, są twardymi",
            "     dowiązaniami — widać je w wielu folderach, a miejsce zajmują raz.",
            "   • W każdym folderze z datą jest podfolder dla każdego źródła kopii",
            "     (np. „Dokumenty”), a w nim pliki w tym samym układzie co na dysku.",
        ]
    if mirror:
        polish += [
            "   • Kopia lustrzana: podfoldery źródeł leżą wprost w tym katalogu i zawsze",
            "     odpowiadają stanowi z ostatniego przebiegu — bez historii wersji.",
        ]
    if chunked:
        polish += [
            "   • Duże pliki (od 256 MB) są zapisane FRAGMENTAMI: w folderze wersji leży",
            "     mały „przepis” (nazwa.cvrecipe), a treść — w katalogu .cleanvault-chunks.",
            f"     Takiego pliku nie skopiujesz Eksploratorem; złoży go skrypt „{SCRIPT_NAME}”",
            "     (poniżej) albo program. Dzięki temu kolejne wersje dużego pliku",
            "     zajmują tylko tyle miejsca, ile realnie się w nim zmieniło.",
        ]
    if evidence:
        polish += [
            f"   • Folder „{EVIDENCE_DIR}” to dowody Sigelith: po jednym folderze na stempel,",
            "     z DOKŁADNIE tym dokumentem, który oznakowano, i jego plikiem .beatproof.",
            "     Plik .beatproof sprawdza się bez żadnego programu — przepis jest w nim.",
            "     Tego folderu program nigdy nie sprząta razem ze starymi wersjami.",
        ]
    if capsules:
        polish += [
            f"   • Folder „{CAPSULES_DIR}” to kapsuły czasu: pliki zapieczętowane do daty",
            "     z nazwy folderu. Otwiera je strona https://sigelith.org/capsule/ — po tej",
            "     dacie; kod odzyskiwania leży w pliku obok kapsuły.",
        ]
    polish += [
        "   • Pliki zaczynające się od „.cleanvault-” to spis treści kopii (sumy",
        "     kontrolne, stan wersji). Do ręcznego odzyskiwania nie są potrzebne.",
        "",
        "2. JAK ODZYSKAĆ",
        "",
        *_how_to_polish(encrypted, chunked),
        "",
        "3. WERSJE W TYM KATALOGU",
        "",
        *table,
        "",
        "   Wersję NIEDOKOŃCZONĄ przerwano przed końcem — ma tylko część plików.",
        "   Do odzyskiwania wybieraj najnowszą wersję kompletną.",
    ]

    english = [
        "SIGELITH BACKUP — HOW TO RECOVER YOUR FILES",
        _RULE,
        "",
        "This folder holds a backup made with Sigelith Backup. This note is here",
        "so that the files can be recovered WITHOUT the program — on another",
        "computer, many years from now, on another operating system.",
        "",
        f"As of: {updated} (local time of the computer that made the backup)",
        "",
        "1. WHAT IS HERE",
        "",
    ]
    if dated:
        english += [
            "   • Every backup run has its own dated folder, e.g. 2026-09-27_@512.",
            "     The date is the UTC date, and “@512” is the time in BeatTime: a day",
            "     is split into 1000 beats of 86.4 seconds counted from UTC midnight",
            "     (@512 = 512 × 86.4 s ≈ 12:17 UTC). A folder topped up later carries",
            "     a second date after “--”.",
            "   • Every dated folder is COMPLETE: it holds every file as of that run,",
            "     not just the changes. Unchanged files are hard links — they appear",
            "     in many folders but take up space once.",
            "   • Inside every dated folder there is a subfolder for each backed-up",
            "     source (e.g. “Documents”), laid out just as on the original disk.",
        ]
    if mirror:
        english += [
            "   • Mirror copy: the source subfolders sit directly in this folder and",
            "     always match the last run — there is no version history.",
        ]
    if chunked:
        english += [
            "   • Large files (256 MB and more) are stored IN CHUNKS: the version folder",
            "     holds a small “recipe” (name.cvrecipe) and the content lives in the",
            "     .cleanvault-chunks folder. Such a file cannot be copied with Explorer;",
            f"     the “{SCRIPT_NAME}” script (below) or the program rebuilds it. This way",
            "     later versions of a large file take only as much space as changed.",
        ]
    if evidence:
        english += [
            f"   • The “{EVIDENCE_DIR}” folder holds Sigelith evidence: one folder per stamp,",
            "     with EXACTLY the document that was stamped and its .beatproof file.",
            "     A .beatproof file can be checked without any program — it explains how.",
            "     The program never removes this folder when it prunes old versions.",
        ]
    if capsules:
        english += [
            f"   • The “{CAPSULES_DIR}” folder holds time capsules: files sealed until the date",
            "     in the folder name. Open them at https://sigelith.org/capsule/ after that",
            "     date; the recovery code is in a file next to the capsule.",
        ]
    english += [
        "   • Files whose names start with “.cleanvault-” are the backup's table",
        "     of contents (checksums, version state). Manual recovery does not",
        "     need them.",
        "",
        "2. HOW TO RECOVER",
        "",
        *_how_to_english(encrypted, chunked),
        "",
        "3. VERSIONS IN THIS FOLDER",
        "",
        *table,
        "",
        "   An INCOMPLETE version was stopped before the end and holds only some",
        "   of the files. Recover from the newest complete version.",
    ]
    return "\n".join([*polish, "", "", *english, ""])


def _how_to_polish(encrypted: bool, chunked: bool = False) -> list[str]:
    if not encrypted and chunked:
        return [
            "   Kopia NIE jest zaszyfrowana. Zwykłe pliki skopiujesz z najnowszego",
            "   kompletnego folderu z datą Eksploratorem albo menedżerem plików.",
            f"   Duże pliki zapisane fragmentami złoży skrypt „{SCRIPT_NAME}” (Python 3.8+,",
            "   bez dodatkowych bibliotek):",
            f"     python {SCRIPT_NAME} FOLDER_WERSJI KATALOG_DOCELOWY",
            "   Skrypt odtworzy cały folder — także zwykłe pliki — i sprawdzi sumy kontrolne.",
        ]
    if not encrypted:
        return [
            "   Kopia NIE jest zaszyfrowana — pliki to zwykłe kopie. Otwórz najnowszy",
            "   kompletny folder z datą i skopiuj potrzebne pliki z powrotem:",
            "   Eksploratorem Windows, Finderem albo menedżerem plików w Linuksie.",
        ]
    return [
        "   Kopia JEST zaszyfrowana (AES-256-GCM): pliki mają końcówkę „.cvlt”.",
        "   Bez hasła nie da się ich odczytać — nikt, także autor programu, nie ma",
        "   do nich innego klucza.",
        "",
        "   Najprościej: zainstaluj Sigelith Backup i użyj ekranu „Przywracanie”.",
        "",
        f"   Bez programu — skrypt „{SCRIPT_NAME}” leżący w tym katalogu:",
        "     1. Zainstaluj Pythona 3.8 lub nowszego (python.org).",
        "     2. W wierszu poleceń:  pip install pycryptodomex argon2-cffi",
        f"     3. Uruchom:            python {SCRIPT_NAME} FOLDER_WERSJI KATALOG_DOCELOWY",
        f"        na przykład:        python {SCRIPT_NAME} 2026-09-27_@512 C:\\Odzyskane",
        "   Skrypt zapyta o hasło, odszyfruje pliki i zapisze je w katalogu",
        "   docelowym. Pliki w kopii zostają nietknięte. Dokładny opis formatu",
        "   jest na początku skryptu.",
    ]


def _how_to_english(encrypted: bool, chunked: bool = False) -> list[str]:
    if not encrypted and chunked:
        return [
            "   The backup is NOT encrypted. Ordinary files can be copied from the newest",
            "   complete dated folder with Explorer or any file manager. Large files",
            f"   stored in chunks are rebuilt by the “{SCRIPT_NAME}” script (Python 3.8+,",
            "   no extra libraries):",
            f"     python {SCRIPT_NAME} VERSION_FOLDER TARGET_FOLDER",
            "   The script restores the whole folder — ordinary files too — and checks checksums.",
        ]
    if not encrypted:
        return [
            "   The backup is NOT encrypted — the files are ordinary copies. Open the",
            "   newest complete dated folder and copy the files you need back with",
            "   Windows Explorer, Finder or a Linux file manager.",
        ]
    return [
        "   The backup IS encrypted (AES-256-GCM): files end in “.cvlt”. They cannot",
        "   be read without the password — nobody, including the program's author,",
        "   has any other key.",
        "",
        "   Easiest: install Sigelith Backup and use the “Restore” screen.",
        "",
        f"   Without the program — the “{SCRIPT_NAME}” script in this folder:",
        "     1. Install Python 3.8 or newer (python.org).",
        "     2. In a terminal:       pip install pycryptodomex argon2-cffi",
        f"     3. Run:                 python {SCRIPT_NAME} VERSION_FOLDER TARGET_FOLDER",
        f"        for example:         python {SCRIPT_NAME} 2026-09-27_@512 C:\\Recovered",
        "   The script asks for the password, decrypts the files and writes them",
        "   to the target folder. The backup itself is never modified. The exact",
        "   file format is described at the top of the script.",
    ]


def _version_table(versions: Mapping[str, VersionState], dated: list[str]) -> list[str]:
    rows: list[str] = []
    for name in dated:
        run = versions[name]
        created = beat.describe(name.partition("--")[0])
        rows.append(f"   {name:<36} {created:<18} {_state(run)}")
    if "" in versions:
        rows.append(f"   {'(kopia lustrzana / mirror copy)':<55} {_state(versions[''])}")
    return rows or ["   (brak wersji / no versions yet)"]


def _state(run: VersionState) -> str:
    if not run.known:
        return "stan nieznany / state unknown"
    if run.complete:
        text = f"kompletna / complete ({run.done_files} plików / files)"
        if run.locked_files:
            text += f", bez / without {run.locked_files} otwartych w innych programach / open in other programs"
        return text
    return f"NIEDOKOŃCZONA / INCOMPLETE (brak ok. / about {run.missing_files} missing)"


def offsite_note() -> str:
    """Notatka zostawiana w kubełku kopii poza domem — obok zaszyfrowanych migawek."""
    return "\n".join([
        "SIGELITH BACKUP — KOPIA POZA DOMEM / OFF-SITE BACKUP",
        "",
        "Pliki w folderach chunks/ i snapshots/ są zaszyfrowane hasłem kopii poza domem.",
        "Aby odzyskać dane bez programu: pobierz CAŁY ten folder (rclone, AWS CLI,",
        "strona usługi), zainstaluj Pythona 3.8+ oraz:  pip install pycryptodomex argon2-cffi",
        f"i uruchom:  python {SCRIPT_NAME} POBRANY_FOLDER KATALOG_DOCELOWY",
        "",
        "Files in chunks/ and snapshots/ are encrypted with the off-site backup password.",
        "To recover without the program: download this WHOLE folder (rclone, AWS CLI,",
        "the provider's website), install Python 3.8+ and:  pip install pycryptodomex argon2-cffi",
        f"then run:  python {SCRIPT_NAME} DOWNLOADED_FOLDER TARGET_FOLDER",
        "",
    ])


def capsule_note(name: str, recovery_code: str, opens_at: datetime, files: Sequence[str]) -> str:
    """Notatka obok kapsuły czasu — czyta ją ktoś bez programu, może za wiele lat."""
    when = opens_at.astimezone(UTC).strftime("%Y-%m-%d %H:%M UTC")
    return "\n".join([
        f"SIGELITH BACKUP — KAPSUŁA CZASU / TIME CAPSULE — {name}",
        "",
        f"Kod odzyskiwania / Recovery code:  {recovery_code}",
        f"Otwarcie najwcześniej / Opens no earlier than:  {when}",
        f"Pliki kapsuły / Capsule files:  {' + '.join(files)}",
        "",
        "PL: Po tej chwili otwórz kapsułę na https://sigelith.org/capsule/ — wskaż plik",
        "    .beatseal.json (i plik .bin obok niego). Po niej otworzy ją każdy, kto ma jej",
        "    pliki. Otwierają ją dowolne dwie z trzech części: runda sieci drand z tej chwili,",
        "    udział serwera kluczy Sigelith — wydawany dopiero po dacie, co jest zasadą",
        "    operatora, a nie wymogiem kryptografii — i kod odzyskiwania podany wyżej. Kod",
        "    zastępuje jeden z dwóch kluczy, gdyby po tej dacie któryś był niedostępny. SAM",
        "    niczego nie otwiera, ale kto ma tę notatkę, temu do otwarcia kapsuły przed datą",
        "    wystarczy, że operator złamie swoją zasadę.",
        "",
        "EN: After that moment open the capsule at https://sigelith.org/capsule/ — choose the",
        "    .beatseal.json file (and the .bin file next to it); from then on anyone who has",
        "    its files can open it. Any two of three parts open it: the drand network's round",
        "    for that moment, the Sigelith key server's share — released only after the date,",
        "    by the operator's policy rather than by cryptography — and the recovery code",
        "    above. The code replaces one of the two keys should one of them be unavailable",
        "    after that date. On its OWN it opens nothing, but whoever has this note needs only",
        "    the operator to break its policy to open the capsule before the date.",
        "",
    ])
