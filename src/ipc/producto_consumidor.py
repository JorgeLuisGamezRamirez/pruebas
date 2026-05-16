import threading
import time
import random

class BúferCompartido:
    def __init__(self, capacidad: int):
        self.capacidad = capacidad
        self.búfer = []
        
        # Sincronización: Semáforos y Mutex solicitados en los requisitos
        self.mutex = threading.Lock() # Protege la sección crítica (el arreglo)
        self.huecos_vacios = threading.Semaphore(capacidad) # Cuenta el espacio libre
        self.elementos_llenos = threading.Semaphore(0)      # Cuenta el espacio ocupado

    def producir(self, item: str):
        self.huecos_vacios.acquire()  # Espera si el búfer está lleno
        self.mutex.acquire()          # Bloquea el acceso a otros hilos
        
        self.búfer.append(item)
        print(f"[Productor] Produjo: {item} | Búfer: {self.búfer}")
        
        self.mutex.release()          # Libera la sección crítica
        self.elementos_llenos.release() # Notifica que hay un nuevo elemento

    def consumir(self) -> str:
        self.elementos_llenos.acquire() # Espera si el búfer está vacío
        self.mutex.acquire()            # Bloquea el acceso a otros hilos
        
        item = self.búfer.pop(0)
        print(f"[Consumidor] Consumió: {item} | Búfer: {self.búfer}")
        
        self.mutex.release()            # Libera la sección crítica
        self.huecos_vacios.release()    # Notifica que hay un hueco libre
        return item

# --- Bloque para probarlo en terminal ---
if __name__ == "__main__":
    bufer_demo = BúferCompartido(capacidad=3)

    def tarea_productor():
        for i in range(1, 6):
            bufer_demo.producir(f"Dato-{i}")
            time.sleep(random.uniform(0.5, 1.5))

    def tarea_consumidor():
        for _ in range(5):
            time.sleep(random.uniform(1.0, 2.0))
            bufer_demo.consumir()

    # Arrancamos los hilos
    hilo_prod = threading.Thread(target=tarea_productor)
    hilo_cons = threading.Thread(target=tarea_consumidor)
    
    hilo_prod.start()
    hilo_cons.start()
    
    hilo_prod.join()
    hilo_cons.join()
    print("Demostración IPC completada.")