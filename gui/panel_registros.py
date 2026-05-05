from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QTextCursor
from gui import estilos


class PanelRegistros(QWidget):
    """Tab: Consola de logs estilo terminal del sistema."""

    def __init__(self):
        super().__init__()
        self._ultimo_len = 0
        self._construir_ui()

    def _construir_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        header = QLabel("▌ SYS_LOG // REGISTROS DEL SISTEMA")
        header.setFont(QFont(estilos.FONT_FAMILY, 16, QFont.Weight.Bold))
        layout.addWidget(header)

        self.consola = QTextEdit()
        self.consola.setReadOnly(True)
        self.consola.setFont(QFont(estilos.FONT_MONO, 11))
        self.consola.setStyleSheet(f"""
            QTextEdit {{
                background-color: {estilos.BG_DARKEST};
                color: {estilos.SECONDARY};
                border: 1px solid {estilos.BORDER};
                border-radius: 8px;
                padding: 12px;
                line-height: 1.5;
            }}
        """)
        layout.addWidget(self.consola)

    def actualizar(self, estado: dict):
        logs = estado.get('log', [])
        # Solo agregar logs nuevos (para eficiencia)
        if len(logs) > self._ultimo_len:
            nuevos = logs[self._ultimo_len:]
            for msg in nuevos:
                self.consola.append(msg)
            self._ultimo_len = len(logs)
            # Auto-scroll al final
            cursor = self.consola.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.consola.setTextCursor(cursor)

    def limpiar(self):
        self.consola.clear()
        self._ultimo_len = 0
