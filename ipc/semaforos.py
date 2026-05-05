import threading

class SemaforoSO:
    """
    Implementación personalizada de un Semáforo Contador.
    Construido usando las primitivas Mutex (Lock) y Condvar (Condition)
    para ilustrar los conceptos de Sistemas Operativos.
    """
    def __init__(self, valor_inicial: int = 0):
        self.valor = valor_inicial
        # El Mutex protege la sección crítica (nuestra variable 'valor')
        self.mutex = threading.Lock()
        # La Variable de Condición permite a los hilos dormir y despertar
        self.condicion = threading.Condition(self.mutex)

    def wait(self):
        """
        Operación Wait (también conocida como P o Down).
        Decrementa el semáforo. Si el valor es 0, el hilo se bloquea hasta que otro haga signal.
        """
        with self.condicion:  # Adquiere el mutex automáticamente
            while self.valor == 0:
                # El hilo actual se va a dormir y libera el mutex temporalmente
                self.condicion.wait() 
            
            # Cuando despierta (y vuelve a adquirir el mutex), decrementa el valor
            self.valor -= 1

    def signal(self):
        """
        Operación Signal (también conocida como V o Up).
        Incrementa el semáforo y despierta a un hilo que esté esperando.
        """
        with self.condicion:  # Adquiere el mutex automáticamente
            self.valor += 1
            # Notifica a un (1) hilo dormido que ya hay recursos disponibles
            self.condicion.notify()