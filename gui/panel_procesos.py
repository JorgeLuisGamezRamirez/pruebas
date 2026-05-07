from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from nucleo.proceso import EstadoProceso
from gui import estilos


class PanelProcesos(QWidget):
    """Tab: Tabla de procesos con acciones de crear/eliminar."""

    def __init__(self, simulador):
        super().__init__()
        self.simulador = simulador
        self._construir_ui()

    def _construir_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        # Header
        header = QHBoxLayout()
        lbl = QLabel("▌ LISTADO DE PROCESOS")
        lbl.setFont(QFont(estilos.FONT_FAMILY, 16, QFont.Weight.Bold))
        header.addWidget(lbl)
        header.addStretch()

        layout.addLayout(header)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(8)
        self.tabla.setHorizontalHeaderLabels([
            "PID", "Nombre", "Estado", "Prioridad",
            "Ráfaga Total", "Ráfaga Rest.", "Memoria (MB)", "T. Espera"
        ])
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setShowGrid(False)
        layout.addWidget(self.tabla)

    def actualizar(self, estado: dict):
        """Recibe el estado completo y repinta la tabla."""
        todos = estado.get('todos', [])
        self.tabla.setRowCount(len(todos))

        for i, p in enumerate(todos):
            # PID
            item_pid = QTableWidgetItem(str(p.pid))
            item_pid.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_pid.setFont(QFont(estilos.FONT_MONO, 12, QFont.Weight.Bold))
            self.tabla.setItem(i, 0, item_pid)

            # Nombre
            item_nom = QTableWidgetItem(p.nombre)
            item_nom.setFont(QFont(estilos.FONT_MONO, 11))
            item_nom.setForeground(QColor(estilos.PRIMARY_LIGHT))
            self.tabla.setItem(i, 1, item_nom)

            # Estado (badge)
            item_estado = QTableWidgetItem(p.estado.value)
            item_estado.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            color = self._color_estado(p.estado)
            item_estado.setForeground(QColor(color))
            item_estado.setFont(QFont(estilos.FONT_FAMILY, 11, QFont.Weight.Bold))
            self.tabla.setItem(i, 2, item_estado)

            # Prioridad
            item_prio = QTableWidgetItem(str(p.prioridad))
            item_prio.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla.setItem(i, 3, item_prio)

            # Ráfaga total
            item_rt = QTableWidgetItem(f"{p.rafaga_cpu_total} ticks")
            item_rt.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla.setItem(i, 4, item_rt)

            # Ráfaga restante
            item_rr = QTableWidgetItem(f"{p.rafaga_restante} ticks")
            item_rr.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if p.rafaga_restante > 0 and p.estado != EstadoProceso.TERMINADO:
                item_rr.setForeground(QColor(estilos.WARNING))
            self.tabla.setItem(i, 5, item_rr)

            # Memoria
            item_mem = QTableWidgetItem(f"{p.mem_mb}")
            item_mem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabla.setItem(i, 6, item_mem)

            # T. Espera
            item_te = QTableWidgetItem(str(p.tiempo_espera))
            item_te.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if p.tiempo_espera > 0:
                item_te.setForeground(QColor(estilos.SECONDARY))
            self.tabla.setItem(i, 7, item_te)

    def _color_estado(self, estado: EstadoProceso) -> str:
        return {
            EstadoProceso.NUEVO: estilos.ESTADO_NUEVO,
            EstadoProceso.LISTO: estilos.ESTADO_LISTO,
            EstadoProceso.EJECUTANDO: estilos.ESTADO_EJECUTANDO,
            EstadoProceso.ESPERANDO: estilos.ESTADO_ESPERANDO,
            EstadoProceso.TERMINADO: estilos.ESTADO_TERMINADO,
        }.get(estado, estilos.TEXT_MUTED)
