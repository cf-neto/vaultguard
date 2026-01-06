import pandas as pd

from database.accounts import (
    get_account_stats,
    delete_all_accounts
)

from database.users import (
    is_admin,
    is_super_admin,
    is_user,
    get_user_stats,
    delete_user_by_name as delete_user_by_name_db,
    list_users as list_users_db,
    transform_user_into_admin,
    transform_into_user
)

class AdminController:
    @staticmethod
    def list_users(admin_username: str, search: str = "") -> pd.DataFrame:
        if not (is_admin(admin_username) or is_super_admin(admin_username)):
            return pd.DataFrame()
        
        requester_role = (
            "super-admin" if is_super_admin(admin_username) else "admin"
        )

        data = list_users_db(requester_role)

        df = pd.DataFrame(data, columns=["ID", "Username", "Role"])

        if search:
            df = df[df["Username"].str.contains(search, case=False, na=False)]

        return df



    @staticmethod
    def get_dashboard_data(username: str):
        if not (is_admin(username) or is_super_admin(username)):
            return False, "Restricted admin access"
        

        try:
            user_stats = get_user_stats()
            account_stats = get_account_stats()

            admin_info = {
                "total_users": user_stats.get("total_users", 0),
                "total_accounts": account_stats.get("total_accounts", 0)
            }

            return True, admin_info

        except Exception as e:
            return False, f"Error loading information: {str(e)}"

    @staticmethod
    def check_admin_access(username: str) -> bool:
        return is_admin(username)
    
    @staticmethod
    def check_super_admin_access(username: str) -> bool:
        return is_super_admin(username)

    @staticmethod
    def delete_user(target_username: str, requester_username: str):
        if not target_username:
            return False, "Invalid username"

        # Nunca permitir deletar super-admin
        if is_super_admin(target_username):
            return False, f"{target_username} is super-admin"

        # Verifica permissão do requester
        if is_super_admin(requester_username):
            pass  # pode continuar
        elif is_admin(requester_username):
            if is_admin(target_username):
                return False, f"{target_username} is administrator"
        else:
            return False, "Permission denied"

        # Primeiro deleta dados relacionados
        delete_all_accounts(target_username)

        # Depois deleta o usuário
        deleted = delete_user_by_name_db(target_username)

        if not deleted:
            return False, "User not found"

        return True, f"User {target_username} deleted successfully."


    @staticmethod
    def promote_to_admin(username):
        if is_admin(username):
            return False, f"{username} is already an admin."
        
        try:
            return transform_user_into_admin(username)
        except Exception as e:
            return False, f"Error promoting user: {e}"
        
    
    @staticmethod
    def remove_admin(username):
        if is_user(username):
            return False, f"{username} is already an user."
            
        try:
            return transform_into_user(username)
        except Exception as e:
            return False, f"Error removing user: {e}"