# Mapa/controlador/mapa_controller.py

import folium
from Mapa.modelo.nasa_data import NASAData
import random

class MapaController:
    def __init__(self):
        self.modelo = NASAData()

    def generar_mapa_interactivo(self):
        """
        Genera un mapa interactivo con LayerControl visualmente atractivo.
        """
        # Crear mapa centrado en México
        mapa = folium.Map(
            location=[23.6345, -102.5528],
            zoom_start=5,
            tiles=None
        )

        # --- Capa base con nombre personalizado ---
        folium.TileLayer(
            tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr="&copy; OpenStreetMap contributors",
            name="Clima en tiempo real",
            control=True
        ).add_to(mapa)

        # --- Tipos de clima ---
        tipos_clima = {
            "Soleado 🌞": "yellow",
            "Nublado ☁️": "gray",
            "Lluvia 🌧️": "blue",
            "Tormenta ⛈️": "purple",
            "Despejado 🌤️": "orange"
        }

        # --- Capas de clima ---
        for clima, color in tipos_clima.items():
            capa = folium.FeatureGroup(name=clima)
            for _ in range(25):
                lat = random.uniform(14.5, 32.7)
                lon = random.uniform(-117, -86)
                popup_info = f"{clima}<br>🌡️ Temp: {random.randint(18, 35)}°C<br>💧 Humedad: {random.randint(40, 90)}%"
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=7,
                    color="white",
                    fill=True,
                    fill_color=color.split(",")[0].replace("linear-gradient(45deg,", "").strip(),
                    fill_opacity=0.7,
                    popup=popup_info
                ).add_to(capa)
            capa.add_to(mapa)

        # --- Popups por ciudad ---
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

        # --- LayerControl ---
        folium.LayerControl(collapsed=False).add_to(mapa)

        # --- CSS para mejorar apariencia del menú ---
        css = """
        <style>
        /* === PANEL PRINCIPAL === */
        .leaflet-control-layers {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            padding: 12px 15px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.3);
            font-family: 'Segoe UI', Roboto, sans-serif;
            color: #2c3e50;
            max-width: 220px;
        }

        /* === TÍTULO PRINCIPAL === */
        .leaflet-control-layers-base label {
            display: block;
            font-size: 17px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 10px;
            color: #1e88e5;
            border-bottom: 2px solid #1e88e5;
            padding-bottom: 5px;
        }

        /* === OPCIONES DE CLIMA === */
        .leaflet-control-layers-overlays label {
            font-size: 15px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
            transition: transform 0.15s ease, background 0.2s ease;
            padding: 4px 6px;
            border-radius: 8px;
        }

        .leaflet-control-layers-overlays label:hover {
            background: #f1f1f1;
            transform: scale(1.03);
            cursor: pointer;
        }

        /* === CHECKBOX REDONDEADOS === */
        .leaflet-control-layers-overlays input[type="checkbox"] {
            appearance: none;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            margin-right: 5px;
            border: 2px solid #555;
            position: relative;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .leaflet-control-layers-overlays input[type="checkbox"]:checked::before {
            content: '✔';
            position: absolute;
            top: -2px;
            left: 3px;
            font-size: 14px;
            color: white;
        }

        /* === COLORES DE CADA OPCIÓN === */
        .leaflet-control-layers-overlays label:nth-child(1) input { background: linear-gradient(45deg, #FFD700, #FFA500); border: none; }
        .leaflet-control-layers-overlays label:nth-child(2) input { background: linear-gradient(45deg, #B0BEC5, #ECEFF1); border: none; }
        .leaflet-control-layers-overlays label:nth-child(3) input { background: linear-gradient(45deg, #4FC3F7, #0288D1); border: none; }
        .leaflet-control-layers-overlays label:nth-child(4) input { background: linear-gradient(45deg, #673AB7, #311B92); border: none; }
        .leaflet-control-layers-overlays label:nth-child(5) input { background: linear-gradient(45deg, #FFB74D, #FFE082); border: none; }

        /* === RESPONSIVE === */
        @media (max-width: 768px) {
            .leaflet-control-layers { font-size: 14px; max-width: 180px; }
        }
        </style>
        """
        mapa.get_root().html.add_child(folium.Element(css))

        # Guardar mapa
        mapa.save("mapa_mexico.html")
        print("✅ Mapa interactivo generado: mapa_mexico.html")
