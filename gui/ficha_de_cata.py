import customtkinter as ctk
from PIL import Image, ImageTk
from styles import Colors, Fonts
from utils import WindowManager, ErrorHandler, NotificationManager
from components import AnimatedButton

class RatingStars(ctk.CTkFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.command = command
        self.rating = 0
        self.stars = []
        
        for i in range(5):
            star = ctk.CTkButton(
                self,
                text="★",
                width=30,
                height=30,
                fg_color="transparent",
                text_color=Colors.CREAM,
                hover_color=Colors.HOVER_BURGUNDY,
                font=ctk.CTkFont(size=24),
                command=lambda x=i+1: self.set_rating(x)
            )
            star.pack(side="left", padx=2)
            self.stars.append(star)

    def set_rating(self, value):
        self.rating = value
        for i, star in enumerate(self.stars):
            star.configure(text_color=Colors.GOLD if i < value else Colors.CREAM)
        if self.command:
            self.command(value)

class FormularioCataVino(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.window_manager = WindowManager()
        self.title("Ficha de Cata - ViniPedia")
        self.geometry("1300x800")
        self.configure(fg_color=Colors.DARK_BURGUNDY)
        self.center_window()
        self.create_layout()
        self.animate_startup()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1300) // 2
        y = (screen_height - 800) // 2
        self.geometry(f"1300x800+{x}+{y}")

    def create_layout(self):
        main_container = ctk.CTkScrollableFrame(
            self,
            fg_color=Colors.LIGHT_BURGUNDY,
            corner_radius=20,
            border_width=2,
            border_color=Colors.GOLD
        )
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.create_header(main_container)
        
        self.create_wine_info(main_container)
        
        self.create_visual_phase(main_container)
        self.create_nose_phase(main_container)
        self.create_taste_phase(main_container)
        
        self.create_conclusion(main_container)
        
        self.create_action_buttons(main_container)

    def create_header(self, parent):
        header_frame = ctk.CTkFrame(
            parent,
            fg_color=Colors.DARK_BURGUNDY,
            corner_radius=15,
            height=120,
            border_width=2,
            border_color=Colors.GOLD
        )
        header_frame.pack(fill="x", pady=20)
        
        try:
            logo_image = Image.open("assets/wine_glass.png")
            logo_image = logo_image.resize((60, 60))
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = ctk.CTkLabel(
                header_frame,
                image=self.logo_photo,
                text=""
            )
            logo_label.pack(pady=(20,5))
        except:
            logo_text = ctk.CTkLabel(
                header_frame,
                text="🍷",
                font=ctk.CTkFont(size=48),
                text_color=Colors.GOLD
            )
            logo_text.pack(pady=(20,5))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Ficha de Cata",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=Colors.GOLD
        )
        title_label.pack(pady=5)

    def create_wine_info(self, parent):
        info_frame = ctk.CTkFrame(
            parent,
            fg_color=Colors.DARK_BURGUNDY,
            corner_radius=15,
            border_width=2,
            border_color=Colors.GOLD
        )
        info_frame.pack(fill="x", pady=20)
        
        title = ctk.CTkLabel(
            info_frame,
            text="Información del Vino",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=Colors.GOLD
        )
        title.pack(pady=15)
        
        fields = [
            ("Nombre del Vino:", "entry"),
            ("Bodega:", "entry"),
            ("Añada:", "entry"),
            ("D.O.:", "entry"),
            ("Variedad de Uva:", "entry"),
            ("Temperatura de Servicio:", "entry")
        ]
        
        for i, (label_text, field_type) in enumerate(fields):
            label = ctk.CTkLabel(
                info_frame,
                text=label_text,
                font=ctk.CTkFont(size=14),
                text_color=Colors.CREAM
            )
            label.pack(padx=20, pady=(10,0), anchor="w")
            
            entry = ctk.CTkEntry(
                info_frame,
                height=35,
                font=ctk.CTkFont(size=14),
                fg_color=Colors.CREAM,
                text_color=Colors.DARK_BURGUNDY,
                border_color=Colors.GOLD,
                corner_radius=8
            )
            entry.pack(fill="x", padx=20, pady=(5,10))

    def create_visual_phase(self, parent):
        phase_frame = self.create_phase_frame(parent, "Fase Visual")
        
        aspects = [
            ("Limpidez", ["Brillante", "Limpio", "Turbio", "Opaco"]),
            ("Color", ["Amarillo", "Dorado", "Rubí", "Granate", "Púrpura"]),
            ("Intensidad", ["Pálido", "Medio", "Intenso", "Profundo"]),
            ("Viscosidad", ["Fluida", "Media", "Densa", "Muy densa"])
        ]
        
        self.create_aspect_groups(phase_frame, aspects)

    def create_nose_phase(self, parent):
        phase_frame = self.create_phase_frame(parent, "Fase Olfativa")
        
        aspects = [
            ("Intensidad", ["Baja", "Media-baja", "Media", "Alta", "Muy alta"]),
            ("Aromas Primarios", ["Frutal", "Floral", "Herbáceo", "Mineral"]),
            ("Aromas Secundarios", ["Lácteos", "Levaduras", "Pan", "Mantequilla"]),
            ("Aromas Terciarios", ["Madera", "Especias", "Cuero", "Tabaco"])
        ]
        
        self.create_aspect_groups(phase_frame, aspects)

    def create_taste_phase(self, parent):
        phase_frame = self.create_phase_frame(parent, "Fase Gustativa")
        
        aspects = [
            ("Dulzor", ["Seco", "Semiseco", "Semidulce", "Dulce"]),
            ("Acidez", ["Baja", "Media-baja", "Media", "Alta"]),
            ("Taninos", ["Suaves", "Medios", "Firmes", "Astringentes"]),
            ("Cuerpo", ["Ligero", "Medio", "Completo", "Muy completo"]),
            ("Alcohol", ["Bajo", "Medio", "Alto", "Muy alto"]),
            ("Persistencia", ["Corta", "Media", "Larga", "Muy larga"])
        ]
        
        self.create_aspect_groups(phase_frame, aspects)

    def create_phase_frame(self, parent, title):
        frame = ctk.CTkFrame(
            parent,
            fg_color=Colors.DARK_BURGUNDY,
            corner_radius=15,
            border_width=2,
            border_color=Colors.GOLD
        )
        frame.pack(fill="x", pady=20)
        
        title_label = ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=Colors.GOLD
        )
        title_label.pack(pady=15)
        
        return frame

    def create_aspect_groups(self, parent, aspects):
        for aspect, options in aspects:
            group_frame = ctk.CTkFrame(parent, fg_color="transparent")
            group_frame.pack(fill="x", padx=20, pady=10)
            
            label = ctk.CTkLabel(
                group_frame,
                text=aspect,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=Colors.CREAM
            )
            label.pack(anchor="w")
            
            options_frame = ctk.CTkFrame(group_frame, fg_color="transparent")
            options_frame.pack(fill="x", pady=(5,0))
            
            for option in options:
                checkbox = ctk.CTkCheckBox(
                    options_frame,
                    text=option,
                    font=ctk.CTkFont(size=14),
                    text_color=Colors.CREAM,
                    fg_color=Colors.GOLD,
                    hover_color=Colors.ACCENT_GOLD,
                    border_color=Colors.GOLD,
                    checkmark_color=Colors.DARK_BURGUNDY
                )
                checkbox.pack(side="left", padx=10)

    def create_conclusion(self, parent):
        conclusion_frame = ctk.CTkFrame(
            parent,
            fg_color=Colors.DARK_BURGUNDY,
            corner_radius=15,
            border_width=2,
            border_color=Colors.GOLD
        )
        conclusion_frame.pack(fill="x", pady=20)
        
        title = ctk.CTkLabel(
            conclusion_frame,
            text="Conclusión",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=Colors.GOLD
        )
        title.pack(pady=15)
        
        rating_frame = ctk.CTkFrame(conclusion_frame, fg_color="transparent")
        rating_frame.pack(fill="x", padx=20, pady=10)
        
        rating_label = ctk.CTkLabel(
            rating_frame,
            text="Puntuación:",
            font=ctk.CTkFont(size=16),
            text_color=Colors.CREAM
        )
        rating_label.pack(side="left", padx=(0,10))
        
        self.rating_stars = RatingStars(rating_frame)
        self.rating_stars.pack(side="left")
        
        notes_label = ctk.CTkLabel(
            conclusion_frame,
            text="Notas de cata:",
            font=ctk.CTkFont(size=14),
            text_color=Colors.CREAM
        )
        notes_label.pack(padx=20, pady=(10,0), anchor="w")
        
        self.notes_text = ctk.CTkTextbox(
            conclusion_frame,
            height=150,
            font=ctk.CTkFont(size=14),
            fg_color=Colors.CREAM,
            text_color=Colors.DARK_BURGUNDY,
            border_color=Colors.GOLD,
            border_width=2,
            corner_radius=8
        )
        self.notes_text.pack(fill="x", padx=20, pady=10)

    def create_action_buttons(self, parent):
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)
        
        save_button = AnimatedButton(
            button_frame,
            text="Guardar Cata",
            command=self.save_cata,
            fg_color=Colors.GOLD,
            text_color=Colors.DARK_BURGUNDY,
            hover_color=Colors.ACCENT_GOLD,
            width=200,
            height=45
        )
        save_button.pack(side="right", padx=5)
        
        cancel_button = AnimatedButton(
            button_frame,
            text="Cancelar",
            command=self.cancel_cata,
            fg_color="transparent",
            text_color=Colors.CREAM,
            hover_color=Colors.HOVER_BURGUNDY,
            border_width=2,
            border_color=Colors.GOLD,
            width=200,
            height=45
        )
        cancel_button.pack(side="right", padx=5)
        
        back_button = AnimatedButton(
            button_frame,
            text="Volver al Inicio",
            command=self.back_to_home,
            fg_color=Colors.GOLD,
            text_color=Colors.DARK_BURGUNDY,
            hover_color=Colors.ACCENT_GOLD,
            width=200,
            height=40
        )
        back_button.pack(side="left", padx=5)

    def save_cata(self):
        NotificationManager.show_notification(
            "Cata guardada exitosamente",
            self
        )

    def cancel_cata(self):
        self.destroy()

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
    app = FormularioCataVino()
    app.mainloop()

