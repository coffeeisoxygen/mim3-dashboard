"""Authentication helper functions for page access control."""

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Callable, Optional, TypeVar, cast

from loguru import logger
import streamlit as st

from sales_dashboard.core.streamlit_session_manager import session_manager

if TYPE_CHECKING:
    from sales_dashboard.infrastructure.db_entities import UserEntity

F = TypeVar("F", bound=Callable[..., None])


def require_login(func: F) -> F:
    """Decorator to require user login for page access."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        user = session_manager.get_logged_in_user()
        if not user:
            st.error("🔒 Silakan login terlebih dahulu untuk mengakses halaman ini.")
            st.stop()
            return

        # Store validated user in session for page use
        st.session_state.validated_user = user
        return func(*args, **kwargs)

    return cast(F, wrapper)


def require_admin(func: F) -> F:
    """Decorator to require admin access for page."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        user = session_manager.get_logged_in_user()
        if not user:
            st.error("🔒 Silakan login terlebih dahulu untuk mengakses halaman ini.")
            st.stop()
            return

        if not user.is_admin:
            st.error("❌ Anda tidak memiliki akses administrator untuk halaman ini.")
            logger.warning(f"Non-admin user {user.username} attempted admin access")
            st.stop()
            return

        # Store validated admin user in session for page use
        st.session_state.validated_user = user
        return func(*args, **kwargs)

    return cast(F, wrapper)


def require_user_access() -> Optional["UserEntity"]:
    """Require user to be logged in. Returns user or stops execution."""
    if session_manager.check_and_handle_session_timeout():
        return None

    user = session_manager.get_logged_in_user()
    if not user:
        st.warning("🔒 Silakan login terlebih dahulu untuk mengakses halaman ini.")
        st.stop()
        return None

    return user


def require_admin_access() -> Optional["UserEntity"]:
    """Require user to be logged in as admin. Returns user or stops execution."""
    user = require_user_access()
    if not user:
        return None

    if not user.is_admin:
        st.error("❌ Anda tidak memiliki akses administrator untuk halaman ini.")
        st.stop()
        return None

    return user


def get_current_user() -> Optional["UserEntity"]:
    """Get current logged in user without requiring access."""
    return session_manager.get_logged_in_user()


def is_logged_in() -> bool:
    """Check if user is currently logged in."""
    return session_manager.get_logged_in_user() is not None


def is_admin() -> bool:
    """Check if current user is admin."""
    user = session_manager.get_logged_in_user()
    return user is not None and user.is_admin
