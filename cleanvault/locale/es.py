"""Katalog hiszpański: „polski tekst źródłowy” → „tekst (hiszpański)”.

Klucze są te same co w ``en.py`` i muszą dokładnie odpowiadać napisom w kodzie;
pilnuje tego ``tests/test_i18n.py``. Pola w nawiasach klamrowych (``{count}``)
zostają bez zmian. Formaty dat są te same co w Sigelith Desktop.
"""

from __future__ import annotations

TEXTS: dict[str, str] = {
    '\n\nLokalizacja:\n{path}':
        '\n\nUbicación:\n{path}',
    '\nDo uzupełnienia: niedokończone kopie: {count} — możesz je uzupełnić, wybierając wersję poniżej.':
        '\nPor completar — copias sin terminar: {count}. Puedes completarlas eligiendo una versión abajo.',
    '\nUwaga: duży klaster ({size}): każdy mały plik zajmuje co najmniej tyle miejsca. Przy wielu małych plikach kopia zajmie wielokrotnie więcej niż dane.':
        '\nAtención: clúster grande ({size}): cada archivo pequeño ocupa como mínimo ese espacio. Con muchos archivos pequeños, la copia ocupará varias veces más que los datos.',
    '\nUwaga: niedokończone wersje (nie zawierają wszystkich plików): {names}':
        '\nAtención: versiones sin terminar (no contienen todos los archivos): {names}',
    '\nUwaga: {filesystem} nie obsługuje twardych dowiązań — każda wersja z datą zajmuje tyle miejsca co pełna kopia.':
        '\nAtención: {filesystem} no admite vínculos físicos, así que cada versión fechada ocupa tanto como una copia completa.',
    ' wersji':
        ' versiones',
    ' z szyfrowaniem AES-256-GCM…':
        ' con cifrado AES-256-GCM…',
    ' ×':
        ' ×',
    ' — a ponieważ {filesystem} nie obsługuje twardych dowiązań, zapisze ponownie wszystkie pliki i zajmie tyle miejsca co cała kopia':
        ' — y como {filesystem} no admite vínculos físicos, volverá a escribir todos los archivos y ocupará tanto espacio como la copia entera',
    ' • pozostało {time}':
        ' • quedan {time}',
    '%d.%m %H:%M':
        '%d/%m %H:%M',
    '%d.%m.%Y':
        '%d/%m/%Y',
    '%d.%m.%Y %H:%M':
        '%d/%m/%Y, %H:%M',
    ', klaster {size}':
        ', clúster {size}',
    ', uzupełniona {when}':
        ', actualizada el {when}',
    'Analizuje pliki i pokazuje plan. Nic nie zapisuje.':
        'Analiza los archivos y muestra el plan. No escribe nada.',
    'Anulowano przed rozpoczęciem kopii.':
        'Cancelado antes de empezar la copia.',
    'Anuluj':
        'Cancelar',
    'Argon2id (t={passes}, {memory} MiB, p={threads})':
        'Argon2id (t={passes}, {memory} MiB, p={threads})',
    'Argon2id — {passes} przebiegi, {memory} MiB, {threads} wątki':
        'Argon2id — {passes} pasadas, {memory} MiB, {threads} hilos',
    'Automatycznie (język systemu)':
        'Automático (idioma del sistema)',
    'Bardzo dobre':
        'Muy fuerte',
    'Bardzo słabe':
        'Muy débil',
    'Brak manifestu — skanuję katalog kopii.':
        'No hay manifiesto: analizando la carpeta de la copia.',
    'Brakuje tagu uwierzytelniającego — plik jest obcięty.':
        'Falta la etiqueta de autenticación: el archivo está truncado.',
    'Błąd uruchamiania':
        'Error al iniciar',
    'Ciemny':
        'Oscuro',
    'Co dokładnie zostanie zapisane przy najbliższym przebiegu.':
        'Qué se escribirá exactamente en la próxima ejecución.',
    'Co kopiujemy':
        'Qué se copia',
    'Co zrobić, gdy plik o tej nazwie już istnieje w katalogu docelowym.':
        'Qué hacer cuando ya existe un archivo con ese nombre en la carpeta de destino.',
    'Czas w nazwie to BeatTime — 1000 beatów na dobę, kotwica w UTC, ten sam moment na całym świecie. Data jest datą UTC, więc zgadza się z zegarem.':
        'La hora del nombre es BeatTime: 1000 beats al día con anclaje en UTC, el mismo momento en todo el mundo. La fecha es la fecha UTC, así que coincide con el reloj.',
    'Czym jest {app}':
        'Qué es {app}',
    'Czyści tylko okno — plik dziennika pozostaje':
        'Solo vacía la ventana; el archivo de registro se conserva',
    'Dane aplikacji: {path}':
        'Datos de la aplicación: {path}',
    'Decyduje, czy zachowujemy historię wersji.':
        'Decide si se conserva el historial de versiones.',
    'Dobre':
        'Fuerte',
    'Dodaj folder':
        'Añadir carpeta',
    'Dodaj przynajmniej jeden folder źródłowy.':
        'Añade al menos una carpeta de origen.',
    'Dogrywka zmian z czasu kopii:':
        'Pasada complementaria (cambios durante la copia):',
    'Dokąd przywracamy':
        'Adónde se restaura',
    'Dokładnie to, co program realnie stosuje.':
        'Exactamente lo que el programa usa en realidad.',
    'Domyślne wykluczenia':
        'Exclusiones predeterminadas',
    'Domyślne wykluczenia zapisane.':
        'Exclusiones predeterminadas guardadas.',
    'Domyślnie wyłączone. Przy włączonej opcji skasowanie pliku w źródle\nusuwa też jego jedyną kopię zapasową — operacja nieodwracalna.':
        'Desactivado de forma predeterminada. Con esta opción activada, borrar un archivo en el origen\nelimina también su única copia de seguridad, y eso no se puede deshacer.',
    'Dopisuj do nazwy katalogu datę ostatniego uzupełnienia':
        'Añadir al nombre de la carpeta la fecha de la última actualización',
    'Dziennik':
        'Registro',
    'Dziennik: {path}':
        'Registro: {path}',
    'Ekran przywracania wypełniony danymi szablonu.':
        'La pantalla de restauración se ha rellenado con los datos de la plantilla.',
    'Folder docelowy kopii — najlepiej na innym dysku fizycznym.':
        'Carpeta de destino de la copia, a ser posible en otro disco físico.',
    'Folder zawierający kopię utworzoną przez {app}.':
        'Carpeta que contiene una copia creada por {app}.',
    'Gdy plik już istnieje:':
        'Si el archivo ya existe:',
    'Gdzie zapisujemy':
        'Dónde se guarda',
    'Gotowe do pracy.':
        'Listo.',
    'Gotowe. Wybierz foldery do kopii.':
        'Listo. Elige las carpetas que quieres copiar.',
    'Gotowe: {count} {files}, {size}, {seconds} s.':
        'Hecho: {count} {files}, {size}, {seconds} s.',
    'Główny folder kopii. Zawiera spis treści (.cleanvault-manifest).':
        'Carpeta principal de la copia. Contiene el índice (.cleanvault-manifest).',
    'Hasła nie da się odzyskać ani zresetować. Jeśli je zgubisz, dane z kopii zaszyfrowanej są bezpowrotnie stracone — tak działa poprawne szyfrowanie.':
        'La contraseña no se puede recuperar ni restablecer. Si la pierdes, los datos de una copia cifrada se pierden para siempre: así funciona un cifrado correcto.',
    'Hasła w obu polach różnią się.':
        'Las contraseñas de los dos campos no coinciden.',
    'Hasło':
        'Contraseña',
    'Hasło do kopii':
        'Contraseña de la copia',
    'Hasło nie jest nigdzie zapisywane w postaci jawnej.\nBez niego nie da się odzyskać danych — nie istnieje żadna furtka serwisowa.':
        'La contraseña nunca se guarda en texto claro.\nSin ella no se pueden recuperar los datos: no existe ninguna puerta trasera.',
    'Hasło nie może być puste.':
        'La contraseña no puede estar vacía.',
    'Hasło niezapisane':
        'Contraseña no guardada',
    'Hasło powinno mieć co najmniej 8 znaków.':
        'La contraseña debe tener al menos 8 caracteres.',
    'Hasło trafia do magazynu systemowego powiązanego z Twoim kontem.\nNigdy nie jest zapisywane w plikach programu.':
        'La contraseña va al almacén del sistema vinculado a tu cuenta.\nNunca se escribe en los archivos del programa.',
    'Hasło użyte przy tworzeniu kopii':
        'Contraseña usada al crear la copia',
    'Ile plików kopia przetwarza jednocześnie. Przy setkach tysięcy małych plików\nczas kopii to głównie opóźnienia na każdy plik (otwarcie, skanowanie\nantywirusowe, zapis na nośnik), a nie przesył danych — praca równoległa\nskraca go kilkukrotnie.\n\n„automatycznie” dobiera liczbę do procesora (do 32). Na wolnym dysku\ntalerzowym mniejsza wartość (2–4) bywa szybsza.':
        'Cuántos archivos procesa la copia a la vez. Con cientos de miles de archivos pequeños,\nel tiempo de copia se va sobre todo en esperas por cada archivo (apertura, análisis\nantivirus, escritura en la unidad), no en la transferencia de datos: trabajar en paralelo\nlo reduce varias veces.\n\n«automático» ajusta el número al procesador (hasta 32). En un disco duro\nmecánico lento, un valor menor (2–4) suele ser más rápido.',
    'Informacje przydatne przy zgłaszaniu problemu.':
        'Información útil para informar de un problema.',
    'Jak to działa':
        'Cómo funciona',
    'Jasny':
        'Claro',
    'Jeden folder utrzymywany w zgodzie ze źródłem. Brak historii wersji,\nza to najprostsza struktura i najmniejsze zużycie miejsca.':
        'Una sola carpeta que se mantiene igual que el origen. Sin historial de versiones,\npero con la estructura más simple y el menor uso de espacio.',
    'Jeśli operacja zakończy się błędem, skopiuj stąd ostatnie wiersze — zawierają dokładną przyczynę, a nie tylko komunikat ogólny.':
        'Si una operación termina con un error, copia de aquí las últimas líneas: contienen la causa exacta, no solo un mensaje general.',
    'Język interfejsu zmieniony.':
        'Idioma de la interfaz cambiado.',
    'Język zmienisz po zakończeniu bieżącej operacji.':
        'Podrás cambiar el idioma cuando termine la operación en curso.',
    'Język:':
        'Idioma:',
    'Katalog docelowy leży wewnątrz źródła ({path}). Kopia kopiowałaby samą siebie w nieskończoność.':
        'La carpeta de destino está dentro del origen ({path}). La copia se copiaría a sí misma sin fin.',
    'Katalog docelowy nie może być tym samym katalogiem co źródłowy.':
        'La carpeta de destino no puede ser la misma que la de origen.',
    'Katalog jeszcze nie istnieje — zostanie utworzony.':
        'La carpeta aún no existe: se creará.',
    'Katalog kopii nie istnieje: {path}':
        'La carpeta de la copia no existe: {path}',
    'Katalog źródłowy nie istnieje: {path}':
        'La carpeta de origen no existe: {path}',
    'Katalog, w którym pojawią się odtworzone pliki.':
        'Carpeta donde aparecerán los archivos restaurados.',
    'Katalog, w którym powstanie kopia. Nie może leżeć wewnątrz folderu źródłowego.':
        'Carpeta donde se creará la copia. No puede estar dentro de una carpeta de origen.',
    'Katalogi objęte kopią.\nMożesz przeciągnąć foldery z Eksploratora Windows wprost na tę listę.':
        'Carpetas incluidas en la copia.\nPuedes arrastrar carpetas desde el Explorador de archivos directamente a esta lista.',
    'Każdy folder z datą jest kompletny — przywracanie nie wymaga sklejania wersji.':
        'Cada carpeta fechada está completa: para restaurar no hace falta combinar versiones.',
    'Każdy plik jest czytany ponownie zaraz po zapisaniu. Dane pochodzą wtedy\nzwykle z pamięci podręcznej systemu, więc niewiele mówi to o nośniku,\na wydłuża kopię nawet dwukrotnie.\n\nSkuteczniejsza jest weryfikacja odroczona: ekran „Przywracanie” →\n„Sprawdź kopię”, najlepiej po ponownym podłączeniu dysku.':
        'Cada archivo se vuelve a leer justo después de escribirlo. Los datos suelen venir\nentonces de la caché del sistema, así que dice poco sobre la unidad,\ny la copia puede tardar hasta el doble.\n\nEs más eficaz la verificación diferida: pantalla «Restauración» →\n«Comprobar copia», mejor tras volver a conectar el disco.',
    'Każdy plik trafia do kopii jako zaszyfrowany kontener .cvlt.\nKlucz powstaje z hasła przez Argon2id.':
        'Cada archivo entra en la copia como un contenedor cifrado .cvlt.\nLa clave se deriva de la contraseña con Argon2id.',
    'Każdy przebieg tworzy osobny folder z datą i godziną.\nPliki niezmienione są podpinane twardym dowiązaniem, więc historia\nzajmuje tyle miejsca, ile realnie się zmieniło.':
        'Cada ejecución crea su propia carpeta con fecha y hora.\nLos archivos sin cambios se enlazan con vínculos físicos, así que el historial\nocupa solo lo que realmente ha cambiado.',
    'Klaster nośnika to {cluster} — pliki zajmą {actual} zamiast {logical} (narzut {overhead}).':
        'El clúster de la unidad es de {cluster}: los archivos ocuparán {actual} en lugar de {logical} (exceso: {overhead}).',
    'Kliknij szablon, aby zobaczyć jego szczegóły.':
        'Haz clic en una plantilla para ver sus detalles.',
    'Kliknij „Podgląd zmian”, aby sprawdzić plan bez zapisywania czegokolwiek.':
        'Haz clic en «Vista previa de cambios» para comprobar el plan sin escribir nada.',
    'Kolor wyróżnienia':
        'Color de énfasis',
    'Kolor wyróżnienia…':
        'Color de énfasis…',
    'Kopia':
        'Copia',
    'Kopia do dokończenia':
        'Copia por terminar',
    'Kopia jest aktualna — nie ma czego zapisywać.':
        'La copia está al día: no hay nada que escribir.',
    'Kopia jest zaszyfrowana — podaj hasło użyte przy jej tworzeniu.':
        'La copia está cifrada: introduce la contraseña con la que se creó.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją przywrócić.':
        'La copia está cifrada: introduce la contraseña para restaurarla.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją zweryfikować.':
        'La copia está cifrada: introduce la contraseña para verificarla.',
    'Kopia jest zaszyfrowana — podaj hasło.':
        'La copia está cifrada: introduce la contraseña.',
    'Kopia lustrzana':
        'Copia espejo',
    'Kopia nie została uruchomiona.':
        'La copia no se ha iniciado.',
    'Kopia wykonana. Uruchom podgląd ponownie, aby sprawdzić stan.':
        'Copia realizada. Vuelve a ejecutar la vista previa para comprobar el estado.',
    'Kopia zapasowa':
        'Copia de seguridad',
    'Kopia {folder}':
        'Copia de {folder}',
    'Kopia {kind} • {count} {files} • {size} • ostatnia aktualizacja {when}\nŹródła: {roots}':
        'Copia {kind} • {count} {files} • {size} • última actualización: {when}\nOrígenes: {roots}',
    'Kopiowane są wyłącznie pliki nowe i zmienione od ostatniego przebiegu.':
        'Solo se copian los archivos nuevos y los modificados desde la última ejecución.',
    'Kopiuje ustawienia szablonu na ekran „Kopia zapasowa”':
        'Copia los ajustes de la plantilla en la pantalla «Copia de seguridad»',
    'Kopię możesz sprawdzić później: ekran „Przywracanie” → „Sprawdź kopię”. Najlepiej po ponownym podłączeniu dysku — wtedy dane są czytane z nośnika.':
        'Puedes comprobar la copia más tarde: pantalla «Restauración» → «Comprobar copia». Mejor tras volver a conectar el disco: así los datos se leen de verdad de la unidad.',
    'Kryptografia':
        'Criptografía',
    'Lista podpowiadana przy tworzeniu nowej kopii.':
        'La lista que se propone al configurar una copia nueva.',
    'Magazyn haseł: {backend}':
        'Almacén de contraseñas: {backend}',
    'Magazyn systemowy: {backend}':
        'Almacén del sistema: {backend}',
    'Menedżer poświadczeń Windows (DPAPI, powiązany z kontem użytkownika).':
        'Administrador de credenciales de Windows (DPAPI, vinculado a tu cuenta de usuario).',
    'Miejsce i układ odtwarzanych plików.':
        'Ubicación y disposición de los archivos restaurados.',
    'Motyw zmieniony na {theme}.':
        'Tema cambiado a {theme}.',
    'Motyw:':
        'Tema:',
    'Możesz też przeciągnąć foldery z Eksploratora Windows wprost na listę.':
        'También puedes arrastrar carpetas desde el Explorador de archivos directamente a la lista.',
    'Można ją dokończyć — zostaną dograne tylko brakujące i zmienione pliki.':
        'Se puede terminar: solo se añadirán los archivos que faltan y los modificados.',
    'Na nośniku docelowym zajmie to ok. {size}.':
        'En la unidad de destino ocupará unos {size}.',
    'Nadpisywanie plików':
        'Sobrescritura de archivos',
    'Nadpisz istniejące pliki':
        'Sobrescribir los archivos existentes',
    'Nazwa szablonu':
        'Nombre de la plantilla',
    'Nazwa szablonu nie może być pusta.':
        'El nombre de la plantilla no puede estar vacío.',
    'Nazwa szablonu zapisana.':
        'Nombre de la plantilla guardado.',
    'Nazwa szablonu:':
        'Nombre de la plantilla:',
    'Nie ma wersji kopii o nazwie {name} w katalogu {path}.':
        'No hay ninguna versión de la copia llamada {name} en la carpeta {path}.',
    'Nie można odczytać informacji o dysku: {error}':
        'No se ha podido leer la información de la unidad: {error}',
    'Nie udało się uruchomić programu — brakuje biblioteki: {error}\nZainstaluj zależności poleceniem:  pip install -r requirements.txt':
        'No se ha podido iniciar el programa — falta una biblioteca: {error}\nInstala las dependencias con el comando:  pip install -r requirements.txt',
    'Nie udało się wykonać operacji':
        'No se ha podido completar la operación',
    'Nie udało się zapisać hasła w magazynie systemowym.\nSzablon działa normalnie — program poprosi o hasło przy uruchomieniu.':
        'No se ha podido guardar la contraseña en el almacén del sistema.\nLa plantilla funciona con normalidad: el programa pedirá la contraseña al ejecutarla.',
    'Nie udało się znaleźć wolnej nazwy dla {path}':
        'No se ha encontrado ningún nombre libre para {path}',
    'Nie wskazano katalogu docelowego.':
        'No se ha indicado ninguna carpeta de destino.',
    'Nie wskazano żadnego katalogu źródłowego.':
        'No se ha indicado ninguna carpeta de origen.',
    'Nie wybrano katalogu':
        'No se ha elegido ninguna carpeta',
    'Nie wybrano szablonu':
        'Ninguna plantilla seleccionada',
    'Nie znaleziono spisu treści kopii — program przeskanuje folder i rozpozna pliki po ich zawartości.':
        'No se ha encontrado el índice de la copia: el programa analizará la carpeta y reconocerá los archivos por su contenido.',
    'Nie znam oryginalnej lokalizacji dla {key} — wybierz inny układ przywracania.':
        'Se desconoce la ubicación original de {key}: elige otra disposición de restauración.',
    'Niedostępny — backend {backend} nie gwarantuje poufności.':
        'No disponible: el backend {backend} no garantiza la confidencialidad.',
    'Niedostępny — brak biblioteki keyring.':
        'No disponible: falta la biblioteca keyring.',
    'Nieznany algorytm wyprowadzania klucza: {name}':
        'Algoritmo de derivación de clave desconocido: {name}',
    'Nowa wersja z datą':
        'Nueva versión fechada',
    'Nowa wersja z datą to kopia od początku do osobnego folderu':
        'Una nueva versión fechada es una copia desde cero en una carpeta aparte',
    'Nowa wersja z datą — kopia do nowego folderu.\nWybrana istniejąca wersja — dogrywa do niej tylko brakujące i zmienione\npliki, a pliki różniące się od źródła nadpisuje. Tak dokończysz przerwaną\nkopię albo uzupełnisz ją o dane, które powstały w trakcie jej wykonywania.':
        'Nueva versión fechada: copia en una carpeta nueva.\nUna versión existente elegida: se le añaden solo los archivos que faltan y los modificados,\ny se sobrescriben los que difieren del origen. Así terminas una copia\ninterrumpida o la completas con los datos creados mientras se hacía.',
    'Nowy szablon':
        'Plantilla nueva',
    'Nośnik docelowy ({filesystem}) nie obsługuje twardych dowiązań, więc każda wersja z datą jest pełną kopią. Te {count} niezmienionych plików zostanie powielone ({size}). Rozważ układ „kopia lustrzana” albo nośnik NTFS.':
        'La unidad de destino ({filesystem}) no admite vínculos físicos, así que cada versión fechada es una copia completa. Archivos sin cambios que se duplicarán: {count} ({size}). Considera la disposición «copia espejo» o una unidad NTFS.',
    'O programie':
        'Acerca de',
    'Obsługiwane są wzorce w stylu Windows:\n  *.tmp          — wszystkie pliki tymczasowe\n  Thumbs.db      — konkretna nazwa\n  node_modules/* — cały folder wraz z zawartością':
        'Se admiten patrones al estilo de Windows:\n  *.tmp          — todos los archivos temporales\n  Thumbs.db      — un nombre concreto\n  node_modules/* — una carpeta entera con su contenido',
    'Ochrona danych':
        'Protección de datos',
    'Odczytuje wszystkie pliki kopii i weryfikuje ich poprawność.\nNic nie zapisuje na dysku.':
        'Lee todos los archivos de la copia y verifica que estén intactos.\nNo escribe nada en el disco.',
    'Odpowiednik synchronizacji folderu. Wcześniejsze wersje plików nie są zachowywane.':
        'Equivale a sincronizar una carpeta. No se conservan las versiones anteriores de los archivos.',
    'Odtwarza pliki z kopii — również z kopii zaszyfrowanej.':
        'Restaura archivos de una copia, también de una copia cifrada.',
    'Odtwarza pliki zgodnie z ustawieniami powyżej':
        'Restaura los archivos según los ajustes de arriba',
    'Odtwórz pełną strukturę folderów':
        'Recrear toda la estructura de carpetas',
    'Odtwórz pliki z istniejącej kopii':
        'Restaurar archivos de una copia existente',
    'Operacja nie powiodła się.':
        'La operación ha fallado.',
    'Operacja przerwana przez użytkownika.':
        'Operación cancelada por el usuario.',
    'Operacja przerwana — utrwalam stan dotychczas zapisanych plików.':
        'Operación cancelada: guardando el estado de los archivos escritos hasta ahora.',
    'Operacja w toku':
        'Operación en curso',
    'Operacja zakończona błędem.':
        'La operación ha terminado con un error.',
    'Ostatnie operacje':
        'Operaciones recientes',
    'Otwiera ekran przywracania z wypełnionymi ścieżkami':
        'Abre la pantalla de restauración con las rutas ya rellenadas',
    'Otwiera pełny dziennik w domyślnym edytorze':
        'Abre el registro completo en el editor predeterminado',
    'Otwórz katalog danych':
        'Abrir la carpeta de datos',
    'Otwórz katalog dziennika':
        'Abrir la carpeta del registro',
    'Otwórz okno wyboru katalogu':
        'Abrir el selector de carpetas',
    'Otwórz plik dziennika':
        'Abrir el archivo de registro',
    'PBKDF2-HMAC-SHA256 ({count} iteracji)':
        'PBKDF2-HMAC-SHA256 ({count} iteraciones)',
    'PBKDF2-HMAC-SHA256 — {count} iteracji':
        'PBKDF2-HMAC-SHA256 — {count} iteraciones',
    'PBKDF2-HMAC-SHA256, {count} iteracji':
        'PBKDF2-HMAC-SHA256, {count} iteraciones',
    'Pełna struktura — układ jak w źródle, wewnątrz wskazanego katalogu.\nJeden folder — wygodne, gdy szukasz kilku plików.\nPierwotne lokalizacje — zapisuje pliki tam, skąd zostały pobrane.':
        'Estructura completa: la misma disposición que en el origen, dentro de la carpeta elegida.\nUna carpeta: práctico cuando buscas unos pocos archivos.\nUbicaciones originales: escribe los archivos en el lugar del que salieron.',
    'Pierwszy przebieg kopiuje wszystko i trwa najdłużej. Kolejne porównują rozmiar i datę modyfikacji, więc zwykle kończą się w kilka sekund.':
        'La primera ejecución lo copia todo y es la que más tarda. Las siguientes comparan el tamaño y la fecha de modificación, así que suelen terminar en unos segundos.',
    'Plan gotowy: {count} {files} do zapisania.':
        'Plan listo: {count} {files} por escribir.',
    'Plik jest za krótki, by być kontenerem tego programu.':
        'El archivo es demasiado corto para ser un contenedor de este programa.',
    'Plik skończył się wcześniej, niż deklaruje nagłówek.':
        'El archivo termina antes de lo que indica su encabezado.',
    'Plik w formacie w wersji {found}; ta wersja programu obsługuje {supported}.':
        'El archivo usa la versión {found} del formato; esta versión del programa admite {supported}.',
    'Plik wymaga Argon2id, a biblioteka argon2-cffi jest niedostępna.':
        'El archivo requiere Argon2id, pero la biblioteca argon2-cffi no está disponible.',
    'Pliki pominięte — kopia jest aktualna':
        'Archivos omitidos: la copia está al día',
    'Pliki trafią do wskazanego katalogu z zachowaniem struktury folderów.':
        'Los archivos irán a la carpeta elegida conservando la estructura de carpetas.',
    'Pliki wrócą dokładnie tam, skąd pochodzą. Katalog docelowy zostanie zignorowany.':
        'Los archivos volverán exactamente a su lugar de origen. Se ignorará la carpeta de destino.',
    'Pliki zmienione od ostatniego przebiegu':
        'Archivos modificados desde la última ejecución',
    'Pliki zostaną zapisane dokładnie tam, skąd pochodzą.\n\nKonflikty nazw: {collision}.\n\nCzy kontynuować?':
        'Los archivos se escribirán exactamente en su lugar de origen.\n\nConflictos de nombres: {collision}.\n\n¿Continuar?',
    'Pliki, których jeszcze nie ma w kopii':
        'Archivos que aún no están en la copia',
    'Po uzupełnieniu istniejącej wersji jej katalog nazywa się np.\n  2026-09-17_@687--2026-09-24_@921\nczyli: data utworzenia kopii i data ostatniego uzupełnienia.\n\nData utworzenia zostaje z przodu, więc katalogi nadal układają się\nchronologicznie. Widać to w Eksploratorze bez uruchamiania programu.':
        'Al completar una versión existente, su carpeta pasa a llamarse, por ejemplo:\n  2026-09-17_@687--2026-09-24_@921\nes decir: la fecha de creación de la copia y la fecha de la última actualización.\n\nLa fecha de creación queda delante, así que las carpetas se siguen ordenando\ncronológicamente. Se ve en el Explorador de archivos sin abrir el programa.',
    'Po wykonaniu kopii zostanie mało wolnego miejsca ({free}).':
        'Tras la copia quedará poco espacio libre ({free}).',
    'Po zakończeniu kopii program ponownie skanuje źródło i dogrywa do tej samej\nwersji pliki, które w międzyczasie powstały lub się zmieniły.\nPrzydatne, gdy pracujesz na danych w trakcie wielogodzinnej kopii.\nPlik zmieniony w trakcie własnego kopiowania nigdy nie jest uznawany za zapisany.':
        'Al terminar la copia, el programa vuelve a analizar el origen y añade a la misma\nversión los archivos que se crearon o cambiaron mientras tanto.\nÚtil si trabajas con los datos durante una copia que dura horas.\nUn archivo que cambia mientras se copia nunca se da por escrito.',
    'Poczekaj na zakończenie bieżącej operacji.':
        'Espera a que termine la operación en curso.',
    'Podaj hasło dla szablonu „{name}”:':
        'Introduce la contraseña de la plantilla «{name}»:',
    'Podaj hasło — bez niego nie można zaszyfrować kopii.':
        'Introduce una contraseña: sin ella no se puede cifrar la copia.',
    'Podane hasło nie pasuje do plików zapisanych wcześniej w tej kopii. Wznowienie z innym hasłem zostawiłoby w jednej kopii pliki pod dwoma hasłami. Podaj hasło użyte przy poprzednim przebiegu albo utwórz kopię w nowym katalogu.':
        'La contraseña introducida no coincide con la de los archivos ya escritos en esta copia. Reanudarla con otra contraseña dejaría en una misma copia archivos con dos contraseñas distintas. Introduce la contraseña de la ejecución anterior o crea la copia en una carpeta nueva.',
    'Podgląd zmian':
        'Vista previa de cambios',
    'Pokazuje folder z plikami dziennika':
        'Muestra la carpeta con los archivos de registro',
    'Pokazuje folder z ustawieniami i szablonami':
        'Muestra la carpeta con los ajustes y las plantillas',
    'Pokaż / ukryj wpisane hasło':
        'Mostrar u ocultar la contraseña escrita',
    'Pomiń istniejące pliki':
        'Omitir los archivos existentes',
    'Potwierdź usuwanie':
        'Confirmar la eliminación',
    'Powtórz hasło':
        'Repite la contraseña',
    'Program nie mógł się uruchomić:\n\n{error}\n\nSzczegóły zapisano w dzienniku aplikacji.':
        'El programa no ha podido iniciarse:\n\n{error}\n\nLos detalles se han escrito en el registro de la aplicación.',
    'Program nie wie, czy ta kopia została dokończona. Uzupełnienie jej dogra tylko brakujące i zmienione pliki, a tego, co już jest zapisane, nie kopiuje ponownie.':
        'El programa no sabe si esta copia se terminó. Completarla añade solo los archivos que faltan y los modificados, y no vuelve a copiar lo que ya está escrito.',
    'Program sam wykryje, czy kopia jest zaszyfrowana.':
        'El programa detecta por sí solo si la copia está cifrada.',
    'Przebieg operacji i diagnostyka':
        'Progreso de las operaciones y diagnóstico',
    'Przebieg operacji na żywo. Pełna historia trafia do pliku.':
        'Progreso de las operaciones en directo. El historial completo se guarda en un archivo.',
    'Przebieg uzupełniający: {error}':
        'Pasada complementaria: {error}',
    'Przeciętne':
        'Aceptable',
    'Przerwano liczenie sumy kontrolnej.':
        'Se ha cancelado el cálculo de la suma de comprobación.',
    'Przerwano skanowanie.':
        'Se ha cancelado el análisis.',
    'Przerwano. Zapisano {count} {files} ({size}).':
        'Interrumpido. Escritos: {count} {files} ({size}).',
    'Przerwij':
        'Detener',
    'Przerywanie operacji…':
        'Deteniendo la operación…',
    'Przerywanie — zapisuję spis treści kopii, nie wyłączaj komputera…':
        'Deteniendo: escribiendo el índice de la copia, no apagues el equipo…',
    'Przeskanowano {count} {files}.':
        'Analizados: {count} {files}.',
    'Przygotowanie…':
        'Preparando…',
    'Przywracanie':
        'Restauración',
    'Przywracanie do pierwotnych lokalizacji':
        'Restauración en las ubicaciones originales',
    'Przywracanie przerwane.':
        'Restauración cancelada.',
    'Przywracanie {count} {files} ({size})…':
        'Restaurando {count} {files} ({size})…',
    'Przywróć do pierwotnych lokalizacji':
        'Restaurar en las ubicaciones originales',
    'Przywróć domyślne':
        'Restablecer valores predeterminados',
    'Przywróć fabryczne':
        'Restablecer la lista de fábrica',
    'Przywróć pliki':
        'Restaurar archivos',
    'Przywróć z tej kopii':
        'Restaurar desde esta copia',
    'Pusta nazwa':
        'Nombre vacío',
    'Równoległe operacje:':
        'Operaciones en paralelo:',
    'Skanowanie plików źródłowych…':
        'Analizando los archivos de origen…',
    'Skrót z dziennika — pełny zapis znajdziesz w zakładce „Dziennik”.':
        'Resumen del registro; el detalle completo está en la pestaña «Registro».',
    'Skąd przywracamy':
        'Desde dónde se restaura',
    'Sprawdzam, co zmieniło się w źródle w trakcie kopii (przebieg uzupełniający {attempt} z {passes})…':
        'Comprobando qué cambió en el origen durante la copia (pasada complementaria {attempt} de {passes})…',
    'Sprawdzam, czy hasło zgadza się z hasłem wcześniej zapisanych plików…':
        'Comprobando que la contraseña coincide con la de los archivos escritos antes…',
    'Sprawdzam, czy w katalogu docelowym jest kopia do dokończenia…':
        'Comprobando si en la carpeta de destino hay una copia por terminar…',
    'Sprawdź hasło':
        'Comprueba la contraseña',
    'Sprawdź kopię':
        'Comprobar copia',
    'Szablon przechowuje foldery, opcje i wykluczenia. Hasło nigdy nie trafia do szablonu — jest przechowywane w Menedżerze poświadczeń Windows albo wpisywane przy każdym uruchomieniu.':
        'Una plantilla guarda las carpetas, las opciones y las exclusiones. La contraseña nunca va a la plantilla: se guarda en el Administrador de credenciales de Windows o se escribe en cada ejecución.',
    'Szablon usunięty.':
        'Plantilla eliminada.',
    'Szablon „{name}”':
        'Plantilla «{name}»',
    'Szablon „{name}” już istnieje.\n\nZastąpić go bieżącymi ustawieniami z formularza?':
        'La plantilla «{name}» ya existe.\n\n¿Sustituirla por los ajustes actuales del formulario?',
    'Szablon „{name}” zostanie usunięty.\n\nPliki kopii zapasowej pozostaną nienaruszone.':
        'Se eliminará la plantilla «{name}».\n\nLos archivos de la copia de seguridad no se tocarán.',
    'Szablony':
        'Plantillas',
    'Szablony: {count}\nSzyfrowanie: AES-256-GCM\nKlucz: {kdf}':
        'Plantillas: {count}\nCifrado: AES-256-GCM\nClave: {kdf}',
    'Szyfrowanie i kontrola poprawności zapisu.':
        'Cifrado y verificación de la escritura.',
    'Szyfrowanie: AES-256-GCM (uwierzytelnione)\nWyprowadzanie klucza: {kdf}':
        'Cifrado: AES-256-GCM (autenticado)\nDerivación de clave: {kdf}',
    'Szyfruj kopię (AES-256-GCM)':
        'Cifrar la copia (AES-256-GCM)',
    'Słabe':
        'Débil',
    'Ta kopia nie jest zaszyfrowana — hasło nie jest potrzebne.':
        'Esta copia no está cifrada: no hace falta contraseña.',
    'Ten folder jest już na liście.':
        'Esa carpeta ya está en la lista.',
    'To nie jest plik zaszyfrowany przez ten program.':
        'Este archivo no se ha cifrado con este programa.',
    'Trwa inna operacja — poczekaj na jej zakończenie.':
        'Hay otra operación en curso: espera a que termine.',
    'Trwa operacja':
        'Operación en curso',
    'Trwa operacja na plikach. Zamknięcie programu ją przerwie.\n\nPliki zapisane do tej chwili zostaną zachowane, a kopię będzie można później dokończyć.\n\nZamknąć mimo to?':
        'Hay una operación con archivos en curso. Si cierras el programa, se interrumpirá.\n\nLos archivos escritos hasta ahora se conservan, y la copia se podrá terminar más tarde.\n\n¿Cerrar de todos modos?',
    'Trwa: {description}…':
        'En curso: {description}…',
    'Tryb dokładny — licz sumę kontrolną każdego pliku':
        'Modo exhaustivo: calcular la suma de comprobación de cada archivo',
    'Układ kopii':
        'Disposición de la copia',
    'Układ plików:':
        'Disposición de los archivos:',
    'Uruchom kopię':
        'Iniciar copia',
    'Ustawienia':
        'Ajustes',
    'Usunąć szablon?':
        '¿Eliminar la plantilla?',
    'Usuwa pozycję z listy. Nie kasuje żadnych plików.':
        'Quita el elemento de la lista. No borra ningún archivo.',
    'Usuwa szablon. Nie kasuje żadnych plików kopii.':
        'Elimina la plantilla. No borra ningún archivo de la copia.',
    'Usuwaj z kopii pliki skasowane w źródle':
        'Eliminar de la copia los archivos borrados en el origen',
    'Usuń':
        'Eliminar',
    'Usuń zaznaczone':
        'Quitar seleccionadas',
    'Uszkodzony nagłówek pliku.':
        'El encabezado del archivo está dañado.',
    'Utwórz lub zaktualizuj kopię wybranych folderów':
        'Crear o actualizar una copia de las carpetas elegidas',
    'Utwórz nową wersję':
        'Crear una versión nueva',
    'Uzupełnienie istniejącej wersji nie kopiuje ponownie tego, co już w niej jest — dokończysz przerwaną kopię bez tworzenia kolejnej pełnej wersji.':
        'Completar una versión existente no vuelve a copiar lo que ya contiene: así terminas una copia interrumpida sin crear otra versión completa.',
    'Uzupełnij tę wersję':
        'Completar esta versión',
    'Uzupełnij: {version} • {labels}':
        'Completar: {version} • {labels}',
    'W katalogu docelowym jest kopia tych samych folderów zapisana starszą wersją programu:':
        'En la carpeta de destino hay una copia de las mismas carpetas escrita con una versión anterior del programa:',
    'W katalogu docelowym jest niedokończona kopia tych samych folderów:':
        'En la carpeta de destino hay una copia sin terminar de las mismas carpetas:',
    'W tym katalogu nie ma spisu treści kopii — nie ma z czym porównać plików.':
        'Esta carpeta no tiene índice de la copia: no hay con qué comparar los archivos.',
    'Wczytaj do formularza':
        'Cargar en el formulario',
    'Wczytano manifest kopii: {count} {files}.':
        'Manifiesto de la copia cargado: {count} {files}.',
    'Wczytano szablon „{name}” do formularza.':
        'Plantilla «{name}» cargada en el formulario.',
    'Wersja kopii nosi teraz nazwę {name}.':
        'La versión de la copia se llama ahora {name}.',
    'Wersja, licencja i użyta kryptografia':
        'Versión, licencia y criptografía utilizada',
    'Wersje z datą (zalecane)':
        'Versiones fechadas (recomendado)',
    'Weryfikacja kopii':
        'Comprobación de la copia',
    'Weryfikacja nie powiodła się: nieprawidłowe hasło lub uszkodzony plik.':
        'La verificación ha fallado: contraseña incorrecta o archivo dañado.',
    'Weryfikacja po zapisie nie powiodła się — zapisane dane różnią się od źródła.':
        'La verificación tras la escritura ha fallado: los datos escritos difieren del origen.',
    'Weryfikacja {count} {files} ({size}), {threads} równolegle…':
        'Verificando {count} {files} ({size}), {threads} en paralelo…',
    'Weryfikuj natychmiast po zapisie (spowalnia kopię)':
        'Verificar justo después de escribir (ralentiza la copia)',
    'Wolne miejsce: {free} z {total}':
        'Espacio libre: {free} de {total}',
    'Wolniejszy, ale wykrywa zmiany, które nie zmieniły rozmiaru ani daty\n(np. po przywróceniu pliku z innego nośnika).':
        'Más lento, pero detecta cambios que no alteraron ni el tamaño ni la fecha\n(por ejemplo, tras restaurar un archivo desde otra unidad).',
    'Wpis {key} w spisie treści kopii wskazuje poza katalog docelowy — pomijam go.':
        'La entrada {key} del índice de la copia apunta fuera de la carpeta de destino: se omite.',
    'Wraca do listy wbudowanej w program':
        'Vuelve a la lista integrada en el programa',
    'Wskaż folder kopii, aby zobaczyć jej zawartość.':
        'Elige la carpeta de la copia para ver su contenido.',
    'Wskaż folder kopii.':
        'Elige la carpeta de la copia.',
    'Wskaż foldery objęte kopią. Podfoldery są uwzględniane automatycznie.':
        'Elige las carpetas que se copiarán. Las subcarpetas se incluyen automáticamente.',
    'Wskaż główny folder kopii (ten, który wybrałeś jako cel), a nie pojedynczy folder z datą. Program sam odczyta spis treści kopii.':
        'Elige la carpeta principal de la copia (la que elegiste como destino), no una sola carpeta fechada. El programa leerá por sí solo el índice de la copia.',
    'Wskaż katalog docelowy kopii.':
        'Elige la carpeta de destino de la copia.',
    'Wskaż katalog docelowy.':
        'Elige la carpeta de destino.',
    'Wstawia zalecaną listę wykluczeń':
        'Inserta la lista de exclusiones recomendada',
    'Wszystkie pliki wylądują bezpośrednio w katalogu docelowym, bez podfolderów.':
        'Todos los archivos irán directamente a la carpeta de destino, sin subcarpetas.',
    'Wszystko do jednego folderu':
        'Todo en una sola carpeta',
    'Wybierz folder do kopii':
        'Elige una carpeta para copiar',
    'Wybierz folder kopii':
        'Elige la carpeta de la copia',
    'Wybierz katalog':
        'Elige una carpeta',
    'Wybierz katalog docelowy':
        'Elige la carpeta de destino',
    'Wybierz katalog docelowy kopii':
        'Elige la carpeta de destino de la copia',
    'Wybierz katalog, aby zobaczyć dostępne miejsce.':
        'Elige una carpeta para ver el espacio disponible.',
    'Wybierz kolejny folder do kopii':
        'Elige otra carpeta para copiar',
    'Wybierz szablon z listy.':
        'Elige una plantilla de la lista.',
    'Wybierz…':
        'Elegir…',
    'Wybrano nadpisywanie istniejących plików. Ich obecna zawartość zostanie bezpowrotnie zastąpiona.\n\nCzy kontynuować?':
        'Has elegido sobrescribir los archivos existentes. Su contenido actual se sustituirá para siempre.\n\n¿Continuar?',
    'Wyczyść widok':
        'Limpiar la vista',
    'Wygląd':
        'Apariencia',
    'Wygląd, wykluczenia domyślne i informacje o środowisku.':
        'Apariencia, exclusiones predeterminadas e información del entorno.',
    'Wygląd, wykluczenia i magazyn haseł':
        'Apariencia, exclusiones y almacén de contraseñas',
    'Wykluczenia':
        'Exclusiones',
    'Wykonuje kopię według tego szablonu':
        'Ejecuta la copia según esta plantilla',
    'Wykonuje kopię zgodnie z powyższymi ustawieniami':
        'Ejecuta la copia con los ajustes de arriba',
    'Wymagane wyłącznie dla kopii zaszyfrowanych.':
        'Solo se necesita para copias cifradas.',
    'Wzorce plików i folderów pomijanych w kopii — po jednym w wierszu.':
        'Patrones de archivos y carpetas que no se copian, uno por línea.',
    'Włączono szyfrowanie, ale nie podano hasła.':
        'El cifrado está activado, pero no se ha indicado ninguna contraseña.',
    'Włączono usuwanie z kopii plików skasowanych w źródle.\n\nPliki usunięte w źródle stracą swoją jedyną kopię zapasową. Czy na pewno kontynuować?':
        'Está activada la eliminación de la copia de los archivos borrados en el origen.\n\nLos archivos borrados en el origen perderán su única copia de seguridad. ¿Seguro que quieres continuar?',
    'Za mało miejsca w katalogu docelowym. Potrzeba ok. {needed}, dostępne {free}.':
        'No hay espacio suficiente en la carpeta de destino. Se necesitan unos {needed} y hay {free} disponibles.',
    'Zabezpieczenie przed literówką — hasła nie da się odzyskać.':
        'Para evitar erratas: la contraseña no se puede recuperar.',
    'Zachowaj oba — dopisz numer do nazwy':
        'Conservar ambos: añadir un número al nombre',
    'Zakończono z błędami ({errors}). Zapisano {count} {files}.':
        'Finalizado con errores ({errors}). Escritos: {count} {files}.',
    'Zakończono.':
        'Finalizado.',
    'Zapamiętaj hasło w Menedżerze poświadczeń Windows':
        'Recordar la contraseña en el Administrador de credenciales de Windows',
    'Zapamiętuje te ustawienia do ponownego użycia':
        'Guarda estos ajustes para volver a usarlos',
    'Zapis bieżącej sesji':
        'Registro de esta sesión',
    'Zapisane konfiguracje do ponownego użycia':
        'Configuraciones guardadas para reutilizar',
    'Zapisane konfiguracje — uruchamiasz je jednym kliknięciem.':
        'Configuraciones guardadas: se ejecutan con un clic.',
    'Zapisane szablony':
        'Plantillas guardadas',
    'Zapisano szablon „{name}”.':
        'Plantilla «{name}» guardada.',
    'Zapisuje listę jako domyślną':
        'Guarda la lista como predeterminada',
    'Zapisuje nową nazwę szablonu':
        'Guarda el nuevo nombre de la plantilla',
    'Zapisywanie {count} {files} ({size}), {workers} równolegle':
        'Escribiendo {count} {files} ({size}), {workers} en paralelo',
    'Zapisz':
        'Guardar',
    'Zapisz do:':
        'Guardar en:',
    'Zapisz jako szablon':
        'Guardar como plantilla',
    'Zapisz nazwę':
        'Guardar el nombre',
    'Zapisz szablon':
        'Guardar plantilla',
    'Zastąpić szablon?':
        '¿Sustituir la plantilla?',
    'Zatrzymuje operację. Pliki już zapisane pozostają nienaruszone.':
        'Detiene la operación. Los archivos ya escritos no se tocan.',
    'Zaznacz szablon na liście.':
        'Selecciona una plantilla en la lista.',
    'Zmiana języka przebudowuje okno; wypełnione ścieżki zostają.':
        'Cambiar el idioma reconstruye la ventana; las rutas que hayas rellenado se mantienen.',
    'Zmiana motywu działa natychmiast.':
        'El cambio de tema se aplica de inmediato.',
    'Zmienia kolor przycisków i zaznaczeń':
        'Cambia el color de los botones y de la selección',
    'Zmień nazwę, aby łatwiej rozpoznawać szablon.':
        'Cambia el nombre para reconocer la plantilla más fácilmente.',
    'Znaleziono {count} {files}. Porównuję z poprzednią kopią…':
        'Encontrados: {count} {files}. Comparando con la copia anterior…',
    'automatycznie':
        'automático',
    'bez zmian':
        'sin cambios',
    'brak (biblioteka keyring niezainstalowana)':
        'ninguno (la biblioteca keyring no está instalada)',
    'brak danych':
        'sin datos',
    'brak pliku w kopii':
        'el archivo no está en la copia',
    'do zapisania':
        'por escribir',
    'istniejąca kopia: {count} {files}, ostatnio {when}':
        'copia existente: {count} {files}, actualizada el {when}',
    'jeszcze nie uruchamiany':
        'aún no se ha ejecutado',
    'kompletna':
        'completa',
    'kopia lustrzana':
        'copia espejo',
    'kopia zapasowa':
        'copia de seguridad',
    'nie':
        'no',
    'niedokończona':
        'sin terminar',
    'niedokończona — brakuje ok. {count} {files} ({size})':
        'sin terminar — falta copiar aprox. {count} {files} ({size})',
    'niezaszyfrowana':
        'sin cifrar',
    'nieznany format manifestu':
        'formato de manifiesto desconocido',
    'nowych plików':
        'archivos nuevos',
    'np. C:\\Odzyskane':
        'p. ej. C:\\Recuperados',
    'np. E:\\Kopie zapasowe':
        'p. ej. E:\\Copias de seguridad',
    'plik':
        'archivo',
    'plik stanu jest za krótki':
        'el archivo de estado es demasiado corto',
    'plik stanu w wersji {found}, obsługiwana: {supported}':
        'archivo de estado en la versión {found}; versión admitida: {supported}',
    'pliki':
        'archivos',
    'plików':
        'archivos',
    'podgląd kopii':
        'vista previa de la copia',
    'pozostaną w kopii':
        'se quedan en la copia',
    'rozmiar w kopii {actual} B zamiast {expected} B':
        'tamaño en la copia: {actual} B en lugar de {expected} B',
    'sprawdzanie kopii':
        'comprobación de la copia',
    'stan nieznany (zapisana starszą wersją programu)':
        'estado desconocido (escrita con una versión anterior del programa)',
    'suma kontrolna manifestu się nie zgadza':
        'la suma de comprobación del manifiesto no coincide',
    'suma kontrolna się nie zgadza — plik uszkodzony':
        'la suma de comprobación no coincide: archivo dañado',
    'szablon {name}':
        'plantilla {name}',
    'tak':
        'sí',
    'ten system plików':
        'este sistema de archivos',
    'wersja {version}':
        'versión {version}',
    'wersje z datą':
        'versiones fechadas',
    'weryfikacja':
        'verificación',
    'wyłączona':
        'desactivada',
    'zaszyfrowana (AES-256-GCM)':
        'cifrada (AES-256-GCM)',
    'zawartość różni się od pliku źródłowego':
        'el contenido difiere del archivo de origen',
    'zawartość różni się od sumy kontrolnej zapisanej podczas kopii':
        'el contenido no coincide con la suma de comprobación registrada durante la copia',
    'zmienionych':
        'modificados',
    'zostaną usunięte z kopii':
        'se eliminarán de la copia',
    '{done} z {total} • {speed}/s{eta}':
        '{done} de {total} • {speed}/s{eta}',
    '{done} • {speed}/s':
        '{done} • {speed}/s',
    '{hours} h {minutes} min':
        '{hours} h {minutes} min',
    '{label}: {count} {files}':
        '{label}: {count} {files}',
    '{message}\n\nSzczegóły techniczne znajdziesz w zakładce „Dziennik”.':
        '{message}\n\nEncontrarás los detalles técnicos en la pestaña «Registro».',
    '{minutes} min {seconds} s':
        '{minutes} min {seconds} s',
    '{name}: nie można odczytać ({error})':
        '{name}: no se puede leer ({error})',
    '{seconds} s':
        '{seconds} s',
    '{summary}\n\nProblemy:\n{problems}\n\nPełna lista znajduje się w zakładce „Dziennik”.':
        '{summary}\n\nProblemas:\n{problems}\n\nLa lista completa está en la pestaña «Registro».',
    '{summary}{notes}\n\nPliki zapisane przed przerwaniem są kompletne i zostały odnotowane w spisie treści kopii.\n\nAby dokończyć kopię, uruchom ją ponownie — program zaproponuje uzupełnienie tej wersji zamiast tworzenia nowej.':
        '{summary}{notes}\n\nLos archivos escritos antes de la interrupción están completos y figuran en el índice de la copia.\n\nPara terminar la copia, vuelve a iniciarla: el programa te propondrá completar esta versión en lugar de crear una nueva.',
    '{title} — gotowe':
        '{title} — completada',
    '{title} — przerwano':
        '{title} — interrumpida',
    '{title} — zakończono z błędami':
        '{title} — finalizada con errores',
    '{when}  •  {action}  •  {count} {files}':
        '{when}  •  {action}  •  {count} {files}',
    'Łączny rozmiar danych do przesłania':
        'Tamaño total de los datos que se transferirán',
    'Środowisko':
        'Entorno',
    'Źródła: {sources}\nCel: {destination}\nUkład: {structure} • Szyfrowanie: {encrypt} • Weryfikacja: {verify} • Dogrywka: {catchup} • Równolegle: {workers} • Data uzupełnienia w nazwie: {stamp}\nUtworzony: {created} • Ostatni przebieg: {last}':
        'Orígenes: {sources}\nDestino: {destination}\nDisposición: {structure} • Cifrado: {encrypt} • Verificación: {verify} • Pasada complementaria: {catchup} • En paralelo: {workers} • Fecha de actualización en el nombre: {stamp}\nCreada: {created} • Última ejecución: {last}',
    'Źródło nie zmieniło się w trakcie kopii — nie ma czego uzupełniać.':
        'El origen no cambió durante la copia: no hay nada que completar.',
    '—':
        '—',
    '• Kopia przyrostowa — zapisywane są wyłącznie pliki nowe i zmienione.\n  Porównanie opiera się na spisie treści kopii, rozmiarze i dacie modyfikacji;\n  przy różnicy liczona jest suma kontrolna SHA-256.\n\n• Wersje z datą — każdy przebieg tworzy kompletny folder z datą, a pliki\n  niezmienione są podpinane twardym dowiązaniem, więc nie zajmują miejsca dwa razy.\n\n• Weryfikacja po zapisie — zapisany plik jest odczytywany z powrotem\n  i porównywany ze źródłem.\n\n• Odporność na przerwania — pliki powstają pod nazwą tymczasową i są\n  podmieniane dopiero po pełnym zapisie.':
        '• Copia incremental: solo se escriben los archivos nuevos y los modificados.\n  La comparación se basa en el índice de la copia, el tamaño y la fecha de modificación;\n  si hay diferencias, se calcula una suma de comprobación SHA-256.\n\n• Versiones fechadas: cada ejecución crea una carpeta fechada completa, y los archivos\n  sin cambios se enlazan con vínculos físicos, así que nunca ocupan espacio dos veces.\n\n• Verificación tras la escritura: el archivo escrito se vuelve a leer\n  y se compara con el origen.\n\n• Resistencia a interrupciones: los archivos se crean con un nombre temporal y\n  solo se sustituyen cuando están escritos por completo.',
    '• Szyfr: AES-256 w trybie GCM (szyfrowanie z uwierzytelnieniem).\n• Wyprowadzanie klucza z hasła: {kdf}.\n• Nagłówek każdego pliku jest uwierzytelniony jako AAD — podmiana parametrów\n  unieważnia tag.\n• Każdy plik dostaje losowy, niepowtarzalny nonce.\n• Odszyfrowany plik powstaje dopiero po pomyślnej weryfikacji tagu.\n• Hasła nie są zapisywane w plikach programu. Opcjonalnie trafiają do\n  Menedżera poświadczeń Windows.':
        '• Cifrado: AES-256 en modo GCM (cifrado autenticado).\n• Derivación de la clave a partir de la contraseña: {kdf}.\n• El encabezado de cada archivo se autentica como AAD: cambiar los parámetros\n  invalida la etiqueta.\n• Cada archivo recibe un nonce aleatorio y único.\n• El archivo descifrado solo se crea después de verificar la etiqueta.\n• Las contraseñas no se escriben en los archivos del programa. Opcionalmente se guardan en el\n  Administrador de credenciales de Windows.',
    'Bez hasła nie da się odczytać ani jednego pliku z kopii.':
        'Sin la contraseña no se puede leer ni un solo archivo de la copia.',
    'Co chcesz chronić?':
        '¿Qué quieres proteger?',
    'Co chcesz teraz zrobić?':
        '¿Qué quieres hacer?',
    'Czyta kopię z nośnika i porównuje ją z zapisanymi sumami kontrolnymi.':
        'Lee la copia de la unidad y la compara con las sumas de comprobación registradas.',
    'Dalej':
        'Siguiente',
    'Dokumenty i zdjęcia':
        'Documentos y fotos',
    'Ekran powitalny wrócisz w ustawieniach, gdy zmienisz zdanie.':
        'Si cambias de opinión, puedes recuperar la pantalla de bienvenida en los ajustes.',
    'Ekran z pytaniem, co chcesz teraz zrobić: kopia, przywracanie, sprawdzenie.':
        'Una pantalla que pregunta qué quieres hacer: copia, restauración o comprobación.',
    'Foldery objęte kopią':
        'Carpetas incluidas en la copia',
    'Foldery z pracą. Kreator pominie katalogi, które odtwarza się jednym poleceniem (node_modules, venv, build).':
        'Carpetas con tu trabajo. El asistente omitirá las carpetas que se pueden regenerar con un solo comando (node_modules, venv, build).',
    'Gdzie zapisać kopię?':
        '¿Dónde guardar la copia?',
    'Historia i szyfrowanie':
        'Historial y cifrado',
    'Historia zmian (zalecane)':
        'Historial de cambios (recomendado)',
    'Jak bardzo chcesz się zabezpieczyć?':
        '¿Cuánta protección quieres?',
    'Jak wyżej, a dodatkowo każdy plik trafia do kopii zaszyfrowany (AES-256-GCM). Potrzebne przy kopii wożonej poza dom.':
        'Como la anterior y, además, cada archivo entra cifrado en la copia (AES-256-GCM). Necesario si te llevas la copia fuera de casa.',
    'Jedna aktualna kopia':
        'Una sola copia actualizada',
    'Język, motyw, domyślne wykluczenia i informacje o środowisku.':
        'Idioma, tema, exclusiones predeterminadas e información del entorno.',
    'Katalog docelowy leży wewnątrz źródła — wybierz inny.':
        'La carpeta de destino está dentro del origen: elige otra.',
    'Każdy przebieg tworzy folder z datą. Pliki niezmienione są podpinane dowiązaniem, więc historia kosztuje tyle, ile realnie się zmieniło.':
        'Cada ejecución crea una carpeta fechada. Los archivos sin cambios se enlazan, así que el historial solo ocupa lo que realmente ha cambiado.',
    'Każdy przebieg utworzy folder z datą. Pierwszy zajmie tyle, ile dane; kolejne — tyle, ile realnie się zmieniło.':
        'Cada ejecución creará una carpeta fechada. La primera ocupará lo mismo que los datos; las siguientes, solo lo que realmente haya cambiado.',
    'Kopia powstanie w: {path}':
        'La copia se creará en: {path}',
    'Kopia trafi do: {path}':
        'La copia irá a: {path}',
    'Kopia: {what}':
        'Copia: {what}',
    'Krok {number} z {total}':
        'Paso {number} de {total}',
    'Najlepiej na innym dysku fizycznym niż ten, który chronisz — kopia obok oryginału ginie razem z nim.':
        'Mejor en un disco físico distinto del que proteges: una copia junto al original se pierde con él.',
    'Najszybsza i najmniejsza. Kopia odpowiada temu, co masz teraz — bez historii wcześniejszych wersji.':
        'La más rápida y la que menos ocupa. La copia refleja lo que tienes ahora, sin historial de versiones anteriores.',
    'Nie było jeszcze żadnej kopii. Zacznij od „Zrób kopię”.':
        'Todavía no se ha hecho ninguna copia. Empieza por «Hacer copia».',
    'Nie lista ustawień, tylko ich skutki.':
        'No una lista de ajustes, sino sus efectos.',
    'Nie pokazuj tego ekranu przy starcie':
        'No mostrar esta pantalla al iniciar',
    'Nośnik docelowy':
        'Unidad de destino',
    'Odtwarza pliki z kopii — całość albo wybrany folder.':
        'Restaura archivos de una copia: todo o una carpeta concreta.',
    'Odśwież listę':
        'Actualizar la lista',
    'Ostatnia kopia: {when} • {count} {files}.':
        'Última copia: {when} • {count} {files}.',
    'Pierwszy przebieg jest najdłuższy — kolejne porównują rozmiar i datę modyfikacji, więc zwykle trwają sekundy.':
        'La primera ejecución es la más larga; las siguientes comparan el tamaño y la fecha de modificación, así que suelen durar segundos.',
    'Pliki w kopii będą zaszyfrowane; bez hasła nie da się ich odczytać.':
        'Los archivos de la copia estarán cifrados; sin la contraseña no se pueden leer.',
    'Podfoldery są uwzględniane automatycznie.':
        'Las subcarpetas se incluyen automáticamente.',
    'Pokazuj ekran powitalny przy starcie':
        'Mostrar la pantalla de bienvenida al iniciar',
    'Ponownie sprawdza podłączone nośniki':
        'Vuelve a comprobar las unidades conectadas',
    'Program będzie utrzymywał jeden folder zgodny ze źródłem. Każdy kolejny przebieg dopisze tylko to, co się zmieniło.':
        'El programa mantendrá una sola carpeta igual que el origen. Cada ejecución posterior añadirá solo lo que haya cambiado.',
    'Projekty i kod':
        'Proyectos y código',
    'Przechodzi do następnego kroku':
        'Pasa al paso siguiente',
    'Przechodzi do pełnego okna programu':
        'Va a la ventana completa del programa',
    'Sam wskażesz, co ma trafić do kopii.':
        'Tú eliges qué se copia.',
    'System plików: {filesystem}, klaster {cluster}':
        'Sistema de archivos: {filesystem}, clúster {cluster}',
    'Ten katalog leży wewnątrz folderu źródłowego — wybierz inny.':
        'Esta carpeta está dentro de una carpeta de origen: elige otra.',
    'Ten nośnik nie obsługuje twardych dowiązań, więc każda wersja z datą zajmie tyle miejsca co pełna kopia. Przy tym nośniku rozważ „jedną aktualną kopię”.':
        'Esta unidad no admite vínculos físicos, así que cada versión fechada ocupará tanto como una copia completa. Con esta unidad, considera «Una sola copia actualizada».',
    'To dysk systemowy — kopia nie przetrwa jego awarii. Jeśli masz drugi dysk albo pendrive, wybierz jego.':
        'Es el disco del sistema: si se avería, la copia se perderá con él. Si tienes otro disco o una memoria USB, elígelo.',
    'To się wydarzy':
        'Esto es lo que pasará',
    'Trzy gotowe zestawy zamiast kilkunastu przełączników.':
        'Tres configuraciones listas en lugar de una docena de opciones.',
    'Twoje pliki osobiste z folderów użytkownika. Najczęstszy wybór.':
        'Tus archivos personales de las carpetas de usuario. La opción más habitual.',
    'Uruchamia kreator, który ustawi kopię krok po kroku':
        'Inicia el asistente, que configura la copia paso a paso',
    'Nowa kopia krok po kroku…':
        'Nueva copia paso a paso…',
    'Ustawia kopię krok po kroku i zapisuje ją jako szablon':
        'Configura la copia paso a paso y la guarda como plantilla',
    'Ustawienia pierwszej kopii':
        'Configurar tu primera copia',
    'Ustawienia pierwszej kopii…':
        'Configurar la primera copia…',
    'W tym katalogu jest już kopia ({count} {files}) — program ją uzupełni, a nie nadpisze.':
        'Esta carpeta ya contiene una copia ({count} {files}): el programa la completará, no la sobrescribirá.',
    'Wraca do poprzedniego kroku':
        'Vuelve al paso anterior',
    'Wskaż dowolny katalog docelowy':
        'Elige cualquier carpeta de destino',
    'Wskaż folder kopii i kliknij „Sprawdź kopię”.':
        'Elige la carpeta de la copia y haz clic en «Comprobar copia».',
    'Wstecz':
        'Atrás',
    'Wybierz':
        'Elegir',
    'Wybierz inny folder…':
        'Elegir otra carpeta…',
    'Wybierz to, co najbliższe. Dokładną listę folderów poprawisz niżej.':
        'Elige lo más parecido. La lista exacta de carpetas la ajustas más abajo.',
    'Wybrane foldery':
        'Carpetas elegidas',
    'Zamknij':
        'Cerrar',
    'Zamyka kreator bez zapisywania':
        'Cierra el asistente sin guardar',
    'Zapisuje nowe i zmienione pliki. Pierwszy raz trwa najdłużej.':
        'Guarda los archivos nuevos y los modificados. La primera vez es la que más tarda.',
    'Zapisuje szablon bez uruchamiania kopii':
        'Guarda la plantilla sin iniciar la copia',
    'Zapisuje szablon i od razu uruchamia kopię':
        'Guarda la plantilla e inicia la copia enseguida',
    'Zapisz i zrób kopię':
        'Guardar y hacer copia',
    'Zapisz ustawienia':
        'Guardar ajustes',
    'Zrób kopię':
        'Hacer copia',
    'dysk systemowy':
        'disco del sistema',
    'wolne {free} z {total}':
        '{free} libres de {total}',
    'Porównano ze źródłem: {source}; tylko z sumą kontrolną (źródło zmieniło się albo jest niedostępne): {checksum}.':
        'Comparados con el origen: {source}; solo con la suma de comprobación (el origen ha cambiado o no está disponible): {checksum}.',
    'Przywraca losową próbkę plików do katalogu tymczasowego i porównuje je ze źródłem.\nSprawdza całą drogę odzyskiwania, a trwa minuty. Nic nie zostaje na dysku.':
        'Restaura una muestra aleatoria de archivos en una carpeta temporal y la compara con el origen.\nComprueba todo el proceso de recuperación y tarda minutos. No deja nada en el disco.',
    'Próbne przywrócenie':
        'Restauración de prueba',
    'W kopii nie ma plików, które dałoby się sprawdzić próbnie.':
        'La copia no tiene archivos que se puedan comprobar con una restauración de prueba.',
    'przywrócony plik różni się od pliku źródłowego':
        'el archivo restaurado difiere del archivo de origen',
    'przywrócony plik różni się od sumy kontrolnej zapisanej podczas kopii':
        'el archivo restaurado no coincide con la suma de comprobación registrada durante la copia',
    'próbne przywrócenie':
        'restauración de prueba',
    '(brak zapisanych szablonów)':
        '(no hay plantillas guardadas)',
    'Bez tego kopia planowa ruszy dopiero wtedy, gdy sam otworzysz program.':
        'Sin esto, una copia programada solo empezará cuando abras tú el programa.',
    'Codziennie o godzinie':
        'A diario a una hora fija',
    'Codziennie o wybranej godzinie (zalecane)':
        'A diario a la hora elegida (recomendado)',
    'Dla dysku USB podłączanego od czasu do czasu. Najwyżej jedna kopia na 12 godzin.':
        'Para un disco USB que conectas de vez en cuando. Como máximo, una copia cada 12 horas.',
    'Dostępne w zainstalowanej wersji programu (plik EXE).':
        'Disponible en la versión instalada del programa (el archivo EXE).',
    'Godzina kopii codziennej (czas tego komputera).':
        'Hora de la copia diaria (según el reloj de este equipo).',
    'Harmonogram działa wtedy, gdy działa program — także ukryty przy zegarze.':
        'La programación funciona mientras el programa está en marcha, también oculto junto al reloj.',
    'Harmonogram nie uruchamia kopii, dopóki tego nie odznaczysz. Ręczne kopie działają.':
        'La programación no inicia ninguna copia hasta que desmarques esta opción. Las copias manuales siguen funcionando.',
    'Harmonogram szablonu „{name}” zapisany.':
        'Programación de la plantilla «{name}» guardada.',
    'Harmonogram:':
        'Programación:',
    'Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.':
        'Si a esa hora el equipo está apagado, la copia empezará al encenderlo.',
    'Kiedy kopia z tego szablonu ma ruszać sama.':
        'Cuándo debe empezar sola la copia de esta plantilla.',
    'Kiedy robić kopię?':
        '¿Cuándo hacer la copia?',
    'Kopia będzie robiona codziennie o {time}; termin przegapiony przy wyłączonym komputerze program nadrobi po jego włączeniu.':
        'La copia se hará cada día a las {time}; si el equipo está apagado a esa hora, el programa la recuperará al encenderlo.',
    'Kopia planowa nie powiodła się':
        'La copia programada ha fallado',
    'Kopia rusza tylko wtedy, gdy ją uruchomisz.':
        'La copia solo empieza cuando la inicias tú.',
    'Kopia ruszy po podłączeniu dysku docelowego (najwyżej raz na 12 godzin).':
        'La copia empezará al conectar el disco de destino (como máximo, una vez cada 12 horas).',
    'Kopia ruszy po podłączeniu dysku docelowego — najwyżej raz na 12 godzin.':
        'La copia empieza al conectar el disco de destino, como máximo una vez cada 12 horas.',
    'Kopia sprzed miesiąca nie chroni tego, co zmieniło się od tamtej pory.':
        'Una copia de hace un mes no protege lo que ha cambiado desde entonces.',
    'Kopia „{name}” czeka':
        'La copia «{name}» está atrasada',
    'Kopia „{name}” nie ruszyła':
        'La copia «{name}» no ha empezado',
    'Kopie planowe działają, gdy działa program (także ukryty przy zegarze).':
        'Las copias programadas funcionan mientras el programa está en marcha (también oculto junto al reloj).',
    'Kopie planowe działają, gdy działa program: po zamknięciu okna zostaje ikona przy zegarze, a przy logowaniu do Windows program uruchamia się w tle.':
        'Las copias programadas funcionan mientras el programa está en marcha: al cerrar la ventana queda un icono junto al reloj, y al iniciar sesión en Windows el programa se abre en segundo plano.',
    'Kopie planowe i praca w tle':
        'Copias programadas y ejecución en segundo plano',
    'Kopie planowe wykonają się o czasie. Program zamkniesz z menu ikony przy zegarze.':
        'Las copias programadas se harán a su hora. Puedes salir del programa desde el menú del icono junto al reloj.',
    'Kopię uruchamiasz przyciskiem. Najprostsze, ale łatwo o niej zapomnieć.':
        'Inicias la copia con un botón. Es lo más sencillo, pero es fácil olvidarla.',
    'Kopię uruchamiasz sam — przyciskiem w programie albo z menu ikony przy zegarze.':
        'Inicias tú la copia: con el botón del programa o desde el menú del icono junto al reloj.',
    'Następna kopia: {when}. Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.':
        'Próxima copia: {when}. Si a esa hora el equipo está apagado, la copia empezará al encenderlo.',
    'Nie udało się zmienić startu przy logowaniu — szczegóły w dzienniku.':
        'No se ha podido cambiar el arranque al iniciar sesión; los detalles están en el registro.',
    'Od {days} dni nie było udanej kopii. Podłącz dysk docelowy albo otwórz program, żeby sprawdzić, co się dzieje.':
        'Hace {days} días que no hay ninguna copia correcta. Conecta el disco de destino o abre el programa para ver qué pasa.',
    'Otwórz Sigelith Backup':
        'Abrir Sigelith Backup',
    'Po podłączeniu dysku docelowego':
        'Al conectar el disco de destino',
    'Po podłączeniu dysku z kopią':
        'Al conectar el disco de copias',
    'Po zamknięciu okna działaj dalej przy zegarze, gdy są kopie planowe':
        'Al cerrar la ventana, seguir en marcha junto al reloj si hay copias programadas',
    'Potrzebne, żeby kopie planowe ruszały bez Twojego udziału. Hasło trafia do magazynu systemowego powiązanego z Twoim kontem, nie do plików programu.':
        'Necesario para que las copias programadas empiecen sin ti. La contraseña va al almacén del sistema vinculado a tu cuenta, no a los archivos del programa.',
    'Program uruchamia się w tle przy logowaniu, więc terminy nie przepadną.':
        'El programa se abre en segundo plano al iniciar sesión, así que no se pierde ninguna copia programada.',
    'Ręcznie':
        'Manualmente',
    'Ręcznie — kiedy zechcę':
        'Manualmente, cuando yo quiera',
    'Start przy logowaniu włączony':
        'Arranque al iniciar sesión activado',
    'Szablon jest zaszyfrowany, a hasło nie jest zapamiętane. Kopie planowe potrzebują hasła zapisanego w Menedżerze poświadczeń Windows.':
        'La plantilla está cifrada y la contraseña no está guardada. Las copias programadas necesitan la contraseña guardada en el Administrador de credenciales de Windows.',
    'Sigelith Backup będzie uruchamiał się w tle, żeby wykonywać kopie planowe. Wyłączysz to w ustawieniach programu.':
        'Sigelith Backup se abrirá en segundo plano para hacer las copias programadas. Puedes desactivarlo en los ajustes del programa.',
    'Sigelith Backup działa w tle':
        'Sigelith Backup sigue funcionando en segundo plano',
    'Uruchamiaj program w tle przy logowaniu do Windows':
        'Abrir el programa en segundo plano al iniciar sesión en Windows',
    'Wstrzymaj kopie planowe':
        'Pausar las copias programadas',
    'Zakończ':
        'Salir',
    'Zamknięcie okna chowa je, a harmonogram pilnuje terminów. Program zamkniesz z menu ikony przy zegarze.':
        'Cerrar la ventana solo la oculta, y la programación vigila los horarios. Para salir del programa, usa el menú del icono junto al reloj.',
    'Zrób kopię teraz':
        'Hacer copia ahora',
    '{summary} Szczegóły znajdziesz w programie, w zakładce „Dziennik”.':
        '{summary} Encontrarás los detalles en el programa, en la pestaña «Registro».',
    'Program działa z uprawnieniami administratora. Nie są mu potrzebne — kopia i przywracanie działają bez nich, a pliki zapisane przez administratora mogą później nie dać się zmienić ze zwykłego konta.':
        'El programa se está ejecutando con permisos de administrador. No los necesita: la copia y la restauración funcionan sin ellos, y los archivos escritos como administrador quizá no se puedan modificar después desde una cuenta normal.',
    'Pliki otwarte w innych programach nie trafiły do kopii: {files}. Zamknij te programy i uruchom kopię ponownie — dograne zostaną tylko te pliki.':
        'Los archivos abiertos en otros programas no han entrado en la copia: {files}. Cierra esos programas y vuelve a iniciar la copia: solo se añadirán esos archivos.',
    'Uwaga: w źródle zmieniło się podejrzanie dużo plików — {reasons}':
        'Atención: en el origen ha cambiado una cantidad sospechosa de archivos — {reasons}',
    'Wstrzymano kopię: w źródle zmieniło się podejrzanie dużo plików. {reasons}':
        'Copia en pausa: en el origen ha cambiado una cantidad sospechosa de archivos. {reasons}',
    'Zmieniło się albo zniknęło {count} z {previous} plików poprzedniej kopii.':
        'Han cambiado o desaparecido {count} de los {previous} archivos de la copia anterior.',
    '{suspicious} z {evaluated} sprawdzonych zmienionych plików ma treść, która nie pasuje do ich typu (wygląda na zaszyfrowaną).':
        '{suspicious} de {evaluated} archivos modificados comprobados tienen un contenido que no corresponde a su tipo (parece cifrado).',
    'Kontynuuj mimo to':
        'Continuar de todos modos',
    'Kopia planowa wstrzymana':
        'Copia programada en pausa',
    'Kopia wstrzymana do decyzji.':
        'Copia en pausa hasta que decidas.',
    'Kopia wstrzymana — w źródle zmieniło się podejrzanie dużo plików.':
        'Copia en pausa: en el origen ha cambiado una cantidad sospechosa de archivos.',
    'Podejrzanie dużo zmian':
        'Cantidad sospechosa de cambios',
    'Wstrzymaj kopię':
        'Pausar la copia',
    '{reasons}\n\nJeśli to spodziewane — aktualizacja programu, przeniesienie albo przerobienie wielu plików — kontynuuj.\n\nJeśli nie, NIE kontynuuj: tak wygląda działanie oprogramowania szyfrującego pliki (ransomware). Sprawdź najpierw, czy Twoje pliki dają się otworzyć. Wcześniejsze wersje w kopii pozostają nietknięte.':
        '{reasons}\n\nSi lo esperabas (una actualización de software, mover o rehacer muchos archivos), continúa.\n\nSi no, NO continúes: así actúa el software que cifra archivos (ransomware). Comprueba primero que tus archivos se abren. Las versiones anteriores de la copia siguen intactas.',
    '{reasons} To może być działanie złośliwego oprogramowania szyfrującego pliki. Otwórz program, sprawdź pliki i uruchom kopię ręcznie.':
        '{reasons} Puede ser obra de un programa malicioso que cifra archivos. Abre el programa, revisa los archivos e inicia la copia manualmente.',
    'Pominięto {count} {files}.':
        'Omitidos: {count} {files}.',
    'Ponawiam {count} {files}…':
        'Reintentando {count} {files}…',
    ' (bez {count} {files})':
        ' (sin {count} {files})',
    'plik otwarty w innym programie':
        'archivo abierto en otro programa',
    'pliki otwarte w innych programach':
        'archivos abiertos en otros programas',
    'plików otwartych w innych programach':
        'archivos abiertos en otros programas',
    'pliku otwartego w innym programie':
        'archivo abierto en otro programa',
    '\n\n…i kolejne: {count}.':
        '\n\n…y más: {count}.',
    'Foldery objęte kopią ({count}): {list}':
        'Carpetas incluidas en la copia ({count}): {list}',
    'Nośnik nie obsługuje twardych dowiązań — kopiuję do nowej wersji niezmienione pliki: {count} ({size})…':
        'La unidad no admite vínculos físicos: copiando a la nueva versión los archivos sin cambios: {count} ({size})…',
    'Pliki bez sumy kontrolnej sprawdzone tylko co do rozmiaru, bo ich źródło zmieniło się albo jest niedostępne: {count}.':
        'Archivos sin suma de comprobación verificados solo por tamaño, porque su origen ha cambiado o no está disponible: {count}.',
    'Pliki bez zapisanej sumy kontrolnej, porównane ze źródłem i uzupełnione w spisie treści: {count}.':
        'Archivos sin suma de comprobación registrada, comparados con el origen y añadidos al índice: {count}.',
    'Pliki przeniesione w źródle: {count} — trafią do kopii bez przesyłania danych.':
        'Archivos movidos en el origen: {count}; entrarán en la copia sin transferir datos.',
    'Pliki skasowane w źródle: {count} — {action}.':
        'Archivos borrados en el origen: {count} — {action}.',
    'Pliki z końcówką dopisaną do nazwy, których oryginały zniknęły: {count}.':
        'Archivos con una terminación añadida al nombre cuyos originales han desaparecido: {count}.',
    'Pliki zmienione w trakcie kopiowania: {count} — zostaną zapisane ponownie w przebiegu uzupełniającym.':
        'Archivos modificados mientras se copiaban: {count}; se volverán a escribir en la pasada complementaria.',
    'Pliki, których brakuje w kopii i które zostaną zapisane ponownie: {count}.':
        'Archivos que faltan en la copia y que se volverán a escribir: {count}.',
    'Podpinanie niezmienionych plików do nowej wersji: {count}…':
        'Enlazando los archivos sin cambios con la nueva versión: {count}…',
    'Pomijam pliki, które już są w tej wersji kopii: {count}.':
        'Omitiendo los archivos que ya están en esta versión de la copia: {count}.',
    'Porządkowanie historii — usunięte najstarsze wersje: {count}.':
        'Limpieza del historial — versiones más antiguas eliminadas: {count}.',
    'Przenoszenie plików, które zmieniły miejsce w źródle: {count}…':
        'Moviendo los archivos que cambiaron de sitio en el origen: {count}…',
    'Próbne przywrócenie losowo wybranych plików: {count}…':
        'Restauración de prueba de archivos elegidos al azar: {count}…',
    'Usuwanie z kopii plików skasowanych w źródle: {count}…':
        'Eliminando de la copia los archivos borrados en el origen: {count}…',
    'Uzupełniam kopię o pliki, które przybyły lub zmieniły się w trakcie: {count} ({size})…':
        'Completando la copia con los archivos nuevos o modificados mientras tanto: {count} ({size})…',
    'Uzupełnianie wersji {version} — pliki już zapisane, które zostaną pominięte: {count}.':
        'Completando la versión {version} — archivos ya escritos que se omitirán: {count}.',
    'Wznawiam wersję {version} — już zapisane: {done}, do dogrania: {todo}.':
        'Reanudando la versión {version} — ya escritos: {done}; pendientes: {todo}.',
    'pliku':
        'archivo',
    'Brak fragmentu {cid} w magazynie kopii.':
        'Falta el fragmento {cid} en el almacén de la copia.',
    'Brak opisu magazynu fragmentów w katalogu kopii.':
        'Falta la descripción del almacén de fragmentos en la carpeta de la copia.',
    'Duże pliki zapisuj różnicowo (od 256 MB)':
        'Guardar los archivos grandes de forma diferencial (desde 256 MB)',
    'Fragment {cid} jest uszkodzony.':
        'El fragmento {cid} está dañado.',
    'Kolejna wersja dużego pliku — maszyny wirtualnej, skrzynki pocztowej, bazy —\nzapisuje tylko zmienione fragmenty zamiast całego pliku. W kopii taki plik\nleży jako przepis + fragmenty; złoży go program albo skrypt ratunkowy.':
        'La siguiente versión de un archivo grande (una máquina virtual, un buzón de correo, una base de datos)\nguarda solo los fragmentos modificados en lugar del archivo entero. En la copia, ese archivo\nse guarda como receta + fragmentos; lo reconstruye el programa o el script de rescate.',
    'Opis magazynu fragmentów jest uszkodzony.':
        'La descripción del almacén de fragmentos está dañada.',
    'Plik złożony z fragmentów różni się od zapisanego w przepisie.':
        'El archivo reconstruido a partir de los fragmentos difiere del registrado en su receta.',
    'Podane hasło nie pasuje do fragmentów zapisanych wcześniej w tej kopii.':
        'La contraseña introducida no coincide con la de los fragmentos escritos antes en esta copia.',
    'Przepis pliku jest uszkodzony.':
        'La receta del archivo está dañada.',
    'To nie jest przepis pliku zapisanego fragmentami.':
        'No es la receta de un archivo guardado por fragmentos.',
    'Usunięto nieużywane fragmenty dużych plików: {count} ({size}).':
        'Fragmentos sin usar de archivos grandes eliminados: {count} ({size}).',
    ', zakotwiczona w Bitcoinie':
        ', anclada en Bitcoin',
    'Adres usługi:':
        'Dirección del servicio:',
    'Brak fragmentu {cid} w kopii poza domem.':
        'Falta el fragmento {cid} en la copia externa.',
    'Brak klucza albo hasła w Menedżerze poświadczeń Windows — zapisz ustawienia kopii poza domem jeszcze raz.':
        'Falta la clave o la contraseña en el Administrador de credenciales de Windows: vuelve a guardar los ajustes de la copia externa.',
    'Brak spisu wersji, którego dotyczy znacznik.':
        'Falta la lista de archivos de la versión a la que se refiere el sello de tiempo.',
    'Certyfikat PDF':
        'Certificado PDF',
    'Druga, zaszyfrowana kopia w usłudze zgodnej z S3 (np. Backblaze B2)':
        'Una segunda copia, cifrada, en un servicio compatible con S3 (p. ej., Backblaze B2)',
    'Folder w kubełku:':
        'Carpeta en el bucket:',
    'Hasło kopii poza domem':
        'Contraseña de la copia externa',
    'Hasło kopii poza domem nie pasuje do danych zapisanych w tym miejscu.':
        'La contraseña de la copia externa no coincide con los datos guardados en esa ubicación.',
    'Hasło kopii poza domem powinno mieć co najmniej 10 znaków.':
        'La contraseña de la copia externa debe tener al menos 10 caracteres.',
    'Hasło szyfrowania:':
        'Contraseña de cifrado:',
    'Identyfikator klucza:':
        'ID de clave:',
    'Katalog, do którego trafią pliki':
        'Carpeta a la que irán los archivos',
    'Klucz tajny':
        'Clave secreta',
    'Klucz tajny:':
        'Clave secreta:',
    'Kopia na dysku obok komputera nie przetrwa pożaru ani kradzieży. Tu ustawisz drugą kopię w usłudze zgodnej z S3 (np. Backblaze B2). Pliki są szyfrowane na tym komputerze osobnym hasłem — usługa widzi tylko nieczytelne fragmenty.':
        'Una copia en un disco junto al equipo no sobrevive a un incendio ni a un robo. Aquí configuras una segunda copia en un servicio compatible con S3 (p. ej., Backblaze B2). Los archivos se cifran en este equipo con una contraseña aparte: el servicio solo ve fragmentos ilegibles.',
    'Kopia poza domem':
        'Copia externa',
    'Kopia poza domem dla szablonu „{name}” zapisana.':
        'Copia externa de la plantilla «{name}» guardada.',
    'Kopia poza domem nie ruszyła':
        'La copia externa no ha empezado',
    'Kopia poza domem potrzebuje Menedżera poświadczeń Windows, a jest on niedostępny.':
        'La copia externa necesita el Administrador de credenciales de Windows, que no está disponible.',
    'Kopia poza domem „{name}”':
        'Copia externa «{name}»',
    'Kopia poza domem…':
        'Copia externa…',
    'Korzeń tygodnia zakotwiczony w łańcuchu Bitcoina.':
        'La raíz semanal está anclada en la cadena de Bitcoin.',
    'Kubełek (bucket):':
        'Bucket:',
    'Migawek w usłudze: {count}.':
        'Instantáneas en el servicio: {count}.',
    'Migawka i cel':
        'Instantánea y destino',
    'Migawka kopii poza domem jest uszkodzona.':
        'La instantánea de la copia externa está dañada.',
    'Migawka {stamp}: plików bez zmian {reused}, wysłanych {files}, nowych fragmentów {chunks} ({size}).':
        'Instantánea {stamp} — archivos sin cambios: {reused}, subidos: {files}, fragmentos nuevos: {chunks} ({size}).',
    'MinIO / Wasabi / inna zgodna z S3':
        'MinIO / Wasabi / otro compatible con S3',
    'NIEPOPRAWNY':
        'NO VÁLIDA',
    'Nie ma migawki {stamp} w kopii poza domem.':
        'No existe la instantánea {stamp} en la copia externa.',
    'Nie udało się połączyć z usługą przechowywania: {error}':
        'No se ha podido conectar con el servicio de almacenamiento: {error}',
    'Nie udało się wczytać migawek: {error}':
        'No se han podido cargar las instantáneas: {error}',
    'Nie udało się zapisać klucza albo hasła w magazynie systemowym.':
        'No se ha podido guardar la clave o la contraseña en el almacén del sistema.',
    'Odśwież z sieci':
        'Actualizar en línea',
    'Opis kopii poza domem jest uszkodzony.':
        'La descripción de la copia externa está dañada.',
    'Oznakowana: {utc} (BeatTime {beat})':
        'Sello de tiempo: {utc} (BeatTime {beat})',
    'Pliki wersji różnią się od spisu, który został oznakowany.':
        'Los archivos de la versión difieren de la lista que recibió el sello de tiempo.',
    'Pobiera i odszyfrowuje pliki wybranej migawki':
        'Descarga y descifra los archivos de la instantánea elegida',
    'Pobiera listę migawek z usługi':
        'Descarga del servicio la lista de instantáneas',
    'Pobiera podpis tygodnia i stan kotwicy w Bitcoinie':
        'Descarga la firma semanal y el estado del anclaje en Bitcoin',
    'Pobieram potwierdzenia…':
        'Descargando los recibos…',
    'Podaj hasło szyfrowania kopii poza domem.':
        'Introduce la contraseña de cifrado de la copia externa.',
    'Podaj klucz tajny usługi.':
        'Introduce la clave secreta del servicio.',
    'Podam dane ręcznie':
        'Introduciré los datos a mano',
    'Pominięte (otwarte w innych programach albo zmienione w trakcie): {count}.':
        'Omitidos (abiertos en otros programas o modificados durante la operación): {count}.',
    'Porządkowanie kopii poza domem…':
        'Limpiando la copia externa…',
    'Potwierdzenia odświeżone.':
        'Recibos actualizados.',
    'Poza dom':
        'Copia externa',
    'Połączenie działa: zapis, odczyt i usuwanie się udały.':
        'La conexión funciona: escritura, lectura y borrado correctos.',
    'Połączenie nie działa: {error}':
        'La conexión no funciona: {error}',
    'Przywraca pliki z zaszyfrowanej kopii w usłudze S3 — także na nowym komputerze':
        'Restaura archivos de la copia cifrada en el servicio S3, también en un equipo nuevo',
    'Przywracanie z kopii poza domem':
        'Restauración desde la copia externa',
    'Przywracanie {count} {files} z kopii poza domem…':
        'Restaurando {count} {files} desde la copia externa…',
    'Przywróć':
        'Restaurar',
    'Region:':
        'Región:',
    'Skąd':
        'Origen',
    'Spis wersji zgodny ze znacznikiem: {answer}':
        'Lista de la versión conforme al sello de tiempo: {answer}',
    'Spis wersji został zmieniony po oznakowaniu.':
        'La lista de archivos de la versión se modificó después de recibir el sello de tiempo.',
    'Sprawdza spis wersji, drogę w drzewie tygodnia i podpis — bez sieci':
        'Comprueba la lista de la versión, la ruta en el árbol de la semana y la firma, sin conexión',
    'Sprawdzam połączenie…':
        'Comprobando la conexión…',
    'Sprawdź':
        'Comprobar',
    'Sprawdź połączenie':
        'Comprobar la conexión',
    'Starsze migawki są usuwane, gdy nadmiar sięgnie kilku — co kilka dni.':
        'Las instantáneas más antiguas se eliminan cuando sobran unas cuantas, cada pocos días.',
    'Suma w drzewie tygodnia: {answer}':
        'Hash en el árbol de la semana: {answer}',
    'Suma wersji nie należy do drzewa tygodnia podanego w potwierdzeniu.':
        'El hash de la versión no forma parte del árbol de la semana indicado en el recibo.',
    'Ta wersja nie ma znacznika czasu.':
        'Esta versión no tiene sello de tiempo.',
    'Także po kopiach planowych. Wysyłane są tylko pliki nowe i zmienione.':
        'También tras las copias programadas. Solo se suben los archivos nuevos y los modificados.',
    'Tydzień jeszcze się nie zamknął — podpis pojawi się po poniedziałku 00:00 UTC.':
        'La semana aún no se ha cerrado: la firma llegará después del lunes a las 00:00 UTC.',
    'Usunięto starsze migawki: {count}, nieużywane fragmenty: {chunks}.':
        'Instantáneas antiguas eliminadas: {count}; fragmentos sin usar: {chunks}.',
    'Usługa chwilowo niedostępna ({status}).':
        'El servicio no está disponible temporalmente ({status}).',
    'Usługa odrzuciła żądanie ({status} {code}): {message}':
        'El servicio ha rechazado la solicitud ({status} {code}): {message}',
    'Usługa przechowywania':
        'Servicio de almacenamiento',
    'Usługa zwróciła inną treść niż zapisana.':
        'El servicio ha devuelto un contenido distinto del que se escribió.',
    'Usługa:':
        'Servicio:',
    'Uzupełnij adres usługi, nazwę kubełka i klucze dostępu.':
        'Rellena la dirección del servicio, el nombre del bucket y las claves de acceso.',
    'Uzupełnij adres usługi, region, kubełek i identyfikator klucza.':
        'Rellena la dirección del servicio, la región, el bucket y el ID de clave.',
    'W tym katalogu kopii nie ma jeszcze znaczników czasu.':
        'En esta carpeta de copia aún no hay sellos de tiempo.',
    'W tym miejscu nie ma jeszcze kopii poza domem.':
        'En esta ubicación aún no hay ninguna copia externa.',
    'Wczytaj migawki':
        'Cargar instantáneas',
    'Wczytaj migawki i wybierz jedną z listy.':
        'Carga las instantáneas y elige una de la lista.',
    'Wczytuję migawkę {stamp}…':
        'Cargando la instantánea {stamp}…',
    'Wczytuję poprzednią migawkę kopii poza domem…':
        'Cargando la instantánea anterior de la copia externa…',
    'Wybierz migawkę i katalog, do którego trafią pliki.':
        'Elige una instantánea y la carpeta a la que irán los archivos.',
    'Wybierz wersję z listy.':
        'Elige una versión de la lista.',
    'Wysyłaj poza dom po każdej udanej kopii z tego szablonu':
        'Subir a la copia externa tras cada copia correcta de esta plantilla',
    'Wysyłam poza dom pliki nowe i zmienione: {count}…':
        'Subiendo a la copia externa los archivos nuevos y modificados: {count}…',
    'Z kopii poza domem…':
        'Desde la copia externa…',
    'Zachowuj migawek:':
        'Instantáneas que conservar:',
    'Zapisuje ustawienia; klucz i hasło trafiają do Menedżera poświadczeń Windows':
        'Guarda los ajustes; la clave y la contraseña van al Administrador de credenciales de Windows',
    'Zapisuje, odczytuje i usuwa mały plik próbny':
        'Escribe, lee y borra un pequeño archivo de prueba',
    'Zapisuję migawkę {stamp}…':
        'Guardando la instantánea {stamp}…',
    'Znacznik dowodzi, że wersja kopii w dokładnie tym kształcie istniała w podanej chwili. Podpis tygodnia pojawia się po jego zamknięciu (poniedziałek 00:00 UTC), a kotwica w Bitcoinie — zwykle kilka godzin później.':
        'El sello de tiempo demuestra que la versión de la copia existía exactamente así en el momento indicado. La firma semanal llega cuando se cierra la semana (lunes 00:00 UTC), y el anclaje en Bitcoin, normalmente unas horas después.',
    'Znacznika czasu nie udało się zapisać: {error}':
        'No se ha podido guardar el sello de tiempo: {error}',
    'Znaczniki czasu':
        'Sellos de tiempo',
    'Znaczniki czasu…':
        'Sellos de tiempo…',
    'kopia poza domem':
        'copia externa',
    'np. komputer-domowy':
        'p. ej. equipo-casa',
    'oznakowana {when} — podpis po zamknięciu tygodnia':
        'sellada el {when} — firma al cerrarse la semana',
    'podpisana (tydzień {week}){bitcoin}':
        'firmada (semana {week}){bitcoin}',
    'poprawny':
        'válida',
    'przywracanie z kopii poza domem':
        'restauración desde la copia externa',
    'Łączę się z usługą…':
        'Conectando con el servicio…',
    ' dni':
        ' días',
    ' mies.':
        ' meses',
    ' tyg.':
        ' sem.',
    'Ile ostatnich wersji zachować. Starsze są kasowane po udanym przebiegu.':
        'Cuántas versiones recientes conservar. Las más antiguas se borran tras una ejecución correcta.',
    'Kalendarz zostawia najnowszą wersję z każdego z ostatnich dni, tygodni\ni miesięcy — gęsto dla świeżych zmian, rzadko dla dawnych. Nadmiar jest\nkasowany po udanym przebiegu; wersje niedokończone nigdy.':
        'El calendario conserva la versión más reciente de cada uno de los últimos días, semanas\ny meses: muchas para los cambios recientes, pocas para los antiguos. El sobrante se\nborra tras una ejecución correcta; las versiones sin terminar, nunca.',
    'Z ilu ostatnich dni zachować po jednej, najnowszej wersji.':
        'Número de días recientes de los que se conserva una versión (la más reciente de cada día).',
    'Z ilu ostatnich miesięcy zachować po jednej, najnowszej wersji.':
        'Número de meses recientes de los que se conserva una versión (la más reciente de cada mes).',
    'Z ilu ostatnich tygodni zachować po jednej, najnowszej wersji.':
        'Número de semanas recientes de las que se conserva una versión (la más reciente de cada semana).',
    'Zachowuj:':
        'Conservar:',
    'kalendarz: dni, tygodnie, miesiące':
        'calendario: días, semanas, meses',
    'ostatnie wersje':
        'últimas versiones',
    'wszystkie wersje':
        'todas las versiones',
    ' (niedokończona)':
        ' (sin terminar)',
    'Fragment nazwy albo ścieżki, bez rozróżniania wielkości liter.':
        'Parte de un nombre o de una ruta, sin distinguir mayúsculas y minúsculas.',
    'Główny folder kopii':
        'Carpeta principal de la copia',
    'Historia pliku':
        'Historial del archivo',
    'Nazwa':
        'Nombre',
    'Nic nie znaleziono.':
        'No se ha encontrado nada.',
    'Nie udało się: {error}':
        'Ha fallado: {error}',
    'Odtwarza plik do katalogu tymczasowego i otwiera go':
        'Restaura el archivo en una carpeta temporal y lo abre',
    'Odtwarza plik w wybranym miejscu':
        'Restaura el archivo en el lugar que elijas',
    'Odtwarzam „{name}”…':
        'Restaurando «{name}»…',
    'Otwarto kopię „{name}” (plik tymczasowy, zniknie po zamknięciu programu).':
        'Se ha abierto la copia de «{name}» (archivo temporal: desaparecerá al cerrar el programa).',
    'Otwórz':
        'Abrir',
    'Otwórz kopię':
        'Abrir copia',
    'Pliki i wersje wprost z kopii — bez przywracania':
        'Archivos y versiones directamente de la copia, sin restaurar',
    'Pliki i wersje wprost z kopii — bez przywracania całości.':
        'Archivos y versiones directamente de la copia, sin restaurarla entera.',
    'Pokazuje pliki i wersje tej kopii — pojedynczy plik otworzysz bez przywracania całości':
        'Muestra los archivos y las versiones de esta copia: puedes abrir un solo archivo sin restaurarla entera',
    'Pokaż foldery':
        'Mostrar carpetas',
    'Przeglądaj…':
        'Explorar…',
    'Przeglądanie':
        'Explorar',
    'Przeszukuje spis treści kopii':
        'Busca en el índice de la copia',
    'Rozmiar':
        'Tamaño',
    'Szukaj':
        'Buscar',
    'Szukaj pliku w najnowszym stanie kopii…':
        'Buscar un archivo en el estado más reciente de la copia…',
    'Szukam…':
        'Buscando…',
    'W których wersjach jest ten plik i kiedy się zmieniał':
        'En qué versiones está este archivo y cuándo cambió',
    'W tym folderze nie ma wersji kopii.':
        'En esta carpeta no hay versiones de la copia.',
    'Wczytuje wersje z tego folderu kopii':
        'Carga las versiones de esta carpeta de copia',
    'Wersja kopii, której zawartość widzisz poniżej.':
        'La versión de la copia cuyo contenido ves abajo.',
    'Wersja: {version}':
        'Versión: {version}',
    'Wersje z tym plikiem: {count}. Dwuklik otwiera kopię z danej wersji.':
        'Versiones con este archivo: {count}. Haz doble clic para abrir la copia de esa versión.',
    'Wraca z wyników wyszukiwania do drzewa folderów':
        'Vuelve de los resultados de búsqueda al árbol de carpetas',
    'Wskaż folder kopii i kliknij „Otwórz”.':
        'Elige la carpeta de la copia y haz clic en «Abrir».',
    'Zapisano: {path}':
        'Guardado: {path}',
    'Zapisz jako…':
        'Guardar como…',
    'Zapisz kopię pliku':
        'Guardar una copia del archivo',
    'Zaznacz plik i wybierz „Otwórz kopię”, żeby zajrzeć do niego w zwykłym programie, albo „Historia pliku”, żeby zobaczyć, w których wersjach się zmieniał.':
        'Selecciona un archivo y elige «Abrir copia» para verlo en su programa habitual, o «Historial del archivo» para ver en qué versiones cambió.',
    'Zmieniono':
        'Modificado',
    'Znalezione pliki: {count}. Wyniki pochodzą z najnowszego stanu kopii.':
        'Archivos encontrados: {count}. Los resultados proceden del estado más reciente de la copia.',
    'przeglądanie kopii':
        'exploración de la copia',
    'zmieniony':
        'modificado',
    'najstarsza zachowana kopia':
        'copia más antigua conservada',
    'Foldery w AppData':
        'Carpetas en AppData',
    'Przywracanie utworzy nowe foldery bezpośrednio w AppData:\n\n{folders}\n\nWindows pozwala wersji programu ze Sklepu tworzyć je tylko w jej prywatnej kopii — pliki będą widoczne w tym programie, ale nie w programie, do którego należą.\n\nNajprościej: zainstaluj i raz uruchom tamten program (utworzy swój folder), a potem przywróć jeszcze raz. Albo przywróć do zwykłego folderu i przenieś pliki Eksploratorem.':
        'La restauración creará carpetas nuevas directamente en AppData:\n\n{folders}\n\nWindows solo deja que la versión de Microsoft Store de este programa las cree en su copia privada: los archivos se verán en este programa, pero no en el programa al que pertenecen.\n\nLo más sencillo: instala y abre una vez ese otro programa (creará su carpeta) y luego vuelve a restaurar. O restaura en una carpeta normal y mueve los archivos con el Explorador de archivos.',
    'Przywracanie utworzyłoby w AppData nowe foldery, których inne programy nie zobaczą: {folders}':
        'La restauración crearía en AppData carpetas nuevas que otros programas no verán: {folders}',
    'Przywracanie wstrzymane do decyzji.':
        'Restauración en pausa hasta que decidas.',
    'Przywróć mimo to':
        'Restaurar de todos modos',
    'Start programu przy logowaniu wyłączono w Ustawieniach Windows. Włączysz go tam: Ustawienia → Aplikacje → Uruchamianie → Sigelith Backup.':
        'El arranque del programa al iniciar sesión se desactivó en la Configuración de Windows. Puedes activarlo allí: Configuración → Aplicaciones → Inicio → Sigelith Backup.',
    'Start przy logowaniu':
        'Arranque al iniciar sesión',
    'Start przy logowaniu wyłączono w Ustawieniach Windows → Aplikacje → Uruchamianie; dopóki go tam nie włączysz, kopie planowe działają tylko przy otwartym programie.':
        'El arranque al iniciar sesión se desactivó en Configuración de Windows → Aplicaciones → Inicio; hasta que lo actives allí, las copias programadas solo funcionan con el programa abierto.',
    'Ten sam przełącznik jest w Ustawieniach Windows → Aplikacje → Uruchamianie. Wyłączony tam da się włączyć tylko tam.':
        'El mismo interruptor está en Configuración de Windows → Aplicaciones → Inicio. Si se desactiva allí, solo se puede volver a activar allí.',
    'Brak pliku {name} w katalogu programu.':
        'Falta el archivo {name} en la carpeta del programa.',
    'Jakie dane program przetwarza i gdzie':
        'Qué datos trata el programa y dónde',
    'Kod źródłowy Qt':
        'Código fuente de Qt',
    'Licencja programu':
        'Licencia del programa',
    'Licencja programu i licencje użytych składników':
        'Licencia del programa y licencias de los componentes que usa',
    'Licencje':
        'Licencias',
    'Licencje i prywatność':
        'Licencias y privacidad',
    'Licencje…':
        'Licencias…',
    'Otwiera folder z plikami licencji w Eksploratorze':
        'Abre la carpeta con los archivos de licencia en el Explorador de archivos',
    'Pokaż pliki licencji':
        'Mostrar los archivos de licencia',
    'Polityka prywatności':
        'Política de privacidad',
    'Polityka prywatności…':
        'Política de privacidad…',
    'Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0 — to osobne pliki w katalogu programu, które można zastąpić zgodnymi wersjami. Kod źródłowy wersji dołączonych do programu: {qt} oraz {pyside}.':
        'El programa usa las bibliotecas Qt y PySide6 bajo la licencia LGPL-3.0: son archivos aparte en la carpeta del programa y se pueden sustituir por versiones compatibles. Código fuente de las versiones incluidas en el programa: {qt} y {pyside}.',
    'Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0, z Pythona i z innych składników na licencjach otwartych (m.in. MIT, BSD, Apache 2.0); ikony: Bootstrap Icons (MIT). Wykaz, prawa autorskie, pełne teksty licencji i adresy kodu źródłowego Qt są pod przyciskiem „Licencje”.':
        'El programa usa las bibliotecas Qt y PySide6 bajo la licencia LGPL-3.0, Python y otros componentes con licencias de código abierto (entre ellas MIT, BSD y Apache 2.0); iconos: Bootstrap Icons (MIT). La lista, los avisos de copyright, los textos completos de las licencias y las direcciones del código fuente de Qt están en el botón «Licencias».',
    'Program usunie z Menedżera poświadczeń Windows wszystkie hasła, które zapamiętał: hasła kopii i dane dostępu do kopii poza domem. Kopie planowe szablonów zaszyfrowanych będą potem czekać, aż podasz hasło.\n\nUsunąć?':
        'El programa eliminará del Administrador de credenciales de Windows todas las contraseñas que ha recordado: las de las copias y los datos de acceso de la copia externa. Después, las copias programadas de las plantillas cifradas esperarán a que introduzcas la contraseña.\n\n¿Eliminarlas?',
    'Składniki i ich licencje':
        'Componentes y sus licencias',
    'Strona z kodem źródłowym Qt w wersji użytej w programie':
        'La página con el código fuente de Qt en la versión usada en el programa',
    'Usunięte zapamiętane hasła: {count}.':
        'Contraseñas recordadas eliminadas: {count}.',
    'Usuwa z Menedżera poświadczeń Windows wszystkie hasła zapamiętane przez program — na przykład przed odinstalowaniem':
        'Elimina del Administrador de credenciales de Windows todas las contraseñas que ha recordado el programa, por ejemplo antes de desinstalarlo',
    'Usuń zapamiętane hasła':
        'Eliminar las contraseñas recordadas',
    'Usuń zapamiętane hasła…':
        'Eliminar las contraseñas recordadas…',
    '© {years} {publisher}. Wolne oprogramowanie na licencji GNU GPL w wersji 3 lub nowszej.':
        '© {years} {publisher}. Software libre bajo la licencia GNU GPL, versión 3 o posterior.',
    'Kod źródłowy':
        'Código fuente',
    'Kod źródłowy programu w serwisie GitHub':
        'El código fuente del programa en GitHub',
    'Sigelith odrzucił żądanie ({status}): {detail}':
        'Sigelith ha rechazado la solicitud ({status}): {detail}',
    'Nie udało się połączyć z Sigelith: {error}':
        'No se ha podido conectar con Sigelith: {error}',
    'Sigelith odesłał potwierdzenie innej sumy kontrolnej.':
        'Sigelith ha devuelto el recibo de otro hash.',
    'Znacznik czeka na połączenie z Sigelith.':
        'El sello de tiempo está esperando a conectar con Sigelith.',
    'Podpis tygodnia nie zgadza się z kluczem Sigelith zapisanym w programie.':
        'La firma semanal no corresponde a la clave de Sigelith integrada en el programa.',
    'Otwiera certyfikat znacznika na stronie Sigelith':
        'Abre el certificado del sello de tiempo en la web de Sigelith',
    'Podpis Sigelith: {answer}':
        'Firma de Sigelith: {answer}',
    'Znaczniki Sigelith wersji w tym katalogu kopii: sprawdzenie i certyfikat':
        'Sellos de tiempo de Sigelith de las versiones de esta carpeta de copia: comprobación y certificado',
    'Znakuję wersję czasem Sigelith (wysyłana jest tylko suma kontrolna)…':
        'Dando a la versión un sello de tiempo de Sigelith (solo se envía el hash)…',
    'Znacznik czasu czeka na połączenie z Sigelith — zostanie wysłany przy następnej kopii.':
        'El sello de tiempo está esperando a conectar con Sigelith: se enviará con la próxima copia.',
    'Znakuj wersję czasem Sigelith':
        'Dar a la versión un sello de tiempo de Sigelith',
    'Znaczniki czasu Sigelith':
        'Sellos de tiempo de Sigelith',
    'czeka na połączenie z Sigelith':
        'esperando a conectar con Sigelith',
    'Dowód, że kopia w tym kształcie istniała danego dnia (podpis Ed25519, kotwica\nw Bitcoinie). Do sigelith.org trafia wyłącznie suma kontrolna spisu wersji —\nżadne nazwy plików ani ich treść.':
        'Prueba de que la copia existía exactamente así en un día dado (firma Ed25519, anclaje\nen Bitcoin). A sigelith.org solo llega el hash de la lista de archivos de la versión:\nni nombres de archivo ni su contenido.',
    'Kopie zapasowe folderów na dysk zewnętrzny, z historią wersji i szyfrowaniem. Wszystko dzieje się na Twoim komputerze, bez konta i bez telemetrii. Z internetem program łączy się tylko wtedy, gdy sam włączysz kopię poza domem albo znaczniki czasu Sigelith.':
        'Copias de seguridad de tus carpetas en un disco externo, con historial de versiones y cifrado. Todo ocurre en tu equipo, sin cuenta y sin telemetría. El programa solo se conecta a internet si tú activas la copia externa o los sellos de tiempo de Sigelith.',
    'Bez dokumentu: {count} {stamps} — plik zmienił się po stemplu albo zniknął i nie ma go w żadnej wersji tej kopii ({names}). Sam dowód jest zachowany.':
        'Sin documento: {count} {stamps} — el archivo cambió después del sellado o desapareció, y no está en ninguna versión de esta copia ({names}). La prueba en sí se conserva.',
    'Brak pliku dowodu albo dowód jest zaszyfrowany.':
        'Falta el archivo de la prueba o la prueba está cifrada.',
    'Chroni dowody Sigelith: historię stempli i oznakowane dokumenty.':
        'Protege las pruebas de Sigelith: el historial de sellos y los documentos sellados.',
    'Chroń dowody Sigelith':
        'Proteger las pruebas de Sigelith',
    'Chroń też dowody Sigelith':
        'Proteger también las pruebas de Sigelith',
    'Dokument':
        'Documento',
    'Dokumenty oznakowane w Sigelith, zabezpieczone w tej kopii: sprawdzenie i odzyskanie':
        'Documentos sellados con Sigelith y resguardados en esta copia: comprobación y recuperación',
    'Dowody Sigelith':
        'Pruebas de Sigelith',
    'Dowody Sigelith: historia stempli i dokładne kopie oznakowanych dokumentów z plikami .beatproof trafią do magazynu dowodów w katalogu kopii.':
        'Pruebas de Sigelith: el historial de sellos y copias exactas de los documentos sellados, con sus archivos .beatproof, irán al almacén de pruebas de la carpeta de la copia.',
    'Dowody Sigelith: zabezpieczone dokumenty {count} z {total}':
        'Pruebas de Sigelith: documentos resguardados {count} de {total}',
    'Dowody Sigelith…':
        'Pruebas de Sigelith…',
    'Dowody z problemem: {count} — szczegóły w kolumnie „Stan”.':
        'Pruebas con problemas: {count}; los detalles están en la columna «Estado».',
    'Dowodów Sigelith nie udało się zabezpieczyć: {error}':
        'No se han podido resguardar las pruebas de Sigelith: {error}',
    "Droga w drzewie Merkle'a nie prowadzi do podpisanego korzenia tygodnia.":
        'La ruta en el árbol de Merkle no lleva a la raíz semanal firmada.',
    'Gdzie zapisać dokumenty i dowody':
        'Dónde guardar los documentos y las pruebas',
    'Historia stempli Sigelith Desktop i dokładne bajty oznakowanych dokumentów, z plikami .beatproof — w osobnym magazynie, którego retencja nie sprząta.':
        'El historial de sellos de Sigelith Desktop y los bytes exactos de los documentos sellados, con sus archivos .beatproof, en un almacén aparte que la limpieza por retención nunca toca.',
    'Każdy stempel ma tu swój folder z dokładnie tym dokumentem, który oznakowano, i plikiem .beatproof. „Sprawdź” liczy sumę każdego dokumentu i sprawdza podpis tygodnia bez łączenia się z siecią.':
        'Cada sello tiene aquí su propia carpeta con exactamente el documento que se selló y su archivo .beatproof. «Comprobar» calcula el hash de cada documento y comprueba la firma semanal sin conectarse a la red.',
    'Kopia obejmie folder danych Sigelith Desktop (historię stempli), a każdy oznakowany\ndokument trafi — dokładnie w tej postaci, którą oznakowano — do magazynu dowodów\nw katalogu kopii, razem z plikiem .beatproof. Starych wersji magazyn nie dotyczy:\nretencja go nie sprząta.':
        'La copia incluirá la carpeta de datos de Sigelith Desktop (el historial de sellos), y cada documento\nsellado irá, exactamente tal como se selló, al almacén de pruebas de la carpeta\nde la copia, junto con su archivo .beatproof. El almacén no forma parte de las versiones antiguas:\nla limpieza por retención nunca lo toca.',
    'Magazyn dowodów jest pusty.':
        'El almacén de pruebas está vacío.',
    'Na tym komputerze jest Sigelith Desktop: {count} {stamps}.':
        'Sigelith Desktop está instalado en este equipo: {count} {stamps}.',
    'Na tym komputerze nie ma danych Sigelith Desktop.':
        'En este equipo no hay datos de Sigelith Desktop.',
    'Otwórz folder dowodów':
        'Abrir la carpeta de pruebas',
    'Oznakowano':
        'Sellado',
    'Pokazuje magazyn dowodów w Eksploratorze':
        'Muestra el almacén de pruebas en el Explorador de archivos',
    'Przywróć zaznaczone…':
        'Restaurar seleccionados…',
    'Sigelith Desktop: {count} {stamps} w folderze {path}.':
        'Sigelith Desktop: {count} {stamps} en la carpeta {path}.',
    'Sprawdza każdy dokument i jego dowód bez łączenia z siecią':
        'Comprueba cada documento y su prueba sin conectarse a la red',
    'Sprawdzam dowody…':
        'Comprobando las pruebas…',
    'Stan':
        'Estado',
    'Stemple w magazynie: {count}, z dokumentem: {documents}.':
        'Sellos en el almacén: {count}; con documento: {documents}.',
    'Suma dokumentu nie zgadza się z dowodem.':
        'El hash del documento no coincide con la prueba.',
    'To nie jest plik dowodu Sigelith (beatproof-v1).':
        'No es un archivo de prueba de Sigelith (beatproof-v1).',
    'Tydzień stempla jeszcze się nie zamknął — podpis dojdzie przy kolejnej kopii.':
        'La semana del sello aún no se ha cerrado: la firma se añadirá en una copia posterior.',
    'W magazynie nie ma dokumentu do tego dowodu.':
        'En el almacén no hay ningún documento para esta prueba.',
    'Wszystkie dowody pasują do dokumentów i mają poprawny podpis.':
        'Todas las pruebas coinciden con sus documentos y tienen una firma válida.',
    'Zabezpieczam dokumenty oznakowane w Sigelith…':
        'Resguardando los documentos sellados con Sigelith…',
    'Zapisano pliki: {count} w {path}.':
        'Archivos guardados: {count} en {path}.',
    'Zapisuje dokumenty razem z plikami .beatproof we wskazanym folderze':
        'Guarda los documentos junto con sus archivos .beatproof en la carpeta que elijas',
    'bez dokumentu — dowód zachowany':
        'sin documento — prueba conservada',
    'czekają na podpis tygodnia: {count}':
        'esperan la firma semanal: {count}',
    'dokument i dowód są w kopii':
        'el documento y la prueba están en la copia',
    'dokument jest; dowód czeka na podpis tygodnia':
        'documento presente; la prueba espera la firma semanal',
    'dowodu nie da się odczytać':
        'no se puede leer la prueba',
    'dowody Sigelith':
        'pruebas de Sigelith',
    'dowody uzupełnione o podpis tygodnia: {count}':
        'pruebas completadas con la firma semanal: {count}',
    'nowe: {count}':
        'nuevos: {count}',
    'odtworzone ze starszych wersji kopii: {count}':
        'recuperados de versiones anteriores de la copia: {count}',
    'sprawdzony: dokument i dowód się zgadzają':
        'comprobado: el documento y la prueba coinciden',
    'stempel':
        'sello',
    'stemple':
        'sellos',
    'stempli':
        'sellos',
    'zaszyfrowany — podaj hasło, żeby sprawdzić':
        'cifrado — introduce la contraseña para comprobarlo',
    'Chroń dowody Sigelith, gdy go zainstaluję':
        'Proteger las pruebas de Sigelith cuando lo instale',
    'Dowody Sigelith: na tym komputerze nie ma jeszcze Sigelith Desktop — ochrona zacznie działać sama, gdy się pojawi.':
        'Pruebas de Sigelith: Sigelith Desktop aún no está en este equipo; la protección se activará sola cuando aparezca.',
    'Dowody Sigelith: ochrona zacznie działać sama, gdy zainstalujesz Sigelith Desktop.':
        'Pruebas de Sigelith: la protección se activará sola cuando instales Sigelith Desktop.',
    'Dowody czasu dla ważnych dokumentów':
        'Pruebas de tiempo para documentos importantes',
    'Kopia zachowa każdy dokument oznakowany w Sigelith Desktop dokładnie w tej postaci, którą oznakowano, razem z dowodem — nawet gdy oryginał później się zmieni.':
        'La copia conservará cada documento sellado con Sigelith Desktop exactamente tal como se selló, junto con su prueba, aunque el original cambie después.',
    'Ochrona zacznie działać sama, gdy na komputerze pojawi się Sigelith Desktop.':
        'La protección se activará sola cuando Sigelith Desktop aparezca en el equipo.',
    'Otwiera stronę programu Sigelith Desktop':
        'Abre la página de Sigelith Desktop',
    'Poznaj Sigelith Desktop':
        'Descubrir Sigelith Desktop',
    'Sigelith Desktop, program tego samego wydawcy, oznakuje dokument czasem: to podpisany dowód, że plik w tej postaci istniał w danej chwili, sprawdzalny bez udziału kogokolwiek. Sigelith Backup przechowa potem każdy oznakowany dokument razem z dowodem.':
        'Sigelith Desktop, un programa del mismo editor, da a un documento un sello de tiempo: una prueba firmada de que el archivo existía exactamente así en un momento dado, que cualquiera puede comprobar sin depender de nadie. Después, Sigelith Backup guarda cada documento sellado junto con su prueba.',
    'Umowy, faktury, projekty — czasem trzeba wykazać, że dokument istniał danego dnia.':
        'Contratos, facturas, proyectos: a veces hay que demostrar que un documento existía en una fecha concreta.',
    'Nieznany format spisu wersji.':
        'Formato desconocido de la lista de la versión.',
    'Ta wersja nie ma pieczęci dla pojedynczych plików (kopia sprzed wersji 3.0 albo bez znaczników czasu).':
        'Esta versión no tiene sello para archivos individuales (copia anterior a la versión 3.0 o sin sellos de tiempo).',
    'Pieczęć tej wersji czeka jeszcze na podpis tygodnia Sigelith — dowód będzie gotowy po poniedziałku 00:00 UTC i kolejnej kopii.':
        'El sello de esta versión aún espera la firma semanal de Sigelith: la prueba estará lista después del lunes a las 00:00 UTC y de la siguiente copia.',
    'Brak oświadczenia pieczęci w folderze wersji.':
        'Falta la declaración del sello en la carpeta de la versión.',
    'Oświadczenie pieczęci nie zgadza się z pieczęcią wersji.':
        'La declaración del sello no coincide con el sello de la versión.',
    'Drzewo plików wersji nie zgadza się z pieczęcią.':
        'El árbol de archivos de la versión no coincide con el sello.',
    'Tego pliku nie ma w spisie tej wersji.':
        'Este archivo no está en la lista de esta versión.',
    'To nie jest dowód pliku z kopii Sigelith Backup ({format}).':
        'No es una prueba de archivo de Sigelith Backup ({format}).',
    'Dowód jest uszkodzony — brakuje pól albo mają zły format.':
        'La prueba está dañada: faltan campos o tienen un formato incorrecto.',
    'Ten plik nie jest plikiem, którego dotyczy dowód.':
        'Este archivo no es el archivo al que se refiere la prueba.',
    'Ścieżka pliku w dowodzie nie zgadza się z liściem drzewa.':
        'La ruta del archivo en la prueba no coincide con la hoja del árbol.',
    'Droga w drzewie plików nie prowadzi do korzenia z pieczęci.':
        'El camino en el árbol de archivos no lleva a la raíz sellada.',
    'Oświadczenie pieczęci nie potwierdza tego drzewa plików.':
        'La declaración del sello no confirma este árbol de archivos.',
    'Potwierdzenie Sigelith nie dotyczy tej pieczęci.':
        'La confirmación de Sigelith no corresponde a este sello.',
    'Dowód czasu…':
        'Prueba de tiempo…',
    'Zapisuje dowód, że ten plik był w kopii w chwili jej oznakowania — bez ujawniania innych plików':
        'Guarda una prueba de que este archivo estaba en la copia cuando se selló, sin revelar los demás archivos',
    'Dowód czasu':
        'Prueba de tiempo',
    'Dołączyć do dowodu ścieżkę pliku w kopii („{path}”)?\n\nBez niej dowód dalej potwierdza plik i chwilę oznakowania, ale nie mówi, gdzie plik leżał.':
        '¿Incluir en la prueba la ruta del archivo en la copia («{path}»)?\n\nSin ella, la prueba sigue confirmando el archivo y el momento del sellado, pero no dice dónde estaba el archivo.',
    'Przygotowuję dowód dla „{name}”…':
        'Preparando la prueba de «{name}»…',
    'Zapisz dowód czasu':
        'Guardar la prueba de tiempo',
    'Dowód pliku Sigelith (*{suffix})':
        'Prueba de archivo de Sigelith (*{suffix})',
    'Zapisano dowód i certyfikat PDF: {path}. Sprawdzi go Sigelith Desktop albo strona sigelith.org/verify/.':
        'Se han guardado la prueba y el certificado PDF: {path}. Puedes comprobarla con Sigelith Desktop o en sigelith.org/verify/.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją sprawdzić.':
        'La copia está cifrada: introduce la contraseña para comprobarla.',
    'Ta wersja nie ma pieczęci — nie ma z czym porównać plików.':
        'Esta versión no tiene sello: no hay con qué comparar los archivos.',
    'Pieczęć wersji się nie potwierdza: {problems}':
        'El sello de la versión no se confirma: {problems}',
    'brak podpisu tygodnia':
        'falta la firma semanal',
    'Audyt przerwany.':
        'Auditoría cancelada.',
    'próbka {checked} z {listed} plików':
        'una muestra de {checked} de {listed} archivos',
    'wszystkie pliki ({count})':
        'todos los archivos ({count})',
    'Nietknięta: sprawdzono {scope}, wszystko zgodne z pieczęcią w publicznym dzienniku.':
        'Intacta: comprobación de {scope}; todo coincide con el sello del registro público.',
    'zmienione: {files}':
        'modificados: {files}',
    'brakujące: {files}':
        'faltan: {files}',
    'nieczytelne albo uszkodzone: {files}':
        'ilegibles o dañados: {files}',
    'PODMIENIONA albo uszkodzona ({scope}) — {details}.':
        'MANIPULADA o dañada ({scope}) — {details}.',
    'Audyt treści':
        'Auditoría de contenido',
    'Czyta z nośnika każdy plik tej wersji i porównuje go z sumą oznakowaną w publicznym dzienniku':
        'Lee de la unidad cada archivo de esta versión y lo compara con el hash sellado en el registro público',
    'Ostatnia nietknięta':
        'Última intacta',
    'Sprawdza wersje od najnowszej i wskazuje ostatnią zgodną z pieczęcią — z niej przywracaj':
        'Comprueba las versiones empezando por la más reciente y señala la última que coincide con su sello: restaura desde ella',
    'Ostatnia nietknięta wersja: {label} — z niej przywracaj.':
        'Última versión intacta: {label}. Restaura desde ella.',
    'Żadna wersja z pieczęcią nie jest nietknięta.':
        'Ninguna versión con sello está intacta.',
    'Czytam pliki kopii i porównuję je z pieczęcią w publicznym dzienniku…':
        'Leyendo los archivos de la copia y comparándolos con el sello del registro público…',
    'Sprawdzam próbkę starszej wersji z pieczęcią w publicznym dzienniku…':
        'Comprobando una muestra de una versión anterior con su sello del registro público…',
    'Audyt z pieczęcią: próbka wersji {label} zgodna z publicznym dziennikiem.':
        'Auditoría con sello: la muestra de la versión {label} coincide con el registro público.',
    'UWAGA — audyt z pieczęcią, wersja {label}: {details}':
        'ATENCIÓN — auditoría con sello, versión {label}: {details}',
    'Przekaż…':
        'Entregar…',
    'Zapisuje tę wersję pliku i otwiera ją w Sigelith Handover — odbiorca potwierdzi odbiór własnym kluczem':
        'Guarda esta versión del archivo y la abre en Sigelith Handover: el destinatario confirmará la recepción con su propia clave',
    'Przekazanie z dowodem doręczenia':
        'Entrega con prueba de entrega',
    'Przekazanie z dowodem doręczenia robi Sigelith Desktop (od wersji 3.0.1): odbiorca potwierdza odbiór własnym kluczem, a chwila doręczenia trafia do publicznego dziennika. Na tym komputerze go nie ma albo jest w starszej wersji. Otworzyć stronę programu?':
        'La entrega con prueba de entrega la hace Sigelith Desktop (versión 3.0.1 o posterior): el destinatario confirma la recepción con su propia clave y el momento de la entrega queda anotado en el registro público. En este equipo no está instalado o su versión es anterior. ¿Abrir la página del programa?',
    'Zapisz plik do przekazania':
        'Guardar el archivo que se va a entregar',
    'Otwieram Sigelith Handover z plikiem „{name}” — wybierz odbiorcę.':
        'Abriendo Sigelith Handover con «{name}»: elige el destinatario.',
    'Kapsuły czasu…':
        'Cápsulas del tiempo…',
    'Pliki zapieczętowane w tej kopii do daty — klucze wydają dopiero po niej sieć drand i serwer kluczy Sigelith':
        'Archivos sellados en esta copia hasta una fecha: la red drand y el servidor de claves de Sigelith solo liberan las claves después de ella',
    'Wskaż najpierw folder kopii — kapsuła leży w kopii.':
        'Elige primero la carpeta de la copia: la cápsula se guarda en la copia.',
    'Kapsuły czasu':
        'Cápsulas del tiempo',
    'Kapsuła pieczętuje wybrany folder do chwili, którą wskażesz. Otwierają ją dowolne dwie z trzech części: runda sieci drand z tej chwili, udział serwera kluczy Sigelith (wydawany dopiero po tej chwili — to zasada operatora, nie kryptografia) i kod odzyskiwania zapisany obok kapsuły. Kto ma tę kopię, ma więc i kod: do wcześniejszego otwarcia wystarczy mu, że operator złamie swoją zasadę. Po tej chwili otworzy ją każdy, kto ma jej pliki. Kapsuła leży w tej kopii, nie na serwerze; otwiera ją strona sigelith.org/capsule/.':
        'Una cápsula sella la carpeta elegida hasta el momento que indiques. La abren dos cualesquiera de tres partes: la ronda de la red drand de ese momento, la parte del servidor de claves de Sigelith (que solo se libera después de ese momento: es una norma del operador, no criptografía) y el código de recuperación guardado junto a la cápsula. Así que quien tenga esta copia tiene también el código: para abrirla antes de tiempo, solo necesita que el operador rompa su norma. Después de ese momento, podrá abrirla cualquiera que tenga sus archivos. La cápsula está en esta copia, no en un servidor; se abre en sigelith.org/capsule/.',
    'Wybierz kapsułę z listy albo utwórz nową.':
        'Elige una cápsula de la lista o crea una nueva.',
    'Nowa kapsuła…':
        'Nueva cápsula…',
    'Pieczętuje wybrany folder do daty':
        'Sella la carpeta elegida hasta una fecha',
    'Pokaż w folderze':
        'Mostrar en la carpeta',
    'Otwiera folder kapsuły w Eksploratorze':
        'Abre la carpeta de la cápsula en el Explorador de archivos',
    'Otwórz na stronie':
        'Abrir en la web',
    'Strona sigelith.org/capsule/ otwiera kapsułę po jej dacie':
        'La página sigelith.org/capsule/ abre la cápsula después de su fecha',
    'można otworzyć':
        'se puede abrir',
    'zamknięta':
        'sellada',
    'W tej kopii nie ma jeszcze kapsuł czasu.':
        'En esta copia aún no hay cápsulas del tiempo.',
    'Ta kapsuła da się otworzyć na stronie sigelith.org/capsule/ — wskaż jej pliki.':
        'Esta cápsula ya se puede abrir en sigelith.org/capsule/: elige allí sus archivos.',
    'Kapsuła jest zamknięta do daty z listy. Kod odzyskiwania leży w pliku obok niej.':
        'La cápsula está sellada hasta la fecha de la lista. El código de recuperación está en un archivo junto a ella.',
    'Wybierz folder do zapieczętowania':
        'Elige la carpeta que quieres sellar',
    'Pieczętuję „{name}” — kilka sekund na krzywej eliptycznej…':
        'Sellando «{name}»: unos segundos de curva elíptica…',
    'kapsuła czasu':
        'cápsula del tiempo',
    'Kapsuła zapieczętowana':
        'Cápsula sellada',
    '„{name}” otworzy się najwcześniej {when}.\n\nKod odzyskiwania (skopiowany do schowka, zapisany też obok kapsuły):\n\n{code}\n\nZapisz go w bezpiecznym miejscu. Przed datą otwarcia sam niczego nie otwiera; po niej zastępuje jeden z kluczy, gdyby był niedostępny.':
        '«{name}» se abrirá no antes del {when}.\n\nCódigo de recuperación (copiado al portapapeles y guardado también junto a la cápsula):\n\n{code}\n\nGuárdalo en un lugar seguro. Antes de la fecha de apertura no abre nada por sí solo; después, sustituye a una de las claves si no estuviera disponible.',
    'Nie udało się zapieczętować: {error}':
        'No se ha podido sellar: {error}',
    'Nowa kapsuła czasu':
        'Nueva cápsula del tiempo',
    'Otworzy się najwcześniej':
        'Se abrirá no antes de',
    'kapsuła':
        'cápsula',
    'Chwila otwarcia musi być w przyszłości.':
        'El momento de apertura debe estar en el futuro.',
    'Na bieżąco':
        'Continuamente',
    'Zmiany w folderach źródłowych trafiają do dzisiejszej wersji kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje. Jedna wersja na dzień; ze znacznikami czasu zamyka ją pieczęć następnego dnia.':
        'Los cambios en las carpetas de origen llegan a la versión de hoy de la copia unos minutos después de guardarse, y al conectar el disco la copia se sincroniza enseguida. Una versión por día; con sellos de tiempo, la cierra un sello al día siguiente.',
    'Na bieżąco — po każdej zmianie i po podłączeniu dysku':
        'Continuamente: tras cada cambio y al conectar el disco',
    'Dla dysku podłączonego na stałe albo często: zmiany trafiają do kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje.':
        'Para un disco conectado siempre o a menudo: los cambios llegan a la copia unos minutos después de guardarse, y al conectar el disco la copia se sincroniza enseguida.',
    'Kopia będzie na bieżąco: zmiany trafią do dzisiejszej wersji kilka minut po zapisie, a po podłączeniu dysku kopia od razu się zsynchronizuje.':
        'La copia estará siempre al día: los cambios llegarán a la versión de hoy unos minutos después de guardarse, y al conectar el disco la copia se sincronizará enseguida.',
    'przywracanie':
        'restauración',
    'Nowa kopia krok po kroku':
        'Nueva copia paso a paso',
}
