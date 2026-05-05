from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QComboBox, QPushButton, QFrame, QCheckBox
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from gui import estilos


class PantallaConfig(QWidget):
    """Pantalla de configuración inicial (Boot Screen) del simulador."""
    senal_iniciar = pyqtSignal(dict)  # Emite parámetros al presionar Iniciar

    def __init__(self):
        super().__init__()
        self._construir_ui()

    def _construir_ui(self):
        layout_ext = QVBoxLayout(self)
        layout_ext.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_container = QFrame()
        main_container.setFixedWidth(800)
        main_container.setStyleSheet(f"""
            QFrame {{
                background-color: {estilos.BG_DARKEST};
                border: 2px solid {estilos.PRIMARY_DARK};
                border-radius: 20px;
            }}
        """)
        main_layout = QHBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        panel_izq = QFrame()
        panel_izq.setStyleSheet(f"""
            QFrame {{
                background-color: {estilos.BG_CARD};
                border-top-left-radius: 18px;
                border-bottom-left-radius: 18px;
                border: none;
                border-right: 2px solid {estilos.PRIMARY_DARK};
            }}
        """)
        izq_layout = QVBoxLayout(panel_izq)
        izq_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        izq_layout.setContentsMargins(40, 40, 40, 40)

        lbl_logo = QLabel('⚙️')
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_logo.setFont(QFont(estilos.FONT_MONO, 48))
        lbl_logo.setStyleSheet('border: none; background: transparent;')
        izq_layout.addWidget(lbl_logo)

        lbl_titulo = QLabel('NEXUS // CTRL')
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_titulo.setFont(QFont(estilos.FONT_MONO, 20, QFont.Weight.Bold))
        lbl_titulo.setStyleSheet(f'color: {estilos.PRIMARY_LIGHT}; border: none; background: transparent;')
        izq_layout.addWidget(lbl_titulo)

        panel_der = QFrame()
        panel_der.setStyleSheet('border: none; background: transparent;')
        der_layout = QVBoxLayout(panel_der)
        der_layout.setSpacing(15)
        der_layout.setContentsMargins(30, 40, 30, 40)

        # Grupo Hardware
        lbl_hw = QLabel('/// RECURSOS DEL SISTEMA')
        lbl_hw.setFont(QFont(estilos.FONT_MONO, 12, QFont.Weight.Bold))
        lbl_hw.setStyleSheet(f'color: {estilos.SUCCESS}; border: none; background: transparent;')
        der_layout.addWidget(lbl_hw)

        fila_mem = QHBoxLayout()
        lbl_mem = QLabel('Memoria RAM:')
        lbl_mem.setStyleSheet('border: none; background: transparent; font-weight: bold;')
        self.spin_memoria = QSpinBox()
        self.spin_memoria.setRange(256, 16384)
        self.spin_memoria.setValue(4096)
        self.spin_memoria.setSingleStep(256)
        self.spin_memoria.setSuffix(' MB')
        self.spin_memoria.setFixedHeight(35)
        fila_mem.addWidget(lbl_mem)
        fila_mem.addWidget(self.spin_memoria)
        der_layout.addLayout(fila_mem)

        # Grupo Planificador
        lbl_sw = QLabel('/// PLANIFICADOR DE TAREAS')
        lbl_sw.setFont(QFont(estilos.FONT_MONO, 12, QFont.Weight.Bold))
        lbl_sw.setStyleSheet(f'color: {estilos.SUCCESS}; border: none; background: transparent;')
        der_layout.addWidget(lbl_sw)

        self.combo_algoritmo = QComboBox()
        self.combo_algoritmo.addItems([
            'FCFS (First-Come, First-Served)',
            'SJF (Shortest Job First)',
            'Round Robin',
            'Prioridades',
        ])
        self.combo_algoritmo.setFixedHeight(35)
        self.combo_algoritmo.currentIndexChanged.connect(self._on_algoritmo_cambio)
        der_layout.addWidget(self.combo_algoritmo)

        self.contenedor_quantum = QWidget()
        q_layout = QHBoxLayout(self.contenedor_quantum)
        q_layout.setContentsMargins(0, 0, 0, 0)
        lbl_quantum = QLabel('Quantum (Ticks):')
        lbl_quantum.setStyleSheet('border: none; background: transparent; font-weight: bold;')
        self.spin_quantum = QSpinBox()
        self.spin_quantum.setRange(1, 100)
        self.spin_quantum.setValue(3)
        self.spin_quantum.setFixedHeight(35)
        q_layout.addWidget(lbl_quantum)
        q_layout.addWidget(self.spin_quantum)
        self.contenedor_quantum.setVisible(False)
        der_layout.addWidget(self.contenedor_quantum)

        # Grupo Procesos
        fila_procs = QHBoxLayout()
        lbl_procs = QLabel('Procesos Iniciales:')
        lbl_procs.setStyleSheet('border: none; background: transparent; font-weight: bold;')
        self.spin_procesos = QSpinBox()
        self.spin_procesos.setRange(0, 30)
        self.spin_procesos.setValue(5)
        self.spin_procesos.setFixedHeight(35)
        fila_procs.addWidget(lbl_procs)
        fila_procs.addWidget(self.spin_procesos)
        der_layout.addLayout(fila_procs)

        self.chk_auto = QCheckBox('Generar automáticamente')
        self.chk_auto.setChecked(True)
        self.chk_auto.setStyleSheet(f"""
            QCheckBox {{ color: {estilos.TEXT_PRIMARY}; border: none; background: transparent; font-weight: bold; }}
            QCheckBox::indicator {{ width: 18px; height: 18px; border-radius: 4px; border: 1px solid {estilos.BORDER}; background: {estilos.BG_INPUT}; }}
            QCheckBox::indicator:checked {{ background-color: {estilos.SUCCESS}; border-color: {estilos.SUCCESS}; }}
        """)
        der_layout.addWidget(self.chk_auto)

        der_layout.addSpacing(20)

        self.btn_iniciar = QPushButton('▶ INICIALIZAR ENTORNO')
        self.btn_iniciar.setObjectName('btn_primario')
        self.btn_iniciar.setFixedHeight(50)
        self.btn_iniciar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_iniciar.clicked.connect(self._on_iniciar)
        der_layout.addWidget(self.btn_iniciar)

        main_layout.addWidget(panel_izq, 1)
        main_layout.addWidget(panel_der, 2)
        layout_ext.addWidget(main_container)

    def _on_algoritmo_cambio(self, index):
        self.contenedor_quantum.setVisible(index == 2)  # Round Robin

    def _on_iniciar(self):
        params = {
            'procesos_iniciales': self.spin_procesos.value(),
            'memoria_mb': self.spin_memoria.value(),
            'algoritmo': self.combo_algoritmo.currentIndex(),
            'quantum': self.spin_quantum.value(),
            'auto_crear': self.chk_auto.isChecked(),
        }
        self.senal_iniciar.emit(params)
