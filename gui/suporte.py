import customtkinter as ctk
from PIL import Image, ImageTk
from styles import Colors, Fonts
from utils import WindowManager, ErrorHandler, NotificationManager
from components import AnimatedButton

class SupportTicket(ctk.CTkFrame):
    def __init__(self, master, ticket_data, **kwargs):
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
        
        # Header con título y estado
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x")
        
        # Icono y título
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        
        icon_label = ctk.CTkLabel(
            title_frame,
            text=ticket_data["icon"],
            font=ctk.CTkFont(size=24),
            text_color=Colors.GOLD
        )
        icon_label.pack(side="left", padx=5)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text=ticket_data["title"],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=Colors.CREAM
        )
        title_label.pack(side="left", padx=5)
        
        # Estado y fecha
        info_frame = ctk.CTkFrame(header, fg_color="transparent")
        info_frame.pack(side="right")
        
        status_label = ctk.CTkLabel(
            info_frame,
            text=f"Estado: {ticket_data['status']}",
            font=ctk.CTkFont(size=12),
            text_color=self.get_status_color(ticket_data['status'])
        )
        status_label.pack(side="left", padx=10)
        
        date_label = ctk.CTkLabel(
            info_frame,
            text=ticket_data["date"],
            font=ctk.CTkFont(size=12),
            text_color=Colors.GOLD
        )
        date_label.pack(side="right")
        
        # Descripción si existe
        if "description" in ticket_data:
            desc_label = ctk.CTkLabel(
                content,
                text=ticket_data["description"],
                font=ctk.CTkFont(size=14),
                text_color=Colors.CREAM,
                wraplength=600
            )
            desc_label.pack(pady=(10,0), anchor="w")
        
        # Botones de acción
        self.create_action_buttons(content, ticket_data)
        
        # Animaciones
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def get_status_color(self, status):
        status_colors = {
            "Pendiente": "#FFA500",  # Naranja
            "En proceso": "#4CAF50",  # Verde
            "Resuelto": Colors.GOLD,
            "Cerrado": Colors.CREAM
        }
        return status_colors.get(status, Colors.CREAM)

    def create_action_buttons(self, parent, ticket_data):
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10,0))
        
        if ticket_data["status"] != "Cerrado":
            reply_button = AnimatedButton(
                button_frame,
                text="Responder",
                width=100,
                height=30,
                fg_color=Colors.GOLD,
                text_color=Colors.DARK_BURGUNDY,
                hover_color=Colors.ACCENT_GOLD
            )
            reply_button.pack(side="right", padx=5)
        
        view_button = AnimatedButton(
            button_frame,
            text="Ver detalles",
            width=100,
            height=30,
            fg_color="transparent",
            text_color=Colors.CREAM,
            hover_color=Colors.HOVER_BURGUNDY,
            border_width=2,
            border_color=Colors.GOLD
        )
        view_button.pack(side="right", padx=5)

    def on_enter(self, event):
        self.configure(border_color=Colors.ACCENT_GOLD)
        
    def on_leave(self, event):
        self.configure(border_color=Colors.GOLD)

class Formulario(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.window_manager = WindowManager()
        self.title("Soporte - ViniPedia")
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
        # Contenedor principal con scroll
        main_container = ctk.CTkScrollableFrame(
            self,
            fg_color=Colors.LIGHT_BURGUNDY,
            corner_radius=20,
            border_width=2,
            border_color=Colors.GOLD
        )
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_container)
        
        # Formulario de contacto
        self.create_contact_form(main_container)
        
        # Historial de tickets
        self.create_ticket_history(main_container)
        
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

    def create_header(self, parent):
        header_frame = ctk.CTkFrame(
            parent,
            fg_color=Colors.DARK_BURGUNDY,
            corner_radius=15,
            height=120
        )
        header_frame.pack(fill="x", pady=20)
        
        # Logo y título
        try:
            logo_image = Image.open("assets/support_icon.png")
            logo_image = logo_image.resize((60, 60))
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = ctk.CTkLabel(
                header_frame,
                image=self.logo_photo,
                text=""
            )
            logo_label.pack(pady=(20,5))
        except:
            pass
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Centro de Soporte",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=Colors.GOLD
        )
        title_label.pack(pady=5)
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Estamos aquí para ayudarte",
            font=ctk.CTkFont(size=16),
            text_color=Colors.CREAM
        )
        subtitle_label.pack(pady=(0,20))

    def create_contact_form(self, parent):
        form_frame = ctk.CTkFrame(
            parent,
            fg_color=Colors.DARK_BURGUNDY,
            corner_radius=15,
            border_width=2,
            border_color=Colors.GOLD
        )
        form_frame.pack(fill="x", pady=20)
        
        form_title = ctk.CTkLabel(
            form_frame,
            text="Nuevo Ticket de Soporte",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=Colors.GOLD
        )
        form_title.pack(pady=20)
        
        # Campos del formulario
        fields = [
            ("Asunto", "entry"),
            ("Categoría", "combobox", ["General", "Técnico", "Facturación", "Otro"]),
            ("Prioridad", "combobox", ["Normal", "Alta", "Urgente"]),
            ("Mensaje", "textbox")
        ]
        
        for field_name, field_type, *args in fields:
            label = ctk.CTkLabel(
                form_frame,
                text=field_name,
                font=ctk.CTkFont(size=14),
                text_color=Colors.CREAM
            )
            label.pack(padx=20, pady=(10,0), anchor="w")
            
            if field_type == "entry":
                widget = ctk.CTkEntry(
                    form_frame,
                    height=40,
                    font=ctk.CTkFont(size=14),
                    fg_color=Colors.CREAM,
                    text_color=Colors.DARK_BURGUNDY,
                    border_color=Colors.GOLD,
                    corner_radius=8
                )
            elif field_type == "combobox":
                widget = ctk.CTkComboBox(
                    form_frame,
                    values=args[0],
                    height=40,
                    font=ctk.CTkFont(size=14),
                    fg_color=Colors.CREAM,
                    text_color=Colors.DARK_BURGUNDY,
                    border_color=Colors.GOLD,
                    button_color=Colors.GOLD,
                    button_hover_color=Colors.ACCENT_GOLD,
                    dropdown_fg_color=Colors.CREAM,
                    dropdown_text_color=Colors.DARK_BURGUNDY,
                    dropdown_hover_color=Colors.LIGHT_BURGUNDY
                )
            else:  # textbox
                widget = ctk.CTkTextbox(
                    form_frame,
                    height=150,
                    font=ctk.CTkFont(size=14),
                    fg_color=Colors.CREAM,
                    text_color=Colors.DARK_BURGUNDY,
                    border_color=Colors.GOLD,
                    corner_radius=8
                )
            
            widget.pack(fill="x", padx=20, pady=(5,10))
        
        # Botón de enviar
        send_button = AnimatedButton(
            form_frame,
            text="Enviar Ticket",
            command=self.submit_ticket,
            fg_color=Colors.GOLD,
            text_color=Colors.DARK_BURGUNDY,
            hover_color=Colors.ACCENT_GOLD,
            width=200,
            height=45
        )
        send_button.pack(pady=20)

    def create_ticket_history(self, parent):
        history_frame = ctk.CTkFrame(
            parent,
            fg_color=Colors.DARK_BURGUNDY,
            corner_radius=15,
            border_width=2,
            border_color=Colors.GOLD
        )
        history_frame.pack(fill="x", pady=20)
        
        history_title = ctk.CTkLabel(
            history_frame,
            text="Historial de Tickets",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=Colors.GOLD
        )
        history_title.pack(pady=20)
        
        # Ejemplo de tickets
        tickets = [
            {
                "icon": "🔧",
                "title": "Problema técnico con la app",
                "status": "En proceso",
                "date": "Hoy",
                "description": "La aplicación se cierra inesperadamente..."
            },
            {
                "icon": "💳",
                "title": "Consulta sobre facturación",
                "status": "Resuelto",
                "date": "Ayer",
                "description": "No puedo ver mi última factura..."
            },
            {
                "icon": "❓",
                "title": "Pregunta general",
                "status": "Pendiente",
                "date": "Hace 2 días",
                "description": "¿Cómo puedo cambiar mi contraseña?"
            }
        ]
        
        for ticket in tickets:
            ticket_widget = SupportTicket(history_frame, ticket)
            ticket_widget.pack(fill="x", padx=20, pady=5)

    def submit_ticket(self):
        # Implementar lógica de envío
        NotificationManager.show_notification(
            "Ticket enviado exitosamente",
            self
        )

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
    app = Formulario()
    app.mainloop()
