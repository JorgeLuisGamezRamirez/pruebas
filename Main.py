import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

# Importamos nuestra interfaz gráfica y estilos
from gui.ventana_principal import VentanaPrincipal
from gui.estilos import obtener_stylesheet, FONT_FAMILY


if __name__ == '__main__':
    # 1. Instanciamos la aplicación Qt
    app = QApplication(sys.argv)

    # 2. Aplicamos la fuente global
    font = QFont(FONT_FAMILY, 11)
    app.setFont(font)

    # 3. Aplicamos el stylesheet global
    app.setStyleSheet(obtener_stylesheet())

    # 4. Creamos la ventana principal y la iniciamos maximizada
    #    (el simulador se crea DESPUÉS desde la pantalla de configuración)
    ventana = VentanaPrincipal()
    ventana.showMaximized()

    # 5. Entregamos el control al bucle de eventos de PyQt6
    sys.exit(app.exec())