from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QSpinBox, QSlider, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from gui import estilos


class DialogoProceso(QDialog):
    """Diálogo modal para crear o editar un proceso."""

    def __init__(self, parent=None, proceso=None):
        super().__init__(parent)
        self.proceso = proceso
        self.resultado = None
        self.setWindowTitle("Editar Proceso" if proceso else "Nuevo Proceso")
        self.setFixedSize(440, 400)
        self.setModal(True)
        self._construir_ui()

    def _construir_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(30, 25, 30, 25)

        # Título
        icono = "✎" if self.proceso else "+"
        titulo = "EDITAR PROCESO" if self.proceso else "NUEVO PROCESO"
        lbl_titulo = QLabel(f"{icono}  {titulo}")
        lbl_titulo.setFont(QFont(estilos.FONT_FAMILY, 16, QFont.Weight.Bold))
        lbl_titulo.setStyleSheet(f"color: {estilos.TEXT_PRIMARY};")
        layout.addWidget(lbl_titulo)

        if self.proceso:
            lbl_id = QLabel(f"PID: {self.proceso.pid}")
            lbl_id.setStyleSheet(f"color: {estilos.TEXT_MUTED}; font-size: 11px;")
            layout.addWidget(lbl_id)

        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"background-color: {estilos.BORDER};")
        sep.setFixedHeight(1)
        layout.addWidget(sep)

        # Nombre
        lbl_nombre = QLabel("NOMBRE DEL PROCESO")
        lbl_nombre.setStyleSheet(f"color: {estilos.TEXT_SECONDARY}; font-size: 11px; font-weight: bold;")
        layout.addWidget(lbl_nombre)
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Ej: mi_proceso")
        self.txt_nombre.setFixedHeight(36)
        if self.proceso:
            self.txt_nombre.setText(self.proceso.nombre)
        layout.addWidget(self.txt_nombre)

        # Ráfaga CPU
        lbl_rafaga = QLabel("RÁFAGA CPU (TICKS)")
        lbl_rafaga.setStyleSheet(f"color: {estilos.TEXT_SECONDARY}; font-size: 11px; font-weight: bold;")
        layout.addWidget(lbl_rafaga)
        self.spin_rafaga = QSpinBox()
        self.spin_rafaga.setRange(1, 100)
        self.spin_rafaga.setValue(self.proceso.rafaga_cpu_total if self.proceso else 5)
        self.spin_rafaga.setSuffix("  ticks")
        self.spin_rafaga.setFixedHeight(36)
        layout.addWidget(self.spin_rafaga)

        # Prioridad (slider)
        fila_prio = QHBoxLayout()
        col_lbl = QVBoxLayout()
        lbl_prio = QLabel("PRIORIDAD (1-10)")
        lbl_prio.setStyleSheet(f"color: {estilos.TEXT_SECONDARY}; font-size: 11px; font-weight: bold;")
        col_lbl.addWidget(lbl_prio)

        slider_row = QHBoxLayout()
        self.slider_prioridad = QSlider(Qt.Orientation.Horizontal)
        self.slider_prioridad.setRange(1, 10)
        self.slider_prioridad.setValue(self.proceso.prioridad if self.proceso else 5)
        self.slider_prioridad.setTickPosition(QSlider.TickPosition.TicksBelow)
        slider_row.addWidget(self.slider_prioridad)

        self.lbl_prio_val = QLabel(str(self.slider_prioridad.value()))
        self.lbl_prio_val.setFixedWidth(35)
        self.lbl_prio_val.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_prio_val.setStyleSheet(
            f"background-color: {estilos.BG_INPUT}; border: 1px solid {estilos.BORDER}; "
            f"border-radius: 4px; color: {estilos.PRIMARY_LIGHT}; font-family: {estilos.FONT_MONO};"
        )
        self.slider_prioridad.valueChanged.connect(
            lambda v: self.lbl_prio_val.setText(str(v))
        )
        slider_row.addWidget(self.lbl_prio_val)

        col_lbl.addLayout(slider_row)
        fila_prio.addLayout(col_lbl)
        layout.addLayout(fila_prio)

        # Memoria
        lbl_mem = QLabel("MEMORIA (MB)")
        lbl_mem.setStyleSheet(f"color: {estilos.TEXT_SECONDARY}; font-size: 11px; font-weight: bold;")
        layout.addWidget(lbl_mem)
        self.spin_memoria = QSpinBox()
        self.spin_memoria.setRange(8, 2048)
        self.spin_memoria.setValue(self.proceso.mem_mb if self.proceso else 128)
        self.spin_memoria.setSingleStep(32)
        self.spin_memoria.setSuffix("  MB")
        self.spin_memoria.setFixedHeight(36)
        layout.addWidget(self.spin_memoria)

        layout.addStretch()

        # Botones
        fila_btns = QHBoxLayout()
        fila_btns.addStretch()

        btn_cancelar = QPushButton("CANCELAR")
        btn_cancelar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancelar.clicked.connect(self.reject)
        fila_btns.addWidget(btn_cancelar)

        btn_guardar = QPushButton("💾  GUARDAR")
        btn_guardar.setObjectName("btn_secundario")
        btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_guardar.clicked.connect(self._guardar)
        fila_btns.addWidget(btn_guardar)

        layout.addLayout(fila_btns)

    def _guardar(self):
        nombre = self.txt_nombre.text().strip()
        if not nombre:
            nombre = "sin_nombre"
        self.resultado = {
            'nombre': nombre,
            'rafaga_cpu': self.spin_rafaga.value(),
            'prioridad': self.slider_prioridad.value(),
            'mem_mb': self.spin_memoria.value(),
        }
        self.accept()
