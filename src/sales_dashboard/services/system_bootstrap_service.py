from __future__ import annotations

from typing import Optional
from loguru import logger
import streamlit as st

from sales_dashboard.domain.models.user import User
from sales_dashboard.domain.repository.user_repository import UserRepository
from sales_dashboard.utils.hasher import get_password_hasher


class SystemBootstrapService:
    """System initialization service"""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self.hasher = get_password_hasher(use_bcrypt=False)

    def ensure_default_admin(self) -> Optional[User]:
        """Ensure default admin exists - handle Streamlit reruns gracefully"""

        # Simple session state check
        if st.session_state.get("bootstrap_completed", False):
            logger.debug("Bootstrap already completed in this session")
            return self.user_repo.get_by_username("admin")

        logger.info("Checking for default admin user...")

        # Check if specific admin username exists
        existing_admin = self.user_repo.get_by_username("admin")
        if existing_admin:
            logger.info(f"Default admin already exists: {existing_admin.username}")
            st.session_state.bootstrap_completed = True
            return existing_admin

        # Check if any admin exists
        try:
            admins = self.user_repo.get_all_admins()
            if admins:
                logger.info(f"Other admin users exist: {len(admins)} admins found")
                st.session_state.bootstrap_completed = True
                return admins[0]
        except Exception as e:
            logger.warning(f"Error checking existing admins: {e}")

        # Create default admin if none exists
        logger.warning("No admin users found. Creating default admin...")

        try:
            default_admin = User(
                id=None,
                nama="System Administrator",
                email="admin@dashboard.com",
                username="admin",
                password=self.hasher.hash_password("admin123"),
                is_admin=True,
                is_active=True
            )

            created_admin = self.user_repo.create(default_admin)
            st.session_state.bootstrap_completed = True
            logger.info(f"Default admin created with ID: {created_admin.id}")
            return created_admin

        except Exception as e:
            logger.error(f"Failed to create default admin: {e}")

            # Try to get existing admin one more time (race condition protection)
            existing_admin = self.user_repo.get_by_username("admin")
            if existing_admin:
                logger.info("Found existing admin after creation attempt")
                st.session_state.bootstrap_completed = True
                return existing_admin

            raise
