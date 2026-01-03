import sqlite3 as sql
import bcrypt

from services.password_service import is_strong_password

conn = sql.connect("data/passwd.db", check_same_thread=False)
cursor = conn.cursor()

def init_users():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()

def register_user(username, password):
    try:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cursor.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True, "User registered successfully"
    except sql.IntegrityError:
        return False, "Username already exists"


def verify_user(username, password):
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    
    if result:
        return bcrypt.checkpw(password.encode(), result[0])
    return False

def user_exists(username):
    cursor.execute("SELECT 1 FROM users WHERE username=?", (username,))
    return cursor.fetchone() is not None

init_users()