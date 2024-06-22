import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Tworzy połączenie z bazą danych SQLite"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Połączono z SQLite wersja: {sqlite3.version}")
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """Tworzy tabelę na podstawie podanego polecenia SQL"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = "library.db"

    sql_create_books_table = """ CREATE TABLE IF NOT EXISTS books (
                                    id integer PRIMARY KEY,
                                    title text NOT NULL,
                                    author text NOT NULL,
                                    publication_year integer,
                                    isbn text
                                ); """

    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                email text NOT NULL UNIQUE
                            );"""

    sql_create_borrows_table = """CREATE TABLE IF NOT EXISTS borrows (
                                    id integer PRIMARY KEY,
                                    book_id integer NOT NULL,
                                    user_id integer NOT NULL,
                                    borrow_date text NOT NULL,
                                    return_date text,
                                    FOREIGN KEY (book_id) REFERENCES books (id),
                                    FOREIGN KEY (user_id) REFERENCES users (id)
                                );"""

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_books_table)
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_borrows_table)
        conn.close()
    else:
        print("Błąd! Nie można utworzyć połączenia z bazą danych.")

if __name__ == '__main__':
    main()

def add_book(conn, book):
    """Dodaje nową książkę do bazy danych"""
    sql = ''' INSERT INTO books(title,author,publication_year,isbn)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, book)
    conn.commit()
    return cur.lastrowid

def add_user(conn, user):
    """Dodaje nowego użytkownika do bazy danych"""
    sql = ''' INSERT INTO users(name,email)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

conn = create_connection(database)
with conn:
    book = ('1984', 'George Orwell', 1949, '9780451524935')
    book_id = add_book(conn, book)
    print(f"Dodano książkę o ID: {book_id}")

    user = ('Jan Kowalski', 'jan@example.com')
    user_id = add_user(conn, user)
    print(f"Dodano użytkownika o ID: {user_id}")