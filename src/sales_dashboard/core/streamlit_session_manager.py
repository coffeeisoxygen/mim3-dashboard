"""Session state management with optimized Streamlit caching."""

from __future__ import annotations

from datetime import datetime, timedelta
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

from loguru import logger
import streamlit as st

from sales_dashboard.config.constant import (
    SESSION_CACHE_TTL_MINUTES,
    SESSION_FILE,
    SESSION_TIMEOUT_HOURS,
    USER_CACHE_TTL_MINUTES,
)

if TYPE_CHECKING:
    from sales_dashboard.infrastructure.db_entities import UserEntity


# Global cache functions for better performance
@st.cache_data(ttl=SESSION_CACHE_TTL_MINUTES * 60)  # Convert minutes to seconds
def _load_session_file(session_file_path: str) -> dict[str, Any] | None:
    """Load session data from file with caching for performance."""
    try:
        session_file = Path(session_file_path)
        if not session_file.exists():
            return None

        with open(session_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Only log actual file reads, not cache hits
            logger.debug(f"Session file read from disk: {list(data.keys())}")
            return data

    except Exception as e:
        logger.warning(f"Failed to load session data: {e}")
        return None


@st.cache_data(ttl=USER_CACHE_TTL_MINUTES * 60)  # Convert minutes to seconds
def _get_user_from_database(user_id: int) -> "UserEntity | None":
    """Get user from database with caching."""
    try:
        from sales_dashboard.models.user_operations import get_user_by_id

        user = get_user_by_id(user_id)
        if user:
            logger.debug(f"User loaded from database: {user.username}")
        return user
    except Exception as e:
        logger.error(f"Failed to get user by ID {user_id}: {e}")
        return None


class StreamlitSessionManager:
    """Manages session state using Streamlit native patterns with optimized caching."""

    def init_session_state(self) -> None:
        """Initialize session state with proper restoration order."""
        # Only initialize once per session
        if "session_initialized" in st.session_state:
            return

        # Mark as initialized immediately
        st.session_state.session_initialized = True

        # Try to restore session FIRST (now cached)
        restored = self._try_restore_session()

        # Only set defaults if restoration failed
        if not restored:
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.login_time = None
            logger.debug("Session state initialized with defaults")
        else:
            # Only log successful restoration once per browser session
            if not st.session_state.get("restoration_logged", False):
                logger.info("Session state restored from cache")
                st.session_state.restoration_logged = True
            else:
                logger.debug("Session state restored from cache")

    def _try_restore_session(self) -> bool:
        """Try to restore session from file. Returns True if successful."""
        try:
            # Use cached session data (major performance improvement)
            session_data = _load_session_file(str(SESSION_FILE))
            if not session_data:
                return False

            # Check if session is still valid
            if not self._is_session_valid(session_data):
                self._cleanup_session_file()
                # Clear cache when invalid - correct Streamlit way
                self._clear_session_caches()
                return False

            # Restore user from database (with caching)
            return self._restore_user_from_session(session_data)

        except Exception as e:
            logger.warning(f"Session restoration failed: {e}")
            return False

    def _is_session_valid(self, session_data: dict[str, Any]) -> bool:
        """Check if session data is still valid."""
        try:
            # Check if explicitly logged in
            if not session_data.get("logged_in", False):
                return False

            # Check expiry time if available
            expires_at_str = session_data.get("expires_at")
            if expires_at_str:
                expires_at = datetime.fromisoformat(expires_at_str)
                if datetime.now() > expires_at:
                    logger.debug("Session expired")
                    return False

            # Fallback: check login time
            login_time_str = session_data.get("login_time")
            if login_time_str:
                login_time = datetime.fromisoformat(login_time_str)
                age = datetime.now() - login_time
                if age > timedelta(hours=SESSION_TIMEOUT_HOURS):
                    logger.debug(f"Session too old: {age}")
                    return False

            return True

        except Exception as e:
            logger.warning(f"Session validation error: {e}")
            return False

    def _restore_user_from_session(self, session_data: dict[str, Any]) -> bool:
        """Restore user from session data. Returns True if successful."""
        try:
            user_id = session_data.get("user_id")
            username = session_data.get("username")

            if not user_id:
                logger.warning("No user_id in session data")
                return False

            # Use cached user lookup (major performance improvement)
            user = _get_user_from_database(user_id)

            if not user:
                logger.warning(f"User not found: id={user_id}, username={username}")
                return False

            if not user.is_active:
                logger.warning(f"User {username} is not active")
                return False

            # Restore session state
            st.session_state.user = user
            st.session_state.logged_in = True
            st.session_state.login_time = datetime.fromisoformat(
                session_data["login_time"]
            )

            # Only log restoration once per browser session, not on every navigation
            if not st.session_state.get("user_restoration_logged", False):
                logger.info(f"Session restored for user {user.username}")
                st.session_state.user_restoration_logged = True

            return True

        except Exception as e:
            logger.error(f"Failed to restore user from session: {e}")
            return False

    def _clear_session_caches(self) -> None:
        """Clear session-related caches using proper Streamlit methods."""
        try:
            # Correct way to clear all cache data in Streamlit
            st.cache_data.clear()
            logger.debug("Session caches cleared")
        except Exception as e:
            logger.warning(f"Failed to clear session cache: {e}")

    def login_user(self, user: "UserEntity", remember: bool = True) -> None:
        """Login user and optionally persist session."""
        st.session_state.user = user
        st.session_state.logged_in = True
        st.session_state.login_time = datetime.now()

        # Reset restoration logging flags for new session
        st.session_state.restoration_logged = False
        st.session_state.user_restoration_logged = False

        if remember:
            self._save_session_data(user)

        # Clear caches on new login
        self._clear_session_caches()

        logger.info(f"User {user.username} logged in successfully")

    def logout_user(self) -> None:
        """Logout user and cleanup session."""
        username = getattr(st.session_state.get("user"), "username", "unknown")

        # Clear session state
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.login_time = None

        # Reset restoration logging flags
        st.session_state.restoration_logged = False
        st.session_state.user_restoration_logged = False

        # Clear persistent session
        self._cleanup_session_file()

        # Clear all caches
        self._clear_session_caches()

        logger.info(f"User {username} logged out")

    def _save_session_data(self, user: "UserEntity") -> None:
        """Save session data to persistent storage."""
        try:
            session_data = {
                "user_id": user.id,
                "username": user.username,
                "logged_in": True,
                "login_time": datetime.now().isoformat(),
                "last_activity": datetime.now().isoformat(),
                "expires_at": (
                    datetime.now() + timedelta(hours=SESSION_TIMEOUT_HOURS)
                ).isoformat(),
            }

            with open(SESSION_FILE, "w", encoding="utf-8") as f:
                json.dump(session_data, f, indent=2)

            # Clear cache after file update - correct approach
            st.cache_data.clear()
            logger.debug(f"Session saved for user {user.username}")

        except Exception as e:
            logger.warning(f"Failed to save session data: {e}")

    def _cleanup_session_file(self) -> None:
        """Clean up session file."""
        try:
            if SESSION_FILE.exists():
                SESSION_FILE.unlink()
                logger.debug("Session file cleaned up")
        except Exception as e:
            logger.warning(f"Failed to cleanup session file: {e}")

    def check_and_handle_session_timeout(self) -> bool:
        """Check session timeout and handle logout if expired."""
        if not st.session_state.get("logged_in", False):
            return False

        login_time = st.session_state.get("login_time")
        if not login_time:
            return False

        session_age = datetime.now() - login_time
        is_expired = session_age > timedelta(hours=SESSION_TIMEOUT_HOURS)

        if is_expired:
            self.logout_user()
            st.warning("⏰ Sesi telah berakhir setelah 8 jam. Silakan login kembali.")
            st.rerun()
            return True

        return False

    def get_logged_in_user(self) -> Optional["UserEntity"]:
        """Get current logged in user from session state."""
        if not st.session_state.get("logged_in", False):
            return None
        return st.session_state.get("user")


# Global instance
session_manager = StreamlitSessionManager()
