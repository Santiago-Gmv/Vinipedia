import customtkinter as ctk
from styles import Colors
from components import AnimatedButton
from utils import WindowManager

class WineRatingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.window_manager = WindowManager()
        self.title("Clasificación de Vinos")
        self.geometry("1300x800")
        self.configure(fg_color=Colors.DARK_BURGUNDY)
        self.center_window()
        self.create_widgets()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1300) // 2
        y = (screen_height - 800) // 2
        self.geometry(f"1300x800+{x}+{y}")

    def create_widgets(self):
        # Título
        title_label = ctk.CTkLabel(
            self, 
            text="Clasificación de Vinos", 
            font=("Helvetica", 28, "bold"), 
            text_color=Colors.GOLD
        )
        title_label.pack(pady=20)

        # Cuadro de búsqueda
        search_frame = ctk.CTkFrame(
            self, 
            fg_color=Colors.LIGHT_BURGUNDY, 
            corner_radius=10
        )
        search_frame.pack(fill="x", padx=20, pady=10)

        search_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Buscar vino...", 
            font=("Helvetica", 14), 
            corner_radius=10, 
            text_color=Colors.CREAM, 
            fg_color=Colors.LIGHT_BURGUNDY, 
            placeholder_text_color=Colors.GOLD
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=(10, 0), pady=10)

        search_button = ctk.CTkButton(
            search_frame, 
            text="Buscar", 
            corner_radius=10, 
            fg_color=Colors.GOLD, 
            hover_color=Colors.ACCENT_GOLD, 
            font=("Helvetica", 14), 
            text_color=Colors.DARK_BURGUNDY
        )
        search_button.pack(side="right", padx=10)

        # Contenedor de vinos
        wine_frame = ctk.CTkFrame(
            self, 
            fg_color=Colors.LIGHT_BURGUNDY, 
            corner_radius=10
        )
        wine_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.wines = ["Cabernet Sauvignon", "Merlot", "Pinot Noir", "Chardonnay", "Sauvignon Blanc"]
        self.ratings = {wine: 0 for wine in self.wines}
        self.star_labels = {}

        for wine in self.wines:
            wine_container = ctk.CTkFrame(
                wine_frame, 
                fg_color=Colors.DARK_BURGUNDY, 
                corner_radius=10
            )
            wine_container.pack(fill="x", padx=10, pady=5)

            wine_label = ctk.CTkLabel(
                wine_container, 
                text=wine, 
                font=("Helvetica", 18), 
                text_color=Colors.CREAM
            )
            wine_label.pack(side="left", padx=10)

            stars_frame = ctk.CTkFrame(
                wine_container, 
                fg_color=Colors.DARK_BURGUNDY
            )
            stars_frame.pack(side="right", padx=10)

            self.star_labels[wine] = []
            for i in range(5):
                star = ctk.CTkLabel(
                    stars_frame, 
                    text="★", 
                    font=("Helvetica", 24), 
                    text_color=Colors.GOLD if i < self.ratings[wine] else Colors.CREAM
                )
                star.pack(side="left", padx=2)
                star.bind("<Button-1>", lambda e, w=wine, r=i+1: self.rate_wine(w, r))
                self.star_labels[wine].append(star)

        action_button = ctk.CTkButton(
            self, 
            text="Guardar Clasificación", 
            corner_radius=10, 
            fg_color=Colors.GOLD, 
            hover_color=Colors.ACCENT_GOLD, 
            font=("Helvetica", 16, "bold"), 
            text_color=Colors.DARK_BURGUNDY
        )
        action_button.pack(pady=20)

        # Botón de volver
        back_button = AnimatedButton(
            self,
            text="Volver al Inicio",
            command=self.back_to_home,
            fg_color=Colors.GOLD,
            text_color=Colors.DARK_BURGUNDY,
            hover_color=Colors.ACCENT_GOLD,
            width=200,
            height=40
        )
        back_button.pack(pady=20)

        self.update_ratings()

    def rate_wine(self, wine, rating):
        self.ratings[wine] = rating
        self.update_ratings()

    def update_ratings(self):
        for wine in self.wines:
            stars = self.ratings.get(wine, 0)
            for i in range(5):
                self.star_labels[wine][i].configure(
                    text_color=Colors.GOLD if i < stars else Colors.CREAM
                )

    def back_to_home(self):
        from home import WineAppHomeGUI
        self.window_manager.switch_window(self, WineAppHomeGUI)

if __name__ == "__main__":
    app = WineRatingApp()
    app.mainloop()