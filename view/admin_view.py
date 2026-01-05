import time
import streamlit as st

from controllers.admin_controller import AdminController

def show_info():
    # ====================
    # ACCESS
    # ====================
    if not AdminController.check_admin_access(st.session_state.username):
        st.error("Acesso restrito ao administrador.")
        return
    
    # ====================
    # TITLE AND SUB
    # ====================
    st.subheader("Admin Panel")
    st.caption("Here is the admin panel; you can view data, delete users, reset passwords, and much more.")
    st.divider()

    # ====================
    # CHECK IF THE USER IS AN ADMIN
    # ====================
    ok, data = AdminController.get_dashboard_data(
        st.session_state.username
    )

    if not ok:
        st.error(data)
        return


    # ====================
    # KPI WITH USERS INFO
    # ====================
    col1, col2 = st.columns(2, gap="large")

    # Total Users
    with col1:
        st.metric(
            label="Total Users",
            value=f"{data['total_users']:,}",
            help="Total number of users registered in the system."
        )
        st.caption("Current user base")

    # Total Accounts
    with col2:
        st.metric(
            label="Total Accounts",
            value=f"{data['total_accounts']:,}",
            help="Total number of accounts associated with users"
        )
        st.caption("Total volume of registered accounts")

    st.divider()

    # ====================
    # TEXT INPUT TO SEARCH USERS
    # ====================
    st.subheader("Registered Users")
    search = st.text_input("Search user:", key="Text_input to search users")

    df = AdminController.list_users(st.session_state.username, search=search)
    # DATAFRAME WITH ID, USERNAME
    st.dataframe(df, width="stretch")


    st.subheader("Delete Account")

    username_delete = st.text_input("Username to delete")

    if st.button("Delete", key="Button_delete_user"):
            ok, msg = AdminController.delete_user(username_delete)
            

            if ok:
                st.success(msg)
                time.sleep(1)
                st.rerun()
            else:
                st.error(msg)
                time.sleep(1)
                st.rerun()

    st.divider()