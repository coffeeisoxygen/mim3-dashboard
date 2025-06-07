"""Authentication page - Clean Google/GitHub inspired design."""

from __future__ import annotations

from datetime import datetime

from loguru import logger
import streamlit as st

from sales_dashboard.models.user_operations import authenticate_user
from sales_dashboard.ui.ui_config import ICONS


def show_login_page() -> None:
    """Clean login page inspired by Google/GitHub."""
    # Center the form with columns
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Simple welcome message instead of complex header
        st.markdown(
            "## :streamlit: SDP IM3`Report Management System"
        )  # ✅ Simple and clean
        st.markdown("")  # Simple spacing

        # The login form
        _render_clean_login_form()


@st.fragment
def _render_clean_login_form() -> None:
    """Clean login form - Google/GitHub style."""
    # Check if already logged in
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
            _handle_clean_login(username, password)


def _handle_clean_login(username: str, password: str) -> None:
    """Handle login with clean UX."""
    # Simple validation
    if not username or not password:
        st.error("Please enter both username and password")
        return

    # Clean loading
    with st.spinner("Signing in..."):
        try:
            user = authenticate_user(username, password)

            if user:
                # Set session state
                st.session_state.user = user
                st.session_state.logged_in = True
                st.session_state.login_time = datetime.now()
                st.session_state.last_activity = datetime.now()

                # Simple success
                st.success(f"Welcome, {user.nama}!")
                logger.info(f"User {user.username} logged in successfully")
                st.rerun()
            else:
                # Clean error
                st.error("Invalid credentials")
                logger.warning(f"Failed login attempt for username: {username}")

        except Exception as e:
            logger.error(f"Login error for {username}: {e}")
            st.error("Sign in failed. Please try again.")


def handle_logout() -> None:
    """Clean logout."""
    username = getattr(st.session_state.get("user"), "username", "unknown")

    # Clear session
    st.session_state.user = None
    st.session_state.logged_in = False
    st.session_state.login_time = None
    st.session_state.last_activity = None

    # Log and notify
    logger.info(f"User {username} logged out")
    st.toast("Logged out successfully", icon="✅")
    st.rerun()


def show_user_info_sidebar(user) -> None:
    """Clean sidebar - GitHub style."""
    with st.sidebar:
        # Simple user info
        if user.is_admin:
            st.write(f"👑 **{user.nama}**")
            st.caption(f"Administrator (@{user.username})")
        else:
            st.write(f"👤 **{user.nama}**")
            st.caption(f"User (@{user.username})")

        # Session info
        if st.session_state.get("login_time"):
            login_time = st.session_state.login_time
            st.caption(f"Signed in at {login_time.strftime('%H:%M')}")

        st.divider()
