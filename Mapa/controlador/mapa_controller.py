# Mapa/controlador/mapa_controller.py
import folium
from Mapa.modelo.nasa_data import NASAData
from Mapa.modelo.clima_data import ClimaData
import random

class MapaController:
    def __init__(self):
        self.nasa = NASAData()
        self.clima = ClimaData()

    def generar_mapa_interactivo(self):
        """
        Genera el mapa interactivo con datos reales en todos los puntos,
        incluyendo aleatorios, ciudades y municipios.
        """
        mapa = folium.Map(location=[23.6345, -102.5528], zoom_start=5, tiles=None)

        # --- Capas base ---
        folium.TileLayer(
            tiles="https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/{time}/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpg",
            attr="NASA GIBS / WorldView",
            name="Imágenes Satelitales NASA",
            overlay=False,
            control=True,
            fmt="image/jpeg",
            time="2025-10-01"
        ).add_to(mapa)

        folium.TileLayer(
            tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr="Mapa en blanco con divisiones",
            name="🗒️ Mapa en blanco",
            overlay=False,
            control=True,
            opacity=0
        ).add_to(mapa)

        mapa.get_root().html.add_child(
            folium.Element("""<style>.leaflet-tile-pane { background-color: white !important; }</style>""")
        )

        # --- Tipos de clima fusionados ---
        tipos_clima = {
            "Soleado 🌞": "yellow",
            "Nublado ☁️": "gray",
            "Lluvia 🌧️": "blue",
            "Tormenta ⛈️": "purple",
            "Despejado 🌤️": "orange"
        }

        capas_clima = {clima: folium.FeatureGroup(name=clima, show=True) for clima in tipos_clima}

        # --- Función para clasificar el clima ---
        def tipo_clima(datos):
            if datos['lluvia'] >= 10:
                return "Tormenta ⛈️", "purple"
            elif datos['lluvia'] > 0:
                return "Lluvia 🌧️", "blue"
            elif datos['nubosidad'] > 50:
                return "Nublado ☁️", "gray"
            elif datos['nubosidad'] > 20:
                return "Despejado 🌤️", "orange"
            else:
                return "Soleado 🌞", "yellow"

        # --- Generar puntos aleatorios con datos reales ---
        for _ in range(200):
            lat = random.uniform(14.5, 32.7)
            lon = random.uniform(-117, -86)
            datos = self.clima.obtener_clima(lat, lon)
            if not datos:
                continue

            clima_nombre, color = tipo_clima(datos)
            popup_info = f"""
            <b>🌍 Coordenadas:</b> {lat:.4f}, {lon:.4f}<br>
            🌡️ Temp: {datos['temperatura']} °C<br>
            💧 Humedad: {datos['humedad']}%<br>
            ☁️ Nubosidad: {datos['nubosidad']}%<br>
            🌧️ Lluvia: {datos['lluvia']} mm<br>
            💨 Viento: {datos['viento']} km/h<br>
            🕓 {datos['hora']}<br>
            <b>Tipo de clima:</b> {clima_nombre}
            """
            folium.CircleMarker(
                location=[lat, lon],
                radius=6,
                color="white",
                fill=True,
                fill_color=color,
                fill_opacity=0.8,
                popup=popup_info
            ).add_to(capas_clima[clima_nombre])

        # --- Municipios reales ---
        municipios = {
            "CDMX": [19.4326, -99.1332],
            "Guadalajara": [20.6597, -103.3496],
            "Monterrey": [25.6866, -100.3161],
            "Mérida": [20.9674, -89.5926],
            "Tijuana": [32.5149, -117.0382],
            "Puebla": [19.0413, -98.2062],
            "Cancún": [21.1619, -86.8515],
            "Chihuahua": [28.632, -106.0691],
            "Tuxtla Gutiérrez": [16.752, -93.116],
            "Toluca": [19.292, -99.655],
            "Ecatepec de Morelos, Edo. Méx.": [19.6012, -99.0525],
            "Querétaro, Qro.": [20.5888, -100.3899],
            "León, Gto.": [21.122, -101.68],
            "San Luis Potosí, SLP": [22.1565, -100.9855],
            "Aguascalientes, Ags.": [21.8833, -102.3],
            "Cuernavaca, Mor.": [18.9186, -99.2342],
            "Morelia, Mich.": [19.705, -101.194],
            "Oaxaca de Juárez, Oax.": [17.0732, -96.7266],
            "Villahermosa, Tab.": [17.9892, -92.9475],
            "Culiacán, Sin.": [24.799, -107.389],
            "Mazatlán, Sin.": [23.2167, -106.4167],
            "Durango, Dgo.": [24.022, -104.657],
            "Saltillo, Coah.": [25.4232, -100.9917],
            "Veracruz, Ver.": [19.1738, -96.1342],
            "Hermosillo, Son.": [29.0729, -110.9559],
            "La Paz, B.C.S.": [24.1426, -110.3128]
        }

        for municipio, coords in municipios.items():
            datos = self.clima.obtener_clima(*coords)
            if not datos:
                continue
            clima_nombre, color = tipo_clima(datos)
            popup_text = f"""
            <b>{municipio}</b><br>
            🌍 Coordenadas: {coords[0]:.4f}, {coords[1]:.4f}<br>
            🌡️ Temp: {datos['temperatura']} °C<br>
            💧 Humedad: {datos['humedad']}%<br>
            ☁️ Nubosidad: {datos['nubosidad']}%<br>
            🌧️ Lluvia: {datos['lluvia']} mm<br>
            💨 Viento: {datos['viento']} km/h<br>
            🕓 {datos['hora']}<br>
            <b>Tipo de clima:</b> {clima_nombre}
            """
            folium.CircleMarker(
                location=coords,
                radius=7,
                color="white",
                fill=True,
                fill_color=color,
                fill_opacity=0.9,
                popup=popup_text
            ).add_to(capas_clima[clima_nombre])

        # --- Agregar capas ---
        for capa in capas_clima.values():
            capa.add_to(mapa)

        # --- Control de capas ---
        folium.LayerControl(collapsed=False).add_to(mapa)

        # --- Overlays fijos NASA ---
        for layer, name in [
            ("Reference_Features", "Features"),
            ("Reference_Labels", "Labels"),
            ("Coastlines", "Coastlines")
        ]:
            folium.TileLayer(
                tiles=f"https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/{layer}/default/{{time}}/GoogleMapsCompatible_Level9/{{z}}/{{y}}/{{x}}.png",
                attr=name,
                overlay=True,
                control=False,
                fmt="image/png",
                opacity=0.9,
                time="2025-10-01"
            ).add_to(mapa)

        # --- Estilos CSS personalizados ---
        with open("Mapa/vista/estilos.css", "r", encoding="utf-8") as css:
            mapa.get_root().html.add_child(folium.Element(f"<style>{css.read()}</style>"))

        mapa.save("mapa_mexico.html")
        print("✅ Mapa actualizado con datos reales en todos los puntos: mapa_mexico.html")
