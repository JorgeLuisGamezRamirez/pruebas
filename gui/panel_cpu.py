from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from nucleo.proceso import EstadoProceso
from gui import estilos


class PanelCPU(QWidget):
    """Tab: Visualización en vivo de la CPU, colas de listos y terminados."""

    def __init__(self):
        super().__init__()
        self._construir_ui()

    def _construir_ui(self):
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(15, 15, 15, 15)
        layout_principal.setSpacing(15)

        # ─── Columna izquierda: Cola de Listos ───
        self.col_listos = self._crear_columna_cola("● COLA DE LISTOS", estilos.ESTADO_LISTO)
        layout_principal.addWidget(self.col_listos, 2)

        # ─── Centro: CPU ───
        centro = QVBoxLayout()
        centro.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Flecha izquierda
        lbl_flecha = QLabel("►")
        lbl_flecha.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_flecha.setStyleSheet(f"color: {estilos.TEXT_MUTED}; font-size: 24px;")

        self.card_cpu = QFrame()
        self.card_cpu.setObjectName("card")
        self.card_cpu.setFixedSize(280, 220)
        self.card_cpu.setStyleSheet(f"""
            QFrame#card {{
                background-color: {estilos.BG_CARD};
                border: 2px solid {estilos.BORDER};
                border-radius: 14px;
            }}
        """)
        cpu_layout = QVBoxLayout(self.card_cpu)
        cpu_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cpu_layout.setSpacing(8)

        self.lbl_cpu_estado = QLabel("● INACTIVA")
        self.lbl_cpu_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_cpu_estado.setStyleSheet(f"color: {estilos.TEXT_MUTED}; font-size: 12px; font-weight: bold;")
        cpu_layout.addWidget(self.lbl_cpu_estado)

        self.lbl_cpu_pid = QLabel("—")
        self.lbl_cpu_pid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_cpu_pid.setFont(QFont(estilos.FONT_MONO, 32, QFont.Weight.Bold))
        self.lbl_cpu_pid.setStyleSheet(f"color: {estilos.PRIMARY_LIGHT};")
        cpu_layout.addWidget(self.lbl_cpu_pid)

        self.lbl_cpu_nombre = QLabel("")
        self.lbl_cpu_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_cpu_nombre.setStyleSheet(f"color: {estilos.TEXT_SECONDARY}; font-size: 12px;")
        cpu_layout.addWidget(self.lbl_cpu_nombre)

        self.lbl_cpu_rafaga = QLabel("")
        self.lbl_cpu_rafaga.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_cpu_rafaga.setStyleSheet(
            f"color: {estilos.SECONDARY}; font-family: {estilos.FONT_MONO}; font-size: 13px;"
        )
        cpu_layout.addWidget(self.lbl_cpu_rafaga)

        centro.addStretch()
        centro.addWidget(self.card_cpu)
        centro.addStretch()

        layout_principal.addLayout(centro, 3)

        # ─── Columna derecha: Terminados ───
        self.col_terminados = self._crear_columna_cola("● TERMINADOS", estilos.ESTADO_TERMINADO)
        layout_principal.addWidget(self.col_terminados, 2)

    def _crear_columna_cola(self, titulo: str, color: str) -> QFrame:
        frame = QFrame()
        frame.setObjectName("card")
        frame.setStyleSheet(f"""
            QFrame#card {{
                background-color: {estilos.BG_CARD};
                border: 1px solid {estilos.BORDER};
                border-radius: 10px;
            }}
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)

        header = QHBoxLayout()
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setFont(QFont(estilos.FONT_FAMILY, 11, QFont.Weight.Bold))
        lbl_titulo.setStyleSheet(f"color: {color};")
        header.addWidget(lbl_titulo)

        lbl_count = QLabel("Q:0")
        lbl_count.setObjectName("lbl_count")
        lbl_count.setStyleSheet(f"color: {estilos.TEXT_MUTED}; font-size: 11px;")
        header.addStretch()
        header.addWidget(lbl_count)
        layout.addLayout(header)

        # Área scrollable para los items
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll_content = QWidget()
        scroll_content.setObjectName("scroll_inner")
        scroll_content.setStyleSheet("QWidget#scroll_inner { background: transparent; }")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(4)
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        return frame

    def _crear_item_proceso(self, proceso, color_borde: str) -> QFrame:
        item = QFrame()
        item.setStyleSheet(f"""
            QFrame {{
                background-color: {estilos.BG_DARKEST};
                border: 1px solid {color_borde};
                border-left: 3px solid {color_borde};
                border-radius: 6px;
                padding: 6px;
            }}
        """)
        h = QHBoxLayout(item)
        h.setContentsMargins(8, 5, 8, 5)

        lbl_pid = QLabel(f"PID: {proceso.pid}")
        lbl_pid.setFont(QFont(estilos.FONT_MONO, 10))
        lbl_pid.setStyleSheet(f"color: {estilos.TEXT_PRIMARY}; border: none;")
        h.addWidget(lbl_pid)

        h.addStretch()

        lbl_bt = QLabel(f"BT: {proceso.rafaga_restante}t")
        lbl_bt.setFont(QFont(estilos.FONT_MONO, 10))
        lbl_bt.setStyleSheet(f"color: {color_borde}; border: none;")
        h.addWidget(lbl_bt)

        return item

    def actualizar(self, estado: dict):
        """Actualiza la visualización con el estado recibido."""
        proceso_cpu = estado.get('proceso_en_cpu')
        cola_listos = estado.get('cola_listos', [])
        terminados = estado.get('terminados', [])

        # --- Actualizar CPU ---
        if proceso_cpu:
            self.card_cpu.setStyleSheet(f"""
                QFrame#card {{
                    background-color: {estilos.BG_CARD};
                    border: 2px solid {estilos.ESTADO_EJECUTANDO};
                    border-radius: 14px;
                }}
            """)
            self.lbl_cpu_estado.setText("● EJECUTANDO")
            self.lbl_cpu_estado.setStyleSheet(f"color: {estilos.ESTADO_EJECUTANDO}; font-size: 12px; font-weight: bold;")
            self.lbl_cpu_pid.setText(f"P{proceso_cpu.pid}")
            self.lbl_cpu_nombre.setText(proceso_cpu.nombre)
            pct = int((1 - proceso_cpu.rafaga_restante / max(proceso_cpu.rafaga_cpu_total, 1)) * 100)
            self.lbl_cpu_rafaga.setText(f"Ráfaga: {proceso_cpu.rafaga_restante}t restante ({pct}%)")
        else:
            self.card_cpu.setStyleSheet(f"""
                QFrame#card {{
                    background-color: {estilos.BG_CARD};
                    border: 2px dashed {estilos.BORDER};
                    border-radius: 14px;
                }}
            """)
            self.lbl_cpu_estado.setText("● INACTIVA")
            self.lbl_cpu_estado.setStyleSheet(f"color: {estilos.TEXT_MUTED}; font-size: 12px; font-weight: bold;")
            self.lbl_cpu_pid.setText("—")
            self.lbl_cpu_nombre.setText("")
            self.lbl_cpu_rafaga.setText("")

        # --- Actualizar Cola Listos ---
        self._llenar_cola(self.col_listos, cola_listos, estilos.ESTADO_LISTO)

        # --- Actualizar Terminados ---
        self._llenar_cola(self.col_terminados, terminados, estilos.ESTADO_TERMINADO)

    def _llenar_cola(self, frame_cola: QFrame, procesos: list, color: str):
        scroll = frame_cola.findChild(QScrollArea)
        # takeWidget() desvincula el widget anterior sin destruirlo
        old_content = scroll.takeWidget()
        if old_content:
            old_content.deleteLater()

        new_content = QWidget()
        new_content.setObjectName("scroll_inner")
        new_content.setStyleSheet("QWidget#scroll_inner { background: transparent; }")
        new_layout = QVBoxLayout(new_content)
        new_layout.setContentsMargins(0, 0, 0, 0)
        new_layout.setSpacing(4)

        for p in procesos:
            item = self._crear_item_proceso(p, color)
            new_layout.addWidget(item)
        new_layout.addStretch()

        scroll.setWidget(new_content)

        # Actualizar contador
        lbl_count = frame_cola.findChild(QLabel, "lbl_count")
        if lbl_count:
            lbl_count.setText(f"Q:{len(procesos)}")
