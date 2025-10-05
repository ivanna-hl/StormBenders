# Mapa/modelo/clima_data.py
import requests

class ClimaData:
    """
    Capa Modelo: obtiene datos meteorológicos reales desde la API Open-Meteo.
    Sin necesidad de API key.
    """

    API_URL = "https://api.open-meteo.com/v1/forecast"

    def obtener_clima(self, lat, lon):
        """
        Obtiene datos en tiempo real para una coordenada específica.
        Retorna temperatura, humedad, nubosidad, lluvia y viento.
        """
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "hourly": "temperature_2m,relative_humidity_2m,precipitation,cloud_cover,windspeed_10m"
        }

        response = requests.get(self.API_URL, params=params)
        if response.status_code != 200:
            print(f"⚠️ Error obteniendo datos ({response.status_code})")
            return None

        data = response.json()

        current = data.get("current_weather", {})
        temp = current.get("temperature")
        wind = current.get("windspeed")
        time = current.get("time")

        # Humedad, nubes y precipitación se obtienen de los datos horarios más recientes
        hourly = data.get("hourly", {})
        humidity = hourly.get("relative_humidity_2m", [None])[-1]
        clouds = hourly.get("cloud_cover", [None])[-1]
        rain = hourly.get("precipitation", [None])[-1]

        return {
            "temperatura": temp,
            "humedad": humidity,
            "nubosidad": clouds,
            "lluvia": rain,
            "viento": wind,
            "hora": time
        }
