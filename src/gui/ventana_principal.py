from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QStackedWidget, QTabWidget, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from gui import estilos
from gui.worker import WorkerSimulador
from gui.pantalla_config import PantallaConfig
from gui.panel_procesos import PanelProcesos
from gui.panel_cpu import PanelCPU
from gui.panel_gantt import PanelGantt
from gui.panel_registros import PanelRegistros
from gui.panel_ipc import PanelIPC

from nucleo.simulador import Simulador
from nucleo.recursos import GestorRecursos
from algoritmos.fcfs import PlanificadorFCFS
from algoritmos.sjf import PlanificadorSJF
from algoritmos.round_robin import PlanificadorRoundRobin
from algoritmos.prioridades import PlanificadorPrioridades


class VentanaPrincipal(QMainWindow):
    """Ventana principal — orquesta Config Screen y Dashboard."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("NEXUS // CTRL — Simulador de Sistemas Operativos")
        self.resize(1200, 800)
        self.setMinimumSize(900, 600)

        self.simulador = None
        self.worker = None

        # Stack para alternar entre pantallas
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Pantalla 0: Configuración
        self.pantalla_config = PantallaConfig()
        self.pantalla_config.senal_iniciar.connect(self._on_iniciar_sistema)
        self.stack.addWidget(self.pantalla_config)

        # Pantalla 1: Dashboard (se construye al iniciar)
        self.dashboard = None

    def _on_iniciar_sistema(self, params: dict):
        """Callback cuando el usuario presiona Iniciar en la config screen."""
        # Crear backend con los parámetros elegidos
        mem = params['memoria_mb']
        algoritmo_idx = params['algoritmo']
        quantum = params['quantum']
        nucleos = params.get('nucleos', params.get('nucleos_cpu', 1))

        planificador = self._crear_planificador(algoritmo_idx, quantum)
        recursos = GestorRecursos(total_cpu=nucleos, total_ram_mb=mem)
        self.simulador = Simulador(planificador, recursos)

        # Crear procesos iniciales si se pidió
        if params['auto_crear'] and params['procesos_iniciales'] > 0:
            self.simulador.crear_procesos_aleatorios(params['procesos_iniciales'])

        # Construir dashboard
        self._construir_dashboard()
        self.stack.setCurrentIndex(1)

        # Iniciar worker (pausado)
        self.worker = WorkerSimulador(self.simulador)
        self.worker.senal_estado.connect(self._on_tick)
        self.worker.start()

        # Mostrar estado inicial
        estado_inicial = self.simulador.obtener_estado()
        self._on_tick(estado_inicial)

        self._on_ejecutar()

    def _crear_planificador(self, idx: int, quantum: int):
        if idx == 0:
            return PlanificadorFCFS()
        elif idx == 1:
            return PlanificadorSJF()
        elif idx == 2:
            return PlanificadorRoundRobin(quantum)
        elif idx == 3:
            return PlanificadorPrioridades()
        return PlanificadorFCFS()

    def _construir_dashboard(self):
        """Construye toda la interfaz del dashboard."""
        self.dashboard = QWidget()
        layout = QVBoxLayout(self.dashboard)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ─── Barra Superior ───
        barra = QFrame()
        barra.setFixedHeight(56)
        barra.setStyleSheet(f"""
            QFrame {{
                background-color: {estilos.BG_DARKEST};
                border-bottom: 1px solid {estilos.BORDER};
            }}
        """)
        barra_layout = QHBoxLayout(barra)
        barra_layout.setContentsMargins(20, 0, 20, 0)

        lbl_titulo = QLabel("⬡  NEXUS // CTRL")
        lbl_titulo.setFont(QFont(estilos.FONT_MONO, 14, QFont.Weight.Bold))
        lbl_titulo.setStyleSheet(f"color: {estilos.PRIMARY_LIGHT};")
        barra_layout.addWidget(lbl_titulo)

        self.lbl_estado_sys = QLabel("● SISTEMA LISTO")
        self.lbl_estado_sys.setStyleSheet(f"color: {estilos.SECONDARY}; font-size: 12px; font-weight: bold;")
        barra_layout.addWidget(self.lbl_estado_sys)

        barra_layout.addStretch()

        # Controles
        self.btn_ejecutar = QPushButton("▶  EJECUTAR")
        self.btn_ejecutar.setObjectName("btn_secundario")
        self.btn_ejecutar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_ejecutar.clicked.connect(self._on_ejecutar)
        barra_layout.addWidget(self.btn_ejecutar)

        self.btn_pausar = QPushButton("⏸  PAUSAR")
        self.btn_pausar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_pausar.setEnabled(False)
        self.btn_pausar.clicked.connect(self._on_pausar)
        barra_layout.addWidget(self.btn_pausar)

        self.btn_reiniciar = QPushButton("↺  REINICIAR")
        self.btn_reiniciar.setObjectName("btn_peligro")
        self.btn_reiniciar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_reiniciar.clicked.connect(self._on_reiniciar)
        barra_layout.addWidget(self.btn_reiniciar)

        layout.addWidget(barra)

        # ─── Métricas ───
        metricas = QFrame()
        metricas.setFixedHeight(80)
        metricas.setStyleSheet(f"background-color: {estilos.BG_DARK}; border-bottom: 1px solid {estilos.BORDER};")
        met_layout = QHBoxLayout(metricas)
        met_layout.setContentsMargins(20, 8, 20, 8)
        met_layout.setSpacing(15)

        self.met_cpu = self._crear_metrica_mini("⚡ CPU", "0%", estilos.PRIMARY)
        met_layout.addWidget(self.met_cpu)

        self.met_ram = self._crear_metrica_mini("≡ MEMORIA", "0 / 0 MB", estilos.SECONDARY)
        met_layout.addWidget(self.met_ram)

        self.met_procs = self._crear_metrica_mini("⚙ PROCESOS", "0", estilos.ACCENT)
        met_layout.addWidget(self.met_procs)

        self.met_algo = self._crear_metrica_mini("⊞ ALGORITMO", "—", estilos.WARNING)
        met_layout.addWidget(self.met_algo)

        self.met_tick = self._crear_metrica_mini("⏱ TICK", "0", estilos.INFO)
        met_layout.addWidget(self.met_tick)

        met_layout.addStretch()
        layout.addWidget(metricas)

        # ─── Tabs ───
        self.tabs = QTabWidget()
        self.panel_procesos = PanelProcesos(self.simulador)
        self.panel_cpu = PanelCPU()
        self.panel_gantt = PanelGantt()
        self.panel_registros = PanelRegistros()
        self.panel_ipc = PanelIPC()

        self.tabs.addTab(self.panel_procesos, "📋  PROCESOS")
        self.tabs.addTab(self.panel_cpu, "🖥  EJECUCIÓN CPU")
        self.tabs.addTab(self.panel_gantt, "📊  DIAGRAMA GANTT")
        self.tabs.addTab(self.panel_ipc, "🔗  IPC")
        self.tabs.addTab(self.panel_registros, "📝  REGISTROS")

        layout.addWidget(self.tabs)

        self.stack.addWidget(self.dashboard)

    def _crear_metrica_mini(self, titulo: str, valor: str, color: str) -> QFrame:
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {estilos.BG_CARD};
                border: 1px solid {estilos.BORDER};
                border-radius: 8px;
                padding: 4px;
            }}
        """)
        card.setFixedWidth(180)
        v = QVBoxLayout(card)
        v.setContentsMargins(12, 4, 12, 4)
        v.setSpacing(1)

        lbl_t = QLabel(titulo)
        lbl_t.setStyleSheet(f"color: {estilos.TEXT_MUTED}; font-size: 9px; font-weight: bold; border: none;")
        v.addWidget(lbl_t)

        lbl_v = QLabel(valor)
        lbl_v.setObjectName("met_valor")
        lbl_v.setFont(QFont(estilos.FONT_MONO, 14, QFont.Weight.Bold))
        lbl_v.setStyleSheet(f"color: {color}; border: none;")
        v.addWidget(lbl_v)

        return card

    # ─── Controles ───

    def _on_ejecutar(self):
        if self.worker:
            self.worker.reanudar()
        self.btn_ejecutar.setEnabled(False)
        self.btn_pausar.setEnabled(True)
        self.lbl_estado_sys.setText("● EJECUTANDO")
        self.lbl_estado_sys.setStyleSheet(f"color: {estilos.ESTADO_EJECUTANDO}; font-size: 12px; font-weight: bold;")

    def _on_pausar(self):
        if self.worker:
            self.worker.pausar()
        self.btn_ejecutar.setEnabled(True)
        self.btn_pausar.setEnabled(False)
        self.lbl_estado_sys.setText("● PAUSADO")
        self.lbl_estado_sys.setStyleSheet(f"color: {estilos.WARNING}; font-size: 12px; font-weight: bold;")

    def _on_reiniciar(self):
        if self.worker:
            self.worker.pausar()
        self.btn_ejecutar.setEnabled(True)
        self.btn_pausar.setEnabled(False)

        # Detener worker y volver a config
        if self.worker:
            self.worker.detener()
            self.worker.wait()
            self.worker = None

        self.panel_ipc.detener_si_corriendo()

        # Remover dashboard
        if self.dashboard:
            self.stack.removeWidget(self.dashboard)
            self.dashboard.deleteLater()
            self.dashboard = None

        self.stack.setCurrentIndex(0)

    # ─── Actualización en cada tick ───

    def _on_tick(self, estado: dict):
        """Recibe el estado completo del simulador y actualiza todos los paneles."""
        # Métricas superiores
        cpu_pct = estado.get('cpu_porcentaje', 0)
        ram_usada = estado.get('ram_usada', 0)
        ram_total = estado.get('ram_total', 0)
        n_procs = len(estado.get('todos', []))
        algo = estado.get('algoritmo', '—').replace('Planificador', '')
        tick = estado.get('tick', 0)

        self.met_cpu.findChild(QLabel, "met_valor").setText(f"{cpu_pct:.0f}%")
        self.met_ram.findChild(QLabel, "met_valor").setText(f"{ram_usada}/{ram_total}")
        self.met_procs.findChild(QLabel, "met_valor").setText(str(n_procs))
        self.met_algo.findChild(QLabel, "met_valor").setText(algo)
        self.met_tick.findChild(QLabel, "met_valor").setText(str(tick))

        # Actualizar todos los paneles
        self.panel_procesos.actualizar(estado)
        self.panel_cpu.actualizar(estado)
        self.panel_gantt.actualizar(estado)
        self.panel_registros.actualizar(estado)

        terminados = estado.get('terminados', [])
        todos = estado.get('todos', [])
        if len(todos) > 0 and len(terminados) == len(todos):
            if self.worker:
                self.worker.pausar()
            self.btn_ejecutar.setEnabled(False)
            self.btn_pausar.setEnabled(False)
            self.lbl_estado_sys.setText("● SIMULACIÓN FINALIZADA")
            self.lbl_estado_sys.setStyleSheet(
                f"color: {estilos.SUCCESS}; font-size: 12px; font-weight: bold;"
            )

    def closeEvent(self, event):
        """Cleanup al cerrar la ventana."""
        if self.worker:
            self.worker.detener()
            self.worker.wait()
        self.panel_ipc.detener_si_corriendo() if hasattr(self, 'panel_ipc') else None
        event.accept()