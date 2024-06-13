import tkinter as tk
from tkinter import messagebox


def check_login(username, password):
    if username == "admin" and password == "1234":
        return True
    else:
        return False


def login():
    username = entry_username.get()
    password = entry_password.get()

    if check_login(username, password):
        messagebox.showinfo("Login bem-sucedido", "Bem-vindo, " + username + "!")
        root.destroy()  # Fechar a janela de login
        open_main_application()  # Abrir a aplicação principal
    else:
        messagebox.showerror("Erro de login", "Nome de usuário ou senha incorretos.")


def open_main_application():
    main_app = tk.Tk()
    main_app.title("Aplicação Principal")

    # Aqui tem que por o body.py
    label_welcome = tk.Label(main_app, text="Bem-vindo à Aplicação Principal!")
    label_welcome.pack()

    main_app.mainloop()


# Criação da janela de login
root = tk.Tk()
root.title("Login")
root.geometry('250x200')

label_username = tk.Label(root, text="Nome de usuário:")
label_username.pack(pady=(20, 0))

entry_username = tk.Entry(root)
entry_username.pack(pady=(0, 10))

label_password = tk.Label(root, text="Senha:")
label_password.pack(pady=(10, 0))

entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=(0, 20))

button_login = tk.Button(root, text="Login", command=login)
button_login.pack(pady=(10, 20))

root.mainloop()
