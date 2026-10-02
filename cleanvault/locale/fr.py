"""Katalog francuski: „polski tekst źródłowy” → „tekst (francuski)”.

Klucze są te same co w ``en.py`` i muszą dokładnie odpowiadać napisom w kodzie;
pilnuje tego ``tests/test_i18n.py``. Pola w nawiasach klamrowych (``{count}``)
zostają bez zmian. Formaty dat są te same co w Sigelith Desktop.
"""

from __future__ import annotations

TEXTS: dict[str, str] = {
    '\n\nLokalizacja:\n{path}':
        '\n\nEmplacement\xa0:\n{path}',
    '\nDo uzupełnienia: niedokończone kopie: {count} — możesz je uzupełnić, wybierając wersję poniżej.':
        '\nÀ compléter\xa0: sauvegardes inachevées\xa0: {count} — vous pouvez les compléter en choisissant une version ci-dessous.',
    '\nUwaga: duży klaster ({size}): każdy mały plik zajmuje co najmniej tyle miejsca. Przy wielu małych plikach kopia zajmie wielokrotnie więcej niż dane.':
        '\nAttention\xa0: cluster de grande taille ({size})\xa0: chaque petit fichier occupe au moins cet espace. Avec beaucoup de petits fichiers, la sauvegarde occupera plusieurs fois plus d’espace que les données elles-mêmes.',
    '\nUwaga: niedokończone wersje (nie zawierają wszystkich plików): {names}':
        '\nAttention\xa0: versions inachevées (elles ne contiennent pas tous les fichiers)\xa0: {names}',
    '\nUwaga: {filesystem} nie obsługuje twardych dowiązań — każda wersja z datą zajmuje tyle miejsca co pełna kopia.':
        '\nAttention\xa0: {filesystem} ne prend pas en charge les liens physiques — chaque version datée occupe autant d’espace qu’une copie complète.',
    ' wersji':
        ' versions',
    ' z szyfrowaniem AES-256-GCM…':
        ' avec chiffrement AES-256-GCM…',
    ' ×':
        ' ×',
    ' — a ponieważ {filesystem} nie obsługuje twardych dowiązań, zapisze ponownie wszystkie pliki i zajmie tyle miejsca co cała kopia':
        ' — et comme {filesystem} ne prend pas en charge les liens physiques, elle réécrira tous les fichiers et occupera autant d’espace que toute la sauvegarde',
    ' • pozostało {time}':
        ' • reste {time}',
    '%d.%m %H:%M':
        '%d/%m %H:%M',
    '%d.%m.%Y':
        '%d/%m/%Y',
    '%d.%m.%Y %H:%M':
        '%d/%m/%Y %H:%M',
    ', klaster {size}':
        ', cluster de {size}',
    ', uzupełniona {when}':
        ', complétée le {when}',
    'Analizuje pliki i pokazuje plan. Nic nie zapisuje.':
        'Analyse les fichiers et affiche le plan. N’écrit rien.',
    'Anulowano przed rozpoczęciem kopii.':
        'Annulé avant le début de la sauvegarde.',
    'Anuluj':
        'Annuler',
    'Argon2id (t={passes}, {memory} MiB, p={threads})':
        'Argon2id (t={passes}, {memory} MiB, p={threads})',
    'Argon2id — {passes} przebiegi, {memory} MiB, {threads} wątki':
        'Argon2id — {passes} passes, {memory} MiB, {threads} threads',
    'Automatycznie (język systemu)':
        'Automatique (langue du système)',
    'Bardzo dobre':
        'Très fort',
    'Bardzo słabe':
        'Très faible',
    'Brak manifestu — skanuję katalog kopii.':
        'Aucun manifeste — analyse du dossier de la sauvegarde.',
    'Brakuje tagu uwierzytelniającego — plik jest obcięty.':
        'Le tag d’authentification est absent — le fichier est tronqué.',
    'Błąd uruchamiania':
        'Erreur au démarrage',
    'Ciemny':
        'Sombre',
    'Co dokładnie zostanie zapisane przy najbliższym przebiegu.':
        'Ce qui sera écrit exactement lors de la prochaine exécution.',
    'Co kopiujemy':
        'Que sauvegarder',
    'Co zrobić, gdy plik o tej nazwie już istnieje w katalogu docelowym.':
        'Que faire lorsqu’un fichier portant ce nom existe déjà dans le dossier de destination.',
    'Czas w nazwie to BeatTime — 1000 beatów na dobę, kotwica w UTC, ten sam moment na całym świecie. Data jest datą UTC, więc zgadza się z zegarem.':
        'L’heure dans le nom est en BeatTime — 1000 beats par jour, ancrés sur UTC, le même instant partout dans le monde. La date est la date UTC, elle concorde donc avec l’horloge.',
    'Czym jest {app}':
        '{app} en quelques mots',
    'Czyści tylko okno — plik dziennika pozostaje':
        'Efface seulement la fenêtre — le fichier journal est conservé',
    'Dane aplikacji: {path}':
        'Données de l’application\xa0: {path}',
    'Decyduje, czy zachowujemy historię wersji.':
        'Détermine si l’historique des versions est conservé.',
    'Dobre':
        'Fort',
    'Dodaj folder':
        'Ajouter un dossier',
    'Dodaj przynajmniej jeden folder źródłowy.':
        'Ajoutez au moins un dossier source.',
    'Dogrywka zmian z czasu kopii:':
        'Rattrapage des modifications faites pendant la sauvegarde\xa0:',
    'Dokąd przywracamy':
        'Restaurer vers',
    'Dokładnie to, co program realnie stosuje.':
        'Exactement ce que le programme utilise réellement.',
    'Domyślne wykluczenia':
        'Exclusions par défaut',
    'Domyślne wykluczenia zapisane.':
        'Exclusions par défaut enregistrées.',
    'Domyślnie wyłączone. Przy włączonej opcji skasowanie pliku w źródle\nusuwa też jego jedyną kopię zapasową — operacja nieodwracalna.':
        'Désactivé par défaut. Avec cette option, supprimer un fichier de la source\nsupprime aussi sa seule copie de sauvegarde — opération irréversible.',
    'Dopisuj do nazwy katalogu datę ostatniego uzupełnienia':
        'Ajouter au nom du dossier la date du dernier complément',
    'Dziennik':
        'Journal',
    'Dziennik: {path}':
        'Journal\xa0: {path}',
    'Ekran przywracania wypełniony danymi szablonu.':
        'L’écran de restauration a été rempli à partir du modèle.',
    'Folder docelowy kopii — najlepiej na innym dysku fizycznym.':
        'Dossier de destination de la sauvegarde — idéalement sur un autre disque physique.',
    'Folder zawierający kopię utworzoną przez {app}.':
        'Un dossier contenant une sauvegarde créée par {app}.',
    'Gdy plik już istnieje:':
        'Si le fichier existe déjà\xa0:',
    'Gdzie zapisujemy':
        'Où enregistrer',
    'Gotowe do pracy.':
        'Prêt.',
    'Gotowe. Wybierz foldery do kopii.':
        'Prêt. Choisissez les dossiers à sauvegarder.',
    'Gotowe: {count} {files}, {size}, {seconds} s.':
        'Terminé\xa0: {count} {files}, {size}, {seconds} s.',
    'Główny folder kopii. Zawiera spis treści (.cleanvault-manifest).':
        'Le dossier principal de la sauvegarde. Il contient la table des matières (.cleanvault-manifest).',
    'Hasła nie da się odzyskać ani zresetować. Jeśli je zgubisz, dane z kopii zaszyfrowanej są bezpowrotnie stracone — tak działa poprawne szyfrowanie.':
        'Le mot de passe ne peut être ni récupéré ni réinitialisé. Si vous le perdez, les données d’une sauvegarde chiffrée sont perdues pour de bon — c’est ainsi que fonctionne un chiffrement correct.',
    'Hasła w obu polach różnią się.':
        'Les mots de passe des deux champs ne correspondent pas.',
    'Hasło':
        'Mot de passe',
    'Hasło do kopii':
        'Mot de passe de la sauvegarde',
    'Hasło nie jest nigdzie zapisywane w postaci jawnej.\nBez niego nie da się odzyskać danych — nie istnieje żadna furtka serwisowa.':
        'Le mot de passe n’est jamais enregistré en clair.\nSans lui, les données sont irrécupérables — il n’existe aucune porte dérobée.',
    'Hasło nie może być puste.':
        'Le mot de passe ne peut pas être vide.',
    'Hasło niezapisane':
        'Mot de passe non enregistré',
    'Hasło powinno mieć co najmniej 8 znaków.':
        'Le mot de passe doit comporter au moins 8 caractères.',
    'Hasło trafia do magazynu systemowego powiązanego z Twoim kontem.\nNigdy nie jest zapisywane w plikach programu.':
        'Le mot de passe est conservé dans le coffre du système, lié à votre compte.\nIl n’est jamais écrit dans les fichiers du programme.',
    'Hasło użyte przy tworzeniu kopii':
        'Mot de passe utilisé lors de la création de la sauvegarde',
    'Ile plików kopia przetwarza jednocześnie. Przy setkach tysięcy małych plików\nczas kopii to głównie opóźnienia na każdy plik (otwarcie, skanowanie\nantywirusowe, zapis na nośnik), a nie przesył danych — praca równoległa\nskraca go kilkukrotnie.\n\n„automatycznie” dobiera liczbę do procesora (do 32). Na wolnym dysku\ntalerzowym mniejsza wartość (2–4) bywa szybsza.':
        'Nombre de fichiers que la sauvegarde traite simultanément. Avec des centaines de milliers\nde petits fichiers, la durée dépend surtout du délai propre à chaque fichier (ouverture,\nanalyse antivirus, écriture sur le support) et non du transfert des données — le travail\nen parallèle la rend plusieurs fois plus courte.\n\n«\xa0automatique\xa0» adapte ce nombre au processeur (jusqu’à 32). Sur un disque dur\nà plateaux lent, une valeur plus petite (2–4) est souvent plus rapide.',
    'Informacje przydatne przy zgłaszaniu problemu.':
        'Informations utiles pour signaler un problème.',
    'Jak to działa':
        'Fonctionnement',
    'Jasny':
        'Clair',
    'Jeden folder utrzymywany w zgodzie ze źródłem. Brak historii wersji,\nza to najprostsza struktura i najmniejsze zużycie miejsca.':
        'Un seul dossier tenu en phase avec la source. Pas d’historique des versions,\nmais la structure la plus simple et l’encombrement le plus faible.',
    'Jeśli operacja zakończy się błędem, skopiuj stąd ostatnie wiersze — zawierają dokładną przyczynę, a nie tylko komunikat ogólny.':
        'Si une opération se termine par une erreur, copiez les dernières lignes affichées ici — elles indiquent la cause exacte, pas seulement un message général.',
    'Język interfejsu zmieniony.':
        'Langue de l’interface modifiée.',
    'Język zmienisz po zakończeniu bieżącej operacji.':
        'Vous pourrez changer de langue une fois l’opération en cours terminée.',
    'Język:':
        'Langue\xa0:',
    'Katalog docelowy leży wewnątrz źródła ({path}). Kopia kopiowałaby samą siebie w nieskończoność.':
        'Le dossier de destination se trouve à l’intérieur de la source ({path}). La sauvegarde se copierait elle-même à l’infini.',
    'Katalog docelowy nie może być tym samym katalogiem co źródłowy.':
        'Le dossier de destination ne peut pas être le même que le dossier source.',
    'Katalog jeszcze nie istnieje — zostanie utworzony.':
        'Le dossier n’existe pas encore — il sera créé.',
    'Katalog kopii nie istnieje: {path}':
        'Le dossier de la sauvegarde n’existe pas\xa0: {path}',
    'Katalog źródłowy nie istnieje: {path}':
        'Le dossier source n’existe pas\xa0: {path}',
    'Katalog, w którym pojawią się odtworzone pliki.':
        'Le dossier où apparaîtront les fichiers restaurés.',
    'Katalog, w którym powstanie kopia. Nie może leżeć wewnątrz folderu źródłowego.':
        'Le dossier où sera créée la sauvegarde. Il ne doit pas se trouver dans un dossier source.',
    'Katalogi objęte kopią.\nMożesz przeciągnąć foldery z Eksploratora Windows wprost na tę listę.':
        'Dossiers inclus dans la sauvegarde.\nVous pouvez glisser des dossiers depuis l’Explorateur de fichiers directement sur cette liste.',
    'Każdy folder z datą jest kompletny — przywracanie nie wymaga sklejania wersji.':
        'Chaque dossier daté est complet — la restauration n’exige jamais de recoller des versions.',
    'Każdy plik jest czytany ponownie zaraz po zapisaniu. Dane pochodzą wtedy\nzwykle z pamięci podręcznej systemu, więc niewiele mówi to o nośniku,\na wydłuża kopię nawet dwukrotnie.\n\nSkuteczniejsza jest weryfikacja odroczona: ekran „Przywracanie” →\n„Sprawdź kopię”, najlepiej po ponownym podłączeniu dysku.':
        'Chaque fichier est relu juste après son écriture. Les données viennent alors\ngénéralement du cache du système\xa0: cela renseigne donc peu sur le support,\net peut doubler la durée de la sauvegarde.\n\nUne vérification différée est plus efficace\xa0: écran «\xa0Restauration\xa0» →\n«\xa0Vérifier la sauvegarde\xa0», idéalement après avoir rebranché le disque.',
    'Każdy plik trafia do kopii jako zaszyfrowany kontener .cvlt.\nKlucz powstaje z hasła przez Argon2id.':
        'Chaque fichier entre dans la sauvegarde sous forme de conteneur chiffré .cvlt.\nLa clé est dérivée du mot de passe par Argon2id.',
    'Każdy przebieg tworzy osobny folder z datą i godziną.\nPliki niezmienione są podpinane twardym dowiązaniem, więc historia\nzajmuje tyle miejsca, ile realnie się zmieniło.':
        'Chaque exécution crée son propre dossier avec la date et l’heure.\nLes fichiers inchangés y sont rattachés par un lien physique\xa0: l’historique\nn’occupe donc que l’espace de ce qui a réellement changé.',
    'Klaster nośnika to {cluster} — pliki zajmą {actual} zamiast {logical} (narzut {overhead}).':
        'Le cluster du support est de {cluster} — les fichiers occuperont {actual} au lieu de {logical} (surcoût {overhead}).',
    'Kliknij szablon, aby zobaczyć jego szczegóły.':
        'Cliquez sur un modèle pour en voir les détails.',
    'Kliknij „Podgląd zmian”, aby sprawdzić plan bez zapisywania czegokolwiek.':
        'Cliquez sur «\xa0Aperçu des modifications\xa0» pour vérifier le plan sans rien écrire.',
    'Kolor wyróżnienia':
        'Couleur d’accentuation',
    'Kolor wyróżnienia…':
        'Couleur d’accentuation…',
    'Kopia':
        'Sauvegarde',
    'Kopia do dokończenia':
        'Sauvegarde à terminer',
    'Kopia jest aktualna — nie ma czego zapisywać.':
        'La sauvegarde est à jour — il n’y a rien à écrire.',
    'Kopia jest zaszyfrowana — podaj hasło użyte przy jej tworzeniu.':
        'La sauvegarde est chiffrée — saisissez le mot de passe utilisé lors de sa création.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją przywrócić.':
        'La sauvegarde est chiffrée — saisissez le mot de passe pour la restaurer.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją zweryfikować.':
        'La sauvegarde est chiffrée — saisissez le mot de passe pour la vérifier.',
    'Kopia jest zaszyfrowana — podaj hasło.':
        'La sauvegarde est chiffrée — saisissez le mot de passe.',
    'Kopia lustrzana':
        'Copie miroir',
    'Kopia nie została uruchomiona.':
        'La sauvegarde n’a pas été lancée.',
    'Kopia wykonana. Uruchom podgląd ponownie, aby sprawdzić stan.':
        'Sauvegarde effectuée. Relancez l’aperçu pour vérifier l’état.',
    'Kopia zapasowa':
        'Sauvegarde',
    'Kopia {folder}':
        'Sauvegarde de {folder}',
    'Kopia {kind} • {count} {files} • {size} • ostatnia aktualizacja {when}\nŹródła: {roots}':
        'Sauvegarde {kind} • {count} {files} • {size} • dernière mise à jour le {when}\nSources\xa0: {roots}',
    'Kopiowane są wyłącznie pliki nowe i zmienione od ostatniego przebiegu.':
        'Seuls les fichiers nouveaux ou modifiés depuis la dernière exécution sont copiés.',
    'Kopiuje ustawienia szablonu na ekran „Kopia zapasowa”':
        'Copie les réglages du modèle sur l’écran «\xa0Sauvegarde\xa0»',
    'Kopię możesz sprawdzić później: ekran „Przywracanie” → „Sprawdź kopię”. Najlepiej po ponownym podłączeniu dysku — wtedy dane są czytane z nośnika.':
        'Vous pourrez vérifier la sauvegarde plus tard\xa0: écran «\xa0Restauration\xa0» → «\xa0Vérifier la sauvegarde\xa0». Idéalement après avoir rebranché le disque — les données sont alors vraiment lues sur le support.',
    'Kryptografia':
        'Cryptographie',
    'Lista podpowiadana przy tworzeniu nowej kopii.':
        'La liste proposée lors de la création d’une nouvelle sauvegarde.',
    'Magazyn haseł: {backend}':
        'Coffre des mots de passe\xa0: {backend}',
    'Magazyn systemowy: {backend}':
        'Coffre du système\xa0: {backend}',
    'Menedżer poświadczeń Windows (DPAPI, powiązany z kontem użytkownika).':
        'Gestionnaire d’identification Windows (DPAPI, lié à votre compte utilisateur).',
    'Miejsce i układ odtwarzanych plików.':
        'Emplacement et disposition des fichiers restaurés.',
    'Motyw zmieniony na {theme}.':
        'Thème modifié\xa0: {theme}.',
    'Motyw:':
        'Thème\xa0:',
    'Możesz też przeciągnąć foldery z Eksploratora Windows wprost na listę.':
        'Vous pouvez aussi glisser des dossiers depuis l’Explorateur de fichiers directement sur la liste.',
    'Można ją dokończyć — zostaną dograne tylko brakujące i zmienione pliki.':
        'Elle peut être terminée — seuls les fichiers manquants et modifiés seront ajoutés.',
    'Na nośniku docelowym zajmie to ok. {size}.':
        'Sur le support de destination, cela occupera environ {size}.',
    'Nadpisywanie plików':
        'Remplacement des fichiers',
    'Nadpisz istniejące pliki':
        'Remplacer les fichiers existants',
    'Nazwa szablonu':
        'Nom du modèle',
    'Nazwa szablonu nie może być pusta.':
        'Le nom du modèle ne peut pas être vide.',
    'Nazwa szablonu zapisana.':
        'Nom du modèle enregistré.',
    'Nazwa szablonu:':
        'Nom du modèle\xa0:',
    'Nie ma wersji kopii o nazwie {name} w katalogu {path}.':
        'Aucune version de sauvegarde nommée {name} dans le dossier {path}.',
    'Nie można odczytać informacji o dysku: {error}':
        'Impossible de lire les informations du disque\xa0: {error}',
    'Nie udało się uruchomić programu — brakuje biblioteki: {error}\nZainstaluj zależności poleceniem:  pip install -r requirements.txt':
        'Le programme n’a pas pu démarrer — une bibliothèque est manquante\xa0: {error}\nInstallez les dépendances avec la commande\xa0:  pip install -r requirements.txt',
    'Nie udało się wykonać operacji':
        'L’opération n’a pas pu être effectuée',
    'Nie udało się zapisać hasła w magazynie systemowym.\nSzablon działa normalnie — program poprosi o hasło przy uruchomieniu.':
        'Impossible d’enregistrer le mot de passe dans le coffre du système.\nLe modèle fonctionne normalement — le programme demandera le mot de passe à l’exécution.',
    'Nie udało się znaleźć wolnej nazwy dla {path}':
        'Impossible de trouver un nom libre pour {path}',
    'Nie wskazano katalogu docelowego.':
        'Aucun dossier de destination indiqué.',
    'Nie wskazano żadnego katalogu źródłowego.':
        'Aucun dossier source indiqué.',
    'Nie wybrano katalogu':
        'Aucun dossier choisi',
    'Nie wybrano szablonu':
        'Aucun modèle sélectionné',
    'Nie znaleziono spisu treści kopii — program przeskanuje folder i rozpozna pliki po ich zawartości.':
        'Table des matières de la sauvegarde introuvable — le programme analysera le dossier et reconnaîtra les fichiers à leur contenu.',
    'Nie znam oryginalnej lokalizacji dla {key} — wybierz inny układ przywracania.':
        'L’emplacement d’origine de {key} est inconnu — choisissez une autre disposition de restauration.',
    'Niedostępny — backend {backend} nie gwarantuje poufności.':
        'Indisponible — le backend {backend} ne garantit pas la confidentialité.',
    'Niedostępny — brak biblioteki keyring.':
        'Indisponible — la bibliothèque keyring est absente.',
    'Nieznany algorytm wyprowadzania klucza: {name}':
        'Algorithme de dérivation de clé inconnu\xa0: {name}',
    'Nowa wersja z datą':
        'Nouvelle version datée',
    'Nowa wersja z datą to kopia od początku do osobnego folderu':
        'Une nouvelle version datée signifie tout recopier depuis le début dans un dossier distinct',
    'Nowa wersja z datą — kopia do nowego folderu.\nWybrana istniejąca wersja — dogrywa do niej tylko brakujące i zmienione\npliki, a pliki różniące się od źródła nadpisuje. Tak dokończysz przerwaną\nkopię albo uzupełnisz ją o dane, które powstały w trakcie jej wykonywania.':
        'Nouvelle version datée — une sauvegarde dans un nouveau dossier.\nVersion existante choisie — seuls les fichiers manquants et modifiés y sont ajoutés,\net les fichiers qui diffèrent de la source sont remplacés. C’est ainsi que vous terminez\nune sauvegarde interrompue ou la complétez avec les données créées pendant son exécution.',
    'Nowy szablon':
        'Nouveau modèle',
    'Nośnik docelowy ({filesystem}) nie obsługuje twardych dowiązań, więc każda wersja z datą jest pełną kopią. Te {count} niezmienionych plików zostanie powielone ({size}). Rozważ układ „kopia lustrzana” albo nośnik NTFS.':
        'Le support de destination ({filesystem}) ne prend pas en charge les liens physiques\xa0: chaque version datée est donc une copie complète. Les {count} fichiers inchangés seront dupliqués ({size}). Envisagez le mode «\xa0copie miroir\xa0» ou un support NTFS.',
    'O programie':
        'À propos',
    'Obsługiwane są wzorce w stylu Windows:\n  *.tmp          — wszystkie pliki tymczasowe\n  Thumbs.db      — konkretna nazwa\n  node_modules/* — cały folder wraz z zawartością':
        'Les motifs de style Windows sont pris en charge\xa0:\n  *.tmp          — tous les fichiers temporaires\n  Thumbs.db      — un nom précis\n  node_modules/* — un dossier entier avec son contenu',
    'Ochrona danych':
        'Protection des données',
    'Odczytuje wszystkie pliki kopii i weryfikuje ich poprawność.\nNic nie zapisuje na dysku.':
        'Lit tous les fichiers de la sauvegarde et vérifie leur intégrité.\nN’écrit rien sur le disque.',
    'Odpowiednik synchronizacji folderu. Wcześniejsze wersje plików nie są zachowywane.':
        'L’équivalent d’une synchronisation de dossier. Les versions antérieures des fichiers ne sont pas conservées.',
    'Odtwarza pliki z kopii — również z kopii zaszyfrowanej.':
        'Restaure des fichiers à partir d’une sauvegarde — y compris chiffrée.',
    'Odtwarza pliki zgodnie z ustawieniami powyżej':
        'Restaure les fichiers selon les réglages ci-dessus',
    'Odtwórz pełną strukturę folderów':
        'Recréer toute l’arborescence des dossiers',
    'Odtwórz pliki z istniejącej kopii':
        'Restaurer des fichiers d’une sauvegarde existante',
    'Operacja nie powiodła się.':
        'L’opération a échoué.',
    'Operacja przerwana przez użytkownika.':
        'Opération annulée par l’utilisateur.',
    'Operacja przerwana — utrwalam stan dotychczas zapisanych plików.':
        'Opération interrompue — enregistrement de l’état des fichiers écrits jusqu’ici.',
    'Operacja w toku':
        'Opération en cours',
    'Operacja zakończona błędem.':
        'L’opération s’est terminée par une erreur.',
    'Ostatnie operacje':
        'Opérations récentes',
    'Otwiera ekran przywracania z wypełnionymi ścieżkami':
        'Ouvre l’écran de restauration avec les chemins déjà remplis',
    'Otwiera pełny dziennik w domyślnym edytorze':
        'Ouvre le journal complet dans l’éditeur par défaut',
    'Otwórz katalog danych':
        'Ouvrir le dossier des données',
    'Otwórz katalog dziennika':
        'Ouvrir le dossier du journal',
    'Otwórz okno wyboru katalogu':
        'Ouvrir la fenêtre de choix du dossier',
    'Otwórz plik dziennika':
        'Ouvrir le fichier journal',
    'PBKDF2-HMAC-SHA256 ({count} iteracji)':
        'PBKDF2-HMAC-SHA256 ({count} itérations)',
    'PBKDF2-HMAC-SHA256 — {count} iteracji':
        'PBKDF2-HMAC-SHA256 — {count} itérations',
    'PBKDF2-HMAC-SHA256, {count} iteracji':
        'PBKDF2-HMAC-SHA256, {count} itérations',
    'Pełna struktura — układ jak w źródle, wewnątrz wskazanego katalogu.\nJeden folder — wygodne, gdy szukasz kilku plików.\nPierwotne lokalizacje — zapisuje pliki tam, skąd zostały pobrane.':
        'Arborescence complète — disposition identique à la source, dans le dossier choisi.\nUn seul dossier — pratique quand vous cherchez quelques fichiers.\nEmplacements d’origine — réécrit les fichiers là d’où ils viennent.',
    'Pierwszy przebieg kopiuje wszystko i trwa najdłużej. Kolejne porównują rozmiar i datę modyfikacji, więc zwykle kończą się w kilka sekund.':
        'La première exécution copie tout et dure le plus longtemps. Les suivantes comparent la taille et la date de modification, et se terminent donc généralement en quelques secondes.',
    'Plan gotowy: {count} {files} do zapisania.':
        'Plan prêt\xa0: {count} {files} à écrire.',
    'Plik jest za krótki, by być kontenerem tego programu.':
        'Le fichier est trop court pour être un conteneur de ce programme.',
    'Plik skończył się wcześniej, niż deklaruje nagłówek.':
        'Le fichier se termine plus tôt que ne l’indique son en-tête.',
    'Plik w formacie w wersji {found}; ta wersja programu obsługuje {supported}.':
        'Le fichier utilise la version {found} du format\xa0; cette version du programme prend en charge {supported}.',
    'Plik wymaga Argon2id, a biblioteka argon2-cffi jest niedostępna.':
        'Le fichier nécessite Argon2id, mais la bibliothèque argon2-cffi n’est pas disponible.',
    'Pliki pominięte — kopia jest aktualna':
        'Fichiers ignorés — la sauvegarde est à jour',
    'Pliki trafią do wskazanego katalogu z zachowaniem struktury folderów.':
        'Les fichiers iront dans le dossier choisi, en conservant l’arborescence des dossiers.',
    'Pliki wrócą dokładnie tam, skąd pochodzą. Katalog docelowy zostanie zignorowany.':
        'Les fichiers retourneront exactement là d’où ils viennent. Le dossier de destination sera ignoré.',
    'Pliki zmienione od ostatniego przebiegu':
        'Fichiers modifiés depuis la dernière exécution',
    'Pliki zostaną zapisane dokładnie tam, skąd pochodzą.\n\nKonflikty nazw: {collision}.\n\nCzy kontynuować?':
        'Les fichiers seront écrits exactement là d’où ils viennent.\n\nConflits de noms\xa0: {collision}.\n\nContinuer\xa0?',
    'Pliki, których jeszcze nie ma w kopii':
        'Fichiers qui ne sont pas encore dans la sauvegarde',
    'Po uzupełnieniu istniejącej wersji jej katalog nazywa się np.\n  2026-09-17_@687--2026-09-24_@921\nczyli: data utworzenia kopii i data ostatniego uzupełnienia.\n\nData utworzenia zostaje z przodu, więc katalogi nadal układają się\nchronologicznie. Widać to w Eksploratorze bez uruchamiania programu.':
        'Une fois une version existante complétée, son dossier s’appelle par exemple\n  2026-09-17_@687--2026-09-24_@921\nc’est-à-dire\xa0: la date de création de la sauvegarde et la date du dernier complément.\n\nLa date de création reste en tête\xa0: les dossiers se trient donc toujours\nchronologiquement. On le voit dans l’Explorateur de fichiers sans lancer le programme.',
    'Po wykonaniu kopii zostanie mało wolnego miejsca ({free}).':
        'Après la sauvegarde, il restera peu d’espace libre ({free}).',
    'Po zakończeniu kopii program ponownie skanuje źródło i dogrywa do tej samej\nwersji pliki, które w międzyczasie powstały lub się zmieniły.\nPrzydatne, gdy pracujesz na danych w trakcie wielogodzinnej kopii.\nPlik zmieniony w trakcie własnego kopiowania nigdy nie jest uznawany za zapisany.':
        'Une fois la sauvegarde terminée, le programme analyse à nouveau la source et ajoute à la même\nversion les fichiers apparus ou modifiés entre-temps.\nUtile si vous continuez à travailler sur les données pendant une sauvegarde de plusieurs heures.\nUn fichier modifié pendant sa propre copie n’est jamais considéré comme écrit.',
    'Poczekaj na zakończenie bieżącej operacji.':
        'Attendez la fin de l’opération en cours.',
    'Podaj hasło dla szablonu „{name}”:':
        'Saisissez le mot de passe du modèle «\xa0{name}\xa0»\xa0:',
    'Podaj hasło — bez niego nie można zaszyfrować kopii.':
        'Saisissez un mot de passe — sans lui, la sauvegarde ne peut pas être chiffrée.',
    'Podane hasło nie pasuje do plików zapisanych wcześniej w tej kopii. Wznowienie z innym hasłem zostawiłoby w jednej kopii pliki pod dwoma hasłami. Podaj hasło użyte przy poprzednim przebiegu albo utwórz kopię w nowym katalogu.':
        'Le mot de passe saisi ne correspond pas aux fichiers déjà écrits dans cette sauvegarde. Reprendre avec un autre mot de passe laisserait dans une même sauvegarde des fichiers protégés par deux mots de passe différents. Saisissez le mot de passe utilisé lors de l’exécution précédente ou créez la sauvegarde dans un nouveau dossier.',
    'Podgląd zmian':
        'Aperçu des modifications',
    'Pokazuje folder z plikami dziennika':
        'Affiche le dossier des fichiers journaux',
    'Pokazuje folder z ustawieniami i szablonami':
        'Affiche le dossier des paramètres et des modèles',
    'Pokaż / ukryj wpisane hasło':
        'Afficher / masquer le mot de passe saisi',
    'Pomiń istniejące pliki':
        'Ignorer les fichiers existants',
    'Potwierdź usuwanie':
        'Confirmer la suppression',
    'Powtórz hasło':
        'Répéter le mot de passe',
    'Program nie mógł się uruchomić:\n\n{error}\n\nSzczegóły zapisano w dzienniku aplikacji.':
        'Le programme n’a pas pu démarrer\xa0:\n\n{error}\n\nLes détails ont été écrits dans le journal de l’application.',
    'Program nie wie, czy ta kopia została dokończona. Uzupełnienie jej dogra tylko brakujące i zmienione pliki, a tego, co już jest zapisane, nie kopiuje ponownie.':
        'Le programme ne sait pas si cette sauvegarde a été terminée. La compléter n’ajoutera que les fichiers manquants et modifiés, sans recopier ce qui est déjà écrit.',
    'Program sam wykryje, czy kopia jest zaszyfrowana.':
        'Le programme détecte de lui-même si la sauvegarde est chiffrée.',
    'Przebieg operacji i diagnostyka':
        'Déroulement des opérations et diagnostic',
    'Przebieg operacji na żywo. Pełna historia trafia do pliku.':
        'Déroulement de l’opération en direct. L’historique complet est enregistré dans un fichier.',
    'Przebieg uzupełniający: {error}':
        'Passe de rattrapage\xa0: {error}',
    'Przeciętne':
        'Moyen',
    'Przerwano liczenie sumy kontrolnej.':
        'Calcul de la somme de contrôle interrompu.',
    'Przerwano skanowanie.':
        'Analyse interrompue.',
    'Przerwano. Zapisano {count} {files} ({size}).':
        'Interrompu. Total écrit\xa0: {count} {files} ({size}).',
    'Przerwij':
        'Arrêter',
    'Przerywanie operacji…':
        'Arrêt de l’opération…',
    'Przerywanie — zapisuję spis treści kopii, nie wyłączaj komputera…':
        'Arrêt en cours — écriture de la table des matières de la sauvegarde, n’éteignez pas l’ordinateur…',
    'Przeskanowano {count} {files}.':
        'Analyse terminée\xa0: {count} {files}.',
    'Przygotowanie…':
        'Préparation…',
    'Przywracanie':
        'Restauration',
    'Przywracanie do pierwotnych lokalizacji':
        'Restauration aux emplacements d’origine',
    'Przywracanie przerwane.':
        'Restauration interrompue.',
    'Przywracanie {count} {files} ({size})…':
        'Restauration de {count} {files} ({size})…',
    'Przywróć do pierwotnych lokalizacji':
        'Restaurer aux emplacements d’origine',
    'Przywróć domyślne':
        'Rétablir les valeurs par défaut',
    'Przywróć fabryczne':
        'Rétablir la liste intégrée',
    'Przywróć pliki':
        'Restaurer les fichiers',
    'Przywróć z tej kopii':
        'Restaurer depuis cette sauvegarde',
    'Pusta nazwa':
        'Nom vide',
    'Równoległe operacje:':
        'Opérations parallèles\xa0:',
    'Skanowanie plików źródłowych…':
        'Analyse des fichiers source…',
    'Skrót z dziennika — pełny zapis znajdziesz w zakładce „Dziennik”.':
        'Extrait du journal — l’historique complet se trouve sur l’écran «\xa0Journal\xa0».',
    'Skąd przywracamy':
        'Restaurer depuis',
    'Sprawdzam, co zmieniło się w źródle w trakcie kopii (przebieg uzupełniający {attempt} z {passes})…':
        'Recherche des modifications de la source pendant la sauvegarde (passe de rattrapage {attempt} sur {passes})…',
    'Sprawdzam, czy hasło zgadza się z hasłem wcześniej zapisanych plików…':
        'Vérification du mot de passe par rapport aux fichiers déjà écrits…',
    'Sprawdzam, czy w katalogu docelowym jest kopia do dokończenia…':
        'Recherche d’une sauvegarde à terminer dans le dossier de destination…',
    'Sprawdź hasło':
        'Vérifiez le mot de passe',
    'Sprawdź kopię':
        'Vérifier la sauvegarde',
    'Szablon przechowuje foldery, opcje i wykluczenia. Hasło nigdy nie trafia do szablonu — jest przechowywane w Menedżerze poświadczeń Windows albo wpisywane przy każdym uruchomieniu.':
        'Un modèle contient les dossiers, les options et les exclusions. Le mot de passe n’entre jamais dans le modèle — il est conservé dans le Gestionnaire d’identification Windows ou saisi à chaque exécution.',
    'Szablon usunięty.':
        'Modèle supprimé.',
    'Szablon „{name}”':
        'Modèle «\xa0{name}\xa0»',
    'Szablon „{name}” już istnieje.\n\nZastąpić go bieżącymi ustawieniami z formularza?':
        'Le modèle «\xa0{name}\xa0» existe déjà.\n\nLe remplacer par les réglages actuels du formulaire\xa0?',
    'Szablon „{name}” zostanie usunięty.\n\nPliki kopii zapasowej pozostaną nienaruszone.':
        'Le modèle «\xa0{name}\xa0» va être supprimé.\n\nLes fichiers de sauvegarde resteront intacts.',
    'Szablony':
        'Modèles',
    'Szablony: {count}\nSzyfrowanie: AES-256-GCM\nKlucz: {kdf}':
        'Modèles\xa0: {count}\nChiffrement\xa0: AES-256-GCM\nClé\xa0: {kdf}',
    'Szyfrowanie i kontrola poprawności zapisu.':
        'Chiffrement et contrôle de l’écriture.',
    'Szyfrowanie: AES-256-GCM (uwierzytelnione)\nWyprowadzanie klucza: {kdf}':
        'Chiffrement\xa0: AES-256-GCM (authentifié)\nDérivation de clé\xa0: {kdf}',
    'Szyfruj kopię (AES-256-GCM)':
        'Chiffrer la sauvegarde (AES-256-GCM)',
    'Słabe':
        'Faible',
    'Ta kopia nie jest zaszyfrowana — hasło nie jest potrzebne.':
        'Cette sauvegarde n’est pas chiffrée — aucun mot de passe n’est nécessaire.',
    'Ten folder jest już na liście.':
        'Ce dossier figure déjà dans la liste.',
    'To nie jest plik zaszyfrowany przez ten program.':
        'Ce fichier n’a pas été chiffré par ce programme.',
    'Trwa inna operacja — poczekaj na jej zakończenie.':
        'Une autre opération est en cours — attendez qu’elle se termine.',
    'Trwa operacja':
        'Opération en cours',
    'Trwa operacja na plikach. Zamknięcie programu ją przerwie.\n\nPliki zapisane do tej chwili zostaną zachowane, a kopię będzie można później dokończyć.\n\nZamknąć mimo to?':
        'Une opération sur les fichiers est en cours. Fermer le programme l’interrompra.\n\nLes fichiers écrits jusqu’ici seront conservés, et la sauvegarde pourra être terminée plus tard.\n\nFermer quand même\xa0?',
    'Trwa: {description}…':
        'En cours\xa0: {description}…',
    'Tryb dokładny — licz sumę kontrolną każdego pliku':
        'Mode approfondi — calculer la somme de contrôle de chaque fichier',
    'Układ kopii':
        'Mode de sauvegarde',
    'Układ plików:':
        'Disposition des fichiers\xa0:',
    'Uruchom kopię':
        'Lancer la sauvegarde',
    'Ustawienia':
        'Paramètres',
    'Usunąć szablon?':
        'Supprimer le modèle\xa0?',
    'Usuwa pozycję z listy. Nie kasuje żadnych plików.':
        'Retire l’élément de la liste. Aucun fichier n’est supprimé.',
    'Usuwa szablon. Nie kasuje żadnych plików kopii.':
        'Supprime le modèle. Aucun fichier de sauvegarde n’est supprimé.',
    'Usuwaj z kopii pliki skasowane w źródle':
        'Retirer de la sauvegarde les fichiers supprimés de la source',
    'Usuń':
        'Supprimer',
    'Usuń zaznaczone':
        'Retirer la sélection',
    'Uszkodzony nagłówek pliku.':
        'En-tête du fichier endommagé.',
    'Utwórz lub zaktualizuj kopię wybranych folderów':
        'Créer ou mettre à jour la sauvegarde des dossiers choisis',
    'Utwórz nową wersję':
        'Créer une nouvelle version',
    'Uzupełnienie istniejącej wersji nie kopiuje ponownie tego, co już w niej jest — dokończysz przerwaną kopię bez tworzenia kolejnej pełnej wersji.':
        'Compléter une version existante ne recopie pas ce qu’elle contient déjà — vous terminez une sauvegarde interrompue sans créer une nouvelle version complète.',
    'Uzupełnij tę wersję':
        'Compléter cette version',
    'Uzupełnij: {version} • {labels}':
        'Compléter\xa0: {version} • {labels}',
    'W katalogu docelowym jest kopia tych samych folderów zapisana starszą wersją programu:':
        'Le dossier de destination contient une sauvegarde des mêmes dossiers écrite par une ancienne version du programme\xa0:',
    'W katalogu docelowym jest niedokończona kopia tych samych folderów:':
        'Le dossier de destination contient une sauvegarde inachevée des mêmes dossiers\xa0:',
    'W tym katalogu nie ma spisu treści kopii — nie ma z czym porównać plików.':
        'Ce dossier ne contient pas de table des matières de sauvegarde — impossible de comparer les fichiers.',
    'Wczytaj do formularza':
        'Charger dans le formulaire',
    'Wczytano manifest kopii: {count} {files}.':
        'Manifeste de la sauvegarde chargé\xa0: {count} {files}.',
    'Wczytano szablon „{name}” do formularza.':
        'Modèle «\xa0{name}\xa0» chargé dans le formulaire.',
    'Wersja kopii nosi teraz nazwę {name}.':
        'La version de la sauvegarde s’appelle désormais {name}.',
    'Wersja, licencja i użyta kryptografia':
        'Version, licence et cryptographie utilisée',
    'Wersje z datą (zalecane)':
        'Versions datées (recommandé)',
    'Weryfikacja kopii':
        'Vérification de la sauvegarde',
    'Weryfikacja nie powiodła się: nieprawidłowe hasło lub uszkodzony plik.':
        'Échec de la vérification\xa0: mot de passe incorrect ou fichier endommagé.',
    'Weryfikacja po zapisie nie powiodła się — zapisane dane różnią się od źródła.':
        'Échec de la vérification après écriture — les données écrites diffèrent de la source.',
    'Weryfikacja {count} {files} ({size}), {threads} równolegle…':
        'Vérification de {count} {files} ({size}), {threads} en parallèle…',
    'Weryfikuj natychmiast po zapisie (spowalnia kopię)':
        'Vérifier immédiatement après l’écriture (ralentit la sauvegarde)',
    'Wolne miejsce: {free} z {total}':
        'Espace libre\xa0: {free} sur {total}',
    'Wolniejszy, ale wykrywa zmiany, które nie zmieniły rozmiaru ani daty\n(np. po przywróceniu pliku z innego nośnika).':
        'Plus lent, mais détecte les modifications qui n’ont changé ni la taille ni la date\n(p. ex. après la restauration d’un fichier depuis un autre support).',
    'Wpis {key} w spisie treści kopii wskazuje poza katalog docelowy — pomijam go.':
        'L’entrée {key} de la table des matières de la sauvegarde pointe hors du dossier de destination — elle est ignorée.',
    'Wraca do listy wbudowanej w program':
        'Revient à la liste intégrée au programme',
    'Wskaż folder kopii, aby zobaczyć jej zawartość.':
        'Indiquez le dossier de la sauvegarde pour voir son contenu.',
    'Wskaż folder kopii.':
        'Indiquez le dossier de la sauvegarde.',
    'Wskaż foldery objęte kopią. Podfoldery są uwzględniane automatycznie.':
        'Choisissez les dossiers à sauvegarder. Les sous-dossiers sont inclus automatiquement.',
    'Wskaż główny folder kopii (ten, który wybrałeś jako cel), a nie pojedynczy folder z datą. Program sam odczyta spis treści kopii.':
        'Indiquez le dossier principal de la sauvegarde (celui que vous avez choisi comme destination), et non un dossier daté isolé. Le programme lira lui-même la table des matières de la sauvegarde.',
    'Wskaż katalog docelowy kopii.':
        'Indiquez le dossier de destination de la sauvegarde.',
    'Wskaż katalog docelowy.':
        'Indiquez le dossier de destination.',
    'Wstawia zalecaną listę wykluczeń':
        'Insère la liste d’exclusions recommandée',
    'Wszystkie pliki wylądują bezpośrednio w katalogu docelowym, bez podfolderów.':
        'Tous les fichiers iront directement dans le dossier de destination, sans sous-dossiers.',
    'Wszystko do jednego folderu':
        'Tout dans un seul dossier',
    'Wybierz folder do kopii':
        'Choisir un dossier à sauvegarder',
    'Wybierz folder kopii':
        'Choisir le dossier de la sauvegarde',
    'Wybierz katalog':
        'Choisir un dossier',
    'Wybierz katalog docelowy':
        'Choisir le dossier de destination',
    'Wybierz katalog docelowy kopii':
        'Choisir le dossier de destination de la sauvegarde',
    'Wybierz katalog, aby zobaczyć dostępne miejsce.':
        'Choisissez un dossier pour voir l’espace disponible.',
    'Wybierz kolejny folder do kopii':
        'Choisir un autre dossier à sauvegarder',
    'Wybierz szablon z listy.':
        'Choisissez un modèle dans la liste.',
    'Wybierz…':
        'Choisir…',
    'Wybrano nadpisywanie istniejących plików. Ich obecna zawartość zostanie bezpowrotnie zastąpiona.\n\nCzy kontynuować?':
        'Vous avez choisi de remplacer les fichiers existants. Leur contenu actuel sera remplacé définitivement.\n\nContinuer\xa0?',
    'Wyczyść widok':
        'Effacer l’affichage',
    'Wygląd':
        'Apparence',
    'Wygląd, wykluczenia domyślne i informacje o środowisku.':
        'Apparence, exclusions par défaut et informations sur l’environnement.',
    'Wygląd, wykluczenia i magazyn haseł':
        'Apparence, exclusions et coffre des mots de passe',
    'Wykluczenia':
        'Exclusions',
    'Wykonuje kopię według tego szablonu':
        'Effectue la sauvegarde définie par ce modèle',
    'Wykonuje kopię zgodnie z powyższymi ustawieniami':
        'Effectue la sauvegarde selon les réglages ci-dessus',
    'Wymagane wyłącznie dla kopii zaszyfrowanych.':
        'Nécessaire uniquement pour les sauvegardes chiffrées.',
    'Wzorce plików i folderów pomijanych w kopii — po jednym w wierszu.':
        'Motifs des fichiers et dossiers exclus de la sauvegarde — un par ligne.',
    'Włączono szyfrowanie, ale nie podano hasła.':
        'Le chiffrement est activé, mais aucun mot de passe n’a été saisi.',
    'Włączono usuwanie z kopii plików skasowanych w źródle.\n\nPliki usunięte w źródle stracą swoją jedyną kopię zapasową. Czy na pewno kontynuować?':
        'Le retrait de la sauvegarde des fichiers supprimés de la source est activé.\n\nLes fichiers supprimés de la source perdront leur seule copie de sauvegarde. Voulez-vous vraiment continuer\xa0?',
    'Za mało miejsca w katalogu docelowym. Potrzeba ok. {needed}, dostępne {free}.':
        'Espace insuffisant dans le dossier de destination. Il faut environ {needed}\xa0; disponible\xa0: {free}.',
    'Zabezpieczenie przed literówką — hasła nie da się odzyskać.':
        'Protection contre les fautes de frappe — le mot de passe est irrécupérable.',
    'Zachowaj oba — dopisz numer do nazwy':
        'Garder les deux — ajouter un numéro au nom',
    'Zakończono z błędami ({errors}). Zapisano {count} {files}.':
        'Terminé avec des erreurs ({errors}). Total écrit\xa0: {count} {files}.',
    'Zakończono.':
        'Terminé.',
    'Zapamiętaj hasło w Menedżerze poświadczeń Windows':
        'Mémoriser le mot de passe dans le Gestionnaire d’identification Windows',
    'Zapamiętuje te ustawienia do ponownego użycia':
        'Mémorise ces réglages pour les réutiliser',
    'Zapis bieżącej sesji':
        'Journal de la session en cours',
    'Zapisane konfiguracje do ponownego użycia':
        'Configurations enregistrées, prêtes à réutiliser',
    'Zapisane konfiguracje — uruchamiasz je jednym kliknięciem.':
        'Configurations enregistrées — lancez-les d’un seul clic.',
    'Zapisane szablony':
        'Modèles enregistrés',
    'Zapisano szablon „{name}”.':
        'Modèle «\xa0{name}\xa0» enregistré.',
    'Zapisuje listę jako domyślną':
        'Enregistre la liste comme liste par défaut',
    'Zapisuje nową nazwę szablonu':
        'Enregistre le nouveau nom du modèle',
    'Zapisywanie {count} {files} ({size}), {workers} równolegle':
        'Écriture de {count} {files} ({size}), {workers} en parallèle',
    'Zapisz':
        'Enregistrer',
    'Zapisz do:':
        'Écrire dans\xa0:',
    'Zapisz jako szablon':
        'Enregistrer comme modèle',
    'Zapisz nazwę':
        'Enregistrer le nom',
    'Zapisz szablon':
        'Enregistrer le modèle',
    'Zastąpić szablon?':
        'Remplacer le modèle\xa0?',
    'Zatrzymuje operację. Pliki już zapisane pozostają nienaruszone.':
        'Arrête l’opération. Les fichiers déjà écrits restent intacts.',
    'Zaznacz szablon na liście.':
        'Sélectionnez un modèle dans la liste.',
    'Zmiana języka przebudowuje okno; wypełnione ścieżki zostają.':
        'Changer de langue reconstruit la fenêtre\xa0; les chemins saisis sont conservés.',
    'Zmiana motywu działa natychmiast.':
        'Le changement de thème est immédiat.',
    'Zmienia kolor przycisków i zaznaczeń':
        'Change la couleur des boutons et des sélections',
    'Zmień nazwę, aby łatwiej rozpoznawać szablon.':
        'Renommez le modèle pour le reconnaître plus facilement.',
    'Znaleziono {count} {files}. Porównuję z poprzednią kopią…':
        '{count} {files} au total. Comparaison avec la sauvegarde précédente…',
    'automatycznie':
        'automatique',
    'bez zmian':
        'sans changement',
    'brak (biblioteka keyring niezainstalowana)':
        'aucun (bibliothèque keyring non installée)',
    'brak danych':
        'aucune donnée',
    'brak pliku w kopii':
        'fichier absent de la sauvegarde',
    'do zapisania':
        'à écrire',
    'istniejąca kopia: {count} {files}, ostatnio {when}':
        'sauvegarde existante\xa0: {count} {files}, mise à jour le {when}',
    'jeszcze nie uruchamiany':
        'jamais exécuté',
    'kompletna':
        'complète',
    'kopia lustrzana':
        'copie miroir',
    'kopia zapasowa':
        'sauvegarde',
    'nie':
        'non',
    'niedokończona':
        'inachevée',
    'niedokończona — brakuje ok. {count} {files} ({size})':
        'inachevée — il manque environ {count} {files} ({size})',
    'niezaszyfrowana':
        'non chiffrée',
    'nieznany format manifestu':
        'format de manifeste inconnu',
    'nowych plików':
        'nouveaux fichiers',
    'np. C:\\Odzyskane':
        'p. ex. C:\\Récupération',
    'np. E:\\Kopie zapasowe':
        'p. ex. E:\\Sauvegardes',
    'plik':
        'fichier',
    'plik stanu jest za krótki':
        'le fichier d’état est trop court',
    'plik stanu w wersji {found}, obsługiwana: {supported}':
        'fichier d’état en version {found}, version prise en charge\xa0: {supported}',
    'pliki':
        'fichiers',
    'plików':
        'fichiers',
    'podgląd kopii':
        'aperçu de la sauvegarde',
    'pozostaną w kopii':
        'ils resteront dans la sauvegarde',
    'rozmiar w kopii {actual} B zamiast {expected} B':
        'taille dans la sauvegarde\xa0: {actual} o au lieu de {expected} o',
    'sprawdzanie kopii':
        'vérification de la sauvegarde',
    'stan nieznany (zapisana starszą wersją programu)':
        'état inconnu (écrite par une ancienne version du programme)',
    'suma kontrolna manifestu się nie zgadza':
        'la somme de contrôle du manifeste ne correspond pas',
    'suma kontrolna się nie zgadza — plik uszkodzony':
        'la somme de contrôle ne correspond pas — fichier endommagé',
    'szablon {name}':
        'modèle {name}',
    'tak':
        'oui',
    'ten system plików':
        'ce système de fichiers',
    'wersja {version}':
        'version {version}',
    'wersje z datą':
        'versions datées',
    'weryfikacja':
        'vérification',
    'wyłączona':
        'désactivé',
    'zaszyfrowana (AES-256-GCM)':
        'chiffrée (AES-256-GCM)',
    'zawartość różni się od pliku źródłowego':
        'le contenu diffère du fichier source',
    'zawartość różni się od sumy kontrolnej zapisanej podczas kopii':
        'le contenu ne correspond pas à la somme de contrôle enregistrée pendant la sauvegarde',
    'zmienionych':
        'modifiés',
    'zostaną usunięte z kopii':
        'ils seront retirés de la sauvegarde',
    '{done} z {total} • {speed}/s{eta}':
        '{done} sur {total} • {speed}/s{eta}',
    '{done} • {speed}/s':
        '{done} • {speed}/s',
    '{hours} h {minutes} min':
        '{hours} h {minutes} min',
    '{label}: {count} {files}':
        '{label}\xa0: {count} {files}',
    '{message}\n\nSzczegóły techniczne znajdziesz w zakładce „Dziennik”.':
        '{message}\n\nLes détails techniques se trouvent sur l’écran «\xa0Journal\xa0».',
    '{minutes} min {seconds} s':
        '{minutes} min {seconds} s',
    '{name}: nie można odczytać ({error})':
        '{name}\xa0: lecture impossible ({error})',
    '{seconds} s':
        '{seconds} s',
    '{summary}\n\nProblemy:\n{problems}\n\nPełna lista znajduje się w zakładce „Dziennik”.':
        '{summary}\n\nProblèmes\xa0:\n{problems}\n\nLa liste complète se trouve sur l’écran «\xa0Journal\xa0».',
    '{summary}{notes}\n\nPliki zapisane przed przerwaniem są kompletne i zostały odnotowane w spisie treści kopii.\n\nAby dokończyć kopię, uruchom ją ponownie — program zaproponuje uzupełnienie tej wersji zamiast tworzenia nowej.':
        '{summary}{notes}\n\nLes fichiers écrits avant l’interruption sont complets et ont été consignés dans la table des matières de la sauvegarde.\n\nPour terminer la sauvegarde, relancez-la — le programme proposera de compléter cette version au lieu d’en créer une nouvelle.',
    '{title} — gotowe':
        '{title} — terminé',
    '{title} — przerwano':
        '{title} — interrompu',
    '{title} — zakończono z błędami':
        '{title} — terminé avec des erreurs',
    '{when}  •  {action}  •  {count} {files}':
        '{when}  •  {action}  •  {count} {files}',
    'Łączny rozmiar danych do przesłania':
        'Taille totale des données à transférer',
    'Środowisko':
        'Environnement',
    'Źródła: {sources}\nCel: {destination}\nUkład: {structure} • Szyfrowanie: {encrypt} • Weryfikacja: {verify} • Dogrywka: {catchup} • Równolegle: {workers} • Data uzupełnienia w nazwie: {stamp}\nUtworzony: {created} • Ostatni przebieg: {last}':
        'Sources\xa0: {sources}\nDestination\xa0: {destination}\nMode\xa0: {structure} • Chiffrement\xa0: {encrypt} • Vérification\xa0: {verify} • Rattrapage\xa0: {catchup} • En parallèle\xa0: {workers} • Date du complément dans le nom\xa0: {stamp}\nCréé\xa0: {created} • Dernière exécution\xa0: {last}',
    'Źródło nie zmieniło się w trakcie kopii — nie ma czego uzupełniać.':
        'La source n’a pas changé pendant la sauvegarde — rien à rattraper.',
    '—':
        '—',
    '• Kopia przyrostowa — zapisywane są wyłącznie pliki nowe i zmienione.\n  Porównanie opiera się na spisie treści kopii, rozmiarze i dacie modyfikacji;\n  przy różnicy liczona jest suma kontrolna SHA-256.\n\n• Wersje z datą — każdy przebieg tworzy kompletny folder z datą, a pliki\n  niezmienione są podpinane twardym dowiązaniem, więc nie zajmują miejsca dwa razy.\n\n• Weryfikacja po zapisie — zapisany plik jest odczytywany z powrotem\n  i porównywany ze źródłem.\n\n• Odporność na przerwania — pliki powstają pod nazwą tymczasową i są\n  podmieniane dopiero po pełnym zapisie.':
        '• Sauvegarde incrémentale — seuls les fichiers nouveaux et modifiés sont écrits.\n  La comparaison s’appuie sur la table des matières de la sauvegarde, la taille et la date de modification\xa0;\n  en cas de différence, une somme de contrôle SHA-256 est calculée.\n\n• Versions datées — chaque exécution crée un dossier daté complet, et les fichiers\n  inchangés y sont rattachés par un lien physique\xa0: ils n’occupent donc jamais deux fois l’espace.\n\n• Vérification après écriture — le fichier écrit est relu\n  et comparé à la source.\n\n• Résistance aux interruptions — les fichiers sont créés sous un nom temporaire et\n  ne prennent leur nom définitif qu’une fois entièrement écrits.',
    '• Szyfr: AES-256 w trybie GCM (szyfrowanie z uwierzytelnieniem).\n• Wyprowadzanie klucza z hasła: {kdf}.\n• Nagłówek każdego pliku jest uwierzytelniony jako AAD — podmiana parametrów\n  unieważnia tag.\n• Każdy plik dostaje losowy, niepowtarzalny nonce.\n• Odszyfrowany plik powstaje dopiero po pomyślnej weryfikacji tagu.\n• Hasła nie są zapisywane w plikach programu. Opcjonalnie trafiają do\n  Menedżera poświadczeń Windows.':
        '• Algorithme de chiffrement\xa0: AES-256 en mode GCM (chiffrement authentifié).\n• Dérivation de la clé à partir du mot de passe\xa0: {kdf}.\n• L’en-tête de chaque fichier est authentifié comme AAD — toute modification des paramètres\n  invalide le tag.\n• Chaque fichier reçoit un nonce aléatoire et unique.\n• Le fichier déchiffré n’est créé qu’après la vérification réussie du tag.\n• Les mots de passe ne sont jamais écrits dans les fichiers du programme. En option, ils vont dans le\n  Gestionnaire d’identification Windows.',
    'Bez hasła nie da się odczytać ani jednego pliku z kopii.':
        'Sans le mot de passe, aucun fichier de la sauvegarde ne peut être lu.',
    'Co chcesz chronić?':
        'Que voulez-vous protéger\xa0?',
    'Co chcesz teraz zrobić?':
        'Que voulez-vous faire\xa0?',
    'Czyta kopię z nośnika i porównuje ją z zapisanymi sumami kontrolnymi.':
        'Lit la sauvegarde sur le support et la compare aux sommes de contrôle enregistrées.',
    'Dalej':
        'Suivant',
    'Dokumenty i zdjęcia':
        'Documents et photos',
    'Ekran powitalny wrócisz w ustawieniach, gdy zmienisz zdanie.':
        'Vous pourrez réactiver l’écran d’accueil dans les paramètres si vous changez d’avis.',
    'Ekran z pytaniem, co chcesz teraz zrobić: kopia, przywracanie, sprawdzenie.':
        'Un écran qui vous demande ce que vous voulez faire\xa0: sauvegarder, restaurer ou vérifier.',
    'Foldery objęte kopią':
        'Dossiers inclus dans la sauvegarde',
    'Foldery z pracą. Kreator pominie katalogi, które odtwarza się jednym poleceniem (node_modules, venv, build).':
        'Les dossiers de votre travail. L’assistant laisse de côté les dossiers qu’une seule commande permet de recréer (node_modules, venv, build).',
    'Gdzie zapisać kopię?':
        'Où enregistrer la sauvegarde\xa0?',
    'Historia i szyfrowanie':
        'Historique et chiffrement',
    'Historia zmian (zalecane)':
        'Historique des modifications (recommandé)',
    'Jak bardzo chcesz się zabezpieczyć?':
        'Quel niveau de protection souhaitez-vous\xa0?',
    'Jak wyżej, a dodatkowo każdy plik trafia do kopii zaszyfrowany (AES-256-GCM). Potrzebne przy kopii wożonej poza dom.':
        'Comme ci-dessus, et en plus chaque fichier est chiffré dans la sauvegarde (AES-256-GCM). Indispensable pour une sauvegarde qui quitte la maison.',
    'Jedna aktualna kopia':
        'Une seule copie à jour',
    'Język, motyw, domyślne wykluczenia i informacje o środowisku.':
        'Langue, thème, exclusions par défaut et informations sur l’environnement.',
    'Katalog docelowy leży wewnątrz źródła — wybierz inny.':
        'Le dossier de destination se trouve dans la source — choisissez-en un autre.',
    'Każdy przebieg tworzy folder z datą. Pliki niezmienione są podpinane dowiązaniem, więc historia kosztuje tyle, ile realnie się zmieniło.':
        'Chaque exécution crée un dossier daté. Les fichiers inchangés y sont rattachés par un lien\xa0: l’historique ne coûte donc que ce qui a réellement changé.',
    'Każdy przebieg utworzy folder z datą. Pierwszy zajmie tyle, ile dane; kolejne — tyle, ile realnie się zmieniło.':
        'Chaque exécution créera un dossier daté. La première occupera autant d’espace que les données\xa0; les suivantes, seulement ce qui a réellement changé.',
    'Kopia powstanie w: {path}':
        'La sauvegarde sera créée dans\xa0: {path}',
    'Kopia trafi do: {path}':
        'La sauvegarde ira dans\xa0: {path}',
    'Kopia: {what}':
        'Sauvegarde\xa0: {what}',
    'Krok {number} z {total}':
        'Étape {number} sur {total}',
    'Najlepiej na innym dysku fizycznym niż ten, który chronisz — kopia obok oryginału ginie razem z nim.':
        'Idéalement sur un autre disque physique que celui que vous protégez — une sauvegarde placée à côté de l’original disparaît avec lui.',
    'Najszybsza i najmniejsza. Kopia odpowiada temu, co masz teraz — bez historii wcześniejszych wersji.':
        'La plus rapide et la plus compacte. La sauvegarde reflète ce que vous avez maintenant — sans historique des versions antérieures.',
    'Nie było jeszcze żadnej kopii. Zacznij od „Zrób kopię”.':
        'Aucune sauvegarde pour l’instant. Commencez par «\xa0Sauvegarder\xa0».',
    'Nie lista ustawień, tylko ich skutki.':
        'Pas la liste des réglages, mais leurs effets.',
    'Nie pokazuj tego ekranu przy starcie':
        'Ne plus afficher cet écran au démarrage',
    'Nośnik docelowy':
        'Support de destination',
    'Odtwarza pliki z kopii — całość albo wybrany folder.':
        'Restaure des fichiers d’une sauvegarde — tout ou un dossier choisi.',
    'Odśwież listę':
        'Actualiser la liste',
    'Ostatnia kopia: {when} • {count} {files}.':
        'Dernière sauvegarde\xa0: {when} • {count} {files}.',
    'Pierwszy przebieg jest najdłuższy — kolejne porównują rozmiar i datę modyfikacji, więc zwykle trwają sekundy.':
        'La première exécution est la plus longue — les suivantes comparent la taille et la date de modification, et ne prennent donc généralement que quelques secondes.',
    'Pliki w kopii będą zaszyfrowane; bez hasła nie da się ich odczytać.':
        'Les fichiers de la sauvegarde seront chiffrés\xa0; sans le mot de passe, ils sont illisibles.',
    'Podfoldery są uwzględniane automatycznie.':
        'Les sous-dossiers sont inclus automatiquement.',
    'Pokazuj ekran powitalny przy starcie':
        'Afficher l’écran d’accueil au démarrage',
    'Ponownie sprawdza podłączone nośniki':
        'Recherche à nouveau les supports connectés',
    'Program będzie utrzymywał jeden folder zgodny ze źródłem. Każdy kolejny przebieg dopisze tylko to, co się zmieniło.':
        'Le programme tiendra un seul dossier en phase avec la source. Chaque exécution suivante n’ajoutera que ce qui a changé.',
    'Projekty i kod':
        'Projets et code',
    'Przechodzi do następnego kroku':
        'Passe à l’étape suivante',
    'Przechodzi do pełnego okna programu':
        'Ouvre la fenêtre complète du programme',
    'Sam wskażesz, co ma trafić do kopii.':
        'Vous choisissez vous-même ce qui entre dans la sauvegarde.',
    'System plików: {filesystem}, klaster {cluster}':
        'Système de fichiers\xa0: {filesystem}, cluster de {cluster}',
    'Ten katalog leży wewnątrz folderu źródłowego — wybierz inny.':
        'Ce dossier se trouve dans un dossier source — choisissez-en un autre.',
    'Ten nośnik nie obsługuje twardych dowiązań, więc każda wersja z datą zajmie tyle miejsca co pełna kopia. Przy tym nośniku rozważ „jedną aktualną kopię”.':
        'Ce support ne prend pas en charge les liens physiques\xa0: chaque version datée occupera donc autant d’espace qu’une copie complète. Avec ce support, envisagez «\xa0une seule copie à jour\xa0».',
    'To dysk systemowy — kopia nie przetrwa jego awarii. Jeśli masz drugi dysk albo pendrive, wybierz jego.':
        'C’est le disque système — la sauvegarde ne survivra pas à sa panne. Si vous avez un second disque ou une clé USB, choisissez plutôt ce support.',
    'To się wydarzy':
        'Ce qui va se passer',
    'Trzy gotowe zestawy zamiast kilkunastu przełączników.':
        'Trois formules prêtes à l’emploi au lieu d’une douzaine d’options.',
    'Twoje pliki osobiste z folderów użytkownika. Najczęstszy wybór.':
        'Vos fichiers personnels, dans vos dossiers utilisateur. Le choix le plus courant.',
    'Uruchamia kreator, który ustawi kopię krok po kroku':
        'Lance l’assistant, qui configure la sauvegarde étape par étape',
    'Uruchom kreator…':
        'Lancer l’assistant…',
    'Ustawia kopię krok po kroku i zapisuje ją jako szablon':
        'Configure la sauvegarde étape par étape et l’enregistre comme modèle',
    'Ustawienia pierwszej kopii':
        'Configuration de la première sauvegarde',
    'Ustawienia pierwszej kopii…':
        'Configurer la première sauvegarde…',
    'W tym katalogu jest już kopia ({count} {files}) — program ją uzupełni, a nie nadpisze.':
        'Ce dossier contient déjà une sauvegarde ({count} {files}) — le programme la complétera au lieu de l’écraser.',
    'Wraca do poprzedniego kroku':
        'Revient à l’étape précédente',
    'Wskaż dowolny katalog docelowy':
        'Choisissez n’importe quel dossier de destination',
    'Wskaż folder kopii i kliknij „Sprawdź kopię”.':
        'Indiquez le dossier de la sauvegarde et cliquez sur «\xa0Vérifier la sauvegarde\xa0».',
    'Wstecz':
        'Précédent',
    'Wybierz':
        'Choisir',
    'Wybierz inny folder…':
        'Choisir un autre dossier…',
    'Wybierz to, co najbliższe. Dokładną listę folderów poprawisz niżej.':
        'Choisissez l’option la plus proche. Vous ajusterez la liste exacte des dossiers ci-dessous.',
    'Wybrane foldery':
        'Dossiers choisis',
    'Zamknij':
        'Fermer',
    'Zamyka kreator bez zapisywania':
        'Ferme l’assistant sans enregistrer',
    'Zapisuje nowe i zmienione pliki. Pierwszy raz trwa najdłużej.':
        'Écrit les fichiers nouveaux et modifiés. La première fois est la plus longue.',
    'Zapisuje szablon bez uruchamiania kopii':
        'Enregistre le modèle sans lancer la sauvegarde',
    'Zapisuje szablon i od razu uruchamia kopię':
        'Enregistre le modèle et lance aussitôt la sauvegarde',
    'Zapisz i zrób kopię':
        'Enregistrer et sauvegarder',
    'Zapisz ustawienia':
        'Enregistrer les réglages',
    'Zrób kopię':
        'Sauvegarder',
    'dysk systemowy':
        'disque système',
    'wolne {free} z {total}':
        '{free} libres sur {total}',
    'Porównano ze źródłem: {source}; tylko z sumą kontrolną (źródło zmieniło się albo jest niedostępne): {checksum}.':
        'Fichiers comparés à la source\xa0: {source}\xa0; à la somme de contrôle seulement (source modifiée ou indisponible)\xa0: {checksum}.',
    'Przywraca losową próbkę plików do katalogu tymczasowego i porównuje je ze źródłem.\nSprawdza całą drogę odzyskiwania, a trwa minuty. Nic nie zostaje na dysku.':
        'Restaure un échantillon aléatoire de fichiers dans un dossier temporaire et les compare à la source.\nTeste toute la chaîne de récupération, en quelques minutes. Rien ne reste sur le disque.',
    'Próbne przywrócenie':
        'Restauration d’essai',
    'W kopii nie ma plików, które dałoby się sprawdzić próbnie.':
        'La sauvegarde ne contient aucun fichier qu’une restauration d’essai pourrait vérifier.',
    'przywrócony plik różni się od pliku źródłowego':
        'le fichier restauré diffère du fichier source',
    'przywrócony plik różni się od sumy kontrolnej zapisanej podczas kopii':
        'le fichier restauré ne correspond pas à la somme de contrôle enregistrée pendant la sauvegarde',
    'próbne przywrócenie':
        'restauration d’essai',
    '(brak zapisanych szablonów)':
        '(aucun modèle enregistré)',
    'Bez tego kopia planowa ruszy dopiero wtedy, gdy sam otworzysz program.':
        'Sans cela, une sauvegarde planifiée ne démarre que lorsque vous ouvrez vous-même le programme.',
    'Codziennie o godzinie':
        'Chaque jour à heure fixe',
    'Codziennie o wybranej godzinie (zalecane)':
        'Chaque jour à l’heure choisie (recommandé)',
    'Dla dysku USB podłączanego od czasu do czasu. Najwyżej jedna kopia na 12 godzin.':
        'Pour un disque USB branché de temps en temps. Une sauvegarde toutes les 12 heures au plus.',
    'Dostępne w zainstalowanej wersji programu (plik EXE).':
        'Disponible dans la version installée du programme (fichier EXE).',
    'Godzina kopii codziennej (czas tego komputera).':
        'Heure de la sauvegarde quotidienne (horloge de cet ordinateur).',
    'Harmonogram działa wtedy, gdy działa program — także ukryty przy zegarze.':
        'La planification fonctionne tant que le programme tourne — y compris réduit en icône près de l’horloge.',
    'Harmonogram nie uruchamia kopii, dopóki tego nie odznaczysz. Ręczne kopie działają.':
        'La planification ne lance aucune sauvegarde tant que vous ne décochez pas cette case. Les sauvegardes manuelles restent possibles.',
    'Harmonogram szablonu „{name}” zapisany.':
        'Planification du modèle «\xa0{name}\xa0» enregistrée.',
    'Harmonogram:':
        'Planification\xa0:',
    'Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.':
        'Si l’ordinateur est éteint à ce moment-là, la sauvegarde démarrera dès qu’il sera rallumé.',
    'Kiedy kopia z tego szablonu ma ruszać sama.':
        'Quand la sauvegarde de ce modèle doit démarrer d’elle-même.',
    'Kiedy robić kopię?':
        'Quand sauvegarder\xa0?',
    'Kopia będzie robiona codziennie o {time}; termin przegapiony przy wyłączonym komputerze program nadrobi po jego włączeniu.':
        'La sauvegarde aura lieu chaque jour à {time}\xa0; si l’ordinateur est éteint à cette heure-là, le programme la rattrapera au prochain démarrage.',
    'Kopia planowa nie powiodła się':
        'La sauvegarde planifiée a échoué',
    'Kopia rusza tylko wtedy, gdy ją uruchomisz.':
        'La sauvegarde ne démarre que lorsque vous la lancez.',
    'Kopia ruszy po podłączeniu dysku docelowego (najwyżej raz na 12 godzin).':
        'La sauvegarde démarrera au branchement du disque de destination (au plus une fois toutes les 12 heures).',
    'Kopia ruszy po podłączeniu dysku docelowego — najwyżej raz na 12 godzin.':
        'La sauvegarde démarre au branchement du disque de destination — au plus une fois toutes les 12 heures.',
    'Kopia sprzed miesiąca nie chroni tego, co zmieniło się od tamtej pory.':
        'Une sauvegarde vieille d’un mois ne protège pas ce qui a changé depuis.',
    'Kopia „{name}” czeka':
        'Sauvegarde «\xa0{name}\xa0» en retard',
    'Kopia „{name}” nie ruszyła':
        'La sauvegarde «\xa0{name}\xa0» n’a pas démarré',
    'Kopie planowe działają, gdy działa program (także ukryty przy zegarze).':
        'Les sauvegardes planifiées s’exécutent tant que le programme tourne (y compris réduit en icône près de l’horloge).',
    'Kopie planowe działają, gdy działa program: po zamknięciu okna zostaje ikona przy zegarze, a przy logowaniu do Windows program uruchamia się w tle.':
        'Les sauvegardes planifiées s’exécutent tant que le programme tourne\xa0: après la fermeture de la fenêtre, une icône reste près de l’horloge, et le programme démarre en arrière-plan à l’ouverture de session Windows.',
    'Kopie planowe i praca w tle':
        'Sauvegardes planifiées et arrière-plan',
    'Kopie planowe wykonają się o czasie. Program zamkniesz z menu ikony przy zegarze.':
        'Les sauvegardes planifiées s’exécuteront à l’heure. Pour quitter le programme, utilisez le menu de l’icône près de l’horloge.',
    'Kopię uruchamiasz przyciskiem. Najprostsze, ale łatwo o niej zapomnieć.':
        'Vous lancez la sauvegarde avec un bouton. Le plus simple, mais on l’oublie facilement.',
    'Kopię uruchamiasz sam — przyciskiem w programie albo z menu ikony przy zegarze.':
        'Vous lancez vous-même la sauvegarde — avec le bouton du programme ou depuis le menu de l’icône près de l’horloge.',
    'Następna kopia: {when}. Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.':
        'Prochaine sauvegarde\xa0: {when}. Si l’ordinateur est éteint à ce moment-là, la sauvegarde démarrera dès qu’il sera rallumé.',
    'Nie udało się zmienić startu przy logowaniu — szczegóły w dzienniku.':
        'Impossible de modifier le lancement à l’ouverture de session — détails dans le journal.',
    'Od {days} dni nie było udanej kopii. Podłącz dysk docelowy albo otwórz program, żeby sprawdzić, co się dzieje.':
        'Aucune sauvegarde réussie depuis {days} jours. Branchez le disque de destination ou ouvrez le programme pour voir ce qui se passe.',
    'Otwórz Sigelith Backup':
        'Ouvrir Sigelith Backup',
    'Po podłączeniu dysku docelowego':
        'Au branchement du disque de destination',
    'Po podłączeniu dysku z kopią':
        'Au branchement du disque de sauvegarde',
    'Po zamknięciu okna działaj dalej przy zegarze, gdy są kopie planowe':
        'Rester actif près de l’horloge après la fermeture de la fenêtre si des sauvegardes sont planifiées',
    'Potrzebne, żeby kopie planowe ruszały bez Twojego udziału. Hasło trafia do magazynu systemowego powiązanego z Twoim kontem, nie do plików programu.':
        'Nécessaire pour que les sauvegardes planifiées démarrent sans vous. Le mot de passe est conservé dans le coffre du système, lié à votre compte, et non dans les fichiers du programme.',
    'Program uruchamia się w tle przy logowaniu, więc terminy nie przepadną.':
        'Le programme démarre en arrière-plan à l’ouverture de session\xa0: aucune échéance n’est manquée.',
    'Ręcznie':
        'Manuellement',
    'Ręcznie — kiedy zechcę':
        'Manuellement — quand je le souhaite',
    'Start przy logowaniu włączony':
        'Lancement à l’ouverture de session activé',
    'Szablon jest zaszyfrowany, a hasło nie jest zapamiętane. Kopie planowe potrzebują hasła zapisanego w Menedżerze poświadczeń Windows.':
        'Le modèle est chiffré et son mot de passe n’est pas mémorisé. Les sauvegardes planifiées ont besoin du mot de passe enregistré dans le Gestionnaire d’identification Windows.',
    'Sigelith Backup będzie uruchamiał się w tle, żeby wykonywać kopie planowe. Wyłączysz to w ustawieniach programu.':
        'Sigelith Backup démarrera en arrière-plan pour exécuter les sauvegardes planifiées. Vous pouvez désactiver cela dans les paramètres du programme.',
    'Sigelith Backup działa w tle':
        'Sigelith Backup fonctionne en arrière-plan',
    'Uruchamiaj program w tle przy logowaniu do Windows':
        'Lancer le programme en arrière-plan à l’ouverture de session Windows',
    'Wstrzymaj kopie planowe':
        'Suspendre les sauvegardes planifiées',
    'Zakończ':
        'Quitter',
    'Zamknięcie okna chowa je, a harmonogram pilnuje terminów. Program zamkniesz z menu ikony przy zegarze.':
        'Fermer la fenêtre la masque, et la planification veille aux échéances. Pour quitter le programme, utilisez le menu de l’icône près de l’horloge.',
    'Zrób kopię teraz':
        'Sauvegarder maintenant',
    '{summary} Szczegóły znajdziesz w programie, w zakładce „Dziennik”.':
        '{summary} Les détails se trouvent dans le programme, sur l’écran «\xa0Journal\xa0».',
    'Program działa z uprawnieniami administratora. Nie są mu potrzebne — kopia i przywracanie działają bez nich, a pliki zapisane przez administratora mogą później nie dać się zmienić ze zwykłego konta.':
        'Le programme s’exécute avec des droits d’administrateur. Il n’en a pas besoin — la sauvegarde et la restauration fonctionnent sans eux, et les fichiers écrits par un administrateur risquent ensuite de ne plus pouvoir être modifiés depuis un compte ordinaire.',
    'Pliki otwarte w innych programach nie trafiły do kopii: {files}. Zamknij te programy i uruchom kopię ponownie — dograne zostaną tylko te pliki.':
        'Des fichiers ouverts dans d’autres programmes n’ont pas été sauvegardés\xa0: {files}. Fermez ces programmes et relancez la sauvegarde — seuls ces fichiers seront ajoutés.',
    'Uwaga: w źródle zmieniło się podejrzanie dużo plików — {reasons}':
        'Attention\xa0: un nombre suspect de fichiers a changé dans la source — {reasons}',
    'Wstrzymano kopię: w źródle zmieniło się podejrzanie dużo plików. {reasons}':
        'Sauvegarde suspendue\xa0: un nombre suspect de fichiers a changé dans la source. {reasons}',
    'Zmieniło się albo zniknęło {count} z {previous} plików poprzedniej kopii.':
        'Fichiers de la sauvegarde précédente modifiés ou disparus\xa0: {count} sur {previous}.',
    '{suspicious} z {evaluated} sprawdzonych zmienionych plików ma treść, która nie pasuje do ich typu (wygląda na zaszyfrowaną).':
        'Fichiers modifiés dont le contenu ne correspond pas à leur type (il semble chiffré)\xa0: {suspicious} sur {evaluated} vérifiés.',
    'Kontynuuj mimo to':
        'Continuer quand même',
    'Kopia planowa wstrzymana':
        'Sauvegarde planifiée suspendue',
    'Kopia wstrzymana do decyzji.':
        'Sauvegarde suspendue en attente de votre décision.',
    'Kopia wstrzymana — w źródle zmieniło się podejrzanie dużo plików.':
        'Sauvegarde suspendue — un nombre suspect de fichiers a changé dans la source.',
    'Podejrzanie dużo zmian':
        'Nombre suspect de modifications',
    'Wstrzymaj kopię':
        'Suspendre la sauvegarde',
    '{reasons}\n\nJeśli to spodziewane — aktualizacja programu, przeniesienie albo przerobienie wielu plików — kontynuuj.\n\nJeśli nie, NIE kontynuuj: tak wygląda działanie oprogramowania szyfrującego pliki (ransomware). Sprawdź najpierw, czy Twoje pliki dają się otworzyć. Wcześniejsze wersje w kopii pozostają nietknięte.':
        '{reasons}\n\nSi c’est attendu — mise à jour d’un logiciel, déplacement ou remaniement de nombreux fichiers —, continuez.\n\nSinon, NE continuez PAS\xa0: c’est ainsi qu’agit un logiciel qui chiffre les fichiers (rançongiciel, ou ransomware). Vérifiez d’abord que vos fichiers s’ouvrent encore. Les versions antérieures de la sauvegarde restent intactes.',
    '{reasons} To może być działanie złośliwego oprogramowania szyfrującego pliki. Otwórz program, sprawdź pliki i uruchom kopię ręcznie.':
        '{reasons} Il peut s’agir d’un logiciel malveillant qui chiffre les fichiers. Ouvrez le programme, vérifiez vos fichiers et lancez la sauvegarde manuellement.',
    'Pominięto {count} {files}.':
        'Hors sauvegarde\xa0: {count} {files}.',
    'Ponawiam {count} {files}…':
        'Nouvelle tentative\xa0: {count} {files}…',
    ' (bez {count} {files})':
        ' (sans {count} {files})',
    'plik otwarty w innym programie':
        'fichier ouvert dans un autre programme',
    'pliki otwarte w innych programach':
        'fichiers ouverts dans d’autres programmes',
    'plików otwartych w innych programach':
        'fichiers ouverts dans d’autres programmes',
    'pliku otwartego w innym programie':
        'fichier ouvert dans un autre programme',
    '\n\n…i kolejne: {count}.':
        '\n\n…et d’autres encore\xa0: {count}.',
    'Foldery objęte kopią ({count}): {list}':
        'Dossiers inclus dans la sauvegarde ({count})\xa0: {list}',
    'Nośnik nie obsługuje twardych dowiązań — kopiuję do nowej wersji niezmienione pliki: {count} ({size})…':
        'Le support ne prend pas en charge les liens physiques — copie des fichiers inchangés dans la nouvelle version\xa0: {count} ({size})…',
    'Pliki bez sumy kontrolnej sprawdzone tylko co do rozmiaru, bo ich źródło zmieniło się albo jest niedostępne: {count}.':
        'Fichiers sans somme de contrôle vérifiés uniquement sur leur taille, car leur source a changé ou est indisponible\xa0: {count}.',
    'Pliki bez zapisanej sumy kontrolnej, porównane ze źródłem i uzupełnione w spisie treści: {count}.':
        'Fichiers sans somme de contrôle enregistrée, comparés à la source et ajoutés à la table des matières\xa0: {count}.',
    'Pliki przeniesione w źródle: {count} — trafią do kopii bez przesyłania danych.':
        'Fichiers déplacés dans la source\xa0: {count} — ils entreront dans la sauvegarde sans transfert de données.',
    'Pliki skasowane w źródle: {count} — {action}.':
        'Fichiers supprimés de la source\xa0: {count} — {action}.',
    'Pliki z końcówką dopisaną do nazwy, których oryginały zniknęły: {count}.':
        'Fichiers dont le nom a reçu un suffixe et dont l’original a disparu\xa0: {count}.',
    'Pliki zmienione w trakcie kopiowania: {count} — zostaną zapisane ponownie w przebiegu uzupełniającym.':
        'Fichiers modifiés pendant la copie\xa0: {count} — ils seront réécrits lors de la passe de rattrapage.',
    'Pliki, których brakuje w kopii i które zostaną zapisane ponownie: {count}.':
        'Fichiers absents de la sauvegarde qui seront réécrits\xa0: {count}.',
    'Podpinanie niezmienionych plików do nowej wersji: {count}…':
        'Rattachement des fichiers inchangés à la nouvelle version\xa0: {count}…',
    'Pomijam pliki, które już są w tej wersji kopii: {count}.':
        'Fichiers déjà présents dans cette version de la sauvegarde, ignorés\xa0: {count}.',
    'Porządkowanie historii — usunięte najstarsze wersje: {count}.':
        'Nettoyage de l’historique — versions les plus anciennes supprimées\xa0: {count}.',
    'Przenoszenie plików, które zmieniły miejsce w źródle: {count}…':
        'Déplacement des fichiers qui ont changé de place dans la source\xa0: {count}…',
    'Próbne przywrócenie losowo wybranych plików: {count}…':
        'Restauration d’essai de fichiers choisis au hasard\xa0: {count}…',
    'Usuwanie z kopii plików skasowanych w źródle: {count}…':
        'Retrait de la sauvegarde des fichiers supprimés de la source\xa0: {count}…',
    'Uzupełniam kopię o pliki, które przybyły lub zmieniły się w trakcie: {count} ({size})…':
        'Ajout à la sauvegarde des fichiers apparus ou modifiés entre-temps\xa0: {count} ({size})…',
    'Uzupełnianie wersji {version} — pliki już zapisane, które zostaną pominięte: {count}.':
        'Complément de la version {version} — fichiers déjà écrits, qui seront ignorés\xa0: {count}.',
    'Wznawiam wersję {version} — już zapisane: {done}, do dogrania: {todo}.':
        'Reprise de la version {version} — déjà écrits\xa0: {done}, restant à écrire\xa0: {todo}.',
    'pliku':
        'fichier',
    'Brak fragmentu {cid} w magazynie kopii.':
        'Le fragment {cid} est absent du dépôt de fragments de la sauvegarde.',
    'Brak opisu magazynu fragmentów w katalogu kopii.':
        'Le dossier de la sauvegarde ne contient pas la description de son dépôt de fragments.',
    'Duże pliki zapisuj różnicowo (od 256 MB)':
        'Enregistrer les gros fichiers par différences (à partir de 256 MB)',
    'Fragment {cid} jest uszkodzony.':
        'Le fragment {cid} est endommagé.',
    'Kolejna wersja dużego pliku — maszyny wirtualnej, skrzynki pocztowej, bazy —\nzapisuje tylko zmienione fragmenty zamiast całego pliku. W kopii taki plik\nleży jako przepis + fragmenty; złoży go program albo skrypt ratunkowy.':
        'La version suivante d’un gros fichier — machine virtuelle, boîte aux lettres, base de données —\nn’enregistre que les fragments modifiés au lieu du fichier entier. Dans la sauvegarde, un tel fichier\nest conservé sous forme de recette + fragments\xa0; le programme ou le script de secours le reconstitue.',
    'Opis magazynu fragmentów jest uszkodzony.':
        'La description du dépôt de fragments est endommagée.',
    'Plik złożony z fragmentów różni się od zapisanego w przepisie.':
        'Le fichier reconstitué à partir des fragments diffère de celui décrit dans sa recette.',
    'Podane hasło nie pasuje do fragmentów zapisanych wcześniej w tej kopii.':
        'Le mot de passe saisi ne correspond pas aux fragments déjà écrits dans cette sauvegarde.',
    'Przepis pliku jest uszkodzony.':
        'La recette du fichier est endommagée.',
    'To nie jest przepis pliku zapisanego fragmentami.':
        'Ce n’est pas la recette d’un fichier enregistré par fragments.',
    'Usunięto nieużywane fragmenty dużych plików: {count} ({size}).':
        'Fragments inutilisés de gros fichiers supprimés\xa0: {count} ({size}).',
    ', zakotwiczona w Bitcoinie':
        ', ancrée dans Bitcoin',
    'Adres usługi:':
        'Adresse du service\xa0:',
    'Brak fragmentu {cid} w kopii poza domem.':
        'Le fragment {cid} est absent de la copie hors site.',
    'Brak klucza albo hasła w Menedżerze poświadczeń Windows — zapisz ustawienia kopii poza domem jeszcze raz.':
        'La clé ou le mot de passe est absent du Gestionnaire d’identification Windows — enregistrez à nouveau les réglages de la copie hors site.',
    'Brak spisu wersji, którego dotyczy znacznik.':
        'La liste des fichiers de la version visée par l’horodatage est introuvable.',
    'Certyfikat PDF':
        'Certificat PDF',
    'Druga, zaszyfrowana kopia w usłudze zgodnej z S3 (np. Backblaze B2)':
        'Une seconde copie, chiffrée, dans un service compatible S3 (p. ex. Backblaze B2)',
    'Folder w kubełku:':
        'Dossier dans le compartiment\xa0:',
    'Hasło kopii poza domem':
        'Mot de passe de la copie hors site',
    'Hasło kopii poza domem nie pasuje do danych zapisanych w tym miejscu.':
        'Le mot de passe de la copie hors site ne correspond pas aux données enregistrées à cet emplacement.',
    'Hasło kopii poza domem powinno mieć co najmniej 10 znaków.':
        'Le mot de passe de la copie hors site doit comporter au moins 10 caractères.',
    'Hasło szyfrowania:':
        'Mot de passe de chiffrement\xa0:',
    'Identyfikator klucza:':
        'ID de clé\xa0:',
    'Katalog, do którego trafią pliki':
        'Dossier où iront les fichiers',
    'Klucz tajny':
        'Clé secrète',
    'Klucz tajny:':
        'Clé secrète\xa0:',
    'Kopia na dysku obok komputera nie przetrwa pożaru ani kradzieży. Tu ustawisz drugą kopię w usłudze zgodnej z S3 (np. Backblaze B2). Pliki są szyfrowane na tym komputerze osobnym hasłem — usługa widzi tylko nieczytelne fragmenty.':
        'Une sauvegarde sur un disque à côté de l’ordinateur ne survivra ni à un incendie ni à un vol. Configurez ici une seconde copie dans un service compatible S3 (p. ex. Backblaze B2). Les fichiers sont chiffrés sur cet ordinateur avec un mot de passe distinct — le service ne voit que des fragments illisibles.',
    'Kopia poza domem':
        'Copie hors site',
    'Kopia poza domem dla szablonu „{name}” zapisana.':
        'Copie hors site du modèle «\xa0{name}\xa0» enregistrée.',
    'Kopia poza domem nie ruszyła':
        'La copie hors site n’a pas démarré',
    'Kopia poza domem potrzebuje Menedżera poświadczeń Windows, a jest on niedostępny.':
        'La copie hors site a besoin du Gestionnaire d’identification Windows, qui n’est pas disponible.',
    'Kopia poza domem „{name}”':
        'Copie hors site «\xa0{name}\xa0»',
    'Kopia poza domem…':
        'Copie hors site…',
    'Korzeń tygodnia zakotwiczony w łańcuchu Bitcoina.':
        'La racine de la semaine est ancrée dans la blockchain Bitcoin.',
    'Kubełek (bucket):':
        'Compartiment (bucket)\xa0:',
    'Migawek w usłudze: {count}.':
        'Instantanés dans le service\xa0: {count}.',
    'Migawka i cel':
        'Instantané et destination',
    'Migawka kopii poza domem jest uszkodzona.':
        'L’instantané de la copie hors site est endommagé.',
    'Migawka {stamp}: plików bez zmian {reused}, wysłanych {files}, nowych fragmentów {chunks} ({size}).':
        'Instantané {stamp} — fichiers inchangés\xa0: {reused}, envoyés\xa0: {files}, nouveaux fragments\xa0: {chunks} ({size}).',
    'MinIO / Wasabi / inna zgodna z S3':
        'MinIO / Wasabi / autre service compatible S3',
    'NIEPOPRAWNY':
        'INVALIDE',
    'Nie ma migawki {stamp} w kopii poza domem.':
        'Aucun instantané {stamp} dans la copie hors site.',
    'Nie udało się połączyć z usługą przechowywania: {error}':
        'Impossible de se connecter au service de stockage\xa0: {error}',
    'Nie udało się wczytać migawek: {error}':
        'Impossible de charger les instantanés\xa0: {error}',
    'Nie udało się zapisać klucza albo hasła w magazynie systemowym.':
        'Impossible d’enregistrer la clé ou le mot de passe dans le coffre du système.',
    'Odśwież z sieci':
        'Actualiser en ligne',
    'Opis kopii poza domem jest uszkodzony.':
        'La description de la copie hors site est endommagée.',
    'Oznakowana: {utc} (BeatTime {beat})':
        'Horodatée\xa0: {utc} (BeatTime {beat})',
    'Pliki wersji różnią się od spisu, który został oznakowany.':
        'Les fichiers de la version diffèrent de la liste qui a été horodatée.',
    'Pobiera i odszyfrowuje pliki wybranej migawki':
        'Télécharge et déchiffre les fichiers de l’instantané choisi',
    'Pobiera listę migawek z usługi':
        'Télécharge la liste des instantanés depuis le service',
    'Pobiera podpis tygodnia i stan kotwicy w Bitcoinie':
        'Télécharge la signature hebdomadaire et l’état de l’ancrage Bitcoin',
    'Pobieram potwierdzenia…':
        'Téléchargement des reçus…',
    'Podaj hasło szyfrowania kopii poza domem.':
        'Saisissez le mot de passe de chiffrement de la copie hors site.',
    'Podaj klucz tajny usługi.':
        'Saisissez la clé secrète du service.',
    'Podam dane ręcznie':
        'Je saisirai les informations moi-même',
    'Pominięte (otwarte w innych programach albo zmienione w trakcie): {count}.':
        'Ignorés (ouverts dans d’autres programmes ou modifiés entre-temps)\xa0: {count}.',
    'Porządkowanie kopii poza domem…':
        'Nettoyage de la copie hors site…',
    'Potwierdzenia odświeżone.':
        'Reçus actualisés.',
    'Poza dom':
        'Hors site',
    'Połączenie działa: zapis, odczyt i usuwanie się udały.':
        'La connexion fonctionne\xa0: l’écriture, la lecture et la suppression ont réussi.',
    'Połączenie nie działa: {error}':
        'La connexion ne fonctionne pas\xa0: {error}',
    'Przywraca pliki z zaszyfrowanej kopii w usłudze S3 — także na nowym komputerze':
        'Restaure des fichiers depuis la copie chiffrée du service S3 — y compris sur un nouvel ordinateur',
    'Przywracanie z kopii poza domem':
        'Restauration depuis la copie hors site',
    'Przywracanie {count} {files} z kopii poza domem…':
        'Restauration de {count} {files} depuis la copie hors site…',
    'Przywróć':
        'Restaurer',
    'Region:':
        'Région\xa0:',
    'Skąd':
        'Source',
    'Spis wersji zgodny ze znacznikiem: {answer}':
        'Liste des fichiers conforme à l’horodatage\xa0: {answer}',
    'Spis wersji został zmieniony po oznakowaniu.':
        'La liste des fichiers de la version a été modifiée après l’horodatage.',
    'Sprawdza spis wersji, drogę w drzewie tygodnia i podpis — bez sieci':
        'Vérifie la liste des fichiers, le chemin dans l’arbre de la semaine et la signature — hors ligne',
    'Sprawdzam połączenie…':
        'Vérification de la connexion…',
    'Sprawdź':
        'Vérifier',
    'Sprawdź połączenie':
        'Tester la connexion',
    'Starsze migawki są usuwane, gdy nadmiar sięgnie kilku — co kilka dni.':
        'Les instantanés plus anciens sont supprimés lorsque l’excédent atteint quelques unités — donc à quelques jours d’intervalle.',
    'Suma w drzewie tygodnia: {answer}':
        'Empreinte dans l’arbre de la semaine\xa0: {answer}',
    'Suma wersji nie należy do drzewa tygodnia podanego w potwierdzeniu.':
        'L’empreinte de la version ne fait pas partie de l’arbre de la semaine indiqué dans le reçu.',
    'Ta wersja nie ma znacznika czasu.':
        'Cette version n’a pas d’horodatage.',
    'Także po kopiach planowych. Wysyłane są tylko pliki nowe i zmienione.':
        'Aussi après les sauvegardes planifiées. Seuls les fichiers nouveaux et modifiés sont envoyés.',
    'Tydzień jeszcze się nie zamknął — podpis pojawi się po poniedziałku 00:00 UTC.':
        'La semaine n’est pas encore close — la signature apparaîtra après lundi 00:00 UTC.',
    'Usunięto starsze migawki: {count}, nieużywane fragmenty: {chunks}.':
        'Anciens instantanés supprimés\xa0: {count}\xa0; fragments inutilisés\xa0: {chunks}.',
    'Usługa chwilowo niedostępna ({status}).':
        'Service temporairement indisponible ({status}).',
    'Usługa odrzuciła żądanie ({status} {code}): {message}':
        'Le service a rejeté la requête ({status} {code})\xa0: {message}',
    'Usługa przechowywania':
        'Service de stockage',
    'Usługa zwróciła inną treść niż zapisana.':
        'Le service a renvoyé un contenu différent de celui qui a été écrit.',
    'Usługa:':
        'Service\xa0:',
    'Uzupełnij adres usługi, nazwę kubełka i klucze dostępu.':
        'Renseignez l’adresse du service, le nom du compartiment et les clés d’accès.',
    'Uzupełnij adres usługi, region, kubełek i identyfikator klucza.':
        'Renseignez l’adresse du service, la région, le compartiment et l’ID de clé.',
    'W tym katalogu kopii nie ma jeszcze znaczników czasu.':
        'Ce dossier de sauvegarde ne contient encore aucun horodatage.',
    'W tym miejscu nie ma jeszcze kopii poza domem.':
        'Il n’y a pas encore de copie hors site à cet emplacement.',
    'Wczytaj migawki':
        'Charger les instantanés',
    'Wczytaj migawki i wybierz jedną z listy.':
        'Chargez les instantanés et choisissez-en un dans la liste.',
    'Wczytuję migawkę {stamp}…':
        'Chargement de l’instantané {stamp}…',
    'Wczytuję poprzednią migawkę kopii poza domem…':
        'Chargement de l’instantané précédent de la copie hors site…',
    'Wybierz migawkę i katalog, do którego trafią pliki.':
        'Choisissez un instantané et le dossier où iront les fichiers.',
    'Wybierz wersję z listy.':
        'Choisissez une version dans la liste.',
    'Wysyłaj poza dom po każdej udanej kopii z tego szablonu':
        'Envoyer hors site après chaque sauvegarde réussie de ce modèle',
    'Wysyłam poza dom pliki nowe i zmienione: {count}…':
        'Envoi hors site des fichiers nouveaux et modifiés\xa0: {count}…',
    'Z kopii poza domem…':
        'Depuis la copie hors site…',
    'Zachowuj migawek:':
        'Instantanés à conserver\xa0:',
    'Zapisuje ustawienia; klucz i hasło trafiają do Menedżera poświadczeń Windows':
        'Enregistre les réglages\xa0; la clé et le mot de passe vont dans le Gestionnaire d’identification Windows',
    'Zapisuje, odczytuje i usuwa mały plik próbny':
        'Écrit, lit et supprime un petit fichier de test',
    'Zapisuję migawkę {stamp}…':
        'Enregistrement de l’instantané {stamp}…',
    'Znacznik dowodzi, że wersja kopii w dokładnie tym kształcie istniała w podanej chwili. Podpis tygodnia pojawia się po jego zamknięciu (poniedziałek 00:00 UTC), a kotwica w Bitcoinie — zwykle kilka godzin później.':
        'L’horodatage prouve que la version de la sauvegarde existait exactement sous cette forme au moment indiqué. La signature hebdomadaire apparaît à la clôture de la semaine (lundi 00:00 UTC), et l’ancrage Bitcoin généralement quelques heures plus tard.',
    'Znacznika czasu nie udało się zapisać: {error}':
        'Impossible d’enregistrer l’horodatage\xa0: {error}',
    'Znaczniki czasu':
        'Horodatages',
    'Znaczniki czasu…':
        'Horodatages…',
    'kopia poza domem':
        'copie hors site',
    'np. komputer-domowy':
        'p. ex. ordinateur-maison',
    'oznakowana {when} — podpis po zamknięciu tygodnia':
        'horodatée le {when} — signature après la clôture de la semaine',
    'podpisana (tydzień {week}){bitcoin}':
        'signée (semaine {week}){bitcoin}',
    'poprawny':
        'valide',
    'przywracanie z kopii poza domem':
        'restauration depuis la copie hors site',
    'Łączę się z usługą…':
        'Connexion au service…',
    ' dni':
        ' jours',
    ' mies.':
        ' mois',
    ' tyg.':
        ' sem.',
    'Ile ostatnich wersji zachować. Starsze są kasowane po udanym przebiegu.':
        'Nombre de versions récentes à conserver. Les plus anciennes sont supprimées après une exécution réussie.',
    'Kalendarz zostawia najnowszą wersję z każdego z ostatnich dni, tygodni\ni miesięcy — gęsto dla świeżych zmian, rzadko dla dawnych. Nadmiar jest\nkasowany po udanym przebiegu; wersje niedokończone nigdy.':
        'Le calendrier garde la version la plus récente de chacun des derniers jours, semaines\net mois — dense pour les changements récents, espacé pour les anciens. L’excédent est\nsupprimé après une exécution réussie\xa0; les versions inachevées, jamais.',
    'Z ilu ostatnich dni zachować po jednej, najnowszej wersji.':
        'Pour combien des derniers jours conserver une version — la plus récente de chacun.',
    'Z ilu ostatnich miesięcy zachować po jednej, najnowszej wersji.':
        'Pour combien des derniers mois conserver une version — la plus récente de chacun.',
    'Z ilu ostatnich tygodni zachować po jednej, najnowszej wersji.':
        'Pour combien des dernières semaines conserver une version — la plus récente de chacune.',
    'Zachowuj:':
        'Conserver\xa0:',
    'kalendarz: dni, tygodnie, miesiące':
        'calendrier\xa0: jours, semaines, mois',
    'ostatnie wersje':
        'versions récentes',
    'wszystkie wersje':
        'toutes les versions',
    ' (niedokończona)':
        ' (inachevée)',
    'Fragment nazwy albo ścieżki, bez rozróżniania wielkości liter.':
        'Partie d’un nom ou d’un chemin, sans tenir compte de la casse.',
    'Główny folder kopii':
        'Dossier principal de la sauvegarde',
    'Historia pliku':
        'Historique du fichier',
    'Nazwa':
        'Nom',
    'Nic nie znaleziono.':
        'Aucun résultat.',
    'Nie udało się: {error}':
        'Échec\xa0: {error}',
    'Odtwarza plik do katalogu tymczasowego i otwiera go':
        'Restaure le fichier dans un dossier temporaire et l’ouvre',
    'Odtwarza plik w wybranym miejscu':
        'Restaure le fichier à l’emplacement de votre choix',
    'Odtwarzam „{name}”…':
        'Restauration de «\xa0{name}\xa0»…',
    'Otwarto kopię „{name}” (plik tymczasowy, zniknie po zamknięciu programu).':
        'Copie de «\xa0{name}\xa0» ouverte (fichier temporaire, supprimé à la fermeture du programme).',
    'Otwórz':
        'Ouvrir',
    'Otwórz kopię':
        'Ouvrir une copie',
    'Pliki i wersje wprost z kopii — bez przywracania':
        'Fichiers et versions directement dans la sauvegarde — sans restauration',
    'Pliki i wersje wprost z kopii — bez przywracania całości.':
        'Fichiers et versions directement dans la sauvegarde — sans tout restaurer.',
    'Pokazuje pliki i wersje tej kopii — pojedynczy plik otworzysz bez przywracania całości':
        'Affiche les fichiers et les versions de cette sauvegarde — ouvrez un seul fichier sans tout restaurer',
    'Pokaż foldery':
        'Afficher les dossiers',
    'Przeglądaj…':
        'Parcourir…',
    'Przeglądanie':
        'Parcourir',
    'Przeszukuje spis treści kopii':
        'Recherche dans la table des matières de la sauvegarde',
    'Rozmiar':
        'Taille',
    'Szukaj':
        'Rechercher',
    'Szukaj pliku w najnowszym stanie kopii…':
        'Rechercher un fichier dans le dernier état de la sauvegarde…',
    'Szukam…':
        'Recherche…',
    'W których wersjach jest ten plik i kiedy się zmieniał':
        'Dans quelles versions se trouve ce fichier et quand il a changé',
    'W tym folderze nie ma wersji kopii.':
        'Ce dossier ne contient aucune version de sauvegarde.',
    'Wczytuje wersje z tego folderu kopii':
        'Charge les versions de ce dossier de sauvegarde',
    'Wersja kopii, której zawartość widzisz poniżej.':
        'La version de la sauvegarde dont vous voyez le contenu ci-dessous.',
    'Wersja: {version}':
        'Version\xa0: {version}',
    'Wersje z tym plikiem: {count}. Dwuklik otwiera kopię z danej wersji.':
        'Versions contenant ce fichier\xa0: {count}. Un double-clic ouvre la copie de la version choisie.',
    'Wraca z wyników wyszukiwania do drzewa folderów':
        'Revient des résultats de recherche à l’arborescence des dossiers',
    'Wskaż folder kopii i kliknij „Otwórz”.':
        'Indiquez le dossier de la sauvegarde et cliquez sur «\xa0Ouvrir\xa0».',
    'Zapisano: {path}':
        'Enregistré\xa0: {path}',
    'Zapisz jako…':
        'Enregistrer sous…',
    'Zapisz kopię pliku':
        'Enregistrer une copie du fichier',
    'Zaznacz plik i wybierz „Otwórz kopię”, żeby zajrzeć do niego w zwykłym programie, albo „Historia pliku”, żeby zobaczyć, w których wersjach się zmieniał.':
        'Sélectionnez un fichier et choisissez «\xa0Ouvrir une copie\xa0» pour le consulter dans son programme habituel, ou «\xa0Historique du fichier\xa0» pour voir dans quelles versions il a changé.',
    'Zmieniono':
        'Modifié',
    'Znalezione pliki: {count}. Wyniki pochodzą z najnowszego stanu kopii.':
        'Fichiers trouvés\xa0: {count}. Les résultats proviennent du dernier état de la sauvegarde.',
    'przeglądanie kopii':
        'parcours de la sauvegarde',
    'zmieniony':
        'modifié',
    'najstarsza zachowana kopia':
        'plus ancienne copie conservée',
    'Foldery w AppData':
        'Dossiers dans AppData',
    'Przywracanie utworzy nowe foldery bezpośrednio w AppData:\n\n{folders}\n\nWindows pozwala wersji programu ze Sklepu tworzyć je tylko w jej prywatnej kopii — pliki będą widoczne w tym programie, ale nie w programie, do którego należą.\n\nNajprościej: zainstaluj i raz uruchom tamten program (utworzy swój folder), a potem przywróć jeszcze raz. Albo przywróć do zwykłego folderu i przenieś pliki Eksploratorem.':
        'La restauration va créer de nouveaux dossiers directement dans AppData\xa0:\n\n{folders}\n\nWindows ne permet à la version Microsoft Store de ce programme de les créer que dans sa copie privée — les fichiers seront visibles dans ce programme, mais pas dans le programme auquel ils appartiennent.\n\nLe plus simple\xa0: installez cet autre programme et lancez-le une fois (il créera son dossier), puis restaurez à nouveau. Ou restaurez dans un dossier ordinaire et déplacez les fichiers avec l’Explorateur de fichiers.',
    'Przywracanie utworzyłoby w AppData nowe foldery, których inne programy nie zobaczą: {folders}':
        'La restauration créerait dans AppData de nouveaux dossiers que les autres programmes ne verront pas\xa0: {folders}',
    'Przywracanie wstrzymane do decyzji.':
        'Restauration suspendue en attente de votre décision.',
    'Przywróć mimo to':
        'Restaurer quand même',
    'Start programu przy logowaniu wyłączono w Ustawieniach Windows. Włączysz go tam: Ustawienia → Aplikacje → Uruchamianie → Sigelith Backup.':
        'Le lancement du programme à l’ouverture de session a été désactivé dans les Paramètres Windows. Pour le réactiver\xa0: Paramètres → Applications → Démarrage → Sigelith Backup.',
    'Start przy logowaniu':
        'Lancement à l’ouverture de session',
    'Start przy logowaniu wyłączono w Ustawieniach Windows → Aplikacje → Uruchamianie; dopóki go tam nie włączysz, kopie planowe działają tylko przy otwartym programie.':
        'Le lancement à l’ouverture de session a été désactivé dans Paramètres Windows → Applications → Démarrage\xa0; tant que vous ne l’y réactivez pas, les sauvegardes planifiées ne s’exécutent que lorsque le programme est ouvert.',
    'Ten sam przełącznik jest w Ustawieniach Windows → Aplikacje → Uruchamianie. Wyłączony tam da się włączyć tylko tam.':
        'Le même interrupteur se trouve dans Paramètres Windows → Applications → Démarrage. S’il y a été désactivé, c’est seulement là qu’il peut être réactivé.',
    'Brak pliku {name} w katalogu programu.':
        'Le fichier {name} est absent du dossier du programme.',
    'Jakie dane program przetwarza i gdzie':
        'Quelles données le programme traite, et où',
    'Kod źródłowy Qt':
        'Code source de Qt',
    'Licencja programu':
        'Licence du programme',
    'Licencja programu i licencje użytych składników':
        'Licence du programme et licences des composants utilisés',
    'Licencje':
        'Licences',
    'Licencje i prywatność':
        'Licences et confidentialité',
    'Licencje…':
        'Licences…',
    'Otwiera folder z plikami licencji w Eksploratorze':
        'Ouvre le dossier des fichiers de licence dans l’Explorateur de fichiers',
    'Pokaż pliki licencji':
        'Afficher les fichiers de licence',
    'Polityka prywatności':
        'Politique de confidentialité',
    'Polityka prywatności…':
        'Politique de confidentialité…',
    'Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0 — to osobne pliki w katalogu programu, które można zastąpić zgodnymi wersjami. Kod źródłowy wersji dołączonych do programu: {qt} oraz {pyside}.':
        'Le programme utilise les bibliothèques Qt et PySide6 sous licence LGPL-3.0 — ce sont des fichiers distincts dans le dossier du programme, qui peuvent être remplacés par des versions compatibles. Code source des versions fournies avec le programme\xa0: {qt} et {pyside}.',
    'Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0, z Pythona i z innych składników na licencjach otwartych (m.in. MIT, BSD, Apache 2.0); ikony: Bootstrap Icons (MIT). Wykaz, prawa autorskie, pełne teksty licencji i adresy kodu źródłowego Qt są pod przyciskiem „Licencje”.':
        'Le programme utilise les bibliothèques Qt et PySide6 sous licence LGPL-3.0, Python et d’autres composants sous licences libres (notamment MIT, BSD, Apache 2.0)\xa0; icônes\xa0: Bootstrap Icons (MIT). La liste, les mentions de droits d’auteur, les textes complets des licences et les adresses du code source de Qt se trouvent sous le bouton «\xa0Licences\xa0».',
    'Program usunie z Menedżera poświadczeń Windows wszystkie hasła, które zapamiętał: hasła kopii i dane dostępu do kopii poza domem. Kopie planowe szablonów zaszyfrowanych będą potem czekać, aż podasz hasło.\n\nUsunąć?':
        'Le programme va supprimer du Gestionnaire d’identification Windows tous les mots de passe qu’il a mémorisés\xa0: mots de passe des sauvegardes et identifiants de la copie hors site. Les sauvegardes planifiées des modèles chiffrés attendront ensuite que vous saisissiez le mot de passe.\n\nSupprimer\xa0?',
    'Składniki i ich licencje':
        'Composants et leurs licences',
    'Strona z kodem źródłowym Qt w wersji użytej w programie':
        'La page du code source de Qt, dans la version utilisée par le programme',
    'Usunięte zapamiętane hasła: {count}.':
        'Mots de passe mémorisés supprimés\xa0: {count}.',
    'Usuwa z Menedżera poświadczeń Windows wszystkie hasła zapamiętane przez program — na przykład przed odinstalowaniem':
        'Supprime du Gestionnaire d’identification Windows tous les mots de passe mémorisés par le programme — par exemple avant la désinstallation',
    'Usuń zapamiętane hasła':
        'Supprimer les mots de passe mémorisés',
    'Usuń zapamiętane hasła…':
        'Supprimer les mots de passe mémorisés…',
    '© {years} {publisher}. Wolne oprogramowanie na licencji GNU GPL w wersji 3 lub nowszej.':
        '© {years} {publisher}. Logiciel libre sous licence GNU GPL version 3 ou ultérieure.',
    'Kod źródłowy':
        'Code source',
    'Kod źródłowy programu w serwisie GitHub':
        'Le code source du programme sur GitHub',
    'Sigelith odrzucił żądanie ({status}): {detail}':
        'Sigelith a rejeté la requête ({status})\xa0: {detail}',
    'Nie udało się połączyć z Sigelith: {error}':
        'Impossible de se connecter à Sigelith\xa0: {error}',
    'Sigelith odesłał potwierdzenie innej sumy kontrolnej.':
        'Sigelith a renvoyé un reçu pour une autre empreinte.',
    'Znacznik czeka na połączenie z Sigelith.':
        'L’horodatage attend une connexion à Sigelith.',
    'Podpis tygodnia nie zgadza się z kluczem Sigelith zapisanym w programie.':
        'La signature hebdomadaire ne correspond pas à la clé Sigelith intégrée au programme.',
    'Otwiera certyfikat znacznika na stronie Sigelith':
        'Ouvre le certificat de l’horodatage sur le site de Sigelith',
    'Podpis Sigelith: {answer}':
        'Signature Sigelith\xa0: {answer}',
    'Znaczniki Sigelith wersji w tym katalogu kopii: sprawdzenie i certyfikat':
        'Horodatages Sigelith des versions de ce dossier de sauvegarde\xa0: vérification et certificat',
    'Znakuję wersję czasem Sigelith (wysyłana jest tylko suma kontrolna)…':
        'Horodatage de la version avec Sigelith (seule l’empreinte est envoyée)…',
    'Znacznik czasu czeka na połączenie z Sigelith — zostanie wysłany przy następnej kopii.':
        'L’horodatage attend une connexion à Sigelith — il sera envoyé lors de la prochaine sauvegarde.',
    'Znakuj wersję czasem Sigelith':
        'Horodater la version avec Sigelith',
    'Znaczniki czasu Sigelith':
        'Horodatages Sigelith',
    'czeka na połączenie z Sigelith':
        'en attente de connexion à Sigelith',
    'Dowód, że kopia w tym kształcie istniała danego dnia (podpis Ed25519, kotwica\nw Bitcoinie). Do sigelith.org trafia wyłącznie suma kontrolna spisu wersji —\nżadne nazwy plików ani ich treść.':
        'La preuve que la sauvegarde existait sous cette forme à une date donnée (signature Ed25519,\nancrage Bitcoin). Seule l’empreinte de la liste des fichiers de la version part vers sigelith.org —\naucun nom de fichier, aucun contenu.',
    'Kopie zapasowe folderów na dysk zewnętrzny, z historią wersji i szyfrowaniem. Wszystko dzieje się na Twoim komputerze, bez konta i bez telemetrii. Z internetem program łączy się tylko wtedy, gdy sam włączysz kopię poza domem albo znaczniki czasu Sigelith.':
        'Des sauvegardes de vos dossiers sur un disque externe, avec historique des versions et chiffrement. Tout se passe sur votre ordinateur, sans compte et sans télémétrie. Le programme ne se connecte à internet que si vous activez vous-même la copie hors site ou les horodatages Sigelith.',
    'Bez dokumentu: {count} {stamps} — plik zmienił się po stemplu albo zniknął i nie ma go w żadnej wersji tej kopii ({names}). Sam dowód jest zachowany.':
        'Sans document\xa0: {count} {stamps} — le fichier a changé après l’horodatage ou a disparu, et il ne figure dans aucune version de cette sauvegarde ({names}). La preuve elle-même est conservée.',
    'Brak pliku dowodu albo dowód jest zaszyfrowany.':
        'Le fichier de preuve est absent ou la preuve est chiffrée.',
    'Chroni dowody Sigelith: historię stempli i oznakowane dokumenty.':
        'Protège les preuves Sigelith\xa0: l’historique des horodatages et les documents horodatés.',
    'Chroń dowody Sigelith':
        'Protéger les preuves Sigelith',
    'Chroń też dowody Sigelith':
        'Protéger aussi les preuves Sigelith',
    'Dokument':
        'Document',
    'Dokumenty oznakowane w Sigelith, zabezpieczone w tej kopii: sprawdzenie i odzyskanie':
        'Documents horodatés avec Sigelith et mis en sécurité dans cette sauvegarde\xa0: vérification et récupération',
    'Dowody Sigelith':
        'Preuves Sigelith',
    'Dowody Sigelith: historia stempli i dokładne kopie oznakowanych dokumentów z plikami .beatproof trafią do magazynu dowodów w katalogu kopii.':
        'Preuves Sigelith\xa0: l’historique des horodatages et des copies exactes des documents horodatés, avec leurs fichiers .beatproof, iront dans le dépôt de preuves du dossier de sauvegarde.',
    'Dowody Sigelith: zabezpieczone dokumenty {count} z {total}':
        'Preuves Sigelith\xa0: documents mis en sécurité — {count} sur {total}',
    'Dowody Sigelith…':
        'Preuves Sigelith…',
    'Dowody z problemem: {count} — szczegóły w kolumnie „Stan”.':
        'Preuves présentant un problème\xa0: {count} — détails dans la colonne «\xa0État\xa0».',
    'Dowodów Sigelith nie udało się zabezpieczyć: {error}':
        'Impossible de mettre en sécurité les preuves Sigelith\xa0: {error}',
    "Droga w drzewie Merkle'a nie prowadzi do podpisanego korzenia tygodnia.":
        'Le chemin dans l’arbre de Merkle ne mène pas à la racine signée de la semaine.',
    'Gdzie zapisać dokumenty i dowody':
        'Où enregistrer les documents et les preuves',
    'Historia stempli Sigelith Desktop i dokładne bajty oznakowanych dokumentów, z plikami .beatproof — w osobnym magazynie, którego retencja nie sprząta.':
        'L’historique des horodatages de Sigelith Desktop et les octets exacts des documents horodatés, avec les fichiers .beatproof — dans un dépôt distinct que la politique de rétention ne purge jamais.',
    'Każdy stempel ma tu swój folder z dokładnie tym dokumentem, który oznakowano, i plikiem .beatproof. „Sprawdź” liczy sumę każdego dokumentu i sprawdza podpis tygodnia bez łączenia się z siecią.':
        'Chaque horodatage a ici son propre dossier, avec exactement le document qui a été horodaté et son fichier .beatproof. «\xa0Vérifier\xa0» calcule l’empreinte de chaque document et vérifie la signature hebdomadaire sans se connecter au réseau.',
    'Kopia obejmie folder danych Sigelith Desktop (historię stempli), a każdy oznakowany\ndokument trafi — dokładnie w tej postaci, którą oznakowano — do magazynu dowodów\nw katalogu kopii, razem z plikiem .beatproof. Starych wersji magazyn nie dotyczy:\nretencja go nie sprząta.':
        'La sauvegarde inclura le dossier de données de Sigelith Desktop (l’historique des horodatages), et chaque\ndocument horodaté ira — exactement tel qu’il a été horodaté — dans le dépôt de preuves\ndu dossier de sauvegarde, avec son fichier .beatproof. Ce dépôt est indépendant des anciennes versions\xa0:\nla politique de rétention ne le purge jamais.',
    'Magazyn dowodów jest pusty.':
        'Le dépôt de preuves est vide.',
    'Na tym komputerze jest Sigelith Desktop: {count} {stamps}.':
        'Sigelith Desktop est installé sur cet ordinateur\xa0: {count} {stamps}.',
    'Na tym komputerze nie ma danych Sigelith Desktop.':
        'Aucune donnée de Sigelith Desktop sur cet ordinateur.',
    'Otwórz folder dowodów':
        'Ouvrir le dossier des preuves',
    'Oznakowano':
        'Horodaté',
    'Pokazuje magazyn dowodów w Eksploratorze':
        'Affiche le dépôt de preuves dans l’Explorateur de fichiers',
    'Przywróć zaznaczone…':
        'Restaurer la sélection…',
    'Sigelith Desktop: {count} {stamps} w folderze {path}.':
        'Sigelith Desktop\xa0: {count} {stamps} dans le dossier {path}.',
    'Sprawdza każdy dokument i jego dowód bez łączenia z siecią':
        'Vérifie chaque document et sa preuve sans connexion au réseau',
    'Sprawdzam dowody…':
        'Vérification des preuves…',
    'Stan':
        'État',
    'Stemple w magazynie: {count}, z dokumentem: {documents}.':
        'Horodatages dans le dépôt\xa0: {count}, avec document\xa0: {documents}.',
    'Suma dokumentu nie zgadza się z dowodem.':
        'L’empreinte du document ne correspond pas à la preuve.',
    'To nie jest plik dowodu Sigelith (beatproof-v1).':
        'Ce n’est pas un fichier de preuve Sigelith (beatproof-v1).',
    'Tydzień stempla jeszcze się nie zamknął — podpis dojdzie przy kolejnej kopii.':
        'La semaine de l’horodatage n’est pas encore close — la signature sera ajoutée lors d’une prochaine sauvegarde.',
    'W magazynie nie ma dokumentu do tego dowodu.':
        'Le dépôt ne contient pas le document de cette preuve.',
    'Wszystkie dowody pasują do dokumentów i mają poprawny podpis.':
        'Toutes les preuves correspondent à leurs documents et ont une signature valide.',
    'Zabezpieczam dokumenty oznakowane w Sigelith…':
        'Mise en sécurité des documents horodatés avec Sigelith…',
    'Zapisano pliki: {count} w {path}.':
        'Fichiers enregistrés\xa0: {count} dans {path}.',
    'Zapisuje dokumenty razem z plikami .beatproof we wskazanym folderze':
        'Enregistre les documents avec leurs fichiers .beatproof dans le dossier choisi',
    'bez dokumentu — dowód zachowany':
        'sans document — preuve conservée',
    'czekają na podpis tygodnia: {count}':
        'en attente de la signature hebdomadaire\xa0: {count}',
    'dokument i dowód są w kopii':
        'document et preuve dans la sauvegarde',
    'dokument jest; dowód czeka na podpis tygodnia':
        'document présent\xa0; preuve en attente de la signature hebdomadaire',
    'dowodu nie da się odczytać':
        'preuve illisible',
    'dowody Sigelith':
        'preuves Sigelith',
    'dowody uzupełnione o podpis tygodnia: {count}':
        'preuves complétées par la signature hebdomadaire\xa0: {count}',
    'nowe: {count}':
        'nouveaux\xa0: {count}',
    'odtworzone ze starszych wersji kopii: {count}':
        'récupérés dans des versions plus anciennes de la sauvegarde\xa0: {count}',
    'sprawdzony: dokument i dowód się zgadzają':
        'vérifié\xa0: le document et la preuve correspondent',
    'stempel':
        'horodatage',
    'stemple':
        'horodatages',
    'stempli':
        'horodatages',
    'zaszyfrowany — podaj hasło, żeby sprawdzić':
        'chiffré — saisissez le mot de passe pour vérifier',
    'Chroń dowody Sigelith, gdy go zainstaluję':
        'Protéger les preuves Sigelith quand je l’aurai installé',
    'Dowody Sigelith: na tym komputerze nie ma jeszcze Sigelith Desktop — ochrona zacznie działać sama, gdy się pojawi.':
        'Preuves Sigelith\xa0: Sigelith Desktop n’est pas encore installé sur cet ordinateur — la protection démarrera d’elle-même dès qu’il apparaîtra.',
    'Dowody Sigelith: ochrona zacznie działać sama, gdy zainstalujesz Sigelith Desktop.':
        'Preuves Sigelith\xa0: la protection démarrera d’elle-même dès que vous installerez Sigelith Desktop.',
    'Dowody czasu dla ważnych dokumentów':
        'Preuves horodatées pour les documents importants',
    'Kopia zachowa każdy dokument oznakowany w Sigelith Desktop dokładnie w tej postaci, którą oznakowano, razem z dowodem — nawet gdy oryginał później się zmieni.':
        'La sauvegarde conservera chaque document horodaté avec Sigelith Desktop exactement tel qu’il a été horodaté, avec sa preuve — même si l’original change ensuite.',
    'Ochrona zacznie działać sama, gdy na komputerze pojawi się Sigelith Desktop.':
        'La protection démarrera d’elle-même dès que Sigelith Desktop apparaîtra sur l’ordinateur.',
    'Otwiera stronę programu Sigelith Desktop':
        'Ouvre la page de Sigelith Desktop',
    'Poznaj Sigelith Desktop':
        'Découvrir Sigelith Desktop',
    'Sigelith Desktop, program tego samego wydawcy, oznakuje dokument czasem: to podpisany dowód, że plik w tej postaci istniał w danej chwili, sprawdzalny bez udziału kogokolwiek. Sigelith Backup przechowa potem każdy oznakowany dokument razem z dowodem.':
        'Sigelith Desktop, un programme du même éditeur, horodate un document\xa0: une preuve signée que le fichier existait sous cette forme à un moment donné, vérifiable sans dépendre de personne. Sigelith Backup conserve ensuite chaque document horodaté avec sa preuve.',
    'Umowy, faktury, projekty — czasem trzeba wykazać, że dokument istniał danego dnia.':
        'Contrats, factures, projets — il faut parfois prouver qu’un document existait à une date donnée.',
    'Nieznany format spisu wersji.':
        'Format inconnu de la liste des fichiers de la version.',
    'Ta wersja nie ma pieczęci dla pojedynczych plików (kopia sprzed wersji 3.0 albo bez znaczników czasu).':
        'Cette version n’a pas de sceau pour les fichiers individuels (sauvegarde antérieure à la version 3.0 ou sans horodatages).',
    'Pieczęć tej wersji czeka jeszcze na podpis tygodnia Sigelith — dowód będzie gotowy po poniedziałku 00:00 UTC i kolejnej kopii.':
        'Le sceau de cette version attend encore la signature hebdomadaire de Sigelith — la preuve sera prête après lundi 00:00 UTC et la sauvegarde suivante.',
    'Brak oświadczenia pieczęci w folderze wersji.':
        'La déclaration du sceau est absente du dossier de la version.',
    'Oświadczenie pieczęci nie zgadza się z pieczęcią wersji.':
        'La déclaration du sceau ne correspond pas au sceau de la version.',
    'Drzewo plików wersji nie zgadza się z pieczęcią.':
        'L’arbre des fichiers de la version ne correspond pas au sceau.',
    'Tego pliku nie ma w spisie tej wersji.':
        'Ce fichier ne figure pas dans la liste de cette version.',
    'To nie jest dowód pliku z kopii Sigelith Backup ({format}).':
        'Ce n’est pas une preuve de fichier Sigelith Backup ({format}).',
    'Dowód jest uszkodzony — brakuje pól albo mają zły format.':
        'La preuve est endommagée — des champs manquent ou sont mal formés.',
    'Ten plik nie jest plikiem, którego dotyczy dowód.':
        'Ce fichier n’est pas celui que concerne la preuve.',
    'Ścieżka pliku w dowodzie nie zgadza się z liściem drzewa.':
        'Le chemin du fichier dans la preuve ne correspond pas à la feuille de l’arbre.',
    'Droga w drzewie plików nie prowadzi do korzenia z pieczęci.':
        'Le chemin dans l’arbre des fichiers ne mène pas à la racine scellée.',
    'Oświadczenie pieczęci nie potwierdza tego drzewa plików.':
        'La déclaration du sceau ne confirme pas cet arbre de fichiers.',
    'Potwierdzenie Sigelith nie dotyczy tej pieczęci.':
        'La confirmation Sigelith ne concerne pas ce sceau.',
    'Dowód czasu…':
        'Preuve horodatée…',
    'Zapisuje dowód, że ten plik był w kopii w chwili jej oznakowania — bez ujawniania innych plików':
        'Enregistre la preuve que ce fichier se trouvait dans la sauvegarde au moment où elle a été scellée — sans révéler les autres fichiers',
    'Dowód czasu':
        'Preuve horodatée',
    'Dołączyć do dowodu ścieżkę pliku w kopii („{path}”)?\n\nBez niej dowód dalej potwierdza plik i chwilę oznakowania, ale nie mówi, gdzie plik leżał.':
        'Inclure dans la preuve le chemin du fichier dans la sauvegarde («\xa0{path}\xa0»)\xa0?\n\nSans lui, la preuve confirme toujours le fichier et le moment du scellement, mais n’indique pas où se trouvait le fichier.',
    'Przygotowuję dowód dla „{name}”…':
        'Préparation de la preuve pour «\xa0{name}\xa0»…',
    'Zapisz dowód czasu':
        'Enregistrer la preuve horodatée',
    'Dowód pliku Sigelith (*{suffix})':
        'Preuve de fichier Sigelith (*{suffix})',
    'Zapisano dowód i certyfikat PDF: {path}. Sprawdzi go Sigelith Desktop albo strona sigelith.org/verify/.':
        'Preuve et certificat PDF enregistrés\xa0: {path}. Sigelith Desktop ou la page sigelith.org/verify/ peuvent la vérifier.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją sprawdzić.':
        'La sauvegarde est chiffrée — saisissez le mot de passe pour la vérifier.',
    'Ta wersja nie ma pieczęci — nie ma z czym porównać plików.':
        'Cette version n’a pas de sceau — impossible de comparer les fichiers.',
    'Pieczęć wersji się nie potwierdza: {problems}':
        'Le sceau de la version n’est pas confirmé\xa0: {problems}',
    'brak podpisu tygodnia':
        'pas de signature hebdomadaire',
    'Audyt przerwany.':
        'Audit interrompu.',
    'próbka {checked} z {listed} plików':
        'un échantillon de {checked} fichiers sur {listed}',
    'wszystkie pliki ({count})':
        'tous les fichiers ({count})',
    'Nietknięta: sprawdzono {scope}, wszystko zgodne z pieczęcią w publicznym dzienniku.':
        'Intacte — vérifié\xa0: {scope}\xa0; tout est conforme au sceau du journal public.',
    'zmienione: {files}':
        'modifiés\xa0: {files}',
    'brakujące: {files}':
        'manquants\xa0: {files}',
    'nieczytelne albo uszkodzone: {files}':
        'illisibles ou endommagés\xa0: {files}',
    'PODMIENIONA albo uszkodzona ({scope}) — {details}.':
        'FALSIFIÉE ou endommagée ({scope}) — {details}.',
    'Audyt treści':
        'Audit du contenu',
    'Czyta z nośnika każdy plik tej wersji i porównuje go z sumą oznakowaną w publicznym dzienniku':
        'Lit sur le support chaque fichier de cette version et le compare à l’empreinte scellée dans le journal public',
    'Ostatnia nietknięta':
        'Dernière intacte',
    'Sprawdza wersje od najnowszej i wskazuje ostatnią zgodną z pieczęcią — z niej przywracaj':
        'Vérifie les versions en partant de la plus récente et indique la dernière conforme à son sceau — restaurez à partir de celle-ci',
    'Ostatnia nietknięta wersja: {label} — z niej przywracaj.':
        'Dernière version intacte\xa0: {label} — restaurez à partir de celle-ci.',
    'Żadna wersja z pieczęcią nie jest nietknięta.':
        'Aucune version scellée n’est intacte.',
    'Czytam pliki kopii i porównuję je z pieczęcią w publicznym dzienniku…':
        'Lecture des fichiers de la sauvegarde et comparaison avec le sceau du journal public…',
    'Sprawdzam próbkę starszej wersji z pieczęcią w publicznym dzienniku…':
        'Vérification d’un échantillon d’une version plus ancienne par rapport à son sceau dans le journal public…',
    'Audyt z pieczęcią: próbka wersji {label} zgodna z publicznym dziennikiem.':
        'Audit par le sceau\xa0: l’échantillon de la version {label} est conforme au journal public.',
    'UWAGA — audyt z pieczęcią, wersja {label}: {details}':
        'ATTENTION — audit par le sceau, version {label}\xa0: {details}',
    'Przekaż…':
        'Remettre…',
    'Zapisuje tę wersję pliku i otwiera ją w Sigelith Handover — odbiorca potwierdzi odbiór własnym kluczem':
        'Enregistre cette version du fichier et l’ouvre dans Sigelith Handover — le destinataire confirmera la réception avec sa propre clé',
    'Przekazanie z dowodem doręczenia':
        'Remettre un fichier avec preuve de remise',
    'Przekazanie z dowodem doręczenia robi Sigelith Desktop (od wersji 3.0.1): odbiorca potwierdza odbiór własnym kluczem, a chwila doręczenia trafia do publicznego dziennika. Na tym komputerze go nie ma albo jest w starszej wersji. Otworzyć stronę programu?':
        'La remise avec preuve de remise passe par Sigelith Desktop (version 3.0.1 ou ultérieure)\xa0: le destinataire confirme la réception avec sa propre clé, et le moment de la remise est inscrit au journal public. Il n’est pas installé sur cet ordinateur, ou sa version est trop ancienne. Ouvrir la page du programme\xa0?',
    'Zapisz plik do przekazania':
        'Enregistrer le fichier à remettre',
    'Otwieram Sigelith Handover z plikiem „{name}” — wybierz odbiorcę.':
        'Ouverture de Sigelith Handover avec «\xa0{name}\xa0» — choisissez le destinataire.',
    'Kapsuły czasu…':
        'Capsules temporelles…',
    'Pliki zapieczętowane w tej kopii do daty — klucze wydają dopiero po niej sieć drand i serwer kluczy Sigelith':
        'Fichiers scellés dans cette sauvegarde jusqu’à une date — le réseau drand et le serveur de clés Sigelith ne libèrent les clés qu’après celle-ci',
    'Wskaż najpierw folder kopii — kapsuła leży w kopii.':
        'Indiquez d’abord le dossier de la sauvegarde — la capsule se trouve dans la sauvegarde.',
    'Kapsuły czasu':
        'Capsules temporelles',
    'Kapsuła pieczętuje wybrany folder do chwili, którą wskażesz. Otwierają ją dowolne dwie z trzech części: runda sieci drand z tej chwili, udział serwera kluczy Sigelith (wydawany dopiero po tej chwili — to zasada operatora, nie kryptografia) i kod odzyskiwania zapisany obok kapsuły. Kto ma tę kopię, ma więc i kod: do wcześniejszego otwarcia wystarczy mu, że operator złamie swoją zasadę. Po tej chwili otworzy ją każdy, kto ma jej pliki. Kapsuła leży w tej kopii, nie na serwerze; otwiera ją strona sigelith.org/capsule/.':
        'Une capsule scelle le dossier choisi jusqu’au moment que vous indiquez. Deux des trois éléments suivants suffisent à l’ouvrir\xa0: le tour du réseau drand correspondant à ce moment, la part du serveur de clés Sigelith (libérée seulement après ce moment — c’est une règle de l’opérateur, pas une limite cryptographique) et le code de récupération enregistré à côté de la capsule. Qui détient cette sauvegarde détient donc aussi le code\xa0: pour l’ouvrir plus tôt, il lui suffit que l’opérateur enfreigne sa règle. Après ce moment, toute personne qui possède ses fichiers peut l’ouvrir. La capsule se trouve dans cette sauvegarde, pas sur un serveur\xa0; c’est la page sigelith.org/capsule/ qui l’ouvre.',
    'Wybierz kapsułę z listy albo utwórz nową.':
        'Choisissez une capsule dans la liste ou créez-en une nouvelle.',
    'Nowa kapsuła…':
        'Nouvelle capsule…',
    'Pieczętuje wybrany folder do daty':
        'Scelle le dossier choisi jusqu’à une date',
    'Pokaż w folderze':
        'Afficher dans le dossier',
    'Otwiera folder kapsuły w Eksploratorze':
        'Ouvre le dossier de la capsule dans l’Explorateur de fichiers',
    'Otwórz na stronie':
        'Ouvrir sur le site',
    'Strona sigelith.org/capsule/ otwiera kapsułę po jej dacie':
        'La page sigelith.org/capsule/ ouvre la capsule après sa date',
    'można otworzyć':
        'peut être ouverte',
    'zamknięta':
        'scellée',
    'W tej kopii nie ma jeszcze kapsuł czasu.':
        'Cette sauvegarde ne contient encore aucune capsule temporelle.',
    'Ta kapsuła da się otworzyć na stronie sigelith.org/capsule/ — wskaż jej pliki.':
        'Cette capsule peut être ouverte sur la page sigelith.org/capsule/ — indiquez-y ses fichiers.',
    'Kapsuła jest zamknięta do daty z listy. Kod odzyskiwania leży w pliku obok niej.':
        'La capsule est scellée jusqu’à la date indiquée dans la liste. Le code de récupération se trouve dans un fichier à côté d’elle.',
    'Wybierz folder do zapieczętowania':
        'Choisir le dossier à sceller',
    'Pieczętuję „{name}” — kilka sekund na krzywej eliptycznej…':
        'Scellement de «\xa0{name}\xa0» — quelques secondes sur la courbe elliptique…',
    'kapsuła czasu':
        'capsule temporelle',
    'Kapsuła zapieczętowana':
        'Capsule scellée',
    '„{name}” otworzy się najwcześniej {when}.\n\nKod odzyskiwania (skopiowany do schowka, zapisany też obok kapsuły):\n\n{code}\n\nZapisz go w bezpiecznym miejscu. Przed datą otwarcia sam niczego nie otwiera; po niej zastępuje jeden z kluczy, gdyby był niedostępny.':
        '«\xa0{name}\xa0» s’ouvrira au plus tôt le {when}.\n\nCode de récupération (copié dans le presse-papiers et enregistré aussi à côté de la capsule)\xa0:\n\n{code}\n\nConservez-le en lieu sûr. Avant la date d’ouverture, il n’ouvre rien à lui seul\xa0; après, il remplace l’une des clés si celle-ci venait à manquer.',
    'Nie udało się zapieczętować: {error}':
        'Échec du scellement\xa0: {error}',
    'Nowa kapsuła czasu':
        'Nouvelle capsule temporelle',
    'Otworzy się najwcześniej':
        'Ouverture au plus tôt',
    'kapsuła':
        'capsule',
    'Chwila otwarcia musi być w przyszłości.':
        'Le moment d’ouverture doit se situer dans le futur.',
    'Na bieżąco':
        'En continu',
    'Zmiany w folderach źródłowych trafiają do dzisiejszej wersji kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje. Jedna wersja na dzień; ze znacznikami czasu zamyka ją pieczęć następnego dnia.':
        'Les modifications des dossiers source rejoignent la version du jour quelques minutes après leur enregistrement, et au branchement du disque, la sauvegarde se synchronise aussitôt. Une version par jour\xa0; avec les horodatages, un sceau la clôt le lendemain.',
    'Na bieżąco — po każdej zmianie i po podłączeniu dysku':
        'En continu — après chaque modification et au branchement du disque',
    'Dla dysku podłączonego na stałe albo często: zmiany trafiają do kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje.':
        'Pour un disque branché en permanence ou souvent\xa0: les modifications rejoignent la sauvegarde quelques minutes après leur enregistrement, et au branchement du disque, la sauvegarde se synchronise aussitôt.',
    'Kopia będzie na bieżąco: zmiany trafią do dzisiejszej wersji kilka minut po zapisie, a po podłączeniu dysku kopia od razu się zsynchronizuje.':
        'La sauvegarde sera tenue à jour en continu\xa0: les modifications rejoindront la version du jour quelques minutes après leur enregistrement, et au branchement du disque, la sauvegarde se synchronisera aussitôt.',
    'przywracanie':
        'restauration',
}
