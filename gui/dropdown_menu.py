import customtkinter as ctk
import importlib
import inspect
from PIL import Image, ImageTk

# Paleta de colores mejorada
DARK_BURGUNDY = "#2C041C"
LIGHT_BURGUNDY = "#6F1A37"
GOLD = "#C1A87D"
CREAM = "#FFF8E7"
ACCENT_GOLD = "#8B7355"
HOVER_BURGUNDY = "#4A0D2D"

class AnimatedMenuItem(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            corner_radius=10,
            border_width=2,
            border_color="transparent",
            font=ctk.CTkFont(family="Helvetica", size=14)
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.configure(
            border_color=GOLD,
            fg_color=HOVER_BURGUNDY
        )

    def on_leave(self, event):
        self.configure(
            border_color="transparent",
            fg_color="transparent"
        )

class WineAppDropdownMenu(ctk.CTkFrame):
    def __init__(self, master, current_page=None):
        super().__init__(master, fg_color="transparent")
        self.current_page = current_page
        self.is_menu_visible = False
        
        # Cargar iconos
        self.load_icons()
        
        # Botón del menú con animación
        self.menu_button = ctk.CTkButton(
            self,
            text="☰",
            width=45,
            height=45,
            fg_color=LIGHT_BURGUNDY,
            hover_color=GOLD,
            text_color=CREAM,
            corner_radius=10,
            command=self.toggle_menu,
            font=ctk.CTkFont(size=20)
        )
        self.menu_button.pack(side="left", padx=10, pady=10)

        # Marco del borde con efecto de vidrio
        self.border_frame = ctk.CTkFrame(
            self.master,
            fg_color=GOLD,
            corner_radius=15
        )

        # Marco del menú con efecto de vidrio
        self.menu_frame = ctk.CTkFrame(
            self.border_frame,
            fg_color=DARK_BURGUNDY,
            corner_radius=12
        )

        self.create_menu_items()

    def load_icons(self):
        icon_size = (20, 20)
        icons_path = "assets/icons/"
        
        self.icons = {
            "home": self.load_and_resize_image(f"{icons_path}home.png", icon_size),
            "profile": self.load_and_resize_image(f"{icons_path}profile.png", icon_size),
            "upload": self.load_and_resize_image(f"{icons_path}upload.png", icon_size),
            "favorites": self.load_and_resize_image(f"{icons_path}favorite.png", icon_size),
            "support": self.load_and_resize_image(f"{icons_path}support.png", icon_size),
            "logout": self.load_and_resize_image(f"{icons_path}logout.png", icon_size)
        }

    def load_and_resize_image(self, path: str, size: tuple) -> ImageTk.PhotoImage:
        try:
            image = Image.open(path)
            image = image.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error cargando imagen {path}: {e}")
            return None

    def create_menu_items(self):
        menu_items = [
            ("Inicio", "home", "WineAppHomeGUI", "home"),
            ("Perfil", "perfil", "WineAppMobileGUI", "profile"),
            ("Subir Opinión", None, None, "upload"),
            ("Favoritos", "gui.perfil_gui.favs", "WineRatingApp", "favorites"),
            ("Soporte", None, None, "support"),
            ("Cerrar Sesión", "login", None, "logout")
        ]

        for text, module, class_name, icon_key in menu_items:
            command = (
                (lambda m=module, c=class_name: self.navigate_to(m, c))
                if module
                else self.placeholder_command
            )

            menu_item = AnimatedMenuItem(
                self.menu_frame,
                text=f" {text}",
                image=self.icons.get(icon_key),
                command=command,
                fg_color="transparent",
                text_color=CREAM,
                height=45,
                anchor="w"
            )
            menu_item.pack(pady=5, padx=10, fill="x")

        # Botón de cerrar con animación
        close_button = ctk.CTkButton(
            self.menu_frame,
            text="Cerrar Menú",
            command=self.hide_menu,
            fg_color=GOLD,
            hover_color=ACCENT_GOLD,
            text_color=DARK_BURGUNDY,
            height=45,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        close_button.pack(pady=20, padx=10, fill="x", side="bottom")

    def toggle_menu(self):
        if self.is_menu_visible:
            self.hide_menu()
        else:
            self.show_menu()

    def show_menu(self):
        self.border_frame.place(relx=0.05, rely=0.1, relwidth=0.3, relheight=0.8)
        self.menu_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Animación de aparición
        self.border_frame.lift()
        self.animate_menu_show()
        self.is_menu_visible = True

    def hide_menu(self):
        # Animación de desaparición
        self.animate_menu_hide()

    def animate_menu_show(self):
        def animate(alpha=0):
            if alpha <= 1:
                self.border_frame.configure(fg_color=(f"#{int(193*alpha):02x}", f"#{int(168*alpha):02x}", f"#{int(125*alpha):02x}"))
                self.after(20, lambda: animate(alpha + 0.1))
        animate()

    def animate_menu_hide(self):
        def animate(alpha=1):
            if alpha >= 0:
                self.border_frame.configure(fg_color=(f"#{int(193*alpha):02x}", f"#{int(168*alpha):02x}", f"#{int(125*alpha):02x}"))
                if alpha <= 0:
                    self.border_frame.place_forget()
                    self.is_menu_visible = False
                else:
                    self.after(20, lambda: animate(alpha - 0.1))
        animate()

    def navigate_to(self, module_name, class_name):
        self.hide_menu()
        if self.current_page:
            self.current_page.destroy()

        module = importlib.import_module(module_name)
        if class_name:
            class_ = getattr(module, class_name)
            new_page = (
                class_(self.master)
                if "master" in inspect.signature(class_.__init__).parameters
                else class_()
            )
            new_page.pack(fill="both", expand=True)
            self.current_page = new_page
        else:
            self.master.destroy()
            module.app_login.mainloop()

    def placeholder_command(self):
        print("Esta función aún no está implementada")
