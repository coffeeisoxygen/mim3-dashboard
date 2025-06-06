from __future__ import annotations

from typing import Any

from loguru import logger
import streamlit as st

from sales_dashboard.domain.models.user import User
from sales_dashboard.domain.schemas.user import UserCreateByAdmin
from sales_dashboard.services.interfaces import (
    BootstrapServiceInterface,
    UserServiceInterface,
)


class BootstrapService(BootstrapServiceInterface):
    """System bootstrap service with proper dependencies"""

    def __init__(self, user_service: UserServiceInterface) -> None:
        self.user_service = user_service
        self._max_retry_attempts = 3

    def ensure_default_admin(self) -> User | None:
        """Ensure default admin exists with proper cache management"""
        # Session state check (fastest)
        if st.session_state.get("bootstrap_completed", False):
            logger.debug("Bootstrap already completed in this session")
            # Try to get existing admin
            try:
                admins = self.user_service.get_all_admins()
                return admins[0] if admins else None
            except Exception as e:
                logger.warning(f"Error retrieving admin during bootstrap check: {e}")
                st.session_state.bootstrap_completed = False

        logger.info("Checking for default admin user...")

        # Check if any admin exists with retry logic
        for attempt in range(self._max_retry_attempts):
            try:
                admins = self.user_service.get_all_admins()
                if admins:
                    logger.info(f"Admin users exist: {len(admins)} found")
                    st.session_state.bootstrap_completed = True
                    return admins[0]
                break  # No admins found, proceed to creation
            except Exception as e:
                logger.warning(
                    f"Error checking existing admins (attempt {attempt + 1}): {e}"
                )
                if attempt == self._max_retry_attempts - 1:
                    raise  # Re-raise on final attempt

        # Create default admin
        return self._create_default_admin()

    def _create_default_admin(self) -> User:
        """Create default admin with proper error handling"""
        logger.warning("No admin users found. Creating default admin...")

        for attempt in range(self._max_retry_attempts):
            try:
                # Create admin user data
                admin_data = UserCreateByAdmin(
                    nama="System Administrator",
                    email="admin@dashboard.com",
                    username="admin",
                    password="admin123",
                    is_admin=True,
                )

                # Create a temporary admin user for the creation process
                # This is a special case for bootstrap - we need admin privileges to create admin
                temp_admin = User(
                    id=0,  # Temporary ID for bootstrap process
                    nama="Bootstrap System",
                    email="bootstrap@system.internal",
                    username="bootstrap",
                    password="",
                    is_admin=True,
                    is_active=True,
                )

                created_admin = self.user_service.create_user_by_admin(
                    admin_data, temp_admin
                )
                st.session_state.bootstrap_completed = True
                logger.info(f"Default admin created with ID: {created_admin.id}")
                return created_admin

            except ValueError as ve:
                # Username/email already exists - try to get existing
                if "already exists" in str(ve):
                    logger.info("Admin user already exists, attempting to retrieve...")
                    try:
                        admins = self.user_service.get_all_admins()
                        if admins:
                            st.session_state.bootstrap_completed = True
                            return admins[0]
                    except Exception as retrieval_error:
                        logger.debug(
                            f"Could not retrieve existing admin during bootstrap: {retrieval_error}"
                        )

                if attempt == self._max_retry_attempts - 1:
                    raise
                logger.warning(f"Bootstrap attempt {attempt + 1} failed: {ve}")

            except Exception as e:
                logger.error(
                    f"Failed to create default admin (attempt {attempt + 1}): {e}"
                )

                # Try to get existing admin one more time (race condition protection)
                try:
                    admins = self.user_service.get_all_admins()
                    if admins:
                        logger.info("Found existing admin after creation attempt")
                        st.session_state.bootstrap_completed = True
                        return admins[0]
                except Exception as creation_error:
                    logger.debug(
                        f"Could not retrieve admin after creation attempt: {creation_error}"
                    )

                if attempt == self._max_retry_attempts - 1:
                    raise

        raise RuntimeError("Failed to ensure default admin after all retry attempts")

    def reset_bootstrap_cache(self) -> None:
        """Reset bootstrap cache - useful for development"""
        st.session_state.bootstrap_completed = False
        logger.info("Bootstrap cache reset")

    def get_bootstrap_status(self) -> dict[str, Any]:
        """Get current bootstrap status for debugging"""
        try:
            admins = self.user_service.get_all_admins()
            return {
                "completed": st.session_state.get("bootstrap_completed", False),
                "admins_count": len(admins),
                "session_state_keys": list(st.session_state.keys()),
                "status": "healthy" if admins else "no_admins",
            }
        except Exception as e:
            return {"completed": False, "error": str(e), "status": "error"}
