"""Katalog arabski: „polski tekst źródłowy” → „tekst (arabski)”.

Klucze są te same co w ``en.py`` i muszą dokładnie odpowiadać napisom w kodzie;
pilnuje tego ``tests/test_i18n.py``. Pola w nawiasach klamrowych (``{count}``)
zostają bez zmian. Formaty dat są te same co w Sigelith Desktop.
"""

from __future__ import annotations

TEXTS: dict[str, str] = {
    '\n\nLokalizacja:\n{path}':
        '\n\nالموقع:\n{path}',
    '\nDo uzupełnienia: niedokończone kopie: {count} — możesz je uzupełnić, wybierając wersję poniżej.':
        '\nنسخ احتياطية غير مكتملة بانتظار الاستكمال: {count} — يمكنك استكمالها باختيار إصدارها أدناه.',
    '\nUwaga: duży klaster ({size}): każdy mały plik zajmuje co najmniej tyle miejsca. Przy wielu małych plikach kopia zajmie wielokrotnie więcej niż dane.':
        '\nملاحظة: وحدة تخصيص كبيرة ({size}): يشغل كل ملف صغير هذه المساحة على الأقل. ومع كثرة الملفات الصغيرة ستشغل النسخة الاحتياطية أضعاف حجم البيانات.',
    '\nUwaga: niedokończone wersje (nie zawierają wszystkich plików): {names}':
        '\nملاحظة: إصدارات غير مكتملة (لا تحتوي على كل الملفات): {names}',
    '\nUwaga: {filesystem} nie obsługuje twardych dowiązań — każda wersja z datą zajmuje tyle miejsca co pełna kopia.':
        '\nملاحظة: لا يدعم {filesystem} الروابط الثابتة — فكل إصدار مؤرَّخ يشغل مساحة نسخة كاملة.',
    ' wersji':
        ' إصدارات',
    ' z szyfrowaniem AES-256-GCM…':
        ' مع تشفير AES-256-GCM…',
    ' ×':
        ' ×',
    ' — a ponieważ {filesystem} nie obsługuje twardych dowiązań, zapisze ponownie wszystkie pliki i zajmie tyle miejsca co cała kopia':
        ' — ولأن {filesystem} لا يدعم الروابط الثابتة، فسيعيد كتابة كل الملفات ويشغل مساحة النسخة الاحتياطية كاملة',
    ' • pozostało {time}':
        ' • المتبقي {time}',
    '%d.%m %H:%M':
        '\u2066%d/%m %H:%M\u2069',
    '%d.%m.%Y':
        '\u2066%d/%m/%Y\u2069',
    '%d.%m.%Y %H:%M':
        '\u2066%d/%m/%Y %H:%M\u2069',
    ', klaster {size}':
        '، وحدة التخصيص {size}',
    ', uzupełniona {when}':
        '، استُكمل في {when}',
    'Analizuje pliki i pokazuje plan. Nic nie zapisuje.':
        'يحلّل الملفات ويعرض الخطة. لا يكتب شيئًا.',
    'Anulowano przed rozpoczęciem kopii.':
        'أُلغي قبل بدء النسخ الاحتياطي.',
    'Anuluj':
        'إلغاء',
    'Argon2id (t={passes}, {memory} MiB, p={threads})':
        'Argon2id (t={passes}, {memory} MiB, p={threads})\u200e',
    'Argon2id — {passes} przebiegi, {memory} MiB, {threads} wątki':
        'Argon2id — تمريرات: {passes}، الذاكرة: {memory} MiB، خيوط المعالجة: {threads}',
    'Automatycznie (język systemu)':
        'تلقائي (لغة النظام)',
    'Bardzo dobre':
        'قوية جدًا',
    'Bardzo słabe':
        'ضعيفة جدًا',
    'Brak manifestu — skanuję katalog kopii.':
        'لا يوجد فهرس — جارٍ فحص مجلد النسخة الاحتياطية.',
    'Brakuje tagu uwierzytelniającego — plik jest obcięty.':
        'وسم المصادقة مفقود — الملف مبتور.',
    'Błąd uruchamiania':
        'خطأ في بدء التشغيل',
    'Ciemny':
        'داكن',
    'Co dokładnie zostanie zapisane przy najbliższym przebiegu.':
        'ما الذي سيُكتب بالضبط في التشغيل القادم.',
    'Co kopiujemy':
        'ما الذي سيُنسخ',
    'Co zrobić, gdy plik o tej nazwie już istnieje w katalogu docelowym.':
        'ما العمل إذا كان في مجلد الوجهة ملف بالاسم نفسه.',
    'Czas w nazwie to BeatTime — 1000 beatów na dobę, kotwica w UTC, ten sam moment na całym świecie. Data jest datą UTC, więc zgadza się z zegarem.':
        'الوقت في الاسم هو BeatTime — يُقسَم فيه اليوم إلى 1000 بيت، وهو مرتبط بـ UTC ويعني اللحظة نفسها في كل أنحاء العالم. والتاريخ تاريخ UTC، لذا يطابق الساعة.',
    'Czym jest {app}':
        'ما هو {app}',
    'Czyści tylko okno — plik dziennika pozostaje':
        'يمسح النافذة فقط — ويبقى ملف سجل الأحداث',
    'Dane aplikacji: {path}':
        'بيانات التطبيق: {path}',
    'Decyduje, czy zachowujemy historię wersji.':
        'يحدد ما إذا كان سجل الإصدارات سيُحفظ.',
    'Dobre':
        'قوية',
    'Dodaj folder':
        'إضافة مجلد',
    'Dodaj przynajmniej jeden folder źródłowy.':
        'أضف مجلدًا مصدرًا واحدًا على الأقل.',
    'Dogrywka zmian z czasu kopii:':
        'استكمال التغييرات التي حدثت أثناء النسخ:',
    'Dokąd przywracamy':
        'وجهة الاستعادة',
    'Dokładnie to, co program realnie stosuje.':
        'بالضبط ما يستخدمه البرنامج فعلًا.',
    'Domyślne wykluczenia':
        'الاستثناءات الافتراضية',
    'Domyślne wykluczenia zapisane.':
        'تم حفظ الاستثناءات الافتراضية.',
    'Domyślnie wyłączone. Przy włączonej opcji skasowanie pliku w źródle\nusuwa też jego jedyną kopię zapasową — operacja nieodwracalna.':
        'معطَّل افتراضيًا. عند تفعيل هذا الخيار يؤدي حذف ملف في المصدر\nإلى حذف نسخته الاحتياطية الوحيدة أيضًا — ولا يمكن التراجع عن ذلك.',
    'Dopisuj do nazwy katalogu datę ostatniego uzupełnienia':
        'إضافة تاريخ آخر استكمال إلى اسم المجلد',
    'Dziennik':
        'سجل الأحداث',
    'Dziennik: {path}':
        'سجل الأحداث: {path}',
    'Ekran przywracania wypełniony danymi szablonu.':
        'مُلئت شاشة الاستعادة ببيانات القالب.',
    'Folder docelowy kopii — najlepiej na innym dysku fizycznym.':
        'مجلد وجهة النسخة الاحتياطية — ويُفضَّل أن يكون على قرص فعلي آخر.',
    'Folder zawierający kopię utworzoną przez {app}.':
        'مجلد يحتوي على نسخة احتياطية أنشأها {app}.',
    'Gdy plik już istnieje:':
        'إذا كان الملف موجودًا:',
    'Gdzie zapisujemy':
        'أين ستُحفظ النسخة',
    'Gotowe do pracy.':
        'جاهز للعمل.',
    'Gotowe. Wybierz foldery do kopii.':
        'جاهز. اختر المجلدات المراد نسخها احتياطيًا.',
    'Gotowe: {count} {files}, {size}, {seconds} s.':
        'اكتمل: {count} {files}، {size}، {seconds} ث.',
    'Główny folder kopii. Zawiera spis treści (.cleanvault-manifest).':
        'المجلد الرئيسي للنسخة الاحتياطية. يحتوي على الفهرس (\u200e.cleanvault-manifest).',
    'Hasła nie da się odzyskać ani zresetować. Jeśli je zgubisz, dane z kopii zaszyfrowanej są bezpowrotnie stracone — tak działa poprawne szyfrowanie.':
        'لا يمكن استرجاع كلمة المرور ولا إعادة تعيينها. إذا فقدتها، ضاعت بيانات النسخة الاحتياطية المشفّرة إلى الأبد — هكذا يعمل التشفير السليم.',
    'Hasła w obu polach różnią się.':
        'كلمتا المرور في الحقلين غير متطابقتين.',
    'Hasło':
        'كلمة المرور',
    'Hasło do kopii':
        'كلمة مرور النسخة الاحتياطية',
    'Hasło nie jest nigdzie zapisywane w postaci jawnej.\nBez niego nie da się odzyskać danych — nie istnieje żadna furtka serwisowa.':
        'لا تُحفظ كلمة المرور في أي مكان بصورة مقروءة.\nومن دونها لا يمكن استرجاع البيانات — فلا يوجد أي باب خلفي.',
    'Hasło nie może być puste.':
        'لا يمكن أن تكون كلمة المرور فارغة.',
    'Hasło niezapisane':
        'لم تُحفظ كلمة المرور',
    'Hasło powinno mieć co najmniej 8 znaków.':
        'يجب ألا تقل كلمة المرور عن 8 أحرف.',
    'Hasło trafia do magazynu systemowego powiązanego z Twoim kontem.\nNigdy nie jest zapisywane w plikach programu.':
        'تُحفظ كلمة المرور في مخزن النظام المرتبط بحسابك.\nولا تُكتب أبدًا في ملفات البرنامج.',
    'Hasło użyte przy tworzeniu kopii':
        'كلمة المرور المستخدمة عند إنشاء النسخة الاحتياطية',
    'Ile plików kopia przetwarza jednocześnie. Przy setkach tysięcy małych plików\nczas kopii to głównie opóźnienia na każdy plik (otwarcie, skanowanie\nantywirusowe, zapis na nośnik), a nie przesył danych — praca równoległa\nskraca go kilkukrotnie.\n\n„automatycznie” dobiera liczbę do procesora (do 32). Na wolnym dysku\ntalerzowym mniejsza wartość (2–4) bywa szybsza.':
        'عدد الملفات التي يعالجها النسخ الاحتياطي في آن واحد. مع مئات الآلاف من الملفات الصغيرة\nيضيع معظم وقت النسخ في التأخير الخاص بكل ملف (الفتح، وفحص مكافح\nالفيروسات، والكتابة على وسيط التخزين)، لا في نقل البيانات — والعمل بالتوازي\nيختصره أضعافًا.\n\nالقيمة «تلقائي» تختار العدد بحسب المعالج (حتى 32). على قرص\nدوّار بطيء قد تكون القيمة الأصغر (2–4) أسرع.',
    'Informacje przydatne przy zgłaszaniu problemu.':
        'معلومات مفيدة عند الإبلاغ عن مشكلة.',
    'Jak to działa':
        'كيف يعمل',
    'Jasny':
        'فاتح',
    'Jeden folder utrzymywany w zgodzie ze źródłem. Brak historii wersji,\nza to najprostsza struktura i najmniejsze zużycie miejsca.':
        'مجلد واحد يبقى مطابقًا للمصدر. لا يوجد سجل إصدارات،\nلكنه أبسط بنية وأقل استهلاكًا للمساحة.',
    'Jeśli operacja zakończy się błędem, skopiuj stąd ostatnie wiersze — zawierają dokładną przyczynę, a nie tylko komunikat ogólny.':
        'إذا انتهت عملية بخطأ، فانسخ من هنا الأسطر الأخيرة — ففيها السبب الدقيق، لا مجرد رسالة عامة.',
    'Język interfejsu zmieniony.':
        'تم تغيير لغة الواجهة.',
    'Język zmienisz po zakończeniu bieżącej operacji.':
        'يمكنك تغيير اللغة بعد انتهاء العملية الجارية.',
    'Język:':
        'اللغة:',
    'Katalog docelowy leży wewnątrz źródła ({path}). Kopia kopiowałaby samą siebie w nieskończoność.':
        'مجلد الوجهة يقع داخل المصدر ({path}). وعندها ستنسخ النسخة الاحتياطية نفسها بلا نهاية.',
    'Katalog docelowy nie może być tym samym katalogiem co źródłowy.':
        'لا يمكن أن يكون مجلد الوجهة هو المجلد المصدر نفسه.',
    'Katalog jeszcze nie istnieje — zostanie utworzony.':
        'المجلد غير موجود بعد — سيُنشأ.',
    'Katalog kopii nie istnieje: {path}':
        'مجلد النسخة الاحتياطية غير موجود: {path}',
    'Katalog źródłowy nie istnieje: {path}':
        'المجلد المصدر غير موجود: {path}',
    'Katalog, w którym pojawią się odtworzone pliki.':
        'المجلد الذي ستظهر فيه الملفات المستعادة.',
    'Katalog, w którym powstanie kopia. Nie może leżeć wewnątrz folderu źródłowego.':
        'المجلد الذي ستُنشأ فيه النسخة الاحتياطية. لا يجوز أن يقع داخل مجلد مصدر.',
    'Katalogi objęte kopią.\nMożesz przeciągnąć foldery z Eksploratora Windows wprost na tę listę.':
        'المجلدات المشمولة بالنسخ الاحتياطي.\nيمكنك سحب المجلدات من مستكشف الملفات مباشرة إلى هذه القائمة.',
    'Każdy folder z datą jest kompletny — przywracanie nie wymaga sklejania wersji.':
        'كل مجلد مؤرَّخ مكتمل — فالاستعادة لا تتطلب تجميع الإصدارات.',
    'Każdy plik jest czytany ponownie zaraz po zapisaniu. Dane pochodzą wtedy\nzwykle z pamięci podręcznej systemu, więc niewiele mówi to o nośniku,\na wydłuża kopię nawet dwukrotnie.\n\nSkuteczniejsza jest weryfikacja odroczona: ekran „Przywracanie” →\n„Sprawdź kopię”, najlepiej po ponownym podłączeniu dysku.':
        'يُقرأ كل ملف مجددًا فور كتابته. وتأتي البيانات حينها\nعادةً من ذاكرة النظام المؤقتة، فلا يدل ذلك كثيرًا على حالة وسيط التخزين،\nبينما قد يطيل النسخ إلى الضعف.\n\nالتحقق المؤجَّل أجدى: شاشة «الاستعادة» ←\n«فحص النسخة الاحتياطية»، ويُفضَّل بعد إعادة توصيل القرص.',
    'Każdy plik trafia do kopii jako zaszyfrowany kontener .cvlt.\nKlucz powstaje z hasła przez Argon2id.':
        'يدخل كل ملف النسخة الاحتياطية كحاوية \u200e.cvlt مشفّرة.\nويُشتق المفتاح من كلمة المرور عبر Argon2id.',
    'Każdy przebieg tworzy osobny folder z datą i godziną.\nPliki niezmienione są podpinane twardym dowiązaniem, więc historia\nzajmuje tyle miejsca, ile realnie się zmieniło.':
        'كل تشغيل ينشئ مجلدًا خاصًا يحمل التاريخ والوقت.\nوتُربط الملفات غير المتغيّرة بروابط ثابتة، لذا لا يشغل السجل\nإلا مساحة ما تغيّر فعلًا.',
    'Klaster nośnika to {cluster} — pliki zajmą {actual} zamiast {logical} (narzut {overhead}).':
        'وحدة التخصيص في وسيط التخزين {cluster} — ستشغل الملفات {actual} بدلًا من {logical} (زيادة قدرها {overhead}).',
    'Kliknij szablon, aby zobaczyć jego szczegóły.':
        'انقر قالبًا لعرض تفاصيله.',
    'Kliknij „Podgląd zmian”, aby sprawdzić plan bez zapisywania czegokolwiek.':
        'انقر «معاينة التغييرات» لفحص الخطة دون كتابة أي شيء.',
    'Kolor wyróżnienia':
        'لون التمييز',
    'Kolor wyróżnienia…':
        'لون التمييز…',
    'Kopia':
        'النسخة الاحتياطية',
    'Kopia do dokończenia':
        'نسخة احتياطية بحاجة إلى إكمال',
    'Kopia jest aktualna — nie ma czego zapisywać.':
        'النسخة الاحتياطية محدَّثة — لا يوجد ما يُكتب.',
    'Kopia jest zaszyfrowana — podaj hasło użyte przy jej tworzeniu.':
        'النسخة الاحتياطية مشفّرة — أدخل كلمة المرور المستخدمة عند إنشائها.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją przywrócić.':
        'النسخة الاحتياطية مشفّرة — أدخل كلمة المرور لاستعادتها.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją zweryfikować.':
        'النسخة الاحتياطية مشفّرة — أدخل كلمة المرور للتحقق منها.',
    'Kopia jest zaszyfrowana — podaj hasło.':
        'النسخة الاحتياطية مشفّرة — أدخل كلمة المرور.',
    'Kopia lustrzana':
        'نسخة مطابقة',
    'Kopia nie została uruchomiona.':
        'لم يبدأ النسخ الاحتياطي.',
    'Kopia wykonana. Uruchom podgląd ponownie, aby sprawdzić stan.':
        'اكتمل النسخ الاحتياطي. شغّل المعاينة مجددًا لفحص الحالة.',
    'Kopia zapasowa':
        'النسخ الاحتياطي',
    'Kopia {folder}':
        'نسخة {folder} الاحتياطية',
    'Kopia {kind} • {count} {files} • {size} • ostatnia aktualizacja {when}\nŹródła: {roots}':
        'نسخة احتياطية {kind} • {count} {files} • {size} • آخر تحديث {when}\nالمصادر: {roots}',
    'Kopiowane są wyłącznie pliki nowe i zmienione od ostatniego przebiegu.':
        'لا تُنسخ إلا الملفات الجديدة والمعدّلة منذ آخر تشغيل.',
    'Kopiuje ustawienia szablonu na ekran „Kopia zapasowa”':
        'ينسخ إعدادات القالب إلى شاشة «النسخ الاحتياطي»',
    'Kopię możesz sprawdzić później: ekran „Przywracanie” → „Sprawdź kopię”. Najlepiej po ponownym podłączeniu dysku — wtedy dane są czytane z nośnika.':
        'يمكنك فحص النسخة الاحتياطية لاحقًا: شاشة «الاستعادة» ← «فحص النسخة الاحتياطية». ويُفضَّل ذلك بعد إعادة توصيل القرص — فعندها تُقرأ البيانات فعلًا من وسيط التخزين.',
    'Kryptografia':
        'التشفير',
    'Lista podpowiadana przy tworzeniu nowej kopii.':
        'القائمة المقترحة عند إعداد نسخة احتياطية جديدة.',
    'Magazyn haseł: {backend}':
        'مخزن كلمات المرور: {backend}',
    'Magazyn systemowy: {backend}':
        'مخزن النظام: {backend}',
    'Menedżer poświadczeń Windows (DPAPI, powiązany z kontem użytkownika).':
        'إدارة بيانات الاعتماد في Windows (عبر DPAPI، ومرتبطة بحساب المستخدم).',
    'Miejsce i układ odtwarzanych plików.':
        'مكان الملفات المستعادة وطريقة ترتيبها.',
    'Motyw zmieniony na {theme}.':
        'تم تغيير السمة إلى {theme}.',
    'Motyw:':
        'السمة:',
    'Możesz też przeciągnąć foldery z Eksploratora Windows wprost na listę.':
        'يمكنك أيضًا سحب المجلدات من مستكشف الملفات مباشرة إلى القائمة.',
    'Można ją dokończyć — zostaną dograne tylko brakujące i zmienione pliki.':
        'يمكن إكمالها — ولن تُضاف إلا الملفات الناقصة والمعدّلة.',
    'Na nośniku docelowym zajmie to ok. {size}.':
        'سيشغل ذلك نحو {size} على وسيط الوجهة.',
    'Nadpisywanie plików':
        'الكتابة فوق الملفات',
    'Nadpisz istniejące pliki':
        'الكتابة فوق الملفات الموجودة',
    'Nazwa szablonu':
        'اسم القالب',
    'Nazwa szablonu nie może być pusta.':
        'لا يمكن أن يكون اسم القالب فارغًا.',
    'Nazwa szablonu zapisana.':
        'تم حفظ اسم القالب.',
    'Nazwa szablonu:':
        'اسم القالب:',
    'Nie ma wersji kopii o nazwie {name} w katalogu {path}.':
        'لا يوجد إصدار نسخة احتياطية باسم {name} في المجلد {path}.',
    'Nie można odczytać informacji o dysku: {error}':
        'تعذّرت قراءة معلومات القرص: {error}',
    'Nie udało się uruchomić programu — brakuje biblioteki: {error}\nZainstaluj zależności poleceniem:  pip install -r requirements.txt':
        'تعذّر تشغيل البرنامج — مكتبة مفقودة: {error}\nثبّت التبعيات بالأمر:  pip install -r requirements.txt',
    'Nie udało się wykonać operacji':
        'تعذّر تنفيذ العملية',
    'Nie udało się zapisać hasła w magazynie systemowym.\nSzablon działa normalnie — program poprosi o hasło przy uruchomieniu.':
        'تعذّر حفظ كلمة المرور في مخزن النظام.\nيعمل القالب كالمعتاد — وسيطلب البرنامج كلمة المرور عند التشغيل.',
    'Nie udało się znaleźć wolnej nazwy dla {path}':
        'تعذّر العثور على اسم متاح لـ {path}',
    'Nie wskazano katalogu docelowego.':
        'لم يُحدَّد مجلد الوجهة.',
    'Nie wskazano żadnego katalogu źródłowego.':
        'لم يُحدَّد أي مجلد مصدر.',
    'Nie wybrano katalogu':
        'لم يتم اختيار مجلد',
    'Nie wybrano szablonu':
        'لم يتم اختيار قالب',
    'Nie znaleziono spisu treści kopii — program przeskanuje folder i rozpozna pliki po ich zawartości.':
        'لم يُعثر على فهرس النسخة الاحتياطية — سيفحص البرنامج المجلد ويتعرّف على الملفات من محتواها.',
    'Nie znam oryginalnej lokalizacji dla {key} — wybierz inny układ przywracania.':
        'الموقع الأصلي لـ {key} غير معروف — اختر ترتيبًا آخر للاستعادة.',
    'Niedostępny — backend {backend} nie gwarantuje poufności.':
        'غير متاح — الواجهة الخلفية {backend} لا تضمن السرية.',
    'Niedostępny — brak biblioteki keyring.':
        'غير متاح — مكتبة keyring غير موجودة.',
    'Nieznany algorytm wyprowadzania klucza: {name}':
        'خوارزمية اشتقاق مفتاح غير معروفة: {name}',
    'Nowa wersja z datą':
        'إصدار مؤرَّخ جديد',
    'Nowa wersja z datą to kopia od początku do osobnego folderu':
        'الإصدار المؤرَّخ الجديد يعني نسخًا من البداية إلى مجلد منفصل',
    'Nowa wersja z datą — kopia do nowego folderu.\nWybrana istniejąca wersja — dogrywa do niej tylko brakujące i zmienione\npliki, a pliki różniące się od źródła nadpisuje. Tak dokończysz przerwaną\nkopię albo uzupełnisz ją o dane, które powstały w trakcie jej wykonywania.':
        'إصدار مؤرَّخ جديد — نسخ إلى مجلد جديد.\nإصدار موجود تختاره — تُضاف إليه الملفات الناقصة والمعدّلة فقط،\nوتُكتب الملفات المختلفة عن المصدر فوق نظيراتها. هكذا تُكمل نسخًا\nمتوقفًا أو تستكمله بالبيانات التي نشأت أثناء تنفيذه.',
    'Nowy szablon':
        'قالب جديد',
    'Nośnik docelowy ({filesystem}) nie obsługuje twardych dowiązań, więc każda wersja z datą jest pełną kopią. Te {count} niezmienionych plików zostanie powielone ({size}). Rozważ układ „kopia lustrzana” albo nośnik NTFS.':
        'وسيط الوجهة ({filesystem}) لا يدعم الروابط الثابتة، لذا فكل إصدار مؤرَّخ نسخة كاملة. وسيُكرَّر عدد {count} من الملفات غير المتغيّرة ({size}). فكّر في ترتيب «نسخة مطابقة» أو في وسيط تخزين بنظام NTFS.',
    'O programie':
        'حول البرنامج',
    'Obsługiwane są wzorce w stylu Windows:\n  *.tmp          — wszystkie pliki tymczasowe\n  Thumbs.db      — konkretna nazwa\n  node_modules/* — cały folder wraz z zawartością':
        'تُدعم أنماط بأسلوب Windows:\n  *.tmp          — كل الملفات المؤقتة\n  Thumbs.db      — اسم محدد بعينه\n  node_modules/*\u200e — مجلد كامل مع محتواه',
    'Ochrona danych':
        'حماية البيانات',
    'Odczytuje wszystkie pliki kopii i weryfikuje ich poprawność.\nNic nie zapisuje na dysku.':
        'يقرأ كل ملفات النسخة الاحتياطية ويتحقق من سلامتها.\nلا يكتب أي شيء على القرص.',
    'Odpowiednik synchronizacji folderu. Wcześniejsze wersje plików nie są zachowywane.':
        'يعادل مزامنة مجلد. لا تُحفظ الإصدارات السابقة من الملفات.',
    'Odtwarza pliki z kopii — również z kopii zaszyfrowanej.':
        'يستعيد الملفات من نسخة احتياطية — حتى من نسخة مشفّرة.',
    'Odtwarza pliki zgodnie z ustawieniami powyżej':
        'يستعيد الملفات وفق الإعدادات أعلاه',
    'Odtwórz pełną strukturę folderów':
        'إعادة إنشاء بنية المجلدات كاملة',
    'Odtwórz pliki z istniejącej kopii':
        'استعِد الملفات من نسخة احتياطية موجودة',
    'Operacja nie powiodła się.':
        'فشلت العملية.',
    'Operacja przerwana przez użytkownika.':
        'أوقف المستخدم العملية.',
    'Operacja przerwana — utrwalam stan dotychczas zapisanych plików.':
        'أُوقفت العملية — جارٍ حفظ حالة الملفات المكتوبة حتى الآن.',
    'Operacja w toku':
        'عملية قيد التنفيذ',
    'Operacja zakończona błędem.':
        'انتهت العملية بخطأ.',
    'Ostatnie operacje':
        'العمليات الأخيرة',
    'Otwiera ekran przywracania z wypełnionymi ścieżkami':
        'يفتح شاشة الاستعادة مع ملء المسارات',
    'Otwiera pełny dziennik w domyślnym edytorze':
        'يفتح سجل الأحداث كاملًا في المحرر الافتراضي',
    'Otwórz katalog danych':
        'فتح مجلد البيانات',
    'Otwórz katalog dziennika':
        'فتح مجلد سجل الأحداث',
    'Otwórz okno wyboru katalogu':
        'يفتح نافذة اختيار المجلد',
    'Otwórz plik dziennika':
        'فتح ملف سجل الأحداث',
    'PBKDF2-HMAC-SHA256 ({count} iteracji)':
        'PBKDF2-HMAC-SHA256 (التكرارات: \u2066{count}\u2069)',
    'PBKDF2-HMAC-SHA256 — {count} iteracji':
        'PBKDF2-HMAC-SHA256 — التكرارات: \u2066{count}\u2069',
    'PBKDF2-HMAC-SHA256, {count} iteracji':
        'PBKDF2-HMAC-SHA256، التكرارات: \u2066{count}\u2069',
    'Pełna struktura — układ jak w źródle, wewnątrz wskazanego katalogu.\nJeden folder — wygodne, gdy szukasz kilku plików.\nPierwotne lokalizacje — zapisuje pliki tam, skąd zostały pobrane.':
        'البنية الكاملة — الترتيب نفسه كما في المصدر، داخل المجلد الذي تختاره.\nمجلد واحد — مناسب عندما تبحث عن بضعة ملفات.\nالمواقع الأصلية — تُكتب الملفات حيث كانت في الأصل.',
    'Pierwszy przebieg kopiuje wszystko i trwa najdłużej. Kolejne porównują rozmiar i datę modyfikacji, więc zwykle kończą się w kilka sekund.':
        'التشغيل الأول ينسخ كل شيء ويستغرق أطول وقت. أما التشغيلات اللاحقة فتقارن الحجم وتاريخ التعديل، لذا تنتهي عادةً في ثوانٍ.',
    'Plan gotowy: {count} {files} do zapisania.':
        'الخطة جاهزة: {count} {files} للكتابة.',
    'Plik jest za krótki, by być kontenerem tego programu.':
        'الملف أقصر من أن يكون حاوية لهذا البرنامج.',
    'Plik skończył się wcześniej, niż deklaruje nagłówek.':
        'انتهى الملف قبل الطول الذي يعلنه رأسه.',
    'Plik w formacie w wersji {found}; ta wersja programu obsługuje {supported}.':
        'صيغة الملف من الإصدار {found}؛ وهذا الإصدار من البرنامج يدعم {supported}.',
    'Plik wymaga Argon2id, a biblioteka argon2-cffi jest niedostępna.':
        'يتطلب الملف Argon2id، لكن مكتبة argon2-cffi غير متاحة.',
    'Pliki pominięte — kopia jest aktualna':
        'ملفات متخطاة — النسخة الاحتياطية محدَّثة',
    'Pliki trafią do wskazanego katalogu z zachowaniem struktury folderów.':
        'ستُوضع الملفات في المجلد الذي تختاره مع الحفاظ على بنية المجلدات.',
    'Pliki wrócą dokładnie tam, skąd pochodzą. Katalog docelowy zostanie zignorowany.':
        'ستعود الملفات إلى أماكنها الأصلية بالضبط. وسيُتجاهل مجلد الوجهة.',
    'Pliki zmienione od ostatniego przebiegu':
        'الملفات المعدّلة منذ آخر تشغيل',
    'Pliki zostaną zapisane dokładnie tam, skąd pochodzą.\n\nKonflikty nazw: {collision}.\n\nCzy kontynuować?':
        'ستُكتب الملفات في أماكنها الأصلية بالضبط.\n\nتعارض الأسماء: {collision}.\n\nهل تريد المتابعة؟',
    'Pliki, których jeszcze nie ma w kopii':
        'ملفات ليست في النسخة الاحتياطية بعد',
    'Po uzupełnieniu istniejącej wersji jej katalog nazywa się np.\n  2026-09-17_@687--2026-09-24_@921\nczyli: data utworzenia kopii i data ostatniego uzupełnienia.\n\nData utworzenia zostaje z przodu, więc katalogi nadal układają się\nchronologicznie. Widać to w Eksploratorze bez uruchamiania programu.':
        'بعد استكمال إصدار موجود يصبح اسم مجلده مثلًا:\n  \u20662026-09-17_@687--2026-09-24_@921\u2069\nأي: تاريخ إنشاء النسخة الاحتياطية وتاريخ آخر استكمال.\n\nيبقى تاريخ الإنشاء في البداية، لذا تظل المجلدات مرتبة\nزمنيًا. ويظهر ذلك في مستكشف الملفات دون تشغيل البرنامج.',
    'Po wykonaniu kopii zostanie mało wolnego miejsca ({free}).':
        'ستبقى مساحة حرة قليلة بعد النسخ الاحتياطي ({free}).',
    'Po zakończeniu kopii program ponownie skanuje źródło i dogrywa do tej samej\nwersji pliki, które w międzyczasie powstały lub się zmieniły.\nPrzydatne, gdy pracujesz na danych w trakcie wielogodzinnej kopii.\nPlik zmieniony w trakcie własnego kopiowania nigdy nie jest uznawany za zapisany.':
        'عند انتهاء النسخ يفحص البرنامج المصدر مجددًا ويضيف إلى الإصدار نفسه\nالملفات التي ظهرت أو تغيّرت في أثناء ذلك.\nمفيد عندما تواصل العمل على البيانات أثناء نسخ احتياطي يستغرق ساعات.\nالملف الذي يتغيّر أثناء نسخه لا يُعدّ مكتوبًا أبدًا.',
    'Poczekaj na zakończenie bieżącej operacji.':
        'انتظر حتى تنتهي العملية الجارية.',
    'Podaj hasło dla szablonu „{name}”:':
        'أدخل كلمة مرور القالب «{name}»:',
    'Podaj hasło — bez niego nie można zaszyfrować kopii.':
        'أدخل كلمة مرور — فمن دونها لا يمكن تشفير النسخة الاحتياطية.',
    'Podane hasło nie pasuje do plików zapisanych wcześniej w tej kopii. Wznowienie z innym hasłem zostawiłoby w jednej kopii pliki pod dwoma hasłami. Podaj hasło użyte przy poprzednim przebiegu albo utwórz kopię w nowym katalogu.':
        'كلمة المرور المُدخلة لا تطابق الملفات المكتوبة سابقًا في هذه النسخة الاحتياطية. والاستئناف بكلمة مرور أخرى سيترك في نسخة واحدة ملفات بكلمتي مرور مختلفتين. أدخل كلمة المرور المستخدمة في التشغيل السابق أو أنشئ النسخة الاحتياطية في مجلد جديد.',
    'Podgląd zmian':
        'معاينة التغييرات',
    'Pokazuje folder z plikami dziennika':
        'يعرض المجلد الذي يحوي ملفات سجل الأحداث',
    'Pokazuje folder z ustawieniami i szablonami':
        'يعرض المجلد الذي يحوي الإعدادات والقوالب',
    'Pokaż / ukryj wpisane hasło':
        'إظهار كلمة المرور المكتوبة / إخفاؤها',
    'Pomiń istniejące pliki':
        'تخطي الملفات الموجودة',
    'Potwierdź usuwanie':
        'تأكيد الحذف',
    'Powtórz hasło':
        'تأكيد كلمة المرور',
    'Program nie mógł się uruchomić:\n\n{error}\n\nSzczegóły zapisano w dzienniku aplikacji.':
        'تعذّر تشغيل البرنامج:\n\n{error}\n\nكُتبت التفاصيل في سجل أحداث التطبيق.',
    'Program nie wie, czy ta kopia została dokończona. Uzupełnienie jej dogra tylko brakujące i zmienione pliki, a tego, co już jest zapisane, nie kopiuje ponownie.':
        'لا يعرف البرنامج ما إذا كانت هذه النسخة الاحتياطية قد اكتملت. واستكمالها يضيف الملفات الناقصة والمعدّلة فقط، ولا يعيد نسخ ما كُتب من قبل.',
    'Program sam wykryje, czy kopia jest zaszyfrowana.':
        'سيكتشف البرنامج بنفسه ما إذا كانت النسخة الاحتياطية مشفّرة.',
    'Przebieg operacji i diagnostyka':
        'سير العمليات والتشخيص',
    'Przebieg operacji na żywo. Pełna historia trafia do pliku.':
        'سير العملية مباشرةً. ويُحفظ السجل الكامل في ملف.',
    'Przebieg uzupełniający: {error}':
        'جولة الاستكمال: {error}',
    'Przeciętne':
        'متوسطة',
    'Przerwano liczenie sumy kontrolnej.':
        'أُوقف حساب المجموع الاختباري.',
    'Przerwano skanowanie.':
        'أُوقف الفحص.',
    'Przerwano. Zapisano {count} {files} ({size}).':
        'أُوقفت العملية. تمت كتابة {count} {files} ({size}).',
    'Przerwij':
        'إيقاف',
    'Przerywanie operacji…':
        'جارٍ إيقاف العملية…',
    'Przerywanie — zapisuję spis treści kopii, nie wyłączaj komputera…':
        'جارٍ الإيقاف — يُكتب فهرس النسخة الاحتياطية، فلا تُطفئ الحاسوب…',
    'Przeskanowano {count} {files}.':
        'تم فحص {count} {files}.',
    'Przygotowanie…':
        'جارٍ التحضير…',
    'Przywracanie':
        'الاستعادة',
    'Przywracanie do pierwotnych lokalizacji':
        'الاستعادة إلى المواقع الأصلية',
    'Przywracanie przerwane.':
        'أُوقفت الاستعادة.',
    'Przywracanie {count} {files} ({size})…':
        'جارٍ استعادة {count} {files} ({size})…',
    'Przywróć do pierwotnych lokalizacji':
        'الاستعادة إلى المواقع الأصلية',
    'Przywróć domyślne':
        'استعادة الافتراضيات',
    'Przywróć fabryczne':
        'استعادة القائمة المدمجة',
    'Przywróć pliki':
        'استعادة الملفات',
    'Przywróć z tej kopii':
        'الاستعادة من هذه النسخة الاحتياطية',
    'Pusta nazwa':
        'اسم فارغ',
    'Równoległe operacje:':
        'العمليات المتوازية:',
    'Skanowanie plików źródłowych…':
        'جارٍ فحص الملفات المصدر…',
    'Skrót z dziennika — pełny zapis znajdziesz w zakładce „Dziennik”.':
        'موجز من سجل الأحداث — والسجل الكامل في تبويب «سجل الأحداث».',
    'Skąd przywracamy':
        'مصدر الاستعادة',
    'Sprawdzam, co zmieniło się w źródle w trakcie kopii (przebieg uzupełniający {attempt} z {passes})…':
        'جارٍ فحص ما تغيّر في المصدر أثناء النسخ (جولة الاستكمال {attempt} من {passes})…',
    'Sprawdzam, czy hasło zgadza się z hasłem wcześniej zapisanych plików…':
        'جارٍ التحقق من تطابق كلمة المرور مع الملفات المكتوبة سابقًا…',
    'Sprawdzam, czy w katalogu docelowym jest kopia do dokończenia…':
        'جارٍ التحقق مما إذا كان في مجلد الوجهة نسخة احتياطية بحاجة إلى إكمال…',
    'Sprawdź hasło':
        'تحقق من كلمة المرور',
    'Sprawdź kopię':
        'فحص النسخة الاحتياطية',
    'Szablon przechowuje foldery, opcje i wykluczenia. Hasło nigdy nie trafia do szablonu — jest przechowywane w Menedżerze poświadczeń Windows albo wpisywane przy każdym uruchomieniu.':
        'يحفظ القالب المجلدات والخيارات والاستثناءات. ولا تدخل كلمة المرور القالب أبدًا — فهي تُحفظ في إدارة بيانات الاعتماد في Windows أو تُكتب عند كل تشغيل.',
    'Szablon usunięty.':
        'تم حذف القالب.',
    'Szablon „{name}”':
        'القالب «{name}»',
    'Szablon „{name}” już istnieje.\n\nZastąpić go bieżącymi ustawieniami z formularza?':
        'القالب «{name}» موجود بالفعل.\n\nهل تريد استبداله بالإعدادات الحالية من النموذج؟',
    'Szablon „{name}” zostanie usunięty.\n\nPliki kopii zapasowej pozostaną nienaruszone.':
        'سيُحذف القالب «{name}».\n\nوستبقى ملفات النسخة الاحتياطية دون مساس.',
    'Szablony':
        'القوالب',
    'Szablony: {count}\nSzyfrowanie: AES-256-GCM\nKlucz: {kdf}':
        'القوالب: {count}\nالتشفير: AES-256-GCM\nالمفتاح: {kdf}',
    'Szyfrowanie i kontrola poprawności zapisu.':
        'التشفير والتحقق من سلامة الكتابة.',
    'Szyfrowanie: AES-256-GCM (uwierzytelnione)\nWyprowadzanie klucza: {kdf}':
        'التشفير: AES-256-GCM (مع المصادقة)\nاشتقاق المفتاح: {kdf}',
    'Szyfruj kopię (AES-256-GCM)':
        'تشفير النسخة الاحتياطية (AES-256-GCM)',
    'Słabe':
        'ضعيفة',
    'Ta kopia nie jest zaszyfrowana — hasło nie jest potrzebne.':
        'هذه النسخة الاحتياطية غير مشفّرة — لا حاجة إلى كلمة مرور.',
    'Ten folder jest już na liście.':
        'هذا المجلد موجود في القائمة بالفعل.',
    'To nie jest plik zaszyfrowany przez ten program.':
        'هذا الملف لم يُشفَّر بهذا البرنامج.',
    'Trwa inna operacja — poczekaj na jej zakończenie.':
        'هناك عملية أخرى قيد التنفيذ — انتظر حتى تنتهي.',
    'Trwa operacja':
        'عملية قيد التنفيذ',
    'Trwa operacja na plikach. Zamknięcie programu ją przerwie.\n\nPliki zapisane do tej chwili zostaną zachowane, a kopię będzie można później dokończyć.\n\nZamknąć mimo to?':
        'تجري عملية على الملفات. وإغلاق البرنامج سيوقفها.\n\nستُحفظ الملفات المكتوبة حتى الآن، ويمكن إكمال النسخة الاحتياطية لاحقًا.\n\nهل تريد الإغلاق رغم ذلك؟',
    'Trwa: {description}…':
        'قيد التنفيذ: {description}…',
    'Tryb dokładny — licz sumę kontrolną każdego pliku':
        'الوضع الدقيق — حساب المجموع الاختباري لكل ملف',
    'Układ kopii':
        'ترتيب النسخة الاحتياطية',
    'Układ plików:':
        'ترتيب الملفات:',
    'Uruchom kopię':
        'بدء النسخ الاحتياطي',
    'Ustawienia':
        'الإعدادات',
    'Usunąć szablon?':
        'هل تريد حذف القالب؟',
    'Usuwa pozycję z listy. Nie kasuje żadnych plików.':
        'يزيل العنصر من القائمة. لا يحذف أي ملفات.',
    'Usuwa szablon. Nie kasuje żadnych plików kopii.':
        'يحذف القالب. لا يحذف أي ملفات من النسخة الاحتياطية.',
    'Usuwaj z kopii pliki skasowane w źródle':
        'إزالة الملفات المحذوفة في المصدر من النسخة الاحتياطية',
    'Usuń':
        'حذف',
    'Usuń zaznaczone':
        'إزالة المحدد',
    'Uszkodzony nagłówek pliku.':
        'رأس الملف تالف.',
    'Utwórz lub zaktualizuj kopię wybranych folderów':
        'أنشئ نسخة احتياطية من المجلدات المختارة أو حدّثها',
    'Utwórz nową wersję':
        'إنشاء إصدار جديد',
    'Uzupełnienie istniejącej wersji nie kopiuje ponownie tego, co już w niej jest — dokończysz przerwaną kopię bez tworzenia kolejnej pełnej wersji.':
        'استكمال إصدار موجود لا يعيد نسخ ما فيه بالفعل — فتُكمل نسخًا متوقفًا دون إنشاء إصدار كامل آخر.',
    'Uzupełnij tę wersję':
        'استكمال هذا الإصدار',
    'Uzupełnij: {version} • {labels}':
        'استكمال: {version} • {labels}',
    'W katalogu docelowym jest kopia tych samych folderów zapisana starszą wersją programu:':
        'في مجلد الوجهة نسخة احتياطية للمجلدات نفسها كتبها إصدار أقدم من البرنامج:',
    'W katalogu docelowym jest niedokończona kopia tych samych folderów:':
        'في مجلد الوجهة نسخة احتياطية غير مكتملة للمجلدات نفسها:',
    'W tym katalogu nie ma spisu treści kopii — nie ma z czym porównać plików.':
        'لا يوجد فهرس للنسخة الاحتياطية في هذا المجلد — فلا يوجد ما تُقارن به الملفات.',
    'Wczytaj do formularza':
        'تحميل في النموذج',
    'Wczytano manifest kopii: {count} {files}.':
        'تم تحميل فهرس النسخة الاحتياطية: {count} {files}.',
    'Wczytano szablon „{name}” do formularza.':
        'تم تحميل القالب «{name}» في النموذج.',
    'Wersja kopii nosi teraz nazwę {name}.':
        'أصبح اسم إصدار النسخة الاحتياطية الآن {name}.',
    'Wersja, licencja i użyta kryptografia':
        'الإصدار والترخيص والتشفير المستخدم',
    'Wersje z datą (zalecane)':
        'إصدارات مؤرَّخة (موصى بها)',
    'Weryfikacja kopii':
        'التحقق من النسخة الاحتياطية',
    'Weryfikacja nie powiodła się: nieprawidłowe hasło lub uszkodzony plik.':
        'فشل التحقق: كلمة مرور غير صحيحة أو ملف تالف.',
    'Weryfikacja po zapisie nie powiodła się — zapisane dane różnią się od źródła.':
        'فشل التحقق بعد الكتابة — البيانات المكتوبة تختلف عن المصدر.',
    'Weryfikacja {count} {files} ({size}), {threads} równolegle…':
        'جارٍ التحقق من {count} {files} ({size})، {threads} بالتوازي…',
    'Weryfikuj natychmiast po zapisie (spowalnia kopię)':
        'التحقق فور الكتابة (يبطئ النسخ الاحتياطي)',
    'Wolne miejsce: {free} z {total}':
        'المساحة الحرة: {free} من {total}',
    'Wolniejszy, ale wykrywa zmiany, które nie zmieniły rozmiaru ani daty\n(np. po przywróceniu pliku z innego nośnika).':
        'أبطأ، لكنه يكتشف التغييرات التي لم تغيّر الحجم ولا التاريخ\n(مثلًا بعد استعادة ملف من وسيط تخزين آخر).',
    'Wpis {key} w spisie treści kopii wskazuje poza katalog docelowy — pomijam go.':
        'القيد {key} في فهرس النسخة الاحتياطية يشير إلى خارج مجلد الوجهة — سيُتخطّى.',
    'Wraca do listy wbudowanej w program':
        'يعود إلى القائمة المدمجة في البرنامج',
    'Wskaż folder kopii, aby zobaczyć jej zawartość.':
        'حدد مجلد النسخة الاحتياطية لعرض محتواها.',
    'Wskaż folder kopii.':
        'حدد مجلد النسخة الاحتياطية.',
    'Wskaż foldery objęte kopią. Podfoldery są uwzględniane automatycznie.':
        'حدد المجلدات المشمولة بالنسخ الاحتياطي. تُضمَّن المجلدات الفرعية تلقائيًا.',
    'Wskaż główny folder kopii (ten, który wybrałeś jako cel), a nie pojedynczy folder z datą. Program sam odczyta spis treści kopii.':
        'حدد المجلد الرئيسي للنسخة الاحتياطية (الذي اخترته وجهةً)، لا مجلدًا مؤرَّخًا منفردًا. وسيقرأ البرنامج الفهرس بنفسه.',
    'Wskaż katalog docelowy kopii.':
        'حدد مجلد وجهة النسخة الاحتياطية.',
    'Wskaż katalog docelowy.':
        'حدد مجلد الوجهة.',
    'Wstawia zalecaną listę wykluczeń':
        'يُدرج قائمة الاستثناءات الموصى بها',
    'Wszystkie pliki wylądują bezpośrednio w katalogu docelowym, bez podfolderów.':
        'ستوضع كل الملفات مباشرة في مجلد الوجهة، دون مجلدات فرعية.',
    'Wszystko do jednego folderu':
        'كل شيء في مجلد واحد',
    'Wybierz folder do kopii':
        'اختر مجلدًا لنسخه احتياطيًا',
    'Wybierz folder kopii':
        'اختر مجلد النسخة الاحتياطية',
    'Wybierz katalog':
        'اختر مجلدًا',
    'Wybierz katalog docelowy':
        'اختر مجلد الوجهة',
    'Wybierz katalog docelowy kopii':
        'اختر مجلد وجهة النسخة الاحتياطية',
    'Wybierz katalog, aby zobaczyć dostępne miejsce.':
        'اختر مجلدًا لعرض المساحة المتاحة.',
    'Wybierz kolejny folder do kopii':
        'اختر مجلدًا آخر لنسخه احتياطيًا',
    'Wybierz szablon z listy.':
        'اختر قالبًا من القائمة.',
    'Wybierz…':
        'اختر…',
    'Wybrano nadpisywanie istniejących plików. Ich obecna zawartość zostanie bezpowrotnie zastąpiona.\n\nCzy kontynuować?':
        'اخترت الكتابة فوق الملفات الموجودة. وسيُستبدل محتواها الحالي إلى الأبد.\n\nهل تريد المتابعة؟',
    'Wyczyść widok':
        'مسح العرض',
    'Wygląd':
        'المظهر',
    'Wygląd, wykluczenia domyślne i informacje o środowisku.':
        'المظهر والاستثناءات الافتراضية ومعلومات البيئة.',
    'Wygląd, wykluczenia i magazyn haseł':
        'المظهر والاستثناءات ومخزن كلمات المرور',
    'Wykluczenia':
        'الاستثناءات',
    'Wykonuje kopię według tego szablonu':
        'ينفّذ النسخ الاحتياطي وفق هذا القالب',
    'Wykonuje kopię zgodnie z powyższymi ustawieniami':
        'ينفّذ النسخ الاحتياطي وفق الإعدادات أعلاه',
    'Wymagane wyłącznie dla kopii zaszyfrowanych.':
        'مطلوبة للنسخ الاحتياطية المشفّرة فقط.',
    'Wzorce plików i folderów pomijanych w kopii — po jednym w wierszu.':
        'أنماط الملفات والمجلدات المستثناة من النسخ الاحتياطي — نمط واحد في كل سطر.',
    'Włączono szyfrowanie, ale nie podano hasła.':
        'التشفير مفعَّل، لكن لم تُدخل كلمة مرور.',
    'Włączono usuwanie z kopii plików skasowanych w źródle.\n\nPliki usunięte w źródle stracą swoją jedyną kopię zapasową. Czy na pewno kontynuować?':
        'خيار حذف الملفات المحذوفة في المصدر من النسخة الاحتياطية مفعَّل.\n\nستفقد الملفات المحذوفة في المصدر نسختها الاحتياطية الوحيدة. هل أنت متأكد من المتابعة؟',
    'Za mało miejsca w katalogu docelowym. Potrzeba ok. {needed}, dostępne {free}.':
        'لا توجد مساحة كافية في مجلد الوجهة. المطلوب نحو {needed}، والمتاح {free}.',
    'Zabezpieczenie przed literówką — hasła nie da się odzyskać.':
        'حماية من الخطأ المطبعي — فلا يمكن استرجاع كلمة المرور.',
    'Zachowaj oba — dopisz numer do nazwy':
        'الاحتفاظ بالاثنين — إضافة رقم إلى الاسم',
    'Zakończono z błędami ({errors}). Zapisano {count} {files}.':
        'انتهت العملية بأخطاء ({errors}). تمت كتابة {count} {files}.',
    'Zakończono.':
        'انتهت العملية.',
    'Zapamiętaj hasło w Menedżerze poświadczeń Windows':
        'حفظ كلمة المرور في إدارة بيانات الاعتماد في Windows',
    'Zapamiętuje te ustawienia do ponownego użycia':
        'يحفظ هذه الإعدادات لإعادة استخدامها',
    'Zapis bieżącej sesji':
        'سجل الجلسة الحالية',
    'Zapisane konfiguracje do ponownego użycia':
        'إعدادات محفوظة لإعادة الاستخدام',
    'Zapisane konfiguracje — uruchamiasz je jednym kliknięciem.':
        'إعدادات محفوظة — تشغّلها بنقرة واحدة.',
    'Zapisane szablony':
        'القوالب المحفوظة',
    'Zapisano szablon „{name}”.':
        'تم حفظ القالب «{name}».',
    'Zapisuje listę jako domyślną':
        'يحفظ القائمة بوصفها الافتراضية',
    'Zapisuje nową nazwę szablonu':
        'يحفظ الاسم الجديد للقالب',
    'Zapisywanie {count} {files} ({size}), {workers} równolegle':
        'جارٍ كتابة {count} {files} ({size})، {workers} بالتوازي',
    'Zapisz':
        'حفظ',
    'Zapisz do:':
        'الكتابة إلى:',
    'Zapisz jako szablon':
        'حفظ كقالب',
    'Zapisz nazwę':
        'حفظ الاسم',
    'Zapisz szablon':
        'حفظ القالب',
    'Zastąpić szablon?':
        'هل تريد استبدال القالب؟',
    'Zatrzymuje operację. Pliki już zapisane pozostają nienaruszone.':
        'يوقف العملية. وتبقى الملفات المكتوبة بالفعل دون مساس.',
    'Zaznacz szablon na liście.':
        'حدد قالبًا في القائمة.',
    'Zmiana języka przebudowuje okno; wypełnione ścieżki zostają.':
        'تغيير اللغة يعيد بناء النافذة؛ وتبقى المسارات التي أدخلتها.',
    'Zmiana motywu działa natychmiast.':
        'يسري تغيير السمة فورًا.',
    'Zmienia kolor przycisków i zaznaczeń':
        'يغيّر لون الأزرار والتحديد',
    'Zmień nazwę, aby łatwiej rozpoznawać szablon.':
        'غيّر الاسم ليسهل التعرف على القالب.',
    'Znaleziono {count} {files}. Porównuję z poprzednią kopią…':
        'عُثر على {count} {files}. جارٍ المقارنة بالنسخة الاحتياطية السابقة…',
    'automatycznie':
        'تلقائي',
    'bez zmian':
        'دون تغيير',
    'brak (biblioteka keyring niezainstalowana)':
        'لا يوجد (مكتبة keyring غير مثبتة)',
    'brak danych':
        'لا بيانات',
    'brak pliku w kopii':
        'الملف غير موجود في النسخة الاحتياطية',
    'do zapisania':
        'للكتابة',
    'istniejąca kopia: {count} {files}, ostatnio {when}':
        'نسخة احتياطية موجودة: {count} {files}، آخر مرة {when}',
    'jeszcze nie uruchamiany':
        'لم يُشغَّل بعد',
    'kompletna':
        'مكتمل',
    'kopia lustrzana':
        'نسخة مطابقة',
    'kopia zapasowa':
        'النسخ الاحتياطي',
    'nie':
        'لا',
    'niedokończona':
        'غير مكتمل',
    'niedokończona — brakuje ok. {count} {files} ({size})':
        'غير مكتمل — ينقص نحو {count} {files} ({size})',
    'niezaszyfrowana':
        'غير مشفّرة',
    'nieznany format manifestu':
        'صيغة فهرس غير معروفة',
    'nowych plików':
        'ملفات جديدة',
    'np. C:\\Odzyskane':
        'مثلًا C:\\Recovered',
    'np. E:\\Kopie zapasowe':
        'مثلًا E:\\Backups',
    'plik':
        'ملف',
    'plik stanu jest za krótki':
        'ملف الحالة أقصر من اللازم',
    'plik stanu w wersji {found}, obsługiwana: {supported}':
        'ملف الحالة من الإصدار {found}، والمدعوم: {supported}',
    'pliki':
        'ملفات',
    'plików':
        'ملفات',
    'podgląd kopii':
        'معاينة النسخ الاحتياطي',
    'pozostaną w kopii':
        'ستبقى في النسخة الاحتياطية',
    'rozmiar w kopii {actual} B zamiast {expected} B':
        'الحجم في النسخة الاحتياطية {actual} بايت بدلًا من {expected} بايت',
    'sprawdzanie kopii':
        'فحص النسخة الاحتياطية',
    'stan nieznany (zapisana starszą wersją programu)':
        'الحالة غير معروفة (كتبه إصدار أقدم من البرنامج)',
    'suma kontrolna manifestu się nie zgadza':
        'المجموع الاختباري للفهرس غير مطابق',
    'suma kontrolna się nie zgadza — plik uszkodzony':
        'المجموع الاختباري غير مطابق — الملف تالف',
    'szablon {name}':
        'القالب {name}',
    'tak':
        'نعم',
    'ten system plików':
        'نظام الملفات هذا',
    'wersja {version}':
        'الإصدار {version}',
    'wersje z datą':
        'إصدارات مؤرَّخة',
    'weryfikacja':
        'التحقق',
    'wyłączona':
        'معطَّل',
    'zaszyfrowana (AES-256-GCM)':
        'مشفّرة (AES-256-GCM)\u200f',
    'zawartość różni się od pliku źródłowego':
        'المحتوى يختلف عن الملف المصدر',
    'zawartość różni się od sumy kontrolnej zapisanej podczas kopii':
        'المحتوى يختلف عن المجموع الاختباري المسجَّل أثناء النسخ',
    'zmienionych':
        'معدّلة',
    'zostaną usunięte z kopii':
        'ستُحذف من النسخة الاحتياطية',
    '{done} z {total} • {speed}/s{eta}':
        '{done} من {total} • {speed}/ث{eta}',
    '{done} • {speed}/s':
        '{done} • {speed}/ث',
    '{hours} h {minutes} min':
        '{hours} س {minutes} د',
    '{label}: {count} {files}':
        '{label}: {count} {files}',
    '{message}\n\nSzczegóły techniczne znajdziesz w zakładce „Dziennik”.':
        '{message}\n\nتجد التفاصيل التقنية في تبويب «سجل الأحداث».',
    '{minutes} min {seconds} s':
        '{minutes} د {seconds} ث',
    '{name}: nie można odczytać ({error})':
        '{name}: تتعذّر القراءة ({error})',
    '{seconds} s':
        '{seconds} ث',
    '{summary}\n\nProblemy:\n{problems}\n\nPełna lista znajduje się w zakładce „Dziennik”.':
        '{summary}\n\nالمشكلات:\n{problems}\n\nالقائمة الكاملة في تبويب «سجل الأحداث».',
    '{summary}{notes}\n\nPliki zapisane przed przerwaniem są kompletne i zostały odnotowane w spisie treści kopii.\n\nAby dokończyć kopię, uruchom ją ponownie — program zaproponuje uzupełnienie tej wersji zamiast tworzenia nowej.':
        '{summary}{notes}\n\nالملفات المكتوبة قبل الإيقاف مكتملة وقد سُجّلت في فهرس النسخة الاحتياطية.\n\nلإكمال النسخ الاحتياطي، شغّله مجددًا — وسيقترح البرنامج استكمال هذا الإصدار بدلًا من إنشاء إصدار جديد.',
    '{title} — gotowe':
        '{title} — اكتملت العملية',
    '{title} — przerwano':
        '{title} — أُوقفت العملية',
    '{title} — zakończono z błędami':
        '{title} — انتهت العملية بأخطاء',
    '{when}  •  {action}  •  {count} {files}':
        '{when}  •  {action}  •  {count} {files}',
    'Łączny rozmiar danych do przesłania':
        'الحجم الإجمالي للبيانات المراد نقلها',
    'Środowisko':
        'البيئة',
    'Źródła: {sources}\nCel: {destination}\nUkład: {structure} • Szyfrowanie: {encrypt} • Weryfikacja: {verify} • Dogrywka: {catchup} • Równolegle: {workers} • Data uzupełnienia w nazwie: {stamp}\nUtworzony: {created} • Ostatni przebieg: {last}':
        'المصادر: {sources}\nالوجهة: {destination}\nالترتيب: {structure} • التشفير: {encrypt} • التحقق: {verify} • الاستكمال: {catchup} • العمليات المتوازية: {workers} • تاريخ الاستكمال في الاسم: {stamp}\nأُنشئ في: {created} • آخر تشغيل: {last}',
    'Źródło nie zmieniło się w trakcie kopii — nie ma czego uzupełniać.':
        'لم يتغيّر المصدر أثناء النسخ — لا يوجد ما يُستكمل.',
    '—':
        '—',
    '• Kopia przyrostowa — zapisywane są wyłącznie pliki nowe i zmienione.\n  Porównanie opiera się na spisie treści kopii, rozmiarze i dacie modyfikacji;\n  przy różnicy liczona jest suma kontrolna SHA-256.\n\n• Wersje z datą — każdy przebieg tworzy kompletny folder z datą, a pliki\n  niezmienione są podpinane twardym dowiązaniem, więc nie zajmują miejsca dwa razy.\n\n• Weryfikacja po zapisie — zapisany plik jest odczytywany z powrotem\n  i porównywany ze źródłem.\n\n• Odporność na przerwania — pliki powstają pod nazwą tymczasową i są\n  podmieniane dopiero po pełnym zapisie.':
        '• النسخ التزايدي — لا تُكتب إلا الملفات الجديدة والمعدّلة.\n  تعتمد المقارنة على فهرس النسخة الاحتياطية والحجم وتاريخ التعديل؛\n  وعند وجود اختلاف يُحسب المجموع الاختباري SHA-256.\n\n• الإصدارات المؤرَّخة — كل تشغيل ينشئ مجلدًا مؤرَّخًا مكتملًا، وتُربط الملفات\n  غير المتغيّرة بروابط ثابتة، فلا تشغل المساحة مرتين.\n\n• التحقق بعد الكتابة — يُقرأ الملف المكتوب مجددًا\n  ويُقارن بالمصدر.\n\n• مقاومة الانقطاع — تُنشأ الملفات باسم مؤقت ولا تحل\n  محل الأصل إلا بعد اكتمال كتابتها.',
    '• Szyfr: AES-256 w trybie GCM (szyfrowanie z uwierzytelnieniem).\n• Wyprowadzanie klucza z hasła: {kdf}.\n• Nagłówek każdego pliku jest uwierzytelniony jako AAD — podmiana parametrów\n  unieważnia tag.\n• Każdy plik dostaje losowy, niepowtarzalny nonce.\n• Odszyfrowany plik powstaje dopiero po pomyślnej weryfikacji tagu.\n• Hasła nie są zapisywane w plikach programu. Opcjonalnie trafiają do\n  Menedżera poświadczeń Windows.':
        '• خوارزمية التشفير: AES-256 في وضع GCM (تشفير مع المصادقة).\n• اشتقاق المفتاح من كلمة المرور: {kdf}.\n• رأس كل ملف مُصادَق عليه بوصفه AAD — وتغيير المعاملات\n  يُبطل الوسم.\n• يحصل كل ملف على nonce عشوائي فريد.\n• لا يُنشأ الملف المفكوك تشفيره إلا بعد التحقق من الوسم بنجاح.\n• لا تُحفظ كلمات المرور في ملفات البرنامج. ويمكن اختياريًا حفظها في\n  إدارة بيانات الاعتماد في Windows.',
    'Bez hasła nie da się odczytać ani jednego pliku z kopii.':
        'من دون كلمة المرور لا يمكن قراءة أي ملف من النسخة الاحتياطية.',
    'Co chcesz chronić?':
        'ما الذي تريد حمايته؟',
    'Co chcesz teraz zrobić?':
        'ماذا تريد أن تفعل الآن؟',
    'Czyta kopię z nośnika i porównuje ją z zapisanymi sumami kontrolnymi.':
        'يقرأ النسخة الاحتياطية من وسيط التخزين ويقارنها بالمجاميع الاختبارية المسجَّلة.',
    'Dalej':
        'التالي',
    'Dokumenty i zdjęcia':
        'المستندات والصور',
    'Ekran powitalny wrócisz w ustawieniach, gdy zmienisz zdanie.':
        'يمكنك إعادة شاشة الترحيب من الإعدادات إذا غيّرت رأيك.',
    'Ekran z pytaniem, co chcesz teraz zrobić: kopia, przywracanie, sprawdzenie.':
        'شاشة تسألك عما تريد فعله الآن: نسخ احتياطي أو استعادة أو فحص.',
    'Foldery objęte kopią':
        'المجلدات المشمولة بالنسخ الاحتياطي',
    'Foldery z pracą. Kreator pominie katalogi, które odtwarza się jednym poleceniem (node_modules, venv, build).':
        'مجلدات عملك. سيتخطى المعالج المجلدات التي يمكن إعادة إنشائها بأمر واحد (node_modules, venv, build).',
    'Gdzie zapisać kopię?':
        'أين تريد حفظ النسخة الاحتياطية؟',
    'Historia i szyfrowanie':
        'سجل التغييرات والتشفير',
    'Historia zmian (zalecane)':
        'سجل التغييرات (موصى به)',
    'Jak bardzo chcesz się zabezpieczyć?':
        'ما مستوى الحماية الذي تريده؟',
    'Jak wyżej, a dodatkowo każdy plik trafia do kopii zaszyfrowany (AES-256-GCM). Potrzebne przy kopii wożonej poza dom.':
        'كما في الخيار السابق، ويُشفَّر أيضًا كل ملف في النسخة الاحتياطية (AES-256-GCM). ضروري لنسخة احتياطية تُحمل خارج المنزل.',
    'Jedna aktualna kopia':
        'نسخة واحدة محدَّثة',
    'Język, motyw, domyślne wykluczenia i informacje o środowisku.':
        'اللغة والسمة والاستثناءات الافتراضية ومعلومات البيئة.',
    'Katalog docelowy leży wewnątrz źródła — wybierz inny.':
        'مجلد الوجهة يقع داخل المصدر — اختر مجلدًا آخر.',
    'Każdy przebieg tworzy folder z datą. Pliki niezmienione są podpinane dowiązaniem, więc historia kosztuje tyle, ile realnie się zmieniło.':
        'كل تشغيل ينشئ مجلدًا مؤرَّخًا. وتُربط الملفات غير المتغيّرة برابط، لذا لا يكلّف السجل إلا مساحة ما تغيّر فعلًا.',
    'Każdy przebieg utworzy folder z datą. Pierwszy zajmie tyle, ile dane; kolejne — tyle, ile realnie się zmieniło.':
        'سينشئ كل تشغيل مجلدًا مؤرَّخًا. يشغل الأول مساحة البيانات نفسها، وكل تشغيل لاحق مساحة ما تغيّر فعلًا فقط.',
    'Kopia powstanie w: {path}':
        'ستُنشأ النسخة الاحتياطية في: {path}',
    'Kopia trafi do: {path}':
        'ستُحفظ النسخة الاحتياطية في: {path}',
    'Kopia: {what}':
        'نسخة احتياطية: {what}',
    'Krok {number} z {total}':
        'الخطوة {number} من {total}',
    'Najlepiej na innym dysku fizycznym niż ten, który chronisz — kopia obok oryginału ginie razem z nim.':
        'يُفضَّل أن تكون على قرص فعلي غير الذي تحميه — فالنسخة الموجودة بجانب الأصل تضيع معه.',
    'Najszybsza i najmniejsza. Kopia odpowiada temu, co masz teraz — bez historii wcześniejszych wersji.':
        'الأسرع والأصغر. تطابق النسخة الاحتياطية ما لديك الآن — دون سجل للإصدارات السابقة.',
    'Nie było jeszcze żadnej kopii. Zacznij od „Zrób kopię”.':
        'لم تُنشأ أي نسخة احتياطية بعد. ابدأ بـ «إنشاء نسخة احتياطية».',
    'Nie lista ustawień, tylko ich skutki.':
        'لا قائمة إعدادات، بل ما ستفعله.',
    'Nie pokazuj tego ekranu przy starcie':
        'عدم إظهار هذه الشاشة عند بدء التشغيل',
    'Nośnik docelowy':
        'وسيط الوجهة',
    'Odtwarza pliki z kopii — całość albo wybrany folder.':
        'يستعيد الملفات من النسخة الاحتياطية — كلها أو مجلدًا تختاره.',
    'Odśwież listę':
        'تحديث القائمة',
    'Ostatnia kopia: {when} • {count} {files}.':
        'آخر نسخة احتياطية: {when} • {count} {files}.',
    'Pierwszy przebieg jest najdłuższy — kolejne porównują rozmiar i datę modyfikacji, więc zwykle trwają sekundy.':
        'التشغيل الأول هو الأطول — أما اللاحقة فتقارن الحجم وتاريخ التعديل، لذا لا تستغرق عادةً إلا ثوانيَ.',
    'Pliki w kopii będą zaszyfrowane; bez hasła nie da się ich odczytać.':
        'ستكون الملفات في النسخة الاحتياطية مشفّرة؛ ولا يمكن قراءتها دون كلمة المرور.',
    'Podfoldery są uwzględniane automatycznie.':
        'تُضمَّن المجلدات الفرعية تلقائيًا.',
    'Pokazuj ekran powitalny przy starcie':
        'إظهار شاشة الترحيب عند بدء التشغيل',
    'Ponownie sprawdza podłączone nośniki':
        'يعيد فحص وسائط التخزين المتصلة',
    'Program będzie utrzymywał jeden folder zgodny ze źródłem. Każdy kolejny przebieg dopisze tylko to, co się zmieniło.':
        'سيُبقي البرنامج مجلدًا واحدًا مطابقًا للمصدر. وكل تشغيل لاحق يضيف ما تغيّر فقط.',
    'Projekty i kod':
        'المشاريع والشيفرة البرمجية',
    'Przechodzi do następnego kroku':
        'ينتقل إلى الخطوة التالية',
    'Przechodzi do pełnego okna programu':
        'ينتقل إلى نافذة البرنامج الكاملة',
    'Sam wskażesz, co ma trafić do kopii.':
        'تحدد بنفسك ما يدخل النسخة الاحتياطية.',
    'System plików: {filesystem}, klaster {cluster}':
        'نظام الملفات: {filesystem}، وحدة التخصيص {cluster}',
    'Ten katalog leży wewnątrz folderu źródłowego — wybierz inny.':
        'هذا المجلد يقع داخل مجلد مصدر — اختر مجلدًا آخر.',
    'Ten nośnik nie obsługuje twardych dowiązań, więc każda wersja z datą zajmie tyle miejsca co pełna kopia. Przy tym nośniku rozważ „jedną aktualną kopię”.':
        'لا يدعم وسيط التخزين هذا الروابط الثابتة، لذا سيشغل كل إصدار مؤرَّخ مساحة نسخة كاملة. ومع هذا الوسيط فكّر في «نسخة واحدة محدَّثة».',
    'To dysk systemowy — kopia nie przetrwa jego awarii. Jeśli masz drugi dysk albo pendrive, wybierz jego.':
        'هذا قرص النظام — ولن تنجو النسخة الاحتياطية من تعطّله. إن كان لديك قرص ثانٍ أو ذاكرة USB، فاختر أحدهما.',
    'To się wydarzy':
        'ما سيحدث',
    'Trzy gotowe zestawy zamiast kilkunastu przełączników.':
        'ثلاث مجموعات جاهزة بدلًا من خيارات كثيرة.',
    'Twoje pliki osobiste z folderów użytkownika. Najczęstszy wybór.':
        'ملفاتك الشخصية من مجلدات المستخدم. الخيار الأكثر شيوعًا.',
    'Uruchamia kreator, który ustawi kopię krok po kroku':
        'يشغّل المعالج الذي يُعدّ النسخ الاحتياطي خطوة بخطوة',
    'Uruchom kreator…':
        'تشغيل المعالج…',
    'Ustawia kopię krok po kroku i zapisuje ją jako szablon':
        'يُعدّ النسخ الاحتياطي خطوة بخطوة ويحفظه كقالب',
    'Ustawienia pierwszej kopii':
        'إعداد أول نسخة احتياطية',
    'Ustawienia pierwszej kopii…':
        'إعداد أول نسخة احتياطية…',
    'W tym katalogu jest już kopia ({count} {files}) — program ją uzupełni, a nie nadpisze.':
        'يحتوي هذا المجلد على نسخة احتياطية بالفعل ({count} {files}) — وسيستكملها البرنامج ولن يكتب فوقها.',
    'Wraca do poprzedniego kroku':
        'يعود إلى الخطوة السابقة',
    'Wskaż dowolny katalog docelowy':
        'حدد أي مجلد وجهة تريده',
    'Wskaż folder kopii i kliknij „Sprawdź kopię”.':
        'حدد مجلد النسخة الاحتياطية وانقر «فحص النسخة الاحتياطية».',
    'Wstecz':
        'السابق',
    'Wybierz':
        'اختر',
    'Wybierz inny folder…':
        'اختيار مجلد آخر…',
    'Wybierz to, co najbliższe. Dokładną listę folderów poprawisz niżej.':
        'اختر الأقرب إلى حاجتك. ويمكنك تعديل قائمة المجلدات بدقة أدناه.',
    'Wybrane foldery':
        'مجلدات مختارة',
    'Zamknij':
        'إغلاق',
    'Zamyka kreator bez zapisywania':
        'يغلق المعالج دون حفظ',
    'Zapisuje nowe i zmienione pliki. Pierwszy raz trwa najdłużej.':
        'يكتب الملفات الجديدة والمعدّلة. المرة الأولى تستغرق أطول وقت.',
    'Zapisuje szablon bez uruchamiania kopii':
        'يحفظ القالب دون بدء النسخ الاحتياطي',
    'Zapisuje szablon i od razu uruchamia kopię':
        'يحفظ القالب ويبدأ النسخ الاحتياطي فورًا',
    'Zapisz i zrób kopię':
        'حفظ وإنشاء نسخة احتياطية',
    'Zapisz ustawienia':
        'حفظ الإعدادات',
    'Zrób kopię':
        'إنشاء نسخة احتياطية',
    'dysk systemowy':
        'قرص النظام',
    'wolne {free} z {total}':
        'متاح {free} من {total}',
    'Porównano ze źródłem: {source}; tylko z sumą kontrolną (źródło zmieniło się albo jest niedostępne): {checksum}.':
        'المقارنة بالمصدر: {source}؛ وبالمجموع الاختباري فقط (لأن المصدر تغيّر أو غير متاح): {checksum}.',
    'Przywraca losową próbkę plików do katalogu tymczasowego i porównuje je ze źródłem.\nSprawdza całą drogę odzyskiwania, a trwa minuty. Nic nie zostaje na dysku.':
        'يستعيد عينة عشوائية من الملفات إلى مجلد مؤقت ويقارنها بالمصدر.\nيختبر مسار الاسترجاع كله في دقائق. ولا يبقى شيء على القرص.',
    'Próbne przywrócenie':
        'استعادة تجريبية',
    'W kopii nie ma plików, które dałoby się sprawdzić próbnie.':
        'لا توجد في النسخة الاحتياطية ملفات يمكن فحصها باستعادة تجريبية.',
    'przywrócony plik różni się od pliku źródłowego':
        'الملف المستعاد يختلف عن الملف المصدر',
    'przywrócony plik różni się od sumy kontrolnej zapisanej podczas kopii':
        'الملف المستعاد يختلف عن المجموع الاختباري المسجَّل أثناء النسخ',
    'próbne przywrócenie':
        'الاستعادة التجريبية',
    '(brak zapisanych szablonów)':
        '(لا توجد قوالب محفوظة)',
    'Bez tego kopia planowa ruszy dopiero wtedy, gdy sam otworzysz program.':
        'من دون ذلك لن يبدأ النسخ الاحتياطي المجدول إلا عندما تفتح البرنامج بنفسك.',
    'Codziennie o godzinie':
        'يوميًا في وقت محدد',
    'Codziennie o wybranej godzinie (zalecane)':
        'يوميًا في وقت تختاره (موصى به)',
    'Dla dysku USB podłączanego od czasu do czasu. Najwyżej jedna kopia na 12 godzin.':
        'لقرص USB تصله من حين لآخر. نسخة احتياطية واحدة على الأكثر كل 12 ساعة.',
    'Dostępne w zainstalowanej wersji programu (plik EXE).':
        'متاح في الإصدار المثبَّت من البرنامج (ملف EXE).',
    'Godzina kopii codziennej (czas tego komputera).':
        'وقت النسخ الاحتياطي اليومي (بحسب ساعة هذا الحاسوب).',
    'Harmonogram działa wtedy, gdy działa program — także ukryty przy zegarze.':
        'تعمل الجدولة ما دام البرنامج يعمل — حتى وهو مخفي بجوار الساعة.',
    'Harmonogram nie uruchamia kopii, dopóki tego nie odznaczysz. Ręczne kopie działają.':
        'لن تبدأ الجدولة أي نسخ احتياطي حتى تلغي تحديد هذا الخيار. أما النسخ اليدوي فيعمل.',
    'Harmonogram szablonu „{name}” zapisany.':
        'تم حفظ جدولة القالب «{name}».',
    'Harmonogram:':
        'الجدولة:',
    'Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.':
        'إذا كان الحاسوب مطفأً حينها، فسيبدأ النسخ الاحتياطي بعد تشغيله.',
    'Kiedy kopia z tego szablonu ma ruszać sama.':
        'متى يبدأ النسخ الاحتياطي من هذا القالب تلقائيًا.',
    'Kiedy robić kopię?':
        'متى يجري النسخ الاحتياطي؟',
    'Kopia będzie robiona codziennie o {time}; termin przegapiony przy wyłączonym komputerze program nadrobi po jego włączeniu.':
        'سيجري النسخ الاحتياطي يوميًا في {time}؛ وإذا فات الموعد والحاسوب مطفأ، فسيعوّضه البرنامج بعد تشغيله.',
    'Kopia planowa nie powiodła się':
        'فشل النسخ الاحتياطي المجدول',
    'Kopia rusza tylko wtedy, gdy ją uruchomisz.':
        'لا يبدأ النسخ الاحتياطي إلا عندما تشغّله بنفسك.',
    'Kopia ruszy po podłączeniu dysku docelowego (najwyżej raz na 12 godzin).':
        'سيبدأ النسخ الاحتياطي عند توصيل قرص الوجهة (مرة واحدة كل 12 ساعة على الأكثر).',
    'Kopia ruszy po podłączeniu dysku docelowego — najwyżej raz na 12 godzin.':
        'يبدأ النسخ الاحتياطي عند توصيل قرص الوجهة — مرة واحدة كل 12 ساعة على الأكثر.',
    'Kopia sprzed miesiąca nie chroni tego, co zmieniło się od tamtej pory.':
        'النسخة الاحتياطية التي مضى عليها شهر لا تحمي ما تغيّر منذ ذلك الحين.',
    'Kopia „{name}” czeka':
        'النسخة الاحتياطية «{name}» متأخرة',
    'Kopia „{name}” nie ruszyła':
        'لم يبدأ النسخ الاحتياطي «{name}»',
    'Kopie planowe działają, gdy działa program (także ukryty przy zegarze).':
        'تعمل النسخ الاحتياطية المجدولة ما دام البرنامج يعمل (حتى وهو مخفي بجوار الساعة).',
    'Kopie planowe działają, gdy działa program: po zamknięciu okna zostaje ikona przy zegarze, a przy logowaniu do Windows program uruchamia się w tle.':
        'تعمل النسخ الاحتياطية المجدولة ما دام البرنامج يعمل: بعد إغلاق النافذة تبقى أيقونة بجوار الساعة، وعند تسجيل الدخول إلى Windows يبدأ البرنامج في الخلفية.',
    'Kopie planowe i praca w tle':
        'النسخ المجدولة والعمل في الخلفية',
    'Kopie planowe wykonają się o czasie. Program zamkniesz z menu ikony przy zegarze.':
        'ستُنفَّذ النسخ الاحتياطية المجدولة في موعدها. ويمكنك إنهاء البرنامج من قائمة الأيقونة بجوار الساعة.',
    'Kopię uruchamiasz przyciskiem. Najprostsze, ale łatwo o niej zapomnieć.':
        'تبدأ النسخ الاحتياطي بزر. الأبسط، لكن من السهل نسيانه.',
    'Kopię uruchamiasz sam — przyciskiem w programie albo z menu ikony przy zegarze.':
        'تبدأ النسخ الاحتياطي بنفسك — بالزر في البرنامج أو من قائمة الأيقونة بجوار الساعة.',
    'Następna kopia: {when}. Jeśli komputer będzie wtedy wyłączony, kopia ruszy po jego włączeniu.':
        'النسخ الاحتياطي التالي: {when}. إذا كان الحاسوب مطفأً حينها، فسيبدأ النسخ بعد تشغيله.',
    'Nie udało się zmienić startu przy logowaniu — szczegóły w dzienniku.':
        'تعذّر تغيير التشغيل عند تسجيل الدخول — التفاصيل في سجل الأحداث.',
    'Od {days} dni nie było udanej kopii. Podłącz dysk docelowy albo otwórz program, żeby sprawdzić, co się dzieje.':
        'لم يتم أي نسخ احتياطي ناجح منذ {days} أيام. وصّل قرص الوجهة أو افتح البرنامج لترى ما يجري.',
    'Otwórz Sigelith Backup':
        'فتح Sigelith Backup',
    'Po podłączeniu dysku docelowego':
        'عند توصيل قرص الوجهة',
    'Po podłączeniu dysku z kopią':
        'عند توصيل قرص النسخ الاحتياطي',
    'Po zamknięciu okna działaj dalej przy zegarze, gdy są kopie planowe':
        'متابعة العمل بجوار الساعة بعد إغلاق النافذة، عند وجود نسخ مجدولة',
    'Potrzebne, żeby kopie planowe ruszały bez Twojego udziału. Hasło trafia do magazynu systemowego powiązanego z Twoim kontem, nie do plików programu.':
        'ضروري كي تبدأ النسخ الاحتياطية المجدولة دون تدخلك. تُحفظ كلمة المرور في مخزن النظام المرتبط بحسابك، لا في ملفات البرنامج.',
    'Program uruchamia się w tle przy logowaniu, więc terminy nie przepadną.':
        'يبدأ البرنامج في الخلفية عند تسجيل الدخول، فلا تفوت أي مواعيد.',
    'Ręcznie':
        'يدويًا',
    'Ręcznie — kiedy zechcę':
        'يدويًا — متى شئت',
    'Start przy logowaniu włączony':
        'تم تفعيل التشغيل عند تسجيل الدخول',
    'Szablon jest zaszyfrowany, a hasło nie jest zapamiętane. Kopie planowe potrzebują hasła zapisanego w Menedżerze poświadczeń Windows.':
        'القالب مشفّر، وكلمة مروره غير محفوظة. والنسخ الاحتياطية المجدولة تحتاج إلى كلمة مرور محفوظة في إدارة بيانات الاعتماد في Windows.',
    'Sigelith Backup będzie uruchamiał się w tle, żeby wykonywać kopie planowe. Wyłączysz to w ustawieniach programu.':
        'سيبدأ Sigelith Backup في الخلفية لتنفيذ النسخ الاحتياطية المجدولة. ويمكنك إيقاف ذلك من إعدادات البرنامج.',
    'Sigelith Backup działa w tle':
        'يعمل Sigelith Backup في الخلفية',
    'Uruchamiaj program w tle przy logowaniu do Windows':
        'تشغيل البرنامج في الخلفية عند تسجيل الدخول إلى Windows',
    'Wstrzymaj kopie planowe':
        'إيقاف النسخ المجدولة مؤقتًا',
    'Zakończ':
        'إنهاء',
    'Zamknięcie okna chowa je, a harmonogram pilnuje terminów. Program zamkniesz z menu ikony przy zegarze.':
        'إغلاق النافذة يخفيها فقط، وتواصل الجدولة مراقبة المواعيد. ويمكنك إنهاء البرنامج من قائمة الأيقونة بجوار الساعة.',
    'Zrób kopię teraz':
        'إنشاء نسخة احتياطية الآن',
    '{summary} Szczegóły znajdziesz w programie, w zakładce „Dziennik”.':
        '{summary} تجد التفاصيل في البرنامج، في تبويب «سجل الأحداث».',
    'Program działa z uprawnieniami administratora. Nie są mu potrzebne — kopia i przywracanie działają bez nich, a pliki zapisane przez administratora mogą później nie dać się zmienić ze zwykłego konta.':
        'يعمل البرنامج بصلاحيات المسؤول. وهو لا يحتاج إليها — فالنسخ الاحتياطي والاستعادة يعملان من دونها، والملفات التي يكتبها المسؤول قد يتعذّر تعديلها لاحقًا من حساب عادي.',
    'Pliki otwarte w innych programach nie trafiły do kopii: {files}. Zamknij te programy i uruchom kopię ponownie — dograne zostaną tylko te pliki.':
        'لم تدخل النسخة الاحتياطية ملفات مفتوحة في برامج أخرى: {files}. أغلق تلك البرامج وشغّل النسخ الاحتياطي مجددًا — ولن تُضاف إلا هذه الملفات.',
    'Uwaga: w źródle zmieniło się podejrzanie dużo plików — {reasons}':
        'تحذير: تغيّر عدد كبير على نحو مريب من الملفات في المصدر — {reasons}',
    'Wstrzymano kopię: w źródle zmieniło się podejrzanie dużo plików. {reasons}':
        'أُوقف النسخ الاحتياطي مؤقتًا: تغيّر عدد كبير على نحو مريب من الملفات في المصدر. {reasons}',
    'Zmieniło się albo zniknęło {count} z {previous} plików poprzedniej kopii.':
        'تغيّر أو اختفى {count} من أصل {previous} من ملفات النسخة الاحتياطية السابقة.',
    '{suspicious} z {evaluated} sprawdzonych zmienionych plików ma treść, która nie pasuje do ich typu (wygląda na zaszyfrowaną).':
        '{suspicious} من أصل {evaluated} من الملفات المعدّلة التي فُحصت محتواها لا يطابق نوعها (يبدو مشفّرًا).',
    'Kontynuuj mimo to':
        'المتابعة على أي حال',
    'Kopia planowa wstrzymana':
        'أُوقف النسخ الاحتياطي المجدول مؤقتًا',
    'Kopia wstrzymana do decyzji.':
        'أُوقف النسخ الاحتياطي مؤقتًا بانتظار قرارك.',
    'Kopia wstrzymana — w źródle zmieniło się podejrzanie dużo plików.':
        'أُوقف النسخ الاحتياطي مؤقتًا — تغيّر عدد كبير على نحو مريب من الملفات في المصدر.',
    'Podejrzanie dużo zmian':
        'تغييرات كثيرة على نحو مريب',
    'Wstrzymaj kopię':
        'إيقاف النسخ مؤقتًا',
    '{reasons}\n\nJeśli to spodziewane — aktualizacja programu, przeniesienie albo przerobienie wielu plików — kontynuuj.\n\nJeśli nie, NIE kontynuuj: tak wygląda działanie oprogramowania szyfrującego pliki (ransomware). Sprawdź najpierw, czy Twoje pliki dają się otworzyć. Wcześniejsze wersje w kopii pozostają nietknięte.':
        '{reasons}\n\nإذا كان ذلك متوقعًا — تحديث برنامج، أو نقل ملفات كثيرة أو إعادة تحريرها — فتابع.\n\nوإن لم يكن كذلك، فلا تتابع إطلاقًا: هذا ما يبدو عليه عمل البرامج الخبيثة التي تشفّر الملفات (ransomware). تحقق أولًا من أن ملفاتك ما زالت تُفتح. وتبقى الإصدارات السابقة في النسخة الاحتياطية سليمة.',
    '{reasons} To może być działanie złośliwego oprogramowania szyfrującego pliki. Otwórz program, sprawdź pliki i uruchom kopię ręcznie.':
        '{reasons} قد يكون هذا من فعل برنامج خبيث يشفّر الملفات. افتح البرنامج، وتحقق من الملفات، وشغّل النسخ الاحتياطي يدويًا.',
    'Pominięto {count} {files}.':
        'تم تخطي {count} {files}.',
    'Ponawiam {count} {files}…':
        'جارٍ إعادة محاولة {count} {files}…',
    ' (bez {count} {files})':
        ' (دون {count} {files})',
    'plik otwarty w innym programie':
        'ملف مفتوح في برنامج آخر',
    'pliki otwarte w innych programach':
        'ملفات مفتوحة في برامج أخرى',
    'plików otwartych w innych programach':
        'ملفات مفتوحة في برامج أخرى',
    'pliku otwartego w innym programie':
        'ملف مفتوح في برنامج آخر',
    '\n\n…i kolejne: {count}.':
        '\n\n…وغيرها: {count}.',
    'Foldery objęte kopią ({count}): {list}':
        'المجلدات المشمولة بالنسخ الاحتياطي ({count}): {list}',
    'Nośnik nie obsługuje twardych dowiązań — kopiuję do nowej wersji niezmienione pliki: {count} ({size})…':
        'لا يدعم وسيط التخزين الروابط الثابتة — جارٍ نسخ الملفات غير المتغيّرة إلى الإصدار الجديد: {count} ({size})…',
    'Pliki bez sumy kontrolnej sprawdzone tylko co do rozmiaru, bo ich źródło zmieniło się albo jest niedostępne: {count}.':
        'ملفات دون مجموع اختباري فُحص حجمها فقط، لأن مصدرها تغيّر أو غير متاح: {count}.',
    'Pliki bez zapisanej sumy kontrolnej, porównane ze źródłem i uzupełnione w spisie treści: {count}.':
        'ملفات دون مجموع اختباري مسجَّل، قورنت بالمصدر وأُضيفت إلى الفهرس: {count}.',
    'Pliki przeniesione w źródle: {count} — trafią do kopii bez przesyłania danych.':
        'ملفات نُقلت في المصدر: {count} — ستدخل النسخة الاحتياطية دون نقل بيانات.',
    'Pliki skasowane w źródle: {count} — {action}.':
        'ملفات حُذفت في المصدر: {count} — {action}.',
    'Pliki z końcówką dopisaną do nazwy, których oryginały zniknęły: {count}.':
        'ملفات أُضيفت لاحقة إلى أسمائها واختفت أصولها: {count}.',
    'Pliki zmienione w trakcie kopiowania: {count} — zostaną zapisane ponownie w przebiegu uzupełniającym.':
        'ملفات تغيّرت أثناء نسخها: {count} — ستُكتب مجددًا في جولة الاستكمال.',
    'Pliki, których brakuje w kopii i które zostaną zapisane ponownie: {count}.':
        'ملفات ناقصة من النسخة الاحتياطية وستُكتب مجددًا: {count}.',
    'Podpinanie niezmienionych plików do nowej wersji: {count}…':
        'جارٍ ربط الملفات غير المتغيّرة بالإصدار الجديد: {count}…',
    'Pomijam pliki, które już są w tej wersji kopii: {count}.':
        'جارٍ تخطي الملفات الموجودة بالفعل في هذا الإصدار: {count}.',
    'Porządkowanie historii — usunięte najstarsze wersje: {count}.':
        'تنظيف سجل الإصدارات — الإصدارات الأقدم المحذوفة: {count}.',
    'Przenoszenie plików, które zmieniły miejsce w źródle: {count}…':
        'جارٍ نقل الملفات التي تغيّر مكانها في المصدر: {count}…',
    'Próbne przywrócenie losowo wybranych plików: {count}…':
        'جارٍ الاستعادة التجريبية لملفات مختارة عشوائيًا: {count}…',
    'Usuwanie z kopii plików skasowanych w źródle: {count}…':
        'جارٍ حذف الملفات المحذوفة في المصدر من النسخة الاحتياطية: {count}…',
    'Uzupełniam kopię o pliki, które przybyły lub zmieniły się w trakcie: {count} ({size})…':
        'جارٍ استكمال النسخة الاحتياطية بالملفات التي ظهرت أو تغيّرت في أثناء ذلك: {count} ({size})…',
    'Uzupełnianie wersji {version} — pliki już zapisane, które zostaną pominięte: {count}.':
        'استكمال الإصدار {version} — ملفات مكتوبة بالفعل ستُتخطّى: {count}.',
    'Wznawiam wersję {version} — już zapisane: {done}, do dogrania: {todo}.':
        'جارٍ استئناف الإصدار {version} — المكتوب بالفعل: {done}، والمتبقي: {todo}.',
    'pliku':
        'ملف',
    'Brak fragmentu {cid} w magazynie kopii.':
        'القطعة {cid} مفقودة من مخزن قطع النسخة الاحتياطية.',
    'Brak opisu magazynu fragmentów w katalogu kopii.':
        'لا يوجد وصف لمخزن القطع في مجلد النسخة الاحتياطية.',
    'Duże pliki zapisuj różnicowo (od 256 MB)':
        'تخزين الملفات الكبيرة تزايديًا (256 MB فأكثر)',
    'Fragment {cid} jest uszkodzony.':
        'القطعة {cid} تالفة.',
    'Kolejna wersja dużego pliku — maszyny wirtualnej, skrzynki pocztowej, bazy —\nzapisuje tylko zmienione fragmenty zamiast całego pliku. W kopii taki plik\nleży jako przepis + fragmenty; złoży go program albo skrypt ratunkowy.':
        'الإصدار التالي من ملف كبير — آلة افتراضية أو صندوق بريد أو قاعدة بيانات —\nيحفظ القطع المعدّلة فقط بدلًا من الملف كله. وفي النسخة الاحتياطية يُخزَّن مثل هذا الملف\nكوصفة + قطع؛ ويعيد البرنامج أو سكربت الإنقاذ تجميعه.',
    'Opis magazynu fragmentów jest uszkodzony.':
        'وصف مخزن القطع تالف.',
    'Plik złożony z fragmentów różni się od zapisanego w przepisie.':
        'الملف المُجمَّع من القطع يختلف عما سُجّل في وصفته.',
    'Podane hasło nie pasuje do fragmentów zapisanych wcześniej w tej kopii.':
        'كلمة المرور المُدخلة لا تطابق القطع المكتوبة سابقًا في هذه النسخة الاحتياطية.',
    'Przepis pliku jest uszkodzony.':
        'وصفة الملف تالفة.',
    'To nie jest przepis pliku zapisanego fragmentami.':
        'هذه ليست وصفة ملف مخزَّن على هيئة قطع.',
    'Usunięto nieużywane fragmenty dużych plików: {count} ({size}).':
        'حُذفت القطع غير المستخدمة من الملفات الكبيرة: {count} ({size}).',
    ', zakotwiczona w Bitcoinie':
        '، مُرسَّخ في Bitcoin',
    'Adres usługi:':
        'عنوان الخدمة:',
    'Brak fragmentu {cid} w kopii poza domem.':
        'القطعة {cid} مفقودة من النسخة خارج المنزل.',
    'Brak klucza albo hasła w Menedżerze poświadczeń Windows — zapisz ustawienia kopii poza domem jeszcze raz.':
        'المفتاح أو كلمة المرور غير موجودين في إدارة بيانات الاعتماد في Windows — احفظ إعدادات النسخة خارج المنزل مرة أخرى.',
    'Brak spisu wersji, którego dotyczy znacznik.':
        'قائمة ملفات الإصدار التي يخصها الطابع الزمني مفقودة.',
    'Certyfikat PDF':
        'شهادة PDF',
    'Druga, zaszyfrowana kopia w usłudze zgodnej z S3 (np. Backblaze B2)':
        'نسخة احتياطية ثانية مشفّرة في خدمة متوافقة مع S3 (مثل Backblaze B2)',
    'Folder w kubełku:':
        'المجلد داخل الحاوية:',
    'Hasło kopii poza domem':
        'كلمة مرور النسخة خارج المنزل',
    'Hasło kopii poza domem nie pasuje do danych zapisanych w tym miejscu.':
        'كلمة مرور النسخة خارج المنزل لا تطابق البيانات المحفوظة في هذا الموقع.',
    'Hasło kopii poza domem powinno mieć co najmniej 10 znaków.':
        'يجب ألا تقل كلمة مرور النسخة خارج المنزل عن 10 أحرف.',
    'Hasło szyfrowania:':
        'كلمة مرور التشفير:',
    'Identyfikator klucza:':
        'معرّف المفتاح:',
    'Katalog, do którego trafią pliki':
        'المجلد الذي ستُوضع فيه الملفات',
    'Klucz tajny':
        'المفتاح السري',
    'Klucz tajny:':
        'المفتاح السري:',
    'Kopia na dysku obok komputera nie przetrwa pożaru ani kradzieży. Tu ustawisz drugą kopię w usłudze zgodnej z S3 (np. Backblaze B2). Pliki są szyfrowane na tym komputerze osobnym hasłem — usługa widzi tylko nieczytelne fragmenty.':
        'النسخة الاحتياطية على قرص بجوار الحاسوب لن تنجو من حريق أو سرقة. هنا تُعدّ نسخة ثانية في خدمة متوافقة مع S3 (مثل Backblaze B2). تُشفَّر الملفات على هذا الحاسوب بكلمة مرور مستقلة — فلا ترى الخدمة إلا قطعًا غير مقروءة.',
    'Kopia poza domem':
        'النسخة خارج المنزل',
    'Kopia poza domem dla szablonu „{name}” zapisana.':
        'تم حفظ إعدادات النسخة خارج المنزل للقالب «{name}».',
    'Kopia poza domem nie ruszyła':
        'لم يبدأ إرسال النسخة خارج المنزل',
    'Kopia poza domem potrzebuje Menedżera poświadczeń Windows, a jest on niedostępny.':
        'النسخة خارج المنزل تحتاج إلى إدارة بيانات الاعتماد في Windows، وهي غير متاحة.',
    'Kopia poza domem „{name}”':
        'النسخة خارج المنزل «{name}»',
    'Kopia poza domem…':
        'النسخة خارج المنزل…',
    'Korzeń tygodnia zakotwiczony w łańcuchu Bitcoina.':
        'جذر الأسبوع مُرسَّخ في سلسلة Bitcoin.',
    'Kubełek (bucket):':
        'الحاوية (bucket):',
    'Migawek w usłudze: {count}.':
        'اللقطات في الخدمة: {count}.',
    'Migawka i cel':
        'اللقطة والوجهة',
    'Migawka kopii poza domem jest uszkodzona.':
        'لقطة النسخة خارج المنزل تالفة.',
    'Migawka {stamp}: plików bez zmian {reused}, wysłanych {files}, nowych fragmentów {chunks} ({size}).':
        'اللقطة {stamp}: ملفات دون تغيير {reused}، ملفات مرفوعة {files}، قطع جديدة {chunks} ({size}).',
    'MinIO / Wasabi / inna zgodna z S3':
        'MinIO / Wasabi / خدمة أخرى متوافقة مع S3',
    'NIEPOPRAWNY':
        'غير صالح',
    'Nie ma migawki {stamp} w kopii poza domem.':
        'لا توجد لقطة {stamp} في النسخة خارج المنزل.',
    'Nie udało się połączyć z usługą przechowywania: {error}':
        'تعذّر الاتصال بخدمة التخزين: {error}',
    'Nie udało się wczytać migawek: {error}':
        'تعذّر تحميل اللقطات: {error}',
    'Nie udało się zapisać klucza albo hasła w magazynie systemowym.':
        'تعذّر حفظ المفتاح أو كلمة المرور في مخزن النظام.',
    'Odśwież z sieci':
        'تحديث من الشبكة',
    'Opis kopii poza domem jest uszkodzony.':
        'وصف النسخة خارج المنزل تالف.',
    'Oznakowana: {utc} (BeatTime {beat})':
        'الطابع الزمني: {utc} (بتوقيت BeatTime {beat})',
    'Pliki wersji różnią się od spisu, który został oznakowany.':
        'ملفات الإصدار تختلف عن القائمة التي حصلت على الطابع الزمني.',
    'Pobiera i odszyfrowuje pliki wybranej migawki':
        'ينزّل ملفات اللقطة المحددة ويفك تشفيرها',
    'Pobiera listę migawek z usługi':
        'ينزّل قائمة اللقطات من الخدمة',
    'Pobiera podpis tygodnia i stan kotwicy w Bitcoinie':
        'ينزّل توقيع الأسبوع وحالة الترسيخ في Bitcoin',
    'Pobieram potwierdzenia…':
        'جارٍ تنزيل الإيصالات…',
    'Podaj hasło szyfrowania kopii poza domem.':
        'أدخل كلمة مرور تشفير النسخة خارج المنزل.',
    'Podaj klucz tajny usługi.':
        'أدخل المفتاح السري للخدمة.',
    'Podam dane ręcznie':
        'إدخال البيانات يدويًا',
    'Pominięte (otwarte w innych programach albo zmienione w trakcie): {count}.':
        'الملفات المتخطّاة (مفتوحة في برامج أخرى أو تغيّرت في أثناء ذلك): {count}.',
    'Porządkowanie kopii poza domem…':
        'جارٍ تنظيف النسخة خارج المنزل…',
    'Potwierdzenia odświeżone.':
        'تم تحديث الإيصالات.',
    'Poza dom':
        'خارج المنزل',
    'Połączenie działa: zapis, odczyt i usuwanie się udały.':
        'الاتصال يعمل: نجحت الكتابة والقراءة والحذف.',
    'Połączenie nie działa: {error}':
        'الاتصال لا يعمل: {error}',
    'Przywraca pliki z zaszyfrowanej kopii w usłudze S3 — także na nowym komputerze':
        'يستعيد الملفات من النسخة المشفّرة في خدمة S3 — حتى على حاسوب جديد',
    'Przywracanie z kopii poza domem':
        'الاستعادة من النسخة خارج المنزل',
    'Przywracanie {count} {files} z kopii poza domem…':
        'جارٍ استعادة {count} {files} من النسخة خارج المنزل…',
    'Przywróć':
        'استعادة',
    'Region:':
        'المنطقة:',
    'Skąd':
        'المصدر',
    'Spis wersji zgodny ze znacznikiem: {answer}':
        'قائمة ملفات الإصدار مطابقة للطابع الزمني: {answer}',
    'Spis wersji został zmieniony po oznakowaniu.':
        'عُدّلت قائمة ملفات الإصدار بعد منحها الطابع الزمني.',
    'Sprawdza spis wersji, drogę w drzewie tygodnia i podpis — bez sieci':
        'يفحص قائمة ملفات الإصدار والمسار في شجرة الأسبوع والتوقيع — دون الشبكة',
    'Sprawdzam połączenie…':
        'جارٍ فحص الاتصال…',
    'Sprawdź':
        'فحص',
    'Sprawdź połączenie':
        'فحص الاتصال',
    'Starsze migawki są usuwane, gdy nadmiar sięgnie kilku — co kilka dni.':
        'تُحذف اللقطات الأقدم عندما تتراكم بضع لقطات زائدة — كل بضعة أيام.',
    'Suma w drzewie tygodnia: {answer}':
        'البصمة في شجرة الأسبوع: {answer}',
    'Suma wersji nie należy do drzewa tygodnia podanego w potwierdzeniu.':
        'بصمة الإصدار ليست جزءًا من شجرة الأسبوع المذكورة في الإيصال.',
    'Ta wersja nie ma znacznika czasu.':
        'ليس لهذا الإصدار طابع زمني.',
    'Także po kopiach planowych. Wysyłane są tylko pliki nowe i zmienione.':
        'بعد النسخ المجدولة أيضًا. ولا تُرفع إلا الملفات الجديدة والمعدّلة.',
    'Tydzień jeszcze się nie zamknął — podpis pojawi się po poniedziałku 00:00 UTC.':
        'لم يُغلق الأسبوع بعد — سيظهر التوقيع بعد يوم الاثنين الساعة 00:00 UTC.',
    'Usunięto starsze migawki: {count}, nieużywane fragmenty: {chunks}.':
        'حُذفت لقطات أقدم: {count}، وقطع غير مستخدمة: {chunks}.',
    'Usługa chwilowo niedostępna ({status}).':
        'الخدمة غير متاحة مؤقتًا ({status}).',
    'Usługa odrzuciła żądanie ({status} {code}): {message}':
        'رفضت الخدمة الطلب ({status} {code}): {message}',
    'Usługa przechowywania':
        'خدمة التخزين',
    'Usługa zwróciła inną treść niż zapisana.':
        'أعادت الخدمة محتوى مختلفًا عما كُتب.',
    'Usługa:':
        'الخدمة:',
    'Uzupełnij adres usługi, nazwę kubełka i klucze dostępu.':
        'أكمل عنوان الخدمة واسم الحاوية ومفاتيح الوصول.',
    'Uzupełnij adres usługi, region, kubełek i identyfikator klucza.':
        'أكمل عنوان الخدمة والمنطقة والحاوية ومعرّف المفتاح.',
    'W tym katalogu kopii nie ma jeszcze znaczników czasu.':
        'لا توجد طوابع زمنية في مجلد النسخة الاحتياطية هذا بعد.',
    'W tym miejscu nie ma jeszcze kopii poza domem.':
        'لا توجد نسخة خارج المنزل في هذا الموقع بعد.',
    'Wczytaj migawki':
        'تحميل اللقطات',
    'Wczytaj migawki i wybierz jedną z listy.':
        'حمّل اللقطات واختر واحدة من القائمة.',
    'Wczytuję migawkę {stamp}…':
        'جارٍ تحميل اللقطة {stamp}…',
    'Wczytuję poprzednią migawkę kopii poza domem…':
        'جارٍ تحميل اللقطة السابقة للنسخة خارج المنزل…',
    'Wybierz migawkę i katalog, do którego trafią pliki.':
        'اختر لقطة والمجلد الذي ستُوضع فيه الملفات.',
    'Wybierz wersję z listy.':
        'اختر إصدارًا من القائمة.',
    'Wysyłaj poza dom po każdej udanej kopii z tego szablonu':
        'الإرسال إلى خارج المنزل بعد كل نسخ احتياطي ناجح من هذا القالب',
    'Wysyłam poza dom pliki nowe i zmienione: {count}…':
        'جارٍ إرسال الملفات الجديدة والمعدّلة إلى خارج المنزل: {count}…',
    'Z kopii poza domem…':
        'من النسخة خارج المنزل…',
    'Zachowuj migawek:':
        'عدد اللقطات المحفوظة:',
    'Zapisuje ustawienia; klucz i hasło trafiają do Menedżera poświadczeń Windows':
        'يحفظ الإعدادات؛ ويُحفظ المفتاح وكلمة المرور في إدارة بيانات الاعتماد في Windows',
    'Zapisuje, odczytuje i usuwa mały plik próbny':
        'يكتب ملف اختبار صغيرًا ويقرؤه ويحذفه',
    'Zapisuję migawkę {stamp}…':
        'جارٍ حفظ اللقطة {stamp}…',
    'Znacznik dowodzi, że wersja kopii w dokładnie tym kształcie istniała w podanej chwili. Podpis tygodnia pojawia się po jego zamknięciu (poniedziałek 00:00 UTC), a kotwica w Bitcoinie — zwykle kilka godzin później.':
        'يثبت الطابع الزمني أن إصدار النسخة الاحتياطية كان موجودًا بهذا الشكل تمامًا في اللحظة المذكورة. ويظهر توقيع الأسبوع بعد إغلاقه (الاثنين 00:00 UTC)، والترسيخ في Bitcoin — عادةً بعد ذلك ببضع ساعات.',
    'Znacznika czasu nie udało się zapisać: {error}':
        'تعذّر حفظ الطابع الزمني: {error}',
    'Znaczniki czasu':
        'الطوابع الزمنية',
    'Znaczniki czasu…':
        'الطوابع الزمنية…',
    'kopia poza domem':
        'النسخة خارج المنزل',
    'np. komputer-domowy':
        'مثلًا home-computer',
    'oznakowana {when} — podpis po zamknięciu tygodnia':
        'طابع زمني في {when} — التوقيع بعد إغلاق الأسبوع',
    'podpisana (tydzień {week}){bitcoin}':
        'موقَّع (الأسبوع \u2066{week}\u2069){bitcoin}',
    'poprawny':
        'صالح',
    'przywracanie z kopii poza domem':
        'الاستعادة من النسخة خارج المنزل',
    'Łączę się z usługą…':
        'جارٍ الاتصال بالخدمة…',
    ' dni':
        ' أيام',
    ' mies.':
        ' شهرًا',
    ' tyg.':
        ' أسابيع',
    'Ile ostatnich wersji zachować. Starsze są kasowane po udanym przebiegu.':
        'عدد الإصدارات الأخيرة التي يُحتفظ بها. وتُحذف الأقدم بعد تشغيل ناجح.',
    'Kalendarz zostawia najnowszą wersję z każdego z ostatnich dni, tygodni\ni miesięcy — gęsto dla świeżych zmian, rzadko dla dawnych. Nadmiar jest\nkasowany po udanym przebiegu; wersje niedokończone nigdy.':
        'يُبقي التقويم أحدث إصدار من كل يوم وأسبوع\nوشهر من الفترة الأخيرة — بكثافة للتغييرات الحديثة، وبتباعد للقديمة. ويُحذف الزائد\nبعد تشغيل ناجح؛ أما الإصدارات غير المكتملة فلا تُحذف أبدًا.',
    'Z ilu ostatnich dni zachować po jednej, najnowszej wersji.':
        'عدد الأيام الأخيرة التي يُحتفظ من كل منها بإصدار واحد، هو الأحدث.',
    'Z ilu ostatnich miesięcy zachować po jednej, najnowszej wersji.':
        'عدد الأشهر الأخيرة التي يُحتفظ من كل منها بإصدار واحد، هو الأحدث.',
    'Z ilu ostatnich tygodni zachować po jednej, najnowszej wersji.':
        'عدد الأسابيع الأخيرة التي يُحتفظ من كل منها بإصدار واحد، هو الأحدث.',
    'Zachowuj:':
        'الاحتفاظ بـ:',
    'kalendarz: dni, tygodnie, miesiące':
        'تقويم: أيام وأسابيع وأشهر',
    'ostatnie wersje':
        'الإصدارات الأخيرة',
    'wszystkie wersje':
        'كل الإصدارات',
    ' (niedokończona)':
        ' (غير مكتمل)',
    'Fragment nazwy albo ścieżki, bez rozróżniania wielkości liter.':
        'جزء من اسم أو مسار، دون التمييز بين الأحرف الكبيرة والصغيرة.',
    'Główny folder kopii':
        'المجلد الرئيسي للنسخة الاحتياطية',
    'Historia pliku':
        'سجل إصدارات الملف',
    'Nazwa':
        'الاسم',
    'Nic nie znaleziono.':
        'لم يُعثر على شيء.',
    'Nie udało się: {error}':
        'فشلت العملية: {error}',
    'Odtwarza plik do katalogu tymczasowego i otwiera go':
        'يستعيد الملف إلى مجلد مؤقت ويفتحه',
    'Odtwarza plik w wybranym miejscu':
        'يستعيد الملف إلى مكان تختاره',
    'Odtwarzam „{name}”…':
        'جارٍ استعادة «{name}»…',
    'Otwarto kopię „{name}” (plik tymczasowy, zniknie po zamknięciu programu).':
        'فُتحت نسخة من «{name}» (ملف مؤقت يُحذف عند إغلاق البرنامج).',
    'Otwórz':
        'فتح',
    'Otwórz kopię':
        'فتح نسخة',
    'Pliki i wersje wprost z kopii — bez przywracania':
        'الملفات والإصدارات مباشرة من النسخة الاحتياطية — دون استعادة',
    'Pliki i wersje wprost z kopii — bez przywracania całości.':
        'الملفات والإصدارات مباشرة من النسخة الاحتياطية — دون استعادتها كاملة.',
    'Pokazuje pliki i wersje tej kopii — pojedynczy plik otworzysz bez przywracania całości':
        'يعرض ملفات هذه النسخة الاحتياطية وإصداراتها — يمكنك فتح ملف منفرد دون استعادة كل شيء',
    'Pokaż foldery':
        'إظهار المجلدات',
    'Przeglądaj…':
        'تصفّح…',
    'Przeglądanie':
        'التصفح',
    'Przeszukuje spis treści kopii':
        'يبحث في فهرس النسخة الاحتياطية',
    'Rozmiar':
        'الحجم',
    'Szukaj':
        'بحث',
    'Szukaj pliku w najnowszym stanie kopii…':
        'ابحث عن ملف في أحدث حالة للنسخة الاحتياطية…',
    'Szukam…':
        'جارٍ البحث…',
    'W których wersjach jest ten plik i kiedy się zmieniał':
        'الإصدارات التي تحتوي على هذا الملف ومتى تغيّر',
    'W tym folderze nie ma wersji kopii.':
        'لا توجد إصدارات للنسخة الاحتياطية في هذا المجلد.',
    'Wczytuje wersje z tego folderu kopii':
        'يحمّل الإصدارات من مجلد النسخة الاحتياطية هذا',
    'Wersja kopii, której zawartość widzisz poniżej.':
        'إصدار النسخة الاحتياطية الذي تعرض محتواه أدناه.',
    'Wersja: {version}':
        'الإصدار: {version}',
    'Wersje z tym plikiem: {count}. Dwuklik otwiera kopię z danej wersji.':
        'الإصدارات التي تحتوي على هذا الملف: {count}. النقر المزدوج يفتح النسخة من الإصدار المعني.',
    'Wraca z wyników wyszukiwania do drzewa folderów':
        'يعود من نتائج البحث إلى شجرة المجلدات',
    'Wskaż folder kopii i kliknij „Otwórz”.':
        'حدد مجلد النسخة الاحتياطية وانقر «فتح».',
    'Zapisano: {path}':
        'تم الحفظ: {path}',
    'Zapisz jako…':
        'حفظ باسم…',
    'Zapisz kopię pliku':
        'حفظ نسخة من الملف',
    'Zaznacz plik i wybierz „Otwórz kopię”, żeby zajrzeć do niego w zwykłym programie, albo „Historia pliku”, żeby zobaczyć, w których wersjach się zmieniał.':
        'حدد ملفًا واختر «فتح نسخة» لتطّلع عليه في برنامجه المعتاد، أو «سجل إصدارات الملف» لترى في أي الإصدارات تغيّر.',
    'Zmieniono':
        'تاريخ التعديل',
    'Znalezione pliki: {count}. Wyniki pochodzą z najnowszego stanu kopii.':
        'الملفات التي عُثر عليها: {count}. النتائج من أحدث حالة للنسخة الاحتياطية.',
    'przeglądanie kopii':
        'تصفح النسخة الاحتياطية',
    'zmieniony':
        'معدَّل',
    'najstarsza zachowana kopia':
        'أقدم نسخة محفوظة',
    'Foldery w AppData':
        'مجلدات في AppData',
    'Przywracanie utworzy nowe foldery bezpośrednio w AppData:\n\n{folders}\n\nWindows pozwala wersji programu ze Sklepu tworzyć je tylko w jej prywatnej kopii — pliki będą widoczne w tym programie, ale nie w programie, do którego należą.\n\nNajprościej: zainstaluj i raz uruchom tamten program (utworzy swój folder), a potem przywróć jeszcze raz. Albo przywróć do zwykłego folderu i przenieś pliki Eksploratorem.':
        'ستُنشئ الاستعادة مجلدات جديدة مباشرة في AppData:\n\n{folders}\n\nلا يسمح Windows لإصدار البرنامج المثبَّت من Microsoft Store بإنشائها إلا في نسخته الخاصة — فستظهر الملفات في هذا البرنامج، لا في البرنامج الذي تنتمي إليه.\n\nالحل الأبسط: ثبّت ذلك البرنامج وشغّله مرة واحدة (سينشئ مجلده)، ثم أعد الاستعادة. أو استعِد إلى مجلد عادي وانقل الملفات بمستكشف الملفات.',
    'Przywracanie utworzyłoby w AppData nowe foldery, których inne programy nie zobaczą: {folders}':
        'ستُنشئ الاستعادة في AppData مجلدات جديدة لن تراها البرامج الأخرى: {folders}',
    'Przywracanie wstrzymane do decyzji.':
        'أُوقفت الاستعادة مؤقتًا بانتظار قرارك.',
    'Przywróć mimo to':
        'الاستعادة على أي حال',
    'Start programu przy logowaniu wyłączono w Ustawieniach Windows. Włączysz go tam: Ustawienia → Aplikacje → Uruchamianie → Sigelith Backup.':
        'عُطّل تشغيل البرنامج عند تسجيل الدخول في إعدادات Windows. ويمكنك تفعيله من هناك: الإعدادات ← التطبيقات ← بدء التشغيل ← Sigelith Backup.',
    'Start przy logowaniu':
        'التشغيل عند تسجيل الدخول',
    'Start przy logowaniu wyłączono w Ustawieniach Windows → Aplikacje → Uruchamianie; dopóki go tam nie włączysz, kopie planowe działają tylko przy otwartym programie.':
        'عُطّل التشغيل عند تسجيل الدخول في إعدادات Windows ← التطبيقات ← بدء التشغيل؛ وما لم تفعّله هناك، فلن تعمل النسخ الاحتياطية المجدولة إلا والبرنامج مفتوح.',
    'Ten sam przełącznik jest w Ustawieniach Windows → Aplikacje → Uruchamianie. Wyłączony tam da się włączyć tylko tam.':
        'المفتاح نفسه موجود في إعدادات Windows ← التطبيقات ← بدء التشغيل. وإذا عُطّل هناك فلا يمكن تفعيله إلا من هناك.',
    'Brak pliku {name} w katalogu programu.':
        'الملف {name} غير موجود في مجلد البرنامج.',
    'Jakie dane program przetwarza i gdzie':
        'ما البيانات التي يعالجها البرنامج وأين',
    'Kod źródłowy Qt':
        'الشيفرة المصدرية لـ Qt',
    'Licencja programu':
        'ترخيص البرنامج',
    'Licencja programu i licencje użytych składników':
        'ترخيص البرنامج وتراخيص المكوّنات المستخدمة',
    'Licencje':
        'التراخيص',
    'Licencje i prywatność':
        'التراخيص والخصوصية',
    'Licencje…':
        'التراخيص…',
    'Otwiera folder z plikami licencji w Eksploratorze':
        'يفتح المجلد الذي يحوي ملفات التراخيص في مستكشف الملفات',
    'Pokaż pliki licencji':
        'إظهار ملفات التراخيص',
    'Polityka prywatności':
        'سياسة الخصوصية',
    'Polityka prywatności…':
        'سياسة الخصوصية…',
    'Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0 — to osobne pliki w katalogu programu, które można zastąpić zgodnymi wersjami. Kod źródłowy wersji dołączonych do programu: {qt} oraz {pyside}.':
        'يستخدم البرنامج مكتبتَي Qt وPySide6 المرخّصتين بموجب LGPL-3.0 — وملفاتهما منفصلة في مجلد البرنامج ويمكن استبدالها بإصدارات متوافقة. الشيفرة المصدرية للإصدارات المرفقة بالبرنامج: {qt}\u200e و{pyside}\u200e.',
    'Program korzysta z bibliotek Qt i PySide6 na licencji LGPL-3.0, z Pythona i z innych składników na licencjach otwartych (m.in. MIT, BSD, Apache 2.0); ikony: Bootstrap Icons (MIT). Wykaz, prawa autorskie, pełne teksty licencji i adresy kodu źródłowego Qt są pod przyciskiem „Licencje”.':
        'يستخدم البرنامج مكتبتَي Qt وPySide6 المرخّصتين بموجب LGPL-3.0، وPython ومكوّنات أخرى بتراخيص مفتوحة المصدر (منها MIT وBSD وApache 2.0)؛ والأيقونات: Bootstrap Icons (بترخيص MIT). وتجد القائمة وحقوق النشر والنصوص الكاملة للتراخيص وعناوين الشيفرة المصدرية لـ Qt تحت الزر «التراخيص».',
    'Program usunie z Menedżera poświadczeń Windows wszystkie hasła, które zapamiętał: hasła kopii i dane dostępu do kopii poza domem. Kopie planowe szablonów zaszyfrowanych będą potem czekać, aż podasz hasło.\n\nUsunąć?':
        'سيحذف البرنامج من إدارة بيانات الاعتماد في Windows كل كلمات المرور التي حفظها: كلمات مرور النسخ الاحتياطية وبيانات الوصول إلى النسخة خارج المنزل. وبعد ذلك ستنتظر النسخ المجدولة للقوالب المشفّرة حتى تُدخل كلمة المرور.\n\nهل تريد حذفها؟',
    'Składniki i ich licencje':
        'المكوّنات وتراخيصها',
    'Strona z kodem źródłowym Qt w wersji użytej w programie':
        'صفحة الشيفرة المصدرية لـ Qt بالإصدار المستخدم في البرنامج',
    'Usunięte zapamiętane hasła: {count}.':
        'كلمات المرور المحفوظة التي حُذفت: {count}.',
    'Usuwa z Menedżera poświadczeń Windows wszystkie hasła zapamiętane przez program — na przykład przed odinstalowaniem':
        'يحذف من إدارة بيانات الاعتماد في Windows كل كلمات المرور التي حفظها البرنامج — مثلًا قبل إلغاء التثبيت',
    'Usuń zapamiętane hasła':
        'حذف كلمات المرور المحفوظة',
    'Usuń zapamiętane hasła…':
        'حذف كلمات المرور المحفوظة…',
    '© {years} {publisher}. Wolne oprogramowanie na licencji GNU GPL w wersji 3 lub nowszej.':
        '© {years} {publisher}. برنامج حر مرخَّص بموجب GNU GPL، الإصدار 3 أو أي إصدار أحدث.',
    'Kod źródłowy':
        'الشيفرة المصدرية',
    'Kod źródłowy programu w serwisie GitHub':
        'الشيفرة المصدرية للبرنامج على GitHub',
    'Sigelith odrzucił żądanie ({status}): {detail}':
        'رفض Sigelith الطلب ({status}): {detail}',
    'Nie udało się połączyć z Sigelith: {error}':
        'تعذّر الاتصال بـ Sigelith: {error}',
    'Sigelith odesłał potwierdzenie innej sumy kontrolnej.':
        'أعاد Sigelith إيصالًا لبصمة مختلفة.',
    'Znacznik czeka na połączenie z Sigelith.':
        'الطابع الزمني بانتظار الاتصال بـ Sigelith.',
    'Podpis tygodnia nie zgadza się z kluczem Sigelith zapisanym w programie.':
        'توقيع الأسبوع لا يطابق مفتاح Sigelith المدمج في البرنامج.',
    'Otwiera certyfikat znacznika na stronie Sigelith':
        'يفتح شهادة الطابع الزمني على موقع Sigelith',
    'Podpis Sigelith: {answer}':
        'توقيع Sigelith: {answer}',
    'Znaczniki Sigelith wersji w tym katalogu kopii: sprawdzenie i certyfikat':
        'طوابع Sigelith الزمنية لإصدارات مجلد النسخة الاحتياطية هذا: الفحص والشهادة',
    'Znakuję wersję czasem Sigelith (wysyłana jest tylko suma kontrolna)…':
        'جارٍ منح الإصدار طابعًا زمنيًا من Sigelith (لا تُرسل إلا البصمة)…',
    'Znacznik czasu czeka na połączenie z Sigelith — zostanie wysłany przy następnej kopii.':
        'الطابع الزمني بانتظار الاتصال بـ Sigelith — وسيُرسل مع النسخ الاحتياطي التالي.',
    'Znakuj wersję czasem Sigelith':
        'منح الإصدار طابعًا زمنيًا من Sigelith',
    'Znaczniki czasu Sigelith':
        'طوابع Sigelith الزمنية',
    'czeka na połączenie z Sigelith':
        'بانتظار الاتصال بـ Sigelith',
    'Dowód, że kopia w tym kształcie istniała danego dnia (podpis Ed25519, kotwica\nw Bitcoinie). Do sigelith.org trafia wyłącznie suma kontrolna spisu wersji —\nżadne nazwy plików ani ich treść.':
        'إثبات أن النسخة الاحتياطية كانت موجودة بهذا الشكل في يوم معيّن (توقيع Ed25519، وترسيخ\nفي Bitcoin). ولا يصل إلى sigelith.org سوى بصمة قائمة ملفات الإصدار —\nلا أسماء ملفات ولا محتوى.',
    'Kopie zapasowe folderów na dysk zewnętrzny, z historią wersji i szyfrowaniem. Wszystko dzieje się na Twoim komputerze, bez konta i bez telemetrii. Z internetem program łączy się tylko wtedy, gdy sam włączysz kopię poza domem albo znaczniki czasu Sigelith.':
        'نسخ احتياطية لمجلداتك على قرص خارجي، مع سجل للإصدارات وتشفير. يجري كل شيء على حاسوبك، دون حساب ودون قياس عن بُعد. ولا يتصل البرنامج بالإنترنت إلا إذا فعّلت بنفسك النسخة خارج المنزل أو طوابع Sigelith الزمنية.',
    'Bez dokumentu: {count} {stamps} — plik zmienił się po stemplu albo zniknął i nie ma go w żadnej wersji tej kopii ({names}). Sam dowód jest zachowany.':
        'دون مستند: {count} {stamps} — تغيّر الملف بعد الختم أو اختفى، وليس موجودًا في أي إصدار من هذه النسخة الاحتياطية ({names}). أما الإثبات نفسه فمحفوظ.',
    'Brak pliku dowodu albo dowód jest zaszyfrowany.':
        'ملف الإثبات مفقود أو الإثبات مشفّر.',
    'Chroni dowody Sigelith: historię stempli i oznakowane dokumenty.':
        'يحمي أدلة Sigelith: سجل الأختام والمستندات المختومة.',
    'Chroń dowody Sigelith':
        'حماية أدلة Sigelith',
    'Chroń też dowody Sigelith':
        'حماية أدلة Sigelith أيضًا',
    'Dokument':
        'المستند',
    'Dokumenty oznakowane w Sigelith, zabezpieczone w tej kopii: sprawdzenie i odzyskanie':
        'المستندات المختومة في Sigelith والمحفوظة في هذه النسخة الاحتياطية: الفحص والاسترجاع',
    'Dowody Sigelith':
        'أدلة Sigelith',
    'Dowody Sigelith: historia stempli i dokładne kopie oznakowanych dokumentów z plikami .beatproof trafią do magazynu dowodów w katalogu kopii.':
        'أدلة Sigelith: سيُحفظ سجل الأختام ونسخ طبق الأصل من المستندات المختومة مع ملفات \u200e.beatproof في مخزن الأدلة داخل مجلد النسخة الاحتياطية.',
    'Dowody Sigelith: zabezpieczone dokumenty {count} z {total}':
        'أدلة Sigelith: المستندات المحفوظة {count} من {total}',
    'Dowody Sigelith…':
        'أدلة Sigelith…',
    'Dowody z problemem: {count} — szczegóły w kolumnie „Stan”.':
        'إثباتات بها مشكلة: {count} — التفاصيل في العمود «الحالة».',
    'Dowodów Sigelith nie udało się zabezpieczyć: {error}':
        'تعذّر حفظ أدلة Sigelith: {error}',
    "Droga w drzewie Merkle'a nie prowadzi do podpisanego korzenia tygodnia.":
        'المسار في شجرة Merkle لا يؤدي إلى جذر الأسبوع الموقَّع.',
    'Gdzie zapisać dokumenty i dowody':
        'أين تُحفظ المستندات والإثباتات',
    'Historia stempli Sigelith Desktop i dokładne bajty oznakowanych dokumentów, z plikami .beatproof — w osobnym magazynie, którego retencja nie sprząta.':
        'سجل أختام Sigelith Desktop والبايتات الدقيقة للمستندات المختومة، مع ملفات \u200e.beatproof — في مخزن منفصل لا تنظّفه سياسة الاحتفاظ.',
    'Każdy stempel ma tu swój folder z dokładnie tym dokumentem, który oznakowano, i plikiem .beatproof. „Sprawdź” liczy sumę każdego dokumentu i sprawdza podpis tygodnia bez łączenia się z siecią.':
        'لكل ختم هنا مجلده الخاص الذي يحوي المستند الذي خُتم بعينه وملف \u200e.beatproof. ويحسب الزر «فحص» بصمة كل مستند ويتحقق من توقيع الأسبوع دون الاتصال بالشبكة.',
    'Kopia obejmie folder danych Sigelith Desktop (historię stempli), a każdy oznakowany\ndokument trafi — dokładnie w tej postaci, którą oznakowano — do magazynu dowodów\nw katalogu kopii, razem z plikiem .beatproof. Starych wersji magazyn nie dotyczy:\nretencja go nie sprząta.':
        'ستشمل النسخة الاحتياطية مجلد بيانات Sigelith Desktop (سجل الأختام)، وسيُحفظ كل مستند\nمختوم — بالشكل الذي خُتم به تمامًا — في مخزن الأدلة داخل مجلد\nالنسخة الاحتياطية، مع ملف \u200e.beatproof الخاص به. والمخزن منفصل عن الإصدارات القديمة:\nلا تنظّفه سياسة الاحتفاظ.',
    'Magazyn dowodów jest pusty.':
        'مخزن الأدلة فارغ.',
    'Na tym komputerze jest Sigelith Desktop: {count} {stamps}.':
        'Sigelith Desktop موجود على هذا الحاسوب، وفيه {count} {stamps}.',
    'Na tym komputerze nie ma danych Sigelith Desktop.':
        'لا توجد بيانات Sigelith Desktop على هذا الحاسوب.',
    'Otwórz folder dowodów':
        'فتح مجلد الأدلة',
    'Oznakowano':
        'تاريخ الختم',
    'Pokazuje magazyn dowodów w Eksploratorze':
        'يعرض مخزن الأدلة في مستكشف الملفات',
    'Przywróć zaznaczone…':
        'استعادة المحدد…',
    'Sigelith Desktop: {count} {stamps} w folderze {path}.':
        'Sigelith Desktop: يوجد {count} {stamps} في المجلد {path}.',
    'Sprawdza każdy dokument i jego dowód bez łączenia z siecią':
        'يفحص كل مستند وإثباته دون الاتصال بالشبكة',
    'Sprawdzam dowody…':
        'جارٍ فحص الإثباتات…',
    'Stan':
        'الحالة',
    'Stemple w magazynie: {count}, z dokumentem: {documents}.':
        'الأختام في المخزن: {count}، ومنها مع مستند: {documents}.',
    'Suma dokumentu nie zgadza się z dowodem.':
        'بصمة المستند لا تطابق الإثبات.',
    'To nie jest plik dowodu Sigelith (beatproof-v1).':
        'هذا ليس ملف إثبات من Sigelith (بصيغة beatproof-v1).',
    'Tydzień stempla jeszcze się nie zamknął — podpis dojdzie przy kolejnej kopii.':
        'لم يُغلق أسبوع الختم بعد — وسيُضاف التوقيع مع النسخ الاحتياطي التالي.',
    'W magazynie nie ma dokumentu do tego dowodu.':
        'لا يوجد في المخزن مستند لهذا الإثبات.',
    'Wszystkie dowody pasują do dokumentów i mają poprawny podpis.':
        'كل الإثباتات تطابق مستنداتها وتوقيعها صالح.',
    'Zabezpieczam dokumenty oznakowane w Sigelith…':
        'جارٍ حفظ المستندات المختومة في Sigelith…',
    'Zapisano pliki: {count} w {path}.':
        'الملفات المحفوظة: {count} في {path}.',
    'Zapisuje dokumenty razem z plikami .beatproof we wskazanym folderze':
        'يحفظ المستندات مع ملفات \u200e.beatproof في المجلد الذي تحدده',
    'bez dokumentu — dowód zachowany':
        'دون مستند — الإثبات محفوظ',
    'czekają na podpis tygodnia: {count}':
        'بانتظار توقيع الأسبوع: {count}',
    'dokument i dowód są w kopii':
        'المستند والإثبات في النسخة الاحتياطية',
    'dokument jest; dowód czeka na podpis tygodnia':
        'المستند موجود؛ والإثبات بانتظار توقيع الأسبوع',
    'dowodu nie da się odczytać':
        'تتعذّر قراءة الإثبات',
    'dowody Sigelith':
        'أدلة Sigelith',
    'dowody uzupełnione o podpis tygodnia: {count}':
        'إثباتات أُكملت بتوقيع الأسبوع: {count}',
    'nowe: {count}':
        'جديدة: {count}',
    'odtworzone ze starszych wersji kopii: {count}':
        'مستعادة من إصدارات أقدم للنسخة الاحتياطية: {count}',
    'sprawdzony: dokument i dowód się zgadzają':
        'تم الفحص: المستند والإثبات متطابقان',
    'stempel':
        'ختم',
    'stemple':
        'أختام',
    'stempli':
        'ختمًا',
    'zaszyfrowany — podaj hasło, żeby sprawdzić':
        'مشفّر — أدخل كلمة المرور للفحص',
    'Chroń dowody Sigelith, gdy go zainstaluję':
        'حماية أدلة Sigelith عندما أثبّته',
    'Dowody Sigelith: na tym komputerze nie ma jeszcze Sigelith Desktop — ochrona zacznie działać sama, gdy się pojawi.':
        'أدلة Sigelith: لا يوجد Sigelith Desktop على هذا الحاسوب بعد — وستبدأ الحماية تلقائيًا عند ظهوره.',
    'Dowody Sigelith: ochrona zacznie działać sama, gdy zainstalujesz Sigelith Desktop.':
        'أدلة Sigelith: ستبدأ الحماية تلقائيًا عندما تثبّت Sigelith Desktop.',
    'Dowody czasu dla ważnych dokumentów':
        'إثباتات زمنية للمستندات المهمة',
    'Kopia zachowa każdy dokument oznakowany w Sigelith Desktop dokładnie w tej postaci, którą oznakowano, razem z dowodem — nawet gdy oryginał później się zmieni.':
        'ستحفظ النسخة الاحتياطية كل مستند مختوم في Sigelith Desktop بالشكل الذي خُتم به تمامًا، مع إثباته — حتى لو تغيّر الأصل لاحقًا.',
    'Ochrona zacznie działać sama, gdy na komputerze pojawi się Sigelith Desktop.':
        'ستبدأ الحماية تلقائيًا عندما يظهر Sigelith Desktop على الحاسوب.',
    'Otwiera stronę programu Sigelith Desktop':
        'يفتح صفحة برنامج Sigelith Desktop',
    'Poznaj Sigelith Desktop':
        'تعرّف على Sigelith Desktop',
    'Sigelith Desktop, program tego samego wydawcy, oznakuje dokument czasem: to podpisany dowód, że plik w tej postaci istniał w danej chwili, sprawdzalny bez udziału kogokolwiek. Sigelith Backup przechowa potem każdy oznakowany dokument razem z dowodem.':
        'يختم Sigelith Desktop، وهو برنامج من الناشر نفسه، المستند بطابع زمني: إثبات موقَّع على أن الملف كان موجودًا بهذا الشكل في لحظة معيّنة، ويمكن التحقق منه دون الاعتماد على أحد. ثم يحفظ Sigelith Backup كل مستند مختوم مع إثباته.',
    'Umowy, faktury, projekty — czasem trzeba wykazać, że dokument istniał danego dnia.':
        'عقود وفواتير ومشاريع — أحيانًا يلزمك إثبات أن مستندًا كان موجودًا في يوم معيّن.',
    'Nieznany format spisu wersji.':
        'صيغة قائمة ملفات الإصدار غير معروفة.',
    'Ta wersja nie ma pieczęci dla pojedynczych plików (kopia sprzed wersji 3.0 albo bez znaczników czasu).':
        'ليس لهذا الإصدار ختم للملفات المنفردة (نسخة احتياطية سابقة للإصدار 3.0 أو دون طوابع زمنية).',
    'Pieczęć tej wersji czeka jeszcze na podpis tygodnia Sigelith — dowód będzie gotowy po poniedziałku 00:00 UTC i kolejnej kopii.':
        'ختم هذا الإصدار ما زال بانتظار توقيع Sigelith الأسبوعي — وسيكون الإثبات جاهزًا بعد يوم الاثنين الساعة 00:00 UTC وبعد النسخ الاحتياطي التالي.',
    'Brak oświadczenia pieczęci w folderze wersji.':
        'بيان الختم مفقود من مجلد الإصدار.',
    'Oświadczenie pieczęci nie zgadza się z pieczęcią wersji.':
        'بيان الختم لا يطابق ختم الإصدار.',
    'Drzewo plików wersji nie zgadza się z pieczęcią.':
        'شجرة ملفات الإصدار لا تطابق الختم.',
    'Tego pliku nie ma w spisie tej wersji.':
        'هذا الملف غير موجود في قائمة ملفات هذا الإصدار.',
    'To nie jest dowód pliku z kopii Sigelith Backup ({format}).':
        'هذا ليس إثبات ملف من Sigelith Backup (الصيغة: {format}).',
    'Dowód jest uszkodzony — brakuje pól albo mają zły format.':
        'الإثبات تالف — بعض الحقول ناقصة أو صيغتها غير صحيحة.',
    'Ten plik nie jest plikiem, którego dotyczy dowód.':
        'هذا الملف ليس الملف الذي يخصه الإثبات.',
    'Ścieżka pliku w dowodzie nie zgadza się z liściem drzewa.':
        'مسار الملف في الإثبات لا يطابق ورقة الشجرة.',
    'Droga w drzewie plików nie prowadzi do korzenia z pieczęci.':
        'المسار في شجرة الملفات لا يؤدي إلى الجذر المختوم.',
    'Oświadczenie pieczęci nie potwierdza tego drzewa plików.':
        'بيان الختم لا يؤكد شجرة الملفات هذه.',
    'Potwierdzenie Sigelith nie dotyczy tej pieczęci.':
        'تأكيد Sigelith لا يخص هذا الختم.',
    'Dowód czasu…':
        'إثبات زمني…',
    'Zapisuje dowód, że ten plik był w kopii w chwili jej oznakowania — bez ujawniania innych plików':
        'يحفظ إثباتًا على أن هذا الملف كان في النسخة الاحتياطية لحظة ختمها — دون كشف الملفات الأخرى',
    'Dowód czasu':
        'إثبات زمني',
    'Dołączyć do dowodu ścieżkę pliku w kopii („{path}”)?\n\nBez niej dowód dalej potwierdza plik i chwilę oznakowania, ale nie mówi, gdzie plik leżał.':
        'هل تريد تضمين مسار الملف في النسخة الاحتياطية («{path}») في الإثبات؟\n\nمن دونه يظل الإثبات يؤكد الملف ولحظة الختم، لكنه لا يذكر أين كان الملف.',
    'Przygotowuję dowód dla „{name}”…':
        'جارٍ تجهيز الإثبات لـ «{name}»…',
    'Zapisz dowód czasu':
        'حفظ الإثبات الزمني',
    'Dowód pliku Sigelith (*{suffix})':
        'إثبات ملف Sigelith (*{suffix})',
    'Zapisano dowód i certyfikat PDF: {path}. Sprawdzi go Sigelith Desktop albo strona sigelith.org/verify/.':
        'حُفظ الإثبات وشهادة PDF: {path}. ويمكن التحقق منه في Sigelith Desktop أو على sigelith.org/verify/\u200e.',
    'Kopia jest zaszyfrowana — podaj hasło, aby ją sprawdzić.':
        'النسخة الاحتياطية مشفّرة — أدخل كلمة المرور لفحصها.',
    'Ta wersja nie ma pieczęci — nie ma z czym porównać plików.':
        'ليس لهذا الإصدار ختم — فلا يوجد ما تُقارن به الملفات.',
    'Pieczęć wersji się nie potwierdza: {problems}':
        'ختم الإصدار لم يجتز التحقق: {problems}',
    'brak podpisu tygodnia':
        'لا يوجد توقيع للأسبوع',
    'Audyt przerwany.':
        'أُوقف التدقيق.',
    'próbka {checked} z {listed} plików':
        'عينة من الملفات، {checked} من أصل {listed}',
    'wszystkie pliki ({count})':
        'كل الملفات ({count})',
    'Nietknięta: sprawdzono {scope}, wszystko zgodne z pieczęcią w publicznym dzienniku.':
        'سليم: فُحصت {scope}، وكل شيء مطابق للختم في السجل العلني.',
    'zmienione: {files}':
        'معدَّلة: {files}',
    'brakujące: {files}':
        'مفقودة: {files}',
    'nieczytelne albo uszkodzone: {files}':
        'غير مقروءة أو تالفة: {files}',
    'PODMIENIONA albo uszkodzona ({scope}) — {details}.':
        'تم التلاعب به أو تلف ({scope}) — {details}.',
    'Audyt treści':
        'تدقيق المحتوى',
    'Czyta z nośnika każdy plik tej wersji i porównuje go z sumą oznakowaną w publicznym dzienniku':
        'يقرأ من وسيط التخزين كل ملف في هذا الإصدار ويقارنه بالبصمة المختومة في السجل العلني',
    'Ostatnia nietknięta':
        'آخر إصدار سليم',
    'Sprawdza wersje od najnowszej i wskazuje ostatnią zgodną z pieczęcią — z niej przywracaj':
        'يفحص الإصدارات بدءًا من الأحدث ويحدد آخر إصدار مطابق لختمه — استعِد منه',
    'Ostatnia nietknięta wersja: {label} — z niej przywracaj.':
        'آخر إصدار سليم: {label} — استعِد منه.',
    'Żadna wersja z pieczęcią nie jest nietknięta.':
        'لا يوجد إصدار مختوم سليم.',
    'Czytam pliki kopii i porównuję je z pieczęcią w publicznym dzienniku…':
        'جارٍ قراءة ملفات النسخة الاحتياطية ومقارنتها بالختم في السجل العلني…',
    'Sprawdzam próbkę starszej wersji z pieczęcią w publicznym dzienniku…':
        'جارٍ فحص عينة من إصدار أقدم مقارنةً بختمه في السجل العلني…',
    'Audyt z pieczęcią: próbka wersji {label} zgodna z publicznym dziennikiem.':
        'تدقيق الختم: عينة الإصدار {label} مطابقة للسجل العلني.',
    'UWAGA — audyt z pieczęcią, wersja {label}: {details}':
        'تحذير — تدقيق الختم، الإصدار {label}: {details}',
    'Przekaż…':
        'تسليم…',
    'Zapisuje tę wersję pliku i otwiera ją w Sigelith Handover — odbiorca potwierdzi odbiór własnym kluczem':
        'يحفظ هذا الإصدار من الملف ويفتحه في Sigelith Handover — وسيؤكد المستلم الاستلام بمفتاحه الخاص',
    'Przekazanie z dowodem doręczenia':
        'التسليم مع إثبات التسليم',
    'Przekazanie z dowodem doręczenia robi Sigelith Desktop (od wersji 3.0.1): odbiorca potwierdza odbiór własnym kluczem, a chwila doręczenia trafia do publicznego dziennika. Na tym komputerze go nie ma albo jest w starszej wersji. Otworzyć stronę programu?':
        'التسليم مع إثبات التسليم يتولاه Sigelith Desktop (الإصدار 3.0.1 أو أحدث): يؤكد المستلم الاستلام بمفتاحه الخاص، وتُسجَّل لحظة التسليم في السجل العلني. وهو غير موجود على هذا الحاسوب أو مثبَّت بإصدار أقدم. هل تريد فتح صفحة البرنامج؟',
    'Zapisz plik do przekazania':
        'حفظ الملف المراد تسليمه',
    'Otwieram Sigelith Handover z plikiem „{name}” — wybierz odbiorcę.':
        'جارٍ فتح Sigelith Handover مع الملف «{name}» — اختر المستلم.',
    'Kapsuły czasu…':
        'كبسولات الزمن…',
    'Pliki zapieczętowane w tej kopii do daty — klucze wydają dopiero po niej sieć drand i serwer kluczy Sigelith':
        'ملفات مختومة في هذه النسخة الاحتياطية حتى تاريخ معيّن — لا تُطلق شبكة drand وخادم مفاتيح Sigelith المفاتيح إلا بعده',
    'Wskaż najpierw folder kopii — kapsuła leży w kopii.':
        'حدد مجلد النسخة الاحتياطية أولًا — فالكبسولة محفوظة داخل النسخة الاحتياطية.',
    'Kapsuły czasu':
        'كبسولات الزمن',
    'Kapsuła pieczętuje wybrany folder do chwili, którą wskażesz. Otwierają ją dowolne dwie z trzech części: runda sieci drand z tej chwili, udział serwera kluczy Sigelith (wydawany dopiero po tej chwili — to zasada operatora, nie kryptografia) i kod odzyskiwania zapisany obok kapsuły. Kto ma tę kopię, ma więc i kod: do wcześniejszego otwarcia wystarczy mu, że operator złamie swoją zasadę. Po tej chwili otworzy ją każdy, kto ma jej pliki. Kapsuła leży w tej kopii, nie na serwerze; otwiera ją strona sigelith.org/capsule/.':
        'تختم الكبسولة المجلد المختار حتى اللحظة التي تحددها. ويفتحها أيُّ جزأين من ثلاثة: جولة شبكة drand الخاصة بتلك اللحظة، وحصة خادم مفاتيح Sigelith (التي لا تُطلق إلا بعد تلك اللحظة — وهذه قاعدة يلتزم بها المشغّل، لا قيد تشفيري)، ورمز الاسترجاع المحفوظ بجانب الكبسولة. فمن يملك هذه النسخة الاحتياطية يملك الرمز أيضًا، ولا يحتاج لفتحها مبكرًا إلا إلى أن يخالف المشغّل قاعدته. وبعد تلك اللحظة يستطيع فتحها كل من لديه ملفاتها. الكبسولة محفوظة في هذه النسخة الاحتياطية لا على خادم؛ وتفتحها صفحة sigelith.org/capsule/\u200e.',
    'Wybierz kapsułę z listy albo utwórz nową.':
        'اختر كبسولة من القائمة أو أنشئ كبسولة جديدة.',
    'Nowa kapsuła…':
        'كبسولة جديدة…',
    'Pieczętuje wybrany folder do daty':
        'يختم المجلد المختار حتى تاريخ معيّن',
    'Pokaż w folderze':
        'إظهار في المجلد',
    'Otwiera folder kapsuły w Eksploratorze':
        'يفتح مجلد الكبسولة في مستكشف الملفات',
    'Otwórz na stronie':
        'فتح على الموقع',
    'Strona sigelith.org/capsule/ otwiera kapsułę po jej dacie':
        'تفتح صفحة sigelith.org/capsule/\u200e الكبسولة بعد تاريخها',
    'można otworzyć':
        'يمكن فتحها',
    'zamknięta':
        'مختومة',
    'W tej kopii nie ma jeszcze kapsuł czasu.':
        'لا توجد كبسولات زمن في هذه النسخة الاحتياطية بعد.',
    'Ta kapsuła da się otworzyć na stronie sigelith.org/capsule/ — wskaż jej pliki.':
        'يمكن فتح هذه الكبسولة على صفحة sigelith.org/capsule/\u200e — حدد ملفاتها هناك.',
    'Kapsuła jest zamknięta do daty z listy. Kod odzyskiwania leży w pliku obok niej.':
        'الكبسولة مختومة حتى التاريخ المذكور في القائمة. ورمز الاسترجاع محفوظ في ملف بجانبها.',
    'Wybierz folder do zapieczętowania':
        'اختر المجلد المراد ختمه',
    'Pieczętuję „{name}” — kilka sekund na krzywej eliptycznej…':
        'جارٍ ختم «{name}» — بضع ثوانٍ من حسابات المنحنى الإهليلجي…',
    'kapsuła czasu':
        'كبسولة زمن',
    'Kapsuła zapieczętowana':
        'خُتمت الكبسولة',
    '„{name}” otworzy się najwcześniej {when}.\n\nKod odzyskiwania (skopiowany do schowka, zapisany też obok kapsuły):\n\n{code}\n\nZapisz go w bezpiecznym miejscu. Przed datą otwarcia sam niczego nie otwiera; po niej zastępuje jeden z kluczy, gdyby był niedostępny.':
        'لن تُفتح الكبسولة «{name}» قبل {when}.\n\nرمز الاسترجاع (نُسخ إلى الحافظة، وحُفظ أيضًا بجانب الكبسولة):\n\n{code}\n\nاحفظه في مكان آمن. قبل تاريخ الفتح لا يفتح شيئًا وحده؛ وبعده يحل محل أحد المفاتيح إذا تعذّر الوصول إليه.',
    'Nie udało się zapieczętować: {error}':
        'تعذّر الختم: {error}',
    'Nowa kapsuła czasu':
        'كبسولة زمن جديدة',
    'Otworzy się najwcześniej':
        'لا تُفتح قبل',
    'kapsuła':
        'كبسولة',
    'Chwila otwarcia musi być w przyszłości.':
        'يجب أن تكون لحظة الفتح في المستقبل.',
    'Na bieżąco':
        'أولًا بأول',
    'Zmiany w folderach źródłowych trafiają do dzisiejszej wersji kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje. Jedna wersja na dzień; ze znacznikami czasu zamyka ją pieczęć następnego dnia.':
        'تدخل التغييرات في المجلدات المصدر إصدار اليوم من النسخة الاحتياطية بعد حفظها ببضع دقائق، وعند توصيل القرص تُزامَن النسخة الاحتياطية فورًا. إصدار واحد في اليوم؛ ومع الطوابع الزمنية يُغلقه ختم في اليوم التالي.',
    'Na bieżąco — po każdej zmianie i po podłączeniu dysku':
        'أولًا بأول — بعد كل تغيير وعند توصيل القرص',
    'Dla dysku podłączonego na stałe albo często: zmiany trafiają do kopii kilka minut po zapisie, a po podłączeniu dysku kopia od razu się synchronizuje.':
        'لقرص موصول دائمًا أو غالبًا: تدخل التغييرات النسخة الاحتياطية بعد حفظها ببضع دقائق، وعند توصيل القرص تُزامَن النسخة الاحتياطية فورًا.',
    'Kopia będzie na bieżąco: zmiany trafią do dzisiejszej wersji kilka minut po zapisie, a po podłączeniu dysku kopia od razu się zsynchronizuje.':
        'ستبقى النسخة الاحتياطية محدَّثة أولًا بأول: تدخل التغييرات إصدار اليوم بعد حفظها ببضع دقائق، وعند توصيل القرص تُزامَن النسخة الاحتياطية فورًا.',
    'przywracanie':
        'الاستعادة',
}
