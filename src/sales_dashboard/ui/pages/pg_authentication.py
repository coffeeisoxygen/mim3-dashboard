"""Authentication page - Clean Google/GitHub inspired design with fragments."""

from __future__ import annotations

from loguru import logger
import streamlit as st

from sales_dashboard.config.messages import (
    AUTH_ENTER_CREDENTIALS,
    AUTH_LOGIN_ERROR,
    AUTH_LOGIN_REDIRECT_INFO,
    AUTH_LOGIN_SUCCESS,
    AUTH_PLEASE_WAIT,
    AUTH_SIGNING_IN,
    AUTH_WELCOME_TITLE,
    AUTH_WELCOME_USER,
    ERROR_INVALID_CREDENTIALS,
)
from sales_dashboard.core.streamlit_session_manager import session_manager
from sales_dashboard.models.user_operations import authenticate_user


def main() -> None:
    """Main authentication page - native Streamlit approach."""
    show_login_page()


def show_login_page() -> None:
    """Clean login page inspired by Google/GitHub."""
    # ✅ Check if user is already logged in (outside fragment)
    if st.session_state.get("logged_in", False):
        _show_success_state()
        return

    # ✅ Show login form with fragment isolation
    _show_login_form_with_fragment()


def _show_success_state() -> None:
    """Show success state when user is logged in."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.success(AUTH_LOGIN_SUCCESS)
        st.info(AUTH_LOGIN_REDIRECT_INFO)


@st.fragment
def _show_login_form_with_fragment() -> None:
    """Login form isolated in fragment for better performance."""
    # Center the form with columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Simple welcome message
        st.markdown(f"## {AUTH_WELCOME_TITLE}")
        st.markdown("")

        # ✅ Check fragment-specific states
        if st.session_state.get("login_in_progress", False):
            _show_login_progress_in_fragment()
            return

        # Render login form
        _render_login_form_in_fragment()


def _show_login_progress_in_fragment() -> None:
    """Show progress state within the fragment."""
    with st.spinner(AUTH_SIGNING_IN):
        st.info(AUTH_PLEASE_WAIT)


def _render_login_form_in_fragment() -> None:
    """Clean login form within fragment scope."""
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
            _handle_login_in_fragment(username, password)


def _handle_login_in_fragment(username: str, password: str) -> None:
    """Handle login - simple and reliable."""
    if not username or not password:
        st.error(AUTH_ENTER_CREDENTIALS)
        return

    # Show progress with spinner during authentication
    with st.spinner(AUTH_SIGNING_IN):
        try:
            user = authenticate_user(username, password)

            if user:
                session_manager.login_user(user, remember=True)
                st.success(AUTH_WELCOME_USER.format(nama=user.nama))
                st.rerun()  # Navigate to dashboard
            else:
                st.error(ERROR_INVALID_CREDENTIALS)

        except Exception as e:
            logger.error(f"Login error for {username}: {e}")
            st.error(AUTH_LOGIN_ERROR)


# Entry point for navigation
main()
