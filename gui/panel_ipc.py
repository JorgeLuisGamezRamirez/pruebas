import threading
import time
import random
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QSpinBox, QTextEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QTextCursor
from gui import estilos


class WorkerIPC(QThread):
    """Hilo que ejecuta la demo productor-consumidor y emite señales."""
    senal_evento = pyqtSignal(str, list)  # (mensaje, estado_bufer)
    senal_finalizado = pyqtSignal()

    def __init__(self, capacidad: int, n_items: int):
        super().__init__()
        self.capacidad = capacidad
        self.n_items = n_items
        self.corriendo = True

    def run(self):
        bufer = []
        mutex = threading.Lock()
        huecos = threading.Semaphore(self.capacidad)
        llenos = threading.Semaphore(0)

        def producir():
            for i in range(1, self.n_items + 1):
                if not self.corriendo:
                    return
                huecos.acquire()
                mutex.acquire()
                item = f"D-{i}"
                bufer.append(item)
                self.senal_evento.emit(
                    f"[Productor] Produjo: {item}",
                    list(bufer)
                )
                mutex.release()
                llenos.release()
                time.sleep(random.uniform(0.4, 1.0))

        def consumir():
            for _ in range(self.n_items):
                if not self.corriendo:
                    return
                llenos.acquire()
                mutex.acquire()
                item = bufer.pop(0)
                self.senal_evento.emit(
                    f"[Consumidor] Consumió: {item}",
                    list(bufer)
                )
                mutex.release()
                huecos.release()
                time.sleep(random.uniform(0.6, 1.5))

        hilo_p = threading.Thread(target=producir)
        hilo_c = threading.Thread(target=consumir)
        hilo_p.start()
        hilo_c.start()
        hilo_p.join()
        hilo_c.join()
        if self.corriendo:
            self.senal_finalizado.emit()

    def detener(self):
        self.corriendo = False


class PanelIPC(QWidget):
    """Tab: Demostración visual del problema Productor-Consumidor."""

    def __init__(self):
        super().__init__()
        self.worker_ipc = None
        self._construir_ui()

    def _construir_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        # Header
        lbl = QLabel("▌ IPC — PRODUCTOR / CONSUMIDOR")
        lbl.setFont(QFont(estilos.FONT_FAMILY, 16, QFont.Weight.Bold))
        layout.addWidget(lbl)

        lbl_desc = QLabel(
            "Demostración del problema clásico de sincronización usando semáforos y mutex. "
            "El productor genera datos y el consumidor los procesa."
        )
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet(f"color: {estilos.TEXT_SECONDARY}; font-size: 12px;")
        layout.addWidget(lbl_desc)

        # Configuración
        config_row = QHBoxLayout()

        # Capacidad del búfer
        col_cap = QVBoxLayout()
        col_cap.addWidget(self._lbl_seccion("CAPACIDAD DEL BÚFER"))
        self.spin_cap = QSpinBox()
        self.spin_cap.setRange(2, 10)
        self.spin_cap.setValue(5)
        self.spin_cap.setFixedHeight(36)
        col_cap.addWidget(self.spin_cap)
        config_row.addLayout(col_cap)

        # Items a producir
        col_items = QVBoxLayout()
        col_items.addWidget(self._lbl_seccion("ITEMS A PRODUCIR"))
        self.spin_items = QSpinBox()
        self.spin_items.setRange(3, 20)
        self.spin_items.setValue(8)
        self.spin_items.setFixedHeight(36)
        col_items.addWidget(self.spin_items)
        config_row.addLayout(col_items)

        config_row.addStretch()

        self.btn_iniciar = QPushButton("▶  INICIAR DEMO")
        self.btn_iniciar.setObjectName("btn_primario")
        self.btn_iniciar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_iniciar.setFixedHeight(42)
        self.btn_iniciar.clicked.connect(self._iniciar_demo)
        config_row.addWidget(self.btn_iniciar)

        self.btn_detener = QPushButton("⏹  DETENER")
        self.btn_detener.setObjectName("btn_peligro")
        self.btn_detener.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_detener.setFixedHeight(42)
        self.btn_detener.setEnabled(False)
        self.btn_detener.clicked.connect(self._detener_demo)
        config_row.addWidget(self.btn_detener)

        layout.addLayout(config_row)

        # Visualización del búfer
        bufer_frame = QFrame()
        bufer_frame.setObjectName("card")
        bufer_frame.setStyleSheet(f"""
            QFrame#card {{
                background-color: {estilos.BG_CARD};
                border: 1px solid {estilos.BORDER};
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        bufer_layout = QVBoxLayout(bufer_frame)

        lbl_bufer = QLabel("ESTADO DEL BÚFER")
        lbl_bufer.setStyleSheet(f"color: {estilos.TEXT_SECONDARY}; font-size: 11px; font-weight: bold;")
        bufer_layout.addWidget(lbl_bufer)

        self.layout_slots = QHBoxLayout()
        self.layout_slots.setSpacing(6)
        self._crear_slots_vacios(5)
        bufer_layout.addLayout(self.layout_slots)

        layout.addWidget(bufer_frame)

        # Log de eventos IPC
        self.consola_ipc = QTextEdit()
        self.consola_ipc.setReadOnly(True)
        self.consola_ipc.setFont(QFont(estilos.FONT_MONO, 11))
        self.consola_ipc.setMaximumHeight(250)
        layout.addWidget(self.consola_ipc)

        layout.addStretch()

    def _lbl_seccion(self, texto: str) -> QLabel:
        lbl = QLabel(texto)
        lbl.setStyleSheet(f"color: {estilos.TEXT_SECONDARY}; font-size: 11px; font-weight: bold;")
        return lbl

    def _crear_slots_vacios(self, n: int):
        while self.layout_slots.count():
            item = self.layout_slots.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for _ in range(n):
            slot = QFrame()
            slot.setFixedSize(60, 50)
            slot.setStyleSheet(f"""
                background-color: {estilos.BG_DARKEST};
                border: 1px dashed {estilos.BORDER};
                border-radius: 6px;
            """)
            self.layout_slots.addWidget(slot)
        self.layout_slots.addStretch()

    def _iniciar_demo(self):
        self.consola_ipc.clear()
        self.consola_ipc.append("Iniciando proceso robotizado...")
        cap = self.spin_cap.value()
        items = self.spin_items.value()
        self._crear_slots_vacios(cap)

        self.btn_iniciar.setEnabled(False)
        self.btn_detener.setEnabled(True)
        self.spin_cap.setEnabled(False)
        self.spin_items.setEnabled(False)

        self.worker_ipc = WorkerIPC(cap, items)
        self.worker_ipc.senal_evento.connect(self._on_evento)
        self.worker_ipc.senal_finalizado.connect(self._on_finalizado)
        self.worker_ipc.start()

    def _detener_demo(self):
        if self.worker_ipc:
            self.worker_ipc.detener()
            self.worker_ipc.wait(2000)
        self.btn_iniciar.setEnabled(True)
        self.btn_detener.setEnabled(False)
        self.spin_cap.setEnabled(True)
        self.spin_items.setEnabled(True)

    def _on_evento(self, mensaje: str, estado_bufer: list):
        self.consola_ipc.append(mensaje)
        cursor = self.consola_ipc.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.consola_ipc.setTextCursor(cursor)

        # Actualizar visualización de slots
        cap = self.spin_cap.value()
        while self.layout_slots.count():
            item = self.layout_slots.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for i in range(cap):
            slot = QFrame()
            slot.setFixedSize(60, 50)
            if i < len(estado_bufer):
                lbl = QLabel(estado_bufer[i])
                lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lbl.setStyleSheet(f"color: white; font-size: 11px; font-weight: bold; border: none;")
                slot_layout = QVBoxLayout(slot)
                slot_layout.setContentsMargins(0, 0, 0, 0)
                slot_layout.addWidget(lbl)
                slot.setStyleSheet(f"""
                    background-color: {estilos.SECONDARY};
                    border: 1px solid {estilos.SEC_DARK};
                    border-radius: 6px;
                """)
            else:
                slot.setStyleSheet(f"""
                    background-color: {estilos.BG_DARKEST};
                    border: 1px dashed {estilos.BORDER};
                    border-radius: 6px;
                """)
            self.layout_slots.addWidget(slot)
        self.layout_slots.addStretch()

    def _on_finalizado(self):
        self.consola_ipc.append("\n✓ Demo IPC completada exitosamente.")
        self.btn_iniciar.setEnabled(True)
        self.btn_detener.setEnabled(False)
        self.spin_cap.setEnabled(True)
        self.spin_items.setEnabled(True)

    def detener_si_corriendo(self):
        """Detiene el worker si está activo (para cleanup al cerrar)."""
        if self.worker_ipc and self.worker_ipc.isRunning():
            self.worker_ipc.detener()
            self.worker_ipc.wait(2000)
