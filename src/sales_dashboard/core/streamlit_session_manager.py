"""Session state management with integrated page access control.

Responsibility: Complete session and access management
- Session lifecycle management using Streamlit patterns
- Centralized page access control configuration
- Reusable auth wrappers for all pages
"""

from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, NamedTuple, Optional

from loguru import logger
import streamlit as st

if TYPE_CHECKING:
    from sales_dashboard.infrastructure.db_entities import UserEntity


class PageAccess(NamedTuple):
    """Page access configuration."""

    requires_login: bool = True
    requires_admin: bool = False
    description: str = ""


class PageName(str, Enum):
    """Centralized page names - prevents typos and improves maintainability."""

    # Public pages
    LOGIN = "login"

    # User pages
    DASHBOARD = "dashboard"
    PROFILE = "profile"
    HPP_CALCULATOR = "hpp_calculator"

    # Admin pages
    ADMIN_USERS = "admin_users"
    ADMIN_SETTINGS = "admin_settings"


class StreamlitSessionManager:
    """Manages session state and page access using Streamlit native patterns.

    Responsibility: Complete session and access management
    - Uses st.session_state for state management
    - Caches file I/O to prevent rerun spam
    - Provides clean session timeout handling
    - Provides reusable auth wrappers for pages
    - Centralized page access control
    """

    SESSION_TIMEOUT_HOURS = 8
    SESSION_FILE = Path(".streamlit_session")

    # =============================================================================
    # 📄 PAGES ACCESS CONFIGURATION - INTEGRATED
    # =============================================================================

    _PAGES_CONFIG = {
        # Public pages (no login required)
        PageName.LOGIN: PageAccess(
            requires_login=False, requires_admin=False, description="Login page"
        ),
        # User pages (login required, any role)
        PageName.DASHBOARD: PageAccess(
            requires_login=True,
            requires_admin=False,
            description="Main dashboard - accessible to all users",
        ),
        PageName.PROFILE: PageAccess(
            requires_login=True,
            requires_admin=False,
            description="User profile management",
        ),
        PageName.HPP_CALCULATOR: PageAccess(
            requires_login=True, requires_admin=False, description="HPP Calculator tool"
        ),
        # Admin pages (admin role required)
        PageName.ADMIN_USERS: PageAccess(
            requires_login=True,
            requires_admin=True,
            description="User management - admin only",
        ),
        PageName.ADMIN_SETTINGS: PageAccess(
            requires_login=True,
            requires_admin=True,
            description="System settings - admin only",
        ),
    }

    # =============================================================================
    # 🔐 SESSION STATE MANAGEMENT
    # =============================================================================

    def init_session_state(self) -> None:
        """Initialize session state - Streamlit native approach."""
        # Basic session state initialization - safe defaults
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False

        if "user" not in st.session_state:
            st.session_state.user = None

        if "login_time" not in st.session_state:
            st.session_state.login_time = None

        # Session initialization flag - only restore once per session
        if "session_initialized" not in st.session_state:
            st.session_state.session_initialized = True
            self._try_restore_session()
            logger.debug("Session state initialized")

    def _try_restore_session(self) -> None:
        """Try to restore session from persistent storage."""
        try:
            session_data = self._load_session_data()
            if not session_data:
                logger.debug("No session data found")
                return

            # Validate session is still valid
            if not self._is_session_valid(session_data):
                logger.debug("Session data expired")
                self._cleanup_session_file()
                return

            # Restore user from database
            self._restore_user_from_session(session_data)

        except Exception as e:
            logger.warning(f"Session restoration failed: {e}")

    @st.cache_data(ttl=300)  # Cache for 5 minutes to prevent file I/O spam
    def _load_session_data(_self) -> dict[str, Any] | None:
        """Load session data from file - cached to prevent I/O spam."""
        try:
            if not _self.SESSION_FILE.exists():
                return None

            with open(_self.SESSION_FILE, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception as e:
            logger.warning(f"Failed to load session data: {e}")
            return None

    def _is_session_valid(self, session_data: dict[str, Any]) -> bool:
        """Check if session data is still valid."""
        try:
            login_time_str = session_data.get("login_time")
            if not login_time_str:
                return False

            login_time = datetime.fromisoformat(login_time_str)
            session_age = datetime.now() - login_time

            return session_age < timedelta(hours=self.SESSION_TIMEOUT_HOURS)

        except Exception:
            return False

    def _restore_user_from_session(self, session_data: dict[str, Any]) -> None:
        """Restore user from session data."""
        try:
            from sales_dashboard.models.user_operations import get_user_by_username

            username = session_data.get("username")
            if not username:
                return

            user = get_user_by_username(username)
            if user and user.is_active:
                st.session_state.user = user
                st.session_state.logged_in = True
                st.session_state.login_time = datetime.fromisoformat(
                    session_data["login_time"]
                )
                logger.info(f"Session restored for user {username}")

        except Exception as e:
            logger.warning(f"Failed to restore user from session: {e}")

    def login_user(self, user: "UserEntity", remember: bool = True) -> None:
        """Login user and optionally persist session."""
        st.session_state.user = user
        st.session_state.logged_in = True
        st.session_state.login_time = datetime.now()

        if remember:
            self._save_session_data(user)

        logger.info(f"User {user.username} logged in successfully")

    def logout_user(self) -> None:
        """Logout user and cleanup session."""
        username = getattr(st.session_state.get("user"), "username", "unknown")

        # Clear session state
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.login_time = None

        # Clear persistent session
        self._cleanup_session_file()

        logger.info(f"User {username} logged out")

    def check_session_timeout(self) -> bool:
        """Check if current session has timed out."""
        if not st.session_state.get("logged_in", False):
            return False

        login_time = st.session_state.get("login_time")
        if not login_time:
            return False

        session_age = datetime.now() - login_time
        is_expired = session_age > timedelta(hours=self.SESSION_TIMEOUT_HOURS)

        if is_expired:
            logger.info(f"Session expired after {session_age}")

        return is_expired

    def _save_session_data(self, user: "UserEntity") -> None:
        """Save session data to persistent storage."""
        try:
            session_data = {
                "username": user.username,
                "login_time": st.session_state.login_time.isoformat(),
            }

            with open(self.SESSION_FILE, "w", encoding="utf-8") as f:
                json.dump(session_data, f)

            logger.debug(f"Session saved for user {user.username}")

        except Exception as e:
            logger.warning(f"Failed to save session data: {e}")

    def _cleanup_session_file(self) -> None:
        """Clean up session file."""
        try:
            if self.SESSION_FILE.exists():
                self.SESSION_FILE.unlink()
                logger.debug("Session file cleaned up")
        except Exception as e:
            logger.warning(f"Failed to cleanup session file: {e}")

    # =============================================================================
    # 🔐 REUSABLE AUTH WRAPPERS - DRY PRINCIPLE
    # =============================================================================

    def check_and_handle_session_timeout(self) -> bool:
        """Check session timeout and handle logout if expired."""
        if self.check_session_timeout():
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

    # =============================================================================
    # 📄 INTEGRATED PAGE ACCESS CONTROL - CONFIG-BASED APPROACH
    # =============================================================================

    def get_page_access(self, page_name: str | PageName) -> PageAccess:
        """Get access configuration for a page."""
        # Convert string to PageName enum if needed
        if isinstance(page_name, str):
            try:
                page_name = PageName(page_name)
            except ValueError:
                raise ValueError(f"Page '{page_name}' not found in configuration")

        if page_name not in self._PAGES_CONFIG:
            raise ValueError(f"Page '{page_name}' not found in configuration")

        return self._PAGES_CONFIG[page_name]

    def can_user_access_page(
        self, page_name: str | PageName, user: Optional["UserEntity"] = None
    ) -> bool:
        """Check if user can access a specific page."""
        try:
            # Use current user if not provided
            if user is None:
                user = self.get_logged_in_user()

            access_config = self.get_page_access(page_name)

            # Check login requirement
            if access_config.requires_login and not user:
                return False

            # Check admin requirement
            if access_config.requires_admin and (not user or not user.is_admin):
                return False

            return True

        except ValueError:
            # Unknown page - deny access by default
            return False

    def require_page_access(self, page_name: str | PageName) -> Optional["UserEntity"]:
        """Require access to a specific page based on its configuration.

        Preferred method - uses centralized page config for access control.

        Args:
            page_name: Name of the page (PageName enum or string)

        Returns:
            User entity if access granted

        Note:
            This function will stop execution (st.stop()) if access denied

        Example:
            user = session_manager.require_page_access(PageName.DASHBOARD)
            admin = session_manager.require_page_access(PageName.ADMIN_USERS)
        """
        try:
            # Step 1: Check and handle session timeout
            if self.check_and_handle_session_timeout():
                return None

            access_config = self.get_page_access(page_name)

            # Step 2: If no login required, allow access
            if not access_config.requires_login:
                return None

            # Step 3: Check if user is logged in
            user = self.get_logged_in_user()
            if not user:
                st.warning(
                    "🔒 Silakan login terlebih dahulu untuk mengakses halaman ini."
                )
                st.stop()
                return None

            # Step 4: Check admin requirement
            if access_config.requires_admin and not user.is_admin:
                st.error(
                    "❌ Anda tidak memiliki akses administrator untuk halaman ini."
                )
                st.stop()
                return None

            # Step 5: Access granted - return user
            return user

        except ValueError as e:
            st.error(f"❌ Halaman tidak ditemukan: {e}")
            st.stop()
            return None

    # =============================================================================
    # 🔐 LEGACY AUTH METHODS - KEPT FOR BACKWARD COMPATIBILITY
    # =============================================================================

    def require_login_with_role(
        self, required_admin: bool = False
    ) -> Optional["UserEntity"]:
        """Legacy method - use require_page_access() instead."""
        if self.check_and_handle_session_timeout():
            return None

        user = self.get_logged_in_user()
        if not user:
            st.warning("🔒 Silakan login terlebih dahulu untuk mengakses halaman ini.")
            st.stop()
            return None

        if required_admin and not user.is_admin:
            st.error("❌ Anda tidak memiliki akses administrator untuk halaman ini.")
            st.stop()
            return None

        return user

    def require_admin_access(self) -> Optional["UserEntity"]:
        """Legacy method - use require_page_access(PageName.ADMIN_*) instead."""
        return self.require_login_with_role(required_admin=True)

    def require_user_access(self) -> Optional["UserEntity"]:
        """Legacy method - use require_page_access(PageName.*) instead."""
        return self.require_login_with_role(required_admin=False)


# Global instance - Streamlit singleton pattern
session_manager = StreamlitSessionManager()


# =============================================================================
# 📚 USAGE EXAMPLES AND DOCUMENTATION
# =============================================================================

"""
Usage Examples:

1. Simple auth (recommended for most cases):
   ```python
   user = session_manager.require_user_access()
   admin_user = session_manager.require_admin_access()
   ```

2. Page-based auth (uses centralized config):
   ```python
   user = session_manager.require_page_access(PageName.DASHBOARD)
   admin = session_manager.require_page_access(PageName.ADMIN_USERS)
   ```

3. Check access without stopping:
   ```python
   if session_manager.can_user_access_page(PageName.ADMIN_USERS):
       st.button("Go to User Management")
   ```

4. Get page configuration:
   ```python
   config = session_manager.get_page_access(PageName.HPP_CALCULATOR)
   st.write(f"Page description: {config.description}")
   ```
"""
