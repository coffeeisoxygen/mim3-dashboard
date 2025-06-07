"""Authentication page - clean login/logout with fragment isolation."""

from __future__ import annotations

from loguru import logger
import streamlit as st

from sales_dashboard.models.user_operations import authenticate_user
from sales_dashboard.ui.ui_config import AUTH, ICONS


def show_login_page() -> None:
    """Main login page with professional styling."""
    st.header(AUTH.LOGIN_TITLE, anchor=False)

    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Use fragment to isolate login form interactions
        _render_login_form_fragment()


@st.fragment  # 🎯 Fragment isolates this form from full page re-runs
def _render_login_form_fragment() -> None:
    """Render login form with fragment isolation for smooth UX."""

    # Check if already logged in (avoid showing form after successful login)
    if st.session_state.get("logged_in", False):
        st.success("Login successful! Redirecting...")
        st.rerun()  # This will trigger navigation to main app
        return

    with st.form("login_form", clear_on_submit=False):
        st.subheader(AUTH.LOGIN_SUBTITLE, anchor=False)

        # Input fields
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="auth_username",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="auth_password",
        )

        # Submit button
        submitted = st.form_submit_button(
            AUTH.LOGIN_BUTTON_TEXT,
            use_container_width=True,
            type="primary",
        )

        if submitted:
            _handle_login_attempt(username, password)


def _handle_login_attempt(username: str, password: str) -> None:
    """Handle login attempt with proper validation and error handling."""
    # Validate inputs
    if not username or not password:
        st.warning(AUTH.MISSING_FIELDS)
        return

    # Show loading state
    with st.spinner("Authenticating..."):
        try:
            user = authenticate_user(username, password)

            if user:
                # Success - set session state
                st.session_state.user = user
                st.session_state.logged_in = True
                st.success(AUTH.WELCOME_MESSAGE.format(name=user.nama))
                logger.info(f"User {user.username} logged in successfully")

                # Fragment will handle the rerun smoothly
                st.rerun()
            else:
                # Failed authentication
                st.error(AUTH.INVALID_CREDENTIALS)
                logger.warning(f"Failed login attempt for username: {username}")

        except Exception as e:
            logger.error(f"Login error for {username}: {e}")
            st.error("An error occurred during login. Please try again.")


def handle_logout() -> None:
    """Clean logout with session cleanup."""
    username = getattr(st.session_state.get("user"), "username", "unknown")

    # Clear session state
    st.session_state.user = None
    st.session_state.logged_in = False

    # Log the logout
    logger.info(f"User {username} logged out")

    # Rerun to show login page
    st.rerun()


def show_user_info_sidebar(user) -> None:
    """Display user information in sidebar with clean styling."""
    with st.sidebar:
        # User welcome
        st.success(f"Welcome, **{user.nama}**")

        # Role indicator
        role_icon = ICONS.ADMIN_PANEL if user.is_admin else ICONS.PERSON
        role_text = "Admin" if user.is_admin else "User"
        st.caption(f"{role_icon} {role_text}")

        st.divider()
