from algoritmos.base import PlanificadorBase
from nucleo.proceso import PCB

class PlanificadorRoundRobin(PlanificadorBase):
    """
    Implementación del algoritmo Round Robin.
    Utiliza una cola FIFO, pero el simulador expulsará al proceso 
    si agota su quantum de tiempo.
    """
    def __init__(self, quantum: int):
        super().__init__()
        self.quantum = quantum  # Quantum configurable solicitado

    def agregar_proceso(self, pcb: PCB):
        """Agrega (o re-encola) un proceso al final de la fila."""
        self.cola_listos.append(pcb)

    def obtener_siguiente(self) -> PCB | None:
        """Extrae el proceso al frente de la fila."""
        if not self.cola_listos:
            return None
            
        return self.cola_listos.pop(0)