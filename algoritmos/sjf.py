from algoritmos.base import PlanificadorBase
from nucleo.proceso import PCB

class PlanificadorSJF(PlanificadorBase):
    """
    Implementación del algoritmo Shortest Job First (SJF).
    Selecciona el proceso con la ráfaga de CPU restante más corta.
    """
    def __init__(self):
        super().__init__()

    def agregar_proceso(self, pcb: PCB):
        """Agrega el proceso a la cola de listos."""
        self.cola_listos.append(pcb)

    def obtener_siguiente(self) -> PCB | None:
        """Extrae y retorna el proceso más corto disponible."""
        if not self.cola_listos:
            return None
            
        # Ordenamos la cola basándonos en la ráfaga restante (de menor a mayor)
        self.cola_listos.sort(key=lambda p: p.rafaga_restante)
        
        # Extraemos el primero (el más corto)
        return self.cola_listos.pop(0)