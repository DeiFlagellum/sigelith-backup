"""Motyw graficzny aplikacji.

Wersja 1.x ustawiała kilkanaście kolorów przez ``QPalette`` i na tym kończyła —
kontrolki miały domyślny wygląd systemowy, bez odstępów, hierarchii i stanów
hover/focus. Tutaj definiujemy spójny zestaw tokenów kolorystycznych i generujemy
z nich arkusz stylów, dzięki czemu motyw jasny i ciemny różnią się wyłącznie
wartościami tokenów, a nie osobnym kodem.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from cleanvault import i18n

#: Czcionki Windows dla pism, których Segoe UI nie ma — te same co w Sigelith Desktop
#: (``ui/theme.py``, ``SCRIPT_FAMILIES``). Stoją ZA Segoe UI: łacinka (nazwy, @beat)
#: zostaje w niej, a dopiero znaki spoza niej biorą następną rodzinę. Bez tego Qt
#: dobiera czcionkę sam i japoński tekst bywa rysowany chińskimi kształtami ideogramów.
SCRIPT_FAMILIES = {
    "ja": ("Yu Gothic UI", "Meiryo UI", "Meiryo"),
    "ko": ("Malgun Gothic",),
    "zh": ("Microsoft YaHei UI", "Microsoft YaHei"),
}


def font_stack(language: str | None = None) -> str:
    """Lista czcionek do arkusza stylów dla języka (domyślnie bieżącego)."""
    names = ["Segoe UI", *SCRIPT_FAMILIES.get(language or i18n.language(), ()), "Inter", "Noto Sans"]
    return ", ".join(f'"{name}"' for name in names) + ", sans-serif"

#: Akcent marki Sigelith — ten sam co w Sigelith Desktop (``ui/theme.py``, ``ACCENT``),
#: na certyfikacie i na stronie. Domyślny kolor wyróżnienia; w ustawieniach można wybrać inny.
BRAND_ACCENT = "#ff5c39"
#: Dawny domyślny akcent (bursztyn). Kto go sam nie zmieniał, dostaje akcent marki.
LEGACY_DEFAULT_ACCENT = "#f59e0b"


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
    #: akcent jako kolor TEKSTU (linki) — sam akcent ma na jasnym tle za mały kontrast
    accent_ink: str
    #: tło zaznaczenia na listach i w polach: delikatny odcień akcentu, tekst zostaje zwykły
    selection: str
    #: chłodny kolor „na żywo” z Sigelith Desktop (cyjan) — drugi koniec paska postępu
    signal: str
    success: str
    warning: str
    danger: str
    shadow: str


# Wartości z motywu Sigelith Desktop — obie aplikacje mają wyglądać jak jedna marka.
DARK = Palette(
    bg="#090d14",
    surface="#101724",
    surface_alt="#141d2d",
    border="#212d43",
    border_strong="#33425d",
    text="#e8edf5",
    muted="#9aa7bc",
    accent=BRAND_ACCENT,
    accent_text="#ffffff",
    accent_hover="#ff7a5c",
    accent_ink="#ff8a6c",
    selection="#2b1f2a",
    signal="#3ccfff",
    success="#3ddc97",
    warning="#f4b94d",
    danger="#ff6b6b",
    shadow="rgba(0,0,0,0.45)",
)

LIGHT = Palette(
    bg="#f2f4f8",
    surface="#ffffff",
    surface_alt="#f6f8fb",
    border="#dde3ec",
    border_strong="#c2cbd9",
    text="#0f1624",
    muted="#53607a",
    accent=BRAND_ACCENT,
    accent_text="#ffffff",
    accent_hover="#ff7654",
    accent_ink="#c43d1c",
    selection="#ffe6dc",
    signal="#0b87a8",
    success="#12805a",
    warning="#a05a00",
    danger="#c62828",
    shadow="rgba(15,23,42,0.12)",
)


def effective_accent(stored: str | None) -> str:
    """Akcent z ustawień; brak albo dawny domyślny bursztyn → akcent marki."""
    if not stored or stored.lower() == LEGACY_DEFAULT_ACCENT:
        return BRAND_ACCENT
    return stored


def palette_for(theme: str, accent: str | None = None) -> Palette:
    base = LIGHT if theme == "light" else DARK
    accent = effective_accent(accent)
    if accent.lower() == BRAND_ACCENT:
        return base
    # Własny kolor użytkownika: odcienie liczymy z niego tak, żeby tekst dało się czytać.
    light = theme == "light"
    return replace(
        base,
        accent=accent,
        accent_hover=_lighten(accent, 0.12),
        accent_text=_text_on(accent),
        accent_ink=_darken(accent, 0.3) if light else _lighten(accent, 0.3),
        selection=_mix(accent, base.surface, 0.2),
    )


def _rgb(hex_color: str) -> tuple[int, int, int] | None:
    try:
        value = hex_color.lstrip("#")
        return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)
    except (ValueError, IndexError):
        return None


def _hex(rgb) -> str:
    return "#{:02x}{:02x}{:02x}".format(*(max(0, min(255, round(c))) for c in rgb))


def _lighten(hex_color: str, factor: float = 0.18) -> str:
    rgb = _rgb(hex_color)
    return _hex(c + (255 - c) * factor for c in rgb) if rgb else hex_color


def _darken(hex_color: str, factor: float) -> str:
    rgb = _rgb(hex_color)
    return _hex(c * (1 - factor) for c in rgb) if rgb else hex_color


def _mix(hex_color: str, base: str, share: float) -> str:
    a, b = _rgb(hex_color), _rgb(base)
    return _hex(x * share + y * (1 - share) for x, y in zip(a, b, strict=True)) if a and b else base


def _text_on(hex_color: str) -> str:
    """Biały albo ciemny tekst na tle akcentu — jak w Desktopie biały, chyba że tło jest jasne."""
    rgb = _rgb(hex_color)
    if not rgb:
        return "#ffffff"
    linear = [(c / 255) / 12.92 if c <= 10 else ((c / 255 + 0.055) / 1.055) ** 2.4 for c in rgb]
    luminance = 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]
    return "#ffffff" if luminance < 0.35 else "#1a1206"


def build_stylesheet(theme: str = "dark", accent: str | None = None) -> str:
    p = palette_for(theme, accent)
    return f"""
* {{
    font-family: {font_stack()};
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
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {p.accent_hover}, stop:1 {p.accent});
    color: {p.accent_text};
    border: 1px solid {p.accent};
    font-weight: 700;
    padding: 11px 22px;
    font-size: 13.5px;
}}
QPushButton#Primary:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 {_lighten(p.accent_hover, 0.12)}, stop:1 {p.accent_hover});
    border-color: {p.accent_hover};
}}
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
    color: {p.accent_ink};
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
    selection-background-color: {p.selection};
    selection-color: {p.text};
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
    background: {p.selection};
    color: {p.text};
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
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {p.accent}, stop:1 {p.signal});
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
