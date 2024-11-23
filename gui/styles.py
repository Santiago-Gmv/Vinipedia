from dataclasses import dataclass

@dataclass
class Colors:
    DARK_BURGUNDY = "#1A0F0F"
    LIGHT_BURGUNDY = "#2B1B17"
    GOLD = "#D4AF37"
    CREAM = "#F5F5DC"
    ACCENT_GOLD = "#FFD700"
    HOVER_BURGUNDY = "#3D2B25"
    TEXT_DARK = "#2B1B17"
    TEXT_LIGHT = "#F5F5DC"

@dataclass
class Fonts:
    TITLE = ("Helvetica", 32, "bold")
    SUBTITLE = ("Helvetica", 24, "bold")
    BUTTON = ("Helvetica", 14, "bold")
    TEXT = ("Helvetica", 12)
    SMALL = ("Helvetica", 10)

@dataclass
class Styles:
    BUTTON = {
        "corner_radius": 10,
        "border_width": 2,
        "border_color": Colors.GOLD,
        "fg_color": Colors.LIGHT_BURGUNDY,
        "hover_color": Colors.HOVER_BURGUNDY,
        "text_color": Colors.CREAM,
        "height": 40
    }
    
    FRAME = {
        "corner_radius": 20,
        "border_width": 2,
        "border_color": Colors.GOLD,
        "fg_color": Colors.LIGHT_BURGUNDY
    }
    
    ENTRY = {
        "corner_radius": 10,
        "border_width": 2,
        "border_color": Colors.GOLD,
        "fg_color": Colors.CREAM,
        "text_color": Colors.TEXT_DARK,
        "placeholder_text_color": Colors.LIGHT_BURGUNDY
    } 