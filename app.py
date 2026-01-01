import streamlit as st
import pandas as pd
from database.accounts import cursor, add, delete_account
from database.users import register_user, verify_user, user_exists
import time

st.set_page_config(
    page_title="VaultGuard ",
    page_icon="🔐",
    layout="centered",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');
    * {
        font-family: "Poppins", sans-serif;
        font-weight: 100;
        font-style: normal;
    }
</style>
""", unsafe_allow_html=True)

# --------------------
#   LOGIN
# --------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""


def show_login():
    st.title("🔐 Login / Register")

    tabs = st.tabs(["Login", "Register"]) 

    # ---------- REGISTER ----------
    with tabs[1]:
        st.subheader("Register")

        with st.form("register_form"):
            new_user = st.text_input("Username")
            new_pass = st.text_input("Password", type="password")
            register_submit = st.form_submit_button("Register")

            if register_submit:
                if not new_user or not new_pass:
                    st.warning("Fill all fields")
                elif user_exists(new_user):
                    st.error("User already exists")
                else:
                    register_user(new_user, new_pass)
                    st.success("User registered successfully!")
    # ---------- LOGIN ----------
    with tabs[0]:
        st.subheader("Login")

        with st.form("login_form"):
            username = st.text_input("Username: ")
            password = st.text_input("Password: ", type="password")
            login_submit = st.form_submit_button("Login")

        if login_submit:
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Incorrect username or password")


def show_app():
    st.title("🔐 VaultGuard ")

    # --------------------
    #   MENU
    # --------------------
    tabs = st.tabs(["Registered Accounts", "Manage Account", "Settings"])

    # --------------------
    #   REGISTERED ACCOUNTS
    # --------------------
    with tabs[0]:
        st.subheader("Registered Accounts")
        search = st.text_input("Search account:")

        table_placeholder = st.empty()

        def show_table(filter=""):
            cursor.execute(
                "SELECT account_id, app, user, password FROM accounts WHERE user_owner=?",
                (st.session_state.username,)
            )
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=["ID", "App", "Username", "Password"])

            if filter:
                df = df[df['App'].str.contains(filter, case=False, na=False)]

            table_placeholder.dataframe(df, width='stretch')

        show_table(search)

    # --------------------
    #   FIELD SEARCH
    # --------------------
    with tabs[1]:
        # NEW ACCOUNT
        st.subheader("Add new account")
        with st.form("add_form"):
            app_name = st.text_input("App / Platform", key="app_name")
            user = st.text_input("Username / Email", key="user_name")
            password = st.text_input("Password", type="password", key="pass_word")
            submitted = st.form_submit_button("Save")
            if submitted:
                if app_name and user and password:
                    add(app_name, user, password, st.session_state.username)

                    # Clear the fields
                    st.success("Account added successfully!")
                    time.sleep(2)

                    st.rerun()
                else:
                    st.warning("Fill all fields before saving.")
        
        st.divider()

        # EDIT
        st.subheader("Edit Account")
        account_id = st.number_input("Account ID to edit", min_value=1, step=1)
        
        current_data = None
        if account_id > 0:
            cursor.execute(
                "SELECT app, user, password FROM accounts WHERE account_id=? AND user_owner=?",
                (account_id, st.session_state.username)
            )
            current_data = cursor.fetchone()
        
        if current_data:
            pass
        else:
            if account_id > 0:
                st.warning("No account found with this ID or you don't have permission to edit it.")

        with st.form("edit_form"):
            app_value = current_data[0] if current_data else ""
            user_value = current_data[1] if current_data else ""
            password_value = current_data[2] if current_data else ""
            
            new_app = st.text_input("App / Platform", value=app_value)
            new_user = st.text_input("Username / Email", value=user_value)
            new_password = st.text_input("Password", type="password", value=password_value)
            
            submitted_edit = st.form_submit_button("Update Account")
            
            if submitted_edit:
                if not new_app or not new_user:
                    st.error("App and Username fields are required!")
                elif account_id <= 0:
                    st.error("Please enter a valid Account ID!")
                else:
                    try:
                        if not new_password and current_data:
                            final_password = current_data[2]
                        else:
                            final_password = new_password
                        
                        # UPDATE DB
                        cursor.execute(
                            "UPDATE accounts SET app=?, user=?, password=? WHERE account_id=? AND user_owner=?",
                            (new_app, new_user, final_password, account_id, st.session_state.username)
                        )
                        cursor.connection.commit()
                        
                        if cursor.rowcount > 0:
                            st.success("Account updated successfully!")
                            time.sleep(2)

                            st.rerun()
                        else:
                            st.error("Account not found.")
                            
                    except Exception as e:
                        st.error(f"Error updating account: {str(e)}")

        st.divider()

        st.divider()

        # DELETE ACCOUNT
        st.subheader("Delete Account")

        account_id = st.number_input("Account ID to delete", min_value=1, step=1)

        if st.button("Delete"):
            if delete_account(account_id, st.session_state.username):
                st.success("Deleted successfully")
                show_table(search)
            else:
                st.error("ID does not exist")

        st.divider()


    # --------------------
    #   SETTINGS
    # --------------------
    with tabs[2]:
        st.subheader("Settings")

        st.write("Account:")
        st.text_input("Username", value=st.session_state.username, disabled=True)
        st.text_input("Password", value="*******", disabled=True)

        # LOGOUT
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()         
        
        st.divider()
            
# ====================
# ENTRY POINT
# ====================
if not st.session_state.logged_in:
    show_login()
else:
    show_app()