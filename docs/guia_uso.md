# Guia de uso

## 1) Pantalla de configuracion

1. Ajusta la memoria RAM (MB) y el numero de nucleos de CPU.
2. Selecciona el algoritmo de planificacion.
3. Si usas Round Robin, define el quantum (ticks).
4. Indica la cantidad de procesos iniciales.
5. Presiona **Iniciar** para construir el sistema y abrir el dashboard.

## 2) Dashboard

- **Ejecutar:** inicia la simulacion (o reanuda si estaba pausada).
- **Pausar:** detiene el avance de ticks.
- **Reiniciar:** detiene la simulacion y regresa a la pantalla de configuracion.

### Paneles

- **Procesos:** lista los procesos y su estado.
- **Ejecucion CPU:** muestra el estado de los nucleos.
- **Diagrama Gantt:** visualiza la ejecucion en el tiempo.
- **IPC:** permite simular mecanismos de comunicacion.
- **Registros:** muestra eventos y mensajes del sistema.

## 3) Consejos rapidos

- Si no aparecen procesos, reinicia y aumenta la cantidad inicial.
- Para comparar algoritmos, ejecuta la misma carga inicial con distintos planificadores.
