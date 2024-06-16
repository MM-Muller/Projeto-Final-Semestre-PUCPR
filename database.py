"""
Módulo: Sistema de Gerenciamento de Funcionários e Estoque
Data: 09/06/2024
Versão: 1.0
Descrição: Sistema para gerenciar funcionários, pedidos e estoque utilizando SQLite.
"""

import sqlite3


def connect_bd():
    """
    Conecta ao banco de dados SQLite.

    :return: Conexão com o banco de dados.
    """
    return sqlite3.connect('employee.db')


def desconect_bd(conn):
    """
    Fecha a conexão com o banco de dados.

    :param conn: Conexão com o banco de dados.
    :return: None
    """
    conn.close()


def create_tab():
    """
    Cria as tabelas necessárias no banco de dados.

    :return: None
    """
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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Product TEXT NOT NULL,
            Available INTEGER NOT NULL
        );
    """)
    conn.commit()
    desconect_bd(conn)