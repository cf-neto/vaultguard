import streamlit as st
import time

from controllers.account_controller import AccountController

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

        df = AccountController.list_accounts(owner=st.session_state.username, search=search)

        st.dataframe(df, width="stretch")


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
                ok, msg = AccountController.create_account(app_name, user, password, st.session_state.username)

                if ok:
                    st.success(msg)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(msg)
        
        st.divider()

        # EDIT
        st.subheader("Edit Account")

        account_id = st.number_input("Account ID to edit", min_value=1, step=1)
        
        current_data = None
        if account_id:
            account_data, error = AccountController.get_account(account_id, st.session_state.username)
            if error:
                st.warning(error)


        with st.form("edit_form"):
            new_app = st.text_input(
                "App / Platform",
                value=account_data["app"] if account_data else ""
                )

            new_user = st.text_input(
                "Username / Email",
                value=account_data["user"] if account_data else ""
                )

            new_password = st.text_input(
                "Password", type="password",
                value=account_data["password"] if account_data else ""
                )
            
            submitted = st.form_submit_button("Update Account")
            
            if submitted:
                ok, msg = AccountController.update_account(account_id, new_app, new_user, new_password, st.session_state.username)

                if ok:
                    st.success(msg)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(msg)

        st.divider()

        st.divider()

        # DELETE ACCOUNT
        st.subheader("Delete Account")

        account_id = st.number_input("Account ID to delete", min_value=1, step=1)
        confirm_checkbox = st.checkbox("I confirm the deletion")

        if st.button("Delete"):
            if not confirm_checkbox:
                st.warning("Please confirm before deleting.")
            
            else:
                ok, msg = AccountController.delete_account(account_id, st.session_state.username)

                if ok:
                    st.success(msg)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(msg )

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