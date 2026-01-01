import sqlite3 as sql

conn = sql.connect("passwd.db", check_same_thread=False)
cursor = conn.cursor()

def init():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app TEXT NOT NULL,
        user TEXT NOT NULL,
        password TEXT,
        user_owner TEXT           
    )
    """)
    conn.commit()

def add(app, user, password, user_owner):
    cursor.execute(
        "INSERT INTO accounts (app, user, password, user_owner) VALUES (?, ?, ?, ?)",
        (app, user, password, user_owner)
    )
    conn.commit()

def delete_account(account_id, user_owner):
    cursor.execute("DELETE FROM accounts WHERE id=? AND user_owner=?", (account_id, user_owner))
    conn.commit()
    return cursor.rowcount > 0

def update_account(account_id, app, user, password, user_owner):
    cursor.execute(
        "UPDATE accounts SET app=?, user=?, password=? WHERE id=? and user_owner=?",
        (app, user, password, account_id, user_owner)
    )
    cursor.connection.commit()
    return cursor.rowcount > 0

def get_account_by_id(account_id, user_owner):
    cursor.execute("SELECT app, user, password FROM accounts WHERE id=? AND user_owner=?",
    (account_id, user_owner)
    )

    return cursor.fetchone()

init()