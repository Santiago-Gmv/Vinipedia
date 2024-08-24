import sys
import os
import folium
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class WineMapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mapa de Lugares que Venden Vino")
        self.setGeometry(100, 100, 1024, 768)
        
        ''' Establecer color de fondo vino '''
        self.setStyleSheet("background-color: #800000;")  # Color vino
        
        ''' Crear el mapa en la ubicación de Mar del Plata '''
        self.current_location = (-38.0054773, -57.5426106)
        self.map = folium.Map(location=self.current_location, zoom_start=14)

        ''' Agregar varios marcadores para lugares ficticios donde se vende vino '''
        places = [
            {"name": "Bodega del Puerto", "location": (-38.0034773, -57.5406106)},
            {"name": "La Viña de Mar del Plata", "location": (-38.0074773, -57.5456106)},
            {"name": "Vino y Sabores", "location": (-38.0104773, -57.5506106)},
            {"name": "Bodega Los Andenes", "location": (-37.9904773, -57.5506106)},  # Nueva ubicación
            {"name": "El Rincón del Vino", "location": (-38.0084773, -57.5406106)},
            {"name": "Vinoteca La Costera", "location": (-38.0114773, -57.5456106)},
            {"name": "El Sabor del Vino", "location": (-38.0044773, -57.5506106)},
            {"name": "La Bodega de Oro", "location": (-38.0094773, -57.5376106)},
            {"name": "Cava del Mar", "location": (-38.0064773, -57.5436106)},
            {"name": "El Valle del Vino", "location": (-38.0054773, -57.5536106)},
            {"name": "Bodega Vino y Arte", "location": (-38.0004773, -57.5476106)},
            {"name": "La Bodega del Viajero", "location": (-38.0124773, -57.5506106)},
            {"name": "El Destino del Vino", "location": (-38.0034773, -57.5526106)},
            {"name": "Vinoteca El Retoño", "location": (-38.0074773, -57.5486106)},
            {"name": "La Viña del Lago", "location": (-38.0104773, -57.5426106)},
            {"name": "El Jardín del Vino", "location": (-38.0024773, -57.5456106)},
        ]

        for place in places:
            folium.Marker(
                location=place["location"],
                popup=place["name"],
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(self.map)

        ''' Guardar el mapa en un archivo HTML '''
        self.map_file = 'mi_mapa_vino.html'  # Cambia el nombre del archivo aquí
        self.map.save(self.map_file)

        ''' Inicializar la interfaz de usuario '''
        self.initUI()

    def initUI(self):
        ''' Configura la interfaz gráfica '''
        # Crear un widget central y un layout vertical
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        ''' Crear un QWebEngineView para mostrar el HTML del mapa '''
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        ''' Verificar si el archivo HTML existe '''
        if os.path.exists(self.map_file):
            ''' Convertir la cadena de archivo en un objeto QUrl '''
            url = QUrl.fromLocalFile(os.path.abspath(self.map_file))
            self.web_view.setUrl(url)
        else:
            ''' Mostrar un mensaje de error si el archivo no se encuentra '''
            error_label = QLabel("No se pudo encontrar el archivo del mapa.")
            error_label.setStyleSheet("color: white;")
            layout.addWidget(error_label)

if __name__ == "__main__":
    ''' Ejecutar la aplicación '''
    app = QApplication(sys.argv)
    window = WineMapApp()
    window.show()
    sys.exit(app.exec_())
