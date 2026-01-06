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
        cursor.execute("SELECT COUNT(*) FROM users")
        total = cursor.fetchone()[0]

        role = "super-admin" if total == 0 else "user"

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed, role)
        )
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

def list_users(requester_role):
    if requester_role == "super-admin":
        cursor.execute("SELECT id, username, role FROM users")
    else:
        cursor.execute("""
            SELECT id, username, role
            FROM users
            WHERE role IN ('user', 'admin')
        """)
    return cursor.fetchall()

def is_admin(username):
    cursor.execute(
        "SELECT role FROM users WHERE username=?",
        (username,)
    )
    row = cursor.fetchone()
    return row and row[0] == "admin"

def is_user(username):
    cursor.execute(
        "SELECT role FROM users WHERE username=?",
        (username,)
    )
    row = cursor.fetchone()
    return row and row[0] == "user"

def is_super_admin(username):
    cursor.execute(
        "SELECT role FROM users WHERE username=?",
        (username,)
    )
    row = cursor.fetchone()
    return row and row[0] == "super-admin"


def delete_user_by_name(username):
    cursor.execute(
        "DELETE FROM users WHERE username=?",
        (username,)
    )
    conn.commit()
    return cursor.rowcount > 0

def transform_user_into_admin(username):
    cursor.execute("UPDATE users SET role = 'admin' WHERE username=? and role !='admin'", (username,))
    
    if cursor.rowcount == 0:
        return False, "User not found or already an administrator."

    conn.commit()
    return True, "User successfully promoted to administrator."

def transform_into_user(username):
    cursor.execute("UPDATE users SET role = 'user' WHERE username=? and role ='admin'", (username,))
    
    if cursor.rowcount == 0:
        return False, "User not found or already a user."

    conn.commit()
    return True, "User successfully removed as administrator."

init_users()