import sqlite3


def create_db():
    conn = sqlite3.connect('transactions.db')

    # Create a cursor object
    c = conn.cursor()

    # Create a table with the specified columns
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_account TEXT,
                to_account TEXT,
                amount REAL,
                date TEXT,
                remarks TEXT)''')

    conn.commit()

    # Close the connection
    conn.close()

def insert_docs(from_account, to_account, amount, date, remarks):
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute("INSERT INTO transactions (from_account, to_account, amount, date, remarks) VALUES (?, ?, ?, ?, ?)", 
              (from_account, to_account, amount, date, remarks))
    conn.commit()
    conn.close()

def fetch_docs():
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute("SELECT * FROM transactions")
    data = c.fetchall()
    conn.close()
    return data

def reports1(from_account,to_account,from_date,to_date):
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    query = '''SELECT * FROM transactions 
               WHERE date BETWEEN ? AND ?
               AND from_account = ?
               AND to_account = ?'''
    c.execute(query, (from_date, to_date, from_account, to_account))
    data = c.fetchall()
    conn.close()
    return data

def reports2(from_account,from_date,to_date):
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    query = '''SELECT * FROM transactions 
               WHERE date BETWEEN ? AND ?
               AND (from_account = ? OR to_account=?)
               '''
    c.execute(query, (from_date, to_date, from_account,from_account))
    data = c.fetchall()
    conn.close()
    
    return data