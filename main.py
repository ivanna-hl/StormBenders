'''
from Mapa.controlador.mapa_controller import MapaController

if __name__ == "__main__":
    controlador = MapaController()
    
    # 1️⃣ Genera el mapa con puntos de calor simulados
    controlador.actualizar_clima()

    # 2️⃣ Descarga una tesela de mapa satelital desde la NASA
    controlador.descargar_mapa_nasa()
'''

# main.py
from Mapa.controlador.mapa_controller import MapaController

if __name__ == "__main__":
    controlador = MapaController()
    controlador.generar_mapa_interactivo()
