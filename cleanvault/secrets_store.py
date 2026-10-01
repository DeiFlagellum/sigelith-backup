"""Opcjonalne zapamiętywanie haseł w magazynie systemowym.

Wersja 1.x zapisywała hasło do kopii **otwartym tekstem** w pliku stanu
(``vault_state.msgpack``), obok listy plików. Hasło leżące jawnie obok
zaszyfrowanych danych unieważnia całe szyfrowanie.

Tutaj hasło trafia wyłącznie do magazynu systemowego — w Windows jest to
Menedżer poświadczeń (DPAPI, klucz związany z kontem użytkownika). Jeśli
``keyring`` nie ma bezpiecznego backendu, **odmawiamy zapisu** zamiast po cichu
degradować się do pliku tekstowego; biblioteka ``keyrings.alt`` potrafi taki
zapis wykonać i właśnie tego chcemy uniknąć.
"""

from __future__ import annotations

from .i18n import tr
from .log import get_logger

log = get_logger("secrets")

#: Nazwa usługi w Menedżerze poświadczeń Windows. **Nie zmieniamy jej przy
#: zmianie nazwy produktu** — pod tą nazwą leżą hasła już zapisane przez
#: użytkowników i zmiana odcięłaby ich od własnych kopii.
SERVICE_NAME = "TVS CleanVault"

#: Backendy, które trzymają sekrety w postaci jawnej lub słabo zaszyfrowanej.
_INSECURE_BACKENDS = {
    "keyrings.alt.file.PlaintextKeyring",
    "keyrings.alt.file.EncryptedKeyring",
    "keyrings.alt.file.UncryptedFileKeyring",
    "keyring.backends.fail.Keyring",
    "keyring.backends.null.Keyring",
}

try:
    import keyring as _keyring

    KEYRING_AVAILABLE = True
except ImportError:  # pragma: no cover
    _keyring = None
    KEYRING_AVAILABLE = False


def backend_name() -> str:
    if not KEYRING_AVAILABLE:
        return tr("brak (biblioteka keyring niezainstalowana)")
    backend = _keyring.get_keyring()
    return f"{type(backend).__module__}.{type(backend).__name__}"


def is_available() -> bool:
    """Czy da się bezpiecznie zapisać hasło w magazynie systemowym."""
    if not KEYRING_AVAILABLE:
        return False
    try:
        name = backend_name()
    except Exception as exc:  # noqa: BLE001
        log.warning("Nie udało się ustalić backendu keyring: %s", exc)
        return False
    if name in _INSECURE_BACKENDS:
        log.warning("Backend keyring %s nie jest bezpieczny — zapamiętywanie haseł wyłączone.", name)
        return False
    return True


def describe() -> str:
    """Krótki opis magazynu do pokazania w ustawieniach."""
    if not KEYRING_AVAILABLE:
        return tr("Niedostępny — brak biblioteki keyring.")
    if not is_available():
        return tr("Niedostępny — backend {backend} nie gwarantuje poufności.").format(
            backend=backend_name()
        )
    name = backend_name()
    if "Windows" in name or "WinVault" in name:
        return tr("Menedżer poświadczeń Windows (DPAPI, powiązany z kontem użytkownika).")
    return tr("Magazyn systemowy: {backend}").format(backend=name)


def save_password(template_id: str, password: str) -> bool:
    if not is_available() or not password:
        return False
    try:
        _keyring.set_password(SERVICE_NAME, template_id, password)
        log.info("Hasło szablonu %s zapisane w magazynie systemowym.", template_id)
        return True
    except Exception as exc:  # noqa: BLE001
        log.error("Nie udało się zapisać hasła w magazynie systemowym: %s", exc)
        return False


def load_password(template_id: str) -> str | None:
    if not is_available():
        return None
    try:
        return _keyring.get_password(SERVICE_NAME, template_id)
    except Exception as exc:  # noqa: BLE001
        log.error("Nie udało się odczytać hasła z magazynu systemowego: %s", exc)
        return None


def delete_password(template_id: str) -> bool:
    if not KEYRING_AVAILABLE:
        return False
    try:
        _keyring.delete_password(SERVICE_NAME, template_id)
        log.info("Hasło szablonu %s usunięte z magazynu systemowego.", template_id)
        return True
    except Exception:  # noqa: BLE001 - brak wpisu to nie błąd
        return False
