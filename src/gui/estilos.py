"""
NEXUS // CTRL — Sistema de estilos global.
Paleta: Púrpura violeta + Esmeralda sobre gris grafito.
"""

# ─── Paleta de colores ───
BG_DARKEST  = "#0f0f1a"
BG_DARK     = "#1a1a2e"
BG_MEDIUM   = "#16213e"
BG_CARD     = "#252547"
BG_CARD_ALT = "#1e1e3a"
BG_HOVER    = "#2d2d5e"
BG_INPUT    = "#1c1c35"

PRIMARY       = "#A855F7"
PRIMARY_DARK  = "#7C3AED"
PRIMARY_LIGHT = "#C084FC"
SECONDARY     = "#10B981"
SEC_DARK      = "#059669"
ACCENT        = "#6366F1"

TEXT_PRIMARY   = "#E2E8F0"
TEXT_SECONDARY = "#94A3B8"
TEXT_MUTED     = "#64748B"
TEXT_ON_PRIMARY = "#FFFFFF"

BORDER       = "#334155"
BORDER_LIGHT = "#475569"

SUCCESS = "#10B981"
WARNING = "#F59E0B"
ERROR   = "#EF4444"
INFO    = "#3B82F6"

# Colores para estados de proceso
ESTADO_LISTO      = "#10B981"
ESTADO_EJECUTANDO = "#6366F1"
ESTADO_ESPERANDO  = "#F59E0B"
ESTADO_TERMINADO  = "#64748B"
ESTADO_NUEVO      = "#A855F7"

# Colores para procesos en Gantt (paleta de 10 colores distinguibles)
COLORES_PROCESOS = [
    "#A855F7", "#10B981", "#3B82F6", "#F59E0B", "#EF4444",
    "#EC4899", "#14B8A6", "#8B5CF6", "#F97316", "#06B6D4",
]

FONT_FAMILY = "Segoe UI"
FONT_MONO   = "Consolas"


def obtener_stylesheet() -> str:
    """Retorna el QSS global para toda la aplicación."""
    return f"""
    /* ─── Base ─── */
    QMainWindow, QWidget {{
        background-color: {BG_DARK};
        color: {TEXT_PRIMARY};
        font-family: "{FONT_FAMILY}";
        font-size: 13px;
    }}

    /* ─── Labels ─── */
    QLabel {{
        color: {TEXT_PRIMARY};
        background: transparent;
    }}

    /* ─── Botones ─── */
    QPushButton {{
        background-color: {ACCENT};
        color: {TEXT_ON_PRIMARY};
        border: 1px solid {ACCENT};
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 600;
        font-size: 13px;
    }}
    QPushButton:hover {{
        background-color: {PRIMARY_LIGHT};
        border-color: {PRIMARY_LIGHT};
    }}
    QPushButton:pressed {{
        background-color: {PRIMARY_DARK};
    }}
    QPushButton:disabled {{
        background-color: {BG_CARD_ALT};
        color: {TEXT_MUTED};
        border-color: {BORDER};
    }}

    /* Botón primario */
    QPushButton#btn_primario {{
        background-color: {SUCCESS};
        color: {TEXT_ON_PRIMARY};
        border: none;
        font-size: 15px;
        font-weight: bold;
        padding: 14px 30px;
        border-radius: 10px;
    }}
    QPushButton#btn_primario:hover {{
        background-color: {SEC_DARK};
    }}
    QPushButton#btn_primario:pressed {{
        background-color: {SECONDARY};
    }}

    /* Botón secundario (esmeralda) */
    QPushButton#btn_secundario {{
        background-color: {SECONDARY};
        color: {TEXT_ON_PRIMARY};
        border: none;
    }}
    QPushButton#btn_secundario:hover {{
        background-color: {SEC_DARK};
    }}

    /* Botón peligro */
    QPushButton#btn_peligro {{
        background-color: transparent;
        color: {ERROR};
        border: 2px solid {ERROR};
    }}
    QPushButton#btn_peligro:hover {{
        background-color: {ERROR};
        color: white;
    }}

    /* ─── Inputs ─── */
    QLineEdit, QSpinBox, QComboBox {{
        background-color: {BG_INPUT};
        color: {TEXT_PRIMARY};
        border: 2px solid {BORDER_LIGHT};
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 14px;
        selection-background-color: {PRIMARY_DARK};
    }}
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
        border-color: {SUCCESS};
        background-color: {BG_MEDIUM};
    }}

    QSpinBox::up-button, QSpinBox::down-button {{
        width: 0px;
        border: none;
        background: transparent;
    }}

    /* ─── ComboBox ─── */
    QComboBox {{
        background-color: {BG_INPUT};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER};
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 13px;
        min-width: 180px;
    }}
    QComboBox:hover {{
        border-color: {PRIMARY};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {BG_CARD};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER};
        selection-background-color: {PRIMARY_DARK};
        selection-color: white;
        outline: none;
    }}

    /* ─── Slider ─── */
    QSlider::groove:horizontal {{
        border: none;
        height: 6px;
        background: {BORDER};
        border-radius: 3px;
    }}
    QSlider::handle:horizontal {{
        background: {PRIMARY};
        width: 18px;
        height: 18px;
        margin: -6px 0;
        border-radius: 9px;
    }}
    QSlider::handle:horizontal:hover {{
        background: {PRIMARY_LIGHT};
    }}
    QSlider::sub-page:horizontal {{
        background: {PRIMARY_DARK};
        border-radius: 3px;
    }}

    /* ─── TabWidget ─── */
    QTabWidget::pane {{
        border: 1px solid {BORDER};
        border-radius: 0px 0px 8px 8px;
        background-color: {BG_DARK};
        top: -1px;
    }}
    QTabBar::tab {{
        background-color: {BG_CARD};
        color: {TEXT_SECONDARY};
        border: 1px solid {BORDER};
        border-bottom: none;
        padding: 10px 22px;
        margin-right: 2px;
        border-radius: 6px 6px 0 0;
        font-weight: 600;
        font-size: 12px;
    }}
    QTabBar::tab:selected {{
        background-color: {BG_DARK};
        color: {PRIMARY_LIGHT};
        border-bottom: 2px solid {PRIMARY};
    }}
    QTabBar::tab:hover:!selected {{
        background-color: {BG_HOVER};
        color: {TEXT_PRIMARY};
    }}

    /* ─── TableWidget ─── */
    QTableWidget {{
        background-color: {BG_DARKEST};
        alternate-background-color: {BG_CARD_ALT};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER};
        border-radius: 8px;
        gridline-color: {BORDER};
        font-size: 12px;
    }}
    QTableWidget::item {{
        padding: 6px 10px;
        border-bottom: 1px solid {BORDER};
    }}
    QTableWidget::item:selected {{
        background-color: {PRIMARY_DARK};
        color: white;
    }}
    QHeaderView::section {{
        background-color: {BG_CARD};
        color: {TEXT_SECONDARY};
        padding: 8px 10px;
        border: none;
        border-bottom: 2px solid {PRIMARY_DARK};
        font-weight: 700;
        font-size: 11px;
        text-transform: uppercase;
    }}

    /* ─── ScrollBar ─── */
    QScrollBar:vertical {{
        background: {BG_DARKEST};
        width: 10px;
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical {{
        background: {BORDER};
        border-radius: 5px;
        min-height: 30px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {BORDER_LIGHT};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QScrollBar:horizontal {{
        background: {BG_DARKEST};
        height: 10px;
        border-radius: 5px;
    }}
    QScrollBar::handle:horizontal {{
        background: {BORDER};
        border-radius: 5px;
        min-width: 30px;
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}

    /* ─── TextEdit (Logs) ─── */
    QTextEdit {{
        background-color: {BG_DARKEST};
        color: {SECONDARY};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 10px;
        font-family: "{FONT_MONO}";
        font-size: 12px;
    }}

    /* ─── Frames / Cards ─── */
    QFrame#card {{
        background-color: {BG_CARD};
        border: 1px solid {BORDER};
        border-radius: 10px;
    }}
    QFrame#card_metrica {{
        background-color: {BG_CARD};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 10px;
    }}

    /* ─── ProgressBar ─── */
    QProgressBar {{
        background-color: {BORDER};
        border: none;
        border-radius: 4px;
        height: 8px;
        text-align: center;
    }}
    QProgressBar::chunk {{
        background-color: {PRIMARY};
        border-radius: 4px;
    }}

    /* ─── GroupBox ─── */
    QGroupBox {{
        color: {TEXT_SECONDARY};
        border: 1px solid {BORDER};
        border-radius: 8px;
        margin-top: 12px;
        padding-top: 16px;
        font-weight: 600;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        padding: 0 8px;
    }}

    /* ─── Dialog ─── */
    QDialog {{
        background-color: {BG_DARK};
    }}
    """
