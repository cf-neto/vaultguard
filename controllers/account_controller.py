import pandas as pd
from database.accounts import (
    add,
    delete_account,
    update_account,
    get_account_by_id,
    get_accounts_by_owner
)

class AccountController:

    @staticmethod
    def list_accounts(owner: str, search: str = "") -> pd.DataFrame:
        data = get_accounts_by_owner(owner)

        df = pd.DataFrame(data, columns=["ID", "App", "Username", "Password"])

        if search:
            df = df[df['App'].str.contains(search, case=False, na=False)]

        return df

    @staticmethod
    def create_account(app: str, user: str, password: str, owner: str):
        if not app or not user or not password:
            return False, "Fill in all fields."
        
        add(app, user, password, owner)
        return True, "Account added successfully."

    @staticmethod
    def update_account(account_id: int, app: str, user: str, password: str, owner: str):
        if account_id <= 0:
            return False, "Invalid account ID"

        if not app or not user:
            return False, "App and Username are required."

        updated = update_account(account_id, app, user, password, owner)

        if not updated:
            return False, "App and Username are required."
    
        return True, "Account updated successfully."
    
    @staticmethod
    def delete_account(account_id: int, owner: str):
        if account_id <= 0:
            return False, "Invalid account ID"
        
        deleted = delete_account(account_id, owner)

        if not deleted:
            return False, "Account not found or permission denied"
        
        return True, "Account deleted successfully."
    
    @staticmethod
    def get_account(account_id: int, owner: str):
        if account_id <= 0:
            return False, "Invalid account ID"
        
        account = get_account_by_id(account_id, owner)

        if not account:
            return None, "Account not found or permission denied."
        
        return {
            "app": account[0],
            "user": account[1],
            "password": account[2]
        }, None
