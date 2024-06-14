import tkinter as tk
from tkinter import ttk, messagebox
import os

USERS_FILE = "users.txt"


def check_login(username, password):
    if not os.path.exists(USERS_FILE):
        return False

    with open(USERS_FILE, "r") as file:
        for line in file:
            stored_username, stored_password, approved = line.strip().split(",")
            if stored_username == username and stored_password == password and approved == "yes":
                return True
    return False


def register_user(username, password):
    with open(USERS_FILE, "a") as file:
        file.write(f"{username},{password},no\n")


def approve_user(username):
    if not os.path.exists(USERS_FILE):
        return False

    lines = []
    with open(USERS_FILE, "r") as file:
        lines = file.readlines()

    with open(USERS_FILE, "w") as file:
        for line in lines:
            stored_username, stored_password, approved = line.strip().split(",")
            if stored_username == username:
                file.write(f"{stored_username},{stored_password},yes\n")
            else:
                file.write(line)

    refresh_admin_approval_window()


def reject_user(username):
    if not os.path.exists(USERS_FILE):
        return False

    lines = []
    with open(USERS_FILE, "r") as file:
        lines = file.readlines()

    with open(USERS_FILE, "w") as file:
        for line in lines:
            stored_username, stored_password, approved = line.strip().split(",")
            if stored_username != username:
                file.write(line)

    refresh_admin_approval_window()


def refresh_admin_approval_window():
    global admin_window
    admin_window.destroy()
    open_admin_approval_window()


def login():
    username = entry_username.get()
    password = entry_password.get()

    if check_login(username, password):
        messagebox.showinfo("Login bem-sucedido", "Bem-vindo, " + username + "!")
        root.destroy()
        open_main_application()
    else:
        messagebox.showerror("Erro de login", "Nome de usuário ou senha incorretos ou a conta não foi aprovada.")


def register():
    username = entry_register_username.get()
    password = entry_register_password.get()

    register_user(username, password)
    messagebox.showinfo("Registro bem-sucedido", "Registro bem-sucedido! Aguarde a aprovação do administrador.")
    register_window.destroy()


def open_register_window():
    global entry_register_username, entry_register_password, register_window

    register_window = tk.Toplevel(root)
    register_window.title("Registrar")
    register_window.geometry("250x250")

    label_register_username = tk.Label(register_window, text="Nome de usuário:", font=("Helvetica", 12))
    label_register_username.pack(pady=(20, 0))

    entry_register_username = tk.Entry(register_window, font=("Helvetica", 10))
    entry_register_username.pack(pady=(0, 10), ipadx=30, ipady=5)

    label_register_password = tk.Label(register_window, text="Senha:", font=("Helvetica", 12))
    label_register_password.pack(pady=(10, 0))

    entry_register_password = tk.Entry(register_window, show="*", font=("Helvetica", 10))
    entry_register_password.pack(pady=(0, 20), ipadx=30, ipady=5)

    button_register = ttk.Button(register_window, text="Registrar", command=register, style="Custom.TButton")
    button_register.pack(pady=(10, 20))


def open_main_application():
    import body
    body.main()


def admin_login():
    admin_username = admin_username_entry.get()
    admin_password = admin_password_entry.get()

    if admin_username == "admin" and admin_password == "password":
        messagebox.showinfo("Login bem-sucedido", "Bem-vindo, administrador!")
        admin_window.destroy()
        open_admin_approval_window()
    else:
        messagebox.showerror("Erro de login", "Nome de usuário ou senha de administrador incorretos.")


def open_admin_login_window():
    global admin_username_entry, admin_password_entry, admin_window

    admin_window = tk.Toplevel(root)
    admin_window.title("Login do Administrador")
    admin_window.geometry("250x250")

    tk.Label(admin_window, text="Nome de usuário:", font=("Helvetica", 12)).pack(pady=(20, 0))
    admin_username_entry = tk.Entry(admin_window, font=("Helvetica", 10))
    admin_username_entry.pack(pady=(0, 10), ipadx=30, ipady=5)

    tk.Label(admin_window, text="Senha:", font=("Helvetica", 12)).pack(pady=(10, 0))
    admin_password_entry = tk.Entry(admin_window, show="*", font=("Helvetica", 10))
    admin_password_entry.pack(pady=(0, 20), ipadx=30, ipady=5)

    ttk.Button(admin_window, text="Login", command=admin_login, style="Custom.TButton").pack(pady=(10, 20))


def open_admin_approval_window():
    global admin_window
    admin_window = tk.Toplevel(root)
    admin_window.title("Aprovar Usuários")
    admin_window.geometry("400x400")

    if not os.path.exists(USERS_FILE):
        tk.Label(admin_window, text="Nenhum usuário registrado.", font=("Helvetica", 12)).pack()
        return

    with open(USERS_FILE, "r") as file:
        for line in file:
            username, password, approved = line.strip().split(",")
            if approved == "no":
                frame = tk.Frame(admin_window)
                frame.pack(pady=(10, 0))
                tk.Label(frame, text=f"Usuário: {username}", font=("Helvetica", 12)).pack(side=tk.LEFT)
                ttk.Button(frame, text="Aprovar", command=lambda u=username: approve_user(u),
                           style="Custom.TButton").pack(side=tk.LEFT)
                ttk.Button(frame, text="Recusar", command=lambda u=username: reject_user(u),
                           style="Custom.TButton").pack(side=tk.RIGHT)


# Criação da janela de login
root = tk.Tk()
root.title("Login")
root.geometry("500x300")

# Estilo personalizado para botões
style = ttk.Style()
style.configure("Custom.TButton",
                font=("Helvetica", 10, "bold"),
                foreground="black",
                background="black",
                padding=5)
style.map("Custom.TButton",
          foreground=[("active", "red")],
          background=[("active", "white")])

# Widgets da interface
label_username = tk.Label(root, text="Nome de usuário:", font=("Helvetica", 12))
label_username.pack(pady=(20, 0))

entry_username = tk.Entry(root, font=("Helvetica", 10))
entry_username.pack(pady=(0, 10), ipadx=30, ipady=5)

label_password = tk.Label(root, text="Senha:", font=("Helvetica", 12))
label_password.pack(pady=(10, 0))

entry_password = tk.Entry(root, show="*", font=("Helvetica", 10))
entry_password.pack(pady=(0, 20), ipadx=30, ipady=5)

# Botões em linha
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=20)

button_login = ttk.Button(buttons_frame, text="Login", command=login, style="Custom.TButton")
button_login.pack(side=tk.LEFT, padx=10)

button_register = ttk.Button(buttons_frame, text="Registrar", command=open_register_window, style="Custom.TButton")
button_register.pack(side=tk.LEFT, padx=10)

button_admin = ttk.Button(buttons_frame, text="Administração", command=open_admin_login_window, style="Custom.TButton")
button_admin.pack(side=tk.LEFT, padx=10)

# Inicialização da janela de login
root.mainloop()
