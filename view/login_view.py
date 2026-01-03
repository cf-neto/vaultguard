import streamlit as st
import time

from controllers.auth_controller import AuthController

def show_login():
    # Login/Registration Interface
    st.title("🔐 Login / Register")

    tabs = st.tabs(["Login", "Register"]) 

    # TAB LOGIN
    with tabs[0]:
        st.subheader("Login")

        with st.form("login_form"):
            username = st.text_input("Username:")
            password = st.text_input("Password:", type="password")
            login = st.form_submit_button("Login")

        if login:
            success, message = AuthController.login(username, password)

            if success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(message)
                time.sleep(1)
                st.rerun()
            else:
                st.error(message)

    # TAB REGISTER
    with tabs[1]:
        st.subheader("Register")

        with st.form("register_form"):
            new_user = st.text_input("Username:")
            new_pass = st.text_input("Password:", type="password")
            register = st.form_submit_button("Register")

            if register:
                success, message = AuthController.register(new_user, new_pass)

                if success:
                    st.success(message)
                    st.info("You can now log in.")
                else:
                    st.error(message)
