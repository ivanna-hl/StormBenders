# Mapa/modelo/nasa_data.py
import requests
from datetime import datetime

class NASAData:
    """
    Capa Modelo: maneja la extracción de imágenes del servicio NASA GIBS / WorldView.
    """

    BASE_URL = "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best"
    LAYER = "MODIS_Terra_CorrectedReflectance_TrueColor"  # capa visible y funcional
    TILE_MATRIX_SET = "250m"
    FORMAT = "image/jpeg"

    def __init__(self):
        self.session = requests.Session()

    def obtener_mapa(self, fecha=None, nivel_zoom=5, tile_matrix=5, tile_row=10, tile_col=5):
        """
        Descarga una tesela válida del mapa NASA WorldView (GIBS).
        """
        if fecha is None:
            fecha = datetime.utcnow().strftime("%Y-%m-%d")

        url = (
            f"{self.BASE_URL}/{self.LAYER}/default/{fecha}/{self.TILE_MATRIX_SET}/"
            f"{tile_matrix}/{tile_row}/{tile_col}.jpg"
        )

        print(f"🌍 Descargando mapa desde:\n{url}\n")  # para depuración

        response = self.session.get(url)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Error al obtener mapa ({response.status_code}): {response.text[:100]}")

    def obtener_datos_clima(self, lat, lon):
        """
        Simulación: retorna datos de temperatura o nubosidad para una coordenada (lat, lon).
        """
        return {
            "lat": lat,
            "lon": lon,
            "temperatura": 27.3,
            "humedad": 70,
            "viento": 5.2
        }
