from tkinter import *
from tkinter import ttk, messagebox
from database import *


# Funções do Tkinter
def clean_info_product():
    """

    :return:
    """
    name_entry_product.delete(0, END)
    age_entry_product.delete(0, END)
    product_combobox_product.set('')  # Limpar a seleção do combobox
    ident_entry_product.delete(0, END)


def clean_info_order():
    """

    :return:
    """
    name_entry_order.delete(0, END)
    age_entry_order.delete(0, END)
    product_combobox_order.set('')  # Limpar a seleção do combobox
    ident_entry_order.delete(0, END)


def add_client():
    """

    :return:
    """
    conn = connect_bd()
    cursor = conn.cursor()

    nome = name_entry_product.get()
    quantidade = int(age_entry_product.get())
    id = ident_entry_product.get()
    produto = product_combobox_product.get()

    cursor.execute("SELECT * FROM employee WHERE Ident =?", (id,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("Erro", "Já existe um usuário com esse ID.")
        desconect_bd(conn)
        return

    cursor.execute(""" INSERT INTO employee (Name, Age, Role, Ident)
        VALUES (?, ?, ?, ?)""", (nome, quantidade, produto, id))
    conn.commit()

    # Atualiza o estoque após adicionar um novo produto
    cursor.execute("SELECT Available FROM stock WHERE Product = ?", (produto,))
    current_stock = cursor.fetchone()
    if current_stock:
        updated_stock = current_stock[0] + quantidade  # Incrementa o estoque pela quantidade inserida
        cursor.execute("UPDATE stock SET Available = ? WHERE Product = ?", (updated_stock, produto))
    else:
        cursor.execute("INSERT INTO stock (Product, Available) VALUES (?, ?)", (produto, quantidade))

    conn.commit()
    desconect_bd(conn)
    select_client()
    clean_info_product()
    update_stock_list()


def add_order():
    """

    :return:
    """
    conn = connect_bd()
    cursor = conn.cursor()

    nome = name_entry_order.get()
    quantidade = int(age_entry_order.get())
    cpf = ident_entry_order.get()
    produto = product_combobox_order.get()

    # Verificar se há estoque suficiente para o pedido
    cursor.execute("SELECT Available FROM stock WHERE Product = ?", (produto,))
    current_stock = cursor.fetchone()

    if current_stock:
        available_quantity = current_stock[0]

        if quantidade > available_quantity:
            messagebox.showinfo("Erro!", "Estoque insuficiente para o produto")
            desconect_bd(conn)
            return

        # Inserir o pedido na tabela 'orders'
        cursor.execute(""" INSERT INTO orders (Name, Quantity, CPF, Product)
            VALUES (?, ?, ?, ?)""", (nome, quantidade, cpf, produto))
        conn.commit()

        # Atualizar o estoque subtraindo a quantidade do pedido
        updated_stock = available_quantity - quantidade
        cursor.execute("UPDATE stock SET Available = ? WHERE Product = ?", (updated_stock, produto))
        conn.commit()

    else:
        print(f"Produto '{produto}' não encontrado no estoque.")

    desconect_bd(conn)
    select_orders()
    clean_info_order()
    update_stock_list()


def validate_age_input(new_value):
    """

    :param new_value:
    :return:
    """
    return new_value.isdigit() or new_value == ""


def select_client():
    """

    :return:
    """
    conn = connect_bd()
    cursor = conn.cursor()
    client_list.delete(*client_list.get_children())
    lista = cursor.execute(""" SELECT code, Name, Age, Role, Ident FROM employee ORDER BY Name ASC; """)
    for i in lista:
        client_list.insert("", END, values=i)
    desconect_bd(conn)


def select_orders():
    """

    :return:
    """
    conn = connect_bd()
    cursor = conn.cursor()
    order_list.delete(*order_list.get_children())
    lista = cursor.execute(""" SELECT order_id, Name, Quantity, CPF, Product FROM orders ORDER BY Name ASC; """)
    for i in lista:
        order_list.insert("", END, values=i)
    desconect_bd(conn)


def show_selected_client(event):
    """

    :param event:
    :return:
    """
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
    """

    :param event:
    :return:
    """
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
    """

    :return:
    """
    conn = connect_bd()
    cursor = conn.cursor()

    selected_item = client_list.selection()
    if len(selected_item) == 0:
        print("Aviso!! Selecione um cliente para deletar.")
        desconect_bd(conn)
        return

    client_code = client_list.item(selected_item)['values'][0]
    quantidade = client_list.item(selected_item)['values'][2]
    produto = client_list.item(selected_item)['values'][3]

    # Deletar o cliente da tabela 'employee'
    cursor.execute("DELETE FROM employee WHERE code = ?", (client_code,))
    conn.commit()

    # Atualizar o estoque subtraindo a quantidade associada ao cliente deletado
    cursor.execute("SELECT Available FROM stock WHERE Product = ?", (produto,))
    stock_result = cursor.fetchone()

    if stock_result:
        current_stock = stock_result[0]
        updated_stock = current_stock - quantidade
        cursor.execute("UPDATE stock SET Available = ? WHERE Product = ?", (updated_stock, produto))
        conn.commit()
    else:
        print(f"Aviso!! Produto '{produto}' não encontrado no estoque.")

    desconect_bd(conn)
    select_client()
    update_stock_list()


def delete_order():
    """

    :return:
    """
    conn = connect_bd()
    cursor = conn.cursor()

    selected_item = order_list.selection()
    if len(selected_item) == 0:
        print("Aviso!! Selecione um pedido para deletar.")
        desconect_bd(conn)
        return

    order_id = order_list.item(selected_item)['values'][0]
    cursor.execute("SELECT Product, Quantity FROM orders WHERE order_id = ?", (order_id,))
    order_info = cursor.fetchone()
    if not order_info:
        print(f"Pedido com ID {order_id} não encontrado.")
        desconect_bd(conn)
        return

    product_name = order_info[0]
    order_quantity = order_info[1]

    # Obter a quantidade atual do produto no estoque
    cursor.execute("SELECT Available FROM stock WHERE Product = ?", (product_name,))
    stock_info = cursor.fetchone()
    if not stock_info:
        print(f"Produto '{product_name}' não encontrado no estoque.")
        desconect_bd(conn)
        return

    current_available = stock_info[0]

    # Deletar o pedido da tabela 'orders'
    cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
    conn.commit()

    # Restaurar a quantidade no estoque com a quantidade cadastrada
    updated_stock = current_available + order_quantity
    cursor.execute("UPDATE stock SET Available = ? WHERE Product = ?", (updated_stock, product_name))
    conn.commit()

    desconect_bd(conn)
    select_orders()
    clean_info_order()
    update_stock_list()


def edit_client():
    """

    :return:
    """
    conn = connect_bd()
    cursor = conn.cursor()

    selected_item = client_list.selection()
    if len(selected_item) == 0:
        print("Aviso!! Selecione um cliente para editar.")
        desconect_bd(conn)
        return

    nome = name_entry_product.get()
    idade = int(age_entry_product.get())
    id = ident_entry_product.get()
    produto = product_combobox_product.get()

    client_code = client_list.item(selected_item)['values'][0]
    quantidade_anterior = client_list.item(selected_item)['values'][2]

    cursor.execute(""" UPDATE employee SET Name = ?, Age = ?, Role = ?, Ident = ?
        WHERE code = ?""", (nome, idade, produto, id, client_code))
    conn.commit()

    # Atualiza o estoque após editar o produto
    cursor.execute("SELECT Available FROM stock WHERE Product = ?", (produto,))
    current_stock = cursor.fetchone()
    if current_stock:
        updated_stock = current_stock[0] - quantidade_anterior + idade
        cursor.execute("UPDATE stock SET Available = ? WHERE Product = ?", (updated_stock, produto))
    else:
        cursor.execute("INSERT INTO stock (Product, Available) VALUES (?, ?)", (produto, idade))

    conn.commit()
    desconect_bd(conn)
    select_client()
    clean_info_product()
    update_stock_list()


def edit_order():
    """

    :return:
    """
    conn = connect_bd()
    cursor = conn.cursor()

    selected_item = order_list.selection()
    if len(selected_item) == 0:
        print("Aviso!! Selecione um pedido para editar.")
        desconect_bd(conn)
        return

    nome = name_entry_order.get()
    quantidade_nova = int(age_entry_order.get())
    cpf = ident_entry_order.get()
    produto_novo = product_combobox_order.get()

    order_id = order_list.item(selected_item)['values'][0]

    # Obter informações atuais do pedido antes da edição
    cursor.execute("SELECT Product, Quantity FROM orders WHERE order_id = ?", (order_id,))
    current_order_info = cursor.fetchone()

    if not current_order_info:
        print(f"Pedido com ID {order_id} não encontrado.")
        desconect_bd(conn)
        return

    produto_atual = current_order_info[0]
    quantidade_atual = current_order_info[1]

    # Restaurar a quantidade atual no estoque
    cursor.execute("UPDATE stock SET Available = Available + ? WHERE Product = ?", (quantidade_atual, produto_atual))
    conn.commit()

    # Verificar se há estoque suficiente para a nova quantidade do pedido
    cursor.execute("SELECT Available FROM stock WHERE Product = ?", (produto_novo,))
    stock_info = cursor.fetchone()

    if not stock_info:
        print(f"Produto {produto_novo} não encontrado no estoque.")
        cursor.execute("UPDATE stock SET Available = Available - ? WHERE Product = ?", (quantidade_atual, produto_atual))
        conn.commit()
        desconect_bd(conn)
        return

    quantidade_disponivel = stock_info[0]

    if quantidade_nova > quantidade_disponivel:
        messagebox.showinfo("Erro!", "Estoque insuficiente para o produto")
        # Restaurar a quantidade original no estoque, já que a atualização falhou
        cursor.execute("UPDATE stock SET Available = Available - ? WHERE Product = ?", (quantidade_atual, produto_atual))
        conn.commit()
        desconect_bd(conn)
        return

    # Atualizar o pedido
    cursor.execute("""UPDATE orders SET Name = ?, Quantity = ?, CPF = ?, Product = ?
        WHERE order_id = ?""", (nome, quantidade_nova, cpf, produto_novo, order_id))
    conn.commit()

    # Atualizar o estoque subtraindo a nova quantidade do pedido
    cursor.execute("UPDATE stock SET Available = Available - ? WHERE Product = ?", (quantidade_nova, produto_novo))
    conn.commit()

    desconect_bd(conn)
    select_orders()
    clean_info_order()
    update_stock_list()


def add_stock(product, quantity):
    """

    :param product:
    :param quantity:
    :return:
    """
    conn = connect_bd()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO stock (Product, Available) VALUES (?, ?)", (product, quantity))
    conn.commit()
    desconect_bd(conn)


def update_stock(product, quantity):
    """

    :param product:
    :param quantity:
    :return:
    """
    conn = connect_bd()
    cursor = conn.cursor()
    cursor.execute("UPDATE stock SET Available = Available - ? WHERE Product = ?", (quantity, product))
    conn.commit()
    desconect_bd(conn)


def get_stock_info():
    """

    :return:
    """
    conn = connect_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stock")
    stock_info = cursor.fetchall()
    desconect_bd(conn)
    return stock_info


def calculate_stock():
    """

    :return:
    """
    conn = connect_bd()
    cursor = conn.cursor()

    # Selecionar os produtos e a quantidade total retirada
    cursor.execute("""
        SELECT s.Product, s.Available, IFNULL(SUM(o.Quantity), 0) as Retirada
        FROM stock s LEFT JOIN orders o ON s.Product = o.Product
        GROUP BY s.Product
    """)
    stock_data = cursor.fetchall()

    desconect_bd(conn)

    # Calcular a quantidade disponível atualmente
    stock_with_available = []
    for product, available, retirada in stock_data:
        current_available = available - retirada
        stock_with_available.append((product, available, retirada, current_available))

    return stock_with_available


def update_stock_list():
    """
    
    :return:
    """
    stock_list.delete(*stock_list.get_children())
    stock_data = calculate_stock()
    for item in stock_data:
        stock_list.insert("", END, values=item)


# Inicializa a janela principal
window = Tk()
window.title('Gerenciamento Papelaria')
window.geometry('900x600')

# Frame principal
frame = Frame(window)
frame.pack()

# Primeira parte
user_info_frame = LabelFrame(frame, text='Cadastro :')
user_info_frame.grid(row=0, column=0, padx=100, pady=20, sticky=W)

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

# Segunda parte
show_info_frame = LabelFrame(frame, text='Visualizar Cadastros e Estoque')
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
client_list.grid(row=0, column=0, padx=100, columnspan=1, pady=10, sticky=W)

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
order_list.grid(row=0, column=0, padx=100, columnspan=1, pady=10, sticky=W)

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

# Treeview para Estoque
stock_list = ttk.Treeview(aba5, columns=('col1', 'col2', 'col3'))
stock_list.grid(row=0, column=0, padx=150, columnspan=1, pady=10, sticky=W)

stock_list.heading("#0", text="")
stock_list.column("#0", width=0, stretch=NO)
stock_list.heading("#1", text='Produto')
stock_list.column("#1", width=150)
stock_list.heading("#2", text='Disponível')
stock_list.column("#2", width=150)
stock_list.heading("#3", text='Quant. Produto Retirado')
stock_list.column("#3", width=150)

scrollbar3 = ttk.Scrollbar(aba5, orient=VERTICAL)
stock_list.configure(yscroll=scrollbar3.set)
scrollbar3.place(relx=0.95, rely=0.01, relwidth=0.05, relheight=0.95)


# Inicializa banco de dados e interface
create_tab()
select_client()
select_orders()
update_stock_list()
window.mainloop()
