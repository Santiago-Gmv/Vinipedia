import customtkinter as ctk
import importlib
import inspect

# Color palette
DARK_BURGUNDY = "#4A0E0E"
LIGHT_BURGUNDY = "#800020"
GOLD = "#FFD700"
CREAM = "#FFFDD0"
BORDER_COLOR = "#FFD700"


class WineAppDropdownMenu(ctk.CTkFrame):
    def __init__(self, master, current_page=None):
        super().__init__(master, fg_color="transparent")
        self.current_page = current_page
        self.is_menu_visible = False

        self.menu_button = ctk.CTkButton(
            self,
            text="☰",
            width=40,
            height=40,
            fg_color=LIGHT_BURGUNDY,
            hover_color=GOLD,
            text_color=CREAM,
            command=self.toggle_menu,
        )
        self.menu_button.pack(side="left", padx=10, pady=10)

        # Create the border frame
        self.border_frame = ctk.CTkFrame(
            self.master,
            fg_color=BORDER_COLOR,
            corner_radius=12,
        )

        # Create the menu frame inside the border frame
        self.menu_frame = ctk.CTkFrame(
            self.border_frame,
            fg_color=DARK_BURGUNDY,
            corner_radius=10,
        )

        self.create_menu_items()

    def create_menu_items(self):
        menu_items = [
            ("Home", "home", "WineAppHomeGUI"),
            ("Profile", "perfil", "WineAppMobileGUI"),
            ("Upload Opinion", None, None),
            ("Favorites", "gui.perfil_gui.favs", "WineRatingApp"),
            ("Support", None, None),
            ("Logout", "login", None),
        ]

        for text, module, class_name in menu_items:
            command = (
                (lambda m=module, c=class_name: self.navigate_to(m, c))
                if module
                else self.placeholder_command
            )

            ctk.CTkButton(
                self.menu_frame,
                text=text,
                command=command,
                fg_color="transparent",
                hover_color=GOLD,
                text_color=CREAM,
                height=40,
                anchor="w",
            ).pack(pady=5, padx=10, fill="x")

        ctk.CTkButton(
            self.menu_frame,
            text="Close",
            command=self.hide_menu,
            fg_color=GOLD,
            hover_color=LIGHT_BURGUNDY,
            text_color=DARK_BURGUNDY,
            height=40,
        ).pack(pady=20, padx=10, fill="x", side="bottom")

    def toggle_menu(self):
        if self.is_menu_visible:
            self.hide_menu()
        else:
            self.show_menu()

    def show_menu(self):
        self.border_frame.place(relx=0.05, rely=0.1, relwidth=0.42, relheight=0.82)
        self.menu_frame.pack(fill="both", expand=True, padx=2, pady=2)
        self.border_frame.lift()
        self.is_menu_visible = True

    def hide_menu(self):
        self.border_frame.place_forget()
        self.is_menu_visible = False

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
        else:  # For logout
            self.master.destroy()
            module.app_login.mainloop()

    def placeholder_command(self):
        print("This function is not yet implemented.")
