import customtkinter as ctk
from PIL import Image, ImageTk
import os
import sys
from typing import Optional, Tuple, Union
from CTkMessagebox import CTkMessagebox

# Importaciones locales
from utils import WindowManager, ErrorHandler, NotificationManager
from styles import Colors, Fonts, Styles
from components import AnimatedButton

class WineAppHomeGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.window_manager = WindowManager()
        # ... (resto del código igual)

    def profile_event(self):
        from gui.perfil import WineAppMobileGUI  # Importación local
        self.window_manager.switch_window(self, WineAppMobileGUI)

    def support_event(self):
        from gui.suporte import Formulario  # Importación local
        self.window_manager.switch_window(self, Formulario)

    def Cata_De_Vinos(self):
        from gui.ficha_de_cata import FormularioCataVino  # Importación local
        self.window_manager.switch_window(self, FormularioCataVino)

    def map_event(self):
        from gui.mapa import WineMapApp  # Importación local
        self.window_manager.switch_window(self, WineMapApp)
