from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QFont, QPainter, QColor, QPen, QBrush
from gui import estilos


class WidgetGantt(QWidget):
    """Widget personalizado que dibuja el diagrama de Gantt con QPainter."""

    def __init__(self):
        super().__init__()
        self.historial = []
        self.setMinimumHeight(200)
        self._colores_pid = {}
        self._color_idx = 0

    def set_historial(self, historial: list):
        self.historial = historial
        self.setMinimumWidth(max(600, len(historial) * 28 + 100))
        self.update()

    def _color_para_pid(self, pid: int) -> str:
        if pid not in self._colores_pid:
            self._colores_pid[pid] = estilos.COLORES_PROCESOS[
                self._color_idx % len(estilos.COLORES_PROCESOS)
            ]
            self._color_idx += 1
        return self._colores_pid[pid]

    def paintEvent(self, event):
        if not self.historial:
            painter = QPainter(self)
            painter.setPen(QColor(estilos.TEXT_MUTED))
            painter.setFont(QFont(estilos.FONT_FAMILY, 12))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Sin datos de ejecución")
            painter.end()
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Recopilar PIDs únicos (con nombre)
        pids_info = {}
        for tick, pid, nombre in self.historial:
            if pid is not None and pid not in pids_info:
                pids_info[pid] = nombre

        if not pids_info:
            painter.setPen(QColor(estilos.TEXT_MUTED))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "CPU inactiva")
            painter.end()
            return

        pids = sorted(pids_info.keys())
        pid_to_row = {pid: i for i, pid in enumerate(pids)}

        # Dimensiones
        margin_left = 80
        margin_top = 30
        margin_bottom = 40
        row_height = 40
        cell_width = 25
        total_ticks = len(self.historial)

        chart_height = len(pids) * row_height
        chart_width = total_ticks * cell_width

        # Fondo del gráfico
        painter.fillRect(
            QRectF(margin_left, margin_top, chart_width, chart_height),
            QColor(estilos.BG_DARKEST)
        )

        # Grid horizontal
        pen_grid = QPen(QColor(estilos.BORDER))
        pen_grid.setWidth(1)
        painter.setPen(pen_grid)
        for i in range(len(pids) + 1):
            y = margin_top + i * row_height
            painter.drawLine(margin_left, int(y), int(margin_left + chart_width), int(y))

        # Grid vertical (cada 5 ticks)
        for t in range(0, total_ticks + 1, 5):
            x = margin_left + t * cell_width
            painter.drawLine(int(x), margin_top, int(x), int(margin_top + chart_height))

        # Labels Y (PIDs)
        painter.setFont(QFont(estilos.FONT_MONO, 10, QFont.Weight.Bold))
        for pid, row in pid_to_row.items():
            y = margin_top + row * row_height + row_height / 2
            painter.setPen(QColor(self._color_para_pid(pid)))
            painter.drawText(
                QRectF(0, y - 10, margin_left - 8, 20),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                f"P{pid}"
            )

        # Labels X (ticks)
        painter.setPen(QColor(estilos.TEXT_MUTED))
        painter.setFont(QFont(estilos.FONT_MONO, 8))
        for t in range(0, total_ticks + 1, 5):
            x = margin_left + t * cell_width
            painter.drawText(
                QRectF(x - 15, margin_top + chart_height + 5, 30, 20),
                Qt.AlignmentFlag.AlignCenter,
                f"{t}"
            )

        # Barras de ejecución
        for tick, pid, nombre in self.historial:
            if pid is None:
                continue
            row = pid_to_row[pid]
            x = margin_left + tick * cell_width
            y = margin_top + row * row_height + 6
            w = cell_width - 2
            h = row_height - 12

            color = QColor(self._color_para_pid(pid))
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(color.darker(130), 1))
            painter.drawRoundedRect(QRectF(x + 1, y, w, h), 4, 4)

            # Tick number inside bar
            painter.setPen(QColor(255, 255, 255, 200))
            painter.setFont(QFont(estilos.FONT_MONO, 7))
            painter.drawText(
                QRectF(x + 1, y, w, h),
                Qt.AlignmentFlag.AlignCenter,
                f"{tick}"
            )

        painter.end()


class PanelGantt(QWidget):
    """Tab: Diagrama de Gantt + métricas de rendimiento."""

    def __init__(self):
        super().__init__()
        self._construir_ui()

    def _construir_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        # Header con métricas
        header = QHBoxLayout()
        lbl = QLabel("▌ DIAGRAMA DE GANTT")
        lbl.setFont(QFont(estilos.FONT_FAMILY, 16, QFont.Weight.Bold))
        header.addWidget(lbl)
        header.addStretch()

        # Cards de métricas
        self.card_tiempo = self._crear_card_metrica("TIEMPO TOTAL", "0", "ticks")
        header.addWidget(self.card_tiempo)
        self.card_espera = self._crear_card_metrica("T. ESPERA PROM", "0.0", "ticks")
        header.addWidget(self.card_espera)
        self.card_retorno = self._crear_card_metrica("T. RETORNO PROM", "0.0", "ticks")
        header.addWidget(self.card_retorno)

        layout.addLayout(header)

        # Gantt chart scrollable
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet(f"""
            QScrollArea {{
                border: 1px solid {estilos.BORDER};
                border-radius: 8px;
                background-color: {estilos.BG_DARKEST};
            }}
        """)
        self.widget_gantt = WidgetGantt()
        self.scroll.setWidget(self.widget_gantt)
        layout.addWidget(self.scroll)

        # Leyenda
        self.layout_leyenda = QHBoxLayout()
        self.layout_leyenda.addWidget(QLabel("Leyenda:"))
        self.layout_leyenda.addStretch()
        layout.addLayout(self.layout_leyenda)

    def _crear_card_metrica(self, titulo: str, valor: str, unidad: str) -> QFrame:
        card = QFrame()
        card.setObjectName("card_metrica")
        card.setFixedWidth(160)
        card.setStyleSheet(f"""
            QFrame#card_metrica {{
                background-color: {estilos.BG_CARD};
                border: 1px solid {estilos.BORDER};
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        v = QVBoxLayout(card)
        v.setContentsMargins(10, 6, 10, 6)
        v.setSpacing(2)

        lbl_t = QLabel(titulo)
        lbl_t.setStyleSheet(f"color: {estilos.TEXT_MUTED}; font-size: 9px; font-weight: bold;")
        v.addWidget(lbl_t)

        h = QHBoxLayout()
        lbl_v = QLabel(valor)
        lbl_v.setObjectName("valor")
        lbl_v.setFont(QFont(estilos.FONT_MONO, 18, QFont.Weight.Bold))
        lbl_v.setStyleSheet(f"color: {estilos.PRIMARY_LIGHT};")
        h.addWidget(lbl_v)

        lbl_u = QLabel(unidad)
        lbl_u.setObjectName("unidad")
        lbl_u.setStyleSheet(f"color: {estilos.TEXT_MUTED}; font-size: 10px;")
        lbl_u.setAlignment(Qt.AlignmentFlag.AlignBottom)
        h.addWidget(lbl_u)
        h.addStretch()
        v.addLayout(h)

        return card

    def actualizar(self, estado: dict):
        historial = estado.get('historial_gantt', [])
        self.widget_gantt.set_historial(historial)

        # Métricas
        tick = estado.get('tick', 0)
        avg_e = estado.get('avg_espera', 0)
        avg_r = estado.get('avg_retorno', 0)

        self.card_tiempo.findChild(QLabel, "valor").setText(str(tick))
        self.card_espera.findChild(QLabel, "valor").setText(f"{avg_e:.1f}")
        self.card_retorno.findChild(QLabel, "valor").setText(f"{avg_r:.1f}")

        # Actualizar leyenda
        # Limpiar leyenda vieja (excepto el label "Leyenda:" y el stretch)
        while self.layout_leyenda.count() > 2:
            item = self.layout_leyenda.takeAt(1)
            if item.widget():
                item.widget().deleteLater()

        pids_vistos = {}
        for _, pid, nombre in historial:
            if pid and pid not in pids_vistos:
                pids_vistos[pid] = nombre
        for pid, nombre in pids_vistos.items():
            color = self.widget_gantt._color_para_pid(pid)
            lbl = QLabel(f"  ■ P{pid}: {nombre}")
            lbl.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: bold;")
            self.layout_leyenda.insertWidget(self.layout_leyenda.count() - 1, lbl)
