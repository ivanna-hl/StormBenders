# Mapa/controlador/mapa_controller.py
'''
from ..modelo.nasa_data import NASAData
from ..vista.mapa_ui import MapaUI
import time
import random

class MapaController:
    """
    Capa Controlador: coordina los datos (modelo) con la visualización (vista).
    """

    def __init__(self):
        self.modelo = NASAData()
        self.vista = MapaUI()

    def actualizar_clima(self):
        """
        Actualiza el mapa con puntos de calor basados en datos simulados del modelo.
        """
        puntos = []
        for _ in range(100):
            lat = random.uniform(14.5, 32.7)
            lon = random.uniform(-117, -86)
            temp = random.uniform(20, 40)
            puntos.append([lat, lon, temp])
        
        self.vista.agregar_capa_calor(puntos)
        self.vista.mostrar()

    def descargar_mapa_nasa(self):
        """
        Descarga una tesela del mapa de la NASA para mostrarla o procesarla.
        """
        data = self.modelo.obtener_mapa()
        with open("nasa_mapa.png", "wb") as f:
            f.write(data)
        print("🛰️ Mapa de la NASA descargado: nasa_mapa.png")
'''
# Mapa/controlador/mapa_controller.py
import folium
from folium.plugins import HeatMap
from branca.element import Template, MacroElement
from Mapa.modelo.nasa_data import NASAData
import random

class MapaController:
    def __init__(self):
        self.modelo = NASAData()

    def generar_mapa_interactivo(self):
        """
        Genera un mapa interactivo con menú dinámico de tipos de clima
        y popups informativos en ciudades.
        """
        # Crear mapa centrado en México
        mapa = folium.Map(
            location=[23.6345, -102.5528],
            zoom_start=5,
            tiles="OpenStreetMap"
        )

        # Capa base: diferentes tipos de climas (simulados)
        tipos_clima = {
            "Soleado": "yellow",
            "Nublado": "gray",
            "Lluvia": "blue",
            "Tormenta": "purple",
            "Despejado": "orange"
        }

        capas = {}

        # Crea una capa de puntos por cada tipo de clima
        for clima, color in tipos_clima.items():
            capa = folium.FeatureGroup(name=clima)
            for _ in range(25):  # puntos simulados
                lat = random.uniform(14.5, 32.7)
                lon = random.uniform(-117, -86)
                popup_info = f"{clima} <br>Temp: {random.randint(20, 35)}°C<br>Humedad: {random.randint(40, 80)}%"
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=8,
                    color=color,
                    fill=True,
                    fill_opacity=0.6,
                    popup=popup_info
                ).add_to(capa)
            capas[clima] = capa
            capa.add_to(mapa)

        # --- Popups interactivos por ciudad ---
        ciudades = {
            "CDMX": [19.4326, -99.1332],
            "Guadalajara": [20.6597, -103.3496],
            "Monterrey": [25.6866, -100.3161],
            "Mérida": [20.9674, -89.5926],
            "Tijuana": [32.5149, -117.0382]
        }

        for ciudad, coords in ciudades.items():
            datos = self.modelo.obtener_datos_clima(*coords)
            popup_text = f"""
            <b>{ciudad}</b><br>
            🌡️ Temp: {datos['temperatura']} °C<br>
            💧 Humedad: {datos['humedad']}%<br>
            💨 Viento: {datos['viento']} m/s
            """
            folium.Marker(
                location=coords,
                popup=popup_text,
                icon=folium.Icon(color="red", icon="cloud")
            ).add_to(mapa)

        # --- Menú dinámico para seleccionar clima ---
        html_menu = """
        {% macro html(this, kwargs) %}
        <div style="
            position: fixed; 
            top: 10px; left: 50%; 
            transform: translateX(-50%);
            z-index: 9999;
            background-color: white; 
            padding: 10px 20px; 
            border-radius: 10px;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.3);
            font-family: Arial;
        ">
            <h3 style="text-align:center; margin:5px;">☀️ Clima en tiempo real</h3>
            <label>Seleccionar tipo de clima:</label>
            <select id="climaSelect" onchange="seleccionarClima()">
                <option value="Todos">Todos</option>
                <option value="Soleado">Soleado</option>
                <option value="Nublado">Nublado</option>
                <option value="Lluvia">Lluvia</option>
                <option value="Tormenta">Tormenta</option>
                <option value="Despejado">Despejado</option>
            </select>
        </div>

        <script>
        function seleccionarClima(){
            var clima = document.getElementById('climaSelect').value;
            for (let layer in window.layer_control._layers) {
                var name = window.layer_control._layers[layer].name;
                var obj = window.layer_control._layers[layer].layer;
                if(clima === 'Todos' || clima === name){
                    mapa.addLayer(obj);
                } else {
                    mapa.removeLayer(obj);
                }
            }
        }
        </script>
        {% endmacro %}
        """
        menu = MacroElement()
        menu._template = Template(html_menu)
        mapa.get_root().add_child(menu)

        # Control de capas
        layer_control = folium.LayerControl(collapsed=False)
        layer_control.add_to(mapa)
        mapa.get_root().script.add_child(folium.Element("window.layer_control = layer_control;"))

        # Guardar mapa
        mapa.save("mapa_mexico.html")
        print("✅ Mapa interactivo generado: mapa_mexico.html")
