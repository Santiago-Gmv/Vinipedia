import customtkinter as ctk
from PIL import Image, ImageTk
import sqlite3
from styles import Colors, Fonts
from utils import ErrorHandler, NotificationManager, WindowManager

class AnimatedEntry(ctk.CTkEntry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_border_color = kwargs.get("border_color", Colors.GOLD)
        self.configure(
            corner_radius=10,
            border_width=2,
            border_color=self.default_border_color,
            height=45,
            font=ctk.CTkFont(family="Helvetica", size=14)
        )
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

    def on_focus_in(self, event):
        self.configure(border_color=Colors.ACCENT_GOLD)

    def on_focus_out(self, event):
        self.configure(border_color=self.default_border_color)

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.window_manager = WindowManager()
        
        # Configuración básica
        self.title("ViniPedia")
        self.geometry("1000x600")
        self.configure(fg_color=Colors.DARK_BURGUNDY)
        
        # Centrar la ventana
        self.center_window()
        
        # Crear contenedor principal con efecto de vidrio
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=Colors.LIGHT_BURGUNDY,
            corner_radius=20,
            border_width=2,
            border_color=Colors.GOLD
        )
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
        
        # Crear layout
        self.create_layout()
        
        # Animación de inicio
        self.animate_startup()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1000) // 2
        y = (screen_height - 600) // 2
        self.geometry(f"1000x600+{x}+{y}")

    def create_layout(self):
        # Panel izquierdo (decorativo)
        left_panel = ctk.CTkFrame(
            self.main_frame,
            fg_color=Colors.DARK_BURGUNDY,
            corner_radius=15,
            border_width=2,
            border_color=Colors.GOLD
        )
        left_panel.place(relx=0.02, rely=0.02, relwidth=0.46, relheight=0.96)
        
        # Cargar y mostrar logo
        try:
            logo_image = Image.open("assets/logo.png")
            logo_image = logo_image.resize((200, 200))
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = ctk.CTkLabel(
                left_panel,
                image=self.logo_photo,
                text=""
            )
            logo_label.pack(pady=(50,20))
        except:
            # Fallback si no hay logo
            logo_text = ctk.CTkLabel(
                left_panel,
                text="🍷",
                font=ctk.CTkFont(size=80),
                text_color=Colors.GOLD
            )
            logo_text.pack(pady=(50,20))

        # Título y subtítulo
        title = ctk.CTkLabel(
            left_panel,
            text="ViniPedia",
            font=ctk.CTkFont(family="Helvetica", size=40, weight="bold"),
            text_color=Colors.GOLD
        )
        title.pack(pady=10)
        
        subtitle = ctk.CTkLabel(
            left_panel,
            text="Tu guía experta en el mundo del vino",
            font=ctk.CTkFont(size=16),
            text_color=Colors.CREAM
        )
        subtitle.pack()

        # Panel derecho (login)
        right_panel = ctk.CTkFrame(
            self.main_frame,
            fg_color=Colors.DARK_BURGUNDY,
            corner_radius=15,
            border_width=2,
            border_color=Colors.GOLD
        )
        right_panel.place(relx=0.52, rely=0.02, relwidth=0.46, relheight=0.96)
        
        # Formulario de login
        login_title = ctk.CTkLabel(
            right_panel,
            text="Iniciar Sesión",
            font=ctk.CTkFont(family="Helvetica", size=32, weight="bold"),
            text_color=Colors.GOLD
        )
        login_title.pack(pady=(50,30))
        
        # Campos de entrada
        self.username_entry = AnimatedEntry(
            right_panel,
            placeholder_text="👤 Usuario",
            fg_color=Colors.CREAM,
            text_color=Colors.DARK_BURGUNDY,
            placeholder_text_color=Colors.LIGHT_BURGUNDY
        )
        self.username_entry.pack(pady=10, padx=40, fill="x")
        
        self.password_entry = AnimatedEntry(
            right_panel,
            placeholder_text="🔒 Contraseña",
            show="•",
            fg_color=Colors.CREAM,
            text_color=Colors.DARK_BURGUNDY,
            placeholder_text_color=Colors.LIGHT_BURGUNDY
        )
        self.password_entry.pack(pady=10, padx=40, fill="x")
        
        # Botones
        login_button = ctk.CTkButton(
            right_panel,
            text="Iniciar Sesión",
            command=self.login,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=Colors.GOLD,
            text_color=Colors.DARK_BURGUNDY,
            hover_color=Colors.ACCENT_GOLD,
            height=45,
            corner_radius=10
        )
        login_button.pack(pady=20, padx=40, fill="x")
        
        register_button = ctk.CTkButton(
            right_panel,
            text="Crear Cuenta",
            command=self.show_register,
            font=ctk.CTkFont(size=16),
            fg_color="transparent",
            text_color=Colors.CREAM,
            hover_color=Colors.HOVER_BURGUNDY,
            height=45,
            corner_radius=10,
            border_width=2,
            border_color=Colors.GOLD
        )
        register_button.pack(pady=10, padx=40, fill="x")
        
        # Enlace de recuperación
        forgot_password = ctk.CTkLabel(
            right_panel,
            text="¿Olvidaste tu contraseña?",
            font=ctk.CTkFont(size=14),
            text_color=Colors.GOLD,
            cursor="hand2"
        )
        forgot_password.pack(pady=20)
        forgot_password.bind("<Button-1>", lambda e: self.forgot_password())

    def animate_startup(self):
        def fade_in(widget, alpha=0):
            if alpha < 1:
                widget.attributes('-alpha', alpha)
                self.after(20, lambda: fade_in(widget, alpha + 0.1))
        
        self.attributes('-alpha', 0)
        fade_in(self)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username and password:  # Por ahora, solo verificamos que no estén vacíos
            from gui.home import WineAppHomeGUI  # Importación local para evitar circular
            self.window_manager.switch_window(self, WineAppHomeGUI)
        else:
            ErrorHandler.show_error("Por favor, complete todos los campos", self)

    def show_register(self):
        register_window = RegisterWindow(self)
        register_window.grab_set()

    def forgot_password(self):
        NotificationManager.show_notification(
            "Se ha enviado un correo de recuperación",
            self
        )

class RegisterWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registro - ViniPedia")
        self.geometry("500x600")
        self.configure(fg_color=Colors.DARK_BURGUNDY)
        
        # Contenedor principal
        main_frame = ctk.CTkFrame(
            self,
            fg_color=Colors.LIGHT_BURGUNDY,
            corner_radius=20,
            border_width=2,
            border_color=Colors.GOLD
        )
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="Crear Cuenta",
            font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"),
            text_color=Colors.GOLD
        )
        title.pack(pady=20)
        
        # Campos de registro
        fields = [
            ("👤 Nombre completo", "name"),
            ("📧 Correo electrónico", "email"),
            ("🔑 Nombre de usuario", "username"),
            ("🔒 Contraseña", "password"),
            ("🔒 Confirmar contraseña", "confirm_password")
        ]
        
        self.entries = {}
        for placeholder, key in fields:
            entry = AnimatedEntry(
                main_frame,
                placeholder_text=placeholder,
                font=ctk.CTkFont(size=14),
                fg_color=Colors.CREAM,
                text_color=Colors.DARK_BURGUNDY,
                placeholder_text_color=Colors.LIGHT_BURGUNDY,
                show="•" if "password" in key else ""
            )
            entry.pack(pady=10, padx=30, fill="x")
            self.entries[key] = entry
        
        # Botón de registro
        register_button = ctk.CTkButton(
            main_frame,
            text="Registrarse",
            command=self.register,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=Colors.GOLD,
            text_color=Colors.DARK_BURGUNDY,
            hover_color=Colors.ACCENT_GOLD,
            height=45,
            corner_radius=10
        )
        register_button.pack(pady=20, padx=30, fill="x")

    def register(self):
        # Implementar lógica de registro aquí
        pass
