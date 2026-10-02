"""Katalog chiński uproszczony: „polski tekst źródłowy” → „tekst (chiński (uproszczony))”.

Klucze są te same co w ``en.py`` i muszą dokładnie odpowiadać napisom w kodzie;
pilnuje tego ``tests/test_i18n.py``. Pola w nawiasach klamrowych (``{count}``)
zostają bez zmian. Formaty dat są te same co w Sigelith Desktop.
"""

from __future__ import annotations

TEXTS: dict[str, str] = {
    '\n\nLokalizacja:\n{path}':
        '\n\n位置：\n{path}',
    '\nDo uzupełnienia: niedokończone kopie: {count} — możesz je uzupełnić, wybierając wersję poniżej.':
        '\n待补全：有 {count} 个未完成的备份——在下方选择对应版本即可将其补全。',
    '\nUwaga: duży klaster ({size}): każdy mały plik zajmuje co najmniej tyle miejsca. Przy wielu małych plikach kopia zajmie wielokrotnie więcej niż dane.':
        '\n注意：簇较大（{size}），每个小文件至少占用这么多空间。小文件很多时，备份占用的空间会是数据本身的数倍。',
    '\nUwaga: niedokończone wersje (nie zawierają wszystkich plików): {names}':
        '\n注意：以下版本未完成（未包含全部文件）：{names}',
    '\nUwaga: {filesystem} nie obsługuje twardych dowiązań — każda wersja z datą zajmuje tyle miejsca co pełna kopia.':
        '\n注意：{filesystem} 不支持硬链接——每个带日期的版本都会占用与完整备份相同的空间。',
    ' wersji':
        ' 个版本',
    ' z szyfrowaniem AES-256-GCM…':
        ' — 使用 AES-256-GCM 加密…',
    ' ×':
        ' 次',
    ' — a ponieważ {filesystem} nie obsługuje twardych dowiązań, zapisze ponownie wszystkie pliki i zajmie tyle miejsca co cała kopia':
        ' ——而且由于 {filesystem} 不支持硬链接，它会重新写入所有文件，占用与整个备份相同的空间',
    ' • pozostało {time}':
        ' • 剩余 {time}',
    '%d.%m %H:%M':
        '%m/%d %H:%M',
    '%d.%m.%Y':
        '%Y/%m/%d',
    '%d.%m.%Y %H:%M':
        '%Y/%m/%d %H:%M',
    ', klaster {size}':
        '，簇大小 {size}',
    ', uzupełniona {when}':
        '，补全于 {when}',
    'Analizuje pliki i pokazuje plan. Nic nie zapisuje.':
        '分析文件并显示计划。不写入任何内容。',
    'Anulowano przed rozpoczęciem kopii.':
        '已在备份开始前取消。',
    'Anuluj':
        '取消',
    'Argon2id (t={passes}, {memory} MiB, p={threads})':
        'Argon2id (t={passes}, {memory} MiB, p={threads})',
    'Argon2id — {passes} przebiegi, {memory} MiB, {threads} wątki':
        'Argon2id — {passes} 次迭代，{memory} MiB，{threads} 个线程',
    'Automatycznie (język systemu)':
        '自动（系统语言）',
    'Bardzo dobre':
        '很强',
    'Bardzo słabe':
        '很弱',
    'Brak manifestu — skanuję katalog kopii.':
        '没有内容清单——正在扫描备份文件夹。',
    'Brakuje tagu uwierzytelniającego — plik jest obcięty.':
        '缺少认证标签——文件已被截断。',
    'Błąd uruchamiania':
        '启动错误',
    'Ciemny':
        '深色',
    'Co dokładnie zostanie zapisane przy najbliższym przebiegu.':
        '下次运行时将会写入的确切内容。',
    'Co kopiujemy':
        '备份什么',
    'Co zrobić, gdy plik o tej nazwie już istnieje w katalogu docelowym.':
        '目标文件夹中已存在同名文件时如何处理。',
    'Czas w nazwie to BeatTime — 1000 beatów na dobę, kotwica w UTC, ten sam moment na całym świecie. Data jest datą UTC, więc zgadza się z zegarem.':
        '名称中的时间是 BeatTime——每天 1000 个 beat，以 UTC 为基准，全世界都是同一时刻。日期是 UTC 日期，因此与该时钟一致。',
    'Czym jest {app}':
        '{app} 是什么',
    'Czyści tylko okno — plik dziennika pozostaje':
        '只清空窗口——日志文件会保留',
    'Dane aplikacji: {path}':
        '应用数据：{path}',
    'Decyduje, czy zachowujemy historię wersji.':
        '决定是否保留版本历史。',
    'Dobre':
        '强',
    'Dodaj folder':
        '添加文件夹',
    'Dodaj przynajmniej jeden folder źródłowy.':
        '请至少添加一个源文件夹。',
    'Dogrywka zmian z czasu kopii:':
        '补录备份期间的更改：',
    'Dokąd przywracamy':
        '恢复到哪里',
    'Dokładnie to, co program realnie stosuje.':
        '程序实际使用的确切配置。',
    'Domyślne wykluczenia':
        '默认排除项',
    'Domyślne wykluczenia zapisane.':
        '默认排除项已保存。',
    'Domyślnie wyłączone. Przy włączonej opcji skasowanie pliku w źródle\nusuwa też jego jedyną kopię zapasową — operacja nieodwracalna.':
        '默认关闭。开启后，在源中删除文件\n也会删除它唯一的备份——此操作不可撤销。',
    'Dopisuj do nazwy katalogu datę ostatniego uzupełnienia':
        '在文件夹名称后附加最后一次补全的日期',
    'Dziennik':
        '日志',
    'Dziennik: {path}':
        '日志：{path}',
    'Ekran przywracania wypełniony danymi szablonu.':
        '已用模板数据填写恢复页面。',
    'Folder docelowy kopii — najlepiej na innym dysku fizycznym.':
        '备份的目标文件夹——最好位于另一块物理硬盘上。',
    'Folder zawierający kopię utworzoną przez {app}.':
        '包含由 {app} 创建的备份的文件夹。',
    'Gdy plik już istnieje:':
        '文件已存在时：',
    'Gdzie zapisujemy':
        '保存到哪里',
    'Gotowe do pracy.':
        '就绪。',
    'Gotowe. Wybierz foldery do kopii.':
        '就绪。请选择要备份的文件夹。',
    'Gotowe: {count} {files}, {size}, {seconds} s.':
        '完成：{count} {files}，{size}，{seconds} 秒。',
    'Główny folder kopii. Zawiera spis treści (.cleanvault-manifest).':
        '备份主文件夹，其中包含内容清单（.cleanvault-manifest）。',
    'Hasła nie da się odzyskać ani zresetować. Jeśli je zgubisz, dane z kopii zaszyfrowanej są bezpowrotnie stracone — tak działa poprawne szyfrowanie.':
        '密码无法找回，也无法重置。如果丢失密码，加密备份中的数据将永久丢失——正确的加密就是这样工作的。',
    'Hasła w obu polach różnią się.':
        '两次输入的密码不一致。',
    'Hasło':
        '密码',
    'Hasło do kopii':
        '备份密码',
    'Hasło nie jest nigdzie zapisywane w postaci jawnej.\nBez niego nie da się odzyskać danych — nie istnieje żadna furtka serwisowa.':
        '密码不会以明文形式保存在任何地方。\n没有密码就无法恢复数据——不存在任何后门。',
    'Hasło nie może być puste.':
        '密码不能为空。',
    'Hasło niezapisane':
        '密码未保存',
    'Hasło powinno mieć co najmniej 8 znaków.':
        '密码应至少包含 8 个字符。',
    'Hasło trafia do magazynu systemowego powiązanego z Twoim kontem.\nNigdy nie jest zapisywane w plikach programu.':
        '密码会存入与你的账户绑定的系统存储。\n它永远不会写入程序自己的文件。',
    'Hasło użyte przy tworzeniu kopii':
        '创建备份时使用的密码',
    'Ile plików kopia przetwarza jednocześnie. Przy setkach tysięcy małych plików\nczas kopii to głównie opóźnienia na każdy plik (otwarcie, skanowanie\nantywirusowe, zapis na nośnik), a nie przesył danych — praca równoległa\nskraca go kilkukrotnie.\n\n„automatycznie” dobiera liczbę do procesora (do 32). Na wolnym dysku\ntalerzowym mniejsza wartość (2–4) bywa szybsza.':
        '备份同时处理的文件数。面对数十万个小文件时，\n备份时间主要耗在每个文件的延迟上（打开、杀毒\n扫描、写入存储介质），而不是数据传输——并行处理\n可将其缩短数倍。\n\n“自动”会根据处理器选择数量（最多 32）。在较慢的\n机械硬盘上，较小的值（2–4）往往更快。',
    'Informacje przydatne przy zgłaszaniu problemu.':
        '报告问题时有用的信息。',
    'Jak to działa':
        '工作原理',
    'Jasny':
        '浅色',
    'Jeden folder utrzymywany w zgodzie ze źródłem. Brak historii wersji,\nza to najprostsza struktura i najmniejsze zużycie miejsca.':
        '单个文件夹，始终与源保持一致。没有版本历史，\n但结构最简单，占用空间最少。',
    'Jeśli operacja zakończy się błędem, skopiuj stąd ostatnie wiersze — zawierają dokładną przyczynę, a nie tylko komunikat ogólny.':
        '如果操作以错误结束，请从这里复制最后几行——其中包含确切原因，而不只是笼统的提示。',
    'Język interfejsu zmieniony.':
        '界面语言已更改。',
    'Język zmienisz po zakończeniu bieżącej operacji.':
        '当前操作完成后才能更改语言。',
    'Język:':
        '语言：',
    'Katalog docelowy leży wewnątrz źródła ({path}). Kopia kopiowałaby samą siebie w nieskończoność.':
        '目标文件夹位于源文件夹内（{path}）。备份会无休止地复制自身。',
    'Katalog docelowy nie może być tym samym katalogiem co źródłowy.':
        '目标文件夹不能与源文件夹相同。',
    'Katalog jeszcze nie istnieje — zostanie utworzony.':
        '文件夹尚不存在——将自动创建。',
    'Katalog kopii nie istnieje: {path}':
        '备份文件夹不存在：{path}',
    'Katalog źródłowy nie istnieje: {path}':
        '源文件夹不存在：{path}',
    'Katalog, w którym pojawią się odtworzone pliki.':
        '恢复的文件将出现在此文件夹中。',
    'Katalog, w którym powstanie kopia. Nie może leżeć wewnątrz folderu źródłowego.':
        '将在其中创建备份的文件夹。它不能位于源文件夹内。',
    'Katalogi objęte kopią.\nMożesz przeciągnąć foldery z Eksploratora Windows wprost na tę listę.':
        '要备份的文件夹。\n你可以把文件夹从 Windows 文件资源管理器直接拖到此列表中。',
    'Każdy folder z datą jest kompletny — przywracanie nie wymaga sklejania wersji.':
        '每个带日期的文件夹都是完整的——恢复时无需拼合多个版本。',
    'Każdy plik jest czytany ponownie zaraz po zapisaniu. Dane pochodzą wtedy\nzwykle z pamięci podręcznej systemu, więc niewiele mówi to o nośniku,\na wydłuża kopię nawet dwukrotnie.\n\nSkuteczniejsza jest weryfikacja odroczona: ekran „Przywracanie” →\n„Sprawdź kopię”, najlepiej po ponownym podłączeniu dysku.':
        '每个文件写入后都会立即重新读取。此时数据通常\n来自系统缓存，因此说明不了存储介质的状况，\n却可能让备份时间延长一倍。\n\n延后校验更有效：“恢复”页面 →\n“检查备份”，最好在重新连接驱动器之后进行。',
    'Każdy plik trafia do kopii jako zaszyfrowany kontener .cvlt.\nKlucz powstaje z hasła przez Argon2id.':
        '每个文件都以加密的 .cvlt 容器形式存入备份。\n密钥由 Argon2id 从密码派生。',
    'Każdy przebieg tworzy osobny folder z datą i godziną.\nPliki niezmienione są podpinane twardym dowiązaniem, więc historia\nzajmuje tyle miejsca, ile realnie się zmieniło.':
        '每次运行都会创建一个带日期和时间的独立文件夹。\n未更改的文件通过硬链接引用，因此历史记录\n只占用实际发生变化的那部分空间。',
    'Klaster nośnika to {cluster} — pliki zajmą {actual} zamiast {logical} (narzut {overhead}).':
        '存储介质的簇大小为 {cluster}——文件将占用 {actual}，而不是 {logical}（额外开销 {overhead}）。',
    'Kliknij szablon, aby zobaczyć jego szczegóły.':
        '点击模板以查看其详细信息。',
    'Kliknij „Podgląd zmian”, aby sprawdzić plan bez zapisywania czegokolwiek.':
        '点击“预览更改”，即可在不写入任何内容的情况下检查计划。',
    'Kolor wyróżnienia':
        '强调色',
    'Kolor wyróżnienia…':
        '强调色…',
    'Kopia':
        '备份',
    'Kopia do dokończenia':
        '待完成的备份',
    'Kopia jest aktualna — nie ma czego zapisywać.':
        '备份已是最新——无需写入任何内容。',
    'Kopia jest zaszyfrowana — podaj hasło użyte przy jej tworzeniu.':
        '备份已加密——请输入创建备份时使用的密码。',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją przywrócić.':
        '备份已加密——请输入密码以进行恢复。',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją zweryfikować.':
        '备份已加密——请输入密码以进行校验。',
    'Kopia jest zaszyfrowana — podaj hasło.':
        '备份已加密——请输入密码。',
    'Kopia lustrzana':
        '镜像副本',
    'Kopia nie została uruchomiona.':
        '备份未启动。',
    'Kopia wykonana. Uruchom podgląd ponownie, aby sprawdzić stan.':
        '备份已完成。再次运行预览即可检查状态。',
    'Kopia zapasowa':
        '备份',
    'Kopia {folder}':
        '{folder} 的备份',
    'Kopia {kind} • {count} {files} • {size} • ostatnia aktualizacja {when}\nŹródła: {roots}':
        '{kind}备份 • {count} {files} • {size} • 最后更新于 {when}\n来源：{roots}',
    'Kopiowane są wyłącznie pliki nowe i zmienione od ostatniego przebiegu.':
        '只复制自上次运行以来新增和更改的文件。',
    'Kopiuje ustawienia szablonu na ekran „Kopia zapasowa”':
        '将模板设置复制到“备份”页面',
    'Kopię możesz sprawdzić później: ekran „Przywracanie” → „Sprawdź kopię”. Najlepiej po ponownym podłączeniu dysku — wtedy dane są czytane z nośnika.':
        '你可以稍后检查备份：“恢复”页面 → “检查备份”。最好在重新连接驱动器之后进行——这样数据才真正从存储介质读取。',
    'Kryptografia':
        '加密技术',
    'Lista podpowiadana przy tworzeniu nowej kopii.':
        '新建备份时建议使用的列表。',
    'Magazyn haseł: {backend}':
        '密码存储：{backend}',
    'Magazyn systemowy: {backend}':
        '系统存储：{backend}',
    'Menedżer poświadczeń Windows (DPAPI, powiązany z kontem użytkownika).':
        'Windows 凭据管理器（DPAPI，与用户账户绑定）。',
    'Miejsce i układ odtwarzanych plików.':
        '恢复文件的位置和布局。',
    'Motyw zmieniony na {theme}.':
        '主题已更改为{theme}。',
    'Motyw:':
        '主题：',
    'Możesz też przeciągnąć foldery z Eksploratora Windows wprost na listę.':
        '也可以把文件夹从 Windows 文件资源管理器直接拖到列表中。',
    'Można ją dokończyć — zostaną dograne tylko brakujące i zmienione pliki.':
        '可以将其完成——只会补写缺失和已更改的文件。',
    'Na nośniku docelowym zajmie to ok. {size}.':
        '这将在目标存储介质上占用约 {size}。',
    'Nadpisywanie plików':
        '覆盖文件',
    'Nadpisz istniejące pliki':
        '覆盖已有文件',
    'Nazwa szablonu':
        '模板名称',
    'Nazwa szablonu nie może być pusta.':
        '模板名称不能为空。',
    'Nazwa szablonu zapisana.':
        '模板名称已保存。',
    'Nazwa szablonu:':
        '模板名称：',
    'Nie ma wersji kopii o nazwie {name} w katalogu {path}.':
        '文件夹 {path} 中没有名为 {name} 的备份版本。',
    'Nie można odczytać informacji o dysku: {error}':
        '无法读取驱动器信息：{error}',
    'Nie udało się uruchomić programu — brakuje biblioteki: {error}\nZainstaluj zależności poleceniem:  pip install -r requirements.txt':
        '程序无法启动——缺少库：{error}\n请使用以下命令安装依赖项：  pip install -r requirements.txt',
    'Nie udało się wykonać operacji':
        '无法完成操作',
    'Nie udało się zapisać hasła w magazynie systemowym.\nSzablon działa normalnie — program poprosi o hasło przy uruchomieniu.':
        '无法将密码保存到系统存储。\n模板仍可正常使用——运行时程序会要求输入密码。',
    'Nie udało się znaleźć wolnej nazwy dla {path}':
        '无法为 {path} 找到可用的名称',
    'Nie wskazano katalogu docelowego.':
        '未指定目标文件夹。',
    'Nie wskazano żadnego katalogu źródłowego.':
        '未指定任何源文件夹。',
    'Nie wybrano katalogu':
        '未选择文件夹',
    'Nie wybrano szablonu':
        '未选择模板',
    'Nie znaleziono spisu treści kopii — program przeskanuje folder i rozpozna pliki po ich zawartości.':
        '未找到备份的内容清单——程序将扫描该文件夹，并根据内容识别文件。',
    'Nie znam oryginalnej lokalizacji dla {key} — wybierz inny układ przywracania.':
        '{key} 的原始位置未知——请选择其他恢复布局。',
    'Niedostępny — backend {backend} nie gwarantuje poufności.':
        '不可用——后端 {backend} 无法保证机密性。',
    'Niedostępny — brak biblioteki keyring.':
        '不可用——缺少 keyring 库。',
    'Nieznany algorytm wyprowadzania klucza: {name}':
        '未知的密钥派生算法：{name}',
    'Nowa wersja z datą':
        '新建带日期的版本',
    'Nowa wersja z datą to kopia od początku do osobnego folderu':
        '新建带日期的版本意味着从头复制到一个单独的文件夹',
    'Nowa wersja z datą — kopia do nowego folderu.\nWybrana istniejąca wersja — dogrywa do niej tylko brakujące i zmienione\npliki, a pliki różniące się od źródła nadpisuje. Tak dokończysz przerwaną\nkopię albo uzupełnisz ją o dane, które powstały w trakcie jej wykonywania.':
        '新建带日期的版本——备份到一个新文件夹。\n选择已有版本——只向其中补写缺失和已更改的文件，\n并覆盖与源不同的文件。这样即可完成中断的备份，\n或补入备份进行期间产生的数据。',
    'Nowy szablon':
        '新模板',
    'Nośnik docelowy ({filesystem}) nie obsługuje twardych dowiązań, więc każda wersja z datą jest pełną kopią. Te {count} niezmienionych plików zostanie powielone ({size}). Rozważ układ „kopia lustrzana” albo nośnik NTFS.':
        '目标存储介质（{filesystem}）不支持硬链接，因此每个带日期的版本都是完整备份。这 {count} 个未更改的文件将被重复存储（{size}）。可考虑使用“镜像副本”布局或 NTFS 存储介质。',
    'O programie':
        '关于',
    'Obsługiwane są wzorce w stylu Windows:\n  *.tmp          — wszystkie pliki tymczasowe\n  Thumbs.db      — konkretna nazwa\n  node_modules/* — cały folder wraz z zawartością':
        '支持 Windows 风格的通配模式：\n  *.tmp          — 所有临时文件\n  Thumbs.db      — 某个具体名称\n  node_modules/* — 整个文件夹及其内容',
    'Ochrona danych':
        '数据保护',
    'Odczytuje wszystkie pliki kopii i weryfikuje ich poprawność.\nNic nie zapisuje na dysku.':
        '读取备份中的所有文件并校验其完整性。\n不会向磁盘写入任何内容。',
    'Odpowiednik synchronizacji folderu. Wcześniejsze wersje plików nie są zachowywane.':
        '相当于同步文件夹。不保留文件的早期版本。',
    'Odtwarza pliki z kopii — również z kopii zaszyfrowanej.':
        '从备份中恢复文件——包括加密备份。',
    'Odtwarza pliki zgodnie z ustawieniami powyżej':
        '按上方设置恢复文件',
    'Odtwórz pełną strukturę folderów':
        '重建完整的文件夹结构',
    'Odtwórz pliki z istniejącej kopii':
        '从现有备份中恢复文件',
    'Operacja nie powiodła się.':
        '操作失败。',
    'Operacja przerwana przez użytkownika.':
        '操作已被用户取消。',
    'Operacja przerwana — utrwalam stan dotychczas zapisanych plików.':
        '操作已中断——正在保存已写入文件的状态。',
    'Operacja w toku':
        '操作进行中',
    'Operacja zakończona błędem.':
        '操作以错误结束。',
    'Ostatnie operacje':
        '最近的操作',
    'Otwiera ekran przywracania z wypełnionymi ścieżkami':
        '打开恢复页面并填好路径',
    'Otwiera pełny dziennik w domyślnym edytorze':
        '在默认编辑器中打开完整日志',
    'Otwórz katalog danych':
        '打开数据文件夹',
    'Otwórz katalog dziennika':
        '打开日志文件夹',
    'Otwórz okno wyboru katalogu':
        '打开文件夹选择窗口',
    'Otwórz plik dziennika':
        '打开日志文件',
    'PBKDF2-HMAC-SHA256 ({count} iteracji)':
        'PBKDF2-HMAC-SHA256（{count} 次迭代）',
    'PBKDF2-HMAC-SHA256 — {count} iteracji':
        'PBKDF2-HMAC-SHA256 — {count} 次迭代',
    'PBKDF2-HMAC-SHA256, {count} iteracji':
        'PBKDF2-HMAC-SHA256，{count} 次迭代',
    'Pełna struktura — układ jak w źródle, wewnątrz wskazanego katalogu.\nJeden folder — wygodne, gdy szukasz kilku plików.\nPierwotne lokalizacje — zapisuje pliki tam, skąd zostały pobrane.':
        '完整结构——在所选文件夹内按源的布局存放。\n单个文件夹——只需找回几个文件时很方便。\n原始位置——把文件写回它们原来的位置。',
    'Pierwszy przebieg kopiuje wszystko i trwa najdłużej. Kolejne porównują rozmiar i datę modyfikacji, więc zwykle kończą się w kilka sekund.':
        '第一次运行会复制所有内容，耗时最长。之后的运行会比较大小和修改日期，因此通常几秒钟即可完成。',
    'Plan gotowy: {count} {files} do zapisania.':
        '计划已就绪：需写入 {count} {files}。',
    'Plik jest za krótki, by być kontenerem tego programu.':
        '文件太短，不可能是本程序的容器。',
    'Plik skończył się wcześniej, niż deklaruje nagłówek.':
        '文件提前结束，比文件头声明的长度短。',
    'Plik w formacie w wersji {found}; ta wersja programu obsługuje {supported}.':
        '文件格式版本为 {found}；此版本的程序支持 {supported}。',
    'Plik wymaga Argon2id, a biblioteka argon2-cffi jest niedostępna.':
        '该文件需要 Argon2id，但 argon2-cffi 库不可用。',
    'Pliki pominięte — kopia jest aktualna':
        '将跳过的文件——备份中已是最新',
    'Pliki trafią do wskazanego katalogu z zachowaniem struktury folderów.':
        '文件将存入所选文件夹，并保留文件夹结构。',
    'Pliki wrócą dokładnie tam, skąd pochodzą. Katalog docelowy zostanie zignorowany.':
        '文件将准确回到原来的位置。目标文件夹将被忽略。',
    'Pliki zmienione od ostatniego przebiegu':
        '自上次运行以来更改的文件',
    'Pliki zostaną zapisane dokładnie tam, skąd pochodzą.\n\nKonflikty nazw: {collision}.\n\nCzy kontynuować?':
        '文件将准确写回它们原来的位置。\n\n名称冲突：{collision}。\n\n是否继续？',
    'Pliki, których jeszcze nie ma w kopii':
        '备份中尚没有的文件',
    'Po uzupełnieniu istniejącej wersji jej katalog nazywa się np.\n  2026-09-17_@687--2026-09-24_@921\nczyli: data utworzenia kopii i data ostatniego uzupełnienia.\n\nData utworzenia zostaje z przodu, więc katalogi nadal układają się\nchronologicznie. Widać to w Eksploratorze bez uruchamiania programu.':
        '补全现有版本后，其文件夹名称例如：\n  2026-09-17_@687--2026-09-24_@921\n即：备份的创建日期和最后一次补全的日期。\n\n创建日期保持在前面，因此文件夹仍按时间\n顺序排列。无需启动程序，在文件资源管理器中就能看到。',
    'Po wykonaniu kopii zostanie mało wolnego miejsca ({free}).':
        '备份完成后剩余的可用空间将很少（{free}）。',
    'Po zakończeniu kopii program ponownie skanuje źródło i dogrywa do tej samej\nwersji pliki, które w międzyczasie powstały lub się zmieniły.\nPrzydatne, gdy pracujesz na danych w trakcie wielogodzinnej kopii.\nPlik zmieniony w trakcie własnego kopiowania nigdy nie jest uznawany za zapisany.':
        '备份完成后，程序会再次扫描源，并把期间新增或更改的文件\n补写到同一版本中。\n适用于在长达数小时的备份过程中仍在处理数据的情况。\n在复制过程中发生更改的文件，永远不会被视为已写入。',
    'Poczekaj na zakończenie bieżącej operacji.':
        '请等待当前操作完成。',
    'Podaj hasło dla szablonu „{name}”:':
        '请输入模板“{name}”的密码：',
    'Podaj hasło — bez niego nie można zaszyfrować kopii.':
        '请输入密码——没有密码就无法加密备份。',
    'Podane hasło nie pasuje do plików zapisanych wcześniej w tej kopii. Wznowienie z innym hasłem zostawiłoby w jednej kopii pliki pod dwoma hasłami. Podaj hasło użyte przy poprzednim przebiegu albo utwórz kopię w nowym katalogu.':
        '输入的密码与此备份中先前写入的文件不匹配。用另一个密码继续，会使同一个备份中的文件使用两个不同的密码。请输入上次运行时使用的密码，或在新文件夹中创建备份。',
    'Podgląd zmian':
        '预览更改',
    'Pokazuje folder z plikami dziennika':
        '显示存放日志文件的文件夹',
    'Pokazuje folder z ustawieniami i szablonami':
        '显示存放设置和模板的文件夹',
    'Pokaż / ukryj wpisane hasło':
        '显示/隐藏输入的密码',
    'Pomiń istniejące pliki':
        '跳过已有文件',
    'Potwierdź usuwanie':
        '确认删除',
    'Powtórz hasło':
        '再次输入密码',
    'Program nie mógł się uruchomić:\n\n{error}\n\nSzczegóły zapisano w dzienniku aplikacji.':
        '程序无法启动：\n\n{error}\n\n详细信息已写入应用日志。',
    'Program nie wie, czy ta kopia została dokończona. Uzupełnienie jej dogra tylko brakujące i zmienione pliki, a tego, co już jest zapisane, nie kopiuje ponownie.':
        '程序无法确定此备份是否已完成。补全它只会补写缺失和已更改的文件，不会重新复制已写入的内容。',
    'Program sam wykryje, czy kopia jest zaszyfrowana.':
        '程序会自动检测备份是否已加密。',
    'Przebieg operacji i diagnostyka':
        '操作进度与诊断',
    'Przebieg operacji na żywo. Pełna historia trafia do pliku.':
        '操作的实时进度。完整记录会写入文件。',
    'Przebieg uzupełniający: {error}':
        '补录轮次：{error}',
    'Przeciętne':
        '一般',
    'Przerwano liczenie sumy kontrolnej.':
        '已取消校验和计算。',
    'Przerwano skanowanie.':
        '已取消扫描。',
    'Przerwano. Zapisano {count} {files} ({size}).':
        '已中断。已写入 {count} {files}（{size}）。',
    'Przerwij':
        '停止',
    'Przerywanie operacji…':
        '正在停止操作…',
    'Przerywanie — zapisuję spis treści kopii, nie wyłączaj komputera…':
        '正在停止——正在写入备份的内容清单，请勿关闭计算机…',
    'Przeskanowano {count} {files}.':
        '已扫描 {count} {files}。',
    'Przygotowanie…':
        '正在准备…',
    'Przywracanie':
        '恢复',
    'Przywracanie do pierwotnych lokalizacji':
        '恢复到原始位置',
    'Przywracanie przerwane.':
        '恢复已取消。',
    'Przywracanie {count} {files} ({size})…':
        '正在恢复 {count} {files}（{size}）…',
    'Przywróć do pierwotnych lokalizacji':
        '恢复到原始位置',
    'Przywróć domyślne':
        '恢复默认值',
    'Przywróć fabryczne':
        '恢复出厂列表',
    'Przywróć pliki':
        '恢复文件',
    'Przywróć z tej kopii':
        '从此备份恢复',
    'Pusta nazwa':
        '名称为空',
    'Równoległe operacje:':
        '并行操作数：',
    'Skanowanie plików źródłowych…':
        '正在扫描源文件…',
    'Skrót z dziennika — pełny zapis znajdziesz w zakładce „Dziennik”.':
        '日志摘要——完整记录见“日志”页面。',
    'Skąd przywracamy':
        '从哪里恢复',
    'Sprawdzam, co zmieniło się w źródle w trakcie kopii (przebieg uzupełniający {attempt} z {passes})…':
        '正在检查备份期间源中发生了哪些变化（补录轮次 {attempt}/{passes}）…',
    'Sprawdzam, czy hasło zgadza się z hasłem wcześniej zapisanych plików…':
        '正在检查密码是否与先前写入的文件的密码一致…',
    'Sprawdzam, czy w katalogu docelowym jest kopia do dokończenia…':
        '正在检查目标文件夹中是否有待完成的备份…',
    'Sprawdź hasło':
        '检查密码',
    'Sprawdź kopię':
        '检查备份',
    'Szablon przechowuje foldery, opcje i wykluczenia. Hasło nigdy nie trafia do szablonu — jest przechowywane w Menedżerze poświadczeń Windows albo wpisywane przy każdym uruchomieniu.':
        '模板保存文件夹、选项和排除项。密码永远不会存入模板——它保存在 Windows 凭据管理器中，或在每次运行时输入。',
    'Szablon usunięty.':
        '模板已删除。',
    'Szablon „{name}”':
        '模板“{name}”',
    'Szablon „{name}” już istnieje.\n\nZastąpić go bieżącymi ustawieniami z formularza?':
        '模板“{name}”已存在。\n\n要用表单中的当前设置替换它吗？',
    'Szablon „{name}” zostanie usunięty.\n\nPliki kopii zapasowej pozostaną nienaruszone.':
        '模板“{name}”将被删除。\n\n备份文件不受影响。',
    'Szablony':
        '模板',
    'Szablony: {count}\nSzyfrowanie: AES-256-GCM\nKlucz: {kdf}':
        '模板：{count}\n加密：AES-256-GCM\n密钥：{kdf}',
    'Szyfrowanie i kontrola poprawności zapisu.':
        '加密与写入校验。',
    'Szyfrowanie: AES-256-GCM (uwierzytelnione)\nWyprowadzanie klucza: {kdf}':
        '加密：AES-256-GCM（认证加密）\n密钥派生：{kdf}',
    'Szyfruj kopię (AES-256-GCM)':
        '加密备份（AES-256-GCM）',
    'Słabe':
        '弱',
    'Ta kopia nie jest zaszyfrowana — hasło nie jest potrzebne.':
        '此备份未加密——无需密码。',
    'Ten folder jest już na liście.':
        '该文件夹已在列表中。',
    'To nie jest plik zaszyfrowany przez ten program.':
        '此文件不是由本程序加密的。',
    'Trwa inna operacja — poczekaj na jej zakończenie.':
        '另一个操作正在进行——请等待其完成。',
    'Trwa operacja':
        '正在执行操作',
    'Trwa operacja na plikach. Zamknięcie programu ją przerwie.\n\nPliki zapisane do tej chwili zostaną zachowane, a kopię będzie można później dokończyć.\n\nZamknąć mimo to?':
        '正在进行文件操作。关闭程序会中断该操作。\n\n到目前为止写入的文件会保留，之后可以继续完成备份。\n\n仍要关闭吗？',
    'Trwa: {description}…':
        '正在进行：{description}…',
    'Tryb dokładny — licz sumę kontrolną każdego pliku':
        '精确模式——计算每个文件的校验和',
    'Układ kopii':
        '备份布局',
    'Układ plików:':
        '文件布局：',
    'Uruchom kopię':
        '开始备份',
    'Ustawienia':
        '设置',
    'Usunąć szablon?':
        '删除模板？',
    'Usuwa pozycję z listy. Nie kasuje żadnych plików.':
        '从列表中移除该项。不会删除任何文件。',
    'Usuwa szablon. Nie kasuje żadnych plików kopii.':
        '删除模板。不会删除任何备份文件。',
    'Usuwaj z kopii pliki skasowane w źródle':
        '从备份中删除源中已删除的文件',
    'Usuń':
        '删除',
    'Usuń zaznaczone':
        '移除所选项',
    'Uszkodzony nagłówek pliku.':
        '文件头已损坏。',
    'Utwórz lub zaktualizuj kopię wybranych folderów':
        '创建或更新所选文件夹的备份',
    'Utwórz nową wersję':
        '创建新版本',
    'Uzupełnienie istniejącej wersji nie kopiuje ponownie tego, co już w niej jest — dokończysz przerwaną kopię bez tworzenia kolejnej pełnej wersji.':
        '补全现有版本不会重新复制其中已有的内容——无需再创建一个完整版本即可完成中断的备份。',
    'Uzupełnij tę wersję':
        '补全此版本',
    'Uzupełnij: {version} • {labels}':
        '补全：{version} • {labels}',
    'W katalogu docelowym jest kopia tych samych folderów zapisana starszą wersją programu:':
        '目标文件夹中有一份由旧版程序写入的、相同文件夹的备份：',
    'W katalogu docelowym jest niedokończona kopia tych samych folderów:':
        '目标文件夹中有一份相同文件夹的未完成备份：',
    'W tym katalogu nie ma spisu treści kopii — nie ma z czym porównać plików.':
        '此文件夹中没有备份的内容清单——无从比对文件。',
    'Wczytaj do formularza':
        '载入表单',
    'Wczytano manifest kopii: {count} {files}.':
        '已载入备份的内容清单：{count} {files}。',
    'Wczytano szablon „{name}” do formularza.':
        '已将模板“{name}”载入表单。',
    'Wersja kopii nosi teraz nazwę {name}.':
        '该备份版本现在的名称为 {name}。',
    'Wersja, licencja i użyta kryptografia':
        '版本、许可证和所用的加密技术',
    'Wersje z datą (zalecane)':
        '带日期的版本（推荐）',
    'Weryfikacja kopii':
        '备份校验',
    'Weryfikacja nie powiodła się: nieprawidłowe hasło lub uszkodzony plik.':
        '校验失败：密码错误或文件已损坏。',
    'Weryfikacja po zapisie nie powiodła się — zapisane dane różnią się od źródła.':
        '写入后校验失败——写入的数据与源不同。',
    'Weryfikacja {count} {files} ({size}), {threads} równolegle…':
        '正在校验 {count} {files}（{size}），{threads} 路并行…',
    'Weryfikuj natychmiast po zapisie (spowalnia kopię)':
        '写入后立即校验（会减慢备份速度）',
    'Wolne miejsce: {free} z {total}':
        '可用空间：{free}（共 {total}）',
    'Wolniejszy, ale wykrywa zmiany, które nie zmieniły rozmiaru ani daty\n(np. po przywróceniu pliku z innego nośnika).':
        '较慢，但能发现大小和日期都未改变的更改\n（例如从其他存储介质恢复文件之后）。',
    'Wpis {key} w spisie treści kopii wskazuje poza katalog docelowy — pomijam go.':
        '备份内容清单中的条目 {key} 指向目标文件夹之外——已跳过。',
    'Wraca do listy wbudowanej w program':
        '恢复为程序内置的列表',
    'Wskaż folder kopii, aby zobaczyć jej zawartość.':
        '请指定备份文件夹以查看其内容。',
    'Wskaż folder kopii.':
        '请指定备份文件夹。',
    'Wskaż foldery objęte kopią. Podfoldery są uwzględniane automatycznie.':
        '请选择要备份的文件夹。子文件夹会自动包含在内。',
    'Wskaż główny folder kopii (ten, który wybrałeś jako cel), a nie pojedynczy folder z datą. Program sam odczyta spis treści kopii.':
        '请指定备份主文件夹（即你选作目标的那个文件夹），而不是单个带日期的文件夹。程序会自行读取备份的内容清单。',
    'Wskaż katalog docelowy kopii.':
        '请指定备份的目标文件夹。',
    'Wskaż katalog docelowy.':
        '请指定目标文件夹。',
    'Wstawia zalecaną listę wykluczeń':
        '填入推荐的排除项列表',
    'Wszystkie pliki wylądują bezpośrednio w katalogu docelowym, bez podfolderów.':
        '所有文件都将直接放入目标文件夹，不含子文件夹。',
    'Wszystko do jednego folderu':
        '全部放入一个文件夹',
    'Wybierz folder do kopii':
        '选择要备份的文件夹',
    'Wybierz folder kopii':
        '选择备份文件夹',
    'Wybierz katalog':
        '选择文件夹',
    'Wybierz katalog docelowy':
        '选择目标文件夹',
    'Wybierz katalog docelowy kopii':
        '选择备份的目标文件夹',
    'Wybierz katalog, aby zobaczyć dostępne miejsce.':
        '选择文件夹以查看可用空间。',
    'Wybierz kolejny folder do kopii':
        '再选择一个要备份的文件夹',
    'Wybierz szablon z listy.':
        '请从列表中选择模板。',
    'Wybierz…':
        '选择…',
    'Wybrano nadpisywanie istniejących plików. Ich obecna zawartość zostanie bezpowrotnie zastąpiona.\n\nCzy kontynuować?':
        '你选择了覆盖已有文件。它们当前的内容将被永久替换。\n\n是否继续？',
    'Wyczyść widok':
        '清空视图',
    'Wygląd':
        '外观',
    'Wygląd, wykluczenia domyślne i informacje o środowisku.':
        '外观、默认排除项和环境信息。',
    'Wygląd, wykluczenia i magazyn haseł':
        '外观、排除项和密码存储',
    'Wykluczenia':
        '排除项',
    'Wykonuje kopię według tego szablonu':
        '按此模板执行备份',
    'Wykonuje kopię zgodnie z powyższymi ustawieniami':
        '按上方设置执行备份',
    'Wymagane wyłącznie dla kopii zaszyfrowanych.':
        '仅加密备份需要。',
    'Wzorce plików i folderów pomijanych w kopii — po jednym w wierszu.':
        '备份时要排除的文件和文件夹的模式——每行一个。',
    'Włączono szyfrowanie, ale nie podano hasła.':
        '已开启加密，但未提供密码。',
    'Włączono usuwanie z kopii plików skasowanych w źródle.\n\nPliki usunięte w źródle stracą swoją jedyną kopię zapasową. Czy na pewno kontynuować?':
        '已开启“从备份中删除源中已删除的文件”。\n\n在源中删除的文件将失去它们唯一的备份。确定要继续吗？',
    'Za mało miejsca w katalogu docelowym. Potrzeba ok. {needed}, dostępne {free}.':
        '目标文件夹空间不足。约需 {needed}，可用 {free}。',
    'Zabezpieczenie przed literówką — hasła nie da się odzyskać.':
        '防止输错——密码无法找回。',
    'Zachowaj oba — dopisz numer do nazwy':
        '保留两者——在名称后添加编号',
    'Zakończono z błędami ({errors}). Zapisano {count} {files}.':
        '已完成，但有错误（{errors}）。已写入 {count} {files}。',
    'Zakończono.':
        '已完成。',
    'Zapamiętaj hasło w Menedżerze poświadczeń Windows':
        '在 Windows 凭据管理器中记住密码',
    'Zapamiętuje te ustawienia do ponownego użycia':
        '记住这些设置以便再次使用',
    'Zapis bieżącej sesji':
        '本次会话的记录',
    'Zapisane konfiguracje do ponownego użycia':
        '可重复使用的已保存配置',
    'Zapisane konfiguracje — uruchamiasz je jednym kliknięciem.':
        '已保存的配置——点击一下即可运行。',
    'Zapisane szablony':
        '已保存的模板',
    'Zapisano szablon „{name}”.':
        '已保存模板“{name}”。',
    'Zapisuje listę jako domyślną':
        '将列表保存为默认值',
    'Zapisuje nową nazwę szablonu':
        '保存新的模板名称',
    'Zapisywanie {count} {files} ({size}), {workers} równolegle':
        '正在写入 {count} {files}（{size}），{workers} 路并行',
    'Zapisz':
        '保存',
    'Zapisz do:':
        '写入到：',
    'Zapisz jako szablon':
        '另存为模板',
    'Zapisz nazwę':
        '保存名称',
    'Zapisz szablon':
        '保存模板',
    'Zastąpić szablon?':
        '替换模板？',
    'Zatrzymuje operację. Pliki już zapisane pozostają nienaruszone.':
        '停止操作。已写入的文件保持不变。',
    'Zaznacz szablon na liście.':
        '请在列表中选择一个模板。',
    'Zmiana języka przebudowuje okno; wypełnione ścieżki zostają.':
        '更改语言会重建窗口；已填写的路径会保留。',
    'Zmiana motywu działa natychmiast.':
        '主题更改立即生效。',
    'Zmienia kolor przycisków i zaznaczeń':
        '更改按钮和选中项的颜色',
    'Zmień nazwę, aby łatwiej rozpoznawać szablon.':
        '重命名模板，使其更易于识别。',
    'Znaleziono {count} {files}. Porównuję z poprzednią kopią…':
        '找到 {count} {files}。正在与上一次备份比较…',
    'automatycznie':
        '自动',
    'bez zmian':
        '未更改',
    'brak (biblioteka keyring niezainstalowana)':
        '无（未安装 keyring 库）',
    'brak danych':
        '无数据',
    'brak pliku w kopii':
        '备份中缺少该文件',
    'do zapisania':
        '待写入',
    'istniejąca kopia: {count} {files}, ostatnio {when}':
        '已有备份：{count} {files}，最近一次 {when}',
    'jeszcze nie uruchamiany':
        '尚未运行过',
    'kompletna':
        '完整',
    'kopia lustrzana':
        '镜像副本',
    'kopia zapasowa':
        '备份',
    'nie':
        '否',
    'niedokończona':
        '未完成',
    'niedokończona — brakuje ok. {count} {files} ({size})':
        '未完成——约缺少 {count} {files}（{size}）',
    'niezaszyfrowana':
        '未加密',
    'nieznany format manifestu':
        '未知的内容清单格式',
    'nowych plików':
        '新文件',
    'np. C:\\Odzyskane':
        '例如 C:\\恢复的文件',
    'np. E:\\Kopie zapasowe':
        '例如 E:\\备份',
    'plik':
        '个文件',
    'plik stanu jest za krótki':
        '状态文件太短',
    'plik stanu w wersji {found}, obsługiwana: {supported}':
        '状态文件版本为 {found}，支持的版本：{supported}',
    'pliki':
        '个文件',
    'plików':
        '个文件',
    'podgląd kopii':
        '备份预览',
    'pozostaną w kopii':
        '将保留在备份中',
    'rozmiar w kopii {actual} B zamiast {expected} B':
        '备份中的大小为 {actual} B，而非 {expected} B',
    'sprawdzanie kopii':
        '检查备份',
    'stan nieznany (zapisana starszą wersją programu)':
        '状态未知（由旧版程序写入）',
    'suma kontrolna manifestu się nie zgadza':
        '内容清单的校验和不匹配',
    'suma kontrolna się nie zgadza — plik uszkodzony':
        '校验和不匹配——文件已损坏',
    'szablon {name}':
        '模板 {name}',
    'tak':
        '是',
    'ten system plików':
        '此文件系统',
    'wersja {version}':
        '版本 {version}',
    'wersje z datą':
        '带日期的版本',
    'weryfikacja':
        '校验',
    'wyłączona':
        '关闭',
    'zaszyfrowana (AES-256-GCM)':
        'AES-256-GCM 加密',
    'zawartość różni się od pliku źródłowego':
        '内容与源文件不同',
    'zawartość różni się od sumy kontrolnej zapisanej podczas kopii':
        '内容与备份时记录的校验和不符',
    'zmienionych':
        '已更改',
    'zostaną usunięte z kopii':
        '将从备份中删除',
    '{done} z {total} • {speed}/s{eta}':
        '{done} / {total} • {speed}/秒{eta}',
    '{done} • {speed}/s':
        '{done} • {speed}/秒',
    '{hours} h {minutes} min':
        '{hours} 小时 {minutes} 分钟',
    '{label}: {count} {files}':
        '{label}：{count} {files}',
    '{message}\n\nSzczegóły techniczne znajdziesz w zakładce „Dziennik”.':
        '{message}\n\n技术细节见“日志”页面。',
    '{minutes} min {seconds} s':
        '{minutes} 分 {seconds} 秒',
    '{name}: nie można odczytać ({error})':
        '{name}：无法读取（{error}）',
    '{seconds} s':
        '{seconds} 秒',
    '{summary}\n\nProblemy:\n{problems}\n\nPełna lista znajduje się w zakładce „Dziennik”.':
        '{summary}\n\n问题：\n{problems}\n\n完整列表见“日志”页面。',
    '{summary}{notes}\n\nPliki zapisane przed przerwaniem są kompletne i zostały odnotowane w spisie treści kopii.\n\nAby dokończyć kopię, uruchom ją ponownie — program zaproponuje uzupełnienie tej wersji zamiast tworzenia nowej.':
        '{summary}{notes}\n\n中断前写入的文件是完整的，并已记录在备份的内容清单中。\n\n要完成备份，请重新运行——程序会建议补全此版本，而不是新建一个版本。',
    '{title} — gotowe':
        '{title}——完成',
    '{title} — przerwano':
        '{title}——已中断',
    '{title} — zakończono z błędami':
        '{title}——完成，但有错误',
    '{when}  •  {action}  •  {count} {files}':
        '{when}  •  {action}  •  {count} {files}',
    'Łączny rozmiar danych do przesłania':
        '需要传输的数据总量',
    'Środowisko':
        '环境',
    'Źródła: {sources}\nCel: {destination}\nUkład: {structure} • Szyfrowanie: {encrypt} • Weryfikacja: {verify} • Dogrywka: {catchup} • Równolegle: {workers} • Data uzupełnienia w nazwie: {stamp}\nUtworzony: {created} • Ostatni przebieg: {last}':
        '来源：{sources}\n目标：{destination}\n布局：{structure} • 加密：{encrypt} • 校验：{verify} • 补录：{catchup} • 并行：{workers} • 名称中含补全日期：{stamp}\n创建于：{created} • 上次运行：{last}',
    'Źródło nie zmieniło się w trakcie kopii — nie ma czego uzupełniać.':
        '备份期间源没有变化——无需补录。',
    '—':
        '—',
    '• Kopia przyrostowa — zapisywane są wyłącznie pliki nowe i zmienione.\n  Porównanie opiera się na spisie treści kopii, rozmiarze i dacie modyfikacji;\n  przy różnicy liczona jest suma kontrolna SHA-256.\n\n• Wersje z datą — każdy przebieg tworzy kompletny folder z datą, a pliki\n  niezmienione są podpinane twardym dowiązaniem, więc nie zajmują miejsca dwa razy.\n\n• Weryfikacja po zapisie — zapisany plik jest odczytywany z powrotem\n  i porównywany ze źródłem.\n\n• Odporność na przerwania — pliki powstają pod nazwą tymczasową i są\n  podmieniane dopiero po pełnym zapisie.':
        '• 增量备份——只写入新增和更改的文件。\n  比较依据备份的内容清单、文件大小和修改日期；\n  若有差异，则计算 SHA-256 校验和。\n\n• 带日期的版本——每次运行都会创建一个完整的带日期文件夹，\n  未更改的文件通过硬链接引用，因此不会重复占用空间。\n\n• 写入后校验——写入的文件会被重新读取，\n  并与源进行比较。\n\n• 抗中断——文件先以临时名称创建，\n  完全写入后才替换为正式文件。',
    '• Szyfr: AES-256 w trybie GCM (szyfrowanie z uwierzytelnieniem).\n• Wyprowadzanie klucza z hasła: {kdf}.\n• Nagłówek każdego pliku jest uwierzytelniony jako AAD — podmiana parametrów\n  unieważnia tag.\n• Każdy plik dostaje losowy, niepowtarzalny nonce.\n• Odszyfrowany plik powstaje dopiero po pomyślnej weryfikacji tagu.\n• Hasła nie są zapisywane w plikach programu. Opcjonalnie trafiają do\n  Menedżera poświadczeń Windows.':
        '• 密码算法：GCM 模式的 AES-256（认证加密）。\n• 从密码派生密钥：{kdf}。\n• 每个文件的文件头都作为 AAD 参与认证——篡改参数\n  会使标签失效。\n• 每个文件都获得一个随机且唯一的 nonce。\n• 只有在标签校验成功后，才会生成解密后的文件。\n• 密码不会写入程序的文件。也可以选择存入\n  Windows 凭据管理器。',
    'Bez hasła nie da się odczytać ani jednego pliku z kopii.':
        '没有密码，备份中的任何一个文件都无法读取。',
    'Co chcesz chronić?':
        '你想保护什么？',
    'Co chcesz teraz zrobić?':
        '你现在想做什么？',
    'Czyta kopię z nośnika i porównuje ją z zapisanymi sumami kontrolnymi.':
        '从存储介质读取备份，并与记录的校验和进行比较。',
    'Dalej':
        '下一步',
    'Dokumenty i zdjęcia':
        '文档和照片',
    'Ekran powitalny wrócisz w ustawieniach, gdy zmienisz zdanie.':
        '如果改变主意，可以在设置中重新启用欢迎页面。',
    'Ekran z pytaniem, co chcesz teraz zrobić: kopia, przywracanie, sprawdzenie.':
        '询问你现在想做什么的页面：备份、恢复或检查。',
    'Foldery objęte kopią':
        '要备份的文件夹',
    'Foldery z pracą. Kreator pominie katalogi, które odtwarza się jednym poleceniem (node_modules, venv, build).':
        '存放工作成果的文件夹。向导会排除可用一条命令重新生成的文件夹（node_modules、venv、build）。',
    'Gdzie zapisać kopię?':
        '备份保存到哪里？',
    'Historia i szyfrowanie':
        '历史与加密',
    'Historia zmian (zalecane)':
        '更改历史（推荐）',
    'Jak bardzo chcesz się zabezpieczyć?':
        '你需要多大程度的保护？',
    'Jak wyżej, a dodatkowo każdy plik trafia do kopii zaszyfrowany (AES-256-GCM). Potrzebne przy kopii wożonej poza dom.':
        '同上，另外每个文件都会加密后存入备份（AES-256-GCM）。适合需要带出家门的备份。',
    'Jedna aktualna kopia':
        '一份最新副本',
    'Język, motyw, domyślne wykluczenia i informacje o środowisku.':
        '语言、主题、默认排除项和环境信息。',
    'Katalog docelowy leży wewnątrz źródła — wybierz inny.':
        '目标文件夹位于源文件夹内——请另选一个。',
    'Każdy przebieg tworzy folder z datą. Pliki niezmienione są podpinane dowiązaniem, więc historia kosztuje tyle, ile realnie się zmieniło.':
        '每次运行都会创建一个带日期的文件夹。未更改的文件通过链接引用，因此历史记录只占用实际变化的那部分空间。',
    'Każdy przebieg utworzy folder z datą. Pierwszy zajmie tyle, ile dane; kolejne — tyle, ile realnie się zmieniło.':
        '每次运行都会创建一个带日期的文件夹。第一次占用的空间与数据量相当；之后只占用实际变化的部分。',
    'Kopia powstanie w: {path}':
        '备份将创建在：{path}',
    'Kopia trafi do: {path}':
        '备份将保存到：{path}',
    'Kopia: {what}':
        '备份：{what}',
    'Krok {number} z {total}':
        '第 {number} 步，共 {total} 步',
    'Najlepiej na innym dysku fizycznym niż ten, który chronisz — kopia obok oryginału ginie razem z nim.':
        '最好放在另一块物理硬盘上，而不是你要保护的那块——与原件放在一起的备份会和原件一起丢失。',
    'Najszybsza i najmniejsza. Kopia odpowiada temu, co masz teraz — bez historii wcześniejszych wersji.':
        '最快、最省空间。备份与你现在的文件一致——不保留早期版本的历史。',
    'Nie było jeszcze żadnej kopii. Zacznij od „Zrób kopię”.':
        '还没有任何备份。请从“立即备份”开始。',
    'Nie lista ustawień, tylko ich skutki.':
        '不是设置列表，而是这些设置的效果。',
    'Nie pokazuj tego ekranu przy starcie':
        '启动时不再显示此页面',
    'Nośnik docelowy':
        '目标存储介质',
    'Odtwarza pliki z kopii — całość albo wybrany folder.':
        '从备份中恢复文件——全部或所选文件夹。',
    'Odśwież listę':
        '刷新列表',
    'Ostatnia kopia: {when} • {count} {files}.':
        '上次备份：{when} • {count} {files}。',
    'Pierwszy przebieg jest najdłuższy — kolejne porównują rozmiar i datę modyfikacji, więc zwykle trwają sekundy.':
        '第一次运行耗时最长——之后的运行会比较大小和修改日期，因此通常只需几秒钟。',
    'Pliki w kopii będą zaszyfrowane; bez hasła nie da się ich odczytać.':
        '备份中的文件将被加密；没有密码就无法读取。',
    'Podfoldery są uwzględniane automatycznie.':
        '子文件夹会自动包含在内。',
    'Pokazuj ekran powitalny przy starcie':
        '启动时显示欢迎页面',
    'Ponownie sprawdza podłączone nośniki':
        '重新检查已连接的存储设备',
    'Program będzie utrzymywał jeden folder zgodny ze źródłem. Każdy kolejny przebieg dopisze tylko to, co się zmieniło.':
        '程序将维护一个与源保持一致的文件夹。之后每次运行只写入发生变化的内容。',
    'Projekty i kod':
        '项目和代码',
    'Przechodzi do następnego kroku':
        '进入下一步',
    'Przechodzi do pełnego okna programu':
        '进入完整的程序窗口',
    'Sam wskażesz, co ma trafić do kopii.':
        '由你自己选择要备份的内容。',
    'System plików: {filesystem}, klaster {cluster}':
        '文件系统：{filesystem}，簇大小 {cluster}',
    'Ten katalog leży wewnątrz folderu źródłowego — wybierz inny.':
        '此文件夹位于源文件夹内——请另选一个。',
    'Ten nośnik nie obsługuje twardych dowiązań, więc każda wersja z datą zajmie tyle miejsca co pełna kopia. Przy tym nośniku rozważ „jedną aktualną kopię”.':
        '此存储介质不支持硬链接，因此每个带日期的版本都会占用与完整备份相同的空间。使用此存储介质时，可考虑选择“一份最新副本”。',
    'To dysk systemowy — kopia nie przetrwa jego awarii. Jeśli masz drugi dysk albo pendrive, wybierz jego.':
        '这是系统盘——它一旦故障，备份也保不住。如果你有第二块硬盘或 U 盘，请选择它。',
    'To się wydarzy':
        '将会发生什么',
    'Trzy gotowe zestawy zamiast kilkunastu przełączników.':
        '三套现成方案，代替十几个开关。',
    'Twoje pliki osobiste z folderów użytkownika. Najczęstszy wybór.':
        '用户文件夹中的个人文件。最常见的选择。',
    'Uruchamia kreator, który ustawi kopię krok po kroku':
        '启动向导，逐步设置备份',
    'Uruchom kreator…':
        '运行向导…',
    'Ustawia kopię krok po kroku i zapisuje ją jako szablon':
        '逐步设置备份，并将其保存为模板',
    'Ustawienia pierwszej kopii':
        '设置首次备份',
    'Ustawienia pierwszej kopii…':
        '设置首次备份…',
    'W tym katalogu jest już kopia ({count} {files}) — program ją uzupełni, a nie nadpisze.':
        '此文件夹中已有备份（{count} {files}）——程序会补全它，而不是覆盖。',
    'Wraca do poprzedniego kroku':
        '返回上一步',
    'Wskaż dowolny katalog docelowy':
        '指定任意目标文件夹',
    'Wskaż folder kopii i kliknij „Sprawdź kopię”.':
        '请指定备份文件夹，然后点击“检查备份”。',
    'Wstecz':
        '上一步',
    'Wybierz':
        '选择',
    'Wybierz inny folder…':
        '选择其他文件夹…',
    'Wybierz to, co najbliższe. Dokładną listę folderów poprawisz niżej.':
        '选择最接近的一项。具体的文件夹列表可在下方调整。',
    'Wybrane foldery':
        '所选文件夹',
    'Zamknij':
        '关闭',
    'Zamyka kreator bez zapisywania':
        '关闭向导，不保存',
    'Zapisuje nowe i zmienione pliki. Pierwszy raz trwa najdłużej.':
        '写入新增和更改的文件。第一次耗时最长。',
    'Zapisuje szablon bez uruchamiania kopii':
        '保存模板，但不开始备份',
    'Zapisuje szablon i od razu uruchamia kopię':
        '保存模板并立即开始备份',
    'Zapisz i zrób kopię':
        '保存并立即备份',
    'Zapisz ustawienia':
        '保存设置',
    'Zrób kopię':
        '立即备份',
    'dysk systemowy':
        '系统盘',
    'wolne {free} z {total}':
        '可用 {free}（共 {total}）',
    'Porównano ze źródłem: {source}; tylko z sumą kontrolną (źródło zmieniło się albo jest niedostępne): {checksum}.':
        '已与源比较：{source}；仅与校验和比较（源已更改或不可用）：{checksum}。',
    'Przywraca losową próbkę plików do katalogu tymczasowego i porównuje je ze źródłem.\nSprawdza całą drogę odzyskiwania, a trwa minuty. Nic nie zostaje na dysku.':
        '将随机抽取的一部分文件恢复到临时文件夹，并与源进行比较。\n可检验整个恢复流程，只需几分钟。不会在磁盘上留下任何内容。',
    'Próbne przywrócenie':
        '恢复演练',
    'W kopii nie ma plików, które dałoby się sprawdzić próbnie.':
        '备份中没有可用于恢复演练的文件。',
    'przywrócony plik różni się od pliku źródłowego':
        '恢复的文件与源文件不同',
    'przywrócony plik różni się od sumy kontrolnej zapisanej podczas kopii':
        '恢复的文件与备份时记录的校验和不符',
    'próbne przywrócenie':
        '恢复演练',
    '(brak zapisanych szablonów)':
        '（没有已保存的模板）',
    'Bez tego kopia planowa ruszy dopiero wtedy, gdy sam otworzysz program.':
        '否则，计划备份只会在你自己打开程序时才开始。',
    'Codziennie o godzinie':
        '每天定时',
    'Codziennie o wybranej godzinie (zalecane)':
        '每天在选定的时间（推荐）',
    'Dla dysku USB podłączanego od czasu do czasu. Najwyżej jedna kopia na 12 godzin.':
        '适用于不时连接的 USB 驱动器。每 12 小时最多备份一次。',
    'Dostępne w zainstalowanej wersji programu (plik EXE).':
        '仅在已安装的程序版本（EXE 文件）中可用。',
    'Godzina kopii codziennej (czas tego komputera).':
        '每日备份的时间（以本机时钟为准）。',
    'Harmonogram działa wtedy, gdy działa program — także ukryty przy zegarze.':
        '计划在程序运行时生效——包括程序隐藏在时钟旁时。',
    'Harmonogram nie uruchamia kopii, dopóki tego nie odznaczysz. Ręczne kopie działają.':
        '在你取消勾选此项之前，计划不会启动任何备份。手动备份仍然可用。',
    'Harmonogram szablonu „{name}” zapisany.':
        '模板“{name}”的计划已保存。',
    'Harmonogram:':
        '计划：',
    'Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.':
        '如果届时计算机处于关机状态，备份会在开机后开始。',
    'Kiedy kopia z tego szablonu ma ruszać sama.':
        '此模板的备份何时自动开始。',
    'Kiedy robić kopię?':
        '何时备份？',
    'Kopia będzie robiona codziennie o {time}; termin przegapiony przy wyłączonym komputerze program nadrobi po jego włączeniu.':
        '备份将在每天 {time} 进行；如果因计算机关机而错过时间，程序会在开机后补做。',
    'Kopia planowa nie powiodła się':
        '计划备份失败',
    'Kopia rusza tylko wtedy, gdy ją uruchomisz.':
        '只有在你启动时才会备份。',
    'Kopia ruszy po podłączeniu dysku docelowego (najwyżej raz na 12 godzin).':
        '连接目标驱动器后开始备份（每 12 小时最多一次）。',
    'Kopia ruszy po podłączeniu dysku docelowego — najwyżej raz na 12 godzin.':
        '连接目标驱动器后开始备份——每 12 小时最多一次。',
    'Kopia sprzed miesiąca nie chroni tego, co zmieniło się od tamtej pory.':
        '一个月前的备份无法保护此后发生的更改。',
    'Kopia „{name}” czeka':
        '备份“{name}”已逾期',
    'Kopia „{name}” nie ruszyła':
        '备份“{name}”未能启动',
    'Kopie planowe działają, gdy działa program (także ukryty przy zegarze).':
        '计划备份在程序运行时进行（包括程序隐藏在时钟旁时）。',
    'Kopie planowe działają, gdy działa program: po zamknięciu okna zostaje ikona przy zegarze, a przy logowaniu do Windows program uruchamia się w tle.':
        '计划备份在程序运行时进行：关闭窗口后，时钟旁会保留一个图标；登录 Windows 时，程序会在后台启动。',
    'Kopie planowe i praca w tle':
        '计划备份与后台运行',
    'Kopie planowe wykonają się o czasie. Program zamkniesz z menu ikony przy zegarze.':
        '计划备份会按时进行。可通过时钟旁图标的菜单退出程序。',
    'Kopię uruchamiasz przyciskiem. Najprostsze, ale łatwo o niej zapomnieć.':
        '通过按钮启动备份。最简单，但容易忘记。',
    'Kopię uruchamiasz sam — przyciskiem w programie albo z menu ikony przy zegarze.':
        '由你自己启动备份——使用程序中的按钮，或时钟旁图标的菜单。',
    'Następna kopia: {when}. Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.':
        '下次备份：{when}。如果届时计算机处于关机状态，备份会在开机后开始。',
    'Nie udało się zmienić startu przy logowaniu — szczegóły w dzienniku.':
        '无法更改登录时启动的设置——详情见日志。',
    'Od {days} dni nie było udanej kopii. Podłącz dysk docelowy albo otwórz program, żeby sprawdzić, co się dzieje.':
        '已经 {days} 天没有成功的备份了。请连接目标驱动器，或打开程序查看情况。',
    'Otwórz Sigelith Backup':
        '打开 Sigelith Backup',
    'Po podłączeniu dysku docelowego':
        '连接目标驱动器时',
    'Po podłączeniu dysku z kopią':
        '连接备份驱动器时',
    'Po zamknięciu okna działaj dalej przy zegarze, gdy są kopie planowe':
        '有计划备份时，关闭窗口后继续在时钟旁运行',
    'Potrzebne, żeby kopie planowe ruszały bez Twojego udziału. Hasło trafia do magazynu systemowego powiązanego z Twoim kontem, nie do plików programu.':
        '计划备份需要它才能在无人值守时启动。密码会存入与你的账户绑定的系统存储，而不是程序的文件。',
    'Program uruchamia się w tle przy logowaniu, więc terminy nie przepadną.':
        '程序会在登录时于后台启动，因此不会错过计划时间。',
    'Ręcznie':
        '手动',
    'Ręcznie — kiedy zechcę':
        '手动——由我决定何时备份',
    'Start przy logowaniu włączony':
        '已开启登录时启动',
    'Szablon jest zaszyfrowany, a hasło nie jest zapamiętane. Kopie planowe potrzebują hasła zapisanego w Menedżerze poświadczeń Windows.':
        '模板已加密，但未记住密码。计划备份需要保存在 Windows 凭据管理器中的密码。',
    'Sigelith Backup będzie uruchamiał się w tle, żeby wykonywać kopie planowe. Wyłączysz to w ustawieniach programu.':
        'Sigelith Backup 将在后台启动以执行计划备份。可在程序设置中关闭此功能。',
    'Sigelith Backup działa w tle':
        'Sigelith Backup 正在后台运行',
    'Uruchamiaj program w tle przy logowaniu do Windows':
        '登录 Windows 时在后台启动程序',
    'Wstrzymaj kopie planowe':
        '暂停计划备份',
    'Zakończ':
        '退出',
    'Zamknięcie okna chowa je, a harmonogram pilnuje terminów. Program zamkniesz z menu ikony przy zegarze.':
        '关闭窗口只会将其隐藏，计划会继续按时执行。可通过时钟旁图标的菜单退出程序。',
    'Zrób kopię teraz':
        '立即备份',
    '{summary} Szczegóły znajdziesz w programie, w zakładce „Dziennik”.':
        '{summary}详情见程序中的“日志”页面。',
    'Program działa z uprawnieniami administratora. Nie są mu potrzebne — kopia i przywracanie działają bez nich, a pliki zapisane przez administratora mogą później nie dać się zmienić ze zwykłego konta.':
        '程序正以管理员权限运行。它并不需要这些权限——备份和恢复无需管理员权限即可工作，而由管理员写入的文件以后可能无法在普通账户下修改。',
    'Pliki otwarte w innych programach nie trafiły do kopii: {files}. Zamknij te programy i uruchom kopię ponownie — dograne zostaną tylko te pliki.':
        '在其他程序中打开的文件未能存入备份：{files}。请关闭这些程序并重新运行备份——只会补写这些文件。',
    'Uwaga: w źródle zmieniło się podejrzanie dużo plików — {reasons}':
        '警告：源中有可疑的大量文件发生了变化——{reasons}',
    'Wstrzymano kopię: w źródle zmieniło się podejrzanie dużo plików. {reasons}':
        '备份已暂停：源中有可疑的大量文件发生了变化。{reasons}',
    'Zmieniło się albo zniknęło {count} z {previous} plików poprzedniej kopii.':
        '上一次备份的 {previous} 个文件中，有 {count} 个已更改或消失。',
    '{suspicious} z {evaluated} sprawdzonych zmienionych plików ma treść, która nie pasuje do ich typu (wygląda na zaszyfrowaną).':
        '在检查的 {evaluated} 个已更改文件中，有 {suspicious} 个的内容与其文件类型不符（看起来像是被加密了）。',
    'Kontynuuj mimo to':
        '仍然继续',
    'Kopia planowa wstrzymana':
        '计划备份已暂停',
    'Kopia wstrzymana do decyzji.':
        '备份已暂停，等待你的决定。',
    'Kopia wstrzymana — w źródle zmieniło się podejrzanie dużo plików.':
        '备份已暂停——源中有可疑的大量文件发生了变化。',
    'Podejrzanie dużo zmian':
        '更改数量可疑',
    'Wstrzymaj kopię':
        '暂停备份',
    '{reasons}\n\nJeśli to spodziewane — aktualizacja programu, przeniesienie albo przerobienie wielu plików — kontynuuj.\n\nJeśli nie, NIE kontynuuj: tak wygląda działanie oprogramowania szyfrującego pliki (ransomware). Sprawdź najpierw, czy Twoje pliki dają się otworzyć. Wcześniejsze wersje w kopii pozostają nietknięte.':
        '{reasons}\n\n如果这在意料之中——例如软件更新、移动或大量修改文件——请继续。\n\n如果不是，请务必不要继续：这正是加密文件的恶意软件（勒索软件）的表现。请先检查你的文件是否还能打开。备份中的早期版本不受影响。',
    '{reasons} To może być działanie złośliwego oprogramowania szyfrującego pliki. Otwórz program, sprawdź pliki i uruchom kopię ręcznie.':
        '{reasons}这可能是加密文件的恶意软件所为。请打开程序，检查文件，然后手动运行备份。',
    'Pominięto {count} {files}.':
        '已跳过 {count} {files}。',
    'Ponawiam {count} {files}…':
        '正在重试 {count} {files}…',
    ' (bez {count} {files})':
        ' (不含 {count} {files})',
    'plik otwarty w innym programie':
        '个在其他程序中打开的文件',
    'pliki otwarte w innych programach':
        '个在其他程序中打开的文件',
    'plików otwartych w innych programach':
        '个在其他程序中打开的文件',
    'pliku otwartego w innym programie':
        '个在其他程序中打开的文件',
    '\n\n…i kolejne: {count}.':
        '\n\n…另有 {count} 项。',
    'Foldery objęte kopią ({count}): {list}':
        '要备份的文件夹（{count}）：{list}',
    'Nośnik nie obsługuje twardych dowiązań — kopiuję do nowej wersji niezmienione pliki: {count} ({size})…':
        '存储介质不支持硬链接——正在将未更改的文件复制到新版本：{count}（{size}）…',
    'Pliki bez sumy kontrolnej sprawdzone tylko co do rozmiaru, bo ich źródło zmieniło się albo jest niedostępne: {count}.':
        '没有校验和、仅按大小检查的文件（因其源已更改或不可用）：{count}。',
    'Pliki bez zapisanej sumy kontrolnej, porównane ze źródłem i uzupełnione w spisie treści: {count}.':
        '没有记录校验和、已与源比较并补入内容清单的文件：{count}。',
    'Pliki przeniesione w źródle: {count} — trafią do kopii bez przesyłania danych.':
        '在源中被移动的文件：{count}——它们无需传输数据即可存入备份。',
    'Pliki skasowane w źródle: {count} — {action}.':
        '源中已删除的文件：{count}——{action}。',
    'Pliki z końcówką dopisaną do nazwy, których oryginały zniknęły: {count}.':
        '名称后被添加了后缀、且原文件已消失的文件：{count}。',
    'Pliki zmienione w trakcie kopiowania: {count} — zostaną zapisane ponownie w przebiegu uzupełniającym.':
        '复制过程中发生更改的文件：{count}——将在补录轮次中重新写入。',
    'Pliki, których brakuje w kopii i które zostaną zapisane ponownie: {count}.':
        '备份中缺失、将重新写入的文件：{count}。',
    'Podpinanie niezmienionych plików do nowej wersji: {count}…':
        '正在将未更改的文件链接到新版本：{count}…',
    'Pomijam pliki, które już są w tej wersji kopii: {count}.':
        '跳过此备份版本中已有的文件：{count}。',
    'Porządkowanie historii — usunięte najstarsze wersje: {count}.':
        '整理历史记录——已删除最旧的版本：{count}。',
    'Przenoszenie plików, które zmieniły miejsce w źródle: {count}…':
        '正在移动在源中位置发生变化的文件：{count}…',
    'Próbne przywrócenie losowo wybranych plików: {count}…':
        '正在对随机选取的文件进行恢复演练：{count}…',
    'Usuwanie z kopii plików skasowanych w źródle: {count}…':
        '正在从备份中删除源中已删除的文件：{count}…',
    'Uzupełniam kopię o pliki, które przybyły lub zmieniły się w trakcie: {count} ({size})…':
        '正在补录备份期间新增或更改的文件：{count}（{size}）…',
    'Uzupełnianie wersji {version} — pliki już zapisane, które zostaną pominięte: {count}.':
        '补全版本 {version}——将跳过已写入的文件：{count}。',
    'Wznawiam wersję {version} — już zapisane: {done}, do dogrania: {todo}.':
        '继续写入版本 {version}——已写入：{done}，待补写：{todo}。',
    'pliku':
        '个文件',
    'Brak fragmentu {cid} w magazynie kopii.':
        '备份的数据块存储中缺少数据块 {cid}。',
    'Brak opisu magazynu fragmentów w katalogu kopii.':
        '备份文件夹中缺少数据块存储的描述。',
    'Duże pliki zapisuj różnicowo (od 256 MB)':
        '大文件以差异方式存储（256 MB 及以上）',
    'Fragment {cid} jest uszkodzony.':
        '数据块 {cid} 已损坏。',
    'Kolejna wersja dużego pliku — maszyny wirtualnej, skrzynki pocztowej, bazy —\nzapisuje tylko zmienione fragmenty zamiast całego pliku. W kopii taki plik\nleży jako przepis + fragmenty; złoży go program albo skrypt ratunkowy.':
        '大文件（虚拟机、邮箱、数据库）的后续版本\n只存储发生变化的数据块，而不是整个文件。在备份中，这样的文件\n以“配方 + 数据块”的形式存放；由本程序或救援脚本将其重新组装。',
    'Opis magazynu fragmentów jest uszkodzony.':
        '数据块存储的描述已损坏。',
    'Plik złożony z fragmentów różni się od zapisanego w przepisie.':
        '由数据块组装出的文件与配方中记录的不同。',
    'Podane hasło nie pasuje do fragmentów zapisanych wcześniej w tej kopii.':
        '输入的密码与此备份中先前写入的数据块不匹配。',
    'Przepis pliku jest uszkodzony.':
        '文件的配方已损坏。',
    'To nie jest przepis pliku zapisanego fragmentami.':
        '这不是分块存储文件的配方。',
    'Usunięto nieużywane fragmenty dużych plików: {count} ({size}).':
        '已删除大文件中不再使用的数据块：{count}（{size}）。',
    ', zakotwiczona w Bitcoinie':
        '，已锚定到 Bitcoin',
    'Adres usługi:':
        '服务地址：',
    'Brak fragmentu {cid} w kopii poza domem.':
        '异地副本中缺少数据块 {cid}。',
    'Brak klucza albo hasła w Menedżerze poświadczeń Windows — zapisz ustawienia kopii poza domem jeszcze raz.':
        'Windows 凭据管理器中缺少密钥或密码——请重新保存异地副本的设置。',
    'Brak spisu wersji, którego dotyczy znacznik.':
        '缺少该时间戳所对应的版本清单。',
    'Certyfikat PDF':
        'PDF 证书',
    'Druga, zaszyfrowana kopia w usłudze zgodnej z S3 (np. Backblaze B2)':
        '在兼容 S3 的服务（例如 Backblaze B2）中保存第二份加密副本',
    'Folder w kubełku:':
        '存储桶中的文件夹：',
    'Hasło kopii poza domem':
        '异地副本密码',
    'Hasło kopii poza domem nie pasuje do danych zapisanych w tym miejscu.':
        '异地副本密码与该位置存储的数据不匹配。',
    'Hasło kopii poza domem powinno mieć co najmniej 10 znaków.':
        '异地副本密码应至少包含 10 个字符。',
    'Hasło szyfrowania:':
        '加密密码：',
    'Identyfikator klucza:':
        '访问密钥 ID：',
    'Katalog, do którego trafią pliki':
        '文件将存入的文件夹',
    'Klucz tajny':
        '秘密访问密钥',
    'Klucz tajny:':
        '秘密访问密钥：',
    'Kopia na dysku obok komputera nie przetrwa pożaru ani kradzieży. Tu ustawisz drugą kopię w usłudze zgodnej z S3 (np. Backblaze B2). Pliki są szyfrowane na tym komputerze osobnym hasłem — usługa widzi tylko nieczytelne fragmenty.':
        '放在电脑旁边驱动器上的备份，躲不过火灾或盗窃。在这里可以在兼容 S3 的服务（例如 Backblaze B2）中设置第二份副本。文件会在这台电脑上用单独的密码加密——服务只能看到无法读取的数据块。',
    'Kopia poza domem':
        '异地副本',
    'Kopia poza domem dla szablonu „{name}” zapisana.':
        '模板“{name}”的异地副本设置已保存。',
    'Kopia poza domem nie ruszyła':
        '异地副本上传未能开始',
    'Kopia poza domem potrzebuje Menedżera poświadczeń Windows, a jest on niedostępny.':
        '异地副本需要使用 Windows 凭据管理器，但它不可用。',
    'Kopia poza domem „{name}”':
        '异地副本“{name}”',
    'Kopia poza domem…':
        '异地副本…',
    'Korzeń tygodnia zakotwiczony w łańcuchu Bitcoina.':
        '周根已锚定到 Bitcoin 区块链。',
    'Kubełek (bucket):':
        '存储桶（bucket）：',
    'Migawek w usłudze: {count}.':
        '服务中的快照：{count} 个。',
    'Migawka i cel':
        '快照与目标',
    'Migawka kopii poza domem jest uszkodzona.':
        '异地副本的快照已损坏。',
    'Migawka {stamp}: plików bez zmian {reused}, wysłanych {files}, nowych fragmentów {chunks} ({size}).':
        '快照 {stamp}：未更改的文件 {reused} 个，已上传 {files} 个，新数据块 {chunks} 个（{size}）。',
    'MinIO / Wasabi / inna zgodna z S3':
        'MinIO / Wasabi / 其他兼容 S3 的服务',
    'NIEPOPRAWNY':
        '无效',
    'Nie ma migawki {stamp} w kopii poza domem.':
        '异地副本中没有快照 {stamp}。',
    'Nie udało się połączyć z usługą przechowywania: {error}':
        '无法连接到存储服务：{error}',
    'Nie udało się wczytać migawek: {error}':
        '无法载入快照：{error}',
    'Nie udało się zapisać klucza albo hasła w magazynie systemowym.':
        '无法将密钥或密码保存到系统存储。',
    'Odśwież z sieci':
        '联网刷新',
    'Opis kopii poza domem jest uszkodzony.':
        '异地副本的描述已损坏。',
    'Oznakowana: {utc} (BeatTime {beat})':
        '盖戳时间：{utc}（BeatTime {beat}）',
    'Pliki wersji różnią się od spisu, który został oznakowany.':
        '该版本的文件与已加盖时间戳的清单不一致。',
    'Pobiera i odszyfrowuje pliki wybranej migawki':
        '下载并解密所选快照中的文件',
    'Pobiera listę migawek z usługi':
        '从服务下载快照列表',
    'Pobiera podpis tygodnia i stan kotwicy w Bitcoinie':
        '下载周签名和 Bitcoin 锚定的状态',
    'Pobieram potwierdzenia…':
        '正在下载回执…',
    'Podaj hasło szyfrowania kopii poza domem.':
        '请输入异地副本的加密密码。',
    'Podaj klucz tajny usługi.':
        '请输入该服务的秘密访问密钥。',
    'Podam dane ręcznie':
        '手动输入连接信息',
    'Pominięte (otwarte w innych programach albo zmienione w trakcie): {count}.':
        '已跳过（在其他程序中打开或期间发生更改）：{count}。',
    'Porządkowanie kopii poza domem…':
        '正在整理异地副本…',
    'Potwierdzenia odświeżone.':
        '回执已刷新。',
    'Poza dom':
        '异地',
    'Połączenie działa: zapis, odczyt i usuwanie się udały.':
        '连接正常：写入、读取和删除均成功。',
    'Połączenie nie działa: {error}':
        '连接失败：{error}',
    'Przywraca pliki z zaszyfrowanej kopii w usłudze S3 — także na nowym komputerze':
        '从 S3 服务中的加密副本恢复文件——在新电脑上也可以',
    'Przywracanie z kopii poza domem':
        '从异地副本恢复',
    'Przywracanie {count} {files} z kopii poza domem…':
        '正在从异地副本恢复 {count} {files}…',
    'Przywróć':
        '恢复',
    'Region:':
        '区域：',
    'Skąd':
        '来源',
    'Spis wersji zgodny ze znacznikiem: {answer}':
        '版本清单与时间戳一致：{answer}',
    'Spis wersji został zmieniony po oznakowaniu.':
        '版本清单在加盖时间戳后被修改过。',
    'Sprawdza spis wersji, drogę w drzewie tygodnia i podpis — bez sieci':
        '检查版本清单、该周 Merkle 树中的路径和签名——无需联网',
    'Sprawdzam połączenie…':
        '正在检查连接…',
    'Sprawdź':
        '检查',
    'Sprawdź połączenie':
        '检查连接',
    'Starsze migawki są usuwane, gdy nadmiar sięgnie kilku — co kilka dni.':
        '多出的快照累积到几个时，会删除较旧的快照——大约每隔几天一次。',
    'Suma w drzewie tygodnia: {answer}':
        '校验和在该周 Merkle 树中：{answer}',
    'Suma wersji nie należy do drzewa tygodnia podanego w potwierdzeniu.':
        '版本校验和不属于回执中给出的该周 Merkle 树。',
    'Ta wersja nie ma znacznika czasu.':
        '此版本没有时间戳。',
    'Także po kopiach planowych. Wysyłane są tylko pliki nowe i zmienione.':
        '计划备份后同样如此。只上传新增和更改的文件。',
    'Tydzień jeszcze się nie zamknął — podpis pojawi się po poniedziałku 00:00 UTC.':
        '该周尚未结束——签名将在周一 00:00 UTC 之后出现。',
    'Usunięto starsze migawki: {count}, nieużywane fragmenty: {chunks}.':
        '已删除较旧的快照：{count}，不再使用的数据块：{chunks}。',
    'Usługa chwilowo niedostępna ({status}).':
        '服务暂时不可用（{status}）。',
    'Usługa odrzuciła żądanie ({status} {code}): {message}':
        '服务拒绝了请求（{status} {code}）：{message}',
    'Usługa przechowywania':
        '存储服务',
    'Usługa zwróciła inną treść niż zapisana.':
        '服务返回的内容与写入的不同。',
    'Usługa:':
        '服务：',
    'Uzupełnij adres usługi, nazwę kubełka i klucze dostępu.':
        '请填写服务地址、存储桶名称和访问密钥。',
    'Uzupełnij adres usługi, region, kubełek i identyfikator klucza.':
        '请填写服务地址、区域、存储桶和访问密钥 ID。',
    'W tym katalogu kopii nie ma jeszcze znaczników czasu.':
        '此备份文件夹中还没有时间戳。',
    'W tym miejscu nie ma jeszcze kopii poza domem.':
        '此位置还没有异地副本。',
    'Wczytaj migawki':
        '载入快照',
    'Wczytaj migawki i wybierz jedną z listy.':
        '请载入快照，并从列表中选择一个。',
    'Wczytuję migawkę {stamp}…':
        '正在载入快照 {stamp}…',
    'Wczytuję poprzednią migawkę kopii poza domem…':
        '正在载入异地副本的上一个快照…',
    'Wybierz migawkę i katalog, do którego trafią pliki.':
        '请选择快照以及文件将存入的文件夹。',
    'Wybierz wersję z listy.':
        '请从列表中选择一个版本。',
    'Wysyłaj poza dom po każdej udanej kopii z tego szablonu':
        '每次用此模板成功备份后上传到异地',
    'Wysyłam poza dom pliki nowe i zmienione: {count}…':
        '正在将新增和更改的文件上传到异地：{count}…',
    'Z kopii poza domem…':
        '从异地副本恢复…',
    'Zachowuj migawek:':
        '保留快照数：',
    'Zapisuje ustawienia; klucz i hasło trafiają do Menedżera poświadczeń Windows':
        '保存设置；密钥和密码将存入 Windows 凭据管理器',
    'Zapisuje, odczytuje i usuwa mały plik próbny':
        '写入、读取并删除一个小测试文件',
    'Zapisuję migawkę {stamp}…':
        '正在保存快照 {stamp}…',
    'Znacznik dowodzi, że wersja kopii w dokładnie tym kształcie istniała w podanej chwili. Podpis tygodnia pojawia się po jego zamknięciu (poniedziałek 00:00 UTC), a kotwica w Bitcoinie — zwykle kilka godzin później.':
        '时间戳证明该备份版本在给定时刻以完全相同的状态存在。周签名在该周结束后出现（周一 00:00 UTC），Bitcoin 锚定通常在几小时后出现。',
    'Znacznika czasu nie udało się zapisać: {error}':
        '无法保存时间戳：{error}',
    'Znaczniki czasu':
        '时间戳',
    'Znaczniki czasu…':
        '时间戳…',
    'kopia poza domem':
        '异地副本',
    'np. komputer-domowy':
        '例如 home-pc',
    'oznakowana {when} — podpis po zamknięciu tygodnia':
        '已于 {when} 加盖时间戳——周结束后签名',
    'podpisana (tydzień {week}){bitcoin}':
        '已签名（{week} 周）{bitcoin}',
    'poprawny':
        '有效',
    'przywracanie z kopii poza domem':
        '从异地副本恢复',
    'Łączę się z usługą…':
        '正在连接服务…',
    ' dni':
        ' 天',
    ' mies.':
        ' 个月',
    ' tyg.':
        ' 周',
    'Ile ostatnich wersji zachować. Starsze są kasowane po udanym przebiegu.':
        '保留最近的多少个版本。更早的版本会在成功运行后删除。',
    'Kalendarz zostawia najnowszą wersję z każdego z ostatnich dni, tygodni\ni miesięcy — gęsto dla świeżych zmian, rzadko dla dawnych. Nadmiar jest\nkasowany po udanym przebiegu; wersje niedokończone nigdy.':
        '日历方式会为最近的每一天、每一周\n和每个月各保留最新的一个版本——近期的更改保留得密，久远的保留得疏。多余的版本\n会在成功运行后删除；未完成的版本永远不会被删除。',
    'Z ilu ostatnich dni zachować po jednej, najnowszej wersji.':
        '为最近多少天各保留一个最新版本。',
    'Z ilu ostatnich miesięcy zachować po jednej, najnowszej wersji.':
        '为最近多少个月各保留一个最新版本。',
    'Z ilu ostatnich tygodni zachować po jednej, najnowszej wersji.':
        '为最近多少周各保留一个最新版本。',
    'Zachowuj:':
        '保留：',
    'kalendarz: dni, tygodnie, miesiące':
        '日历：天、周、月',
    'ostatnie wersje':
        '最近的版本',
    'wszystkie wersje':
        '所有版本',
    ' (niedokończona)':
        ' (未完成)',
    'Fragment nazwy albo ścieżki, bez rozróżniania wielkości liter.':
        '名称或路径的一部分，不区分大小写。',
    'Główny folder kopii':
        '备份主文件夹',
    'Historia pliku':
        '文件历史',
    'Nazwa':
        '名称',
    'Nic nie znaleziono.':
        '未找到任何内容。',
    'Nie udało się: {error}':
        '失败：{error}',
    'Odtwarza plik do katalogu tymczasowego i otwiera go':
        '将文件恢复到临时文件夹并打开',
    'Odtwarza plik w wybranym miejscu':
        '将文件恢复到你选择的位置',
    'Odtwarzam „{name}”…':
        '正在恢复“{name}”…',
    'Otwarto kopię „{name}” (plik tymczasowy, zniknie po zamknięciu programu).':
        '已打开“{name}”的副本（临时文件，关闭程序后将被删除）。',
    'Otwórz':
        '打开',
    'Otwórz kopię':
        '打开副本',
    'Pliki i wersje wprost z kopii — bez przywracania':
        '直接查看备份中的文件和版本——无需恢复',
    'Pliki i wersje wprost z kopii — bez przywracania całości.':
        '直接查看备份中的文件和版本——无需恢复全部内容。',
    'Pokazuje pliki i wersje tej kopii — pojedynczy plik otworzysz bez przywracania całości':
        '显示此备份中的文件和版本——无需恢复全部内容即可打开单个文件',
    'Pokaż foldery':
        '显示文件夹',
    'Przeglądaj…':
        '浏览…',
    'Przeglądanie':
        '浏览',
    'Przeszukuje spis treści kopii':
        '搜索备份的内容清单',
    'Rozmiar':
        '大小',
    'Szukaj':
        '搜索',
    'Szukaj pliku w najnowszym stanie kopii…':
        '在备份的最新状态中搜索文件…',
    'Szukam…':
        '正在搜索…',
    'W których wersjach jest ten plik i kiedy się zmieniał':
        '此文件存在于哪些版本中，以及何时发生过更改',
    'W tym folderze nie ma wersji kopii.':
        '此文件夹中没有备份版本。',
    'Wczytuje wersje z tego folderu kopii':
        '载入此备份文件夹中的版本',
    'Wersja kopii, której zawartość widzisz poniżej.':
        '下方所显示内容对应的备份版本。',
    'Wersja: {version}':
        '版本：{version}',
    'Wersje z tym plikiem: {count}. Dwuklik otwiera kopię z danej wersji.':
        '包含此文件的版本：{count}。双击可打开该版本中的副本。',
    'Wraca z wyników wyszukiwania do drzewa folderów':
        '从搜索结果返回文件夹树',
    'Wskaż folder kopii i kliknij „Otwórz”.':
        '请指定备份文件夹，然后点击“打开”。',
    'Zapisano: {path}':
        '已保存：{path}',
    'Zapisz jako…':
        '另存为…',
    'Zapisz kopię pliku':
        '保存文件副本',
    'Zaznacz plik i wybierz „Otwórz kopię”, żeby zajrzeć do niego w zwykłym programie, albo „Historia pliku”, żeby zobaczyć, w których wersjach się zmieniał.':
        '选中一个文件后，选择“打开副本”即可用常用程序查看它，或选择“文件历史”查看它在哪些版本中发生过更改。',
    'Zmieniono':
        '修改时间',
    'Znalezione pliki: {count}. Wyniki pochodzą z najnowszego stanu kopii.':
        '找到的文件：{count}。结果来自备份的最新状态。',
    'przeglądanie kopii':
        '浏览备份',
    'zmieniony':
        '已更改',
    'najstarsza zachowana kopia':
        '保留的最早副本',
    'Foldery w AppData':
        'AppData 中的文件夹',
    'Przywracanie utworzy nowe foldery bezpośrednio w AppData:\n\n{folders}\n\nWindows pozwala wersji programu ze Sklepu tworzyć je tylko w jej prywatnej kopii — pliki będą widoczne w tym programie, ale nie w programie, do którego należą.\n\nNajprościej: zainstaluj i raz uruchom tamten program (utworzy swój folder), a potem przywróć jeszcze raz. Albo przywróć do zwykłego folderu i przenieś pliki Eksploratorem.':
        '恢复操作将直接在 AppData 中创建新文件夹：\n\n{folders}\n\nWindows 只允许本程序的 Microsoft Store 版本在其私有副本中创建这些文件夹——文件在本程序中可见，但在它们所属的程序中不可见。\n\n最简单的办法：安装并运行一次那个程序（它会创建自己的文件夹），然后再恢复一次。或者恢复到普通文件夹，再用文件资源管理器移动这些文件。',
    'Przywracanie utworzyłoby w AppData nowe foldery, których inne programy nie zobaczą: {folders}':
        '恢复操作会在 AppData 中创建其他程序看不到的新文件夹：{folders}',
    'Przywracanie wstrzymane do decyzji.':
        '恢复已暂停，等待你的决定。',
    'Przywróć mimo to':
        '仍然恢复',
    'Start programu przy logowaniu wyłączono w Ustawieniach Windows. Włączysz go tam: Ustawienia → Aplikacje → Uruchamianie → Sigelith Backup.':
        '登录时启动程序的选项已在 Windows 设置中关闭。请在那里重新开启：设置 → 应用 → 启动 → Sigelith Backup。',
    'Start przy logowaniu':
        '登录时启动',
    'Start przy logowaniu wyłączono w Ustawieniach Windows → Aplikacje → Uruchamianie; dopóki go tam nie włączysz, kopie planowe działają tylko przy otwartym programie.':
        '登录时启动已在 Windows 设置 → 应用 → 启动中关闭；在你重新开启之前，计划备份只会在程序打开时运行。',
    'Ten sam przełącznik jest w Ustawieniach Windows → Aplikacje → Uruchamianie. Wyłączony tam da się włączyć tylko tam.':
        '同一个开关也位于 Windows 设置 → 应用 → 启动中。如果在那里关闭，就只能在那里重新开启。',
    'Brak pliku {name} w katalogu programu.':
        '程序文件夹中缺少文件 {name}。',
    'Jakie dane program przetwarza i gdzie':
        '程序处理哪些数据，以及在哪里处理',
    'Kod źródłowy Qt':
        'Qt 源代码',
    'Licencja programu':
        '程序许可证',
    'Licencja programu i licencje użytych składników':
        '程序许可证及所用组件的许可证',
    'Licencje':
        '许可证',
    'Licencje i prywatność':
        '许可证与隐私',
    'Licencje…':
        '许可证…',
    'Otwiera folder z plikami licencji w Eksploratorze':
        '在文件资源管理器中打开存放许可证文件的文件夹',
    'Pokaż pliki licencji':
        '显示许可证文件',
    'Polityka prywatności':
        '隐私政策',
    'Polityka prywatności…':
        '隐私政策…',
    'Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0 — to osobne pliki w katalogu programu, które można zastąpić zgodnymi wersjami. Kod źródłowy wersji dołączonych do programu: {qt} oraz {pyside}.':
        '本程序依据 LGPL-3.0 许可证使用 Qt 和 PySide6 库——它们是程序文件夹中的独立文件，可以替换为兼容的版本。随程序提供的版本的源代码：{qt} 和 {pyside}。',
    'Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0, z Pythona i z innych składników na licencjach otwartych (m.in. MIT, BSD, Apache 2.0); ikony: Bootstrap Icons (MIT). Wykaz, prawa autorskie, pełne teksty licencji i adresy kodu źródłowego Qt są pod przyciskiem „Licencje”.':
        '本程序依据 LGPL-3.0 许可证使用 Qt 和 PySide6 库，并使用 Python 以及其他采用开源许可证（包括 MIT、BSD、Apache 2.0）的组件；图标：Bootstrap Icons（MIT）。组件清单、版权声明、完整许可证文本以及 Qt 源代码的地址，见“许可证”按钮。',
    'Program usunie z Menedżera poświadczeń Windows wszystkie hasła, które zapamiętał: hasła kopii i dane dostępu do kopii poza domem. Kopie planowe szablonów zaszyfrowanych będą potem czekać, aż podasz hasło.\n\nUsunąć?':
        '程序将从 Windows 凭据管理器中删除它记住的所有密码：备份密码以及异地副本的访问凭据。之后，加密模板的计划备份将等待你输入密码。\n\n要删除吗？',
    'Składniki i ich licencje':
        '组件及其许可证',
    'Strona z kodem źródłowym Qt w wersji użytej w programie':
        '本程序所用版本的 Qt 源代码页面',
    'Usunięte zapamiętane hasła: {count}.':
        '已删除记住的密码：{count}。',
    'Usuwa z Menedżera poświadczeń Windows wszystkie hasła zapamiętane przez program — na przykład przed odinstalowaniem':
        '从 Windows 凭据管理器中删除程序记住的所有密码——例如在卸载之前',
    'Usuń zapamiętane hasła':
        '删除记住的密码',
    'Usuń zapamiętane hasła…':
        '删除记住的密码…',
    '© {years} {publisher}. Wolne oprogramowanie na licencji GNU GPL w wersji 3 lub nowszej.':
        '© {years} {publisher}。依据 GNU GPL 第 3 版或更高版本授权的自由软件。',
    'Kod źródłowy':
        '源代码',
    'Kod źródłowy programu w serwisie GitHub':
        'GitHub 上的程序源代码',
    'Sigelith odrzucił żądanie ({status}): {detail}':
        'Sigelith 拒绝了请求（{status}）：{detail}',
    'Nie udało się połączyć z Sigelith: {error}':
        '无法连接到 Sigelith：{error}',
    'Sigelith odesłał potwierdzenie innej sumy kontrolnej.':
        'Sigelith 返回的回执对应的是另一个校验和。',
    'Znacznik czeka na połączenie z Sigelith.':
        '时间戳正在等待连接 Sigelith。',
    'Podpis tygodnia nie zgadza się z kluczem Sigelith zapisanym w programie.':
        '周签名与程序内置的 Sigelith 密钥不符。',
    'Otwiera certyfikat znacznika na stronie Sigelith':
        '在 Sigelith 网站上打开该时间戳的证书',
    'Podpis Sigelith: {answer}':
        'Sigelith 签名：{answer}',
    'Znaczniki Sigelith wersji w tym katalogu kopii: sprawdzenie i certyfikat':
        '此备份文件夹中各版本的 Sigelith 时间戳：检查与证书',
    'Znakuję wersję czasem Sigelith (wysyłana jest tylko suma kontrolna)…':
        '正在用 Sigelith 为版本加盖时间戳（只发送校验和）…',
    'Znacznik czasu czeka na połączenie z Sigelith — zostanie wysłany przy następnej kopii.':
        '时间戳正在等待连接 Sigelith——将在下次备份时发送。',
    'Znakuj wersję czasem Sigelith':
        '用 Sigelith 为版本加盖时间戳',
    'Znaczniki czasu Sigelith':
        'Sigelith 时间戳',
    'czeka na połączenie z Sigelith':
        '等待连接 Sigelith',
    'Dowód, że kopia w tym kształcie istniała danego dnia (podpis Ed25519, kotwica\nw Bitcoinie). Do sigelith.org trafia wyłącznie suma kontrolna spisu wersji —\nżadne nazwy plików ani ich treść.':
        '证明备份在某一天以完全相同的状态存在（Ed25519 签名、Bitcoin\n锚定）。只有版本清单的校验和会发送到 sigelith.org——\n不含任何文件名，也不含文件内容。',
    'Kopie zapasowe folderów na dysk zewnętrzny, z historią wersji i szyfrowaniem. Wszystko dzieje się na Twoim komputerze, bez konta i bez telemetrii. Z internetem program łączy się tylko wtedy, gdy sam włączysz kopię poza domem albo znaczniki czasu Sigelith.':
        '将文件夹备份到外部驱动器，带版本历史和加密。一切都在你的电脑上进行，无需账户，没有遥测。只有在你自己开启异地副本或 Sigelith 时间戳时，程序才会连接互联网。',
    'Bez dokumentu: {count} {stamps} — plik zmienił się po stemplu albo zniknął i nie ma go w żadnej wersji tej kopii ({names}). Sam dowód jest zachowany.':
        '缺少文档：{count} {stamps}——文件在盖戳后被更改或已消失，且此备份的任何版本中都没有它（{names}）。证明本身已保留。',
    'Brak pliku dowodu albo dowód jest zaszyfrowany.':
        '缺少证明文件，或证明已加密。',
    'Chroni dowody Sigelith: historię stempli i oznakowane dokumenty.':
        '保护 Sigelith 证据：盖戳历史记录和已盖戳的文档。',
    'Chroń dowody Sigelith':
        '保护 Sigelith 证据',
    'Chroń też dowody Sigelith':
        '同时保护 Sigelith 证据',
    'Dokument':
        '文档',
    'Dokumenty oznakowane w Sigelith, zabezpieczone w tej kopii: sprawdzenie i odzyskanie':
        '用 Sigelith 盖戳、并在此备份中妥善保存的文档：检查与找回',
    'Dowody Sigelith':
        'Sigelith 证据',
    'Dowody Sigelith: historia stempli i dokładne kopie oznakowanych dokumentów z plikami .beatproof trafią do magazynu dowodów w katalogu kopii.':
        'Sigelith 证据：盖戳历史记录，以及已盖戳文档的精确副本及其 .beatproof 文件，将存入备份文件夹中的证据存储区。',
    'Dowody Sigelith: zabezpieczone dokumenty {count} z {total}':
        'Sigelith 证据：已妥善保存的文档 {count}/{total}',
    'Dowody Sigelith…':
        'Sigelith 证据…',
    'Dowody z problemem: {count} — szczegóły w kolumnie „Stan”.':
        '有问题的证明：{count}——详情见“状态”列。',
    'Dowodów Sigelith nie udało się zabezpieczyć: {error}':
        '无法妥善保存 Sigelith 证据：{error}',
    "Droga w drzewie Merkle'a nie prowadzi do podpisanego korzenia tygodnia.":
        'Merkle 树中的路径没有通向该周已签名的根。',
    'Gdzie zapisać dokumenty i dowody':
        '文档和证明保存到哪里',
    'Historia stempli Sigelith Desktop i dokładne bajty oznakowanych dokumentów, z plikami .beatproof — w osobnym magazynie, którego retencja nie sprząta.':
        'Sigelith Desktop 的盖戳历史记录，以及已盖戳文档的原始字节和 .beatproof 文件——保存在单独的存储区中，保留策略永远不会清理它。',
    'Każdy stempel ma tu swój folder z dokładnie tym dokumentem, który oznakowano, i plikiem .beatproof. „Sprawdź” liczy sumę każdego dokumentu i sprawdza podpis tygodnia bez łączenia się z siecią.':
        '每个戳记在这里都有自己的文件夹，其中存放着被盖戳的那份文档原件及其 .beatproof 文件。“检查”会计算每份文档的校验和，并在不联网的情况下核验周签名。',
    'Kopia obejmie folder danych Sigelith Desktop (historię stempli), a każdy oznakowany\ndokument trafi — dokładnie w tej postaci, którą oznakowano — do magazynu dowodów\nw katalogu kopii, razem z plikiem .beatproof. Starych wersji magazyn nie dotyczy:\nretencja go nie sprząta.':
        '备份将包含 Sigelith Desktop 的数据文件夹（盖戳历史记录），每份已盖戳的\n文档都会按盖戳时的原样，连同其 .beatproof 文件一起存入备份文件夹中的\n证据存储区。该存储区独立于旧版本：\n保留策略永远不会清理它。',
    'Magazyn dowodów jest pusty.':
        '证据存储区为空。',
    'Na tym komputerze jest Sigelith Desktop: {count} {stamps}.':
        '此电脑上装有 Sigelith Desktop：{count} {stamps}。',
    'Na tym komputerze nie ma danych Sigelith Desktop.':
        '此电脑上没有 Sigelith Desktop 的数据。',
    'Otwórz folder dowodów':
        '打开证据文件夹',
    'Oznakowano':
        '盖戳时间',
    'Pokazuje magazyn dowodów w Eksploratorze':
        '在文件资源管理器中显示证据存储区',
    'Przywróć zaznaczone…':
        '恢复所选项…',
    'Sigelith Desktop: {count} {stamps} w folderze {path}.':
        'Sigelith Desktop：{count} {stamps}，位于文件夹 {path}。',
    'Sprawdza każdy dokument i jego dowód bez łączenia z siecią':
        '在不联网的情况下检查每份文档及其证明',
    'Sprawdzam dowody…':
        '正在检查证明…',
    'Stan':
        '状态',
    'Stemple w magazynie: {count}, z dokumentem: {documents}.':
        '存储区中的戳记：{count}，其中附有文档的：{documents}。',
    'Suma dokumentu nie zgadza się z dowodem.':
        '文档的校验和与证明不符。',
    'To nie jest plik dowodu Sigelith (beatproof-v1).':
        '这不是 Sigelith 证明文件（beatproof-v1）。',
    'Tydzień stempla jeszcze się nie zamknął — podpis dojdzie przy kolejnej kopii.':
        '戳记所在的周尚未结束——签名将在之后的备份中补上。',
    'W magazynie nie ma dokumentu do tego dowodu.':
        '存储区中没有与此证明对应的文档。',
    'Wszystkie dowody pasują do dokumentów i mają poprawny podpis.':
        '所有证明都与其文档相符，且签名有效。',
    'Zabezpieczam dokumenty oznakowane w Sigelith…':
        '正在妥善保存用 Sigelith 盖戳的文档…',
    'Zapisano pliki: {count} w {path}.':
        '已保存文件：{count}，位于 {path}。',
    'Zapisuje dokumenty razem z plikami .beatproof we wskazanym folderze':
        '将文档连同其 .beatproof 文件保存到你指定的文件夹',
    'bez dokumentu — dowód zachowany':
        '无文档——证明已保留',
    'czekają na podpis tygodnia: {count}':
        '正在等待周签名：{count}',
    'dokument i dowód są w kopii':
        '文档和证明都在备份中',
    'dokument jest; dowód czeka na podpis tygodnia':
        '文档已在；证明正在等待周签名',
    'dowodu nie da się odczytać':
        '无法读取证明',
    'dowody Sigelith':
        'Sigelith 证据',
    'dowody uzupełnione o podpis tygodnia: {count}':
        '已补上周签名的证明：{count}',
    'nowe: {count}':
        '新增：{count}',
    'odtworzone ze starszych wersji kopii: {count}':
        '从较早的备份版本中找回：{count}',
    'sprawdzony: dokument i dowód się zgadzają':
        '已检查：文档与证明相符',
    'stempel':
        '个戳记',
    'stemple':
        '个戳记',
    'stempli':
        '个戳记',
    'zaszyfrowany — podaj hasło, żeby sprawdzić':
        '已加密——请输入密码以检查',
    'Chroń dowody Sigelith, gdy go zainstaluję':
        '在我安装 Sigelith Desktop 后保护 Sigelith 证据',
    'Dowody Sigelith: na tym komputerze nie ma jeszcze Sigelith Desktop — ochrona zacznie działać sama, gdy się pojawi.':
        'Sigelith 证据：此电脑上还没有 Sigelith Desktop——一旦安装，保护功能会自动开始工作。',
    'Dowody Sigelith: ochrona zacznie działać sama, gdy zainstalujesz Sigelith Desktop.':
        'Sigelith 证据：安装 Sigelith Desktop 后，保护功能会自动开始工作。',
    'Dowody czasu dla ważnych dokumentów':
        '为重要文档提供时间证明',
    'Kopia zachowa każdy dokument oznakowany w Sigelith Desktop dokładnie w tej postaci, którą oznakowano, razem z dowodem — nawet gdy oryginał później się zmieni.':
        '备份会按盖戳时的原样，保存每份用 Sigelith Desktop 盖过戳的文档及其证明——即使原件之后发生了更改。',
    'Ochrona zacznie działać sama, gdy na komputerze pojawi się Sigelith Desktop.':
        '一旦电脑上安装了 Sigelith Desktop，保护功能会自动开始工作。',
    'Otwiera stronę programu Sigelith Desktop':
        '打开 Sigelith Desktop 的介绍页面',
    'Poznaj Sigelith Desktop':
        '了解 Sigelith Desktop',
    'Sigelith Desktop, program tego samego wydawcy, oznakuje dokument czasem: to podpisany dowód, że plik w tej postaci istniał w danej chwili, sprawdzalny bez udziału kogokolwiek. Sigelith Backup przechowa potem każdy oznakowany dokument razem z dowodem.':
        'Sigelith Desktop 是同一发行者的程序，可以为文档加盖时间戳：这是一份经过签名的证明，证明该文件在某一时刻就以这种形式存在，无需依赖任何人即可核验。之后，Sigelith Backup 会把每份已盖戳的文档连同其证明一起保存。',
    'Umowy, faktury, projekty — czasem trzeba wykazać, że dokument istniał danego dnia.':
        '合同、发票、项目——有时需要证明某份文档在某一天就已存在。',
    'Nieznany format spisu wersji.':
        '未知的版本清单格式。',
    'Ta wersja nie ma pieczęci dla pojedynczych plików (kopia sprzed wersji 3.0 albo bez znaczników czasu).':
        '此版本没有针对单个文件的封印（备份创建于 3.0 版之前，或未使用时间戳）。',
    'Pieczęć tej wersji czeka jeszcze na podpis tygodnia Sigelith — dowód będzie gotowy po poniedziałku 00:00 UTC i kolejnej kopii.':
        '此版本的封印仍在等待 Sigelith 周签名——证明将在周一 00:00 UTC 之后、下一次备份完成时就绪。',
    'Brak oświadczenia pieczęci w folderze wersji.':
        '版本文件夹中缺少封印声明。',
    'Oświadczenie pieczęci nie zgadza się z pieczęcią wersji.':
        '封印声明与版本的封印不符。',
    'Drzewo plików wersji nie zgadza się z pieczęcią.':
        '版本的文件树与封印不符。',
    'Tego pliku nie ma w spisie tej wersji.':
        '此文件不在该版本的清单中。',
    'To nie jest dowód pliku z kopii Sigelith Backup ({format}).':
        '这不是 Sigelith Backup 的文件证明（{format}）。',
    'Dowód jest uszkodzony — brakuje pól albo mają zły format.':
        '证明已损坏——缺少字段或字段格式错误。',
    'Ten plik nie jest plikiem, którego dotyczy dowód.':
        '此文件不是该证明所针对的文件。',
    'Ścieżka pliku w dowodzie nie zgadza się z liściem drzewa.':
        '证明中的文件路径与树的叶子不一致。',
    'Droga w drzewie plików nie prowadzi do korzenia z pieczęci.':
        '文件树中的路径没有通向已封印的根。',
    'Oświadczenie pieczęci nie potwierdza tego drzewa plików.':
        '封印声明没有确认这棵文件树。',
    'Potwierdzenie Sigelith nie dotyczy tej pieczęci.':
        'Sigelith 的确认不属于此封印。',
    'Dowód czasu…':
        '时间证明…',
    'Zapisuje dowód, że ten plik był w kopii w chwili jej oznakowania — bez ujawniania innych plików':
        '保存一份证明，证明此文件在备份加盖时间戳时就在备份中——不会透露其他文件',
    'Dowód czasu':
        '时间证明',
    'Dołączyć do dowodu ścieżkę pliku w kopii („{path}”)?\n\nBez niej dowód dalej potwierdza plik i chwilę oznakowania, ale nie mówi, gdzie plik leżał.':
        '要在证明中包含该文件在备份中的路径（“{path}”）吗？\n\n不包含路径时，证明仍能确认该文件和加盖时间戳的时刻，但不会说明文件存放在哪里。',
    'Przygotowuję dowód dla „{name}”…':
        '正在为“{name}”准备证明…',
    'Zapisz dowód czasu':
        '保存时间证明',
    'Dowód pliku Sigelith (*{suffix})':
        'Sigelith 文件证明 (*{suffix})',
    'Zapisano dowód i certyfikat PDF: {path}. Sprawdzi go Sigelith Desktop albo strona sigelith.org/verify/.':
        '已保存证明和 PDF 证书：{path}。可用 Sigelith Desktop 或 sigelith.org/verify/ 页面检查。',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją sprawdzić.':
        '备份已加密——请输入密码以进行检查。',
    'Ta wersja nie ma pieczęci — nie ma z czym porównać plików.':
        '此版本没有封印——无从比对文件。',
    'Pieczęć wersji się nie potwierdza: {problems}':
        '版本的封印未通过核验：{problems}',
    'brak podpisu tygodnia':
        '缺少周签名',
    'Audyt przerwany.':
        '审计已取消。',
    'próbka {checked} z {listed} plików':
        '从 {listed} 个文件中抽查的 {checked} 个',
    'wszystkie pliki ({count})':
        '全部 {count} 个文件',
    'Nietknięta: sprawdzono {scope}, wszystko zgodne z pieczęcią w publicznym dzienniku.':
        '完好：已检查{scope}，均与公开日志中的封印相符。',
    'zmienione: {files}':
        '已更改：{files}',
    'brakujące: {files}':
        '缺失：{files}',
    'nieczytelne albo uszkodzone: {files}':
        '无法读取或已损坏：{files}',
    'PODMIENIONA albo uszkodzona ({scope}) — {details}.':
        '已被调包或已损坏（{scope}）——{details}。',
    'Audyt treści':
        '内容审计',
    'Czyta z nośnika każdy plik tej wersji i porównuje go z sumą oznakowaną w publicznym dzienniku':
        '从存储介质读取此版本的每个文件，并与封印在公开日志中的校验和比对',
    'Ostatnia nietknięta':
        '最近完好版本',
    'Sprawdza wersje od najnowszej i wskazuje ostatnią zgodną z pieczęcią — z niej przywracaj':
        '从最新版本开始检查，找出最近一个与封印相符的版本——请从它恢复',
    'Ostatnia nietknięta wersja: {label} — z niej przywracaj.':
        '最近完好的版本：{label}——请从它恢复。',
    'Żadna wersja z pieczęcią nie jest nietknięta.':
        '没有一个带封印的版本是完好的。',
    'Czytam pliki kopii i porównuję je z pieczęcią w publicznym dzienniku…':
        '正在读取备份文件，并与公开日志中的封印比对…',
    'Sprawdzam próbkę starszej wersji z pieczęcią w publicznym dzienniku…':
        '正在对照公开日志中的封印，抽查一个较早的版本…',
    'Audyt z pieczęcią: próbka wersji {label} zgodna z publicznym dziennikiem.':
        '封印审计：版本 {label} 的抽查样本与公开日志相符。',
    'UWAGA — audyt z pieczęcią, wersja {label}: {details}':
        '警告——封印审计，版本 {label}：{details}',
    'Przekaż…':
        '交付…',
    'Zapisuje tę wersję pliku i otwiera ją w Sigelith Handover — odbiorca potwierdzi odbiór własnym kluczem':
        '保存此版本的文件，并在 Sigelith Handover 中打开——接收方会用自己的密钥确认收到',
    'Przekazanie z dowodem doręczenia':
        '带交付证明地交付',
    'Przekazanie z dowodem doręczenia robi Sigelith Desktop (od wersji 3.0.1): odbiorca potwierdza odbiór własnym kluczem, a chwila doręczenia trafia do publicznego dziennika. Na tym komputerze go nie ma albo jest w starszej wersji. Otworzyć stronę programu?':
        '带交付证明的交付由 Sigelith Desktop（3.0.1 及以上版本）完成：接收方用自己的密钥确认收到，交付时刻会记入公开日志。此电脑上没有安装它，或者安装的是旧版本。要打开该程序的页面吗？',
    'Zapisz plik do przekazania':
        '保存要交付的文件',
    'Otwieram Sigelith Handover z plikiem „{name}” — wybierz odbiorcę.':
        '正在用文件“{name}”打开 Sigelith Handover——请选择接收方。',
    'Kapsuły czasu…':
        '时间胶囊…',
    'Pliki zapieczętowane w tej kopii do daty — klucze wydają dopiero po niej sieć drand i serwer kluczy Sigelith':
        '在此备份中封存到某个日期的文件——drand 网络和 Sigelith 密钥服务器只在该日期之后才释放密钥',
    'Wskaż najpierw folder kopii — kapsuła leży w kopii.':
        '请先指定备份文件夹——胶囊保存在备份中。',
    'Kapsuły czasu':
        '时间胶囊',
    'Kapsuła pieczętuje wybrany folder do chwili, którą wskażesz. Otwierają ją dowolne dwie z trzech części: runda sieci drand z tej chwili, udział serwera kluczy Sigelith (wydawany dopiero po tej chwili — to zasada operatora, nie kryptografia) i kod odzyskiwania zapisany obok kapsuły. Kto ma tę kopię, ma więc i kod: do wcześniejszego otwarcia wystarczy mu, że operator złamie swoją zasadę. Po tej chwili otworzy ją każdy, kto ma jej pliki. Kapsuła leży w tej kopii, nie na serwerze; otwiera ją strona sigelith.org/capsule/.':
        '胶囊会把所选文件夹封存到你指定的时刻。三部分中的任意两部分即可打开它：drand 网络在该时刻的轮次、Sigelith 密钥服务器的份额（只在该时刻之后才释放——这是运营方的规则，而不是密码学上的限制），以及保存在胶囊旁边的恢复码。因此，持有这份备份的人也持有恢复码：只要运营方违反自己的规则，他就能提前打开。过了该时刻，任何拥有胶囊文件的人都能打开它。胶囊保存在这份备份中，而不是服务器上；可在 sigelith.org/capsule/ 页面打开。',
    'Wybierz kapsułę z listy albo utwórz nową.':
        '请从列表中选择一个胶囊，或新建一个。',
    'Nowa kapsuła…':
        '新建胶囊…',
    'Pieczętuje wybrany folder do daty':
        '将所选文件夹封存到某个日期',
    'Pokaż w folderze':
        '在文件夹中显示',
    'Otwiera folder kapsuły w Eksploratorze':
        '在文件资源管理器中打开胶囊文件夹',
    'Otwórz na stronie':
        '在网站上打开',
    'Strona sigelith.org/capsule/ otwiera kapsułę po jej dacie':
        '过了日期后，可在 sigelith.org/capsule/ 页面打开胶囊',
    'można otworzyć':
        '可以打开',
    'zamknięta':
        '已封存',
    'W tej kopii nie ma jeszcze kapsuł czasu.':
        '此备份中还没有时间胶囊。',
    'Ta kapsuła da się otworzyć na stronie sigelith.org/capsule/ — wskaż jej pliki.':
        '这个胶囊可以在 sigelith.org/capsule/ 页面打开——请在那里选择它的文件。',
    'Kapsuła jest zamknięta do daty z listy. Kod odzyskiwania leży w pliku obok niej.':
        '胶囊封存至列表中的日期。恢复码保存在它旁边的文件中。',
    'Wybierz folder do zapieczętowania':
        '选择要封存的文件夹',
    'Pieczętuję „{name}” — kilka sekund na krzywej eliptycznej…':
        '正在封存“{name}”——在椭圆曲线上计算需要几秒钟…',
    'kapsuła czasu':
        '时间胶囊',
    'Kapsuła zapieczętowana':
        '胶囊已封存',
    '„{name}” otworzy się najwcześniej {when}.\n\nKod odzyskiwania (skopiowany do schowka, zapisany też obok kapsuły):\n\n{code}\n\nZapisz go w bezpiecznym miejscu. Przed datą otwarcia sam niczego nie otwiera; po niej zastępuje jeden z kluczy, gdyby był niedostępny.':
        '“{name}”最早将于 {when} 打开。\n\n恢复码（已复制到剪贴板，并已保存在胶囊旁边）：\n\n{code}\n\n请把它保存在安全的地方。在打开日期之前，单凭它打不开任何东西；过了该日期，若某把密钥不可用，它可以替代其中一把。',
    'Nie udało się zapieczętować: {error}':
        '封存失败：{error}',
    'Nowa kapsuła czasu':
        '新建时间胶囊',
    'Otworzy się najwcześniej':
        '最早打开时间',
    'kapsuła':
        '胶囊',
    'Chwila otwarcia musi być w przyszłości.':
        '打开时刻必须在将来。',
    'Na bieżąco':
        '实时',
    'Zmiany w folderach źródłowych trafiają do dzisiejszej wersji kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje. Jedna wersja na dzień; ze znacznikami czasu zamyka ją pieczęć następnego dnia.':
        '源文件夹中的更改会在保存几分钟后写入当天的备份版本；连接驱动器后，备份会立即同步。每天一个版本；启用时间戳时，次日会为该版本加上封印，将其关闭。',
    'Na bieżąco — po każdej zmianie i po podłączeniu dysku':
        '实时——每次更改后以及连接驱动器时',
    'Dla dysku podłączonego na stałe albo często: zmiany trafiają do kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje.':
        '适用于一直或经常连接的驱动器：更改会在保存几分钟后写入备份；连接驱动器后，备份会立即同步。',
    'Kopia będzie na bieżąco: zmiany trafią do dzisiejszej wersji kilka minut po zapisie, a po podłączeniu dysku kopia od razu się zsynchronizuje.':
        '备份将实时更新：更改会在保存几分钟后写入当天的版本；连接驱动器后，备份会立即同步。',
    'przywracanie':
        '恢复',
}
