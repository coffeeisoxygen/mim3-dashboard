"""Session management with refresh persistence - TODO: Implement browser storage."""

from __future__ import annotations

from datetime import datetime, timedelta
import json
from pathlib import Path

from loguru import logger
import streamlit as st

from sales_dashboard.models.user_operations import get_user_by_username


class SessionManager:
    """Handles user session persistence and management."""

    def __init__(self) -> None:
        self._session_file = Path(".streamlit_session")

    def init_session_state(self) -> None:
        """Initialize session state with simple, reliable approach."""
        # TODO: Implement browser sessionStorage for refresh persistence

        # Basic session initialization
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False

        if "user" not in st.session_state:
            st.session_state.user = None

        if "login_time" not in st.session_state:
            st.session_state.login_time = None

        if "last_activity" not in st.session_state:
            st.session_state.last_activity = None

        # Try to restore session
        self._try_restore_session()

    def login_user(self, user) -> None:
        """Set user as logged in and persist session."""
        st.session_state.user = user
        st.session_state.logged_in = True
        st.session_state.login_time = datetime.now()
        st.session_state.last_activity = datetime.now()

        # Save to file (TODO: Replace with browser storage)
        self._save_session_to_file(user)

        logger.info(f"User {user.username} logged in successfully")

    def logout_user(self) -> None:
        """Clear user session and cleanup."""
        username = getattr(st.session_state.get("user"), "username", "unknown")

        # Clear session state
        st.session_state.user = None
        st.session_state.logged_in = False
        st.session_state.login_time = None
        st.session_state.last_activity = None

        # Clear file storage
        self._clear_session_file()

        logger.info(f"User {username} logged out")
        st.toast("Logged out successfully", icon="✅")

    def check_session_timeout(self) -> bool:
        """Check if session has timed out (8 hours for office use)."""
        if not st.session_state.get("logged_in", False):
            return False

        login_time = st.session_state.get("login_time")
        if not login_time:
            return False

        # 8-hour timeout for office environment
        timeout_hours = 8
        time_diff = datetime.now() - login_time
        return time_diff > timedelta(hours=timeout_hours)

    def update_activity(self) -> None:
        """Update last activity timestamp."""
        if st.session_state.get("logged_in", False):
            st.session_state.last_activity = datetime.now()

    def _save_session_to_file(self, user) -> None:
        """Save current session to file - TODO: Replace with browser storage."""
        session_data = {
            "username": user.username,
            "login_time": datetime.now().isoformat(),
            "user_id": user.id,
        }

        try:
            with open(self._session_file, "w") as f:
                json.dump(session_data, f)
        except Exception as e:
            logger.warning(f"Failed to save session to file: {e}")

    def _try_restore_session(self) -> None:
        """Try to restore session from file if valid."""
        try:
            if not self._session_file.exists():
                return

            with open(self._session_file, "r") as f:
                session_data = json.load(f)

            # Validate session data
            username = session_data.get("username")
            login_time_str = session_data.get("login_time")

            if not username or not login_time_str:
                return

            login_time = datetime.fromisoformat(login_time_str)

            # Check if session is still valid (8 hours)
            if (datetime.now() - login_time).total_seconds() < 8 * 3600:
                # Restore user session
                user = get_user_by_username(username)
                if user:
                    st.session_state.user = user
                    st.session_state.logged_in = True
                    st.session_state.login_time = login_time
                    st.session_state.last_activity = datetime.now()

                    logger.info(f"Session restored for user {username}")
            else:
                # Session expired, clean up
                self._clear_session_file()

        except Exception as e:
            logger.warning(f"Failed to restore session: {e}")
            self._clear_session_file()

    def _clear_session_file(self) -> None:
        """Clear session file."""
        try:
            if self._session_file.exists():
                self._session_file.unlink()
        except Exception as e:
            logger.warning(f"Failed to clear session file: {e}")


# Global session manager instance
session_manager = SessionManager()
