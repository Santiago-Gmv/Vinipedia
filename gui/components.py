import customtkinter as ctk
from styles import Colors, Fonts, Styles
from utils import ErrorHandler, NotificationManager

class BaseFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(**Styles.FRAME)

class AnimatedButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        button_style = Styles.BUTTON.copy()
        button_style.update(kwargs)
        super().__init__(*args, **button_style)
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.configure(border_color=Colors.ACCENT_GOLD)

    def on_leave(self, event):
        self.configure(border_color=Colors.GOLD)

class StyledEntry(ctk.CTkEntry):
    def __init__(self, *args, **kwargs):
        entry_style = Styles.ENTRY.copy()
        entry_style.update(kwargs)
        super().__init__(*args, **entry_style) 