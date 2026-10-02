"""Katalog turecki: „polski tekst źródłowy” → „tekst (turecki)”.

Klucze są te same co w ``en.py`` i muszą dokładnie odpowiadać napisom w kodzie;
pilnuje tego ``tests/test_i18n.py``. Pola w nawiasach klamrowych (``{count}``)
zostają bez zmian. Formaty dat są te same co w Sigelith Desktop.
"""

from __future__ import annotations

TEXTS: dict[str, str] = {
    '\n\nLokalizacja:\n{path}':
        '\n\nKonum:\n{path}',
    '\nDo uzupełnienia: niedokończone kopie: {count} — możesz je uzupełnić, wybierając wersję poniżej.':
        '\nTamamlanmamış yedekler: {count} — aşağıdan bir sürüm seçerek bunları tamamlayabilirsiniz.',
    '\nUwaga: duży klaster ({size}): każdy mały plik zajmuje co najmniej tyle miejsca. Przy wielu małych plikach kopia zajmie wielokrotnie więcej niż dane.':
        '\nNot: büyük küme ({size}): her küçük dosya en az bu kadar yer kaplar. Çok sayıda küçük dosyada yedek, verinin kendisinden kat kat fazla yer kaplar.',
    '\nUwaga: niedokończone wersje (nie zawierają wszystkich plików): {names}':
        '\nNot: tamamlanmamış sürümler (tüm dosyaları içermez): {names}',
    '\nUwaga: {filesystem} nie obsługuje twardych dowiązań — każda wersja z datą zajmuje tyle miejsca co pełna kopia.':
        '\nNot: {filesystem} sabit bağlantıları desteklemiyor — her tarihli sürüm tam bir yedek kadar yer kaplar.',
    ' wersji':
        ' sürüm',
    ' z szyfrowaniem AES-256-GCM…':
        ' (AES-256-GCM şifrelemeyle)…',
    ' ×':
        ' ×',
    ' — a ponieważ {filesystem} nie obsługuje twardych dowiązań, zapisze ponownie wszystkie pliki i zajmie tyle miejsca co cała kopia':
        ' — ve {filesystem} sabit bağlantıları desteklemediği için tüm dosyaları yeniden yazar ve yedeğin tamamı kadar yer kaplar',
    ' • pozostało {time}':
        ' • {time} kaldı',
    '%d.%m %H:%M':
        '%d.%m %H:%M',
    '%d.%m.%Y':
        '%d.%m.%Y',
    '%d.%m.%Y %H:%M':
        '%d.%m.%Y %H:%M',
    ', klaster {size}':
        ', küme {size}',
    ', uzupełniona {when}':
        ', tamamlama: {when}',
    'Analizuje pliki i pokazuje plan. Nic nie zapisuje.':
        'Dosyaları inceler ve planı gösterir. Hiçbir şey yazmaz.',
    'Anulowano przed rozpoczęciem kopii.':
        'Yedekleme başlamadan iptal edildi.',
    'Anuluj':
        'İptal',
    'Argon2id (t={passes}, {memory} MiB, p={threads})':
        'Argon2id (t={passes}, {memory} MiB, p={threads})',
    'Argon2id — {passes} przebiegi, {memory} MiB, {threads} wątki':
        'Argon2id — {passes} geçiş, {memory} MiB, {threads} iş parçacığı',
    'Automatycznie (język systemu)':
        'Otomatik (sistem dili)',
    'Bardzo dobre':
        'Çok güçlü',
    'Bardzo słabe':
        'Çok zayıf',
    'Brak manifestu — skanuję katalog kopii.':
        'Manifest yok — yedek klasörü taranıyor.',
    'Brakuje tagu uwierzytelniającego — plik jest obcięty.':
        'Kimlik doğrulama etiketi eksik — dosya yarıda kesilmiş.',
    'Błąd uruchamiania':
        'Başlatma hatası',
    'Ciemny':
        'Koyu',
    'Co dokładnie zostanie zapisane przy najbliższym przebiegu.':
        'Bir sonraki çalıştırmada tam olarak neyin yazılacağı.',
    'Co kopiujemy':
        'Neyi yedekliyoruz',
    'Co zrobić, gdy plik o tej nazwie już istnieje w katalogu docelowym.':
        'Hedef klasörde aynı adlı bir dosya zaten varsa ne yapılacağı.',
    'Czas w nazwie to BeatTime — 1000 beatów na dobę, kotwica w UTC, ten sam moment na całym świecie. Data jest datą UTC, więc zgadza się z zegarem.':
        'Klasör adındaki saat BeatTime biçimindedir — günde 1000 beat, UTC’ye sabitlenmiş, dünyanın her yerinde aynı an. Tarih UTC tarihidir, bu yüzden saatle uyuşur.',
    'Czym jest {app}':
        '{app} nedir',
    'Czyści tylko okno — plik dziennika pozostaje':
        'Yalnızca pencereyi temizler — günlük dosyası kalır',
    'Dane aplikacji: {path}':
        'Uygulama verileri: {path}',
    'Decyduje, czy zachowujemy historię wersji.':
        'Sürüm geçmişinin tutulup tutulmayacağını belirler.',
    'Dobre':
        'Güçlü',
    'Dodaj folder':
        'Klasör ekle',
    'Dodaj przynajmniej jeden folder źródłowy.':
        'En az bir kaynak klasör ekleyin.',
    'Dogrywka zmian z czasu kopii:':
        'Yedekleme sırasındaki değişiklikler için tamamlama:',
    'Dokąd przywracamy':
        'Nereye geri yüklüyoruz',
    'Dokładnie to, co program realnie stosuje.':
        'Programın gerçekte kullandığı yöntemlerin tam listesi.',
    'Domyślne wykluczenia':
        'Varsayılan dışlamalar',
    'Domyślne wykluczenia zapisane.':
        'Varsayılan dışlamalar kaydedildi.',
    'Domyślnie wyłączone. Przy włączonej opcji skasowanie pliku w źródle\nusuwa też jego jedyną kopię zapasową — operacja nieodwracalna.':
        'Varsayılan olarak kapalı. Seçenek açıkken kaynakta bir dosyayı silmek\nonun tek yedeğini de kaldırır — bu işlem geri alınamaz.',
    'Dopisuj do nazwy katalogu datę ostatniego uzupełnienia':
        'Klasör adına son tamamlama tarihini ekle',
    'Dziennik':
        'Günlük',
    'Dziennik: {path}':
        'Günlük: {path}',
    'Ekran przywracania wypełniony danymi szablonu.':
        'Geri yükleme ekranı şablon verileriyle dolduruldu.',
    'Folder docelowy kopii — najlepiej na innym dysku fizycznym.':
        'Yedeğin hedef klasörü — tercihen başka bir fiziksel diskte.',
    'Folder zawierający kopię utworzoną przez {app}.':
        '{app} tarafından oluşturulmuş bir yedeği içeren klasör.',
    'Gdy plik już istnieje:':
        'Dosya zaten varsa:',
    'Gdzie zapisujemy':
        'Nereye kaydediyoruz',
    'Gotowe do pracy.':
        'Hazır.',
    'Gotowe. Wybierz foldery do kopii.':
        'Hazır. Yedeklenecek klasörleri seçin.',
    'Gotowe: {count} {files}, {size}, {seconds} s.':
        'Tamamlandı: {count} {files}, {size}, {seconds} sn.',
    'Główny folder kopii. Zawiera spis treści (.cleanvault-manifest).':
        'Yedeğin ana klasörü. İçindekiler listesini (.cleanvault-manifest) içerir.',
    'Hasła nie da się odzyskać ani zresetować. Jeśli je zgubisz, dane z kopii zaszyfrowanej są bezpowrotnie stracone — tak działa poprawne szyfrowanie.':
        'Parola kurtarılamaz ve sıfırlanamaz. Parolayı kaybederseniz şifreli yedekteki veriler kalıcı olarak kaybolur — doğru şifreleme böyle çalışır.',
    'Hasła w obu polach różnią się.':
        'İki alandaki parolalar birbirinden farklı.',
    'Hasło':
        'Parola',
    'Hasło do kopii':
        'Yedek parolası',
    'Hasło nie jest nigdzie zapisywane w postaci jawnej.\nBez niego nie da się odzyskać danych — nie istnieje żadna furtka serwisowa.':
        'Parola hiçbir yerde açık metin olarak saklanmaz.\nParola olmadan veriler kurtarılamaz — hiçbir arka kapı yoktur.',
    'Hasło nie może być puste.':
        'Parola boş olamaz.',
    'Hasło niezapisane':
        'Parola kaydedilmedi',
    'Hasło powinno mieć co najmniej 8 znaków.':
        'Parola en az 8 karakter olmalıdır.',
    'Hasło trafia do magazynu systemowego powiązanego z Twoim kontem.\nNigdy nie jest zapisywane w plikach programu.':
        'Parola, hesabınıza bağlı sistem deposuna kaydedilir.\nProgramın kendi dosyalarına asla yazılmaz.',
    'Hasło użyte przy tworzeniu kopii':
        'Yedek oluşturulurken kullanılan parola',
    'Ile plików kopia przetwarza jednocześnie. Przy setkach tysięcy małych plików\nczas kopii to głównie opóźnienia na każdy plik (otwarcie, skanowanie\nantywirusowe, zapis na nośnik), a nie przesył danych — praca równoległa\nskraca go kilkukrotnie.\n\n„automatycznie” dobiera liczbę do procesora (do 32). Na wolnym dysku\ntalerzowym mniejsza wartość (2–4) bywa szybsza.':
        'Yedeklemenin aynı anda kaç dosya işlediği. Yüz binlerce küçük dosyada\nyedekleme süresini veri aktarımı değil, dosya başına gecikmeler (açma,\nvirüsten koruma taraması, sürücüye yazma) belirler — paralel çalışma\nbu süreyi birkaç kat kısaltır.\n\n“otomatik” sayıyı işlemciye göre seçer (en fazla 32). Yavaş bir mekanik\ndiskte daha küçük bir değer (2–4) genellikle daha hızlıdır.',
    'Informacje przydatne przy zgłaszaniu problemu.':
        'Bir sorunu bildirirken işe yarayan bilgiler.',
    'Jak to działa':
        'Nasıl çalışır',
    'Jasny':
        'Açık',
    'Jeden folder utrzymywany w zgodzie ze źródłem. Brak historii wersji,\nza to najprostsza struktura i najmniejsze zużycie miejsca.':
        'Kaynakla eşit tutulan tek bir klasör. Sürüm geçmişi yoktur,\nama yapı en basit ve kapladığı yer en azdır.',
    'Jeśli operacja zakończy się błędem, skopiuj stąd ostatnie wiersze — zawierają dokładną przyczynę, a nie tylko komunikat ogólny.':
        'Bir işlem hatayla biterse son satırları buradan kopyalayın — genel bir iletiyi değil, hatanın tam nedenini içerirler.',
    'Język interfejsu zmieniony.':
        'Arayüz dili değiştirildi.',
    'Język zmienisz po zakończeniu bieżącej operacji.':
        'Dili, geçerli işlem bittikten sonra değiştirebilirsiniz.',
    'Język:':
        'Dil:',
    'Katalog docelowy leży wewnątrz źródła ({path}). Kopia kopiowałaby samą siebie w nieskończoność.':
        'Hedef klasör kaynağın içinde ({path}). Yedek kendini sonsuza kadar kopyalardı.',
    'Katalog docelowy nie może być tym samym katalogiem co źródłowy.':
        'Hedef klasör, kaynak klasörle aynı olamaz.',
    'Katalog jeszcze nie istnieje — zostanie utworzony.':
        'Klasör henüz yok — oluşturulacak.',
    'Katalog kopii nie istnieje: {path}':
        'Yedek klasörü yok: {path}',
    'Katalog źródłowy nie istnieje: {path}':
        'Kaynak klasör yok: {path}',
    'Katalog, w którym pojawią się odtworzone pliki.':
        'Geri yüklenen dosyaların yer alacağı klasör.',
    'Katalog, w którym powstanie kopia. Nie może leżeć wewnątrz folderu źródłowego.':
        'Yedeğin oluşturulacağı klasör. Kaynak klasörün içinde olamaz.',
    'Katalogi objęte kopią.\nMożesz przeciągnąć foldery z Eksploratora Windows wprost na tę listę.':
        'Yedeğe dahil edilen klasörler.\nKlasörleri Dosya Gezgini’nden doğrudan bu listeye sürükleyebilirsiniz.',
    'Każdy folder z datą jest kompletny — przywracanie nie wymaga sklejania wersji.':
        'Her tarihli klasör eksiksizdir — geri yükleme için sürümleri birleştirmek gerekmez.',
    'Każdy plik jest czytany ponownie zaraz po zapisaniu. Dane pochodzą wtedy\nzwykle z pamięci podręcznej systemu, więc niewiele mówi to o nośniku,\na wydłuża kopię nawet dwukrotnie.\n\nSkuteczniejsza jest weryfikacja odroczona: ekran „Przywracanie” →\n„Sprawdź kopię”, najlepiej po ponownym podłączeniu dysku.':
        'Her dosya yazıldıktan hemen sonra yeniden okunur. Veriler o sırada\ngenellikle sistem önbelleğinden gelir; bu yüzden sürücü hakkında pek bir şey\nsöylemez, ama yedeklemeyi iki katına kadar uzatabilir.\n\nErtelenmiş doğrulama daha etkilidir: “Geri yükleme” ekranı →\n“Yedeği kontrol et”, tercihen sürücüyü yeniden bağladıktan sonra.',
    'Każdy plik trafia do kopii jako zaszyfrowany kontener .cvlt.\nKlucz powstaje z hasła przez Argon2id.':
        'Her dosya yedeğe şifreli bir .cvlt kapsayıcısı olarak girer.\nAnahtar, paroladan Argon2id ile türetilir.',
    'Każdy przebieg tworzy osobny folder z datą i godziną.\nPliki niezmienione są podpinane twardym dowiązaniem, więc historia\nzajmuje tyle miejsca, ile realnie się zmieniło.':
        'Her çalıştırma, tarih ve saat içeren ayrı bir klasör oluşturur.\nDeğişmeyen dosyalar sabit bağlantıyla eklenir; böylece geçmiş\nyalnızca gerçekten değişen kadar yer kaplar.',
    'Klaster nośnika to {cluster} — pliki zajmą {actual} zamiast {logical} (narzut {overhead}).':
        'Sürücünün küme boyutu {cluster} — dosyalar {logical} yerine {actual} yer kaplayacak (ek yük {overhead}).',
    'Kliknij szablon, aby zobaczyć jego szczegóły.':
        'Ayrıntılarını görmek için bir şablona tıklayın.',
    'Kliknij „Podgląd zmian”, aby sprawdzić plan bez zapisywania czegokolwiek.':
        'Hiçbir şey yazmadan planı görmek için “Değişiklikleri önizle” düğmesine tıklayın.',
    'Kolor wyróżnienia':
        'Vurgu rengi',
    'Kolor wyróżnienia…':
        'Vurgu rengi…',
    'Kopia':
        'Yedek',
    'Kopia do dokończenia':
        'Tamamlanacak yedek',
    'Kopia jest aktualna — nie ma czego zapisywać.':
        'Yedek güncel — yazılacak bir şey yok.',
    'Kopia jest zaszyfrowana — podaj hasło użyte przy jej tworzeniu.':
        'Yedek şifreli — oluşturulurken kullanılan parolayı girin.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją przywrócić.':
        'Yedek şifreli — geri yüklemek için parolayı girin.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją zweryfikować.':
        'Yedek şifreli — doğrulamak için parolayı girin.',
    'Kopia jest zaszyfrowana — podaj hasło.':
        'Yedek şifreli — parolayı girin.',
    'Kopia lustrzana':
        'Ayna kopya',
    'Kopia nie została uruchomiona.':
        'Yedekleme başlatılmadı.',
    'Kopia wykonana. Uruchom podgląd ponownie, aby sprawdzić stan.':
        'Yedekleme tamamlandı. Durumu görmek için önizlemeyi yeniden çalıştırın.',
    'Kopia zapasowa':
        'Yedekleme',
    'Kopia {folder}':
        '{folder} yedeği',
    'Kopia {kind} • {count} {files} • {size} • ostatnia aktualizacja {when}\nŹródła: {roots}':
        'Yedek: {kind} • {count} {files} • {size} • son güncelleme: {when}\nKaynaklar: {roots}',
    'Kopiowane są wyłącznie pliki nowe i zmienione od ostatniego przebiegu.':
        'Yalnızca son çalıştırmadan bu yana yeni olan veya değişen dosyalar kopyalanır.',
    'Kopiuje ustawienia szablonu na ekran „Kopia zapasowa”':
        'Şablonun ayarlarını “Yedekleme” ekranına kopyalar',
    'Kopię możesz sprawdzić później: ekran „Przywracanie” → „Sprawdź kopię”. Najlepiej po ponownym podłączeniu dysku — wtedy dane są czytane z nośnika.':
        'Yedeği daha sonra kontrol edebilirsiniz: “Geri yükleme” ekranı → “Yedeği kontrol et”. En iyisi sürücüyü yeniden bağladıktan sonra yapmaktır — o zaman veriler gerçekten sürücüden okunur.',
    'Kryptografia':
        'Kriptografi',
    'Lista podpowiadana przy tworzeniu nowej kopii.':
        'Yeni bir yedek ayarlanırken önerilen liste.',
    'Magazyn haseł: {backend}':
        'Parola deposu: {backend}',
    'Magazyn systemowy: {backend}':
        'Sistem deposu: {backend}',
    'Menedżer poświadczeń Windows (DPAPI, powiązany z kontem użytkownika).':
        'Windows Kimlik Bilgileri Yöneticisi (DPAPI, kullanıcı hesabınıza bağlı).',
    'Miejsce i układ odtwarzanych plików.':
        'Geri yüklenen dosyaların yeri ve düzeni.',
    'Motyw zmieniony na {theme}.':
        'Tema değiştirildi: {theme}.',
    'Motyw:':
        'Tema:',
    'Możesz też przeciągnąć foldery z Eksploratora Windows wprost na listę.':
        'Klasörleri Dosya Gezgini’nden doğrudan listeye de sürükleyebilirsiniz.',
    'Można ją dokończyć — zostaną dograne tylko brakujące i zmienione pliki.':
        'Tamamlanabilir — yalnızca eksik ve değişen dosyalar eklenecek.',
    'Na nośniku docelowym zajmie to ok. {size}.':
        'Bu, hedef sürücüde yaklaşık {size} yer kaplayacak.',
    'Nadpisywanie plików':
        'Dosyaların üzerine yazma',
    'Nadpisz istniejące pliki':
        'Var olan dosyaların üzerine yaz',
    'Nazwa szablonu':
        'Şablon adı',
    'Nazwa szablonu nie może być pusta.':
        'Şablon adı boş olamaz.',
    'Nazwa szablonu zapisana.':
        'Şablon adı kaydedildi.',
    'Nazwa szablonu:':
        'Şablon adı:',
    'Nie ma wersji kopii o nazwie {name} w katalogu {path}.':
        '{path} klasöründe {name} adlı bir yedek sürümü yok.',
    'Nie można odczytać informacji o dysku: {error}':
        'Sürücü bilgileri okunamadı: {error}',
    'Nie udało się uruchomić programu — brakuje biblioteki: {error}\nZainstaluj zależności poleceniem:  pip install -r requirements.txt':
        'Program başlatılamadı — bir kitaplık eksik: {error}\nBağımlılıkları şu komutla yükleyin:  pip install -r requirements.txt',
    'Nie udało się wykonać operacji':
        'İşlem gerçekleştirilemedi',
    'Nie udało się zapisać hasła w magazynie systemowym.\nSzablon działa normalnie — program poprosi o hasło przy uruchomieniu.':
        'Parola sistem deposuna kaydedilemedi.\nŞablon normal şekilde çalışır — program çalıştırıldığında parolayı soracak.',
    'Nie udało się znaleźć wolnej nazwy dla {path}':
        'Şunun için boş bir ad bulunamadı: {path}',
    'Nie wskazano katalogu docelowego.':
        'Hedef klasör belirtilmedi.',
    'Nie wskazano żadnego katalogu źródłowego.':
        'Hiçbir kaynak klasör belirtilmedi.',
    'Nie wybrano katalogu':
        'Klasör seçilmedi',
    'Nie wybrano szablonu':
        'Şablon seçilmedi',
    'Nie znaleziono spisu treści kopii — program przeskanuje folder i rozpozna pliki po ich zawartości.':
        'Yedeğin içindekiler listesi bulunamadı — program klasörü tarayacak ve dosyaları içeriklerinden tanıyacak.',
    'Nie znam oryginalnej lokalizacji dla {key} — wybierz inny układ przywracania.':
        'Şu öğenin özgün konumu bilinmiyor: {key} — başka bir geri yükleme düzeni seçin.',
    'Niedostępny — backend {backend} nie gwarantuje poufności.':
        'Kullanılamıyor — {backend} arka ucu gizliliği garanti etmiyor.',
    'Niedostępny — brak biblioteki keyring.':
        'Kullanılamıyor — keyring kitaplığı yok.',
    'Nieznany algorytm wyprowadzania klucza: {name}':
        'Bilinmeyen anahtar türetme algoritması: {name}',
    'Nowa wersja z datą':
        'Yeni tarihli sürüm',
    'Nowa wersja z datą to kopia od początku do osobnego folderu':
        'Yeni tarihli sürüm, ayrı bir klasöre baştan yedek almak demektir',
    'Nowa wersja z datą — kopia do nowego folderu.\nWybrana istniejąca wersja — dogrywa do niej tylko brakujące i zmienione\npliki, a pliki różniące się od źródła nadpisuje. Tak dokończysz przerwaną\nkopię albo uzupełnisz ją o dane, które powstały w trakcie jej wykonywania.':
        'Yeni tarihli sürüm — yeni bir klasöre yedek.\nSeçilen mevcut sürüm — ona yalnızca eksik ve değişen dosyalar eklenir,\nkaynaktan farklı dosyaların üzerine yazılır. Böylece yarıda kalan bir\nyedeği tamamlar ya da yedekleme sırasında oluşan verileri eklersiniz.',
    'Nowy szablon':
        'Yeni şablon',
    'Nośnik docelowy ({filesystem}) nie obsługuje twardych dowiązań, więc każda wersja z datą jest pełną kopią. Te {count} niezmienionych plików zostanie powielone ({size}). Rozważ układ „kopia lustrzana” albo nośnik NTFS.':
        'Hedef sürücü ({filesystem}) sabit bağlantıları desteklemiyor, bu yüzden her tarihli sürüm tam bir kopyadır. Değişmeyen {count} dosya yeniden kopyalanacak ({size}). “Ayna kopya” düzenini ya da NTFS biçimli bir sürücüyü düşünün.',
    'O programie':
        'Hakkında',
    'Obsługiwane są wzorce w stylu Windows:\n  *.tmp          — wszystkie pliki tymczasowe\n  Thumbs.db      — konkretna nazwa\n  node_modules/* — cały folder wraz z zawartością':
        'Windows tarzı desenler desteklenir:\n  *.tmp          — tüm geçici dosyalar\n  Thumbs.db      — belirli bir ad\n  node_modules/* — içeriğiyle birlikte bütün bir klasör',
    'Ochrona danych':
        'Veri koruma',
    'Odczytuje wszystkie pliki kopii i weryfikuje ich poprawność.\nNic nie zapisuje na dysku.':
        'Yedekteki tüm dosyaları okur ve sağlam olup olmadıklarını doğrular.\nDiske hiçbir şey yazmaz.',
    'Odpowiednik synchronizacji folderu. Wcześniejsze wersje plików nie są zachowywane.':
        'Klasör eşitlemenin karşılığı. Dosyaların önceki sürümleri tutulmaz.',
    'Odtwarza pliki z kopii — również z kopii zaszyfrowanej.':
        'Dosyaları yedekten geri yükler — şifreli yedekten de.',
    'Odtwarza pliki zgodnie z ustawieniami powyżej':
        'Dosyaları yukarıdaki ayarlara göre geri yükler',
    'Odtwórz pełną strukturę folderów':
        'Tam klasör yapısını yeniden oluştur',
    'Odtwórz pliki z istniejącej kopii':
        'Var olan bir yedekten dosyaları geri yükle',
    'Operacja nie powiodła się.':
        'İşlem başarısız oldu.',
    'Operacja przerwana przez użytkownika.':
        'İşlem kullanıcı tarafından durduruldu.',
    'Operacja przerwana — utrwalam stan dotychczas zapisanych plików.':
        'İşlem durduruldu — şimdiye kadar yazılan dosyaların durumu kaydediliyor.',
    'Operacja w toku':
        'İşlem sürüyor',
    'Operacja zakończona błędem.':
        'İşlem hatayla sona erdi.',
    'Ostatnie operacje':
        'Son işlemler',
    'Otwiera ekran przywracania z wypełnionymi ścieżkami':
        'Geri yükleme ekranını yollar doldurulmuş olarak açar',
    'Otwiera pełny dziennik w domyślnym edytorze':
        'Günlüğün tamamını varsayılan düzenleyicide açar',
    'Otwórz katalog danych':
        'Veri klasörünü aç',
    'Otwórz katalog dziennika':
        'Günlük klasörünü aç',
    'Otwórz okno wyboru katalogu':
        'Klasör seçme penceresini aç',
    'Otwórz plik dziennika':
        'Günlük dosyasını aç',
    'PBKDF2-HMAC-SHA256 ({count} iteracji)':
        'PBKDF2-HMAC-SHA256 ({count} yineleme)',
    'PBKDF2-HMAC-SHA256 — {count} iteracji':
        'PBKDF2-HMAC-SHA256 — {count} yineleme',
    'PBKDF2-HMAC-SHA256, {count} iteracji':
        'PBKDF2-HMAC-SHA256, {count} yineleme',
    'Pełna struktura — układ jak w źródle, wewnątrz wskazanego katalogu.\nJeden folder — wygodne, gdy szukasz kilku plików.\nPierwotne lokalizacje — zapisuje pliki tam, skąd zostały pobrane.':
        'Tam yapı — seçtiğiniz klasörün içinde, kaynaktaki düzenle.\nTek klasör — birkaç dosya arıyorsanız kullanışlıdır.\nÖzgün konumlar — dosyaları alındıkları yere yazar.',
    'Pierwszy przebieg kopiuje wszystko i trwa najdłużej. Kolejne porównują rozmiar i datę modyfikacji, więc zwykle kończą się w kilka sekund.':
        'İlk çalıştırma her şeyi kopyalar ve en uzun sürer. Sonrakiler boyutu ve değiştirilme tarihini karşılaştırır, bu yüzden genellikle birkaç saniyede biter.',
    'Plan gotowy: {count} {files} do zapisania.':
        'Plan hazır: yazılacak {count} {files}.',
    'Plik jest za krótki, by być kontenerem tego programu.':
        'Dosya, bu programın bir kapsayıcısı olamayacak kadar kısa.',
    'Plik skończył się wcześniej, niż deklaruje nagłówek.':
        'Dosya, başlığında belirtilenden önce bitiyor.',
    'Plik w formacie w wersji {found}; ta wersja programu obsługuje {supported}.':
        'Dosyanın biçim sürümü: {found}; programın bu sürümü şunu destekliyor: {supported}.',
    'Plik wymaga Argon2id, a biblioteka argon2-cffi jest niedostępna.':
        'Dosya Argon2id gerektiriyor, ancak argon2-cffi kitaplığı kullanılamıyor.',
    'Pliki pominięte — kopia jest aktualna':
        'Atlanan dosyalar — yedek zaten güncel',
    'Pliki trafią do wskazanego katalogu z zachowaniem struktury folderów.':
        'Dosyalar, klasör yapısı korunarak seçilen klasöre yazılır.',
    'Pliki wrócą dokładnie tam, skąd pochodzą. Katalog docelowy zostanie zignorowany.':
        'Dosyalar tam olarak geldikleri yere döner. Hedef klasör yok sayılır.',
    'Pliki zmienione od ostatniego przebiegu':
        'Son çalıştırmadan bu yana değişen dosyalar',
    'Pliki zostaną zapisane dokładnie tam, skąd pochodzą.\n\nKonflikty nazw: {collision}.\n\nCzy kontynuować?':
        'Dosyalar tam olarak geldikleri yere yazılacak.\n\nAd çakışmaları: {collision}.\n\nDevam edilsin mi?',
    'Pliki, których jeszcze nie ma w kopii':
        'Henüz yedekte olmayan dosyalar',
    'Po uzupełnieniu istniejącej wersji jej katalog nazywa się np.\n  2026-09-17_@687--2026-09-24_@921\nczyli: data utworzenia kopii i data ostatniego uzupełnienia.\n\nData utworzenia zostaje z przodu, więc katalogi nadal układają się\nchronologicznie. Widać to w Eksploratorze bez uruchamiania programu.':
        'Mevcut bir sürüm tamamlandıktan sonra klasörünün adı örneğin şöyle olur:\n  2026-09-17_@687--2026-09-24_@921\nyani: yedeğin oluşturulma tarihi ve son tamamlama tarihi.\n\nOluşturulma tarihi başta kalır, bu yüzden klasörler yine kronolojik\nolarak sıralanır. Bunu programı başlatmadan Dosya Gezgini’nde görebilirsiniz.',
    'Po wykonaniu kopii zostanie mało wolnego miejsca ({free}).':
        'Yedeklemeden sonra az boş alan kalacak ({free}).',
    'Po zakończeniu kopii program ponownie skanuje źródło i dogrywa do tej samej\nwersji pliki, które w międzyczasie powstały lub się zmieniły.\nPrzydatne, gdy pracujesz na danych w trakcie wielogodzinnej kopii.\nPlik zmieniony w trakcie własnego kopiowania nigdy nie jest uznawany za zapisany.':
        'Yedekleme bittiğinde program kaynağı yeniden tarar ve bu arada oluşan\nya da değişen dosyaları aynı sürüme ekler.\nSaatlerce süren bir yedekleme sırasında verilerle çalışmaya devam ediyorsanız işe yarar.\nKopyalanırken değişen bir dosya hiçbir zaman yazılmış sayılmaz.',
    'Poczekaj na zakończenie bieżącej operacji.':
        'Geçerli işlemin bitmesini bekleyin.',
    'Podaj hasło dla szablonu „{name}”:':
        '“{name}” şablonunun parolasını girin:',
    'Podaj hasło — bez niego nie można zaszyfrować kopii.':
        'Bir parola girin — parola olmadan yedek şifrelenemez.',
    'Podane hasło nie pasuje do plików zapisanych wcześniej w tej kopii. Wznowienie z innym hasłem zostawiłoby w jednej kopii pliki pod dwoma hasłami. Podaj hasło użyte przy poprzednim przebiegu albo utwórz kopię w nowym katalogu.':
        'Girilen parola, bu yedeğe daha önce yazılmış dosyalarla eşleşmiyor. Farklı bir parolayla devam etmek, tek bir yedekte iki farklı parolayla korunan dosyalar bırakırdı. Önceki çalıştırmada kullanılan parolayı girin ya da yedeği yeni bir klasörde oluşturun.',
    'Podgląd zmian':
        'Değişiklikleri önizle',
    'Pokazuje folder z plikami dziennika':
        'Günlük dosyalarının bulunduğu klasörü gösterir',
    'Pokazuje folder z ustawieniami i szablonami':
        'Ayarların ve şablonların bulunduğu klasörü gösterir',
    'Pokaż / ukryj wpisane hasło':
        'Yazılan parolayı göster / gizle',
    'Pomiń istniejące pliki':
        'Var olan dosyaları atla',
    'Potwierdź usuwanie':
        'Silme onayı',
    'Powtórz hasło':
        'Parolayı tekrar girin',
    'Program nie mógł się uruchomić:\n\n{error}\n\nSzczegóły zapisano w dzienniku aplikacji.':
        'Program başlatılamadı:\n\n{error}\n\nAyrıntılar uygulama günlüğüne yazıldı.',
    'Program nie wie, czy ta kopia została dokończona. Uzupełnienie jej dogra tylko brakujące i zmienione pliki, a tego, co już jest zapisane, nie kopiuje ponownie.':
        'Program bu yedeğin tamamlanıp tamamlanmadığını bilmiyor. Tamamlama yalnızca eksik ve değişen dosyaları ekler; zaten yazılmış olanları yeniden kopyalamaz.',
    'Program sam wykryje, czy kopia jest zaszyfrowana.':
        'Program yedeğin şifreli olup olmadığını kendisi algılar.',
    'Przebieg operacji i diagnostyka':
        'İşlem akışı ve tanılama',
    'Przebieg operacji na żywo. Pełna historia trafia do pliku.':
        'İşlemlerin canlı akışı. Geçmişin tamamı bir dosyaya yazılır.',
    'Przebieg uzupełniający: {error}':
        'Tamamlama geçişi: {error}',
    'Przeciętne':
        'Orta',
    'Przerwano liczenie sumy kontrolnej.':
        'Sağlama toplamı hesaplaması durduruldu.',
    'Przerwano skanowanie.':
        'Tarama durduruldu.',
    'Przerwano. Zapisano {count} {files} ({size}).':
        'Durduruldu. {count} {files} yazıldı ({size}).',
    'Przerwij':
        'Durdur',
    'Przerywanie operacji…':
        'İşlem durduruluyor…',
    'Przerywanie — zapisuję spis treści kopii, nie wyłączaj komputera…':
        'Durduruluyor — yedeğin içindekiler listesi yazılıyor, lütfen bilgisayarı kapatmayın…',
    'Przeskanowano {count} {files}.':
        '{count} {files} tarandı.',
    'Przygotowanie…':
        'Hazırlanıyor…',
    'Przywracanie':
        'Geri yükleme',
    'Przywracanie do pierwotnych lokalizacji':
        'Özgün konumlara geri yükleme',
    'Przywracanie przerwane.':
        'Geri yükleme durduruldu.',
    'Przywracanie {count} {files} ({size})…':
        'Geri yükleniyor: {count} {files} ({size})…',
    'Przywróć do pierwotnych lokalizacji':
        'Özgün konumlara geri yükle',
    'Przywróć domyślne':
        'Varsayılanları geri yükle',
    'Przywróć fabryczne':
        'Fabrika listesini geri yükle',
    'Przywróć pliki':
        'Dosyaları geri yükle',
    'Przywróć z tej kopii':
        'Bu yedekten geri yükle',
    'Pusta nazwa':
        'Boş ad',
    'Równoległe operacje:':
        'Paralel işlemler:',
    'Skanowanie plików źródłowych…':
        'Kaynak dosyalar taranıyor…',
    'Skrót z dziennika — pełny zapis znajdziesz w zakładce „Dziennik”.':
        'Günlükten bir özet — kaydın tamamı “Günlük” ekranında.',
    'Skąd przywracamy':
        'Nereden geri yüklüyoruz',
    'Sprawdzam, co zmieniło się w źródle w trakcie kopii (przebieg uzupełniający {attempt} z {passes})…':
        'Yedekleme sırasında kaynakta neyin değiştiği kontrol ediliyor (tamamlama geçişi {attempt}/{passes})…',
    'Sprawdzam, czy hasło zgadza się z hasłem wcześniej zapisanych plików…':
        'Parolanın daha önce yazılan dosyalarla eşleşip eşleşmediği kontrol ediliyor…',
    'Sprawdzam, czy w katalogu docelowym jest kopia do dokończenia…':
        'Hedef klasörde tamamlanacak bir yedek olup olmadığı kontrol ediliyor…',
    'Sprawdź hasło':
        'Parolayı kontrol edin',
    'Sprawdź kopię':
        'Yedeği kontrol et',
    'Szablon przechowuje foldery, opcje i wykluczenia. Hasło nigdy nie trafia do szablonu — jest przechowywane w Menedżerze poświadczeń Windows albo wpisywane przy każdym uruchomieniu.':
        'Şablon klasörleri, seçenekleri ve dışlamaları saklar. Parola asla şablona kaydedilmez — Windows Kimlik Bilgileri Yöneticisi’nde saklanır ya da her çalıştırmada girilir.',
    'Szablon usunięty.':
        'Şablon silindi.',
    'Szablon „{name}”':
        'Şablon “{name}”',
    'Szablon „{name}” już istnieje.\n\nZastąpić go bieżącymi ustawieniami z formularza?':
        '“{name}” adlı şablon zaten var.\n\nFormdaki geçerli ayarlarla değiştirilsin mi?',
    'Szablon „{name}” zostanie usunięty.\n\nPliki kopii zapasowej pozostaną nienaruszone.':
        '“{name}” şablonu silinecek.\n\nYedek dosyalarına dokunulmaz.',
    'Szablony':
        'Şablonlar',
    'Szablony: {count}\nSzyfrowanie: AES-256-GCM\nKlucz: {kdf}':
        'Şablonlar: {count}\nŞifreleme: AES-256-GCM\nAnahtar: {kdf}',
    'Szyfrowanie i kontrola poprawności zapisu.':
        'Şifreleme ve yazma doğrulaması.',
    'Szyfrowanie: AES-256-GCM (uwierzytelnione)\nWyprowadzanie klucza: {kdf}':
        'Şifreleme: AES-256-GCM (kimlik doğrulamalı)\nAnahtar türetme: {kdf}',
    'Szyfruj kopię (AES-256-GCM)':
        'Yedeği şifrele (AES-256-GCM)',
    'Słabe':
        'Zayıf',
    'Ta kopia nie jest zaszyfrowana — hasło nie jest potrzebne.':
        'Bu yedek şifreli değil — parola gerekmez.',
    'Ten folder jest już na liście.':
        'Bu klasör zaten listede.',
    'To nie jest plik zaszyfrowany przez ten program.':
        'Bu dosya bu programla şifrelenmemiş.',
    'Trwa inna operacja — poczekaj na jej zakończenie.':
        'Başka bir işlem sürüyor — bitmesini bekleyin.',
    'Trwa operacja':
        'Bir işlem sürüyor',
    'Trwa operacja na plikach. Zamknięcie programu ją przerwie.\n\nPliki zapisane do tej chwili zostaną zachowane, a kopię będzie można później dokończyć.\n\nZamknąć mimo to?':
        'Dosyalar üzerinde bir işlem sürüyor. Programı kapatmak işlemi durdurur.\n\nŞu ana kadar yazılan dosyalar korunur ve yedek daha sonra tamamlanabilir.\n\nYine de kapatılsın mı?',
    'Trwa: {description}…':
        'Sürüyor: {description}…',
    'Tryb dokładny — licz sumę kontrolną każdego pliku':
        'Kapsamlı mod — her dosyanın sağlama toplamını hesapla',
    'Układ kopii':
        'Yedek düzeni',
    'Układ plików:':
        'Dosya düzeni:',
    'Uruchom kopię':
        'Yedeklemeyi başlat',
    'Ustawienia':
        'Ayarlar',
    'Usunąć szablon?':
        'Şablon silinsin mi?',
    'Usuwa pozycję z listy. Nie kasuje żadnych plików.':
        'Öğeyi listeden kaldırır. Hiçbir dosyayı silmez.',
    'Usuwa szablon. Nie kasuje żadnych plików kopii.':
        'Şablonu siler. Hiçbir yedek dosyasını silmez.',
    'Usuwaj z kopii pliki skasowane w źródle':
        'Kaynakta silinen dosyaları yedekten de kaldır',
    'Usuń':
        'Sil',
    'Usuń zaznaczone':
        'Seçilenleri kaldır',
    'Uszkodzony nagłówek pliku.':
        'Dosya başlığı bozuk.',
    'Utwórz lub zaktualizuj kopię wybranych folderów':
        'Seçilen klasörlerin yedeğini oluştur veya güncelle',
    'Utwórz nową wersję':
        'Yeni sürüm oluştur',
    'Uzupełnienie istniejącej wersji nie kopiuje ponownie tego, co już w niej jest — dokończysz przerwaną kopię bez tworzenia kolejnej pełnej wersji.':
        'Mevcut bir sürümü tamamlamak, içinde zaten olanı yeniden kopyalamaz — yarıda kalan bir yedeği, yeni bir tam sürüm oluşturmadan tamamlarsınız.',
    'Uzupełnij tę wersję':
        'Bu sürümü tamamla',
    'Uzupełnij: {version} • {labels}':
        'Tamamla: {version} • {labels}',
    'W katalogu docelowym jest kopia tych samych folderów zapisana starszą wersją programu:':
        'Hedef klasörde, programın eski bir sürümüyle yazılmış, aynı klasörlerin bir yedeği var:',
    'W katalogu docelowym jest niedokończona kopia tych samych folderów:':
        'Hedef klasörde aynı klasörlerin tamamlanmamış bir yedeği var:',
    'W tym katalogu nie ma spisu treści kopii — nie ma z czym porównać plików.':
        'Bu klasörde yedeğin içindekiler listesi yok — dosyaların karşılaştırılacağı bir şey yok.',
    'Wczytaj do formularza':
        'Forma yükle',
    'Wczytano manifest kopii: {count} {files}.':
        'Yedek manifesti yüklendi: {count} {files}.',
    'Wczytano szablon „{name}” do formularza.':
        '“{name}” şablonu forma yüklendi.',
    'Wersja kopii nosi teraz nazwę {name}.':
        'Yedek sürümünün yeni adı: {name}.',
    'Wersja, licencja i użyta kryptografia':
        'Sürüm, lisans ve kullanılan kriptografi',
    'Wersje z datą (zalecane)':
        'Tarihli sürümler (önerilir)',
    'Weryfikacja kopii':
        'Yedek doğrulama',
    'Weryfikacja nie powiodła się: nieprawidłowe hasło lub uszkodzony plik.':
        'Doğrulama başarısız: yanlış parola ya da bozuk dosya.',
    'Weryfikacja po zapisie nie powiodła się — zapisane dane różnią się od źródła.':
        'Yazma sonrası doğrulama başarısız — yazılan veriler kaynaktan farklı.',
    'Weryfikacja {count} {files} ({size}), {threads} równolegle…':
        'Doğrulanıyor: {count} {files} ({size}), {threads} paralel işlem…',
    'Weryfikuj natychmiast po zapisie (spowalnia kopię)':
        'Yazdıktan hemen sonra doğrula (yedeklemeyi yavaşlatır)',
    'Wolne miejsce: {free} z {total}':
        'Boş alan: {free} / {total}',
    'Wolniejszy, ale wykrywa zmiany, które nie zmieniły rozmiaru ani daty\n(np. po przywróceniu pliku z innego nośnika).':
        'Daha yavaştır, ancak boyutu ya da tarihi değiştirmeyen değişiklikleri de yakalar\n(örneğin bir dosya başka bir sürücüden geri yüklendiğinde).',
    'Wpis {key} w spisie treści kopii wskazuje poza katalog docelowy — pomijam go.':
        'Yedeğin içindekiler listesindeki {key} kaydı hedef klasörün dışını gösteriyor — atlanıyor.',
    'Wraca do listy wbudowanej w program':
        'Programa yerleşik listeye döner',
    'Wskaż folder kopii, aby zobaczyć jej zawartość.':
        'İçeriğini görmek için yedek klasörünü seçin.',
    'Wskaż folder kopii.':
        'Yedek klasörünü seçin.',
    'Wskaż foldery objęte kopią. Podfoldery są uwzględniane automatycznie.':
        'Yedeklenecek klasörleri seçin. Alt klasörler otomatik olarak dahil edilir.',
    'Wskaż główny folder kopii (ten, który wybrałeś jako cel), a nie pojedynczy folder z datą. Program sam odczyta spis treści kopii.':
        'Tek bir tarihli klasörü değil, yedeğin ana klasörünü (hedef olarak seçtiğiniz klasörü) seçin. Program yedeğin içindekiler listesini kendisi okur.',
    'Wskaż katalog docelowy kopii.':
        'Yedeğin hedef klasörünü seçin.',
    'Wskaż katalog docelowy.':
        'Hedef klasörü seçin.',
    'Wstawia zalecaną listę wykluczeń':
        'Önerilen dışlama listesini ekler',
    'Wszystkie pliki wylądują bezpośrednio w katalogu docelowym, bez podfolderów.':
        'Tüm dosyalar alt klasör olmadan doğrudan hedef klasöre yazılır.',
    'Wszystko do jednego folderu':
        'Her şey tek klasöre',
    'Wybierz folder do kopii':
        'Yedeklenecek klasörü seçin',
    'Wybierz folder kopii':
        'Yedek klasörünü seçin',
    'Wybierz katalog':
        'Klasör seçin',
    'Wybierz katalog docelowy':
        'Hedef klasörü seçin',
    'Wybierz katalog docelowy kopii':
        'Yedeğin hedef klasörünü seçin',
    'Wybierz katalog, aby zobaczyć dostępne miejsce.':
        'Kullanılabilir alanı görmek için bir klasör seçin.',
    'Wybierz kolejny folder do kopii':
        'Yedeklenecek başka bir klasör seçin',
    'Wybierz szablon z listy.':
        'Listeden bir şablon seçin.',
    'Wybierz…':
        'Seç…',
    'Wybrano nadpisywanie istniejących plików. Ich obecna zawartość zostanie bezpowrotnie zastąpiona.\n\nCzy kontynuować?':
        'Var olan dosyaların üzerine yazmayı seçtiniz. Mevcut içerikleri kalıcı olarak değiştirilecek.\n\nDevam edilsin mi?',
    'Wyczyść widok':
        'Görünümü temizle',
    'Wygląd':
        'Görünüm',
    'Wygląd, wykluczenia domyślne i informacje o środowisku.':
        'Görünüm, varsayılan dışlamalar ve ortam bilgileri.',
    'Wygląd, wykluczenia i magazyn haseł':
        'Görünüm, dışlamalar ve parola deposu',
    'Wykluczenia':
        'Dışlamalar',
    'Wykonuje kopię według tego szablonu':
        'Bu şablona göre yedekleme yapar',
    'Wykonuje kopię zgodnie z powyższymi ustawieniami':
        'Yukarıdaki ayarlarla yedekleme yapar',
    'Wymagane wyłącznie dla kopii zaszyfrowanych.':
        'Yalnızca şifreli yedekler için gereklidir.',
    'Wzorce plików i folderów pomijanych w kopii — po jednym w wierszu.':
        'Yedeğe alınmayacak dosya ve klasörlerin desenleri — her satıra bir tane.',
    'Włączono szyfrowanie, ale nie podano hasła.':
        'Şifreleme açık, ancak parola girilmedi.',
    'Włączono usuwanie z kopii plików skasowanych w źródle.\n\nPliki usunięte w źródle stracą swoją jedyną kopię zapasową. Czy na pewno kontynuować?':
        'Kaynakta silinen dosyaları yedekten kaldırma seçeneği açık.\n\nKaynakta silinen dosyalar tek yedeklerini kaybedecek. Devam etmek istediğinizden emin misiniz?',
    'Za mało miejsca w katalogu docelowym. Potrzeba ok. {needed}, dostępne {free}.':
        'Hedef klasörde yeterli alan yok. Yaklaşık {needed} gerekiyor, kullanılabilir alan: {free}.',
    'Zabezpieczenie przed literówką — hasła nie da się odzyskać.':
        'Yazım hatasına karşı önlem — parola kurtarılamaz.',
    'Zachowaj oba — dopisz numer do nazwy':
        'Her ikisini de koru — ada numara ekle',
    'Zakończono z błędami ({errors}). Zapisano {count} {files}.':
        'Hatalarla tamamlandı ({errors}). {count} {files} yazıldı.',
    'Zakończono.':
        'Tamamlandı.',
    'Zapamiętaj hasło w Menedżerze poświadczeń Windows':
        'Parolayı Windows Kimlik Bilgileri Yöneticisi’nde hatırla',
    'Zapamiętuje te ustawienia do ponownego użycia':
        'Bu ayarları yeniden kullanmak üzere saklar',
    'Zapis bieżącej sesji':
        'Geçerli oturumun kaydı',
    'Zapisane konfiguracje do ponownego użycia':
        'Yeniden kullanılmak üzere kaydedilmiş yapılandırmalar',
    'Zapisane konfiguracje — uruchamiasz je jednym kliknięciem.':
        'Kaydedilmiş yapılandırmalar — tek tıklamayla çalıştırırsınız.',
    'Zapisane szablony':
        'Kayıtlı şablonlar',
    'Zapisano szablon „{name}”.':
        '“{name}” şablonu kaydedildi.',
    'Zapisuje listę jako domyślną':
        'Listeyi varsayılan olarak kaydeder',
    'Zapisuje nową nazwę szablonu':
        'Şablonun yeni adını kaydeder',
    'Zapisywanie {count} {files} ({size}), {workers} równolegle':
        'Yazılıyor: {count} {files} ({size}), {workers} paralel işlem',
    'Zapisz':
        'Kaydet',
    'Zapisz do:':
        'Şuraya yaz:',
    'Zapisz jako szablon':
        'Şablon olarak kaydet',
    'Zapisz nazwę':
        'Adı kaydet',
    'Zapisz szablon':
        'Şablonu kaydet',
    'Zastąpić szablon?':
        'Şablon değiştirilsin mi?',
    'Zatrzymuje operację. Pliki już zapisane pozostają nienaruszone.':
        'İşlemi durdurur. Zaten yazılmış dosyalara dokunulmaz.',
    'Zaznacz szablon na liście.':
        'Listede bir şablon seçin.',
    'Zmiana języka przebudowuje okno; wypełnione ścieżki zostają.':
        'Dili değiştirmek pencereyi yeniden oluşturur; doldurduğunuz yollar korunur.',
    'Zmiana motywu działa natychmiast.':
        'Tema değişikliği hemen uygulanır.',
    'Zmienia kolor przycisków i zaznaczeń':
        'Düğmelerin ve seçimlerin rengini değiştirir',
    'Zmień nazwę, aby łatwiej rozpoznawać szablon.':
        'Şablonu daha kolay tanımak için adını değiştirin.',
    'Znaleziono {count} {files}. Porównuję z poprzednią kopią…':
        '{count} {files} bulundu. Önceki yedekle karşılaştırılıyor…',
    'automatycznie':
        'otomatik',
    'bez zmian':
        'değişmeyen',
    'brak (biblioteka keyring niezainstalowana)':
        'yok (keyring kitaplığı yüklü değil)',
    'brak danych':
        'veri yok',
    'brak pliku w kopii':
        'dosya yedekte yok',
    'do zapisania':
        'yazılacak',
    'istniejąca kopia: {count} {files}, ostatnio {when}':
        'mevcut yedek: {count} {files}, son: {when}',
    'jeszcze nie uruchamiany':
        'henüz çalıştırılmadı',
    'kompletna':
        'eksiksiz',
    'kopia lustrzana':
        'ayna kopya',
    'kopia zapasowa':
        'yedekleme',
    'nie':
        'hayır',
    'niedokończona':
        'tamamlanmamış',
    'niedokończona — brakuje ok. {count} {files} ({size})':
        'tamamlanmamış — yaklaşık {count} {files} eksik ({size})',
    'niezaszyfrowana':
        'şifresiz',
    'nieznany format manifestu':
        'bilinmeyen manifest biçimi',
    'nowych plików':
        'yeni dosya',
    'np. C:\\Odzyskane':
        'ör. C:\\Kurtarılanlar',
    'np. E:\\Kopie zapasowe':
        'ör. E:\\Yedekler',
    'plik':
        'dosya',
    'plik stanu jest za krótki':
        'durum dosyası çok kısa',
    'plik stanu w wersji {found}, obsługiwana: {supported}':
        'durum dosyası sürümü {found}, desteklenen: {supported}',
    'pliki':
        'dosya',
    'plików':
        'dosya',
    'podgląd kopii':
        'yedek önizlemesi',
    'pozostaną w kopii':
        'yedekte kalacaklar',
    'rozmiar w kopii {actual} B zamiast {expected} B':
        'yedekteki boyut {expected} B yerine {actual} B',
    'sprawdzanie kopii':
        'yedek kontrolü',
    'stan nieznany (zapisana starszą wersją programu)':
        'durum bilinmiyor (programın eski bir sürümüyle yazılmış)',
    'suma kontrolna manifestu się nie zgadza':
        'manifestin sağlama toplamı eşleşmiyor',
    'suma kontrolna się nie zgadza — plik uszkodzony':
        'sağlama toplamı eşleşmiyor — dosya bozuk',
    'szablon {name}':
        '{name} şablonu',
    'tak':
        'evet',
    'ten system plików':
        'bu dosya sistemi',
    'wersja {version}':
        'sürüm {version}',
    'wersje z datą':
        'tarihli sürümler',
    'weryfikacja':
        'doğrulama',
    'wyłączona':
        'kapalı',
    'zaszyfrowana (AES-256-GCM)':
        'şifreli (AES-256-GCM)',
    'zawartość różni się od pliku źródłowego':
        'içerik kaynak dosyadan farklı',
    'zawartość różni się od sumy kontrolnej zapisanej podczas kopii':
        'içerik, yedekleme sırasında kaydedilen sağlama toplamıyla uyuşmuyor',
    'zmienionych':
        'değişen',
    'zostaną usunięte z kopii':
        'yedekten kaldırılacaklar',
    '{done} z {total} • {speed}/s{eta}':
        '{done} / {total} • {speed}/sn{eta}',
    '{done} • {speed}/s':
        '{done} • {speed}/sn',
    '{hours} h {minutes} min':
        '{hours} sa {minutes} dk',
    '{label}: {count} {files}':
        '{label}: {count} {files}',
    '{message}\n\nSzczegóły techniczne znajdziesz w zakładce „Dziennik”.':
        '{message}\n\nTeknik ayrıntılar “Günlük” ekranında.',
    '{minutes} min {seconds} s':
        '{minutes} dk {seconds} sn',
    '{name}: nie można odczytać ({error})':
        '{name}: okunamıyor ({error})',
    '{seconds} s':
        '{seconds} sn',
    '{summary}\n\nProblemy:\n{problems}\n\nPełna lista znajduje się w zakładce „Dziennik”.':
        '{summary}\n\nSorunlar:\n{problems}\n\nListenin tamamı “Günlük” ekranında.',
    '{summary}{notes}\n\nPliki zapisane przed przerwaniem są kompletne i zostały odnotowane w spisie treści kopii.\n\nAby dokończyć kopię, uruchom ją ponownie — program zaproponuje uzupełnienie tej wersji zamiast tworzenia nowej.':
        '{summary}{notes}\n\nDurdurmadan önce yazılan dosyalar eksiksizdir ve yedeğin içindekiler listesine kaydedildi.\n\nYedeği tamamlamak için yeniden çalıştırın — program yeni bir sürüm oluşturmak yerine bu sürümü tamamlamayı önerecek.',
    '{title} — gotowe':
        '{title} — tamamlandı',
    '{title} — przerwano':
        '{title} — durduruldu',
    '{title} — zakończono z błędami':
        '{title} — hatalarla tamamlandı',
    '{when}  •  {action}  •  {count} {files}':
        '{when}  •  {action}  •  {count} {files}',
    'Łączny rozmiar danych do przesłania':
        'Aktarılacak verilerin toplam boyutu',
    'Środowisko':
        'Ortam',
    'Źródła: {sources}\nCel: {destination}\nUkład: {structure} • Szyfrowanie: {encrypt} • Weryfikacja: {verify} • Dogrywka: {catchup} • Równolegle: {workers} • Data uzupełnienia w nazwie: {stamp}\nUtworzony: {created} • Ostatni przebieg: {last}':
        'Kaynaklar: {sources}\nHedef: {destination}\nDüzen: {structure} • Şifreleme: {encrypt} • Doğrulama: {verify} • Tamamlama: {catchup} • Paralel: {workers} • Adda tamamlama tarihi: {stamp}\nOluşturulma: {created} • Son çalıştırma: {last}',
    'Źródło nie zmieniło się w trakcie kopii — nie ma czego uzupełniać.':
        'Yedekleme sırasında kaynak değişmedi — tamamlanacak bir şey yok.',
    '—':
        '—',
    '• Kopia przyrostowa — zapisywane są wyłącznie pliki nowe i zmienione.\n  Porównanie opiera się na spisie treści kopii, rozmiarze i dacie modyfikacji;\n  przy różnicy liczona jest suma kontrolna SHA-256.\n\n• Wersje z datą — każdy przebieg tworzy kompletny folder z datą, a pliki\n  niezmienione są podpinane twardym dowiązaniem, więc nie zajmują miejsca dwa razy.\n\n• Weryfikacja po zapisie — zapisany plik jest odczytywany z powrotem\n  i porównywany ze źródłem.\n\n• Odporność na przerwania — pliki powstają pod nazwą tymczasową i są\n  podmieniane dopiero po pełnym zapisie.':
        '• Artımlı yedekleme — yalnızca yeni ve değişen dosyalar yazılır.\n  Karşılaştırma yedeğin içindekiler listesine, boyuta ve değiştirilme tarihine dayanır;\n  fark varsa SHA-256 sağlama toplamı hesaplanır.\n\n• Tarihli sürümler — her çalıştırma eksiksiz, tarihli bir klasör oluşturur;\n  değişmeyen dosyalar sabit bağlantıyla eklendiği için iki kez yer kaplamaz.\n\n• Yazma sonrası doğrulama — yazılan dosya geri okunur\n  ve kaynakla karşılaştırılır.\n\n• Kesintilere dayanıklılık — dosyalar geçici bir adla oluşturulur ve\n  ancak tamamen yazıldıktan sonra yerine konur.',
    '• Szyfr: AES-256 w trybie GCM (szyfrowanie z uwierzytelnieniem).\n• Wyprowadzanie klucza z hasła: {kdf}.\n• Nagłówek każdego pliku jest uwierzytelniony jako AAD — podmiana parametrów\n  unieważnia tag.\n• Każdy plik dostaje losowy, niepowtarzalny nonce.\n• Odszyfrowany plik powstaje dopiero po pomyślnej weryfikacji tagu.\n• Hasła nie są zapisywane w plikach programu. Opcjonalnie trafiają do\n  Menedżera poświadczeń Windows.':
        '• Şifreleme algoritması: GCM kipinde AES-256 (kimlik doğrulamalı şifreleme).\n• Paroladan anahtar türetme: {kdf}.\n• Her dosyanın başlığı AAD olarak doğrulanır — parametreleri değiştirmek\n  etiketi geçersiz kılar.\n• Her dosya rastgele, benzersiz bir nonce alır.\n• Şifresi çözülmüş dosya ancak etiket başarıyla doğrulandıktan sonra oluşturulur.\n• Parolalar programın dosyalarına yazılmaz. İsteğe bağlı olarak\n  Windows Kimlik Bilgileri Yöneticisi’ne kaydedilir.',
    'Bez hasła nie da się odczytać ani jednego pliku z kopii.':
        'Parola olmadan yedekteki tek bir dosya bile okunamaz.',
    'Co chcesz chronić?':
        'Neyi korumak istiyorsunuz?',
    'Co chcesz teraz zrobić?':
        'Şimdi ne yapmak istersiniz?',
    'Czyta kopię z nośnika i porównuje ją z zapisanymi sumami kontrolnymi.':
        'Yedeği sürücüden okur ve kaydedilmiş sağlama toplamlarıyla karşılaştırır.',
    'Dalej':
        'İleri',
    'Dokumenty i zdjęcia':
        'Belgeler ve fotoğraflar',
    'Ekran powitalny wrócisz w ustawieniach, gdy zmienisz zdanie.':
        'Fikrinizi değiştirirseniz karşılama ekranını Ayarlar’dan geri açabilirsiniz.',
    'Ekran z pytaniem, co chcesz teraz zrobić: kopia, przywracanie, sprawdzenie.':
        'Şimdi ne yapmak istediğinizi soran ekran: yedekleme, geri yükleme, kontrol.',
    'Foldery objęte kopią':
        'Yedeğe dahil klasörler',
    'Foldery z pracą. Kreator pominie katalogi, które odtwarza się jednym poleceniem (node_modules, venv, build).':
        'Çalışmalarınızın bulunduğu klasörler. Sihirbaz, tek bir komutla yeniden oluşturulabilen klasörleri (node_modules, venv, build) atlar.',
    'Gdzie zapisać kopię?':
        'Yedek nereye kaydedilsin?',
    'Historia i szyfrowanie':
        'Geçmiş ve şifreleme',
    'Historia zmian (zalecane)':
        'Değişiklik geçmişi (önerilir)',
    'Jak bardzo chcesz się zabezpieczyć?':
        'Ne kadar koruma istiyorsunuz?',
    'Jak wyżej, a dodatkowo każdy plik trafia do kopii zaszyfrowany (AES-256-GCM). Potrzebne przy kopii wożonej poza dom.':
        'Yukarıdaki gibi; ayrıca her dosya yedeğe şifreli olarak girer (AES-256-GCM). Evden dışarı götürülen bir yedek için gereklidir.',
    'Jedna aktualna kopia':
        'Tek güncel kopya',
    'Język, motyw, domyślne wykluczenia i informacje o środowisku.':
        'Dil, tema, varsayılan dışlamalar ve ortam bilgileri.',
    'Katalog docelowy leży wewnątrz źródła — wybierz inny.':
        'Hedef klasör kaynağın içinde — başka bir klasör seçin.',
    'Każdy przebieg tworzy folder z datą. Pliki niezmienione są podpinane dowiązaniem, więc historia kosztuje tyle, ile realnie się zmieniło.':
        'Her çalıştırma tarihli bir klasör oluşturur. Değişmeyen dosyalar bağlantıyla eklenir; böylece geçmiş yalnızca gerçekten değişen kadar yer kaplar.',
    'Każdy przebieg utworzy folder z datą. Pierwszy zajmie tyle, ile dane; kolejne — tyle, ile realnie się zmieniło.':
        'Her çalıştırma tarihli bir klasör oluşturacak. İlki veriler kadar yer kaplar; sonrakiler yalnızca gerçekten değişen kadar.',
    'Kopia powstanie w: {path}':
        'Yedek şurada oluşturulacak: {path}',
    'Kopia trafi do: {path}':
        'Yedek şuraya kaydedilecek: {path}',
    'Kopia: {what}':
        'Yedek: {what}',
    'Krok {number} z {total}':
        'Adım {number} / {total}',
    'Najlepiej na innym dysku fizycznym niż ten, który chronisz — kopia obok oryginału ginie razem z nim.':
        'Tercihen koruduğunuz diskten farklı bir fiziksel diskte — orijinalin yanında duran bir yedek onunla birlikte kaybolur.',
    'Najszybsza i najmniejsza. Kopia odpowiada temu, co masz teraz — bez historii wcześniejszych wersji.':
        'En hızlı ve en küçük seçenek. Yedek şu anki durumunuzla aynıdır — önceki sürümlerin geçmişi olmadan.',
    'Nie było jeszcze żadnej kopii. Zacznij od „Zrób kopię”.':
        'Henüz hiç yedek alınmadı. “Şimdi yedekle” ile başlayın.',
    'Nie lista ustawień, tylko ich skutki.':
        'Bir ayar listesi değil, ayarların sonuçları.',
    'Nie pokazuj tego ekranu przy starcie':
        'Bu ekranı başlangıçta gösterme',
    'Nośnik docelowy':
        'Hedef sürücü',
    'Odtwarza pliki z kopii — całość albo wybrany folder.':
        'Dosyaları yedekten geri yükler — tamamını ya da seçilen bir klasörü.',
    'Odśwież listę':
        'Listeyi yenile',
    'Ostatnia kopia: {when} • {count} {files}.':
        'Son yedek: {when} • {count} {files}.',
    'Pierwszy przebieg jest najdłuższy — kolejne porównują rozmiar i datę modyfikacji, więc zwykle trwają sekundy.':
        'İlk çalıştırma en uzunudur — sonrakiler boyutu ve değiştirilme tarihini karşılaştırır, bu yüzden genellikle saniyeler sürer.',
    'Pliki w kopii będą zaszyfrowane; bez hasła nie da się ich odczytać.':
        'Yedekteki dosyalar şifreli olacak; parola olmadan okunamazlar.',
    'Podfoldery są uwzględniane automatycznie.':
        'Alt klasörler otomatik olarak dahil edilir.',
    'Pokazuj ekran powitalny przy starcie':
        'Başlangıçta karşılama ekranını göster',
    'Ponownie sprawdza podłączone nośniki':
        'Bağlı sürücüleri yeniden kontrol eder',
    'Program będzie utrzymywał jeden folder zgodny ze źródłem. Każdy kolejny przebieg dopisze tylko to, co się zmieniło.':
        'Program kaynakla eşit tek bir klasör tutacak. Sonraki her çalıştırma yalnızca değişenleri ekler.',
    'Projekty i kod':
        'Projeler ve kod',
    'Przechodzi do następnego kroku':
        'Sonraki adıma geçer',
    'Przechodzi do pełnego okna programu':
        'Programın tam penceresine geçer',
    'Sam wskażesz, co ma trafić do kopii.':
        'Yedeğe neyin gireceğini siz seçersiniz.',
    'System plików: {filesystem}, klaster {cluster}':
        'Dosya sistemi: {filesystem}, küme {cluster}',
    'Ten katalog leży wewnątrz folderu źródłowego — wybierz inny.':
        'Bu klasör bir kaynak klasörün içinde — başka bir klasör seçin.',
    'Ten nośnik nie obsługuje twardych dowiązań, więc każda wersja z datą zajmie tyle miejsca co pełna kopia. Przy tym nośniku rozważ „jedną aktualną kopię”.':
        'Bu sürücü sabit bağlantıları desteklemiyor, bu yüzden her tarihli sürüm tam bir yedek kadar yer kaplayacak. Bu sürücü için “Tek güncel kopya” seçeneğini düşünün.',
    'To dysk systemowy — kopia nie przetrwa jego awarii. Jeśli masz drugi dysk albo pendrive, wybierz jego.':
        'Bu sistem sürücüsü — sürücü arızalanırsa yedek de onunla birlikte kaybolur. İkinci bir diskiniz ya da USB belleğiniz varsa onu seçin.',
    'To się wydarzy':
        'Şunlar olacak',
    'Trzy gotowe zestawy zamiast kilkunastu przełączników.':
        'Bir düzine ayar yerine üç hazır set.',
    'Twoje pliki osobiste z folderów użytkownika. Najczęstszy wybór.':
        'Kullanıcı klasörlerinizdeki kişisel dosyalarınız. En sık yapılan seçim.',
    'Uruchamia kreator, który ustawi kopię krok po kroku':
        'Yedeği adım adım ayarlayan sihirbazı başlatır',
    'Uruchom kreator…':
        'Sihirbazı başlat…',
    'Ustawia kopię krok po kroku i zapisuje ją jako szablon':
        'Yedeği adım adım ayarlar ve şablon olarak kaydeder',
    'Ustawienia pierwszej kopii':
        'İlk yedeği ayarlama',
    'Ustawienia pierwszej kopii…':
        'İlk yedeği ayarla…',
    'W tym katalogu jest już kopia ({count} {files}) — program ją uzupełni, a nie nadpisze.':
        'Bu klasörde zaten bir yedek var ({count} {files}) — program onun üzerine yazmaz, onu tamamlar.',
    'Wraca do poprzedniego kroku':
        'Önceki adıma döner',
    'Wskaż dowolny katalog docelowy':
        'İstediğiniz hedef klasörü seçin',
    'Wskaż folder kopii i kliknij „Sprawdź kopię”.':
        'Yedek klasörünü seçin ve “Yedeği kontrol et” düğmesine tıklayın.',
    'Wstecz':
        'Geri',
    'Wybierz':
        'Seç',
    'Wybierz inny folder…':
        'Başka bir klasör seç…',
    'Wybierz to, co najbliższe. Dokładną listę folderów poprawisz niżej.':
        'Size en yakın olanı seçin. Klasör listesini aşağıda ayrıntılı olarak düzenleyebilirsiniz.',
    'Wybrane foldery':
        'Seçilen klasörler',
    'Zamknij':
        'Kapat',
    'Zamyka kreator bez zapisywania':
        'Sihirbazı kaydetmeden kapatır',
    'Zapisuje nowe i zmienione pliki. Pierwszy raz trwa najdłużej.':
        'Yeni ve değişen dosyaları yazar. İlk sefer en uzun sürer.',
    'Zapisuje szablon bez uruchamiania kopii':
        'Yedeklemeyi başlatmadan şablonu kaydeder',
    'Zapisuje szablon i od razu uruchamia kopię':
        'Şablonu kaydeder ve yedeklemeyi hemen başlatır',
    'Zapisz i zrób kopię':
        'Kaydet ve yedekle',
    'Zapisz ustawienia':
        'Ayarları kaydet',
    'Zrób kopię':
        'Şimdi yedekle',
    'dysk systemowy':
        'sistem sürücüsü',
    'wolne {free} z {total}':
        'boş: {free} / {total}',
    'Porównano ze źródłem: {source}; tylko z sumą kontrolną (źródło zmieniło się albo jest niedostępne): {checksum}.':
        'Kaynakla karşılaştırılan: {source}; yalnızca sağlama toplamıyla karşılaştırılan (kaynak değişmiş ya da erişilemiyor): {checksum}.',
    'Przywraca losową próbkę plików do katalogu tymczasowego i porównuje je ze źródłem.\nSprawdza całą drogę odzyskiwania, a trwa minuty. Nic nie zostaje na dysku.':
        'Rastgele seçilen dosyaları geçici bir klasöre geri yükler ve kaynakla karşılaştırır.\nKurtarma sürecinin tamamını dener ve yalnızca dakikalar sürer. Diskte hiçbir şey kalmaz.',
    'Próbne przywrócenie':
        'Deneme geri yüklemesi',
    'W kopii nie ma plików, które dałoby się sprawdzić próbnie.':
        'Yedekte deneme geri yüklemesiyle kontrol edilebilecek dosya yok.',
    'przywrócony plik różni się od pliku źródłowego':
        'geri yüklenen dosya kaynak dosyadan farklı',
    'przywrócony plik różni się od sumy kontrolnej zapisanej podczas kopii':
        'geri yüklenen dosya, yedekleme sırasında kaydedilen sağlama toplamıyla uyuşmuyor',
    'próbne przywrócenie':
        'deneme geri yüklemesi',
    '(brak zapisanych szablonów)':
        '(kayıtlı şablon yok)',
    'Bez tego kopia planowa ruszy dopiero wtedy, gdy sam otworzysz program.':
        'Bu olmadan zamanlanmış yedekleme ancak programı kendiniz açtığınızda başlar.',
    'Codziennie o godzinie':
        'Her gün belirli saatte',
    'Codziennie o wybranej godzinie (zalecane)':
        'Her gün seçilen saatte (önerilir)',
    'Dla dysku USB podłączanego od czasu do czasu. Najwyżej jedna kopia na 12 godzin.':
        'Ara sıra takılan bir USB sürücü için. 12 saatte en fazla bir yedekleme.',
    'Dostępne w zainstalowanej wersji programu (plik EXE).':
        'Programın yüklü sürümünde (EXE dosyası) kullanılabilir.',
    'Godzina kopii codziennej (czas tego komputera).':
        'Her günkü yedeklemenin saati (bu bilgisayarın saatine göre).',
    'Harmonogram działa wtedy, gdy działa program — także ukryty przy zegarze.':
        'Zamanlama, program çalışırken çalışır — saatin yanında gizliyken de.',
    'Harmonogram nie uruchamia kopii, dopóki tego nie odznaczysz. Ręczne kopie działają.':
        'Bu işareti kaldırana kadar zamanlama hiçbir yedeklemeyi başlatmaz. Elle yedekleme çalışmaya devam eder.',
    'Harmonogram szablonu „{name}” zapisany.':
        '“{name}” şablonunun zamanlaması kaydedildi.',
    'Harmonogram:':
        'Zamanlama:',
    'Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.':
        'Bilgisayar o saatte kapalıysa yedekleme, bilgisayar açıldıktan sonra başlar.',
    'Kiedy kopia z tego szablonu ma ruszać sama.':
        'Bu şablondaki yedeklemenin ne zaman kendiliğinden başlayacağı.',
    'Kiedy robić kopię?':
        'Yedekleme ne zaman yapılsın?',
    'Kopia będzie robiona codziennie o {time}; termin przegapiony przy wyłączonym komputerze program nadrobi po jego włączeniu.':
        'Yedekleme her gün şu saatte yapılacak: {time}; bilgisayar kapalıyken kaçırılan yedeklemeyi program, bilgisayar açıldığında telafi eder.',
    'Kopia planowa nie powiodła się':
        'Zamanlanmış yedekleme başarısız oldu',
    'Kopia rusza tylko wtedy, gdy ją uruchomisz.':
        'Yedekleme yalnızca siz başlattığınızda başlar.',
    'Kopia ruszy po podłączeniu dysku docelowego (najwyżej raz na 12 godzin).':
        'Yedekleme, hedef sürücü bağlandığında başlayacak (12 saatte en fazla bir kez).',
    'Kopia ruszy po podłączeniu dysku docelowego — najwyżej raz na 12 godzin.':
        'Yedekleme, hedef sürücü bağlandığında başlar — 12 saatte en fazla bir kez.',
    'Kopia sprzed miesiąca nie chroni tego, co zmieniło się od tamtej pory.':
        'Bir ay önceki yedek, o zamandan beri değişenleri korumaz.',
    'Kopia „{name}” czeka':
        '“{name}” yedeği gecikti',
    'Kopia „{name}” nie ruszyła':
        '“{name}” yedeği başlamadı',
    'Kopie planowe działają, gdy działa program (także ukryty przy zegarze).':
        'Zamanlanmış yedeklemeler program çalışırken çalışır (saatin yanında gizliyken de).',
    'Kopie planowe działają, gdy działa program: po zamknięciu okna zostaje ikona przy zegarze, a przy logowaniu do Windows program uruchamia się w tle.':
        'Zamanlanmış yedeklemeler program çalışırken çalışır: pencere kapatıldığında saatin yanında bir simge kalır, Windows’ta oturum açtığınızda da program arka planda başlar.',
    'Kopie planowe i praca w tle':
        'Zamanlanmış yedeklemeler ve arka planda çalışma',
    'Kopie planowe wykonają się o czasie. Program zamkniesz z menu ikony przy zegarze.':
        'Zamanlanmış yedeklemeler zamanında yapılacak. Programdan, saatin yanındaki simgenin menüsünden çıkabilirsiniz.',
    'Kopię uruchamiasz przyciskiem. Najprostsze, ale łatwo o niej zapomnieć.':
        'Yedeklemeyi bir düğmeyle başlatırsınız. En basit yöntem, ama unutması kolay.',
    'Kopię uruchamiasz sam — przyciskiem w programie albo z menu ikony przy zegarze.':
        'Yedeklemeyi kendiniz başlatırsınız — programdaki düğmeyle ya da saatin yanındaki simgenin menüsünden.',
    'Następna kopia: {when}. Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.':
        'Sonraki yedekleme: {when}. Bilgisayar o saatte kapalıysa yedekleme, bilgisayar açıldıktan sonra başlar.',
    'Nie udało się zmienić startu przy logowaniu — szczegóły w dzienniku.':
        'Oturum açılışında başlatma ayarı değiştirilemedi — ayrıntılar günlükte.',
    'Od {days} dni nie było udanej kopii. Podłącz dysk docelowy albo otwórz program, żeby sprawdzić, co się dzieje.':
        '{days} gündür başarılı bir yedekleme yapılmadı. Hedef sürücüyü bağlayın ya da neler olduğunu görmek için programı açın.',
    'Otwórz Sigelith Backup':
        'Sigelith Backup’ı aç',
    'Po podłączeniu dysku docelowego':
        'Hedef sürücü bağlandığında',
    'Po podłączeniu dysku z kopią':
        'Yedek sürücüsü bağlandığında',
    'Po zamknięciu okna działaj dalej przy zegarze, gdy są kopie planowe':
        'Zamanlanmış yedeklemeler varsa pencere kapatıldıktan sonra saatin yanında çalışmaya devam et',
    'Potrzebne, żeby kopie planowe ruszały bez Twojego udziału. Hasło trafia do magazynu systemowego powiązanego z Twoim kontem, nie do plików programu.':
        'Zamanlanmış yedeklemelerin siz olmadan başlayabilmesi için gereklidir. Parola, programın dosyalarına değil, hesabınıza bağlı sistem deposuna kaydedilir.',
    'Program uruchamia się w tle przy logowaniu, więc terminy nie przepadną.':
        'Program oturum açılışında arka planda başlar, böylece hiçbir zamanlanmış yedekleme kaçırılmaz.',
    'Ręcznie':
        'Elle',
    'Ręcznie — kiedy zechcę':
        'Elle — istediğim zaman',
    'Start przy logowaniu włączony':
        'Oturum açılışında başlatma açıldı',
    'Szablon jest zaszyfrowany, a hasło nie jest zapamiętane. Kopie planowe potrzebują hasła zapisanego w Menedżerze poświadczeń Windows.':
        'Şablon şifreli ve parolası hatırlanmıyor. Zamanlanmış yedeklemeler için parolanın Windows Kimlik Bilgileri Yöneticisi’ne kaydedilmiş olması gerekir.',
    'Sigelith Backup będzie uruchamiał się w tle, żeby wykonywać kopie planowe. Wyłączysz to w ustawieniach programu.':
        'Sigelith Backup, zamanlanmış yedeklemeleri yapmak için arka planda başlayacak. Bunu programın ayarlarından kapatabilirsiniz.',
    'Sigelith Backup działa w tle':
        'Sigelith Backup arka planda çalışıyor',
    'Uruchamiaj program w tle przy logowaniu do Windows':
        'Windows’ta oturum açılınca programı arka planda başlat',
    'Wstrzymaj kopie planowe':
        'Zamanlanmış yedeklemeleri duraklat',
    'Zakończ':
        'Çıkış',
    'Zamknięcie okna chowa je, a harmonogram pilnuje terminów. Program zamkniesz z menu ikony przy zegarze.':
        'Pencereyi kapatmak onu gizler, zamanlama ise saatleri takip etmeye devam eder. Programdan, saatin yanındaki simgenin menüsünden çıkarsınız.',
    'Zrób kopię teraz':
        'Şimdi yedekle',
    '{summary} Szczegóły znajdziesz w programie, w zakładce „Dziennik”.':
        '{summary} Ayrıntılar programda, “Günlük” ekranında.',
    'Program działa z uprawnieniami administratora. Nie są mu potrzebne — kopia i przywracanie działają bez nich, a pliki zapisane przez administratora mogą później nie dać się zmienić ze zwykłego konta.':
        'Program yönetici haklarıyla çalışıyor. Bu haklara ihtiyacı yok — yedekleme ve geri yükleme onlarsız da çalışır; üstelik yönetici olarak yazılan dosyalar daha sonra normal bir hesaptan değiştirilemeyebilir.',
    'Pliki otwarte w innych programach nie trafiły do kopii: {files}. Zamknij te programy i uruchom kopię ponownie — dograne zostaną tylko te pliki.':
        'Başka programlarda açık olan dosyalar yedeğe alınmadı: {files}. Bu programları kapatıp yedeklemeyi yeniden başlatın — yalnızca bu dosyalar eklenecek.',
    'Uwaga: w źródle zmieniło się podejrzanie dużo plików — {reasons}':
        'Uyarı: kaynakta şüpheli derecede çok dosya değişti — {reasons}',
    'Wstrzymano kopię: w źródle zmieniło się podejrzanie dużo plików. {reasons}':
        'Yedekleme duraklatıldı: kaynakta şüpheli derecede çok dosya değişti. {reasons}',
    'Zmieniło się albo zniknęło {count} z {previous} plików poprzedniej kopii.':
        'Önceki yedekteki {previous} dosyadan {count} tanesi değişti ya da kayboldu.',
    '{suspicious} z {evaluated} sprawdzonych zmienionych plików ma treść, która nie pasuje do ich typu (wygląda na zaszyfrowaną).':
        'Kontrol edilen {evaluated} değişmiş dosyadan {suspicious} tanesinin içeriği türüne uymuyor (şifrelenmiş görünüyor).',
    'Kontynuuj mimo to':
        'Yine de devam et',
    'Kopia planowa wstrzymana':
        'Zamanlanmış yedekleme duraklatıldı',
    'Kopia wstrzymana do decyzji.':
        'Yedekleme, siz karar verene kadar duraklatıldı.',
    'Kopia wstrzymana — w źródle zmieniło się podejrzanie dużo plików.':
        'Yedekleme duraklatıldı — kaynakta şüpheli derecede çok dosya değişti.',
    'Podejrzanie dużo zmian':
        'Şüpheli derecede çok değişiklik',
    'Wstrzymaj kopię':
        'Yedeklemeyi duraklat',
    '{reasons}\n\nJeśli to spodziewane — aktualizacja programu, przeniesienie albo przerobienie wielu plików — kontynuuj.\n\nJeśli nie, NIE kontynuuj: tak wygląda działanie oprogramowania szyfrującego pliki (ransomware). Sprawdź najpierw, czy Twoje pliki dają się otworzyć. Wcześniejsze wersje w kopii pozostają nietknięte.':
        '{reasons}\n\nBu bekleniyorsa — bir yazılım güncellemesi, çok sayıda dosyanın taşınması ya da yeniden düzenlenmesi — devam edin.\n\nBeklenmiyorsa devam ETMEYİN: dosyaları şifreleyen kötü amaçlı yazılımlar (fidye yazılımı) tam böyle görünür. Önce dosyalarınızın açılıp açılmadığını kontrol edin. Yedekteki önceki sürümlere dokunulmaz.',
    '{reasons} To może być działanie złośliwego oprogramowania szyfrującego pliki. Otwórz program, sprawdź pliki i uruchom kopię ręcznie.':
        '{reasons} Bu, dosyaları şifreleyen kötü amaçlı bir yazılımın işi olabilir. Programı açın, dosyalarınızı kontrol edin ve yedeklemeyi elle başlatın.',
    'Pominięto {count} {files}.':
        '{count} {files} atlandı.',
    'Ponawiam {count} {files}…':
        '{count} {files} yeniden deneniyor…',
    ' (bez {count} {files})':
        ' ({count} {files} yedeğe alınmadı)',
    'plik otwarty w innym programie':
        'dosya, başka bir programda açık olduğu için',
    'pliki otwarte w innych programach':
        'dosya, başka programlarda açık olduğu için',
    'plików otwartych w innych programach':
        'dosya, başka programlarda açık olduğu için',
    'pliku otwartego w innym programie':
        'dosya, başka bir programda açık olduğu için',
    '\n\n…i kolejne: {count}.':
        '\n\n…ve {count} tane daha.',
    'Foldery objęte kopią ({count}): {list}':
        'Yedeğe dahil klasörler ({count}): {list}',
    'Nośnik nie obsługuje twardych dowiązań — kopiuję do nowej wersji niezmienione pliki: {count} ({size})…':
        'Sürücü sabit bağlantıları desteklemiyor — değişmeyen dosyalar yeni sürüme kopyalanıyor: {count} ({size})…',
    'Pliki bez sumy kontrolnej sprawdzone tylko co do rozmiaru, bo ich źródło zmieniło się albo jest niedostępne: {count}.':
        'Sağlama toplamı olmadığı ve kaynağı değiştiği ya da erişilemediği için yalnızca boyutu kontrol edilen dosyalar: {count}.',
    'Pliki bez zapisanej sumy kontrolnej, porównane ze źródłem i uzupełnione w spisie treści: {count}.':
        'Kayıtlı sağlama toplamı olmayan, kaynakla karşılaştırılıp içindekiler listesine eklenen dosyalar: {count}.',
    'Pliki przeniesione w źródle: {count} — trafią do kopii bez przesyłania danych.':
        'Kaynakta taşınan dosyalar: {count} — veri aktarılmadan yedeğe eklenecek.',
    'Pliki skasowane w źródle: {count} — {action}.':
        'Kaynakta silinen dosyalar: {count} — {action}.',
    'Pliki z końcówką dopisaną do nazwy, których oryginały zniknęły: {count}.':
        'Adının sonuna ek eklenmiş ve orijinali kaybolmuş dosyalar: {count}.',
    'Pliki zmienione w trakcie kopiowania: {count} — zostaną zapisane ponownie w przebiegu uzupełniającym.':
        'Kopyalanırken değişen dosyalar: {count} — tamamlama geçişinde yeniden yazılacak.',
    'Pliki, których brakuje w kopii i które zostaną zapisane ponownie: {count}.':
        'Yedekte eksik olan ve yeniden yazılacak dosyalar: {count}.',
    'Podpinanie niezmienionych plików do nowej wersji: {count}…':
        'Değişmeyen dosyalar yeni sürüme bağlanıyor: {count}…',
    'Pomijam pliki, które już są w tej wersji kopii: {count}.':
        'Yedeğin bu sürümünde zaten bulunan dosyalar atlanıyor: {count}.',
    'Porządkowanie historii — usunięte najstarsze wersje: {count}.':
        'Geçmiş temizleniyor — silinen en eski sürümler: {count}.',
    'Przenoszenie plików, które zmieniły miejsce w źródle: {count}…':
        'Kaynakta yeri değişen dosyalar taşınıyor: {count}…',
    'Próbne przywrócenie losowo wybranych plików: {count}…':
        'Rastgele seçilen dosyaların deneme geri yüklemesi: {count}…',
    'Usuwanie z kopii plików skasowanych w źródle: {count}…':
        'Kaynakta silinen dosyalar yedekten kaldırılıyor: {count}…',
    'Uzupełniam kopię o pliki, które przybyły lub zmieniły się w trakcie: {count} ({size})…':
        'Bu arada eklenen ya da değişen dosyalar yedeğe ekleniyor: {count} ({size})…',
    'Uzupełnianie wersji {version} — pliki już zapisane, które zostaną pominięte: {count}.':
        '{version} sürümü tamamlanıyor — zaten yazılmış olduğu için atlanacak dosyalar: {count}.',
    'Wznawiam wersję {version} — już zapisane: {done}, do dogrania: {todo}.':
        '{version} sürümüne devam ediliyor — zaten yazılmış: {done}, kalan: {todo}.',
    'pliku':
        'dosya',
    'Brak fragmentu {cid} w magazynie kopii.':
        'Yedeğin parça deposunda {cid} parçası yok.',
    'Brak opisu magazynu fragmentów w katalogu kopii.':
        'Yedek klasöründe parça deposunun tanımı yok.',
    'Duże pliki zapisuj różnicowo (od 256 MB)':
        'Büyük dosyaları artımlı kaydet (256 MB ve üzeri)',
    'Fragment {cid} jest uszkodzony.':
        '{cid} parçası bozuk.',
    'Kolejna wersja dużego pliku — maszyny wirtualnej, skrzynki pocztowej, bazy —\nzapisuje tylko zmienione fragmenty zamiast całego pliku. W kopii taki plik\nleży jako przepis + fragmenty; złoży go program albo skrypt ratunkowy.':
        'Büyük bir dosyanın — sanal makine, posta kutusu, veritabanı — sonraki sürümünde\ndosyanın tamamı yerine yalnızca değişen parçalar kaydedilir. Yedekte böyle bir dosya\ntarif + parçalar olarak durur; onu program ya da kurtarma betiği yeniden birleştirir.',
    'Opis magazynu fragmentów jest uszkodzony.':
        'Parça deposunun tanımı bozuk.',
    'Plik złożony z fragmentów różni się od zapisanego w przepisie.':
        'Parçalardan birleştirilen dosya, tarifte kayıtlı olandan farklı.',
    'Podane hasło nie pasuje do fragmentów zapisanych wcześniej w tej kopii.':
        'Girilen parola, bu yedeğe daha önce yazılmış parçalarla eşleşmiyor.',
    'Przepis pliku jest uszkodzony.':
        'Dosyanın tarifi bozuk.',
    'To nie jest przepis pliku zapisanego fragmentami.':
        'Bu, parçalar hâlinde kaydedilmiş bir dosyanın tarifi değil.',
    'Usunięto nieużywane fragmenty dużych plików: {count} ({size}).':
        'Büyük dosyaların kullanılmayan parçaları kaldırıldı: {count} ({size}).',
    ', zakotwiczona w Bitcoinie':
        ', Bitcoin’e çıpalandı',
    'Adres usługi:':
        'Hizmet adresi:',
    'Brak fragmentu {cid} w kopii poza domem.':
        'Tesis dışı yedekte {cid} parçası yok.',
    'Brak klucza albo hasła w Menedżerze poświadczeń Windows — zapisz ustawienia kopii poza domem jeszcze raz.':
        'Windows Kimlik Bilgileri Yöneticisi’nde anahtar ya da parola yok — tesis dışı yedek ayarlarını yeniden kaydedin.',
    'Brak spisu wersji, którego dotyczy znacznik.':
        'Zaman damgasının ait olduğu sürüm listesi yok.',
    'Certyfikat PDF':
        'PDF sertifikası',
    'Druga, zaszyfrowana kopia w usłudze zgodnej z S3 (np. Backblaze B2)':
        'S3 uyumlu bir hizmette ikinci, şifreli bir yedek (ör. Backblaze B2)',
    'Folder w kubełku:':
        'Kovadaki klasör:',
    'Hasło kopii poza domem':
        'Tesis dışı yedek parolası',
    'Hasło kopii poza domem nie pasuje do danych zapisanych w tym miejscu.':
        'Tesis dışı yedek parolası, orada kayıtlı verilerle eşleşmiyor.',
    'Hasło kopii poza domem powinno mieć co najmniej 10 znaków.':
        'Tesis dışı yedek parolası en az 10 karakter olmalıdır.',
    'Hasło szyfrowania:':
        'Şifreleme parolası:',
    'Identyfikator klucza:':
        'Anahtar kimliği:',
    'Katalog, do którego trafią pliki':
        'Dosyaların yazılacağı klasör',
    'Klucz tajny':
        'Gizli anahtar',
    'Klucz tajny:':
        'Gizli anahtar:',
    'Kopia na dysku obok komputera nie przetrwa pożaru ani kradzieży. Tu ustawisz drugą kopię w usłudze zgodnej z S3 (np. Backblaze B2). Pliki są szyfrowane na tym komputerze osobnym hasłem — usługa widzi tylko nieczytelne fragmenty.':
        'Bilgisayarın yanındaki bir diskte duran yedek, yangından ya da hırsızlıktan kurtulamaz. Burada S3 uyumlu bir hizmette (ör. Backblaze B2) ikinci bir yedek ayarlarsınız. Dosyalar bu bilgisayarda ayrı bir parolayla şifrelenir — hizmet yalnızca okunamayan parçalar görür.',
    'Kopia poza domem':
        'Tesis dışı yedek',
    'Kopia poza domem dla szablonu „{name}” zapisana.':
        '“{name}” şablonu için tesis dışı yedek kaydedildi.',
    'Kopia poza domem nie ruszyła':
        'Tesis dışı yedekleme başlamadı',
    'Kopia poza domem potrzebuje Menedżera poświadczeń Windows, a jest on niedostępny.':
        'Tesis dışı yedek için Windows Kimlik Bilgileri Yöneticisi gerekiyor, ancak kullanılamıyor.',
    'Kopia poza domem „{name}”':
        'Tesis dışı yedek “{name}”',
    'Kopia poza domem…':
        'Tesis dışı yedek…',
    'Korzeń tygodnia zakotwiczony w łańcuchu Bitcoina.':
        'Hafta kökü Bitcoin zincirine çıpalandı.',
    'Kubełek (bucket):':
        'Kova (bucket):',
    'Migawek w usłudze: {count}.':
        'Hizmetteki anlık görüntüler: {count}.',
    'Migawka i cel':
        'Anlık görüntü ve hedef',
    'Migawka kopii poza domem jest uszkodzona.':
        'Tesis dışı yedeğin anlık görüntüsü bozuk.',
    'Migawka {stamp}: plików bez zmian {reused}, wysłanych {files}, nowych fragmentów {chunks} ({size}).':
        'Anlık görüntü {stamp}: değişmeyen dosya {reused}, gönderilen dosya {files}, yeni parça {chunks} ({size}).',
    'MinIO / Wasabi / inna zgodna z S3':
        'MinIO / Wasabi / başka bir S3 uyumlu hizmet',
    'NIEPOPRAWNY':
        'GEÇERSİZ',
    'Nie ma migawki {stamp} w kopii poza domem.':
        'Tesis dışı yedekte {stamp} anlık görüntüsü yok.',
    'Nie udało się połączyć z usługą przechowywania: {error}':
        'Depolama hizmetine bağlanılamadı: {error}',
    'Nie udało się wczytać migawek: {error}':
        'Anlık görüntüler yüklenemedi: {error}',
    'Nie udało się zapisać klucza albo hasła w magazynie systemowym.':
        'Anahtar ya da parola sistem deposuna kaydedilemedi.',
    'Odśwież z sieci':
        'Çevrimiçi yenile',
    'Opis kopii poza domem jest uszkodzony.':
        'Tesis dışı yedeğin tanımı bozuk.',
    'Oznakowana: {utc} (BeatTime {beat})':
        'Damgalandı: {utc} (BeatTime {beat})',
    'Pliki wersji różnią się od spisu, który został oznakowany.':
        'Sürümün dosyaları, zaman damgası verilen listeden farklı.',
    'Pobiera i odszyfrowuje pliki wybranej migawki':
        'Seçilen anlık görüntünün dosyalarını indirir ve şifrelerini çözer',
    'Pobiera listę migawek z usługi':
        'Anlık görüntü listesini hizmetten indirir',
    'Pobiera podpis tygodnia i stan kotwicy w Bitcoinie':
        'Haftalık imzayı ve Bitcoin çıpasının durumunu indirir',
    'Pobieram potwierdzenia…':
        'Makbuzlar indiriliyor…',
    'Podaj hasło szyfrowania kopii poza domem.':
        'Tesis dışı yedeğin şifreleme parolasını girin.',
    'Podaj klucz tajny usługi.':
        'Hizmetin gizli anahtarını girin.',
    'Podam dane ręcznie':
        'Bilgileri kendim gireceğim',
    'Pominięte (otwarte w innych programach albo zmienione w trakcie): {count}.':
        'Atlanan (başka programlarda açık ya da bu sırada değişmiş): {count}.',
    'Porządkowanie kopii poza domem…':
        'Tesis dışı yedek temizleniyor…',
    'Potwierdzenia odświeżone.':
        'Makbuzlar yenilendi.',
    'Poza dom':
        'Tesis dışı',
    'Połączenie działa: zapis, odczyt i usuwanie się udały.':
        'Bağlantı çalışıyor: yazma, okuma ve silme başarılı.',
    'Połączenie nie działa: {error}':
        'Bağlantı çalışmıyor: {error}',
    'Przywraca pliki z zaszyfrowanej kopii w usłudze S3 — także na nowym komputerze':
        'Dosyaları S3 hizmetindeki şifreli yedekten geri yükler — yeni bir bilgisayarda da',
    'Przywracanie z kopii poza domem':
        'Tesis dışı yedekten geri yükleme',
    'Przywracanie {count} {files} z kopii poza domem…':
        'Tesis dışı yedekten geri yükleniyor: {count} {files}…',
    'Przywróć':
        'Geri yükle',
    'Region:':
        'Bölge:',
    'Skąd':
        'Kaynak',
    'Spis wersji zgodny ze znacznikiem: {answer}':
        'Sürüm listesi zaman damgasıyla eşleşiyor: {answer}',
    'Spis wersji został zmieniony po oznakowaniu.':
        'Sürüm listesi, zaman damgası verildikten sonra değiştirilmiş.',
    'Sprawdza spis wersji, drogę w drzewie tygodnia i podpis — bez sieci':
        'Sürüm listesini, hafta ağacındaki yolu ve imzayı kontrol eder — ağ olmadan',
    'Sprawdzam połączenie…':
        'Bağlantı kontrol ediliyor…',
    'Sprawdź':
        'Kontrol et',
    'Sprawdź połączenie':
        'Bağlantıyı kontrol et',
    'Starsze migawki są usuwane, gdy nadmiar sięgnie kilku — co kilka dni.':
        'Fazladan birkaç anlık görüntü biriktiğinde eskileri silinir — birkaç günde bir.',
    'Suma w drzewie tygodnia: {answer}':
        'Özet hafta ağacında: {answer}',
    'Suma wersji nie należy do drzewa tygodnia podanego w potwierdzeniu.':
        'Sürümün özeti, makbuzda belirtilen hafta ağacına ait değil.',
    'Ta wersja nie ma znacznika czasu.':
        'Bu sürümün zaman damgası yok.',
    'Także po kopiach planowych. Wysyłane są tylko pliki nowe i zmienione.':
        'Zamanlanmış yedeklemelerden sonra da. Yalnızca yeni ve değişen dosyalar gönderilir.',
    'Tydzień jeszcze się nie zamknął — podpis pojawi się po poniedziałku 00:00 UTC.':
        'Hafta henüz kapanmadı — imza pazartesi 00:00 UTC’den sonra gelecek.',
    'Usunięto starsze migawki: {count}, nieużywane fragmenty: {chunks}.':
        'Silinen eski anlık görüntüler: {count}, kullanılmayan parçalar: {chunks}.',
    'Usługa chwilowo niedostępna ({status}).':
        'Hizmet geçici olarak kullanılamıyor ({status}).',
    'Usługa odrzuciła żądanie ({status} {code}): {message}':
        'Hizmet isteği reddetti ({status} {code}): {message}',
    'Usługa przechowywania':
        'Depolama hizmeti',
    'Usługa zwróciła inną treść niż zapisana.':
        'Hizmet, yazılandan farklı bir içerik döndürdü.',
    'Usługa:':
        'Hizmet:',
    'Uzupełnij adres usługi, nazwę kubełka i klucze dostępu.':
        'Hizmet adresini, kova adını ve erişim anahtarlarını girin.',
    'Uzupełnij adres usługi, region, kubełek i identyfikator klucza.':
        'Hizmet adresini, bölgeyi, kovayı ve anahtar kimliğini girin.',
    'W tym katalogu kopii nie ma jeszcze znaczników czasu.':
        'Bu yedek klasöründe henüz zaman damgası yok.',
    'W tym miejscu nie ma jeszcze kopii poza domem.':
        'Bu konumda henüz tesis dışı yedek yok.',
    'Wczytaj migawki':
        'Anlık görüntüleri yükle',
    'Wczytaj migawki i wybierz jedną z listy.':
        'Anlık görüntüleri yükleyin ve listeden birini seçin.',
    'Wczytuję migawkę {stamp}…':
        'Anlık görüntü yükleniyor: {stamp}…',
    'Wczytuję poprzednią migawkę kopii poza domem…':
        'Tesis dışı yedeğin önceki anlık görüntüsü yükleniyor…',
    'Wybierz migawkę i katalog, do którego trafią pliki.':
        'Bir anlık görüntü ve dosyaların yazılacağı klasörü seçin.',
    'Wybierz wersję z listy.':
        'Listeden bir sürüm seçin.',
    'Wysyłaj poza dom po każdej udanej kopii z tego szablonu':
        'Bu şablondaki her başarılı yedeklemeden sonra tesis dışına gönder',
    'Wysyłam poza dom pliki nowe i zmienione: {count}…':
        'Yeni ve değişen dosyalar tesis dışına gönderiliyor: {count}…',
    'Z kopii poza domem…':
        'Tesis dışı yedekten…',
    'Zachowuj migawek:':
        'Saklanacak anlık görüntü:',
    'Zapisuje ustawienia; klucz i hasło trafiają do Menedżera poświadczeń Windows':
        'Ayarları kaydeder; anahtar ve parola Windows Kimlik Bilgileri Yöneticisi’ne kaydedilir',
    'Zapisuje, odczytuje i usuwa mały plik próbny':
        'Küçük bir deneme dosyası yazar, okur ve siler',
    'Zapisuję migawkę {stamp}…':
        'Anlık görüntü kaydediliyor: {stamp}…',
    'Znacznik dowodzi, że wersja kopii w dokładnie tym kształcie istniała w podanej chwili. Podpis tygodnia pojawia się po jego zamknięciu (poniedziałek 00:00 UTC), a kotwica w Bitcoinie — zwykle kilka godzin później.':
        'Zaman damgası, yedek sürümünün tam olarak bu hâliyle belirtilen anda var olduğunu kanıtlar. Haftalık imza hafta kapandıktan sonra (pazartesi 00:00 UTC), Bitcoin çıpası ise genellikle birkaç saat sonra gelir.',
    'Znacznika czasu nie udało się zapisać: {error}':
        'Zaman damgası kaydedilemedi: {error}',
    'Znaczniki czasu':
        'Zaman damgaları',
    'Znaczniki czasu…':
        'Zaman damgaları…',
    'kopia poza domem':
        'tesis dışı yedek',
    'np. komputer-domowy':
        'ör. ev-pc',
    'oznakowana {when} — podpis po zamknięciu tygodnia':
        '{when} tarihinde damgalandı — imza hafta kapanınca gelecek',
    'podpisana (tydzień {week}){bitcoin}':
        'imzalandı (hafta {week}){bitcoin}',
    'poprawny':
        'geçerli',
    'przywracanie z kopii poza domem':
        'tesis dışı yedekten geri yükleme',
    'Łączę się z usługą…':
        'Hizmete bağlanılıyor…',
    ' dni':
        ' gün',
    ' mies.':
        ' ay',
    ' tyg.':
        ' hafta',
    'Ile ostatnich wersji zachować. Starsze są kasowane po udanym przebiegu.':
        'Son kaç sürümün saklanacağı. Daha eskileri başarılı bir çalıştırmadan sonra silinir.',
    'Kalendarz zostawia najnowszą wersję z każdego z ostatnich dni, tygodni\ni miesięcy — gęsto dla świeżych zmian, rzadko dla dawnych. Nadmiar jest\nkasowany po udanym przebiegu; wersje niedokończone nigdy.':
        'Takvim, son günlerin, haftaların ve ayların her birinden en yeni sürümü\nsaklar — yeni değişiklikler için sık, eskiler için seyrek. Fazlası başarılı\nbir çalıştırmadan sonra silinir; tamamlanmamış sürümler asla silinmez.',
    'Z ilu ostatnich dni zachować po jednej, najnowszej wersji.':
        'Son kaç günün her birinden en yeni birer sürümün saklanacağı.',
    'Z ilu ostatnich miesięcy zachować po jednej, najnowszej wersji.':
        'Son kaç ayın her birinden en yeni birer sürümün saklanacağı.',
    'Z ilu ostatnich tygodni zachować po jednej, najnowszej wersji.':
        'Son kaç haftanın her birinden en yeni birer sürümün saklanacağı.',
    'Zachowuj:':
        'Sakla:',
    'kalendarz: dni, tygodnie, miesiące':
        'takvim: günler, haftalar, aylar',
    'ostatnie wersje':
        'son sürümler',
    'wszystkie wersje':
        'tüm sürümler',
    ' (niedokończona)':
        ' (tamamlanmamış)',
    'Fragment nazwy albo ścieżki, bez rozróżniania wielkości liter.':
        'Ad ya da yolun bir parçası; büyük/küçük harf duyarsız.',
    'Główny folder kopii':
        'Yedeğin ana klasörü',
    'Historia pliku':
        'Dosya geçmişi',
    'Nazwa':
        'Ad',
    'Nic nie znaleziono.':
        'Hiçbir şey bulunamadı.',
    'Nie udało się: {error}':
        'Başarısız: {error}',
    'Odtwarza plik do katalogu tymczasowego i otwiera go':
        'Dosyayı geçici bir klasöre geri yükler ve açar',
    'Odtwarza plik w wybranym miejscu':
        'Dosyayı seçtiğiniz konuma geri yükler',
    'Odtwarzam „{name}”…':
        '“{name}” geri yükleniyor…',
    'Otwarto kopię „{name}” (plik tymczasowy, zniknie po zamknięciu programu).':
        '“{name}” dosyasının kopyası açıldı (geçici bir dosya; program kapanınca silinir).',
    'Otwórz':
        'Aç',
    'Otwórz kopię':
        'Kopyayı aç',
    'Pliki i wersje wprost z kopii — bez przywracania':
        'Dosyalar ve sürümler doğrudan yedekten — geri yüklemeden',
    'Pliki i wersje wprost z kopii — bez przywracania całości.':
        'Dosyalar ve sürümler doğrudan yedekten — tamamını geri yüklemeden.',
    'Pokazuje pliki i wersje tej kopii — pojedynczy plik otworzysz bez przywracania całości':
        'Bu yedeğin dosyalarını ve sürümlerini gösterir — tek bir dosyayı her şeyi geri yüklemeden açabilirsiniz',
    'Pokaż foldery':
        'Klasörleri göster',
    'Przeglądaj…':
        'Göz at…',
    'Przeglądanie':
        'Göz atma',
    'Przeszukuje spis treści kopii':
        'Yedeğin içindekiler listesinde arar',
    'Rozmiar':
        'Boyut',
    'Szukaj':
        'Ara',
    'Szukaj pliku w najnowszym stanie kopii…':
        'Yedeğin en son durumunda dosya ara…',
    'Szukam…':
        'Aranıyor…',
    'W których wersjach jest ten plik i kiedy się zmieniał':
        'Bu dosyanın hangi sürümlerde bulunduğu ve ne zaman değiştiği',
    'W tym folderze nie ma wersji kopii.':
        'Bu klasörde yedek sürümü yok.',
    'Wczytuje wersje z tego folderu kopii':
        'Bu yedek klasöründeki sürümleri yükler',
    'Wersja kopii, której zawartość widzisz poniżej.':
        'İçeriğini aşağıda gördüğünüz yedek sürümü.',
    'Wersja: {version}':
        'Sürüm: {version}',
    'Wersje z tym plikiem: {count}. Dwuklik otwiera kopię z danej wersji.':
        'Bu dosyayı içeren sürümler: {count}. Çift tıklama, o sürümdeki kopyayı açar.',
    'Wraca z wyników wyszukiwania do drzewa folderów':
        'Arama sonuçlarından klasör ağacına döner',
    'Wskaż folder kopii i kliknij „Otwórz”.':
        'Yedek klasörünü seçin ve “Aç” düğmesine tıklayın.',
    'Zapisano: {path}':
        'Kaydedildi: {path}',
    'Zapisz jako…':
        'Farklı kaydet…',
    'Zapisz kopię pliku':
        'Dosyanın kopyasını kaydet',
    'Zaznacz plik i wybierz „Otwórz kopię”, żeby zajrzeć do niego w zwykłym programie, albo „Historia pliku”, żeby zobaczyć, w których wersjach się zmieniał.':
        'Bir dosya seçin; dosyayı her zamanki programında görmek için “Kopyayı aç” düğmesini, hangi sürümlerde değiştiğini görmek için “Dosya geçmişi” düğmesini kullanın.',
    'Zmieniono':
        'Değiştirme tarihi',
    'Znalezione pliki: {count}. Wyniki pochodzą z najnowszego stanu kopii.':
        'Bulunan dosyalar: {count}. Sonuçlar yedeğin en son durumundan.',
    'przeglądanie kopii':
        'yedeğe göz atma',
    'zmieniony':
        'değişen',
    'najstarsza zachowana kopia':
        'saklanan en eski kopya',
    'Foldery w AppData':
        'AppData’daki klasörler',
    'Przywracanie utworzy nowe foldery bezpośrednio w AppData:\n\n{folders}\n\nWindows pozwala wersji programu ze Sklepu tworzyć je tylko w jej prywatnej kopii — pliki będą widoczne w tym programie, ale nie w programie, do którego należą.\n\nNajprościej: zainstaluj i raz uruchom tamten program (utworzy swój folder), a potem przywróć jeszcze raz. Albo przywróć do zwykłego folderu i przenieś pliki Eksploratorem.':
        'Geri yükleme doğrudan AppData içinde yeni klasörler oluşturacak:\n\n{folders}\n\nWindows, bu programın Microsoft Store sürümünün bunları yalnızca kendi özel kopyasında oluşturmasına izin verir — dosyalar bu programda görünür, ancak ait oldukları programda görünmez.\n\nEn kolayı: o programı yükleyip bir kez çalıştırın (kendi klasörünü oluşturur), ardından yeniden geri yükleyin. Ya da normal bir klasöre geri yükleyip dosyaları Dosya Gezgini ile taşıyın.',
    'Przywracanie utworzyłoby w AppData nowe foldery, których inne programy nie zobaczą: {folders}':
        'Geri yükleme, AppData içinde diğer programların göremeyeceği yeni klasörler oluştururdu: {folders}',
    'Przywracanie wstrzymane do decyzji.':
        'Geri yükleme, siz karar verene kadar duraklatıldı.',
    'Przywróć mimo to':
        'Yine de geri yükle',
    'Start programu przy logowaniu wyłączono w Ustawieniach Windows. Włączysz go tam: Ustawienia → Aplikacje → Uruchamianie → Sigelith Backup.':
        'Programın oturum açılışında başlatılması Windows Ayarları’nda kapatıldı. Oradan açabilirsiniz: Ayarlar → Uygulamalar → Başlangıç → Sigelith Backup.',
    'Start przy logowaniu':
        'Oturum açılışında başlatma',
    'Start przy logowaniu wyłączono w Ustawieniach Windows → Aplikacje → Uruchamianie; dopóki go tam nie włączysz, kopie planowe działają tylko przy otwartym programie.':
        'Oturum açılışında başlatma, Windows Ayarları → Uygulamalar → Başlangıç bölümünde kapatıldı; orada yeniden açana kadar zamanlanmış yedeklemeler yalnızca program açıkken çalışır.',
    'Ten sam przełącznik jest w Ustawieniach Windows → Aplikacje → Uruchamianie. Wyłączony tam da się włączyć tylko tam.':
        'Aynı anahtar Windows Ayarları → Uygulamalar → Başlangıç bölümünde de var. Orada kapatıldıysa yalnızca oradan yeniden açılabilir.',
    'Brak pliku {name} w katalogu programu.':
        'Program klasöründe {name} dosyası yok.',
    'Jakie dane program przetwarza i gdzie':
        'Program hangi verileri nerede işler',
    'Kod źródłowy Qt':
        'Qt kaynak kodu',
    'Licencja programu':
        'Program lisansı',
    'Licencja programu i licencje użytych składników':
        'Programın lisansı ve kullanılan bileşenlerin lisansları',
    'Licencje':
        'Lisanslar',
    'Licencje i prywatność':
        'Lisanslar ve gizlilik',
    'Licencje…':
        'Lisanslar…',
    'Otwiera folder z plikami licencji w Eksploratorze':
        'Lisans dosyalarının bulunduğu klasörü Dosya Gezgini’nde açar',
    'Pokaż pliki licencji':
        'Lisans dosyalarını göster',
    'Polityka prywatności':
        'Gizlilik politikası',
    'Polityka prywatności…':
        'Gizlilik politikası…',
    'Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0 — to osobne pliki w katalogu programu, które można zastąpić zgodnymi wersjami. Kod źródłowy wersji dołączonych do programu: {qt} oraz {pyside}.':
        'Program, LGPL-3.0 lisanslı Qt ve PySide6 kitaplıklarını kullanır — bunlar program klasöründe ayrı dosyalardır ve uyumlu sürümlerle değiştirilebilir. Programla birlikte gelen sürümlerin kaynak kodu: {qt} ve {pyside}.',
    'Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0, z Pythona i z innych składników na licencjach otwartych (m.in. MIT, BSD, Apache 2.0); ikony: Bootstrap Icons (MIT). Wykaz, prawa autorskie, pełne teksty licencji i adresy kodu źródłowego Qt są pod przyciskiem „Licencje”.':
        'Program, LGPL-3.0 lisanslı Qt ve PySide6 kitaplıklarını, Python’ı ve açık kaynak lisanslı diğer bileşenleri (MIT, BSD, Apache 2.0 vb.) kullanır; simgeler: Bootstrap Icons (MIT). Liste, telif hakkı bildirimleri, tam lisans metinleri ve Qt kaynak kodu adresleri “Lisanslar” düğmesinin altındadır.',
    'Program usunie z Menedżera poświadczeń Windows wszystkie hasła, które zapamiętał: hasła kopii i dane dostępu do kopii poza domem. Kopie planowe szablonów zaszyfrowanych będą potem czekać, aż podasz hasło.\n\nUsunąć?':
        'Program, hatırladığı tüm parolaları Windows Kimlik Bilgileri Yöneticisi’nden silecek: yedek parolalarını ve tesis dışı yedeğin erişim bilgilerini. Şifreli şablonların zamanlanmış yedeklemeleri bundan sonra siz parolayı girene kadar bekleyecek.\n\nSilinsin mi?',
    'Składniki i ich licencje':
        'Bileşenler ve lisansları',
    'Strona z kodem źródłowym Qt w wersji użytej w programie':
        'Programda kullanılan Qt sürümünün kaynak kodunun bulunduğu sayfa',
    'Usunięte zapamiętane hasła: {count}.':
        'Silinen hatırlanan parolalar: {count}.',
    'Usuwa z Menedżera poświadczeń Windows wszystkie hasła zapamiętane przez program — na przykład przed odinstalowaniem':
        'Programın hatırladığı tüm parolaları Windows Kimlik Bilgileri Yöneticisi’nden siler — örneğin kaldırmadan önce',
    'Usuń zapamiętane hasła':
        'Hatırlanan parolaları sil',
    'Usuń zapamiętane hasła…':
        'Hatırlanan parolaları sil…',
    '© {years} {publisher}. Wolne oprogramowanie na licencji GNU GPL w wersji 3 lub nowszej.':
        '© {years} {publisher}. GNU GPL sürüm 3 veya üzeri kapsamında özgür yazılım.',
    'Kod źródłowy':
        'Kaynak kodu',
    'Kod źródłowy programu w serwisie GitHub':
        'Programın GitHub’daki kaynak kodu',
    'Sigelith odrzucił żądanie ({status}): {detail}':
        'Sigelith isteği reddetti ({status}): {detail}',
    'Nie udało się połączyć z Sigelith: {error}':
        'Sigelith’e bağlanılamadı: {error}',
    'Sigelith odesłał potwierdzenie innej sumy kontrolnej.':
        'Sigelith başka bir özete ait makbuz döndürdü.',
    'Znacznik czeka na połączenie z Sigelith.':
        'Zaman damgası Sigelith ile bağlantı bekliyor.',
    'Podpis tygodnia nie zgadza się z kluczem Sigelith zapisanym w programie.':
        'Haftalık imza, programa yerleşik Sigelith anahtarıyla eşleşmiyor.',
    'Otwiera certyfikat znacznika na stronie Sigelith':
        'Zaman damgası sertifikasını Sigelith web sitesinde açar',
    'Podpis Sigelith: {answer}':
        'Sigelith imzası: {answer}',
    'Znaczniki Sigelith wersji w tym katalogu kopii: sprawdzenie i certyfikat':
        'Bu yedek klasöründeki sürümlerin Sigelith zaman damgaları: kontrol ve sertifika',
    'Znakuję wersję czasem Sigelith (wysyłana jest tylko suma kontrolna)…':
        'Sürüme Sigelith zaman damgası veriliyor (yalnızca özet gönderilir)…',
    'Znacznik czasu czeka na połączenie z Sigelith — zostanie wysłany przy następnej kopii.':
        'Zaman damgası Sigelith ile bağlantı bekliyor — bir sonraki yedeklemede gönderilecek.',
    'Znakuj wersję czasem Sigelith':
        'Sürüme Sigelith zaman damgası ver',
    'Znaczniki czasu Sigelith':
        'Sigelith zaman damgaları',
    'czeka na połączenie z Sigelith':
        'Sigelith ile bağlantı bekleniyor',
    'Dowód, że kopia w tym kształcie istniała danego dnia (podpis Ed25519, kotwica\nw Bitcoinie). Do sigelith.org trafia wyłącznie suma kontrolna spisu wersji —\nżadne nazwy plików ani ich treść.':
        'Yedeğin tam bu hâliyle belirli bir günde var olduğunun kanıtı (Ed25519 imzası,\nBitcoin çıpası). sigelith.org’a yalnızca sürüm listesinin özeti gider —\nne dosya adları ne de içerikleri.',
    'Kopie zapasowe folderów na dysk zewnętrzny, z historią wersji i szyfrowaniem. Wszystko dzieje się na Twoim komputerze, bez konta i bez telemetrii. Z internetem program łączy się tylko wtedy, gdy sam włączysz kopię poza domem albo znaczniki czasu Sigelith.':
        'Klasörlerinizi sürüm geçmişi ve şifrelemeyle harici bir sürücüye yedekler. Her şey bilgisayarınızda olur; hesap ve telemetri yoktur. Program internete yalnızca tesis dışı yedeği ya da Sigelith zaman damgalarını kendiniz açtığınızda bağlanır.',
    'Bez dokumentu: {count} {stamps} — plik zmienił się po stemplu albo zniknął i nie ma go w żadnej wersji tej kopii ({names}). Sam dowód jest zachowany.':
        'Belgesiz: {count} {stamps} — dosya damgalandıktan sonra değişti ya da kayboldu ve bu yedeğin hiçbir sürümünde yok ({names}). Kanıtın kendisi korunuyor.',
    'Brak pliku dowodu albo dowód jest zaszyfrowany.':
        'Kanıt dosyası yok ya da kanıt şifreli.',
    'Chroni dowody Sigelith: historię stempli i oznakowane dokumenty.':
        'Sigelith kanıtlarını korur: damga geçmişini ve damgalanan belgeleri.',
    'Chroń dowody Sigelith':
        'Sigelith kanıtlarını koru',
    'Chroń też dowody Sigelith':
        'Sigelith kanıtlarını da koru',
    'Dokument':
        'Belge',
    'Dokumenty oznakowane w Sigelith, zabezpieczone w tej kopii: sprawdzenie i odzyskanie':
        'Sigelith ile damgalanmış ve bu yedekte güvenceye alınmış belgeler: kontrol ve kurtarma',
    'Dowody Sigelith':
        'Sigelith kanıtları',
    'Dowody Sigelith: historia stempli i dokładne kopie oznakowanych dokumentów z plikami .beatproof trafią do magazynu dowodów w katalogu kopii.':
        'Sigelith kanıtları: damga geçmişi ve damgalanan belgelerin .beatproof dosyalarıyla birlikte birebir kopyaları, yedek klasöründeki kanıt deposuna kaydedilecek.',
    'Dowody Sigelith: zabezpieczone dokumenty {count} z {total}':
        'Sigelith kanıtları: güvenceye alınan belgeler {count} / {total}',
    'Dowody Sigelith…':
        'Sigelith kanıtları…',
    'Dowody z problemem: {count} — szczegóły w kolumnie „Stan”.':
        'Sorunlu kanıtlar: {count} — ayrıntılar “Durum” sütununda.',
    'Dowodów Sigelith nie udało się zabezpieczyć: {error}':
        'Sigelith kanıtları güvenceye alınamadı: {error}',
    "Droga w drzewie Merkle'a nie prowadzi do podpisanego korzenia tygodnia.":
        'Merkle ağacındaki yol, haftanın imzalı köküne ulaşmıyor.',
    'Gdzie zapisać dokumenty i dowody':
        'Belgeler ve kanıtlar nereye kaydedilsin',
    'Historia stempli Sigelith Desktop i dokładne bajty oznakowanych dokumentów, z plikami .beatproof — w osobnym magazynie, którego retencja nie sprząta.':
        'Sigelith Desktop damga geçmişi ve damgalanan belgelerin birebir baytları, .beatproof dosyalarıyla birlikte — saklama politikasının hiç temizlemediği ayrı bir depoda.',
    'Każdy stempel ma tu swój folder z dokładnie tym dokumentem, który oznakowano, i plikiem .beatproof. „Sprawdź” liczy sumę każdego dokumentu i sprawdza podpis tygodnia bez łączenia się z siecią.':
        'Burada her damganın, damgalanan belgenin birebir kendisini ve .beatproof dosyasını içeren kendi klasörü vardır. “Kontrol et”, ağa bağlanmadan her belgenin özetini hesaplar ve haftalık imzayı doğrular.',
    'Kopia obejmie folder danych Sigelith Desktop (historię stempli), a każdy oznakowany\ndokument trafi — dokładnie w tej postaci, którą oznakowano — do magazynu dowodów\nw katalogu kopii, razem z plikiem .beatproof. Starych wersji magazyn nie dotyczy:\nretencja go nie sprząta.':
        'Yedek, Sigelith Desktop veri klasörünü (damga geçmişini) kapsayacak; damgalanan her\nbelge de — damgalandığı hâliyle — .beatproof dosyasıyla birlikte yedek klasöründeki\nkanıt deposuna kaydedilecek. Depo eski sürümlerden ayrıdır:\nsaklama politikası onu hiç temizlemez.',
    'Magazyn dowodów jest pusty.':
        'Kanıt deposu boş.',
    'Na tym komputerze jest Sigelith Desktop: {count} {stamps}.':
        'Bu bilgisayarda Sigelith Desktop var: {count} {stamps}.',
    'Na tym komputerze nie ma danych Sigelith Desktop.':
        'Bu bilgisayarda Sigelith Desktop verisi yok.',
    'Otwórz folder dowodów':
        'Kanıt klasörünü aç',
    'Oznakowano':
        'Damga zamanı',
    'Pokazuje magazyn dowodów w Eksploratorze':
        'Kanıt deposunu Dosya Gezgini’nde gösterir',
    'Przywróć zaznaczone…':
        'Seçilenleri geri yükle…',
    'Sigelith Desktop: {count} {stamps} w folderze {path}.':
        'Sigelith Desktop: {path} klasöründe {count} {stamps}.',
    'Sprawdza każdy dokument i jego dowód bez łączenia z siecią':
        'Her belgeyi ve kanıtını ağa bağlanmadan kontrol eder',
    'Sprawdzam dowody…':
        'Kanıtlar kontrol ediliyor…',
    'Stan':
        'Durum',
    'Stemple w magazynie: {count}, z dokumentem: {documents}.':
        'Depodaki damgalar: {count}, belgesi olanlar: {documents}.',
    'Suma dokumentu nie zgadza się z dowodem.':
        'Belgenin özeti kanıtla eşleşmiyor.',
    'To nie jest plik dowodu Sigelith (beatproof-v1).':
        'Bu bir Sigelith kanıt dosyası (beatproof-v1) değil.',
    'Tydzień stempla jeszcze się nie zamknął — podpis dojdzie przy kolejnej kopii.':
        'Damganın haftası henüz kapanmadı — imza sonraki bir yedeklemede eklenecek.',
    'W magazynie nie ma dokumentu do tego dowodu.':
        'Depoda bu kanıta ait belge yok.',
    'Wszystkie dowody pasują do dokumentów i mają poprawny podpis.':
        'Tüm kanıtlar belgeleriyle eşleşiyor ve imzaları geçerli.',
    'Zabezpieczam dokumenty oznakowane w Sigelith…':
        'Sigelith ile damgalanmış belgeler güvenceye alınıyor…',
    'Zapisano pliki: {count} w {path}.':
        'Kaydedilen dosyalar: {count}, konum: {path}.',
    'Zapisuje dokumenty razem z plikami .beatproof we wskazanym folderze':
        'Belgeleri .beatproof dosyalarıyla birlikte seçtiğiniz klasöre kaydeder',
    'bez dokumentu — dowód zachowany':
        'belge yok — kanıt korunuyor',
    'czekają na podpis tygodnia: {count}':
        'haftalık imza bekleyenler: {count}',
    'dokument i dowód są w kopii':
        'belge ve kanıt yedekte',
    'dokument jest; dowód czeka na podpis tygodnia':
        'belge var; kanıt haftalık imzayı bekliyor',
    'dowodu nie da się odczytać':
        'kanıt okunamıyor',
    'dowody Sigelith':
        'Sigelith kanıtları',
    'dowody uzupełnione o podpis tygodnia: {count}':
        'haftalık imzası eklenen kanıtlar: {count}',
    'nowe: {count}':
        'yeni: {count}',
    'odtworzone ze starszych wersji kopii: {count}':
        'eski yedek sürümlerinden kurtarılan: {count}',
    'sprawdzony: dokument i dowód się zgadzają':
        'kontrol edildi: belge ve kanıt eşleşiyor',
    'stempel':
        'damga',
    'stemple':
        'damga',
    'stempli':
        'damga',
    'zaszyfrowany — podaj hasło, żeby sprawdzić':
        'şifreli — kontrol etmek için parolayı girin',
    'Chroń dowody Sigelith, gdy go zainstaluję':
        'Sigelith Desktop yüklendiğinde Sigelith kanıtlarını koru',
    'Dowody Sigelith: na tym komputerze nie ma jeszcze Sigelith Desktop — ochrona zacznie działać sama, gdy się pojawi.':
        'Sigelith kanıtları: bu bilgisayarda henüz Sigelith Desktop yok — yüklendiğinde koruma kendiliğinden başlayacak.',
    'Dowody Sigelith: ochrona zacznie działać sama, gdy zainstalujesz Sigelith Desktop.':
        'Sigelith kanıtları: Sigelith Desktop’u yüklediğinizde koruma kendiliğinden başlayacak.',
    'Dowody czasu dla ważnych dokumentów':
        'Önemli belgeler için zaman kanıtları',
    'Kopia zachowa każdy dokument oznakowany w Sigelith Desktop dokładnie w tej postaci, którą oznakowano, razem z dowodem — nawet gdy oryginał później się zmieni.':
        'Yedek, Sigelith Desktop ile damgalanan her belgeyi damgalandığı hâliyle, kanıtıyla birlikte saklar — orijinal daha sonra değişse bile.',
    'Ochrona zacznie działać sama, gdy na komputerze pojawi się Sigelith Desktop.':
        'Bilgisayara Sigelith Desktop yüklendiğinde koruma kendiliğinden başlayacak.',
    'Otwiera stronę programu Sigelith Desktop':
        'Sigelith Desktop sayfasını açar',
    'Poznaj Sigelith Desktop':
        'Sigelith Desktop’u tanıyın',
    'Sigelith Desktop, program tego samego wydawcy, oznakuje dokument czasem: to podpisany dowód, że plik w tej postaci istniał w danej chwili, sprawdzalny bez udziału kogokolwiek. Sigelith Backup przechowa potem każdy oznakowany dokument razem z dowodem.':
        'Aynı yayıncının programı olan Sigelith Desktop, bir belgeye zaman damgası verir: dosyanın tam bu hâliyle belirli bir anda var olduğunun, kimseye güvenmeden doğrulanabilen imzalı kanıtı. Ardından Sigelith Backup da damgalanan her belgeyi kanıtıyla birlikte saklar.',
    'Umowy, faktury, projekty — czasem trzeba wykazać, że dokument istniał danego dnia.':
        'Sözleşmeler, faturalar, projeler — bazen bir belgenin belirli bir günde var olduğunu göstermeniz gerekir.',
    'Nieznany format spisu wersji.':
        'Bilinmeyen sürüm listesi biçimi.',
    'Ta wersja nie ma pieczęci dla pojedynczych plików (kopia sprzed wersji 3.0 albo bez znaczników czasu).':
        'Bu sürümün tek tek dosyalar için mührü yok (3.0 sürümünden önce ya da zaman damgası olmadan alınmış bir yedek).',
    'Pieczęć tej wersji czeka jeszcze na podpis tygodnia Sigelith — dowód będzie gotowy po poniedziałku 00:00 UTC i kolejnej kopii.':
        'Bu sürümün mührü hâlâ Sigelith’in haftalık imzasını bekliyor — kanıt, pazartesi 00:00 UTC’den ve sonraki yedeklemeden sonra hazır olacak.',
    'Brak oświadczenia pieczęci w folderze wersji.':
        'Sürüm klasöründe mühür beyanı yok.',
    'Oświadczenie pieczęci nie zgadza się z pieczęcią wersji.':
        'Mühür beyanı, sürümün mührüyle eşleşmiyor.',
    'Drzewo plików wersji nie zgadza się z pieczęcią.':
        'Sürümün dosya ağacı mühürle eşleşmiyor.',
    'Tego pliku nie ma w spisie tej wersji.':
        'Bu dosya, bu sürümün listesinde yok.',
    'To nie jest dowód pliku z kopii Sigelith Backup ({format}).':
        'Bu bir Sigelith Backup dosya kanıtı değil ({format}).',
    'Dowód jest uszkodzony — brakuje pól albo mają zły format.':
        'Kanıt bozuk — alanlar eksik ya da biçimleri hatalı.',
    'Ten plik nie jest plikiem, którego dotyczy dowód.':
        'Bu dosya, kanıtın ait olduğu dosya değil.',
    'Ścieżka pliku w dowodzie nie zgadza się z liściem drzewa.':
        'Kanıttaki dosya yolu ağacın yaprağıyla eşleşmiyor.',
    'Droga w drzewie plików nie prowadzi do korzenia z pieczęci.':
        'Dosya ağacındaki yol mühürlü köke çıkmıyor.',
    'Oświadczenie pieczęci nie potwierdza tego drzewa plików.':
        'Mühür beyanı bu dosya ağacını doğrulamıyor.',
    'Potwierdzenie Sigelith nie dotyczy tej pieczęci.':
        'Sigelith onayı bu mühre ait değil.',
    'Dowód czasu…':
        'Zaman kanıtı…',
    'Zapisuje dowód, że ten plik był w kopii w chwili jej oznakowania — bez ujawniania innych plików':
        'Bu dosyanın, yedek mühürlendiği anda yedekte olduğunu gösteren bir kanıt kaydeder — diğer dosyaları açığa çıkarmadan',
    'Dowód czasu':
        'Zaman kanıtı',
    'Dołączyć do dowodu ścieżkę pliku w kopii („{path}”)?\n\nBez niej dowód dalej potwierdza plik i chwilę oznakowania, ale nie mówi, gdzie plik leżał.':
        'Dosyanın yedekteki yolu (“{path}”) kanıta eklensin mi?\n\nYol olmadan da kanıt dosyayı ve mühürlenme anını doğrular, ancak dosyanın nerede durduğunu söylemez.',
    'Przygotowuję dowód dla „{name}”…':
        '“{name}” için kanıt hazırlanıyor…',
    'Zapisz dowód czasu':
        'Zaman kanıtını kaydet',
    'Dowód pliku Sigelith (*{suffix})':
        'Sigelith dosya kanıtı (*{suffix})',
    'Zapisano dowód i certyfikat PDF: {path}. Sprawdzi go Sigelith Desktop albo strona sigelith.org/verify/.':
        'Kanıt ve PDF sertifikası kaydedildi: {path}. Sigelith Desktop ya da sigelith.org/verify/ sayfası bunu doğrulayabilir.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją sprawdzić.':
        'Yedek şifreli — kontrol etmek için parolayı girin.',
    'Ta wersja nie ma pieczęci — nie ma z czym porównać plików.':
        'Bu sürümün mührü yok — dosyaların karşılaştırılacağı bir şey yok.',
    'Pieczęć wersji się nie potwierdza: {problems}':
        'Sürümün mührü doğrulanamıyor: {problems}',
    'brak podpisu tygodnia':
        'haftalık imza yok',
    'Audyt przerwany.':
        'Denetim durduruldu.',
    'próbka {checked} z {listed} plików':
        '{listed} dosyadan {checked} dosyalık örnek',
    'wszystkie pliki ({count})':
        'tüm dosyalar ({count})',
    'Nietknięta: sprawdzono {scope}, wszystko zgodne z pieczęcią w publicznym dzienniku.':
        'Sağlam: {scope} kontrol edildi; her şey herkese açık günlükteki mühürle eşleşiyor.',
    'zmienione: {files}':
        'değişen: {files}',
    'brakujące: {files}':
        'eksik: {files}',
    'nieczytelne albo uszkodzone: {files}':
        'okunamayan ya da bozuk: {files}',
    'PODMIENIONA albo uszkodzona ({scope}) — {details}.':
        'KURCALANMIŞ ya da bozuk ({scope}) — {details}.',
    'Audyt treści':
        'İçerik denetimi',
    'Czyta z nośnika każdy plik tej wersji i porównuje go z sumą oznakowaną w publicznym dzienniku':
        'Bu sürümün her dosyasını sürücüden okur ve herkese açık günlükte mühürlenmiş özetle karşılaştırır',
    'Ostatnia nietknięta':
        'Son sağlam sürüm',
    'Sprawdza wersje od najnowszej i wskazuje ostatnią zgodną z pieczęcią — z niej przywracaj':
        'Sürümleri en yeniden başlayarak kontrol eder ve mührüyle eşleşen en son sürümü gösterir — geri yüklemeyi ondan yapın',
    'Ostatnia nietknięta wersja: {label} — z niej przywracaj.':
        'Son sağlam sürüm: {label} — geri yüklemeyi bundan yapın.',
    'Żadna wersja z pieczęcią nie jest nietknięta.':
        'Mühürlü sürümlerin hiçbiri sağlam değil.',
    'Czytam pliki kopii i porównuję je z pieczęcią w publicznym dzienniku…':
        'Yedek dosyaları okunuyor ve herkese açık günlükteki mühürle karşılaştırılıyor…',
    'Sprawdzam próbkę starszej wersji z pieczęcią w publicznym dzienniku…':
        'Eski bir sürümden alınan örnek, herkese açık günlükteki mühürle karşılaştırılıyor…',
    'Audyt z pieczęcią: próbka wersji {label} zgodna z publicznym dziennikiem.':
        'Mühür denetimi: {label} sürümünden alınan örnek herkese açık günlükle eşleşiyor.',
    'UWAGA — audyt z pieczęcią, wersja {label}: {details}':
        'UYARI — mühür denetimi, sürüm {label}: {details}',
    'Przekaż…':
        'Teslim et…',
    'Zapisuje tę wersję pliku i otwiera ją w Sigelith Handover — odbiorca potwierdzi odbiór własnym kluczem':
        'Dosyanın bu sürümünü kaydeder ve Sigelith Handover’da açar — alıcı teslim aldığını kendi anahtarıyla onaylar',
    'Przekazanie z dowodem doręczenia':
        'Teslim kanıtıyla teslim',
    'Przekazanie z dowodem doręczenia robi Sigelith Desktop (od wersji 3.0.1): odbiorca potwierdza odbiór własnym kluczem, a chwila doręczenia trafia do publicznego dziennika. Na tym komputerze go nie ma albo jest w starszej wersji. Otworzyć stronę programu?':
        'Teslim kanıtıyla teslimi Sigelith Desktop (3.0.1 ve üzeri sürüm) yapar: alıcı teslim aldığını kendi anahtarıyla onaylar ve teslim anı herkese açık günlüğe kaydedilir. Bu bilgisayarda Sigelith Desktop yok ya da eski bir sürümü yüklü. Programın sayfası açılsın mı?',
    'Zapisz plik do przekazania':
        'Teslim edilecek dosyayı kaydet',
    'Otwieram Sigelith Handover z plikiem „{name}” — wybierz odbiorcę.':
        'Sigelith Handover, “{name}” dosyasıyla açılıyor — alıcıyı seçin.',
    'Kapsuły czasu…':
        'Zaman kapsülleri…',
    'Pliki zapieczętowane w tej kopii do daty — klucze wydają dopiero po niej sieć drand i serwer kluczy Sigelith':
        'Bu yedekte belirli bir tarihe kadar mühürlenmiş dosyalar — anahtarlarını drand ağı ve Sigelith anahtar sunucusu ancak o tarihten sonra serbest bırakır',
    'Wskaż najpierw folder kopii — kapsuła leży w kopii.':
        'Önce yedek klasörünü seçin — kapsül yedeğin içinde durur.',
    'Kapsuły czasu':
        'Zaman kapsülleri',
    'Kapsuła pieczętuje wybrany folder do chwili, którą wskażesz. Otwierają ją dowolne dwie z trzech części: runda sieci drand z tej chwili, udział serwera kluczy Sigelith (wydawany dopiero po tej chwili — to zasada operatora, nie kryptografia) i kod odzyskiwania zapisany obok kapsuły. Kto ma tę kopię, ma więc i kod: do wcześniejszego otwarcia wystarczy mu, że operator złamie swoją zasadę. Po tej chwili otworzy ją każdy, kto ma jej pliki. Kapsuła leży w tej kopii, nie na serwerze; otwiera ją strona sigelith.org/capsule/.':
        'Kapsül, seçilen klasörü belirlediğiniz ana kadar mühürler. Kapsülü üç parçadan herhangi ikisi açar: drand ağının o ana ait turu, Sigelith anahtar sunucusunun payı (yalnızca o andan sonra serbest bırakılır — bu kriptografik bir sınır değil, operatörün kuralıdır) ve kapsülün yanına kaydedilen kurtarma kodu. Yani bu yedeğe sahip olan kişi kodu da elinde tutar: kapsülü erken açmak için operatörün kendi kuralını çiğnemesi yeterlidir. O andan sonra kapsülün dosyalarına sahip olan herkes onu açabilir. Kapsül bir sunucuda değil, bu yedekte durur; onu sigelith.org/capsule/ sayfası açar.',
    'Wybierz kapsułę z listy albo utwórz nową.':
        'Listeden bir kapsül seçin ya da yeni bir kapsül oluşturun.',
    'Nowa kapsuła…':
        'Yeni kapsül…',
    'Pieczętuje wybrany folder do daty':
        'Seçilen klasörü belirli bir tarihe kadar mühürler',
    'Pokaż w folderze':
        'Klasörde göster',
    'Otwiera folder kapsuły w Eksploratorze':
        'Kapsül klasörünü Dosya Gezgini’nde açar',
    'Otwórz na stronie':
        'Web sitesinde aç',
    'Strona sigelith.org/capsule/ otwiera kapsułę po jej dacie':
        'sigelith.org/capsule/ sayfası, kapsülü tarihi geldikten sonra açar',
    'można otworzyć':
        'açılabilir',
    'zamknięta':
        'mühürlü',
    'W tej kopii nie ma jeszcze kapsuł czasu.':
        'Bu yedekte henüz zaman kapsülü yok.',
    'Ta kapsuła da się otworzyć na stronie sigelith.org/capsule/ — wskaż jej pliki.':
        'Bu kapsül sigelith.org/capsule/ sayfasında açılabilir — orada kapsülün dosyalarını seçin.',
    'Kapsuła jest zamknięta do daty z listy. Kod odzyskiwania leży w pliku obok niej.':
        'Kapsül, listedeki tarihe kadar mühürlü. Kurtarma kodu yanındaki bir dosyada.',
    'Wybierz folder do zapieczętowania':
        'Mühürlenecek klasörü seçin',
    'Pieczętuję „{name}” — kilka sekund na krzywej eliptycznej…':
        '“{name}” mühürleniyor — eliptik eğri üzerinde birkaç saniye…',
    'kapsuła czasu':
        'zaman kapsülü',
    'Kapsuła zapieczętowana':
        'Kapsül mühürlendi',
    '„{name}” otworzy się najwcześniej {when}.\n\nKod odzyskiwania (skopiowany do schowka, zapisany też obok kapsuły):\n\n{code}\n\nZapisz go w bezpiecznym miejscu. Przed datą otwarcia sam niczego nie otwiera; po niej zastępuje jeden z kluczy, gdyby był niedostępny.':
        '“{name}” en erken şu tarihte açılır: {when}.\n\nKurtarma kodu (panoya kopyalandı, kapsülün yanına da kaydedildi):\n\n{code}\n\nKodu güvenli bir yerde saklayın. Açılış tarihinden önce tek başına hiçbir şeyi açmaz; bu tarihten sonra, anahtarlardan biri erişilemez olursa onun yerine geçer.',
    'Nie udało się zapieczętować: {error}':
        'Mühürlenemedi: {error}',
    'Nowa kapsuła czasu':
        'Yeni zaman kapsülü',
    'Otworzy się najwcześniej':
        'En erken açılış',
    'kapsuła':
        'kapsül',
    'Chwila otwarcia musi być w przyszłości.':
        'Açılış anı gelecekte olmalıdır.',
    'Na bieżąco':
        'Sürekli',
    'Zmiany w folderach źródłowych trafiają do dzisiejszej wersji kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje. Jedna wersja na dzień; ze znacznikami czasu zamyka ją pieczęć następnego dnia.':
        'Kaynak klasörlerdeki değişiklikler, kaydedildikten birkaç dakika sonra yedeğin bugünkü sürümüne eklenir; sürücü bağlandığında da yedek hemen eşitlenir. Günde bir sürüm; zaman damgaları açıksa sürüm ertesi gün bir mühürle kapatılır.',
    'Na bieżąco — po każdej zmianie i po podłączeniu dysku':
        'Sürekli — her değişiklikten sonra ve sürücü bağlandığında',
    'Dla dysku podłączonego na stałe albo często: zmiany trafiają do kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje.':
        'Her zaman ya da sık sık bağlı olan bir sürücü için: değişiklikler kaydedildikten birkaç dakika sonra yedeğe eklenir; sürücü bağlandığında da yedek hemen eşitlenir.',
    'Kopia będzie na bieżąco: zmiany trafią do dzisiejszej wersji kilka minut po zapisie, a po podłączeniu dysku kopia od razu się zsynchronizuje.':
        'Yedek sürekli güncel kalacak: değişiklikler kaydedildikten birkaç dakika sonra bugünkü sürüme eklenecek; sürücü bağlandığında da yedek hemen eşitlenecek.',
    'przywracanie':
        'geri yükleme',
}
