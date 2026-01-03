import streamlit as st
import pandas as pd
import time

from database.accounts import cursor, add, delete_account
from database.users import register_user, verify_user, user_exists

from view.login_view import show_login
from view.accounts_view import show_app

# Page Settings
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

            
# ====================
# ENTRY POINT
# ====================
if not st.session_state.logged_in:
    show_login()
else:
    show_app()