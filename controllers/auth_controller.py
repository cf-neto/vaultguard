from database.users import verify_user, user_exists, register_user
from services.password_service import is_strong_password


class AuthController:
    @staticmethod
    def login(username: str, password: str):
        if not username or not password:
            return False, "Fill in all the fields."
        
        if verify_user(username, password):
            return True, f"Welcome, {username}"
        
        return False, "Incorrect username or password"
    
    @staticmethod
    def register(username: str, password: str):
        valid, message = is_strong_password(password)
        if not valid:
            return False, message
        
        return register_user(username, password)