from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QGridLayout
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

        # ─── Centro: CPUs ───
        centro = QVBoxLayout()
        centro.setAlignment(Qt.AlignmentFlag.AlignCenter)

        scroll_cpus = QScrollArea()
        scroll_cpus.setWidgetResizable(True)
        scroll_cpus.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll_content = QWidget()
        scroll_content.setObjectName("scroll_cpus_inner")
        scroll_content.setStyleSheet("QWidget#scroll_cpus_inner { background: transparent; }")
        self.layout_cpus = QGridLayout(scroll_content)
        self.layout_cpus.setContentsMargins(0, 0, 0, 0)
        self.layout_cpus.setSpacing(12)
        scroll_cpus.setWidget(scroll_content)

        centro.addWidget(scroll_cpus)
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

    def _crear_card_cpu(self, proceso=None) -> QFrame:
        card = QFrame()
        card.setObjectName("card_cpu")
        card.setStyleSheet(f"""
            QFrame#card_cpu {{
                background-color: {estilos.BG_CARD};
                border: 2px solid {estilos.BORDER};
                border-radius: 14px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.setSpacing(6)

        if proceso is None:
            lbl_estado = QLabel("● INACTIVA")
            lbl_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_estado.setStyleSheet(f"color: {estilos.TEXT_MUTED}; font-size: 12px; font-weight: bold;")
            card_layout.addWidget(lbl_estado)

            lbl_pid = QLabel("CPU LIBRE")
            lbl_pid.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_pid.setFont(QFont(estilos.FONT_MONO, 18, QFont.Weight.Bold))
            lbl_pid.setStyleSheet(f"color: {estilos.TEXT_SECONDARY};")
            card_layout.addWidget(lbl_pid)
            return card

        lbl_estado = QLabel("● EJECUTANDO")
        lbl_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_estado.setStyleSheet(
            f"color: {estilos.ESTADO_EJECUTANDO}; font-size: 12px; font-weight: bold;"
        )
        card_layout.addWidget(lbl_estado)

        lbl_pid = QLabel(f"P{proceso.pid}")
        lbl_pid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_pid.setFont(QFont(estilos.FONT_MONO, 28, QFont.Weight.Bold))
        lbl_pid.setStyleSheet(f"color: {estilos.PRIMARY_LIGHT};")
        card_layout.addWidget(lbl_pid)

        lbl_nombre = QLabel(proceso.nombre)
        lbl_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_nombre.setStyleSheet(f"color: {estilos.TEXT_SECONDARY}; font-size: 12px;")
        card_layout.addWidget(lbl_nombre)

        pct = int((1 - proceso.rafaga_restante / max(proceso.rafaga_cpu_total, 1)) * 100)
        lbl_rafaga = QLabel(f"Rafaga: {proceso.rafaga_restante}t ({pct}%)")
        lbl_rafaga.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_rafaga.setStyleSheet(
            f"color: {estilos.ESTADO_EJECUTANDO}; font-family: {estilos.FONT_MONO}; font-size: 12px;"
        )
        card_layout.addWidget(lbl_rafaga)

        card.setStyleSheet(f"""
            QFrame#card_cpu {{
                background-color: {estilos.BG_CARD};
                border: 2px solid {estilos.ESTADO_EJECUTANDO};
                border-radius: 14px;
            }}
        """)
        return card

    def _limpiar_layout(self, layout: QGridLayout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def actualizar(self, estado: dict):
        """Actualiza la visualización con el estado recibido."""
        procesos_cpu = estado.get('procesos_en_cpu', [])
        cola_listos = estado.get('cola_listos', [])
        terminados = estado.get('terminados', [])

        # --- Actualizar CPUs ---
        self._limpiar_layout(self.layout_cpus)
        if not procesos_cpu:
            self.layout_cpus.addWidget(self._crear_card_cpu(), 0, 0)
        else:
            cols = 2
            for idx, proc in enumerate(procesos_cpu):
                row = idx // cols
                col = idx % cols
                self.layout_cpus.addWidget(self._crear_card_cpu(proc), row, col)

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
