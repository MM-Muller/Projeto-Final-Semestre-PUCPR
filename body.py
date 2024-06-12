from tkinter import *
from tkinter import ttk
import sqlite3

# Funções do banco de dados
def connect_bd():
    return sqlite3.connect('employee.db')

def desconect_bd(conn):
    conn.close()

def create_tab():
    conn = connect_bd()
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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Quantity INTEGER NOT NULL,
            CPF TEXT NOT NULL,
            Product TEXT NOT NULL
        );
    """)
    conn.commit()
    desconect_bd(conn)

# Funções do Tkinter
def clean_info_product():
    name_entry_product.delete(0, END)
    age_entry_product.delete(0, END)
    product_combobox_product.set('')  # Limpar a seleção do combobox
    ident_entry_product.delete(0, END)

def clean_info_order():
    name_entry_order.delete(0, END)
    age_entry_order.delete(0, END)
    product_combobox_order.set('')  # Limpar a seleção do combobox
    ident_entry_order.delete(0, END)

def add_client():
    conn = connect_bd()
    cursor = conn.cursor()

    nome = name_entry_product.get()
    idade = age_entry_product.get()
    id = ident_entry_product.get()
    produto = product_combobox_product.get()

    cursor.execute("SELECT * FROM employee WHERE Ident =?", (id,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("Erro", "Já existe um usuário com esse ID.")
        desconect_bd(conn)
        return

    cursor.execute(""" INSERT INTO employee (Name, Age, Role, Ident)
        VALUES (?, ?, ?, ?)""", (nome, idade, produto, id))
    conn.commit()
    desconect_bd(conn)
    select_client()
    clean_info_product()

def add_order():
    conn = connect_bd()
    cursor = conn.cursor()

    nome = name_entry_order.get()
    quantidade = age_entry_order.get()
    cpf = ident_entry_order.get()
    produto = product_combobox_order.get()

    cursor.execute(""" INSERT INTO orders (Name, Quantity, CPF, Product)
        VALUES (?, ?, ?, ?)""", (nome, quantidade, cpf, produto))
    conn.commit()
    desconect_bd(conn)
    select_orders()
    clean_info_order()

def validate_age_input(new_value):
    return new_value.isdigit() or new_value == ""

def select_client():
    conn = connect_bd()
    cursor = conn.cursor()
    client_list.delete(*client_list.get_children())
    lista = cursor.execute(""" SELECT code, Name, Age, Role, Ident FROM employee ORDER BY Name ASC; """)
    for i in lista:
        client_list.insert("", END, values=i)
    desconect_bd(conn)

def select_orders():
    conn = connect_bd()
    cursor = conn.cursor()
    order_list.delete(*order_list.get_children())
    lista = cursor.execute(""" SELECT order_id, Name, Quantity, CPF, Product FROM orders ORDER BY Name ASC; """)
    for i in lista:
        order_list.insert("", END, values=i)
    desconect_bd(conn)

def show_selected_client(event):
    selected_item = client_list.selection()
    if selected_item:
        client_info = client_list.item(selected_item)['values']
        name_entry_product.delete(0, END)
        name_entry_product.insert(0, client_info[1])
        age_entry_product.delete(0, END)
        age_entry_product.insert(0, client_info[2])
        product_combobox_product.set(client_info[3])
        ident_entry_product.delete(0, END)
        ident_entry_product.insert(0, client_info[4])

def show_selected_order(event):
    selected_item = order_list.selection()
    if selected_item:
        order_info = order_list.item(selected_item)['values']
        name_entry_order.delete(0, END)
        name_entry_order.insert(0, order_info[1])
        age_entry_order.delete(0, END)
        age_entry_order.insert(0, order_info[2])
        ident_entry_order.delete(0, END)
        ident_entry_order.insert(0, order_info[3])
        product_combobox_order.set(order_info[4])

def delete_client():
    conn = connect_bd()
    cursor = conn.cursor()

    selected_item = client_list.selection()
    if len(selected_item) == 0:
        print("Aviso!! Selecione um cliente para deletar.")
        desconect_bd(conn)
        return

    client_code = client_list.item(selected_item)['values'][0]
    cursor.execute("DELETE FROM employee WHERE code = ?", (client_code,))
    conn.commit()
    desconect_bd(conn)
    clean_info_product()
    select_client()

def delete_order():
    conn = connect_bd()
    cursor = conn.cursor()

    selected_item = order_list.selection()
    if len(selected_item) == 0:
        print("Aviso!! Selecione um pedido para deletar.")
        desconect_bd(conn)
        return

    order_id = order_list.item(selected_item)['values'][0]
    cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
    conn.commit()
    desconect_bd(conn)
    clean_info_order()
    select_orders()

def edit_client():
    conn = connect_bd()
    cursor = conn.cursor()

    selected_item = client_list.selection()
    if len(selected_item) == 0:
        print("Aviso!! Selecione um cliente para editar.")
        desconect_bd(conn)
        return

    nome = name_entry_product.get()
    idade = age_entry_product.get()
    id = ident_entry_product.get()
    produto = product_combobox_product.get()

    client_code = client_list.item(selected_item)['values'][0]
    cursor.execute(""" UPDATE employee SET Name = ?, Age = ?, Role = ?, Ident = ?
        WHERE code = ?""", (nome, idade, produto, id, client_code))
    conn.commit()
    desconect_bd(conn)
    select_client()
    clean_info_product()

def edit_order():
    conn = connect_bd()
    cursor = conn.cursor()

    selected_item = order_list.selection()
    if len(selected_item) == 0:
        print("Aviso!! Selecione um pedido para editar.")
        desconect_bd(conn)
        return

    nome = name_entry_order.get()
    quantidade = age_entry_order.get()
    cpf = ident_entry_order.get()
    produto = product_combobox_order.get()

    order_id = order_list.item(selected_item)['values'][0]
    cursor.execute(""" UPDATE orders SET Name = ?, Quantity = ?, CPF = ?, Product = ?
        WHERE order_id = ?""", (nome, quantidade, cpf, produto, order_id))
    conn.commit()
    desconect_bd(conn)
    select_orders()
    clean_info_order()

# Interface gráfica
window = Tk()
window.title('Registration')
window.geometry('800x600')

frame = Frame(window)
frame.pack()

# Primeira parte - 1
user_info_frame = LabelFrame(frame, text='User Info')
user_info_frame.grid(row=0, column=0, padx=35, pady=20, sticky=W)

abas = ttk.Notebook(user_info_frame)
aba1 = Frame(abas)
aba2 = Frame(abas)

aba1.config(background='white')
aba2.config(background='lightgray')

abas.add(aba1, text='Cadastro de Produtos')
abas.add(aba2, text='Cadastro de Pedidos')

abas.grid(row=0, column=0, padx=10, pady=10)

# Pegar informacoes da Empresa - Aba1
Label(aba1, text='Nome da Empresa :').grid(row=0, column=0, padx=15, pady=10, sticky=W)
name_entry_product = Entry(aba1)
name_entry_product.grid(row=0, column=1, padx=15, pady=10, sticky=W)

Label(aba1, text='Quantidade :').grid(row=0, column=2, padx=5, pady=10, sticky=W)
age_var_product = StringVar()
validate_age = window.register(validate_age_input)
age_entry_product = Entry(aba1, textvariable=age_var_product, validate="key", validatecommand=(validate_age, '%P'))
age_entry_product.grid(row=0, column=3, padx=15, pady=10, sticky=W)

Label(aba1, text='ID :').grid(row=1, column=0, padx=15, pady=10, sticky=W)
ident_entry_product = Entry(aba1)
ident_entry_product.grid(row=1, column=1, padx=15, pady=10, sticky=W)

Label(aba1, text='Produto :').grid(row=1, column=2, padx=5, pady=10, sticky=W)
product_combobox_product = ttk.Combobox(aba1, values=["Caneta", "Borracha", "Papel"], state='readonly')
product_combobox_product.grid(row=1, column=3, padx=15, pady=10, sticky=W)

Button(aba1, text='Limpar informacoes', command=clean_info_product).grid(row=2, column=0, padx=15, pady=10)
Button(aba1, text='Novo Produto', command=add_client).grid(row=2, column=3, padx=15, pady=10)
Button(aba1, text='Alterar Produto', command=edit_client).grid(row=2, column=1, padx=15, pady=10)
Button(aba1, text='Deletar Produto', command=delete_client).grid(row=2, column=2, padx=15, pady=10)

# Pedidos - Aba2
Label(aba2, text='Nome :').grid(row=0, column=0, padx=15, pady=10, sticky=W)
name_entry_order = Entry(aba2)
name_entry_order.grid(row=0, column=1, padx=15, pady=10, sticky=W)

Label(aba2, text='Quantidade desejada :').grid(row=0, column=2, padx=5, pady=10, sticky=W)
age_var_order = StringVar()
age_entry_order = Entry(aba2, textvariable=age_var_order, validate="key", validatecommand=(validate_age, '%P'))
age_entry_order.grid(row=0, column=3, padx=15, pady=10, sticky=W)

Label(aba2, text='CPF :').grid(row=1, column=0, padx=15, pady=10, sticky=W)
ident_var_order = StringVar()
ident_entry_order = Entry(aba2, textvariable=ident_var_order, validate="key", validatecommand=(validate_age, '%P'))
ident_entry_order.grid(row=1, column=1, padx=15, pady=10, sticky=W)

Label(aba2, text='Produto :').grid(row=1, column=2, padx=5, pady=10, sticky=W)
product_combobox_order = ttk.Combobox(aba2, values=["Caneta", "Borracha", "Papel"], state='readonly')
product_combobox_order.grid(row=1, column=3, padx=15, pady=10, sticky=W)

Button(aba2, text='Limpar informacoes', command=clean_info_order).grid(row=2, column=0, padx=15, pady=10)
Button(aba2, text='Novo Pedido', command=add_order).grid(row=2, column=3, padx=15, pady=10)
Button(aba2, text='Alterar Pedido', command=edit_order).grid(row=2, column=1, padx=15, pady=10)
Button(aba2, text='Deletar Pedido', command=delete_order).grid(row=2, column=2, padx=15, pady=10)

# Segunda parte - 1
show_info_frame = LabelFrame(frame, text='View information')
show_info_frame.grid(row=1, column=0, padx=15, pady=20, sticky=W)

abas_info = ttk.Notebook(show_info_frame)
aba3 = Frame(abas_info)
aba4 = Frame(abas_info)
aba5 = Frame(abas_info)

aba3.config(background='white')
aba4.config(background='lightgray')
aba5.config(background='white')

abas_info.add(aba3, text='Cadastro de Produtos')
abas_info.add(aba4, text='Cadastro de Pedidos')
abas_info.add(aba5, text='Estoque')

abas_info.grid(row=1, column=0, padx=10, pady=10)

# Treeview para Cadastro de Produtos
client_list = ttk.Treeview(aba3, columns=('col1', 'col2', 'col3', 'col4', 'col5'))
client_list.grid(row=0, column=0, padx=35, columnspan=1, pady=10, sticky=W)

client_list.heading("#0", text="")
client_list.column("#0", width=0, stretch=NO)
client_list.heading("#1", text='Nº Cadastro')
client_list.column("#1", width=100)
client_list.heading("#2", text='Empresa')
client_list.column("#2", width=150)
client_list.heading("#3", text='Quantidade')
client_list.column("#3", width=100)
client_list.heading("#4", text='Produto')
client_list.column("#4", width=125)
client_list.heading("#5", text='Identificação')
client_list.column("#5", width=100)

scrollbar = ttk.Scrollbar(aba3, orient=VERTICAL)
client_list.configure(yscroll=scrollbar.set)
scrollbar.place(relx=0.95, rely=0.01, relwidth=0.05, relheight=0.95)
client_list.bind("<Double-1>", show_selected_client)

# Treeview para Cadastro de Pedidos
order_list = ttk.Treeview(aba4, columns=('col1', 'col2', 'col3', 'col4', 'col5'))
order_list.grid(row=0, column=0, padx=35, columnspan=1, pady=10, sticky=W)

order_list.heading("#0", text="")
order_list.column("#0", width=0, stretch=NO)
order_list.heading("#1", text='Nº Pedido')
order_list.column("#1", width=100)
order_list.heading("#2", text='Nome')
order_list.column("#2", width=150)
order_list.heading("#3", text='Quantidade')
order_list.column("#3", width=100)
order_list.heading("#4", text='CPF')
order_list.column("#4", width=125)
order_list.heading("#5", text='Produto')
order_list.column("#5", width=100)

scrollbar2 = ttk.Scrollbar(aba4, orient=VERTICAL)
order_list.configure(yscroll=scrollbar2.set)
scrollbar2.place(relx=0.95, rely=0.01, relwidth=0.05, relheight=0.95)
order_list.bind("<Double-1>", show_selected_order)

# Inicializa banco de dados e interface
create_tab()
select_client()
select_orders()
window.mainloop()
