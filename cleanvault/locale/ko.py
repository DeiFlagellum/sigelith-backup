"""Katalog koreański: „polski tekst źródłowy” → „tekst (koreański)”.

Klucze są te same co w ``en.py`` i muszą dokładnie odpowiadać napisom w kodzie;
pilnuje tego ``tests/test_i18n.py``. Pola w nawiasach klamrowych (``{count}``)
zostają bez zmian. Formaty dat są te same co w Sigelith Desktop.
"""

from __future__ import annotations

TEXTS: dict[str, str] = {
    '\n\nLokalizacja:\n{path}':
        '\n\n위치:\n{path}',
    '\nDo uzupełnienia: niedokończone kopie: {count} — możesz je uzupełnić, wybierając wersję poniżej.':
        '\n보충 필요: 미완료 백업 {count}개 — 아래에서 버전을 선택해 보충할 수 있습니다.',
    '\nUwaga: duży klaster ({size}): każdy mały plik zajmuje co najmniej tyle miejsca. Przy wielu małych plikach kopia zajmie wielokrotnie więcej niż dane.':
        '\n주의: 클러스터가 큽니다({size}). 작은 파일도 하나당 최소 이만큼의 공간을 차지합니다. 작은 파일이 많으면 백업이 실제 데이터보다 몇 배 더 많은 공간을 차지합니다.',
    '\nUwaga: niedokończone wersje (nie zawierają wszystkich plików): {names}':
        '\n주의: 미완료 버전(모든 파일이 들어 있지 않음): {names}',
    '\nUwaga: {filesystem} nie obsługuje twardych dowiązań — każda wersja z datą zajmuje tyle miejsca co pełna kopia.':
        '\n주의: {filesystem} 파일 시스템은 하드 링크를 지원하지 않습니다 — 날짜별 버전마다 전체 백업만큼의 공간을 차지합니다.',
    ' wersji':
        ' 개',
    ' z szyfrowaniem AES-256-GCM…':
        ' (AES-256-GCM 암호화)…',
    ' ×':
        ' 회',
    ' — a ponieważ {filesystem} nie obsługuje twardych dowiązań, zapisze ponownie wszystkie pliki i zajmie tyle miejsca co cała kopia':
        ' — 또한 {filesystem} 파일 시스템은 하드 링크를 지원하지 않으므로 모든 파일을 다시 기록하고 전체 백업만큼의 공간을 차지합니다',
    ' • pozostało {time}':
        ' • {time} 남음',
    '%d.%m %H:%M':
        '%m. %d. %H:%M',
    '%d.%m.%Y':
        '%Y. %m. %d.',
    '%d.%m.%Y %H:%M':
        '%Y. %m. %d. %H:%M',
    ', klaster {size}':
        ', 클러스터 {size}',
    ', uzupełniona {when}':
        ', {when}에 보충됨',
    'Analizuje pliki i pokazuje plan. Nic nie zapisuje.':
        '파일을 분석해 계획을 보여 줍니다. 아무것도 기록하지 않습니다.',
    'Anulowano przed rozpoczęciem kopii.':
        '백업을 시작하기 전에 취소했습니다.',
    'Anuluj':
        '취소',
    'Argon2id (t={passes}, {memory} MiB, p={threads})':
        'Argon2id(t={passes}, {memory} MiB, p={threads})',
    'Argon2id — {passes} przebiegi, {memory} MiB, {threads} wątki':
        'Argon2id — {passes}회 반복, {memory} MiB, 스레드 {threads}개',
    'Automatycznie (język systemu)':
        '자동(시스템 언어)',
    'Bardzo dobre':
        '매우 강함',
    'Bardzo słabe':
        '매우 약함',
    'Brak manifestu — skanuję katalog kopii.':
        '매니페스트가 없습니다 — 백업 폴더를 스캔합니다.',
    'Brakuje tagu uwierzytelniającego — plik jest obcięty.':
        '인증 태그가 없습니다 — 파일이 잘려 있습니다.',
    'Błąd uruchamiania':
        '시작 오류',
    'Ciemny':
        '다크',
    'Co dokładnie zostanie zapisane przy najbliższym przebiegu.':
        '다음 실행 때 기록될 내용을 정확히 보여 줍니다.',
    'Co kopiujemy':
        '백업할 대상',
    'Co zrobić, gdy plik o tej nazwie już istnieje w katalogu docelowym.':
        '대상 폴더에 같은 이름의 파일이 이미 있을 때 어떻게 할지 정합니다.',
    'Czas w nazwie to BeatTime — 1000 beatów na dobę, kotwica w UTC, ten sam moment na całym świecie. Data jest datą UTC, więc zgadza się z zegarem.':
        '이름에 들어가는 시각은 BeatTime입니다 — 하루 1000비트, UTC 기준, 전 세계 어디서나 같은 순간. 날짜도 UTC 날짜이므로 이 시각과 일치합니다.',
    'Czym jest {app}':
        '{app} 소개',
    'Czyści tylko okno — plik dziennika pozostaje':
        '창만 지웁니다 — 로그 파일은 그대로 남습니다',
    'Dane aplikacji: {path}':
        '애플리케이션 데이터: {path}',
    'Decyduje, czy zachowujemy historię wersji.':
        '버전 기록을 보관할지 정합니다.',
    'Dobre':
        '강함',
    'Dodaj folder':
        '폴더 추가',
    'Dodaj przynajmniej jeden folder źródłowy.':
        '원본 폴더를 하나 이상 추가하세요.',
    'Dogrywka zmian z czasu kopii:':
        '백업 중 바뀐 파일 보충:',
    'Dokąd przywracamy':
        '복원할 위치',
    'Dokładnie to, co program realnie stosuje.':
        '프로그램이 실제로 사용하는 방식 그대로입니다.',
    'Domyślne wykluczenia':
        '기본 제외 항목',
    'Domyślne wykluczenia zapisane.':
        '기본 제외 항목을 저장했습니다.',
    'Domyślnie wyłączone. Przy włączonej opcji skasowanie pliku w źródle\nusuwa też jego jedyną kopię zapasową — operacja nieodwracalna.':
        '기본적으로 꺼져 있습니다. 이 옵션을 켜면 원본에서 파일을 삭제할 때\n그 파일의 유일한 백업 사본도 함께 삭제됩니다 — 되돌릴 수 없습니다.',
    'Dopisuj do nazwy katalogu datę ostatniego uzupełnienia':
        '폴더 이름에 마지막 보충 날짜 덧붙이기',
    'Dziennik':
        '로그',
    'Dziennik: {path}':
        '로그: {path}',
    'Ekran przywracania wypełniony danymi szablonu.':
        '템플릿 정보로 복원 화면을 채웠습니다.',
    'Folder docelowy kopii — najlepiej na innym dysku fizycznym.':
        '백업을 저장할 폴더 — 가능하면 다른 물리 드라이브를 사용하세요.',
    'Folder zawierający kopię utworzoną przez {app}.':
        '{app}에서 만든 백업이 들어 있는 폴더입니다.',
    'Gdy plik już istnieje:':
        '파일이 이미 있으면:',
    'Gdzie zapisujemy':
        '저장할 위치',
    'Gotowe do pracy.':
        '준비됨.',
    'Gotowe. Wybierz foldery do kopii.':
        '준비됨. 백업할 폴더를 선택하세요.',
    'Gotowe: {count} {files}, {size}, {seconds} s.':
        '완료: {files} {count}개, {size}, {seconds}초.',
    'Główny folder kopii. Zawiera spis treści (.cleanvault-manifest).':
        '백업 최상위 폴더입니다. 목차(.cleanvault-manifest)가 들어 있습니다.',
    'Hasła nie da się odzyskać ani zresetować. Jeśli je zgubisz, dane z kopii zaszyfrowanej są bezpowrotnie stracone — tak działa poprawne szyfrowanie.':
        '비밀번호는 복구하거나 재설정할 수 없습니다. 비밀번호를 잃어버리면 암호화된 백업의 데이터는 영영 되찾을 수 없습니다 — 제대로 된 암호화는 원래 이렇게 작동합니다.',
    'Hasła w obu polach różnią się.':
        '두 칸에 입력한 비밀번호가 서로 다릅니다.',
    'Hasło':
        '비밀번호',
    'Hasło do kopii':
        '백업 비밀번호',
    'Hasło nie jest nigdzie zapisywane w postaci jawnej.\nBez niego nie da się odzyskać danych — nie istnieje żadna furtka serwisowa.':
        '비밀번호는 어디에도 평문으로 저장되지 않습니다.\n비밀번호 없이는 데이터를 복구할 수 없습니다 — 어떤 뒷문도 없습니다.',
    'Hasło nie może być puste.':
        '비밀번호를 비워 둘 수 없습니다.',
    'Hasło niezapisane':
        '비밀번호가 저장되지 않음',
    'Hasło powinno mieć co najmniej 8 znaków.':
        '비밀번호는 8자 이상이어야 합니다.',
    'Hasło trafia do magazynu systemowego powiązanego z Twoim kontem.\nNigdy nie jest zapisywane w plikach programu.':
        '비밀번호는 사용자 계정에 연결된 시스템 저장소에 보관됩니다.\n프로그램 파일에는 절대 기록되지 않습니다.',
    'Hasło użyte przy tworzeniu kopii':
        '백업을 만들 때 사용한 비밀번호',
    'Ile plików kopia przetwarza jednocześnie. Przy setkach tysięcy małych plików\nczas kopii to głównie opóźnienia na każdy plik (otwarcie, skanowanie\nantywirusowe, zapis na nośnik), a nie przesył danych — praca równoległa\nskraca go kilkukrotnie.\n\n„automatycznie” dobiera liczbę do procesora (do 32). Na wolnym dysku\ntalerzowym mniejsza wartość (2–4) bywa szybsza.':
        '백업이 동시에 처리하는 파일 수입니다. 작은 파일이 수십만 개라면\n백업 시간은 데이터 전송보다 파일마다 생기는 지연(열기, 바이러스\n검사, 저장 매체에 기록)이 대부분을 차지합니다. 병렬로 처리하면\n이 시간이 몇 배 줄어듭니다.\n\n‘자동’은 프로세서에 맞춰 개수를 정합니다(최대 32). 느린 하드\n디스크에서는 더 작은 값(2–4)이 더 빠를 때가 있습니다.',
    'Informacje przydatne przy zgłaszaniu problemu.':
        '문제를 신고할 때 유용한 정보입니다.',
    'Jak to działa':
        '작동 방식',
    'Jasny':
        '라이트',
    'Jeden folder utrzymywany w zgodzie ze źródłem. Brak historii wersji,\nza to najprostsza struktura i najmniejsze zużycie miejsca.':
        '원본과 똑같이 유지되는 폴더 하나입니다. 버전 기록은 없지만\n구조가 가장 단순하고 공간도 가장 적게 차지합니다.',
    'Jeśli operacja zakończy się błędem, skopiuj stąd ostatnie wiersze — zawierają dokładną przyczynę, a nie tylko komunikat ogólny.':
        '작업이 오류로 끝나면 여기서 마지막 몇 줄을 복사하세요 — 일반적인 메시지가 아니라 정확한 원인이 들어 있습니다.',
    'Język interfejsu zmieniony.':
        '인터페이스 언어를 변경했습니다.',
    'Język zmienisz po zakończeniu bieżącej operacji.':
        '현재 작업이 끝난 뒤에 언어를 변경할 수 있습니다.',
    'Język:':
        '언어:',
    'Katalog docelowy leży wewnątrz źródła ({path}). Kopia kopiowałaby samą siebie w nieskończoność.':
        '대상 폴더가 원본 안에 있습니다({path}). 백업이 자기 자신을 끝없이 복사하게 됩니다.',
    'Katalog docelowy nie może być tym samym katalogiem co źródłowy.':
        '대상 폴더는 원본 폴더와 같을 수 없습니다.',
    'Katalog jeszcze nie istnieje — zostanie utworzony.':
        '폴더가 아직 없습니다 — 새로 만들어집니다.',
    'Katalog kopii nie istnieje: {path}':
        '백업 폴더가 없습니다: {path}',
    'Katalog źródłowy nie istnieje: {path}':
        '원본 폴더가 없습니다: {path}',
    'Katalog, w którym pojawią się odtworzone pliki.':
        '복원된 파일이 저장될 폴더입니다.',
    'Katalog, w którym powstanie kopia. Nie może leżeć wewnątrz folderu źródłowego.':
        '백업이 만들어질 폴더입니다. 원본 폴더 안에 있으면 안 됩니다.',
    'Katalogi objęte kopią.\nMożesz przeciągnąć foldery z Eksploratora Windows wprost na tę listę.':
        '백업 대상 폴더입니다.\n파일 탐색기에서 폴더를 이 목록으로 바로 끌어 올 수 있습니다.',
    'Każdy folder z datą jest kompletny — przywracanie nie wymaga sklejania wersji.':
        '날짜별 폴더는 각각 완전합니다 — 복원할 때 여러 버전을 이어 붙일 필요가 없습니다.',
    'Każdy plik jest czytany ponownie zaraz po zapisaniu. Dane pochodzą wtedy\nzwykle z pamięci podręcznej systemu, więc niewiele mówi to o nośniku,\na wydłuża kopię nawet dwukrotnie.\n\nSkuteczniejsza jest weryfikacja odroczona: ekran „Przywracanie” →\n„Sprawdź kopię”, najlepiej po ponownym podłączeniu dysku.':
        '각 파일을 기록한 직후 다시 읽습니다. 이때 데이터는 대개\n시스템 캐시에서 오므로 저장 매체에 대해 알려 주는 것은 별로 없고,\n백업 시간만 최대 두 배로 늘어납니다.\n\n나중에 검증하는 편이 더 효과적입니다: ‘복원’ 화면 →\n‘백업 확인’, 가능하면 드라이브를 다시 연결한 뒤에 하세요.',
    'Każdy plik trafia do kopii jako zaszyfrowany kontener .cvlt.\nKlucz powstaje z hasła przez Argon2id.':
        '모든 파일은 암호화된 .cvlt 컨테이너로 백업에 저장됩니다.\n키는 Argon2id로 비밀번호에서 파생됩니다.',
    'Każdy przebieg tworzy osobny folder z datą i godziną.\nPliki niezmienione są podpinane twardym dowiązaniem, więc historia\nzajmuje tyle miejsca, ile realnie się zmieniło.':
        '실행할 때마다 날짜와 시각이 붙은 별도 폴더를 만듭니다.\n바뀌지 않은 파일은 하드 링크로 연결하므로 기록은\n실제로 바뀐 만큼만 공간을 차지합니다.',
    'Klaster nośnika to {cluster} — pliki zajmą {actual} zamiast {logical} (narzut {overhead}).':
        '저장 매체의 클러스터 크기는 {cluster}입니다 — 파일이 {logical} 대신 {actual}만큼 공간을 차지합니다(오버헤드 {overhead}).',
    'Kliknij szablon, aby zobaczyć jego szczegóły.':
        '템플릿을 클릭하면 세부 정보가 표시됩니다.',
    'Kliknij „Podgląd zmian”, aby sprawdzić plan bez zapisywania czegokolwiek.':
        '아무것도 기록하지 않고 계획을 확인하려면 ‘변경 사항 미리 보기’를 클릭하세요.',
    'Kolor wyróżnienia':
        '강조 색',
    'Kolor wyróżnienia…':
        '강조 색…',
    'Kopia':
        '백업',
    'Kopia do dokończenia':
        '미완료 백업',
    'Kopia jest aktualna — nie ma czego zapisywać.':
        '백업이 최신 상태입니다 — 기록할 것이 없습니다.',
    'Kopia jest zaszyfrowana — podaj hasło użyte przy jej tworzeniu.':
        '암호화된 백업입니다 — 백업을 만들 때 사용한 비밀번호를 입력하세요.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją przywrócić.':
        '암호화된 백업입니다 — 복원하려면 비밀번호를 입력하세요.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją zweryfikować.':
        '암호화된 백업입니다 — 검증하려면 비밀번호를 입력하세요.',
    'Kopia jest zaszyfrowana — podaj hasło.':
        '암호화된 백업입니다 — 비밀번호를 입력하세요.',
    'Kopia lustrzana':
        '미러 백업',
    'Kopia nie została uruchomiona.':
        '백업을 시작하지 않았습니다.',
    'Kopia wykonana. Uruchom podgląd ponownie, aby sprawdzić stan.':
        '백업을 마쳤습니다. 상태를 확인하려면 미리 보기를 다시 실행하세요.',
    'Kopia zapasowa':
        '백업',
    'Kopia {folder}':
        '{folder} 백업',
    'Kopia {kind} • {count} {files} • {size} • ostatnia aktualizacja {when}\nŹródła: {roots}':
        '백업: {kind} • {files} {count}개 • {size} • 마지막 업데이트 {when}\n원본: {roots}',
    'Kopiowane są wyłącznie pliki nowe i zmienione od ostatniego przebiegu.':
        '마지막 실행 이후 새로 생기거나 바뀐 파일만 복사합니다.',
    'Kopiuje ustawienia szablonu na ekran „Kopia zapasowa”':
        '템플릿 설정을 ‘백업’ 화면으로 가져옵니다',
    'Kopię możesz sprawdzić później: ekran „Przywracanie” → „Sprawdź kopię”. Najlepiej po ponownym podłączeniu dysku — wtedy dane są czytane z nośnika.':
        '백업은 나중에 확인할 수 있습니다: ‘복원’ 화면 → ‘백업 확인’. 드라이브를 다시 연결한 뒤에 하는 것이 가장 좋습니다 — 그래야 데이터를 실제로 저장 매체에서 읽습니다.',
    'Kryptografia':
        '암호 기술',
    'Lista podpowiadana przy tworzeniu nowej kopii.':
        '새 백업을 설정할 때 제안되는 목록입니다.',
    'Magazyn haseł: {backend}':
        '비밀번호 저장소: {backend}',
    'Magazyn systemowy: {backend}':
        '시스템 저장소: {backend}',
    'Menedżer poświadczeń Windows (DPAPI, powiązany z kontem użytkownika).':
        'Windows 자격 증명 관리자(DPAPI, 사용자 계정에 연결됨).',
    'Miejsce i układ odtwarzanych plików.':
        '복원할 파일의 위치와 배치.',
    'Motyw zmieniony na {theme}.':
        '테마를 변경했습니다: {theme}.',
    'Motyw:':
        '테마:',
    'Możesz też przeciągnąć foldery z Eksploratora Windows wprost na listę.':
        '파일 탐색기에서 폴더를 목록으로 바로 끌어 올 수도 있습니다.',
    'Można ją dokończyć — zostaną dograne tylko brakujące i zmienione pliki.':
        '이어서 완료할 수 있습니다 — 빠졌거나 바뀐 파일만 추가로 기록합니다.',
    'Na nośniku docelowym zajmie to ok. {size}.':
        '대상 저장 매체에서 차지할 공간: 약 {size}.',
    'Nadpisywanie plików':
        '파일 덮어쓰기',
    'Nadpisz istniejące pliki':
        '기존 파일 덮어쓰기',
    'Nazwa szablonu':
        '템플릿 이름',
    'Nazwa szablonu nie może być pusta.':
        '템플릿 이름을 비워 둘 수 없습니다.',
    'Nazwa szablonu zapisana.':
        '템플릿 이름을 저장했습니다.',
    'Nazwa szablonu:':
        '템플릿 이름:',
    'Nie ma wersji kopii o nazwie {name} w katalogu {path}.':
        '{path} 폴더에 이름이 {name}인 백업 버전이 없습니다.',
    'Nie można odczytać informacji o dysku: {error}':
        '드라이브 정보를 읽을 수 없습니다: {error}',
    'Nie udało się uruchomić programu — brakuje biblioteki: {error}\nZainstaluj zależności poleceniem:  pip install -r requirements.txt':
        '프로그램을 시작하지 못했습니다 — 라이브러리가 없습니다: {error}\n다음 명령으로 종속성을 설치하세요:  pip install -r requirements.txt',
    'Nie udało się wykonać operacji':
        '작업을 완료하지 못했습니다',
    'Nie udało się zapisać hasła w magazynie systemowym.\nSzablon działa normalnie — program poprosi o hasło przy uruchomieniu.':
        '비밀번호를 시스템 저장소에 저장하지 못했습니다.\n템플릿은 정상적으로 작동하며, 실행할 때 프로그램이 비밀번호를 묻습니다.',
    'Nie udało się znaleźć wolnej nazwy dla {path}':
        '{path}에 사용할 수 있는 이름을 찾지 못했습니다',
    'Nie wskazano katalogu docelowego.':
        '대상 폴더를 지정하지 않았습니다.',
    'Nie wskazano żadnego katalogu źródłowego.':
        '원본 폴더를 하나도 지정하지 않았습니다.',
    'Nie wybrano katalogu':
        '선택한 폴더 없음',
    'Nie wybrano szablonu':
        '선택한 템플릿 없음',
    'Nie znaleziono spisu treści kopii — program przeskanuje folder i rozpozna pliki po ich zawartości.':
        '백업 목차를 찾지 못했습니다 — 프로그램이 폴더를 스캔해 내용으로 파일을 알아냅니다.',
    'Nie znam oryginalnej lokalizacji dla {key} — wybierz inny układ przywracania.':
        '{key}의 원래 위치를 알 수 없습니다 — 다른 복원 배치를 선택하세요.',
    'Niedostępny — backend {backend} nie gwarantuje poufności.':
        '사용할 수 없음 — {backend} 백엔드는 기밀성을 보장하지 않습니다.',
    'Niedostępny — brak biblioteki keyring.':
        '사용할 수 없음 — keyring 라이브러리가 없습니다.',
    'Nieznany algorytm wyprowadzania klucza: {name}':
        '알 수 없는 키 파생 알고리즘: {name}',
    'Nowa wersja z datą':
        '새 날짜별 버전',
    'Nowa wersja z datą to kopia od początku do osobnego folderu':
        '새 날짜별 버전을 만들면 별도 폴더에 처음부터 다시 백업합니다',
    'Nowa wersja z datą — kopia do nowego folderu.\nWybrana istniejąca wersja — dogrywa do niej tylko brakujące i zmienione\npliki, a pliki różniące się od źródła nadpisuje. Tak dokończysz przerwaną\nkopię albo uzupełnisz ją o dane, które powstały w trakcie jej wykonywania.':
        '새 날짜별 버전 — 새 폴더에 백업합니다.\n기존 버전 — 빠졌거나 바뀐 파일만 그 버전에 추가하고,\n원본과 다른 파일은 덮어씁니다. 이렇게 중단된 백업을 마치거나\n백업하는 동안 새로 생긴 데이터로 보충할 수 있습니다.',
    'Nowy szablon':
        '새 템플릿',
    'Nośnik docelowy ({filesystem}) nie obsługuje twardych dowiązań, więc każda wersja z datą jest pełną kopią. Te {count} niezmienionych plików zostanie powielone ({size}). Rozważ układ „kopia lustrzana” albo nośnik NTFS.':
        '대상 저장 매체({filesystem})가 하드 링크를 지원하지 않으므로 날짜별 버전마다 전체 사본이 됩니다. 바뀌지 않은 파일 {count}개가 중복 저장됩니다({size}). ‘미러 백업’ 구조나 NTFS 저장 매체를 고려하세요.',
    'O programie':
        '정보',
    'Obsługiwane są wzorce w stylu Windows:\n  *.tmp          — wszystkie pliki tymczasowe\n  Thumbs.db      — konkretna nazwa\n  node_modules/* — cały folder wraz z zawartością':
        'Windows 방식의 패턴을 지원합니다:\n  *.tmp          — 모든 임시 파일\n  Thumbs.db      — 특정 이름 하나\n  node_modules/* — 폴더 전체와 그 내용',
    'Ochrona danych':
        '데이터 보호',
    'Odczytuje wszystkie pliki kopii i weryfikuje ich poprawność.\nNic nie zapisuje na dysku.':
        '백업의 모든 파일을 읽어 손상 여부를 검증합니다.\n디스크에 아무것도 기록하지 않습니다.',
    'Odpowiednik synchronizacji folderu. Wcześniejsze wersje plików nie są zachowywane.':
        '폴더 동기화와 같은 방식입니다. 파일의 이전 버전은 보관하지 않습니다.',
    'Odtwarza pliki z kopii — również z kopii zaszyfrowanej.':
        '백업에서 파일을 복원합니다 — 암호화된 백업도 가능합니다.',
    'Odtwarza pliki zgodnie z ustawieniami powyżej':
        '위 설정대로 파일을 복원합니다',
    'Odtwórz pełną strukturę folderów':
        '전체 폴더 구조 그대로 복원',
    'Odtwórz pliki z istniejącej kopii':
        '기존 백업에서 파일 복원',
    'Operacja nie powiodła się.':
        '작업에 실패했습니다.',
    'Operacja przerwana przez użytkownika.':
        '사용자가 작업을 중단했습니다.',
    'Operacja przerwana — utrwalam stan dotychczas zapisanych plików.':
        '작업 중단됨 — 지금까지 기록한 파일의 상태를 저장합니다.',
    'Operacja w toku':
        '작업 진행 중',
    'Operacja zakończona błędem.':
        '작업이 오류로 끝났습니다.',
    'Ostatnie operacje':
        '최근 작업',
    'Otwiera ekran przywracania z wypełnionymi ścieżkami':
        '경로가 채워진 복원 화면을 엽니다',
    'Otwiera pełny dziennik w domyślnym edytorze':
        '기본 편집기에서 전체 로그를 엽니다',
    'Otwórz katalog danych':
        '데이터 폴더 열기',
    'Otwórz katalog dziennika':
        '로그 폴더 열기',
    'Otwórz okno wyboru katalogu':
        '폴더 선택 창 열기',
    'Otwórz plik dziennika':
        '로그 파일 열기',
    'PBKDF2-HMAC-SHA256 ({count} iteracji)':
        'PBKDF2-HMAC-SHA256({count}회 반복)',
    'PBKDF2-HMAC-SHA256 — {count} iteracji':
        'PBKDF2-HMAC-SHA256 — {count}회 반복',
    'PBKDF2-HMAC-SHA256, {count} iteracji':
        'PBKDF2-HMAC-SHA256, {count}회 반복',
    'Pełna struktura — układ jak w źródle, wewnątrz wskazanego katalogu.\nJeden folder — wygodne, gdy szukasz kilku plików.\nPierwotne lokalizacje — zapisuje pliki tam, skąd zostały pobrane.':
        '전체 구조 — 원본과 같은 배치로, 지정한 폴더 안에 복원합니다.\n폴더 하나 — 파일 몇 개를 찾을 때 편리합니다.\n원래 위치 — 파일을 원래 있던 곳에 다시 기록합니다.',
    'Pierwszy przebieg kopiuje wszystko i trwa najdłużej. Kolejne porównują rozmiar i datę modyfikacji, więc zwykle kończą się w kilka sekund.':
        '첫 실행은 모든 것을 복사하므로 가장 오래 걸립니다. 그다음부터는 크기와 수정 날짜를 비교하므로 보통 몇 초 만에 끝납니다.',
    'Plan gotowy: {count} {files} do zapisania.':
        '계획 준비 완료: 기록할 {files} {count}개.',
    'Plik jest za krótki, by być kontenerem tego programu.':
        '파일이 너무 짧아 이 프로그램의 컨테이너일 수 없습니다.',
    'Plik skończył się wcześniej, niż deklaruje nagłówek.':
        '파일이 헤더에 선언된 것보다 일찍 끝납니다.',
    'Plik w formacie w wersji {found}; ta wersja programu obsługuje {supported}.':
        '파일 형식 버전: {found}. 이 버전의 프로그램이 지원하는 형식: {supported}.',
    'Plik wymaga Argon2id, a biblioteka argon2-cffi jest niedostępna.':
        '파일에 Argon2id가 필요하지만 argon2-cffi 라이브러리를 사용할 수 없습니다.',
    'Pliki pominięte — kopia jest aktualna':
        '건너뛸 파일 — 백업이 이미 최신 상태입니다',
    'Pliki trafią do wskazanego katalogu z zachowaniem struktury folderów.':
        '파일이 폴더 구조를 유지한 채 지정한 폴더에 복원됩니다.',
    'Pliki wrócą dokładnie tam, skąd pochodzą. Katalog docelowy zostanie zignorowany.':
        '파일이 원래 있던 곳으로 정확히 돌아갑니다. 대상 폴더는 무시됩니다.',
    'Pliki zmienione od ostatniego przebiegu':
        '마지막 실행 이후 바뀐 파일',
    'Pliki zostaną zapisane dokładnie tam, skąd pochodzą.\n\nKonflikty nazw: {collision}.\n\nCzy kontynuować?':
        '파일이 원래 있던 곳에 그대로 기록됩니다.\n\n이름 충돌: {collision}.\n\n계속할까요?',
    'Pliki, których jeszcze nie ma w kopii':
        '아직 백업에 없는 파일',
    'Po uzupełnieniu istniejącej wersji jej katalog nazywa się np.\n  2026-09-17_@687--2026-09-24_@921\nczyli: data utworzenia kopii i data ostatniego uzupełnienia.\n\nData utworzenia zostaje z przodu, więc katalogi nadal układają się\nchronologicznie. Widać to w Eksploratorze bez uruchamiania programu.':
        '기존 버전을 보충하면 그 폴더 이름은 예를 들어 다음과 같습니다.\n  2026-09-17_@687--2026-09-24_@921\n즉, 백업을 만든 날짜와 마지막으로 보충한 날짜입니다.\n\n만든 날짜가 앞에 오므로 폴더는 계속\n시간순으로 정렬됩니다. 프로그램을 실행하지 않아도 파일 탐색기에서 볼 수 있습니다.',
    'Po wykonaniu kopii zostanie mało wolnego miejsca ({free}).':
        '백업 후 남는 여유 공간이 적습니다({free}).',
    'Po zakończeniu kopii program ponownie skanuje źródło i dogrywa do tej samej\nwersji pliki, które w międzyczasie powstały lub się zmieniły.\nPrzydatne, gdy pracujesz na danych w trakcie wielogodzinnej kopii.\nPlik zmieniony w trakcie własnego kopiowania nigdy nie jest uznawany za zapisany.':
        '백업이 끝나면 프로그램이 원본을 다시 스캔해, 그사이 새로 생기거나 바뀐 파일을\n같은 버전에 추가로 기록합니다.\n몇 시간씩 걸리는 백업 중에도 데이터로 작업할 때 유용합니다.\n복사되는 도중에 바뀐 파일은 절대 기록된 것으로 간주하지 않습니다.',
    'Poczekaj na zakończenie bieżącej operacji.':
        '현재 작업이 끝날 때까지 기다리세요.',
    'Podaj hasło dla szablonu „{name}”:':
        '‘{name}’ 템플릿의 비밀번호를 입력하세요:',
    'Podaj hasło — bez niego nie można zaszyfrować kopii.':
        '비밀번호를 입력하세요 — 비밀번호가 없으면 백업을 암호화할 수 없습니다.',
    'Podane hasło nie pasuje do plików zapisanych wcześniej w tej kopii. Wznowienie z innym hasłem zostawiłoby w jednej kopii pliki pod dwoma hasłami. Podaj hasło użyte przy poprzednim przebiegu albo utwórz kopię w nowym katalogu.':
        '입력한 비밀번호가 이 백업에 이전에 기록된 파일과 맞지 않습니다. 다른 비밀번호로 이어서 진행하면 한 백업 안에 서로 다른 두 비밀번호로 된 파일이 섞이게 됩니다. 이전 실행 때 사용한 비밀번호를 입력하거나 새 폴더에 백업을 만드세요.',
    'Podgląd zmian':
        '변경 사항 미리 보기',
    'Pokazuje folder z plikami dziennika':
        '로그 파일이 있는 폴더를 보여 줍니다',
    'Pokazuje folder z ustawieniami i szablonami':
        '설정과 템플릿이 있는 폴더를 보여 줍니다',
    'Pokaż / ukryj wpisane hasło':
        '입력한 비밀번호 표시/숨기기',
    'Pomiń istniejące pliki':
        '기존 파일 건너뛰기',
    'Potwierdź usuwanie':
        '삭제 확인',
    'Powtórz hasło':
        '비밀번호 다시 입력',
    'Program nie mógł się uruchomić:\n\n{error}\n\nSzczegóły zapisano w dzienniku aplikacji.':
        '프로그램을 시작할 수 없습니다:\n\n{error}\n\n자세한 내용은 애플리케이션 로그에 기록했습니다.',
    'Program nie wie, czy ta kopia została dokończona. Uzupełnienie jej dogra tylko brakujące i zmienione pliki, a tego, co już jest zapisane, nie kopiuje ponownie.':
        '이 백업이 완료되었는지 프로그램이 알 수 없습니다. 보충하면 빠졌거나 바뀐 파일만 추가로 기록하고, 이미 기록된 것은 다시 복사하지 않습니다.',
    'Program sam wykryje, czy kopia jest zaszyfrowana.':
        '백업이 암호화되었는지는 프로그램이 알아서 감지합니다.',
    'Przebieg operacji i diagnostyka':
        '작업 진행 상황과 진단',
    'Przebieg operacji na żywo. Pełna historia trafia do pliku.':
        '작업 진행 상황을 실시간으로 보여 줍니다. 전체 기록은 파일에 저장됩니다.',
    'Przebieg uzupełniający: {error}':
        '보충 실행: {error}',
    'Przeciętne':
        '보통',
    'Przerwano liczenie sumy kontrolnej.':
        '체크섬 계산을 중단했습니다.',
    'Przerwano skanowanie.':
        '스캔을 중단했습니다.',
    'Przerwano. Zapisano {count} {files} ({size}).':
        '중단했습니다. {files} {count}개({size})를 기록했습니다.',
    'Przerwij':
        '중지',
    'Przerywanie operacji…':
        '작업을 중지하는 중…',
    'Przerywanie — zapisuję spis treści kopii, nie wyłączaj komputera…':
        '중지하는 중 — 백업 목차를 저장하고 있으니 컴퓨터를 끄지 마세요…',
    'Przeskanowano {count} {files}.':
        '{files} {count}개를 스캔했습니다.',
    'Przygotowanie…':
        '준비 중…',
    'Przywracanie':
        '복원',
    'Przywracanie do pierwotnych lokalizacji':
        '원래 위치로 복원',
    'Przywracanie przerwane.':
        '복원을 중단했습니다.',
    'Przywracanie {count} {files} ({size})…':
        '{files} {count}개({size}) 복원 중…',
    'Przywróć do pierwotnych lokalizacji':
        '원래 위치로 복원',
    'Przywróć domyślne':
        '기본값 복원',
    'Przywróć fabryczne':
        '내장 목록 복원',
    'Przywróć pliki':
        '파일 복원',
    'Przywróć z tej kopii':
        '이 백업에서 복원',
    'Pusta nazwa':
        '빈 이름',
    'Równoległe operacje:':
        '병렬 작업:',
    'Skanowanie plików źródłowych…':
        '원본 파일을 스캔하는 중…',
    'Skrót z dziennika — pełny zapis znajdziesz w zakładce „Dziennik”.':
        '로그 요약 — 전체 기록은 ‘로그’ 화면에서 볼 수 있습니다.',
    'Skąd przywracamy':
        '복원할 백업',
    'Sprawdzam, co zmieniło się w źródle w trakcie kopii (przebieg uzupełniający {attempt} z {passes})…':
        '백업 중에 원본에서 바뀐 내용을 확인하는 중(보충 실행 {passes}회 중 {attempt}회째)…',
    'Sprawdzam, czy hasło zgadza się z hasłem wcześniej zapisanych plików…':
        '비밀번호가 이전에 기록된 파일의 비밀번호와 일치하는지 확인하는 중…',
    'Sprawdzam, czy w katalogu docelowym jest kopia do dokończenia…':
        '대상 폴더에 완료할 백업이 있는지 확인하는 중…',
    'Sprawdź hasło':
        '비밀번호 확인',
    'Sprawdź kopię':
        '백업 확인',
    'Szablon przechowuje foldery, opcje i wykluczenia. Hasło nigdy nie trafia do szablonu — jest przechowywane w Menedżerze poświadczeń Windows albo wpisywane przy każdym uruchomieniu.':
        '템플릿에는 폴더, 옵션, 제외 항목이 저장됩니다. 비밀번호는 템플릿에 절대 들어가지 않으며, Windows 자격 증명 관리자에 보관되거나 실행할 때마다 입력합니다.',
    'Szablon usunięty.':
        '템플릿을 삭제했습니다.',
    'Szablon „{name}”':
        '‘{name}’ 템플릿',
    'Szablon „{name}” już istnieje.\n\nZastąpić go bieżącymi ustawieniami z formularza?':
        '‘{name}’ 템플릿이 이미 있습니다.\n\n양식의 현재 설정으로 바꿀까요?',
    'Szablon „{name}” zostanie usunięty.\n\nPliki kopii zapasowej pozostaną nienaruszone.':
        '‘{name}’ 템플릿이 삭제됩니다.\n\n백업 파일은 그대로 남습니다.',
    'Szablony':
        '템플릿',
    'Szablony: {count}\nSzyfrowanie: AES-256-GCM\nKlucz: {kdf}':
        '템플릿: {count}개\n암호화: AES-256-GCM\n키: {kdf}',
    'Szyfrowanie i kontrola poprawności zapisu.':
        '암호화와 기록 검증.',
    'Szyfrowanie: AES-256-GCM (uwierzytelnione)\nWyprowadzanie klucza: {kdf}':
        '암호화: AES-256-GCM(인증 암호화)\n키 파생: {kdf}',
    'Szyfruj kopię (AES-256-GCM)':
        '백업 암호화(AES-256-GCM)',
    'Słabe':
        '약함',
    'Ta kopia nie jest zaszyfrowana — hasło nie jest potrzebne.':
        '암호화되지 않은 백업입니다 — 비밀번호가 필요 없습니다.',
    'Ten folder jest już na liście.':
        '이 폴더는 이미 목록에 있습니다.',
    'To nie jest plik zaszyfrowany przez ten program.':
        '이 프로그램으로 암호화한 파일이 아닙니다.',
    'Trwa inna operacja — poczekaj na jej zakończenie.':
        '다른 작업이 진행 중입니다 — 끝날 때까지 기다리세요.',
    'Trwa operacja':
        '작업 진행 중',
    'Trwa operacja na plikach. Zamknięcie programu ją przerwie.\n\nPliki zapisane do tej chwili zostaną zachowane, a kopię będzie można później dokończyć.\n\nZamknąć mimo to?':
        '파일 작업이 진행 중입니다. 프로그램을 닫으면 작업이 중단됩니다.\n\n지금까지 기록한 파일은 그대로 남으며, 백업은 나중에 마저 완료할 수 있습니다.\n\n그래도 닫을까요?',
    'Trwa: {description}…':
        '진행 중: {description}…',
    'Tryb dokładny — licz sumę kontrolną każdego pliku':
        '정밀 모드 — 모든 파일의 체크섬 계산',
    'Układ kopii':
        '백업 구조',
    'Układ plików:':
        '파일 배치:',
    'Uruchom kopię':
        '백업 실행',
    'Ustawienia':
        '설정',
    'Usunąć szablon?':
        '템플릿을 삭제할까요?',
    'Usuwa pozycję z listy. Nie kasuje żadnych plików.':
        '목록에서 항목을 제거합니다. 파일은 삭제하지 않습니다.',
    'Usuwa szablon. Nie kasuje żadnych plików kopii.':
        '템플릿을 삭제합니다. 백업 파일은 삭제하지 않습니다.',
    'Usuwaj z kopii pliki skasowane w źródle':
        '원본에서 삭제된 파일을 백업에서도 삭제',
    'Usuń':
        '삭제',
    'Usuń zaznaczone':
        '선택 항목 제거',
    'Uszkodzony nagłówek pliku.':
        '파일 헤더가 손상되었습니다.',
    'Utwórz lub zaktualizuj kopię wybranych folderów':
        '선택한 폴더의 백업 생성 또는 업데이트',
    'Utwórz nową wersję':
        '새 버전 만들기',
    'Uzupełnienie istniejącej wersji nie kopiuje ponownie tego, co już w niej jest — dokończysz przerwaną kopię bez tworzenia kolejnej pełnej wersji.':
        '기존 버전을 보충하면 이미 들어 있는 것은 다시 복사하지 않습니다 — 전체 버전을 새로 만들지 않고도 중단된 백업을 마칠 수 있습니다.',
    'Uzupełnij tę wersję':
        '이 버전 보충',
    'Uzupełnij: {version} • {labels}':
        '보충: {version} • {labels}',
    'W katalogu docelowym jest kopia tych samych folderów zapisana starszą wersją programu:':
        '대상 폴더에 이전 버전의 프로그램으로 기록한 같은 폴더의 백업이 있습니다:',
    'W katalogu docelowym jest niedokończona kopia tych samych folderów:':
        '대상 폴더에 같은 폴더의 미완료 백업이 있습니다:',
    'W tym katalogu nie ma spisu treści kopii — nie ma z czym porównać plików.':
        '이 폴더에는 백업 목차가 없습니다 — 파일을 비교할 기준이 없습니다.',
    'Wczytaj do formularza':
        '양식으로 불러오기',
    'Wczytano manifest kopii: {count} {files}.':
        '백업 매니페스트를 불러왔습니다: {files} {count}개.',
    'Wczytano szablon „{name}” do formularza.':
        '‘{name}’ 템플릿을 양식으로 불러왔습니다.',
    'Wersja kopii nosi teraz nazwę {name}.':
        '이제 백업 버전의 이름은 {name}입니다.',
    'Wersja, licencja i użyta kryptografia':
        '버전, 라이선스, 사용한 암호 기술',
    'Wersje z datą (zalecane)':
        '날짜별 버전(권장)',
    'Weryfikacja kopii':
        '백업 검증',
    'Weryfikacja nie powiodła się: nieprawidłowe hasło lub uszkodzony plik.':
        '검증 실패: 비밀번호가 틀렸거나 파일이 손상되었습니다.',
    'Weryfikacja po zapisie nie powiodła się — zapisane dane różnią się od źródła.':
        '기록 후 검증에 실패했습니다 — 기록된 데이터가 원본과 다릅니다.',
    'Weryfikacja {count} {files} ({size}), {threads} równolegle…':
        '{files} {count}개({size}) 검증 중, 병렬 작업 {threads}개…',
    'Weryfikuj natychmiast po zapisie (spowalnia kopię)':
        '기록 직후 바로 검증(백업이 느려짐)',
    'Wolne miejsce: {free} z {total}':
        '여유 공간: {total} 중 {free}',
    'Wolniejszy, ale wykrywa zmiany, które nie zmieniły rozmiaru ani daty\n(np. po przywróceniu pliku z innego nośnika).':
        '느리지만 크기나 날짜가 바뀌지 않은 변경도 찾아냅니다\n(예: 다른 저장 매체에서 파일을 복원한 경우).',
    'Wpis {key} w spisie treści kopii wskazuje poza katalog docelowy — pomijam go.':
        '백업 목차의 {key} 항목이 대상 폴더 밖을 가리킵니다 — 건너뜁니다.',
    'Wraca do listy wbudowanej w program':
        '프로그램에 내장된 목록으로 되돌립니다',
    'Wskaż folder kopii, aby zobaczyć jej zawartość.':
        '내용을 보려면 백업 폴더를 지정하세요.',
    'Wskaż folder kopii.':
        '백업 폴더를 지정하세요.',
    'Wskaż foldery objęte kopią. Podfoldery są uwzględniane automatycznie.':
        '백업할 폴더를 지정하세요. 하위 폴더는 자동으로 포함됩니다.',
    'Wskaż główny folder kopii (ten, który wybrałeś jako cel), a nie pojedynczy folder z datą. Program sam odczyta spis treści kopii.':
        '날짜별 폴더 하나가 아니라 백업 최상위 폴더(대상으로 선택했던 폴더)를 지정하세요. 백업 목차는 프로그램이 알아서 읽습니다.',
    'Wskaż katalog docelowy kopii.':
        '백업 대상 폴더를 지정하세요.',
    'Wskaż katalog docelowy.':
        '대상 폴더를 지정하세요.',
    'Wstawia zalecaną listę wykluczeń':
        '권장 제외 목록을 넣습니다',
    'Wszystkie pliki wylądują bezpośrednio w katalogu docelowym, bez podfolderów.':
        '모든 파일이 하위 폴더 없이 대상 폴더에 바로 들어갑니다.',
    'Wszystko do jednego folderu':
        '모두 한 폴더에',
    'Wybierz folder do kopii':
        '백업할 폴더 선택',
    'Wybierz folder kopii':
        '백업 폴더 선택',
    'Wybierz katalog':
        '폴더 선택',
    'Wybierz katalog docelowy':
        '대상 폴더 선택',
    'Wybierz katalog docelowy kopii':
        '백업 대상 폴더 선택',
    'Wybierz katalog, aby zobaczyć dostępne miejsce.':
        '사용 가능한 공간을 보려면 폴더를 선택하세요.',
    'Wybierz kolejny folder do kopii':
        '백업할 폴더 하나 더 선택',
    'Wybierz szablon z listy.':
        '목록에서 템플릿을 선택하세요.',
    'Wybierz…':
        '선택…',
    'Wybrano nadpisywanie istniejących plików. Ich obecna zawartość zostanie bezpowrotnie zastąpiona.\n\nCzy kontynuować?':
        '기존 파일 덮어쓰기를 선택했습니다. 지금의 내용은 되돌릴 수 없게 대체됩니다.\n\n계속할까요?',
    'Wyczyść widok':
        '보기 지우기',
    'Wygląd':
        '모양',
    'Wygląd, wykluczenia domyślne i informacje o środowisku.':
        '모양, 기본 제외 항목, 환경 정보.',
    'Wygląd, wykluczenia i magazyn haseł':
        '모양, 제외 항목, 비밀번호 저장소',
    'Wykluczenia':
        '제외 항목',
    'Wykonuje kopię według tego szablonu':
        '이 템플릿대로 백업을 실행합니다',
    'Wykonuje kopię zgodnie z powyższymi ustawieniami':
        '위 설정대로 백업을 실행합니다',
    'Wymagane wyłącznie dla kopii zaszyfrowanych.':
        '암호화된 백업에만 필요합니다.',
    'Wzorce plików i folderów pomijanych w kopii — po jednym w wierszu.':
        '백업에서 제외할 파일과 폴더의 패턴 — 한 줄에 하나씩.',
    'Włączono szyfrowanie, ale nie podano hasła.':
        '암호화를 켰지만 비밀번호를 입력하지 않았습니다.',
    'Włączono usuwanie z kopii plików skasowanych w źródle.\n\nPliki usunięte w źródle stracą swoją jedyną kopię zapasową. Czy na pewno kontynuować?':
        '원본에서 삭제된 파일을 백업에서도 삭제하는 옵션이 켜져 있습니다.\n\n원본에서 삭제된 파일은 유일한 백업 사본을 잃게 됩니다. 정말 계속할까요?',
    'Za mało miejsca w katalogu docelowym. Potrzeba ok. {needed}, dostępne {free}.':
        '대상 폴더에 공간이 부족합니다. 필요: 약 {needed}, 사용 가능: {free}.',
    'Zabezpieczenie przed literówką — hasła nie da się odzyskać.':
        '오타 방지용입니다 — 비밀번호는 복구할 수 없습니다.',
    'Zachowaj oba — dopisz numer do nazwy':
        '둘 다 유지 — 이름에 번호 붙이기',
    'Zakończono z błędami ({errors}). Zapisano {count} {files}.':
        '완료했지만 오류가 {errors}개 있습니다. {files} {count}개를 기록했습니다.',
    'Zakończono.':
        '완료했습니다.',
    'Zapamiętaj hasło w Menedżerze poświadczeń Windows':
        'Windows 자격 증명 관리자에 비밀번호 기억',
    'Zapamiętuje te ustawienia do ponownego użycia':
        '다음에 다시 쓸 수 있도록 이 설정을 기억합니다',
    'Zapis bieżącej sesji':
        '현재 세션 기록',
    'Zapisane konfiguracje do ponownego użycia':
        '다시 쓸 수 있도록 저장한 구성',
    'Zapisane konfiguracje — uruchamiasz je jednym kliknięciem.':
        '저장한 구성 — 클릭 한 번으로 실행합니다.',
    'Zapisane szablony':
        '저장한 템플릿',
    'Zapisano szablon „{name}”.':
        '‘{name}’ 템플릿을 저장했습니다.',
    'Zapisuje listę jako domyślną':
        '목록을 기본값으로 저장합니다',
    'Zapisuje nową nazwę szablonu':
        '새 템플릿 이름을 저장합니다',
    'Zapisywanie {count} {files} ({size}), {workers} równolegle':
        '{files} {count}개({size}) 기록 중, 병렬 작업 {workers}개',
    'Zapisz':
        '저장',
    'Zapisz do:':
        '기록 위치:',
    'Zapisz jako szablon':
        '템플릿으로 저장',
    'Zapisz nazwę':
        '이름 저장',
    'Zapisz szablon':
        '템플릿 저장',
    'Zastąpić szablon?':
        '템플릿을 바꿀까요?',
    'Zatrzymuje operację. Pliki już zapisane pozostają nienaruszone.':
        '작업을 중지합니다. 이미 기록된 파일은 그대로 남습니다.',
    'Zaznacz szablon na liście.':
        '목록에서 템플릿을 선택하세요.',
    'Zmiana języka przebudowuje okno; wypełnione ścieżki zostają.':
        '언어를 바꾸면 창을 다시 구성합니다. 입력한 경로는 그대로 유지됩니다.',
    'Zmiana motywu działa natychmiast.':
        '테마 변경은 즉시 적용됩니다.',
    'Zmienia kolor przycisków i zaznaczeń':
        '버튼과 선택 영역의 색을 바꿉니다',
    'Zmień nazwę, aby łatwiej rozpoznawać szablon.':
        '템플릿을 쉽게 알아볼 수 있도록 이름을 바꾸세요.',
    'Znaleziono {count} {files}. Porównuję z poprzednią kopią…':
        '{files} {count}개를 찾았습니다. 이전 백업과 비교하는 중…',
    'automatycznie':
        '자동',
    'bez zmian':
        '변경 없음',
    'brak (biblioteka keyring niezainstalowana)':
        '없음(keyring 라이브러리가 설치되지 않음)',
    'brak danych':
        '정보 없음',
    'brak pliku w kopii':
        '백업에 파일이 없음',
    'do zapisania':
        '기록할 용량',
    'istniejąca kopia: {count} {files}, ostatnio {when}':
        '기존 백업: {files} {count}개, 마지막 {when}',
    'jeszcze nie uruchamiany':
        '아직 실행 안 함',
    'kompletna':
        '완료',
    'kopia lustrzana':
        '미러 백업',
    'kopia zapasowa':
        '백업',
    'nie':
        '아니요',
    'niedokończona':
        '미완료',
    'niedokończona — brakuje ok. {count} {files} ({size})':
        '미완료 — {files} 약 {count}개({size}) 누락',
    'niezaszyfrowana':
        '암호화 안 됨',
    'nieznany format manifestu':
        '알 수 없는 매니페스트 형식',
    'nowych plików':
        '새 파일',
    'np. C:\\Odzyskane':
        '예: C:\\복원',
    'np. E:\\Kopie zapasowe':
        '예: E:\\백업',
    'plik':
        '파일',
    'plik stanu jest za krótki':
        '상태 파일이 너무 짧습니다',
    'plik stanu w wersji {found}, obsługiwana: {supported}':
        '상태 파일 버전 {found}, 지원 버전: {supported}',
    'pliki':
        '파일',
    'plików':
        '파일',
    'podgląd kopii':
        '백업 미리 보기',
    'pozostaną w kopii':
        '백업에 그대로 남습니다',
    'rozmiar w kopii {actual} B zamiast {expected} B':
        '백업의 크기: {expected} B 대신 {actual} B',
    'sprawdzanie kopii':
        '백업 확인',
    'stan nieznany (zapisana starszą wersją programu)':
        '상태 알 수 없음(이전 버전의 프로그램으로 기록됨)',
    'suma kontrolna manifestu się nie zgadza':
        '매니페스트 체크섬이 일치하지 않음',
    'suma kontrolna się nie zgadza — plik uszkodzony':
        '체크섬이 일치하지 않음 — 파일이 손상됨',
    'szablon {name}':
        '템플릿 {name}',
    'tak':
        '예',
    'ten system plików':
        '이 파일 시스템',
    'wersja {version}':
        '버전 {version}',
    'wersje z datą':
        '날짜별 버전',
    'weryfikacja':
        '검증',
    'wyłączona':
        '끔',
    'zaszyfrowana (AES-256-GCM)':
        '암호화됨(AES-256-GCM)',
    'zawartość różni się od pliku źródłowego':
        '내용이 원본 파일과 다름',
    'zawartość różni się od sumy kontrolnej zapisanej podczas kopii':
        '내용이 백업 때 기록한 체크섬과 다름',
    'zmienionych':
        '변경됨',
    'zostaną usunięte z kopii':
        '백업에서 삭제됩니다',
    '{done} z {total} • {speed}/s{eta}':
        '{total} 중 {done} • {speed}/s{eta}',
    '{done} • {speed}/s':
        '{done} • {speed}/s',
    '{hours} h {minutes} min':
        '{hours}시간 {minutes}분',
    '{label}: {count} {files}':
        '{label}: {files} {count}개',
    '{message}\n\nSzczegóły techniczne znajdziesz w zakładce „Dziennik”.':
        '{message}\n\n기술적인 세부 정보는 ‘로그’ 화면에서 볼 수 있습니다.',
    '{minutes} min {seconds} s':
        '{minutes}분 {seconds}초',
    '{name}: nie można odczytać ({error})':
        '{name}: 읽을 수 없음({error})',
    '{seconds} s':
        '{seconds}초',
    '{summary}\n\nProblemy:\n{problems}\n\nPełna lista znajduje się w zakładce „Dziennik”.':
        '{summary}\n\n문제:\n{problems}\n\n전체 목록은 ‘로그’ 화면에서 볼 수 있습니다.',
    '{summary}{notes}\n\nPliki zapisane przed przerwaniem są kompletne i zostały odnotowane w spisie treści kopii.\n\nAby dokończyć kopię, uruchom ją ponownie — program zaproponuje uzupełnienie tej wersji zamiast tworzenia nowej.':
        '{summary}{notes}\n\n중단 전에 기록된 파일은 완전하며 백업 목차에 반영되었습니다.\n\n백업을 마치려면 다시 실행하세요 — 프로그램이 새 버전을 만드는 대신 이 버전을 보충하도록 제안합니다.',
    '{title} — gotowe':
        '{title} — 완료',
    '{title} — przerwano':
        '{title} — 중단됨',
    '{title} — zakończono z błędami':
        '{title} — 완료(오류 있음)',
    '{when}  •  {action}  •  {count} {files}':
        '{when}  •  {action}  •  {files} {count}개',
    'Łączny rozmiar danych do przesłania':
        '전송할 데이터의 총 크기',
    'Środowisko':
        '환경',
    'Źródła: {sources}\nCel: {destination}\nUkład: {structure} • Szyfrowanie: {encrypt} • Weryfikacja: {verify} • Dogrywka: {catchup} • Równolegle: {workers} • Data uzupełnienia w nazwie: {stamp}\nUtworzony: {created} • Ostatni przebieg: {last}':
        '원본: {sources}\n대상: {destination}\n구조: {structure} • 암호화: {encrypt} • 검증: {verify} • 보충: {catchup} • 병렬: {workers} • 이름에 보충 날짜: {stamp}\n만든 날짜: {created} • 마지막 실행: {last}',
    'Źródło nie zmieniło się w trakcie kopii — nie ma czego uzupełniać.':
        '백업 중에 원본이 바뀌지 않았습니다 — 보충할 것이 없습니다.',
    '—':
        '—',
    '• Kopia przyrostowa — zapisywane są wyłącznie pliki nowe i zmienione.\n  Porównanie opiera się na spisie treści kopii, rozmiarze i dacie modyfikacji;\n  przy różnicy liczona jest suma kontrolna SHA-256.\n\n• Wersje z datą — każdy przebieg tworzy kompletny folder z datą, a pliki\n  niezmienione są podpinane twardym dowiązaniem, więc nie zajmują miejsca dwa razy.\n\n• Weryfikacja po zapisie — zapisany plik jest odczytywany z powrotem\n  i porównywany ze źródłem.\n\n• Odporność na przerwania — pliki powstają pod nazwą tymczasową i są\n  podmieniane dopiero po pełnym zapisie.':
        '• 증분 백업 — 새로 생기거나 바뀐 파일만 기록합니다.\n  백업 목차, 크기, 수정 날짜를 비교하며,\n  차이가 있으면 SHA-256 체크섬을 계산합니다.\n\n• 날짜별 버전 — 실행할 때마다 날짜가 붙은 완전한 폴더를 만들고,\n  바뀌지 않은 파일은 하드 링크로 연결하므로 공간을 두 번 차지하지 않습니다.\n\n• 기록 후 검증 — 기록한 파일을 다시 읽어\n  원본과 비교합니다.\n\n• 중단 대비 — 파일은 임시 이름으로 만들어지고\n  완전히 기록된 뒤에야 원래 이름으로 바뀝니다.',
    '• Szyfr: AES-256 w trybie GCM (szyfrowanie z uwierzytelnieniem).\n• Wyprowadzanie klucza z hasła: {kdf}.\n• Nagłówek każdego pliku jest uwierzytelniony jako AAD — podmiana parametrów\n  unieważnia tag.\n• Każdy plik dostaje losowy, niepowtarzalny nonce.\n• Odszyfrowany plik powstaje dopiero po pomyślnej weryfikacji tagu.\n• Hasła nie są zapisywane w plikach programu. Opcjonalnie trafiają do\n  Menedżera poświadczeń Windows.':
        '• 암호: GCM 모드의 AES-256(인증 암호화).\n• 비밀번호에서 키 파생: {kdf}.\n• 각 파일의 헤더는 AAD로 인증됩니다 — 매개변수를 바꾸면\n  태그가 무효가 됩니다.\n• 파일마다 무작위의 고유한 nonce를 사용합니다.\n• 복호화된 파일은 태그 검증에 성공한 뒤에만 만들어집니다.\n• 비밀번호는 프로그램 파일에 기록되지 않습니다. 원하면\n  Windows 자격 증명 관리자에 저장됩니다.',
    'Bez hasła nie da się odczytać ani jednego pliku z kopii.':
        '비밀번호가 없으면 백업의 파일을 단 하나도 읽을 수 없습니다.',
    'Co chcesz chronić?':
        '무엇을 보호할까요?',
    'Co chcesz teraz zrobić?':
        '이제 무엇을 할까요?',
    'Czyta kopię z nośnika i porównuje ją z zapisanymi sumami kontrolnymi.':
        '저장 매체에서 백업을 읽어 기록된 체크섬과 비교합니다.',
    'Dalej':
        '다음',
    'Dokumenty i zdjęcia':
        '문서와 사진',
    'Ekran powitalny wrócisz w ustawieniach, gdy zmienisz zdanie.':
        '마음이 바뀌면 설정에서 환영 화면을 다시 켤 수 있습니다.',
    'Ekran z pytaniem, co chcesz teraz zrobić: kopia, przywracanie, sprawdzenie.':
        '지금 무엇을 할지 묻는 화면: 백업, 복원, 확인.',
    'Foldery objęte kopią':
        '백업 대상 폴더',
    'Foldery z pracą. Kreator pominie katalogi, które odtwarza się jednym poleceniem (node_modules, venv, build).':
        '작업 폴더입니다. 명령 하나로 다시 만들 수 있는 폴더(node_modules, venv, build)는 마법사가 제외합니다.',
    'Gdzie zapisać kopię?':
        '백업을 어디에 저장할까요?',
    'Historia i szyfrowanie':
        '기록과 암호화',
    'Historia zmian (zalecane)':
        '변경 기록(권장)',
    'Jak bardzo chcesz się zabezpieczyć?':
        '어느 정도로 보호할까요?',
    'Jak wyżej, a dodatkowo każdy plik trafia do kopii zaszyfrowany (AES-256-GCM). Potrzebne przy kopii wożonej poza dom.':
        '위와 같으며, 모든 파일을 암호화(AES-256-GCM)해 백업합니다. 백업을 집 밖으로 가지고 다닐 때 필요합니다.',
    'Jedna aktualna kopia':
        '최신 사본 하나',
    'Język, motyw, domyślne wykluczenia i informacje o środowisku.':
        '언어, 테마, 기본 제외 항목, 환경 정보.',
    'Katalog docelowy leży wewnątrz źródła — wybierz inny.':
        '대상 폴더가 원본 안에 있습니다 — 다른 폴더를 선택하세요.',
    'Każdy przebieg tworzy folder z datą. Pliki niezmienione są podpinane dowiązaniem, więc historia kosztuje tyle, ile realnie się zmieniło.':
        '실행할 때마다 날짜별 폴더를 만듭니다. 바뀌지 않은 파일은 링크로 연결하므로 기록은 실제로 바뀐 만큼만 공간을 차지합니다.',
    'Każdy przebieg utworzy folder z datą. Pierwszy zajmie tyle, ile dane; kolejne — tyle, ile realnie się zmieniło.':
        '실행할 때마다 날짜별 폴더를 만듭니다. 첫 번째는 데이터만큼, 그다음부터는 실제로 바뀐 만큼만 공간을 차지합니다.',
    'Kopia powstanie w: {path}':
        '백업이 만들어질 위치: {path}',
    'Kopia trafi do: {path}':
        '백업 저장 위치: {path}',
    'Kopia: {what}':
        '백업: {what}',
    'Krok {number} z {total}':
        '{total}단계 중 {number}단계',
    'Najlepiej na innym dysku fizycznym niż ten, który chronisz — kopia obok oryginału ginie razem z nim.':
        '보호하려는 드라이브가 아닌 다른 물리 드라이브가 가장 좋습니다 — 원본 옆에 있는 백업은 원본과 함께 사라집니다.',
    'Najszybsza i najmniejsza. Kopia odpowiada temu, co masz teraz — bez historii wcześniejszych wersji.':
        '가장 빠르고 가장 작습니다. 백업은 지금 가진 그대로이며 이전 버전의 기록은 없습니다.',
    'Nie było jeszcze żadnej kopii. Zacznij od „Zrób kopię”.':
        '아직 백업한 적이 없습니다. ‘지금 백업’으로 시작하세요.',
    'Nie lista ustawień, tylko ich skutki.':
        '설정 목록이 아니라 실제로 일어날 일입니다.',
    'Nie pokazuj tego ekranu przy starcie':
        '시작할 때 이 화면 표시 안 함',
    'Nośnik docelowy':
        '대상 저장 매체',
    'Odtwarza pliki z kopii — całość albo wybrany folder.':
        '백업에서 파일을 복원합니다 — 전체 또는 선택한 폴더.',
    'Odśwież listę':
        '목록 새로 고침',
    'Ostatnia kopia: {when} • {count} {files}.':
        '마지막 백업: {when} • {files} {count}개.',
    'Pierwszy przebieg jest najdłuższy — kolejne porównują rozmiar i datę modyfikacji, więc zwykle trwają sekundy.':
        '첫 실행이 가장 오래 걸립니다 — 그다음부터는 크기와 수정 날짜를 비교하므로 보통 몇 초면 끝납니다.',
    'Pliki w kopii będą zaszyfrowane; bez hasła nie da się ich odczytać.':
        '백업의 파일은 암호화되며, 비밀번호 없이는 읽을 수 없습니다.',
    'Podfoldery są uwzględniane automatycznie.':
        '하위 폴더는 자동으로 포함됩니다.',
    'Pokazuj ekran powitalny przy starcie':
        '시작할 때 환영 화면 표시',
    'Ponownie sprawdza podłączone nośniki':
        '연결된 저장 매체를 다시 확인합니다',
    'Program będzie utrzymywał jeden folder zgodny ze źródłem. Każdy kolejny przebieg dopisze tylko to, co się zmieniło.':
        '프로그램이 원본과 똑같은 폴더 하나를 유지합니다. 이후 실행에서는 바뀐 것만 기록합니다.',
    'Projekty i kod':
        '프로젝트와 코드',
    'Przechodzi do następnego kroku':
        '다음 단계로 이동합니다',
    'Przechodzi do pełnego okna programu':
        '프로그램 전체 창으로 이동합니다',
    'Sam wskażesz, co ma trafić do kopii.':
        '백업할 항목을 직접 지정합니다.',
    'System plików: {filesystem}, klaster {cluster}':
        '파일 시스템: {filesystem}, 클러스터 {cluster}',
    'Ten katalog leży wewnątrz folderu źródłowego — wybierz inny.':
        '이 폴더는 원본 폴더 안에 있습니다 — 다른 폴더를 선택하세요.',
    'Ten nośnik nie obsługuje twardych dowiązań, więc każda wersja z datą zajmie tyle miejsca co pełna kopia. Przy tym nośniku rozważ „jedną aktualną kopię”.':
        '이 저장 매체는 하드 링크를 지원하지 않으므로 날짜별 버전마다 전체 백업만큼 공간을 차지합니다. 이 저장 매체에서는 ‘최신 사본 하나’를 고려하세요.',
    'To dysk systemowy — kopia nie przetrwa jego awarii. Jeśli masz drugi dysk albo pendrive, wybierz jego.':
        '시스템 드라이브입니다 — 이 드라이브가 고장 나면 백업도 함께 사라집니다. 다른 드라이브나 USB 메모리가 있다면 그것을 선택하세요.',
    'To się wydarzy':
        '이렇게 진행됩니다',
    'Trzy gotowe zestawy zamiast kilkunastu przełączników.':
        '스위치 십여 개 대신 준비된 세 가지 조합.',
    'Twoje pliki osobiste z folderów użytkownika. Najczęstszy wybór.':
        '사용자 폴더에 있는 개인 파일입니다. 가장 많이 선택하는 항목입니다.',
    'Uruchamia kreator, który ustawi kopię krok po kroku':
        '백업을 단계별로 설정하는 마법사를 시작합니다',
    'Uruchom kreator…':
        '마법사 실행…',
    'Ustawia kopię krok po kroku i zapisuje ją jako szablon':
        '백업을 단계별로 설정하고 템플릿으로 저장합니다',
    'Ustawienia pierwszej kopii':
        '첫 백업 설정',
    'Ustawienia pierwszej kopii…':
        '첫 백업 설정…',
    'W tym katalogu jest już kopia ({count} {files}) — program ją uzupełni, a nie nadpisze.':
        '이 폴더에는 이미 백업이 있습니다({files} {count}개) — 프로그램이 덮어쓰지 않고 보충합니다.',
    'Wraca do poprzedniego kroku':
        '이전 단계로 돌아갑니다',
    'Wskaż dowolny katalog docelowy':
        '원하는 대상 폴더 지정',
    'Wskaż folder kopii i kliknij „Sprawdź kopię”.':
        '백업 폴더를 지정하고 ‘백업 확인’을 클릭하세요.',
    'Wstecz':
        '뒤로',
    'Wybierz':
        '선택',
    'Wybierz inny folder…':
        '다른 폴더 선택…',
    'Wybierz to, co najbliższe. Dokładną listę folderów poprawisz niżej.':
        '가장 가까운 것을 고르세요. 정확한 폴더 목록은 아래에서 고칠 수 있습니다.',
    'Wybrane foldery':
        '선택한 폴더',
    'Zamknij':
        '닫기',
    'Zamyka kreator bez zapisywania':
        '저장하지 않고 마법사를 닫습니다',
    'Zapisuje nowe i zmienione pliki. Pierwszy raz trwa najdłużej.':
        '새 파일과 바뀐 파일을 기록합니다. 처음에는 가장 오래 걸립니다.',
    'Zapisuje szablon bez uruchamiania kopii':
        '백업을 실행하지 않고 템플릿만 저장합니다',
    'Zapisuje szablon i od razu uruchamia kopię':
        '템플릿을 저장하고 바로 백업을 실행합니다',
    'Zapisz i zrób kopię':
        '저장 후 지금 백업',
    'Zapisz ustawienia':
        '설정 저장',
    'Zrób kopię':
        '지금 백업',
    'dysk systemowy':
        '시스템 드라이브',
    'wolne {free} z {total}':
        '{total} 중 {free} 여유',
    'Porównano ze źródłem: {source}; tylko z sumą kontrolną (źródło zmieniło się albo jest niedostępne): {checksum}.':
        '원본과 비교한 파일: {source}개, 체크섬으로만 확인한 파일(원본이 바뀌었거나 사용할 수 없음): {checksum}개.',
    'Przywraca losową próbkę plików do katalogu tymczasowego i porównuje je ze źródłem.\nSprawdza całą drogę odzyskiwania, a trwa minuty. Nic nie zostaje na dysku.':
        '무작위로 고른 파일 일부를 임시 폴더에 복원해 원본과 비교합니다.\n복구 과정 전체를 시험하며 몇 분이면 끝납니다. 디스크에는 아무것도 남지 않습니다.',
    'Próbne przywrócenie':
        '시험 복원',
    'W kopii nie ma plików, które dałoby się sprawdzić próbnie.':
        '백업에 시험 복원으로 확인할 수 있는 파일이 없습니다.',
    'przywrócony plik różni się od pliku źródłowego':
        '복원한 파일이 원본 파일과 다름',
    'przywrócony plik różni się od sumy kontrolnej zapisanej podczas kopii':
        '복원한 파일이 백업 때 기록한 체크섬과 다름',
    'próbne przywrócenie':
        '시험 복원',
    '(brak zapisanych szablonów)':
        '(저장한 템플릿 없음)',
    'Bez tego kopia planowa ruszy dopiero wtedy, gdy sam otworzysz program.':
        '이 옵션을 켜지 않으면 예약 백업은 사용자가 프로그램을 직접 열 때에야 시작됩니다.',
    'Codziennie o godzinie':
        '매일 정해진 시각',
    'Codziennie o wybranej godzinie (zalecane)':
        '매일 정해진 시각(권장)',
    'Dla dysku USB podłączanego od czasu do czasu. Najwyżej jedna kopia na 12 godzin.':
        '가끔 연결하는 USB 드라이브용입니다. 백업은 12시간에 최대 한 번입니다.',
    'Dostępne w zainstalowanej wersji programu (plik EXE).':
        '설치된 버전의 프로그램(EXE 파일)에서 사용할 수 있습니다.',
    'Godzina kopii codziennej (czas tego komputera).':
        '매일 백업할 시각(이 컴퓨터의 시계 기준).',
    'Harmonogram działa wtedy, gdy działa program — także ukryty przy zegarze.':
        '일정은 프로그램이 실행 중일 때 작동합니다 — 시계 옆에 숨겨져 있을 때도 마찬가지입니다.',
    'Harmonogram nie uruchamia kopii, dopóki tego nie odznaczysz. Ręczne kopie działają.':
        '이 항목의 선택을 해제할 때까지 일정에 따라 백업을 시작하지 않습니다. 수동 백업은 그대로 작동합니다.',
    'Harmonogram szablonu „{name}” zapisany.':
        '‘{name}’ 템플릿의 일정을 저장했습니다.',
    'Harmonogram:':
        '일정:',
    'Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.':
        '그 시각에 컴퓨터가 꺼져 있으면 컴퓨터를 켠 뒤에 백업이 시작됩니다.',
    'Kiedy kopia z tego szablonu ma ruszać sama.':
        '이 템플릿의 백업이 자동으로 시작될 시점입니다.',
    'Kiedy robić kopię?':
        '언제 백업할까요?',
    'Kopia będzie robiona codziennie o {time}; termin przegapiony przy wyłączonym komputerze program nadrobi po jego włączeniu.':
        '매일 {time}에 백업합니다. 컴퓨터가 꺼져 있어 놓친 백업은 컴퓨터를 켠 뒤에 실행합니다.',
    'Kopia planowa nie powiodła się':
        '예약 백업에 실패했습니다',
    'Kopia rusza tylko wtedy, gdy ją uruchomisz.':
        '직접 실행할 때만 백업이 시작됩니다.',
    'Kopia ruszy po podłączeniu dysku docelowego (najwyżej raz na 12 godzin).':
        '대상 드라이브를 연결하면 백업이 시작됩니다(12시간에 최대 한 번).',
    'Kopia ruszy po podłączeniu dysku docelowego — najwyżej raz na 12 godzin.':
        '대상 드라이브를 연결하면 백업이 시작됩니다 — 12시간에 최대 한 번.',
    'Kopia sprzed miesiąca nie chroni tego, co zmieniło się od tamtej pory.':
        '한 달 전 백업은 그 뒤에 바뀐 내용을 지켜 주지 못합니다.',
    'Kopia „{name}” czeka':
        '‘{name}’ 백업이 늦어지고 있습니다',
    'Kopia „{name}” nie ruszyła':
        '‘{name}’ 백업이 시작되지 않았습니다',
    'Kopie planowe działają, gdy działa program (także ukryty przy zegarze).':
        '예약 백업은 프로그램이 실행 중일 때 작동합니다(시계 옆에 숨겨져 있을 때도).',
    'Kopie planowe działają, gdy działa program: po zamknięciu okna zostaje ikona przy zegarze, a przy logowaniu do Windows program uruchamia się w tle.':
        '예약 백업은 프로그램이 실행 중일 때 작동합니다. 창을 닫아도 시계 옆에 아이콘이 남고, Windows에 로그인하면 프로그램이 백그라운드에서 시작됩니다.',
    'Kopie planowe i praca w tle':
        '예약 백업과 백그라운드 실행',
    'Kopie planowe wykonają się o czasie. Program zamkniesz z menu ikony przy zegarze.':
        '예약 백업은 제시간에 실행됩니다. 프로그램은 시계 옆 아이콘의 메뉴에서 종료할 수 있습니다.',
    'Kopię uruchamiasz przyciskiem. Najprostsze, ale łatwo o niej zapomnieć.':
        '버튼을 눌러 백업을 시작합니다. 가장 간단하지만 잊어버리기 쉽습니다.',
    'Kopię uruchamiasz sam — przyciskiem w programie albo z menu ikony przy zegarze.':
        '백업을 직접 시작합니다 — 프로그램의 버튼이나 시계 옆 아이콘의 메뉴에서.',
    'Następna kopia: {when}. Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.':
        '다음 백업: {when}. 그 시각에 컴퓨터가 꺼져 있으면 컴퓨터를 켠 뒤에 백업이 시작됩니다.',
    'Nie udało się zmienić startu przy logowaniu — szczegóły w dzienniku.':
        '로그인 시 시작 설정을 바꾸지 못했습니다 — 자세한 내용은 로그를 확인하세요.',
    'Od {days} dni nie było udanej kopii. Podłącz dysk docelowy albo otwórz program, żeby sprawdzić, co się dzieje.':
        '{days}일 동안 성공한 백업이 없습니다. 대상 드라이브를 연결하거나 프로그램을 열어 무슨 일인지 확인하세요.',
    'Otwórz Sigelith Backup':
        'Sigelith Backup 열기',
    'Po podłączeniu dysku docelowego':
        '대상 드라이브를 연결할 때',
    'Po podłączeniu dysku z kopią':
        '백업 드라이브를 연결할 때',
    'Po zamknięciu okna działaj dalej przy zegarze, gdy są kopie planowe':
        '예약 백업이 있으면 창을 닫은 뒤에도 시계 옆에서 계속 실행',
    'Potrzebne, żeby kopie planowe ruszały bez Twojego udziału. Hasło trafia do magazynu systemowego powiązanego z Twoim kontem, nie do plików programu.':
        '예약 백업이 사용자 없이도 시작되려면 필요합니다. 비밀번호는 프로그램 파일이 아니라 사용자 계정에 연결된 시스템 저장소에 보관됩니다.',
    'Program uruchamia się w tle przy logowaniu, więc terminy nie przepadną.':
        '로그인할 때 프로그램이 백그라운드에서 시작되므로 예정된 백업을 놓치지 않습니다.',
    'Ręcznie':
        '수동',
    'Ręcznie — kiedy zechcę':
        '수동 — 원할 때',
    'Start przy logowaniu włączony':
        '로그인 시 시작 켜짐',
    'Szablon jest zaszyfrowany, a hasło nie jest zapamiętane. Kopie planowe potrzebują hasła zapisanego w Menedżerze poświadczeń Windows.':
        '템플릿은 암호화되어 있는데 비밀번호가 기억되어 있지 않습니다. 예약 백업에는 Windows 자격 증명 관리자에 저장된 비밀번호가 필요합니다.',
    'Sigelith Backup będzie uruchamiał się w tle, żeby wykonywać kopie planowe. Wyłączysz to w ustawieniach programu.':
        '예약 백업을 실행하기 위해 Sigelith Backup이 백그라운드에서 시작됩니다. 프로그램 설정에서 끌 수 있습니다.',
    'Sigelith Backup działa w tle':
        'Sigelith Backup이 백그라운드에서 실행 중입니다',
    'Uruchamiaj program w tle przy logowaniu do Windows':
        'Windows에 로그인할 때 백그라운드에서 프로그램 시작',
    'Wstrzymaj kopie planowe':
        '예약 백업 일시 중지',
    'Zakończ':
        '종료',
    'Zamknięcie okna chowa je, a harmonogram pilnuje terminów. Program zamkniesz z menu ikony przy zegarze.':
        '창을 닫으면 창이 숨겨지고 일정은 계속 시각을 지킵니다. 프로그램은 시계 옆 아이콘의 메뉴에서 종료할 수 있습니다.',
    'Zrób kopię teraz':
        '지금 백업',
    '{summary} Szczegóły znajdziesz w programie, w zakładce „Dziennik”.':
        '{summary} 자세한 내용은 프로그램의 ‘로그’ 화면에서 볼 수 있습니다.',
    'Program działa z uprawnieniami administratora. Nie są mu potrzebne — kopia i przywracanie działają bez nich, a pliki zapisane przez administratora mogą później nie dać się zmienić ze zwykłego konta.':
        '프로그램이 관리자 권한으로 실행 중입니다. 관리자 권한은 필요하지 않습니다 — 백업과 복원은 관리자 권한 없이도 작동하며, 관리자로 기록한 파일은 나중에 일반 계정에서 수정하지 못할 수 있습니다.',
    'Pliki otwarte w innych programach nie trafiły do kopii: {files}. Zamknij te programy i uruchom kopię ponownie — dograne zostaną tylko te pliki.':
        '다른 프로그램에서 열려 있던 파일은 백업되지 않았습니다: {files}. 그 프로그램을 닫고 백업을 다시 실행하세요 — 해당 파일만 추가로 기록됩니다.',
    'Uwaga: w źródle zmieniło się podejrzanie dużo plików — {reasons}':
        '경고: 원본에서 의심스러울 만큼 많은 파일이 바뀌었습니다 — {reasons}',
    'Wstrzymano kopię: w źródle zmieniło się podejrzanie dużo plików. {reasons}':
        '백업을 일시 중지했습니다: 원본에서 의심스러울 만큼 많은 파일이 바뀌었습니다. {reasons}',
    'Zmieniło się albo zniknęło {count} z {previous} plików poprzedniej kopii.':
        '이전 백업의 파일 {previous}개 중 {count}개가 바뀌었거나 사라졌습니다.',
    '{suspicious} z {evaluated} sprawdzonych zmienionych plików ma treść, która nie pasuje do ich typu (wygląda na zaszyfrowaną).':
        '확인한 변경 파일 {evaluated}개 중 {suspicious}개는 내용이 파일 형식과 맞지 않습니다(암호화된 것으로 보임).',
    'Kontynuuj mimo to':
        '그래도 계속',
    'Kopia planowa wstrzymana':
        '예약 백업 일시 중지됨',
    'Kopia wstrzymana do decyzji.':
        '결정할 때까지 백업을 일시 중지했습니다.',
    'Kopia wstrzymana — w źródle zmieniło się podejrzanie dużo plików.':
        '백업 일시 중지 — 원본에서 의심스러울 만큼 많은 파일이 바뀌었습니다.',
    'Podejrzanie dużo zmian':
        '의심스러울 만큼 많은 변경',
    'Wstrzymaj kopię':
        '백업 일시 중지',
    '{reasons}\n\nJeśli to spodziewane — aktualizacja programu, przeniesienie albo przerobienie wielu plików — kontynuuj.\n\nJeśli nie, NIE kontynuuj: tak wygląda działanie oprogramowania szyfrującego pliki (ransomware). Sprawdź najpierw, czy Twoje pliki dają się otworzyć. Wcześniejsze wersje w kopii pozostają nietknięte.':
        '{reasons}\n\n예상한 일이라면(소프트웨어 업데이트, 많은 파일의 이동이나 수정) 계속하세요.\n\n그렇지 않다면 절대 계속하지 마세요: 파일을 암호화하는 악성 소프트웨어(랜섬웨어)가 바로 이렇게 작동합니다. 먼저 파일이 제대로 열리는지 확인하세요. 백업에 있는 이전 버전은 그대로 안전합니다.',
    '{reasons} To może być działanie złośliwego oprogramowania szyfrującego pliki. Otwórz program, sprawdź pliki i uruchom kopię ręcznie.':
        '{reasons} 파일을 암호화하는 악성 소프트웨어의 소행일 수 있습니다. 프로그램을 열어 파일을 확인하고 백업을 수동으로 실행하세요.',
    'Pominięto {count} {files}.':
        '{files} {count}개를 건너뛰었습니다.',
    'Ponawiam {count} {files}…':
        '{files} {count}개 다시 시도 중…',
    ' (bez {count} {files})':
        ' ({files} {count}개 제외)',
    'plik otwarty w innym programie':
        '다른 프로그램에서 열린 파일',
    'pliki otwarte w innych programach':
        '다른 프로그램에서 열린 파일',
    'plików otwartych w innych programach':
        '다른 프로그램에서 열린 파일',
    'pliku otwartego w innym programie':
        '다른 프로그램에서 열린 파일',
    '\n\n…i kolejne: {count}.':
        '\n\n…외 {count}개.',
    'Foldery objęte kopią ({count}): {list}':
        '백업 대상 폴더({count}개): {list}',
    'Nośnik nie obsługuje twardych dowiązań — kopiuję do nowej wersji niezmienione pliki: {count} ({size})…':
        '저장 매체가 하드 링크를 지원하지 않습니다 — 바뀌지 않은 파일을 새 버전에 복사하는 중: {count}개({size})…',
    'Pliki bez sumy kontrolnej sprawdzone tylko co do rozmiaru, bo ich źródło zmieniło się albo jest niedostępne: {count}.':
        '체크섬이 없어 크기만 확인한 파일(원본이 바뀌었거나 사용할 수 없음): {count}개.',
    'Pliki bez zapisanej sumy kontrolnej, porównane ze źródłem i uzupełnione w spisie treści: {count}.':
        '기록된 체크섬이 없어 원본과 비교한 뒤 목차에 보충한 파일: {count}개.',
    'Pliki przeniesione w źródle: {count} — trafią do kopii bez przesyłania danych.':
        '원본에서 이동된 파일: {count}개 — 데이터를 전송하지 않고 백업에 반영됩니다.',
    'Pliki skasowane w źródle: {count} — {action}.':
        '원본에서 삭제된 파일: {count}개 — {action}.',
    'Pliki z końcówką dopisaną do nazwy, których oryginały zniknęły: {count}.':
        '이름 끝에 확장자가 덧붙었고 원래 파일은 사라진 파일: {count}개.',
    'Pliki zmienione w trakcie kopiowania: {count} — zostaną zapisane ponownie w przebiegu uzupełniającym.':
        '복사하는 도중 바뀐 파일: {count}개 — 보충 실행에서 다시 기록됩니다.',
    'Pliki, których brakuje w kopii i które zostaną zapisane ponownie: {count}.':
        '백업에 없어서 다시 기록할 파일: {count}개.',
    'Podpinanie niezmienionych plików do nowej wersji: {count}…':
        '바뀌지 않은 파일을 새 버전에 연결하는 중: {count}개…',
    'Pomijam pliki, które już są w tej wersji kopii: {count}.':
        '이 백업 버전에 이미 있는 파일을 건너뜁니다: {count}개.',
    'Porządkowanie historii — usunięte najstarsze wersje: {count}.':
        '기록 정리 — 삭제한 가장 오래된 버전: {count}개.',
    'Przenoszenie plików, które zmieniły miejsce w źródle: {count}…':
        '원본에서 위치가 바뀐 파일을 옮기는 중: {count}개…',
    'Próbne przywrócenie losowo wybranych plików: {count}…':
        '무작위로 고른 파일을 시험 복원하는 중: {count}개…',
    'Usuwanie z kopii plików skasowanych w źródle: {count}…':
        '원본에서 삭제된 파일을 백업에서 삭제하는 중: {count}개…',
    'Uzupełniam kopię o pliki, które przybyły lub zmieniły się w trakcie: {count} ({size})…':
        '그사이 새로 생기거나 바뀐 파일로 백업을 보충하는 중: {count}개({size})…',
    'Uzupełnianie wersji {version} — pliki już zapisane, które zostaną pominięte: {count}.':
        '{version} 버전 보충 — 이미 기록되어 건너뛸 파일: {count}개.',
    'Wznawiam wersję {version} — już zapisane: {done}, do dogrania: {todo}.':
        '{version} 버전 이어서 진행 — 기록 완료: {done}개, 남은 파일: {todo}개.',
    'pliku':
        '파일',
    'Brak fragmentu {cid} w magazynie kopii.':
        '백업의 조각 저장소에서 조각을 찾을 수 없습니다: {cid}.',
    'Brak opisu magazynu fragmentów w katalogu kopii.':
        '백업 폴더에 조각 저장소 설명이 없습니다.',
    'Duże pliki zapisuj różnicowo (od 256 MB)':
        '큰 파일은 변경분만 기록(256 MB 이상)',
    'Fragment {cid} jest uszkodzony.':
        '조각이 손상되었습니다: {cid}.',
    'Kolejna wersja dużego pliku — maszyny wirtualnej, skrzynki pocztowej, bazy —\nzapisuje tylko zmienione fragmenty zamiast całego pliku. W kopii taki plik\nleży jako przepis + fragmenty; złoży go program albo skrypt ratunkowy.':
        '큰 파일(가상 머신, 메일함, 데이터베이스 등)의 다음 버전은\n파일 전체 대신 바뀐 조각만 기록합니다. 백업에서 이런 파일은\n구성 정보와 조각으로 보관되며, 프로그램이나 복구 스크립트가 다시 조립합니다.',
    'Opis magazynu fragmentów jest uszkodzony.':
        '조각 저장소 설명이 손상되었습니다.',
    'Plik złożony z fragmentów różni się od zapisanego w przepisie.':
        '조각으로 조립한 파일이 구성 정보에 기록된 것과 다릅니다.',
    'Podane hasło nie pasuje do fragmentów zapisanych wcześniej w tej kopii.':
        '입력한 비밀번호가 이 백업에 이전에 기록된 조각과 맞지 않습니다.',
    'Przepis pliku jest uszkodzony.':
        '파일 구성 정보가 손상되었습니다.',
    'To nie jest przepis pliku zapisanego fragmentami.':
        '조각으로 저장된 파일의 구성 정보가 아닙니다.',
    'Usunięto nieużywane fragmenty dużych plików: {count} ({size}).':
        '사용하지 않는 큰 파일 조각을 삭제했습니다: {count}개({size}).',
    ', zakotwiczona w Bitcoinie':
        ', Bitcoin에 앵커링됨',
    'Adres usługi:':
        '서비스 주소:',
    'Brak fragmentu {cid} w kopii poza domem.':
        '원격 백업에서 조각을 찾을 수 없습니다: {cid}.',
    'Brak klucza albo hasła w Menedżerze poświadczeń Windows — zapisz ustawienia kopii poza domem jeszcze raz.':
        'Windows 자격 증명 관리자에 키나 비밀번호가 없습니다 — 원격 백업 설정을 다시 저장하세요.',
    'Brak spisu wersji, którego dotyczy znacznik.':
        '타임스탬프가 가리키는 버전 목록이 없습니다.',
    'Certyfikat PDF':
        'PDF 인증서',
    'Druga, zaszyfrowana kopia w usłudze zgodnej z S3 (np. Backblaze B2)':
        'S3 호환 서비스(예: Backblaze B2)에 두는 두 번째 암호화 백업',
    'Folder w kubełku:':
        '버킷 내 폴더:',
    'Hasło kopii poza domem':
        '원격 백업 비밀번호',
    'Hasło kopii poza domem nie pasuje do danych zapisanych w tym miejscu.':
        '원격 백업 비밀번호가 이 위치에 저장된 데이터와 맞지 않습니다.',
    'Hasło kopii poza domem powinno mieć co najmniej 10 znaków.':
        '원격 백업 비밀번호는 10자 이상이어야 합니다.',
    'Hasło szyfrowania:':
        '암호화 비밀번호:',
    'Identyfikator klucza:':
        '키 ID:',
    'Katalog, do którego trafią pliki':
        '파일을 저장할 폴더',
    'Klucz tajny':
        '비밀 키',
    'Klucz tajny:':
        '비밀 키:',
    'Kopia na dysku obok komputera nie przetrwa pożaru ani kradzieży. Tu ustawisz drugą kopię w usłudze zgodnej z S3 (np. Backblaze B2). Pliki są szyfrowane na tym komputerze osobnym hasłem — usługa widzi tylko nieczytelne fragmenty.':
        '컴퓨터 옆 드라이브에 있는 백업은 화재나 도난을 견디지 못합니다. 여기서 S3 호환 서비스(예: Backblaze B2)에 두 번째 백업을 설정합니다. 파일은 이 컴퓨터에서 별도의 비밀번호로 암호화되므로 서비스에는 읽을 수 없는 조각만 보입니다.',
    'Kopia poza domem':
        '원격 백업',
    'Kopia poza domem dla szablonu „{name}” zapisana.':
        '‘{name}’ 템플릿의 원격 백업 설정을 저장했습니다.',
    'Kopia poza domem nie ruszyła':
        '원격 백업이 시작되지 않았습니다',
    'Kopia poza domem potrzebuje Menedżera poświadczeń Windows, a jest on niedostępny.':
        '원격 백업에는 Windows 자격 증명 관리자가 필요하지만 사용할 수 없습니다.',
    'Kopia poza domem „{name}”':
        '‘{name}’ 원격 백업',
    'Kopia poza domem…':
        '원격 백업…',
    'Korzeń tygodnia zakotwiczony w łańcuchu Bitcoina.':
        '주간 루트가 Bitcoin 체인에 앵커링되었습니다.',
    'Kubełek (bucket):':
        '버킷(bucket):',
    'Migawek w usłudze: {count}.':
        '서비스의 스냅샷: {count}개.',
    'Migawka i cel':
        '스냅샷과 대상',
    'Migawka kopii poza domem jest uszkodzona.':
        '원격 백업 스냅샷이 손상되었습니다.',
    'Migawka {stamp}: plików bez zmian {reused}, wysłanych {files}, nowych fragmentów {chunks} ({size}).':
        '스냅샷 {stamp}: 변경 없는 파일 {reused}개, 업로드한 파일 {files}개, 새 조각 {chunks}개({size}).',
    'MinIO / Wasabi / inna zgodna z S3':
        'MinIO / Wasabi / 기타 S3 호환 서비스',
    'NIEPOPRAWNY':
        '유효하지 않음',
    'Nie ma migawki {stamp} w kopii poza domem.':
        '원격 백업에서 스냅샷을 찾을 수 없습니다: {stamp}.',
    'Nie udało się połączyć z usługą przechowywania: {error}':
        '스토리지 서비스에 연결하지 못했습니다: {error}',
    'Nie udało się wczytać migawek: {error}':
        '스냅샷을 불러오지 못했습니다: {error}',
    'Nie udało się zapisać klucza albo hasła w magazynie systemowym.':
        '키나 비밀번호를 시스템 저장소에 저장하지 못했습니다.',
    'Odśwież z sieci':
        '온라인으로 새로 고침',
    'Opis kopii poza domem jest uszkodzony.':
        '원격 백업 설명이 손상되었습니다.',
    'Oznakowana: {utc} (BeatTime {beat})':
        '타임스탬프: {utc} (BeatTime {beat})',
    'Pliki wersji różnią się od spisu, który został oznakowany.':
        '버전의 파일이 타임스탬프를 찍은 목록과 다릅니다.',
    'Pobiera i odszyfrowuje pliki wybranej migawki':
        '선택한 스냅샷의 파일을 내려받아 복호화합니다',
    'Pobiera listę migawek z usługi':
        '서비스에서 스냅샷 목록을 내려받습니다',
    'Pobiera podpis tygodnia i stan kotwicy w Bitcoinie':
        '주간 서명과 Bitcoin 앵커 상태를 내려받습니다',
    'Pobieram potwierdzenia…':
        '확인서를 내려받는 중…',
    'Podaj hasło szyfrowania kopii poza domem.':
        '원격 백업의 암호화 비밀번호를 입력하세요.',
    'Podaj klucz tajny usługi.':
        '서비스의 비밀 키를 입력하세요.',
    'Podam dane ręcznie':
        '직접 입력',
    'Pominięte (otwarte w innych programach albo zmienione w trakcie): {count}.':
        '건너뜀(다른 프로그램에서 열려 있었거나 도중에 바뀜): {count}개.',
    'Porządkowanie kopii poza domem…':
        '원격 백업 정리 중…',
    'Potwierdzenia odświeżone.':
        '확인서를 새로 고쳤습니다.',
    'Poza dom':
        '원격',
    'Połączenie działa: zapis, odczyt i usuwanie się udały.':
        '연결이 정상입니다: 쓰기, 읽기, 삭제에 모두 성공했습니다.',
    'Połączenie nie działa: {error}':
        '연결이 되지 않습니다: {error}',
    'Przywraca pliki z zaszyfrowanej kopii w usłudze S3 — także na nowym komputerze':
        'S3 서비스에 있는 암호화된 백업에서 파일을 복원합니다 — 새 컴퓨터에서도 가능합니다',
    'Przywracanie z kopii poza domem':
        '원격 백업에서 복원',
    'Przywracanie {count} {files} z kopii poza domem…':
        '원격 백업에서 {files} {count}개 복원 중…',
    'Przywróć':
        '복원',
    'Region:':
        '리전:',
    'Skąd':
        '가져올 위치',
    'Spis wersji zgodny ze znacznikiem: {answer}':
        '버전 목록이 타임스탬프와 일치: {answer}',
    'Spis wersji został zmieniony po oznakowaniu.':
        '타임스탬프를 찍은 뒤 버전 목록이 변경되었습니다.',
    'Sprawdza spis wersji, drogę w drzewie tygodnia i podpis — bez sieci':
        '버전 목록, 주간 트리의 경로, 서명을 확인합니다 — 네트워크 없이',
    'Sprawdzam połączenie…':
        '연결을 확인하는 중…',
    'Sprawdź':
        '확인',
    'Sprawdź połączenie':
        '연결 확인',
    'Starsze migawki są usuwane, gdy nadmiar sięgnie kilku — co kilka dni.':
        '초과분이 몇 개 쌓이면 오래된 스냅샷을 삭제합니다 — 며칠에 한 번꼴입니다.',
    'Suma w drzewie tygodnia: {answer}':
        '주간 트리에 해시 포함: {answer}',
    'Suma wersji nie należy do drzewa tygodnia podanego w potwierdzeniu.':
        '버전 해시가 확인서에 적힌 주간 트리에 속하지 않습니다.',
    'Ta wersja nie ma znacznika czasu.':
        '이 버전에는 타임스탬프가 없습니다.',
    'Także po kopiach planowych. Wysyłane są tylko pliki nowe i zmienione.':
        '예약 백업 후에도 업로드합니다. 새 파일과 바뀐 파일만 업로드합니다.',
    'Tydzień jeszcze się nie zamknął — podpis pojawi się po poniedziałku 00:00 UTC.':
        '주가 아직 마감되지 않았습니다 — 서명은 월요일 00:00 UTC 이후에 추가됩니다.',
    'Usunięto starsze migawki: {count}, nieużywane fragmenty: {chunks}.':
        '오래된 스냅샷 {count}개와 사용하지 않는 조각 {chunks}개를 삭제했습니다.',
    'Usługa chwilowo niedostępna ({status}).':
        '서비스를 일시적으로 사용할 수 없습니다({status}).',
    'Usługa odrzuciła żądanie ({status} {code}): {message}':
        '서비스가 요청을 거부했습니다({status} {code}): {message}',
    'Usługa przechowywania':
        '스토리지 서비스',
    'Usługa zwróciła inną treść niż zapisana.':
        '서비스가 저장한 것과 다른 내용을 반환했습니다.',
    'Usługa:':
        '서비스:',
    'Uzupełnij adres usługi, nazwę kubełka i klucze dostępu.':
        '서비스 주소, 버킷 이름, 액세스 키를 입력하세요.',
    'Uzupełnij adres usługi, region, kubełek i identyfikator klucza.':
        '서비스 주소, 리전, 버킷, 키 ID를 입력하세요.',
    'W tym katalogu kopii nie ma jeszcze znaczników czasu.':
        '이 백업 폴더에는 아직 타임스탬프가 없습니다.',
    'W tym miejscu nie ma jeszcze kopii poza domem.':
        '이 위치에는 아직 원격 백업이 없습니다.',
    'Wczytaj migawki':
        '스냅샷 불러오기',
    'Wczytaj migawki i wybierz jedną z listy.':
        '스냅샷을 불러온 뒤 목록에서 하나를 선택하세요.',
    'Wczytuję migawkę {stamp}…':
        '스냅샷 {stamp} 불러오는 중…',
    'Wczytuję poprzednią migawkę kopii poza domem…':
        '원격 백업의 이전 스냅샷을 불러오는 중…',
    'Wybierz migawkę i katalog, do którego trafią pliki.':
        '스냅샷과 파일을 저장할 폴더를 선택하세요.',
    'Wybierz wersję z listy.':
        '목록에서 버전을 선택하세요.',
    'Wysyłaj poza dom po każdej udanej kopii z tego szablonu':
        '이 템플릿의 백업이 성공할 때마다 원격으로 업로드',
    'Wysyłam poza dom pliki nowe i zmienione: {count}…':
        '새 파일과 바뀐 파일을 원격으로 업로드하는 중: {count}개…',
    'Z kopii poza domem…':
        '원격 백업에서…',
    'Zachowuj migawek:':
        '보관할 스냅샷 수:',
    'Zapisuje ustawienia; klucz i hasło trafiają do Menedżera poświadczeń Windows':
        '설정을 저장합니다. 키와 비밀번호는 Windows 자격 증명 관리자에 보관됩니다',
    'Zapisuje, odczytuje i usuwa mały plik próbny':
        '작은 시험 파일을 쓰고, 읽고, 삭제합니다',
    'Zapisuję migawkę {stamp}…':
        '스냅샷 {stamp} 저장 중…',
    'Znacznik dowodzi, że wersja kopii w dokładnie tym kształcie istniała w podanej chwili. Podpis tygodnia pojawia się po jego zamknięciu (poniedziałek 00:00 UTC), a kotwica w Bitcoinie — zwykle kilka godzin później.':
        '타임스탬프는 백업 버전이 정확히 이 모습으로 해당 시각에 존재했음을 증명합니다. 주간 서명은 주가 마감된 뒤(월요일 00:00 UTC)에, Bitcoin 앵커는 보통 그로부터 몇 시간 뒤에 추가됩니다.',
    'Znacznika czasu nie udało się zapisać: {error}':
        '타임스탬프를 저장하지 못했습니다: {error}',
    'Znaczniki czasu':
        '타임스탬프',
    'Znaczniki czasu…':
        '타임스탬프…',
    'kopia poza domem':
        '원격 백업',
    'np. komputer-domowy':
        '예: home-computer',
    'oznakowana {when} — podpis po zamknięciu tygodnia':
        '{when}에 타임스탬프 찍음 — 주 마감 후 서명',
    'podpisana (tydzień {week}){bitcoin}':
        '서명됨({week} 주){bitcoin}',
    'poprawny':
        '유효함',
    'przywracanie z kopii poza domem':
        '원격 백업에서 복원',
    'Łączę się z usługą…':
        '서비스에 연결하는 중…',
    ' dni':
        ' 일',
    ' mies.':
        ' 개월',
    ' tyg.':
        ' 주',
    'Ile ostatnich wersji zachować. Starsze są kasowane po udanym przebiegu.':
        '보관할 최근 버전 수입니다. 더 오래된 버전은 실행이 성공한 뒤 삭제됩니다.',
    'Kalendarz zostawia najnowszą wersję z każdego z ostatnich dni, tygodni\ni miesięcy — gęsto dla świeżych zmian, rzadko dla dawnych. Nadmiar jest\nkasowany po udanym przebiegu; wersje niedokończone nigdy.':
        '달력 방식은 최근 며칠, 몇 주, 몇 달 각각에서 가장 최신 버전을\n남깁니다 — 최근 변경은 촘촘하게, 오래된 변경은 듬성듬성하게. 나머지는\n실행이 성공한 뒤 삭제되며, 미완료 버전은 절대 삭제되지 않습니다.',
    'Z ilu ostatnich dni zachować po jednej, najnowszej wersji.':
        '최신 버전을 하루에 하나씩 보관할 최근 일수입니다.',
    'Z ilu ostatnich miesięcy zachować po jednej, najnowszej wersji.':
        '최신 버전을 한 달에 하나씩 보관할 최근 개월 수입니다.',
    'Z ilu ostatnich tygodni zachować po jednej, najnowszej wersji.':
        '최신 버전을 한 주에 하나씩 보관할 최근 주 수입니다.',
    'Zachowuj:':
        '보관:',
    'kalendarz: dni, tygodnie, miesiące':
        '달력: 일, 주, 월',
    'ostatnie wersje':
        '최근 버전',
    'wszystkie wersje':
        '모든 버전',
    ' (niedokończona)':
        ' (미완료)',
    'Fragment nazwy albo ścieżki, bez rozróżniania wielkości liter.':
        '이름이나 경로의 일부입니다. 대소문자를 구분하지 않습니다.',
    'Główny folder kopii':
        '백업 최상위 폴더',
    'Historia pliku':
        '파일 기록',
    'Nazwa':
        '이름',
    'Nic nie znaleziono.':
        '찾은 항목이 없습니다.',
    'Nie udało się: {error}':
        '실패했습니다: {error}',
    'Odtwarza plik do katalogu tymczasowego i otwiera go':
        '파일을 임시 폴더에 복원해 엽니다',
    'Odtwarza plik w wybranym miejscu':
        '파일을 선택한 위치에 복원합니다',
    'Odtwarzam „{name}”…':
        '‘{name}’ 복원 중…',
    'Otwarto kopię „{name}” (plik tymczasowy, zniknie po zamknięciu programu).':
        '‘{name}’의 사본을 열었습니다(임시 파일이며 프로그램을 닫으면 사라집니다).',
    'Otwórz':
        '열기',
    'Otwórz kopię':
        '사본 열기',
    'Pliki i wersje wprost z kopii — bez przywracania':
        '백업에서 바로 보는 파일과 버전 — 복원할 필요 없음',
    'Pliki i wersje wprost z kopii — bez przywracania całości.':
        '백업에서 바로 보는 파일과 버전 — 전체를 복원할 필요가 없습니다.',
    'Pokazuje pliki i wersje tej kopii — pojedynczy plik otworzysz bez przywracania całości':
        '이 백업의 파일과 버전을 보여 줍니다 — 전체를 복원하지 않고도 파일 하나를 열 수 있습니다',
    'Pokaż foldery':
        '폴더 보기',
    'Przeglądaj…':
        '찾아보기…',
    'Przeglądanie':
        '찾아보기',
    'Przeszukuje spis treści kopii':
        '백업 목차를 검색합니다',
    'Rozmiar':
        '크기',
    'Szukaj':
        '검색',
    'Szukaj pliku w najnowszym stanie kopii…':
        '백업의 최신 상태에서 파일 검색…',
    'Szukam…':
        '검색 중…',
    'W których wersjach jest ten plik i kiedy się zmieniał':
        '이 파일이 어느 버전에 있고 언제 바뀌었는지 보여 줍니다',
    'W tym folderze nie ma wersji kopii.':
        '이 폴더에는 백업 버전이 없습니다.',
    'Wczytuje wersje z tego folderu kopii':
        '이 백업 폴더에서 버전을 불러옵니다',
    'Wersja kopii, której zawartość widzisz poniżej.':
        '아래에 내용이 표시되는 백업 버전입니다.',
    'Wersja: {version}':
        '버전: {version}',
    'Wersje z tym plikiem: {count}. Dwuklik otwiera kopię z danej wersji.':
        '이 파일이 있는 버전: {count}개. 두 번 클릭하면 해당 버전의 사본이 열립니다.',
    'Wraca z wyników wyszukiwania do drzewa folderów':
        '검색 결과에서 폴더 트리로 돌아갑니다',
    'Wskaż folder kopii i kliknij „Otwórz”.':
        '백업 폴더를 지정하고 ‘열기’를 클릭하세요.',
    'Zapisano: {path}':
        '저장했습니다: {path}',
    'Zapisz jako…':
        '다른 이름으로 저장…',
    'Zapisz kopię pliku':
        '파일 사본 저장',
    'Zaznacz plik i wybierz „Otwórz kopię”, żeby zajrzeć do niego w zwykłym programie, albo „Historia pliku”, żeby zobaczyć, w których wersjach się zmieniał.':
        '파일을 선택한 다음, 평소 쓰는 프로그램으로 보려면 ‘사본 열기’를, 어느 버전에서 바뀌었는지 보려면 ‘파일 기록’을 선택하세요.',
    'Zmieniono':
        '수정한 날짜',
    'Znalezione pliki: {count}. Wyniki pochodzą z najnowszego stanu kopii.':
        '찾은 파일: {count}개. 결과는 백업의 최신 상태 기준입니다.',
    'przeglądanie kopii':
        '백업 찾아보기',
    'zmieniony':
        '변경됨',
    'najstarsza zachowana kopia':
        '보관된 가장 오래된 사본',
    'Foldery w AppData':
        'AppData의 폴더',
    'Przywracanie utworzy nowe foldery bezpośrednio w AppData:\n\n{folders}\n\nWindows pozwala wersji programu ze Sklepu tworzyć je tylko w jej prywatnej kopii — pliki będą widoczne w tym programie, ale nie w programie, do którego należą.\n\nNajprościej: zainstaluj i raz uruchom tamten program (utworzy swój folder), a potem przywróć jeszcze raz. Albo przywróć do zwykłego folderu i przenieś pliki Eksploratorem.':
        '복원하면 AppData에 바로 새 폴더가 만들어집니다:\n\n{folders}\n\nWindows는 Microsoft Store 버전의 이 프로그램이 이런 폴더를 자체 전용 사본 안에만 만들도록 허용합니다 — 파일은 이 프로그램에서는 보이지만, 그 파일이 속한 프로그램에서는 보이지 않습니다.\n\n가장 쉬운 방법: 해당 프로그램을 설치하고 한 번 실행한 뒤(그 프로그램이 자체 폴더를 만듭니다) 다시 복원하세요. 또는 일반 폴더에 복원한 다음 파일 탐색기로 파일을 옮기세요.',
    'Przywracanie utworzyłoby w AppData nowe foldery, których inne programy nie zobaczą: {folders}':
        '복원하면 다른 프로그램에서 보이지 않는 새 폴더가 AppData에 만들어집니다: {folders}',
    'Przywracanie wstrzymane do decyzji.':
        '결정할 때까지 복원을 일시 중지했습니다.',
    'Przywróć mimo to':
        '그래도 복원',
    'Start programu przy logowaniu wyłączono w Ustawieniach Windows. Włączysz go tam: Ustawienia → Aplikacje → Uruchamianie → Sigelith Backup.':
        '로그인 시 프로그램 시작이 Windows 설정에서 꺼져 있습니다. 그곳에서 켤 수 있습니다: 설정 → 앱 → 시작 프로그램 → Sigelith Backup.',
    'Start przy logowaniu':
        '로그인 시 시작',
    'Start przy logowaniu wyłączono w Ustawieniach Windows → Aplikacje → Uruchamianie; dopóki go tam nie włączysz, kopie planowe działają tylko przy otwartym programie.':
        '로그인 시 시작이 Windows 설정 → 앱 → 시작 프로그램에서 꺼져 있습니다. 그곳에서 다시 켜기 전까지 예약 백업은 프로그램이 열려 있을 때만 작동합니다.',
    'Ten sam przełącznik jest w Ustawieniach Windows → Aplikacje → Uruchamianie. Wyłączony tam da się włączyć tylko tam.':
        '같은 스위치가 Windows 설정 → 앱 → 시작 프로그램에도 있습니다. 그곳에서 끈 경우 그곳에서만 다시 켤 수 있습니다.',
    'Brak pliku {name} w katalogu programu.':
        '프로그램 폴더에 {name} 파일이 없습니다.',
    'Jakie dane program przetwarza i gdzie':
        '프로그램이 어떤 데이터를 어디에서 처리하는지',
    'Kod źródłowy Qt':
        'Qt 소스 코드',
    'Licencja programu':
        '프로그램 라이선스',
    'Licencja programu i licencje użytych składników':
        '프로그램 라이선스와 사용한 구성 요소의 라이선스',
    'Licencje':
        '라이선스',
    'Licencje i prywatność':
        '라이선스 및 개인정보',
    'Licencje…':
        '라이선스…',
    'Otwiera folder z plikami licencji w Eksploratorze':
        '파일 탐색기에서 라이선스 파일이 있는 폴더를 엽니다',
    'Pokaż pliki licencji':
        '라이선스 파일 보기',
    'Polityka prywatności':
        '개인정보 처리방침',
    'Polityka prywatności…':
        '개인정보 처리방침…',
    'Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0 — to osobne pliki w katalogu programu, które można zastąpić zgodnymi wersjami. Kod źródłowy wersji dołączonych do programu: {qt} oraz {pyside}.':
        '이 프로그램은 LGPL-3.0 라이선스의 Qt 및 PySide6 라이브러리를 사용합니다 — 이 라이브러리는 프로그램 폴더에 있는 별도 파일이며 호환되는 버전으로 교체할 수 있습니다. 프로그램에 포함된 버전의 소스 코드: {qt}, {pyside}.',
    'Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0, z Pythona i z innych składników na licencjach otwartych (m.in. MIT, BSD, Apache 2.0); ikony: Bootstrap Icons (MIT). Wykaz, prawa autorskie, pełne teksty licencji i adresy kodu źródłowego Qt są pod przyciskiem „Licencje”.':
        '이 프로그램은 LGPL-3.0 라이선스의 Qt 및 PySide6 라이브러리, Python, 그 밖의 오픈 소스 라이선스(MIT, BSD, Apache 2.0 등) 구성 요소를 사용합니다. 아이콘: Bootstrap Icons(MIT). 목록, 저작권 고지, 라이선스 전문, Qt 소스 코드 주소는 ‘라이선스’ 버튼에서 볼 수 있습니다.',
    'Program usunie z Menedżera poświadczeń Windows wszystkie hasła, które zapamiętał: hasła kopii i dane dostępu do kopii poza domem. Kopie planowe szablonów zaszyfrowanych będą potem czekać, aż podasz hasło.\n\nUsunąć?':
        '프로그램이 기억해 둔 모든 비밀번호(백업 비밀번호와 원격 백업 접속 정보)를 Windows 자격 증명 관리자에서 삭제합니다. 그 후 암호화된 템플릿의 예약 백업은 비밀번호를 입력할 때까지 기다립니다.\n\n삭제할까요?',
    'Składniki i ich licencje':
        '구성 요소와 라이선스',
    'Strona z kodem źródłowym Qt w wersji użytej w programie':
        '프로그램에 사용된 버전의 Qt 소스 코드 페이지',
    'Usunięte zapamiętane hasła: {count}.':
        '저장된 비밀번호 {count}개를 삭제했습니다.',
    'Usuwa z Menedżera poświadczeń Windows wszystkie hasła zapamiętane przez program — na przykład przed odinstalowaniem':
        '프로그램이 기억해 둔 모든 비밀번호를 Windows 자격 증명 관리자에서 삭제합니다 — 예를 들어 프로그램을 제거하기 전에',
    'Usuń zapamiętane hasła':
        '저장된 비밀번호 삭제',
    'Usuń zapamiętane hasła…':
        '저장된 비밀번호 삭제…',
    '© {years} {publisher}. Wolne oprogramowanie na licencji GNU GPL w wersji 3 lub nowszej.':
        '© {years} {publisher}. GNU GPL 버전 3 이상으로 배포되는 자유 소프트웨어입니다.',
    'Kod źródłowy':
        '소스 코드',
    'Kod źródłowy programu w serwisie GitHub':
        'GitHub에 있는 프로그램 소스 코드',
    'Sigelith odrzucił żądanie ({status}): {detail}':
        'Sigelith가 요청을 거부했습니다({status}): {detail}',
    'Nie udało się połączyć z Sigelith: {error}':
        'Sigelith에 연결하지 못했습니다: {error}',
    'Sigelith odesłał potwierdzenie innej sumy kontrolnej.':
        'Sigelith가 다른 해시에 대한 확인서를 보냈습니다.',
    'Znacznik czeka na połączenie z Sigelith.':
        '타임스탬프가 Sigelith 연결을 기다리는 중입니다.',
    'Podpis tygodnia nie zgadza się z kluczem Sigelith zapisanym w programie.':
        '주간 서명이 프로그램에 내장된 Sigelith 키와 일치하지 않습니다.',
    'Otwiera certyfikat znacznika na stronie Sigelith':
        'Sigelith 웹사이트에서 타임스탬프 인증서를 엽니다',
    'Podpis Sigelith: {answer}':
        'Sigelith 서명: {answer}',
    'Znaczniki Sigelith wersji w tym katalogu kopii: sprawdzenie i certyfikat':
        '이 백업 폴더에 있는 버전의 Sigelith 타임스탬프: 확인 및 인증서',
    'Znakuję wersję czasem Sigelith (wysyłana jest tylko suma kontrolna)…':
        'Sigelith로 버전에 타임스탬프를 찍는 중(해시만 전송)…',
    'Znacznik czasu czeka na połączenie z Sigelith — zostanie wysłany przy następnej kopii.':
        '타임스탬프가 Sigelith 연결을 기다리는 중입니다 — 다음 백업 때 전송됩니다.',
    'Znakuj wersję czasem Sigelith':
        'Sigelith로 버전에 타임스탬프 찍기',
    'Znaczniki czasu Sigelith':
        'Sigelith 타임스탬프',
    'czeka na połączenie z Sigelith':
        'Sigelith 연결 대기 중',
    'Dowód, że kopia w tym kształcie istniała danego dnia (podpis Ed25519, kotwica\nw Bitcoinie). Do sigelith.org trafia wyłącznie suma kontrolna spisu wersji —\nżadne nazwy plików ani ich treść.':
        '백업이 그날 정확히 이 모습으로 존재했다는 증명입니다(Ed25519 서명, Bitcoin\n앵커). sigelith.org에는 버전 목록의 해시만 전송됩니다 —\n파일 이름이나 내용은 전송되지 않습니다.',
    'Kopie zapasowe folderów na dysk zewnętrzny, z historią wersji i szyfrowaniem. Wszystko dzieje się na Twoim komputerze, bez konta i bez telemetrii. Z internetem program łączy się tylko wtedy, gdy sam włączysz kopię poza domem albo znaczniki czasu Sigelith.':
        '폴더를 외장 드라이브에 백업하며, 버전 기록과 암호화를 지원합니다. 모든 작업은 사용자의 컴퓨터에서 이루어지며, 계정도 필요 없고 사용 데이터도 수집하지 않습니다. 프로그램은 사용자가 원격 백업이나 Sigelith 타임스탬프를 직접 켰을 때만 인터넷에 연결합니다.',
    'Bez dokumentu: {count} {stamps} — plik zmienił się po stemplu albo zniknął i nie ma go w żadnej wersji tej kopii ({names}). Sam dowód jest zachowany.':
        '문서 없음: {stamps} {count}개 — 스탬프 후 파일이 바뀌었거나 사라져 이 백업의 어느 버전에도 없습니다({names}). 증명 자체는 보관되어 있습니다.',
    'Brak pliku dowodu albo dowód jest zaszyfrowany.':
        '증명 파일이 없거나 증명이 암호화되어 있습니다.',
    'Chroni dowody Sigelith: historię stempli i oznakowane dokumenty.':
        'Sigelith 증거를 보호합니다: 스탬프 내역과 스탬프를 찍은 문서.',
    'Chroń dowody Sigelith':
        'Sigelith 증거 보호',
    'Chroń też dowody Sigelith':
        'Sigelith 증거도 보호',
    'Dokument':
        '문서',
    'Dokumenty oznakowane w Sigelith, zabezpieczone w tej kopii: sprawdzenie i odzyskanie':
        '이 백업에 보관된 Sigelith 스탬프 문서: 확인 및 복구',
    'Dowody Sigelith':
        'Sigelith 증거',
    'Dowody Sigelith: historia stempli i dokładne kopie oznakowanych dokumentów z plikami .beatproof trafią do magazynu dowodów w katalogu kopii.':
        'Sigelith 증거: 스탬프 내역과 스탬프를 찍은 문서의 정확한 사본이 .beatproof 파일과 함께 백업 폴더의 증거 저장소에 보관됩니다.',
    'Dowody Sigelith: zabezpieczone dokumenty {count} z {total}':
        'Sigelith 증거: 문서 {total}개 중 {count}개 보관',
    'Dowody Sigelith…':
        'Sigelith 증거…',
    'Dowody z problemem: {count} — szczegóły w kolumnie „Stan”.':
        '문제가 있는 증명: {count}개 — 자세한 내용은 ‘상태’ 열을 확인하세요.',
    'Dowodów Sigelith nie udało się zabezpieczyć: {error}':
        'Sigelith 증거를 보관하지 못했습니다: {error}',
    "Droga w drzewie Merkle'a nie prowadzi do podpisanego korzenia tygodnia.":
        'Merkle 트리의 경로가 서명된 주간 루트로 이어지지 않습니다.',
    'Gdzie zapisać dokumenty i dowody':
        '문서와 증명을 저장할 위치',
    'Historia stempli Sigelith Desktop i dokładne bajty oznakowanych dokumentów, z plikami .beatproof — w osobnym magazynie, którego retencja nie sprząta.':
        'Sigelith Desktop의 스탬프 내역과 스탬프를 찍은 문서의 정확한 바이트를 .beatproof 파일과 함께 보관합니다 — 보존 정책으로 정리되지 않는 별도의 저장소에.',
    'Każdy stempel ma tu swój folder z dokładnie tym dokumentem, który oznakowano, i plikiem .beatproof. „Sprawdź” liczy sumę każdego dokumentu i sprawdza podpis tygodnia bez łączenia się z siecią.':
        '여기에는 스탬프마다 스탬프를 찍은 바로 그 문서와 .beatproof 파일이 든 폴더가 있습니다. ‘확인’은 네트워크에 연결하지 않고 각 문서의 해시를 계산하고 주간 서명을 확인합니다.',
    'Kopia obejmie folder danych Sigelith Desktop (historię stempli), a każdy oznakowany\ndokument trafi — dokładnie w tej postaci, którą oznakowano — do magazynu dowodów\nw katalogu kopii, razem z plikiem .beatproof. Starych wersji magazyn nie dotyczy:\nretencja go nie sprząta.':
        '백업에 Sigelith Desktop 데이터 폴더(스탬프 내역)가 포함되며, 스탬프를 찍은 각 문서는\n스탬프를 찍은 바로 그 모습 그대로 .beatproof 파일과 함께 백업 폴더의\n증거 저장소에 보관됩니다. 이 저장소는 이전 버전과 별개이므로\n보존 정책으로 정리되지 않습니다.',
    'Magazyn dowodów jest pusty.':
        '증거 저장소가 비어 있습니다.',
    'Na tym komputerze jest Sigelith Desktop: {count} {stamps}.':
        '이 컴퓨터에 Sigelith Desktop이 있습니다: {stamps} {count}개.',
    'Na tym komputerze nie ma danych Sigelith Desktop.':
        '이 컴퓨터에 Sigelith Desktop 데이터가 없습니다.',
    'Otwórz folder dowodów':
        '증거 폴더 열기',
    'Oznakowano':
        '스탬프 시각',
    'Pokazuje magazyn dowodów w Eksploratorze':
        '파일 탐색기에서 증거 저장소를 보여 줍니다',
    'Przywróć zaznaczone…':
        '선택 항목 복원…',
    'Sigelith Desktop: {count} {stamps} w folderze {path}.':
        'Sigelith Desktop: {path} 폴더에 {stamps} {count}개.',
    'Sprawdza każdy dokument i jego dowód bez łączenia z siecią':
        '네트워크에 연결하지 않고 각 문서와 그 증명을 확인합니다',
    'Sprawdzam dowody…':
        '증명 확인 중…',
    'Stan':
        '상태',
    'Stemple w magazynie: {count}, z dokumentem: {documents}.':
        '저장소의 스탬프: {count}개, 문서가 있는 스탬프: {documents}개.',
    'Suma dokumentu nie zgadza się z dowodem.':
        '문서의 해시가 증명과 일치하지 않습니다.',
    'To nie jest plik dowodu Sigelith (beatproof-v1).':
        'Sigelith 증명 파일(beatproof-v1)이 아닙니다.',
    'Tydzień stempla jeszcze się nie zamknął — podpis dojdzie przy kolejnej kopii.':
        '스탬프가 속한 주가 아직 마감되지 않았습니다 — 서명은 다음 백업 때 추가됩니다.',
    'W magazynie nie ma dokumentu do tego dowodu.':
        '저장소에 이 증명의 문서가 없습니다.',
    'Wszystkie dowody pasują do dokumentów i mają poprawny podpis.':
        '모든 증명이 문서와 일치하며 서명도 유효합니다.',
    'Zabezpieczam dokumenty oznakowane w Sigelith…':
        'Sigelith 스탬프 문서를 보관하는 중…',
    'Zapisano pliki: {count} w {path}.':
        '{path}에 파일 {count}개를 저장했습니다.',
    'Zapisuje dokumenty razem z plikami .beatproof we wskazanym folderze':
        '문서를 .beatproof 파일과 함께 지정한 폴더에 저장합니다',
    'bez dokumentu — dowód zachowany':
        '문서 없음 — 증명은 보관됨',
    'czekają na podpis tygodnia: {count}':
        '주간 서명 대기: {count}개',
    'dokument i dowód są w kopii':
        '문서와 증명이 백업에 있음',
    'dokument jest; dowód czeka na podpis tygodnia':
        '문서 있음, 증명은 주간 서명 대기 중',
    'dowodu nie da się odczytać':
        '증명을 읽을 수 없음',
    'dowody Sigelith':
        'Sigelith 증거',
    'dowody uzupełnione o podpis tygodnia: {count}':
        '주간 서명이 추가된 증명: {count}개',
    'nowe: {count}':
        '새 항목: {count}개',
    'odtworzone ze starszych wersji kopii: {count}':
        '이전 백업 버전에서 복구: {count}개',
    'sprawdzony: dokument i dowód się zgadzają':
        '확인됨: 문서와 증명이 일치',
    'stempel':
        '스탬프',
    'stemple':
        '스탬프',
    'stempli':
        '스탬프',
    'zaszyfrowany — podaj hasło, żeby sprawdzić':
        '암호화됨 — 확인하려면 비밀번호를 입력하세요',
    'Chroń dowody Sigelith, gdy go zainstaluję':
        'Sigelith Desktop을 설치하면 Sigelith 증거 보호',
    'Dowody Sigelith: na tym komputerze nie ma jeszcze Sigelith Desktop — ochrona zacznie działać sama, gdy się pojawi.':
        'Sigelith 증거: 이 컴퓨터에 아직 Sigelith Desktop이 없습니다 — 설치되면 보호가 자동으로 시작됩니다.',
    'Dowody Sigelith: ochrona zacznie działać sama, gdy zainstalujesz Sigelith Desktop.':
        'Sigelith 증거: Sigelith Desktop을 설치하면 보호가 자동으로 시작됩니다.',
    'Dowody czasu dla ważnych dokumentów':
        '중요한 문서를 위한 시간 증명',
    'Kopia zachowa każdy dokument oznakowany w Sigelith Desktop dokładnie w tej postaci, którą oznakowano, razem z dowodem — nawet gdy oryginał później się zmieni.':
        'Sigelith Desktop에서 스탬프를 찍은 모든 문서를 스탬프를 찍은 바로 그 모습 그대로 증명과 함께 백업에 보관합니다 — 나중에 원본이 바뀌더라도.',
    'Ochrona zacznie działać sama, gdy na komputerze pojawi się Sigelith Desktop.':
        '컴퓨터에 Sigelith Desktop이 설치되면 보호가 자동으로 시작됩니다.',
    'Otwiera stronę programu Sigelith Desktop':
        'Sigelith Desktop 페이지를 엽니다',
    'Poznaj Sigelith Desktop':
        'Sigelith Desktop 알아보기',
    'Sigelith Desktop, program tego samego wydawcy, oznakuje dokument czasem: to podpisany dowód, że plik w tej postaci istniał w danej chwili, sprawdzalny bez udziału kogokolwiek. Sigelith Backup przechowa potem każdy oznakowany dokument razem z dowodem.':
        '같은 게시자의 프로그램인 Sigelith Desktop은 문서에 타임스탬프를 찍습니다. 파일이 특정 시각에 정확히 이 모습으로 존재했다는 서명된 증명으로, 누구에게도 의존하지 않고 확인할 수 있습니다. 그러면 Sigelith Backup이 스탬프를 찍은 모든 문서를 증명과 함께 보관합니다.',
    'Umowy, faktury, projekty — czasem trzeba wykazać, że dokument istniał danego dnia.':
        '계약서, 청구서, 프로젝트 — 문서가 특정 날짜에 존재했음을 입증해야 할 때가 있습니다.',
    'Nieznany format spisu wersji.':
        '알 수 없는 버전 목록 형식입니다.',
    'Ta wersja nie ma pieczęci dla pojedynczych plików (kopia sprzed wersji 3.0 albo bez znaczników czasu).':
        '이 버전에는 개별 파일용 봉인이 없습니다(버전 3.0 이전에 만들었거나 타임스탬프 없이 만든 백업).',
    'Pieczęć tej wersji czeka jeszcze na podpis tygodnia Sigelith — dowód będzie gotowy po poniedziałku 00:00 UTC i kolejnej kopii.':
        '이 버전의 봉인은 아직 Sigelith 주간 서명을 기다리고 있습니다 — 증명은 월요일 00:00 UTC 이후 다음 백업을 마치면 준비됩니다.',
    'Brak oświadczenia pieczęci w folderze wersji.':
        '버전 폴더에 봉인 선언이 없습니다.',
    'Oświadczenie pieczęci nie zgadza się z pieczęcią wersji.':
        '봉인 선언이 버전 봉인과 일치하지 않습니다.',
    'Drzewo plików wersji nie zgadza się z pieczęcią.':
        '버전의 파일 트리가 봉인과 일치하지 않습니다.',
    'Tego pliku nie ma w spisie tej wersji.':
        '이 파일은 이 버전의 목록에 없습니다.',
    'To nie jest dowód pliku z kopii Sigelith Backup ({format}).':
        'Sigelith Backup 파일 증명이 아닙니다({format}).',
    'Dowód jest uszkodzony — brakuje pól albo mają zły format.':
        '증명이 손상되었습니다 — 항목이 없거나 형식이 잘못되었습니다.',
    'Ten plik nie jest plikiem, którego dotyczy dowód.':
        '이 파일은 증명의 대상 파일이 아닙니다.',
    'Ścieżka pliku w dowodzie nie zgadza się z liściem drzewa.':
        '증명의 파일 경로가 트리의 잎과 일치하지 않습니다.',
    'Droga w drzewie plików nie prowadzi do korzenia z pieczęci.':
        '파일 트리의 경로가 봉인된 루트로 이어지지 않습니다.',
    'Oświadczenie pieczęci nie potwierdza tego drzewa plików.':
        '봉인 선언이 이 파일 트리를 확인하지 않습니다.',
    'Potwierdzenie Sigelith nie dotyczy tej pieczęci.':
        'Sigelith 확인이 이 봉인에 대한 것이 아닙니다.',
    'Dowód czasu…':
        '시간 증명…',
    'Zapisuje dowód, że ten plik był w kopii w chwili jej oznakowania — bez ujawniania innych plików':
        '백업에 타임스탬프를 찍은 시점에 이 파일이 백업 안에 있었다는 증명을 저장합니다 — 다른 파일은 드러내지 않습니다',
    'Dowód czasu':
        '시간 증명',
    'Dołączyć do dowodu ścieżkę pliku w kopii („{path}”)?\n\nBez niej dowód dalej potwierdza plik i chwilę oznakowania, ale nie mówi, gdzie plik leżał.':
        '백업 안의 파일 경로(‘{path}’)를 증명에 포함할까요?\n\n경로가 없어도 증명은 파일과 타임스탬프 시각을 확인해 주지만, 파일이 어디에 있었는지는 알려 주지 않습니다.',
    'Przygotowuję dowód dla „{name}”…':
        '‘{name}’의 증명을 준비하는 중…',
    'Zapisz dowód czasu':
        '시간 증명 저장',
    'Dowód pliku Sigelith (*{suffix})':
        'Sigelith 파일 증명 (*{suffix})',
    'Zapisano dowód i certyfikat PDF: {path}. Sprawdzi go Sigelith Desktop albo strona sigelith.org/verify/.':
        '증명과 PDF 인증서를 저장했습니다: {path}. Sigelith Desktop이나 sigelith.org/verify/ 페이지에서 확인할 수 있습니다.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją sprawdzić.':
        '암호화된 백업입니다 — 확인하려면 비밀번호를 입력하세요.',
    'Ta wersja nie ma pieczęci — nie ma z czym porównać plików.':
        '이 버전에는 봉인이 없습니다 — 파일을 비교할 기준이 없습니다.',
    'Pieczęć wersji się nie potwierdza: {problems}':
        '버전 봉인이 확인되지 않습니다: {problems}',
    'brak podpisu tygodnia':
        '주간 서명 없음',
    'Audyt przerwany.':
        '감사를 중단했습니다.',
    'próbka {checked} z {listed} plików':
        '파일 {listed}개 중 {checked}개 표본',
    'wszystkie pliki ({count})':
        '모든 파일({count}개)',
    'Nietknięta: sprawdzono {scope}, wszystko zgodne z pieczęcią w publicznym dzienniku.':
        '온전함: 확인 범위 {scope} — 모두 공개 로그의 봉인과 일치합니다.',
    'zmienione: {files}':
        '변경됨: {files}',
    'brakujące: {files}':
        '누락됨: {files}',
    'nieczytelne albo uszkodzone: {files}':
        '읽을 수 없거나 손상됨: {files}',
    'PODMIENIONA albo uszkodzona ({scope}) — {details}.':
        '변조 또는 손상됨({scope}) — {details}.',
    'Audyt treści':
        '내용 감사',
    'Czyta z nośnika każdy plik tej wersji i porównuje go z sumą oznakowaną w publicznym dzienniku':
        '이 버전의 모든 파일을 저장 매체에서 읽어 공개 로그에 봉인된 해시와 비교합니다',
    'Ostatnia nietknięta':
        '마지막 온전한 버전',
    'Sprawdza wersje od najnowszej i wskazuje ostatnią zgodną z pieczęcią — z niej przywracaj':
        '최신 버전부터 확인해 봉인과 일치하는 가장 최근 버전을 찾아 줍니다 — 그 버전에서 복원하세요',
    'Ostatnia nietknięta wersja: {label} — z niej przywracaj.':
        '마지막 온전한 버전: {label} — 이 버전에서 복원하세요.',
    'Żadna wersja z pieczęcią nie jest nietknięta.':
        '봉인된 버전 중 온전한 버전이 없습니다.',
    'Czytam pliki kopii i porównuję je z pieczęcią w publicznym dzienniku…':
        '백업 파일을 읽어 공개 로그의 봉인과 비교하는 중…',
    'Sprawdzam próbkę starszej wersji z pieczęcią w publicznym dzienniku…':
        '이전 버전의 표본을 공개 로그의 봉인과 대조하는 중…',
    'Audyt z pieczęcią: próbka wersji {label} zgodna z publicznym dziennikiem.':
        '봉인 감사: {label} 버전의 표본이 공개 로그와 일치합니다.',
    'UWAGA — audyt z pieczęcią, wersja {label}: {details}':
        '경고 — 봉인 감사, {label} 버전: {details}',
    'Przekaż…':
        '전달…',
    'Zapisuje tę wersję pliku i otwiera ją w Sigelith Handover — odbiorca potwierdzi odbiór własnym kluczem':
        '이 버전의 파일을 저장하고 Sigelith Handover에서 엽니다 — 수신자가 자신의 키로 수령을 확인합니다',
    'Przekazanie z dowodem doręczenia':
        '전달 증명과 함께 전달',
    'Przekazanie z dowodem doręczenia robi Sigelith Desktop (od wersji 3.0.1): odbiorca potwierdza odbiór własnym kluczem, a chwila doręczenia trafia do publicznego dziennika. Na tym komputerze go nie ma albo jest w starszej wersji. Otworzyć stronę programu?':
        '전달 증명과 함께 전달하는 기능은 Sigelith Desktop(버전 3.0.1 이상)에서 제공합니다. 수신자가 자신의 키로 수령을 확인하고, 전달 시점은 공개 로그에 기록됩니다. 이 컴퓨터에 Sigelith Desktop이 없거나 이전 버전입니다. 프로그램 페이지를 열까요?',
    'Zapisz plik do przekazania':
        '전달할 파일 저장',
    'Otwieram Sigelith Handover z plikiem „{name}” — wybierz odbiorcę.':
        '‘{name}’ 파일로 Sigelith Handover를 여는 중 — 수신자를 선택하세요.',
    'Kapsuły czasu…':
        '타임캡슐…',
    'Pliki zapieczętowane w tej kopii do daty — klucze wydają dopiero po niej sieć drand i serwer kluczy Sigelith':
        '이 백업 안에 특정 날짜까지 봉인된 파일 — 그 날짜가 지나야 drand 네트워크와 Sigelith 키 서버가 키를 공개합니다',
    'Wskaż najpierw folder kopii — kapsuła leży w kopii.':
        '먼저 백업 폴더를 지정하세요 — 캡슐은 백업 안에 보관됩니다.',
    'Kapsuły czasu':
        '타임캡슐',
    'Kapsuła pieczętuje wybrany folder do chwili, którą wskażesz. Otwierają ją dowolne dwie z trzech części: runda sieci drand z tej chwili, udział serwera kluczy Sigelith (wydawany dopiero po tej chwili — to zasada operatora, nie kryptografia) i kod odzyskiwania zapisany obok kapsuły. Kto ma tę kopię, ma więc i kod: do wcześniejszego otwarcia wystarczy mu, że operator złamie swoją zasadę. Po tej chwili otworzy ją każdy, kto ma jej pliki. Kapsuła leży w tej kopii, nie na serwerze; otwiera ją strona sigelith.org/capsule/.':
        '캡슐은 선택한 폴더를 지정한 시각까지 봉인합니다. 캡슐은 세 부분 중 아무 둘로 열립니다: 그 시각의 drand 네트워크 라운드, Sigelith 키 서버의 몫(그 시각이 지난 뒤에야 공개되며, 이는 암호학적 제약이 아니라 운영자의 원칙입니다), 그리고 캡슐 옆에 저장되는 복구 코드입니다. 따라서 이 백업을 가진 사람은 복구 코드도 가진 셈이며, 미리 열려면 운영자가 원칙을 어기기만 하면 됩니다. 그 시각이 지나면 캡슐 파일을 가진 누구나 열 수 있습니다. 캡슐은 서버가 아니라 이 백업 안에 있으며, sigelith.org/capsule/ 페이지에서 열 수 있습니다.',
    'Wybierz kapsułę z listy albo utwórz nową.':
        '목록에서 캡슐을 선택하거나 새로 만드세요.',
    'Nowa kapsuła…':
        '새 캡슐…',
    'Pieczętuje wybrany folder do daty':
        '선택한 폴더를 특정 날짜까지 봉인합니다',
    'Pokaż w folderze':
        '폴더에서 보기',
    'Otwiera folder kapsuły w Eksploratorze':
        '파일 탐색기에서 캡슐 폴더를 엽니다',
    'Otwórz na stronie':
        '웹사이트에서 열기',
    'Strona sigelith.org/capsule/ otwiera kapsułę po jej dacie':
        '날짜가 지나면 sigelith.org/capsule/ 페이지에서 캡슐을 열 수 있습니다',
    'można otworzyć':
        '열 수 있음',
    'zamknięta':
        '봉인됨',
    'W tej kopii nie ma jeszcze kapsuł czasu.':
        '이 백업에는 아직 타임캡슐이 없습니다.',
    'Ta kapsuła da się otworzyć na stronie sigelith.org/capsule/ — wskaż jej pliki.':
        '이 캡슐은 sigelith.org/capsule/ 페이지에서 열 수 있습니다 — 그곳에서 캡슐 파일을 지정하세요.',
    'Kapsuła jest zamknięta do daty z listy. Kod odzyskiwania leży w pliku obok niej.':
        '캡슐은 목록에 표시된 날짜까지 봉인되어 있습니다. 복구 코드는 캡슐 옆 파일에 있습니다.',
    'Wybierz folder do zapieczętowania':
        '봉인할 폴더 선택',
    'Pieczętuję „{name}” — kilka sekund na krzywej eliptycznej…':
        '‘{name}’ 봉인 중 — 타원 곡선 계산에 몇 초 걸립니다…',
    'kapsuła czasu':
        '타임캡슐',
    'Kapsuła zapieczętowana':
        '캡슐 봉인 완료',
    '„{name}” otworzy się najwcześniej {when}.\n\nKod odzyskiwania (skopiowany do schowka, zapisany też obok kapsuły):\n\n{code}\n\nZapisz go w bezpiecznym miejscu. Przed datą otwarcia sam niczego nie otwiera; po niej zastępuje jeden z kluczy, gdyby był niedostępny.':
        '‘{name}’ 캡슐은 빨라도 {when}에 열립니다.\n\n복구 코드(클립보드에 복사했으며 캡슐 옆에도 저장했습니다):\n\n{code}\n\n안전한 곳에 보관하세요. 열리는 날짜 전에는 이 코드만으로 아무것도 열 수 없으며, 그 후에는 키 중 하나를 쓸 수 없을 때 그 키를 대신합니다.',
    'Nie udało się zapieczętować: {error}':
        '봉인하지 못했습니다: {error}',
    'Nowa kapsuła czasu':
        '새 타임캡슐',
    'Otworzy się najwcześniej':
        '가장 빨리 열리는 시각',
    'kapsuła':
        '캡슐',
    'Chwila otwarcia musi być w przyszłości.':
        '열리는 시각은 미래여야 합니다.',
    'Na bieżąco':
        '실시간',
    'Zmiany w folderach źródłowych trafiają do dzisiejszej wersji kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje. Jedna wersja na dzień; ze znacznikami czasu zamyka ją pieczęć następnego dnia.':
        '원본 폴더의 변경 사항은 저장하고 몇 분 뒤 오늘의 백업 버전에 반영되며, 드라이브를 연결하면 백업이 바로 동기화됩니다. 하루에 한 버전이며, 타임스탬프를 사용하면 다음 날 봉인으로 그 버전을 마감합니다.',
    'Na bieżąco — po każdej zmianie i po podłączeniu dysku':
        '실시간 — 변경될 때마다, 그리고 드라이브를 연결할 때',
    'Dla dysku podłączonego na stałe albo często: zmiany trafiają do kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje.':
        '항상 또는 자주 연결해 두는 드라이브용: 변경 사항은 저장하고 몇 분 뒤 백업에 반영되며, 드라이브를 연결하면 백업이 바로 동기화됩니다.',
    'Kopia będzie na bieżąco: zmiany trafią do dzisiejszej wersji kilka minut po zapisie, a po podłączeniu dysku kopia od razu się zsynchronizuje.':
        '백업이 실시간으로 유지됩니다: 변경 사항은 저장하고 몇 분 뒤 오늘의 버전에 반영되며, 드라이브를 연결하면 백업이 바로 동기화됩니다.',
    'przywracanie':
        '복원',
}
