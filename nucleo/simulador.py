import random
from datetime import datetime
from nucleo.proceso import PCB, EstadoProceso, CausaTerminacion
from nucleo.recursos import GestorRecursos
from algoritmos.base import PlanificadorBase

NOMBRES_PROCESOS = [
    "init", "systemd", "bash", "python3", "node", "java", "gcc",
    "make", "git", "ssh", "nginx", "mysql", "redis", "docker",
    "vim", "nano", "cat", "grep", "awk", "sed", "curl", "wget",
    "tar", "zip", "top", "htop", "cron", "syslog", "udev", "dbus",
]

class Simulador:
    def __init__(self, planificador: PlanificadorBase, gestor_recursos: GestorRecursos):
        self.planificador = planificador
        self.recursos = gestor_recursos
        self.proceso_en_cpu = None
        self.procesos_terminados = []
        self.todos_los_procesos = []
        self.tiempo_actual = 0
        self.historial_gantt = []
        self.log_eventos = []
        self.quantum_restante = 0

    def crear_proceso(self, nombre: str, prioridad: int, rafaga_cpu: int, mem_mb: int) -> tuple[bool, str]:
        """
        Intenta crear un proceso. Primero verifica si hay recursos disponibles.
        """
        exito, msj = self.recursos.solicitar(cpu_req=1, ram_req=mem_mb)
        if not exito:
            self._log(f"⚠ {msj}")
            return False, msj

        nuevo_pcb = PCB(nombre, prioridad, rafaga_cpu, mem_mb)
        nuevo_pcb.tick_llegada = self.tiempo_actual
        nuevo_pcb.transicionar(EstadoProceso.LISTO)
        
        # Le delegamos al algoritmo activo que decida cómo formarlo
        self.planificador.agregar_proceso(nuevo_pcb)
        self.todos_los_procesos.append(nuevo_pcb)
        
        msg = f"Proceso '{nombre}' (PID:{nuevo_pcb.pid}) creado → Cola de Listos"
        self._log(msg)
        return True, msg

    def crear_procesos_aleatorios(self, cantidad: int):
        """Crea N procesos con nombres, ráfagas y memorias aleatorias."""
        nombres = random.sample(NOMBRES_PROCESOS, min(cantidad, len(NOMBRES_PROCESOS)))
        for i in range(cantidad):
            nombre = nombres[i] if i < len(nombres) else f"proc_{i+1}"
            prioridad = random.randint(1, 10)
            rafaga = random.randint(2, 15)
            memoria = random.choice([32, 64, 128, 256, 512])
            self.crear_proceso(nombre, prioridad, rafaga, memoria)

    def tick_reloj(self) -> dict:
        """
        Avanza la simulación un paso de tiempo.
        Retorna un diccionario con el estado completo del sistema.
        """
        mensajes = []

        # --- Round Robin: verificar si se agotó el quantum ---
        if self.proceso_en_cpu and self._es_round_robin():
            self.quantum_restante -= 1
            if self.quantum_restante <= 0 and self.proceso_en_cpu.rafaga_restante > 0:
                proc = self.proceso_en_cpu
                proc.transicionar(EstadoProceso.LISTO)
                self.planificador.agregar_proceso(proc)
                mensajes.append(f"⏳ PID:{proc.pid} expulsado (quantum)")
                self._log(f"RR: PID:{proc.pid} '{proc.nombre}' → quantum agotado")
                self.proceso_en_cpu = None

        # --- Si la CPU está libre, pedimos el siguiente proceso ---
        if self.proceso_en_cpu is None:
            siguiente = self.planificador.obtener_siguiente()
            if siguiente:
                self.proceso_en_cpu = siguiente
                self.proceso_en_cpu.transicionar(EstadoProceso.EJECUTANDO)
                if self.proceso_en_cpu.tick_inicio_ejecucion is None:
                    self.proceso_en_cpu.tick_inicio_ejecucion = self.tiempo_actual
                if self._es_round_robin():
                    self.quantum_restante = self.planificador.quantum
                mensajes.append(f"▶ PID:{siguiente.pid} subió a CPU")
                self._log(f"Dispatch: PID:{siguiente.pid} '{siguiente.nombre}' → CPU")

        # --- Ejecutar proceso actual ---
        if self.proceso_en_cpu:
            self.proceso_en_cpu.rafaga_restante -= 1
            self.historial_gantt.append(
                (self.tiempo_actual, self.proceso_en_cpu.pid, self.proceso_en_cpu.nombre)
            )

            # ¿Terminó su ráfaga?
            if self.proceso_en_cpu.rafaga_restante <= 0:
                self.proceso_en_cpu.terminar(CausaTerminacion.NORMAL)
                self.proceso_en_cpu.tick_finalizacion = self.tiempo_actual + 1
                self.proceso_en_cpu.tiempo_retorno = (
                    self.proceso_en_cpu.tick_finalizacion - self.proceso_en_cpu.tick_llegada
                )
                self.proceso_en_cpu.tiempo_espera = (
                    self.proceso_en_cpu.tiempo_retorno - self.proceso_en_cpu.rafaga_cpu_total
                )
                self.procesos_terminados.append(self.proceso_en_cpu)
                self.recursos.liberar(cpu_liberada=1, ram_liberada=self.proceso_en_cpu.mem_mb)
                mensajes.append(f"✓ PID:{self.proceso_en_cpu.pid} finalizó")
                self._log(
                    f"Fin: PID:{self.proceso_en_cpu.pid} '{self.proceso_en_cpu.nombre}' "
                    f"(T.Retorno={self.proceso_en_cpu.tiempo_retorno})"
                )
                self.proceso_en_cpu = None
        else:
            self.historial_gantt.append((self.tiempo_actual, None, None))

        self.tiempo_actual += 1
        return self.obtener_estado(mensajes)

    def obtener_estado(self, mensajes_tick=None) -> dict:
        """Retorna un snapshot completo del sistema para la GUI."""
        cpu_pct = 0.0
        if self.recursos.total_cpu > 0:
            cpu_pct = (
                (self.recursos.total_cpu - self.recursos.cpu_libre)
                / self.recursos.total_cpu * 100
            )
        ram_usada = self.recursos.total_ram_mb - self.recursos.ram_libre

        # Calcular métricas promedio de procesos terminados
        avg_espera = 0.0
        avg_retorno = 0.0
        if self.procesos_terminados:
            avg_espera = sum(p.tiempo_espera for p in self.procesos_terminados) / len(self.procesos_terminados)
            avg_retorno = sum(p.tiempo_retorno for p in self.procesos_terminados) / len(self.procesos_terminados)

        return {
            'tick': self.tiempo_actual,
            'cpu_porcentaje': cpu_pct,
            'ram_usada': ram_usada,
            'ram_total': self.recursos.total_ram_mb,
            'proceso_en_cpu': self.proceso_en_cpu,
            'cola_listos': list(self.planificador.cola_listos),
            'terminados': list(self.procesos_terminados),
            'todos': list(self.todos_los_procesos),
            'historial_gantt': list(self.historial_gantt),
            'log': list(self.log_eventos),
            'mensajes_tick': mensajes_tick or [],
            'algoritmo': type(self.planificador).__name__,
            'avg_espera': avg_espera,
            'avg_retorno': avg_retorno,
        }

    def cambiar_algoritmo(self, nuevo_planificador: PlanificadorBase):
        """Cambia el algoritmo transfiriendo procesos en cola."""
        procesos_en_cola = list(self.planificador.cola_listos)
        self.planificador.cola_listos.clear()
        self.planificador = nuevo_planificador
        for p in procesos_en_cola:
            self.planificador.agregar_proceso(p)
        self._log(f"Algoritmo cambiado a: {type(nuevo_planificador).__name__}")

    def reiniciar(self):
        """Resetea completamente la simulación."""
        self.proceso_en_cpu = None
        self.procesos_terminados.clear()
        self.todos_los_procesos.clear()
        self.planificador.cola_listos.clear()
        self.tiempo_actual = 0
        self.historial_gantt.clear()
        self.log_eventos.clear()
        self.quantum_restante = 0
        self.recursos.cpu_libre = self.recursos.total_cpu
        self.recursos.ram_libre = self.recursos.total_ram_mb
        PCB.resetear_pids()
        self._log("Sistema reiniciado")

    def _es_round_robin(self) -> bool:
        return hasattr(self.planificador, 'quantum')

    def _log(self, mensaje: str):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_eventos.append(f"[{ts}] T={self.tiempo_actual}: {mensaje}")