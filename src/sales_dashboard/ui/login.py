from __future__ import annotations

import streamlit as st
from loguru import logger
from pydantic import ValidationError

from sales_dashboard.domain.schemas.user import UserLogin
from sales_dashboard.services.auth_service import AuthService
from sales_dashboard.infrastructure.repositories.user_repository import (
    SQLUserRepository,
)


def _handle_validation_errors(
    validation_error: ValidationError, username: str
) -> list[str]:
    """Process Pydantic validation errors and return formatted error messages."""
    error_messages = []

    for error in validation_error.errors():
        # Safely extract field name - convert to string to avoid type issues
        field_raw = error["loc"][0] if error["loc"] else "input"
        field_name = str(field_raw).title()

        error_message = error.get("msg", "Invalid input")

        # Translate common validation messages to Indonesian
        if "at least" in error_message and "characters" in error_message:
            min_length = error.get("ctx", {}).get("min_length", 6)
            error_message = f"minimal {min_length} karakter"
        elif "at most" in error_message and "characters" in error_message:
            max_length = error.get("ctx", {}).get("max_length", 50)
            error_message = f"maksimal {max_length} karakter"

        error_messages.append(f"**{field_name}**: {error_message}")

    logger.warning(f"Validation error for user {username}: {validation_error}")
    return error_messages


def _process_login_attempt(username: str, password: str) -> None:
    """Process login attempt with proper error handling."""
    try:
        logger.debug(f"Login attempt for username: {username}")

        # Validate input using Pydantic
        try:
            login_data = UserLogin(username=username, password=password)
        except ValidationError as validation_error:
            error_messages = _handle_validation_errors(validation_error, username)
            st.error("❌ **Input tidak valid:**\n\n" + "\n\n".join(error_messages))
            return  # Stop execution here

        # Authenticate using service
        authenticated_user = auth_service.authenticate(login_data)

        if authenticated_user:
            logger.info(f"Successful login for user: {username}")
            st.session_state.logged_in = True
            st.session_state.user = authenticated_user
            st.success("✅ Login berhasil! Mengalihkan...")
            st.rerun()
        else:
            logger.warning(f"Failed login attempt for username: {username}")
            st.error("❌ Username atau password salah!")

    except Exception as unexpected_error:
        logger.error(f"Unexpected login error for user {username}: {unexpected_error}")
        st.error("❌ Terjadi kesalahan sistem. Silakan coba lagi.")


def _render_logout_interface() -> None:
    """Render the logout interface for authenticated users."""
    user = st.session_state.get("user")
    st.title("👋 Logout")

    if user:
        st.write(f"Selamat datang, **{user.nama}**!")
        st.write(f"Email: {user.email}")

        if user.is_admin:
            st.success("🔧 Admin Access")
    else:
        st.write("Selamat datang!")

    st.write("Terima kasih telah menggunakan Dashboard IM3.")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Logout", type="secondary", use_container_width=True):
            username = user.username if user else "Unknown"
            logger.info(f"User {username} logged out")
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()


def _render_login_interface() -> None:
    """Render the login interface for unauthenticated users."""
    st.title("🔐 Login Dashboard")
    st.write("Silakan masukkan kredensial Anda untuk mengakses dashboard.")

    with st.container():
        username = st.text_input("Username", placeholder="Masukkan username")
        password = st.text_input(
            "Password", type="password", placeholder="Masukkan password"
        )

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Login", type="primary", use_container_width=True):
                if username and password:
                    _process_login_attempt(username, password)
                else:
                    logger.debug("Login attempt with empty credentials")
                    st.warning("⚠️ Harap isi username dan password!")

    # Show login requirements
    with st.expander("ℹ️ Persyaratan Login"):
        st.write("**Username:** Minimal 3 karakter, maksimal 50 karakter")
        st.write("**Password:** Minimal 6 karakter")
        st.write("")
        st.info("💡 **Default Admin:**\n\nUsername: `admin`\n\nPassword: `admin123`")


# Initialize services
user_repo = SQLUserRepository()
auth_service = AuthService(user_repo)

# Main application logic
if st.session_state.get("logged_in", False):
    _render_logout_interface()
else:
    _render_login_interface()
