import customtkinter as ctk

DARK_BURGUNDY = "#4A0E0E"
LIGHT_BURGUNDY = "#800020"
GOLD = "#FFD700"
CREAM = "#FFFDD0"

class WineRatingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración del título y tamaño de la ventana
        self.title("Clasificación de Vinos")
        self.geometry("600x700")


        # Configurar el color de fondo de la ventana
        self.configure(fg_color=DARK_BURGUNDY)

        self.create_widgets()

    def create_widgets(self):
        # Título
        title_label = ctk.CTkLabel(self, text="Clasificación de Vinos", font=("Helvetica", 28, "bold"), text_color=GOLD)
        title_label.pack(pady=20)

        # Cuadro de búsqueda
        search_frame = ctk.CTkFrame(self, fg_color=LIGHT_BURGUNDY, corner_radius=10)
        search_frame.pack(fill="x", padx=20, pady=10)

        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar vino...", font=("Helvetica", 14), corner_radius=10, text_color=CREAM, fg_color=LIGHT_BURGUNDY, placeholder_text_color=GOLD)
        search_entry.pack(side="left", fill="x", expand=True, padx=(10, 0), pady=10)

        search_button = ctk.CTkButton(search_frame, text="Buscar", corner_radius=10, fg_color=GOLD, hover_color=CREAM, font=("Helvetica", 14), text_color=DARK_BURGUNDY)
        search_button.pack(side="right", padx=10)

        # Contenedor de vinos
        wine_frame = ctk.CTkFrame(self, fg_color=LIGHT_BURGUNDY, corner_radius=10)
        wine_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.wines = ["Cabernet Sauvignon", "Merlot", "Pinot Noir", "Chardonnay", "Sauvignon Blanc"]
        self.ratings = {wine: 0 for wine in self.wines}
        self.star_labels = {}

        for wine in self.wines:
            wine_container = ctk.CTkFrame(wine_frame, fg_color=DARK_BURGUNDY, corner_radius=10)
            wine_container.pack(fill="x", padx=10, pady=5)

            wine_label = ctk.CTkLabel(wine_container, text=wine, font=("Helvetica", 18), text_color=CREAM)
            wine_label.pack(side="left", padx=10)

            stars_frame = ctk.CTkFrame(wine_container, fg_color=DARK_BURGUNDY)
            stars_frame.pack(side="right", padx=10)

            self.star_labels[wine] = []
            for i in range(5):
                star = ctk.CTkLabel(stars_frame, text="★", font=("Helvetica", 24), text_color=GOLD if i < self.ratings[wine] else CREAM)
                star.pack(side="left", padx=2)
                star.bind("<Button-1>", lambda e, w=wine, r=i+1: self.rate_wine(w, r))
                self.star_labels[wine].append(star)

        action_button = ctk.CTkButton(self, text="Guardar Clasificación", corner_radius=10, fg_color=GOLD, hover_color=CREAM, font=("Helvetica", 16, "bold"), text_color=DARK_BURGUNDY)
        action_button.pack(pady=20)

        self.update_ratings()

    def rate_wine(self, wine, rating):
        self.ratings[wine] = rating
        self.update_ratings()

    def update_ratings(self):
        for wine in self.wines:
            stars = self.ratings.get(wine, 0)
            for i in range(5):
                self.star_labels[wine][i].configure(text_color=GOLD if i < stars else CREAM)

if __name__ == "__main__":
    app = WineRatingApp()
    app.mainloop()