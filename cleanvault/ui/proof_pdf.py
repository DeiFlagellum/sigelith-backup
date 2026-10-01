"""Certyfikat PDF do dowodu czasu pliku z kopii (fileproof.py) — dla człowieka.

Maszyna sprawdza plik ``.sigelith-proof``; kancelaria, biegły czy klient
dostaje obok ten PDF: co dowód potwierdza, czego nie, i jak go sprawdzić bez
tego programu. Dwujęzyczny (PL/EN), bo trafia do ludzi, których języka program
nie zna. Rysowany przez Qt — bez dodatkowej biblioteki PDF w programie.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

from PySide6.QtCore import QMarginsF
from PySide6.QtGui import QFont, QPageLayout, QPageSize, QPdfWriter, QTextDocument

_CSS = """
body { font-family: 'Segoe UI', sans-serif; font-size: 10pt; color: #191c23; }
h1 { font-size: 18pt; margin: 0 0 2pt 0; }
h2 { font-size: 12pt; margin: 12pt 0 4pt 0; }
.sub { color: #5b6170; margin: 0 0 10pt 0; }
td { padding: 3pt 8pt 3pt 0; vertical-align: top; }
td.k { color: #5b6170; white-space: nowrap; }
.mono { font-family: Consolas, 'Courier New', monospace; font-size: 8.5pt; }
.small { color: #5b6170; font-size: 8pt; }
"""


def _row(label: str, value: str, mono: bool = False) -> str:
    css = ' class="mono"' if mono else ""
    return f'<tr><td class="k">{escape(label)}</td><td{css}>{escape(value)}</td></tr>'


def certificate_html(doc: dict, proof_name: str) -> str:
    info, stamp = doc["file"], doc["beatproof"]
    week = str(stamp.get("week") or "")
    moment = " ".join(part for part in (str(stamp.get("utc") or ""), str(stamp.get("beat") or "")) if part)
    rows = [
        _row("Plik / File", str(info.get("name") or "")),
        _row("Ścieżka w kopii / Path in the backup",
             str(info.get("path") or "— (nieujawniona / not disclosed)")),
        _row("Rozmiar / Size", f"{int(info.get('size') or 0):,} B".replace(",", " ")),
        _row("SHA-256", str(info.get("sha256") or ""), mono=True),
        _row("Oznakowano / Sealed", moment),
        _row("Tydzień dziennika / Log week", week),
        _row("Korzeń tygodnia / Week root", str(stamp.get("week_root") or ""), mono=True),
        _row("Pieczęć kopii / Backup seal", str(stamp.get("digest") or ""), mono=True),
        _row("Klucz Sigelith / Sigelith key", str(stamp.get("public_key") or ""), mono=True),
    ]
    return f"""<html><head><style>{_CSS}</style></head><body>
<h1>Dowód czasu · Time proof</h1>
<p class="sub">Sigelith Backup — plik z kopii zapasowej / a file from a backup</p>
<table>{''.join(rows)}</table>
<h2>Co to potwierdza · What this confirms</h2>
<p>Plik o dokładnie tych bajtach (SHA-256 wyżej) był w kopii zapasowej, której pieczęć zapisano
w publicznym dzienniku Sigelith w tygodniu {escape(week)} — istniał najpóźniej w tamtej chwili.
Dowód nie ujawnia żadnych innych plików kopii. Nie mówi, kto plik stworzył ani co oznacza.</p>
<p>A file with exactly these bytes (SHA-256 above) was in a backup whose seal was recorded in the
public Sigelith log in week {escape(week)} — it existed no later than that moment. The proof
reveals no other files of the backup. It does not say who created the file or what it means.</p>
<h2>Jak sprawdzić · How to verify</h2>
<ol>
<li>Sigelith Desktop → „Sprawdzanie” / “Verification”: wczytaj plik dowodu „{escape(proof_name)}”
i sam plik / load the proof file and the file itself.</li>
<li>https://sigelith.org/verify/ — upuść plik dowodu / drop the proof file.</li>
<li>Bez żadnego programu / without any program:
<span class="mono">{escape(str(doc.get("how_to_verify") or ""))}</span></li>
</ol>
<p class="small">{escape(str(doc.get("generator") or ""))} · {escape(str(doc.get("created") or ""))}
· format {escape(str(doc.get("format") or ""))}</p>
</body></html>"""


def write_certificate(doc: dict, target: Path, proof_name: str) -> Path:
    writer = QPdfWriter(str(target))
    writer.setPageLayout(QPageLayout(QPageSize(QPageSize.PageSizeId.A4), QPageLayout.Orientation.Portrait,
                                     QMarginsF(16, 16, 16, 16), QPageLayout.Unit.Millimeter))
    writer.setTitle(f"Dowód czasu — {doc['file'].get('name', '')}")
    writer.setCreator(str(doc.get("generator") or "Sigelith Backup"))
    text = QTextDocument()
    text.setDefaultFont(QFont("Segoe UI", 10))
    text.setHtml(certificate_html(doc, proof_name))
    text.print_(writer)
    return target
