import time
import streamlit as st

from controllers.admin_controller import AdminController

def show_info():
    # ====================
    # ACCESS
    # ====================
    if not (
        AdminController.check_admin_access(st.session_state.username)
        or AdminController.check_super_admin_access(st.session_state.username)
    ):
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

    tabs = st.tabs(["System Overview", "Users", "Administration"])

    # ====================
    # KPI WITH USERS INFO
    # ====================
    with tabs[0]:
        st.subheader("📊 System Overview")
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
    with tabs[1]:

        st.subheader("👥 Registered Users")
        search = st.text_input("Search by username", placeholder="Type a username...", key="search_users")

        df = AdminController.list_users(st.session_state.username, search=search)
        # DATAFRAME WITH ID, USERNAME
        st.dataframe(df, width="stretch")

        st.divider()

    # ====================
    # DANGER ZONE
    # ====================
    with tabs[2]:
        st.subheader("⚠️ Danger Zone")
        st.caption("Actions in this section are irreversible.")

        username_delete = st.text_input("Username to delete")

        if st.button("Delete", key="Button_delete_user", type="primary"):
                ok, msg = AdminController.delete_user(username_delete, st.session_state.username)
                
                if ok:
                    st.success(msg)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(msg)
                    time.sleep(1)
                    st.rerun()

        st.divider()

        st.subheader("Promote User to Admin")
        st.caption("Grant administrator privileges to an existing user.")

        username = st.text_input(
            "Username",
            placeholder="Exact username",
            key="promote_admin_username"
        )

        # Segurança mínima
        confirm = st.checkbox(
            "I understand that this user will have full administrative access"
        )

        col1, col2 = st.columns(2)

        with col1:
            promote_btn = st.button(
                "Promote to Admin",
                disabled=not (username.strip() and confirm)
            )

        with col2:
            remove_admin_btn = st.button(
                "Remove Admin",
                disabled=not (username.strip() and confirm)
            )

        if promote_btn:
            ok, msg = AdminController.promote_to_admin(username)

            if ok:
                st.success(msg)
            else:
                st.error(msg)

            time.sleep(1.5)
            st.rerun()


        if remove_admin_btn:
            ok, msg = AdminController.remove_admin(username)

            if ok:
                st.success(msg)
            else:
                st.error(msg)

            time.sleep(1.5)
            st.rerun()
