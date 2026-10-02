# Sigelith Backup — polityka prywatności / Privacy policy

Obowiązuje od: 2026-09-29 · Effective: 2026-09-29

---

## Polski

**W skrócie:** program nie zbiera o Tobie żadnych danych. Nie ma konta, reklam ani
telemetrii. Kopie powstają na Twoim komputerze i na wskazanych przez Ciebie
nośnikach. Z internetem łączą się wyłącznie dwie funkcje, które musisz sam włączyć.

### Administrator

Adam Koch, Weißensteinstr. 44, 58093 Hagen,
Niemcy · e-mail: kontakt@advena-partners.com · Impressum:
https://sigelith.org/de/impressum/

### Co program przetwarza na Twoim komputerze

* Pliki z folderów, które wskażesz do kopii — czyta je i zapisuje ich kopie
  w wybranym przez Ciebie miejscu (np. na dysku zewnętrznym).
* Ustawienia, szablony kopii i historię operacji — w folderze danych programu
  na Twoim komputerze.
* Dziennik działania (m.in. ścieżki kopiowanych folderów i komunikaty o błędach) —
  lokalnie, do diagnozy problemów. Nigdzie nie jest wysyłany.
* Hasła do kopii — tylko jeśli zaznaczysz ich zapamiętanie; przechowuje je
  Menedżer poświadczeń Windows, nigdy pliki programu.
* Dowody Sigelith — tylko jeśli włączysz „Chroń dowody Sigelith”: program czyta na Twoim
  komputerze historię stempli Sigelith Desktop (nazwy, ścieżki i sumy oznakowanych
  dokumentów, notatki) i kopiuje folder danych Sigelith oraz oznakowane dokumenty do
  Twojej kopii. Niczego przy tym nie wysyła i niczego w folderze Sigelith nie zmienia.

Wydawca nie ma dostępu do żadnej z tych informacji.

**Usuwanie danych.** Ustawienia, szablony i dziennik wersji ze Sklepu Windows usuwa
razem z programem. Zapamiętane hasła zostają w Menedżerze poświadczeń Windows, dopóki
ich nie usuniesz: w programie (Ustawienia → „Usuń zapamiętane hasła…”) albo
w Panelu sterowania → Menedżer poświadczeń. Kopie zapasowe na Twoich nośnikach
i w Twojej usłudze S3 należą do Ciebie — program ich nie usuwa.

### Funkcje korzystające z internetu (opcjonalne)

**Kopia poza domem (S3 / Backblaze B2 / MinIO).** Gdy ją skonfigurujesz, program
wysyła kopię do Twojego własnego kubełka w wybranej przez Ciebie usłudze. Dane są
szyfrowane na Twoim komputerze (AES-256-GCM) osobnym hasłem, zanim opuszczą komputer;
usługa widzi tylko zaszyfrowane fragmenty o losowo wyglądających nazwach. Obok nich
program zapisuje w kubełku jawną instrukcję odzyskiwania i skrypt — bez Twoich danych.
Dane dostępowe do usługi przechowuje Menedżer poświadczeń Windows. Wydawca nie otrzymuje
tych danych; przetwarzanie przez dostawcę usługi reguluje jego polityka prywatności.

**Znaczniki czasu Sigelith** (dawniej BeatTime). Gdy włączysz tę opcję, po każdej
kopii program wysyła do usługi Sigelith (https://sigelith.org) skrót SHA-256 spisu
plików danej wersji — 64 znaki, z których nie da się odtworzyć nazw ani treści
plików. Skrót trafia do publicznego rejestru usługi; na tym polega dowód, że wersja
istniała w danej chwili. Usługę prowadzi ten sam wydawca; jak przy każdym połączeniu
internetowym widzi on adres IP komputera. Szczegóły, podstawy prawne i okresy
przechowywania: polityka prywatności Sigelith — https://sigelith.org/privacy/
(wiążący oryginał po niemiecku: https://sigelith.org/de/datenschutz/).

Żadna inna funkcja programu nie łączy się z internetem.

### Twoje prawa

W zakresie danych, które trafiają do wydawcy (wyłącznie przy znacznikach czasu
Sigelith), przysługują Ci prawa z RODO — m.in. dostęp, sprostowanie, usunięcie,
ograniczenie przetwarzania i sprzeciw — oraz prawo skargi do organu nadzorczego.
Opisuje je polityka prywatności Sigelith (adres wyżej). Kontakt: kontakt@advena-partners.com.

Tę politykę znajdziesz też w programie: O programie → „Polityka prywatności…”.

---

## English

**In short:** the program does not collect any data about you. There is no account,
no ads and no telemetry. Backups are created on your computer and on the drives you
choose. Only two features connect to the internet, and only if you turn them on.

### Controller

Adam Koch, Weißensteinstr. 44, 58093 Hagen, Germany ·
e-mail: kontakt@advena-partners.com · legal notice (Impressum):
https://sigelith.org/de/impressum/

### What the program processes on your computer

* Files from the folders you choose to back up — it reads them and writes their copies
  to the location you choose (for example an external drive).
* Settings, backup templates and operation history — in the program's data folder on
  your computer.
* An activity log (including paths of backed-up folders and error messages) — stored
  locally for troubleshooting. It is never sent anywhere.
* Backup passwords — only if you choose to remember them; they are kept by the Windows
  Credential Manager, never in the program's files.
* Sigelith evidence — only if you turn on "Protect Sigelith evidence": the program reads,
  on your computer, the Sigelith Desktop stamp history (names, paths and checksums of the
  stamped documents, notes) and copies the Sigelith data folder and the stamped documents
  into your backup. It sends nothing and changes nothing in the Sigelith folder.

The publisher has no access to any of this information.

**Deleting data.** Windows removes the settings, templates and log of the Store version
together with the program. Remembered passwords stay in the Windows Credential Manager
until you delete them: in the program (Settings → "Delete remembered passwords…") or in
Control Panel → Credential Manager. Backups on your drives and in your S3 service belong
to you — the program does not delete them.

### Features that use the internet (optional)

**Off-site copy (S3 / Backblaze B2 / MinIO).** When you configure it, the program sends
a backup to your own bucket in the service you choose. Data is encrypted on your
computer (AES-256-GCM) with a separate password before it leaves the computer; the
service only sees encrypted pieces with random-looking names. Next to them, the program
stores a plain-text recovery note and script in the bucket — without any of your data.
The service credentials are kept by the Windows Credential Manager. The publisher does
not receive this data; the service provider's own privacy policy governs its processing.

**Sigelith timestamps** (formerly BeatTime). When you turn this option on, after each
backup the program sends a SHA-256 digest of that version's file list to the Sigelith
service (https://sigelith.org) — 64 characters from which neither file names nor
contents can be recovered. The digest is added to the service's public log; that is
what proves the version existed at a given moment. The service is run by the same
publisher; as with any internet connection, it sees your computer's IP address.
Details, legal bases and retention periods: the Sigelith privacy policy —
https://sigelith.org/privacy/ (binding German original: https://sigelith.org/de/datenschutz/).

No other feature of the program connects to the internet.

### Your rights

For the data that reaches the publisher (only with Sigelith timestamps) you have the
rights under the GDPR — including access, rectification, erasure, restriction and
objection — and the right to lodge a complaint with a supervisory authority. They are
described in the Sigelith privacy policy (address above). Contact: kontakt@advena-partners.com.

This privacy policy is also available in the program: About → "Privacy policy…".
