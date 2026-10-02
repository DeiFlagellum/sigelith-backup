"""Katalog japoński: „polski tekst źródłowy” → „tekst (japoński)”.

Klucze są te same co w ``en.py`` i muszą dokładnie odpowiadać napisom w kodzie;
pilnuje tego ``tests/test_i18n.py``. Pola w nawiasach klamrowych (``{count}``)
zostają bez zmian. Formaty dat są te same co w Sigelith Desktop.
"""

from __future__ import annotations

TEXTS: dict[str, str] = {
    '\n\nLokalizacja:\n{path}':
        '\n\n場所：\n{path}',
    '\nDo uzupełnienia: niedokończone kopie: {count} — możesz je uzupełnić, wybierając wersję poniżej.':
        '\n補完が必要：未完了のバックアップが {count} 件あります — 下でバージョンを選ぶと補完できます。',
    '\nUwaga: duży klaster ({size}): każdy mały plik zajmuje co najmniej tyle miejsca. Przy wielu małych plikach kopia zajmie wielokrotnie więcej niż dane.':
        '\n注意：クラスターが大きいため（{size}）、小さなファイルでも 1 つにつき少なくともこの容量を使います。小さなファイルが多いと、バックアップはデータ自体の何倍もの容量を使います。',
    '\nUwaga: niedokończone wersje (nie zawierają wszystkich plików): {names}':
        '\n注意：未完了のバージョン（すべてのファイルを含んでいません）：{names}',
    '\nUwaga: {filesystem} nie obsługuje twardych dowiązań — każda wersja z datą zajmuje tyle miejsca co pełna kopia.':
        '\n注意：{filesystem} はハードリンクに対応していません — 日付付きバージョンはそれぞれ完全なバックアップと同じ容量を使います。',
    ' wersji':
        ' 個',
    ' z szyfrowaniem AES-256-GCM…':
        ' — AES-256-GCM で暗号化…',
    ' ×':
        ' 回',
    ' — a ponieważ {filesystem} nie obsługuje twardych dowiązań, zapisze ponownie wszystkie pliki i zajmie tyle miejsca co cała kopia':
        ' — また、{filesystem} はハードリンクに対応していないため、すべてのファイルを再び書き込み、バックアップ全体と同じ容量を使います',
    ' • pozostało {time}':
        ' • 残り {time}',
    '%d.%m %H:%M':
        '%m/%d %H:%M',
    '%d.%m.%Y':
        '%Y/%m/%d',
    '%d.%m.%Y %H:%M':
        '%Y/%m/%d %H:%M',
    ', klaster {size}':
        '、クラスター {size}',
    ', uzupełniona {when}':
        '、{when} に補完',
    'Analizuje pliki i pokazuje plan. Nic nie zapisuje.':
        'ファイルを分析して計画を表示します。何も書き込みません。',
    'Anulowano przed rozpoczęciem kopii.':
        'バックアップの開始前にキャンセルしました。',
    'Anuluj':
        'キャンセル',
    'Argon2id (t={passes}, {memory} MiB, p={threads})':
        'Argon2id（t={passes}、{memory} MiB、p={threads}）',
    'Argon2id — {passes} przebiegi, {memory} MiB, {threads} wątki':
        'Argon2id — 反復 {passes} 回、{memory} MiB、{threads} スレッド',
    'Automatycznie (język systemu)':
        '自動（システムの言語）',
    'Bardzo dobre':
        '非常に強い',
    'Bardzo słabe':
        '非常に弱い',
    'Brak manifestu — skanuję katalog kopii.':
        'マニフェストがありません — バックアップフォルダーをスキャンしています。',
    'Brakuje tagu uwierzytelniającego — plik jest obcięty.':
        '認証タグがありません — ファイルが途中で切れています。',
    'Błąd uruchamiania':
        '起動エラー',
    'Ciemny':
        'ダーク',
    'Co dokładnie zostanie zapisane przy najbliższym przebiegu.':
        '次回の実行で書き込まれる内容の詳細。',
    'Co kopiujemy':
        'バックアップの対象',
    'Co zrobić, gdy plik o tej nazwie już istnieje w katalogu docelowym.':
        '復元先フォルダーに同じ名前のファイルがすでにある場合の処理。',
    'Czas w nazwie to BeatTime — 1000 beatów na dobę, kotwica w UTC, ten sam moment na całym świecie. Data jest datą UTC, więc zgadza się z zegarem.':
        '名前に含まれる時刻は BeatTime です — 1 日 1000 ビート、UTC 基準で、世界中どこでも同じ瞬間を表します。日付も UTC の日付なので、BeatTime の時計と一致します。',
    'Czym jest {app}':
        '{app} とは',
    'Czyści tylko okno — plik dziennika pozostaje':
        'ウィンドウの表示だけを消去します — ログファイルは残ります',
    'Dane aplikacji: {path}':
        'アプリのデータ：{path}',
    'Decyduje, czy zachowujemy historię wersji.':
        'バージョン履歴を残すかどうかを決めます。',
    'Dobre':
        '強い',
    'Dodaj folder':
        'フォルダーを追加',
    'Dodaj przynajmniej jeden folder źródłowy.':
        'バックアップ元のフォルダーを少なくとも 1 つ追加してください。',
    'Dogrywka zmian z czasu kopii:':
        'バックアップ中の変更の追加取り込み：',
    'Dokąd przywracamy':
        '復元先',
    'Dokładnie to, co program realnie stosuje.':
        'プログラムが実際に使っている方式そのものです。',
    'Domyślne wykluczenia':
        '既定の除外',
    'Domyślne wykluczenia zapisane.':
        '既定の除外を保存しました。',
    'Domyślnie wyłączone. Przy włączonej opcji skasowanie pliku w źródle\nusuwa też jego jedyną kopię zapasową — operacja nieodwracalna.':
        '既定ではオフです。オンにすると、バックアップ元でファイルを削除したときに\nそのファイルの唯一のバックアップも削除されます — 元に戻せません。',
    'Dopisuj do nazwy katalogu datę ostatniego uzupełnienia':
        'フォルダー名に最後に補完した日付を追加する',
    'Dziennik':
        'ログ',
    'Dziennik: {path}':
        'ログ：{path}',
    'Ekran przywracania wypełniony danymi szablonu.':
        'テンプレートの内容を復元画面に入力しました。',
    'Folder docelowy kopii — najlepiej na innym dysku fizycznym.':
        'バックアップ先のフォルダー — できれば別の物理ドライブ上に。',
    'Folder zawierający kopię utworzoną przez {app}.':
        '{app} で作成したバックアップが入っているフォルダー。',
    'Gdy plik już istnieje:':
        'ファイルがすでにある場合：',
    'Gdzie zapisujemy':
        'バックアップ先',
    'Gotowe do pracy.':
        '準備ができました。',
    'Gotowe. Wybierz foldery do kopii.':
        '準備ができました。バックアップするフォルダーを選んでください。',
    'Gotowe: {count} {files}, {size}, {seconds} s.':
        '完了：{count} 個の{files}、{size}、{seconds} 秒。',
    'Główny folder kopii. Zawiera spis treści (.cleanvault-manifest).':
        'バックアップのメインフォルダーです。目次（.cleanvault-manifest）が入っています。',
    'Hasła nie da się odzyskać ani zresetować. Jeśli je zgubisz, dane z kopii zaszyfrowanej są bezpowrotnie stracone — tak działa poprawne szyfrowanie.':
        'パスワードは復旧もリセットもできません。紛失すると、暗号化したバックアップのデータは永久に失われます — 正しい暗号化とはそういうものです。',
    'Hasła w obu polach różnią się.':
        '2 つの欄のパスワードが一致しません。',
    'Hasło':
        'パスワード',
    'Hasło do kopii':
        'バックアップのパスワード',
    'Hasło nie jest nigdzie zapisywane w postaci jawnej.\nBez niego nie da się odzyskać danych — nie istnieje żadna furtka serwisowa.':
        'パスワードが平文でどこかに保存されることはありません。\nパスワードがなければデータは復旧できません — 裏口は一切ありません。',
    'Hasło nie może być puste.':
        'パスワードを空にすることはできません。',
    'Hasło niezapisane':
        'パスワードは保存されていません',
    'Hasło powinno mieć co najmniej 8 znaków.':
        'パスワードは 8 文字以上にしてください。',
    'Hasło trafia do magazynu systemowego powiązanego z Twoim kontem.\nNigdy nie jest zapisywane w plikach programu.':
        'パスワードは、あなたのアカウントに紐づいたシステムの保管場所に保存されます。\nプログラムのファイルに書き込まれることはありません。',
    'Hasło użyte przy tworzeniu kopii':
        'バックアップの作成時に使ったパスワード',
    'Ile plików kopia przetwarza jednocześnie. Przy setkach tysięcy małych plików\nczas kopii to głównie opóźnienia na każdy plik (otwarcie, skanowanie\nantywirusowe, zapis na nośnik), a nie przesył danych — praca równoległa\nskraca go kilkukrotnie.\n\n„automatycznie” dobiera liczbę do procesora (do 32). Na wolnym dysku\ntalerzowym mniejsza wartość (2–4) bywa szybsza.':
        'バックアップで同時に処理するファイルの数です。小さなファイルが数十万個あると、\nかかる時間の大半はデータの転送ではなく、ファイルごとの待ち時間\n（オープン、ウイルススキャン、メディアへの書き込み）です。並列処理で\nこの時間を数分の一に短縮できます。\n\n「自動」はプロセッサーに合わせて数を決めます（最大 32）。低速な\nハードディスクでは、小さい値（2～4）のほうが速いこともあります。',
    'Informacje przydatne przy zgłaszaniu problemu.':
        '問題を報告するときに役立つ情報です。',
    'Jak to działa':
        '仕組み',
    'Jasny':
        'ライト',
    'Jeden folder utrzymywany w zgodzie ze źródłem. Brak historii wersji,\nza to najprostsza struktura i najmniejsze zużycie miejsca.':
        'バックアップ元と常に一致させる 1 つのフォルダーです。バージョン履歴はありませんが、\n構造が最も単純で、使う容量も最小です。',
    'Jeśli operacja zakończy się błędem, skopiuj stąd ostatnie wiersze — zawierają dokładną przyczynę, a nie tylko komunikat ogólny.':
        '操作がエラーで終わったときは、ここから最後の数行をコピーしてください — 一般的なメッセージだけでなく、正確な原因が記録されています。',
    'Język interfejsu zmieniony.':
        '表示言語を変更しました。',
    'Język zmienisz po zakończeniu bieżącej operacji.':
        '言語は、現在の操作が終わってから変更できます。',
    'Język:':
        '言語：',
    'Katalog docelowy leży wewnątrz źródła ({path}). Kopia kopiowałaby samą siebie w nieskończoność.':
        'バックアップ先フォルダーがバックアップ元（{path}）の中にあります。バックアップが自分自身を際限なくコピーしてしまいます。',
    'Katalog docelowy nie może być tym samym katalogiem co źródłowy.':
        'バックアップ先フォルダーをバックアップ元フォルダーと同じにすることはできません。',
    'Katalog jeszcze nie istnieje — zostanie utworzony.':
        'フォルダーはまだありません — 作成されます。',
    'Katalog kopii nie istnieje: {path}':
        'バックアップフォルダーが存在しません：{path}',
    'Katalog źródłowy nie istnieje: {path}':
        'バックアップ元フォルダーが存在しません：{path}',
    'Katalog, w którym pojawią się odtworzone pliki.':
        '復元したファイルが保存されるフォルダー。',
    'Katalog, w którym powstanie kopia. Nie może leżeć wewnątrz folderu źródłowego.':
        'バックアップを作成するフォルダーです。バックアップ元フォルダーの中には置けません。',
    'Katalogi objęte kopią.\nMożesz przeciągnąć foldery z Eksploratora Windows wprost na tę listę.':
        'バックアップの対象フォルダーです。\nエクスプローラーからフォルダーをこの一覧に直接ドラッグできます。',
    'Każdy folder z datą jest kompletny — przywracanie nie wymaga sklejania wersji.':
        '日付付きの各フォルダーはそれだけで完結しています — 復元のためにバージョンをつなぎ合わせる必要はありません。',
    'Każdy plik jest czytany ponownie zaraz po zapisaniu. Dane pochodzą wtedy\nzwykle z pamięci podręcznej systemu, więc niewiele mówi to o nośniku,\na wydłuża kopię nawet dwukrotnie.\n\nSkuteczniejsza jest weryfikacja odroczona: ekran „Przywracanie” →\n„Sprawdź kopię”, najlepiej po ponownym podłączeniu dysku.':
        '各ファイルを書き込んだ直後に読み直します。このときデータは通常\nシステムのキャッシュから読まれるため、メディアの状態はほとんどわからず、\nバックアップの時間が最大で 2 倍になります。\n\n後から検証するほうが効果的です：「復元」画面 →\n「バックアップを検証」。できればドライブを接続し直してから行ってください。',
    'Każdy plik trafia do kopii jako zaszyfrowany kontener .cvlt.\nKlucz powstaje z hasła przez Argon2id.':
        '各ファイルは暗号化された .cvlt コンテナーとしてバックアップに保存されます。\n鍵は Argon2id でパスワードから導出されます。',
    'Każdy przebieg tworzy osobny folder z datą i godziną.\nPliki niezmienione są podpinane twardym dowiązaniem, więc historia\nzajmuje tyle miejsca, ile realnie się zmieniło.':
        '実行するたびに、日付と時刻の付いたフォルダーが新しく作られます。\n変更のないファイルはハードリンクでつながれるため、履歴が使う容量は\n実際に変更された分だけです。',
    'Klaster nośnika to {cluster} — pliki zajmą {actual} zamiast {logical} (narzut {overhead}).':
        'メディアのクラスターは {cluster} です — ファイルは {logical} ではなく {actual} を使います（オーバーヘッド {overhead}）。',
    'Kliknij szablon, aby zobaczyć jego szczegóły.':
        'テンプレートをクリックすると詳細が表示されます。',
    'Kliknij „Podgląd zmian”, aby sprawdzić plan bez zapisywania czegokolwiek.':
        '「変更のプレビュー」をクリックすると、何も書き込まずに計画を確認できます。',
    'Kolor wyróżnienia':
        'アクセントカラー',
    'Kolor wyróżnienia…':
        'アクセントカラー…',
    'Kopia':
        'バックアップ',
    'Kopia do dokończenia':
        '未完了のバックアップ',
    'Kopia jest aktualna — nie ma czego zapisywać.':
        'バックアップは最新です — 書き込むものはありません。',
    'Kopia jest zaszyfrowana — podaj hasło użyte przy jej tworzeniu.':
        'バックアップは暗号化されています — 作成時に使ったパスワードを入力してください。',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją przywrócić.':
        'バックアップは暗号化されています — 復元するにはパスワードを入力してください。',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją zweryfikować.':
        'バックアップは暗号化されています — 検証するにはパスワードを入力してください。',
    'Kopia jest zaszyfrowana — podaj hasło.':
        'バックアップは暗号化されています — パスワードを入力してください。',
    'Kopia lustrzana':
        'ミラーコピー',
    'Kopia nie została uruchomiona.':
        'バックアップは開始されませんでした。',
    'Kopia wykonana. Uruchom podgląd ponownie, aby sprawdzić stan.':
        'バックアップが完了しました。状態を確認するには、もう一度プレビューを実行してください。',
    'Kopia zapasowa':
        'バックアップ',
    'Kopia {folder}':
        '{folder} のバックアップ',
    'Kopia {kind} • {count} {files} • {size} • ostatnia aktualizacja {when}\nŹródła: {roots}':
        '{kind}のバックアップ • {count} 個の{files} • {size} • 最終更新 {when}\nバックアップ元：{roots}',
    'Kopiowane są wyłącznie pliki nowe i zmienione od ostatniego przebiegu.':
        '前回の実行以降に追加・変更されたファイルだけがコピーされます。',
    'Kopiuje ustawienia szablonu na ekran „Kopia zapasowa”':
        'テンプレートの設定を「バックアップ」画面にコピーします',
    'Kopię możesz sprawdzić później: ekran „Przywracanie” → „Sprawdź kopię”. Najlepiej po ponownym podłączeniu dysku — wtedy dane są czytane z nośnika.':
        'バックアップは後から検証できます：「復元」画面 →「バックアップを検証」。できればドライブを接続し直してから行ってください — そうすればデータが実際にメディアから読み込まれます。',
    'Kryptografia':
        '暗号技術',
    'Lista podpowiadana przy tworzeniu nowej kopii.':
        '新しいバックアップを設定するときに提案される一覧です。',
    'Magazyn haseł: {backend}':
        'パスワードの保管場所：{backend}',
    'Magazyn systemowy: {backend}':
        'システムの保管場所：{backend}',
    'Menedżer poświadczeń Windows (DPAPI, powiązany z kontem użytkownika).':
        'Windows 資格情報マネージャー（DPAPI、ユーザーアカウントに紐づけ）。',
    'Miejsce i układ odtwarzanych plików.':
        '復元するファイルの保存先と配置。',
    'Motyw zmieniony na {theme}.':
        'テーマを{theme}に変更しました。',
    'Motyw:':
        'テーマ：',
    'Możesz też przeciągnąć foldery z Eksploratora Windows wprost na listę.':
        'エクスプローラーからフォルダーを一覧に直接ドラッグすることもできます。',
    'Można ją dokończyć — zostaną dograne tylko brakujące i zmienione pliki.':
        'このバックアップは完了させることができます — 足りないファイルと変更されたファイルだけが追加されます。',
    'Na nośniku docelowym zajmie to ok. {size}.':
        '保存先のメディアでは約 {size} を使います。',
    'Nadpisywanie plików':
        'ファイルの上書き',
    'Nadpisz istniejące pliki':
        '既存のファイルを上書き',
    'Nazwa szablonu':
        'テンプレート名',
    'Nazwa szablonu nie może być pusta.':
        'テンプレート名を空にすることはできません。',
    'Nazwa szablonu zapisana.':
        'テンプレート名を保存しました。',
    'Nazwa szablonu:':
        'テンプレート名：',
    'Nie ma wersji kopii o nazwie {name} w katalogu {path}.':
        'フォルダー {path} に、{name} という名前のバックアップバージョンはありません。',
    'Nie można odczytać informacji o dysku: {error}':
        'ドライブの情報を読み取れません：{error}',
    'Nie udało się uruchomić programu — brakuje biblioteki: {error}\nZainstaluj zależności poleceniem:  pip install -r requirements.txt':
        'プログラムを起動できませんでした — ライブラリがありません：{error}\n次のコマンドで依存関係をインストールしてください：  pip install -r requirements.txt',
    'Nie udało się wykonać operacji':
        '操作を完了できませんでした',
    'Nie udało się zapisać hasła w magazynie systemowym.\nSzablon działa normalnie — program poprosi o hasło przy uruchomieniu.':
        'パスワードをシステムの保管場所に保存できませんでした。\nテンプレートは通常どおり使えます — 実行時にパスワードの入力を求めます。',
    'Nie udało się znaleźć wolnej nazwy dla {path}':
        '{path} に使える空いている名前が見つかりませんでした',
    'Nie wskazano katalogu docelowego.':
        'バックアップ先フォルダーが指定されていません。',
    'Nie wskazano żadnego katalogu źródłowego.':
        'バックアップ元フォルダーが指定されていません。',
    'Nie wybrano katalogu':
        'フォルダーが選択されていません',
    'Nie wybrano szablonu':
        'テンプレートが選択されていません',
    'Nie znaleziono spisu treści kopii — program przeskanuje folder i rozpozna pliki po ich zawartości.':
        'バックアップの目次が見つかりません — フォルダーをスキャンし、内容からファイルを判別します。',
    'Nie znam oryginalnej lokalizacji dla {key} — wybierz inny układ przywracania.':
        '{key} の元の場所がわかりません — 「ファイルの配置」で別の方法を選んでください。',
    'Niedostępny — backend {backend} nie gwarantuje poufności.':
        '使用不可 — バックエンド {backend} は機密性を保証しません。',
    'Niedostępny — brak biblioteki keyring.':
        '使用不可 — keyring ライブラリがありません。',
    'Nieznany algorytm wyprowadzania klucza: {name}':
        '不明な鍵導出アルゴリズム：{name}',
    'Nowa wersja z datą':
        '新しい日付付きバージョン',
    'Nowa wersja z datą to kopia od początku do osobnego folderu':
        '新しい日付付きバージョンでは、最初から別のフォルダーにバックアップします',
    'Nowa wersja z datą — kopia do nowego folderu.\nWybrana istniejąca wersja — dogrywa do niej tylko brakujące i zmienione\npliki, a pliki różniące się od źródła nadpisuje. Tak dokończysz przerwaną\nkopię albo uzupełnisz ją o dane, które powstały w trakcie jej wykonywania.':
        '新しい日付付きバージョン — 新しいフォルダーにバックアップします。\n既存のバージョンを選んだ場合 — 足りないファイルと変更されたファイルだけを追加し、\nバックアップ元と異なるファイルは上書きします。中断したバックアップを完了させたり、\nバックアップ中に作成されたデータを補ったりするときに使います。',
    'Nowy szablon':
        '新しいテンプレート',
    'Nośnik docelowy ({filesystem}) nie obsługuje twardych dowiązań, więc każda wersja z datą jest pełną kopią. Te {count} niezmienionych plików zostanie powielone ({size}). Rozważ układ „kopia lustrzana” albo nośnik NTFS.':
        '保存先のメディア（{filesystem}）はハードリンクに対応していないため、日付付きバージョンはそれぞれ完全なコピーになります。変更のない {count} 個のファイルが重複して保存されます（{size}）。「ミラーコピー」の構成か、NTFS のメディアを検討してください。',
    'O programie':
        'バージョン情報',
    'Obsługiwane są wzorce w stylu Windows:\n  *.tmp          — wszystkie pliki tymczasowe\n  Thumbs.db      — konkretna nazwa\n  node_modules/* — cały folder wraz z zawartością':
        'Windows 形式のパターンを使えます：\n  *.tmp          — すべての一時ファイル\n  Thumbs.db      — 特定の名前\n  node_modules/* — フォルダー全体とその中身',
    'Ochrona danych':
        'データの保護',
    'Odczytuje wszystkie pliki kopii i weryfikuje ich poprawność.\nNic nie zapisuje na dysku.':
        'バックアップのすべてのファイルを読み込み、正しいかどうかを検証します。\nディスクには何も書き込みません。',
    'Odpowiednik synchronizacji folderu. Wcześniejsze wersje plików nie są zachowywane.':
        'フォルダーの同期に相当します。ファイルの以前のバージョンは保持されません。',
    'Odtwarza pliki z kopii — również z kopii zaszyfrowanej.':
        'バックアップからファイルを復元します — 暗号化したバックアップからも復元できます。',
    'Odtwarza pliki zgodnie z ustawieniami powyżej':
        '上の設定に従ってファイルを復元します',
    'Odtwórz pełną strukturę folderów':
        'フォルダー構造をすべて再現',
    'Odtwórz pliki z istniejącej kopii':
        '既存のバックアップからファイルを復元',
    'Operacja nie powiodła się.':
        '操作に失敗しました。',
    'Operacja przerwana przez użytkownika.':
        'ユーザーが操作を中止しました。',
    'Operacja przerwana — utrwalam stan dotychczas zapisanych plików.':
        '操作を中止しました — これまでに書き込んだファイルの状態を保存しています。',
    'Operacja w toku':
        '操作の実行中',
    'Operacja zakończona błędem.':
        '操作はエラーで終了しました。',
    'Ostatnie operacje':
        '最近の操作',
    'Otwiera ekran przywracania z wypełnionymi ścieżkami':
        'パスを入力済みの状態で復元画面を開きます',
    'Otwiera pełny dziennik w domyślnym edytorze':
        'ログ全体を既定のエディターで開きます',
    'Otwórz katalog danych':
        'データフォルダーを開く',
    'Otwórz katalog dziennika':
        'ログフォルダーを開く',
    'Otwórz okno wyboru katalogu':
        'フォルダーを選択するダイアログを開きます',
    'Otwórz plik dziennika':
        'ログファイルを開く',
    'PBKDF2-HMAC-SHA256 ({count} iteracji)':
        'PBKDF2-HMAC-SHA256（反復 {count} 回）',
    'PBKDF2-HMAC-SHA256 — {count} iteracji':
        'PBKDF2-HMAC-SHA256 — 反復 {count} 回',
    'PBKDF2-HMAC-SHA256, {count} iteracji':
        'PBKDF2-HMAC-SHA256、反復 {count} 回',
    'Pełna struktura — układ jak w źródle, wewnątrz wskazanego katalogu.\nJeden folder — wygodne, gdy szukasz kilku plików.\nPierwotne lokalizacje — zapisuje pliki tam, skąd zostały pobrane.':
        'フォルダー構造を再現 — バックアップ元と同じ構成で、指定したフォルダーの中に復元します。\n1 つのフォルダー — 少数のファイルを探しているときに便利です。\n元の場所 — ファイルを元あった場所に書き戻します。',
    'Pierwszy przebieg kopiuje wszystko i trwa najdłużej. Kolejne porównują rozmiar i datę modyfikacji, więc zwykle kończą się w kilka sekund.':
        '初回の実行ではすべてをコピーするため、最も時間がかかります。2 回目以降はサイズと更新日時を比較するので、通常は数秒で終わります。',
    'Plan gotowy: {count} {files} do zapisania.':
        '計画ができました：{count} 個の{files}を書き込みます。',
    'Plik jest za krótki, by być kontenerem tego programu.':
        'このプログラムのコンテナーとしてはファイルが短すぎます。',
    'Plik skończył się wcześniej, niż deklaruje nagłówek.':
        'ファイルがヘッダーの宣言より早く終わっています。',
    'Plik w formacie w wersji {found}; ta wersja programu obsługuje {supported}.':
        'ファイルの形式のバージョンは {found} ですが、このバージョンのプログラムが対応しているのは {supported} です。',
    'Plik wymaga Argon2id, a biblioteka argon2-cffi jest niedostępna.':
        'このファイルには Argon2id が必要ですが、argon2-cffi ライブラリを利用できません。',
    'Pliki pominięte — kopia jest aktualna':
        'スキップされるファイル — バックアップは最新です',
    'Pliki trafią do wskazanego katalogu z zachowaniem struktury folderów.':
        'ファイルはフォルダー構造を保ったまま、指定したフォルダーに復元されます。',
    'Pliki wrócą dokładnie tam, skąd pochodzą. Katalog docelowy zostanie zignorowany.':
        'ファイルは元あった場所にそのまま戻ります。復元先フォルダーは無視されます。',
    'Pliki zmienione od ostatniego przebiegu':
        '前回の実行以降に変更されたファイル',
    'Pliki zostaną zapisane dokładnie tam, skąd pochodzą.\n\nKonflikty nazw: {collision}.\n\nCzy kontynuować?':
        'ファイルは元あった場所にそのまま書き込まれます。\n\n名前が重複した場合：{collision}。\n\n続行しますか？',
    'Pliki, których jeszcze nie ma w kopii':
        'まだバックアップにないファイル',
    'Po uzupełnieniu istniejącej wersji jej katalog nazywa się np.\n  2026-09-17_@687--2026-09-24_@921\nczyli: data utworzenia kopii i data ostatniego uzupełnienia.\n\nData utworzenia zostaje z przodu, więc katalogi nadal układają się\nchronologicznie. Widać to w Eksploratorze bez uruchamiania programu.':
        '既存のバージョンを補完すると、そのフォルダー名は次のようになります（例）：\n  2026-09-17_@687--2026-09-24_@921\nつまり、バックアップの作成日と最後に補完した日です。\n\n作成日が先頭に残るので、フォルダーは引き続き\n日付順に並びます。プログラムを起動しなくてもエクスプローラーで確認できます。',
    'Po wykonaniu kopii zostanie mało wolnego miejsca ({free}).':
        'バックアップ後の空き容量が少なくなります（{free}）。',
    'Po zakończeniu kopii program ponownie skanuje źródło i dogrywa do tej samej\nwersji pliki, które w międzyczasie powstały lub się zmieniły.\nPrzydatne, gdy pracujesz na danych w trakcie wielogodzinnej kopii.\nPlik zmieniony w trakcie własnego kopiowania nigdy nie jest uznawany za zapisany.':
        'バックアップの完了後にバックアップ元をもう一度スキャンし、その間に作成・変更されたファイルを\n同じバージョンに追加します。\n何時間もかかるバックアップの最中にデータを編集している場合に便利です。\nコピー中に変更されたファイルが、書き込み済みとみなされることはありません。',
    'Poczekaj na zakończenie bieżącej operacji.':
        '現在の操作が終わるまでお待ちください。',
    'Podaj hasło dla szablonu „{name}”:':
        'テンプレート「{name}」のパスワードを入力してください：',
    'Podaj hasło — bez niego nie można zaszyfrować kopii.':
        'パスワードを入力してください — パスワードがないとバックアップを暗号化できません。',
    'Podane hasło nie pasuje do plików zapisanych wcześniej w tej kopii. Wznowienie z innym hasłem zostawiłoby w jednej kopii pliki pod dwoma hasłami. Podaj hasło użyte przy poprzednim przebiegu albo utwórz kopię w nowym katalogu.':
        '入力したパスワードは、このバックアップに以前書き込まれたファイルと一致しません。別のパスワードで再開すると、1 つのバックアップに 2 つのパスワードのファイルが混在してしまいます。前回の実行で使ったパスワードを入力するか、新しいフォルダーにバックアップを作成してください。',
    'Podgląd zmian':
        '変更のプレビュー',
    'Pokazuje folder z plikami dziennika':
        'ログファイルのフォルダーを表示します',
    'Pokazuje folder z ustawieniami i szablonami':
        '設定とテンプレートのフォルダーを表示します',
    'Pokaż / ukryj wpisane hasło':
        '入力したパスワードを表示 / 非表示',
    'Pomiń istniejące pliki':
        '既存のファイルをスキップ',
    'Potwierdź usuwanie':
        '削除の確認',
    'Powtórz hasło':
        'パスワードを再入力',
    'Program nie mógł się uruchomić:\n\n{error}\n\nSzczegóły zapisano w dzienniku aplikacji.':
        'プログラムを起動できませんでした：\n\n{error}\n\n詳細はアプリケーションのログに記録されました。',
    'Program nie wie, czy ta kopia została dokończona. Uzupełnienie jej dogra tylko brakujące i zmienione pliki, a tego, co już jest zapisane, nie kopiuje ponownie.':
        'このバックアップが完了したかどうかはわかりません。補完すると、足りないファイルと変更されたファイルだけを追加し、すでに書き込まれたものは再度コピーしません。',
    'Program sam wykryje, czy kopia jest zaszyfrowana.':
        'バックアップが暗号化されているかどうかは自動で検出されます。',
    'Przebieg operacji i diagnostyka':
        '操作の経過と診断',
    'Przebieg operacji na żywo. Pełna historia trafia do pliku.':
        '操作の経過をリアルタイムで表示します。全履歴はファイルに保存されます。',
    'Przebieg uzupełniający: {error}':
        '追加取り込み：{error}',
    'Przeciętne':
        '普通',
    'Przerwano liczenie sumy kontrolnej.':
        'チェックサムの計算を中止しました。',
    'Przerwano skanowanie.':
        'スキャンを中止しました。',
    'Przerwano. Zapisano {count} {files} ({size}).':
        '中止しました。{count} 個の{files}を書き込みました（{size}）。',
    'Przerwij':
        '中止',
    'Przerywanie operacji…':
        '操作を中止しています…',
    'Przerywanie — zapisuję spis treści kopii, nie wyłączaj komputera…':
        '中止しています — バックアップの目次を書き込んでいます。コンピューターの電源を切らないでください…',
    'Przeskanowano {count} {files}.':
        '{count} 個の{files}をスキャンしました。',
    'Przygotowanie…':
        '準備しています…',
    'Przywracanie':
        '復元',
    'Przywracanie do pierwotnych lokalizacji':
        '元の場所への復元',
    'Przywracanie przerwane.':
        '復元を中止しました。',
    'Przywracanie {count} {files} ({size})…':
        '{count} 個の{files}を復元しています（{size}）…',
    'Przywróć do pierwotnych lokalizacji':
        '元の場所に復元',
    'Przywróć domyślne':
        '既定値に戻す',
    'Przywróć fabryczne':
        '初期リストに戻す',
    'Przywróć pliki':
        'ファイルを復元',
    'Przywróć z tej kopii':
        'このバックアップから復元',
    'Pusta nazwa':
        '名前が空です',
    'Równoległe operacje:':
        '並列処理数：',
    'Skanowanie plików źródłowych…':
        'バックアップ元のファイルをスキャンしています…',
    'Skrót z dziennika — pełny zapis znajdziesz w zakładce „Dziennik”.':
        'ログの要約です — 全記録は「ログ」画面で確認できます。',
    'Skąd przywracamy':
        '復元元',
    'Sprawdzam, co zmieniło się w źródle w trakcie kopii (przebieg uzupełniający {attempt} z {passes})…':
        'バックアップ中にバックアップ元で変更された内容を確認しています（追加取り込み {passes} 回中 {attempt} 回目）…',
    'Sprawdzam, czy hasło zgadza się z hasłem wcześniej zapisanych plików…':
        'パスワードが以前書き込まれたファイルと一致するか確認しています…',
    'Sprawdzam, czy w katalogu docelowym jest kopia do dokończenia…':
        'バックアップ先フォルダーに未完了のバックアップがあるか確認しています…',
    'Sprawdź hasło':
        'パスワードを確認してください',
    'Sprawdź kopię':
        'バックアップを検証',
    'Szablon przechowuje foldery, opcje i wykluczenia. Hasło nigdy nie trafia do szablonu — jest przechowywane w Menedżerze poświadczeń Windows albo wpisywane przy każdym uruchomieniu.':
        'テンプレートにはフォルダー、オプション、除外が保存されます。パスワードがテンプレートに保存されることはありません — Windows 資格情報マネージャーに保管するか、実行のたびに入力します。',
    'Szablon usunięty.':
        'テンプレートを削除しました。',
    'Szablon „{name}”':
        'テンプレート「{name}」',
    'Szablon „{name}” już istnieje.\n\nZastąpić go bieżącymi ustawieniami z formularza?':
        'テンプレート「{name}」はすでに存在します。\n\nフォームの現在の設定で置き換えますか？',
    'Szablon „{name}” zostanie usunięty.\n\nPliki kopii zapasowej pozostaną nienaruszone.':
        'テンプレート「{name}」を削除します。\n\nバックアップのファイルはそのまま残ります。',
    'Szablony':
        'テンプレート',
    'Szablony: {count}\nSzyfrowanie: AES-256-GCM\nKlucz: {kdf}':
        'テンプレート：{count}\n暗号化：AES-256-GCM\n鍵：{kdf}',
    'Szyfrowanie i kontrola poprawności zapisu.':
        '暗号化と書き込みの検証。',
    'Szyfrowanie: AES-256-GCM (uwierzytelnione)\nWyprowadzanie klucza: {kdf}':
        '暗号化：AES-256-GCM（認証付き）\n鍵の導出：{kdf}',
    'Szyfruj kopię (AES-256-GCM)':
        'バックアップを暗号化（AES-256-GCM）',
    'Słabe':
        '弱い',
    'Ta kopia nie jest zaszyfrowana — hasło nie jest potrzebne.':
        'このバックアップは暗号化されていません — パスワードは不要です。',
    'Ten folder jest już na liście.':
        'このフォルダーはすでに一覧にあります。',
    'To nie jest plik zaszyfrowany przez ten program.':
        'このファイルはこのプログラムで暗号化されたものではありません。',
    'Trwa inna operacja — poczekaj na jej zakończenie.':
        '別の操作を実行中です — 終わるまでお待ちください。',
    'Trwa operacja':
        '操作の実行中',
    'Trwa operacja na plikach. Zamknięcie programu ją przerwie.\n\nPliki zapisane do tej chwili zostaną zachowane, a kopię będzie można później dokończyć.\n\nZamknąć mimo to?':
        'ファイルの操作を実行中です。プログラムを閉じると操作は中止されます。\n\nここまでに書き込んだファイルは保持され、バックアップは後で完了させることができます。\n\nそれでも閉じますか？',
    'Trwa: {description}…':
        '実行中：{description}…',
    'Tryb dokładny — licz sumę kontrolną każdego pliku':
        '精密モード — すべてのファイルのチェックサムを計算する',
    'Układ kopii':
        'バックアップの構成',
    'Układ plików:':
        'ファイルの配置：',
    'Uruchom kopię':
        'バックアップを実行',
    'Ustawienia':
        '設定',
    'Usunąć szablon?':
        'テンプレートを削除しますか？',
    'Usuwa pozycję z listy. Nie kasuje żadnych plików.':
        '一覧から項目を削除します。ファイルは削除しません。',
    'Usuwa szablon. Nie kasuje żadnych plików kopii.':
        'テンプレートを削除します。バックアップのファイルは削除しません。',
    'Usuwaj z kopii pliki skasowane w źródle':
        'バックアップ元で削除されたファイルをバックアップからも削除する',
    'Usuń':
        '削除',
    'Usuń zaznaczone':
        '選択項目を削除',
    'Uszkodzony nagłówek pliku.':
        'ファイルのヘッダーが破損しています。',
    'Utwórz lub zaktualizuj kopię wybranych folderów':
        '選んだフォルダーのバックアップを作成・更新',
    'Utwórz nową wersję':
        '新しいバージョンを作成',
    'Uzupełnienie istniejącej wersji nie kopiuje ponownie tego, co już w niej jest — dokończysz przerwaną kopię bez tworzenia kolejnej pełnej wersji.':
        '既存のバージョンを補完する場合、すでに含まれているものは再度コピーしません — 新しい完全なバージョンを作らずに、中断したバックアップを完了できます。',
    'Uzupełnij tę wersję':
        'このバージョンを補完',
    'Uzupełnij: {version} • {labels}':
        '補完：{version} • {labels}',
    'W katalogu docelowym jest kopia tych samych folderów zapisana starszą wersją programu:':
        'バックアップ先フォルダーに、古いバージョンのプログラムで書き込まれた同じフォルダーのバックアップがあります：',
    'W katalogu docelowym jest niedokończona kopia tych samych folderów:':
        'バックアップ先フォルダーに、同じフォルダーの未完了のバックアップがあります：',
    'W tym katalogu nie ma spisu treści kopii — nie ma z czym porównać plików.':
        'このフォルダーにはバックアップの目次がありません — ファイルを比較する対象がありません。',
    'Wczytaj do formularza':
        'フォームに読み込む',
    'Wczytano manifest kopii: {count} {files}.':
        'バックアップのマニフェストを読み込みました：{count} 個の{files}。',
    'Wczytano szablon „{name}” do formularza.':
        'テンプレート「{name}」をフォームに読み込みました。',
    'Wersja kopii nosi teraz nazwę {name}.':
        'バックアップバージョンの名前は {name} になりました。',
    'Wersja, licencja i użyta kryptografia':
        'バージョン、ライセンス、使用している暗号技術',
    'Wersje z datą (zalecane)':
        '日付付きバージョン（推奨）',
    'Weryfikacja kopii':
        'バックアップの検証',
    'Weryfikacja nie powiodła się: nieprawidłowe hasło lub uszkodzony plik.':
        '検証に失敗しました：パスワードが正しくないか、ファイルが破損しています。',
    'Weryfikacja po zapisie nie powiodła się — zapisane dane różnią się od źródła.':
        '書き込み後の検証に失敗しました — 書き込んだデータがバックアップ元と異なります。',
    'Weryfikacja {count} {files} ({size}), {threads} równolegle…':
        '検証中：{count} 個の{files}（{size}）、{threads} 並列…',
    'Weryfikuj natychmiast po zapisie (spowalnia kopię)':
        '書き込み直後に検証する（バックアップが遅くなります）',
    'Wolne miejsce: {free} z {total}':
        '空き容量：{total} 中 {free}',
    'Wolniejszy, ale wykrywa zmiany, które nie zmieniły rozmiaru ani daty\n(np. po przywróceniu pliku z innego nośnika).':
        '時間はかかりますが、サイズも日付も変わらない変更を検出できます\n（例：別のメディアからファイルを復元した後）。',
    'Wpis {key} w spisie treści kopii wskazuje poza katalog docelowy — pomijam go.':
        'バックアップの目次の項目 {key} が復元先フォルダーの外を指しています — スキップします。',
    'Wraca do listy wbudowanej w program':
        'プログラムに組み込まれたリストに戻します',
    'Wskaż folder kopii, aby zobaczyć jej zawartość.':
        '内容を表示するには、バックアップフォルダーを指定してください。',
    'Wskaż folder kopii.':
        'バックアップフォルダーを指定してください。',
    'Wskaż foldery objęte kopią. Podfoldery są uwzględniane automatycznie.':
        'バックアップするフォルダーを指定してください。サブフォルダーは自動的に含まれます。',
    'Wskaż główny folder kopii (ten, który wybrałeś jako cel), a nie pojedynczy folder z datą. Program sam odczyta spis treści kopii.':
        '個々の日付付きフォルダーではなく、バックアップのメインフォルダー（バックアップ先として選んだフォルダー）を指定してください。バックアップの目次は自動で読み込まれます。',
    'Wskaż katalog docelowy kopii.':
        'バックアップ先フォルダーを指定してください。',
    'Wskaż katalog docelowy.':
        '復元先フォルダーを指定してください。',
    'Wstawia zalecaną listę wykluczeń':
        '推奨される除外リストを挿入します',
    'Wszystkie pliki wylądują bezpośrednio w katalogu docelowym, bez podfolderów.':
        'すべてのファイルが、サブフォルダーなしで復元先フォルダーに直接保存されます。',
    'Wszystko do jednego folderu':
        'すべてを 1 つのフォルダーに',
    'Wybierz folder do kopii':
        'バックアップするフォルダーを選択',
    'Wybierz folder kopii':
        'バックアップフォルダーを選択',
    'Wybierz katalog':
        'フォルダーを選択',
    'Wybierz katalog docelowy':
        '復元先フォルダーを選択',
    'Wybierz katalog docelowy kopii':
        'バックアップ先フォルダーを選択',
    'Wybierz katalog, aby zobaczyć dostępne miejsce.':
        'フォルダーを選ぶと空き容量が表示されます。',
    'Wybierz kolejny folder do kopii':
        'バックアップするフォルダーをさらに選択',
    'Wybierz szablon z listy.':
        '一覧からテンプレートを選んでください。',
    'Wybierz…':
        '選択…',
    'Wybrano nadpisywanie istniejących plików. Ich obecna zawartość zostanie bezpowrotnie zastąpiona.\n\nCzy kontynuować?':
        '既存のファイルを上書きする設定になっています。現在の内容は完全に置き換えられ、元に戻せません。\n\n続行しますか？',
    'Wyczyść widok':
        '表示を消去',
    'Wygląd':
        '外観',
    'Wygląd, wykluczenia domyślne i informacje o środowisku.':
        '外観、既定の除外、環境情報。',
    'Wygląd, wykluczenia i magazyn haseł':
        '外観、除外、パスワードの保管場所',
    'Wykluczenia':
        '除外',
    'Wykonuje kopię według tego szablonu':
        'このテンプレートの設定でバックアップを実行します',
    'Wykonuje kopię zgodnie z powyższymi ustawieniami':
        '上の設定でバックアップを実行します',
    'Wymagane wyłącznie dla kopii zaszyfrowanych.':
        '暗号化したバックアップの場合にのみ必要です。',
    'Wzorce plików i folderów pomijanych w kopii — po jednym w wierszu.':
        'バックアップから除外するファイルとフォルダーのパターン — 1 行に 1 つずつ。',
    'Włączono szyfrowanie, ale nie podano hasła.':
        '暗号化がオンですが、パスワードが入力されていません。',
    'Włączono usuwanie z kopii plików skasowanych w źródle.\n\nPliki usunięte w źródle stracą swoją jedyną kopię zapasową. Czy na pewno kontynuować?':
        'バックアップ元で削除されたファイルをバックアップからも削除する設定がオンです。\n\nバックアップ元で削除されたファイルは、唯一のバックアップも失われます。本当に続行しますか？',
    'Za mało miejsca w katalogu docelowym. Potrzeba ok. {needed}, dostępne {free}.':
        'バックアップ先フォルダーの空き容量が足りません。約 {needed} 必要ですが、空きは {free} です。',
    'Zabezpieczenie przed literówką — hasła nie da się odzyskać.':
        '入力ミスを防ぐためです — パスワードは復旧できません。',
    'Zachowaj oba — dopisz numer do nazwy':
        '両方を残す — 名前に番号を付ける',
    'Zakończono z błędami ({errors}). Zapisano {count} {files}.':
        'エラーありで終了しました（{errors} 件）。{count} 個の{files}を書き込みました。',
    'Zakończono.':
        '完了しました。',
    'Zapamiętaj hasło w Menedżerze poświadczeń Windows':
        'パスワードを Windows 資格情報マネージャーに保存する',
    'Zapamiętuje te ustawienia do ponownego użycia':
        'この設定を保存して再利用できるようにします',
    'Zapis bieżącej sesji':
        '現在のセッションの記録',
    'Zapisane konfiguracje do ponownego użycia':
        '再利用できる保存済みの設定',
    'Zapisane konfiguracje — uruchamiasz je jednym kliknięciem.':
        '保存済みの設定 — ワンクリックで実行できます。',
    'Zapisane szablony':
        '保存済みのテンプレート',
    'Zapisano szablon „{name}”.':
        'テンプレート「{name}」を保存しました。',
    'Zapisuje listę jako domyślną':
        'この一覧を既定として保存します',
    'Zapisuje nową nazwę szablonu':
        'テンプレートの新しい名前を保存します',
    'Zapisywanie {count} {files} ({size}), {workers} równolegle':
        '書き込み中：{count} 個の{files}（{size}）、{workers} 並列',
    'Zapisz':
        '保存',
    'Zapisz do:':
        '書き込み先：',
    'Zapisz jako szablon':
        'テンプレートとして保存',
    'Zapisz nazwę':
        '名前を保存',
    'Zapisz szablon':
        'テンプレートを保存',
    'Zastąpić szablon?':
        'テンプレートを置き換えますか？',
    'Zatrzymuje operację. Pliki już zapisane pozostają nienaruszone.':
        '操作を中止します。書き込み済みのファイルはそのまま残ります。',
    'Zaznacz szablon na liście.':
        '一覧でテンプレートを選択してください。',
    'Zmiana języka przebudowuje okno; wypełnione ścieżki zostają.':
        '言語を変更するとウィンドウが再構成されます。入力済みのパスはそのまま残ります。',
    'Zmiana motywu działa natychmiast.':
        'テーマの変更はすぐに反映されます。',
    'Zmienia kolor przycisków i zaznaczeń':
        'ボタンと選択部分の色を変更します',
    'Zmień nazwę, aby łatwiej rozpoznawać szablon.':
        'テンプレートを見分けやすい名前に変更してください。',
    'Znaleziono {count} {files}. Porównuję z poprzednią kopią…':
        '{count} 個の{files}が見つかりました。前回のバックアップと比較しています…',
    'automatycznie':
        '自動',
    'bez zmian':
        '変更なし',
    'brak (biblioteka keyring niezainstalowana)':
        'なし（keyring ライブラリがインストールされていません）',
    'brak danych':
        'データなし',
    'brak pliku w kopii':
        'バックアップにファイルがありません',
    'do zapisania':
        '書き込み予定',
    'istniejąca kopia: {count} {files}, ostatnio {when}':
        '既存のバックアップ：{count} 個の{files}、最終更新 {when}',
    'jeszcze nie uruchamiany':
        '未実行',
    'kompletna':
        '完了',
    'kopia lustrzana':
        'ミラーコピー',
    'kopia zapasowa':
        'バックアップ',
    'nie':
        'いいえ',
    'niedokończona':
        '未完了',
    'niedokończona — brakuje ok. {count} {files} ({size})':
        '未完了 — 約 {count} 個の{files}が不足（{size}）',
    'niezaszyfrowana':
        '暗号化なし',
    'nieznany format manifestu':
        '不明なマニフェスト形式',
    'nowych plików':
        '新規ファイル',
    'np. C:\\Odzyskane':
        '例：C:\\復元',
    'np. E:\\Kopie zapasowe':
        '例：E:\\バックアップ',
    'plik':
        'ファイル',
    'plik stanu jest za krótki':
        '状態ファイルが短すぎます',
    'plik stanu w wersji {found}, obsługiwana: {supported}':
        '状態ファイルのバージョンは {found}、対応バージョン：{supported}',
    'pliki':
        'ファイル',
    'plików':
        'ファイル',
    'podgląd kopii':
        'バックアップのプレビュー',
    'pozostaną w kopii':
        'バックアップに残ります',
    'rozmiar w kopii {actual} B zamiast {expected} B':
        'バックアップ内のサイズが {expected} B ではなく {actual} B です',
    'sprawdzanie kopii':
        'バックアップの確認',
    'stan nieznany (zapisana starszą wersją programu)':
        '状態不明（古いバージョンのプログラムで書き込み）',
    'suma kontrolna manifestu się nie zgadza':
        'マニフェストのチェックサムが一致しません',
    'suma kontrolna się nie zgadza — plik uszkodzony':
        'チェックサムが一致しません — ファイルが破損しています',
    'szablon {name}':
        'テンプレート「{name}」',
    'tak':
        'はい',
    'ten system plików':
        'このファイルシステム',
    'wersja {version}':
        'バージョン {version}',
    'wersje z datą':
        '日付付きバージョン',
    'weryfikacja':
        '検証',
    'wyłączona':
        'オフ',
    'zaszyfrowana (AES-256-GCM)':
        '暗号化あり（AES-256-GCM）',
    'zawartość różni się od pliku źródłowego':
        '内容がバックアップ元のファイルと異なります',
    'zawartość różni się od sumy kontrolnej zapisanej podczas kopii':
        '内容がバックアップ時に記録したチェックサムと異なります',
    'zmienionych':
        '変更あり',
    'zostaną usunięte z kopii':
        'バックアップから削除されます',
    '{done} z {total} • {speed}/s{eta}':
        '{done} / {total} • {speed}/秒{eta}',
    '{done} • {speed}/s':
        '{done} • {speed}/秒',
    '{hours} h {minutes} min':
        '{hours} 時間 {minutes} 分',
    '{label}: {count} {files}':
        '{label}：{count} 個の{files}',
    '{message}\n\nSzczegóły techniczne znajdziesz w zakładce „Dziennik”.':
        '{message}\n\n技術的な詳細は「ログ」画面で確認できます。',
    '{minutes} min {seconds} s':
        '{minutes} 分 {seconds} 秒',
    '{name}: nie można odczytać ({error})':
        '{name}：読み取れません（{error}）',
    '{seconds} s':
        '{seconds} 秒',
    '{summary}\n\nProblemy:\n{problems}\n\nPełna lista znajduje się w zakładce „Dziennik”.':
        '{summary}\n\n問題：\n{problems}\n\n完全な一覧は「ログ」画面にあります。',
    '{summary}{notes}\n\nPliki zapisane przed przerwaniem są kompletne i zostały odnotowane w spisie treści kopii.\n\nAby dokończyć kopię, uruchom ją ponownie — program zaproponuje uzupełnienie tej wersji zamiast tworzenia nowej.':
        '{summary}{notes}\n\n中止前に書き込まれたファイルは完全な状態で、バックアップの目次に記録されています。\n\nバックアップを完了させるには、もう一度実行してください — 新しいバージョンを作る代わりに、このバージョンを補完するよう提案されます。',
    '{title} — gotowe':
        '{title} — 完了',
    '{title} — przerwano':
        '{title} — 中止',
    '{title} — zakończono z błędami':
        '{title} — エラーありで終了',
    '{when}  •  {action}  •  {count} {files}':
        '{when}  •  {action}  •  {count} 個の{files}',
    'Łączny rozmiar danych do przesłania':
        '転送するデータの合計サイズ',
    'Środowisko':
        '環境',
    'Źródła: {sources}\nCel: {destination}\nUkład: {structure} • Szyfrowanie: {encrypt} • Weryfikacja: {verify} • Dogrywka: {catchup} • Równolegle: {workers} • Data uzupełnienia w nazwie: {stamp}\nUtworzony: {created} • Ostatni przebieg: {last}':
        'バックアップ元：{sources}\nバックアップ先：{destination}\n構成：{structure} • 暗号化：{encrypt} • 検証：{verify} • 追加取り込み：{catchup} • 並列：{workers} • 名前に補完日：{stamp}\n作成日：{created} • 最終実行：{last}',
    'Źródło nie zmieniło się w trakcie kopii — nie ma czego uzupełniać.':
        'バックアップ中にバックアップ元は変更されませんでした — 追加で取り込むものはありません。',
    '—':
        '—',
    '• Kopia przyrostowa — zapisywane są wyłącznie pliki nowe i zmienione.\n  Porównanie opiera się na spisie treści kopii, rozmiarze i dacie modyfikacji;\n  przy różnicy liczona jest suma kontrolna SHA-256.\n\n• Wersje z datą — każdy przebieg tworzy kompletny folder z datą, a pliki\n  niezmienione są podpinane twardym dowiązaniem, więc nie zajmują miejsca dwa razy.\n\n• Weryfikacja po zapisie — zapisany plik jest odczytywany z powrotem\n  i porównywany ze źródłem.\n\n• Odporność na przerwania — pliki powstają pod nazwą tymczasową i są\n  podmieniane dopiero po pełnym zapisie.':
        '• 増分バックアップ — 新規ファイルと変更されたファイルだけを書き込みます。\n  比較にはバックアップの目次、サイズ、更新日時を使い、\n  違いがある場合は SHA-256 チェックサムを計算します。\n\n• 日付付きバージョン — 実行のたびに日付付きの完全なフォルダーを作成し、\n  変更のないファイルはハードリンクでつなぐため、容量を二重に使いません。\n\n• 書き込み後の検証 — 書き込んだファイルを読み直し、\n  バックアップ元と比較します。\n\n• 中断への耐性 — ファイルは一時的な名前で作成され、\n  完全に書き込まれてから置き換えられます。',
    '• Szyfr: AES-256 w trybie GCM (szyfrowanie z uwierzytelnieniem).\n• Wyprowadzanie klucza z hasła: {kdf}.\n• Nagłówek każdego pliku jest uwierzytelniony jako AAD — podmiana parametrów\n  unieważnia tag.\n• Każdy plik dostaje losowy, niepowtarzalny nonce.\n• Odszyfrowany plik powstaje dopiero po pomyślnej weryfikacji tagu.\n• Hasła nie są zapisywane w plikach programu. Opcjonalnie trafiają do\n  Menedżera poświadczeń Windows.':
        '• 暗号：GCM モードの AES-256（認証付き暗号）。\n• パスワードからの鍵の導出：{kdf}。\n• 各ファイルのヘッダーは AAD として認証されます — パラメーターを書き換えると\n  タグが無効になります。\n• 各ファイルには、ランダムで一意のナンスが割り当てられます。\n• 復号したファイルは、タグの検証に成功してから初めて作成されます。\n• パスワードはプログラムのファイルに保存されません。必要に応じて\n  Windows 資格情報マネージャーに保存されます。',
    'Bez hasła nie da się odczytać ani jednego pliku z kopii.':
        'パスワードがなければ、バックアップのファイルは 1 つも読み取れません。',
    'Co chcesz chronić?':
        '何を保護しますか？',
    'Co chcesz teraz zrobić?':
        '何をしますか？',
    'Czyta kopię z nośnika i porównuje ją z zapisanymi sumami kontrolnymi.':
        'メディアからバックアップを読み込み、記録されたチェックサムと比較します。',
    'Dalej':
        '次へ',
    'Dokumenty i zdjęcia':
        '文書と写真',
    'Ekran powitalny wrócisz w ustawieniach, gdy zmienisz zdanie.':
        '気が変わったら、設定でようこそ画面を再び表示できます。',
    'Ekran z pytaniem, co chcesz teraz zrobić: kopia, przywracanie, sprawdzenie.':
        '次に何をするか（バックアップ、復元、検証）を尋ねる画面です。',
    'Foldery objęte kopią':
        'バックアップの対象フォルダー',
    'Foldery z pracą. Kreator pominie katalogi, które odtwarza się jednym poleceniem (node_modules, venv, build).':
        '作業中のフォルダー。コマンド 1 つで再作成できるフォルダー（node_modules、venv、build）はウィザードが除外します。',
    'Gdzie zapisać kopię?':
        'バックアップをどこに保存しますか？',
    'Historia i szyfrowanie':
        '履歴と暗号化',
    'Historia zmian (zalecane)':
        '変更履歴あり（推奨）',
    'Jak bardzo chcesz się zabezpieczyć?':
        'どの程度保護しますか？',
    'Jak wyżej, a dodatkowo każdy plik trafia do kopii zaszyfrowany (AES-256-GCM). Potrzebne przy kopii wożonej poza dom.':
        '上記に加えて、各ファイルを暗号化してバックアップします（AES-256-GCM）。バックアップを自宅の外に持ち出す場合に必要です。',
    'Jedna aktualna kopia':
        '最新のコピーを 1 つだけ',
    'Język, motyw, domyślne wykluczenia i informacje o środowisku.':
        '言語、テーマ、既定の除外、環境情報。',
    'Katalog docelowy leży wewnątrz źródła — wybierz inny.':
        'バックアップ先フォルダーがバックアップ元の中にあります — 別のフォルダーを選んでください。',
    'Każdy przebieg tworzy folder z datą. Pliki niezmienione są podpinane dowiązaniem, więc historia kosztuje tyle, ile realnie się zmieniło.':
        '実行のたびに日付付きのフォルダーを作成します。変更のないファイルはリンクでつなぐため、履歴に使う容量は実際に変更された分だけです。',
    'Każdy przebieg utworzy folder z datą. Pierwszy zajmie tyle, ile dane; kolejne — tyle, ile realnie się zmieniło.':
        '実行のたびに日付付きのフォルダーが作成されます。初回はデータと同じ容量を使い、2 回目以降は実際に変更された分だけを使います。',
    'Kopia powstanie w: {path}':
        'バックアップの作成先：{path}',
    'Kopia trafi do: {path}':
        'バックアップ先：{path}',
    'Kopia: {what}':
        'バックアップ：{what}',
    'Krok {number} z {total}':
        'ステップ {number}/{total}',
    'Najlepiej na innym dysku fizycznym niż ten, który chronisz — kopia obok oryginału ginie razem z nim.':
        '保護したいドライブとは別の物理ドライブが最適です — 元のデータと同じ場所にあるバックアップは、元のデータと一緒に失われます。',
    'Najszybsza i najmniejsza. Kopia odpowiada temu, co masz teraz — bez historii wcześniejszych wersji.':
        '最も速く、容量も最小です。バックアップは現在の状態と同じになり、以前のバージョンの履歴は残りません。',
    'Nie było jeszcze żadnej kopii. Zacznij od „Zrób kopię”.':
        'まだバックアップはありません。「今すぐバックアップ」から始めてください。',
    'Nie lista ustawień, tylko ich skutki.':
        '設定の一覧ではなく、その結果です。',
    'Nie pokazuj tego ekranu przy starcie':
        '起動時にこの画面を表示しない',
    'Nośnik docelowy':
        '保存先のメディア',
    'Odtwarza pliki z kopii — całość albo wybrany folder.':
        'バックアップからファイルを復元します — 全体でも、選んだフォルダーだけでも。',
    'Odśwież listę':
        '一覧を更新',
    'Ostatnia kopia: {when} • {count} {files}.':
        '前回のバックアップ：{when} • {count} 個の{files}。',
    'Pierwszy przebieg jest najdłuższy — kolejne porównują rozmiar i datę modyfikacji, więc zwykle trwają sekundy.':
        '初回の実行が最も長くかかります — 2 回目以降はサイズと更新日時を比較するので、通常は数秒で終わります。',
    'Pliki w kopii będą zaszyfrowane; bez hasła nie da się ich odczytać.':
        'バックアップ内のファイルは暗号化されます。パスワードがなければ読み取れません。',
    'Podfoldery są uwzględniane automatycznie.':
        'サブフォルダーは自動的に含まれます。',
    'Pokazuj ekran powitalny przy starcie':
        '起動時にようこそ画面を表示する',
    'Ponownie sprawdza podłączone nośniki':
        '接続されているドライブをもう一度確認します',
    'Program będzie utrzymywał jeden folder zgodny ze źródłem. Każdy kolejny przebieg dopisze tylko to, co się zmieniło.':
        'バックアップ元と同じ状態のフォルダーを 1 つ維持します。2 回目以降の実行では、変更された部分だけを書き込みます。',
    'Projekty i kod':
        'プロジェクトとコード',
    'Przechodzi do następnego kroku':
        '次のステップに進みます',
    'Przechodzi do pełnego okna programu':
        'プログラムのメインウィンドウに移動します',
    'Sam wskażesz, co ma trafić do kopii.':
        'バックアップする対象を自分で指定します。',
    'System plików: {filesystem}, klaster {cluster}':
        'ファイルシステム：{filesystem}、クラスター {cluster}',
    'Ten katalog leży wewnątrz folderu źródłowego — wybierz inny.':
        'このフォルダーはバックアップ元フォルダーの中にあります — 別のフォルダーを選んでください。',
    'Ten nośnik nie obsługuje twardych dowiązań, więc każda wersja z datą zajmie tyle miejsca co pełna kopia. Przy tym nośniku rozważ „jedną aktualną kopię”.':
        'このメディアはハードリンクに対応していないため、日付付きバージョンはそれぞれ完全なコピーと同じ容量を使います。このメディアでは「最新のコピーを 1 つだけ」を検討してください。',
    'To dysk systemowy — kopia nie przetrwa jego awarii. Jeśli masz drugi dysk albo pendrive, wybierz jego.':
        'これはシステムドライブです — ドライブが故障するとバックアップも失われます。別のドライブや USB メモリがあれば、そちらを選んでください。',
    'To się wydarzy':
        '実行される内容',
    'Trzy gotowe zestawy zamiast kilkunastu przełączników.':
        '十数個のスイッチの代わりに、すぐに使える 3 つのセットから選べます。',
    'Twoje pliki osobiste z folderów użytkownika. Najczęstszy wybór.':
        'ユーザーフォルダーにある個人用ファイル。最も一般的な選択です。',
    'Uruchamia kreator, który ustawi kopię krok po kroku':
        'バックアップを順を追って設定するウィザードを起動します',
    'Nowa kopia krok po kroku…':
        '新しいバックアップを順を追って設定…',
    'Ustawia kopię krok po kroku i zapisuje ją jako szablon':
        'バックアップを順を追って設定し、テンプレートとして保存します',
    'Ustawienia pierwszej kopii':
        '最初のバックアップの設定',
    'Ustawienia pierwszej kopii…':
        '最初のバックアップを設定…',
    'W tym katalogu jest już kopia ({count} {files}) — program ją uzupełni, a nie nadpisze.':
        'このフォルダーにはすでにバックアップがあります（{count} 個の{files}）— 上書きせずに補完します。',
    'Wraca do poprzedniego kroku':
        '前のステップに戻ります',
    'Wskaż dowolny katalog docelowy':
        '任意のバックアップ先フォルダーを指定します',
    'Wskaż folder kopii i kliknij „Sprawdź kopię”.':
        'バックアップフォルダーを指定し、「バックアップを検証」をクリックしてください。',
    'Wstecz':
        '戻る',
    'Wybierz':
        '選択',
    'Wybierz inny folder…':
        '別のフォルダーを選択…',
    'Wybierz to, co najbliższe. Dokładną listę folderów poprawisz niżej.':
        '最も近いものを選んでください。フォルダーの一覧は下で細かく調整できます。',
    'Wybrane foldery':
        '選んだフォルダー',
    'Zamknij':
        '閉じる',
    'Zamyka kreator bez zapisywania':
        '保存せずにウィザードを閉じます',
    'Zapisuje nowe i zmienione pliki. Pierwszy raz trwa najdłużej.':
        '新規ファイルと変更されたファイルを書き込みます。初回が最も時間がかかります。',
    'Zapisuje szablon bez uruchamiania kopii':
        'バックアップを実行せずにテンプレートを保存します',
    'Zapisuje szablon i od razu uruchamia kopię':
        'テンプレートを保存し、すぐにバックアップを実行します',
    'Zapisz i zrób kopię':
        '保存してバックアップ',
    'Zapisz ustawienia':
        '設定を保存',
    'Zrób kopię':
        '今すぐバックアップ',
    'dysk systemowy':
        'システムドライブ',
    'wolne {free} z {total}':
        '空き {free} / {total}',
    'Porównano ze źródłem: {source}; tylko z sumą kontrolną (źródło zmieniło się albo jest niedostępne): {checksum}.':
        'バックアップ元と比較：{source}、チェックサムのみと比較（バックアップ元が変更されたか利用できない）：{checksum}。',
    'Przywraca losową próbkę plików do katalogu tymczasowego i porównuje je ze źródłem.\nSprawdza całą drogę odzyskiwania, a trwa minuty. Nic nie zostaje na dysku.':
        'ランダムに選んだファイルを一時フォルダーに復元し、バックアップ元と比較します。\n復旧の全工程を数分で確認できます。ディスクには何も残りません。',
    'Próbne przywrócenie':
        'テスト復元',
    'W kopii nie ma plików, które dałoby się sprawdzić próbnie.':
        'バックアップには、テスト復元で確認できるファイルがありません。',
    'przywrócony plik różni się od pliku źródłowego':
        '復元したファイルがバックアップ元のファイルと異なります',
    'przywrócony plik różni się od sumy kontrolnej zapisanej podczas kopii':
        '復元したファイルが、バックアップ時に記録したチェックサムと異なります',
    'próbne przywrócenie':
        'テスト復元',
    '(brak zapisanych szablonów)':
        '（保存済みのテンプレートはありません）',
    'Bez tego kopia planowa ruszy dopiero wtedy, gdy sam otworzysz program.':
        'オフにすると、スケジュールバックアップはプログラムを自分で開くまで始まりません。',
    'Codziennie o godzinie':
        '毎日決まった時刻に',
    'Codziennie o wybranej godzinie (zalecane)':
        '毎日、選んだ時刻に（推奨）',
    'Dla dysku USB podłączanego od czasu do czasu. Najwyżej jedna kopia na 12 godzin.':
        'ときどき接続する USB ドライブ向け。バックアップは 12 時間に 1 回までです。',
    'Dostępne w zainstalowanej wersji programu (plik EXE).':
        'インストール版のプログラム（EXE ファイル）で利用できます。',
    'Godzina kopii codziennej (czas tego komputera).':
        '毎日のバックアップの時刻（このコンピューターの時刻）。',
    'Harmonogram działa wtedy, gdy działa program — także ukryty przy zegarze.':
        'スケジュールはプログラムの実行中に機能します — 時計の横に隠れている間も含みます。',
    'Harmonogram nie uruchamia kopii, dopóki tego nie odznaczysz. Ręczne kopie działają.':
        'このチェックを外すまで、スケジュールによるバックアップは開始されません。手動のバックアップは実行できます。',
    'Harmonogram szablonu „{name}” zapisany.':
        'テンプレート「{name}」のスケジュールを保存しました。',
    'Harmonogram:':
        'スケジュール：',
    'Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.':
        'その時刻にコンピューターの電源が切れていた場合は、電源を入れた後にバックアップが始まります。',
    'Kiedy kopia z tego szablonu ma ruszać sama.':
        'このテンプレートのバックアップを自動で開始するタイミング。',
    'Kiedy robić kopię?':
        'いつバックアップしますか？',
    'Kopia będzie robiona codziennie o {time}; termin przegapiony przy wyłączonym komputerze program nadrobi po jego włączeniu.':
        'バックアップは毎日 {time} に実行されます。コンピューターの電源が切れていて実行できなかった分は、電源を入れた後に実行されます。',
    'Kopia planowa nie powiodła się':
        'スケジュールバックアップに失敗しました',
    'Kopia rusza tylko wtedy, gdy ją uruchomisz.':
        'バックアップは、あなたが実行したときだけ始まります。',
    'Kopia ruszy po podłączeniu dysku docelowego (najwyżej raz na 12 godzin).':
        'バックアップ先のドライブを接続するとバックアップが始まります（12 時間に 1 回まで）。',
    'Kopia ruszy po podłączeniu dysku docelowego — najwyżej raz na 12 godzin.':
        'バックアップ先のドライブを接続するとバックアップが始まります — 12 時間に 1 回までです。',
    'Kopia sprzed miesiąca nie chroni tego, co zmieniło się od tamtej pory.':
        '1 か月前のバックアップでは、その後に変更されたものは守れません。',
    'Kopia „{name}” czeka':
        'バックアップ「{name}」が実行されていません',
    'Kopia „{name}” nie ruszyła':
        'バックアップ「{name}」を開始できませんでした',
    'Kopie planowe działają, gdy działa program (także ukryty przy zegarze).':
        'スケジュールバックアップは、プログラムの実行中に動作します（時計の横に隠れている間も含みます）。',
    'Kopie planowe działają, gdy działa program: po zamknięciu okna zostaje ikona przy zegarze, a przy logowaniu do Windows program uruchamia się w tle.':
        'スケジュールバックアップは、プログラムの実行中に動作します。ウィンドウを閉じても時計の横にアイコンが残り、Windows へのサインイン時にはプログラムがバックグラウンドで起動します。',
    'Kopie planowe i praca w tle':
        'スケジュールバックアップとバックグラウンド動作',
    'Kopie planowe wykonają się o czasie. Program zamkniesz z menu ikony przy zegarze.':
        'スケジュールバックアップは予定どおりに実行されます。プログラムを終了するには、時計の横のアイコンのメニューを使います。',
    'Kopię uruchamiasz przyciskiem. Najprostsze, ale łatwo o niej zapomnieć.':
        'ボタンでバックアップを実行します。最も簡単ですが、忘れがちです。',
    'Kopię uruchamiasz sam — przyciskiem w programie albo z menu ikony przy zegarze.':
        'バックアップは自分で実行します — プログラムのボタンか、時計の横のアイコンのメニューから。',
    'Następna kopia: {when}. Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.':
        '次回のバックアップ：{when}。その時刻にコンピューターの電源が切れていた場合は、電源を入れた後にバックアップが始まります。',
    'Nie udało się zmienić startu przy logowaniu — szczegóły w dzienniku.':
        'サインイン時の起動設定を変更できませんでした — 詳細はログを参照してください。',
    'Od {days} dni nie było udanej kopii. Podłącz dysk docelowy albo otwórz program, żeby sprawdzić, co się dzieje.':
        '{days} 日間、成功したバックアップがありません。バックアップ先のドライブを接続するか、プログラムを開いて状況を確認してください。',
    'Otwórz Sigelith Backup':
        'Sigelith Backup を開く',
    'Po podłączeniu dysku docelowego':
        'バックアップ先のドライブを接続したとき',
    'Po podłączeniu dysku z kopią':
        'バックアップ用ドライブを接続したとき',
    'Po zamknięciu okna działaj dalej przy zegarze, gdy są kopie planowe':
        'スケジュールバックアップがある場合、ウィンドウを閉じても時計の横で動作を続ける',
    'Potrzebne, żeby kopie planowe ruszały bez Twojego udziału. Hasło trafia do magazynu systemowego powiązanego z Twoim kontem, nie do plików programu.':
        'スケジュールバックアップを無人で開始するために必要です。パスワードはプログラムのファイルではなく、あなたのアカウントに紐づいたシステムの保管場所に保存されます。',
    'Program uruchamia się w tle przy logowaniu, więc terminy nie przepadną.':
        'サインイン時にプログラムがバックグラウンドで起動するので、予定を逃しません。',
    'Ręcznie':
        '手動',
    'Ręcznie — kiedy zechcę':
        '手動 — 好きなときに',
    'Start przy logowaniu włączony':
        'サインイン時の起動をオンにしました',
    'Szablon jest zaszyfrowany, a hasło nie jest zapamiętane. Kopie planowe potrzebują hasła zapisanego w Menedżerze poświadczeń Windows.':
        'テンプレートは暗号化されていますが、パスワードが保存されていません。スケジュールバックアップには、Windows 資格情報マネージャーに保存されたパスワードが必要です。',
    'Sigelith Backup będzie uruchamiał się w tle, żeby wykonywać kopie planowe. Wyłączysz to w ustawieniach programu.':
        'Sigelith Backup はスケジュールバックアップを実行するため、バックグラウンドで起動します。この動作はプログラムの設定でオフにできます。',
    'Sigelith Backup działa w tle':
        'Sigelith Backup はバックグラウンドで動作しています',
    'Uruchamiaj program w tle przy logowaniu do Windows':
        'Windows へのサインイン時にプログラムをバックグラウンドで起動する',
    'Wstrzymaj kopie planowe':
        'スケジュールバックアップを一時停止',
    'Zakończ':
        '終了',
    'Zamknięcie okna chowa je, a harmonogram pilnuje terminów. Program zamkniesz z menu ikony przy zegarze.':
        'ウィンドウを閉じると非表示になり、スケジュールは引き続き予定を管理します。プログラムを終了するには、時計の横のアイコンのメニューを使います。',
    'Zrób kopię teraz':
        '今すぐバックアップ',
    '{summary} Szczegóły znajdziesz w programie, w zakładce „Dziennik”.':
        '{summary} 詳細はプログラムの「ログ」画面で確認できます。',
    'Program działa z uprawnieniami administratora. Nie są mu potrzebne — kopia i przywracanie działają bez nich, a pliki zapisane przez administratora mogą później nie dać się zmienić ze zwykłego konta.':
        'このプログラムは管理者権限で実行されています。管理者権限は必要ありません — バックアップも復元も管理者権限なしで動作します。また、管理者が書き込んだファイルは、後で通常のアカウントから変更できなくなることがあります。',
    'Pliki otwarte w innych programach nie trafiły do kopii: {files}. Zamknij te programy i uruchom kopię ponownie — dograne zostaną tylko te pliki.':
        '他のプログラムで開かれていたファイルはバックアップされませんでした：{files}。それらのプログラムを閉じてから、もう一度バックアップを実行してください — それらのファイルだけが追加されます。',
    'Uwaga: w źródle zmieniło się podejrzanie dużo plików — {reasons}':
        '警告：バックアップ元で不審なほど多くのファイルが変更されています — {reasons}',
    'Wstrzymano kopię: w źródle zmieniło się podejrzanie dużo plików. {reasons}':
        'バックアップを一時停止しました：バックアップ元で不審なほど多くのファイルが変更されています。{reasons}',
    'Zmieniło się albo zniknęło {count} z {previous} plików poprzedniej kopii.':
        '前回のバックアップの {previous} 個のファイルのうち、{count} 個が変更または削除されています。',
    '{suspicious} z {evaluated} sprawdzonych zmienionych plików ma treść, która nie pasuje do ich typu (wygląda na zaszyfrowaną).':
        '確認した変更済みファイル {evaluated} 個のうち {suspicious} 個は、内容がファイルの種類と一致しません（暗号化されているように見えます）。',
    'Kontynuuj mimo to':
        'それでも続行',
    'Kopia planowa wstrzymana':
        'スケジュールバックアップを一時停止しました',
    'Kopia wstrzymana do decyzji.':
        '判断を待つため、バックアップを一時停止しました。',
    'Kopia wstrzymana — w źródle zmieniło się podejrzanie dużo plików.':
        'バックアップを一時停止しました — バックアップ元で不審なほど多くのファイルが変更されています。',
    'Podejrzanie dużo zmian':
        '不審なほど多くの変更',
    'Wstrzymaj kopię':
        'バックアップを一時停止',
    '{reasons}\n\nJeśli to spodziewane — aktualizacja programu, przeniesienie albo przerobienie wielu plików — kontynuuj.\n\nJeśli nie, NIE kontynuuj: tak wygląda działanie oprogramowania szyfrującego pliki (ransomware). Sprawdź najpierw, czy Twoje pliki dają się otworzyć. Wcześniejsze wersje w kopii pozostają nietknięte.':
        '{reasons}\n\n心当たりがある場合（ソフトウェアの更新、多数のファイルの移動や編集など）は、続行してください。\n\n心当たりがない場合は、絶対に続行しないでください：ファイルを暗号化するマルウェア（ランサムウェア）が動いているときは、このように見えます。まず、ファイルを開けるかどうか確認してください。バックアップ内の以前のバージョンはそのまま残っています。',
    '{reasons} To może być działanie złośliwego oprogramowania szyfrującego pliki. Otwórz program, sprawdź pliki i uruchom kopię ręcznie.':
        '{reasons} ファイルを暗号化するマルウェアの仕業かもしれません。プログラムを開いてファイルを確認し、手動でバックアップを実行してください。',
    'Pominięto {count} {files}.':
        '{files} {count} 個をスキップしました。',
    'Ponawiam {count} {files}…':
        '{files} {count} 個を再試行しています…',
    ' (bez {count} {files})':
        ' （{files} {count} 個を除く）',
    'plik otwarty w innym programie':
        '他のプログラムで開かれているファイル',
    'pliki otwarte w innych programach':
        '他のプログラムで開かれているファイル',
    'plików otwartych w innych programach':
        '他のプログラムで開かれているファイル',
    'pliku otwartego w innym programie':
        '他のプログラムで開かれているファイル',
    '\n\n…i kolejne: {count}.':
        '\n\n…ほか {count} 件。',
    'Foldery objęte kopią ({count}): {list}':
        'バックアップの対象フォルダー（{count}）：{list}',
    'Nośnik nie obsługuje twardych dowiązań — kopiuję do nowej wersji niezmienione pliki: {count} ({size})…':
        'メディアがハードリンクに対応していません — 変更のないファイルを新しいバージョンにコピーしています：{count} 個（{size}）…',
    'Pliki bez sumy kontrolnej sprawdzone tylko co do rozmiaru, bo ich źródło zmieniło się albo jest niedostępne: {count}.':
        'チェックサムがなく、バックアップ元が変更されたか利用できないため、サイズだけを確認したファイル：{count} 個。',
    'Pliki bez zapisanej sumy kontrolnej, porównane ze źródłem i uzupełnione w spisie treści: {count}.':
        'チェックサムが記録されていなかったため、バックアップ元と比較して目次に追加したファイル：{count} 個。',
    'Pliki przeniesione w źródle: {count} — trafią do kopii bez przesyłania danych.':
        'バックアップ元で移動されたファイル：{count} 個 — データを転送せずにバックアップに反映されます。',
    'Pliki skasowane w źródle: {count} — {action}.':
        'バックアップ元で削除されたファイル：{count} 個 — {action}。',
    'Pliki z końcówką dopisaną do nazwy, których oryginały zniknęły: {count}.':
        '名前の末尾に文字列が追加され、元のファイルが消えたファイル：{count} 個。',
    'Pliki zmienione w trakcie kopiowania: {count} — zostaną zapisane ponownie w przebiegu uzupełniającym.':
        'コピー中に変更されたファイル：{count} 個 — 追加取り込みで再度書き込まれます。',
    'Pliki, których brakuje w kopii i które zostaną zapisane ponownie: {count}.':
        'バックアップから欠けていて、再度書き込まれるファイル：{count} 個。',
    'Podpinanie niezmienionych plików do nowej wersji: {count}…':
        '変更のないファイルを新しいバージョンにリンクしています：{count} 個…',
    'Pomijam pliki, które już są w tej wersji kopii: {count}.':
        'このバックアップバージョンにすでにあるファイルをスキップします：{count} 個。',
    'Porządkowanie historii — usunięte najstarsze wersje: {count}.':
        '履歴の整理 — 削除した最も古いバージョン：{count} 個。',
    'Przenoszenie plików, które zmieniły miejsce w źródle: {count}…':
        'バックアップ元で場所が変わったファイルを移動しています：{count} 個…',
    'Próbne przywrócenie losowo wybranych plików: {count}…':
        'ランダムに選んだファイルをテスト復元しています：{count} 個…',
    'Usuwanie z kopii plików skasowanych w źródle: {count}…':
        'バックアップ元で削除されたファイルをバックアップから削除しています：{count} 個…',
    'Uzupełniam kopię o pliki, które przybyły lub zmieniły się w trakcie: {count} ({size})…':
        'バックアップ中に追加・変更されたファイルを取り込んでいます：{count} 個（{size}）…',
    'Uzupełnianie wersji {version} — pliki już zapisane, które zostaną pominięte: {count}.':
        'バージョン {version} の補完 — 書き込み済みのためスキップするファイル：{count} 個。',
    'Wznawiam wersję {version} — już zapisane: {done}, do dogrania: {todo}.':
        'バージョン {version} を再開しています — 書き込み済み：{done}、残り：{todo}。',
    'pliku':
        'ファイル',
    'Brak fragmentu {cid} w magazynie kopii.':
        'バックアップの断片の保管場所に断片 {cid} がありません。',
    'Brak opisu magazynu fragmentów w katalogu kopii.':
        'バックアップフォルダーに断片の保管場所の記述がありません。',
    'Duże pliki zapisuj różnicowo (od 256 MB)':
        '大きなファイルは差分で保存する（256 MB 以上）',
    'Fragment {cid} jest uszkodzony.':
        '断片 {cid} が破損しています。',
    'Kolejna wersja dużego pliku — maszyny wirtualnej, skrzynki pocztowej, bazy —\nzapisuje tylko zmienione fragmenty zamiast całego pliku. W kopii taki plik\nleży jako przepis + fragmenty; złoży go program albo skrypt ratunkowy.':
        '大きなファイル（仮想マシン、メールボックス、データベースなど）の次のバージョンでは、\nファイル全体ではなく変更された断片だけを保存します。バックアップ内のこうしたファイルは\nレシピと断片として保存され、プログラムまたは復旧用スクリプトで元に戻せます。',
    'Opis magazynu fragmentów jest uszkodzony.':
        '断片の保管場所の記述が破損しています。',
    'Plik złożony z fragmentów różni się od zapisanego w przepisie.':
        '断片から組み立てたファイルが、レシピに記録された内容と異なります。',
    'Podane hasło nie pasuje do fragmentów zapisanych wcześniej w tej kopii.':
        '入力したパスワードは、このバックアップに以前書き込まれた断片と一致しません。',
    'Przepis pliku jest uszkodzony.':
        'ファイルのレシピが破損しています。',
    'To nie jest przepis pliku zapisanego fragmentami.':
        '断片で保存されたファイルのレシピではありません。',
    'Usunięto nieużywane fragmenty dużych plików: {count} ({size}).':
        '大きなファイルの使われていない断片を削除しました：{count} 個（{size}）。',
    ', zakotwiczona w Bitcoinie':
        '、Bitcoin にアンカリング済み',
    'Adres usługi:':
        'サービスのアドレス：',
    'Brak fragmentu {cid} w kopii poza domem.':
        'オフサイトコピーに断片 {cid} がありません。',
    'Brak klucza albo hasła w Menedżerze poświadczeń Windows — zapisz ustawienia kopii poza domem jeszcze raz.':
        'Windows 資格情報マネージャーにキーまたはパスワードがありません — オフサイトコピーの設定をもう一度保存してください。',
    'Brak spisu wersji, którego dotyczy znacznik.':
        'タイムスタンプの対象となるファイル一覧がありません。',
    'Certyfikat PDF':
        'PDF 証明書',
    'Druga, zaszyfrowana kopia w usłudze zgodnej z S3 (np. Backblaze B2)':
        'S3 互換サービス（Backblaze B2 など）上の、暗号化された 2 つ目のコピー',
    'Folder w kubełku:':
        'バケット内のフォルダー：',
    'Hasło kopii poza domem':
        'オフサイトコピーのパスワード',
    'Hasło kopii poza domem nie pasuje do danych zapisanych w tym miejscu.':
        'オフサイトコピーのパスワードが、この場所に保存されたデータと一致しません。',
    'Hasło kopii poza domem powinno mieć co najmniej 10 znaków.':
        'オフサイトコピーのパスワードは 10 文字以上にしてください。',
    'Hasło szyfrowania:':
        '暗号化パスワード：',
    'Identyfikator klucza:':
        'キー ID：',
    'Katalog, do którego trafią pliki':
        'ファイルの復元先フォルダー',
    'Klucz tajny':
        'シークレットキー',
    'Klucz tajny:':
        'シークレットキー：',
    'Kopia na dysku obok komputera nie przetrwa pożaru ani kradzieży. Tu ustawisz drugą kopię w usłudze zgodnej z S3 (np. Backblaze B2). Pliki są szyfrowane na tym komputerze osobnym hasłem — usługa widzi tylko nieczytelne fragmenty.':
        'コンピューターのそばにあるドライブのバックアップは、火災や盗難には耐えられません。ここでは S3 互換サービス（Backblaze B2 など）に 2 つ目のコピーを設定します。ファイルはこのコンピューター上で別のパスワードによって暗号化されます — サービスから見えるのは読み取れない断片だけです。',
    'Kopia poza domem':
        'オフサイトコピー',
    'Kopia poza domem dla szablonu „{name}” zapisana.':
        'テンプレート「{name}」のオフサイトコピーの設定を保存しました。',
    'Kopia poza domem nie ruszyła':
        'オフサイトコピーを開始できませんでした',
    'Kopia poza domem potrzebuje Menedżera poświadczeń Windows, a jest on niedostępny.':
        'オフサイトコピーには Windows 資格情報マネージャーが必要ですが、利用できません。',
    'Kopia poza domem „{name}”':
        'オフサイトコピー「{name}」',
    'Kopia poza domem…':
        'オフサイトコピー…',
    'Korzeń tygodnia zakotwiczony w łańcuchu Bitcoina.':
        '週次ルートは Bitcoin のチェーンにアンカリングされています。',
    'Kubełek (bucket):':
        'バケット：',
    'Migawek w usłudze: {count}.':
        'サービス上のスナップショット：{count} 個。',
    'Migawka i cel':
        'スナップショットと復元先',
    'Migawka kopii poza domem jest uszkodzona.':
        'オフサイトコピーのスナップショットが破損しています。',
    'Migawka {stamp}: plików bez zmian {reused}, wysłanych {files}, nowych fragmentów {chunks} ({size}).':
        'スナップショット {stamp}：変更なしのファイル {reused} 個、送信したファイル {files} 個、新しい断片 {chunks} 個（{size}）。',
    'MinIO / Wasabi / inna zgodna z S3':
        'MinIO / Wasabi / その他の S3 互換サービス',
    'NIEPOPRAWNY':
        '無効',
    'Nie ma migawki {stamp} w kopii poza domem.':
        'オフサイトコピーにスナップショット {stamp} はありません。',
    'Nie udało się połączyć z usługą przechowywania: {error}':
        'ストレージサービスに接続できませんでした：{error}',
    'Nie udało się wczytać migawek: {error}':
        'スナップショットを読み込めませんでした：{error}',
    'Nie udało się zapisać klucza albo hasła w magazynie systemowym.':
        'キーまたはパスワードをシステムの保管場所に保存できませんでした。',
    'Odśwież z sieci':
        'オンラインで更新',
    'Opis kopii poza domem jest uszkodzony.':
        'オフサイトコピーの記述が破損しています。',
    'Oznakowana: {utc} (BeatTime {beat})':
        'タイムスタンプ：{utc}（BeatTime {beat}）',
    'Pliki wersji różnią się od spisu, który został oznakowany.':
        'バージョンのファイルが、タイムスタンプを付与したファイル一覧と異なります。',
    'Pobiera i odszyfrowuje pliki wybranej migawki':
        '選んだスナップショットのファイルをダウンロードして復号します',
    'Pobiera listę migawek z usługi':
        'サービスからスナップショットの一覧をダウンロードします',
    'Pobiera podpis tygodnia i stan kotwicy w Bitcoinie':
        '週の署名と Bitcoin のアンカーの状態をダウンロードします',
    'Pobieram potwierdzenia…':
        '受領証をダウンロードしています…',
    'Podaj hasło szyfrowania kopii poza domem.':
        'オフサイトコピーの暗号化パスワードを入力してください。',
    'Podaj klucz tajny usługi.':
        'サービスのシークレットキーを入力してください。',
    'Podam dane ręcznie':
        '手動で入力する',
    'Pominięte (otwarte w innych programach albo zmienione w trakcie): {count}.':
        'スキップ（他のプログラムで開かれていたか、処理中に変更されたファイル）：{count} 個。',
    'Porządkowanie kopii poza domem…':
        'オフサイトコピーを整理しています…',
    'Potwierdzenia odświeżone.':
        '受領証を更新しました。',
    'Poza dom':
        'オフサイト',
    'Połączenie działa: zapis, odczyt i usuwanie się udały.':
        '接続できました：書き込み、読み取り、削除のすべてに成功しました。',
    'Połączenie nie działa: {error}':
        '接続できません：{error}',
    'Przywraca pliki z zaszyfrowanej kopii w usłudze S3 — także na nowym komputerze':
        'S3 サービス上の暗号化されたコピーからファイルを復元します — 新しいコンピューターでも使えます',
    'Przywracanie z kopii poza domem':
        'オフサイトコピーからの復元',
    'Przywracanie {count} {files} z kopii poza domem…':
        'オフサイトコピーから {count} 個の{files}を復元しています…',
    'Przywróć':
        '復元',
    'Region:':
        'リージョン：',
    'Skąd':
        '復元元',
    'Spis wersji zgodny ze znacznikiem: {answer}':
        'ファイル一覧とタイムスタンプの一致：{answer}',
    'Spis wersji został zmieniony po oznakowaniu.':
        'ファイル一覧がタイムスタンプの付与後に変更されています。',
    'Sprawdza spis wersji, drogę w drzewie tygodnia i podpis — bez sieci':
        'ファイル一覧、週のツリー内の経路、署名を確認します — オフラインで',
    'Sprawdzam połączenie…':
        '接続を確認しています…',
    'Sprawdź':
        '確認',
    'Sprawdź połączenie':
        '接続を確認',
    'Starsze migawki są usuwane, gdy nadmiar sięgnie kilku — co kilka dni.':
        '古いスナップショットは、超過分がいくつか溜まったときに削除されます — 数日おきです。',
    'Suma w drzewie tygodnia: {answer}':
        '週のツリーにハッシュが含まれる：{answer}',
    'Suma wersji nie należy do drzewa tygodnia podanego w potwierdzeniu.':
        'バージョンのハッシュが、受領証に記載された週のツリーに含まれていません。',
    'Ta wersja nie ma znacznika czasu.':
        'このバージョンにはタイムスタンプがありません。',
    'Także po kopiach planowych. Wysyłane są tylko pliki nowe i zmienione.':
        'スケジュールバックアップの後にも送信します。送信するのは新規ファイルと変更されたファイルだけです。',
    'Tydzień jeszcze się nie zamknął — podpis pojawi się po poniedziałku 00:00 UTC.':
        '週はまだ締まっていません — 署名は月曜日 00:00 UTC を過ぎると追加されます。',
    'Usunięto starsze migawki: {count}, nieużywane fragmenty: {chunks}.':
        '古いスナップショット {count} 個と、使われていない断片 {chunks} 個を削除しました。',
    'Usługa chwilowo niedostępna ({status}).':
        'サービスは一時的に利用できません（{status}）。',
    'Usługa odrzuciła żądanie ({status} {code}): {message}':
        'サービスがリクエストを拒否しました（{status} {code}）：{message}',
    'Usługa przechowywania':
        'ストレージサービス',
    'Usługa zwróciła inną treść niż zapisana.':
        'サービスから、書き込んだ内容と異なるデータが返されました。',
    'Usługa:':
        'サービス：',
    'Uzupełnij adres usługi, nazwę kubełka i klucze dostępu.':
        'サービスのアドレス、バケット名、アクセスキーを入力してください。',
    'Uzupełnij adres usługi, region, kubełek i identyfikator klucza.':
        'サービスのアドレス、リージョン、バケット、キー ID を入力してください。',
    'W tym katalogu kopii nie ma jeszcze znaczników czasu.':
        'このバックアップフォルダーにはまだタイムスタンプがありません。',
    'W tym miejscu nie ma jeszcze kopii poza domem.':
        'この場所にはまだオフサイトコピーがありません。',
    'Wczytaj migawki':
        'スナップショットを読み込む',
    'Wczytaj migawki i wybierz jedną z listy.':
        'スナップショットを読み込み、一覧から 1 つ選んでください。',
    'Wczytuję migawkę {stamp}…':
        'スナップショット {stamp} を読み込んでいます…',
    'Wczytuję poprzednią migawkę kopii poza domem…':
        'オフサイトコピーの前回のスナップショットを読み込んでいます…',
    'Wybierz migawkę i katalog, do którego trafią pliki.':
        'スナップショットと、ファイルの復元先フォルダーを選んでください。',
    'Wybierz wersję z listy.':
        '一覧からバージョンを選んでください。',
    'Wysyłaj poza dom po każdej udanej kopii z tego szablonu':
        'このテンプレートのバックアップが成功するたびにオフサイトへ送信する',
    'Wysyłam poza dom pliki nowe i zmienione: {count}…':
        '新規ファイルと変更されたファイルをオフサイトへ送信しています：{count} 個…',
    'Z kopii poza domem…':
        'オフサイトコピーから…',
    'Zachowuj migawek:':
        '保持するスナップショット数：',
    'Zapisuje ustawienia; klucz i hasło trafiają do Menedżera poświadczeń Windows':
        '設定を保存します。キーとパスワードは Windows 資格情報マネージャーに保存されます',
    'Zapisuje, odczytuje i usuwa mały plik próbny':
        '小さなテストファイルを書き込み、読み取り、削除します',
    'Zapisuję migawkę {stamp}…':
        'スナップショット {stamp} を保存しています…',
    'Znacznik dowodzi, że wersja kopii w dokładnie tym kształcie istniała w podanej chwili. Podpis tygodnia pojawia się po jego zamknięciu (poniedziałek 00:00 UTC), a kotwica w Bitcoinie — zwykle kilka godzin później.':
        'タイムスタンプは、バックアップバージョンがまさにこの状態で指定の時点に存在したことを証明します。週の署名は週が締まった後（月曜日 00:00 UTC）に、Bitcoin のアンカーは通常その数時間後に追加されます。',
    'Znacznika czasu nie udało się zapisać: {error}':
        'タイムスタンプを保存できませんでした：{error}',
    'Znaczniki czasu':
        'タイムスタンプ',
    'Znaczniki czasu…':
        'タイムスタンプ…',
    'kopia poza domem':
        'オフサイトコピー',
    'np. komputer-domowy':
        '例：home-pc',
    'oznakowana {when} — podpis po zamknięciu tygodnia':
        '{when} にタイムスタンプ付与 — 署名は週が締まった後',
    'podpisana (tydzień {week}){bitcoin}':
        '署名済み（週 {week}）{bitcoin}',
    'poprawny':
        '有効',
    'przywracanie z kopii poza domem':
        'オフサイトコピーからの復元',
    'Łączę się z usługą…':
        'サービスに接続しています…',
    ' dni':
        ' 日',
    ' mies.':
        ' か月',
    ' tyg.':
        ' 週',
    'Ile ostatnich wersji zachować. Starsze są kasowane po udanym przebiegu.':
        '保持する最新バージョンの数。古いものは実行が成功した後に削除されます。',
    'Kalendarz zostawia najnowszą wersję z każdego z ostatnich dni, tygodni\ni miesięcy — gęsto dla świeżych zmian, rzadko dla dawnych. Nadmiar jest\nkasowany po udanym przebiegu; wersje niedokończone nigdy.':
        'カレンダーでは、直近の各日・各週・各月から最新のバージョンを 1 つずつ\n残します — 最近の変更は細かく、古い変更はまばらに。超過分は\n実行が成功した後に削除されますが、未完了のバージョンは削除されません。',
    'Z ilu ostatnich dni zachować po jednej, najnowszej wersji.':
        '最新バージョンを 1 つずつ残す直近の日数。',
    'Z ilu ostatnich miesięcy zachować po jednej, najnowszej wersji.':
        '最新バージョンを 1 つずつ残す直近の月数。',
    'Z ilu ostatnich tygodni zachować po jednej, najnowszej wersji.':
        '最新バージョンを 1 つずつ残す直近の週数。',
    'Zachowuj:':
        '保持：',
    'kalendarz: dni, tygodnie, miesiące':
        'カレンダー：日・週・月',
    'ostatnie wersje':
        '最新のバージョン',
    'wszystkie wersje':
        'すべてのバージョン',
    ' (niedokończona)':
        ' （未完了）',
    'Fragment nazwy albo ścieżki, bez rozróżniania wielkości liter.':
        '名前またはパスの一部（大文字と小文字は区別しません）。',
    'Główny folder kopii':
        'バックアップのメインフォルダー',
    'Historia pliku':
        'ファイルの履歴',
    'Nazwa':
        '名前',
    'Nic nie znaleziono.':
        '見つかりませんでした。',
    'Nie udało się: {error}':
        '失敗しました：{error}',
    'Odtwarza plik do katalogu tymczasowego i otwiera go':
        'ファイルを一時フォルダーに復元して開きます',
    'Odtwarza plik w wybranym miejscu':
        'ファイルを指定した場所に復元します',
    'Odtwarzam „{name}”…':
        '「{name}」を復元しています…',
    'Otwarto kopię „{name}” (plik tymczasowy, zniknie po zamknięciu programu).':
        '「{name}」のコピーを開きました（一時ファイルのため、プログラムを閉じると削除されます）。',
    'Otwórz':
        '開く',
    'Otwórz kopię':
        'コピーを開く',
    'Pliki i wersje wprost z kopii — bez przywracania':
        'バックアップのファイルとバージョンを直接表示 — 復元は不要',
    'Pliki i wersje wprost z kopii — bez przywracania całości.':
        'バックアップのファイルとバージョンを直接表示します — 全体を復元する必要はありません。',
    'Pokazuje pliki i wersje tej kopii — pojedynczy plik otworzysz bez przywracania całości':
        'このバックアップのファイルとバージョンを表示します — 全体を復元せずに個々のファイルを開けます',
    'Pokaż foldery':
        'フォルダーを表示',
    'Przeglądaj…':
        '閲覧…',
    'Przeglądanie':
        '閲覧',
    'Przeszukuje spis treści kopii':
        'バックアップの目次を検索します',
    'Rozmiar':
        'サイズ',
    'Szukaj':
        '検索',
    'Szukaj pliku w najnowszym stanie kopii…':
        'バックアップの最新の状態からファイルを検索…',
    'Szukam…':
        '検索しています…',
    'W których wersjach jest ten plik i kiedy się zmieniał':
        'このファイルを含むバージョンと、変更された日時',
    'W tym folderze nie ma wersji kopii.':
        'このフォルダーにはバックアップバージョンがありません。',
    'Wczytuje wersje z tego folderu kopii':
        'このバックアップフォルダーからバージョンを読み込みます',
    'Wersja kopii, której zawartość widzisz poniżej.':
        '下に内容が表示されているバックアップバージョン。',
    'Wersja: {version}':
        'バージョン：{version}',
    'Wersje z tym plikiem: {count}. Dwuklik otwiera kopię z danej wersji.':
        'このファイルを含むバージョン：{count} 個。ダブルクリックすると、そのバージョンのコピーが開きます。',
    'Wraca z wyników wyszukiwania do drzewa folderów':
        '検索結果からフォルダーツリーに戻ります',
    'Wskaż folder kopii i kliknij „Otwórz”.':
        'バックアップフォルダーを指定し、「開く」をクリックしてください。',
    'Zapisano: {path}':
        '保存しました：{path}',
    'Zapisz jako…':
        '名前を付けて保存…',
    'Zapisz kopię pliku':
        'ファイルのコピーを保存',
    'Zaznacz plik i wybierz „Otwórz kopię”, żeby zajrzeć do niego w zwykłym programie, albo „Historia pliku”, żeby zobaczyć, w których wersjach się zmieniał.':
        'ファイルを選んで「コピーを開く」を選ぶと通常のプログラムで内容を確認でき、「ファイルの履歴」を選ぶとどのバージョンで変更されたかを確認できます。',
    'Zmieniono':
        '更新日時',
    'Znalezione pliki: {count}. Wyniki pochodzą z najnowszego stanu kopii.':
        '見つかったファイル：{count} 個。結果はバックアップの最新の状態に基づいています。',
    'przeglądanie kopii':
        'バックアップの閲覧',
    'zmieniony':
        '変更あり',
    'najstarsza zachowana kopia':
        '保持されている最古のコピー',
    'Foldery w AppData':
        'AppData 内のフォルダー',
    'Przywracanie utworzy nowe foldery bezpośrednio w AppData:\n\n{folders}\n\nWindows pozwala wersji programu ze Sklepu tworzyć je tylko w jej prywatnej kopii — pliki będą widoczne w tym programie, ale nie w programie, do którego należą.\n\nNajprościej: zainstaluj i raz uruchom tamten program (utworzy swój folder), a potem przywróć jeszcze raz. Albo przywróć do zwykłego folderu i przenieś pliki Eksploratorem.':
        '復元すると、AppData の直下に新しいフォルダーが作成されます：\n\n{folders}\n\nWindows では、Microsoft Store 版のプログラムはこれらのフォルダーを自身の専用コピーの中にしか作成できません — ファイルはこのプログラムからは見えますが、本来のプログラムからは見えません。\n\n最も簡単な方法：そのプログラムをインストールして一度起動し（自分のフォルダーが作成されます）、もう一度復元してください。または、通常のフォルダーに復元してから、エクスプローラーでファイルを移動してください。',
    'Przywracanie utworzyłoby w AppData nowe foldery, których inne programy nie zobaczą: {folders}':
        '復元すると、他のプログラムからは見えない新しいフォルダーが AppData に作成されます：{folders}',
    'Przywracanie wstrzymane do decyzji.':
        '判断を待つため、復元を一時停止しました。',
    'Przywróć mimo to':
        'それでも復元',
    'Start programu przy logowaniu wyłączono w Ustawieniach Windows. Włączysz go tam: Ustawienia → Aplikacje → Uruchamianie → Sigelith Backup.':
        'サインイン時のプログラムの起動は、Windows の設定でオフにされています。オンにするには：設定 → アプリ → スタートアップ → Sigelith Backup。',
    'Start przy logowaniu':
        'サインイン時の起動',
    'Start przy logowaniu wyłączono w Ustawieniach Windows → Aplikacje → Uruchamianie; dopóki go tam nie włączysz, kopie planowe działają tylko przy otwartym programie.':
        'サインイン時の起動は Windows の設定 → アプリ → スタートアップでオフにされています。そこでオンにするまで、スケジュールバックアップはプログラムを開いている間だけ動作します。',
    'Ten sam przełącznik jest w Ustawieniach Windows → Aplikacje → Uruchamianie. Wyłączony tam da się włączyć tylko tam.':
        '同じスイッチが Windows の設定 → アプリ → スタートアップにもあります。そこでオフにした場合は、そこでしかオンに戻せません。',
    'Brak pliku {name} w katalogu programu.':
        'プログラムのフォルダーにファイル {name} がありません。',
    'Jakie dane program przetwarza i gdzie':
        'プログラムが扱うデータとその場所',
    'Kod źródłowy Qt':
        'Qt のソースコード',
    'Licencja programu':
        'プログラムのライセンス',
    'Licencja programu i licencje użytych składników':
        'プログラムのライセンスと、使用しているコンポーネントのライセンス',
    'Licencje':
        'ライセンス',
    'Licencje i prywatność':
        'ライセンスとプライバシー',
    'Licencje…':
        'ライセンス…',
    'Otwiera folder z plikami licencji w Eksploratorze':
        'ライセンスファイルのフォルダーをエクスプローラーで開きます',
    'Pokaż pliki licencji':
        'ライセンスファイルを表示',
    'Polityka prywatności':
        'プライバシーポリシー',
    'Polityka prywatności…':
        'プライバシーポリシー…',
    'Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0 — to osobne pliki w katalogu programu, które można zastąpić zgodnymi wersjami. Kod źródłowy wersji dołączonych do programu: {qt} oraz {pyside}.':
        'このプログラムは LGPL-3.0 ライセンスの Qt と PySide6 のライブラリを使用しています — これらはプログラムのフォルダー内の独立したファイルで、互換性のあるバージョンに置き換えることができます。プログラムに同梱されているバージョンのソースコード：{qt} および {pyside}。',
    'Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0, z Pythona i z innych składników na licencjach otwartych (m.in. MIT, BSD, Apache 2.0); ikony: Bootstrap Icons (MIT). Wykaz, prawa autorskie, pełne teksty licencji i adresy kodu źródłowego Qt są pod przyciskiem „Licencje”.':
        'このプログラムは、LGPL-3.0 ライセンスの Qt と PySide6 のライブラリ、Python、およびオープンソースライセンス（MIT、BSD、Apache 2.0 など）のその他のコンポーネントを使用しています。アイコン：Bootstrap Icons（MIT）。一覧、著作権表示、ライセンスの全文、Qt のソースコードの入手先は「ライセンス」ボタンから確認できます。',
    'Program usunie z Menedżera poświadczeń Windows wszystkie hasła, które zapamiętał: hasła kopii i dane dostępu do kopii poza domem. Kopie planowe szablonów zaszyfrowanych będą potem czekać, aż podasz hasło.\n\nUsunąć?':
        'プログラムが保存したすべてのパスワード（バックアップのパスワードとオフサイトコピーの認証情報）を Windows 資格情報マネージャーから削除します。その後、暗号化したテンプレートのスケジュールバックアップは、パスワードを入力するまで待機します。\n\n削除しますか？',
    'Składniki i ich licencje':
        'コンポーネントとそのライセンス',
    'Strona z kodem źródłowym Qt w wersji użytej w programie':
        'プログラムで使用しているバージョンの Qt のソースコードのページ',
    'Usunięte zapamiętane hasła: {count}.':
        '保存済みのパスワードを削除しました：{count} 件。',
    'Usuwa z Menedżera poświadczeń Windows wszystkie hasła zapamiętane przez program — na przykład przed odinstalowaniem':
        'プログラムが保存したすべてのパスワードを Windows 資格情報マネージャーから削除します — アンインストールの前などに',
    'Usuń zapamiętane hasła':
        '保存済みのパスワードを削除',
    'Usuń zapamiętane hasła…':
        '保存済みのパスワードを削除…',
    '© {years} {publisher}. Wolne oprogramowanie na licencji GNU GPL w wersji 3 lub nowszej.':
        '© {years} {publisher}。GNU GPL バージョン 3 以降のライセンスによる自由ソフトウェアです。',
    'Kod źródłowy':
        'ソースコード',
    'Kod źródłowy programu w serwisie GitHub':
        'GitHub 上のプログラムのソースコード',
    'Sigelith odrzucił żądanie ({status}): {detail}':
        'Sigelith がリクエストを拒否しました（{status}）：{detail}',
    'Nie udało się połączyć z Sigelith: {error}':
        'Sigelith に接続できませんでした：{error}',
    'Sigelith odesłał potwierdzenie innej sumy kontrolnej.':
        'Sigelith から、別のハッシュに対する受領証が返されました。',
    'Znacznik czeka na połączenie z Sigelith.':
        'タイムスタンプは Sigelith への接続を待っています。',
    'Podpis tygodnia nie zgadza się z kluczem Sigelith zapisanym w programie.':
        '週の署名が、プログラムに組み込まれた Sigelith の鍵と一致しません。',
    'Otwiera certyfikat znacznika na stronie Sigelith':
        'Sigelith のウェブサイトでタイムスタンプ証明書を開きます',
    'Podpis Sigelith: {answer}':
        'Sigelith の署名：{answer}',
    'Znaczniki Sigelith wersji w tym katalogu kopii: sprawdzenie i certyfikat':
        'このバックアップフォルダー内のバージョンの Sigelith タイムスタンプ：確認と証明書',
    'Znakuję wersję czasem Sigelith (wysyłana jest tylko suma kontrolna)…':
        'Sigelith でバージョンにタイムスタンプを付与しています（送信するのはハッシュだけです）…',
    'Znacznik czasu czeka na połączenie z Sigelith — zostanie wysłany przy następnej kopii.':
        'タイムスタンプは Sigelith への接続を待っています — 次回のバックアップ時に送信されます。',
    'Znakuj wersję czasem Sigelith':
        'Sigelith でバージョンにタイムスタンプを付与する',
    'Znaczniki czasu Sigelith':
        'Sigelith のタイムスタンプ',
    'czeka na połączenie z Sigelith':
        'Sigelith への接続待ち',
    'Dowód, że kopia w tym kształcie istniała danego dnia (podpis Ed25519, kotwica\nw Bitcoinie). Do sigelith.org trafia wyłącznie suma kontrolna spisu wersji —\nżadne nazwy plików ani ich treść.':
        'バックアップがこの状態でその日に存在したことの証明です\n（Ed25519 署名、Bitcoin のアンカー）。sigelith.org に送られるのはバージョンのファイル一覧の\nハッシュだけで、ファイル名や内容は一切送られません。',
    'Kopie zapasowe folderów na dysk zewnętrzny, z historią wersji i szyfrowaniem. Wszystko dzieje się na Twoim komputerze, bez konta i bez telemetrii. Z internetem program łączy się tylko wtedy, gdy sam włączysz kopię poza domem albo znaczniki czasu Sigelith.':
        'フォルダーを外付けドライブにバックアップします。バージョン履歴と暗号化に対応しています。すべての処理はあなたのコンピューター上で行われ、アカウントもテレメトリーもありません。プログラムがインターネットに接続するのは、オフサイトコピーまたは Sigelith のタイムスタンプをあなた自身がオンにしたときだけです。',
    'Bez dokumentu: {count} {stamps} — plik zmienił się po stemplu albo zniknął i nie ma go w żadnej wersji tej kopii ({names}). Sam dowód jest zachowany.':
        '文書なし：{count} 件の{stamps} — タイムスタンプの付与後にファイルが変更されたか削除され、このバックアップのどのバージョンにもありません（{names}）。証明そのものは保持されています。',
    'Brak pliku dowodu albo dowód jest zaszyfrowany.':
        '証明ファイルがないか、証明が暗号化されています。',
    'Chroni dowody Sigelith: historię stempli i oznakowane dokumenty.':
        'Sigelith の証拠（タイムスタンプの履歴と、タイムスタンプを付与した文書）を保護します。',
    'Chroń dowody Sigelith':
        'Sigelith の証拠を保護',
    'Chroń też dowody Sigelith':
        'Sigelith の証拠も保護する',
    'Dokument':
        '文書',
    'Dokumenty oznakowane w Sigelith, zabezpieczone w tej kopii: sprawdzenie i odzyskanie':
        'このバックアップで保護している、Sigelith でタイムスタンプを付与した文書：確認と復元',
    'Dowody Sigelith':
        'Sigelith の証拠',
    'Dowody Sigelith: historia stempli i dokładne kopie oznakowanych dokumentów z plikami .beatproof trafią do magazynu dowodów w katalogu kopii.':
        'Sigelith の証拠：タイムスタンプの履歴と、タイムスタンプを付与した文書の正確なコピーが .beatproof ファイルとともに、バックアップフォルダー内の証拠の保管場所に保存されます。',
    'Dowody Sigelith: zabezpieczone dokumenty {count} z {total}':
        'Sigelith の証拠：保護済みの文書 {count}/{total}',
    'Dowody Sigelith…':
        'Sigelith の証拠…',
    'Dowody z problemem: {count} — szczegóły w kolumnie „Stan”.':
        '問題のある証明：{count} 件 — 詳細は「状態」列を参照してください。',
    'Dowodów Sigelith nie udało się zabezpieczyć: {error}':
        'Sigelith の証拠を保護できませんでした：{error}',
    "Droga w drzewie Merkle'a nie prowadzi do podpisanego korzenia tygodnia.":
        'マークルツリー内の経路が、署名済みの週次ルートにたどり着きません。',
    'Gdzie zapisać dokumenty i dowody':
        '文書と証明の保存先を選択',
    'Historia stempli Sigelith Desktop i dokładne bajty oznakowanych dokumentów, z plikami .beatproof — w osobnym magazynie, którego retencja nie sprząta.':
        'Sigelith Desktop のタイムスタンプ履歴と、タイムスタンプを付与した文書の正確なバイト列を .beatproof ファイルとともに保存します — 保持ルールによる整理の対象にならない専用の保管場所に。',
    'Każdy stempel ma tu swój folder z dokładnie tym dokumentem, który oznakowano, i plikiem .beatproof. „Sprawdź” liczy sumę każdego dokumentu i sprawdza podpis tygodnia bez łączenia się z siecią.':
        'タイムスタンプごとにフォルダーがあり、タイムスタンプを付与したときの文書そのものと .beatproof ファイルが入っています。「確認」は各文書のハッシュを計算し、ネットワークに接続せずに週の署名を検証します。',
    'Kopia obejmie folder danych Sigelith Desktop (historię stempli), a każdy oznakowany\ndokument trafi — dokładnie w tej postaci, którą oznakowano — do magazynu dowodów\nw katalogu kopii, razem z plikiem .beatproof. Starych wersji magazyn nie dotyczy:\nretencja go nie sprząta.':
        'Sigelith Desktop のデータフォルダー（タイムスタンプの履歴）もバックアップの対象になり、タイムスタンプを付与した\n各文書は、付与したときとまったく同じ状態で .beatproof ファイルとともに、バックアップフォルダー内の\n証拠の保管場所に保存されます。この保管場所は古いバージョンとは別で、\n保持ルールによって整理されることはありません。',
    'Magazyn dowodów jest pusty.':
        '証拠の保管場所は空です。',
    'Na tym komputerze jest Sigelith Desktop: {count} {stamps}.':
        'このコンピューターには Sigelith Desktop があります：{count} 件の{stamps}。',
    'Na tym komputerze nie ma danych Sigelith Desktop.':
        'このコンピューターには Sigelith Desktop のデータがありません。',
    'Otwórz folder dowodów':
        '証拠フォルダーを開く',
    'Oznakowano':
        '付与日時',
    'Pokazuje magazyn dowodów w Eksploratorze':
        '証拠の保管場所をエクスプローラーで表示します',
    'Przywróć zaznaczone…':
        '選択項目を復元…',
    'Sigelith Desktop: {count} {stamps} w folderze {path}.':
        'Sigelith Desktop：フォルダー {path} に {count} 件の{stamps}。',
    'Sprawdza każdy dokument i jego dowód bez łączenia z siecią':
        'ネットワークに接続せずに、各文書とその証明を確認します',
    'Sprawdzam dowody…':
        '証明を確認しています…',
    'Stan':
        '状態',
    'Stemple w magazynie: {count}, z dokumentem: {documents}.':
        '保管場所のタイムスタンプ：{count} 件、うち文書あり：{documents} 件。',
    'Suma dokumentu nie zgadza się z dowodem.':
        '文書のハッシュが証明と一致しません。',
    'To nie jest plik dowodu Sigelith (beatproof-v1).':
        'Sigelith の証明ファイル（beatproof-v1）ではありません。',
    'Tydzień stempla jeszcze się nie zamknął — podpis dojdzie przy kolejnej kopii.':
        'タイムスタンプの週はまだ締まっていません — 署名は次回以降のバックアップで追加されます。',
    'W magazynie nie ma dokumentu do tego dowodu.':
        '保管場所にこの証明の文書がありません。',
    'Wszystkie dowody pasują do dokumentów i mają poprawny podpis.':
        'すべての証明が文書と一致し、署名も有効です。',
    'Zabezpieczam dokumenty oznakowane w Sigelith…':
        'Sigelith でタイムスタンプを付与した文書を保護しています…',
    'Zapisano pliki: {count} w {path}.':
        '{path} にファイルを {count} 個保存しました。',
    'Zapisuje dokumenty razem z plikami .beatproof we wskazanym folderze':
        '文書を .beatproof ファイルとともに、指定したフォルダーに保存します',
    'bez dokumentu — dowód zachowany':
        '文書なし — 証明は保持',
    'czekają na podpis tygodnia: {count}':
        '週の署名待ち：{count}',
    'dokument i dowód są w kopii':
        '文書と証明はバックアップ済み',
    'dokument jest; dowód czeka na podpis tygodnia':
        '文書あり、証明は週の署名待ち',
    'dowodu nie da się odczytać':
        '証明を読み取れません',
    'dowody Sigelith':
        'Sigelith の証拠',
    'dowody uzupełnione o podpis tygodnia: {count}':
        '週の署名を追加した証明：{count}',
    'nowe: {count}':
        '新規：{count}',
    'odtworzone ze starszych wersji kopii: {count}':
        '古いバックアップバージョンから復元：{count}',
    'sprawdzony: dokument i dowód się zgadzają':
        '確認済み：文書と証明が一致',
    'stempel':
        'タイムスタンプ',
    'stemple':
        'タイムスタンプ',
    'stempli':
        'タイムスタンプ',
    'zaszyfrowany — podaj hasło, żeby sprawdzić':
        '暗号化済み — 確認するにはパスワードを入力してください',
    'Chroń dowody Sigelith, gdy go zainstaluję':
        'Sigelith Desktop をインストールしたら Sigelith の証拠を保護する',
    'Dowody Sigelith: na tym komputerze nie ma jeszcze Sigelith Desktop — ochrona zacznie działać sama, gdy się pojawi.':
        'Sigelith の証拠：このコンピューターにはまだ Sigelith Desktop がありません — インストールされると保護が自動的に始まります。',
    'Dowody Sigelith: ochrona zacznie działać sama, gdy zainstalujesz Sigelith Desktop.':
        'Sigelith の証拠：Sigelith Desktop をインストールすると、保護が自動的に始まります。',
    'Dowody czasu dla ważnych dokumentów':
        '重要な文書の時刻の証明',
    'Kopia zachowa każdy dokument oznakowany w Sigelith Desktop dokładnie w tej postaci, którą oznakowano, razem z dowodem — nawet gdy oryginał później się zmieni.':
        'Sigelith Desktop でタイムスタンプを付与した各文書を、付与したときとまったく同じ状態で証明とともにバックアップに残します — 後で元のファイルが変更されても失われません。',
    'Ochrona zacznie działać sama, gdy na komputerze pojawi się Sigelith Desktop.':
        'このコンピューターに Sigelith Desktop がインストールされると、保護が自動的に始まります。',
    'Otwiera stronę programu Sigelith Desktop':
        'Sigelith Desktop のページを開きます',
    'Poznaj Sigelith Desktop':
        'Sigelith Desktop について',
    'Sigelith Desktop, program tego samego wydawcy, oznakuje dokument czasem: to podpisany dowód, że plik w tej postaci istniał w danej chwili, sprawdzalny bez udziału kogokolwiek. Sigelith Backup przechowa potem każdy oznakowany dokument razem z dowodem.':
        '同じ発行元のプログラム Sigelith Desktop は、文書にタイムスタンプを付与します。これは、ファイルがその時点でその状態のまま存在したことを示す署名付きの証明で、誰にも頼らずに検証できます。さらに Sigelith Backup が、タイムスタンプを付与した各文書を証明とともに保管します。',
    'Umowy, faktury, projekty — czasem trzeba wykazać, że dokument istniał danego dnia.':
        '契約書、請求書、プロジェクト資料 — ある日に文書が存在したことを示す必要が生じることがあります。',
    'Nieznany format spisu wersji.':
        'ファイル一覧の形式が不明です。',
    'Ta wersja nie ma pieczęci dla pojedynczych plików (kopia sprzed wersji 3.0 albo bez znaczników czasu).':
        'このバージョンには個々のファイル用の封印がありません（バージョン 3.0 より前のバックアップか、タイムスタンプを使っていないバックアップです）。',
    'Pieczęć tej wersji czeka jeszcze na podpis tygodnia Sigelith — dowód będzie gotowy po poniedziałku 00:00 UTC i kolejnej kopii.':
        'このバージョンの封印は、まだ Sigelith の週の署名を待っています — 証明は、月曜日 00:00 UTC を過ぎて次のバックアップを実行した後に用意できます。',
    'Brak oświadczenia pieczęci w folderze wersji.':
        'バージョンのフォルダーに封印の宣言がありません。',
    'Oświadczenie pieczęci nie zgadza się z pieczęcią wersji.':
        '封印の宣言がバージョンの封印と一致しません。',
    'Drzewo plików wersji nie zgadza się z pieczęcią.':
        'バージョンのファイルツリーが封印と一致しません。',
    'Tego pliku nie ma w spisie tej wersji.':
        'このファイルは、このバージョンのファイル一覧にありません。',
    'To nie jest dowód pliku z kopii Sigelith Backup ({format}).':
        'Sigelith Backup のファイル証明ではありません（{format}）。',
    'Dowód jest uszkodzony — brakuje pól albo mają zły format.':
        '証明が壊れています — 項目が欠けているか、形式が正しくありません。',
    'Ten plik nie jest plikiem, którego dotyczy dowód.':
        'このファイルは、証明の対象のファイルではありません。',
    'Ścieżka pliku w dowodzie nie zgadza się z liściem drzewa.':
        '証明内のファイルパスがツリーの葉と一致しません。',
    'Droga w drzewie plików nie prowadzi do korzenia z pieczęci.':
        'ファイルツリー内の経路が、封印されたルートにたどり着きません。',
    'Oświadczenie pieczęci nie potwierdza tego drzewa plików.':
        '封印の宣言がこのファイルツリーを裏付けていません。',
    'Potwierdzenie Sigelith nie dotyczy tej pieczęci.':
        'Sigelith の確認は、この封印に対するものではありません。',
    'Dowód czasu…':
        '時刻の証明…',
    'Zapisuje dowód, że ten plik był w kopii w chwili jej oznakowania — bez ujawniania innych plików':
        'このファイルがタイムスタンプ付与の時点でバックアップに含まれていたことの証明を保存します — 他のファイルは明かしません',
    'Dowód czasu':
        '時刻の証明',
    'Dołączyć do dowodu ścieżkę pliku w kopii („{path}”)?\n\nBez niej dowód dalej potwierdza plik i chwilę oznakowania, ale nie mówi, gdzie plik leżał.':
        'バックアップ内のファイルのパス（「{path}」）を証明に含めますか？\n\nパスを含めなくても、証明はファイルとタイムスタンプの時刻を裏付けますが、ファイルがどこにあったかは示しません。',
    'Przygotowuję dowód dla „{name}”…':
        '「{name}」の証明を準備しています…',
    'Zapisz dowód czasu':
        '時刻の証明を保存',
    'Dowód pliku Sigelith (*{suffix})':
        'Sigelith のファイル証明 (*{suffix})',
    'Zapisano dowód i certyfikat PDF: {path}. Sprawdzi go Sigelith Desktop albo strona sigelith.org/verify/.':
        '証明と PDF 証明書を保存しました：{path}。Sigelith Desktop または sigelith.org/verify/ で確認できます。',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją sprawdzić.':
        'バックアップは暗号化されています — 確認するにはパスワードを入力してください。',
    'Ta wersja nie ma pieczęci — nie ma z czym porównać plików.':
        'このバージョンには封印がありません — ファイルを比較する対象がありません。',
    'Pieczęć wersji się nie potwierdza: {problems}':
        'バージョンの封印を確認できません：{problems}',
    'brak podpisu tygodnia':
        '週の署名なし',
    'Audyt przerwany.':
        '監査を中止しました。',
    'próbka {checked} z {listed} plików':
        '{listed} 個中 {checked} 個のファイルのサンプル',
    'wszystkie pliki ({count})':
        'すべてのファイル（{count} 個）',
    'Nietknięta: sprawdzono {scope}, wszystko zgodne z pieczęcią w publicznym dzienniku.':
        '改ざんなし：{scope}を確認し、すべて公開ログの封印と一致しました。',
    'zmienione: {files}':
        '変更：{files}',
    'brakujące: {files}':
        '欠落：{files}',
    'nieczytelne albo uszkodzone: {files}':
        '読み取り不能または破損：{files}',
    'PODMIENIONA albo uszkodzona ({scope}) — {details}.':
        '改ざんまたは破損あり（{scope}）— {details}。',
    'Audyt treści':
        '内容監査',
    'Czyta z nośnika każdy plik tej wersji i porównuje go z sumą oznakowaną w publicznym dzienniku':
        'このバージョンのすべてのファイルをメディアから読み込み、公開ログに封印されたハッシュと照合します',
    'Ostatnia nietknięta':
        '改ざんのない最新版',
    'Sprawdza wersje od najnowszej i wskazuje ostatnią zgodną z pieczęcią — z niej przywracaj':
        '新しいバージョンから順に確認し、封印と一致する最新のバージョンを示します — そこから復元してください',
    'Ostatnia nietknięta wersja: {label} — z niej przywracaj.':
        '改ざんのない最新バージョン：{label} — ここから復元してください。',
    'Żadna wersja z pieczęcią nie jest nietknięta.':
        '封印のあるバージョンのうち、改ざんのないものはありません。',
    'Czytam pliki kopii i porównuję je z pieczęcią w publicznym dzienniku…':
        'バックアップのファイルを読み込み、公開ログの封印と照合しています…',
    'Sprawdzam próbkę starszej wersji z pieczęcią w publicznym dzienniku…':
        '古いバージョンのサンプルを公開ログの封印と照合しています…',
    'Audyt z pieczęcią: próbka wersji {label} zgodna z publicznym dziennikiem.':
        '封印監査：バージョン {label} のサンプルは公開ログと一致しています。',
    'UWAGA — audyt z pieczęcią, wersja {label}: {details}':
        '警告 — 封印監査、バージョン {label}：{details}',
    'Przekaż…':
        '引き渡す…',
    'Zapisuje tę wersję pliku i otwiera ją w Sigelith Handover — odbiorca potwierdzi odbiór własnym kluczem':
        'このバージョンのファイルを保存し、Sigelith Handover で開きます — 受取人は自分の鍵で受領を確認します',
    'Przekazanie z dowodem doręczenia':
        '引き渡しの証明付きで渡す',
    'Przekazanie z dowodem doręczenia robi Sigelith Desktop (od wersji 3.0.1): odbiorca potwierdza odbiór własnym kluczem, a chwila doręczenia trafia do publicznego dziennika. Na tym komputerze go nie ma albo jest w starszej wersji. Otworzyć stronę programu?':
        '引き渡しの証明付きの受け渡しは、Sigelith Desktop（バージョン 3.0.1 以降）が行います。受取人が自分の鍵で受領を確認し、引き渡しの時刻が公開ログに記録されます。このコンピューターには Sigelith Desktop がないか、古いバージョンです。プログラムのページを開きますか？',
    'Zapisz plik do przekazania':
        '引き渡すファイルを保存',
    'Otwieram Sigelith Handover z plikiem „{name}” — wybierz odbiorcę.':
        '「{name}」を Sigelith Handover で開いています — 受取人を選んでください。',
    'Kapsuły czasu…':
        'タイムカプセル…',
    'Pliki zapieczętowane w tej kopii do daty — klucze wydają dopiero po niej sieć drand i serwer kluczy Sigelith':
        'このバックアップ内で指定日まで封印されたファイル — 鍵は、その日を過ぎてから drand ネットワークと Sigelith の鍵サーバーが公開します',
    'Wskaż najpierw folder kopii — kapsuła leży w kopii.':
        '先にバックアップフォルダーを指定してください — カプセルはバックアップ内に保存されます。',
    'Kapsuły czasu':
        'タイムカプセル',
    'Kapsuła pieczętuje wybrany folder do chwili, którą wskażesz. Otwierają ją dowolne dwie z trzech części: runda sieci drand z tej chwili, udział serwera kluczy Sigelith (wydawany dopiero po tej chwili — to zasada operatora, nie kryptografia) i kod odzyskiwania zapisany obok kapsuły. Kto ma tę kopię, ma więc i kod: do wcześniejszego otwarcia wystarczy mu, że operator złamie swoją zasadę. Po tej chwili otworzy ją każdy, kto ma jej pliki. Kapsuła leży w tej kopii, nie na serwerze; otwiera ją strona sigelith.org/capsule/.':
        'カプセルは、選んだフォルダーを指定した時刻まで封印します。開くには 3 つの要素のうち任意の 2 つが必要です：その時刻の drand ネットワークのラウンド、Sigelith の鍵サーバーのシェア（その時刻を過ぎてから公開されます — これは暗号上の制約ではなく、運用者の方針です）、そしてカプセルの隣に保存される復旧コードです。つまり、このバックアップを持つ人は復旧コードも持っていることになり、期日前に開けるには運用者が方針を破るだけで足ります。その時刻を過ぎれば、カプセルのファイルを持つ人なら誰でも開けます。カプセルはサーバーではなくこのバックアップ内にあり、sigelith.org/capsule/ のページで開けます。',
    'Wybierz kapsułę z listy albo utwórz nową.':
        '一覧からカプセルを選ぶか、新しく作成してください。',
    'Nowa kapsuła…':
        '新しいカプセル…',
    'Pieczętuje wybrany folder do daty':
        '選んだフォルダーを指定日まで封印します',
    'Pokaż w folderze':
        'フォルダーに表示',
    'Otwiera folder kapsuły w Eksploratorze':
        'カプセルのフォルダーをエクスプローラーで開きます',
    'Otwórz na stronie':
        'ウェブサイトで開く',
    'Strona sigelith.org/capsule/ otwiera kapsułę po jej dacie':
        '期日を過ぎたカプセルは sigelith.org/capsule/ のページで開けます',
    'można otworzyć':
        '開封可能',
    'zamknięta':
        '封印中',
    'W tej kopii nie ma jeszcze kapsuł czasu.':
        'このバックアップにはまだタイムカプセルがありません。',
    'Ta kapsuła da się otworzyć na stronie sigelith.org/capsule/ — wskaż jej pliki.':
        'このカプセルは sigelith.org/capsule/ のページで開けます — そこでカプセルのファイルを指定してください。',
    'Kapsuła jest zamknięta do daty z listy. Kod odzyskiwania leży w pliku obok niej.':
        'カプセルは一覧の日付まで封印されています。復旧コードはカプセルの隣のファイルにあります。',
    'Wybierz folder do zapieczętowania':
        '封印するフォルダーを選択',
    'Pieczętuję „{name}” — kilka sekund na krzywej eliptycznej…':
        '「{name}」を封印しています — 楕円曲線の計算に数秒かかります…',
    'kapsuła czasu':
        'タイムカプセル',
    'Kapsuła zapieczętowana':
        'カプセルを封印しました',
    '„{name}” otworzy się najwcześniej {when}.\n\nKod odzyskiwania (skopiowany do schowka, zapisany też obok kapsuły):\n\n{code}\n\nZapisz go w bezpiecznym miejscu. Przed datą otwarcia sam niczego nie otwiera; po niej zastępuje jeden z kluczy, gdyby był niedostępny.':
        '「{name}」を開けるようになるのは {when} 以降です。\n\n復旧コード（クリップボードにコピー済み。カプセルの隣にも保存されています）：\n\n{code}\n\n安全な場所に保管してください。開封日より前は、このコードだけでは何も開けません。開封日以降は、鍵のいずれかが入手できない場合にその代わりになります。',
    'Nie udało się zapieczętować: {error}':
        '封印できませんでした：{error}',
    'Nowa kapsuła czasu':
        '新しいタイムカプセル',
    'Otworzy się najwcześniej':
        '開封可能日時',
    'kapsuła':
        'カプセル',
    'Chwila otwarcia musi być w przyszłości.':
        '開封日時は未来の日時にしてください。',
    'Na bieżąco':
        'リアルタイム',
    'Zmiany w folderach źródłowych trafiają do dzisiejszej wersji kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje. Jedna wersja na dzień; ze znacznikami czasu zamyka ją pieczęć następnego dnia.':
        'バックアップ元フォルダーの変更は、保存から数分後に今日のバックアップバージョンに反映され、ドライブを接続するとすぐに同期されます。バージョンは 1 日に 1 つです。タイムスタンプを使う場合は、翌日に封印されて確定します。',
    'Na bieżąco — po każdej zmianie i po podłączeniu dysku':
        'リアルタイム — 変更のたびと、ドライブの接続時',
    'Dla dysku podłączonego na stałe albo często: zmiany trafiają do kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje.':
        '常時またはよく接続しているドライブ向け：変更は保存の数分後にバックアップに反映され、ドライブを接続するとすぐに同期されます。',
    'Kopia będzie na bieżąco: zmiany trafią do dzisiejszej wersji kilka minut po zapisie, a po podłączeniu dysku kopia od razu się zsynchronizuje.':
        'バックアップは常に最新に保たれます：変更は保存の数分後に今日のバージョンに反映され、ドライブを接続するとすぐに同期されます。',
    'przywracanie':
        '復元',
    'Nowa kopia krok po kroku':
        '新しいバックアップを順を追って設定',
}
