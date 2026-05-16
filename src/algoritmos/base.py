from abc import ABC, abstractmethod
from nucleo.proceso import PCB

class PlanificadorBase(ABC):
    """Interfaz base obligatoria para todos los algoritmos de planificación."""
    
    def __init__(self):
        self.cola_listos = []  # Estructura principal donde esperarán los PCB

    @abstractmethod
    def agregar_proceso(self, pcb: PCB):
        """Añade un proceso a la cola de listos según las reglas del algoritmo."""
        pass

    @abstractmethod
    def obtener_siguiente(self) -> PCB | None:
        """Extrae y retorna el siguiente proceso a ejecutar."""
        pass
        
    def obtener_cola_listos(self) -> list[PCB]:
        """Útil para mostrar el estado en la interfaz gráfica (PyQt6)."""
        return self.cola_listos