"""Authentication page - Clean Google/GitHub inspired design."""

from __future__ import annotations

from loguru import logger
import streamlit as st

from sales_dashboard.core.streamlit_session_manager import session_manager
from sales_dashboard.models.user_operations import authenticate_user


def main() -> None:
    """Main authentication page - native Streamlit approach.

    Note: No st.set_page_config() when used with official navigation.
    Page config is handled by the main app (home.py).
    """
    show_login_page()


def show_login_page() -> None:
    """Clean login page inspired by Google/GitHub."""
    # Center the form with columns
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Simple welcome message
        st.markdown("## Welcome")
        st.markdown("")

        # The login form
        _render_clean_login_form()


def _render_clean_login_form() -> None:
    """Clean login form - Google/GitHub style.

    Removed @st.fragment to avoid duplicate form key issues.
    """
    # Check if already logged in
    if st.session_state.get("logged_in", False):
        st.success("✅ Login successful! Redirecting...")
        # Navigation will handle this automatically
        return

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input(
            "Username", placeholder="Enter your username", key="auth_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="auth_password",
        )

        submitted = st.form_submit_button(
            "🔐 Sign In", type="primary", use_container_width=True
        )

        if submitted:
            _handle_login(username, password)


def _handle_login(username: str, password: str) -> None:
    """Handle login with clean UX and proper error handling."""
    if not username or not password:
        st.error("Please enter both username and password")
        return

    with st.spinner("Signing in..."):
        try:
            user = authenticate_user(username, password)

            if user:
                session_manager.login_user(user, remember=True)
                st.success(f"Welcome, {user.nama}!")
                # Let navigation handle the redirect automatically
                st.rerun()
            else:
                st.error("❌ Username atau password salah")
                logger.warning(f"Failed login attempt for username: {username}")

        except Exception as e:
            logger.error(f"Login error for {username}: {e}")
            st.error("❌ Gagal masuk. Silakan coba lagi atau hubungi administrator.")


# Entry point for navigation
main()
