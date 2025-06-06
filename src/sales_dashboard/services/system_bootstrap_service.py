from __future__ import annotations

from loguru import logger
import streamlit as st

from sales_dashboard.domain.models.user import User
from sales_dashboard.domain.repository.user_repository import UserRepository
from sales_dashboard.infrastructure.db_engine import reset_connection_cache
from sales_dashboard.utils.hasher import get_password_hasher


class SystemBootstrapService:
    """System initialization service with cache awareness"""

    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo
        self.hasher = get_password_hasher(use_bcrypt=False)

    def ensure_default_admin(self) -> User | None:
        """Ensure default admin exists with proper cache management"""
        # Session state check (fastest)
        if st.session_state.get("bootstrap_completed", False):
            logger.debug("Bootstrap already completed in this session")
            return self.user_repo.get_by_username("admin")

        logger.info("Checking for default admin user...")

        # Database check with fresh data (ttl=0)
        existing_admin = self.user_repo.get_by_username("admin")
        if existing_admin:
            logger.info(f"Default admin found: {existing_admin.username}")
            st.session_state.bootstrap_completed = True
            return existing_admin

        # Check other admins (fresh data)
        try:
            admins = self.user_repo.get_all_admins()
            if admins:
                logger.info(f"Other admin users exist: {len(admins)} found")
                st.session_state.bootstrap_completed = True
                return admins[0]
        except Exception as e:
            logger.warning(f"Error checking existing admins: {e}")

        # Create admin
        return self._create_default_admin()

    def _create_default_admin(self) -> User:
        """Create default admin with proper error handling"""
        logger.warning("No admin users found. Creating default admin...")

        try:
            default_admin = User(
                id=None,
                nama="System Administrator",
                email="admin@dashboard.com",
                username="admin",
                password=self.hasher.hash_password("admin123"),
                is_admin=True,
                is_active=True,
            )

            created_admin = self.user_repo.create(default_admin)  # This resets cache
            st.session_state.bootstrap_completed = True
            logger.info(f"Default admin created with ID: {created_admin.id}")
            return created_admin

        except Exception as e:
            logger.error(f"Failed to create default admin: {e}")

            # Race condition protection
            if "UNIQUE constraint failed" in str(e):
                logger.info("Admin user already exists (race condition detected)")
                # Reset cache and try again
                reset_connection_cache()
                existing_admin = self.user_repo.get_by_username("admin")
                if existing_admin:
                    st.session_state.bootstrap_completed = True
                    return existing_admin

            raise

    def reset_bootstrap_cache(self) -> None:
        """Reset bootstrap cache - useful for development"""
        st.session_state.bootstrap_completed = False
        reset_connection_cache()
        logger.info("Bootstrap cache reset")
