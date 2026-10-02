"""Katalog niemiecki: „polski tekst źródłowy” → „tekst (niemiecki)”.

Klucze są te same co w ``en.py`` i muszą dokładnie odpowiadać napisom w kodzie;
pilnuje tego ``tests/test_i18n.py``. Pola w nawiasach klamrowych (``{count}``)
zostają bez zmian. Formaty dat są te same co w Sigelith Desktop.
"""

from __future__ import annotations

TEXTS: dict[str, str] = {
    '\n\nLokalizacja:\n{path}':
        '\n\nSpeicherort:\n{path}',
    '\nDo uzupełnienia: niedokończone kopie: {count} — możesz je uzupełnić, wybierając wersję poniżej.':
        '\nUnvollständige Sicherungen: {count} — du kannst sie ergänzen, indem du unten eine Version wählst.',
    '\nUwaga: duży klaster ({size}): każdy mały plik zajmuje co najmniej tyle miejsca. Przy wielu małych plikach kopia zajmie wielokrotnie więcej niż dane.':
        '\nHinweis: großer Cluster ({size}): Jede kleine Datei belegt mindestens so viel Platz. Bei vielen kleinen Dateien belegt die Sicherung ein Vielfaches der eigentlichen Datenmenge.',
    '\nUwaga: niedokończone wersje (nie zawierają wszystkich plików): {names}':
        '\nHinweis: unvollständige Versionen (sie enthalten nicht alle Dateien): {names}',
    '\nUwaga: {filesystem} nie obsługuje twardych dowiązań — każda wersja z datą zajmuje tyle miejsca co pełna kopia.':
        '\nHinweis: {filesystem} unterstützt keine Hardlinks — jede datierte Version belegt so viel Platz wie eine vollständige Kopie.',
    ' wersji':
        ' Versionen',
    ' z szyfrowaniem AES-256-GCM…':
        ' mit AES-256-GCM-Verschlüsselung…',
    ' ×':
        ' ×',
    ' — a ponieważ {filesystem} nie obsługuje twardych dowiązań, zapisze ponownie wszystkie pliki i zajmie tyle miejsca co cała kopia':
        ' — und da {filesystem} keine Hardlinks unterstützt, schreibt sie alle Dateien neu und belegt so viel Platz wie die gesamte Sicherung',
    ' • pozostało {time}':
        ' • noch {time}',
    '%d.%m %H:%M':
        '%d.%m. %H:%M',
    '%d.%m.%Y':
        '%d.%m.%Y',
    '%d.%m.%Y %H:%M':
        '%d.%m.%Y, %H:%M',
    ', klaster {size}':
        ', Cluster {size}',
    ', uzupełniona {when}':
        ', ergänzt {when}',
    'Analizuje pliki i pokazuje plan. Nic nie zapisuje.':
        'Analysiert die Dateien und zeigt den Plan. Schreibt nichts.',
    'Anulowano przed rozpoczęciem kopii.':
        'Vor Beginn der Sicherung abgebrochen.',
    'Anuluj':
        'Abbrechen',
    'Argon2id (t={passes}, {memory} MiB, p={threads})':
        'Argon2id (t={passes}, {memory} MiB, p={threads})',
    'Argon2id — {passes} przebiegi, {memory} MiB, {threads} wątki':
        'Argon2id — {passes} Durchläufe, {memory} MiB, {threads} Threads',
    'Automatycznie (język systemu)':
        'Automatisch (Systemsprache)',
    'Bardzo dobre':
        'Sehr stark',
    'Bardzo słabe':
        'Sehr schwach',
    'Brak manifestu — skanuję katalog kopii.':
        'Kein Manifest — der Sicherungsordner wird gescannt.',
    'Brakuje tagu uwierzytelniającego — plik jest obcięty.':
        'Das Authentifizierungs-Tag fehlt — die Datei ist abgeschnitten.',
    'Błąd uruchamiania':
        'Startfehler',
    'Ciemny':
        'Dunkel',
    'Co dokładnie zostanie zapisane przy najbliższym przebiegu.':
        'Was beim nächsten Durchlauf genau geschrieben wird.',
    'Co kopiujemy':
        'Was gesichert wird',
    'Co zrobić, gdy plik o tej nazwie już istnieje w katalogu docelowym.':
        'Was geschehen soll, wenn eine Datei dieses Namens im Zielordner bereits existiert.',
    'Czas w nazwie to BeatTime — 1000 beatów na dobę, kotwica w UTC, ten sam moment na całym świecie. Data jest datą UTC, więc zgadza się z zegarem.':
        'Die Zeit im Namen ist BeatTime — 1000 Beats pro Tag, an UTC verankert, überall auf der Welt derselbe Moment. Das Datum ist das UTC-Datum und passt daher zur Uhr.',
    'Czym jest {app}':
        'Was ist {app}',
    'Czyści tylko okno — plik dziennika pozostaje':
        'Leert nur das Fenster — die Protokolldatei bleibt erhalten',
    'Dane aplikacji: {path}':
        'Programmdaten: {path}',
    'Decyduje, czy zachowujemy historię wersji.':
        'Legt fest, ob ein Versionsverlauf aufbewahrt wird.',
    'Dobre':
        'Stark',
    'Dodaj folder':
        'Ordner hinzufügen',
    'Dodaj przynajmniej jeden folder źródłowy.':
        'Füge mindestens einen Quellordner hinzu.',
    'Dogrywka zmian z czasu kopii:':
        'Änderungen während der Sicherung nachsichern:',
    'Dokąd przywracamy':
        'Wohin wiederhergestellt wird',
    'Dokładnie to, co program realnie stosuje.':
        'Genau das, was das Programm tatsächlich verwendet.',
    'Domyślne wykluczenia':
        'Standard-Ausschlüsse',
    'Domyślne wykluczenia zapisane.':
        'Standard-Ausschlüsse gespeichert.',
    'Domyślnie wyłączone. Przy włączonej opcji skasowanie pliku w źródle\nusuwa też jego jedyną kopię zapasową — operacja nieodwracalna.':
        'Standardmäßig aus. Wenn eingeschaltet, wird beim Löschen einer Datei in der Quelle\nauch ihre einzige Sicherungskopie entfernt — das lässt sich nicht rückgängig machen.',
    'Dopisuj do nazwy katalogu datę ostatniego uzupełnienia':
        'Datum der letzten Ergänzung an den Ordnernamen anhängen',
    'Dziennik':
        'Protokoll',
    'Dziennik: {path}':
        'Protokoll: {path}',
    'Ekran przywracania wypełniony danymi szablonu.':
        'Wiederherstellungsseite mit den Daten der Vorlage ausgefüllt.',
    'Folder docelowy kopii — najlepiej na innym dysku fizycznym.':
        'Zielordner der Sicherung — am besten auf einem anderen physischen Laufwerk.',
    'Folder zawierający kopię utworzoną przez {app}.':
        'Ein Ordner mit einer Sicherung, die {app} erstellt hat.',
    'Gdy plik już istnieje:':
        'Wenn die Datei schon existiert:',
    'Gdzie zapisujemy':
        'Wohin gesichert wird',
    'Gotowe do pracy.':
        'Bereit.',
    'Gotowe. Wybierz foldery do kopii.':
        'Bereit. Wähle die Ordner, die gesichert werden sollen.',
    'Gotowe: {count} {files}, {size}, {seconds} s.':
        'Fertig: {count} {files}, {size}, {seconds} s.',
    'Główny folder kopii. Zawiera spis treści (.cleanvault-manifest).':
        'Der Hauptordner der Sicherung. Er enthält das Inhaltsverzeichnis (.cleanvault-manifest).',
    'Hasła nie da się odzyskać ani zresetować. Jeśli je zgubisz, dane z kopii zaszyfrowanej są bezpowrotnie stracone — tak działa poprawne szyfrowanie.':
        'Das Passwort lässt sich weder wiederherstellen noch zurücksetzen. Verlierst du es, sind die Daten einer verschlüsselten Sicherung unwiederbringlich verloren — so funktioniert korrekte Verschlüsselung.',
    'Hasła w obu polach różnią się.':
        'Die Passwörter in den beiden Feldern stimmen nicht überein.',
    'Hasło':
        'Passwort',
    'Hasło do kopii':
        'Passwort der Sicherung',
    'Hasło nie jest nigdzie zapisywane w postaci jawnej.\nBez niego nie da się odzyskać danych — nie istnieje żadna furtka serwisowa.':
        'Das Passwort wird nirgends im Klartext gespeichert.\nOhne Passwort lassen sich die Daten nicht wiederherstellen — eine Hintertür gibt es nicht.',
    'Hasło nie może być puste.':
        'Das Passwort darf nicht leer sein.',
    'Hasło niezapisane':
        'Passwort nicht gespeichert',
    'Hasło powinno mieć co najmniej 8 znaków.':
        'Das Passwort sollte mindestens 8 Zeichen lang sein.',
    'Hasło trafia do magazynu systemowego powiązanego z Twoim kontem.\nNigdy nie jest zapisywane w plikach programu.':
        'Das Passwort kommt in den Passwortspeicher des Systems, der an dein Konto gebunden ist.\nEs wird nie in die Dateien des Programms geschrieben.',
    'Hasło użyte przy tworzeniu kopii':
        'Das beim Erstellen der Sicherung verwendete Passwort',
    'Ile plików kopia przetwarza jednocześnie. Przy setkach tysięcy małych plików\nczas kopii to głównie opóźnienia na każdy plik (otwarcie, skanowanie\nantywirusowe, zapis na nośnik), a nie przesył danych — praca równoległa\nskraca go kilkukrotnie.\n\n„automatycznie” dobiera liczbę do procesora (do 32). Na wolnym dysku\ntalerzowym mniejsza wartość (2–4) bywa szybsza.':
        'Wie viele Dateien die Sicherung gleichzeitig verarbeitet. Bei Hunderttausenden kleiner Dateien\nbesteht die Dauer vor allem aus Wartezeiten pro Datei (Öffnen, Virenscan,\nSchreiben auf den Datenträger), nicht aus der Datenübertragung — paralleles Arbeiten\nverkürzt sie um ein Mehrfaches.\n\n„automatisch“ wählt die Anzahl passend zum Prozessor (bis 32). Auf einer langsamen\nMagnetfestplatte ist ein kleinerer Wert (2–4) oft schneller.',
    'Informacje przydatne przy zgłaszaniu problemu.':
        'Angaben, die beim Melden eines Problems helfen.',
    'Jak to działa':
        'So funktioniert es',
    'Jasny':
        'Hell',
    'Jeden folder utrzymywany w zgodzie ze źródłem. Brak historii wersji,\nza to najprostsza struktura i najmniejsze zużycie miejsca.':
        'Ein einziger Ordner, der mit der Quelle abgeglichen wird. Kein Versionsverlauf,\ndafür die einfachste Struktur und der geringste Platzbedarf.',
    'Jeśli operacja zakończy się błędem, skopiuj stąd ostatnie wiersze — zawierają dokładną przyczynę, a nie tylko komunikat ogólny.':
        'Endet ein Vorgang mit einem Fehler, kopiere von hier die letzten Zeilen — sie enthalten die genaue Ursache, nicht nur eine allgemeine Meldung.',
    'Język interfejsu zmieniony.':
        'Sprache der Oberfläche geändert.',
    'Język zmienisz po zakończeniu bieżącej operacji.':
        'Die Sprache kannst du ändern, sobald der laufende Vorgang abgeschlossen ist.',
    'Język:':
        'Sprache:',
    'Katalog docelowy leży wewnątrz źródła ({path}). Kopia kopiowałaby samą siebie w nieskończoność.':
        'Der Zielordner liegt innerhalb der Quelle ({path}). Die Sicherung würde sich endlos selbst kopieren.',
    'Katalog docelowy nie może być tym samym katalogiem co źródłowy.':
        'Der Zielordner darf nicht derselbe Ordner wie der Quellordner sein.',
    'Katalog jeszcze nie istnieje — zostanie utworzony.':
        'Der Ordner existiert noch nicht — er wird angelegt.',
    'Katalog kopii nie istnieje: {path}':
        'Der Sicherungsordner existiert nicht: {path}',
    'Katalog źródłowy nie istnieje: {path}':
        'Der Quellordner existiert nicht: {path}',
    'Katalog, w którym pojawią się odtworzone pliki.':
        'Der Ordner, in dem die wiederhergestellten Dateien erscheinen.',
    'Katalog, w którym powstanie kopia. Nie może leżeć wewnątrz folderu źródłowego.':
        'Der Ordner, in dem die Sicherung entsteht. Er darf nicht innerhalb eines Quellordners liegen.',
    'Katalogi objęte kopią.\nMożesz przeciągnąć foldery z Eksploratora Windows wprost na tę listę.':
        'Ordner, die gesichert werden.\nDu kannst Ordner aus dem Datei-Explorer direkt auf diese Liste ziehen.',
    'Każdy folder z datą jest kompletny — przywracanie nie wymaga sklejania wersji.':
        'Jeder datierte Ordner ist vollständig — zum Wiederherstellen müssen keine Versionen zusammengesetzt werden.',
    'Każdy plik jest czytany ponownie zaraz po zapisaniu. Dane pochodzą wtedy\nzwykle z pamięci podręcznej systemu, więc niewiele mówi to o nośniku,\na wydłuża kopię nawet dwukrotnie.\n\nSkuteczniejsza jest weryfikacja odroczona: ekran „Przywracanie” →\n„Sprawdź kopię”, najlepiej po ponownym podłączeniu dysku.':
        'Jede Datei wird direkt nach dem Schreiben erneut gelesen. Die Daten kommen dann\nmeist aus dem Cache des Systems, das sagt also wenig über den Datenträger aus,\nverlängert die Sicherung aber bis auf das Doppelte.\n\nWirksamer ist eine spätere Prüfung: Seite „Wiederherstellung“ →\n„Sicherung prüfen“, am besten nach erneutem Anschließen des Laufwerks.',
    'Każdy plik trafia do kopii jako zaszyfrowany kontener .cvlt.\nKlucz powstaje z hasła przez Argon2id.':
        'Jede Datei kommt als verschlüsselter .cvlt-Container in die Sicherung.\nDer Schlüssel wird mit Argon2id aus dem Passwort abgeleitet.',
    'Każdy przebieg tworzy osobny folder z datą i godziną.\nPliki niezmienione są podpinane twardym dowiązaniem, więc historia\nzajmuje tyle miejsca, ile realnie się zmieniło.':
        'Jeder Durchlauf legt einen eigenen Ordner mit Datum und Uhrzeit an.\nUnveränderte Dateien werden per Hardlink eingebunden, daher belegt der Verlauf\nnur so viel Platz, wie sich tatsächlich geändert hat.',
    'Klaster nośnika to {cluster} — pliki zajmą {actual} zamiast {logical} (narzut {overhead}).':
        'Der Cluster des Datenträgers beträgt {cluster} — die Dateien belegen {actual} statt {logical} (Mehrbedarf {overhead}).',
    'Kliknij szablon, aby zobaczyć jego szczegóły.':
        'Klicke auf eine Vorlage, um ihre Details zu sehen.',
    'Kliknij „Podgląd zmian”, aby sprawdzić plan bez zapisywania czegokolwiek.':
        'Klicke auf „Änderungsvorschau“, um den Plan zu prüfen, ohne etwas zu schreiben.',
    'Kolor wyróżnienia':
        'Akzentfarbe',
    'Kolor wyróżnienia…':
        'Akzentfarbe…',
    'Kopia':
        'Sicherung',
    'Kopia do dokończenia':
        'Unvollständige Sicherung',
    'Kopia jest aktualna — nie ma czego zapisywać.':
        'Die Sicherung ist aktuell — es gibt nichts zu schreiben.',
    'Kopia jest zaszyfrowana — podaj hasło użyte przy jej tworzeniu.':
        'Die Sicherung ist verschlüsselt — gib das Passwort ein, mit dem sie erstellt wurde.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją przywrócić.':
        'Die Sicherung ist verschlüsselt — gib das Passwort ein, um sie wiederherzustellen.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją zweryfikować.':
        'Die Sicherung ist verschlüsselt — gib das Passwort ein, um sie zu prüfen.',
    'Kopia jest zaszyfrowana — podaj hasło.':
        'Die Sicherung ist verschlüsselt — gib das Passwort ein.',
    'Kopia lustrzana':
        'Spiegelkopie',
    'Kopia nie została uruchomiona.':
        'Die Sicherung wurde nicht gestartet.',
    'Kopia wykonana. Uruchom podgląd ponownie, aby sprawdzić stan.':
        'Sicherung abgeschlossen. Starte die Vorschau erneut, um den Stand zu prüfen.',
    'Kopia zapasowa':
        'Sicherung',
    'Kopia {folder}':
        'Sicherung von {folder}',
    'Kopia {kind} • {count} {files} • {size} • ostatnia aktualizacja {when}\nŹródła: {roots}':
        'Sicherung, {kind} • {count} {files} • {size} • zuletzt aktualisiert {when}\nQuellen: {roots}',
    'Kopiowane są wyłącznie pliki nowe i zmienione od ostatniego przebiegu.':
        'Kopiert werden nur Dateien, die seit dem letzten Durchlauf neu sind oder sich geändert haben.',
    'Kopiuje ustawienia szablonu na ekran „Kopia zapasowa”':
        'Übernimmt die Einstellungen der Vorlage auf die Seite „Sicherung“',
    'Kopię możesz sprawdzić później: ekran „Przywracanie” → „Sprawdź kopię”. Najlepiej po ponownym podłączeniu dysku — wtedy dane są czytane z nośnika.':
        'Du kannst die Sicherung später prüfen: Seite „Wiederherstellung“ → „Sicherung prüfen“. Am besten nach erneutem Anschließen des Laufwerks — dann werden die Daten wirklich vom Datenträger gelesen.',
    'Kryptografia':
        'Kryptografie',
    'Lista podpowiadana przy tworzeniu nowej kopii.':
        'Die Liste, die beim Einrichten einer neuen Sicherung vorgeschlagen wird.',
    'Magazyn haseł: {backend}':
        'Passwortspeicher: {backend}',
    'Magazyn systemowy: {backend}':
        'Speicher des Systems: {backend}',
    'Menedżer poświadczeń Windows (DPAPI, powiązany z kontem użytkownika).':
        'Windows-Anmeldeinformationsverwaltung (DPAPI, an dein Benutzerkonto gebunden).',
    'Miejsce i układ odtwarzanych plików.':
        'Ort und Anordnung der wiederhergestellten Dateien.',
    'Motyw zmieniony na {theme}.':
        'Farbschema geändert: {theme}.',
    'Motyw:':
        'Farbschema:',
    'Możesz też przeciągnąć foldery z Eksploratora Windows wprost na listę.':
        'Du kannst Ordner auch aus dem Datei-Explorer direkt auf die Liste ziehen.',
    'Można ją dokończyć — zostaną dograne tylko brakujące i zmienione pliki.':
        'Sie lässt sich abschließen — nur fehlende und geänderte Dateien werden nachgetragen.',
    'Na nośniku docelowym zajmie to ok. {size}.':
        'Auf dem Zieldatenträger belegt das ca. {size}.',
    'Nadpisywanie plików':
        'Dateien überschreiben',
    'Nadpisz istniejące pliki':
        'Überschreiben',
    'Nazwa szablonu':
        'Name der Vorlage',
    'Nazwa szablonu nie może być pusta.':
        'Der Name der Vorlage darf nicht leer sein.',
    'Nazwa szablonu zapisana.':
        'Name der Vorlage gespeichert.',
    'Nazwa szablonu:':
        'Name der Vorlage:',
    'Nie ma wersji kopii o nazwie {name} w katalogu {path}.':
        'Im Ordner {path} gibt es keine Sicherungsversion namens {name}.',
    'Nie można odczytać informacji o dysku: {error}':
        'Die Laufwerksinformationen konnten nicht gelesen werden: {error}',
    'Nie udało się uruchomić programu — brakuje biblioteki: {error}\nZainstaluj zależności poleceniem:  pip install -r requirements.txt':
        'Das Programm konnte nicht starten — eine Bibliothek fehlt: {error}\nInstalliere die Abhängigkeiten mit:  pip install -r requirements.txt',
    'Nie udało się wykonać operacji':
        'Der Vorgang konnte nicht ausgeführt werden',
    'Nie udało się zapisać hasła w magazynie systemowym.\nSzablon działa normalnie — program poprosi o hasło przy uruchomieniu.':
        'Das Passwort konnte nicht im Passwortspeicher des Systems gespeichert werden.\nDie Vorlage funktioniert trotzdem — das Programm fragt bei jedem Durchlauf nach dem Passwort.',
    'Nie udało się znaleźć wolnej nazwy dla {path}':
        'Für {path} wurde kein freier Name gefunden',
    'Nie wskazano katalogu docelowego.':
        'Es wurde kein Zielordner angegeben.',
    'Nie wskazano żadnego katalogu źródłowego.':
        'Es wurde kein Quellordner angegeben.',
    'Nie wybrano katalogu':
        'Kein Ordner gewählt',
    'Nie wybrano szablonu':
        'Keine Vorlage gewählt',
    'Nie znaleziono spisu treści kopii — program przeskanuje folder i rozpozna pliki po ich zawartości.':
        'Kein Inhaltsverzeichnis der Sicherung gefunden — das Programm scannt den Ordner und erkennt die Dateien an ihrem Inhalt.',
    'Nie znam oryginalnej lokalizacji dla {key} — wybierz inny układ przywracania.':
        'Der ursprüngliche Speicherort von {key} ist unbekannt — wähle eine andere Anordnung für die Wiederherstellung.',
    'Niedostępny — backend {backend} nie gwarantuje poufności.':
        'Nicht verfügbar — das Backend {backend} garantiert keine Vertraulichkeit.',
    'Niedostępny — brak biblioteki keyring.':
        'Nicht verfügbar — die Bibliothek keyring fehlt.',
    'Nieznany algorytm wyprowadzania klucza: {name}':
        'Unbekanntes Verfahren zur Schlüsselableitung: {name}',
    'Nowa wersja z datą':
        'Neue datierte Version',
    'Nowa wersja z datą to kopia od początku do osobnego folderu':
        'Eine neue datierte Version ist eine Sicherung von Grund auf in einen eigenen Ordner',
    'Nowa wersja z datą — kopia do nowego folderu.\nWybrana istniejąca wersja — dogrywa do niej tylko brakujące i zmienione\npliki, a pliki różniące się od źródła nadpisuje. Tak dokończysz przerwaną\nkopię albo uzupełnisz ją o dane, które powstały w trakcie jej wykonywania.':
        'Neue datierte Version — Sicherung in einen neuen Ordner.\nEine gewählte vorhandene Version — nur fehlende und geänderte Dateien werden\nnachgetragen, von der Quelle abweichende Dateien überschrieben. So schließt du eine\nunterbrochene Sicherung ab oder ergänzt sie um Daten, die währenddessen entstanden sind.',
    'Nowy szablon':
        'Neue Vorlage',
    'Nośnik docelowy ({filesystem}) nie obsługuje twardych dowiązań, więc każda wersja z datą jest pełną kopią. Te {count} niezmienionych plików zostanie powielone ({size}). Rozważ układ „kopia lustrzana” albo nośnik NTFS.':
        'Der Zieldatenträger ({filesystem}) unterstützt keine Hardlinks, daher ist jede datierte Version eine vollständige Kopie. Unveränderte Dateien, die dupliziert werden: {count} ({size}). Erwäge den Aufbau „Spiegelkopie“ oder einen NTFS-Datenträger.',
    'O programie':
        'Über das Programm',
    'Obsługiwane są wzorce w stylu Windows:\n  *.tmp          — wszystkie pliki tymczasowe\n  Thumbs.db      — konkretna nazwa\n  node_modules/* — cały folder wraz z zawartością':
        'Unterstützt werden Muster im Windows-Stil:\n  *.tmp          — alle temporären Dateien\n  Thumbs.db      — ein bestimmter Name\n  node_modules/* — ein ganzer Ordner samt Inhalt',
    'Ochrona danych':
        'Datensicherheit',
    'Odczytuje wszystkie pliki kopii i weryfikuje ich poprawność.\nNic nie zapisuje na dysku.':
        'Liest alle Dateien der Sicherung und prüft, ob sie fehlerfrei sind.\nEs wird nichts auf das Laufwerk geschrieben.',
    'Odpowiednik synchronizacji folderu. Wcześniejsze wersje plików nie są zachowywane.':
        'Entspricht der Synchronisierung eines Ordners. Frühere Versionen von Dateien werden nicht aufbewahrt.',
    'Odtwarza pliki z kopii — również z kopii zaszyfrowanej.':
        'Stellt Dateien aus einer Sicherung wieder her — auch aus einer verschlüsselten.',
    'Odtwarza pliki zgodnie z ustawieniami powyżej':
        'Stellt die Dateien gemäß den Einstellungen oben wieder her',
    'Odtwórz pełną strukturę folderów':
        'Vollständige Ordnerstruktur wiederherstellen',
    'Odtwórz pliki z istniejącej kopii':
        'Dateien aus einer vorhandenen Sicherung wiederherstellen',
    'Operacja nie powiodła się.':
        'Der Vorgang ist fehlgeschlagen.',
    'Operacja przerwana przez użytkownika.':
        'Der Vorgang wurde vom Benutzer abgebrochen.',
    'Operacja przerwana — utrwalam stan dotychczas zapisanych plików.':
        'Vorgang abgebrochen — der Stand der bisher geschriebenen Dateien wird festgehalten.',
    'Operacja w toku':
        'Vorgang läuft',
    'Operacja zakończona błędem.':
        'Der Vorgang endete mit einem Fehler.',
    'Ostatnie operacje':
        'Letzte Vorgänge',
    'Otwiera ekran przywracania z wypełnionymi ścieżkami':
        'Öffnet die Wiederherstellungsseite mit ausgefüllten Pfaden',
    'Otwiera pełny dziennik w domyślnym edytorze':
        'Öffnet das vollständige Protokoll im Standard-Editor',
    'Otwórz katalog danych':
        'Datenordner öffnen',
    'Otwórz katalog dziennika':
        'Protokollordner öffnen',
    'Otwórz okno wyboru katalogu':
        'Ordnerauswahl öffnen',
    'Otwórz plik dziennika':
        'Protokolldatei öffnen',
    'PBKDF2-HMAC-SHA256 ({count} iteracji)':
        'PBKDF2-HMAC-SHA256 ({count} Iterationen)',
    'PBKDF2-HMAC-SHA256 — {count} iteracji':
        'PBKDF2-HMAC-SHA256 — {count} Iterationen',
    'PBKDF2-HMAC-SHA256, {count} iteracji':
        'PBKDF2-HMAC-SHA256, {count} Iterationen',
    'Pełna struktura — układ jak w źródle, wewnątrz wskazanego katalogu.\nJeden folder — wygodne, gdy szukasz kilku plików.\nPierwotne lokalizacje — zapisuje pliki tam, skąd zostały pobrane.':
        'Vollständige Struktur — Anordnung wie in der Quelle, im gewählten Ordner.\nEin Ordner — praktisch, wenn du nur ein paar Dateien suchst.\nUrsprüngliche Speicherorte — schreibt die Dateien dorthin zurück, woher sie stammen.',
    'Pierwszy przebieg kopiuje wszystko i trwa najdłużej. Kolejne porównują rozmiar i datę modyfikacji, więc zwykle kończą się w kilka sekund.':
        'Der erste Durchlauf kopiert alles und dauert am längsten. Weitere vergleichen Größe und Änderungsdatum und sind daher meist in wenigen Sekunden fertig.',
    'Plan gotowy: {count} {files} do zapisania.':
        'Plan fertig: {count} {files} zu schreiben.',
    'Plik jest za krótki, by być kontenerem tego programu.':
        'Die Datei ist zu kurz, um ein Container dieses Programms zu sein.',
    'Plik skończył się wcześniej, niż deklaruje nagłówek.':
        'Die Datei endet früher, als ihr Header angibt.',
    'Plik w formacie w wersji {found}; ta wersja programu obsługuje {supported}.':
        'Die Datei hat das Format in Version {found}; diese Programmversion unterstützt {supported}.',
    'Plik wymaga Argon2id, a biblioteka argon2-cffi jest niedostępna.':
        'Die Datei erfordert Argon2id, aber die Bibliothek argon2-cffi ist nicht verfügbar.',
    'Pliki pominięte — kopia jest aktualna':
        'Übersprungene Dateien — die Sicherung ist aktuell',
    'Pliki trafią do wskazanego katalogu z zachowaniem struktury folderów.':
        'Die Dateien kommen in den gewählten Ordner, die Ordnerstruktur bleibt erhalten.',
    'Pliki wrócą dokładnie tam, skąd pochodzą. Katalog docelowy zostanie zignorowany.':
        'Die Dateien kehren genau dorthin zurück, woher sie stammen. Der Zielordner wird ignoriert.',
    'Pliki zmienione od ostatniego przebiegu':
        'Seit dem letzten Durchlauf geänderte Dateien',
    'Pliki zostaną zapisane dokładnie tam, skąd pochodzą.\n\nKonflikty nazw: {collision}.\n\nCzy kontynuować?':
        'Die Dateien werden genau dorthin geschrieben, woher sie stammen.\n\nNamenskonflikte: {collision}.\n\nFortfahren?',
    'Pliki, których jeszcze nie ma w kopii':
        'Dateien, die noch nicht in der Sicherung sind',
    'Po uzupełnieniu istniejącej wersji jej katalog nazywa się np.\n  2026-09-17_@687--2026-09-24_@921\nczyli: data utworzenia kopii i data ostatniego uzupełnienia.\n\nData utworzenia zostaje z przodu, więc katalogi nadal układają się\nchronologicznie. Widać to w Eksploratorze bez uruchamiania programu.':
        'Nach dem Ergänzen einer vorhandenen Version heißt ihr Ordner z. B.\n  2026-09-17_@687--2026-09-24_@921\nalso: Erstellungsdatum der Sicherung und Datum der letzten Ergänzung.\n\nDas Erstellungsdatum bleibt vorne, daher sortieren sich die Ordner weiterhin\nchronologisch. Das siehst du im Datei-Explorer, ohne das Programm zu starten.',
    'Po wykonaniu kopii zostanie mało wolnego miejsca ({free}).':
        'Nach der Sicherung bleibt wenig freier Platz ({free}).',
    'Po zakończeniu kopii program ponownie skanuje źródło i dogrywa do tej samej\nwersji pliki, które w międzyczasie powstały lub się zmieniły.\nPrzydatne, gdy pracujesz na danych w trakcie wielogodzinnej kopii.\nPlik zmieniony w trakcie własnego kopiowania nigdy nie jest uznawany za zapisany.':
        'Nach der Sicherung scannt das Programm die Quelle erneut und trägt in dieselbe\nVersion Dateien nach, die inzwischen entstanden sind oder sich geändert haben.\nNützlich, wenn du während einer stundenlangen Sicherung mit den Daten arbeitest.\nEine Datei, die sich während ihres eigenen Kopierens ändert, gilt nie als geschrieben.',
    'Poczekaj na zakończenie bieżącej operacji.':
        'Warte, bis der laufende Vorgang abgeschlossen ist.',
    'Podaj hasło dla szablonu „{name}”:':
        'Gib das Passwort für die Vorlage „{name}“ ein:',
    'Podaj hasło — bez niego nie można zaszyfrować kopii.':
        'Gib ein Passwort ein — ohne Passwort lässt sich die Sicherung nicht verschlüsseln.',
    'Podane hasło nie pasuje do plików zapisanych wcześniej w tej kopii. Wznowienie z innym hasłem zostawiłoby w jednej kopii pliki pod dwoma hasłami. Podaj hasło użyte przy poprzednim przebiegu albo utwórz kopię w nowym katalogu.':
        'Das eingegebene Passwort passt nicht zu den Dateien, die zuvor in diese Sicherung geschrieben wurden. Ein Fortsetzen mit einem anderen Passwort hinterließe in einer Sicherung Dateien unter zwei Passwörtern. Gib das Passwort des vorherigen Durchlaufs ein oder lege die Sicherung in einem neuen Ordner an.',
    'Podgląd zmian':
        'Änderungsvorschau',
    'Pokazuje folder z plikami dziennika':
        'Zeigt den Ordner mit den Protokolldateien',
    'Pokazuje folder z ustawieniami i szablonami':
        'Zeigt den Ordner mit Einstellungen und Vorlagen',
    'Pokaż / ukryj wpisane hasło':
        'Eingegebenes Passwort anzeigen / verbergen',
    'Pomiń istniejące pliki':
        'Überspringen',
    'Potwierdź usuwanie':
        'Löschen bestätigen',
    'Powtórz hasło':
        'Passwort wiederholen',
    'Program nie mógł się uruchomić:\n\n{error}\n\nSzczegóły zapisano w dzienniku aplikacji.':
        'Das Programm konnte nicht starten:\n\n{error}\n\nDie Details wurden im Protokoll des Programms gespeichert.',
    'Program nie wie, czy ta kopia została dokończona. Uzupełnienie jej dogra tylko brakujące i zmienione pliki, a tego, co już jest zapisane, nie kopiuje ponownie.':
        'Das Programm weiß nicht, ob diese Sicherung abgeschlossen wurde. Beim Ergänzen werden nur fehlende und geänderte Dateien nachgetragen; was bereits geschrieben ist, wird nicht erneut kopiert.',
    'Program sam wykryje, czy kopia jest zaszyfrowana.':
        'Das Programm erkennt selbst, ob die Sicherung verschlüsselt ist.',
    'Przebieg operacji i diagnostyka':
        'Ablauf der Vorgänge und Diagnose',
    'Przebieg operacji na żywo. Pełna historia trafia do pliku.':
        'Der laufende Vorgang in Echtzeit. Der vollständige Verlauf wird in eine Datei geschrieben.',
    'Przebieg uzupełniający: {error}':
        'Nachsicherung: {error}',
    'Przeciętne':
        'Mittel',
    'Przerwano liczenie sumy kontrolnej.':
        'Berechnung der Prüfsumme abgebrochen.',
    'Przerwano skanowanie.':
        'Scan abgebrochen.',
    'Przerwano. Zapisano {count} {files} ({size}).':
        'Abgebrochen. {count} {files} geschrieben ({size}).',
    'Przerwij':
        'Abbrechen',
    'Przerywanie operacji…':
        'Vorgang wird abgebrochen…',
    'Przerywanie — zapisuję spis treści kopii, nie wyłączaj komputera…':
        'Abbruch — das Inhaltsverzeichnis der Sicherung wird geschrieben, schalte den Computer nicht aus…',
    'Przeskanowano {count} {files}.':
        '{count} {files} gescannt.',
    'Przygotowanie…':
        'Vorbereitung…',
    'Przywracanie':
        'Wiederherstellung',
    'Przywracanie do pierwotnych lokalizacji':
        'Wiederherstellung an den ursprünglichen Speicherorten',
    'Przywracanie przerwane.':
        'Wiederherstellung abgebrochen.',
    'Przywracanie {count} {files} ({size})…':
        'Wiederherstellung von {count} {files} ({size})…',
    'Przywróć do pierwotnych lokalizacji':
        'An den ursprünglichen Speicherorten wiederherstellen',
    'Przywróć domyślne':
        'Standard wiederherstellen',
    'Przywróć fabryczne':
        'Eingebaute Liste wiederherstellen',
    'Przywróć pliki':
        'Dateien wiederherstellen',
    'Przywróć z tej kopii':
        'Aus dieser Sicherung wiederherstellen',
    'Pusta nazwa':
        'Leerer Name',
    'Równoległe operacje:':
        'Parallele Vorgänge:',
    'Skanowanie plików źródłowych…':
        'Quelldateien werden gescannt…',
    'Skrót z dziennika — pełny zapis znajdziesz w zakładce „Dziennik”.':
        'Auszug aus dem Protokoll — die vollständige Aufzeichnung findest du auf der Seite „Protokoll“.',
    'Skąd przywracamy':
        'Woher wiederhergestellt wird',
    'Sprawdzam, co zmieniło się w źródle w trakcie kopii (przebieg uzupełniający {attempt} z {passes})…':
        'Es wird geprüft, was sich während der Sicherung in der Quelle geändert hat (Nachsicherung {attempt} von {passes})…',
    'Sprawdzam, czy hasło zgadza się z hasłem wcześniej zapisanych plików…':
        'Es wird geprüft, ob das Passwort zu den zuvor geschriebenen Dateien passt…',
    'Sprawdzam, czy w katalogu docelowym jest kopia do dokończenia…':
        'Es wird geprüft, ob im Zielordner eine unvollständige Sicherung liegt…',
    'Sprawdź hasło':
        'Passwort prüfen',
    'Sprawdź kopię':
        'Sicherung prüfen',
    'Szablon przechowuje foldery, opcje i wykluczenia. Hasło nigdy nie trafia do szablonu — jest przechowywane w Menedżerze poświadczeń Windows albo wpisywane przy każdym uruchomieniu.':
        'Eine Vorlage enthält Ordner, Optionen und Ausschlüsse. Das Passwort kommt nie in die Vorlage — es liegt in der Windows-Anmeldeinformationsverwaltung oder wird bei jedem Durchlauf eingegeben.',
    'Szablon usunięty.':
        'Vorlage gelöscht.',
    'Szablon „{name}”':
        'Vorlage „{name}“',
    'Szablon „{name}” już istnieje.\n\nZastąpić go bieżącymi ustawieniami z formularza?':
        'Die Vorlage „{name}“ existiert bereits.\n\nMit den aktuellen Einstellungen aus dem Formular ersetzen?',
    'Szablon „{name}” zostanie usunięty.\n\nPliki kopii zapasowej pozostaną nienaruszone.':
        'Die Vorlage „{name}“ wird gelöscht.\n\nDie Sicherungsdateien bleiben unangetastet.',
    'Szablony':
        'Vorlagen',
    'Szablony: {count}\nSzyfrowanie: AES-256-GCM\nKlucz: {kdf}':
        'Vorlagen: {count}\nVerschlüsselung: AES-256-GCM\nSchlüssel: {kdf}',
    'Szyfrowanie i kontrola poprawności zapisu.':
        'Verschlüsselung und Prüfung der geschriebenen Daten.',
    'Szyfrowanie: AES-256-GCM (uwierzytelnione)\nWyprowadzanie klucza: {kdf}':
        'Verschlüsselung: AES-256-GCM (authentifiziert)\nSchlüsselableitung: {kdf}',
    'Szyfruj kopię (AES-256-GCM)':
        'Sicherung verschlüsseln (AES-256-GCM)',
    'Słabe':
        'Schwach',
    'Ta kopia nie jest zaszyfrowana — hasło nie jest potrzebne.':
        'Diese Sicherung ist nicht verschlüsselt — es wird kein Passwort benötigt.',
    'Ten folder jest już na liście.':
        'Dieser Ordner steht bereits in der Liste.',
    'To nie jest plik zaszyfrowany przez ten program.':
        'Diese Datei wurde nicht von diesem Programm verschlüsselt.',
    'Trwa inna operacja — poczekaj na jej zakończenie.':
        'Ein anderer Vorgang läuft — warte, bis er abgeschlossen ist.',
    'Trwa operacja':
        'Vorgang läuft',
    'Trwa operacja na plikach. Zamknięcie programu ją przerwie.\n\nPliki zapisane do tej chwili zostaną zachowane, a kopię będzie można później dokończyć.\n\nZamknąć mimo to?':
        'Ein Dateivorgang läuft. Wenn du das Programm schließt, wird er abgebrochen.\n\nDie bis jetzt geschriebenen Dateien bleiben erhalten, und die Sicherung lässt sich später abschließen.\n\nTrotzdem schließen?',
    'Trwa: {description}…':
        'Läuft: {description}…',
    'Tryb dokładny — licz sumę kontrolną każdego pliku':
        'Gründlicher Modus — Prüfsumme jeder Datei berechnen',
    'Układ kopii':
        'Aufbau der Sicherung',
    'Układ plików:':
        'Anordnung der Dateien:',
    'Uruchom kopię':
        'Sicherung starten',
    'Ustawienia':
        'Einstellungen',
    'Usunąć szablon?':
        'Vorlage löschen?',
    'Usuwa pozycję z listy. Nie kasuje żadnych plików.':
        'Entfernt den Eintrag aus der Liste. Es werden keine Dateien gelöscht.',
    'Usuwa szablon. Nie kasuje żadnych plików kopii.':
        'Löscht die Vorlage. Es werden keine Sicherungsdateien gelöscht.',
    'Usuwaj z kopii pliki skasowane w źródle':
        'In der Quelle gelöschte Dateien aus der Sicherung entfernen',
    'Usuń':
        'Löschen',
    'Usuń zaznaczone':
        'Ausgewählte entfernen',
    'Uszkodzony nagłówek pliku.':
        'Der Header der Datei ist beschädigt.',
    'Utwórz lub zaktualizuj kopię wybranych folderów':
        'Sicherung ausgewählter Ordner erstellen oder aktualisieren',
    'Utwórz nową wersję':
        'Neue Version erstellen',
    'Uzupełnienie istniejącej wersji nie kopiuje ponownie tego, co już w niej jest — dokończysz przerwaną kopię bez tworzenia kolejnej pełnej wersji.':
        'Das Ergänzen einer vorhandenen Version kopiert nicht erneut, was schon darin ist — so schließt du eine unterbrochene Sicherung ab, ohne eine weitere vollständige Version anzulegen.',
    'Uzupełnij tę wersję':
        'Diese Version ergänzen',
    'Uzupełnij: {version} • {labels}':
        'Ergänzen: {version} • {labels}',
    'W katalogu docelowym jest kopia tych samych folderów zapisana starszą wersją programu:':
        'Im Zielordner liegt eine Sicherung derselben Ordner, die mit einer älteren Programmversion geschrieben wurde:',
    'W katalogu docelowym jest niedokończona kopia tych samych folderów:':
        'Im Zielordner liegt eine unvollständige Sicherung derselben Ordner:',
    'W tym katalogu nie ma spisu treści kopii — nie ma z czym porównać plików.':
        'In diesem Ordner gibt es kein Inhaltsverzeichnis der Sicherung — es gibt nichts, womit sich die Dateien vergleichen ließen.',
    'Wczytaj do formularza':
        'Ins Formular laden',
    'Wczytano manifest kopii: {count} {files}.':
        'Manifest der Sicherung geladen: {count} {files}.',
    'Wczytano szablon „{name}” do formularza.':
        'Vorlage „{name}“ ins Formular geladen.',
    'Wersja kopii nosi teraz nazwę {name}.':
        'Die Sicherungsversion heißt jetzt {name}.',
    'Wersja, licencja i użyta kryptografia':
        'Version, Lizenz und verwendete Kryptografie',
    'Wersje z datą (zalecane)':
        'Datierte Versionen (empfohlen)',
    'Weryfikacja kopii':
        'Prüfung der Sicherung',
    'Weryfikacja nie powiodła się: nieprawidłowe hasło lub uszkodzony plik.':
        'Prüfung fehlgeschlagen: falsches Passwort oder beschädigte Datei.',
    'Weryfikacja po zapisie nie powiodła się — zapisane dane różnią się od źródła.':
        'Die Prüfung nach dem Schreiben ist fehlgeschlagen — die geschriebenen Daten weichen von der Quelle ab.',
    'Weryfikacja {count} {files} ({size}), {threads} równolegle…':
        'Prüfung von {count} {files} ({size}), {threads} parallel…',
    'Weryfikuj natychmiast po zapisie (spowalnia kopię)':
        'Sofort nach dem Schreiben prüfen (verlangsamt die Sicherung)',
    'Wolne miejsce: {free} z {total}':
        'Freier Platz: {free} von {total}',
    'Wolniejszy, ale wykrywa zmiany, które nie zmieniły rozmiaru ani daty\n(np. po przywróceniu pliku z innego nośnika).':
        'Langsamer, erkennt aber Änderungen, die weder Größe noch Datum verändert haben\n(z. B. nachdem eine Datei von einem anderen Datenträger wiederhergestellt wurde).',
    'Wpis {key} w spisie treści kopii wskazuje poza katalog docelowy — pomijam go.':
        'Der Eintrag {key} im Inhaltsverzeichnis der Sicherung zeigt aus dem Zielordner hinaus — er wird übersprungen.',
    'Wraca do listy wbudowanej w program':
        'Kehrt zur im Programm eingebauten Liste zurück',
    'Wskaż folder kopii, aby zobaczyć jej zawartość.':
        'Wähle den Sicherungsordner, um den Inhalt der Sicherung zu sehen.',
    'Wskaż folder kopii.':
        'Wähle den Sicherungsordner.',
    'Wskaż foldery objęte kopią. Podfoldery są uwzględniane automatycznie.':
        'Wähle die Ordner, die gesichert werden sollen. Unterordner werden automatisch einbezogen.',
    'Wskaż główny folder kopii (ten, który wybrałeś jako cel), a nie pojedynczy folder z datą. Program sam odczyta spis treści kopii.':
        'Wähle den Hauptordner der Sicherung (den du als Ziel gewählt hast), nicht einen einzelnen datierten Ordner. Das Programm liest das Inhaltsverzeichnis der Sicherung selbst.',
    'Wskaż katalog docelowy kopii.':
        'Wähle den Zielordner der Sicherung.',
    'Wskaż katalog docelowy.':
        'Wähle den Zielordner.',
    'Wstawia zalecaną listę wykluczeń':
        'Fügt die empfohlene Liste von Ausschlüssen ein',
    'Wszystkie pliki wylądują bezpośrednio w katalogu docelowym, bez podfolderów.':
        'Alle Dateien landen direkt im Zielordner, ohne Unterordner.',
    'Wszystko do jednego folderu':
        'Alles in einen Ordner',
    'Wybierz folder do kopii':
        'Ordner zum Sichern wählen',
    'Wybierz folder kopii':
        'Sicherungsordner wählen',
    'Wybierz katalog':
        'Ordner wählen',
    'Wybierz katalog docelowy':
        'Zielordner wählen',
    'Wybierz katalog docelowy kopii':
        'Zielordner der Sicherung wählen',
    'Wybierz katalog, aby zobaczyć dostępne miejsce.':
        'Wähle einen Ordner, um den verfügbaren Platz zu sehen.',
    'Wybierz kolejny folder do kopii':
        'Weiteren Ordner zum Sichern wählen',
    'Wybierz szablon z listy.':
        'Wähle eine Vorlage aus der Liste.',
    'Wybierz…':
        'Wählen…',
    'Wybrano nadpisywanie istniejących plików. Ich obecna zawartość zostanie bezpowrotnie zastąpiona.\n\nCzy kontynuować?':
        'Du hast das Überschreiben vorhandener Dateien gewählt. Ihr jetziger Inhalt wird unwiderruflich ersetzt.\n\nFortfahren?',
    'Wyczyść widok':
        'Ansicht leeren',
    'Wygląd':
        'Darstellung',
    'Wygląd, wykluczenia domyślne i informacje o środowisku.':
        'Darstellung, Standard-Ausschlüsse und Angaben zur Umgebung.',
    'Wygląd, wykluczenia i magazyn haseł':
        'Darstellung, Ausschlüsse und Passwortspeicher',
    'Wykluczenia':
        'Ausschlüsse',
    'Wykonuje kopię według tego szablonu':
        'Führt die Sicherung nach dieser Vorlage aus',
    'Wykonuje kopię zgodnie z powyższymi ustawieniami':
        'Führt die Sicherung mit den Einstellungen oben aus',
    'Wymagane wyłącznie dla kopii zaszyfrowanych.':
        'Nur für verschlüsselte Sicherungen erforderlich.',
    'Wzorce plików i folderów pomijanych w kopii — po jednym w wierszu.':
        'Muster für Dateien und Ordner, die nicht gesichert werden — eines pro Zeile.',
    'Włączono szyfrowanie, ale nie podano hasła.':
        'Die Verschlüsselung ist eingeschaltet, aber es wurde kein Passwort angegeben.',
    'Włączono usuwanie z kopii plików skasowanych w źródle.\n\nPliki usunięte w źródle stracą swoją jedyną kopię zapasową. Czy na pewno kontynuować?':
        'Das Entfernen von in der Quelle gelöschten Dateien aus der Sicherung ist eingeschaltet.\n\nIn der Quelle gelöschte Dateien verlieren ihre einzige Sicherungskopie. Wirklich fortfahren?',
    'Za mało miejsca w katalogu docelowym. Potrzeba ok. {needed}, dostępne {free}.':
        'Nicht genug Platz im Zielordner. Benötigt werden ca. {needed}, verfügbar sind {free}.',
    'Zabezpieczenie przed literówką — hasła nie da się odzyskać.':
        'Schutz vor Tippfehlern — das Passwort lässt sich nicht wiederherstellen.',
    'Zachowaj oba — dopisz numer do nazwy':
        'Beide behalten — durchnummerieren',
    'Zakończono z błędami ({errors}). Zapisano {count} {files}.':
        'Mit Fehlern beendet ({errors}). {count} {files} geschrieben.',
    'Zakończono.':
        'Abgeschlossen.',
    'Zapamiętaj hasło w Menedżerze poświadczeń Windows':
        'Passwort in der Windows-Anmeldeinformationsverwaltung speichern',
    'Zapamiętuje te ustawienia do ponownego użycia':
        'Speichert diese Einstellungen zur erneuten Verwendung',
    'Zapis bieżącej sesji':
        'Aufzeichnung der aktuellen Sitzung',
    'Zapisane konfiguracje do ponownego użycia':
        'Gespeicherte Konfigurationen zur erneuten Verwendung',
    'Zapisane konfiguracje — uruchamiasz je jednym kliknięciem.':
        'Gespeicherte Konfigurationen — du startest sie mit einem Klick.',
    'Zapisane szablony':
        'Gespeicherte Vorlagen',
    'Zapisano szablon „{name}”.':
        'Vorlage „{name}“ gespeichert.',
    'Zapisuje listę jako domyślną':
        'Speichert die Liste als Standard',
    'Zapisuje nową nazwę szablonu':
        'Speichert den neuen Namen der Vorlage',
    'Zapisywanie {count} {files} ({size}), {workers} równolegle':
        'Schreiben von {count} {files} ({size}), {workers} parallel',
    'Zapisz':
        'Speichern',
    'Zapisz do:':
        'Schreiben in:',
    'Zapisz jako szablon':
        'Als Vorlage speichern',
    'Zapisz nazwę':
        'Namen speichern',
    'Zapisz szablon':
        'Vorlage speichern',
    'Zastąpić szablon?':
        'Vorlage ersetzen?',
    'Zatrzymuje operację. Pliki już zapisane pozostają nienaruszone.':
        'Bricht den Vorgang ab. Bereits geschriebene Dateien bleiben unangetastet.',
    'Zaznacz szablon na liście.':
        'Markiere eine Vorlage in der Liste.',
    'Zmiana języka przebudowuje okno; wypełnione ścieżki zostają.':
        'Ein Sprachwechsel baut das Fenster neu auf; eingetragene Pfade bleiben erhalten.',
    'Zmiana motywu działa natychmiast.':
        'Das Farbschema ändert sich sofort.',
    'Zmienia kolor przycisków i zaznaczeń':
        'Ändert die Farbe von Schaltflächen und Markierungen',
    'Zmień nazwę, aby łatwiej rozpoznawać szablon.':
        'Gib der Vorlage einen Namen, an dem du sie leicht erkennst.',
    'Znaleziono {count} {files}. Porównuję z poprzednią kopią…':
        '{count} {files} gefunden. Vergleich mit der vorherigen Sicherung…',
    'automatycznie':
        'automatisch',
    'bez zmian':
        'unverändert',
    'brak (biblioteka keyring niezainstalowana)':
        'keiner (Bibliothek keyring nicht installiert)',
    'brak danych':
        'keine Angaben',
    'brak pliku w kopii':
        'Datei fehlt in der Sicherung',
    'do zapisania':
        'zu schreiben',
    'istniejąca kopia: {count} {files}, ostatnio {when}':
        'vorhandene Sicherung: {count} {files}, zuletzt {when}',
    'jeszcze nie uruchamiany':
        'noch nie ausgeführt',
    'kompletna':
        'vollständig',
    'kopia lustrzana':
        'Spiegelkopie',
    'kopia zapasowa':
        'Sicherung',
    'nie':
        'nein',
    'niedokończona':
        'unvollständig',
    'niedokończona — brakuje ok. {count} {files} ({size})':
        'unvollständig — fehlend: ca. {count} {files} ({size})',
    'niezaszyfrowana':
        'unverschlüsselt',
    'nieznany format manifestu':
        'unbekanntes Manifestformat',
    'nowych plików':
        'neue Dateien',
    'np. C:\\Odzyskane':
        'z. B. C:\\Wiederhergestellt',
    'np. E:\\Kopie zapasowe':
        'z. B. E:\\Sicherungen',
    'plik':
        'Datei',
    'plik stanu jest za krótki':
        'die Statusdatei ist zu kurz',
    'plik stanu w wersji {found}, obsługiwana: {supported}':
        'Statusdatei in Version {found}, unterstützt: {supported}',
    'pliki':
        'Dateien',
    'plików':
        'Dateien',
    'podgląd kopii':
        'Sicherungsvorschau',
    'pozostaną w kopii':
        'sie bleiben in der Sicherung',
    'rozmiar w kopii {actual} B zamiast {expected} B':
        'Größe in der Sicherung {actual} B statt {expected} B',
    'sprawdzanie kopii':
        'Prüfung der Sicherung',
    'stan nieznany (zapisana starszą wersją programu)':
        'Status unbekannt (mit einer älteren Programmversion geschrieben)',
    'suma kontrolna manifestu się nie zgadza':
        'die Prüfsumme des Manifests stimmt nicht',
    'suma kontrolna się nie zgadza — plik uszkodzony':
        'die Prüfsumme stimmt nicht — die Datei ist beschädigt',
    'szablon {name}':
        'Vorlage {name}',
    'tak':
        'ja',
    'ten system plików':
        'dieses Dateisystem',
    'wersja {version}':
        'Version {version}',
    'wersje z datą':
        'datierte Versionen',
    'weryfikacja':
        'Prüfung',
    'wyłączona':
        'aus',
    'zaszyfrowana (AES-256-GCM)':
        'verschlüsselt (AES-256-GCM)',
    'zawartość różni się od pliku źródłowego':
        'der Inhalt weicht von der Quelldatei ab',
    'zawartość różni się od sumy kontrolnej zapisanej podczas kopii':
        'der Inhalt weicht von der bei der Sicherung gespeicherten Prüfsumme ab',
    'zmienionych':
        'geändert',
    'zostaną usunięte z kopii':
        'sie werden aus der Sicherung entfernt',
    '{done} z {total} • {speed}/s{eta}':
        '{done} von {total} • {speed}/s{eta}',
    '{done} • {speed}/s':
        '{done} • {speed}/s',
    '{hours} h {minutes} min':
        '{hours} h {minutes} min',
    '{label}: {count} {files}':
        '{label}: {count} {files}',
    '{message}\n\nSzczegóły techniczne znajdziesz w zakładce „Dziennik”.':
        '{message}\n\nTechnische Details findest du auf der Seite „Protokoll“.',
    '{minutes} min {seconds} s':
        '{minutes} min {seconds} s',
    '{name}: nie można odczytać ({error})':
        '{name}: kann nicht gelesen werden ({error})',
    '{seconds} s':
        '{seconds} s',
    '{summary}\n\nProblemy:\n{problems}\n\nPełna lista znajduje się w zakładce „Dziennik”.':
        '{summary}\n\nProbleme:\n{problems}\n\nDie vollständige Liste findest du auf der Seite „Protokoll“.',
    '{summary}{notes}\n\nPliki zapisane przed przerwaniem są kompletne i zostały odnotowane w spisie treści kopii.\n\nAby dokończyć kopię, uruchom ją ponownie — program zaproponuje uzupełnienie tej wersji zamiast tworzenia nowej.':
        '{summary}{notes}\n\nDie vor dem Abbruch geschriebenen Dateien sind vollständig und im Inhaltsverzeichnis der Sicherung erfasst.\n\nUm die Sicherung abzuschließen, starte sie erneut — das Programm schlägt dann vor, diese Version zu ergänzen, statt eine neue anzulegen.',
    '{title} — gotowe':
        '{title} — fertig',
    '{title} — przerwano':
        '{title} — abgebrochen',
    '{title} — zakończono z błędami':
        '{title} — mit Fehlern beendet',
    '{when}  •  {action}  •  {count} {files}':
        '{when}  •  {action}  •  {count} {files}',
    'Łączny rozmiar danych do przesłania':
        'Gesamtgröße der zu übertragenden Daten',
    'Środowisko':
        'Umgebung',
    'Źródła: {sources}\nCel: {destination}\nUkład: {structure} • Szyfrowanie: {encrypt} • Weryfikacja: {verify} • Dogrywka: {catchup} • Równolegle: {workers} • Data uzupełnienia w nazwie: {stamp}\nUtworzony: {created} • Ostatni przebieg: {last}':
        'Quellen: {sources}\nZiel: {destination}\nAufbau: {structure} • Verschlüsselung: {encrypt} • Prüfung: {verify} • Nachsicherung: {catchup} • Parallel: {workers} • Ergänzungsdatum im Namen: {stamp}\nErstellt: {created} • Letzter Durchlauf: {last}',
    'Źródło nie zmieniło się w trakcie kopii — nie ma czego uzupełniać.':
        'Die Quelle hat sich während der Sicherung nicht geändert — es gibt nichts nachzusichern.',
    '—':
        '—',
    '• Kopia przyrostowa — zapisywane są wyłącznie pliki nowe i zmienione.\n  Porównanie opiera się na spisie treści kopii, rozmiarze i dacie modyfikacji;\n  przy różnicy liczona jest suma kontrolna SHA-256.\n\n• Wersje z datą — każdy przebieg tworzy kompletny folder z datą, a pliki\n  niezmienione są podpinane twardym dowiązaniem, więc nie zajmują miejsca dwa razy.\n\n• Weryfikacja po zapisie — zapisany plik jest odczytywany z powrotem\n  i porównywany ze źródłem.\n\n• Odporność na przerwania — pliki powstają pod nazwą tymczasową i są\n  podmieniane dopiero po pełnym zapisie.':
        '• Inkrementelle Sicherung — geschrieben werden nur neue und geänderte Dateien.\n  Der Vergleich stützt sich auf das Inhaltsverzeichnis der Sicherung, Größe und Änderungsdatum;\n  bei Abweichungen wird eine SHA-256-Prüfsumme berechnet.\n\n• Datierte Versionen — jeder Durchlauf legt einen vollständigen datierten Ordner an, und unveränderte\n  Dateien werden per Hardlink eingebunden, sodass sie nie doppelt Platz belegen.\n\n• Prüfung nach dem Schreiben — die geschriebene Datei wird zurückgelesen\n  und mit der Quelle verglichen.\n\n• Robust bei Unterbrechungen — Dateien entstehen unter einem temporären Namen und\n  ersetzen das Original erst, wenn sie vollständig geschrieben sind.',
    '• Szyfr: AES-256 w trybie GCM (szyfrowanie z uwierzytelnieniem).\n• Wyprowadzanie klucza z hasła: {kdf}.\n• Nagłówek każdego pliku jest uwierzytelniony jako AAD — podmiana parametrów\n  unieważnia tag.\n• Każdy plik dostaje losowy, niepowtarzalny nonce.\n• Odszyfrowany plik powstaje dopiero po pomyślnej weryfikacji tagu.\n• Hasła nie są zapisywane w plikach programu. Opcjonalnie trafiają do\n  Menedżera poświadczeń Windows.':
        '• Chiffre: AES-256 im GCM-Modus (authentifizierte Verschlüsselung).\n• Schlüsselableitung aus dem Passwort: {kdf}.\n• Der Header jeder Datei ist als AAD authentifiziert — eine Änderung der Parameter\n  macht das Authentifizierungs-Tag ungültig.\n• Jede Datei erhält eine zufällige, einmalige Nonce.\n• Eine entschlüsselte Datei entsteht erst nach erfolgreicher Prüfung des Authentifizierungs-Tags.\n• Passwörter werden nicht in den Dateien des Programms gespeichert. Optional kommen sie in die\n  Windows-Anmeldeinformationsverwaltung.',
    'Bez hasła nie da się odczytać ani jednego pliku z kopii.':
        'Ohne das Passwort lässt sich keine einzige Datei der Sicherung lesen.',
    'Co chcesz chronić?':
        'Was möchtest du schützen?',
    'Co chcesz teraz zrobić?':
        'Was möchtest du jetzt tun?',
    'Czyta kopię z nośnika i porównuje ją z zapisanymi sumami kontrolnymi.':
        'Liest die Sicherung vom Datenträger und vergleicht sie mit den gespeicherten Prüfsummen.',
    'Dalej':
        'Weiter',
    'Dokumenty i zdjęcia':
        'Dokumente und Fotos',
    'Ekran powitalny wrócisz w ustawieniach, gdy zmienisz zdanie.':
        'Den Willkommensbildschirm kannst du in den Einstellungen zurückholen, falls du es dir anders überlegst.',
    'Ekran z pytaniem, co chcesz teraz zrobić: kopia, przywracanie, sprawdzenie.':
        'Ein Bildschirm mit der Frage, was du jetzt tun möchtest: sichern, wiederherstellen oder prüfen.',
    'Foldery objęte kopią':
        'Zu sichernde Ordner',
    'Foldery z pracą. Kreator pominie katalogi, które odtwarza się jednym poleceniem (node_modules, venv, build).':
        'Ordner mit deiner Arbeit. Der Assistent lässt Ordner aus, die sich mit einem einzigen Befehl neu erzeugen lassen (node_modules, venv, build).',
    'Gdzie zapisać kopię?':
        'Wohin soll die Sicherung?',
    'Historia i szyfrowanie':
        'Verlauf und Verschlüsselung',
    'Historia zmian (zalecane)':
        'Änderungsverlauf (empfohlen)',
    'Jak bardzo chcesz się zabezpieczyć?':
        'Wie gut möchtest du dich absichern?',
    'Jak wyżej, a dodatkowo każdy plik trafia do kopii zaszyfrowany (AES-256-GCM). Potrzebne przy kopii wożonej poza dom.':
        'Wie oben, zusätzlich wird jede Datei verschlüsselt in der Sicherung abgelegt (AES-256-GCM). Sinnvoll für eine Sicherung, die das Haus verlässt.',
    'Jedna aktualna kopia':
        'Eine aktuelle Kopie',
    'Język, motyw, domyślne wykluczenia i informacje o środowisku.':
        'Sprache, Farbschema, Standard-Ausschlüsse und Angaben zur Umgebung.',
    'Katalog docelowy leży wewnątrz źródła — wybierz inny.':
        'Der Zielordner liegt innerhalb der Quelle — wähle einen anderen.',
    'Każdy przebieg tworzy folder z datą. Pliki niezmienione są podpinane dowiązaniem, więc historia kosztuje tyle, ile realnie się zmieniło.':
        'Jeder Durchlauf legt einen datierten Ordner an. Unveränderte Dateien werden verknüpft, daher kostet der Verlauf nur so viel, wie sich tatsächlich geändert hat.',
    'Każdy przebieg utworzy folder z datą. Pierwszy zajmie tyle, ile dane; kolejne — tyle, ile realnie się zmieniło.':
        'Jeder Durchlauf legt einen datierten Ordner an. Der erste belegt so viel wie die Daten, die weiteren nur so viel, wie sich tatsächlich geändert hat.',
    'Kopia powstanie w: {path}':
        'Die Sicherung entsteht in: {path}',
    'Kopia trafi do: {path}':
        'Ziel der Sicherung: {path}',
    'Kopia: {what}':
        'Sicherung: {what}',
    'Krok {number} z {total}':
        'Schritt {number} von {total}',
    'Najlepiej na innym dysku fizycznym niż ten, który chronisz — kopia obok oryginału ginie razem z nim.':
        'Am besten auf einem anderen physischen Laufwerk als dem, das du schützt — eine Sicherung neben dem Original geht mit ihm verloren.',
    'Najszybsza i najmniejsza. Kopia odpowiada temu, co masz teraz — bez historii wcześniejszych wersji.':
        'Am schnellsten und kleinsten. Die Sicherung entspricht dem, was du jetzt hast — ohne Verlauf früherer Versionen.',
    'Nie było jeszcze żadnej kopii. Zacznij od „Zrób kopię”.':
        'Es gab noch keine Sicherung. Beginne mit „Jetzt sichern“.',
    'Nie lista ustawień, tylko ich skutki.':
        'Keine Liste von Einstellungen, sondern was sie bewirken.',
    'Nie pokazuj tego ekranu przy starcie':
        'Diesen Bildschirm beim Start nicht anzeigen',
    'Nośnik docelowy':
        'Zieldatenträger',
    'Odtwarza pliki z kopii — całość albo wybrany folder.':
        'Stellt Dateien aus einer Sicherung wieder her — alles oder einen gewählten Ordner.',
    'Odśwież listę':
        'Liste aktualisieren',
    'Ostatnia kopia: {when} • {count} {files}.':
        'Letzte Sicherung: {when} • {count} {files}.',
    'Pierwszy przebieg jest najdłuższy — kolejne porównują rozmiar i datę modyfikacji, więc zwykle trwają sekundy.':
        'Der erste Durchlauf dauert am längsten — weitere vergleichen Größe und Änderungsdatum und dauern daher meist nur Sekunden.',
    'Pliki w kopii będą zaszyfrowane; bez hasła nie da się ich odczytać.':
        'Die Dateien in der Sicherung werden verschlüsselt; ohne das Passwort lassen sie sich nicht lesen.',
    'Podfoldery są uwzględniane automatycznie.':
        'Unterordner werden automatisch einbezogen.',
    'Pokazuj ekran powitalny przy starcie':
        'Willkommensbildschirm beim Start anzeigen',
    'Ponownie sprawdza podłączone nośniki':
        'Prüft die angeschlossenen Laufwerke erneut',
    'Program będzie utrzymywał jeden folder zgodny ze źródłem. Każdy kolejny przebieg dopisze tylko to, co się zmieniło.':
        'Das Programm hält einen Ordner mit der Quelle abgeglichen. Jeder weitere Durchlauf schreibt nur, was sich geändert hat.',
    'Projekty i kod':
        'Projekte und Code',
    'Przechodzi do następnego kroku':
        'Geht zum nächsten Schritt',
    'Przechodzi do pełnego okna programu':
        'Wechselt zum vollständigen Programmfenster',
    'Sam wskażesz, co ma trafić do kopii.':
        'Du legst selbst fest, was in die Sicherung kommt.',
    'System plików: {filesystem}, klaster {cluster}':
        'Dateisystem: {filesystem}, Cluster {cluster}',
    'Ten katalog leży wewnątrz folderu źródłowego — wybierz inny.':
        'Dieser Ordner liegt innerhalb eines Quellordners — wähle einen anderen.',
    'Ten nośnik nie obsługuje twardych dowiązań, więc każda wersja z datą zajmie tyle miejsca co pełna kopia. Przy tym nośniku rozważ „jedną aktualną kopię”.':
        'Dieser Datenträger unterstützt keine Hardlinks, daher belegt jede datierte Version so viel Platz wie eine vollständige Kopie. Erwäge bei diesem Datenträger „Eine aktuelle Kopie“.',
    'To dysk systemowy — kopia nie przetrwa jego awarii. Jeśli masz drugi dysk albo pendrive, wybierz jego.':
        'Das ist das Systemlaufwerk — die Sicherung übersteht seinen Ausfall nicht. Wenn du ein zweites Laufwerk oder einen USB-Stick hast, wähle lieber diesen Datenträger.',
    'To się wydarzy':
        'Das wird passieren',
    'Trzy gotowe zestawy zamiast kilkunastu przełączników.':
        'Drei fertige Varianten statt Dutzender Schalter.',
    'Twoje pliki osobiste z folderów użytkownika. Najczęstszy wybór.':
        'Deine persönlichen Dateien aus deinen Benutzerordnern. Die häufigste Wahl.',
    'Uruchamia kreator, który ustawi kopię krok po kroku':
        'Startet den Assistenten, der die Sicherung Schritt für Schritt einrichtet',
    'Uruchom kreator…':
        'Assistent starten…',
    'Ustawia kopię krok po kroku i zapisuje ją jako szablon':
        'Richtet die Sicherung Schritt für Schritt ein und speichert sie als Vorlage',
    'Ustawienia pierwszej kopii':
        'Erste Sicherung einrichten',
    'Ustawienia pierwszej kopii…':
        'Erste Sicherung einrichten…',
    'W tym katalogu jest już kopia ({count} {files}) — program ją uzupełni, a nie nadpisze.':
        'In diesem Ordner liegt bereits eine Sicherung ({count} {files}) — das Programm ergänzt sie, statt sie zu überschreiben.',
    'Wraca do poprzedniego kroku':
        'Geht zum vorherigen Schritt zurück',
    'Wskaż dowolny katalog docelowy':
        'Beliebigen Zielordner wählen',
    'Wskaż folder kopii i kliknij „Sprawdź kopię”.':
        'Wähle den Sicherungsordner und klicke auf „Sicherung prüfen“.',
    'Wstecz':
        'Zurück',
    'Wybierz':
        'Auswählen',
    'Wybierz inny folder…':
        'Anderen Ordner wählen…',
    'Wybierz to, co najbliższe. Dokładną listę folderów poprawisz niżej.':
        'Wähle, was am ehesten passt. Die genaue Ordnerliste kannst du unten anpassen.',
    'Wybrane foldery':
        'Ausgewählte Ordner',
    'Zamknij':
        'Schließen',
    'Zamyka kreator bez zapisywania':
        'Schließt den Assistenten, ohne zu speichern',
    'Zapisuje nowe i zmienione pliki. Pierwszy raz trwa najdłużej.':
        'Schreibt neue und geänderte Dateien. Das erste Mal dauert am längsten.',
    'Zapisuje szablon bez uruchamiania kopii':
        'Speichert die Vorlage, ohne die Sicherung zu starten',
    'Zapisuje szablon i od razu uruchamia kopię':
        'Speichert die Vorlage und startet sofort die Sicherung',
    'Zapisz i zrób kopię':
        'Speichern und jetzt sichern',
    'Zapisz ustawienia':
        'Einstellungen speichern',
    'Zrób kopię':
        'Jetzt sichern',
    'dysk systemowy':
        'Systemlaufwerk',
    'wolne {free} z {total}':
        '{free} von {total} frei',
    'Porównano ze źródłem: {source}; tylko z sumą kontrolną (źródło zmieniło się albo jest niedostępne): {checksum}.':
        'Mit der Quelle verglichen: {source}; nur mit der Prüfsumme (Quelle geändert oder nicht verfügbar): {checksum}.',
    'Przywraca losową próbkę plików do katalogu tymczasowego i porównuje je ze źródłem.\nSprawdza całą drogę odzyskiwania, a trwa minuty. Nic nie zostaje na dysku.':
        'Stellt eine zufällige Stichprobe von Dateien in einem temporären Ordner wieder her und vergleicht sie mit der Quelle.\nPrüft den gesamten Wiederherstellungsweg und dauert nur Minuten. Auf dem Laufwerk bleibt nichts zurück.',
    'Próbne przywrócenie':
        'Probewiederherstellung',
    'W kopii nie ma plików, które dałoby się sprawdzić próbnie.':
        'Die Sicherung enthält keine Dateien, die sich per Probewiederherstellung prüfen ließen.',
    'przywrócony plik różni się od pliku źródłowego':
        'die wiederhergestellte Datei weicht von der Quelldatei ab',
    'przywrócony plik różni się od sumy kontrolnej zapisanej podczas kopii':
        'die wiederhergestellte Datei weicht von der bei der Sicherung gespeicherten Prüfsumme ab',
    'próbne przywrócenie':
        'Probewiederherstellung',
    '(brak zapisanych szablonów)':
        '(keine gespeicherten Vorlagen)',
    'Bez tego kopia planowa ruszy dopiero wtedy, gdy sam otworzysz program.':
        'Ohne das startet eine geplante Sicherung erst, wenn du das Programm selbst öffnest.',
    'Codziennie o godzinie':
        'Täglich zu fester Uhrzeit',
    'Codziennie o wybranej godzinie (zalecane)':
        'Täglich zu einer gewählten Uhrzeit (empfohlen)',
    'Dla dysku USB podłączanego od czasu do czasu. Najwyżej jedna kopia na 12 godzin.':
        'Für ein USB-Laufwerk, das du ab und zu anschließt. Höchstens eine Sicherung alle 12 Stunden.',
    'Dostępne w zainstalowanej wersji programu (plik EXE).':
        'Verfügbar in der installierten Version des Programms (EXE-Datei).',
    'Godzina kopii codziennej (czas tego komputera).':
        'Uhrzeit der täglichen Sicherung (Zeit dieses Computers).',
    'Harmonogram działa wtedy, gdy działa program — także ukryty przy zegarze.':
        'Der Zeitplan arbeitet, solange das Programm läuft — auch nur als Symbol neben der Uhr.',
    'Harmonogram nie uruchamia kopii, dopóki tego nie odznaczysz. Ręczne kopie działają.':
        'Der Zeitplan startet keine Sicherungen, bis du das Häkchen wieder entfernst. Manuelle Sicherungen funktionieren weiterhin.',
    'Harmonogram szablonu „{name}” zapisany.':
        'Zeitplan der Vorlage „{name}“ gespeichert.',
    'Harmonogram:':
        'Zeitplan:',
    'Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.':
        'Ist der Computer zu dieser Zeit aus, startet die Sicherung nach dem Einschalten.',
    'Kiedy kopia z tego szablonu ma ruszać sama.':
        'Wann die Sicherung dieser Vorlage von selbst starten soll.',
    'Kiedy robić kopię?':
        'Wann soll gesichert werden?',
    'Kopia będzie robiona codziennie o {time}; termin przegapiony przy wyłączonym komputerze program nadrobi po jego włączeniu.':
        'Die Sicherung läuft täglich um {time}; einen Termin, der bei ausgeschaltetem Computer verpasst wurde, holt das Programm nach dem Einschalten nach.',
    'Kopia planowa nie powiodła się':
        'Geplante Sicherung fehlgeschlagen',
    'Kopia rusza tylko wtedy, gdy ją uruchomisz.':
        'Die Sicherung läuft nur, wenn du sie selbst startest.',
    'Kopia ruszy po podłączeniu dysku docelowego (najwyżej raz na 12 godzin).':
        'Die Sicherung startet, sobald das Ziellaufwerk angeschlossen wird (höchstens einmal alle 12 Stunden).',
    'Kopia ruszy po podłączeniu dysku docelowego — najwyżej raz na 12 godzin.':
        'Die Sicherung startet, sobald das Ziellaufwerk angeschlossen wird — höchstens einmal alle 12 Stunden.',
    'Kopia sprzed miesiąca nie chroni tego, co zmieniło się od tamtej pory.':
        'Eine Sicherung von vor einem Monat schützt nicht, was sich seitdem geändert hat.',
    'Kopia „{name}” czeka':
        'Sicherung „{name}“ ist überfällig',
    'Kopia „{name}” nie ruszyła':
        'Sicherung „{name}“ wurde nicht gestartet',
    'Kopie planowe działają, gdy działa program (także ukryty przy zegarze).':
        'Geplante Sicherungen laufen, solange das Programm läuft (auch nur als Symbol neben der Uhr).',
    'Kopie planowe działają, gdy działa program: po zamknięciu okna zostaje ikona przy zegarze, a przy logowaniu do Windows program uruchamia się w tle.':
        'Geplante Sicherungen laufen, solange das Programm läuft: Nach dem Schließen des Fensters bleibt ein Symbol neben der Uhr, und bei der Anmeldung bei Windows startet das Programm im Hintergrund.',
    'Kopie planowe i praca w tle':
        'Geplante Sicherungen und Hintergrundbetrieb',
    'Kopie planowe wykonają się o czasie. Program zamkniesz z menu ikony przy zegarze.':
        'Geplante Sicherungen laufen pünktlich. Beenden kannst du das Programm über das Menü des Symbols neben der Uhr.',
    'Kopię uruchamiasz przyciskiem. Najprostsze, ale łatwo o niej zapomnieć.':
        'Du startest die Sicherung per Schaltfläche. Am einfachsten, aber man vergisst sie leicht.',
    'Kopię uruchamiasz sam — przyciskiem w programie albo z menu ikony przy zegarze.':
        'Du startest die Sicherung selbst — mit der Schaltfläche im Programm oder über das Menü des Symbols neben der Uhr.',
    'Następna kopia: {when}. Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.':
        'Nächste Sicherung: {when}. Ist der Computer zu dieser Zeit aus, startet die Sicherung nach dem Einschalten.',
    'Nie udało się zmienić startu przy logowaniu — szczegóły w dzienniku.':
        'Der Start bei der Anmeldung ließ sich nicht ändern — Details im Protokoll.',
    'Od {days} dni nie było udanej kopii. Podłącz dysk docelowy albo otwórz program, żeby sprawdzić, co się dzieje.':
        'Seit {days} Tagen gab es keine erfolgreiche Sicherung. Schließe das Ziellaufwerk an oder öffne das Programm, um nachzusehen, was los ist.',
    'Otwórz Sigelith Backup':
        'Sigelith Backup öffnen',
    'Po podłączeniu dysku docelowego':
        'Beim Anschließen des Ziellaufwerks',
    'Po podłączeniu dysku z kopią':
        'Beim Anschließen des Sicherungslaufwerks',
    'Po zamknięciu okna działaj dalej przy zegarze, gdy są kopie planowe':
        'Nach dem Schließen des Fensters neben der Uhr weiterlaufen, wenn Sicherungen geplant sind',
    'Potrzebne, żeby kopie planowe ruszały bez Twojego udziału. Hasło trafia do magazynu systemowego powiązanego z Twoim kontem, nie do plików programu.':
        'Nötig, damit geplante Sicherungen ohne dein Zutun starten. Das Passwort kommt in den Passwortspeicher des Systems, der an dein Konto gebunden ist, nicht in die Dateien des Programms.',
    'Program uruchamia się w tle przy logowaniu, więc terminy nie przepadną.':
        'Das Programm startet bei der Anmeldung im Hintergrund, sodass keine Termine verloren gehen.',
    'Ręcznie':
        'Manuell',
    'Ręcznie — kiedy zechcę':
        'Manuell — wann ich will',
    'Start przy logowaniu włączony':
        'Start bei der Anmeldung eingeschaltet',
    'Szablon jest zaszyfrowany, a hasło nie jest zapamiętane. Kopie planowe potrzebują hasła zapisanego w Menedżerze poświadczeń Windows.':
        'Die Vorlage ist verschlüsselt, und das Passwort ist nicht gespeichert. Geplante Sicherungen brauchen ein Passwort in der Windows-Anmeldeinformationsverwaltung.',
    'Sigelith Backup będzie uruchamiał się w tle, żeby wykonywać kopie planowe. Wyłączysz to w ustawieniach programu.':
        'Sigelith Backup startet künftig im Hintergrund, um geplante Sicherungen auszuführen. Ausschalten kannst du das in den Einstellungen des Programms.',
    'Sigelith Backup działa w tle':
        'Sigelith Backup läuft im Hintergrund',
    'Uruchamiaj program w tle przy logowaniu do Windows':
        'Programm bei der Windows-Anmeldung im Hintergrund starten',
    'Wstrzymaj kopie planowe':
        'Geplante Sicherungen pausieren',
    'Zakończ':
        'Beenden',
    'Zamknięcie okna chowa je, a harmonogram pilnuje terminów. Program zamkniesz z menu ikony przy zegarze.':
        'Das Schließen blendet das Fenster nur aus, der Zeitplan behält die Termine im Blick. Beenden kannst du das Programm über das Menü des Symbols neben der Uhr.',
    'Zrób kopię teraz':
        'Jetzt sichern',
    '{summary} Szczegóły znajdziesz w programie, w zakładce „Dziennik”.':
        '{summary} Details findest du im Programm auf der Seite „Protokoll“.',
    'Program działa z uprawnieniami administratora. Nie są mu potrzebne — kopia i przywracanie działają bez nich, a pliki zapisane przez administratora mogą później nie dać się zmienić ze zwykłego konta.':
        'Das Programm läuft mit Administratorrechten. Es braucht sie nicht — Sicherung und Wiederherstellung funktionieren ohne sie, und von einem Administrator geschriebene Dateien lassen sich später unter einem normalen Konto womöglich nicht ändern.',
    'Pliki otwarte w innych programach nie trafiły do kopii: {files}. Zamknij te programy i uruchom kopię ponownie — dograne zostaną tylko te pliki.':
        'In anderen Programmen geöffnete Dateien wurden nicht gesichert: {files}. Schließe diese Programme und starte die Sicherung erneut — nur diese Dateien werden nachgetragen.',
    'Uwaga: w źródle zmieniło się podejrzanie dużo plików — {reasons}':
        'Warnung: In der Quelle haben sich verdächtig viele Dateien geändert — {reasons}',
    'Wstrzymano kopię: w źródle zmieniło się podejrzanie dużo plików. {reasons}':
        'Sicherung angehalten: In der Quelle haben sich verdächtig viele Dateien geändert. {reasons}',
    'Zmieniło się albo zniknęło {count} z {previous} plików poprzedniej kopii.':
        '{count} von {previous} Dateien der vorherigen Sicherung wurden geändert oder sind verschwunden.',
    '{suspicious} z {evaluated} sprawdzonych zmienionych plików ma treść, która nie pasuje do ich typu (wygląda na zaszyfrowaną).':
        '{suspicious} von {evaluated} geprüften geänderten Dateien haben einen Inhalt, der nicht zu ihrem Typ passt (er sieht verschlüsselt aus).',
    'Kontynuuj mimo to':
        'Trotzdem fortfahren',
    'Kopia planowa wstrzymana':
        'Geplante Sicherung angehalten',
    'Kopia wstrzymana do decyzji.':
        'Sicherung angehalten, bis du entscheidest.',
    'Kopia wstrzymana — w źródle zmieniło się podejrzanie dużo plików.':
        'Sicherung angehalten — in der Quelle haben sich verdächtig viele Dateien geändert.',
    'Podejrzanie dużo zmian':
        'Verdächtig viele Änderungen',
    'Wstrzymaj kopię':
        'Sicherung anhalten',
    '{reasons}\n\nJeśli to spodziewane — aktualizacja programu, przeniesienie albo przerobienie wielu plików — kontynuuj.\n\nJeśli nie, NIE kontynuuj: tak wygląda działanie oprogramowania szyfrującego pliki (ransomware). Sprawdź najpierw, czy Twoje pliki dają się otworzyć. Wcześniejsze wersje w kopii pozostają nietknięte.':
        '{reasons}\n\nWenn das zu erwarten war — ein Programm-Update, das Verschieben oder Überarbeiten vieler Dateien —, fahre fort.\n\nWenn nicht, fahre NICHT fort: So äußert sich Schadsoftware, die Dateien verschlüsselt (Ransomware). Prüfe zuerst, ob sich deine Dateien öffnen lassen. Frühere Versionen in der Sicherung bleiben unangetastet.',
    '{reasons} To może być działanie złośliwego oprogramowania szyfrującego pliki. Otwórz program, sprawdź pliki i uruchom kopię ręcznie.':
        '{reasons} Das kann das Werk von Schadsoftware sein, die Dateien verschlüsselt. Öffne das Programm, prüfe deine Dateien und starte die Sicherung manuell.',
    'Pominięto {count} {files}.':
        '{count} {files} übersprungen.',
    'Ponawiam {count} {files}…':
        'Neuer Versuch für {count} {files}…',
    ' (bez {count} {files})':
        ' (ohne {count} {files})',
    'plik otwarty w innym programie':
        'in einem anderen Programm geöffnete Datei',
    'pliki otwarte w innych programach':
        'in anderen Programmen geöffnete Dateien',
    'plików otwartych w innych programach':
        'in anderen Programmen geöffnete Dateien',
    'pliku otwartego w innym programie':
        'in einem anderen Programm geöffnete Datei',
    '\n\n…i kolejne: {count}.':
        '\n\n…und weitere: {count}.',
    'Foldery objęte kopią ({count}): {list}':
        'Zu sichernde Ordner ({count}): {list}',
    'Nośnik nie obsługuje twardych dowiązań — kopiuję do nowej wersji niezmienione pliki: {count} ({size})…':
        'Der Datenträger unterstützt keine Hardlinks — unveränderte Dateien werden in die neue Version kopiert: {count} ({size})…',
    'Pliki bez sumy kontrolnej sprawdzone tylko co do rozmiaru, bo ich źródło zmieniło się albo jest niedostępne: {count}.':
        'Dateien ohne Prüfsumme, nur anhand der Größe geprüft, weil ihre Quelle sich geändert hat oder nicht verfügbar ist: {count}.',
    'Pliki bez zapisanej sumy kontrolnej, porównane ze źródłem i uzupełnione w spisie treści: {count}.':
        'Dateien ohne gespeicherte Prüfsumme, mit der Quelle verglichen und im Inhaltsverzeichnis ergänzt: {count}.',
    'Pliki przeniesione w źródle: {count} — trafią do kopii bez przesyłania danych.':
        'In der Quelle verschobene Dateien: {count} — sie kommen ohne Datenübertragung in die Sicherung.',
    'Pliki skasowane w źródle: {count} — {action}.':
        'In der Quelle gelöschte Dateien: {count} — {action}.',
    'Pliki z końcówką dopisaną do nazwy, których oryginały zniknęły: {count}.':
        'Dateien mit einer an den Namen angehängten Endung, deren Originale verschwunden sind: {count}.',
    'Pliki zmienione w trakcie kopiowania: {count} — zostaną zapisane ponownie w przebiegu uzupełniającym.':
        'Während des Kopierens geänderte Dateien: {count} — sie werden bei der Nachsicherung erneut geschrieben.',
    'Pliki, których brakuje w kopii i które zostaną zapisane ponownie: {count}.':
        'Dateien, die in der Sicherung fehlen und erneut geschrieben werden: {count}.',
    'Podpinanie niezmienionych plików do nowej wersji: {count}…':
        'Unveränderte Dateien werden in die neue Version eingebunden: {count}…',
    'Pomijam pliki, które już są w tej wersji kopii: {count}.':
        'Dateien, die bereits in dieser Sicherungsversion sind, werden übersprungen: {count}.',
    'Porządkowanie historii — usunięte najstarsze wersje: {count}.':
        'Verlauf aufgeräumt — älteste Versionen entfernt: {count}.',
    'Przenoszenie plików, które zmieniły miejsce w źródle: {count}…':
        'Dateien, die in der Quelle ihren Ort gewechselt haben, werden verschoben: {count}…',
    'Próbne przywrócenie losowo wybranych plików: {count}…':
        'Probewiederherstellung zufällig gewählter Dateien: {count}…',
    'Usuwanie z kopii plików skasowanych w źródle: {count}…':
        'In der Quelle gelöschte Dateien werden aus der Sicherung entfernt: {count}…',
    'Uzupełniam kopię o pliki, które przybyły lub zmieniły się w trakcie: {count} ({size})…':
        'Dateien, die währenddessen hinzugekommen sind oder sich geändert haben, werden nachgesichert: {count} ({size})…',
    'Uzupełnianie wersji {version} — pliki już zapisane, które zostaną pominięte: {count}.':
        'Version {version} wird ergänzt — bereits geschriebene Dateien, die übersprungen werden: {count}.',
    'Wznawiam wersję {version} — już zapisane: {done}, do dogrania: {todo}.':
        'Version {version} wird fortgesetzt — bereits geschrieben: {done}, noch offen: {todo}.',
    'pliku':
        'Datei',
    'Brak fragmentu {cid} w magazynie kopii.':
        'Fragment {cid} fehlt im Fragmentspeicher der Sicherung.',
    'Brak opisu magazynu fragmentów w katalogu kopii.':
        'Im Sicherungsordner fehlt die Beschreibung des Fragmentspeichers.',
    'Duże pliki zapisuj różnicowo (od 256 MB)':
        'Große Dateien differenziell speichern (ab 256 MB)',
    'Fragment {cid} jest uszkodzony.':
        'Fragment {cid} ist beschädigt.',
    'Kolejna wersja dużego pliku — maszyny wirtualnej, skrzynki pocztowej, bazy —\nzapisuje tylko zmienione fragmenty zamiast całego pliku. W kopii taki plik\nleży jako przepis + fragmenty; złoży go program albo skrypt ratunkowy.':
        'Bei jeder weiteren Version einer großen Datei — einer virtuellen Maschine, eines Postfachs, einer Datenbank —\nwerden nur die geänderten Fragmente statt der ganzen Datei gespeichert. In der Sicherung liegt so eine Datei\nals Bauplan plus Fragmente; das Programm oder das Rettungsskript setzt sie wieder zusammen.',
    'Opis magazynu fragmentów jest uszkodzony.':
        'Die Beschreibung des Fragmentspeichers ist beschädigt.',
    'Plik złożony z fragmentów różni się od zapisanego w przepisie.':
        'Die aus Fragmenten zusammengesetzte Datei weicht von der im Bauplan beschriebenen ab.',
    'Podane hasło nie pasuje do fragmentów zapisanych wcześniej w tej kopii.':
        'Das eingegebene Passwort passt nicht zu den Fragmenten, die zuvor in diese Sicherung geschrieben wurden.',
    'Przepis pliku jest uszkodzony.':
        'Der Bauplan der Datei ist beschädigt.',
    'To nie jest przepis pliku zapisanego fragmentami.':
        'Das ist kein Bauplan einer in Fragmenten gespeicherten Datei.',
    'Usunięto nieużywane fragmenty dużych plików: {count} ({size}).':
        'Nicht mehr benötigte Fragmente großer Dateien entfernt: {count} ({size}).',
    ', zakotwiczona w Bitcoinie':
        ', in Bitcoin verankert',
    'Adres usługi:':
        'Dienstadresse:',
    'Brak fragmentu {cid} w kopii poza domem.':
        'Fragment {cid} fehlt in der Kopie außer Haus.',
    'Brak klucza albo hasła w Menedżerze poświadczeń Windows — zapisz ustawienia kopii poza domem jeszcze raz.':
        'Schlüssel oder Passwort fehlen in der Windows-Anmeldeinformationsverwaltung — speichere die Einstellungen der Kopie außer Haus erneut.',
    'Brak spisu wersji, którego dotyczy znacznik.':
        'Die Dateiliste der Version, auf die sich der Zeitstempel bezieht, fehlt.',
    'Certyfikat PDF':
        'PDF-Zertifikat',
    'Druga, zaszyfrowana kopia w usłudze zgodnej z S3 (np. Backblaze B2)':
        'Eine zweite, verschlüsselte Kopie in einem S3-kompatiblen Dienst (z. B. Backblaze B2)',
    'Folder w kubełku:':
        'Ordner im Bucket:',
    'Hasło kopii poza domem':
        'Passwort der Kopie außer Haus',
    'Hasło kopii poza domem nie pasuje do danych zapisanych w tym miejscu.':
        'Das Passwort der Kopie außer Haus passt nicht zu den dort gespeicherten Daten.',
    'Hasło kopii poza domem powinno mieć co najmniej 10 znaków.':
        'Das Passwort der Kopie außer Haus sollte mindestens 10 Zeichen lang sein.',
    'Hasło szyfrowania:':
        'Verschlüsselungspasswort:',
    'Identyfikator klucza:':
        'Schlüssel-ID:',
    'Katalog, do którego trafią pliki':
        'Ordner, in den die Dateien kommen',
    'Klucz tajny':
        'Geheimer Schlüssel',
    'Klucz tajny:':
        'Geheimer Schlüssel:',
    'Kopia na dysku obok komputera nie przetrwa pożaru ani kradzieży. Tu ustawisz drugą kopię w usłudze zgodnej z S3 (np. Backblaze B2). Pliki są szyfrowane na tym komputerze osobnym hasłem — usługa widzi tylko nieczytelne fragmenty.':
        'Eine Sicherung auf einem Laufwerk neben dem Computer übersteht weder Brand noch Diebstahl. Hier richtest du eine zweite Kopie in einem S3-kompatiblen Dienst ein (z. B. Backblaze B2). Die Dateien werden auf diesem Computer mit einem eigenen Passwort verschlüsselt — der Dienst sieht nur unlesbare Fragmente.',
    'Kopia poza domem':
        'Kopie außer Haus',
    'Kopia poza domem dla szablonu „{name}” zapisana.':
        'Kopie außer Haus für die Vorlage „{name}“ gespeichert.',
    'Kopia poza domem nie ruszyła':
        'Kopie außer Haus wurde nicht gestartet',
    'Kopia poza domem potrzebuje Menedżera poświadczeń Windows, a jest on niedostępny.':
        'Die Kopie außer Haus braucht die Windows-Anmeldeinformationsverwaltung, die aber nicht verfügbar ist.',
    'Kopia poza domem „{name}”':
        'Kopie außer Haus „{name}“',
    'Kopia poza domem…':
        'Kopie außer Haus…',
    'Korzeń tygodnia zakotwiczony w łańcuchu Bitcoina.':
        'Der Root der Woche ist in der Bitcoin-Chain verankert.',
    'Kubełek (bucket):':
        'Bucket:',
    'Migawek w usłudze: {count}.':
        'Snapshots im Dienst: {count}.',
    'Migawka i cel':
        'Snapshot und Ziel',
    'Migawka kopii poza domem jest uszkodzona.':
        'Der Snapshot der Kopie außer Haus ist beschädigt.',
    'Migawka {stamp}: plików bez zmian {reused}, wysłanych {files}, nowych fragmentów {chunks} ({size}).':
        'Snapshot {stamp}: unveränderte Dateien {reused}, hochgeladen {files}, neue Fragmente {chunks} ({size}).',
    'MinIO / Wasabi / inna zgodna z S3':
        'MinIO / Wasabi / anderer S3-kompatibler Dienst',
    'NIEPOPRAWNY':
        'UNGÜLTIG',
    'Nie ma migawki {stamp} w kopii poza domem.':
        'In der Kopie außer Haus gibt es keinen Snapshot {stamp}.',
    'Nie udało się połączyć z usługą przechowywania: {error}':
        'Keine Verbindung zum Speicherdienst: {error}',
    'Nie udało się wczytać migawek: {error}':
        'Die Snapshots konnten nicht geladen werden: {error}',
    'Nie udało się zapisać klucza albo hasła w magazynie systemowym.':
        'Schlüssel oder Passwort konnten nicht im Passwortspeicher des Systems gespeichert werden.',
    'Odśwież z sieci':
        'Online aktualisieren',
    'Opis kopii poza domem jest uszkodzony.':
        'Die Beschreibung der Kopie außer Haus ist beschädigt.',
    'Oznakowana: {utc} (BeatTime {beat})':
        'Gestempelt: {utc} (BeatTime {beat})',
    'Pliki wersji różnią się od spisu, który został oznakowany.':
        'Die Dateien der Version weichen von der gestempelten Dateiliste ab.',
    'Pobiera i odszyfrowuje pliki wybranej migawki':
        'Lädt die Dateien des gewählten Snapshots herunter und entschlüsselt sie',
    'Pobiera listę migawek z usługi':
        'Lädt die Liste der Snapshots vom Dienst',
    'Pobiera podpis tygodnia i stan kotwicy w Bitcoinie':
        'Ruft die Wochensignatur und den Stand der Bitcoin-Verankerung ab',
    'Pobieram potwierdzenia…':
        'Bestätigungen werden abgerufen…',
    'Podaj hasło szyfrowania kopii poza domem.':
        'Gib das Verschlüsselungspasswort der Kopie außer Haus ein.',
    'Podaj klucz tajny usługi.':
        'Gib den geheimen Schlüssel des Dienstes ein.',
    'Podam dane ręcznie':
        'Ich gebe die Daten selbst ein',
    'Pominięte (otwarte w innych programach albo zmienione w trakcie): {count}.':
        'Übersprungen (in anderen Programmen geöffnet oder währenddessen geändert): {count}.',
    'Porządkowanie kopii poza domem…':
        'Kopie außer Haus wird aufgeräumt…',
    'Potwierdzenia odświeżone.':
        'Bestätigungen aktualisiert.',
    'Poza dom':
        'Außer Haus',
    'Połączenie działa: zapis, odczyt i usuwanie się udały.':
        'Die Verbindung funktioniert: Schreiben, Lesen und Löschen waren erfolgreich.',
    'Połączenie nie działa: {error}':
        'Die Verbindung funktioniert nicht: {error}',
    'Przywraca pliki z zaszyfrowanej kopii w usłudze S3 — także na nowym komputerze':
        'Stellt Dateien aus der verschlüsselten Kopie im S3-Dienst wieder her — auch auf einem neuen Computer',
    'Przywracanie z kopii poza domem':
        'Wiederherstellung aus der Kopie außer Haus',
    'Przywracanie {count} {files} z kopii poza domem…':
        'Wiederherstellung von {count} {files} aus der Kopie außer Haus…',
    'Przywróć':
        'Wiederherstellen',
    'Region:':
        'Region:',
    'Skąd':
        'Quelle',
    'Spis wersji zgodny ze znacznikiem: {answer}':
        'Dateiliste der Version passt zum Zeitstempel: {answer}',
    'Spis wersji został zmieniony po oznakowaniu.':
        'Die Dateiliste der Version wurde nach dem Stempeln geändert.',
    'Sprawdza spis wersji, drogę w drzewie tygodnia i podpis — bez sieci':
        'Prüft die Dateiliste der Version, den Pfad im Baum der Woche und die Signatur — offline',
    'Sprawdzam połączenie…':
        'Verbindung wird geprüft…',
    'Sprawdź':
        'Prüfen',
    'Sprawdź połączenie':
        'Verbindung prüfen',
    'Starsze migawki są usuwane, gdy nadmiar sięgnie kilku — co kilka dni.':
        'Ältere Snapshots werden entfernt, sobald sich einige zu viel angesammelt haben — alle paar Tage.',
    'Suma w drzewie tygodnia: {answer}':
        'Hash im Baum der Woche: {answer}',
    'Suma wersji nie należy do drzewa tygodnia podanego w potwierdzeniu.':
        'Der Hash der Version gehört nicht zum Baum der Woche aus der Bestätigung.',
    'Ta wersja nie ma znacznika czasu.':
        'Diese Version hat keinen Zeitstempel.',
    'Także po kopiach planowych. Wysyłane są tylko pliki nowe i zmienione.':
        'Auch nach geplanten Sicherungen. Hochgeladen werden nur neue und geänderte Dateien.',
    'Tydzień jeszcze się nie zamknął — podpis pojawi się po poniedziałku 00:00 UTC.':
        'Die Woche ist noch nicht abgeschlossen — die Signatur kommt nach Montag, 00:00 UTC.',
    'Usunięto starsze migawki: {count}, nieużywane fragmenty: {chunks}.':
        'Ältere Snapshots entfernt: {count}, nicht mehr benötigte Fragmente: {chunks}.',
    'Usługa chwilowo niedostępna ({status}).':
        'Der Dienst ist vorübergehend nicht erreichbar ({status}).',
    'Usługa odrzuciła żądanie ({status} {code}): {message}':
        'Der Dienst hat die Anfrage abgelehnt ({status} {code}): {message}',
    'Usługa przechowywania':
        'Speicherdienst',
    'Usługa zwróciła inną treść niż zapisana.':
        'Der Dienst hat einen anderen Inhalt zurückgegeben als geschrieben.',
    'Usługa:':
        'Dienst:',
    'Uzupełnij adres usługi, nazwę kubełka i klucze dostępu.':
        'Gib die Dienstadresse, den Namen des Buckets und die Zugangsschlüssel ein.',
    'Uzupełnij adres usługi, region, kubełek i identyfikator klucza.':
        'Gib Dienstadresse, Region, Bucket und Schlüssel-ID ein.',
    'W tym katalogu kopii nie ma jeszcze znaczników czasu.':
        'In diesem Sicherungsordner gibt es noch keine Zeitstempel.',
    'W tym miejscu nie ma jeszcze kopii poza domem.':
        'An diesem Ort gibt es noch keine Kopie außer Haus.',
    'Wczytaj migawki':
        'Snapshots laden',
    'Wczytaj migawki i wybierz jedną z listy.':
        'Lade die Snapshots und wähle einen aus der Liste.',
    'Wczytuję migawkę {stamp}…':
        'Snapshot {stamp} wird geladen…',
    'Wczytuję poprzednią migawkę kopii poza domem…':
        'Vorheriger Snapshot der Kopie außer Haus wird geladen…',
    'Wybierz migawkę i katalog, do którego trafią pliki.':
        'Wähle einen Snapshot und den Ordner, in den die Dateien kommen.',
    'Wybierz wersję z listy.':
        'Wähle eine Version aus der Liste.',
    'Wysyłaj poza dom po każdej udanej kopii z tego szablonu':
        'Nach jeder erfolgreichen Sicherung dieser Vorlage außer Haus hochladen',
    'Wysyłam poza dom pliki nowe i zmienione: {count}…':
        'Neue und geänderte Dateien werden außer Haus hochgeladen: {count}…',
    'Z kopii poza domem…':
        'Aus der Kopie außer Haus…',
    'Zachowuj migawek:':
        'Snapshots behalten:',
    'Zapisuje ustawienia; klucz i hasło trafiają do Menedżera poświadczeń Windows':
        'Speichert die Einstellungen; Schlüssel und Passwort kommen in die Windows-Anmeldeinformationsverwaltung',
    'Zapisuje, odczytuje i usuwa mały plik próbny':
        'Schreibt, liest und löscht eine kleine Testdatei',
    'Zapisuję migawkę {stamp}…':
        'Snapshot {stamp} wird gespeichert…',
    'Znacznik dowodzi, że wersja kopii w dokładnie tym kształcie istniała w podanej chwili. Podpis tygodnia pojawia się po jego zamknięciu (poniedziałek 00:00 UTC), a kotwica w Bitcoinie — zwykle kilka godzin później.':
        'Ein Zeitstempel beweist, dass die Sicherungsversion genau in dieser Form zum angegebenen Zeitpunkt existierte. Die Wochensignatur kommt nach dem Abschluss der Woche (Montag 00:00 UTC), die Bitcoin-Verankerung meist einige Stunden später.',
    'Znacznika czasu nie udało się zapisać: {error}':
        'Der Zeitstempel konnte nicht gespeichert werden: {error}',
    'Znaczniki czasu':
        'Zeitstempel',
    'Znaczniki czasu…':
        'Zeitstempel…',
    'kopia poza domem':
        'Kopie außer Haus',
    'np. komputer-domowy':
        'z. B. pc-zuhause',
    'oznakowana {when} — podpis po zamknięciu tygodnia':
        'gestempelt {when} — Signatur nach Abschluss der Woche',
    'podpisana (tydzień {week}){bitcoin}':
        'signiert (Woche {week}){bitcoin}',
    'poprawny':
        'gültig',
    'przywracanie z kopii poza domem':
        'Wiederherstellung aus der Kopie außer Haus',
    'Łączę się z usługą…':
        'Verbindung zum Dienst wird hergestellt…',
    ' dni':
        ' Tage',
    ' mies.':
        ' Mon.',
    ' tyg.':
        ' Wo.',
    'Ile ostatnich wersji zachować. Starsze są kasowane po udanym przebiegu.':
        'Wie viele der letzten Versionen aufbewahrt werden. Ältere werden nach einem erfolgreichen Durchlauf gelöscht.',
    'Kalendarz zostawia najnowszą wersję z każdego z ostatnich dni, tygodni\ni miesięcy — gęsto dla świeżych zmian, rzadko dla dawnych. Nadmiar jest\nkasowany po udanym przebiegu; wersje niedokończone nigdy.':
        'Der Kalender behält die neueste Version jedes der letzten Tage, Wochen\nund Monate — dicht für frische Änderungen, dünn für alte. Der Überschuss wird\nnach einem erfolgreichen Durchlauf gelöscht; unvollständige Versionen nie.',
    'Z ilu ostatnich dni zachować po jednej, najnowszej wersji.':
        'Für wie viele der letzten Tage jeweils die neueste Version aufbewahrt wird.',
    'Z ilu ostatnich miesięcy zachować po jednej, najnowszej wersji.':
        'Für wie viele der letzten Monate jeweils die neueste Version aufbewahrt wird.',
    'Z ilu ostatnich tygodni zachować po jednej, najnowszej wersji.':
        'Für wie viele der letzten Wochen jeweils die neueste Version aufbewahrt wird.',
    'Zachowuj:':
        'Aufbewahren:',
    'kalendarz: dni, tygodnie, miesiące':
        'Kalender: Tage, Wochen, Monate',
    'ostatnie wersje':
        'letzte Versionen',
    'wszystkie wersje':
        'alle Versionen',
    ' (niedokończona)':
        ' (unvollständig)',
    'Fragment nazwy albo ścieżki, bez rozróżniania wielkości liter.':
        'Teil eines Namens oder Pfads, ohne Unterscheidung von Groß- und Kleinschreibung.',
    'Główny folder kopii':
        'Hauptordner der Sicherung',
    'Historia pliku':
        'Dateiverlauf',
    'Nazwa':
        'Name',
    'Nic nie znaleziono.':
        'Nichts gefunden.',
    'Nie udało się: {error}':
        'Fehlgeschlagen: {error}',
    'Odtwarza plik do katalogu tymczasowego i otwiera go':
        'Stellt die Datei in einem temporären Ordner wieder her und öffnet sie',
    'Odtwarza plik w wybranym miejscu':
        'Stellt die Datei an einem Ort deiner Wahl wieder her',
    'Odtwarzam „{name}”…':
        '„{name}“ wird wiederhergestellt…',
    'Otwarto kopię „{name}” (plik tymczasowy, zniknie po zamknięciu programu).':
        'Kopie von „{name}“ geöffnet (temporäre Datei, wird beim Schließen des Programms entfernt).',
    'Otwórz':
        'Öffnen',
    'Otwórz kopię':
        'Kopie öffnen',
    'Pliki i wersje wprost z kopii — bez przywracania':
        'Dateien und Versionen direkt aus der Sicherung — ohne Wiederherstellung',
    'Pliki i wersje wprost z kopii — bez przywracania całości.':
        'Dateien und Versionen direkt aus der Sicherung — ohne alles wiederherzustellen.',
    'Pokazuje pliki i wersje tej kopii — pojedynczy plik otworzysz bez przywracania całości':
        'Zeigt die Dateien und Versionen dieser Sicherung — eine einzelne Datei öffnest du, ohne alles wiederherzustellen',
    'Pokaż foldery':
        'Ordner anzeigen',
    'Przeglądaj…':
        'Durchsuchen…',
    'Przeglądanie':
        'Durchsuchen',
    'Przeszukuje spis treści kopii':
        'Durchsucht das Inhaltsverzeichnis der Sicherung',
    'Rozmiar':
        'Größe',
    'Szukaj':
        'Suchen',
    'Szukaj pliku w najnowszym stanie kopii…':
        'Datei im neuesten Stand der Sicherung suchen…',
    'Szukam…':
        'Suche läuft…',
    'W których wersjach jest ten plik i kiedy się zmieniał':
        'In welchen Versionen diese Datei enthalten ist und wann sie sich geändert hat',
    'W tym folderze nie ma wersji kopii.':
        'In diesem Ordner gibt es keine Sicherungsversionen.',
    'Wczytuje wersje z tego folderu kopii':
        'Lädt die Versionen aus diesem Sicherungsordner',
    'Wersja kopii, której zawartość widzisz poniżej.':
        'Die Sicherungsversion, deren Inhalt du unten siehst.',
    'Wersja: {version}':
        'Version: {version}',
    'Wersje z tym plikiem: {count}. Dwuklik otwiera kopię z danej wersji.':
        'Versionen mit dieser Datei: {count}. Ein Doppelklick öffnet die Kopie aus der jeweiligen Version.',
    'Wraca z wyników wyszukiwania do drzewa folderów':
        'Kehrt von den Suchergebnissen zum Ordnerbaum zurück',
    'Wskaż folder kopii i kliknij „Otwórz”.':
        'Wähle den Sicherungsordner und klicke auf „Öffnen“.',
    'Zapisano: {path}':
        'Gespeichert: {path}',
    'Zapisz jako…':
        'Speichern unter…',
    'Zapisz kopię pliku':
        'Kopie der Datei speichern',
    'Zaznacz plik i wybierz „Otwórz kopię”, żeby zajrzeć do niego w zwykłym programie, albo „Historia pliku”, żeby zobaczyć, w których wersjach się zmieniał.':
        'Markiere eine Datei und wähle „Kopie öffnen“, um sie im gewohnten Programm anzusehen, oder „Dateiverlauf“, um zu sehen, in welchen Versionen sie sich geändert hat.',
    'Zmieniono':
        'Geändert',
    'Znalezione pliki: {count}. Wyniki pochodzą z najnowszego stanu kopii.':
        'Gefundene Dateien: {count}. Die Ergebnisse stammen aus dem neuesten Stand der Sicherung.',
    'przeglądanie kopii':
        'Durchsuchen der Sicherung',
    'zmieniony':
        'geändert',
    'najstarsza zachowana kopia':
        'älteste erhaltene Kopie',
    'Foldery w AppData':
        'Ordner in AppData',
    'Przywracanie utworzy nowe foldery bezpośrednio w AppData:\n\n{folders}\n\nWindows pozwala wersji programu ze Sklepu tworzyć je tylko w jej prywatnej kopii — pliki będą widoczne w tym programie, ale nie w programie, do którego należą.\n\nNajprościej: zainstaluj i raz uruchom tamten program (utworzy swój folder), a potem przywróć jeszcze raz. Albo przywróć do zwykłego folderu i przenieś pliki Eksploratorem.':
        'Die Wiederherstellung legt neue Ordner direkt in AppData an:\n\n{folders}\n\nWindows lässt die Version dieses Programms aus dem Microsoft Store solche Ordner nur in ihrer privaten Kopie anlegen — die Dateien sind dann in diesem Programm sichtbar, aber nicht in dem Programm, zu dem sie gehören.\n\nAm einfachsten: Installiere das andere Programm und starte es einmal (es legt seinen Ordner an), dann stelle erneut wieder her. Oder stelle in einen normalen Ordner wieder her und verschiebe die Dateien mit dem Datei-Explorer.',
    'Przywracanie utworzyłoby w AppData nowe foldery, których inne programy nie zobaczą: {folders}':
        'Die Wiederherstellung würde in AppData neue Ordner anlegen, die andere Programme nicht sehen: {folders}',
    'Przywracanie wstrzymane do decyzji.':
        'Wiederherstellung angehalten, bis du entscheidest.',
    'Przywróć mimo to':
        'Trotzdem wiederherstellen',
    'Start programu przy logowaniu wyłączono w Ustawieniach Windows. Włączysz go tam: Ustawienia → Aplikacje → Uruchamianie → Sigelith Backup.':
        'Der Programmstart bei der Anmeldung wurde in den Windows-Einstellungen ausgeschaltet. Dort kannst du ihn wieder einschalten: Einstellungen → Apps → Autostart → Sigelith Backup.',
    'Start przy logowaniu':
        'Start bei der Anmeldung',
    'Start przy logowaniu wyłączono w Ustawieniach Windows → Aplikacje → Uruchamianie; dopóki go tam nie włączysz, kopie planowe działają tylko przy otwartym programie.':
        'Der Start bei der Anmeldung wurde in den Windows-Einstellungen → Apps → Autostart ausgeschaltet; solange du ihn dort nicht wieder einschaltest, laufen geplante Sicherungen nur bei geöffnetem Programm.',
    'Ten sam przełącznik jest w Ustawieniach Windows → Aplikacje → Uruchamianie. Wyłączony tam da się włączyć tylko tam.':
        'Derselbe Schalter befindet sich in den Windows-Einstellungen → Apps → Autostart. Wurde er dort ausgeschaltet, lässt er sich nur dort wieder einschalten.',
    'Brak pliku {name} w katalogu programu.':
        'Die Datei {name} fehlt im Programmordner.',
    'Jakie dane program przetwarza i gdzie':
        'Welche Daten das Programm verarbeitet und wo',
    'Kod źródłowy Qt':
        'Qt-Quelltext',
    'Licencja programu':
        'Lizenz des Programms',
    'Licencja programu i licencje użytych składników':
        'Lizenz des Programms und Lizenzen der verwendeten Komponenten',
    'Licencje':
        'Lizenzen',
    'Licencje i prywatność':
        'Lizenzen und Datenschutz',
    'Licencje…':
        'Lizenzen…',
    'Otwiera folder z plikami licencji w Eksploratorze':
        'Öffnet den Ordner mit den Lizenzdateien im Datei-Explorer',
    'Pokaż pliki licencji':
        'Lizenzdateien anzeigen',
    'Polityka prywatności':
        'Datenschutzerklärung',
    'Polityka prywatności…':
        'Datenschutzerklärung…',
    'Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0 — to osobne pliki w katalogu programu, które można zastąpić zgodnymi wersjami. Kod źródłowy wersji dołączonych do programu: {qt} oraz {pyside}.':
        'Das Programm verwendet die Bibliotheken Qt und PySide6 unter der Lizenz LGPL-3.0 — es sind separate Dateien im Programmordner, die sich durch kompatible Versionen ersetzen lassen. Quelltext der mitgelieferten Versionen: {qt} und {pyside}.',
    'Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0, z Pythona i z innych składników na licencjach otwartych (m.in. MIT, BSD, Apache 2.0); ikony: Bootstrap Icons (MIT). Wykaz, prawa autorskie, pełne teksty licencji i adresy kodu źródłowego Qt są pod przyciskiem „Licencje”.':
        'Das Programm verwendet die Bibliotheken Qt und PySide6 unter der Lizenz LGPL-3.0, Python und weitere Komponenten unter Open-Source-Lizenzen (u. a. MIT, BSD, Apache 2.0); Symbole: Bootstrap Icons (MIT). Die Liste, Urheberrechtshinweise, vollständige Lizenztexte und die Adressen des Qt-Quelltexts findest du unter der Schaltfläche „Lizenzen“.',
    'Program usunie z Menedżera poświadczeń Windows wszystkie hasła, które zapamiętał: hasła kopii i dane dostępu do kopii poza domem. Kopie planowe szablonów zaszyfrowanych będą potem czekać, aż podasz hasło.\n\nUsunąć?':
        'Das Programm löscht aus der Windows-Anmeldeinformationsverwaltung alle Passwörter, die es gespeichert hat: Passwörter der Sicherungen und Zugangsdaten der Kopie außer Haus. Geplante Sicherungen verschlüsselter Vorlagen warten danach, bis du das Passwort eingibst.\n\nLöschen?',
    'Składniki i ich licencje':
        'Komponenten und ihre Lizenzen',
    'Strona z kodem źródłowym Qt w wersji użytej w programie':
        'Die Seite mit dem Qt-Quelltext der im Programm verwendeten Version',
    'Usunięte zapamiętane hasła: {count}.':
        'Gelöschte gespeicherte Passwörter: {count}.',
    'Usuwa z Menedżera poświadczeń Windows wszystkie hasła zapamiętane przez program — na przykład przed odinstalowaniem':
        'Löscht alle vom Programm gespeicherten Passwörter aus der Windows-Anmeldeinformationsverwaltung — zum Beispiel vor der Deinstallation',
    'Usuń zapamiętane hasła':
        'Gespeicherte Passwörter löschen',
    'Usuń zapamiętane hasła…':
        'Gespeicherte Passwörter löschen…',
    '© {years} {publisher}. Wolne oprogramowanie na licencji GNU GPL w wersji 3 lub nowszej.':
        '© {years} {publisher}. Freie Software unter der GNU GPL, Version 3 oder später.',
    'Kod źródłowy':
        'Quelltext',
    'Kod źródłowy programu w serwisie GitHub':
        'Quelltext des Programms auf GitHub',
    'Sigelith odrzucił żądanie ({status}): {detail}':
        'Sigelith hat die Anfrage abgelehnt ({status}): {detail}',
    'Nie udało się połączyć z Sigelith: {error}':
        'Keine Verbindung zu Sigelith: {error}',
    'Sigelith odesłał potwierdzenie innej sumy kontrolnej.':
        'Sigelith hat eine Bestätigung für einen anderen Hash zurückgeschickt.',
    'Znacznik czeka na połączenie z Sigelith.':
        'Der Zeitstempel wartet auf eine Verbindung zu Sigelith.',
    'Podpis tygodnia nie zgadza się z kluczem Sigelith zapisanym w programie.':
        'Die Wochensignatur passt nicht zum im Programm eingebauten Sigelith-Schlüssel.',
    'Otwiera certyfikat znacznika na stronie Sigelith':
        'Öffnet das Zertifikat des Zeitstempels auf der Sigelith-Website',
    'Podpis Sigelith: {answer}':
        'Sigelith-Signatur: {answer}',
    'Znaczniki Sigelith wersji w tym katalogu kopii: sprawdzenie i certyfikat':
        'Sigelith-Zeitstempel der Versionen in diesem Sicherungsordner: Prüfung und Zertifikat',
    'Znakuję wersję czasem Sigelith (wysyłana jest tylko suma kontrolna)…':
        'Die Version erhält einen Sigelith-Zeitstempel (gesendet wird nur der Hash)…',
    'Znacznik czasu czeka na połączenie z Sigelith — zostanie wysłany przy następnej kopii.':
        'Der Zeitstempel wartet auf eine Verbindung zu Sigelith — er wird bei der nächsten Sicherung gesendet.',
    'Znakuj wersję czasem Sigelith':
        'Version mit Sigelith-Zeitstempel versehen',
    'Znaczniki czasu Sigelith':
        'Sigelith-Zeitstempel',
    'czeka na połączenie z Sigelith':
        'wartet auf eine Verbindung zu Sigelith',
    'Dowód, że kopia w tym kształcie istniała danego dnia (podpis Ed25519, kotwica\nw Bitcoinie). Do sigelith.org trafia wyłącznie suma kontrolna spisu wersji —\nżadne nazwy plików ani ich treść.':
        'Nachweis, dass die Sicherung in genau dieser Form an einem bestimmten Tag existierte (Ed25519-Signatur,\nBitcoin-Verankerung). An sigelith.org geht nur der Hash der Dateiliste der Version —\nkeine Dateinamen und keine Inhalte.',
    'Kopie zapasowe folderów na dysk zewnętrzny, z historią wersji i szyfrowaniem. Wszystko dzieje się na Twoim komputerze, bez konta i bez telemetrii. Z internetem program łączy się tylko wtedy, gdy sam włączysz kopię poza domem albo znaczniki czasu Sigelith.':
        'Sicherungen deiner Ordner auf ein externes Laufwerk, mit Versionsverlauf und Verschlüsselung. Alles geschieht auf deinem Computer, ohne Konto und ohne Telemetrie. Mit dem Internet verbindet sich das Programm nur, wenn du selbst die Kopie außer Haus oder die Sigelith-Zeitstempel einschaltest.',
    'Bez dokumentu: {count} {stamps} — plik zmienił się po stemplu albo zniknął i nie ma go w żadnej wersji tej kopii ({names}). Sam dowód jest zachowany.':
        'Ohne Dokument: {count} {stamps} — die Datei wurde nach dem Stempeln geändert oder ist verschwunden und in keiner Version dieser Sicherung enthalten ({names}). Der Nachweis selbst bleibt erhalten.',
    'Brak pliku dowodu albo dowód jest zaszyfrowany.':
        'Die Nachweisdatei fehlt oder der Nachweis ist verschlüsselt.',
    'Chroni dowody Sigelith: historię stempli i oznakowane dokumenty.':
        'Schützt Sigelith-Nachweise: den Stempelverlauf und die gestempelten Dokumente.',
    'Chroń dowody Sigelith':
        'Sigelith-Nachweise schützen',
    'Chroń też dowody Sigelith':
        'Auch Sigelith-Nachweise schützen',
    'Dokument':
        'Dokument',
    'Dokumenty oznakowane w Sigelith, zabezpieczone w tej kopii: sprawdzenie i odzyskanie':
        'In Sigelith gestempelte Dokumente aus dieser Sicherung: prüfen und wiederherstellen',
    'Dowody Sigelith':
        'Sigelith-Nachweise',
    'Dowody Sigelith: historia stempli i dokładne kopie oznakowanych dokumentów z plikami .beatproof trafią do magazynu dowodów w katalogu kopii.':
        'Sigelith-Nachweise: Der Stempelverlauf und exakte Kopien der gestempelten Dokumente samt ihren .beatproof-Dateien kommen in den Nachweisspeicher im Sicherungsordner.',
    'Dowody Sigelith: zabezpieczone dokumenty {count} z {total}':
        'Sigelith-Nachweise: {count} von {total} Dokumenten gesichert',
    'Dowody Sigelith…':
        'Sigelith-Nachweise…',
    'Dowody z problemem: {count} — szczegóły w kolumnie „Stan”.':
        'Nachweise mit Problemen: {count} — Details in der Spalte „Zustand“.',
    'Dowodów Sigelith nie udało się zabezpieczyć: {error}':
        'Die Sigelith-Nachweise konnten nicht gesichert werden: {error}',
    "Droga w drzewie Merkle'a nie prowadzi do podpisanego korzenia tygodnia.":
        'Der Pfad im Merkle-Baum führt nicht zum signierten Root der Woche.',
    'Gdzie zapisać dokumenty i dowody':
        'Speicherort für Dokumente und Nachweise',
    'Historia stempli Sigelith Desktop i dokładne bajty oznakowanych dokumentów, z plikami .beatproof — w osobnym magazynie, którego retencja nie sprząta.':
        'Der Stempelverlauf von Sigelith Desktop und die exakten Bytes der gestempelten Dokumente, mit .beatproof-Dateien — in einem separaten Speicher, den die Bereinigung alter Versionen nie anrührt.',
    'Każdy stempel ma tu swój folder z dokładnie tym dokumentem, który oznakowano, i plikiem .beatproof. „Sprawdź” liczy sumę każdego dokumentu i sprawdza podpis tygodnia bez łączenia się z siecią.':
        'Jeder Zeitstempel hat hier einen eigenen Ordner mit genau dem Dokument, das gestempelt wurde, und einer .beatproof-Datei. „Prüfen“ berechnet den Hash jedes Dokuments und prüft die Wochensignatur, ohne sich mit dem Netz zu verbinden.',
    'Kopia obejmie folder danych Sigelith Desktop (historię stempli), a każdy oznakowany\ndokument trafi — dokładnie w tej postaci, którą oznakowano — do magazynu dowodów\nw katalogu kopii, razem z plikiem .beatproof. Starych wersji magazyn nie dotyczy:\nretencja go nie sprząta.':
        'Die Sicherung umfasst den Datenordner von Sigelith Desktop (den Stempelverlauf), und jedes gestempelte\nDokument kommt — genau in der Form, in der es gestempelt wurde — in den Nachweisspeicher\nim Sicherungsordner, zusammen mit seiner .beatproof-Datei. Dieser Speicher ist von den Versionen getrennt:\ndie Bereinigung alter Versionen rührt ihn nie an.',
    'Magazyn dowodów jest pusty.':
        'Der Nachweisspeicher ist leer.',
    'Na tym komputerze jest Sigelith Desktop: {count} {stamps}.':
        'Sigelith Desktop ist auf diesem Computer installiert: {count} {stamps}.',
    'Na tym komputerze nie ma danych Sigelith Desktop.':
        'Auf diesem Computer gibt es keine Daten von Sigelith Desktop.',
    'Otwórz folder dowodów':
        'Nachweisordner öffnen',
    'Oznakowano':
        'Gestempelt',
    'Pokazuje magazyn dowodów w Eksploratorze':
        'Zeigt den Nachweisspeicher im Datei-Explorer',
    'Przywróć zaznaczone…':
        'Ausgewählte wiederherstellen…',
    'Sigelith Desktop: {count} {stamps} w folderze {path}.':
        'Sigelith Desktop: {count} {stamps} im Ordner {path}.',
    'Sprawdza każdy dokument i jego dowód bez łączenia z siecią':
        'Prüft jedes Dokument und seinen Nachweis, ohne sich mit dem Netz zu verbinden',
    'Sprawdzam dowody…':
        'Nachweise werden geprüft…',
    'Stan':
        'Zustand',
    'Stemple w magazynie: {count}, z dokumentem: {documents}.':
        'Zeitstempel im Speicher: {count}, mit Dokument: {documents}.',
    'Suma dokumentu nie zgadza się z dowodem.':
        'Der Hash des Dokuments passt nicht zum Nachweis.',
    'To nie jest plik dowodu Sigelith (beatproof-v1).':
        'Das ist keine Sigelith-Nachweisdatei (beatproof-v1).',
    'Tydzień stempla jeszcze się nie zamknął — podpis dojdzie przy kolejnej kopii.':
        'Die Woche des Zeitstempels ist noch nicht abgeschlossen — die Signatur kommt bei einer späteren Sicherung hinzu.',
    'W magazynie nie ma dokumentu do tego dowodu.':
        'Im Speicher gibt es kein Dokument zu diesem Nachweis.',
    'Wszystkie dowody pasują do dokumentów i mają poprawny podpis.':
        'Alle Nachweise passen zu ihren Dokumenten und haben eine gültige Signatur.',
    'Zabezpieczam dokumenty oznakowane w Sigelith…':
        'In Sigelith gestempelte Dokumente werden gesichert…',
    'Zapisano pliki: {count} w {path}.':
        'Dateien gespeichert: {count} in {path}.',
    'Zapisuje dokumenty razem z plikami .beatproof we wskazanym folderze':
        'Speichert die Dokumente samt ihren .beatproof-Dateien in einem Ordner deiner Wahl',
    'bez dokumentu — dowód zachowany':
        'ohne Dokument — Nachweis erhalten',
    'czekają na podpis tygodnia: {count}':
        'warten auf die Wochensignatur: {count}',
    'dokument i dowód są w kopii':
        'Dokument und Nachweis sind in der Sicherung',
    'dokument jest; dowód czeka na podpis tygodnia':
        'Dokument vorhanden; Nachweis wartet auf die Wochensignatur',
    'dowodu nie da się odczytać':
        'Nachweis nicht lesbar',
    'dowody Sigelith':
        'Sigelith-Nachweise',
    'dowody uzupełnione o podpis tygodnia: {count}':
        'um die Wochensignatur ergänzte Nachweise: {count}',
    'nowe: {count}':
        'neu: {count}',
    'odtworzone ze starszych wersji kopii: {count}':
        'aus älteren Sicherungsversionen wiederhergestellt: {count}',
    'sprawdzony: dokument i dowód się zgadzają':
        'geprüft: Dokument und Nachweis stimmen überein',
    'stempel':
        'Zeitstempel',
    'stemple':
        'Zeitstempel',
    'stempli':
        'Zeitstempel',
    'zaszyfrowany — podaj hasło, żeby sprawdzić':
        'verschlüsselt — gib das Passwort ein, um zu prüfen',
    'Chroń dowody Sigelith, gdy go zainstaluję':
        'Sigelith-Nachweise schützen, sobald ich Sigelith Desktop installiere',
    'Dowody Sigelith: na tym komputerze nie ma jeszcze Sigelith Desktop — ochrona zacznie działać sama, gdy się pojawi.':
        'Sigelith-Nachweise: Sigelith Desktop ist auf diesem Computer noch nicht installiert — der Schutz beginnt von selbst, sobald es da ist.',
    'Dowody Sigelith: ochrona zacznie działać sama, gdy zainstalujesz Sigelith Desktop.':
        'Sigelith-Nachweise: Der Schutz beginnt von selbst, sobald du Sigelith Desktop installierst.',
    'Dowody czasu dla ważnych dokumentów':
        'Zeitnachweise für wichtige Dokumente',
    'Kopia zachowa każdy dokument oznakowany w Sigelith Desktop dokładnie w tej postaci, którą oznakowano, razem z dowodem — nawet gdy oryginał później się zmieni.':
        'Die Sicherung bewahrt jedes in Sigelith Desktop gestempelte Dokument genau so auf, wie es gestempelt wurde, samt Nachweis — auch wenn sich das Original später ändert.',
    'Ochrona zacznie działać sama, gdy na komputerze pojawi się Sigelith Desktop.':
        'Der Schutz beginnt von selbst, sobald Sigelith Desktop auf dem Computer installiert ist.',
    'Otwiera stronę programu Sigelith Desktop':
        'Öffnet die Seite von Sigelith Desktop',
    'Poznaj Sigelith Desktop':
        'Sigelith Desktop kennenlernen',
    'Sigelith Desktop, program tego samego wydawcy, oznakuje dokument czasem: to podpisany dowód, że plik w tej postaci istniał w danej chwili, sprawdzalny bez udziału kogokolwiek. Sigelith Backup przechowa potem każdy oznakowany dokument razem z dowodem.':
        'Sigelith Desktop, ein Programm desselben Herausgebers, versieht ein Dokument mit einem Zeitstempel: einem signierten Nachweis, dass die Datei in genau dieser Form zu einem bestimmten Zeitpunkt existierte, prüfbar, ohne jemandem vertrauen zu müssen. Sigelith Backup bewahrt dann jedes gestempelte Dokument samt Nachweis auf.',
    'Umowy, faktury, projekty — czasem trzeba wykazać, że dokument istniał danego dnia.':
        'Verträge, Rechnungen, Projekte — manchmal muss man belegen, dass ein Dokument an einem bestimmten Tag existierte.',
    'Nieznany format spisu wersji.':
        'Unbekanntes Format der Dateiliste der Version.',
    'Ta wersja nie ma pieczęci dla pojedynczych plików (kopia sprzed wersji 3.0 albo bez znaczników czasu).':
        'Diese Version hat kein Siegel für einzelne Dateien (Sicherung aus der Zeit vor Version 3.0 oder ohne Zeitstempel).',
    'Pieczęć tej wersji czeka jeszcze na podpis tygodnia Sigelith — dowód będzie gotowy po poniedziałku 00:00 UTC i kolejnej kopii.':
        'Das Siegel dieser Version wartet noch auf die Sigelith-Wochensignatur — der Nachweis ist nach Montag 00:00 UTC und der nächsten Sicherung fertig.',
    'Brak oświadczenia pieczęci w folderze wersji.':
        'Die Siegelerklärung fehlt im Ordner der Version.',
    'Oświadczenie pieczęci nie zgadza się z pieczęcią wersji.':
        'Die Siegelerklärung passt nicht zum Siegel der Version.',
    'Drzewo plików wersji nie zgadza się z pieczęcią.':
        'Der Dateibaum der Version passt nicht zum Siegel.',
    'Tego pliku nie ma w spisie tej wersji.':
        'Diese Datei steht nicht in der Dateiliste dieser Version.',
    'To nie jest dowód pliku z kopii Sigelith Backup ({format}).':
        'Das ist kein Dateinachweis aus Sigelith Backup ({format}).',
    'Dowód jest uszkodzony — brakuje pól albo mają zły format.':
        'Der Nachweis ist beschädigt — Felder fehlen oder haben ein falsches Format.',
    'Ten plik nie jest plikiem, którego dotyczy dowód.':
        'Diese Datei ist nicht die Datei, auf die sich der Nachweis bezieht.',
    'Ścieżka pliku w dowodzie nie zgadza się z liściem drzewa.':
        'Der Dateipfad im Nachweis passt nicht zum Blatt des Dateibaums.',
    'Droga w drzewie plików nie prowadzi do korzenia z pieczęci.':
        'Der Pfad im Dateibaum führt nicht zur versiegelten Wurzel.',
    'Oświadczenie pieczęci nie potwierdza tego drzewa plików.':
        'Die Siegelerklärung bestätigt diesen Dateibaum nicht.',
    'Potwierdzenie Sigelith nie dotyczy tej pieczęci.':
        'Die Sigelith-Bestätigung betrifft nicht dieses Siegel.',
    'Dowód czasu…':
        'Zeitnachweis…',
    'Zapisuje dowód, że ten plik był w kopii w chwili jej oznakowania — bez ujawniania innych plików':
        'Speichert einen Nachweis, dass diese Datei zum Zeitpunkt des Zeitstempels in der Sicherung war — ohne andere Dateien preiszugeben',
    'Dowód czasu':
        'Zeitnachweis',
    'Dołączyć do dowodu ścieżkę pliku w kopii („{path}”)?\n\nBez niej dowód dalej potwierdza plik i chwilę oznakowania, ale nie mówi, gdzie plik leżał.':
        'Den Pfad der Datei in der Sicherung („{path}“) in den Nachweis aufnehmen?\n\nOhne ihn bestätigt der Nachweis weiterhin die Datei und den Zeitpunkt des Zeitstempels, sagt aber nicht, wo die Datei lag.',
    'Przygotowuję dowód dla „{name}”…':
        'Nachweis für „{name}“ wird vorbereitet…',
    'Zapisz dowód czasu':
        'Zeitnachweis speichern',
    'Dowód pliku Sigelith (*{suffix})':
        'Sigelith-Dateinachweis (*{suffix})',
    'Zapisano dowód i certyfikat PDF: {path}. Sprawdzi go Sigelith Desktop albo strona sigelith.org/verify/.':
        'Nachweis und PDF-Zertifikat gespeichert: {path}. Prüfen lässt sich der Nachweis in Sigelith Desktop oder auf sigelith.org/verify/.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją sprawdzić.':
        'Die Sicherung ist verschlüsselt — gib das Passwort ein, um sie zu prüfen.',
    'Ta wersja nie ma pieczęci — nie ma z czym porównać plików.':
        'Diese Version hat kein Siegel — es gibt nichts, womit sich die Dateien vergleichen ließen.',
    'Pieczęć wersji się nie potwierdza: {problems}':
        'Das Siegel der Version ist nicht stimmig: {problems}',
    'brak podpisu tygodnia':
        'keine Wochensignatur',
    'Audyt przerwany.':
        'Inhaltsprüfung abgebrochen.',
    'próbka {checked} z {listed} plików':
        'Stichprobe von {checked} aus {listed} Dateien',
    'wszystkie pliki ({count})':
        'alle Dateien ({count})',
    'Nietknięta: sprawdzono {scope}, wszystko zgodne z pieczęcią w publicznym dzienniku.':
        'Unversehrt: {scope} geprüft, alles stimmt mit dem Siegel im öffentlichen Log überein.',
    'zmienione: {files}':
        'geändert: {files}',
    'brakujące: {files}':
        'fehlend: {files}',
    'nieczytelne albo uszkodzone: {files}':
        'unlesbar oder beschädigt: {files}',
    'PODMIENIONA albo uszkodzona ({scope}) — {details}.':
        'MANIPULIERT oder beschädigt ({scope}) — {details}.',
    'Audyt treści':
        'Inhaltsprüfung',
    'Czyta z nośnika każdy plik tej wersji i porównuje go z sumą oznakowaną w publicznym dzienniku':
        'Liest jede Datei dieser Version vom Datenträger und vergleicht sie mit dem im öffentlichen Log versiegelten Hash',
    'Ostatnia nietknięta':
        'Letzte unversehrte Version',
    'Sprawdza wersje od najnowszej i wskazuje ostatnią zgodną z pieczęcią — z niej przywracaj':
        'Prüft die Versionen ab der neuesten und zeigt die letzte, die zu ihrem Siegel passt — aus ihr wiederherstellen',
    'Ostatnia nietknięta wersja: {label} — z niej przywracaj.':
        'Letzte unversehrte Version: {label} — stelle aus ihr wieder her.',
    'Żadna wersja z pieczęcią nie jest nietknięta.':
        'Keine versiegelte Version ist unversehrt.',
    'Czytam pliki kopii i porównuję je z pieczęcią w publicznym dzienniku…':
        'Die Dateien der Sicherung werden gelesen und mit dem Siegel im öffentlichen Log verglichen…',
    'Sprawdzam próbkę starszej wersji z pieczęcią w publicznym dzienniku…':
        'Eine Stichprobe einer älteren Version wird mit ihrem Siegel im öffentlichen Log verglichen…',
    'Audyt z pieczęcią: próbka wersji {label} zgodna z publicznym dziennikiem.':
        'Siegelprüfung: Die Stichprobe der Version {label} stimmt mit dem öffentlichen Log überein.',
    'UWAGA — audyt z pieczęcią, wersja {label}: {details}':
        'WARNUNG — Siegelprüfung, Version {label}: {details}',
    'Przekaż…':
        'Übergeben…',
    'Zapisuje tę wersję pliku i otwiera ją w Sigelith Handover — odbiorca potwierdzi odbiór własnym kluczem':
        'Speichert diese Version der Datei und öffnet sie in Sigelith Handover — der Empfänger bestätigt den Erhalt mit seinem eigenen Schlüssel',
    'Przekazanie z dowodem doręczenia':
        'Mit Übergabenachweis übergeben',
    'Przekazanie z dowodem doręczenia robi Sigelith Desktop (od wersji 3.0.1): odbiorca potwierdza odbiór własnym kluczem, a chwila doręczenia trafia do publicznego dziennika. Na tym komputerze go nie ma albo jest w starszej wersji. Otworzyć stronę programu?':
        'Die Übergabe mit Übergabenachweis übernimmt Sigelith Desktop (ab Version 3.0.1): Der Empfänger bestätigt den Erhalt mit seinem eigenen Schlüssel, und der Zeitpunkt der Übergabe wird im öffentlichen Log festgehalten. Auf diesem Computer ist es nicht installiert oder nur in einer älteren Version. Die Seite des Programms öffnen?',
    'Zapisz plik do przekazania':
        'Datei für die Übergabe speichern',
    'Otwieram Sigelith Handover z plikiem „{name}” — wybierz odbiorcę.':
        'Sigelith Handover wird mit „{name}“ geöffnet — wähle den Empfänger.',
    'Kapsuły czasu…':
        'Zeitkapseln…',
    'Pliki zapieczętowane w tej kopii do daty — klucze wydają dopiero po niej sieć drand i serwer kluczy Sigelith':
        'Dateien, die in dieser Sicherung bis zu einem Datum versiegelt sind — die Schlüssel geben das drand-Netzwerk und der Sigelith-Schlüsselserver erst danach frei',
    'Wskaż najpierw folder kopii — kapsuła leży w kopii.':
        'Wähle zuerst den Sicherungsordner — die Kapsel liegt in der Sicherung.',
    'Kapsuły czasu':
        'Zeitkapseln',
    'Kapsuła pieczętuje wybrany folder do chwili, którą wskażesz. Otwierają ją dowolne dwie z trzech części: runda sieci drand z tej chwili, udział serwera kluczy Sigelith (wydawany dopiero po tej chwili — to zasada operatora, nie kryptografia) i kod odzyskiwania zapisany obok kapsuły. Kto ma tę kopię, ma więc i kod: do wcześniejszego otwarcia wystarczy mu, że operator złamie swoją zasadę. Po tej chwili otworzy ją każdy, kto ma jej pliki. Kapsuła leży w tej kopii, nie na serwerze; otwiera ją strona sigelith.org/capsule/.':
        'Die Kapsel versiegelt den gewählten Ordner bis zu dem Moment, den du festlegst. Zwei beliebige von drei Teilen öffnen sie: die drand-Runde für diesen Moment, der Anteil des Sigelith-Schlüsselservers (erst nach diesem Moment freigegeben — eine Regel des Betreibers, keine Kryptografie) und der Wiederherstellungscode, der neben der Kapsel gespeichert ist. Wer diese Sicherung hat, hat also auch den Code: Für ein vorzeitiges Öffnen braucht er nur noch, dass der Betreiber seine Regel bricht. Nach diesem Moment kann sie jeder öffnen, der ihre Dateien hat. Die Kapsel liegt in dieser Sicherung, nicht auf einem Server; geöffnet wird sie auf der Seite sigelith.org/capsule/.',
    'Wybierz kapsułę z listy albo utwórz nową.':
        'Wähle eine Kapsel aus der Liste oder erstelle eine neue.',
    'Nowa kapsuła…':
        'Neue Kapsel…',
    'Pieczętuje wybrany folder do daty':
        'Versiegelt einen gewählten Ordner bis zu einem Datum',
    'Pokaż w folderze':
        'Im Ordner anzeigen',
    'Otwiera folder kapsuły w Eksploratorze':
        'Öffnet den Ordner der Kapsel im Datei-Explorer',
    'Otwórz na stronie':
        'Auf der Website öffnen',
    'Strona sigelith.org/capsule/ otwiera kapsułę po jej dacie':
        'Die Seite sigelith.org/capsule/ öffnet die Kapsel nach ihrem Datum',
    'można otworzyć':
        'kann geöffnet werden',
    'zamknięta':
        'versiegelt',
    'W tej kopii nie ma jeszcze kapsuł czasu.':
        'In dieser Sicherung gibt es noch keine Zeitkapseln.',
    'Ta kapsuła da się otworzyć na stronie sigelith.org/capsule/ — wskaż jej pliki.':
        'Diese Kapsel lässt sich auf der Seite sigelith.org/capsule/ öffnen — wähle dort ihre Dateien.',
    'Kapsuła jest zamknięta do daty z listy. Kod odzyskiwania leży w pliku obok niej.':
        'Die Kapsel ist bis zum Datum in der Liste versiegelt. Der Wiederherstellungscode liegt in einer Datei neben ihr.',
    'Wybierz folder do zapieczętowania':
        'Ordner zum Versiegeln wählen',
    'Pieczętuję „{name}” — kilka sekund na krzywej eliptycznej…':
        '„{name}“ wird versiegelt — ein paar Sekunden auf der elliptischen Kurve…',
    'kapsuła czasu':
        'Zeitkapsel',
    'Kapsuła zapieczętowana':
        'Kapsel versiegelt',
    '„{name}” otworzy się najwcześniej {when}.\n\nKod odzyskiwania (skopiowany do schowka, zapisany też obok kapsuły):\n\n{code}\n\nZapisz go w bezpiecznym miejscu. Przed datą otwarcia sam niczego nie otwiera; po niej zastępuje jeden z kluczy, gdyby był niedostępny.':
        '„{name}“ öffnet sich frühestens am {when}.\n\nWiederherstellungscode (in die Zwischenablage kopiert, auch neben der Kapsel gespeichert):\n\n{code}\n\nBewahre ihn an einem sicheren Ort auf. Vor dem Öffnungsdatum öffnet er allein nichts; danach ersetzt er einen der Schlüssel, falls einer nicht verfügbar ist.',
    'Nie udało się zapieczętować: {error}':
        'Versiegeln fehlgeschlagen: {error}',
    'Nowa kapsuła czasu':
        'Neue Zeitkapsel',
    'Otworzy się najwcześniej':
        'Öffnet sich frühestens am',
    'kapsuła':
        'Kapsel',
    'Chwila otwarcia musi być w przyszłości.':
        'Der Öffnungszeitpunkt muss in der Zukunft liegen.',
    'Na bieżąco':
        'Laufend',
    'Zmiany w folderach źródłowych trafiają do dzisiejszej wersji kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje. Jedna wersja na dzień; ze znacznikami czasu zamyka ją pieczęć następnego dnia.':
        'Änderungen in den Quellordnern kommen wenige Minuten nach dem Speichern in die heutige Sicherungsversion, und beim Anschließen des Laufwerks wird die Sicherung sofort synchronisiert. Eine Version pro Tag; mit Zeitstempeln wird sie am nächsten Tag durch ein Siegel abgeschlossen.',
    'Na bieżąco — po każdej zmianie i po podłączeniu dysku':
        'Laufend — nach jeder Änderung und beim Anschließen des Laufwerks',
    'Dla dysku podłączonego na stałe albo często: zmiany trafiają do kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje.':
        'Für ein Laufwerk, das dauerhaft oder oft angeschlossen ist: Änderungen kommen wenige Minuten nach dem Speichern in die Sicherung, und beim Anschließen des Laufwerks wird die Sicherung sofort synchronisiert.',
    'Kopia będzie na bieżąco: zmiany trafią do dzisiejszej wersji kilka minut po zapisie, a po podłączeniu dysku kopia od razu się zsynchronizuje.':
        'Die Sicherung bleibt laufend aktuell: Änderungen kommen wenige Minuten nach dem Speichern in die heutige Version, und beim Anschließen des Laufwerks wird die Sicherung sofort synchronisiert.',
    'przywracanie':
        'Wiederherstellung',
}
