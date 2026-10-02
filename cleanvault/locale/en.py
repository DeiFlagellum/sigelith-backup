"""Katalog angielski: „polski tekst źródłowy” → „tekst angielski”.

Klucze muszą **dokładnie** odpowiadać napisom w kodzie — łącznie ze znakami
nowej linii, wielokropkami i polskimi cudzysłowami. Pilnuje tego test
``tests/test_i18n.py``: brak klucza albo klucz bez odpowiednika w kodzie
kończy się nieudanym testem, a nie polskim zdaniem w angielskim oknie.

Nazwy pól w nawiasach klamrowych (``{count}``) są częścią umowy z kodem —
tłumaczymy tekst wokół nich, nigdy ich same. Formaty dat celowo zmieniamy na
ISO (``%Y-%m-%d``): angielszczyzna dzieli się na zapis amerykański i brytyjski,
a zapis ISO czyta się jednoznacznie w obu.
"""

from __future__ import annotations

TEXTS: dict[str, str] = {
    # ------------------------------------------------------- fragmenty i daty
    "\n\nLokalizacja:\n{path}": "\n\nLocation:\n{path}",
    "\nDo uzupełnienia: niedokończone kopie: {count} — możesz je uzupełnić, "
    "wybierając wersję poniżej.":
        "\nTo finish: {count} unfinished backup(s) — you can complete them by "
        "choosing a version below.",
    "\nUwaga: duży klaster ({size}): każdy mały plik zajmuje co najmniej tyle miejsca. "
    "Przy wielu małych plikach kopia zajmie wielokrotnie więcej niż dane.":
        "\nNote: large cluster ({size}): every small file takes up at least that much space. "
        "With many small files the backup will take up several times more than the data itself.",
    "\nUwaga: niedokończone wersje (nie zawierają wszystkich plików): {names}":
        "\nNote: unfinished versions (they do not contain every file): {names}",
    "\nUwaga: {filesystem} nie obsługuje twardych dowiązań — każda wersja z datą "
    "zajmuje tyle miejsca co pełna kopia.":
        "\nNote: {filesystem} does not support hard links — every dated version takes up "
        "as much space as a full backup.",
    " wersji": " versions",
    " z szyfrowaniem AES-256-GCM…": " with AES-256-GCM encryption…",
    " ×": " ×",
    " — a ponieważ {filesystem} nie obsługuje twardych dowiązań, zapisze ponownie "
    "wszystkie pliki i zajmie tyle miejsca co cała kopia":
        " — and because {filesystem} does not support hard links, it will write every file "
        "again and take up as much space as the whole backup",
    " • pozostało {time}": " • {time} left",
    "%d.%m %H:%M": "%m-%d %H:%M",
    "%d.%m.%Y": "%Y-%m-%d",
    "%d.%m.%Y %H:%M": "%Y-%m-%d %H:%M",
    ", klaster {size}": ", cluster {size}",
    ", uzupełniona {when}": ", topped up {when}",

    # ------------------------------------------------------------------ ekrany
    "Analizuje pliki i pokazuje plan. Nic nie zapisuje.":
        "Analyses the files and shows the plan. Writes nothing.",
    "Anulowano przed rozpoczęciem kopii.": "Cancelled before the backup started.",
    "Anuluj": "Cancel",
    "Argon2id (t={passes}, {memory} MiB, p={threads})": "Argon2id (t={passes}, {memory} MiB, p={threads})",
    "Argon2id — {passes} przebiegi, {memory} MiB, {threads} wątki":
        "Argon2id — {passes} passes, {memory} MiB, {threads} threads",
    "Automatycznie (język systemu)": "Automatic (system language)",
    "Bardzo dobre": "Very strong",
    "Bardzo słabe": "Very weak",
    "Brak manifestu — skanuję katalog kopii.":
        "No manifest — scanning the backup folder.",
    "Brakuje tagu uwierzytelniającego — plik jest obcięty.":
        "The authentication tag is missing — the file is truncated.",
    "Błąd uruchamiania": "Start-up error",
    "Ciemny": "Dark",
    "Co dokładnie zostanie zapisane przy najbliższym przebiegu.":
        "Exactly what will be written on the next run.",
    "Co kopiujemy": "What we back up",
    "Co zrobić, gdy plik o tej nazwie już istnieje w katalogu docelowym.":
        "What to do when a file of that name already exists in the destination folder.",
    "Czas w nazwie to BeatTime — 1000 beatów na dobę, kotwica w UTC, ten sam moment "
    "na całym świecie. Data jest datą UTC, więc zgadza się z zegarem.":
        "The time in the name is BeatTime — 1000 beats per day, anchored to UTC, the same "
        "moment everywhere. The date is the UTC date, so it matches the clock.",
    "Czym jest {app}": "What {app} is",
    "Czyści tylko okno — plik dziennika pozostaje":
        "Clears the window only — the log file stays",
    "Dane aplikacji: {path}": "Application data: {path}",
    "Decyduje, czy zachowujemy historię wersji.":
        "Decides whether version history is kept.",
    "Dobre": "Strong",
    "Dodaj folder": "Add folder",
    "Dodaj przynajmniej jeden folder źródłowy.": "Add at least one source folder.",
    "Dogrywka zmian z czasu kopii:": "Top-up of changes made during the backup:",
    "Dokąd przywracamy": "Where we restore to",
    "Dokładnie to, co program realnie stosuje.": "Exactly what the program actually uses.",
    "Domyślne wykluczenia": "Default exclusions",
    "Domyślne wykluczenia zapisane.": "Default exclusions saved.",
    "Domyślnie wyłączone. Przy włączonej opcji skasowanie pliku w źródle\n"
    "usuwa też jego jedyną kopię zapasową — operacja nieodwracalna.":
        "Off by default. With this on, deleting a file at the source also removes\n"
        "its only backup copy — this cannot be undone.",
    "Dopisuj do nazwy katalogu datę ostatniego uzupełnienia":
        "Add the date of the last top-up to the folder name",
    "Dziennik": "Log",
    "Dziennik: {path}": "Log: {path}",
    "Ekran przywracania wypełniony danymi szablonu.":
        "The restore screen has been filled in from the template.",
    "Folder docelowy kopii — najlepiej na innym dysku fizycznym.":
        "Destination folder for the backup — ideally on a different physical drive.",
    "Folder zawierający kopię utworzoną przez {app}.":
        "A folder holding a backup created by {app}.",
    "Gdy plik już istnieje:": "When the file already exists:",
    "Gdzie zapisujemy": "Where we write",
    "Gotowe do pracy.": "Ready.",
    "Gotowe. Wybierz foldery do kopii.": "Ready. Choose the folders to back up.",
    "Gotowe: {count} {files}, {size}, {seconds} s.": "Done: {count} {files}, {size}, {seconds} s.",
    "Główny folder kopii. Zawiera spis treści (.cleanvault-manifest).":
        "The main backup folder. It holds the table of contents (.cleanvault-manifest).",
    "Hasła nie da się odzyskać ani zresetować. Jeśli je zgubisz, dane z kopii "
    "zaszyfrowanej są bezpowrotnie stracone — tak działa poprawne szyfrowanie.":
        "The password cannot be recovered or reset. If you lose it, the data in an "
        "encrypted backup is gone for good — that is how correct encryption works.",
    "Hasła w obu polach różnią się.": "The two passwords do not match.",
    "Hasło": "Password",
    "Hasło do kopii": "Backup password",
    "Hasło nie jest nigdzie zapisywane w postaci jawnej.\n"
    "Bez niego nie da się odzyskać danych — nie istnieje żadna furtka serwisowa.":
        "The password is never stored in plain form.\n"
        "Without it the data cannot be recovered — there is no back door.",
    "Hasło nie może być puste.": "The password cannot be empty.",
    "Hasło niezapisane": "Password not saved",
    "Hasło powinno mieć co najmniej 8 znaków.":
        "The password should be at least 8 characters long.",
    "Hasło trafia do magazynu systemowego powiązanego z Twoim kontem.\n"
    "Nigdy nie jest zapisywane w plikach programu.":
        "The password goes into the system store tied to your account.\n"
        "It is never written into the program's own files.",
    "Hasło użyte przy tworzeniu kopii": "The password used when the backup was made",
    "Ile plików kopia przetwarza jednocześnie. Przy setkach tysięcy małych plików\n"
    "czas kopii to głównie opóźnienia na każdy plik (otwarcie, skanowanie\n"
    "antywirusowe, zapis na nośnik), a nie przesył danych — praca równoległa\n"
    "skraca go kilkukrotnie.\n\n"
    "„automatycznie” dobiera liczbę do procesora (do 32). Na wolnym dysku\n"
    "talerzowym mniejsza wartość (2–4) bywa szybsza.":
        "How many files the backup handles at once. With hundreds of thousands of small\n"
        "files the time is dominated by per-file latency (opening, antivirus scanning,\n"
        "writing to the medium) rather than by data transfer — working in parallel\n"
        "cuts it several times over.\n\n"
        "“automatic” picks a number to match the processor (up to 32). On a slow\n"
        "spinning disk a smaller value (2–4) is often faster.",
    "Informacje przydatne przy zgłaszaniu problemu.":
        "Details worth quoting when reporting a problem.",
    "Jak to działa": "How it works",
    "Jasny": "Light",
    "Jeden folder utrzymywany w zgodzie ze źródłem. Brak historii wersji,\n"
    "za to najprostsza struktura i najmniejsze zużycie miejsca.":
        "A single folder kept in step with the source. No version history,\n"
        "but the simplest structure and the smallest footprint.",
    "Jeśli operacja zakończy się błędem, skopiuj stąd ostatnie wiersze — "
    "zawierają dokładną przyczynę, a nie tylko komunikat ogólny.":
        "If an operation ends in an error, copy the last lines from here — they hold "
        "the exact cause, not just a general message.",
    "Język interfejsu zmieniony.": "Interface language changed.",
    "Język zmienisz po zakończeniu bieżącej operacji.":
        "You can change the language once the current operation has finished.",
    "Język:": "Language:",
    "Katalog docelowy leży wewnątrz źródła ({path}). "
    "Kopia kopiowałaby samą siebie w nieskończoność.":
        "The destination folder is inside the source ({path}). "
        "The backup would copy itself forever.",
    "Katalog docelowy nie może być tym samym katalogiem co źródłowy.":
        "The destination folder cannot be the same as the source folder.",
    "Katalog jeszcze nie istnieje — zostanie utworzony.":
        "The folder does not exist yet — it will be created.",
    "Katalog kopii nie istnieje: {path}": "The backup folder does not exist: {path}",
    "Katalog źródłowy nie istnieje: {path}": "The source folder does not exist: {path}",
    "Katalog, w którym pojawią się odtworzone pliki.":
        "The folder where the restored files will appear.",
    "Katalog, w którym powstanie kopia. Nie może leżeć wewnątrz folderu źródłowego.":
        "The folder where the backup will be created. It must not be inside the source folder.",
    "Katalogi objęte kopią.\nMożesz przeciągnąć foldery z Eksploratora Windows wprost na tę listę.":
        "Folders covered by the backup.\nYou can drag folders from Windows Explorer straight onto this list.",
    "Każdy folder z datą jest kompletny — przywracanie nie wymaga sklejania wersji.":
        "Every dated folder is complete — restoring never means stitching versions together.",
    "Każdy plik jest czytany ponownie zaraz po zapisaniu. Dane pochodzą wtedy\n"
    "zwykle z pamięci podręcznej systemu, więc niewiele mówi to o nośniku,\n"
    "a wydłuża kopię nawet dwukrotnie.\n\n"
    "Skuteczniejsza jest weryfikacja odroczona: ekran „Przywracanie” →\n"
    "„Sprawdź kopię”, najlepiej po ponownym podłączeniu dysku.":
        "Every file is read back the moment it is written. The data usually comes\n"
        "from the system cache, so it says little about the medium and can make\n"
        "the backup twice as long.\n\n"
        "Deferred checking works better: the “Restore” screen →\n"
        "“Check backup”, ideally after reconnecting the drive.",
    "Każdy plik trafia do kopii jako zaszyfrowany kontener .cvlt.\n"
    "Klucz powstaje z hasła przez Argon2id.":
        "Every file goes into the backup as an encrypted .cvlt container.\n"
        "The key is derived from the password with Argon2id.",
    "Każdy przebieg tworzy osobny folder z datą i godziną.\n"
    "Pliki niezmienione są podpinane twardym dowiązaniem, więc historia\n"
    "zajmuje tyle miejsca, ile realnie się zmieniło.":
        "Every run creates its own folder with a date and time.\n"
        "Unchanged files are attached with hard links, so the history\n"
        "takes up only as much space as actually changed.",
    "Klaster nośnika to {cluster} — pliki zajmą {actual} zamiast {logical} (narzut {overhead}).":
        "The medium's cluster is {cluster} — the files will take {actual} instead of {logical} "
        "(overhead {overhead}).",
    "Kliknij szablon, aby zobaczyć jego szczegóły.": "Click a template to see its details.",
    "Kliknij „Podgląd zmian”, aby sprawdzić plan bez zapisywania czegokolwiek.":
        "Click “Preview changes” to check the plan without writing anything.",
    "Kolor wyróżnienia": "Accent colour",
    "Kolor wyróżnienia…": "Accent colour…",
    "Kopia": "Backup",
    "Kopia do dokończenia": "A backup to finish",
    "Kopia jest aktualna — nie ma czego zapisywać.":
        "The backup is up to date — there is nothing to write.",
    "Kopia jest zaszyfrowana — podaj hasło użyte przy jej tworzeniu.":
        "The backup is encrypted — enter the password used when it was made.",
    "Kopia jest zaszyfrowana — podaj hasło, aby ją przywrócić.":
        "The backup is encrypted — enter the password to restore it.",
    "Kopia jest zaszyfrowana — podaj hasło, aby ją zweryfikować.":
        "The backup is encrypted — enter the password to check it.",
    "Kopia jest zaszyfrowana — podaj hasło.": "The backup is encrypted — enter the password.",
    "Kopia lustrzana": "Mirror copy",
    "Kopia nie została uruchomiona.": "The backup was not started.",
    "Kopia wykonana. Uruchom podgląd ponownie, aby sprawdzić stan.":
        "Backup finished. Run the preview again to check the state.",
    "Kopia zapasowa": "Backup",
    "Kopia {folder}": "Backup of {folder}",
    "Kopia {kind} • {count} {files} • {size} • ostatnia aktualizacja {when}\nŹródła: {roots}":
        "{kind} backup • {count} {files} • {size} • last updated {when}\nSources: {roots}",
    "Kopiowane są wyłącznie pliki nowe i zmienione od ostatniego przebiegu.":
        "Only files that are new or changed since the last run are copied.",
    "Kopiuje ustawienia szablonu na ekran „Kopia zapasowa”":
        "Copies the template settings onto the “Backup” screen",
    "Kopię możesz sprawdzić później: ekran „Przywracanie” → „Sprawdź kopię”. "
    "Najlepiej po ponownym podłączeniu dysku — wtedy dane są czytane z nośnika.":
        "You can check the backup later: the “Restore” screen → “Check backup”. "
        "Best after reconnecting the drive — then the data really is read from the medium.",
    "Kryptografia": "Cryptography",
    "Lista podpowiadana przy tworzeniu nowej kopii.":
        "The list suggested when a new backup is set up.",
    "Magazyn haseł: {backend}": "Password store: {backend}",
    "Magazyn systemowy: {backend}": "System store: {backend}",
    "Menedżer poświadczeń Windows (DPAPI, powiązany z kontem użytkownika).":
        "Windows Credential Manager (DPAPI, tied to your user account).",
    "Miejsce i układ odtwarzanych plików.": "Where the restored files go and how they are laid out.",
    "Motyw zmieniony na {theme}.": "Theme changed to {theme}.",
    "Motyw:": "Theme:",
    "Możesz też przeciągnąć foldery z Eksploratora Windows wprost na listę.":
        "You can also drag folders from Windows Explorer straight onto the list.",
    "Można ją dokończyć — zostaną dograne tylko brakujące i zmienione pliki.":
        "It can be finished — only the missing and changed files will be added.",
    "Na nośniku docelowym zajmie to ok. {size}.":
        "On the destination medium this will take about {size}.",
    "Nadpisywanie plików": "Overwriting files",
    "Nadpisz istniejące pliki": "Overwrite existing files",
    "Nazwa szablonu": "Template name",
    "Nazwa szablonu nie może być pusta.": "The template name cannot be empty.",
    "Nazwa szablonu zapisana.": "Template name saved.",
    "Nazwa szablonu:": "Template name:",
    "Nie ma wersji kopii o nazwie {name} w katalogu {path}.":
        "There is no backup version named {name} in the folder {path}.",
    "Nie można odczytać informacji o dysku: {error}":
        "The drive information could not be read: {error}",
    "Nie udało się uruchomić programu — brakuje biblioteki: {error}\n"
    "Zainstaluj zależności poleceniem:  pip install -r requirements.txt":
        "The program could not start — a library is missing: {error}\n"
        "Install the dependencies with:  pip install -r requirements.txt",
    "Nie udało się wykonać operacji": "The operation could not be completed",
    "Nie udało się zapisać hasła w magazynie systemowym.\n"
    "Szablon działa normalnie — program poprosi o hasło przy uruchomieniu.":
        "The password could not be saved in the system store.\n"
        "The template still works — the program will ask for the password when it runs.",
    "Nie udało się znaleźć wolnej nazwy dla {path}":
        "No free name could be found for {path}",
    "Nie wskazano katalogu docelowego.": "No destination folder was given.",
    "Nie wskazano żadnego katalogu źródłowego.": "No source folder was given.",
    "Nie wybrano katalogu": "No folder chosen",
    "Nie wybrano szablonu": "No template selected",
    "Nie znaleziono spisu treści kopii — program przeskanuje folder i rozpozna "
    "pliki po ich zawartości.":
        "No backup table of contents was found — the program will scan the folder and "
        "recognise the files by their contents.",
    "Nie znam oryginalnej lokalizacji dla {key} — wybierz inny układ przywracania.":
        "The original location of {key} is unknown — choose a different restore layout.",
    "Niedostępny — backend {backend} nie gwarantuje poufności.":
        "Unavailable — the {backend} back end does not guarantee confidentiality.",
    "Niedostępny — brak biblioteki keyring.": "Unavailable — the keyring library is missing.",
    "Nieznany algorytm wyprowadzania klucza: {name}":
        "Unknown key derivation algorithm: {name}",
    "Nowa wersja z datą": "New dated version",
    "Nowa wersja z datą to kopia od początku do osobnego folderu":
        "A new dated version means copying from scratch into a separate folder",
    "Nowa wersja z datą — kopia do nowego folderu.\n"
    "Wybrana istniejąca wersja — dogrywa do niej tylko brakujące i zmienione\n"
    "pliki, a pliki różniące się od źródła nadpisuje. Tak dokończysz przerwaną\n"
    "kopię albo uzupełnisz ją o dane, które powstały w trakcie jej wykonywania.":
        "New dated version — a backup into a new folder.\n"
        "An existing version — only the missing and changed files are added to it,\n"
        "and files that differ from the source are overwritten. This is how you finish\n"
        "an interrupted backup or top it up with data created while it was running.",
    "Nowy szablon": "New template",
    "Nośnik docelowy ({filesystem}) nie obsługuje twardych dowiązań, więc każda "
    "wersja z datą jest pełną kopią. Te {count} niezmienionych plików zostanie "
    "powielone ({size}). Rozważ układ „kopia lustrzana” albo nośnik NTFS.":
        "The destination medium ({filesystem}) does not support hard links, so every "
        "dated version is a full copy. Those {count} unchanged files will be duplicated "
        "({size}). Consider the “mirror copy” layout or an NTFS medium.",
    "O programie": "About",
    "Obsługiwane są wzorce w stylu Windows:\n"
    "  *.tmp          — wszystkie pliki tymczasowe\n"
    "  Thumbs.db      — konkretna nazwa\n"
    "  node_modules/* — cały folder wraz z zawartością":
        "Windows-style patterns are supported:\n"
        "  *.tmp          — every temporary file\n"
        "  Thumbs.db      — one specific name\n"
        "  node_modules/* — a whole folder with its contents",
    "Ochrona danych": "Data protection",
    "Odczytuje wszystkie pliki kopii i weryfikuje ich poprawność.\nNic nie zapisuje na dysku.":
        "Reads every file of the backup and checks that it is intact.\nNothing is written to disk.",
    "Odpowiednik synchronizacji folderu. Wcześniejsze wersje plików nie są zachowywane.":
        "The equivalent of syncing a folder. Earlier versions of files are not kept.",
    "Odtwarza pliki z kopii — również z kopii zaszyfrowanej.":
        "Restores files from a backup — including an encrypted one.",
    "Odtwarza pliki zgodnie z ustawieniami powyżej":
        "Restores files according to the settings above",
    "Odtwórz pełną strukturę folderów": "Recreate the full folder structure",
    "Odtwórz pliki z istniejącej kopii": "Restore files from an existing backup",
    "Operacja nie powiodła się.": "The operation failed.",
    "Operacja przerwana przez użytkownika.": "The operation was cancelled by the user.",
    "Operacja przerwana — utrwalam stan dotychczas zapisanych plików.":
        "Operation cancelled — saving the state of the files written so far.",
    "Operacja w toku": "Operation in progress",
    "Operacja zakończona błędem.": "The operation ended with an error.",
    "Ostatnie operacje": "Recent operations",
    "Otwiera ekran przywracania z wypełnionymi ścieżkami":
        "Opens the restore screen with the paths filled in",
    "Otwiera pełny dziennik w domyślnym edytorze":
        "Opens the full log in the default editor",
    "Otwórz katalog danych": "Open data folder",
    "Otwórz katalog dziennika": "Open log folder",
    "Otwórz okno wyboru katalogu": "Open the folder chooser",
    "Otwórz plik dziennika": "Open log file",
    "PBKDF2-HMAC-SHA256 ({count} iteracji)": "PBKDF2-HMAC-SHA256 ({count} iterations)",
    "PBKDF2-HMAC-SHA256 — {count} iteracji": "PBKDF2-HMAC-SHA256 — {count} iterations",
    "PBKDF2-HMAC-SHA256, {count} iteracji": "PBKDF2-HMAC-SHA256, {count} iterations",
    "Pełna struktura — układ jak w źródle, wewnątrz wskazanego katalogu.\n"
    "Jeden folder — wygodne, gdy szukasz kilku plików.\n"
    "Pierwotne lokalizacje — zapisuje pliki tam, skąd zostały pobrane.":
        "Full structure — laid out as at the source, inside the folder you choose.\n"
        "One folder — handy when you are after a few files.\n"
        "Original locations — writes the files back where they came from.",
    "Pierwszy przebieg kopiuje wszystko i trwa najdłużej. Kolejne porównują "
    "rozmiar i datę modyfikacji, więc zwykle kończą się w kilka sekund.":
        "The first run copies everything and takes the longest. Later ones compare "
        "size and modification date, so they usually finish in seconds.",
    "Plan gotowy: {count} {files} do zapisania.": "Plan ready: {count} {files} to write.",
    "Plik jest za krótki, by być kontenerem tego programu.":
        "The file is too short to be a container of this program.",
    "Plik skończył się wcześniej, niż deklaruje nagłówek.":
        "The file ended sooner than its header declares.",
    "Plik w formacie w wersji {found}; ta wersja programu obsługuje {supported}.":
        "The file uses format version {found}; this version of the program supports {supported}.",
    "Plik wymaga Argon2id, a biblioteka argon2-cffi jest niedostępna.":
        "The file requires Argon2id, but the argon2-cffi library is unavailable.",
    "Pliki pominięte — kopia jest aktualna": "Files skipped — the backup is up to date",
    "Pliki trafią do wskazanego katalogu z zachowaniem struktury folderów.":
        "The files go into the chosen folder, keeping their folder structure.",
    "Pliki wrócą dokładnie tam, skąd pochodzą. Katalog docelowy zostanie zignorowany.":
        "The files go back exactly where they came from. The destination folder is ignored.",
    "Pliki zmienione od ostatniego przebiegu": "Files changed since the last run",
    "Pliki zostaną zapisane dokładnie tam, skąd pochodzą.\n\n"
    "Konflikty nazw: {collision}.\n\n"
    "Czy kontynuować?":
        "The files will be written exactly where they came from.\n\n"
        "Name conflicts: {collision}.\n\n"
        "Continue?",
    "Pliki, których jeszcze nie ma w kopii": "Files not yet in the backup",
    "Po uzupełnieniu istniejącej wersji jej katalog nazywa się np.\n"
    "  2026-09-17_@687--2026-09-24_@921\n"
    "czyli: data utworzenia kopii i data ostatniego uzupełnienia.\n\n"
    "Data utworzenia zostaje z przodu, więc katalogi nadal układają się\n"
    "chronologicznie. Widać to w Eksploratorze bez uruchamiania programu.":
        "After an existing version is topped up, its folder is named e.g.\n"
        "  2026-09-17_@687--2026-09-24_@921\n"
        "that is: the date the backup was created and the date it was last topped up.\n\n"
        "The creation date stays in front, so the folders still sort\n"
        "chronologically. You can see it in Explorer without starting the program.",
    "Po wykonaniu kopii zostanie mało wolnego miejsca ({free}).":
        "Little free space will be left after the backup ({free}).",
    "Po zakończeniu kopii program ponownie skanuje źródło i dogrywa do tej samej\n"
    "wersji pliki, które w międzyczasie powstały lub się zmieniły.\n"
    "Przydatne, gdy pracujesz na danych w trakcie wielogodzinnej kopii.\n"
    "Plik zmieniony w trakcie własnego kopiowania nigdy nie jest uznawany za zapisany.":
        "When the backup finishes, the program scans the source again and adds to the same\n"
        "version any files that appeared or changed in the meantime.\n"
        "Useful when you keep working on the data during a backup that runs for hours.\n"
        "A file that changes while it is being copied is never counted as written.",
    "Poczekaj na zakończenie bieżącej operacji.":
        "Wait for the current operation to finish.",
    "Podaj hasło dla szablonu „{name}”:": "Enter the password for the template “{name}”:",
    "Podaj hasło — bez niego nie można zaszyfrować kopii.":
        "Enter a password — the backup cannot be encrypted without one.",
    "Podane hasło nie pasuje do plików zapisanych wcześniej w tej kopii. "
    "Wznowienie z innym hasłem zostawiłoby w jednej kopii pliki pod dwoma hasłami. "
    "Podaj hasło użyte przy poprzednim przebiegu albo utwórz kopię w nowym katalogu.":
        "The password given does not match the files already written in this backup. "
        "Resuming with a different password would leave one backup holding files under two "
        "passwords. Enter the password used for the previous run, or create the backup in a "
        "new folder.",
    "Podgląd zmian": "Preview changes",
    "Pokazuje folder z plikami dziennika": "Shows the folder with the log files",
    "Pokazuje folder z ustawieniami i szablonami": "Shows the folder with settings and templates",
    "Pokaż / ukryj wpisane hasło": "Show / hide the typed password",
    "Pomiń istniejące pliki": "Skip existing files",
    "Potwierdź usuwanie": "Confirm deletion",
    "Powtórz hasło": "Repeat the password",
    "Program nie mógł się uruchomić:\n\n{error}\n\nSzczegóły zapisano w dzienniku aplikacji.":
        "The program could not start:\n\n{error}\n\nThe details were written to the application log.",
    "Program nie wie, czy ta kopia została dokończona. Uzupełnienie jej dogra tylko "
    "brakujące i zmienione pliki, a tego, co już jest zapisane, nie kopiuje ponownie.":
        "The program does not know whether this backup was finished. Topping it up adds only "
        "the missing and changed files and does not copy again what is already written.",
    "Program sam wykryje, czy kopia jest zaszyfrowana.":
        "The program detects by itself whether the backup is encrypted.",
    "Przebieg operacji i diagnostyka": "Operation progress and diagnostics",
    "Przebieg operacji na żywo. Pełna historia trafia do pliku.":
        "Live progress of the operation. The full history goes into a file.",
    "Przebieg uzupełniający: {error}": "Top-up pass: {error}",
    "Przeciętne": "Fair",
    "Przerwano liczenie sumy kontrolnej.": "Checksum calculation was cancelled.",
    "Przerwano skanowanie.": "Scanning was cancelled.",
    "Przerwano. Zapisano {count} {files} ({size}).": "Cancelled. {count} {files} written ({size}).",
    "Przerwij": "Stop",
    "Przerywanie operacji…": "Stopping the operation…",
    "Przerywanie — zapisuję spis treści kopii, nie wyłączaj komputera…":
        "Stopping — writing the backup table of contents, please do not turn the computer off…",
    "Przeskanowano {count} {files}.": "{count} {files} scanned.",
    "Przygotowanie…": "Preparing…",
    "Przywracanie": "Restore",
    "Przywracanie do pierwotnych lokalizacji": "Restoring to the original locations",
    "Przywracanie przerwane.": "Restore cancelled.",
    "Przywracanie {count} {files} ({size})…": "Restoring {count} {files} ({size})…",
    "Przywróć do pierwotnych lokalizacji": "Restore to the original locations",
    "Przywróć domyślne": "Restore defaults",
    "Przywróć fabryczne": "Restore factory list",
    "Przywróć pliki": "Restore files",
    "Przywróć z tej kopii": "Restore from this backup",
    "Pusta nazwa": "Empty name",
    "Równoległe operacje:": "Parallel operations:",
    "Skanowanie plików źródłowych…": "Scanning the source files…",
    "Skrót z dziennika — pełny zapis znajdziesz w zakładce „Dziennik”.":
        "A digest of the log — the full record is on the “Log” screen.",
    "Skąd przywracamy": "Where we restore from",
    "Sprawdzam, co zmieniło się w źródle w trakcie kopii "
    "(przebieg uzupełniający {attempt} z {passes})…":
        "Checking what changed at the source during the backup "
        "(top-up pass {attempt} of {passes})…",
    "Sprawdzam, czy hasło zgadza się z hasłem wcześniej zapisanych plików…":
        "Checking that the password matches the files written earlier…",
    "Sprawdzam, czy w katalogu docelowym jest kopia do dokończenia…":
        "Checking whether the destination folder holds a backup to finish…",
    "Sprawdź hasło": "Check the password",
    "Sprawdź kopię": "Check backup",
    "Szablon przechowuje foldery, opcje i wykluczenia. Hasło nigdy nie trafia do "
    "szablonu — jest przechowywane w Menedżerze poświadczeń Windows albo wpisywane "
    "przy każdym uruchomieniu.":
        "A template holds folders, options and exclusions. The password never goes into "
        "the template — it lives in Windows Credential Manager or is typed in on every run.",
    "Szablon usunięty.": "Template deleted.",
    "Szablon „{name}”": "Template “{name}”",
    "Szablon „{name}” już istnieje.\n\nZastąpić go bieżącymi ustawieniami z formularza?":
        "A template named “{name}” already exists.\n\nReplace it with the current settings?",
    "Szablon „{name}” zostanie usunięty.\n\nPliki kopii zapasowej pozostaną nienaruszone.":
        "The template “{name}” will be deleted.\n\nThe backup files stay untouched.",
    "Szablony": "Templates",
    "Szablony: {count}\nSzyfrowanie: AES-256-GCM\nKlucz: {kdf}":
        "Templates: {count}\nEncryption: AES-256-GCM\nKey: {kdf}",
    "Szyfrowanie i kontrola poprawności zapisu.": "Encryption and write verification.",
    "Szyfrowanie: AES-256-GCM (uwierzytelnione)\nWyprowadzanie klucza: {kdf}":
        "Encryption: AES-256-GCM (authenticated)\nKey derivation: {kdf}",
    "Szyfruj kopię (AES-256-GCM)": "Encrypt the backup (AES-256-GCM)",
    "Słabe": "Weak",
    "Ta kopia nie jest zaszyfrowana — hasło nie jest potrzebne.":
        "This backup is not encrypted — no password is needed.",
    "Ten folder jest już na liście.": "That folder is already on the list.",
    "To nie jest plik zaszyfrowany przez ten program.":
        "This file was not encrypted by this program.",
    "Trwa inna operacja — poczekaj na jej zakończenie.":
        "Another operation is running — wait for it to finish.",
    "Trwa operacja": "Operation running",
    "Trwa operacja na plikach. Zamknięcie programu ją przerwie.\n\n"
    "Pliki zapisane do tej chwili zostaną zachowane, a kopię będzie można później dokończyć.\n\n"
    "Zamknąć mimo to?":
        "A file operation is running. Closing the program will stop it.\n\n"
        "The files written so far are kept, and the backup can be finished later.\n\n"
        "Close anyway?",
    "Trwa: {description}…": "In progress: {description}…",
    "Tryb dokładny — licz sumę kontrolną każdego pliku":
        "Thorough mode — compute a checksum for every file",
    "Układ kopii": "Backup layout",
    "Układ plików:": "File layout:",
    "Uruchom kopię": "Run backup",
    "Ustawienia": "Settings",
    "Usunąć szablon?": "Delete the template?",
    "Usuwa pozycję z listy. Nie kasuje żadnych plików.":
        "Removes the entry from the list. No files are deleted.",
    "Usuwa szablon. Nie kasuje żadnych plików kopii.":
        "Deletes the template. No backup files are deleted.",
    "Usuwaj z kopii pliki skasowane w źródle":
        "Remove from the backup files deleted at the source",
    "Usuń": "Delete",
    "Usuń zaznaczone": "Remove selected",
    "Uszkodzony nagłówek pliku.": "The file header is damaged.",
    "Utwórz lub zaktualizuj kopię wybranych folderów":
        "Create or update a backup of the chosen folders",
    "Utwórz nową wersję": "Create a new version",
    "Uzupełnienie istniejącej wersji nie kopiuje ponownie tego, co już w niej jest — "
    "dokończysz przerwaną kopię bez tworzenia kolejnej pełnej wersji.":
        "Topping up an existing version does not copy again what is already there — you finish "
        "an interrupted backup without creating another full version.",
    "Uzupełnij tę wersję": "Finish this version",
    "Uzupełnij: {version} • {labels}": "Finish: {version} • {labels}",
    "W katalogu docelowym jest kopia tych samych folderów zapisana starszą wersją programu:":
        "The destination folder holds a backup of the same folders written by an older version "
        "of the program:",
    "W katalogu docelowym jest niedokończona kopia tych samych folderów:":
        "The destination folder holds an unfinished backup of the same folders:",
    "W tym katalogu nie ma spisu treści kopii — nie ma z czym porównać plików.":
        "This folder has no backup table of contents — there is nothing to compare the files with.",
    "Wczytaj do formularza": "Load into the form",
    "Wczytano manifest kopii: {count} {files}.": "Backup manifest loaded: {count} {files}.",
    "Wczytano szablon „{name}” do formularza.": "Template “{name}” loaded into the form.",
    "Wersja kopii nosi teraz nazwę {name}.": "The backup version is now named {name}.",
    "Wersja, licencja i użyta kryptografia": "Version, licence and the cryptography used",
    "Wersje z datą (zalecane)": "Dated versions (recommended)",
    "Weryfikacja kopii": "Backup check",
    "Weryfikacja nie powiodła się: nieprawidłowe hasło lub uszkodzony plik.":
        "Verification failed: wrong password or a damaged file.",
    "Weryfikacja po zapisie nie powiodła się — zapisane dane różnią się od źródła.":
        "The check after writing failed — the written data differs from the source.",
    "Weryfikacja {count} {files} ({size}), {threads} równolegle…":
        "Checking {count} {files} ({size}), {threads} in parallel…",
    "Weryfikuj natychmiast po zapisie (spowalnia kopię)":
        "Verify immediately after writing (slows the backup down)",
    "Wolne miejsce: {free} z {total}": "Free space: {free} of {total}",
    "Wolniejszy, ale wykrywa zmiany, które nie zmieniły rozmiaru ani daty\n"
    "(np. po przywróceniu pliku z innego nośnika).":
        "Slower, but it spots changes that altered neither size nor date\n"
        "(for example after a file was restored from another medium).",
    "Wpis {key} w spisie treści kopii wskazuje poza katalog docelowy — pomijam go.":
        "Entry {key} in the backup table of contents points outside the destination folder — skipping it.",
    "Wraca do listy wbudowanej w program": "Goes back to the list built into the program",
    "Wskaż folder kopii, aby zobaczyć jej zawartość.":
        "Point to the backup folder to see what is in it.",
    "Wskaż folder kopii.": "Point to the backup folder.",
    "Wskaż foldery objęte kopią. Podfoldery są uwzględniane automatycznie.":
        "Choose the folders to back up. Subfolders are included automatically.",
    "Wskaż główny folder kopii (ten, który wybrałeś jako cel), a nie pojedynczy folder "
    "z datą. Program sam odczyta spis treści kopii.":
        "Point to the main backup folder (the one you chose as the destination), not a single "
        "dated folder. The program reads the table of contents by itself.",
    "Wskaż katalog docelowy kopii.": "Point to the destination folder for the backup.",
    "Wskaż katalog docelowy.": "Point to the destination folder.",
    "Wstawia zalecaną listę wykluczeń": "Inserts the recommended list of exclusions",
    "Wszystkie pliki wylądują bezpośrednio w katalogu docelowym, bez podfolderów.":
        "Every file lands directly in the destination folder, with no subfolders.",
    "Wszystko do jednego folderu": "Everything into one folder",
    "Wybierz folder do kopii": "Choose a folder to back up",
    "Wybierz folder kopii": "Choose the backup folder",
    "Wybierz katalog": "Choose a folder",
    "Wybierz katalog docelowy": "Choose the destination folder",
    "Wybierz katalog docelowy kopii": "Choose the destination folder for the backup",
    "Wybierz katalog, aby zobaczyć dostępne miejsce.":
        "Choose a folder to see the space available.",
    "Wybierz kolejny folder do kopii": "Choose another folder to back up",
    "Wybierz szablon z listy.": "Choose a template from the list.",
    "Wybierz…": "Choose…",
    "Wybrano nadpisywanie istniejących plików. Ich obecna zawartość zostanie "
    "bezpowrotnie zastąpiona.\n\nCzy kontynuować?":
        "You chose to overwrite existing files. Their current contents will be replaced "
        "for good.\n\nContinue?",
    "Wyczyść widok": "Clear the view",
    "Wygląd": "Appearance",
    "Wygląd, wykluczenia domyślne i informacje o środowisku.":
        "Appearance, default exclusions and environment details.",
    "Wygląd, wykluczenia i magazyn haseł": "Appearance, exclusions and the password store",
    "Wykluczenia": "Exclusions",
    "Wykonuje kopię według tego szablonu": "Runs the backup described by this template",
    "Wykonuje kopię zgodnie z powyższymi ustawieniami":
        "Runs the backup with the settings above",
    "Wymagane wyłącznie dla kopii zaszyfrowanych.": "Needed only for encrypted backups.",
    "Wzorce plików i folderów pomijanych w kopii — po jednym w wierszu.":
        "Patterns of files and folders left out of the backup — one per line.",
    "Włączono szyfrowanie, ale nie podano hasła.":
        "Encryption is on, but no password was given.",
    "Włączono usuwanie z kopii plików skasowanych w źródle.\n\n"
    "Pliki usunięte w źródle stracą swoją jedyną kopię zapasową. Czy na pewno kontynuować?":
        "Removing files deleted at the source is switched on.\n\n"
        "Files deleted at the source will lose their only backup copy. Are you sure?",
    "Za mało miejsca w katalogu docelowym. Potrzeba ok. {needed}, dostępne {free}.":
        "Not enough space in the destination folder. About {needed} is needed, {free} is available.",
    "Zabezpieczenie przed literówką — hasła nie da się odzyskać.":
        "A guard against a typo — the password cannot be recovered.",
    "Zachowaj oba — dopisz numer do nazwy": "Keep both — add a number to the name",
    "Zakończono z błędami ({errors}). Zapisano {count} {files}.":
        "Finished with errors ({errors}). {count} {files} written.",
    "Zakończono.": "Finished.",
    "Zapamiętaj hasło w Menedżerze poświadczeń Windows":
        "Remember the password in Windows Credential Manager",
    "Zapamiętuje te ustawienia do ponownego użycia": "Remembers these settings for next time",
    "Zapis bieżącej sesji": "Record of this session",
    "Zapisane konfiguracje do ponownego użycia": "Saved configurations, ready to reuse",
    "Zapisane konfiguracje — uruchamiasz je jednym kliknięciem.":
        "Saved configurations — you run them with one click.",
    "Zapisane szablony": "Saved templates",
    "Zapisano szablon „{name}”.": "Template “{name}” saved.",
    "Zapisuje listę jako domyślną": "Saves the list as the default",
    "Zapisuje nową nazwę szablonu": "Saves the new template name",
    "Zapisywanie {count} {files} ({size}), {workers} równolegle":
        "Writing {count} {files} ({size}), {workers} in parallel",
    "Zapisz": "Save",
    "Zapisz do:": "Write to:",
    "Zapisz jako szablon": "Save as template",
    "Zapisz nazwę": "Save the name",
    "Zapisz szablon": "Save template",
    "Zastąpić szablon?": "Replace the template?",
    "Zatrzymuje operację. Pliki już zapisane pozostają nienaruszone.":
        "Stops the operation. Files already written stay untouched.",
    "Zaznacz szablon na liście.": "Select a template in the list.",
    "Zmiana języka przebudowuje okno; wypełnione ścieżki zostają.":
        "Changing the language rebuilds the window; the paths you filled in stay.",
    "Zmiana motywu działa natychmiast.": "The theme changes immediately.",
    "Zmienia kolor przycisków i zaznaczeń": "Changes the colour of buttons and selections",
    "Zmień nazwę, aby łatwiej rozpoznawać szablon.":
        "Rename it to make the template easier to recognise.",
    "Znaleziono {count} {files}. Porównuję z poprzednią kopią…":
        "{count} {files} found. Comparing with the previous backup…",

    # ------------------------------------------------- drobne wyrazy i liczby
    "automatycznie": "automatic",
    "bez zmian": "unchanged",
    "brak (biblioteka keyring niezainstalowana)": "none (the keyring library is not installed)",
    "brak danych": "no data",
    "brak pliku w kopii": "the file is missing from the backup",
    "do zapisania": "to write",
    "istniejąca kopia: {count} {files}, ostatnio {when}":
        "existing backup: {count} {files}, last {when}",
    "jeszcze nie uruchamiany": "never run yet",
    "kompletna": "complete",
    "kopia lustrzana": "mirror copy",
    "kopia zapasowa": "backup",
    "nie": "no",
    "niedokończona": "unfinished",
    "niedokończona — brakuje ok. {count} {files} ({size})":
        "unfinished — about {count} {files} missing ({size})",
    "niezaszyfrowana": "unencrypted",
    "nieznany format manifestu": "unknown manifest format",
    "nowych plików": "new files",
    "np. C:\\Odzyskane": "e.g. C:\\Recovered",
    "np. E:\\Kopie zapasowe": "e.g. E:\\Backups",
    "plik": "file",
    "plik stanu jest za krótki": "the state file is too short",
    "plik stanu w wersji {found}, obsługiwana: {supported}":
        "state file version {found}, supported: {supported}",
    "pliki": "files",
    "plików": "files",
    "podgląd kopii": "backup preview",
    "pozostaną w kopii": "they stay in the backup",
    "rozmiar w kopii {actual} B zamiast {expected} B":
        "size in the backup is {actual} B instead of {expected} B",
    "sprawdzanie kopii": "checking the backup",
    "stan nieznany (zapisana starszą wersją programu)":
        "state unknown (written by an older version of the program)",
    "suma kontrolna manifestu się nie zgadza": "the manifest checksum does not match",
    "suma kontrolna się nie zgadza — plik uszkodzony":
        "the checksum does not match — the file is damaged",
    "szablon {name}": "template {name}",
    "tak": "yes",
    "ten system plików": "this file system",
    "wersja {version}": "version {version}",
    "wersje z datą": "dated versions",
    "weryfikacja": "verification",
    "wyłączona": "off",
    "zaszyfrowana (AES-256-GCM)": "encrypted (AES-256-GCM)",
    "zawartość różni się od pliku źródłowego": "the contents differ from the source file",
    "zawartość różni się od sumy kontrolnej zapisanej podczas kopii":
        "the contents differ from the checksum recorded during the backup",
    "zmienionych": "changed",
    "zostaną usunięte z kopii": "they will be removed from the backup",

    # ------------------------------------------------------ komunikaty wyniku
    "{done} z {total} • {speed}/s{eta}": "{done} of {total} • {speed}/s{eta}",
    "{done} • {speed}/s": "{done} • {speed}/s",
    "{hours} h {minutes} min": "{hours} h {minutes} min",
    "{label}: {count} {files}": "{label}: {count} {files}",
    "{message}\n\nSzczegóły techniczne znajdziesz w zakładce „Dziennik”.":
        "{message}\n\nThe technical details are on the “Log” screen.",
    "{minutes} min {seconds} s": "{minutes} min {seconds} s",
    "{name}: nie można odczytać ({error})": "{name}: cannot be read ({error})",
    "{seconds} s": "{seconds} s",
    "{summary}\n\nProblemy:\n{problems}\n\nPełna lista znajduje się w zakładce „Dziennik”.":
        "{summary}\n\nProblems:\n{problems}\n\nThe full list is on the “Log” screen.",
    "{summary}{notes}\n\nPliki zapisane przed przerwaniem są kompletne i zostały "
    "odnotowane w spisie treści kopii.\n\nAby dokończyć kopię, uruchom ją ponownie — "
    "program zaproponuje uzupełnienie tej wersji zamiast tworzenia nowej.":
        "{summary}{notes}\n\nThe files written before the stop are complete and were recorded "
        "in the backup table of contents.\n\nTo finish the backup, run it again — the program "
        "will offer to top this version up instead of creating a new one.",
    "{title} — gotowe": "{title} — done",
    "{title} — przerwano": "{title} — cancelled",
    "{title} — zakończono z błędami": "{title} — finished with errors",
    "{when}  •  {action}  •  {count} {files}": "{when}  •  {action}  •  {count} {files}",
    "Łączny rozmiar danych do przesłania": "Total size of the data to transfer",
    "Środowisko": "Environment",
    "Źródła: {sources}\nCel: {destination}\nUkład: {structure} • Szyfrowanie: {encrypt} • "
    "Weryfikacja: {verify} • Dogrywka: {catchup} • Równolegle: {workers} • "
    "Data uzupełnienia w nazwie: {stamp}\nUtworzony: {created} • Ostatni przebieg: {last}":
        "Sources: {sources}\nDestination: {destination}\nLayout: {structure} • Encryption: {encrypt} • "
        "Verification: {verify} • Top-up: {catchup} • Parallel: {workers} • "
        "Top-up date in the name: {stamp}\nCreated: {created} • Last run: {last}",
    "Źródło nie zmieniło się w trakcie kopii — nie ma czego uzupełniać.":
        "The source did not change during the backup — there is nothing to top up.",
    "—": "—",
    "• Kopia przyrostowa — zapisywane są wyłącznie pliki nowe i zmienione.\n"
    "  Porównanie opiera się na spisie treści kopii, rozmiarze i dacie modyfikacji;\n"
    "  przy różnicy liczona jest suma kontrolna SHA-256.\n\n"
    "• Wersje z datą — każdy przebieg tworzy kompletny folder z datą, a pliki\n"
    "  niezmienione są podpinane twardym dowiązaniem, więc nie zajmują miejsca dwa razy.\n\n"
    "• Weryfikacja po zapisie — zapisany plik jest odczytywany z powrotem\n"
    "  i porównywany ze źródłem.\n\n"
    "• Odporność na przerwania — pliki powstają pod nazwą tymczasową i są\n"
    "  podmieniane dopiero po pełnym zapisie.":
        "• Incremental backup — only new and changed files are written.\n"
        "  The comparison uses the backup table of contents, the size and the modification date;\n"
        "  where they differ, a SHA-256 checksum is computed.\n\n"
        "• Dated versions — every run creates a complete dated folder, and unchanged\n"
        "  files are attached with hard links, so they never take up space twice.\n\n"
        "• Verification after writing — the written file is read back\n"
        "  and compared with the source.\n\n"
        "• Resilience to interruptions — files are created under a temporary name and\n"
        "  swapped in only once they are fully written.",
    "• Szyfr: AES-256 w trybie GCM (szyfrowanie z uwierzytelnieniem).\n"
    "• Wyprowadzanie klucza z hasła: {kdf}.\n"
    "• Nagłówek każdego pliku jest uwierzytelniony jako AAD — podmiana parametrów\n"
    "  unieważnia tag.\n"
    "• Każdy plik dostaje losowy, niepowtarzalny nonce.\n"
    "• Odszyfrowany plik powstaje dopiero po pomyślnej weryfikacji tagu.\n"
    "• Hasła nie są zapisywane w plikach programu. Opcjonalnie trafiają do\n"
    "  Menedżera poświadczeń Windows.":
        "• Cipher: AES-256 in GCM mode (authenticated encryption).\n"
        "• Key derivation from the password: {kdf}.\n"
        "• Every file header is authenticated as AAD — changing the parameters\n"
        "  invalidates the tag.\n"
        "• Every file gets a random, unique nonce.\n"
        "• A decrypted file is produced only after the tag has been verified.\n"
        "• Passwords are never written into the program's files. Optionally they go into\n"
        "  Windows Credential Manager.",

    # --------------------------------------------- kreator i ekran powitalny
    "Bez hasła nie da się odczytać ani jednego pliku z kopii.":
        "Without the password not a single file in the backup can be read.",
    "Co chcesz chronić?": "What do you want to protect?",
    "Co chcesz teraz zrobić?": "What would you like to do?",
    "Czyta kopię z nośnika i porównuje ją z zapisanymi sumami kontrolnymi.":
        "Reads the backup from the medium and compares it with the recorded checksums.",
    "Dalej": "Next",
    "Dokumenty i zdjęcia": "Documents and photos",
    "Ekran powitalny wrócisz w ustawieniach, gdy zmienisz zdanie.":
        "You can bring the welcome screen back in Settings if you change your mind.",
    "Ekran z pytaniem, co chcesz teraz zrobić: kopia, przywracanie, sprawdzenie.":
        "A screen asking what you want to do now: back up, restore or check.",
    "Foldery objęte kopią": "Folders covered by the backup",
    "Foldery z pracą. Kreator pominie katalogi, które odtwarza się jednym poleceniem "
    "(node_modules, venv, build).":
        "Folders with your work. The wizard leaves out folders that one command can recreate "
        "(node_modules, venv, build).",
    "Gdzie zapisać kopię?": "Where should the backup go?",
    "Historia i szyfrowanie": "History and encryption",
    "Historia zmian (zalecane)": "History of changes (recommended)",
    "Jak bardzo chcesz się zabezpieczyć?": "How much protection do you want?",
    "Jak wyżej, a dodatkowo każdy plik trafia do kopii zaszyfrowany (AES-256-GCM). "
    "Potrzebne przy kopii wożonej poza dom.":
        "As above, and every file is also encrypted in the backup (AES-256-GCM). "
        "Worth it for a backup that leaves the house.",
    "Jedna aktualna kopia": "One up-to-date copy",
    "Język, motyw, domyślne wykluczenia i informacje o środowisku.":
        "Language, theme, default exclusions and environment details.",
    "Katalog docelowy leży wewnątrz źródła — wybierz inny.":
        "The destination folder is inside the source — choose another one.",
    "Każdy przebieg tworzy folder z datą. Pliki niezmienione są podpinane dowiązaniem, "
    "więc historia kosztuje tyle, ile realnie się zmieniło.":
        "Every run creates a dated folder. Unchanged files are attached with a link, "
        "so the history costs only as much as actually changed.",
    "Każdy przebieg utworzy folder z datą. Pierwszy zajmie tyle, ile dane; "
    "kolejne — tyle, ile realnie się zmieniło.":
        "Every run will create a dated folder. The first takes as much space as the data; "
        "later ones only as much as actually changed.",
    "Kopia powstanie w: {path}": "The backup will be created in: {path}",
    "Kopia trafi do: {path}": "The backup goes to: {path}",
    "Kopia: {what}": "Backup: {what}",
    "Krok {number} z {total}": "Step {number} of {total}",
    "Najlepiej na innym dysku fizycznym niż ten, który chronisz — kopia obok oryginału "
    "ginie razem z nim.":
        "Ideally on a different physical drive from the one you protect — a backup sitting "
        "next to the original is lost along with it.",
    "Najszybsza i najmniejsza. Kopia odpowiada temu, co masz teraz — bez historii "
    "wcześniejszych wersji.":
        "The fastest and smallest. The backup matches what you have right now — with no "
        "history of earlier versions.",
    "Nie było jeszcze żadnej kopii. Zacznij od „Zrób kopię”.":
        "There has been no backup yet. Start with “Back up now”.",
    "Nie lista ustawień, tylko ich skutki.": "Not a list of settings — what they will do.",
    "Nie pokazuj tego ekranu przy starcie": "Do not show this screen at start-up",
    "Nośnik docelowy": "Destination medium",
    "Odtwarza pliki z kopii — całość albo wybrany folder.":
        "Restores files from a backup — all of it or a chosen folder.",
    "Odśwież listę": "Refresh the list",
    "Ostatnia kopia: {when} • {count} {files}.": "Last backup: {when} • {count} {files}.",
    "Pierwszy przebieg jest najdłuższy — kolejne porównują rozmiar i datę modyfikacji, "
    "więc zwykle trwają sekundy.":
        "The first run is the longest — later ones compare size and modification date, "
        "so they usually take seconds.",
    "Pliki w kopii będą zaszyfrowane; bez hasła nie da się ich odczytać.":
        "The files in the backup will be encrypted; they cannot be read without the password.",
    "Podfoldery są uwzględniane automatycznie.": "Subfolders are included automatically.",
    "Pokazuj ekran powitalny przy starcie": "Show the welcome screen at start-up",
    "Ponownie sprawdza podłączone nośniki": "Checks the connected drives again",
    "Program będzie utrzymywał jeden folder zgodny ze źródłem. Każdy kolejny przebieg "
    "dopisze tylko to, co się zmieniło.":
        "The program will keep one folder in step with the source. Every later run adds "
        "only what has changed.",
    "Projekty i kod": "Projects and code",
    "Przechodzi do następnego kroku": "Goes on to the next step",
    "Przechodzi do pełnego okna programu": "Goes to the full program window",
    "Sam wskażesz, co ma trafić do kopii.": "You choose what goes into the backup.",
    "System plików: {filesystem}, klaster {cluster}": "File system: {filesystem}, cluster {cluster}",
    "Ten katalog leży wewnątrz folderu źródłowego — wybierz inny.":
        "This folder is inside a source folder — choose another one.",
    "Ten nośnik nie obsługuje twardych dowiązań, więc każda wersja z datą zajmie tyle "
    "miejsca co pełna kopia. Przy tym nośniku rozważ „jedną aktualną kopię”.":
        "This medium does not support hard links, so every dated version will take up as "
        "much space as a full backup. With this medium, consider “one up-to-date copy”.",
    "To dysk systemowy — kopia nie przetrwa jego awarii. Jeśli masz drugi dysk albo "
    "pendrive, wybierz jego.":
        "This is the system drive — the backup will not survive its failure. If you have "
        "a second drive or a USB stick, choose that instead.",
    "To się wydarzy": "What will happen",
    "Trzy gotowe zestawy zamiast kilkunastu przełączników.":
        "Three ready-made sets instead of a dozen switches.",
    "Twoje pliki osobiste z folderów użytkownika. Najczęstszy wybór.":
        "Your personal files from your user folders. The most common choice.",
    "Uruchamia kreator, który ustawi kopię krok po kroku":
        "Starts the wizard, which sets up the backup step by step",
    "Nowa kopia krok po kroku…": "New backup, step by step…",
    "Ustawia kopię krok po kroku i zapisuje ją jako szablon":
        "Sets up the backup step by step and saves it as a template",
    "Ustawienia pierwszej kopii": "Setting up your first backup",
    "Ustawienia pierwszej kopii…": "Set up your first backup…",
    "W tym katalogu jest już kopia ({count} {files}) — program ją uzupełni, a nie nadpisze.":
        "This folder already holds a backup ({count} {files}) — the program will top it up, "
        "not overwrite it.",
    "Wraca do poprzedniego kroku": "Goes back to the previous step",
    "Wskaż dowolny katalog docelowy": "Choose any destination folder",
    "Wskaż folder kopii i kliknij „Sprawdź kopię”.":
        "Point to the backup folder and click “Check backup”.",
    "Wstecz": "Back",
    "Wybierz": "Choose",
    "Wybierz inny folder…": "Choose another folder…",
    "Wybierz to, co najbliższe. Dokładną listę folderów poprawisz niżej.":
        "Pick the closest match. You can adjust the exact list of folders below.",
    "Wybrane foldery": "Selected folders",
    "Zamknij": "Close",
    "Zamyka kreator bez zapisywania": "Closes the wizard without saving",
    "Zapisuje nowe i zmienione pliki. Pierwszy raz trwa najdłużej.":
        "Writes new and changed files. The first time takes the longest.",
    "Zapisuje szablon bez uruchamiania kopii": "Saves the template without starting the backup",
    "Zapisuje szablon i od razu uruchamia kopię": "Saves the template and starts the backup at once",
    "Zapisz i zrób kopię": "Save and back up now",
    "Zapisz ustawienia": "Save settings",
    "Zrób kopię": "Back up now",
    "dysk systemowy": "system drive",
    "wolne {free} z {total}": "{free} free of {total}",

    # ----------------------------------------------- próbne przywrócenie
    "Porównano ze źródłem: {source}; tylko z sumą kontrolną (źródło zmieniło się albo jest niedostępne): {checksum}.":
        "Compared with the source: {source}; with the checksum only (the source has changed or is unavailable): {checksum}.",
    "Przywraca losową próbkę plików do katalogu tymczasowego i porównuje je ze źródłem.\nSprawdza całą drogę odzyskiwania, a trwa minuty. Nic nie zostaje na dysku.":
        "Restores a random sample of files to a temporary folder and compares them with the source.\nIt tests the whole recovery path and takes minutes. Nothing is left on disk.",
    "Próbne przywrócenie":
        "Trial restore",
    "W kopii nie ma plików, które dałoby się sprawdzić próbnie.":
        "The backup has no files that a trial restore could check.",
    "przywrócony plik różni się od pliku źródłowego":
        "the restored file differs from the source file",
    "przywrócony plik różni się od sumy kontrolnej zapisanej podczas kopii":
        "the restored file differs from the checksum recorded during the backup",
    "próbne przywrócenie":
        "trial restore",

    # ----------------------------------------- harmonogram i praca w tle
    "(brak zapisanych szablonów)":
        "(no saved templates)",
    "Bez tego kopia planowa ruszy dopiero wtedy, gdy sam otworzysz program.":
        "Without it, a scheduled backup only starts once you open the program yourself.",
    "Codziennie o godzinie":
        "Daily at a set time",
    "Codziennie o wybranej godzinie (zalecane)":
        "Daily at a set time (recommended)",
    "Dla dysku USB podłączanego od czasu do czasu. Najwyżej jedna kopia na 12 godzin.":
        "For a USB drive you plug in now and then. At most one backup every 12 hours.",
    "Dostępne w zainstalowanej wersji programu (plik EXE).":
        "Available in the installed version of the program (the EXE file).",
    "Godzina kopii codziennej (czas tego komputera).":
        "Time of the daily backup (this computer's clock).",
    "Harmonogram działa wtedy, gdy działa program — także ukryty przy zegarze.":
        "The schedule works while the program runs — including when it sits hidden by the clock.",
    "Harmonogram nie uruchamia kopii, dopóki tego nie odznaczysz. Ręczne kopie działają.":
        "The schedule starts no backups until you untick this. Manual backups still work.",
    "Harmonogram szablonu „{name}” zapisany.":
        "Schedule of the template “{name}” saved.",
    "Harmonogram:":
        "Schedule:",
    "Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.":
        "If the computer is off at that time, the backup starts once it is switched on.",
    "Kiedy kopia z tego szablonu ma ruszać sama.":
        "When the backup from this template should start by itself.",
    "Kiedy robić kopię?":
        "When should backups run?",
    "Kopia będzie robiona codziennie o {time}; termin przegapiony przy wyłączonym komputerze program nadrobi po jego włączeniu.":
        "The backup will run every day at {time}; a slot missed while the computer was off is made up once it is switched on.",
    "Kopia planowa nie powiodła się":
        "The scheduled backup failed",
    "Kopia rusza tylko wtedy, gdy ją uruchomisz.":
        "The backup starts only when you start it.",
    "Kopia ruszy po podłączeniu dysku docelowego (najwyżej raz na 12 godzin).":
        "The backup will start when the destination drive is connected (at most once every 12 hours).",
    "Kopia ruszy po podłączeniu dysku docelowego — najwyżej raz na 12 godzin.":
        "The backup starts when the destination drive is connected — at most once every 12 hours.",
    "Kopia sprzed miesiąca nie chroni tego, co zmieniło się od tamtej pory.":
        "A backup from a month ago does not protect what has changed since.",
    "Kopia „{name}” czeka":
        "Backup “{name}” is overdue",
    "Kopia „{name}” nie ruszyła":
        "Backup “{name}” did not start",
    "Kopie planowe działają, gdy działa program (także ukryty przy zegarze).":
        "Scheduled backups run while the program runs (including hidden by the clock).",
    "Kopie planowe działają, gdy działa program: po zamknięciu okna zostaje ikona przy zegarze, a przy logowaniu do Windows program uruchamia się w tle.":
        "Scheduled backups run while the program runs: closing the window leaves an icon by the clock, and the program starts in the background when you sign in to Windows.",
    "Kopie planowe i praca w tle":
        "Scheduled backups and running in the background",
    "Kopie planowe wykonają się o czasie. Program zamkniesz z menu ikony przy zegarze.":
        "Scheduled backups will run on time. You can quit the program from the menu of the icon by the clock.",
    "Kopię uruchamiasz przyciskiem. Najprostsze, ale łatwo o niej zapomnieć.":
        "You start the backup with a button. The simplest option, but easy to forget.",
    "Kopię uruchamiasz sam — przyciskiem w programie albo z menu ikony przy zegarze.":
        "You start the backup yourself — with the button in the program or from the menu of the icon by the clock.",
    "Następna kopia: {when}. Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.":
        "Next backup: {when}. If the computer is off at that time, the backup starts once it is switched on.",
    "Nie udało się zmienić startu przy logowaniu — szczegóły w dzienniku.":
        "Start at sign-in could not be changed — see the log for details.",
    "Od {days} dni nie było udanej kopii. Podłącz dysk docelowy albo otwórz program, żeby sprawdzić, co się dzieje.":
        "There has been no successful backup for {days} days. Connect the destination drive or open the program to see what is going on.",
    "Otwórz Sigelith Backup":
        "Open Sigelith Backup",
    "Po podłączeniu dysku docelowego":
        "When the destination drive is connected",
    "Po podłączeniu dysku z kopią":
        "When the backup drive is connected",
    "Po zamknięciu okna działaj dalej przy zegarze, gdy są kopie planowe":
        "Keep running by the clock after the window is closed, when backups are scheduled",
    "Potrzebne, żeby kopie planowe ruszały bez Twojego udziału. Hasło trafia do magazynu systemowego powiązanego z Twoim kontem, nie do plików programu.":
        "Needed for scheduled backups to start without you. The password goes into the system store tied to your account, not into the program's files.",
    "Program uruchamia się w tle przy logowaniu, więc terminy nie przepadną.":
        "The program starts in the background when you sign in, so no slot is missed.",
    "Ręcznie":
        "Manually",
    "Ręcznie — kiedy zechcę":
        "Manually — whenever I want",
    "Start przy logowaniu włączony":
        "Start at sign-in turned on",
    "Szablon jest zaszyfrowany, a hasło nie jest zapamiętane. Kopie planowe potrzebują hasła zapisanego w Menedżerze poświadczeń Windows.":
        "The template is encrypted and its password is not remembered. Scheduled backups need the password saved in Windows Credential Manager.",
    "Sigelith Backup będzie uruchamiał się w tle, żeby wykonywać kopie planowe. Wyłączysz to w ustawieniach programu.":
        "Sigelith Backup will start in the background to run scheduled backups. You can turn this off in the program's settings.",
    "Sigelith Backup działa w tle":
        "Sigelith Backup is running in the background",
    "Uruchamiaj program w tle przy logowaniu do Windows":
        "Start the program in the background when I sign in to Windows",
    "Wstrzymaj kopie planowe":
        "Pause scheduled backups",
    "Zakończ":
        "Quit",
    "Zamknięcie okna chowa je, a harmonogram pilnuje terminów. Program zamkniesz z menu ikony przy zegarze.":
        "Closing the window hides it while the schedule keeps watch. You quit the program from the menu of the icon by the clock.",
    "Zrób kopię teraz":
        "Back up now",
    "{summary} Szczegóły znajdziesz w programie, w zakładce „Dziennik”.":
        "{summary} The details are in the program, on the “Log” screen.",

    # ---------------------------------------------- baner administratora
    "Program działa z uprawnieniami administratora. Nie są mu potrzebne — kopia i przywracanie działają bez nich, a pliki zapisane przez administratora mogą później nie dać się zmienić ze zwykłego konta.":
        "The program is running with administrator rights. It does not need them — backing up and restoring work without them, and files written by an administrator may later be impossible to change from an ordinary account.",

    # --------------------------------- pliki zablokowane i masowe zmiany
    "Pliki otwarte w innych programach nie trafiły do kopii: {files}. Zamknij te programy i uruchom kopię ponownie — dograne zostaną tylko te pliki.":
        "Files open in other programs did not go into the backup: {files}. Close those programs and run the backup again — only those files will be added.",
    "Uwaga: w źródle zmieniło się podejrzanie dużo plików — {reasons}":
        "Warning: a suspiciously large number of files changed at the source — {reasons}",
    "Wstrzymano kopię: w źródle zmieniło się podejrzanie dużo plików. {reasons}":
        "Backup paused: a suspiciously large number of files changed at the source. {reasons}",
    "Zmieniło się albo zniknęło {count} z {previous} plików poprzedniej kopii.":
        "{count} of the {previous} files in the previous backup have changed or disappeared.",
    "{suspicious} z {evaluated} sprawdzonych zmienionych plików ma treść, która nie pasuje do ich typu (wygląda na zaszyfrowaną).":
        "{suspicious} of {evaluated} checked changed files have contents that do not match their type (they look encrypted).",

    # ---------------------------------------------- masowe zmiany — okno
    "Kontynuuj mimo to":
        "Continue anyway",
    "Kopia planowa wstrzymana":
        "Scheduled backup paused",
    "Kopia wstrzymana do decyzji.":
        "Backup paused until you decide.",
    "Kopia wstrzymana — w źródle zmieniło się podejrzanie dużo plików.":
        "Backup paused — a suspiciously large number of files changed at the source.",
    "Podejrzanie dużo zmian":
        "Suspiciously many changes",
    "Wstrzymaj kopię":
        "Pause the backup",
    "{reasons}\n\nJeśli to spodziewane — aktualizacja programu, przeniesienie albo przerobienie wielu plików — kontynuuj.\n\nJeśli nie, NIE kontynuuj: tak wygląda działanie oprogramowania szyfrującego pliki (ransomware). Sprawdź najpierw, czy Twoje pliki dają się otworzyć. Wcześniejsze wersje w kopii pozostają nietknięte.":
        "{reasons}\n\nIf this is expected — a software update, moving or reworking many files — continue.\n\nIf not, do NOT continue: this is what file-encrypting malware (ransomware) looks like. First check that your files still open. Earlier versions in the backup stay untouched.",
    "{reasons} To może być działanie złośliwego oprogramowania szyfrującego pliki. Otwórz program, sprawdź pliki i uruchom kopię ręcznie.":
        "{reasons} This may be the work of file-encrypting malware. Open the program, check your files and run the backup manually.",

    # ------------------------------- opis wersji z plikami zablokowanymi

    # ------------------------ odmiana: pliki otwarte w innych programach
    "Pominięto {count} {files}.":
        "Skipped {count} {files}.",
    "Ponawiam {count} {files}…":
        "Retrying {count} {files}…",
    " (bez {count} {files})":
        " (without {count} {files})",
    "plik otwarty w innym programie":
        "file open in another program",
    "pliki otwarte w innych programach":
        "files open in other programs",
    "plików otwartych w innych programach":
        "files open in other programs",
    "pliku otwartego w innym programie":
        "file open in another program",

    # ------------------------ komunikaty z liczbami (poprawiona odmiana)
    "\n\n…i kolejne: {count}.":
        "\n\n…and more: {count}.",
    "Foldery objęte kopią ({count}): {list}":
        "Folders covered by the backup ({count}): {list}",
    "Nośnik nie obsługuje twardych dowiązań — kopiuję do nowej wersji niezmienione pliki: {count} ({size})…":
        "The medium does not support hard links — copying unchanged files into the new version: {count} ({size})…",
    "Pliki bez sumy kontrolnej sprawdzone tylko co do rozmiaru, bo ich źródło zmieniło się albo jest niedostępne: {count}.":
        "Files without a checksum checked by size only, because their source has changed or is unavailable: {count}.",
    "Pliki bez zapisanej sumy kontrolnej, porównane ze źródłem i uzupełnione w spisie treści: {count}.":
        "Files without a recorded checksum, compared with the source and added to the table of contents: {count}.",
    "Pliki przeniesione w źródle: {count} — trafią do kopii bez przesyłania danych.":
        "Files moved at the source: {count} — they go into the backup without transferring data.",
    "Pliki skasowane w źródle: {count} — {action}.":
        "Files deleted at the source: {count} — {action}.",
    "Pliki z końcówką dopisaną do nazwy, których oryginały zniknęły: {count}.":
        "Files with an ending added to their names whose originals disappeared: {count}.",
    "Pliki zmienione w trakcie kopiowania: {count} — zostaną zapisane ponownie w przebiegu uzupełniającym.":
        "Files changed while being copied: {count} — they will be written again in the top-up pass.",
    "Pliki, których brakuje w kopii i które zostaną zapisane ponownie: {count}.":
        "Files missing from the backup that will be written again: {count}.",
    "Podpinanie niezmienionych plików do nowej wersji: {count}…":
        "Linking unchanged files into the new version: {count}…",
    "Pomijam pliki, które już są w tej wersji kopii: {count}.":
        "Skipping files already in this version of the backup: {count}.",
    "Porządkowanie historii — usunięte najstarsze wersje: {count}.":
        "Tidying up history — oldest versions removed: {count}.",
    "Przenoszenie plików, które zmieniły miejsce w źródle: {count}…":
        "Moving files that changed place at the source: {count}…",
    "Próbne przywrócenie losowo wybranych plików: {count}…":
        "Trial restore of randomly chosen files: {count}…",
    "Usuwanie z kopii plików skasowanych w źródle: {count}…":
        "Removing from the backup files deleted at the source: {count}…",
    "Uzupełniam kopię o pliki, które przybyły lub zmieniły się w trakcie: {count} ({size})…":
        "Topping up the backup with files that appeared or changed meanwhile: {count} ({size})…",
    "Uzupełnianie wersji {version} — pliki już zapisane, które zostaną pominięte: {count}.":
        "Topping up version {version} — files already written that will be skipped: {count}.",
    "Wznawiam wersję {version} — już zapisane: {done}, do dogrania: {todo}.":
        "Resuming version {version} — already written: {done}, still to go: {todo}.",
    "pliku":
        "file",

    # ------------------------------------- zapis różnicowy dużych plików
    "Brak fragmentu {cid} w magazynie kopii.":
        "Chunk {cid} is missing from the backup's chunk store.",
    "Brak opisu magazynu fragmentów w katalogu kopii.":
        "The backup folder has no description of its chunk store.",
    "Duże pliki zapisuj różnicowo (od 256 MB)":
        "Store large files incrementally (256 MB and more)",
    "Fragment {cid} jest uszkodzony.":
        "Chunk {cid} is damaged.",
    "Kolejna wersja dużego pliku — maszyny wirtualnej, skrzynki pocztowej, bazy —\nzapisuje tylko zmienione fragmenty zamiast całego pliku. W kopii taki plik\nleży jako przepis + fragmenty; złoży go program albo skrypt ratunkowy.":
        "The next version of a large file — a virtual machine, a mailbox, a database —\nstores only the changed chunks instead of the whole file. In the backup such a file\nis kept as a recipe plus chunks; the program or the rescue script rebuilds it.",
    "Opis magazynu fragmentów jest uszkodzony.":
        "The chunk store description is damaged.",
    "Plik złożony z fragmentów różni się od zapisanego w przepisie.":
        "The file rebuilt from chunks differs from the one recorded in its recipe.",
    "Podane hasło nie pasuje do fragmentów zapisanych wcześniej w tej kopii.":
        "The password given does not match the chunks written earlier in this backup.",
    "Przepis pliku jest uszkodzony.":
        "The file recipe is damaged.",
    "To nie jest przepis pliku zapisanego fragmentami.":
        "This is not a recipe of a file stored in chunks.",
    "Usunięto nieużywane fragmenty dużych plików: {count} ({size}).":
        "Removed unused chunks of large files: {count} ({size}).",

    # -------------------------------- kopia poza domem i znaczniki czasu
    ", zakotwiczona w Bitcoinie":
        ", anchored in Bitcoin",
    "Adres usługi:":
        "Service address:",
    "Brak fragmentu {cid} w kopii poza domem.":
        "Chunk {cid} is missing from the off-site backup.",
    "Brak klucza albo hasła w Menedżerze poświadczeń Windows — zapisz ustawienia kopii poza domem jeszcze raz.":
        "The key or password is missing from Windows Credential Manager — save the off-site backup settings again.",
    "Brak spisu wersji, którego dotyczy znacznik.":
        "The version list the timestamp refers to is missing.",
    "Certyfikat PDF":
        "PDF certificate",
    "Druga, zaszyfrowana kopia w usłudze zgodnej z S3 (np. Backblaze B2)":
        "A second, encrypted backup in an S3-compatible service (e.g. Backblaze B2)",
    "Folder w kubełku:":
        "Folder in the bucket:",
    "Hasło kopii poza domem":
        "Off-site backup password",
    "Hasło kopii poza domem nie pasuje do danych zapisanych w tym miejscu.":
        "The off-site backup password does not match the data stored there.",
    "Hasło kopii poza domem powinno mieć co najmniej 10 znaków.":
        "The off-site backup password should be at least 10 characters long.",
    "Hasło szyfrowania:":
        "Encryption password:",
    "Identyfikator klucza:":
        "Key ID:",
    "Katalog, do którego trafią pliki":
        "The folder the files will go to",
    "Klucz tajny":
        "Secret key",
    "Klucz tajny:":
        "Secret key:",
    "Kopia na dysku obok komputera nie przetrwa pożaru ani kradzieży. Tu ustawisz drugą kopię w usłudze zgodnej z S3 (np. Backblaze B2). Pliki są szyfrowane na tym komputerze osobnym hasłem — usługa widzi tylko nieczytelne fragmenty.":
        "A backup on a drive next to the computer will not survive a fire or a theft. Here you set up a second copy in an S3-compatible service (e.g. Backblaze B2). Files are encrypted on this computer with a separate password — the service only sees unreadable chunks.",
    "Kopia poza domem":
        "Off-site backup",
    "Kopia poza domem dla szablonu „{name}” zapisana.":
        "Off-site backup for the template “{name}” saved.",
    "Kopia poza domem nie ruszyła":
        "The off-site backup did not start",
    "Kopia poza domem potrzebuje Menedżera poświadczeń Windows, a jest on niedostępny.":
        "The off-site backup needs Windows Credential Manager, which is unavailable.",
    "Kopia poza domem „{name}”":
        "Off-site backup “{name}”",
    "Kopia poza domem…":
        "Off-site backup…",
    "Korzeń tygodnia zakotwiczony w łańcuchu Bitcoina.":
        "The week's root is anchored in the Bitcoin blockchain.",
    "Kubełek (bucket):":
        "Bucket:",
    "Migawek w usłudze: {count}.":
        "Snapshots in the service: {count}.",
    "Migawka i cel":
        "Snapshot and destination",
    "Migawka kopii poza domem jest uszkodzona.":
        "The off-site snapshot is damaged.",
    "Migawka {stamp}: plików bez zmian {reused}, wysłanych {files}, nowych fragmentów {chunks} ({size}).":
        "Snapshot {stamp}: unchanged files {reused}, uploaded {files}, new chunks {chunks} ({size}).",
    "MinIO / Wasabi / inna zgodna z S3":
        "MinIO / Wasabi / other S3-compatible",
    "NIEPOPRAWNY":
        "INVALID",
    "Nie ma migawki {stamp} w kopii poza domem.":
        "There is no snapshot {stamp} in the off-site backup.",
    "Nie udało się połączyć z usługą przechowywania: {error}":
        "Could not connect to the storage service: {error}",
    "Nie udało się wczytać migawek: {error}":
        "Could not load the snapshots: {error}",
    "Nie udało się zapisać klucza albo hasła w magazynie systemowym.":
        "The key or password could not be saved in the system store.",
    "Odśwież z sieci":
        "Refresh online",
    "Opis kopii poza domem jest uszkodzony.":
        "The off-site backup description is damaged.",
    "Oznakowana: {utc} (BeatTime {beat})":
        "Timestamped: {utc} (BeatTime {beat})",
    "Pliki wersji różnią się od spisu, który został oznakowany.":
        "The files of the version differ from the list that was timestamped.",
    "Pobiera i odszyfrowuje pliki wybranej migawki":
        "Downloads and decrypts the files of the chosen snapshot",
    "Pobiera listę migawek z usługi":
        "Downloads the list of snapshots from the service",
    "Pobiera podpis tygodnia i stan kotwicy w Bitcoinie":
        "Downloads the week's signature and the state of the Bitcoin anchor",
    "Pobieram potwierdzenia…":
        "Downloading receipts…",
    "Podaj hasło szyfrowania kopii poza domem.":
        "Enter the encryption password of the off-site backup.",
    "Podaj klucz tajny usługi.":
        "Enter the service's secret key.",
    "Podam dane ręcznie":
        "I will enter the details myself",
    "Pominięte (otwarte w innych programach albo zmienione w trakcie): {count}.":
        "Skipped (open in other programs or changed meanwhile): {count}.",
    "Porządkowanie kopii poza domem…":
        "Tidying up the off-site backup…",
    "Potwierdzenia odświeżone.":
        "Receipts refreshed.",
    "Poza dom":
        "Off-site",
    "Połączenie działa: zapis, odczyt i usuwanie się udały.":
        "The connection works: writing, reading and deleting succeeded.",
    "Połączenie nie działa: {error}":
        "The connection does not work: {error}",
    "Przywraca pliki z zaszyfrowanej kopii w usłudze S3 — także na nowym komputerze":
        "Restores files from the encrypted copy in the S3 service — on a new computer too",
    "Przywracanie z kopii poza domem":
        "Restore from the off-site backup",
    "Przywracanie {count} {files} z kopii poza domem…":
        "Restoring {count} {files} from the off-site backup…",
    "Przywróć":
        "Restore",
    "Region:":
        "Region:",
    "Skąd":
        "From",
    "Spis wersji zgodny ze znacznikiem: {answer}":
        "Version list matches the timestamp: {answer}",
    "Spis wersji został zmieniony po oznakowaniu.":
        "The version list was changed after it was timestamped.",
    "Sprawdza spis wersji, drogę w drzewie tygodnia i podpis — bez sieci":
        "Checks the version list, the path in the week's tree and the signature — offline",
    "Sprawdzam połączenie…":
        "Checking the connection…",
    "Sprawdź":
        "Check",
    "Sprawdź połączenie":
        "Check connection",
    "Starsze migawki są usuwane, gdy nadmiar sięgnie kilku — co kilka dni.":
        "Older snapshots are removed once a few extra have built up — every few days.",
    "Suma w drzewie tygodnia: {answer}":
        "Checksum in the week's tree: {answer}",
    "Suma wersji nie należy do drzewa tygodnia podanego w potwierdzeniu.":
        "The version checksum is not part of the week's tree given in the receipt.",
    "Ta wersja nie ma znacznika czasu.":
        "This version has no timestamp.",
    "Także po kopiach planowych. Wysyłane są tylko pliki nowe i zmienione.":
        "After scheduled backups too. Only new and changed files are uploaded.",
    "Tydzień jeszcze się nie zamknął — podpis pojawi się po poniedziałku 00:00 UTC.":
        "The week has not closed yet — the signature appears after Monday 00:00 UTC.",
    "Usunięto starsze migawki: {count}, nieużywane fragmenty: {chunks}.":
        "Removed older snapshots: {count}, unused chunks: {chunks}.",
    "Usługa chwilowo niedostępna ({status}).":
        "The service is temporarily unavailable ({status}).",
    "Usługa odrzuciła żądanie ({status} {code}): {message}":
        "The service rejected the request ({status} {code}): {message}",
    "Usługa przechowywania":
        "Storage service",
    "Usługa zwróciła inną treść niż zapisana.":
        "The service returned different content than was written.",
    "Usługa:":
        "Service:",
    "Uzupełnij adres usługi, nazwę kubełka i klucze dostępu.":
        "Fill in the service address, the bucket name and the access keys.",
    "Uzupełnij adres usługi, region, kubełek i identyfikator klucza.":
        "Fill in the service address, region, bucket and key ID.",
    "W tym katalogu kopii nie ma jeszcze znaczników czasu.":
        "There are no timestamps in this backup folder yet.",
    "W tym miejscu nie ma jeszcze kopii poza domem.":
        "There is no off-site backup at this location yet.",
    "Wczytaj migawki":
        "Load snapshots",
    "Wczytaj migawki i wybierz jedną z listy.":
        "Load the snapshots and choose one from the list.",
    "Wczytuję migawkę {stamp}…":
        "Loading snapshot {stamp}…",
    "Wczytuję poprzednią migawkę kopii poza domem…":
        "Loading the previous off-site snapshot…",
    "Wybierz migawkę i katalog, do którego trafią pliki.":
        "Choose a snapshot and the folder the files will go to.",
    "Wybierz wersję z listy.":
        "Choose a version from the list.",
    "Wysyłaj poza dom po każdej udanej kopii z tego szablonu":
        "Upload off-site after every successful backup from this template",
    "Wysyłam poza dom pliki nowe i zmienione: {count}…":
        "Uploading new and changed files off-site: {count}…",
    "Z kopii poza domem…":
        "From the off-site backup…",
    "Zachowuj migawek:":
        "Snapshots to keep:",
    "Zapisuje ustawienia; klucz i hasło trafiają do Menedżera poświadczeń Windows":
        "Saves the settings; the key and password go into Windows Credential Manager",
    "Zapisuje, odczytuje i usuwa mały plik próbny":
        "Writes, reads and deletes a small test file",
    "Zapisuję migawkę {stamp}…":
        "Saving snapshot {stamp}…",
    "Znacznik dowodzi, że wersja kopii w dokładnie tym kształcie istniała w podanej chwili. Podpis tygodnia pojawia się po jego zamknięciu (poniedziałek 00:00 UTC), a kotwica w Bitcoinie — zwykle kilka godzin później.":
        "A timestamp proves that the backup version existed in exactly this shape at the given moment. The week's signature appears once the week closes (Monday 00:00 UTC), and the Bitcoin anchor usually a few hours later.",
    "Znacznika czasu nie udało się zapisać: {error}":
        "The timestamp could not be saved: {error}",
    "Znaczniki czasu":
        "Timestamps",
    "Znaczniki czasu…":
        "Timestamps…",
    "kopia poza domem":
        "off-site backup",
    "np. komputer-domowy":
        "e.g. home-computer",
    "oznakowana {when} — podpis po zamknięciu tygodnia":
        "timestamped {when} — signature after the week closes",
    "podpisana (tydzień {week}){bitcoin}":
        "signed (week {week}){bitcoin}",
    "poprawny":
        "valid",
    "przywracanie z kopii poza domem":
        "restore from the off-site backup",
    "Łączę się z usługą…":
        "Connecting to the service…",

    # --------------------------------------------- retencja kalendarzowa
    " dni":
        " days",
    " mies.":
        " mo.",
    " tyg.":
        " wk.",
    "Ile ostatnich wersji zachować. Starsze są kasowane po udanym przebiegu.":
        "How many recent versions to keep. Older ones are deleted after a successful run.",
    "Kalendarz zostawia najnowszą wersję z każdego z ostatnich dni, tygodni\ni miesięcy — gęsto dla świeżych zmian, rzadko dla dawnych. Nadmiar jest\nkasowany po udanym przebiegu; wersje niedokończone nigdy.":
        "The calendar keeps the newest version from each of the recent days, weeks\nand months — dense for fresh changes, sparse for old ones. The excess is\ndeleted after a successful run; unfinished versions never are.",
    "Z ilu ostatnich dni zachować po jednej, najnowszej wersji.":
        "For how many recent days to keep one, newest version.",
    "Z ilu ostatnich miesięcy zachować po jednej, najnowszej wersji.":
        "For how many recent months to keep one, newest version.",
    "Z ilu ostatnich tygodni zachować po jednej, najnowszej wersji.":
        "For how many recent weeks to keep one, newest version.",
    "Zachowuj:":
        "Keep:",
    "kalendarz: dni, tygodnie, miesiące":
        "calendar: days, weeks, months",
    "ostatnie wersje":
        "recent versions",
    "wszystkie wersje":
        "all versions",

    # ------------------------------------------------ przeglądanie kopii
    " (niedokończona)":
        " (unfinished)",
    "Fragment nazwy albo ścieżki, bez rozróżniania wielkości liter.":
        "Part of a name or path, case-insensitive.",
    "Główny folder kopii":
        "Main backup folder",
    "Historia pliku":
        "File history",
    "Nazwa":
        "Name",
    "Nic nie znaleziono.":
        "Nothing found.",
    "Nie udało się: {error}":
        "Failed: {error}",
    "Odtwarza plik do katalogu tymczasowego i otwiera go":
        "Restores the file to a temporary folder and opens it",
    "Odtwarza plik w wybranym miejscu":
        "Restores the file to a location you choose",
    "Odtwarzam „{name}”…":
        "Restoring “{name}”…",
    "Otwarto kopię „{name}” (plik tymczasowy, zniknie po zamknięciu programu).":
        "Opened the copy of “{name}” (a temporary file, removed when the program closes).",
    "Otwórz":
        "Open",
    "Otwórz kopię":
        "Open copy",
    "Pliki i wersje wprost z kopii — bez przywracania":
        "Files and versions straight from the backup — no restore needed",
    "Pliki i wersje wprost z kopii — bez przywracania całości.":
        "Files and versions straight from the backup — without restoring all of it.",
    "Pokazuje pliki i wersje tej kopii — pojedynczy plik otworzysz bez przywracania całości":
        "Shows the files and versions of this backup — open a single file without restoring everything",
    "Pokaż foldery":
        "Show folders",
    "Przeglądaj…":
        "Browse…",
    "Przeglądanie":
        "Browse",
    "Przeszukuje spis treści kopii":
        "Searches the backup's table of contents",
    "Rozmiar":
        "Size",
    "Szukaj":
        "Search",
    "Szukaj pliku w najnowszym stanie kopii…":
        "Search for a file in the latest state of the backup…",
    "Szukam…":
        "Searching…",
    "W których wersjach jest ten plik i kiedy się zmieniał":
        "Which versions contain this file and when it changed",
    "W tym folderze nie ma wersji kopii.":
        "There are no backup versions in this folder.",
    "Wczytuje wersje z tego folderu kopii":
        "Loads the versions from this backup folder",
    "Wersja kopii, której zawartość widzisz poniżej.":
        "The backup version whose contents you see below.",
    "Wersja: {version}":
        "Version: {version}",
    "Wersje z tym plikiem: {count}. Dwuklik otwiera kopię z danej wersji.":
        "Versions with this file: {count}. Double-click opens the copy from that version.",
    "Wraca z wyników wyszukiwania do drzewa folderów":
        "Goes back from the search results to the folder tree",
    "Wskaż folder kopii i kliknij „Otwórz”.":
        "Choose the backup folder and click “Open”.",
    "Zapisano: {path}":
        "Saved: {path}",
    "Zapisz jako…":
        "Save as…",
    "Zapisz kopię pliku":
        "Save a copy of the file",
    "Zaznacz plik i wybierz „Otwórz kopię”, żeby zajrzeć do niego w zwykłym programie, albo „Historia pliku”, żeby zobaczyć, w których wersjach się zmieniał.":
        "Select a file and choose “Open copy” to look at it in its usual program, or “File history” to see in which versions it changed.",
    "Zmieniono":
        "Modified",
    "Znalezione pliki: {count}. Wyniki pochodzą z najnowszego stanu kopii.":
        "Files found: {count}. The results come from the latest state of the backup.",
    "przeglądanie kopii":
        "browsing the backup",
    "zmieniony":
        "changed",

    # ------------------------------------- przeglądanie kopii — historia
    "najstarsza zachowana kopia":
        "oldest copy kept",

    # ------------------------------------------- wersja ze Sklepu (MSIX)
    "Foldery w AppData":
        "Folders in AppData",
    "Przywracanie utworzy nowe foldery bezpośrednio w AppData:\n\n{folders}\n\nWindows pozwala wersji programu ze Sklepu tworzyć je tylko w jej prywatnej kopii — pliki będą widoczne w tym programie, ale nie w programie, do którego należą.\n\nNajprościej: zainstaluj i raz uruchom tamten program (utworzy swój folder), a potem przywróć jeszcze raz. Albo przywróć do zwykłego folderu i przenieś pliki Eksploratorem.":
        "The restore will create new folders directly in AppData:\n\n{folders}\n\nWindows lets the Store version of this program create them only in its private copy — the files will be visible in this program, but not in the program they belong to.\n\nThe easiest way: install and run that program once (it creates its folder), then restore again. Or restore to a regular folder and move the files with File Explorer.",
    "Przywracanie utworzyłoby w AppData nowe foldery, których inne programy nie zobaczą: {folders}":
        "The restore would create new folders in AppData that other programs will not see: {folders}",
    "Przywracanie wstrzymane do decyzji.":
        "Restore paused, waiting for your decision.",
    "Przywróć mimo to":
        "Restore anyway",
    "Start programu przy logowaniu wyłączono w Ustawieniach Windows. Włączysz go tam: Ustawienia → Aplikacje → Uruchamianie → Sigelith Backup.":
        "Starting the program at sign-in was turned off in Windows Settings. Turn it on there: Settings → Apps → Startup → Sigelith Backup.",
    "Start przy logowaniu":
        "Start at sign-in",
    "Start przy logowaniu wyłączono w Ustawieniach Windows → Aplikacje → Uruchamianie; dopóki go tam nie włączysz, kopie planowe działają tylko przy otwartym programie.":
        "Start at sign-in was turned off in Windows Settings → Apps → Startup; until you turn it back on there, scheduled backups run only while the program is open.",
    "Ten sam przełącznik jest w Ustawieniach Windows → Aplikacje → Uruchamianie. Wyłączony tam da się włączyć tylko tam.":
        "The same switch is in Windows Settings → Apps → Startup. If turned off there, it can only be turned back on there.",

    # --------------------------------------------- licencje i prywatność
    "Brak pliku {name} w katalogu programu.":
        "The file {name} is missing from the program folder.",
    "Jakie dane program przetwarza i gdzie":
        "What data the program processes and where",
    "Kod źródłowy Qt":
        "Qt source code",
    "Licencja programu":
        "Program license",
    "Licencja programu i licencje użytych składników":
        "The program's license and the licenses of the components it uses",
    "Licencje":
        "Licenses",
    "Licencje i prywatność":
        "Licenses and privacy",
    "Licencje…":
        "Licenses…",
    "Otwiera folder z plikami licencji w Eksploratorze":
        "Opens the folder with the license files in File Explorer",
    "Pokaż pliki licencji":
        "Show license files",
    "Polityka prywatności":
        "Privacy policy",
    "Polityka prywatności…":
        "Privacy policy…",
    "Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0 — to osobne pliki w katalogu programu, które można zastąpić zgodnymi wersjami. Kod źródłowy wersji dołączonych do programu: {qt} oraz {pyside}.":
        "The program uses the Qt and PySide6 libraries under the LGPL-3.0 license — they are separate files in the program folder and can be replaced with compatible versions. Source code of the versions included with the program: {qt} and {pyside}.",
    "Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0, z Pythona i z innych składników na licencjach otwartych (m.in. MIT, BSD, Apache 2.0); ikony: Bootstrap Icons (MIT). Wykaz, prawa autorskie, pełne teksty licencji i adresy kodu źródłowego Qt są pod przyciskiem „Licencje”.":
        "The program uses the Qt and PySide6 libraries under the LGPL-3.0 license, Python and other components under open-source licenses (including MIT, BSD, Apache 2.0); icons: Bootstrap Icons (MIT). The list, copyright notices, full license texts and the Qt source code addresses are under the “Licenses” button.",
    "Program usunie z Menedżera poświadczeń Windows wszystkie hasła, które zapamiętał: hasła kopii i dane dostępu do kopii poza domem. Kopie planowe szablonów zaszyfrowanych będą potem czekać, aż podasz hasło.\n\nUsunąć?":
        "The program will delete all passwords it remembered from the Windows Credential Manager: backup passwords and off-site copy credentials. Scheduled backups of encrypted templates will then wait until you enter the password.\n\nDelete them?",
    "Składniki i ich licencje":
        "Components and their licenses",
    "Strona z kodem źródłowym Qt w wersji użytej w programie":
        "The page with the Qt source code of the version used in the program",
    "Usunięte zapamiętane hasła: {count}.":
        "Remembered passwords deleted: {count}.",
    "Usuwa z Menedżera poświadczeń Windows wszystkie hasła zapamiętane przez program — na przykład przed odinstalowaniem":
        "Deletes all passwords remembered by the program from the Windows Credential Manager — for example before uninstalling",
    "Usuń zapamiętane hasła":
        "Delete remembered passwords",
    "Usuń zapamiętane hasła…":
        "Delete remembered passwords…",

    # ----------------------------------------------------------- wydawca
    "© {years} {publisher}. Wolne oprogramowanie na licencji GNU GPL w wersji 3 lub nowszej.":
        "© {years} {publisher}. Free software under the GNU GPL version 3 or later.",
    "Kod źródłowy":
        "Source code",
    "Kod źródłowy programu w serwisie GitHub":
        "The program's source code on GitHub",

    # --------------------------------------- Sigelith (dawniej BeatTime)
    "Sigelith odrzucił żądanie ({status}): {detail}":
        "Sigelith rejected the request ({status}): {detail}",
    "Nie udało się połączyć z Sigelith: {error}":
        "Could not connect to Sigelith: {error}",
    "Sigelith odesłał potwierdzenie innej sumy kontrolnej.":
        "Sigelith returned a receipt for a different checksum.",
    "Znacznik czeka na połączenie z Sigelith.":
        "The timestamp is waiting for a connection to Sigelith.",
    "Podpis tygodnia nie zgadza się z kluczem Sigelith zapisanym w programie.":
        "The week's signature does not match the Sigelith key built into the program.",
    "Otwiera certyfikat znacznika na stronie Sigelith":
        "Opens the timestamp certificate on the Sigelith website",
    "Podpis Sigelith: {answer}":
        "Sigelith signature: {answer}",
    "Znaczniki Sigelith wersji w tym katalogu kopii: sprawdzenie i certyfikat":
        "Sigelith timestamps of the versions in this backup folder: check and certificate",
    "Znakuję wersję czasem Sigelith (wysyłana jest tylko suma kontrolna)…":
        "Timestamping the version with Sigelith (only the checksum is sent)…",
    "Znacznik czasu czeka na połączenie z Sigelith — zostanie wysłany przy następnej kopii.":
        "The timestamp is waiting for a connection to Sigelith — it will be sent with the next backup.",
    "Znakuj wersję czasem Sigelith":
        "Timestamp the version with Sigelith",
    "Znaczniki czasu Sigelith":
        "Sigelith timestamps",
    "czeka na połączenie z Sigelith":
        "waiting for a connection to Sigelith",
    "Dowód, że kopia w tym kształcie istniała danego dnia (podpis Ed25519, kotwica\nw Bitcoinie). Do sigelith.org trafia wyłącznie suma kontrolna spisu wersji —\nżadne nazwy plików ani ich treść.":
        "Proof that the backup existed in exactly this shape on a given day (Ed25519 signature,\nBitcoin anchor). Only the checksum of the version list goes to sigelith.org —\nno file names and no content.",
    "Kopie zapasowe folderów na dysk zewnętrzny, z historią wersji i szyfrowaniem. Wszystko dzieje się na Twoim komputerze, bez konta i bez telemetrii. Z internetem program łączy się tylko wtedy, gdy sam włączysz kopię poza domem albo znaczniki czasu Sigelith.":
        "Backups of your folders to an external drive, with version history and encryption. Everything happens on your computer, with no account and no telemetry. The program connects to the internet only when you turn on the off-site copy or Sigelith timestamps yourself.",

    # --------------------------------------------------- dowody Sigelith
    "Bez dokumentu: {count} {stamps} — plik zmienił się po stemplu albo zniknął i nie ma go w żadnej wersji tej kopii ({names}). Sam dowód jest zachowany.":
        "Without a document: {count} {stamps} — the file changed after stamping or disappeared, and it is not in any version of this backup ({names}). The proof itself is kept.",
    "Brak pliku dowodu albo dowód jest zaszyfrowany.":
        "The proof file is missing or encrypted.",
    "Chroni dowody Sigelith: historię stempli i oznakowane dokumenty.":
        "Protects Sigelith evidence: the stamp history and the stamped documents.",
    "Chroń dowody Sigelith":
        "Protect Sigelith evidence",
    "Chroń też dowody Sigelith":
        "Also protect Sigelith evidence",
    "Dokument":
        "Document",
    "Dokumenty oznakowane w Sigelith, zabezpieczone w tej kopii: sprawdzenie i odzyskanie":
        "Documents stamped with Sigelith and safeguarded in this backup: check and recover",
    "Dowody Sigelith":
        "Sigelith evidence",
    "Dowody Sigelith: historia stempli i dokładne kopie oznakowanych dokumentów z plikami .beatproof trafią do magazynu dowodów w katalogu kopii.":
        "Sigelith evidence: the stamp history and exact copies of the stamped documents with their .beatproof files will go to the evidence store in the backup folder.",
    "Dowody Sigelith: zabezpieczone dokumenty {count} z {total}":
        "Sigelith evidence: documents safeguarded {count} of {total}",
    "Dowody Sigelith…":
        "Sigelith evidence…",
    "Dowody z problemem: {count} — szczegóły w kolumnie „Stan”.":
        "Proofs with a problem: {count} — details in the “Status” column.",
    "Dowodów Sigelith nie udało się zabezpieczyć: {error}":
        "Sigelith evidence could not be safeguarded: {error}",
    "Droga w drzewie Merkle'a nie prowadzi do podpisanego korzenia tygodnia.":
        "The Merkle tree path does not lead to the signed root of the week.",
    "Gdzie zapisać dokumenty i dowody":
        "Where to save the documents and proofs",
    "Historia stempli Sigelith Desktop i dokładne bajty oznakowanych dokumentów, z plikami .beatproof — w osobnym magazynie, którego retencja nie sprząta.":
        "The Sigelith Desktop stamp history and the exact bytes of the stamped documents, with .beatproof files — in a separate store that retention never cleans up.",
    "Każdy stempel ma tu swój folder z dokładnie tym dokumentem, który oznakowano, i plikiem .beatproof. „Sprawdź” liczy sumę każdego dokumentu i sprawdza podpis tygodnia bez łączenia się z siecią.":
        "Each stamp has its own folder here with exactly the document that was stamped and a .beatproof file. “Check” computes the checksum of each document and verifies the week's signature without connecting to the network.",
    "Kopia obejmie folder danych Sigelith Desktop (historię stempli), a każdy oznakowany\ndokument trafi — dokładnie w tej postaci, którą oznakowano — do magazynu dowodów\nw katalogu kopii, razem z plikiem .beatproof. Starych wersji magazyn nie dotyczy:\nretencja go nie sprząta.":
        "The backup will include the Sigelith Desktop data folder (the stamp history), and every stamped\ndocument — exactly as it was stamped — will go to the evidence store in the backup\nfolder, together with its .beatproof file. The store is separate from old versions:\nretention never cleans it up.",
    "Magazyn dowodów jest pusty.":
        "The evidence store is empty.",
    "Na tym komputerze jest Sigelith Desktop: {count} {stamps}.":
        "Sigelith Desktop is on this computer: {count} {stamps}.",
    "Na tym komputerze nie ma danych Sigelith Desktop.":
        "There is no Sigelith Desktop data on this computer.",
    "Otwórz folder dowodów":
        "Open evidence folder",
    "Oznakowano":
        "Stamped",
    "Pokazuje magazyn dowodów w Eksploratorze":
        "Shows the evidence store in File Explorer",
    "Przywróć zaznaczone…":
        "Restore selected…",
    "Sigelith Desktop: {count} {stamps} w folderze {path}.":
        "Sigelith Desktop: {count} {stamps} in the folder {path}.",
    "Sprawdza każdy dokument i jego dowód bez łączenia z siecią":
        "Checks every document and its proof without connecting to the network",
    "Sprawdzam dowody…":
        "Checking proofs…",
    "Stan":
        "Status",
    "Stemple w magazynie: {count}, z dokumentem: {documents}.":
        "Stamps in the store: {count}, with a document: {documents}.",
    "Suma dokumentu nie zgadza się z dowodem.":
        "The document's checksum does not match the proof.",
    "To nie jest plik dowodu Sigelith (beatproof-v1).":
        "This is not a Sigelith proof file (beatproof-v1).",
    "Tydzień stempla jeszcze się nie zamknął — podpis dojdzie przy kolejnej kopii.":
        "The stamp's week has not closed yet — the signature will be added with a later backup.",
    "W magazynie nie ma dokumentu do tego dowodu.":
        "The store has no document for this proof.",
    "Wszystkie dowody pasują do dokumentów i mają poprawny podpis.":
        "All proofs match their documents and have a valid signature.",
    "Zabezpieczam dokumenty oznakowane w Sigelith…":
        "Safeguarding documents stamped with Sigelith…",
    "Zapisano pliki: {count} w {path}.":
        "Files saved: {count} in {path}.",
    "Zapisuje dokumenty razem z plikami .beatproof we wskazanym folderze":
        "Saves the documents together with their .beatproof files in a folder you choose",
    "bez dokumentu — dowód zachowany":
        "no document — proof kept",
    "czekają na podpis tygodnia: {count}":
        "waiting for the week's signature: {count}",
    "dokument i dowód są w kopii":
        "document and proof are in the backup",
    "dokument jest; dowód czeka na podpis tygodnia":
        "document present; proof waiting for the week's signature",
    "dowodu nie da się odczytać":
        "the proof cannot be read",
    "dowody Sigelith":
        "Sigelith evidence",
    "dowody uzupełnione o podpis tygodnia: {count}":
        "proofs completed with the week's signature: {count}",
    "nowe: {count}":
        "new: {count}",
    "odtworzone ze starszych wersji kopii: {count}":
        "recovered from older backup versions: {count}",
    "sprawdzony: dokument i dowód się zgadzają":
        "checked: document and proof match",
    "stempel":
        "stamp",
    "stemple":
        "stamps",
    "stempli":
        "stamps",
    "zaszyfrowany — podaj hasło, żeby sprawdzić":
        "encrypted — enter the password to check",

    # ------------------------------------ kreator: dowody czasu Sigelith
    "Chroń dowody Sigelith, gdy go zainstaluję":
        "Protect Sigelith evidence once I install it",
    "Dowody Sigelith: na tym komputerze nie ma jeszcze Sigelith Desktop — ochrona zacznie działać sama, gdy się pojawi.":
        "Sigelith evidence: Sigelith Desktop is not on this computer yet — protection will start by itself once it appears.",
    "Dowody Sigelith: ochrona zacznie działać sama, gdy zainstalujesz Sigelith Desktop.":
        "Sigelith evidence: protection will start by itself once you install Sigelith Desktop.",
    "Dowody czasu dla ważnych dokumentów":
        "Proof of time for important documents",
    "Kopia zachowa każdy dokument oznakowany w Sigelith Desktop dokładnie w tej postaci, którą oznakowano, razem z dowodem — nawet gdy oryginał później się zmieni.":
        "The backup will keep every document stamped with Sigelith Desktop exactly as it was stamped, together with its proof — even if the original changes later.",
    "Ochrona zacznie działać sama, gdy na komputerze pojawi się Sigelith Desktop.":
        "Protection will start by itself once Sigelith Desktop appears on this computer.",
    "Otwiera stronę programu Sigelith Desktop":
        "Opens the Sigelith Desktop page",
    "Poznaj Sigelith Desktop":
        "Discover Sigelith Desktop",
    "Sigelith Desktop, program tego samego wydawcy, oznakuje dokument czasem: to podpisany dowód, że plik w tej postaci istniał w danej chwili, sprawdzalny bez udziału kogokolwiek. Sigelith Backup przechowa potem każdy oznakowany dokument razem z dowodem.":
        "Sigelith Desktop, a program from the same publisher, stamps a document with time: a signed proof that the file existed in exactly this form at a given moment, verifiable without relying on anyone. Sigelith Backup then keeps every stamped document together with its proof.",
    "Umowy, faktury, projekty — czasem trzeba wykazać, że dokument istniał danego dnia.":
        "Contracts, invoices, projects — sometimes you need to show that a document existed on a given day.",
    'Nieznany format spisu wersji.':
        'Unknown version index format.',
    'Ta wersja nie ma pieczęci dla pojedynczych plików (kopia sprzed wersji 3.0 albo bez znaczników czasu).':
        'This version has no seal for individual files (a backup made before version 3.0 or without timestamps).',
    'Pieczęć tej wersji czeka jeszcze na podpis tygodnia Sigelith — dowód będzie gotowy po poniedziałku 00:00 UTC i kolejnej kopii.':
        "This version's seal is still waiting for the Sigelith weekly signature — the proof will be ready after Monday 00:00 UTC and the next backup.",
    'Brak oświadczenia pieczęci w folderze wersji.':
        'The seal statement is missing from the version folder.',
    'Oświadczenie pieczęci nie zgadza się z pieczęcią wersji.':
        'The seal statement does not match the version seal.',
    'Drzewo plików wersji nie zgadza się z pieczęcią.':
        "The version's file tree does not match the seal.",
    'Tego pliku nie ma w spisie tej wersji.':
        "This file is not in this version's index.",
    'To nie jest dowód pliku z kopii Sigelith Backup ({format}).':
        'This is not a Sigelith Backup file proof ({format}).',
    'Dowód jest uszkodzony — brakuje pól albo mają zły format.':
        'The proof is damaged — fields are missing or malformed.',
    'Ten plik nie jest plikiem, którego dotyczy dowód.':
        'This file is not the file the proof is about.',
    'Ścieżka pliku w dowodzie nie zgadza się z liściem drzewa.':
        'The file path in the proof does not match the tree leaf.',
    'Droga w drzewie plików nie prowadzi do korzenia z pieczęci.':
        'The path in the file tree does not lead to the sealed root.',
    'Oświadczenie pieczęci nie potwierdza tego drzewa plików.':
        'The seal statement does not confirm this file tree.',
    'Potwierdzenie Sigelith nie dotyczy tej pieczęci.':
        'The Sigelith confirmation is not for this seal.',
    'Dowód czasu…':
        'Time proof…',
    'Zapisuje dowód, że ten plik był w kopii w chwili jej oznakowania — bez ujawniania innych plików':
        'Saves a proof that this file was in the backup when it was sealed — without revealing other files',
    'Dowód czasu':
        'Time proof',
    'Dołączyć do dowodu ścieżkę pliku w kopii („{path}”)?\n\nBez niej dowód dalej potwierdza plik i chwilę oznakowania, ale nie mówi, gdzie plik leżał.':
        "Include the file's path in the backup (“{path}”) in the proof?\n\nWithout it the proof still confirms the file and the moment of sealing, but not where the file was.",
    'Przygotowuję dowód dla „{name}”…':
        'Preparing the proof for “{name}”…',
    'Zapisz dowód czasu':
        'Save time proof',
    'Dowód pliku Sigelith (*{suffix})':
        'Sigelith file proof (*{suffix})',
    'Zapisano dowód i certyfikat PDF: {path}. Sprawdzi go Sigelith Desktop albo strona sigelith.org/verify/.':
        'Saved the proof and PDF certificate: {path}. Sigelith Desktop or sigelith.org/verify/ can check it.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją sprawdzić.':
        'The backup is encrypted — enter the password to check it.',
    'Ta wersja nie ma pieczęci — nie ma z czym porównać plików.':
        'This version has no seal — there is nothing to compare the files with.',
    'Pieczęć wersji się nie potwierdza: {problems}':
        "The version's seal does not check out: {problems}",
    'brak podpisu tygodnia':
        'no weekly signature',
    'Audyt przerwany.':
        'Audit cancelled.',
    'próbka {checked} z {listed} plików':
        'a sample of {checked} of {listed} files',
    'wszystkie pliki ({count})':
        'all files ({count})',
    'Nietknięta: sprawdzono {scope}, wszystko zgodne z pieczęcią w publicznym dzienniku.':
        'Untouched: checked {scope}, everything matches the seal in the public log.',
    'zmienione: {files}':
        'changed: {files}',
    'brakujące: {files}':
        'missing: {files}',
    'nieczytelne albo uszkodzone: {files}':
        'unreadable or damaged: {files}',
    'PODMIENIONA albo uszkodzona ({scope}) — {details}.':
        'TAMPERED WITH or damaged ({scope}) — {details}.',
    'Audyt treści':
        'Content audit',
    'Czyta z nośnika każdy plik tej wersji i porównuje go z sumą oznakowaną w publicznym dzienniku':
        'Reads every file of this version from the drive and compares it with the hash sealed in the public log',
    'Ostatnia nietknięta':
        'Last untouched',
    'Sprawdza wersje od najnowszej i wskazuje ostatnią zgodną z pieczęcią — z niej przywracaj':
        'Checks versions from the newest and points to the latest one that matches its seal — restore from it',
    'Ostatnia nietknięta wersja: {label} — z niej przywracaj.':
        'Last untouched version: {label} — restore from it.',
    'Żadna wersja z pieczęcią nie jest nietknięta.':
        'No sealed version is untouched.',
    'Czytam pliki kopii i porównuję je z pieczęcią w publicznym dzienniku…':
        'Reading the backup files and comparing them with the seal in the public log…',
    'Sprawdzam próbkę starszej wersji z pieczęcią w publicznym dzienniku…':
        'Checking a sample of an older version against its seal in the public log…',
    'Audyt z pieczęcią: próbka wersji {label} zgodna z publicznym dziennikiem.':
        'Seal audit: a sample of version {label} matches the public log.',
    'UWAGA — audyt z pieczęcią, wersja {label}: {details}':
        'WARNING — seal audit, version {label}: {details}',
    'Przekaż…':
        'Hand over…',
    'Zapisuje tę wersję pliku i otwiera ją w Sigelith Handover — odbiorca potwierdzi odbiór własnym kluczem':
        'Saves this version of the file and opens it in Sigelith Handover — the recipient will confirm receipt with their own key',
    'Przekazanie z dowodem doręczenia':
        'Hand over with proof of delivery',
    'Przekazanie z dowodem doręczenia robi Sigelith Desktop (od wersji 3.0.1): odbiorca potwierdza odbiór własnym kluczem, a chwila doręczenia trafia do publicznego dziennika. Na tym komputerze go nie ma albo jest w starszej wersji. Otworzyć stronę programu?':
        "Handing over with proof of delivery is done by Sigelith Desktop (version 3.0.1 or later): the recipient confirms receipt with their own key, and the moment of delivery goes into the public log. It is not on this computer, or it is an older version. Open the program's page?",
    'Zapisz plik do przekazania':
        'Save the file to hand over',
    'Otwieram Sigelith Handover z plikiem „{name}” — wybierz odbiorcę.':
        'Opening Sigelith Handover with “{name}” — choose the recipient.',
    'Kapsuły czasu…':
        'Time capsules…',
    'Pliki zapieczętowane w tej kopii do daty — klucze wydają dopiero po niej sieć drand i serwer kluczy Sigelith':
        'Files sealed in this backup until a date — the drand network and the Sigelith key server release the keys only after it',
    'Wskaż najpierw folder kopii — kapsuła leży w kopii.':
        'Choose the backup folder first — the capsule is kept in the backup.',
    'Kapsuły czasu':
        'Time capsules',
    'Kapsuła pieczętuje wybrany folder do chwili, którą wskażesz. Otwierają ją dowolne dwie z trzech części: runda sieci drand z tej chwili, udział serwera kluczy Sigelith (wydawany dopiero po tej chwili — to zasada operatora, nie kryptografia) i kod odzyskiwania zapisany obok kapsuły. Kto ma tę kopię, ma więc i kod: do wcześniejszego otwarcia wystarczy mu, że operator złamie swoją zasadę. Po tej chwili otworzy ją każdy, kto ma jej pliki. Kapsuła leży w tej kopii, nie na serwerze; otwiera ją strona sigelith.org/capsule/.':
        "A capsule seals the chosen folder until the moment you pick. Any two of three parts open it: the drand network's round for that moment, the Sigelith key server's share (released only after that moment — by the operator's policy, not by cryptography) and the recovery code saved next to the capsule. Whoever has this backup therefore has the code too, and needs only the operator to break its policy to open it early. After that moment anyone who has its files can open it. The capsule is kept in this backup, not on a server; the sigelith.org/capsule/ page opens it.",
    'Wybierz kapsułę z listy albo utwórz nową.':
        'Choose a capsule from the list or create a new one.',
    'Nowa kapsuła…':
        'New capsule…',
    'Pieczętuje wybrany folder do daty':
        'Seals the chosen folder until a date',
    'Pokaż w folderze':
        'Show in folder',
    'Otwiera folder kapsuły w Eksploratorze':
        'Opens the capsule folder in File Explorer',
    'Otwórz na stronie':
        'Open on the website',
    'Strona sigelith.org/capsule/ otwiera kapsułę po jej dacie':
        'The sigelith.org/capsule/ page opens the capsule after its date',
    'można otworzyć':
        'can be opened',
    'zamknięta':
        'sealed',
    'W tej kopii nie ma jeszcze kapsuł czasu.':
        'There are no time capsules in this backup yet.',
    'Ta kapsuła da się otworzyć na stronie sigelith.org/capsule/ — wskaż jej pliki.':
        'This capsule can be opened on the sigelith.org/capsule/ page — choose its files there.',
    'Kapsuła jest zamknięta do daty z listy. Kod odzyskiwania leży w pliku obok niej.':
        'The capsule is sealed until the date in the list. The recovery code is in a file next to it.',
    'Wybierz folder do zapieczętowania':
        'Choose the folder to seal',
    'Pieczętuję „{name}” — kilka sekund na krzywej eliptycznej…':
        'Sealing “{name}” — a few seconds on the elliptic curve…',
    'kapsuła czasu':
        'time capsule',
    'Kapsuła zapieczętowana':
        'Capsule sealed',
    '„{name}” otworzy się najwcześniej {when}.\n\nKod odzyskiwania (skopiowany do schowka, zapisany też obok kapsuły):\n\n{code}\n\nZapisz go w bezpiecznym miejscu. Przed datą otwarcia sam niczego nie otwiera; po niej zastępuje jeden z kluczy, gdyby był niedostępny.':
        '“{name}” opens no earlier than {when}.\n\nRecovery code (copied to the clipboard, also saved next to the capsule):\n\n{code}\n\nKeep it in a safe place. Before the opening date it opens nothing on its own; after it, it replaces one of the keys should one be unavailable.',
    'Nie udało się zapieczętować: {error}':
        'Could not seal: {error}',
    'Nowa kapsuła czasu':
        'New time capsule',
    'Otworzy się najwcześniej':
        'Opens no earlier than',
    'kapsuła':
        'capsule',
    'Chwila otwarcia musi być w przyszłości.':
        'The opening moment must be in the future.',
    'Na bieżąco':
        'Live',
    'Zmiany w folderach źródłowych trafiają do dzisiejszej wersji kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje. Jedna wersja na dzień; ze znacznikami czasu zamyka ją pieczęć następnego dnia.':
        "Changes in the source folders go into today's backup version a few minutes after they are saved, and when the drive is connected the backup catches up at once. One version per day; with timestamps it is closed by a seal the next day.",
    'Na bieżąco — po każdej zmianie i po podłączeniu dysku':
        'Live — after every change and when the drive is connected',
    'Dla dysku podłączonego na stałe albo często: zmiany trafiają do kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje.':
        'For a drive that is always or often connected: changes reach the backup a few minutes after they are saved, and when the drive is connected the backup catches up at once.',
    'Kopia będzie na bieżąco: zmiany trafią do dzisiejszej wersji kilka minut po zapisie, a po podłączeniu dysku kopia od razu się zsynchronizuje.':
        "The backup will stay current: changes go into today's version a few minutes after they are saved, and when the drive is connected the backup catches up at once.",
    # opis bieżącej operacji w pasku stanu („Trwa: przywracanie…”)
    "przywracanie": "restore",
    # tytuł kreatora, gdy zakłada kolejną kopię (nie pierwszą)
    "Nowa kopia krok po kroku": "New backup, step by step",
}
