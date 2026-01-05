import pandas as pd

from database.accounts import (
    get_account_stats,
    delete_all_accounts
)

from database.users import (
    is_admin,
    get_user_stats,
    delete_user_by_name as delete_user_by_name_db,
    list_users as list_users_db
)

class AdminController:
    @staticmethod
    def list_users(admin_username: str, search: str = "") -> pd.DataFrame:
        if not is_admin(admin_username):
            return None
        
        data = list_users_db()
        df = pd.DataFrame(data, columns=["ID", "Username"])
    
        if search:
            df = df[df['Username'].str.contains(search, case=False, na=False)]

        return pd.DataFrame(data, columns=["Id", "Username"])

    @staticmethod
    def get_dashboard_data(username: str):
        if not is_admin(username):
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
    def delete_user(username: str):
        if not username:
            return False, "Invalid username"

        if is_admin(username):
            return False, f"{username} is administrator"

        # First delete all accounts
        delete_all_accounts(username)

        # After delete user
        deleted = delete_user_by_name_db(username)

        if not deleted:
            return False, "User not found or permission denied"

        return True, f"User {username} deleted successfully."
