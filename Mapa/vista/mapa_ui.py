# Mapa/vista/mapa_ui.py
import folium
from folium import plugins
import webbrowser
import json

class MapaUI:
    """
    Capa Vista: interfaz del mapa, con menú dinámico, título y popups de clima.
    """

    def __init__(self):
        # Crear mapa base centrado en México
        self.mapa = folium.Map(
            location=[23.6345, -102.5528],
            zoom_start=5,
            tiles="CartoDB positron"
        )

        # Agregar título
        title_html = '''
             <h3 align="center" style="font-size:22px; margin-top:10px;">
                 🌎 <b>Clima en tiempo real</b>
             </h3>
             '''
        self.mapa.get_root().html.add_child(folium.Element(title_html))

        # Preparar contenedores de datos
        self.capas = {
            "temperatura": [],
            "lluvia": [],
            "nubes": []
        }
        self.ciudades = []

    # -----------------------------------------------------------------
    def agregar_datos_clima(self, tipo, puntos):
        """
        Guarda los puntos por tipo de clima.
        """
        if tipo in self.capas:
            self.capas[tipo] = puntos

    def agregar_ciudades(self, ciudades):
        """
        Guarda los datos de las ciudades con sus climas.
        """
        self.ciudades = ciudades

    # -----------------------------------------------------------------
    def generar_mapa(self):
        """
        Genera el mapa con menús, capas y eventos dinámicos en JavaScript.
        """

        # Crear capas HeatMap para cada tipo de clima
        script_layers = []
        for tipo, puntos in self.capas.items():
            layer_name = f"layer_{tipo}"
            data_json = json.dumps(puntos)
            script_layers.append(f"""
                var {layer_name} = L.heatLayer({data_json}, {{
                    radius: 25,
                    blur: 30,
                    maxZoom: 8,
                    gradient: {{
                        0.2: '{'red' if tipo=='temperatura' else ('blue' if tipo=='lluvia' else 'gray')}',
                        0.8: '{'orange' if tipo=='temperatura' else ('skyblue' if tipo=='lluvia' else 'lightgray')}'
                    }}
                }}).addTo(map);
            """)

        # Crear marcadores de ciudades
        markers_js = []
        for c in self.ciudades:
            popup = f"""
            <b>{c['nombre']}</b><br>
            🌡️ {c['temp']:.1f} °C<br>
            💧 {c['humedad']}%<br>
            💨 {c['viento']:.1f} km/h
            """
            markers_js.append(f"""
                L.marker([{c['lat']}, {c['lon']}])
                    .bindPopup("{popup}")
                    .bindTooltip("{c['nombre']}")
                    .addTo(map);
            """)

        # Menú dinámico de clima
        menu_html = """
        <div id="menuClima" style="
            position: fixed;
            top: 60px; left: 20px;
            width: 210px;
            background: white;
            border: 2px solid #4e73df;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3);
            z-index: 9999;
        ">
            <label for="tipoClima"><b>Tipo de clima:</b></label><br>
            <select id="tipoClima" style="width:100%; padding:5px;">
                <option value="temperatura">🌡️ Temperatura</option>
                <option value="lluvia">🌧️ Lluvia</option>
                <option value="nubes">☁️ Nubosidad</option>
            </select>
        </div>

        <script>
            function actualizarClima(tipo) {
                // Ocultar todas las capas
                [layer_temperatura, layer_lluvia, layer_nubes].forEach(l => map.removeLayer(l));
                
                // Mostrar solo la capa seleccionada
                if (tipo === "temperatura") map.addLayer(layer_temperatura);
                if (tipo === "lluvia") map.addLayer(layer_lluvia);
                if (tipo === "nubes") map.addLayer(layer_nubes);
            }

            document.getElementById("tipoClima").addEventListener("change", function() {
                actualizarClima(this.value);
            });
        </script>
        """

        # Inyectar todos los elementos al HTML del mapa
        full_script = "\n".join(script_layers + markers_js)
        self.mapa.get_root().script.add_child(folium.Element(full_script))
        self.mapa.get_root().html.add_child(folium.Element(menu_html))

    # -----------------------------------------------------------------
    def mostrar(self):
        """
        Genera y muestra el mapa completo.
        """
        self.generar_mapa()
        self.mapa.save("mapa_mexico.html")
        print("✅ Mapa interactivo generado: mapa_mexico.html")
        webbrowser.open("mapa_mexico.html")
