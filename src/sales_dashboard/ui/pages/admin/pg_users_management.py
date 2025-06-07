"""Admin User Management Page - Create and manage user accounts.

Admin-only page for user administration.
"""

from __future__ import annotations

import streamlit as st

from sales_dashboard.models import (
    activate_user,
    admin_reset_user_password,
    create_user_by_admin,
    deactivate_user,
    get_all_active_users,
)

# Ensure user is authenticated and is admin
user = st.session_state.user

if not user.is_admin:
    st.error("❌ Access denied. Admin privileges required.")
    st.stop()

st.header("👥 User Management")

# =============================================================================
# 📊 USER OVERVIEW
# =============================================================================

st.subheader("📊 User Overview")

# Get all users
all_users = get_all_active_users()

# Display user statistics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_users = len(all_users)
    st.metric("Total Users", total_users)

with col2:
    admin_users = sum(1 for u in all_users if u.is_admin)
    st.metric("Administrators", admin_users)

with col3:
    regular_users = total_users - admin_users
    st.metric("Regular Users", regular_users)

with col4:
    st.metric("Active Sessions", "Real-time")

# =============================================================================
# ➕ CREATE NEW USER
# =============================================================================

st.subheader("➕ Create New User")

with st.expander("Create New User Account", expanded=False):
    with st.form("create_user_form"):
        col1, col2 = st.columns(2)

        with col1:
            new_nama = st.text_input("Full Name", placeholder="Enter full name")
            new_username = st.text_input("Username", placeholder="Enter username")

        with col2:
            new_email = st.text_input("Email", placeholder="Enter email address")
            new_password = st.text_input("Initial Password", type="password", placeholder="Set initial password")

        new_is_admin = st.checkbox("Grant Administrator Privileges")

        if new_is_admin:
            st.warning("⚠️ Administrator accounts have full system access")

        submitted = st.form_submit_button("✨ Create User", use_container_width=True)

        if submitted:
            if not all([new_nama, new_username, new_email, new_password]):
                st.error("❌ Please fill in all fields")
            elif len(new_password) < 6:
                st.error("❌ Password must be at least 6 characters long")
            else:
                # Attempt to create user
                new_user = create_user_by_admin(
                    admin_user_id=user.id,
                    nama=new_nama,
                    email=new_email,
                    username=new_username,
                    password=new_password,
                    is_admin=new_is_admin
                )

                if new_user:
                    st.success(f"✅ User '{new_username}' created successfully!")
                    st.info("ℹ️ The user can now log in with their credentials")
                    st.rerun()
                else:
                    st.error("❌ Failed to create user. Username or email may already exist.")

# =============================================================================
# 👥 USER LIST AND MANAGEMENT
# =============================================================================

st.subheader("👥 Existing Users")

if all_users:
    # Create a table of users
    for idx, u in enumerate(all_users):
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 3])

            with col1:
                # User info
                role_icon = "🔐" if u.is_admin else "👤"
                st.write(f"**{role_icon} {u.nama}**")
                st.caption(f"@{u.username} • {u.email}")

            with col2:
                # Status
                status_color = "green" if u.is_active else "red"
                status_text = "Active" if u.is_active else "Inactive"
                st.markdown(f":{status_color}[{status_text}]")
                st.caption(f"ID: {u.id}")

            with col3:
                # Account info
                st.caption(f"Created: {u.created.strftime('%Y-%m-%d')}")
                role_text = "Administrator" if u.is_admin else "Regular User"
                st.caption(f"Role: {role_text}")

            with col4:
                # Actions
                action_col1, action_col2 = st.columns(2)

                with action_col1:
                    # Reset password
                    if st.button("🔄 Reset Password", key=f"reset_pwd_{u.id}"):
                        st.session_state[f"show_reset_{u.id}"] = True

                with action_col2:
                    # Activate/Deactivate (only if not self)
                    if u.id != user.id:
                        if u.is_active:
                            if st.button("❌ Deactivate", key=f"deactivate_{u.id}"):
                                if deactivate_user(user.id, u.id):
                                    st.success(f"User {u.username} deactivated")
                                    st.rerun()
                                else:
                                    st.error("Failed to deactivate user")
                        else:
                            if st.button("✅ Activate", key=f"activate_{u.id}"):
                                if activate_user(user.id, u.id):
                                    st.success(f"User {u.username} activated")
                                    st.rerun()
                                else:
                                    st.error("Failed to activate user")
                    else:
                        st.caption("(You)")

            st.divider()

else:
    st.info("No users found in the system.")

# =============================================================================
# 🔄 PASSWORD RESET MODALS
# =============================================================================

# Handle password reset modals
for u in all_users:
    if st.session_state.get(f"show_reset_{u.id}", False):
        with st.expander(f"🔄 Reset Password for {u.nama}", expanded=True):
            with st.form(f"reset_password_form_{u.id}"):
                new_temp_password = st.text_input(
                    "New temporary password",
                    type="password",
                    key=f"temp_pwd_{u.id}",
                    placeholder="Enter new password (min 6 characters)"
                )

                col_submit, col_cancel = st.columns(2)

                with col_submit:
                    reset_submitted = st.form_submit_button("🔄 Reset Password")

                with col_cancel:
                    if st.form_submit_button("❌ Cancel"):
                        st.session_state[f"show_reset_{u.id}"] = False
                        st.rerun()

                if reset_submitted:
                    if len(new_temp_password) >= 6:
                        if admin_reset_user_password(user.id, u.id, new_temp_password):
                            st.success(f"✅ Password reset for {u.username}")
                            st.session_state[f"show_reset_{u.id}"] = False
                            st.rerun()
                        else:
                            st.error("❌ Failed to reset password")
                    else:
                        st.error("Password must be at least 6 characters")

# =============================================================================
# 📊 USER ACTIVITY LOGS
# =============================================================================

with st.expander("📊 User Activity Logs", expanded=False):
    st.info("**Activity Logging**\n\nComing soon - user login/logout history, password changes, and administrative actions.")

    # Placeholder for future activity logs
    st.write("**Recent Activity:**")
    st.write("- User authentication events")
    st.write("- Password change requests")
    st.write("- Administrative actions")
    st.write("- Account status changes")
