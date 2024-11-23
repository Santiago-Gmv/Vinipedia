import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from styles import Colors

# Importar los colores necesarios
DARK_BURGUNDY = Colors.DARK_BURGUNDY
LIGHT_BURGUNDY = Colors.LIGHT_BURGUNDY
GOLD = Colors.GOLD
CREAM = Colors.CREAM
HOVER_BURGUNDY = Colors.HOVER_BURGUNDY

class WindowManager:
    def __init__(self):
        self._current_window = None

    def switch_window(self, current_window, new_window_class):
        try:
            # Guardar la posición actual
            x = current_window.winfo_x()
            y = current_window.winfo_y()
            width = current_window.winfo_width()
            height = current_window.winfo_height()
            
            # Crear nueva ventana antes de destruir la actual
            new_window = new_window_class()
            
            # Configurar la nueva ventana
            new_window.geometry(f"{width}x{height}+{x}+{y}")
            
            # Asegurarse de que la nueva ventana tenga un window_manager
            new_window.window_manager = self
            
            # Destruir la ventana actual
            current_window.destroy()
            
            # Mostrar la nueva ventana
            new_window.deiconify()
            new_window.lift()
            new_window.focus_force()
            
            self._current_window = new_window
            return new_window
            
        except Exception as e:
            ErrorHandler.show_error(f"Error al cambiar de ventana: {str(e)}", current_window)
            return None

class ErrorHandler:
    @staticmethod
    def show_error(message, parent=None):
        CTkMessagebox(
            master=parent,
            title="Error",
            message=message,
            icon="cancel",
            fg_color=DARK_BURGUNDY,
            border_color=GOLD,
            button_color=LIGHT_BURGUNDY,
            button_hover_color=HOVER_BURGUNDY
        )

class NotificationManager:
    @staticmethod
    def show_notification(message, parent=None, duration=3000):
        try:
            notification = ctk.CTkFrame(
                parent,
                fg_color=LIGHT_BURGUNDY,
                corner_radius=10,
                border_width=2,
                border_color=GOLD
            )
            
            label = ctk.CTkLabel(
                notification,
                text=message,
                font=("Helvetica", 14),
                text_color=CREAM
            )
            label.pack(padx=20, pady=10)
            
            notification.place(relx=0.5, rely=0.9, anchor="center")
            
            # Asegurarse de que la notificación se destruya
            def destroy_notification():
                try:
                    notification.destroy()
                except:
                    pass
                    
            parent.after(duration, destroy_notification)
            
        except Exception as e:
            print(f"Error mostrando notificación: {str(e)}")