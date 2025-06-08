"""Authentication page - Clean Google/GitHub inspired design."""

from __future__ import annotations

from loguru import logger
import streamlit as st

from sales_dashboard.core.streamlit_session_manager import session_manager
from sales_dashboard.models.user_operations import authenticate_user
from sales_dashboard.ui.ui_config import ICONS


def show_login_page() -> None:
    """Clean login page inspired by Google/GitHub.

    Note: This page doesn't use auth wrappers because it IS the auth solution.
    """
    # Center the form with columns
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Simple welcome message
        st.markdown("## Welcome")  # Clean and simple
        st.markdown("")  # Simple spacing

        # The login form
        _render_clean_login_form()


@st.fragment
def _render_clean_login_form() -> None:
    """Clean login form - Google/GitHub style."""
    # Check if already logged in - use Streamlit native session state
    if st.session_state.get("logged_in", False):
        st.success("✅ Login successful! Redirecting...")
        st.rerun()
        return

    with st.form("login_form", clear_on_submit=False):
        # Clean input fields
        username = st.text_input(
            "Username", placeholder="Enter your username", key="auth_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="auth_password",
        )

        # Clean submit button
        submitted = st.form_submit_button(
            "Sign In", type="primary", icon=ICONS.LOGIN, use_container_width=True
        )

        if submitted:
            _handle_login(username, password)


def _handle_login(username: str, password: str) -> None:
    """Handle login with clean UX and proper error handling."""
    # Simple validation
    if not username or not password:
        st.error("Please enter both username and password")
        return

    # Clean loading with proper error boundaries
    with st.spinner("Signing in..."):
        try:
            user = authenticate_user(username, password)

            if user:
                # Use session manager for login with persistence
                session_manager.login_user(user, remember=True)

                # Simple success message
                st.success(f"Welcome, {user.nama}!")
                st.rerun()
            else:
                # Clean error - user-friendly for MIM3 office
                st.error("❌ Username atau password salah")
                logger.warning(f"Failed login attempt for username: {username}")

        except Exception as e:
            logger.error(f"Login error for {username}: {e}")
            st.error("❌ Gagal masuk. Silakan coba lagi atau hubungi administrator.")


def handle_logout() -> None:
    """Clean logout - delegates to session manager."""
    try:
        session_manager.logout_user()
        st.success("👋 Anda telah keluar. Terima kasih!")
        st.rerun()
    except Exception as e:
        logger.error(f"Logout error: {e}")
        # Still logout even if there's an error - fail-safe approach
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()
