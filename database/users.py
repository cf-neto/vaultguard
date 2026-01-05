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
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user'
    )
    """)
    conn.commit()

def register_user(username, password):
    try:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
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

def get_user_stats():
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    return {
        "total_users": total_users
    }

def list_users():
    cursor.execute("SELECT id, username FROM users")
    return cursor.fetchall()

def is_admin(username):
    cursor.execute("SELECT username FROM users ORDER BY id ASC LIMIT 1")
    result = cursor.fetchone()

    return result and result[0] == username

def delete_user_by_name(username):
    cursor.execute(
        "DELETE FROM users WHERE username=?",
        (username,)
    )
    conn.commit()
    return cursor.rowcount > 0



init_users()