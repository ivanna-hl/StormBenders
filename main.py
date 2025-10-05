# main.py
from Mapa.controlador.mapa_controller import MapaController

if __name__ == "__main__":
    controlador = MapaController()
    controlador.generar_mapa_interactivo()
