"""Profile Page - User settings and password management.

Available to all authenticated users for managing their own account.
"""

from __future__ import annotations

import streamlit as st

from sales_dashboard.models import change_user_password

# Ensure user is authenticated (session state set by navigation)
user = st.session_state.user

st.header(f"👤 User Profile - {user.nama}")

# =============================================================================
# 📋 USER INFORMATION
# =============================================================================

st.subheader("📋 Account Information")

# Display user information in a nice format
col1, col2 = st.columns(2)

with col1:
    st.info(f"**Full Name:** {user.nama}")
    st.info(f"**Username:** {user.username}")
    st.info(f"**Email:** {user.email}")

with col2:
    st.info(
        f"**Account Type:** {'🔐 Administrator' if user.is_admin else '👤 Standard User'}"
    )
    st.info(f"**Status:** {'✅ Active' if user.is_active else '❌ Inactive'}")
    st.info(f"**Member Since:** {user.created.strftime('%B %d, %Y')}")

# =============================================================================
# 🔐 PASSWORD MANAGEMENT
# =============================================================================

st.subheader("🔐 Change Password")

st.write("Update your password to keep your account secure.")

with st.form("change_password_form"):
    col1, col2 = st.columns(2)

    with col1:
        current_password = st.text_input(
            "Current Password",
            type="password",
            placeholder="Enter your current password",
        )

    with col2:
        new_password = st.text_input(
            "New Password", type="password", placeholder="Enter new password"
        )

    confirm_password = st.text_input(
        "Confirm New Password", type="password", placeholder="Confirm new password"
    )

    # Form submission
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        submitted = st.form_submit_button(
            "🔄 Update Password", use_container_width=True
        )

    if submitted:
        # Validation
        if not all([current_password, new_password, confirm_password]):
            st.error("❌ Please fill in all password fields")

        elif new_password != confirm_password:
            st.error("❌ New passwords don't match")

        elif len(new_password) < 6:
            st.error("❌ New password must be at least 6 characters long")

        elif new_password == current_password:
            st.warning("⚠️ New password must be different from current password")

        else:
            # Attempt password change
            success = change_user_password(
                user_id=user.id,
                current_password=current_password,
                new_password=new_password,
            )

            if success:
                st.success("✅ Password updated successfully!")
                st.info("ℹ️ Please use your new password for future logins")
            else:
                st.error(
                    "❌ Password change failed. Please check your current password."
                )

# =============================================================================
# 📊 ACCOUNT ACTIVITY
# =============================================================================

st.subheader("📊 Account Activity")

# Show account statistics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Days Since Last Login", value="Today", delta="Active")

with col2:
    st.metric(label="Password Last Changed", value="Recent", delta="Secure")

with col3:
    # Calculate days since account creation
    from datetime import datetime

    if hasattr(user.created, "date"):
        days_old = (datetime.now().date() - user.created.date()).days
        st.metric(label="Account Age", value=f"{days_old} days", delta="Trusted")
    else:
        st.metric(label="Account Age", value="New", delta="Trusted")

# =============================================================================
# ⚙️ ACCOUNT PREFERENCES
# =============================================================================

st.subheader("⚙️ Preferences")

# Placeholder for future settings
col1, col2 = st.columns(2)

with col1:
    st.checkbox("📧 Email notifications", value=True, disabled=True)
    st.caption("Coming soon")

    st.checkbox("🌙 Dark mode", value=False, disabled=True)
    st.caption("Coming soon")

with col2:
    st.selectbox("🌍 Timezone", options=["Asia/Jakarta"], disabled=True)
    st.caption("Coming soon")

    st.selectbox("📊 Default dashboard view", options=["Standard View"], disabled=True)
    st.caption("Coming soon")

# =============================================================================
# 🆘 HELP & SUPPORT
# =============================================================================

with st.expander("🆘 Help & Support", expanded=False):
    st.write("**Need help with your account?**")

    st.write("**Password Requirements:**")
    st.write("- Minimum 6 characters")
    st.write("- Must be different from current password")
    st.write("- Cannot be empty")

    st.write("**Contact Support:**")
    if user.is_admin:
        st.info(
            "As an administrator, you can reset other users' passwords from the User Management page."
        )
    else:
        st.info(
            "Contact your system administrator if you need additional help or account changes."
        )

    st.write("**Security Tips:**")
    st.write("- Change your password regularly")
    st.write("- Don't share your login credentials")
    st.write("- Log out when finished")
