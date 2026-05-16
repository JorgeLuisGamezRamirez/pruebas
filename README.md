# Simulador de Sistemas Operativos

Breve descripción: Aplicación gráfica que simula la planificación de procesos y el uso de recursos del sistema (CPU, memoria e IPC).

## Tabla de contenidos

- [Portada](#portada)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Documentación](#documentación)

## Portada

- **Nombre del Proyecto:** Simulador de Sistemas Operativos
- **Breve descripción del proyecto:** Simulador gráfico de planificación de procesos con soporte de múltiples algoritmos y gestión de recursos.
- **Materia:** Sistemas Operativos
- **Institución:** Universidad Autónoma de Tamaulipas
- **Semestre:** Sexto
- **Docente:** Muñoz Quintero Dante Adolfo
- **Integrantes del Equipo:**
  - Perea Torres Ariel Neftali
  - Rocha Hernández Edgar de Jesús
  - Gamez Ramírez Jorge Luis
  - Brizuela Gonzalez Gustavo Adrián

## Estructura del repositorio

```
.
├─ .venv/
│  ├─ .gitignore
│  ├─ Include/
│  ├─ Lib/
│  ├─ Scripts/
│  └─ pyvenv.cfg
├─ .gitignore
├─ README.md
├─ requirements.txt
├─ docs/
│  └─ guia_uso.md
└─ src/
  ├─ main.py
  ├─ algoritmos/
  │  ├─ __init__.py
  │  ├─ base.py
  │  ├─ fcfs.py
  │  ├─ prioridades.py
  │  ├─ round_robin.py
  │  └─ sjf.py
  ├─ gui/
  │  ├─ __init__.py
  │  ├─ estilos.py
  │  ├─ panel_cpu.py
  │  ├─ panel_gantt.py
  │  ├─ panel_ipc.py
  │  ├─ panel_procesos.py
  │  ├─ panel_registros.py
  │  ├─ pantalla_config.py
  │  ├─ ventana_principal.py
  │  └─ worker.py
  ├─ ipc/
  │  ├─ __init__.py
  │  ├─ producto_consumidor.py
  │  └─ semaforos.py
  └─ nucleo/
    ├─ __init__.py
    ├─ proceso.py
    ├─ recursos.py
    └─ simulador.py
```

## Requisitos

- Python 3.10 o superior
- PyQt6

## Instalación

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecución

```bash
python src/main.py
```

## Documentación

- Guía de uso: ver docs/guia_uso.md
