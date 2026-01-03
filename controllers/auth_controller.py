from database.users import verify_user, user_exists, register_user

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
        if not username or not password:
            return False, "Fill in all the fields."
        
        if user_exists(username):
            return False, "User already exists"
        
        try:
            register_user(username, password)
            return True, "User successfully registered!"
        
        except Exception as e:
            return False, f"Error when registering: {str(e)}"
        