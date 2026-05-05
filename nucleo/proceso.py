from enum import Enum
import time

class EstadoProceso(Enum):
    NUEVO = "Nuevo"
    LISTO = "Listo"
    EJECUTANDO = "Ejecutando"
    ESPERANDO = "Esperando"
    TERMINADO = "Terminado"

class CausaTerminacion(Enum):
    NORMAL = "Normal"
    ERROR = "Error"
    INTERBLOQUEO = "Interbloqueo"
    USUARIO = "Usuario"

class PCB:
    """Bloque de Control de Proceso"""
    _siguiente_pid = 1  # Variable de clase para generar PIDs únicos

    def __init__(self, nombre: str, prioridad: int, rafaga_cpu: int, mem_mb: int):
        self.pid = PCB._siguiente_pid
        PCB._siguiente_pid += 1
        
        self.nombre = nombre
        self.estado = EstadoProceso.NUEVO
        self.prioridad = prioridad
        self.rafaga_cpu_total = rafaga_cpu
        self.rafaga_restante = rafaga_cpu  # Se irá restando mientras se ejecuta
        self.mem_mb = mem_mb
        self.recursos_asignados = []       # Para registrar recursos de CPU y memoria
        self.tiempo_creacion = time.time()
        self.causa_terminacion = None

        # Métricas de tiempo (en ticks del simulador)
        self.tick_llegada = 0
        self.tick_inicio_ejecucion = None
        self.tick_finalizacion = None
        self.tiempo_espera = 0
        self.tiempo_retorno = 0

    def transicionar(self, nuevo_estado: EstadoProceso):
        """Cambia el estado del proceso de forma segura."""
        self.estado = nuevo_estado

    def terminar(self, causa: CausaTerminacion):
        """Marca el proceso como terminado y registra el motivo."""
        self.transicionar(EstadoProceso.TERMINADO)
        self.causa_terminacion = causa

    @classmethod
    def resetear_pids(cls):
        """Reinicia el contador de PIDs (útil al reiniciar la simulación)."""
        cls._siguiente_pid = 1