"""Testy trwałego stanu: atomowość, odporność na uszkodzenia, migracja z 1.x."""

from __future__ import annotations

import os

import msgpack
import pytest

from cleanvault.state import STATE_MAGIC, StateStore, Template


@pytest.fixture()
def store(tmp_path) -> StateStore:
    return StateStore(tmp_path / "state.msgpack")


def test_starts_from_defaults_when_no_file(tmp_path):
    store = StateStore(tmp_path / "brak.msgpack")
    assert store.templates() == {}
    assert store.setting("theme") == "dark"


def test_template_roundtrip(store):
    template = Template(name="Dokumenty", sources=["C:/Dane"], destination="E:/Kopia")
    store.put_template(template)

    reloaded = StateStore(store.path)
    assert reloaded.get_template(template.id).name == "Dokumenty"
    assert reloaded.get_template(template.id).sources == ["C:/Dane"]


def test_save_is_atomic_and_keeps_backup(store):
    store.put_template(Template(name="Pierwszy"))
    store.put_template(Template(name="Drugi"))

    assert store.backup_path.exists(), "poprzedni stan musi zostać zachowany jako .bak"
    assert not store.path.with_name(store.path.name + ".tmp").exists(), "plik tymczasowy nieposprzątany"


def test_truncated_state_is_detected_and_recovered(store):
    """1.x wywalało się przy starcie na obciętym pliku, tracąc wszystkie szablony."""
    store.put_template(Template(name="Ważny szablon"))
    store.put_template(Template(name="Drugi"))  # tworzy .bak z poprzednim stanem

    blob = store.path.read_bytes()
    tmp = store.path.with_name("uszkodzony.tmp")
    tmp.write_bytes(blob[: len(blob) // 2])
    os.replace(tmp, store.path)

    recovered = StateStore(store.path)
    names = {t.name for t in recovered.templates().values()}

    assert "Ważny szablon" in names, "odzyskanie z kopii .bak nie zadziałało"
    assert list(store.path.parent.glob("*.corrupt-*")), "uszkodzony plik nie został odłożony na bok"


def test_bitflip_is_caught_by_checksum(store):
    store.put_template(Template(name="A"))
    store.put_template(Template(name="B"))

    blob = bytearray(store.path.read_bytes())
    blob[-5] ^= 0xFF
    tmp = store.path.with_name("x.tmp")
    tmp.write_bytes(bytes(blob))
    os.replace(tmp, store.path)

    recovered = StateStore(store.path)
    assert "A" in {t.name for t in recovered.templates().values()}


def test_envelope_has_magic_and_checksum(store):
    store.put_template(Template(name="A"))
    blob = store.path.read_bytes()
    assert blob[:4] == STATE_MAGIC
    assert len(blob) > 4 + 1 + 32


def test_missing_sections_do_not_crash(tmp_path):
    """Regresja: backend.py robił data["files"] i wywalał się na niepełnym pliku."""
    path = tmp_path / "niepelny.msgpack"
    path.write_bytes(msgpack.packb({"version": 2}, use_bin_type=True))

    store = StateStore(path)
    assert store.templates() == {}
    assert store.history() == []
    assert store.setting("theme") == "dark"


def test_garbage_file_falls_back_to_defaults(tmp_path):
    path = tmp_path / "smieci.msgpack"
    path.write_bytes(os.urandom(500))
    store = StateStore(path)
    assert store.templates() == {}


# ------------------------------------------------------------- migracja z 1.x


def _legacy_blob() -> bytes:
    """Dokładny układ zapisywany przez backend.py w wersji 1.x."""
    return msgpack.packb(
        {
            "files": {"C:/Users/U/Desktop/zrzut1.png": {}},
            "settings": {
                "1749998424": {
                    "name": "Szablon z 1749998424",
                    "source": ["C:/Users/U/Downloads/projekt"],  # klucz w liczbie pojedynczej!
                    "destination": "C:/Users/U/Desktop",
                    "created": "1749998424",
                    "encrypt": True,
                    "auto_structure": True,
                    "use_template": True,
                    "password": "tajne-haslo-jawnym-tekstem",
                }
            },
        },
        use_bin_type=True,
    )


def test_legacy_template_is_migrated(tmp_path):
    """W 1.x szablon zapisywał "source", a odczyt szukał "sources" — przez co
    ponowienie kopii z szablonu kończyło się błędem 'sources' za każdym razem."""
    path = tmp_path / "vault_state.msgpack"
    path.write_bytes(_legacy_blob())

    store = StateStore(path)
    templates = list(store.templates().values())

    assert len(templates) == 1
    assert templates[0].sources == ["C:/Users/U/Downloads/projekt"]
    assert templates[0].destination == "C:/Users/U/Desktop"
    assert templates[0].structure == "dated"


def test_legacy_plaintext_password_is_dropped(tmp_path):
    """Hasło zapisane jawnie w 1.x nie może przetrwać migracji."""
    path = tmp_path / "vault_state.msgpack"
    path.write_bytes(_legacy_blob())

    store = StateStore(path)
    store.save()

    template = next(iter(store.templates().values()))
    assert not hasattr(template, "password")
    assert b"tajne-haslo-jawnym-tekstem" not in path.read_bytes()


def test_unknown_fields_are_ignored(tmp_path):
    template = Template.from_dict({"name": "X", "sources": ["a"], "cos_nowego": 42})
    assert template.name == "X"
    assert template.sources == ["a"]


def test_history_is_capped(store):
    for i in range(StateStore.MAX_HISTORY + 40):
        store.add_history({"action": "backup", "n": i})
    assert len(store.data["history"]) == StateStore.MAX_HISTORY
    assert store.history(1)[0]["n"] == StateStore.MAX_HISTORY + 39


def test_delete_template(store):
    template = store.put_template(Template(name="Do usunięcia"))
    assert store.delete_template(template.id)
    assert not store.delete_template(template.id)
    assert store.templates() == {}
