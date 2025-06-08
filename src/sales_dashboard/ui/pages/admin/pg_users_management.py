"""Admin User Management Page - Create and manage user accounts.

🔒 SECURITY: Admin-only page (ADMIN_ONLY access).
🛡️ BYPASS PROTECTION: Direct URL access is validated and blocked for non-admin users.
"""

from __future__ import annotations

import streamlit as st

from sales_dashboard.config.messages import (
    BUTTON_CREATE_USER,
    ERROR_REQUIRED_FIELDS,
    USER_MGMT_ACTIVITY_ADMIN,
    USER_MGMT_ACTIVITY_AUTH,
    USER_MGMT_ACTIVITY_INFO,
    USER_MGMT_ACTIVITY_PASSWORD,
    USER_MGMT_ACTIVITY_RECENT,
    USER_MGMT_ACTIVITY_STATUS,
    USER_MGMT_CREATE_EXPAND,
    USER_MGMT_CREATE_HEADER,
    USER_MGMT_EMAIL,
    USER_MGMT_FULL_NAME,
    USER_MGMT_GRANT_ADMIN,
    USER_MGMT_HEADER,
    USER_MGMT_INITIAL_PASSWORD,
    USER_MGMT_LOGIN_INFO,
    USER_MGMT_NO_USERS,
    USER_MGMT_PLACEHOLDER_EMAIL,
    USER_MGMT_PLACEHOLDER_NAME,
    USER_MGMT_PLACEHOLDER_PASSWORD,
    USER_MGMT_PLACEHOLDER_USERNAME,
    USER_MGMT_USERNAME,
    WARNING_ADMIN_PRIVILEGES,
)
from sales_dashboard.core.page_registry import page_registry
from sales_dashboard.models import (
    activate_user,
    admin_reset_user_password,
    create_user_by_admin,
    deactivate_user,
    get_all_active_users,
)


def main() -> None:
    """User management page with bypass-proof admin security."""

    # 🔒 SECURITY VALIDATION: Prevents direct URL bypass
    page_config = page_registry.get_page_config("user_management")
    user = page_config.validate_access_or_stop()  # Guaranteed admin user or st.stop()    # 🎯 Page logic - user is guaranteed valid admin
    st.header(USER_MGMT_HEADER)

    # ===== USER OVERVIEW =====
    st.subheader("📊 User Overview")

    all_users = get_all_active_users()

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

    # ===== CREATE NEW USER =====
    st.subheader(USER_MGMT_CREATE_HEADER)

    with st.expander(USER_MGMT_CREATE_EXPAND, expanded=False):
        with st.form("create_user_form"):
            col1, col2 = st.columns(2)

            with col1:
                new_nama = st.text_input(
                    USER_MGMT_FULL_NAME, placeholder=USER_MGMT_PLACEHOLDER_NAME
                )
                new_username = st.text_input(
                    USER_MGMT_USERNAME, placeholder=USER_MGMT_PLACEHOLDER_USERNAME
                )

            with col2:
                new_email = st.text_input(
                    USER_MGMT_EMAIL, placeholder=USER_MGMT_PLACEHOLDER_EMAIL
                )
                new_password = st.text_input(
                    USER_MGMT_INITIAL_PASSWORD,
                    type="password",
                    placeholder=USER_MGMT_PLACEHOLDER_PASSWORD,
                )

            new_is_admin = st.checkbox(USER_MGMT_GRANT_ADMIN)

            if new_is_admin:
                st.warning(WARNING_ADMIN_PRIVILEGES)

            submitted = st.form_submit_button(
                BUTTON_CREATE_USER, use_container_width=True
            )

            if submitted:
                if not all([new_nama, new_username, new_email, new_password]):
                    st.error(ERROR_REQUIRED_FIELDS)
                elif len(new_password) < 6:
                    st.error("❌ Password must be at least 6 characters long")
                else:
                    new_user = create_user_by_admin(
                        admin_user_id=user.id,
                        nama=new_nama,
                        email=new_email,
                        username=new_username,
                        password=new_password,
                        is_admin=new_is_admin,
                    )

                    if new_user:
                        st.success(f"✅ User '{new_username}' created successfully!")
                        st.info(USER_MGMT_LOGIN_INFO)
                        st.rerun()
                    else:
                        st.error(
                            "❌ Failed to create user. Username or email may already exist."
                        )

    # ===== USER LIST AND MANAGEMENT =====
    st.subheader("👥 Existing Users")

    if all_users:
        for idx, u in enumerate(all_users):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 3])

                with col1:
                    role_icon = "🔐" if u.is_admin else "👤"
                    st.write(f"**{role_icon} {u.nama}**")
                    st.caption(f"@{u.username} • {u.email}")

                with col2:
                    status_color = "green" if u.is_active else "red"
                    status_text = "Active" if u.is_active else "Inactive"
                    st.markdown(f":{status_color}[{status_text}]")
                    st.caption(f"ID: {u.id}")

                with col3:
                    st.caption(f"Created: {u.created.strftime('%Y-%m-%d')}")
                    role_text = "Administrator" if u.is_admin else "Regular User"
                    st.caption(f"Role: {role_text}")

                with col4:
                    action_col1, action_col2 = st.columns(2)

                    with action_col1:
                        if st.button("🔄 Reset Password", key=f"reset_pwd_{u.id}"):
                            st.session_state[f"show_reset_{u.id}"] = True

                    with action_col2:
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
        st.info(USER_MGMT_NO_USERS)

    # ===== PASSWORD RESET MODALS =====
    for u in all_users:
        if st.session_state.get(f"show_reset_{u.id}", False):
            with st.expander(f"🔄 Reset Password for {u.nama}", expanded=True):
                with st.form(f"reset_password_form_{u.id}"):
                    new_temp_password = st.text_input(
                        "New temporary password",
                        type="password",
                        key=f"temp_pwd_{u.id}",
                        placeholder="Enter new password (min 6 characters)",
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
                            if admin_reset_user_password(
                                user.id, u.id, new_temp_password
                            ):
                                st.success(f"✅ Password reset for {u.username}")
                                st.session_state[f"show_reset_{u.id}"] = False
                                st.rerun()
                            else:
                                st.error("❌ Failed to reset password")
                        else:
                            st.error("Password must be at least 6 characters")

    # ===== USER ACTIVITY LOGS =====
    with st.expander("📊 User Activity Logs", expanded=False):
        st.info(USER_MGMT_ACTIVITY_INFO)

        st.write(USER_MGMT_ACTIVITY_RECENT)
        st.write(USER_MGMT_ACTIVITY_AUTH)
        st.write(USER_MGMT_ACTIVITY_PASSWORD)
        st.write(USER_MGMT_ACTIVITY_ADMIN)
        st.write(USER_MGMT_ACTIVITY_STATUS)


# Entry point for navigation
main()
