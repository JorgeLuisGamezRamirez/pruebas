from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout,
    QSpinBox, QComboBox, QPushButton, QFrame, QSlider
)
from PyQt6.QtCore import pyqtSignal, Qt
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

        self.setStyleSheet(f"""
                border: 1px solid {estilos.BORDER_LIGHT};
                border-radius: 6px;
                padding: 6px 10px;
                min-height: 32px;
            }}
            QComboBox:hover, QSpinBox:hover {{
                border-color: {estilos.PRIMARY_LIGHT};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 28px;
            }}
            QCheckBox {{
                color: {estilos.TEXT_PRIMARY};
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid {estilos.BORDER_LIGHT};
                background: {estilos.BG_INPUT};
            }}
            QCheckBox::indicator:checked {{
                background-color: {estilos.PRIMARY};
                border-color: {estilos.PRIMARY};
            }}
            QPushButton#btn_iniciar {{
                background-color: {estilos.PRIMARY};
                color: {estilos.TEXT_ON_PRIMARY};
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 16px;
            }}
            QPushButton#btn_iniciar:hover {{
                background-color: {estilos.PRIMARY_LIGHT};
            }}
        """)

        card = QFrame()
        card.setObjectName("config_card")
        card.setFixedWidth(720)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 28, 32, 28)
        card_layout.setSpacing(20)

        titulo = QLabel("Configuracion del Entorno")
        titulo.setObjectName("titulo_principal")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(titulo)

        subtitulo = QLabel("Ajusta los recursos y el planificador antes de iniciar la simulacion")
        subtitulo.setObjectName("subtitulo")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(subtitulo)

        separador = QFrame()
        separador.setFixedHeight(1)
        separador.setStyleSheet(f"background-color: {estilos.BORDER};")
        card_layout.addWidget(separador)

        panel_der = QFrame()
        grid = QGridLayout(panel_der)
        grid.setSpacing(20)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 2)
        grid.setColumnStretch(2, 2)

        # Fila 0 - Recursos
        layout_recursos = QVBoxLayout()
        layout_recursos.setSpacing(8)
        lbl_recursos = QLabel("RECURSOS")
        lbl_recursos.setStyleSheet(
            f"color: {estilos.SUCCESS}; font-size: 12px; font-weight: bold;"
        )
        layout_recursos.addWidget(lbl_recursos)

        ram_row = QHBoxLayout()
        lbl_ram = QLabel("RAM (MB):")
        self.slider_ram = QSlider(Qt.Orientation.Horizontal)
        self.slider_ram.setRange(256, 16384)
        self.slider_ram.setSingleStep(256)
        self.slider_ram.setPageStep(1024)
        self.slider_ram.setValue(4096)
        self.spin_ram = QSpinBox()
        self.spin_ram.setRange(256, 16384)
        self.spin_ram.setSingleStep(256)
        self.spin_ram.setValue(4096)
        self.spin_ram.setFixedWidth(120)

        ram_row.addWidget(lbl_ram)
        ram_row.addWidget(self.slider_ram, 1)
        ram_row.addWidget(self.spin_ram)
        layout_recursos.addLayout(ram_row)

        grid.addLayout(layout_recursos, 0, 0, 1, 2)

        # Fila 0 - Algoritmo
        layout_algo = QVBoxLayout()
        layout_algo.setSpacing(8)
        lbl_plan = QLabel("ALGORITMO DE PLANIFICACION")
        lbl_plan.setStyleSheet(
            f"color: {estilos.SUCCESS}; font-size: 12px; font-weight: bold;"
        )
        layout_algo.addWidget(lbl_plan)

        self.combo_algoritmo = QComboBox()
        self.combo_algoritmo.setMinimumWidth(200)
        self.combo_algoritmo.addItems([
            "FCFS (First-Come, First-Served)",
            "SJF (Shortest Job First)",
            "Round Robin",
            "Prioridades",
        ])
        self.combo_algoritmo.currentIndexChanged.connect(self._on_algoritmo_cambio)
        layout_algo.addWidget(self.combo_algoritmo)
        grid.addLayout(layout_algo, 0, 2)

        # Fila 1 - Carga inicial
        layout_carga = QVBoxLayout()
        layout_carga.setSpacing(8)
        lbl_carga = QLabel("CARGA INICIAL")
        lbl_carga.setStyleSheet(
            f"color: {estilos.SUCCESS}; font-size: 12px; font-weight: bold;"
        )
        layout_carga.addWidget(lbl_carga)

        lbl_proc = QLabel("Procesos iniciales:")
        self.spin_procesos = QSpinBox()
        self.spin_procesos.setRange(1, 30)
        self.spin_procesos.setValue(5)
        self.spin_procesos.setFixedHeight(36)
        layout_carga.addWidget(lbl_proc)
        layout_carga.addWidget(self.spin_procesos)

        lbl_nucleos = QLabel("Nucleos CPU:")
        self.spin_nucleos = QSpinBox()
        self.spin_nucleos.setRange(1, 16)
        self.spin_nucleos.setValue(2)
        self.spin_nucleos.setFixedHeight(36)
        layout_carga.addWidget(lbl_nucleos)
        layout_carga.addWidget(self.spin_nucleos)
        layout_carga.addStretch()

        grid.addLayout(layout_carga, 1, 0)

        # Fila 1 - Resumen
        layout_resumen = QVBoxLayout()
        layout_resumen.setSpacing(8)
        resumen_titulo = QLabel("RESUMEN DE SIMULACION")
        resumen_titulo.setStyleSheet(
            f"color: {estilos.SUCCESS}; font-size: 12px; font-weight: bold;"
        )
        layout_resumen.addWidget(resumen_titulo)

        self.lbl_resumen = QLabel("")
        self.lbl_resumen.setWordWrap(True)
        self.lbl_resumen.setStyleSheet(
            f"color: {estilos.TEXT_SECONDARY}; padding: 6px;"
        )
        layout_resumen.addWidget(self.lbl_resumen)
        grid.addLayout(layout_resumen, 1, 1)

        # Fila 1 - Detalle
        layout_detalle = QVBoxLayout()
        layout_detalle.setSpacing(8)
        lbl_desc = QLabel("DETALLE DEL ALGORITMO")
        lbl_desc.setStyleSheet(
            f"color: {estilos.SUCCESS}; font-size: 12px; font-weight: bold;"
        )
        layout_detalle.addWidget(lbl_desc)

        self.contenedor_quantum = QWidget()
        quantum_layout = QHBoxLayout(self.contenedor_quantum)
        quantum_layout.setContentsMargins(0, 0, 0, 0)
        lbl_quantum = QLabel("Quantum (ticks)")
        self.spin_quantum = QSpinBox()
        self.spin_quantum.setRange(1, 100)
        self.spin_quantum.setValue(3)
        quantum_layout.addWidget(lbl_quantum)
        quantum_layout.addWidget(self.spin_quantum)
        self.contenedor_quantum.setVisible(False)
        layout_detalle.addWidget(self.contenedor_quantum)

        self.lbl_desc_algo = QLabel("")
        self.lbl_desc_algo.setWordWrap(True)
        self.lbl_desc_algo.setStyleSheet(f"color: {estilos.TEXT_SECONDARY};")
        layout_detalle.addWidget(self.lbl_desc_algo)

        grid.addLayout(layout_detalle, 1, 2)

        card_layout.addWidget(panel_der)

        acciones = QHBoxLayout()
        self.btn_cerrar = QPushButton("Cerrar")
        self.btn_cerrar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cerrar.clicked.connect(self._on_cerrar)
        acciones.addWidget(self.btn_cerrar)

        acciones.addStretch()

        self.btn_siguiente = QPushButton("Siguiente")
        self.btn_siguiente.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_siguiente.setFixedHeight(46)
        self.btn_siguiente.setStyleSheet(
            f"background-color: {estilos.PRIMARY_DARK}; color: {estilos.TEXT_ON_PRIMARY}; "
            "border: none; border-radius: 8px; font-size: 14px; font-weight: bold; "
            "padding: 12px 16px;"
        )
        self.btn_siguiente.clicked.connect(self._on_iniciar)
        acciones.addWidget(self.btn_siguiente)

        card_layout.addLayout(acciones)

        layout_ext.addWidget(card)

        self.slider_ram.valueChanged.connect(self._on_ram_slider_cambio)
        self.spin_ram.valueChanged.connect(self._on_ram_spin_cambio)
        self.spin_procesos.valueChanged.connect(self._actualizar_resumen)
        self.spin_nucleos.valueChanged.connect(self._actualizar_resumen)
        self.combo_algoritmo.currentIndexChanged.connect(self._actualizar_resumen)
        self.spin_quantum.valueChanged.connect(self._actualizar_resumen)
        self._actualizar_resumen()

    def _on_algoritmo_cambio(self, index):
        self.contenedor_quantum.setVisible(index == 2)  # Round Robin
        self._actualizar_resumen()

    def _on_ram_slider_cambio(self, valor: int):
        if self.spin_ram.value() != valor:
            self.spin_ram.blockSignals(True)
            self.spin_ram.setValue(valor)
            self.spin_ram.blockSignals(False)
        self._actualizar_resumen()

    def _on_ram_spin_cambio(self, valor: int):
        if self.slider_ram.value() != valor:
            self.slider_ram.blockSignals(True)
            self.slider_ram.setValue(valor)
            self.slider_ram.blockSignals(False)
        self._actualizar_resumen()

    def _on_cerrar(self):
        self.window().close()

    def _actualizar_resumen(self):
        memoria_texto = f"{self.spin_ram.value()} MB"
        algoritmo = self.combo_algoritmo.currentText()
        quantum_visible = self.combo_algoritmo.currentIndex() == 2
        quantum_texto = f"{self.spin_quantum.value()} ticks" if quantum_visible else "N/A"

        self.lbl_resumen.setText(
            "\n".join([
                f"Memoria RAM: {memoria_texto}",
                f"Procesos iniciales: {self.spin_procesos.value()}",
                f"Nucleos CPU: {self.spin_nucleos.value()}",
                f"Planificador: {algoritmo}",
                f"Quantum: {quantum_texto}",
            ])
        )
        self.lbl_desc_algo.setText(self._descripcion_algoritmo())

    def _descripcion_algoritmo(self) -> str:
        idx = self.combo_algoritmo.currentIndex()
        return {
            0: "FCFS: ejecuta los procesos en el orden de llegada. Simple y no expropiativo.",
            1: "SJF: prioriza la rafaga mas corta. Puede generar inanicion en procesos largos.",
            2: "Round Robin: asigna un quantum fijo y rota procesos listos. Buena respuesta interactiva.",
            3: "Prioridades: atiende primero mayor prioridad. Puede requerir envejecimiento.",
        }.get(idx, "")

    def _on_iniciar(self):
        params = {
            'procesos_iniciales': self.spin_procesos.value(),
            'memoria_mb': self.spin_ram.value(),
            'algoritmo': self.combo_algoritmo.currentIndex(),
            'quantum': self.spin_quantum.value(),
            'auto_crear': True,
            'nucleos_cpu': self.spin_nucleos.value(),
        }
        self.senal_iniciar.emit(params)
