import customtkinter as ctk
from PIL import Image, ImageTk
import os
from styles import Colors, Fonts
from utils import ErrorHandler, NotificationManager
from components import AnimatedButton

class ProfileStatCard(ctk.CTkFrame):
    def __init__(self, master, title, value, icon=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.configure(
            fg_color=Colors.LIGHT_BURGUNDY,
            corner_radius=20,
            border_width=2,
            border_color=Colors.GOLD
        )
        
        # Contenedor principal
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Icono
        if icon:
            icon_label = ctk.CTkLabel(
                content_frame,
                text=icon,
                font=ctk.CTkFont(size=32),
                text_color=Colors.GOLD
            )
            icon_label.pack(pady=(0,5))
        
        # Valor
        value_label = ctk.CTkLabel(
            content_frame,
            text=str(value),
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=Colors.GOLD
        )
        value_label.pack()
        
        # Título
        title_label = ctk.CTkLabel(
            content_frame,
            text=title,
            font=ctk.CTkFont(size=14),
            text_color=Colors.CREAM
        )
        title_label.pack()
        
        # Animaciones
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, event):
        self.configure(border_color=Colors.ACCENT_GOLD)
        self.lift()
    
    def on_leave(self, event):
        self.configure(border_color=Colors.GOLD)

class ActivityCard(ctk.CTkFrame):
    def __init__(self, master, activity_data, **kwargs):
        super().__init__(master, **kwargs)
        
        self.configure(
            fg_color=Colors.DARK_BURGUNDY,
            corner_radius=15,
            border_width=2,
            border_color=Colors.GOLD
        )
        
        # Contenedor principal
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Icono y título en la misma línea
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x")
        
        icon_label = ctk.CTkLabel(
            header,
            text=activity_data["icon"],
            font=ctk.CTkFont(size=24),
            text_color=Colors.GOLD
        )
        icon_label.pack(side="left", padx=5)
        
        title_label = ctk.CTkLabel(
            header,
            text=activity_data["title"],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=Colors.CREAM
        )
        title_label.pack(side="left", padx=5)
        
        # Fecha
        date_label = ctk.CTkLabel(
            header,
            text=activity_data["date"],
            font=ctk.CTkFont(size=12),
            text_color=Colors.GOLD
        )
        date_label.pack(side="right", padx=5)
        
        # Descripción
        if "description" in activity_data:
            desc_label = ctk.CTkLabel(
                content,
                text=activity_data["description"],
                font=ctk.CTkFont(size=14),
                text_color=Colors.CREAM,
                wraplength=300
            )
            desc_label.pack(pady=(5,0))

class WineAppMobileGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración básica
        self.title("Perfil - ViniPedia")
        self.geometry("1300x800")
        self.configure(fg_color=Colors.DARK_BURGUNDY)
        
        # Centrar ventana
        self.center_window()
        
        # Crear layout principal
        self.create_layout()
        
        # Animación de inicio
        self.animate_startup()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1300) // 2
        y = (screen_height - 800) // 2
        self.geometry(f"1300x800+{x}+{y}")

    def create_layout(self):
        # Contenedor principal (sin scroll)
        main_container = ctk.CTkFrame(
            self,
            fg_color=Colors.LIGHT_BURGUNDY,
            corner_radius=20,
            border_width=2,
            border_color=Colors.GOLD
        )
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header (fuera del scroll)
        self.create_header(main_container)
        
        # Contenedor con scroll para el contenido
        content_scroll = ctk.CTkScrollableFrame(
            main_container,
            fg_color="transparent"
        )
        content_scroll.pack(fill="both", expand=True, padx=20, pady=(0,20))
        
        # Contenedor para el contenido
        content_frame = ctk.CTkFrame(content_scroll, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        content_frame.grid_columnconfigure(0, weight=2)
        content_frame.grid_columnconfigure(1, weight=3)
        
        # Panel izquierdo (stats y actividad)
        left_panel = ctk.CTkFrame(
            content_frame,
            fg_color=Colors.DARK_BURGUNDY,
            corner_radius=15,
            border_width=2,
            border_color=Colors.GOLD
        )
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0,10))
        
        self.create_stats(left_panel)
        self.create_recent_activity(left_panel)
        
        # Panel derecho (colección de vinos)
        right_panel = ctk.CTkFrame(
            content_frame,
            fg_color=Colors.DARK_BURGUNDY,
            corner_radius=15,
            border_width=2,
            border_color=Colors.GOLD
        )
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        self.create_wine_collection(right_panel)
        
        # Botón de volver (fuera del scroll)
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

    def create_header(self, parent):
        header_frame = ctk.CTkFrame(
            parent,
            fg_color=Colors.DARK_BURGUNDY,
            corner_radius=15,
            height=200,
            border_width=2,
            border_color=Colors.GOLD
        )
        header_frame.pack(fill="x", padx=20, pady=20)
        
        # Contenedor para foto y nombre
        profile_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        profile_container.pack(side="left", padx=30, pady=20)
        
        # Foto de perfil
        try:
            profile_image = Image.open("assets/profile.png")
            profile_image = profile_image.resize((150, 150))
            self.profile_photo = ImageTk.PhotoImage(profile_image)
            photo_label = ctk.CTkLabel(
                profile_container,
                image=self.profile_photo,
                text=""
            )
        except:
            # Fallback si no hay foto
            photo_label = ctk.CTkLabel(
                profile_container,
                text="👤",
                font=ctk.CTkFont(size=80),
                text_color=Colors.GOLD
            )
        photo_label.pack()
        
        # Información del usuario
        info_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_container.pack(side="left", fill="both", expand=True, pady=20)
        
        name_label = ctk.CTkLabel(
            info_container,
            text="Juan Pérez",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=Colors.GOLD
        )
        name_label.pack(anchor="w")
        
        title_label = ctk.CTkLabel(
            info_container,
            text="Sommelier Amateur",
            font=ctk.CTkFont(size=18),
            text_color=Colors.CREAM
        )
        title_label.pack(anchor="w")
        
        bio_label = ctk.CTkLabel(
            info_container,
            text="Apasionado por los vinos tintos y la cultura vitivinícola.",
            font=ctk.CTkFont(size=14),
            text_color=Colors.CREAM,
            wraplength=400
        )
        bio_label.pack(anchor="w", pady=(10,0))
        
        # Botones de acción
        button_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        button_container.pack(side="right", padx=30, pady=20)
        
        edit_button = AnimatedButton(
            button_container,
            text="Editar Perfil",
            width=150,
            height=40,
            fg_color=Colors.GOLD,
            text_color=Colors.DARK_BURGUNDY,
            hover_color=Colors.ACCENT_GOLD
        )
        edit_button.pack(pady=5)
        
        settings_button = AnimatedButton(
            button_container,
            text="Configuración",
            width=150,
            height=40,
            fg_color="transparent",
            text_color=Colors.CREAM,
            hover_color=Colors.HOVER_BURGUNDY,
            border_width=2,
            border_color=Colors.GOLD
        )
        settings_button.pack(pady=5)

    def create_stats(self, parent):
        stats_label = ctk.CTkLabel(
            parent,
            text="Estadísticas",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=Colors.GOLD
        )
        stats_label.pack(pady=20)
        
        stats_container = ctk.CTkFrame(parent, fg_color="transparent")
        stats_container.pack(fill="x", padx=20)
        stats_container.grid_columnconfigure((0,1), weight=1)
        
        stats_data = [
            ("Reseñas", "124", "📝"),
            ("Favoritos", "45", "❤️"),
            ("Seguidores", "89", "👥"),
            ("Siguiendo", "56", "🤝")
        ]
        
        for i, (title, value, icon) in enumerate(stats_data):
            card = ProfileStatCard(
                stats_container,
                title,
                value,
                icon,
                width=150,
                height=120
            )
            card.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="nsew")

    def create_recent_activity(self, parent):
        activity_label = ctk.CTkLabel(
            parent,
            text="Actividad Reciente",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=Colors.GOLD
        )
        activity_label.pack(pady=20)
        
        activities = [
            {
                "icon": "🍷",
                "title": "Reseñó Malbec Reserve 2018",
                "date": "Hoy",
                "description": "Un vino excepcional con notas a frutos rojos..."
            },
            {
                "icon": "❤️",
                "title": "Añadió a favoritos",
                "date": "Ayer",
                "description": "Cabernet Sauvignon 2019"
            },
            {
                "icon": "🏆",
                "title": "Logro desbloqueado",
                "date": "Hace 2 días",
                "description": "¡Catador Experto!"
            }
        ]
        
        for activity in activities:
            card = ActivityCard(parent, activity)
            card.pack(fill="x", padx=20, pady=5)

    def create_wine_collection(self, parent):
        collection_label = ctk.CTkLabel(
            parent,
            text="Mi Colección",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=Colors.GOLD
        )
        collection_label.pack(pady=20)
        
        # Aquí irían las tarjetas de vinos...

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
    app = WineAppMobileGUI()
    app.mainloop()
