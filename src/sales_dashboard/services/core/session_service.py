from __future__ import annotations

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from loguru import logger
import streamlit as st

from sales_dashboard.domain.models.user import User


class SessionService:
    """Session management service for Streamlit applications"""

    def __init__(self) -> None:
        self.session_timeout = timedelta(hours=8)  # 8 hours default

    def create_session(self, user: User) -> Dict[str, Any]:
        """Create user session"""
        session_data = {
            "user": user,
            "logged_in": True,
            "login_time": datetime.now(),
            "last_activity": datetime.now(),
        }

        # Store in Streamlit session state
        for key, value in session_data.items():
            st.session_state[key] = value

        logger.info(f"Session created for user: {user.username}")
        return session_data

    def get_current_user(self) -> Optional[User]:
        """Get current logged-in user"""
        if not st.session_state.get("logged_in", False):
            return None

        user = st.session_state.get("user")
        if self.is_session_expired():
            self.destroy_session()
            return None

        # Update last activity
        st.session_state.last_activity = datetime.now()
        return user

    def is_session_expired(self) -> bool:
        """Check if session has expired"""
        last_activity = st.session_state.get("last_activity")
        if not last_activity:
            return True

        return datetime.now() - last_activity > self.session_timeout

    def destroy_session(self) -> None:
        """Destroy current session"""
        user = st.session_state.get("user")
        username = user.username if user else "Unknown"

        # Clear session data
        session_keys = ["user", "logged_in", "login_time", "last_activity"]
        for key in session_keys:
            if key in st.session_state:
                del st.session_state[key]

        logger.info(f"Session destroyed for user: {username}")

    def is_admin(self) -> bool:
        """Check if current user is admin"""
        user = self.get_current_user()
        return user is not None and user.is_admin

    def require_login(self) -> User:
        """Require user to be logged in, redirect if not"""
        user = self.get_current_user()
        if not user:
            st.error("Please log in to access this page")
            st.stop()
        return user

    def require_admin(self) -> User:
        """Require user to be admin, redirect if not"""
        user = self.require_login()
        if not user.is_admin:
            st.error("Admin access required")
            st.stop()
        return user

    def get_session_info(self) -> Dict[str, Any]:
        """Get current session information"""
        if not st.session_state.get("logged_in", False):
            return {"status": "not_logged_in"}

        return {
            "status": "active",
            "user": st.session_state.get("user"),
            "login_time": st.session_state.get("login_time"),
            "last_activity": st.session_state.get("last_activity"),
            "session_expired": self.is_session_expired(),
        }
