import customtkinter as ctk


DARK_BURGUNDY = "#4A0E0E"
LIGHT_BURGUNDY = "#800020"
GOLD = "#FFD700"
CREAM = "#FFFDD0"
TEXT_COLOR = "#000000"

class Formulario(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Soporte Al Cliente")
        self.geometry("500x600")  
        self.configure(fg_color=DARK_BURGUNDY)

        
        label_title = ctk.CTkLabel(self, text="Formulario de Soporte al Cliente", font=("Helvetica", 20, "bold"), text_color=GOLD)
        label_title.pack(pady=10)

        
        label_nombre = ctk.CTkLabel(self, text="Nombre:", font=("Helvetica", 14), text_color=CREAM)
        label_nombre.pack(pady=(10, 0), anchor="w", padx=20)
        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Ingrese su nombre", fg_color=CREAM, text_color=TEXT_COLOR)
        self.entry_nombre.pack(pady=(0, 10), padx=20, fill="x")

        
        label_correo = ctk.CTkLabel(self, text="Correo Electrónico:", font=("Helvetica", 14), text_color=CREAM)
        label_correo.pack(pady=(10, 0), anchor="w", padx=20)
        self.entry_correo = ctk.CTkEntry(self, placeholder_text="Ingrese su correo electrónico", fg_color=CREAM, text_color=TEXT_COLOR)
        self.entry_correo.pack(pady=(0, 10), padx=20, fill="x")

        
        label_asunto = ctk.CTkLabel(self, text="Asunto:", font=("Helvetica", 14), text_color=CREAM)
        label_asunto.pack(pady=(10, 0), anchor="w", padx=20)
        self.entry_asunto = ctk.CTkEntry(self, placeholder_text="Ingrese el asunto", fg_color=CREAM, text_color=TEXT_COLOR)
        self.entry_asunto.pack(pady=(0, 10), padx=20, fill="x")

        
        label_mensaje = ctk.CTkLabel(self, text="Mensaje:", font=("Helvetica", 14), text_color=CREAM)
        label_mensaje.pack(pady=(10, 0), anchor="w", padx=20)
        self.text_mensaje = ctk.CTkTextbox(self, height=200, fg_color=CREAM, text_color=TEXT_COLOR)  # Aumenté la altura a 200
        self.text_mensaje.pack(pady=(0, 10), padx=20, fill="both", expand=True)

        btn_enviar = ctk.CTkButton(self, text="Enviar", command=self.enviar, fg_color=LIGHT_BURGUNDY, hover_color=DARK_BURGUNDY, text_color=CREAM)
        btn_enviar.pack(pady=10, padx=20, side="bottom", anchor="s")

    def enviar(self):
        print("Datos enviados:")
        print(f"Nombre: {self.entry_nombre.get()}")
        print(f"Correo Electrónico: {self.entry_correo.get()}")
        print(f"Asunto: {self.entry_asunto.get()}")
        print(f"Mensaje: {self.text_mensaje.get('1.0', 'end').strip()}")


if __name__ == "__main__":
    app = Formulario()
    app.mainloop()
