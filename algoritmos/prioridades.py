from algoritmos.base import PlanificadorBase
from nucleo.proceso import PCB

class PlanificadorPrioridades(PlanificadorBase):
    """
    Implementación de Planificación por Prioridades.
    Selecciona el proceso con el valor numérico de prioridad más bajo.
    """
    def __init__(self):
        super().__init__()

    def agregar_proceso(self, pcb: PCB):
        """Agrega el proceso a la cola de listos."""
        self.cola_listos.append(pcb)

    def obtener_siguiente(self) -> PCB | None:
        """Extrae y retorna el proceso con mayor prioridad."""
        if not self.cola_listos:
            return None
            
        # Ordenamos la cola por prioridad (menor número = mayor prioridad)
        self.cola_listos.sort(key=lambda p: p.prioridad)
        
        # Extraemos el proceso de mayor prioridad
        return self.cola_listos.pop(0)