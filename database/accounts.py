import sqlite3 as sql

conn = sql.connect("data/passwd.db", check_same_thread=False)
cursor = conn.cursor()

# INIT DB
def init():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER NOT NULL,
        app TEXT NOT NULL,
        user TEXT NOT NULL,
        password TEXT,
        user_owner TEXT,
        UNIQUE (user_owner, account_id)           
    )
    """)
    conn.commit()

# ADD ACCOUNT
def add(app, user, password, user_owner):
    account_id = get_next_account_id(user_owner)
    
    cursor.execute(
        "INSERT INTO accounts (account_id, app, user, password, user_owner) VALUES (?, ?, ?, ?, ?)",
        (account_id, app, user, password, user_owner)
    )
    conn.commit()

# DELETE ACCOUNT
def delete_account(account_id, user_owner):
    cursor.execute(
        "DELETE FROM accounts WHERE account_id=? AND user_owner=?",
        (account_id, user_owner)
    )
    conn.commit()
    return cursor.rowcount > 0

def delete_all_accounts(user_owner):
    cursor.execute(
        "DELETE FROM accounts WHERE user_owner=?",
        (user_owner,)
    )
    conn.commit()
    return cursor.rowcount > 0

# UPDATE ACCOUNT
def update_account(account_id: int, app: str, user: str, password: str, user_owner: str) -> bool:
    cursor.execute(
        "UPDATE accounts SET app=?, user=?, password=? WHERE account_id=? and user_owner=?",
        (app, user, password, account_id, user_owner)
    )
    conn.commit()
    return cursor.rowcount > 0

# GET ACCOUNT BY ID
def get_account_by_id(account_id, user_owner):
    cursor.execute("SELECT app, user, password FROM accounts WHERE account_id=? AND user_owner=?", (account_id, user_owner))

    return cursor.fetchone()

# GET NEXT ACCOUNT ID
def get_next_account_id(user_owner):
    cursor.execute(
        "SELECT COALESCE(MAX(account_id), 0) + 1 FROM accounts WHERE user_owner=?",
        (user_owner,)
    )
    return cursor.fetchone()[0]

def get_accounts_by_owner(owner: str):
    cursor.execute(
        "SELECT account_id, app, user, password FROM accounts WHERE user_owner=?", (owner,)
    )

    return cursor.fetchall()

def get_account_stats():
    cursor.execute("SELECT COUNT(*) FROM accounts")
    total_accounts = cursor.fetchone()[0]

    return {"total_accounts": total_accounts}
init()