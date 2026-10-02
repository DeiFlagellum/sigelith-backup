"""Katalog rosyjski: „polski tekst źródłowy” → „tekst (rosyjski)”.

Klucze są te same co w ``en.py`` i muszą dokładnie odpowiadać napisom w kodzie;
pilnuje tego ``tests/test_i18n.py``. Pola w nawiasach klamrowych (``{count}``)
zostają bez zmian. Formaty dat są te same co w Sigelith Desktop.
"""

from __future__ import annotations

TEXTS: dict[str, str] = {
    '\n\nLokalizacja:\n{path}':
        '\n\nРасположение:\n{path}',
    '\nDo uzupełnienia: niedokończone kopie: {count} — możesz je uzupełnić, wybierając wersję poniżej.':
        '\nНезавершённые копии: {count} — их можно дополнить, выбрав версию ниже.',
    '\nUwaga: duży klaster ({size}): każdy mały plik zajmuje co najmniej tyle miejsca. Przy wielu małych plikach kopia zajmie wielokrotnie więcej niż dane.':
        '\nВнимание: большой кластер ({size}) — каждый маленький файл занимает не меньше этого объёма. При большом количестве мелких файлов копия займёт в несколько раз больше места, чем сами данные.',
    '\nUwaga: niedokończone wersje (nie zawierają wszystkich plików): {names}':
        '\nВнимание: незавершённые версии (содержат не все файлы): {names}',
    '\nUwaga: {filesystem} nie obsługuje twardych dowiązań — każda wersja z datą zajmuje tyle miejsca co pełna kopia.':
        '\nВнимание: {filesystem} не поддерживает жёсткие ссылки — каждая датированная версия занимает столько же места, сколько полная копия.',
    ' wersji':
        ' верс.',
    ' z szyfrowaniem AES-256-GCM…':
        ' — с шифрованием AES-256-GCM…',
    ' ×':
        ' ×',
    ' — a ponieważ {filesystem} nie obsługuje twardych dowiązań, zapisze ponownie wszystkie pliki i zajmie tyle miejsca co cała kopia':
        ' — а поскольку {filesystem} не поддерживает жёсткие ссылки, она заново запишет все файлы и займёт столько же места, сколько вся копия',
    ' • pozostało {time}':
        ' • осталось {time}',
    '%d.%m %H:%M':
        '%d.%m %H:%M',
    '%d.%m.%Y':
        '%d.%m.%Y',
    '%d.%m.%Y %H:%M':
        '%d.%m.%Y, %H:%M',
    ', klaster {size}':
        ', кластер {size}',
    ', uzupełniona {when}':
        ', дополнена {when}',
    'Analizuje pliki i pokazuje plan. Nic nie zapisuje.':
        'Анализирует файлы и показывает план. Ничего не записывает.',
    'Anulowano przed rozpoczęciem kopii.':
        'Отменено до начала копирования.',
    'Anuluj':
        'Отмена',
    'Argon2id (t={passes}, {memory} MiB, p={threads})':
        'Argon2id (t={passes}, {memory} MiB, p={threads})',
    'Argon2id — {passes} przebiegi, {memory} MiB, {threads} wątki':
        'Argon2id — проходов: {passes}, {memory} MiB, потоков: {threads}',
    'Automatycznie (język systemu)':
        'Автоматически (язык системы)',
    'Bardzo dobre':
        'Очень надёжный',
    'Bardzo słabe':
        'Очень слабый',
    'Brak manifestu — skanuję katalog kopii.':
        'Манифест не найден — сканирование папки копии.',
    'Brakuje tagu uwierzytelniającego — plik jest obcięty.':
        'Отсутствует тег аутентификации — файл обрезан.',
    'Błąd uruchamiania':
        'Ошибка запуска',
    'Ciemny':
        'Тёмная',
    'Co dokładnie zostanie zapisane przy najbliższym przebiegu.':
        'Что именно будет записано при следующем запуске.',
    'Co kopiujemy':
        'Что копируем',
    'Co zrobić, gdy plik o tej nazwie już istnieje w katalogu docelowym.':
        'Что делать, если файл с таким именем уже есть в целевой папке.',
    'Czas w nazwie to BeatTime — 1000 beatów na dobę, kotwica w UTC, ten sam moment na całym świecie. Data jest datą UTC, więc zgadza się z zegarem.':
        'Время в имени — это BeatTime: 1000 битов в сутки, привязка к UTC, один и тот же момент во всём мире. Дата указана по UTC, поэтому совпадает с часами.',
    'Czym jest {app}':
        'Что такое {app}',
    'Czyści tylko okno — plik dziennika pozostaje':
        'Очищает только окно — файл журнала остаётся',
    'Dane aplikacji: {path}':
        'Данные приложения: {path}',
    'Decyduje, czy zachowujemy historię wersji.':
        'Определяет, сохраняется ли история версий.',
    'Dobre':
        'Надёжный',
    'Dodaj folder':
        'Добавить папку',
    'Dodaj przynajmniej jeden folder źródłowy.':
        'Добавьте хотя бы одну исходную папку.',
    'Dogrywka zmian z czasu kopii:':
        'Дозапись изменений, сделанных во время копирования:',
    'Dokąd przywracamy':
        'Куда восстанавливаем',
    'Dokładnie to, co program realnie stosuje.':
        'Именно то, что программа реально использует.',
    'Domyślne wykluczenia':
        'Исключения по умолчанию',
    'Domyślne wykluczenia zapisane.':
        'Исключения по умолчанию сохранены.',
    'Domyślnie wyłączone. Przy włączonej opcji skasowanie pliku w źródle\nusuwa też jego jedyną kopię zapasową — operacja nieodwracalna.':
        'По умолчанию выключено. Если опция включена, удаление файла в источнике\nудаляет и его единственную резервную копию — это необратимо.',
    'Dopisuj do nazwy katalogu datę ostatniego uzupełnienia':
        'Добавлять к имени папки дату последнего дополнения',
    'Dziennik':
        'Журнал',
    'Dziennik: {path}':
        'Журнал: {path}',
    'Ekran przywracania wypełniony danymi szablonu.':
        'Экран восстановления заполнен данными шаблона.',
    'Folder docelowy kopii — najlepiej na innym dysku fizycznym.':
        'Целевая папка копии — лучше всего на другом физическом диске.',
    'Folder zawierający kopię utworzoną przez {app}.':
        'Папка с копией, созданной программой {app}.',
    'Gdy plik już istnieje:':
        'Если файл уже существует:',
    'Gdzie zapisujemy':
        'Куда записываем',
    'Gotowe do pracy.':
        'Готово к работе.',
    'Gotowe. Wybierz foldery do kopii.':
        'Готово. Выберите папки для копирования.',
    'Gotowe: {count} {files}, {size}, {seconds} s.':
        'Готово: {count} {files}, {size}, {seconds} с.',
    'Główny folder kopii. Zawiera spis treści (.cleanvault-manifest).':
        'Главная папка копии. Содержит оглавление копии (.cleanvault-manifest).',
    'Hasła nie da się odzyskać ani zresetować. Jeśli je zgubisz, dane z kopii zaszyfrowanej są bezpowrotnie stracone — tak działa poprawne szyfrowanie.':
        'Пароль невозможно восстановить или сбросить. Если вы его потеряете, данные зашифрованной копии будут утрачены безвозвратно — так работает правильное шифрование.',
    'Hasła w obu polach różnią się.':
        'Пароли в двух полях не совпадают.',
    'Hasło':
        'Пароль',
    'Hasło do kopii':
        'Пароль копии',
    'Hasło nie jest nigdzie zapisywane w postaci jawnej.\nBez niego nie da się odzyskać danych — nie istnieje żadna furtka serwisowa.':
        'Пароль нигде не хранится в открытом виде.\nБез него данные восстановить невозможно — никакой сервисной лазейки не существует.',
    'Hasło nie może być puste.':
        'Пароль не может быть пустым.',
    'Hasło niezapisane':
        'Пароль не сохранён',
    'Hasło powinno mieć co najmniej 8 znaków.':
        'Пароль должен содержать не менее 8 символов.',
    'Hasło trafia do magazynu systemowego powiązanego z Twoim kontem.\nNigdy nie jest zapisywane w plikach programu.':
        'Пароль попадает в системное хранилище, привязанное к вашей учётной записи.\nОн никогда не записывается в файлы программы.',
    'Hasło użyte przy tworzeniu kopii':
        'Пароль, указанный при создании копии',
    'Ile plików kopia przetwarza jednocześnie. Przy setkach tysięcy małych plików\nczas kopii to głównie opóźnienia na każdy plik (otwarcie, skanowanie\nantywirusowe, zapis na nośnik), a nie przesył danych — praca równoległa\nskraca go kilkukrotnie.\n\n„automatycznie” dobiera liczbę do procesora (do 32). Na wolnym dysku\ntalerzowym mniejsza wartość (2–4) bywa szybsza.':
        'Сколько файлов копирование обрабатывает одновременно. При сотнях тысяч мелких файлов\nвремя копирования уходит в основном на задержки на каждом файле (открытие, проверка\nантивирусом, запись на носитель), а не на передачу данных — параллельная работа\nсокращает его в несколько раз.\n\n«автоматически» подбирает число под процессор (до 32). На медленном жёстком\nдиске (HDD) меньшее значение (2–4) бывает быстрее.',
    'Informacje przydatne przy zgłaszaniu problemu.':
        'Сведения, полезные при сообщении о проблеме.',
    'Jak to działa':
        'Как это работает',
    'Jasny':
        'Светлая',
    'Jeden folder utrzymywany w zgodzie ze źródłem. Brak historii wersji,\nza to najprostsza struktura i najmniejsze zużycie miejsca.':
        'Одна папка, синхронизированная с источником. Без истории версий,\nзато самая простая структура и наименьший расход места.',
    'Jeśli operacja zakończy się błędem, skopiuj stąd ostatnie wiersze — zawierają dokładną przyczynę, a nie tylko komunikat ogólny.':
        'Если операция завершится ошибкой, скопируйте отсюда последние строки — в них указана точная причина, а не только общее сообщение.',
    'Język interfejsu zmieniony.':
        'Язык интерфейса изменён.',
    'Język zmienisz po zakończeniu bieżącej operacji.':
        'Язык можно будет изменить после завершения текущей операции.',
    'Język:':
        'Язык:',
    'Katalog docelowy leży wewnątrz źródła ({path}). Kopia kopiowałaby samą siebie w nieskończoność.':
        'Целевая папка находится внутри источника ({path}). Копия копировала бы саму себя бесконечно.',
    'Katalog docelowy nie może być tym samym katalogiem co źródłowy.':
        'Целевая папка не может совпадать с исходной.',
    'Katalog jeszcze nie istnieje — zostanie utworzony.':
        'Папка ещё не существует — она будет создана.',
    'Katalog kopii nie istnieje: {path}':
        'Папка копии не существует: {path}',
    'Katalog źródłowy nie istnieje: {path}':
        'Исходная папка не существует: {path}',
    'Katalog, w którym pojawią się odtworzone pliki.':
        'Папка, в которой появятся восстановленные файлы.',
    'Katalog, w którym powstanie kopia. Nie może leżeć wewnątrz folderu źródłowego.':
        'Папка, в которой будет создана копия. Она не может находиться внутри исходной папки.',
    'Katalogi objęte kopią.\nMożesz przeciągnąć foldery z Eksploratora Windows wprost na tę listę.':
        'Папки, включённые в копию.\nПапки можно перетащить из Проводника Windows прямо в этот список.',
    'Każdy folder z datą jest kompletny — przywracanie nie wymaga sklejania wersji.':
        'Каждая папка с датой полная — для восстановления не нужно склеивать версии.',
    'Każdy plik jest czytany ponownie zaraz po zapisaniu. Dane pochodzą wtedy\nzwykle z pamięci podręcznej systemu, więc niewiele mówi to o nośniku,\na wydłuża kopię nawet dwukrotnie.\n\nSkuteczniejsza jest weryfikacja odroczona: ekran „Przywracanie” →\n„Sprawdź kopię”, najlepiej po ponownym podłączeniu dysku.':
        'Каждый файл перечитывается сразу после записи. Данные при этом обычно\nберутся из системного кэша, поэтому о носителе это говорит мало,\nа копирование может стать вдвое дольше.\n\nЭффективнее отложенная проверка: экран «Восстановление» →\n«Проверить копию», лучше всего после повторного подключения диска.',
    'Każdy plik trafia do kopii jako zaszyfrowany kontener .cvlt.\nKlucz powstaje z hasła przez Argon2id.':
        'Каждый файл попадает в копию как зашифрованный контейнер .cvlt.\nКлюч получается из пароля с помощью Argon2id.',
    'Każdy przebieg tworzy osobny folder z datą i godziną.\nPliki niezmienione są podpinane twardym dowiązaniem, więc historia\nzajmuje tyle miejsca, ile realnie się zmieniło.':
        'Каждый запуск создаёт отдельную папку с датой и временем.\nНеизменённые файлы связываются жёсткими ссылками, поэтому история\nзанимает ровно столько места, сколько реально изменилось.',
    'Klaster nośnika to {cluster} — pliki zajmą {actual} zamiast {logical} (narzut {overhead}).':
        'Кластер носителя — {cluster}: файлы займут {actual} вместо {logical} (накладные расходы — {overhead}).',
    'Kliknij szablon, aby zobaczyć jego szczegóły.':
        'Нажмите на шаблон, чтобы увидеть подробности.',
    'Kliknij „Podgląd zmian”, aby sprawdzić plan bez zapisywania czegokolwiek.':
        'Нажмите «Предпросмотр изменений», чтобы проверить план, ничего не записывая.',
    'Kolor wyróżnienia':
        'Цвет акцента',
    'Kolor wyróżnienia…':
        'Цвет акцента…',
    'Kopia':
        'Резервная копия',
    'Kopia do dokończenia':
        'Незавершённая копия',
    'Kopia jest aktualna — nie ma czego zapisywać.':
        'Копия актуальна — записывать нечего.',
    'Kopia jest zaszyfrowana — podaj hasło użyte przy jej tworzeniu.':
        'Копия зашифрована — введите пароль, указанный при её создании.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją przywrócić.':
        'Копия зашифрована — введите пароль, чтобы восстановить её.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją zweryfikować.':
        'Копия зашифрована — введите пароль, чтобы проверить её.',
    'Kopia jest zaszyfrowana — podaj hasło.':
        'Копия зашифрована — введите пароль.',
    'Kopia lustrzana':
        'Зеркальная копия',
    'Kopia nie została uruchomiona.':
        'Копирование не запущено.',
    'Kopia wykonana. Uruchom podgląd ponownie, aby sprawdzić stan.':
        'Копирование выполнено. Запустите предпросмотр снова, чтобы проверить состояние.',
    'Kopia zapasowa':
        'Резервное копирование',
    'Kopia {folder}':
        'Копия {folder}',
    'Kopia {kind} • {count} {files} • {size} • ostatnia aktualizacja {when}\nŹródła: {roots}':
        'Копия {kind} • {count} {files} • {size} • последнее обновление {when}\nИсточники: {roots}',
    'Kopiowane są wyłącznie pliki nowe i zmienione od ostatniego przebiegu.':
        'Копируются только новые файлы и файлы, изменённые с последнего запуска.',
    'Kopiuje ustawienia szablonu na ekran „Kopia zapasowa”':
        'Переносит настройки шаблона на экран «Резервное копирование»',
    'Kopię możesz sprawdzić później: ekran „Przywracanie” → „Sprawdź kopię”. Najlepiej po ponownym podłączeniu dysku — wtedy dane są czytane z nośnika.':
        'Копию можно проверить позже: экран «Восстановление» → «Проверить копию». Лучше всего после повторного подключения диска — тогда данные действительно читаются с носителя.',
    'Kryptografia':
        'Криптография',
    'Lista podpowiadana przy tworzeniu nowej kopii.':
        'Список, предлагаемый при настройке новой копии.',
    'Magazyn haseł: {backend}':
        'Хранилище паролей: {backend}',
    'Magazyn systemowy: {backend}':
        'Системное хранилище: {backend}',
    'Menedżer poświadczeń Windows (DPAPI, powiązany z kontem użytkownika).':
        'Диспетчер учётных данных Windows (DPAPI, привязан к учётной записи пользователя).',
    'Miejsce i układ odtwarzanych plików.':
        'Куда и в каком виде восстанавливаются файлы.',
    'Motyw zmieniony na {theme}.':
        'Выбрана {theme} тема.',
    'Motyw:':
        'Тема:',
    'Możesz też przeciągnąć foldery z Eksploratora Windows wprost na listę.':
        'Папки также можно перетащить из Проводника Windows прямо в список.',
    'Można ją dokończyć — zostaną dograne tylko brakujące i zmienione pliki.':
        'Её можно завершить — будут дописаны только недостающие и изменённые файлы.',
    'Na nośniku docelowym zajmie to ok. {size}.':
        'На целевом носителе это займёт около {size}.',
    'Nadpisywanie plików':
        'Перезапись файлов',
    'Nadpisz istniejące pliki':
        'Перезаписать существующие файлы',
    'Nazwa szablonu':
        'Имя шаблона',
    'Nazwa szablonu nie może być pusta.':
        'Имя шаблона не может быть пустым.',
    'Nazwa szablonu zapisana.':
        'Имя шаблона сохранено.',
    'Nazwa szablonu:':
        'Имя шаблона:',
    'Nie ma wersji kopii o nazwie {name} w katalogu {path}.':
        'В папке {path} нет версии копии с именем {name}.',
    'Nie można odczytać informacji o dysku: {error}':
        'Не удалось прочитать сведения о диске: {error}',
    'Nie udało się uruchomić programu — brakuje biblioteki: {error}\nZainstaluj zależności poleceniem:  pip install -r requirements.txt':
        'Не удалось запустить программу — отсутствует библиотека: {error}\nУстановите зависимости командой:  pip install -r requirements.txt',
    'Nie udało się wykonać operacji':
        'Не удалось выполнить операцию',
    'Nie udało się zapisać hasła w magazynie systemowym.\nSzablon działa normalnie — program poprosi o hasło przy uruchomieniu.':
        'Не удалось сохранить пароль в системном хранилище.\nШаблон работает как обычно — программа запросит пароль при запуске.',
    'Nie udało się znaleźć wolnej nazwy dla {path}':
        'Не удалось подобрать свободное имя для {path}',
    'Nie wskazano katalogu docelowego.':
        'Целевая папка не указана.',
    'Nie wskazano żadnego katalogu źródłowego.':
        'Не указано ни одной исходной папки.',
    'Nie wybrano katalogu':
        'Папка не выбрана',
    'Nie wybrano szablonu':
        'Шаблон не выбран',
    'Nie znaleziono spisu treści kopii — program przeskanuje folder i rozpozna pliki po ich zawartości.':
        'Оглавление копии не найдено — программа просканирует папку и распознает файлы по их содержимому.',
    'Nie znam oryginalnej lokalizacji dla {key} — wybierz inny układ przywracania.':
        'Исходное место для {key} неизвестно — выберите другой вариант расположения файлов.',
    'Niedostępny — backend {backend} nie gwarantuje poufności.':
        'Недоступно — бэкенд {backend} не гарантирует конфиденциальность.',
    'Niedostępny — brak biblioteki keyring.':
        'Недоступно — нет библиотеки keyring.',
    'Nieznany algorytm wyprowadzania klucza: {name}':
        'Неизвестный алгоритм формирования ключа: {name}',
    'Nowa wersja z datą':
        'Новая датированная версия',
    'Nowa wersja z datą to kopia od początku do osobnego folderu':
        'Новая датированная версия — это копирование с нуля в отдельную папку',
    'Nowa wersja z datą — kopia do nowego folderu.\nWybrana istniejąca wersja — dogrywa do niej tylko brakujące i zmienione\npliki, a pliki różniące się od źródła nadpisuje. Tak dokończysz przerwaną\nkopię albo uzupełnisz ją o dane, które powstały w trakcie jej wykonywania.':
        'Новая датированная версия — копирование в новую папку.\nВыбранная существующая версия — в неё дописываются только недостающие и изменённые\nфайлы, а файлы, отличающиеся от источника, перезаписываются. Так можно завершить прерванное\nкопирование или дополнить копию данными, появившимися во время её создания.',
    'Nowy szablon':
        'Новый шаблон',
    'Nośnik docelowy ({filesystem}) nie obsługuje twardych dowiązań, więc każda wersja z datą jest pełną kopią. Te {count} niezmienionych plików zostanie powielone ({size}). Rozważ układ „kopia lustrzana” albo nośnik NTFS.':
        'Целевой носитель ({filesystem}) не поддерживает жёсткие ссылки, поэтому каждая датированная версия — это полная копия. Неизменённые файлы будут продублированы: {count} ({size}). Рассмотрите структуру «зеркальная копия» или носитель NTFS.',
    'O programie':
        'О программе',
    'Obsługiwane są wzorce w stylu Windows:\n  *.tmp          — wszystkie pliki tymczasowe\n  Thumbs.db      — konkretna nazwa\n  node_modules/* — cały folder wraz z zawartością':
        'Поддерживаются маски в стиле Windows:\n  *.tmp          — все временные файлы\n  Thumbs.db      — конкретное имя\n  node_modules/* — вся папка вместе с содержимым',
    'Ochrona danych':
        'Защита данных',
    'Odczytuje wszystkie pliki kopii i weryfikuje ich poprawność.\nNic nie zapisuje na dysku.':
        'Читает все файлы копии и проверяет их целостность.\nНичего не записывает на диск.',
    'Odpowiednik synchronizacji folderu. Wcześniejsze wersje plików nie są zachowywane.':
        'Аналог синхронизации папки. Предыдущие версии файлов не сохраняются.',
    'Odtwarza pliki z kopii — również z kopii zaszyfrowanej.':
        'Восстанавливает файлы из копии — в том числе из зашифрованной.',
    'Odtwarza pliki zgodnie z ustawieniami powyżej':
        'Восстанавливает файлы согласно настройкам выше',
    'Odtwórz pełną strukturę folderów':
        'Воссоздать полную структуру папок',
    'Odtwórz pliki z istniejącej kopii':
        'Восстановить файлы из существующей копии',
    'Operacja nie powiodła się.':
        'Операция не удалась.',
    'Operacja przerwana przez użytkownika.':
        'Операция прервана пользователем.',
    'Operacja przerwana — utrwalam stan dotychczas zapisanych plików.':
        'Операция прервана — сохраняется состояние уже записанных файлов.',
    'Operacja w toku':
        'Операция выполняется',
    'Operacja zakończona błędem.':
        'Операция завершилась ошибкой.',
    'Ostatnie operacje':
        'Последние операции',
    'Otwiera ekran przywracania z wypełnionymi ścieżkami':
        'Открывает экран восстановления с заполненными путями',
    'Otwiera pełny dziennik w domyślnym edytorze':
        'Открывает полный журнал в редакторе по умолчанию',
    'Otwórz katalog danych':
        'Открыть папку данных',
    'Otwórz katalog dziennika':
        'Открыть папку журнала',
    'Otwórz okno wyboru katalogu':
        'Открыть окно выбора папки',
    'Otwórz plik dziennika':
        'Открыть файл журнала',
    'PBKDF2-HMAC-SHA256 ({count} iteracji)':
        'PBKDF2-HMAC-SHA256 (итераций: {count})',
    'PBKDF2-HMAC-SHA256 — {count} iteracji':
        'PBKDF2-HMAC-SHA256 — итераций: {count}',
    'PBKDF2-HMAC-SHA256, {count} iteracji':
        'PBKDF2-HMAC-SHA256, итераций: {count}',
    'Pełna struktura — układ jak w źródle, wewnątrz wskazanego katalogu.\nJeden folder — wygodne, gdy szukasz kilku plików.\nPierwotne lokalizacje — zapisuje pliki tam, skąd zostały pobrane.':
        'Полная структура — как в источнике, внутри указанной папки.\nОдна папка — удобно, если нужно найти несколько файлов.\nИсходные места — файлы записываются туда, откуда были взяты.',
    'Pierwszy przebieg kopiuje wszystko i trwa najdłużej. Kolejne porównują rozmiar i datę modyfikacji, więc zwykle kończą się w kilka sekund.':
        'Первый запуск копирует всё и длится дольше всего. Следующие сравнивают размер и дату изменения, поэтому обычно укладываются в несколько секунд.',
    'Plan gotowy: {count} {files} do zapisania.':
        'План готов: к записи {count} {files}.',
    'Plik jest za krótki, by być kontenerem tego programu.':
        'Файл слишком короткий для контейнера этой программы.',
    'Plik skończył się wcześniej, niż deklaruje nagłówek.':
        'Файл закончился раньше, чем указано в заголовке.',
    'Plik w formacie w wersji {found}; ta wersja programu obsługuje {supported}.':
        'Файл в формате версии {found}; эта версия программы поддерживает {supported}.',
    'Plik wymaga Argon2id, a biblioteka argon2-cffi jest niedostępna.':
        'Файлу нужен Argon2id, но библиотека argon2-cffi недоступна.',
    'Pliki pominięte — kopia jest aktualna':
        'Пропускаемые файлы — в копии они уже актуальны',
    'Pliki trafią do wskazanego katalogu z zachowaniem struktury folderów.':
        'Файлы попадут в указанную папку с сохранением структуры папок.',
    'Pliki wrócą dokładnie tam, skąd pochodzą. Katalog docelowy zostanie zignorowany.':
        'Файлы вернутся точно туда, откуда были взяты. Целевая папка будет проигнорирована.',
    'Pliki zmienione od ostatniego przebiegu':
        'Файлы, изменённые с последнего запуска',
    'Pliki zostaną zapisane dokładnie tam, skąd pochodzą.\n\nKonflikty nazw: {collision}.\n\nCzy kontynuować?':
        'Файлы будут записаны точно туда, откуда были взяты.\n\nКонфликты имён: {collision}.\n\nПродолжить?',
    'Pliki, których jeszcze nie ma w kopii':
        'Файлы, которых ещё нет в копии',
    'Po uzupełnieniu istniejącej wersji jej katalog nazywa się np.\n  2026-09-17_@687--2026-09-24_@921\nczyli: data utworzenia kopii i data ostatniego uzupełnienia.\n\nData utworzenia zostaje z przodu, więc katalogi nadal układają się\nchronologicznie. Widać to w Eksploratorze bez uruchamiania programu.':
        'После дополнения существующей версии её папка называется, например,\n  2026-09-17_@687--2026-09-24_@921\nто есть: дата создания копии и дата последнего дополнения.\n\nДата создания остаётся в начале, поэтому папки по-прежнему сортируются\nв хронологическом порядке. Это видно в Проводнике без запуска программы.',
    'Po wykonaniu kopii zostanie mało wolnego miejsca ({free}).':
        'После копирования останется мало свободного места ({free}).',
    'Po zakończeniu kopii program ponownie skanuje źródło i dogrywa do tej samej\nwersji pliki, które w międzyczasie powstały lub się zmieniły.\nPrzydatne, gdy pracujesz na danych w trakcie wielogodzinnej kopii.\nPlik zmieniony w trakcie własnego kopiowania nigdy nie jest uznawany za zapisany.':
        'После завершения копирования программа снова сканирует источник и дописывает в ту же\nверсию файлы, которые за это время появились или изменились.\nПолезно, если вы работаете с данными во время многочасового копирования.\nФайл, изменённый во время собственного копирования, никогда не считается записанным.',
    'Poczekaj na zakończenie bieżącej operacji.':
        'Дождитесь завершения текущей операции.',
    'Podaj hasło dla szablonu „{name}”:':
        'Введите пароль для шаблона «{name}»:',
    'Podaj hasło — bez niego nie można zaszyfrować kopii.':
        'Введите пароль — без него зашифровать копию невозможно.',
    'Podane hasło nie pasuje do plików zapisanych wcześniej w tej kopii. Wznowienie z innym hasłem zostawiłoby w jednej kopii pliki pod dwoma hasłami. Podaj hasło użyte przy poprzednim przebiegu albo utwórz kopię w nowym katalogu.':
        'Введённый пароль не подходит к файлам, ранее записанным в эту копию. Если продолжить с другим паролем, в одной копии окажутся файлы под двумя паролями. Введите пароль, использованный при предыдущем запуске, или создайте копию в новой папке.',
    'Podgląd zmian':
        'Предпросмотр изменений',
    'Pokazuje folder z plikami dziennika':
        'Показывает папку с файлами журнала',
    'Pokazuje folder z ustawieniami i szablonami':
        'Показывает папку с настройками и шаблонами',
    'Pokaż / ukryj wpisane hasło':
        'Показать / скрыть введённый пароль',
    'Pomiń istniejące pliki':
        'Пропустить существующие файлы',
    'Potwierdź usuwanie':
        'Подтвердите удаление',
    'Powtórz hasło':
        'Повторите пароль',
    'Program nie mógł się uruchomić:\n\n{error}\n\nSzczegóły zapisano w dzienniku aplikacji.':
        'Программа не смогла запуститься:\n\n{error}\n\nПодробности записаны в журнал приложения.',
    'Program nie wie, czy ta kopia została dokończona. Uzupełnienie jej dogra tylko brakujące i zmienione pliki, a tego, co już jest zapisane, nie kopiuje ponownie.':
        'Программа не знает, была ли эта копия завершена. Дополнение допишет только недостающие и изменённые файлы, а уже записанное повторно копировать не будет.',
    'Program sam wykryje, czy kopia jest zaszyfrowana.':
        'Программа сама определит, зашифрована ли копия.',
    'Przebieg operacji i diagnostyka':
        'Ход операций и диагностика',
    'Przebieg operacji na żywo. Pełna historia trafia do pliku.':
        'Ход операции в реальном времени. Полная история записывается в файл.',
    'Przebieg uzupełniający: {error}':
        'Проход дозаписи: {error}',
    'Przeciętne':
        'Средний',
    'Przerwano liczenie sumy kontrolnej.':
        'Вычисление контрольной суммы прервано.',
    'Przerwano skanowanie.':
        'Сканирование прервано.',
    'Przerwano. Zapisano {count} {files} ({size}).':
        'Прервано. Записано: {count} {files} ({size}).',
    'Przerwij':
        'Прервать',
    'Przerywanie operacji…':
        'Прерывание операции…',
    'Przerywanie — zapisuję spis treści kopii, nie wyłączaj komputera…':
        'Прерывание — записывается оглавление копии, не выключайте компьютер…',
    'Przeskanowano {count} {files}.':
        'Просканировано: {count} {files}.',
    'Przygotowanie…':
        'Подготовка…',
    'Przywracanie':
        'Восстановление',
    'Przywracanie do pierwotnych lokalizacji':
        'Восстановление в исходные места',
    'Przywracanie przerwane.':
        'Восстановление прервано.',
    'Przywracanie {count} {files} ({size})…':
        'Восстановление {count} {files} ({size})…',
    'Przywróć do pierwotnych lokalizacji':
        'Восстановить в исходные места',
    'Przywróć domyślne':
        'Вернуть стандартные',
    'Przywróć fabryczne':
        'Вернуть заводские',
    'Przywróć pliki':
        'Восстановить файлы',
    'Przywróć z tej kopii':
        'Восстановить из этой копии',
    'Pusta nazwa':
        'Пустое имя',
    'Równoległe operacje:':
        'Параллельные операции:',
    'Skanowanie plików źródłowych…':
        'Сканирование исходных файлов…',
    'Skrót z dziennika — pełny zapis znajdziesz w zakładce „Dziennik”.':
        'Краткая выдержка из журнала — полная запись на вкладке «Журнал».',
    'Skąd przywracamy':
        'Откуда восстанавливаем',
    'Sprawdzam, co zmieniło się w źródle w trakcie kopii (przebieg uzupełniający {attempt} z {passes})…':
        'Проверка изменений в источнике за время копирования (проход дозаписи {attempt} из {passes})…',
    'Sprawdzam, czy hasło zgadza się z hasłem wcześniej zapisanych plików…':
        'Проверка, совпадает ли пароль с паролем ранее записанных файлов…',
    'Sprawdzam, czy w katalogu docelowym jest kopia do dokończenia…':
        'Проверка, есть ли в целевой папке незавершённая копия…',
    'Sprawdź hasło':
        'Проверьте пароль',
    'Sprawdź kopię':
        'Проверить копию',
    'Szablon przechowuje foldery, opcje i wykluczenia. Hasło nigdy nie trafia do szablonu — jest przechowywane w Menedżerze poświadczeń Windows albo wpisywane przy każdym uruchomieniu.':
        'Шаблон хранит папки, параметры и исключения. Пароль никогда не попадает в шаблон — он хранится в Диспетчере учётных данных Windows или вводится при каждом запуске.',
    'Szablon usunięty.':
        'Шаблон удалён.',
    'Szablon „{name}”':
        'Шаблон «{name}»',
    'Szablon „{name}” już istnieje.\n\nZastąpić go bieżącymi ustawieniami z formularza?':
        'Шаблон «{name}» уже существует.\n\nЗаменить его текущими настройками из формы?',
    'Szablon „{name}” zostanie usunięty.\n\nPliki kopii zapasowej pozostaną nienaruszone.':
        'Шаблон «{name}» будет удалён.\n\nФайлы резервной копии останутся нетронутыми.',
    'Szablony':
        'Шаблоны',
    'Szablony: {count}\nSzyfrowanie: AES-256-GCM\nKlucz: {kdf}':
        'Шаблонов: {count}\nШифрование: AES-256-GCM\nКлюч: {kdf}',
    'Szyfrowanie i kontrola poprawności zapisu.':
        'Шифрование и контроль правильности записи.',
    'Szyfrowanie: AES-256-GCM (uwierzytelnione)\nWyprowadzanie klucza: {kdf}':
        'Шифрование: AES-256-GCM (аутентифицированное)\nФормирование ключа: {kdf}',
    'Szyfruj kopię (AES-256-GCM)':
        'Шифровать копию (AES-256-GCM)',
    'Słabe':
        'Слабый',
    'Ta kopia nie jest zaszyfrowana — hasło nie jest potrzebne.':
        'Эта копия не зашифрована — пароль не нужен.',
    'Ten folder jest już na liście.':
        'Эта папка уже есть в списке.',
    'To nie jest plik zaszyfrowany przez ten program.':
        'Это не файл, зашифрованный этой программой.',
    'Trwa inna operacja — poczekaj na jej zakończenie.':
        'Выполняется другая операция — дождитесь её завершения.',
    'Trwa operacja':
        'Выполняется операция',
    'Trwa operacja na plikach. Zamknięcie programu ją przerwie.\n\nPliki zapisane do tej chwili zostaną zachowane, a kopię będzie można później dokończyć.\n\nZamknąć mimo to?':
        'Выполняется операция с файлами. Закрытие программы прервёт её.\n\nФайлы, записанные к этому моменту, сохранятся, а копирование можно будет завершить позже.\n\nВсё равно закрыть?',
    'Trwa: {description}…':
        'Выполняется: {description}…',
    'Tryb dokładny — licz sumę kontrolną każdego pliku':
        'Тщательный режим — вычислять контрольную сумму каждого файла',
    'Układ kopii':
        'Структура копии',
    'Układ plików:':
        'Расположение файлов:',
    'Uruchom kopię':
        'Запустить копирование',
    'Ustawienia':
        'Настройки',
    'Usunąć szablon?':
        'Удалить шаблон?',
    'Usuwa pozycję z listy. Nie kasuje żadnych plików.':
        'Убирает элемент из списка. Никакие файлы не удаляются.',
    'Usuwa szablon. Nie kasuje żadnych plików kopii.':
        'Удаляет шаблон. Файлы копии не удаляются.',
    'Usuwaj z kopii pliki skasowane w źródle':
        'Удалять из копии файлы, удалённые в источнике',
    'Usuń':
        'Удалить',
    'Usuń zaznaczone':
        'Убрать выбранные',
    'Uszkodzony nagłówek pliku.':
        'Заголовок файла повреждён.',
    'Utwórz lub zaktualizuj kopię wybranych folderów':
        'Создать или обновить копию выбранных папок',
    'Utwórz nową wersję':
        'Создать новую версию',
    'Uzupełnienie istniejącej wersji nie kopiuje ponownie tego, co już w niej jest — dokończysz przerwaną kopię bez tworzenia kolejnej pełnej wersji.':
        'Дополнение существующей версии не копирует повторно то, что в ней уже есть, — так можно завершить прерванное копирование, не создавая ещё одну полную версию.',
    'Uzupełnij tę wersję':
        'Дополнить эту версию',
    'Uzupełnij: {version} • {labels}':
        'Дополнить: {version} • {labels}',
    'W katalogu docelowym jest kopia tych samych folderów zapisana starszą wersją programu:':
        'В целевой папке есть копия тех же папок, записанная более старой версией программы:',
    'W katalogu docelowym jest niedokończona kopia tych samych folderów:':
        'В целевой папке есть незавершённая копия тех же папок:',
    'W tym katalogu nie ma spisu treści kopii — nie ma z czym porównać plików.':
        'В этой папке нет оглавления копии — файлы не с чем сравнить.',
    'Wczytaj do formularza':
        'Загрузить в форму',
    'Wczytano manifest kopii: {count} {files}.':
        'Манифест копии загружен: {count} {files}.',
    'Wczytano szablon „{name}” do formularza.':
        'Шаблон «{name}» загружен в форму.',
    'Wersja kopii nosi teraz nazwę {name}.':
        'Версия копии теперь называется {name}.',
    'Wersja, licencja i użyta kryptografia':
        'Версия, лицензия и используемая криптография',
    'Wersje z datą (zalecane)':
        'Датированные версии (рекомендуется)',
    'Weryfikacja kopii':
        'Проверка копии',
    'Weryfikacja nie powiodła się: nieprawidłowe hasło lub uszkodzony plik.':
        'Проверка не пройдена: неверный пароль или повреждённый файл.',
    'Weryfikacja po zapisie nie powiodła się — zapisane dane różnią się od źródła.':
        'Проверка после записи не пройдена — записанные данные отличаются от источника.',
    'Weryfikacja {count} {files} ({size}), {threads} równolegle…':
        'Проверка {count} {files} ({size}), параллельно: {threads}…',
    'Weryfikuj natychmiast po zapisie (spowalnia kopię)':
        'Проверять сразу после записи (замедляет копирование)',
    'Wolne miejsce: {free} z {total}':
        'Свободно: {free} из {total}',
    'Wolniejszy, ale wykrywa zmiany, które nie zmieniły rozmiaru ani daty\n(np. po przywróceniu pliku z innego nośnika).':
        'Медленнее, но замечает изменения, при которых не изменились ни размер, ни дата\n(например, после восстановления файла с другого носителя).',
    'Wpis {key} w spisie treści kopii wskazuje poza katalog docelowy — pomijam go.':
        'Запись {key} в оглавлении копии указывает за пределы целевой папки — она пропускается.',
    'Wraca do listy wbudowanej w program':
        'Возвращает список, встроенный в программу',
    'Wskaż folder kopii, aby zobaczyć jej zawartość.':
        'Укажите папку копии, чтобы увидеть её содержимое.',
    'Wskaż folder kopii.':
        'Укажите папку копии.',
    'Wskaż foldery objęte kopią. Podfoldery są uwzględniane automatycznie.':
        'Укажите папки для копирования. Вложенные папки включаются автоматически.',
    'Wskaż główny folder kopii (ten, który wybrałeś jako cel), a nie pojedynczy folder z datą. Program sam odczyta spis treści kopii.':
        'Укажите главную папку копии (ту, которую вы выбрали как целевую), а не отдельную папку с датой. Программа сама прочитает оглавление копии.',
    'Wskaż katalog docelowy kopii.':
        'Укажите целевую папку копии.',
    'Wskaż katalog docelowy.':
        'Укажите целевую папку.',
    'Wstawia zalecaną listę wykluczeń':
        'Вставляет рекомендуемый список исключений',
    'Wszystkie pliki wylądują bezpośrednio w katalogu docelowym, bez podfolderów.':
        'Все файлы окажутся прямо в целевой папке, без вложенных папок.',
    'Wszystko do jednego folderu':
        'Всё в одну папку',
    'Wybierz folder do kopii':
        'Выберите папку для копирования',
    'Wybierz folder kopii':
        'Выберите папку копии',
    'Wybierz katalog':
        'Выберите папку',
    'Wybierz katalog docelowy':
        'Выберите целевую папку',
    'Wybierz katalog docelowy kopii':
        'Выберите целевую папку копии',
    'Wybierz katalog, aby zobaczyć dostępne miejsce.':
        'Выберите папку, чтобы увидеть доступное место.',
    'Wybierz kolejny folder do kopii':
        'Выбрать ещё одну папку для копирования',
    'Wybierz szablon z listy.':
        'Выберите шаблон в списке.',
    'Wybierz…':
        'Выбрать…',
    'Wybrano nadpisywanie istniejących plików. Ich obecna zawartość zostanie bezpowrotnie zastąpiona.\n\nCzy kontynuować?':
        'Выбрана перезапись существующих файлов. Их текущее содержимое будет безвозвратно заменено.\n\nПродолжить?',
    'Wyczyść widok':
        'Очистить окно',
    'Wygląd':
        'Внешний вид',
    'Wygląd, wykluczenia domyślne i informacje o środowisku.':
        'Внешний вид, исключения по умолчанию и сведения о среде.',
    'Wygląd, wykluczenia i magazyn haseł':
        'Внешний вид, исключения и хранилище паролей',
    'Wykluczenia':
        'Исключения',
    'Wykonuje kopię według tego szablonu':
        'Выполняет копирование по этому шаблону',
    'Wykonuje kopię zgodnie z powyższymi ustawieniami':
        'Выполняет копирование с настройками выше',
    'Wymagane wyłącznie dla kopii zaszyfrowanych.':
        'Требуется только для зашифрованных копий.',
    'Wzorce plików i folderów pomijanych w kopii — po jednym w wierszu.':
        'Маски файлов и папок, которые не попадают в копию, — по одной в строке.',
    'Włączono szyfrowanie, ale nie podano hasła.':
        'Шифрование включено, но пароль не указан.',
    'Włączono usuwanie z kopii plików skasowanych w źródle.\n\nPliki usunięte w źródle stracą swoją jedyną kopię zapasową. Czy na pewno kontynuować?':
        'Включено удаление из копии файлов, удалённых в источнике.\n\nФайлы, удалённые в источнике, потеряют свою единственную резервную копию. Вы уверены, что хотите продолжить?',
    'Za mało miejsca w katalogu docelowym. Potrzeba ok. {needed}, dostępne {free}.':
        'Недостаточно места в целевой папке. Нужно около {needed}, доступно {free}.',
    'Zabezpieczenie przed literówką — hasła nie da się odzyskać.':
        'Защита от опечатки — пароль невозможно восстановить.',
    'Zachowaj oba — dopisz numer do nazwy':
        'Сохранить оба — добавить номер к имени',
    'Zakończono z błędami ({errors}). Zapisano {count} {files}.':
        'Завершено с ошибками ({errors}). Записано: {count} {files}.',
    'Zakończono.':
        'Завершено.',
    'Zapamiętaj hasło w Menedżerze poświadczeń Windows':
        'Запомнить пароль в Диспетчере учётных данных Windows',
    'Zapamiętuje te ustawienia do ponownego użycia':
        'Запоминает эти настройки для повторного использования',
    'Zapis bieżącej sesji':
        'Запись текущего сеанса',
    'Zapisane konfiguracje do ponownego użycia':
        'Сохранённые конфигурации для повторного использования',
    'Zapisane konfiguracje — uruchamiasz je jednym kliknięciem.':
        'Сохранённые конфигурации — запускаются одним щелчком.',
    'Zapisane szablony':
        'Сохранённые шаблоны',
    'Zapisano szablon „{name}”.':
        'Шаблон «{name}» сохранён.',
    'Zapisuje listę jako domyślną':
        'Сохраняет список как список по умолчанию',
    'Zapisuje nową nazwę szablonu':
        'Сохраняет новое имя шаблона',
    'Zapisywanie {count} {files} ({size}), {workers} równolegle':
        'Запись {count} {files} ({size}), параллельно: {workers}',
    'Zapisz':
        'Сохранить',
    'Zapisz do:':
        'Записать в:',
    'Zapisz jako szablon':
        'Сохранить как шаблон',
    'Zapisz nazwę':
        'Сохранить имя',
    'Zapisz szablon':
        'Сохранить шаблон',
    'Zastąpić szablon?':
        'Заменить шаблон?',
    'Zatrzymuje operację. Pliki już zapisane pozostają nienaruszone.':
        'Останавливает операцию. Уже записанные файлы остаются нетронутыми.',
    'Zaznacz szablon na liście.':
        'Выделите шаблон в списке.',
    'Zmiana języka przebudowuje okno; wypełnione ścieżki zostają.':
        'Смена языка перестраивает окно; заполненные пути сохраняются.',
    'Zmiana motywu działa natychmiast.':
        'Смена темы применяется сразу.',
    'Zmienia kolor przycisków i zaznaczeń':
        'Меняет цвет кнопок и выделения',
    'Zmień nazwę, aby łatwiej rozpoznawać szablon.':
        'Переименуйте шаблон, чтобы его было легче узнать.',
    'Znaleziono {count} {files}. Porównuję z poprzednią kopią…':
        'Найдено: {count} {files}. Сравнение с предыдущей копией…',
    'automatycznie':
        'автоматически',
    'bez zmian':
        'без изменений',
    'brak (biblioteka keyring niezainstalowana)':
        'нет (библиотека keyring не установлена)',
    'brak danych':
        'нет данных',
    'brak pliku w kopii':
        'файла нет в копии',
    'do zapisania':
        'к записи',
    'istniejąca kopia: {count} {files}, ostatnio {when}':
        'существующая копия: {count} {files}, последний раз {when}',
    'jeszcze nie uruchamiany':
        'ещё не запускался',
    'kompletna':
        'завершена',
    'kopia lustrzana':
        'зеркальная копия',
    'kopia zapasowa':
        'резервное копирование',
    'nie':
        'нет',
    'niedokończona':
        'не завершена',
    'niedokończona — brakuje ok. {count} {files} ({size})':
        'не завершена — не хватает около {count} {files} ({size})',
    'niezaszyfrowana':
        'не зашифрована',
    'nieznany format manifestu':
        'неизвестный формат манифеста',
    'nowych plików':
        'новые файлы',
    'np. C:\\Odzyskane':
        'например, C:\\Восстановленные',
    'np. E:\\Kopie zapasowe':
        'например, E:\\Резервные копии',
    'plik':
        'файл',
    'plik stanu jest za krótki':
        'файл состояния слишком короткий',
    'plik stanu w wersji {found}, obsługiwana: {supported}':
        'файл состояния версии {found}, поддерживается: {supported}',
    'pliki':
        'файла',
    'plików':
        'файлов',
    'podgląd kopii':
        'предпросмотр копии',
    'pozostaną w kopii':
        'останутся в копии',
    'rozmiar w kopii {actual} B zamiast {expected} B':
        'размер в копии {actual} B вместо {expected} B',
    'sprawdzanie kopii':
        'проверка копии',
    'stan nieznany (zapisana starszą wersją programu)':
        'состояние неизвестно (записана более старой версией программы)',
    'suma kontrolna manifestu się nie zgadza':
        'контрольная сумма манифеста не совпадает',
    'suma kontrolna się nie zgadza — plik uszkodzony':
        'контрольная сумма не совпадает — файл повреждён',
    'szablon {name}':
        'шаблон {name}',
    'tak':
        'да',
    'ten system plików':
        'эта файловая система',
    'wersja {version}':
        'версия {version}',
    'wersje z datą':
        'датированные версии',
    'weryfikacja':
        'проверка',
    'wyłączona':
        'выключена',
    'zaszyfrowana (AES-256-GCM)':
        'зашифрована (AES-256-GCM)',
    'zawartość różni się od pliku źródłowego':
        'содержимое отличается от исходного файла',
    'zawartość różni się od sumy kontrolnej zapisanej podczas kopii':
        'содержимое не совпадает с контрольной суммой, записанной при копировании',
    'zmienionych':
        'изменённые',
    'zostaną usunięte z kopii':
        'будут удалены из копии',
    '{done} z {total} • {speed}/s{eta}':
        '{done} из {total} • {speed}/s{eta}',
    '{done} • {speed}/s':
        '{done} • {speed}/s',
    '{hours} h {minutes} min':
        '{hours} ч {minutes} мин',
    '{label}: {count} {files}':
        '{label}: {count} {files}',
    '{message}\n\nSzczegóły techniczne znajdziesz w zakładce „Dziennik”.':
        '{message}\n\nТехнические подробности — на вкладке «Журнал».',
    '{minutes} min {seconds} s':
        '{minutes} мин {seconds} с',
    '{name}: nie można odczytać ({error})':
        '{name}: не удаётся прочитать ({error})',
    '{seconds} s':
        '{seconds} с',
    '{summary}\n\nProblemy:\n{problems}\n\nPełna lista znajduje się w zakładce „Dziennik”.':
        '{summary}\n\nПроблемы:\n{problems}\n\nПолный список — на вкладке «Журнал».',
    '{summary}{notes}\n\nPliki zapisane przed przerwaniem są kompletne i zostały odnotowane w spisie treści kopii.\n\nAby dokończyć kopię, uruchom ją ponownie — program zaproponuje uzupełnienie tej wersji zamiast tworzenia nowej.':
        '{summary}{notes}\n\nФайлы, сохранённые до прерывания, записаны полностью и внесены в оглавление копии.\n\nЧтобы завершить копирование, запустите его снова — программа предложит дополнить эту версию вместо создания новой.',
    '{title} — gotowe':
        '{title} — готово',
    '{title} — przerwano':
        '{title} — прервано',
    '{title} — zakończono z błędami':
        '{title} — завершено с ошибками',
    '{when}  •  {action}  •  {count} {files}':
        '{when}  •  {action}  •  {count} {files}',
    'Łączny rozmiar danych do przesłania':
        'Общий объём данных для передачи',
    'Środowisko':
        'Среда',
    'Źródła: {sources}\nCel: {destination}\nUkład: {structure} • Szyfrowanie: {encrypt} • Weryfikacja: {verify} • Dogrywka: {catchup} • Równolegle: {workers} • Data uzupełnienia w nazwie: {stamp}\nUtworzony: {created} • Ostatni przebieg: {last}':
        'Источники: {sources}\nНазначение: {destination}\nСтруктура: {structure} • Шифрование: {encrypt} • Проверка: {verify} • Дозапись: {catchup} • Параллельно: {workers} • Дата дополнения в имени: {stamp}\nСоздан: {created} • Последний запуск: {last}',
    'Źródło nie zmieniło się w trakcie kopii — nie ma czego uzupełniać.':
        'Источник не изменился за время копирования — дополнять нечего.',
    '—':
        '—',
    '• Kopia przyrostowa — zapisywane są wyłącznie pliki nowe i zmienione.\n  Porównanie opiera się na spisie treści kopii, rozmiarze i dacie modyfikacji;\n  przy różnicy liczona jest suma kontrolna SHA-256.\n\n• Wersje z datą — każdy przebieg tworzy kompletny folder z datą, a pliki\n  niezmienione są podpinane twardym dowiązaniem, więc nie zajmują miejsca dwa razy.\n\n• Weryfikacja po zapisie — zapisany plik jest odczytywany z powrotem\n  i porównywany ze źródłem.\n\n• Odporność na przerwania — pliki powstają pod nazwą tymczasową i są\n  podmieniane dopiero po pełnym zapisie.':
        '• Инкрементное копирование — записываются только новые и изменённые файлы.\n  Сравнение основано на оглавлении копии, размере и дате изменения;\n  при расхождении вычисляется контрольная сумма SHA-256.\n\n• Датированные версии — каждый запуск создаёт полную папку с датой, а неизменённые\n  файлы связываются жёсткими ссылками, поэтому не занимают место дважды.\n\n• Проверка после записи — записанный файл считывается обратно\n  и сравнивается с источником.\n\n• Устойчивость к прерываниям — файлы создаются под временным именем и\n  заменяют прежние только после полной записи.',
    '• Szyfr: AES-256 w trybie GCM (szyfrowanie z uwierzytelnieniem).\n• Wyprowadzanie klucza z hasła: {kdf}.\n• Nagłówek każdego pliku jest uwierzytelniony jako AAD — podmiana parametrów\n  unieważnia tag.\n• Każdy plik dostaje losowy, niepowtarzalny nonce.\n• Odszyfrowany plik powstaje dopiero po pomyślnej weryfikacji tagu.\n• Hasła nie są zapisywane w plikach programu. Opcjonalnie trafiają do\n  Menedżera poświadczeń Windows.':
        '• Шифр: AES-256 в режиме GCM (аутентифицированное шифрование).\n• Формирование ключа из пароля: {kdf}.\n• Заголовок каждого файла аутентифицируется как AAD — подмена параметров\n  делает тег недействительным.\n• Каждый файл получает случайный уникальный nonce.\n• Расшифрованный файл создаётся только после успешной проверки тега.\n• Пароли не записываются в файлы программы. При желании они сохраняются\n  в Диспетчере учётных данных Windows.',
    'Bez hasła nie da się odczytać ani jednego pliku z kopii.':
        'Без пароля невозможно прочитать ни одного файла из копии.',
    'Co chcesz chronić?':
        'Что вы хотите защитить?',
    'Co chcesz teraz zrobić?':
        'Что вы хотите сделать?',
    'Czyta kopię z nośnika i porównuje ją z zapisanymi sumami kontrolnymi.':
        'Читает копию с носителя и сравнивает её с записанными контрольными суммами.',
    'Dalej':
        'Далее',
    'Dokumenty i zdjęcia':
        'Документы и фото',
    'Ekran powitalny wrócisz w ustawieniach, gdy zmienisz zdanie.':
        'Если передумаете, экран приветствия можно вернуть в настройках.',
    'Ekran z pytaniem, co chcesz teraz zrobić: kopia, przywracanie, sprawdzenie.':
        'Экран с вопросом, что вы хотите сделать: копирование, восстановление, проверка.',
    'Foldery objęte kopią':
        'Папки для копирования',
    'Foldery z pracą. Kreator pominie katalogi, które odtwarza się jednym poleceniem (node_modules, venv, build).':
        'Папки с вашей работой. Мастер пропустит папки, которые воссоздаются одной командой (node_modules, venv, build).',
    'Gdzie zapisać kopię?':
        'Куда сохранить копию?',
    'Historia i szyfrowanie':
        'История и шифрование',
    'Historia zmian (zalecane)':
        'История изменений (рекомендуется)',
    'Jak bardzo chcesz się zabezpieczyć?':
        'Насколько надёжная защита вам нужна?',
    'Jak wyżej, a dodatkowo każdy plik trafia do kopii zaszyfrowany (AES-256-GCM). Potrzebne przy kopii wożonej poza dom.':
        'То же, что выше, но вдобавок каждый файл попадает в копию в зашифрованном виде (AES-256-GCM). Нужно, если диск с копией увозят из дома.',
    'Jedna aktualna kopia':
        'Одна актуальная копия',
    'Język, motyw, domyślne wykluczenia i informacje o środowisku.':
        'Язык, тема, исключения по умолчанию и сведения о среде.',
    'Katalog docelowy leży wewnątrz źródła — wybierz inny.':
        'Целевая папка находится внутри источника — выберите другую.',
    'Każdy przebieg tworzy folder z datą. Pliki niezmienione są podpinane dowiązaniem, więc historia kosztuje tyle, ile realnie się zmieniło.':
        'Каждый запуск создаёт папку с датой. Неизменённые файлы связываются ссылками, поэтому история стоит ровно столько, сколько реально изменилось.',
    'Każdy przebieg utworzy folder z datą. Pierwszy zajmie tyle, ile dane; kolejne — tyle, ile realnie się zmieniło.':
        'Каждый запуск создаст папку с датой. Первая займёт столько же места, сколько сами данные; следующие — столько, сколько реально изменилось.',
    'Kopia powstanie w: {path}':
        'Копия будет создана здесь: {path}',
    'Kopia trafi do: {path}':
        'Копия попадёт сюда: {path}',
    'Kopia: {what}':
        'Копия: {what}',
    'Krok {number} z {total}':
        'Шаг {number} из {total}',
    'Najlepiej na innym dysku fizycznym niż ten, który chronisz — kopia obok oryginału ginie razem z nim.':
        'Лучше всего на другом физическом диске, а не на том, который вы защищаете: копия рядом с оригиналом погибает вместе с ним.',
    'Najszybsza i najmniejsza. Kopia odpowiada temu, co masz teraz — bez historii wcześniejszych wersji.':
        'Самая быстрая и компактная. Копия соответствует тому, что у вас есть сейчас, — без истории прежних версий.',
    'Nie było jeszcze żadnej kopii. Zacznij od „Zrób kopię”.':
        'Копий ещё не было. Начните с «Сделать копию».',
    'Nie lista ustawień, tylko ich skutki.':
        'Не список настроек, а то, к чему они приведут.',
    'Nie pokazuj tego ekranu przy starcie':
        'Не показывать этот экран при запуске',
    'Nośnik docelowy':
        'Целевой носитель',
    'Odtwarza pliki z kopii — całość albo wybrany folder.':
        'Восстанавливает файлы из копии — целиком или выбранную папку.',
    'Odśwież listę':
        'Обновить список',
    'Ostatnia kopia: {when} • {count} {files}.':
        'Последняя копия: {when} • {count} {files}.',
    'Pierwszy przebieg jest najdłuższy — kolejne porównują rozmiar i datę modyfikacji, więc zwykle trwają sekundy.':
        'Первый запуск самый долгий — следующие сравнивают размер и дату изменения, поэтому обычно занимают секунды.',
    'Pliki w kopii będą zaszyfrowane; bez hasła nie da się ich odczytać.':
        'Файлы в копии будут зашифрованы; без пароля их не прочитать.',
    'Podfoldery są uwzględniane automatycznie.':
        'Вложенные папки включаются автоматически.',
    'Pokazuj ekran powitalny przy starcie':
        'Показывать экран приветствия при запуске',
    'Ponownie sprawdza podłączone nośniki':
        'Заново проверяет подключённые носители',
    'Program będzie utrzymywał jeden folder zgodny ze źródłem. Każdy kolejny przebieg dopisze tylko to, co się zmieniło.':
        'Программа будет поддерживать одну папку в соответствии с источником. Каждый следующий запуск допишет только то, что изменилось.',
    'Projekty i kod':
        'Проекты и код',
    'Przechodzi do następnego kroku':
        'Переходит к следующему шагу',
    'Przechodzi do pełnego okna programu':
        'Переходит к полному окну программы',
    'Sam wskażesz, co ma trafić do kopii.':
        'Вы сами укажете, что должно попасть в копию.',
    'System plików: {filesystem}, klaster {cluster}':
        'Файловая система: {filesystem}, кластер {cluster}',
    'Ten katalog leży wewnątrz folderu źródłowego — wybierz inny.':
        'Эта папка находится внутри исходной папки — выберите другую.',
    'Ten nośnik nie obsługuje twardych dowiązań, więc każda wersja z datą zajmie tyle miejsca co pełna kopia. Przy tym nośniku rozważ „jedną aktualną kopię”.':
        'Этот носитель не поддерживает жёсткие ссылки, поэтому каждая датированная версия займёт столько же места, сколько полная копия. Для этого носителя рассмотрите вариант «Одна актуальная копия».',
    'To dysk systemowy — kopia nie przetrwa jego awarii. Jeśli masz drugi dysk albo pendrive, wybierz jego.':
        'Это системный диск — копия не переживёт его поломку. Если у вас есть второй диск или флешка, лучше сохранить копию туда.',
    'To się wydarzy':
        'Что произойдёт',
    'Trzy gotowe zestawy zamiast kilkunastu przełączników.':
        'Три готовых набора вместо десятка переключателей.',
    'Twoje pliki osobiste z folderów użytkownika. Najczęstszy wybór.':
        'Ваши личные файлы из папок пользователя. Самый частый выбор.',
    'Uruchamia kreator, który ustawi kopię krok po kroku':
        'Запускает мастер, который настроит копирование шаг за шагом',
    'Nowa kopia krok po kroku…':
        'Новая копия шаг за шагом…',
    'Ustawia kopię krok po kroku i zapisuje ją jako szablon':
        'Настраивает копирование шаг за шагом и сохраняет его как шаблон',
    'Ustawienia pierwszej kopii':
        'Настройка первой копии',
    'Ustawienia pierwszej kopii…':
        'Настройка первой копии…',
    'W tym katalogu jest już kopia ({count} {files}) — program ją uzupełni, a nie nadpisze.':
        'В этой папке уже есть копия ({count} {files}) — программа дополнит её, а не перезапишет.',
    'Wraca do poprzedniego kroku':
        'Возвращает к предыдущему шагу',
    'Wskaż dowolny katalog docelowy':
        'Указать любую целевую папку',
    'Wskaż folder kopii i kliknij „Sprawdź kopię”.':
        'Укажите папку копии и нажмите «Проверить копию».',
    'Wstecz':
        'Назад',
    'Wybierz':
        'Выбрать',
    'Wybierz inny folder…':
        'Выбрать другую папку…',
    'Wybierz to, co najbliższe. Dokładną listę folderów poprawisz niżej.':
        'Выберите самый близкий вариант. Точный список папок можно поправить ниже.',
    'Wybrane foldery':
        'Выбранные папки',
    'Zamknij':
        'Закрыть',
    'Zamyka kreator bez zapisywania':
        'Закрывает мастер без сохранения',
    'Zapisuje nowe i zmienione pliki. Pierwszy raz trwa najdłużej.':
        'Записывает новые и изменённые файлы. Первый раз занимает больше всего времени.',
    'Zapisuje szablon bez uruchamiania kopii':
        'Сохраняет шаблон, не запуская копирование',
    'Zapisuje szablon i od razu uruchamia kopię':
        'Сохраняет шаблон и сразу запускает копирование',
    'Zapisz i zrób kopię':
        'Сохранить и сделать копию',
    'Zapisz ustawienia':
        'Сохранить настройки',
    'Zrób kopię':
        'Сделать копию',
    'dysk systemowy':
        'системный диск',
    'wolne {free} z {total}':
        'свободно {free} из {total}',
    'Porównano ze źródłem: {source}; tylko z sumą kontrolną (źródło zmieniło się albo jest niedostępne): {checksum}.':
        'Сравнено с источником: {source}; только с контрольной суммой (источник изменился или недоступен): {checksum}.',
    'Przywraca losową próbkę plików do katalogu tymczasowego i porównuje je ze źródłem.\nSprawdza całą drogę odzyskiwania, a trwa minuty. Nic nie zostaje na dysku.':
        'Восстанавливает случайную выборку файлов во временную папку и сравнивает их с источником.\nПроверяет весь путь восстановления и занимает минуты. На диске ничего не остаётся.',
    'Próbne przywrócenie':
        'Пробное восстановление',
    'W kopii nie ma plików, które dałoby się sprawdzić próbnie.':
        'В копии нет файлов, которые можно проверить пробным восстановлением.',
    'przywrócony plik różni się od pliku źródłowego':
        'восстановленный файл отличается от исходного',
    'przywrócony plik różni się od sumy kontrolnej zapisanej podczas kopii':
        'восстановленный файл не совпадает с контрольной суммой, записанной при копировании',
    'próbne przywrócenie':
        'пробное восстановление',
    '(brak zapisanych szablonów)':
        '(нет сохранённых шаблонов)',
    'Bez tego kopia planowa ruszy dopiero wtedy, gdy sam otworzysz program.':
        'Без этого плановая копия запустится, только когда вы сами откроете программу.',
    'Codziennie o godzinie':
        'Ежедневно в заданное время',
    'Codziennie o wybranej godzinie (zalecane)':
        'Ежедневно в выбранное время (рекомендуется)',
    'Dla dysku USB podłączanego od czasu do czasu. Najwyżej jedna kopia na 12 godzin.':
        'Для USB-диска, который подключается время от времени. Не чаще одной копии за 12 часов.',
    'Dostępne w zainstalowanej wersji programu (plik EXE).':
        'Доступно в установленной версии программы (файл EXE).',
    'Godzina kopii codziennej (czas tego komputera).':
        'Время ежедневного копирования (по часам этого компьютера).',
    'Harmonogram działa wtedy, gdy działa program — także ukryty przy zegarze.':
        'Расписание работает, пока работает программа, — в том числе когда она скрыта рядом с часами.',
    'Harmonogram nie uruchamia kopii, dopóki tego nie odznaczysz. Ręczne kopie działają.':
        'Пока этот флажок установлен, расписание не запускает копирование. Ручное копирование работает.',
    'Harmonogram szablonu „{name}” zapisany.':
        'Расписание шаблона «{name}» сохранено.',
    'Harmonogram:':
        'Расписание:',
    'Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.':
        'Если компьютер в это время будет выключен, копирование начнётся после его включения.',
    'Kiedy kopia z tego szablonu ma ruszać sama.':
        'Когда копирование по этому шаблону должно запускаться само.',
    'Kiedy robić kopię?':
        'Когда делать копию?',
    'Kopia będzie robiona codziennie o {time}; termin przegapiony przy wyłączonym komputerze program nadrobi po jego włączeniu.':
        'Копирование будет выполняться ежедневно в {time}; если компьютер был выключен, пропущенный запуск программа наверстает после его включения.',
    'Kopia planowa nie powiodła się':
        'Плановое копирование не удалось',
    'Kopia rusza tylko wtedy, gdy ją uruchomisz.':
        'Копирование начинается, только когда вы запускаете его сами.',
    'Kopia ruszy po podłączeniu dysku docelowego (najwyżej raz na 12 godzin).':
        'Копирование начнётся после подключения целевого диска (не чаще одного раза в 12 часов).',
    'Kopia ruszy po podłączeniu dysku docelowego — najwyżej raz na 12 godzin.':
        'Копирование начнётся после подключения целевого диска — не чаще одного раза в 12 часов.',
    'Kopia sprzed miesiąca nie chroni tego, co zmieniło się od tamtej pory.':
        'Копия месячной давности не защищает то, что изменилось с тех пор.',
    'Kopia „{name}” czeka':
        'Копирование «{name}» просрочено',
    'Kopia „{name}” nie ruszyła':
        'Копирование «{name}» не запустилось',
    'Kopie planowe działają, gdy działa program (także ukryty przy zegarze).':
        'Плановые копии выполняются, пока работает программа (в том числе скрытая рядом с часами).',
    'Kopie planowe działają, gdy działa program: po zamknięciu okna zostaje ikona przy zegarze, a przy logowaniu do Windows program uruchamia się w tle.':
        'Плановые копии выполняются, пока работает программа: после закрытия окна рядом с часами остаётся значок, а при входе в Windows программа запускается в фоне.',
    'Kopie planowe i praca w tle':
        'Плановые копии и работа в фоне',
    'Kopie planowe wykonają się o czasie. Program zamkniesz z menu ikony przy zegarze.':
        'Плановые копии будут выполнены вовремя. Закрыть программу можно через меню значка рядом с часами.',
    'Kopię uruchamiasz przyciskiem. Najprostsze, ale łatwo o niej zapomnieć.':
        'Вы запускаете копирование кнопкой. Проще всего, но о нём легко забыть.',
    'Kopię uruchamiasz sam — przyciskiem w programie albo z menu ikony przy zegarze.':
        'Вы запускаете копирование сами — кнопкой в программе или из меню значка рядом с часами.',
    'Następna kopia: {when}. Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.':
        'Следующая копия: {when}. Если компьютер в это время будет выключен, копирование начнётся после его включения.',
    'Nie udało się zmienić startu przy logowaniu — szczegóły w dzienniku.':
        'Не удалось изменить запуск при входе в систему — подробности в журнале.',
    'Od {days} dni nie było udanej kopii. Podłącz dysk docelowy albo otwórz program, żeby sprawdzić, co się dzieje.':
        'Дней без успешного копирования: {days}. Подключите целевой диск или откройте программу, чтобы выяснить, в чём дело.',
    'Otwórz Sigelith Backup':
        'Открыть Sigelith Backup',
    'Po podłączeniu dysku docelowego':
        'При подключении целевого диска',
    'Po podłączeniu dysku z kopią':
        'При подключении диска с копией',
    'Po zamknięciu okna działaj dalej przy zegarze, gdy są kopie planowe':
        'После закрытия окна продолжать работу в фоне (значок рядом с часами), если есть плановые копии',
    'Potrzebne, żeby kopie planowe ruszały bez Twojego udziału. Hasło trafia do magazynu systemowego powiązanego z Twoim kontem, nie do plików programu.':
        'Нужно, чтобы плановые копии запускались без вашего участия. Пароль попадает в системное хранилище, привязанное к вашей учётной записи, а не в файлы программы.',
    'Program uruchamia się w tle przy logowaniu, więc terminy nie przepadną.':
        'Программа запускается в фоне при входе в систему, поэтому сроки не будут пропущены.',
    'Ręcznie':
        'Вручную',
    'Ręcznie — kiedy zechcę':
        'Вручную — когда захочу',
    'Start przy logowaniu włączony':
        'Запуск при входе в систему включён',
    'Szablon jest zaszyfrowany, a hasło nie jest zapamiętane. Kopie planowe potrzebują hasła zapisanego w Menedżerze poświadczeń Windows.':
        'Шаблон зашифрован, а пароль не запомнен. Плановым копиям нужен пароль, сохранённый в Диспетчере учётных данных Windows.',
    'Sigelith Backup będzie uruchamiał się w tle, żeby wykonywać kopie planowe. Wyłączysz to w ustawieniach programu.':
        'Sigelith Backup будет запускаться в фоне, чтобы выполнять плановые копии. Отключить это можно в настройках программы.',
    'Sigelith Backup działa w tle':
        'Sigelith Backup работает в фоне',
    'Uruchamiaj program w tle przy logowaniu do Windows':
        'Запускать программу в фоне при входе в Windows',
    'Wstrzymaj kopie planowe':
        'Приостановить плановые копии',
    'Zakończ':
        'Выход',
    'Zamknięcie okna chowa je, a harmonogram pilnuje terminów. Program zamkniesz z menu ikony przy zegarze.':
        'Закрытие окна лишь скрывает его, а расписание следит за сроками. Закрыть программу можно через меню значка рядом с часами.',
    'Zrób kopię teraz':
        'Сделать копию сейчас',
    '{summary} Szczegóły znajdziesz w programie, w zakładce „Dziennik”.':
        '{summary} Подробности — в программе, на вкладке «Журнал».',
    'Program działa z uprawnieniami administratora. Nie są mu potrzebne — kopia i przywracanie działają bez nich, a pliki zapisane przez administratora mogą później nie dać się zmienić ze zwykłego konta.':
        'Программа запущена с правами администратора. Они ей не нужны — копирование и восстановление работают и без них, а файлы, записанные администратором, потом может быть невозможно изменить из обычной учётной записи.',
    'Pliki otwarte w innych programach nie trafiły do kopii: {files}. Zamknij te programy i uruchom kopię ponownie — dograne zostaną tylko te pliki.':
        'Файлы, открытые в других программах, не попали в копию: {files}. Закройте эти программы и запустите копирование снова — будут дописаны только эти файлы.',
    'Uwaga: w źródle zmieniło się podejrzanie dużo plików — {reasons}':
        'Внимание: в источнике изменилось подозрительно много файлов — {reasons}',
    'Wstrzymano kopię: w źródle zmieniło się podejrzanie dużo plików. {reasons}':
        'Копирование приостановлено: в источнике изменилось подозрительно много файлов. {reasons}',
    'Zmieniło się albo zniknęło {count} z {previous} plików poprzedniej kopii.':
        'Изменилось или исчезло файлов предыдущей копии: {count} из {previous}.',
    '{suspicious} z {evaluated} sprawdzonych zmienionych plików ma treść, która nie pasuje do ich typu (wygląda na zaszyfrowaną).':
        'Проверенных изменённых файлов, содержимое которых не соответствует их типу (выглядит зашифрованным): {suspicious} из {evaluated}.',
    'Kontynuuj mimo to':
        'Всё равно продолжить',
    'Kopia planowa wstrzymana':
        'Плановое копирование приостановлено',
    'Kopia wstrzymana do decyzji.':
        'Копирование приостановлено до вашего решения.',
    'Kopia wstrzymana — w źródle zmieniło się podejrzanie dużo plików.':
        'Копирование приостановлено — в источнике изменилось подозрительно много файлов.',
    'Podejrzanie dużo zmian':
        'Подозрительно много изменений',
    'Wstrzymaj kopię':
        'Приостановить копирование',
    '{reasons}\n\nJeśli to spodziewane — aktualizacja programu, przeniesienie albo przerobienie wielu plików — kontynuuj.\n\nJeśli nie, NIE kontynuuj: tak wygląda działanie oprogramowania szyfrującego pliki (ransomware). Sprawdź najpierw, czy Twoje pliki dają się otworzyć. Wcześniejsze wersje w kopii pozostają nietknięte.':
        '{reasons}\n\nЕсли это ожидаемо — обновление программы, перемещение или переработка множества файлов, — продолжайте.\n\nЕсли нет, НЕ продолжайте: так выглядит работа вредоносной программы, шифрующей файлы (программы-вымогателя). Сначала проверьте, открываются ли ваши файлы. Предыдущие версии в копии остаются нетронутыми.',
    '{reasons} To może być działanie złośliwego oprogramowania szyfrującego pliki. Otwórz program, sprawdź pliki i uruchom kopię ręcznie.':
        '{reasons} Это может быть работа вредоносной программы, шифрующей файлы. Откройте программу, проверьте файлы и запустите копирование вручную.',
    'Pominięto {count} {files}.':
        'Пропущено: {count} {files}.',
    'Ponawiam {count} {files}…':
        'Повторная попытка: {count} {files}…',
    ' (bez {count} {files})':
        ' (без {count} {files})',
    'plik otwarty w innym programie':
        'файл, открытый в другой программе',
    'pliki otwarte w innych programach':
        'файла, открытых в других программах',
    'plików otwartych w innych programach':
        'файлов, открытых в других программах',
    'pliku otwartego w innym programie':
        'файла, открытого в другой программе',
    '\n\n…i kolejne: {count}.':
        '\n\n…и ещё: {count}.',
    'Foldery objęte kopią ({count}): {list}':
        'Папки для копирования ({count}): {list}',
    'Nośnik nie obsługuje twardych dowiązań — kopiuję do nowej wersji niezmienione pliki: {count} ({size})…':
        'Носитель не поддерживает жёсткие ссылки — неизменённые файлы копируются в новую версию: {count} ({size})…',
    'Pliki bez sumy kontrolnej sprawdzone tylko co do rozmiaru, bo ich źródło zmieniło się albo jest niedostępne: {count}.':
        'Файлы без контрольной суммы, проверенные только по размеру, так как их источник изменился или недоступен: {count}.',
    'Pliki bez zapisanej sumy kontrolnej, porównane ze źródłem i uzupełnione w spisie treści: {count}.':
        'Файлы без записанной контрольной суммы, сравнённые с источником и дополненные в оглавлении: {count}.',
    'Pliki przeniesione w źródle: {count} — trafią do kopii bez przesyłania danych.':
        'Файлы, перемещённые в источнике: {count} — попадут в копию без передачи данных.',
    'Pliki skasowane w źródle: {count} — {action}.':
        'Файлы, удалённые в источнике: {count} — {action}.',
    'Pliki z końcówką dopisaną do nazwy, których oryginały zniknęły: {count}.':
        'Файлы с окончанием, добавленным к имени, оригиналы которых исчезли: {count}.',
    'Pliki zmienione w trakcie kopiowania: {count} — zostaną zapisane ponownie w przebiegu uzupełniającym.':
        'Файлы, изменённые во время копирования: {count} — будут записаны заново в проходе дозаписи.',
    'Pliki, których brakuje w kopii i które zostaną zapisane ponownie: {count}.':
        'Файлы, которых не хватает в копии и которые будут записаны заново: {count}.',
    'Podpinanie niezmienionych plików do nowej wersji: {count}…':
        'Связывание неизменённых файлов с новой версией: {count}…',
    'Pomijam pliki, które już są w tej wersji kopii: {count}.':
        'Пропуск файлов, которые уже есть в этой версии копии: {count}.',
    'Porządkowanie historii — usunięte najstarsze wersje: {count}.':
        'Упорядочивание истории — удалено самых старых версий: {count}.',
    'Przenoszenie plików, które zmieniły miejsce w źródle: {count}…':
        'Перемещение файлов, сменивших место в источнике: {count}…',
    'Próbne przywrócenie losowo wybranych plików: {count}…':
        'Пробное восстановление случайно выбранных файлов: {count}…',
    'Usuwanie z kopii plików skasowanych w źródle: {count}…':
        'Удаление из копии файлов, удалённых в источнике: {count}…',
    'Uzupełniam kopię o pliki, które przybyły lub zmieniły się w trakcie: {count} ({size})…':
        'Дополнение копии файлами, которые появились или изменились за это время: {count} ({size})…',
    'Uzupełnianie wersji {version} — pliki już zapisane, które zostaną pominięte: {count}.':
        'Дополнение версии {version} — уже записанные файлы, которые будут пропущены: {count}.',
    'Wznawiam wersję {version} — już zapisane: {done}, do dogrania: {todo}.':
        'Возобновление версии {version} — уже записано: {done}, осталось дописать: {todo}.',
    'pliku':
        'файла',
    'Brak fragmentu {cid} w magazynie kopii.':
        'Фрагмент {cid} отсутствует в хранилище фрагментов копии.',
    'Brak opisu magazynu fragmentów w katalogu kopii.':
        'В папке копии нет описания хранилища фрагментов.',
    'Duże pliki zapisuj różnicowo (od 256 MB)':
        'Сохранять только изменения больших файлов (от 256 MB)',
    'Fragment {cid} jest uszkodzony.':
        'Фрагмент {cid} повреждён.',
    'Kolejna wersja dużego pliku — maszyny wirtualnej, skrzynki pocztowej, bazy —\nzapisuje tylko zmienione fragmenty zamiast całego pliku. W kopii taki plik\nleży jako przepis + fragmenty; złoży go program albo skrypt ratunkowy.':
        'Следующая версия большого файла — виртуальной машины, почтового ящика, базы данных —\nсохраняет только изменённые фрагменты вместо всего файла. В копии такой файл\nхранится как схема сборки + фрагменты; собирает его программа или скрипт восстановления.',
    'Opis magazynu fragmentów jest uszkodzony.':
        'Описание хранилища фрагментов повреждено.',
    'Plik złożony z fragmentów różni się od zapisanego w przepisie.':
        'Файл, собранный из фрагментов, отличается от записанного в схеме сборки.',
    'Podane hasło nie pasuje do fragmentów zapisanych wcześniej w tej kopii.':
        'Введённый пароль не подходит к фрагментам, ранее записанным в эту копию.',
    'Przepis pliku jest uszkodzony.':
        'Схема сборки файла повреждена.',
    'To nie jest przepis pliku zapisanego fragmentami.':
        'Это не схема сборки файла, сохранённого фрагментами.',
    'Usunięto nieużywane fragmenty dużych plików: {count} ({size}).':
        'Удалены неиспользуемые фрагменты больших файлов: {count} ({size}).',
    ', zakotwiczona w Bitcoinie':
        ', привязана к Bitcoin',
    'Adres usługi:':
        'Адрес сервиса:',
    'Brak fragmentu {cid} w kopii poza domem.':
        'Фрагмент {cid} отсутствует в удалённой копии.',
    'Brak klucza albo hasła w Menedżerze poświadczeń Windows — zapisz ustawienia kopii poza domem jeszcze raz.':
        'В Диспетчере учётных данных Windows нет ключа или пароля — сохраните настройки удалённой копии ещё раз.',
    'Brak spisu wersji, którego dotyczy znacznik.':
        'Нет списка файлов версии, к которому относится метка времени.',
    'Certyfikat PDF':
        'PDF-сертификат',
    'Druga, zaszyfrowana kopia w usłudze zgodnej z S3 (np. Backblaze B2)':
        'Вторая, зашифрованная копия в S3-совместимом сервисе (например, Backblaze B2)',
    'Folder w kubełku:':
        'Папка в бакете:',
    'Hasło kopii poza domem':
        'Пароль удалённой копии',
    'Hasło kopii poza domem nie pasuje do danych zapisanych w tym miejscu.':
        'Пароль удалённой копии не подходит к данным, сохранённым в этом месте.',
    'Hasło kopii poza domem powinno mieć co najmniej 10 znaków.':
        'Пароль удалённой копии должен содержать не менее 10 символов.',
    'Hasło szyfrowania:':
        'Пароль шифрования:',
    'Identyfikator klucza:':
        'Идентификатор ключа:',
    'Katalog, do którego trafią pliki':
        'Папка, в которую попадут файлы',
    'Klucz tajny':
        'Секретный ключ',
    'Klucz tajny:':
        'Секретный ключ:',
    'Kopia na dysku obok komputera nie przetrwa pożaru ani kradzieży. Tu ustawisz drugą kopię w usłudze zgodnej z S3 (np. Backblaze B2). Pliki są szyfrowane na tym komputerze osobnym hasłem — usługa widzi tylko nieczytelne fragmenty.':
        'Копия на диске рядом с компьютером не переживёт пожар или кражу. Здесь можно настроить вторую копию в S3-совместимом сервисе (например, Backblaze B2). Файлы шифруются на этом компьютере отдельным паролем — сервис видит только нечитаемые фрагменты.',
    'Kopia poza domem':
        'Удалённая копия',
    'Kopia poza domem dla szablonu „{name}” zapisana.':
        'Настройки удалённой копии для шаблона «{name}» сохранены.',
    'Kopia poza domem nie ruszyła':
        'Удалённое копирование не запустилось',
    'Kopia poza domem potrzebuje Menedżera poświadczeń Windows, a jest on niedostępny.':
        'Для удалённой копии нужен Диспетчер учётных данных Windows, а он недоступен.',
    'Kopia poza domem „{name}”':
        'Удалённое копирование «{name}»',
    'Kopia poza domem…':
        'Удалённая копия…',
    'Korzeń tygodnia zakotwiczony w łańcuchu Bitcoina.':
        'Корень недели привязан к блокчейну Bitcoin.',
    'Kubełek (bucket):':
        'Бакет (bucket):',
    'Migawek w usłudze: {count}.':
        'Снимков в сервисе: {count}.',
    'Migawka i cel':
        'Снимок и назначение',
    'Migawka kopii poza domem jest uszkodzona.':
        'Снимок удалённой копии повреждён.',
    'Migawka {stamp}: plików bez zmian {reused}, wysłanych {files}, nowych fragmentów {chunks} ({size}).':
        'Снимок {stamp}: файлов без изменений — {reused}, отправлено — {files}, новых фрагментов — {chunks} ({size}).',
    'MinIO / Wasabi / inna zgodna z S3':
        'MinIO / Wasabi / другой S3-совместимый сервис',
    'NIEPOPRAWNY':
        'НЕДЕЙСТВИТЕЛЬНА',
    'Nie ma migawki {stamp} w kopii poza domem.':
        'В удалённой копии нет снимка {stamp}.',
    'Nie udało się połączyć z usługą przechowywania: {error}':
        'Не удалось подключиться к сервису хранения: {error}',
    'Nie udało się wczytać migawek: {error}':
        'Не удалось загрузить снимки: {error}',
    'Nie udało się zapisać klucza albo hasła w magazynie systemowym.':
        'Не удалось сохранить ключ или пароль в системном хранилище.',
    'Odśwież z sieci':
        'Обновить из сети',
    'Opis kopii poza domem jest uszkodzony.':
        'Описание удалённой копии повреждено.',
    'Oznakowana: {utc} (BeatTime {beat})':
        'Метка времени: {utc} (BeatTime {beat})',
    'Pliki wersji różnią się od spisu, który został oznakowany.':
        'Файлы версии отличаются от списка, на который поставлена метка времени.',
    'Pobiera i odszyfrowuje pliki wybranej migawki':
        'Загружает и расшифровывает файлы выбранного снимка',
    'Pobiera listę migawek z usługi':
        'Загружает список снимков из сервиса',
    'Pobiera podpis tygodnia i stan kotwicy w Bitcoinie':
        'Загружает подпись недели и состояние привязки к Bitcoin',
    'Pobieram potwierdzenia…':
        'Загрузка подтверждений…',
    'Podaj hasło szyfrowania kopii poza domem.':
        'Введите пароль шифрования удалённой копии.',
    'Podaj klucz tajny usługi.':
        'Введите секретный ключ сервиса.',
    'Podam dane ręcznie':
        'Ввести данные вручную',
    'Pominięte (otwarte w innych programach albo zmienione w trakcie): {count}.':
        'Пропущено (открыты в других программах или изменились в процессе): {count}.',
    'Porządkowanie kopii poza domem…':
        'Упорядочивание удалённой копии…',
    'Potwierdzenia odświeżone.':
        'Подтверждения обновлены.',
    'Poza dom':
        'Удалённая копия',
    'Połączenie działa: zapis, odczyt i usuwanie się udały.':
        'Подключение работает: запись, чтение и удаление прошли успешно.',
    'Połączenie nie działa: {error}':
        'Подключение не работает: {error}',
    'Przywraca pliki z zaszyfrowanej kopii w usłudze S3 — także na nowym komputerze':
        'Восстанавливает файлы из зашифрованной копии в сервисе S3 — в том числе на новом компьютере',
    'Przywracanie z kopii poza domem':
        'Восстановление из удалённой копии',
    'Przywracanie {count} {files} z kopii poza domem…':
        'Восстановление {count} {files} из удалённой копии…',
    'Przywróć':
        'Восстановить',
    'Region:':
        'Регион:',
    'Skąd':
        'Откуда',
    'Spis wersji zgodny ze znacznikiem: {answer}':
        'Список файлов версии совпадает с меткой времени: {answer}',
    'Spis wersji został zmieniony po oznakowaniu.':
        'Список файлов версии изменён после постановки метки времени.',
    'Sprawdza spis wersji, drogę w drzewie tygodnia i podpis — bez sieci':
        'Проверяет список файлов версии, путь в дереве недели и подпись — без сети',
    'Sprawdzam połączenie…':
        'Проверка подключения…',
    'Sprawdź':
        'Проверить',
    'Sprawdź połączenie':
        'Проверить подключение',
    'Starsze migawki są usuwane, gdy nadmiar sięgnie kilku — co kilka dni.':
        'Старые снимки удаляются, когда их накопится несколько лишних, — раз в несколько дней.',
    'Suma w drzewie tygodnia: {answer}':
        'Контрольная сумма в дереве недели: {answer}',
    'Suma wersji nie należy do drzewa tygodnia podanego w potwierdzeniu.':
        'Контрольная сумма версии не входит в дерево недели, указанное в подтверждении.',
    'Ta wersja nie ma znacznika czasu.':
        'У этой версии нет метки времени.',
    'Także po kopiach planowych. Wysyłane są tylko pliki nowe i zmienione.':
        'В том числе после плановых копий. Отправляются только новые и изменённые файлы.',
    'Tydzień jeszcze się nie zamknął — podpis pojawi się po poniedziałku 00:00 UTC.':
        'Неделя ещё не закрыта — подпись появится после 00:00 UTC понедельника.',
    'Usunięto starsze migawki: {count}, nieużywane fragmenty: {chunks}.':
        'Удалено старых снимков: {count}, неиспользуемых фрагментов: {chunks}.',
    'Usługa chwilowo niedostępna ({status}).':
        'Сервис временно недоступен ({status}).',
    'Usługa odrzuciła żądanie ({status} {code}): {message}':
        'Сервис отклонил запрос ({status} {code}): {message}',
    'Usługa przechowywania':
        'Сервис хранения',
    'Usługa zwróciła inną treść niż zapisana.':
        'Сервис вернул не то содержимое, которое было записано.',
    'Usługa:':
        'Сервис:',
    'Uzupełnij adres usługi, nazwę kubełka i klucze dostępu.':
        'Укажите адрес сервиса, имя бакета и ключи доступа.',
    'Uzupełnij adres usługi, region, kubełek i identyfikator klucza.':
        'Укажите адрес сервиса, регион, бакет и идентификатор ключа.',
    'W tym katalogu kopii nie ma jeszcze znaczników czasu.':
        'В этой папке копии ещё нет меток времени.',
    'W tym miejscu nie ma jeszcze kopii poza domem.':
        'В этом месте ещё нет удалённой копии.',
    'Wczytaj migawki':
        'Загрузить снимки',
    'Wczytaj migawki i wybierz jedną z listy.':
        'Загрузите снимки и выберите один из списка.',
    'Wczytuję migawkę {stamp}…':
        'Загрузка снимка {stamp}…',
    'Wczytuję poprzednią migawkę kopii poza domem…':
        'Загрузка предыдущего снимка удалённой копии…',
    'Wybierz migawkę i katalog, do którego trafią pliki.':
        'Выберите снимок и папку, в которую попадут файлы.',
    'Wybierz wersję z listy.':
        'Выберите версию в списке.',
    'Wysyłaj poza dom po każdej udanej kopii z tego szablonu':
        'Отправлять в удалённую копию после каждого успешного копирования по этому шаблону',
    'Wysyłam poza dom pliki nowe i zmienione: {count}…':
        'Отправка новых и изменённых файлов в удалённую копию: {count}…',
    'Z kopii poza domem…':
        'Из удалённой копии…',
    'Zachowuj migawek:':
        'Хранить снимков:',
    'Zapisuje ustawienia; klucz i hasło trafiają do Menedżera poświadczeń Windows':
        'Сохраняет настройки; ключ и пароль попадают в Диспетчер учётных данных Windows',
    'Zapisuje, odczytuje i usuwa mały plik próbny':
        'Записывает, читает и удаляет небольшой тестовый файл',
    'Zapisuję migawkę {stamp}…':
        'Сохранение снимка {stamp}…',
    'Znacznik dowodzi, że wersja kopii w dokładnie tym kształcie istniała w podanej chwili. Podpis tygodnia pojawia się po jego zamknięciu (poniedziałek 00:00 UTC), a kotwica w Bitcoinie — zwykle kilka godzin później.':
        'Метка времени доказывает, что версия копии именно в таком виде существовала в указанный момент. Подпись недели появляется после её закрытия (понедельник, 00:00 UTC), а привязка к Bitcoin — обычно через несколько часов.',
    'Znacznika czasu nie udało się zapisać: {error}':
        'Не удалось сохранить метку времени: {error}',
    'Znaczniki czasu':
        'Метки времени',
    'Znaczniki czasu…':
        'Метки времени…',
    'kopia poza domem':
        'удалённое копирование',
    'np. komputer-domowy':
        'например, home-pc',
    'oznakowana {when} — podpis po zamknięciu tygodnia':
        'метка поставлена {when} — подпись после закрытия недели',
    'podpisana (tydzień {week}){bitcoin}':
        'подписана (неделя {week}){bitcoin}',
    'poprawny':
        'действительна',
    'przywracanie z kopii poza domem':
        'восстановление из удалённой копии',
    'Łączę się z usługą…':
        'Подключение к сервису…',
    ' dni':
        ' дн.',
    ' mies.':
        ' мес.',
    ' tyg.':
        ' нед.',
    'Ile ostatnich wersji zachować. Starsze są kasowane po udanym przebiegu.':
        'Сколько последних версий хранить. Более старые удаляются после успешного запуска.',
    'Kalendarz zostawia najnowszą wersję z każdego z ostatnich dni, tygodni\ni miesięcy — gęsto dla świeżych zmian, rzadko dla dawnych. Nadmiar jest\nkasowany po udanym przebiegu; wersje niedokończone nigdy.':
        'Календарь оставляет самую новую версию за каждый из последних дней, недель\nи месяцев — часто для свежих изменений, редко для давних. Лишнее\nудаляется после успешного запуска; незавершённые версии — никогда.',
    'Z ilu ostatnich dni zachować po jednej, najnowszej wersji.':
        'За сколько последних дней хранить по одной, самой новой версии.',
    'Z ilu ostatnich miesięcy zachować po jednej, najnowszej wersji.':
        'За сколько последних месяцев хранить по одной, самой новой версии.',
    'Z ilu ostatnich tygodni zachować po jednej, najnowszej wersji.':
        'За сколько последних недель хранить по одной, самой новой версии.',
    'Zachowuj:':
        'Хранить:',
    'kalendarz: dni, tygodnie, miesiące':
        'календарь: дни, недели, месяцы',
    'ostatnie wersje':
        'последние версии',
    'wszystkie wersje':
        'все версии',
    ' (niedokończona)':
        ' (не завершена)',
    'Fragment nazwy albo ścieżki, bez rozróżniania wielkości liter.':
        'Часть имени или пути, без учёта регистра.',
    'Główny folder kopii':
        'Главная папка копии',
    'Historia pliku':
        'История файла',
    'Nazwa':
        'Имя',
    'Nic nie znaleziono.':
        'Ничего не найдено.',
    'Nie udało się: {error}':
        'Не удалось: {error}',
    'Odtwarza plik do katalogu tymczasowego i otwiera go':
        'Восстанавливает файл во временную папку и открывает его',
    'Odtwarza plik w wybranym miejscu':
        'Восстанавливает файл в выбранное место',
    'Odtwarzam „{name}”…':
        'Восстановление «{name}»…',
    'Otwarto kopię „{name}” (plik tymczasowy, zniknie po zamknięciu programu).':
        'Открыта копия «{name}» (временный файл, исчезнет после закрытия программы).',
    'Otwórz':
        'Открыть',
    'Otwórz kopię':
        'Открыть копию',
    'Pliki i wersje wprost z kopii — bez przywracania':
        'Файлы и версии прямо из копии — без восстановления',
    'Pliki i wersje wprost z kopii — bez przywracania całości.':
        'Файлы и версии прямо из копии — без восстановления всей копии.',
    'Pokazuje pliki i wersje tej kopii — pojedynczy plik otworzysz bez przywracania całości':
        'Показывает файлы и версии этой копии — отдельный файл можно открыть, не восстанавливая всю копию',
    'Pokaż foldery':
        'Показать папки',
    'Przeglądaj…':
        'Просмотреть…',
    'Przeglądanie':
        'Просмотр',
    'Przeszukuje spis treści kopii':
        'Ищет в оглавлении копии',
    'Rozmiar':
        'Размер',
    'Szukaj':
        'Найти',
    'Szukaj pliku w najnowszym stanie kopii…':
        'Поиск файла в последнем состоянии копии…',
    'Szukam…':
        'Поиск…',
    'W których wersjach jest ten plik i kiedy się zmieniał':
        'В каких версиях есть этот файл и когда он менялся',
    'W tym folderze nie ma wersji kopii.':
        'В этой папке нет версий копии.',
    'Wczytuje wersje z tego folderu kopii':
        'Загружает версии из этой папки копии',
    'Wersja kopii, której zawartość widzisz poniżej.':
        'Версия копии, содержимое которой показано ниже.',
    'Wersja: {version}':
        'Версия: {version}',
    'Wersje z tym plikiem: {count}. Dwuklik otwiera kopię z danej wersji.':
        'Версий с этим файлом: {count}. Двойной щелчок открывает копию из выбранной версии.',
    'Wraca z wyników wyszukiwania do drzewa folderów':
        'Возвращает от результатов поиска к дереву папок',
    'Wskaż folder kopii i kliknij „Otwórz”.':
        'Укажите папку копии и нажмите «Открыть».',
    'Zapisano: {path}':
        'Сохранено: {path}',
    'Zapisz jako…':
        'Сохранить как…',
    'Zapisz kopię pliku':
        'Сохранить копию файла',
    'Zaznacz plik i wybierz „Otwórz kopię”, żeby zajrzeć do niego w zwykłym programie, albo „Historia pliku”, żeby zobaczyć, w których wersjach się zmieniał.':
        'Выделите файл и нажмите «Открыть копию», чтобы посмотреть его в обычной программе, или «История файла», чтобы увидеть, в каких версиях он менялся.',
    'Zmieniono':
        'Дата изменения',
    'Znalezione pliki: {count}. Wyniki pochodzą z najnowszego stanu kopii.':
        'Найдено файлов: {count}. Результаты взяты из последнего состояния копии.',
    'przeglądanie kopii':
        'просмотр копии',
    'zmieniony':
        'изменён',
    'najstarsza zachowana kopia':
        'самая старая сохранённая копия',
    'Foldery w AppData':
        'Папки в AppData',
    'Przywracanie utworzy nowe foldery bezpośrednio w AppData:\n\n{folders}\n\nWindows pozwala wersji programu ze Sklepu tworzyć je tylko w jej prywatnej kopii — pliki będą widoczne w tym programie, ale nie w programie, do którego należą.\n\nNajprościej: zainstaluj i raz uruchom tamten program (utworzy swój folder), a potem przywróć jeszcze raz. Albo przywróć do zwykłego folderu i przenieś pliki Eksploratorem.':
        'Восстановление создаст новые папки прямо в AppData:\n\n{folders}\n\nWindows позволяет версии программы из Microsoft Store создавать их только в её личной копии — файлы будут видны в этой программе, но не в той, которой они принадлежат.\n\nПроще всего: установите и один раз запустите ту программу (она создаст свою папку), а затем восстановите ещё раз. Или восстановите в обычную папку и перенесите файлы Проводником.',
    'Przywracanie utworzyłoby w AppData nowe foldery, których inne programy nie zobaczą: {folders}':
        'Восстановление создало бы в AppData новые папки, которых не увидят другие программы: {folders}',
    'Przywracanie wstrzymane do decyzji.':
        'Восстановление приостановлено до вашего решения.',
    'Przywróć mimo to':
        'Всё равно восстановить',
    'Start programu przy logowaniu wyłączono w Ustawieniach Windows. Włączysz go tam: Ustawienia → Aplikacje → Uruchamianie → Sigelith Backup.':
        'Запуск программы при входе в систему отключён в Параметрах Windows. Включить его можно там: Параметры → Приложения → Автозагрузка → Sigelith Backup.',
    'Start przy logowaniu':
        'Запуск при входе в систему',
    'Start przy logowaniu wyłączono w Ustawieniach Windows → Aplikacje → Uruchamianie; dopóki go tam nie włączysz, kopie planowe działają tylko przy otwartym programie.':
        'Запуск при входе в систему отключён в Параметрах Windows → Приложения → Автозагрузка; пока вы не включите его там, плановые копии выполняются только при открытой программе.',
    'Ten sam przełącznik jest w Ustawieniach Windows → Aplikacje → Uruchamianie. Wyłączony tam da się włączyć tylko tam.':
        'Тот же переключатель есть в Параметрах Windows → Приложения → Автозагрузка. Если отключить его там, включить его можно будет только там.',
    'Brak pliku {name} w katalogu programu.':
        'В папке программы нет файла {name}.',
    'Jakie dane program przetwarza i gdzie':
        'Какие данные обрабатывает программа и где',
    'Kod źródłowy Qt':
        'Исходный код Qt',
    'Licencja programu':
        'Лицензия программы',
    'Licencja programu i licencje użytych składników':
        'Лицензия программы и лицензии используемых компонентов',
    'Licencje':
        'Лицензии',
    'Licencje i prywatność':
        'Лицензии и конфиденциальность',
    'Licencje…':
        'Лицензии…',
    'Otwiera folder z plikami licencji w Eksploratorze':
        'Открывает папку с файлами лицензий в Проводнике',
    'Pokaż pliki licencji':
        'Показать файлы лицензий',
    'Polityka prywatności':
        'Политика конфиденциальности',
    'Polityka prywatności…':
        'Политика конфиденциальности…',
    'Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0 — to osobne pliki w katalogu programu, które można zastąpić zgodnymi wersjami. Kod źródłowy wersji dołączonych do programu: {qt} oraz {pyside}.':
        'Программа использует библиотеки Qt и PySide6 на условиях лицензии LGPL-3.0 — это отдельные файлы в папке программы, которые можно заменить совместимыми версиями. Исходный код версий, поставляемых с программой: {qt} и {pyside}.',
    'Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0, z Pythona i z innych składników na licencjach otwartych (m.in. MIT, BSD, Apache 2.0); ikony: Bootstrap Icons (MIT). Wykaz, prawa autorskie, pełne teksty licencji i adresy kodu źródłowego Qt są pod przyciskiem „Licencje”.':
        'Программа использует библиотеки Qt и PySide6 на условиях лицензии LGPL-3.0, Python и другие компоненты под открытыми лицензиями (в том числе MIT, BSD, Apache 2.0); значки: Bootstrap Icons (MIT). Перечень, сведения об авторских правах, полные тексты лицензий и адреса исходного кода Qt доступны по кнопке «Лицензии».',
    'Program usunie z Menedżera poświadczeń Windows wszystkie hasła, które zapamiętał: hasła kopii i dane dostępu do kopii poza domem. Kopie planowe szablonów zaszyfrowanych będą potem czekać, aż podasz hasło.\n\nUsunąć?':
        'Программа удалит из Диспетчера учётных данных Windows все запомненные ею пароли: пароли копий и данные доступа к удалённой копии. После этого плановые копии зашифрованных шаблонов будут ждать, пока вы не введёте пароль.\n\nУдалить?',
    'Składniki i ich licencje':
        'Компоненты и их лицензии',
    'Strona z kodem źródłowym Qt w wersji użytej w programie':
        'Страница с исходным кодом Qt той версии, что используется в программе',
    'Usunięte zapamiętane hasła: {count}.':
        'Удалено запомненных паролей: {count}.',
    'Usuwa z Menedżera poświadczeń Windows wszystkie hasła zapamiętane przez program — na przykład przed odinstalowaniem':
        'Удаляет из Диспетчера учётных данных Windows все пароли, запомненные программой, — например, перед её удалением',
    'Usuń zapamiętane hasła':
        'Удалить запомненные пароли',
    'Usuń zapamiętane hasła…':
        'Удалить запомненные пароли…',
    '© {years} {publisher}. Wolne oprogramowanie na licencji GNU GPL w wersji 3 lub nowszej.':
        '© {years} {publisher}. Свободное программное обеспечение на условиях GNU GPL версии 3 или более поздней.',
    'Kod źródłowy':
        'Исходный код',
    'Kod źródłowy programu w serwisie GitHub':
        'Исходный код программы на GitHub',
    'Sigelith odrzucił żądanie ({status}): {detail}':
        'Sigelith отклонил запрос ({status}): {detail}',
    'Nie udało się połączyć z Sigelith: {error}':
        'Не удалось подключиться к Sigelith: {error}',
    'Sigelith odesłał potwierdzenie innej sumy kontrolnej.':
        'Sigelith вернул подтверждение для другой контрольной суммы.',
    'Znacznik czeka na połączenie z Sigelith.':
        'Метка времени ожидает подключения к Sigelith.',
    'Podpis tygodnia nie zgadza się z kluczem Sigelith zapisanym w programie.':
        'Подпись недели не соответствует ключу Sigelith, встроенному в программу.',
    'Otwiera certyfikat znacznika na stronie Sigelith':
        'Открывает сертификат метки времени на сайте Sigelith',
    'Podpis Sigelith: {answer}':
        'Подпись Sigelith: {answer}',
    'Znaczniki Sigelith wersji w tym katalogu kopii: sprawdzenie i certyfikat':
        'Метки времени Sigelith для версий в этой папке копии: проверка и сертификат',
    'Znakuję wersję czasem Sigelith (wysyłana jest tylko suma kontrolna)…':
        'Постановка метки времени Sigelith на версию (отправляется только контрольная сумма)…',
    'Znacznik czasu czeka na połączenie z Sigelith — zostanie wysłany przy następnej kopii.':
        'Метка времени ожидает подключения к Sigelith — запрос отправится при следующем копировании.',
    'Znakuj wersję czasem Sigelith':
        'Ставить на версию метку времени Sigelith',
    'Znaczniki czasu Sigelith':
        'Метки времени Sigelith',
    'czeka na połączenie z Sigelith':
        'ожидает подключения к Sigelith',
    'Dowód, że kopia w tym kształcie istniała danego dnia (podpis Ed25519, kotwica\nw Bitcoinie). Do sigelith.org trafia wyłącznie suma kontrolna spisu wersji —\nżadne nazwy plików ani ich treść.':
        'Доказательство того, что копия в таком виде существовала в определённый день (подпись Ed25519, привязка\nк Bitcoin). На sigelith.org отправляется только контрольная сумма списка файлов версии —\nникаких имён файлов и никакого содержимого.',
    'Kopie zapasowe folderów na dysk zewnętrzny, z historią wersji i szyfrowaniem. Wszystko dzieje się na Twoim komputerze, bez konta i bez telemetrii. Z internetem program łączy się tylko wtedy, gdy sam włączysz kopię poza domem albo znaczniki czasu Sigelith.':
        'Резервные копии папок на внешний диск, с историей версий и шифрованием. Всё происходит на вашем компьютере, без учётной записи и без телеметрии. К интернету программа подключается, только если вы сами включите удалённую копию или метки времени Sigelith.',
    'Bez dokumentu: {count} {stamps} — plik zmienił się po stemplu albo zniknął i nie ma go w żadnej wersji tej kopii ({names}). Sam dowód jest zachowany.':
        'Без документа: {count} {stamps} — файл изменился после отметки или исчез, и его нет ни в одной версии этой копии ({names}). Само доказательство сохранено.',
    'Brak pliku dowodu albo dowód jest zaszyfrowany.':
        'Файл доказательства отсутствует или зашифрован.',
    'Chroni dowody Sigelith: historię stempli i oznakowane dokumenty.':
        'Защищает доказательства Sigelith: историю отметок и отмеченные документы.',
    'Chroń dowody Sigelith':
        'Защищать доказательства Sigelith',
    'Chroń też dowody Sigelith':
        'Также защищать доказательства Sigelith',
    'Dokument':
        'Документ',
    'Dokumenty oznakowane w Sigelith, zabezpieczone w tej kopii: sprawdzenie i odzyskanie':
        'Документы, отмеченные в Sigelith и сохранённые в этой копии: проверка и восстановление',
    'Dowody Sigelith':
        'Доказательства Sigelith',
    'Dowody Sigelith: historia stempli i dokładne kopie oznakowanych dokumentów z plikami .beatproof trafią do magazynu dowodów w katalogu kopii.':
        'Доказательства Sigelith: история отметок и точные копии отмеченных документов с файлами .beatproof попадут в хранилище доказательств в папке копии.',
    'Dowody Sigelith: zabezpieczone dokumenty {count} z {total}':
        'Доказательства Sigelith: сохранено документов — {count} из {total}',
    'Dowody Sigelith…':
        'Доказательства Sigelith…',
    'Dowody z problemem: {count} — szczegóły w kolumnie „Stan”.':
        'Доказательств с проблемами: {count} — подробности в столбце «Состояние».',
    'Dowodów Sigelith nie udało się zabezpieczyć: {error}':
        'Не удалось сохранить доказательства Sigelith: {error}',
    "Droga w drzewie Merkle'a nie prowadzi do podpisanego korzenia tygodnia.":
        'Путь в дереве Merkle не ведёт к подписанному корню недели.',
    'Gdzie zapisać dokumenty i dowody':
        'Куда сохранить документы и доказательства',
    'Historia stempli Sigelith Desktop i dokładne bajty oznakowanych dokumentów, z plikami .beatproof — w osobnym magazynie, którego retencja nie sprząta.':
        'История отметок Sigelith Desktop и точные байты отмеченных документов с файлами .beatproof — в отдельном хранилище, которое ротация старых версий никогда не очищает.',
    'Każdy stempel ma tu swój folder z dokładnie tym dokumentem, który oznakowano, i plikiem .beatproof. „Sprawdź” liczy sumę każdego dokumentu i sprawdza podpis tygodnia bez łączenia się z siecią.':
        'У каждой отметки здесь своя папка с тем самым документом, который был отмечен, и файлом .beatproof. «Проверить» вычисляет контрольную сумму каждого документа и проверяет подпись недели без подключения к сети.',
    'Kopia obejmie folder danych Sigelith Desktop (historię stempli), a każdy oznakowany\ndokument trafi — dokładnie w tej postaci, którą oznakowano — do magazynu dowodów\nw katalogu kopii, razem z plikiem .beatproof. Starych wersji magazyn nie dotyczy:\nretencja go nie sprząta.':
        'Копия включит папку данных Sigelith Desktop (историю отметок), а каждый отмеченный\nдокумент — точно в том виде, в каком он был отмечен, — попадёт в хранилище доказательств\nв папке копии вместе с файлом .beatproof. Хранилище не относится к старым версиям:\nротация его никогда не очищает.',
    'Magazyn dowodów jest pusty.':
        'Хранилище доказательств пусто.',
    'Na tym komputerze jest Sigelith Desktop: {count} {stamps}.':
        'На этом компьютере есть Sigelith Desktop: {count} {stamps}.',
    'Na tym komputerze nie ma danych Sigelith Desktop.':
        'На этом компьютере нет данных Sigelith Desktop.',
    'Otwórz folder dowodów':
        'Открыть папку доказательств',
    'Oznakowano':
        'Дата отметки',
    'Pokazuje magazyn dowodów w Eksploratorze':
        'Показывает хранилище доказательств в Проводнике',
    'Przywróć zaznaczone…':
        'Восстановить выбранные…',
    'Sigelith Desktop: {count} {stamps} w folderze {path}.':
        'Sigelith Desktop: {count} {stamps} в папке {path}.',
    'Sprawdza każdy dokument i jego dowód bez łączenia z siecią':
        'Проверяет каждый документ и его доказательство без подключения к сети',
    'Sprawdzam dowody…':
        'Проверка доказательств…',
    'Stan':
        'Состояние',
    'Stemple w magazynie: {count}, z dokumentem: {documents}.':
        'Отметок в хранилище: {count}, с документом: {documents}.',
    'Suma dokumentu nie zgadza się z dowodem.':
        'Контрольная сумма документа не совпадает с доказательством.',
    'To nie jest plik dowodu Sigelith (beatproof-v1).':
        'Это не файл доказательства Sigelith (beatproof-v1).',
    'Tydzień stempla jeszcze się nie zamknął — podpis dojdzie przy kolejnej kopii.':
        'Неделя отметки ещё не закрыта — подпись будет добавлена при следующем копировании.',
    'W magazynie nie ma dokumentu do tego dowodu.':
        'В хранилище нет документа для этого доказательства.',
    'Wszystkie dowody pasują do dokumentów i mają poprawny podpis.':
        'Все доказательства соответствуют документам и имеют действительную подпись.',
    'Zabezpieczam dokumenty oznakowane w Sigelith…':
        'Сохранение документов, отмеченных в Sigelith…',
    'Zapisano pliki: {count} w {path}.':
        'Файлы сохранены в {path}: {count}.',
    'Zapisuje dokumenty razem z plikami .beatproof we wskazanym folderze':
        'Сохраняет документы вместе с файлами .beatproof в указанную папку',
    'bez dokumentu — dowód zachowany':
        'нет документа — доказательство сохранено',
    'czekają na podpis tygodnia: {count}':
        'ожидают подписи недели: {count}',
    'dokument i dowód są w kopii':
        'документ и доказательство есть в копии',
    'dokument jest; dowód czeka na podpis tygodnia':
        'документ есть; доказательство ожидает подписи недели',
    'dowodu nie da się odczytać':
        'доказательство не удаётся прочитать',
    'dowody Sigelith':
        'доказательства Sigelith',
    'dowody uzupełnione o podpis tygodnia: {count}':
        'доказательств дополнено подписью недели: {count}',
    'nowe: {count}':
        'новых: {count}',
    'odtworzone ze starszych wersji kopii: {count}':
        'восстановлено из старых версий копии: {count}',
    'sprawdzony: dokument i dowód się zgadzają':
        'проверено: документ и доказательство совпадают',
    'stempel':
        'отметка',
    'stemple':
        'отметки',
    'stempli':
        'отметок',
    'zaszyfrowany — podaj hasło, żeby sprawdzić':
        'зашифровано — введите пароль для проверки',
    'Chroń dowody Sigelith, gdy go zainstaluję':
        'Защищать доказательства Sigelith, когда я его установлю',
    'Dowody Sigelith: na tym komputerze nie ma jeszcze Sigelith Desktop — ochrona zacznie działać sama, gdy się pojawi.':
        'Доказательства Sigelith: на этом компьютере ещё нет Sigelith Desktop — защита включится сама, когда он появится.',
    'Dowody Sigelith: ochrona zacznie działać sama, gdy zainstalujesz Sigelith Desktop.':
        'Доказательства Sigelith: защита включится сама, когда вы установите Sigelith Desktop.',
    'Dowody czasu dla ważnych dokumentów':
        'Доказательства времени для важных документов',
    'Kopia zachowa każdy dokument oznakowany w Sigelith Desktop dokładnie w tej postaci, którą oznakowano, razem z dowodem — nawet gdy oryginał później się zmieni.':
        'Копия сохранит каждый документ, отмеченный в Sigelith Desktop, точно в том виде, в каком он был отмечен, вместе с доказательством — даже если оригинал потом изменится.',
    'Ochrona zacznie działać sama, gdy na komputerze pojawi się Sigelith Desktop.':
        'Защита включится сама, когда на компьютере появится Sigelith Desktop.',
    'Otwiera stronę programu Sigelith Desktop':
        'Открывает страницу программы Sigelith Desktop',
    'Poznaj Sigelith Desktop':
        'Подробнее о Sigelith Desktop',
    'Sigelith Desktop, program tego samego wydawcy, oznakuje dokument czasem: to podpisany dowód, że plik w tej postaci istniał w danej chwili, sprawdzalny bez udziału kogokolwiek. Sigelith Backup przechowa potem każdy oznakowany dokument razem z dowodem.':
        'Sigelith Desktop, программа того же издателя, ставит на документ метку времени: это подписанное доказательство того, что файл в таком виде существовал в определённый момент, и проверить его можно без чьего-либо участия. Затем Sigelith Backup сохранит каждый отмеченный документ вместе с доказательством.',
    'Umowy, faktury, projekty — czasem trzeba wykazać, że dokument istniał danego dnia.':
        'Договоры, счета, проекты — иногда нужно доказать, что документ существовал в определённый день.',
    'Nieznany format spisu wersji.':
        'Неизвестный формат списка файлов версии.',
    'Ta wersja nie ma pieczęci dla pojedynczych plików (kopia sprzed wersji 3.0 albo bez znaczników czasu).':
        'У этой версии нет печати для отдельных файлов (копия создана до версии 3.0 или без меток времени).',
    'Pieczęć tej wersji czeka jeszcze na podpis tygodnia Sigelith — dowód będzie gotowy po poniedziałku 00:00 UTC i kolejnej kopii.':
        'Печать этой версии ещё ожидает подписи недели Sigelith — доказательство будет готово после 00:00 UTC понедельника и следующего копирования.',
    'Brak oświadczenia pieczęci w folderze wersji.':
        'В папке версии нет заявления печати.',
    'Oświadczenie pieczęci nie zgadza się z pieczęcią wersji.':
        'Заявление печати не совпадает с печатью версии.',
    'Drzewo plików wersji nie zgadza się z pieczęcią.':
        'Дерево файлов версии не совпадает с печатью.',
    'Tego pliku nie ma w spisie tej wersji.':
        'Этого файла нет в списке файлов этой версии.',
    'To nie jest dowód pliku z kopii Sigelith Backup ({format}).':
        'Это не доказательство файла из копии Sigelith Backup ({format}).',
    'Dowód jest uszkodzony — brakuje pól albo mają zły format.':
        'Доказательство повреждено — поля отсутствуют или имеют неверный формат.',
    'Ten plik nie jest plikiem, którego dotyczy dowód.':
        'Это не тот файл, к которому относится доказательство.',
    'Ścieżka pliku w dowodzie nie zgadza się z liściem drzewa.':
        'Путь к файлу в доказательстве не совпадает с листом дерева.',
    'Droga w drzewie plików nie prowadzi do korzenia z pieczęci.':
        'Путь в дереве файлов не ведёт к запечатанному корню.',
    'Oświadczenie pieczęci nie potwierdza tego drzewa plików.':
        'Заявление печати не подтверждает это дерево файлов.',
    'Potwierdzenie Sigelith nie dotyczy tej pieczęci.':
        'Подтверждение Sigelith относится не к этой печати.',
    'Dowód czasu…':
        'Доказательство времени…',
    'Zapisuje dowód, że ten plik był w kopii w chwili jej oznakowania — bez ujawniania innych plików':
        'Сохраняет доказательство того, что этот файл был в копии в момент её запечатывания, — не раскрывая другие файлы',
    'Dowód czasu':
        'Доказательство времени',
    'Dołączyć do dowodu ścieżkę pliku w kopii („{path}”)?\n\nBez niej dowód dalej potwierdza plik i chwilę oznakowania, ale nie mówi, gdzie plik leżał.':
        'Включить в доказательство путь к файлу в копии («{path}»)?\n\nБез него доказательство по-прежнему подтверждает файл и момент запечатывания, но не говорит, где лежал файл.',
    'Przygotowuję dowód dla „{name}”…':
        'Подготовка доказательства для «{name}»…',
    'Zapisz dowód czasu':
        'Сохранить доказательство времени',
    'Dowód pliku Sigelith (*{suffix})':
        'Доказательство файла Sigelith (*{suffix})',
    'Zapisano dowód i certyfikat PDF: {path}. Sprawdzi go Sigelith Desktop albo strona sigelith.org/verify/.':
        'Доказательство и PDF-сертификат сохранены: {path}. Проверить его можно в Sigelith Desktop или на sigelith.org/verify/.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją sprawdzić.':
        'Копия зашифрована — введите пароль, чтобы проверить её.',
    'Ta wersja nie ma pieczęci — nie ma z czym porównać plików.':
        'У этой версии нет печати — файлы не с чем сравнить.',
    'Pieczęć wersji się nie potwierdza: {problems}':
        'Печать версии не подтверждается: {problems}',
    'brak podpisu tygodnia':
        'нет подписи недели',
    'Audyt przerwany.':
        'Аудит прерван.',
    'próbka {checked} z {listed} plików':
        'выборка файлов: {checked} из {listed}',
    'wszystkie pliki ({count})':
        'все файлы ({count})',
    'Nietknięta: sprawdzono {scope}, wszystko zgodne z pieczęcią w publicznym dzienniku.':
        'Нетронута: проверено — {scope}; всё совпадает с печатью в публичном журнале.',
    'zmienione: {files}':
        'изменены: {files}',
    'brakujące: {files}':
        'отсутствуют: {files}',
    'nieczytelne albo uszkodzone: {files}':
        'нечитаемы или повреждены: {files}',
    'PODMIENIONA albo uszkodzona ({scope}) — {details}.':
        'ПОДМЕНЕНА или повреждена ({scope}) — {details}.',
    'Audyt treści':
        'Аудит содержимого',
    'Czyta z nośnika każdy plik tej wersji i porównuje go z sumą oznakowaną w publicznym dzienniku':
        'Читает с носителя каждый файл этой версии и сравнивает его с хешем, запечатанным в публичном журнале',
    'Ostatnia nietknięta':
        'Последняя нетронутая',
    'Sprawdza wersje od najnowszej i wskazuje ostatnią zgodną z pieczęcią — z niej przywracaj':
        'Проверяет версии, начиная с самой новой, и указывает последнюю, совпадающую со своей печатью, — восстанавливайте из неё',
    'Ostatnia nietknięta wersja: {label} — z niej przywracaj.':
        'Последняя нетронутая версия: {label} — восстанавливайте из неё.',
    'Żadna wersja z pieczęcią nie jest nietknięta.':
        'Ни одна версия с печатью не осталась нетронутой.',
    'Czytam pliki kopii i porównuję je z pieczęcią w publicznym dzienniku…':
        'Чтение файлов копии и сравнение их с печатью в публичном журнале…',
    'Sprawdzam próbkę starszej wersji z pieczęcią w publicznym dzienniku…':
        'Проверка выборки из более старой версии по её печати в публичном журнале…',
    'Audyt z pieczęcią: próbka wersji {label} zgodna z publicznym dziennikiem.':
        'Аудит по печати: выборка из версии {label} совпадает с публичным журналом.',
    'UWAGA — audyt z pieczęcią, wersja {label}: {details}':
        'ВНИМАНИЕ — аудит по печати, версия {label}: {details}',
    'Przekaż…':
        'Передать…',
    'Zapisuje tę wersję pliku i otwiera ją w Sigelith Handover — odbiorca potwierdzi odbiór własnym kluczem':
        'Сохраняет эту версию файла и открывает её в Sigelith Handover — получатель подтвердит получение собственным ключом',
    'Przekazanie z dowodem doręczenia':
        'Передача с доказательством доставки',
    'Przekazanie z dowodem doręczenia robi Sigelith Desktop (od wersji 3.0.1): odbiorca potwierdza odbiór własnym kluczem, a chwila doręczenia trafia do publicznego dziennika. Na tym komputerze go nie ma albo jest w starszej wersji. Otworzyć stronę programu?':
        'Передачу с доказательством доставки выполняет Sigelith Desktop (версии 3.0.1 или новее): получатель подтверждает получение собственным ключом, а момент доставки записывается в публичный журнал. На этом компьютере его нет или установлена более старая версия. Открыть страницу программы?',
    'Zapisz plik do przekazania':
        'Сохранить файл для передачи',
    'Otwieram Sigelith Handover z plikiem „{name}” — wybierz odbiorcę.':
        'Открывается Sigelith Handover с файлом «{name}» — выберите получателя.',
    'Kapsuły czasu…':
        'Капсулы времени…',
    'Pliki zapieczętowane w tej kopii do daty — klucze wydają dopiero po niej sieć drand i serwer kluczy Sigelith':
        'Файлы, запечатанные в этой копии до определённой даты, — ключи выдают только после неё сеть drand и сервер ключей Sigelith',
    'Wskaż najpierw folder kopii — kapsuła leży w kopii.':
        'Сначала укажите папку копии — капсула хранится в копии.',
    'Kapsuły czasu':
        'Капсулы времени',
    'Kapsuła pieczętuje wybrany folder do chwili, którą wskażesz. Otwierają ją dowolne dwie z trzech części: runda sieci drand z tej chwili, udział serwera kluczy Sigelith (wydawany dopiero po tej chwili — to zasada operatora, nie kryptografia) i kod odzyskiwania zapisany obok kapsuły. Kto ma tę kopię, ma więc i kod: do wcześniejszego otwarcia wystarczy mu, że operator złamie swoją zasadę. Po tej chwili otworzy ją każdy, kto ma jej pliki. Kapsuła leży w tej kopii, nie na serwerze; otwiera ją strona sigelith.org/capsule/.':
        'Капсула запечатывает выбранную папку до указанного вами момента. Её открывают любые две из трёх частей: раунд сети drand для этого момента, доля сервера ключей Sigelith (выдаётся только после этого момента — это правило оператора, а не криптография) и код восстановления, сохранённый рядом с капсулой. Поэтому у того, у кого есть эта копия, есть и код: чтобы открыть капсулу раньше срока, ему достаточно, чтобы оператор нарушил своё правило. После этого момента её откроет любой, у кого есть её файлы. Капсула хранится в этой копии, а не на сервере; открывает её страница sigelith.org/capsule/.',
    'Wybierz kapsułę z listy albo utwórz nową.':
        'Выберите капсулу в списке или создайте новую.',
    'Nowa kapsuła…':
        'Новая капсула…',
    'Pieczętuje wybrany folder do daty':
        'Запечатывает выбранную папку до определённой даты',
    'Pokaż w folderze':
        'Показать в папке',
    'Otwiera folder kapsuły w Eksploratorze':
        'Открывает папку капсулы в Проводнике',
    'Otwórz na stronie':
        'Открыть на сайте',
    'Strona sigelith.org/capsule/ otwiera kapsułę po jej dacie':
        'Страница sigelith.org/capsule/ открывает капсулу после её даты',
    'można otworzyć':
        'можно открыть',
    'zamknięta':
        'запечатана',
    'W tej kopii nie ma jeszcze kapsuł czasu.':
        'В этой копии ещё нет капсул времени.',
    'Ta kapsuła da się otworzyć na stronie sigelith.org/capsule/ — wskaż jej pliki.':
        'Эту капсулу можно открыть на странице sigelith.org/capsule/ — укажите там её файлы.',
    'Kapsuła jest zamknięta do daty z listy. Kod odzyskiwania leży w pliku obok niej.':
        'Капсула запечатана до даты, указанной в списке. Код восстановления лежит в файле рядом с ней.',
    'Wybierz folder do zapieczętowania':
        'Выберите папку, которую нужно запечатать',
    'Pieczętuję „{name}” — kilka sekund na krzywej eliptycznej…':
        'Запечатывание «{name}» — несколько секунд на эллиптической кривой…',
    'kapsuła czasu':
        'капсула времени',
    'Kapsuła zapieczętowana':
        'Капсула запечатана',
    '„{name}” otworzy się najwcześniej {when}.\n\nKod odzyskiwania (skopiowany do schowka, zapisany też obok kapsuły):\n\n{code}\n\nZapisz go w bezpiecznym miejscu. Przed datą otwarcia sam niczego nie otwiera; po niej zastępuje jeden z kluczy, gdyby był niedostępny.':
        '«{name}» откроется не раньше {when}.\n\nКод восстановления (скопирован в буфер обмена и сохранён рядом с капсулой):\n\n{code}\n\nСохраните его в надёжном месте. До даты открытия он сам по себе ничего не открывает; после неё он заменяет один из ключей, если тот окажется недоступен.',
    'Nie udało się zapieczętować: {error}':
        'Не удалось запечатать: {error}',
    'Nowa kapsuła czasu':
        'Новая капсула времени',
    'Otworzy się najwcześniej':
        'Откроется не раньше',
    'kapsuła':
        'капсула',
    'Chwila otwarcia musi być w przyszłości.':
        'Момент открытия должен быть в будущем.',
    'Na bieżąco':
        'Непрерывно',
    'Zmiany w folderach źródłowych trafiają do dzisiejszej wersji kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje. Jedna wersja na dzień; ze znacznikami czasu zamyka ją pieczęć następnego dnia.':
        'Изменения в исходных папках попадают в сегодняшнюю версию копии через несколько минут после сохранения, а при подключении диска копия сразу синхронизируется. Одна версия в день; если включены метки времени, на следующий день её закрывает печать.',
    'Na bieżąco — po każdej zmianie i po podłączeniu dysku':
        'Непрерывно — после каждого изменения и при подключении диска',
    'Dla dysku podłączonego na stałe albo często: zmiany trafiają do kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje.':
        'Для диска, подключённого постоянно или часто: изменения попадают в копию через несколько минут после сохранения, а при подключении диска копия сразу синхронизируется.',
    'Kopia będzie na bieżąco: zmiany trafią do dzisiejszej wersji kilka minut po zapisie, a po podłączeniu dysku kopia od razu się zsynchronizuje.':
        'Копия будет обновляться непрерывно: изменения попадут в сегодняшнюю версию через несколько минут после сохранения, а при подключении диска копия сразу синхронизируется.',
    'przywracanie':
        'восстановление',
    'Nowa kopia krok po kroku':
        'Новая копия шаг за шагом',
}
