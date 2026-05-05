from PyQt6.QtCore import QThread, pyqtSignal
import time


class WorkerSimulador(QThread):
    """Hilo de fondo que ejecuta el bucle de simulación tick-by-tick."""
    # Señal con el estado completo del sistema en cada tick
    senal_estado = pyqtSignal(dict)

    def __init__(self, simulador):
        super().__init__()
        self.simulador = simulador
        self.corriendo = True
        self.pausado = True  # Inicia pausado hasta que el usuario presione Ejecutar
        self.velocidad = 1.0  # Segundos entre ticks

    def run(self):
        """Bucle infinito que simula el avance del tiempo."""
        while self.corriendo:
            if not self.pausado:
                estado = self.simulador.tick_reloj()
                self.senal_estado.emit(estado)
            time.sleep(self.velocidad)

    def pausar(self):
        self.pausado = True

    def reanudar(self):
        self.pausado = False

    def set_velocidad(self, segundos: float):
        self.velocidad = max(0.1, segundos)

    def detener(self):
        self.corriendo = False