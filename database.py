import sqlite3

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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Product TEXT NOT NULL,
            Available INTEGER NOT NULL
        );
    """)
    conn.commit()
    desconect_bd(conn)