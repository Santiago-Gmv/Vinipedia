import customtkinter as ctk
import tkinter.messagebox as tkmb
import re
from home import WineAppHomeGUI
import sqlite3

# Select the GUI theme - dark, light, system (system default)
ctk.set_appearance_mode("dark")

# Create the main app_loginlication window
app_login = ctk.CTk()
app_login.geometry("400x600")
app_login.title("ViniPedia Login")

# Color palette
DARK_BURGUNDY = "#4A0E0E"
LIGHT_BURGUNDY = "#800020"
GOLD = "#FFD700"
CREAM = "#FFFDD0"

# Configure the main window
app_login.configure(fg_color=DARK_BURGUNDY)

# Connect to the database
conn = sqlite3.connect("DB/users.db")
c = conn.cursor()

# Check if the users table existsz
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
if not c.fetchone():
    # Create the users table
    c.execute("CREATE TABLE users (username TEXT PRIMARY KEY, email TEXT, password TEXT)")

# Retrieve the user data from the database
c.execute("SELECT * FROM users")
db_user = {row[0]: {"Email": row[1], "password": row[2]} for row in c.fetchall()}

def register():
    def cargar_datos():
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        user_email = entrada_correo.get()
        user_name = entrada_username.get()
        user_password = entrada_contraseña.get()
        
        if user_name in db_user:
            tkmb.showerror(title="Error", message="El usuario ya existe")
        elif re.match(pattern, user_email) is None:
            tkmb.showerror(title="Error", message="El correo no es válido")
        elif user_email == "" or user_name == "" or user_password == "":
            tkmb.showerror(title="Error", message="Todos los campos son obligatorios")
        elif any(user["Email"] == user_email for user in db_user.values()):
            tkmb.showerror(title="Error", message="El correo ya existe")
        else:
            c.execute("INSERT INTO users VALUES (?, ?, ?)", (user_name, user_email, user_password))
            conn.commit()
            db_user[user_name] = {"Email": user_email, "password": user_password}
            tkmb.showinfo(title="Éxito", message="Usuario creado con éxito")
            print(db_user)
            register_w.destroy()
    
    register_w = ctk.CTkToplevel(app_login)
    register_w.geometry("400x450")
    register_w.title("Register")
    register_w.configure(fg_color=DARK_BURGUNDY)

    label_title = ctk.CTkLabel(register_w, text="Crear cuenta", font=("Helvetica", 24, "bold"), text_color=GOLD)
    label_title.pack(pady=20)

    entrada_correo = ctk.CTkEntry(register_w, placeholder_text="Email", width=300, height=40, fg_color=LIGHT_BURGUNDY, text_color=CREAM, placeholder_text_color=GOLD)
    entrada_correo.pack(pady=10)

    entrada_username = ctk.CTkEntry(register_w, placeholder_text="Username", width=300, height=40, fg_color=LIGHT_BURGUNDY, text_color=CREAM, placeholder_text_color=GOLD)
    entrada_username.pack(pady=10)

    entrada_contraseña = ctk.CTkEntry(register_w, placeholder_text="Password", show="*", width=300, height=40, fg_color=LIGHT_BURGUNDY, text_color=CREAM, placeholder_text_color=GOLD)
    entrada_contraseña.pack(pady=10)

    btn_enviar = ctk.CTkButton(register_w, text="Register", command=cargar_datos, fg_color=GOLD, text_color=DARK_BURGUNDY, hover_color=CREAM, width=200, height=40)
    btn_enviar.pack(pady=20)

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username in db_user:
        if password == db_user[username]["password"]:
            tkmb.showinfo(title="Inicio de sesión exitoso", message="Has iniciado sesión correctamente")
            app = WineAppHomeGUI()
            app_login.destroy()
            app.mainloop()
        else:
            tkmb.showwarning(title='Contraseña incorrecta', message='Por favor verifique su contraseña')
    else:
        tkmb.showerror(title="Inicio de sesión fallido", message="Nombre de usuario inválido")

# Title
title_label = ctk.CTkLabel(app_login, text="ViniPedia Login", font=("Helvetica", 28, "bold"), text_color=GOLD)
title_label.place(relx=0.5, rely=0.15, anchor="center")

# Username entry
username_entry = ctk.CTkEntry(app_login, placeholder_text="Username", width=300, height=40, fg_color=LIGHT_BURGUNDY, text_color=CREAM, placeholder_text_color=GOLD)
username_entry.place(relx=0.5, rely=0.3, anchor="center")

# Password entry
password_entry = ctk.CTkEntry(app_login, placeholder_text="Password", show="*", width=300, height=40, fg_color=LIGHT_BURGUNDY, text_color=CREAM, placeholder_text_color=GOLD)
password_entry.place(relx=0.5, rely=0.4, anchor="center")

# Login button
btn_login = ctk.CTkButton(app_login, text="Login", command=login, fg_color=GOLD, text_color=DARK_BURGUNDY, hover_color=CREAM, width=200, height=40)
btn_login.place(relx=0.5, rely=0.55, anchor="center")

# Register button
btn_register = ctk.CTkButton(app_login, text="Register", command=register, fg_color=LIGHT_BURGUNDY, text_color=GOLD, hover_color=CREAM, width=200, height=40)
btn_register.place(relx=0.5, rely=0.65, anchor="center")

app_login.mainloop()
