from algoritmos.base import PlanificadorBase
from nucleo.proceso import PCB

class PlanificadorFCFS(PlanificadorBase):
    """
    Implementación del algoritmo First-Come, First-Served (FCFS).
    El primer proceso en llegar a la cola de listos es el primero en usar la CPU.
    """
    def __init__(self):
        super().__init__()

    def agregar_proceso(self, pcb: PCB):
        """Agrega el proceso al final de la cola (FIFO)."""
        self.cola_listos.append(pcb)

    def obtener_siguiente(self) -> PCB | None:
        """Extrae y retorna el proceso que lleva más tiempo esperando (el primero)."""
        if not self.cola_listos:
            return None
        return self.cola_listos.pop(0)