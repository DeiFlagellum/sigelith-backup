"""„Przekaż…” — wersja pliku z kopii do Sigelith Handover (Sigelith Desktop 3.0.1+).

Most jest prosty i dlatego łatwo go zepsuć: alias ``sigelith-desktop.exe``
z parametrem ``--handover`` i ścieżką pliku. Bez Desktopu (albo ze starszym,
bez aliasu) program nic nie uruchamia i mówi, skąd go wziąć.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from cleanvault import sigelith


def test_launches_the_desktop_alias_with_the_file(monkeypatch, tmp_path):
    started = []
    monkeypatch.setattr(sigelith.os, "name", "nt")
    monkeypatch.setattr(sigelith.shutil, "which",
                        lambda name: rf"C:\Users\x\AppData\Local\Microsoft\WindowsApps\{name}")
    monkeypatch.setattr(sigelith.subprocess, "Popen", lambda args, **kwargs: started.append(args))
    target = tmp_path / "umowa z marca.pdf"
    assert sigelith.hand_over(target)
    assert started == [[r"C:\Users\x\AppData\Local\Microsoft\WindowsApps\sigelith-desktop.exe",
                        "--handover", str(target)]]


def test_without_the_alias_nothing_is_started(monkeypatch, tmp_path):
    started = []
    monkeypatch.setattr(sigelith.shutil, "which", lambda name: None)
    monkeypatch.setattr(sigelith.subprocess, "Popen", lambda args, **kwargs: started.append(args))
    assert sigelith.desktop_launcher() is None
    assert not sigelith.hand_over(tmp_path / "plik.txt")
    assert started == []


def test_alias_and_flag_match_sigelith_desktop():
    """Te same nazwy co w manifeście i w wierszu poleceń Sigelith Desktop (repo beattime)."""
    repo = Path(os.environ.get("SIGELITH_REPO", Path(__file__).resolve().parents[2] / "beattime"))
    desktop = repo / "desktop"
    if not desktop.is_dir():
        pytest.skip("repozytorium Sigelith (Desktop) nie lezy obok tego repozytorium")
    manifest = (desktop / "packaging" / "AppxManifest.xml").read_text(encoding="utf-8")
    assert f'Alias="{sigelith.DESKTOP_ALIAS}"' in manifest
    instance = (desktop / "beatstamp" / "instance.py").read_text(encoding="utf-8")
    assert f"HANDOVER_FLAG = '{sigelith.HANDOVER_FLAG}'" in instance


@pytest.mark.skipif(os.name != "nt", reason="Windows")
def test_real_lookup_does_not_crash():
    launcher = sigelith.desktop_launcher()
    assert launcher is None or launcher.lower().endswith("sigelith-desktop.exe")
