from tkinter import *
from tkinter import ttk
import sqlite3


window = Tk()
window.title('Employee Registration')
window.geometry('700x600')

frame = Frame(window)
frame.pack()

# Primeira parte - 1
user_info_frame = LabelFrame(frame, text='User Info')
user_info_frame.grid(row=0, column=0, padx=50, pady=20, sticky=W)

# Pegar informacoes do funcionario
name = Label(user_info_frame, text='Nome :')
name.grid(row=0, column=0, padx=15, pady=10, sticky=W)

name = Entry(user_info_frame)
name.grid(row=0, column=1, padx=15, pady=10, sticky=W)

age = Label(user_info_frame, text='Idade :')
age.grid(row=0, column=2, padx=5, pady=10, sticky=W)

age = Entry(user_info_frame)
age.grid(row=0, column=3, padx=15, pady=10, sticky=W)

ident = Label(user_info_frame, text='ID :')
ident.grid(row=1, column=0, padx=15, pady=10, sticky=W)

ident = Entry(user_info_frame)
ident.grid(row=1, column=1, padx=15, pady=10, sticky=W)

role = Label(user_info_frame, text='Função :')
role.grid(row=1, column=2, padx=5, pady=10, sticky=W)

role = Entry(user_info_frame)
role.grid(row=1, column=3, padx=15, pady=10, sticky=W)


# Botoes
def clean_info():
    name.delete(0, END)
    age.delete(0, END)
    role.delete(0, END)
    ident.delete(0, END)


def connect_bd():
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()


def desconect_bd():
    conn = sqlite3.connect('employee.db')
    conn.close()


def create_tab():
    conn = sqlite3.connect('employee.db')
    connect_bd(); print("Conectado ao banco de dados")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee (
            code INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Age INTEGER NOT NULL,
            Role TEXT NOT NULL,
            Ident TEXT NOT NULL
        );
    """)
    conn.commit(); print("Banco de dados criado!")
    desconect_bd(); print("Banco de dados desconectado!")


def add_client():
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()

    nome = name.get()
    idade = age.get()
    id = ident.get()
    cargo = role.get()

    connect_bd()
    cursor.execute("SELECT * FROM employee WHERE Ident =?", (cargo,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("Erro", "Já existe um usuário com esse ID.")
        return

    cursor.execute(""" INSERT INTO employee (Name, Age, Role, Ident)
        VALUES (?, ?, ?, ?)""", (nome, idade, id, cargo))
    conn.commit(); print("Cliente inserido com sucesso!")
    desconect_bd()
    select_client()
    clean_info()


def validate_age_input(new_value):
    if new_value.isdigit() or new_value == "":
        return True
    else:
        return False


age_var = StringVar()
validate_age = window.register(validate_age_input)
age = Entry(user_info_frame, textvariable=age_var, validate="key", validatecommand=(validate_age, '%P'))
age.grid(row=0, column=3, padx=15, pady=10, sticky=W)


def select_client():
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()

    client_list.delete(*client_list.get_children())
    connect_bd()
    lista = cursor.execute(""" SELECT code, Name, Age, Role, Ident FROM employee
        ORDER BY Name ASC; """)
    for i in lista:
        client_list.insert("", END, values=i)
    desconect_bd()


def show_selected_client(event):
    selected_item = client_list.selection()

    if selected_item:
        client_info = client_list.item(selected_item)['values']
        name.delete(0, END)
        name.insert(0, client_info[1])
        age.delete(0, END)
        age.insert(0, client_info[2])
        ident.delete(0, END)
        ident.insert(0, client_info[3])
        role.delete(0, END)
        role.insert(0, client_info[4])


def delete_client():
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()

    selected_item = client_list.selection()
    if len(selected_item) == 0:
        print("Aviso!! Selecione um cliente para deletar.")
        return

    client_code = client_list.item(selected_item)['values'][0]
    cursor.execute("DELETE FROM employee WHERE code = ?", (client_code,))
    conn.commit()
    conn.close()
    desconect_bd()
    clean_info()
    select_client()


def edit_client():
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()

    selected_item = client_list.selection()
    if len(selected_item) == 0:
        print("Aviso!! Selecione um cliente para editar.")
    nome = name.get()
    idade = age.get()
    id = ident.get()
    cargo = role.get()
    connect_bd()
    selected_item = client_list.selection()
    client_code = client_list.item(selected_item)['values'][0]
    cursor.execute(""" UPDATE employee SET Name = ?, Age = ?, Ident = ?, Role = ?
        WHERE code = ?""", (nome, idade, cargo, id, client_code))
    conn.commit()
    desconect_bd()
    select_client()
    clean_info()


clean_bt = Button(user_info_frame, text='Limpar informacoes', command=clean_info)
clean_bt.grid(row=2, column=0, padx=15, pady=10)

add_bt = Button(user_info_frame, text='Novo Usuarior', command=add_client)
add_bt.grid(row=2, column=3, padx=15, pady=10)

change_bt = Button(user_info_frame, text='Alterar Usuarior', command=edit_client)
change_bt.grid(row=2, column=1, padx=15, pady=10)

delete_bt = Button(user_info_frame, text='Deletar Usuario', command=delete_client)
delete_bt.grid(row=2, column=2, padx=15, pady=10)


# Segunda parte - 1
show_info_frame = LabelFrame(frame, text='View users information')
show_info_frame.grid(row=1, column=0, padx=15, pady=20, sticky=W)

client_list = ttk.Treeview(show_info_frame, columns=('col1', 'col2', 'col3', 'col4', 'col5'))
client_list.grid(row=0, column=0, padx=35, columnspan=1, pady=10,sticky=W)

client_list.heading("#0", text="")
client_list.column("#0", width=0, stretch=NO)
client_list.heading("#1", text='Nº Cadastro')
client_list.column("#1", width=100)
client_list.heading("#2", text='Name')
client_list.column("#2", width=150)
client_list.heading("#3", text='Age')
client_list.column("#3", width=100)
client_list.heading("#4", text='Ident')
client_list.column("#4", width=100)
client_list.heading("#5", text='Role')
client_list.column("#5", width=125)

scrollbar = ttk.Scrollbar(show_info_frame, orient=VERTICAL)
client_list.configure(yscroll=scrollbar.set)
scrollbar.place(relx=0.95, rely=0.01, relwidth=0.05, relheight=0.95)
client_list.bind("<Double-1>", show_selected_client)

# Terceira Parte - 1
next_page = LabelFrame(frame, text='')
next_page.grid(row=2, column=0, padx=250, pady=20, sticky=W)

next_bt = Button(next_page, text='Proxima Pagina')
next_bt.grid(row=1, column=3, padx=35, pady=15)

select_client()
create_tab()
window.mainloop()
