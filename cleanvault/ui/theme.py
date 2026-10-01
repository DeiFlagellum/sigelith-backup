"""Motyw graficzny aplikacji.

Wersja 1.x ustawiała kilkanaście kolorów przez ``QPalette`` i na tym kończyła —
kontrolki miały domyślny wygląd systemowy, bez odstępów, hierarchii i stanów
hover/focus. Tutaj definiujemy spójny zestaw tokenów kolorystycznych i generujemy
z nich arkusz stylów, dzięki czemu motyw jasny i ciemny różnią się wyłącznie
wartościami tokenów, a nie osobnym kodem.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    bg: str
    surface: str
    surface_alt: str
    border: str
    border_strong: str
    text: str
    muted: str
    accent: str
    accent_text: str
    accent_hover: str
    success: str
    warning: str
    danger: str
    shadow: str


DARK = Palette(
    bg="#14161a",
    surface="#1c1f26",
    surface_alt="#242832",
    border="#2f3540",
    border_strong="#3d4553",
    text="#e7e9ee",
    muted="#98a1b0",
    accent="#f59e0b",
    accent_text="#1a1206",
    accent_hover="#fbbf24",
    success="#34d399",
    warning="#fbbf24",
    danger="#f87171",
    shadow="rgba(0,0,0,0.45)",
)

LIGHT = Palette(
    bg="#f3f5f8",
    surface="#ffffff",
    surface_alt="#eef1f6",
    border="#d9dee7",
    border_strong="#bcc4d1",
    text="#161a21",
    muted="#5c6674",
    accent="#b45309",
    accent_text="#ffffff",
    accent_hover="#92400e",
    success="#047857",
    warning="#b45309",
    danger="#b91c1c",
    shadow="rgba(15,23,42,0.12)",
)


def palette_for(theme: str, accent: str | None = None) -> Palette:
    base = LIGHT if theme == "light" else DARK
    if accent:
        hover = accent if theme == "light" else _lighten(accent)
        base = Palette(**{**base.__dict__, "accent": accent, "accent_hover": hover})
    return base


def _lighten(hex_color: str, factor: float = 0.18) -> str:
    try:
        value = hex_color.lstrip("#")
        rgb = tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))
    except (ValueError, IndexError):
        return hex_color
    mixed = tuple(min(255, int(channel + (255 - channel) * factor)) for channel in rgb)
    return "#{:02x}{:02x}{:02x}".format(*mixed)


def build_stylesheet(theme: str = "dark", accent: str | None = None) -> str:
    p = palette_for(theme, accent)
    return f"""
* {{
    font-family: "Segoe UI", "Inter", "Noto Sans", sans-serif;
    font-size: 13px;
}}
QWidget {{
    background: {p.bg};
    color: {p.text};
}}
/* Etykiety i pola wyboru muszą być przezroczyste — inaczej rysują prostokąt
   w kolorze tła okna na tle karty, która ma kolor jaśniejszy. */
QLabel, QCheckBox, QRadioButton, QButtonGroup {{
    background: transparent;
}}
QToolTip {{
    background: {p.surface_alt};
    color: {p.text};
    border: 1px solid {p.border_strong};
    border-radius: 6px;
    padding: 7px 10px;
}}

/* ----------------------------------------------------------- nawigacja */
#Sidebar {{
    background: {p.surface};
    border-right: 1px solid {p.border};
}}
#SidebarTitle {{
    font-size: 17px;
    font-weight: 700;
    color: {p.text};
    padding: 2px 0 0 0;
}}
#SidebarSubtitle {{
    font-size: 11px;
    color: {p.muted};
    padding-bottom: 4px;
}}
#NavButton {{
    text-align: left;
    padding: 10px 14px;
    border: none;
    border-radius: 9px;
    background: transparent;
    color: {p.muted};
    font-size: 13.5px;
    font-weight: 500;
}}
#NavButton:hover {{
    background: {p.surface_alt};
    color: {p.text};
}}
#NavButton:checked {{
    background: {p.accent};
    color: {p.accent_text};
    font-weight: 600;
}}

/* --------------------------------------------------------------- karty */
#Card {{
    background: {p.surface};
    border: 1px solid {p.border};
    border-radius: 12px;
}}
#CardTitle {{
    font-size: 14.5px;
    font-weight: 600;
    color: {p.text};
}}
#CardSubtitle {{
    font-size: 11.5px;
    color: {p.muted};
}}
#PageTitle {{
    font-size: 21px;
    font-weight: 700;
}}
#PageSubtitle {{
    font-size: 12.5px;
    color: {p.muted};
}}
#Hint {{
    background: {p.surface_alt};
    border: 1px solid {p.border};
    border-left: 3px solid {p.accent};
    border-radius: 8px;
    padding: 9px 12px;
    color: {p.muted};
    font-size: 12px;
}}
#FieldHelp {{
    color: {p.muted};
    font-size: 11.5px;
}}
#Muted {{ color: {p.muted}; }}
#Success {{ color: {p.success}; font-weight: 600; }}
#Warning {{ color: {p.warning}; font-weight: 600; }}
#Danger  {{ color: {p.danger}; font-weight: 600; }}
#StatValue {{ font-size: 19px; font-weight: 700; }}
#StatLabel {{ font-size: 11px; color: {p.muted}; }}

/* ------------------------------------------------------------ przyciski */
QPushButton {{
    background: {p.surface_alt};
    color: {p.text};
    border: 1px solid {p.border_strong};
    border-radius: 8px;
    padding: 8px 15px;
    font-weight: 500;
}}
QPushButton:hover  {{ border-color: {p.accent}; }}
QPushButton:pressed {{ background: {p.border}; }}
QPushButton:disabled {{
    color: {p.muted};
    background: {p.surface};
    border-color: {p.border};
}}
QPushButton#Primary {{
    background: {p.accent};
    color: {p.accent_text};
    border: none;
    font-weight: 600;
    padding: 11px 22px;
    font-size: 13.5px;
}}
QPushButton#Primary:hover {{ background: {p.accent_hover}; }}
QPushButton#Primary:disabled {{
    background: {p.surface_alt};
    color: {p.muted};
}}
QPushButton#Danger {{ border-color: {p.danger}; color: {p.danger}; }}
QPushButton#Danger:hover {{ background: {p.danger}; color: #ffffff; }}
QPushButton#Ghost {{
    background: transparent;
    border: 1px solid {p.border};
}}
QPushButton#Link {{
    background: transparent;
    border: none;
    color: {p.accent};
    text-decoration: underline;
    padding: 2px 4px;
}}

/* --------------------------------------------------------------- pola */
QLineEdit, QSpinBox, QComboBox, QPlainTextEdit, QTextEdit {{
    background: {p.surface_alt};
    border: 1px solid {p.border_strong};
    border-radius: 8px;
    padding: 8px 11px;
    color: {p.text};
    selection-background-color: {p.accent};
    selection-color: {p.accent_text};
}}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QPlainTextEdit:focus {{
    border-color: {p.accent};
}}
QLineEdit:disabled, QSpinBox:disabled, QComboBox:disabled {{
    color: {p.muted};
    background: {p.surface};
}}
QLineEdit[readOnly="true"] {{ background: {p.surface}; }}
QComboBox::drop-down {{ border: none; width: 22px; }}
QComboBox QAbstractItemView {{
    background: {p.surface_alt};
    border: 1px solid {p.border_strong};
    border-radius: 8px;
    selection-background-color: {p.accent};
    selection-color: {p.accent_text};
    padding: 4px;
}}

/* ------------------------------------------------------------- listy */
QListWidget, QTreeWidget, QTableWidget {{
    background: {p.surface_alt};
    border: 1px solid {p.border};
    border-radius: 9px;
    padding: 4px;
    outline: none;
}}
QListWidget::item, QTreeWidget::item {{
    padding: 7px 9px;
    border-radius: 6px;
}}
QListWidget::item:hover, QTreeWidget::item:hover {{ background: {p.border}; }}
QListWidget::item:selected, QTreeWidget::item:selected {{
    background: {p.accent};
    color: {p.accent_text};
}}
QHeaderView::section {{
    background: {p.surface};
    color: {p.muted};
    border: none;
    border-bottom: 1px solid {p.border};
    padding: 7px 9px;
    font-weight: 600;
}}

/* --------------------------------------------------- pola wyboru itp. */
QCheckBox, QRadioButton {{ spacing: 9px; padding: 3px 0; }}
QCheckBox::indicator, QRadioButton::indicator {{
    width: 17px; height: 17px;
    border: 1px solid {p.border_strong};
    background: {p.surface_alt};
}}
QCheckBox::indicator {{ border-radius: 5px; }}
QRadioButton::indicator {{ border-radius: 9px; }}
QCheckBox::indicator:hover, QRadioButton::indicator:hover {{ border-color: {p.accent}; }}
QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
    background: {p.accent};
    border-color: {p.accent};
}}
QCheckBox:disabled, QRadioButton:disabled {{ color: {p.muted}; }}

/* --------------------------------------------------------- pasek postępu */
QProgressBar {{
    background: {p.surface_alt};
    border: none;
    border-radius: 7px;
    height: 14px;
    text-align: center;
    color: {p.text};
    font-size: 11px;
}}
QProgressBar::chunk {{
    background: {p.accent};
    border-radius: 7px;
}}

/* ------------------------------------------------------------ przewijanie */
QScrollArea {{ border: none; background: transparent; }}
QScrollBar:vertical {{
    background: transparent; width: 11px; margin: 2px;
}}
QScrollBar::handle:vertical {{
    background: {p.border_strong};
    border-radius: 5px;
    min-height: 28px;
}}
QScrollBar::handle:vertical:hover {{ background: {p.accent}; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; width: 0; }}
QScrollBar::add-page, QScrollBar::sub-page {{ background: transparent; }}
QScrollBar:horizontal {{ background: transparent; height: 11px; margin: 2px; }}
QScrollBar::handle:horizontal {{
    background: {p.border_strong}; border-radius: 5px; min-width: 28px;
}}

/* ----------------------------------------------------------- separatory */
QFrame[frameShape="4"], QFrame[frameShape="5"] {{
    background: {p.border};
    border: none;
    max-height: 1px;
}}
#StatusBar {{
    background: {p.surface};
    border-top: 1px solid {p.border};
    color: {p.muted};
}}
QSplitter::handle {{ background: {p.border}; }}
"""
