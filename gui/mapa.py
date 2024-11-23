import customtkinter as ctk
from PIL import Image, ImageTk
import os
import webbrowser
import folium
import geocoder
from styles import Colors, Fonts
from utils import WindowManager, ErrorHandler, NotificationManager
from components import AnimatedButton

class PlaceCard(ctk.CTkFrame):
    def __init__(self, master, place_data, command=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.place_data = place_data  # Guardar los datos del lugar
        
        self.configure(
            fg_color=Colors.DARK_BURGUNDY,
            corner_radius=15,
            border_width=2,
            border_color=Colors.GOLD
        )
        
        # Contenedor principal
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Nombre del lugar
        name_label = ctk.CTkLabel(
            content,
            text=place_data["name"],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=Colors.GOLD
        )
        name_label.pack(anchor="w")
        
        # Detalles
        details_label = ctk.CTkLabel(
            content,
            text=f"🚶 {place_data['distance']} | ⭐ {place_data['rating']}",
            font=ctk.CTkFont(size=14),
            text_color=Colors.CREAM
        )
        details_label.pack(anchor="w", pady=5)
        
        # Botón de navegación
        nav_button = AnimatedButton(
            content,
            text="Ir",
            width=60,
            height=30,
            fg_color=Colors.GOLD,
            text_color=Colors.DARK_BURGUNDY,
            hover_color=Colors.ACCENT_GOLD,
            command=self.navigate_to_place  # Añadir comando
        )
        nav_button.pack(side="right")

    def navigate_to_place(self):
        try:
            # Obtener coordenadas del lugar
            location = self.place_data.get("location", None)
            if location:
                # Actualizar el mapa y centrarlo en la ubicación
                self.master.master.master.map.location = location
                self.master.master.master.map.save(self.master.master.master.map_file)
                # Abrir el mapa en el navegador
                webbrowser.open('file://' + os.path.realpath(self.master.master.master.map_file))
            else:
                ErrorHandler.show_error("No se encontró la ubicación del lugar", self)
        except Exception as e:
            ErrorHandler.show_error(f"Error al navegar: {str(e)}", self)

class WineMapApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.window_manager = WindowManager()
        self.title("Mapa de Vinotecas - ViniPedia")
        self.geometry("1300x800")
        self.configure(fg_color=Colors.DARK_BURGUNDY)
        self.center_window()
        self.create_layout()
        self.create_map()
        self.animate_startup()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1300) // 2
        y = (screen_height - 800) // 2
        self.geometry(f"1300x800+{x}+{y}")

    def create_layout(self):
        # Panel superior
        top_panel = ctk.CTkFrame(
            self,
            fg_color=Colors.LIGHT_BURGUNDY,
            corner_radius=15,
            border_width=2,
            border_color=Colors.GOLD
        )
        top_panel.pack(fill="x", padx=20, pady=20)
        
        # Barra de búsqueda
        search_frame = ctk.CTkFrame(top_panel, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Buscar vinoteca o bodega...",
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=Colors.CREAM,
            text_color=Colors.DARK_BURGUNDY,
            placeholder_text_color=Colors.LIGHT_BURGUNDY
        )
        self.search_entry.pack(side="left", expand=True, fill="x", padx=(0,10))
        
        # Filtro
        self.filter_combo = ctk.CTkComboBox(
            search_frame,
            values=["Todos", "Vinotecas", "Bodegas", "Bares de vino"],
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=Colors.CREAM,
            text_color=Colors.DARK_BURGUNDY,
            button_color=Colors.GOLD,
            button_hover_color=Colors.ACCENT_GOLD,
            dropdown_fg_color=Colors.CREAM
        )
        self.filter_combo.pack(side="left", padx=10)
        
        # Botones
        search_button = AnimatedButton(
            search_frame,
            text="Buscar",
            command=self.search_location,
            width=100,
            height=40
        )
        search_button.pack(side="left", padx=5)
        
        location_button = AnimatedButton(
            search_frame,
            text="Mi Ubicación",
            command=self.go_to_my_location,
            width=120,
            height=40
        )
        location_button.pack(side="left", padx=5)
        
        # Contenedor principal
        main_container = ctk.CTkFrame(
            self,
            fg_color=Colors.LIGHT_BURGUNDY,
            corner_radius=15,
            border_width=2,
            border_color=Colors.GOLD
        )
        main_container.pack(fill="both", expand=True, padx=20, pady=(0,20))
        
        # El mapa se mostrará en el navegador
        self.map_label = ctk.CTkLabel(
            main_container,
            text="El mapa se abrirá en tu navegador web",
            font=ctk.CTkFont(size=16),
            text_color=Colors.CREAM
        )
        self.map_label.pack(pady=20)
        
        # Panel de lugares cercanos
        self.create_nearby_places(main_container)
        
        # Botón de volver
        back_button = AnimatedButton(
            main_container,
            text="Volver al Inicio",
            command=self.back_to_home,
            fg_color=Colors.GOLD,
            text_color=Colors.DARK_BURGUNDY,
            hover_color=Colors.ACCENT_GOLD,
            width=200,
            height=40
        )
        back_button.pack(pady=20)

    def create_nearby_places(self, parent):
        places_frame = ctk.CTkFrame(
            parent,
            fg_color=Colors.DARK_BURGUNDY,
            corner_radius=15,
            border_width=2,
            border_color=Colors.GOLD
        )
        places_frame.pack(fill="x", padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            places_frame,
            text="Lugares Cercanos",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=Colors.GOLD
        )
        title_label.pack(pady=15)
        
        # Lista de lugares con coordenadas
        places = [
            {
                "name": "Vinoteca del Puerto",
                "distance": "0.5 km",
                "rating": "4.5",
                "location": (-38.0034773, -57.5406106)
            },
            {
                "name": "Bodega Los Andes",
                "distance": "1.2 km",
                "rating": "4.8",
                "location": (-38.0074773, -57.5456106)
            },
            {
                "name": "Wine Bar La Cava",
                "distance": "0.8 km",
                "rating": "4.3",
                "location": (-38.0054773, -57.5426106)
            }
        ]
        
        for place in places:
            place_card = PlaceCard(places_frame, place)
            place_card.pack(fill="x", padx=20, pady=5)

    def create_map(self):
        try:
            # Ubicación por defecto
            self.current_location = (-38.0054773, -57.5426106)
            try:
                g = geocoder.ip('me')
                if g.ok:
                    self.current_location = g.latlng
            except:
                pass
            
            # Crear mapa
            self.map = folium.Map(
                location=self.current_location,
                zoom_start=14,
                tiles='CartoDB dark_matter'
            )
            
            # Añadir marcadores
            self.add_markers()
            
            # Guardar mapa
            self.map_file = os.path.join(os.path.dirname(__file__), 'mi_mapa_vino.html')
            self.map.save(self.map_file)
            
            # Abrir en navegador
            webbrowser.open('file://' + os.path.realpath(self.map_file))
            
        except Exception as e:
            ErrorHandler.show_error(f"Error al crear el mapa: {str(e)}", self)

    def add_markers(self):
        places = [
            {
                "name": "Bodega del Puerto",
                "location": (-38.0034773, -57.5406106),
                "rating": 4.5,
                "type": "Vinoteca Premium"
            },
            # Añadir más lugares aquí
        ]
        
        for place in places:
            folium.Marker(
                location=place["location"],
                popup=place["name"],
                icon=folium.Icon(color='darkred', icon='glass', prefix='fa')
            ).add_to(self.map)

    def search_location(self):
        try:
            search_text = self.search_entry.get()
            g = geocoder.osm(search_text)
            if g.ok:
                self.map.location = g.latlng
                self.map.save(self.map_file)
                webbrowser.open('file://' + os.path.realpath(self.map_file))
            else:
                ErrorHandler.show_error("No se encontró la ubicación", self)
        except Exception as e:
            ErrorHandler.show_error(f"Error en la búsqueda: {str(e)}", self)

    def go_to_my_location(self):
        try:
            g = geocoder.ip('me')
            if g.ok:
                self.map.location = g.latlng
                self.map.save(self.map_file)
                webbrowser.open('file://' + os.path.realpath(self.map_file))
            else:
                ErrorHandler.show_error("No se pudo obtener tu ubicación", self)
        except Exception as e:
            ErrorHandler.show_error(f"Error: {str(e)}", self)

    def animate_startup(self):
        def fade_in(widget, alpha=0):
            if alpha < 1:
                widget.attributes('-alpha', alpha)
                self.after(20, lambda: fade_in(widget, alpha + 0.1))
        
        self.attributes('-alpha', 0)
        fade_in(self)

    def back_to_home(self):
        from home import WineAppHomeGUI
        self.window_manager.switch_window(self, WineAppHomeGUI)

if __name__ == "__main__":
    app = WineMapApp()
    app.mainloop()
