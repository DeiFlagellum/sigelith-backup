# Pakiet MSIX i zgłoszenie do Microsoft Store

Instrukcja dla wydawcy. Karta w Sklepie (11 języków, CSV dla Partner Center) i zgłoszenie
krok po kroku leżą w [`packaging/store/`](../store/README.md) ([`PUBLIKACJA.md`](../store/PUBLIKACJA.md)),
polityka prywatności w [`assets/legal/polityka-prywatnosci.md`](../../assets/legal/polityka-prywatnosci.md).

## Wymagania

* Windows 10 22H2 (19045) lub Windows 11 — tyle deklaruje pakiet.
* Windows SDK (narzędzia `makeappx`, `makepri`, `signtool`; skrypt sam wybiera
  najnowszą wersję z `C:\Program Files (x86)\Windows Kits\10\bin`).
* Środowisko Pythona z `requirements.txt` i PyInstallerem (`pip install pyinstaller`).

## Budowanie

```powershell
.venv\Scripts\python tools\build_msix.py
```

Skrypt buduje program w trybie katalogu (`TVB_ONEDIR=1`), rysuje od zera kafelki
i ikony we wszystkich rozmiarach (`tools/make_icon.py`), wypełnia manifest
z [`AppxManifest.xml`](AppxManifest.xml), indeksuje grafiki (`resources.pri`)
i pakuje wszystko do `dist\SigelithBackup_<wersja>_x64.msix` (ok. 54 MB).
Wersja pakietu pochodzi z `cleanvault.__version__` (`2.0.0` → `2.0.0.0`).

Wydawca i jego `CN` są wpisane na stałe — to wartości konta Partner Center (firmowe,
Adam Koch), wspólne dla wszystkich jego produktów, te same co w Sigelith Desktop.
Nazwa pakietu z rezerwacji „Sigelith Backup” (2026-09-30, Store ID `9P403GRSV1TX`)
to `AdamKoch.SigelithBackup` — do Sklepu podaje się ją w `--identity-name`. Bez tego
parametru pakiet ma nazwę testową `AdamKoch.SigelithBackup.Test` i nadaje się tylko
do prób na własnym komputerze.

## Próba na własnym komputerze (bez certyfikatu)

1. Ustawienia Windows → System → Dla deweloperów → **Tryb dewelopera**.
2. `.venv\Scripts\python tools\build_msix.py --register`
   — rejestruje katalog `build\msix\layout` jako zainstalowaną aplikację
   (bez uprawnień administratora). Program pojawia się w menu Start.
3. Usunięcie: `Get-AppxPackage AdamKoch.SigelithBackup.Test | Remove-AppxPackage`.

Zarejestrowany katalog musi zostać na miejscu — program działa wprost z niego.
Przed kolejnym budowaniem zamknij program (także ikonę przy zegarze).

Instalacja samego pliku `.msix` (tak jak u użytkownika) wymaga podpisu
certyfikatem, któremu komputer ufa: `--pfx plik.pfx --pfx-password …`, a certyfikat
testowy trzeba dodać do „Zaufane osoby” komputera lokalnego (to już wymaga
administratora). Do Sklepu podpis nie jest potrzebny.

## Czym wersja ze Sklepu różni się od pliku EXE

| | EXE | Sklep (MSIX) |
|---|---|---|
| Ustawienia, szablony, dziennik | `%LOCALAPPDATA%\Sigelith Backup` (dane spod dawnej nazwy: `Time Vault Backup`, `CleanVault` — program pracuje na nich dalej) | `%LOCALAPPDATA%\Packages\<rodzina pakietu>\LocalState` — zwykły folder, usuwany razem z aplikacją. Przy pierwszym starcie program **kopiuje** stan z wersji EXE, jeśli go znajdzie. |
| Start przy logowaniu | wpis `HKCU\…\Run` | zadanie startowe pakietu (`windows.startupTask`, parametr `--background`), włączane z programu przez API `StartupTask`. Wyłączone w Ustawieniach Windows → Aplikacje → Uruchamianie da się włączyć tylko tam — program o tym informuje. |
| Aktualizacje | ręcznie | przez Sklep |
| Przywracanie do AppData | bez ograniczeń | nowe foldery tworzone **bezpośrednio** w `AppData\Local` lub `AppData\Roaming` Windows zapisuje w prywatnej kopii pakietu (niewidocznej dla innych programów). Program wykrywa to przed zapisem i pyta. W istniejących podfolderach zapis jest zwykły. |

Zachowanie AppData sprawdzone próbą w zarejestrowanym pakiecie (Windows 11 26200):
nowy folder prosto w `Local` → prywatna kopia; nowy plik i podmiana pliku w istniejącym
podfolderze → prawdziwy zapis; `%TEMP%` i `LocalState` → prawdziwy zapis. Wyłączenie
wirtualizacji (`unvirtualizedResources`) Microsoft przewiduje wyłącznie dla gier
partnerów, więc nie wchodzi w grę.

Pakiet deklaruje jedno uprawnienie: `runFullTrust` (zwykły program desktopowy).
`broadFileSystemAccess` nie jest potrzebne — program z pełnym zaufaniem ma dostęp
do plików jak każdy program użytkownika.

Hasła zapamiętane w Menedżerze poświadczeń Windows zostają tam po odinstalowaniu
(tak działa ten magazyn). Zasada Sklepu 10.2.7 wymaga czystego odinstalowania, więc
program ma w Ustawieniach „Usuń zapamiętane hasła…”, a polityka prywatności to opisuje.

## Licencje i informacje wymagane prawem

Zasada 10.2 Sklepu: program musi zawierać wszystkie informacje wymagane prawem —
tu przede wszystkim licencje składników. W programie (O programie → „Licencje…”
i „Polityka prywatności…”) i w katalogu `assets\legal` pakietu są:

| Plik | Treść |
|---|---|
| `LICENSE.txt` | licencja samego programu |
| `THIRD-PARTY-NOTICES.txt` | wykaz składników z wersjami, prawami autorskimi i tekstami licencji — tworzy go `tools\third_party_notices.py` |
| `LGPL-3.0.txt`, `GPL-3.0.txt` | Qt i PySide6 są na LGPL-3.0, która odwołuje się do GPL-3.0 |
| `PYTHON-LICENSE.txt` | licencja Pythona razem z bibliotekami wbudowanymi w Pythona dla Windows (OpenSSL, libffi, bzip2, xz, zlib, expat…) |
| `polityka-prywatnosci.md` | polityka prywatności — ta sama, którą publikujesz pod adresem w Partner Center |

Budowanie (`cleanvault.spec`, EXE i MSIX) przerywa się, gdy wykaz jest nieaktualny
albo gdy do programu trafia biblioteka, której w nim nie ma. Po zmianie zależności:
`.venv\Scripts\python tools\third_party_notices.py`.

**Qt na LGPL-3.0** — co to oznacza dla programu o zamkniętej licencji:

* biblioteki Qt i PySide6 są niezmienione i ładowane dynamicznie; w pakiecie MSIX to
  osobne pliki, które użytkownik może zastąpić zgodnymi wersjami (wymóg LGPL). Wersja
  jednoplikowa EXE rozpakowuje je dopiero przy starcie — do rozpowszechniania poza
  Sklepem lepiej budować wersję katalogową (`TVB_ONEDIR=1`);
* informacja o LGPL, pełne teksty licencji i adresy kodu źródłowego tych samych wersji
  (download.qt.io) są w programie;
* warunki licencji programu nie mogą zabraniać modyfikowania tych bibliotek ani badania
  programu w tym celu — standardowe warunki Sklepu (Microsoft Standard Application
  License Terms) wprost dopuszczają to, na co pozwalają licencje składników otwartych,
  a `LICENSE.txt` mówi to samo;
* do pakietu nie trafiają moduły Qt, których program nie używa. Szczególnie **Qt Virtual
  Keyboard**, który w wersji otwartej jest wyłącznie na GPL-3.0 — hak PySide6 dołączał
  go razem z QML/Quick; budowanie przerywa się, gdyby wrócił.

## Zgłoszenie do Sklepu (Partner Center)

**Warunki wstępne** (uzgodnione z projektem beattime 2026-09-29):

* ~~**Sigelith Desktop jest w Sklepie przed Sigelith Backup**~~ — *gotowe*: Sigelith Desktop
  opublikowany 2026-10-01 (https://apps.microsoft.com/detail/9n5xk65gtf33). Kreator wersji ze
  Sklepu prowadzi przyciskiem „Poznaj Sigelith Desktop” wyłącznie do jego karty w Sklepie
  (`ms-windows-store://pdp/?productid=9N5XK65GTF33`, zasada 10.1.5).
* ~~**Na sigelith.org są wdrożone**~~ — *gotowe, sprawdzone z zewnątrz 2026-09-29*: akapit
  o programie (wtedy jeszcze Time Vault Backup) w punkcie 9 polityki prywatności (`/privacy/#timevault`,
  `/de/datenschutz/#timevault`), strona `/desktop/` (także `/pl/desktop/`, `/de/desktop/` —
  na nie prowadzi przycisk w wersji EXE) i karta programu na `/apps/#time-vault-backup`.
  Adresy są stałe po obu stronach.

1. ~~**Konto wydawcy**~~ — jest: konto firmowe (*Company*) „Adam Koch”, zweryfikowane
   2026-09-26, to samo co dla Sigelith Desktop.
2. ~~**Rezerwacja nazwy**~~ — zrobiona 2026-09-30: „Sigelith Backup”, Store ID
   `9P403GRSV1TX` (nowy produkt). Rezerwacja wygasa po trzech miesiącach bez publikacji
   (ok. 2026-12-30). Wcześniejsza rezerwacja „Time Vault Backup” (`9PF22FJHLWMK`) — porzucona
   po sprawdzeniu znaków (TIME VAULT: USA 4941750, UE przez IR 1196778), wygaśnie sama.
3. ~~**Tożsamość produktu**~~ — potwierdzona 2026-09-30 (Zarządzanie produktem → Tożsamość
   produktu): `Package/Identity/Name` = `AdamKoch.SigelithBackup`; `Publisher`
   i `PublisherDisplayName` równe wartościom w `tools/build_msix.py`
   (`CN=322BC472-4859-4579-991B-25EE879D3796`, `Adam Koch`). Budowanie:

   ```powershell
   .venv\Scripts\python tools\build_msix.py --identity-name "AdamKoch.SigelithBackup"
   ```

   (z nazwą dokładnie taką, jaką pokaże Product identity — co do znaku).
4. **Pakiety**: prześlij `dist\sklep\SigelithBackup_3.0.0.0_x64.msix` (zbudowany z nazwą
   ze Sklepu i odłożony osobno — `dist\` bez `sklep\` to wersja testowa). Każda kolejna
   wersja musi mieć wyższy numer (`cleanvault/__init__.py` i `pyproject.toml`).
5. **Właściwości**: kategoria *Narzędzia i programy użytkowe* → *Kopie zapasowe
   i zarządzanie*.
   * **Adres polityki prywatności** (zasada 10.5.1): `https://sigelith.org/privacy/` —
     ta sama polityka wydawcy co dla Sigelith Desktop, z wiążącym oryginałem
     `https://sigelith.org/de/datenschutz/`. **Warunek:** punkt 9 („Apps”) na stronie musi
     najpierw opisywać także Sigelith Backup — gotowy tekst (DE i EN) jest
     w `docs/sklep/sigelith-datenschutz-time-vault-backup.md`. Treść w programie
     (`assets/legal/polityka-prywatnosci.md`) odsyła do tej polityki.
   * **Dane kontaktowe wsparcia**: `kontakt@advena-partners.com` i Impressum
     `https://sigelith.org/de/impressum/` (jak w Sigelith Desktop; dla konta firmowego
     Microsoft pokazuje je w karcie produktu — zasada 10.14).
   * **Dodatkowe warunki licencyjne** — zostaw puste: obowiązują wtedy standardowe warunki
     Microsoft, zgodne z `LICENSE.txt` i z LGPL.
   * **Deklaracja „czy produkt przesyła dane osobowe”**: **tak** — przy włączonych
     znacznikach Sigelith do sigelith.org trafia adres IP (dane osobowe w RODO) razem
     ze skrótem; opisuje to polityka Sigelith. Bez reklam i zakupów w aplikacji.
6. **Klasyfikacja wiekowa**: ankieta IARC — program nie zawiera treści
   z pytań ankiety, nie udostępnia komunikacji między użytkownikami ani zakupów.
7. **Strona w Sklepie** (11 języków — tyle deklaruje pakiet): `packaging/store/listing.json`
   wpisywany do eksportu z Partner Center przez `packaging/store/fill_listing_csv.py`; zrzuty
   ekranu (1600×1000) — `tools/store_screenshots.py` robi je we wszystkich językach.
8. **Uwagi dla certyfikacji** i uzasadnienie `runFullTrust` (pola do 500 znaków) — gotowe
   teksty w `packaging/store/PUBLIKACJA.md`.
9. Cena i dostępność — decyzja wydawcy.
