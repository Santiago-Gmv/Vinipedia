import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class FormularioCataVino(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formulario de Cata de Vino")
        self.setGeometry(100, 100, 1024, 768)
        
        # Establecer color de fondo vino
        self.setStyleSheet("background-color: #800000;")  # Color vino
        
        # Guardar el formulario en un archivo HTML
        self.form_file = 'ficha_de_cata.html'
        self.guardar_html_formulario()
        
        # Inicializar la interfaz de usuario
        self.initUI()

    def initUI(self):
        # Configurar la interfaz gráfica
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Crear un QWebEngineView para mostrar el HTML del formulario
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        # Verificar si el archivo HTML existe
        if os.path.exists(self.form_file):
            url = QUrl.fromLocalFile(os.path.abspath(self.form_file))
            self.web_view.setUrl(url)
        else:
            error_label = QLabel("No se pudo encontrar el archivo del formulario.")
            error_label.setStyleSheet("color: white;")
            layout.addWidget(error_label)

    def guardar_html_formulario(self):
        # Guardar el contenido del formulario HTML en un archivo
        html_content = '''
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Ficha de Cata</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    color: #333;
                }
                h1 {
                    text-align: center;
                    color: #800000; /* Color vino */
                }
                .form-section {
                    margin-bottom: 20px;
                }
                .form-section h2 {
                    background-color: #f0f0f0;
                    padding: 10px;
                    margin: 0 -20px;
                }
                .form-section input[type="text"],
                .form-section input[type="number"],
                .form-section textarea {
                    width: calc(100% - 22px);
                    padding: 10px;
                    margin: 10px 0;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                .checkbox-group {
                    margin: 10px 0;
                }
                .checkbox-group label {
                    margin-right: 15px;
                }
                .form-section label {
                    display: block;
                    margin-bottom: 5px;
                    font-weight: bold;
                }
                .form-section .checkbox-group {
                    display: flex;
                    flex-wrap: wrap;
                }
                .form-section .checkbox-group label {
                    width: 25%;
                }
            </style>
        </head>
        <body>
            <h1>Ficha de Cata</h1>

            <div class="form-section">
                <h2>Fase 1: Examen Visual</h2>
                <label>Profundidad de color:</label>
                <div class="checkbox-group">
                    <label><input type="checkbox"> Pálido</label>
                    <label><input type="checkbox"> Mediano</label>
                    <label><input type="checkbox"> Profundo</label>
                    <label><input type="checkbox"> Oscuro</label>
                </div>
                <label>Tonalidad de color:</label>
                <div class="checkbox-group">
                    <label><input type="checkbox"> Verdoso</label>
                    <label><input type="checkbox"> Amarillo</label>
                    <label><input type="checkbox"> Pajiso</label>
                    <label><input type="checkbox"> Dorado</label>
                    <label><input type="checkbox"> Ámbar</label>
                    <!-- Agrega más opciones según sea necesario -->
                </div>
                <label>Limpidez:</label>
                <div class="checkbox-group">
                    <label><input type="checkbox"> Brillante</label>
                    <label><input type="checkbox"> Cristalino</label>
                    <label><input type="checkbox"> Limpio</label>
                    <label><input type="checkbox"> Apagado</label>
                    <label><input type="checkbox"> Turbio</label>
                </div>
            </div>

            <div class="form-section">
                <h2>Fase 2: Examen Olfativo</h2>
                <label>Intensidad del aroma:</label>
                <div class="checkbox-group">
                    <label><input type="checkbox"> Poco aromático</label>
                    <label><input type="checkbox"> Aromático</label>
                    <label><input type="checkbox"> Muy aromático</label>
                    <label><input type="checkbox"> Inapreciable</label>
                </div>
            </div>

            <div class="form-section">
                <h2>Fase 3: Examen Gustativo</h2>
                <label>Ataque:</label>
                <div class="checkbox-group">
                    <label><input type="checkbox"> Seco</label>
                    <label><input type="checkbox"> Abocado</label>
                    <label><input type="checkbox"> Dulce</label>
                    <label><input type="checkbox"> Ácido</label>
                </div>
                <label>Cuerpo:</label>
                <div class="checkbox-group">
                    <label><input type="checkbox"> Muy liviano</label>
                    <label><input type="checkbox"> Liviano</label>
                    <label><input type="checkbox"> Mucho cuerpo</label>
                    <label><input type="checkbox"> Cuerpo medio</label>
                </div>
                <label>Acidez:</label>
                <div class="checkbox-group">
                    <label><input type="checkbox"> Ácido</label>
                    <label><input type="checkbox"> Fresco</label>
                    <label><input type="checkbox"> Dulce</label>
                    <label><input type="checkbox"> Suave</label>
                </div>
            </div>

            <div class="form-section">
                <h2>Descripción</h2>
                <textarea rows="4" placeholder="Escriba una descripción..."></textarea>
            </div>

            <div class="form-section">
                <h2>Alumno</h2>
                <input type="text" placeholder="Nombre del alumno...">
            </div>
        </body>
        </html>
        '''
        with open(self.form_file, 'w', encoding='utf-8') as file:
            file.write(html_content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    formulario_cata_vino = FormularioCataVino()
    formulario_cata_vino.show()
    sys.exit(app.exec_())

