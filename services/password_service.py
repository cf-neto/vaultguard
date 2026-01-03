import string
import random

COMMON_PASSWORDS = {"12345678", "senha123", "password"}

def is_strong_password(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Senha muito curta"
    
    if password.lower() in COMMON_PASSWORDS:
        return False, "Password common"
    
    if not any(c.isupper() for c in password):
        return False, "Add a capital letter."
    
    if not any(c.islower() for c in password):
        return False, "Add a lower letter."
    
    if not any(c.isdigit() for c in password):
        return False, "Add a number."
    
    if not any(c in "!@#$%&_/|\][*" for c in password):
        return False, "Adicione símbolo"
    
    return True, "Strong password"