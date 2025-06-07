"""User operations - simple functions using UserEntity directly"""

from __future__ import annotations

from typing import Optional

from loguru import logger

from sales_dashboard.infrastructure.db_engine import get_db_session
from sales_dashboard.infrastructure.db_entities import UserEntity
from sales_dashboard.utils.hasher import get_password_hasher


def authenticate_user(username: str, password: str) -> Optional[UserEntity]:
    """Authenticate user - returns UserEntity directly for Streamlit session"""
    try:
        with get_db_session() as session:
            user = (
                session.query(UserEntity)
                .filter(UserEntity.username == username, UserEntity.is_active)
                .first()
            )

            if user and _verify_password(password, user.password):
                logger.info(f"User {username} authenticated successfully")
                return user

            logger.warning(f"Authentication failed for {username}")
            return None

    except Exception as e:
        logger.error(f"Authentication error for {username}: {e}")
        return None


def create_user_by_admin(
    admin_user_id: int,
    nama: str,
    email: str,
    username: str,
    password: str,
    is_admin: bool = False,
) -> Optional[UserEntity]:
    """Create new user - admin only operation"""
    try:
        with get_db_session() as session:
            # Verify admin permissions
            admin = (
                session.query(UserEntity)
                .filter(
                    UserEntity.id == admin_user_id,
                    UserEntity.is_admin,
                    UserEntity.is_active,
                )
                .first()
            )

            if not admin:
                logger.warning(
                    f"User {admin_user_id} is not authorized to create users"
                )
                return None

            # Check if username already exists
            existing_user = (
                session.query(UserEntity)
                .filter(UserEntity.username == username)
                .first()
            )

            if existing_user:
                logger.warning(f"Username {username} already exists")
                return None

            # Check if email already exists
            existing_email = (
                session.query(UserEntity).filter(UserEntity.email == email).first()
            )

            if existing_email:
                logger.warning(f"Email {email} already exists")
                return None

            # Create new user
            hashed_password = _hash_password(password)
            user = UserEntity(
                nama=nama,
                email=email,
                username=username,
                password=hashed_password,
                is_admin=is_admin,
                is_active=True,
            )

            session.add(user)
            session.flush()  # Get ID before commit

            logger.info(
                f"User {username} created successfully by admin {admin.username}"
            )
            return user

    except Exception as e:
        logger.error(f"Failed to create user {username}: {e}")
        return None


def activate_user(admin_user_id: int, target_user_id: int) -> bool:
    """Activate user - admin only operation"""
    try:
        with get_db_session() as session:
            # Verify admin permissions
            admin = (
                session.query(UserEntity)
                .filter(
                    UserEntity.id == admin_user_id,
                    UserEntity.is_admin,
                    UserEntity.is_active,
                )
                .first()
            )

            if not admin:
                logger.warning(
                    f"User {admin_user_id} is not authorized to activate users"
                )
                return False

            # Find target user
            target_user = (
                session.query(UserEntity)
                .filter(UserEntity.id == target_user_id)
                .first()
            )

            if not target_user:
                logger.warning(f"User {target_user_id} not found")
                return False

            # Activate user
            target_user.is_active = True

            logger.info(
                f"User {target_user.username} activated by admin {admin.username}"
            )
            return True

    except Exception as e:
        logger.error(f"Failed to activate user {target_user_id}: {e}")
        return False


def deactivate_user(admin_user_id: int, target_user_id: int) -> bool:
    """Deactivate user (soft delete) - admin only operation"""
    try:
        with get_db_session() as session:
            # Verify admin permissions
            admin = (
                session.query(UserEntity)
                .filter(
                    UserEntity.id == admin_user_id,
                    UserEntity.is_admin,
                    UserEntity.is_active,
                )
                .first()
            )

            if not admin:
                logger.warning(
                    f"User {admin_user_id} is not authorized to deactivate users"
                )
                return False

            # Find target user
            target_user = (
                session.query(UserEntity)
                .filter(UserEntity.id == target_user_id)
                .first()
            )

            if not target_user:
                logger.warning(f"User {target_user_id} not found")
                return False

            # Prevent admin from deactivating themselves
            if target_user_id == admin_user_id:
                logger.warning(f"Admin {admin.username} cannot deactivate themselves")
                return False

            # Deactivate user
            target_user.is_active = False

            logger.info(
                f"User {target_user.username} deactivated by admin {admin.username}"
            )
            return True

    except Exception as e:
        logger.error(f"Failed to deactivate user {target_user_id}: {e}")
        return False


def get_user_by_id(user_id: int) -> Optional[UserEntity]:
    """Get user by ID - simple query function"""
    try:
        with get_db_session() as session:
            return (
                session.query(UserEntity)
                .filter(UserEntity.id == user_id, UserEntity.is_active)
                .first()
            )
    except Exception as e:
        logger.error(f"Failed to get user by ID {user_id}: {e}")
        return None


def get_all_active_users() -> list[UserEntity]:
    """Get all active users - for admin interface"""
    try:
        with get_db_session() as session:
            return (
                session.query(UserEntity)
                .filter(UserEntity.is_active)
                .order_by(UserEntity.created.desc())
                .all()
            )
    except Exception as e:
        logger.error(f"Failed to get active users: {e}")
        return []


def change_user_password(
    user_id: int, current_password: str, new_password: str
) -> bool:
    """Allow user to change their own password with current password verification"""
    try:
        with get_db_session() as session:
            # Get user and verify current password
            user = (
                session.query(UserEntity)
                .filter(UserEntity.id == user_id, UserEntity.is_active)
                .first()
            )

            if not user:
                logger.warning(f"User {user_id} not found or inactive")
                return False

            # Verify current password
            if not _verify_password(current_password, user.password):
                logger.warning(
                    f"Password change failed for user {user.username} - incorrect current password"
                )
                return False

            # Hash new password and update
            new_hashed_password = _hash_password(new_password)
            user.password = new_hashed_password

            logger.info(f"Password changed successfully for user {user.username}")
            return True

    except Exception as e:
        logger.error(f"Failed to change password for user {user_id}: {e}")
        return False


def admin_reset_user_password(
    admin_user_id: int, target_user_id: int, new_password: str
) -> bool:
    """Allow admin to reset any user's password - admin only operation"""
    try:
        with get_db_session() as session:
            # Verify admin permissions
            admin = (
                session.query(UserEntity)
                .filter(
                    UserEntity.id == admin_user_id,
                    UserEntity.is_admin,
                    UserEntity.is_active,
                )
                .first()
            )

            if not admin:
                logger.warning(
                    f"User {admin_user_id} is not authorized to reset passwords"
                )
                return False

            # Find target user
            target_user = (
                session.query(UserEntity)
                .filter(UserEntity.id == target_user_id, UserEntity.is_active)
                .first()
            )

            if not target_user:
                logger.warning(f"Target user {target_user_id} not found or inactive")
                return False

            # Hash new password and update
            new_hashed_password = _hash_password(new_password)
            target_user.password = new_hashed_password

            logger.info(
                f"Password reset for user {target_user.username} by admin {admin.username}"
            )
            return True

    except Exception as e:
        logger.error(f"Failed to reset password for user {target_user_id}: {e}")
        return False


# =============================================================================
# 🔒 PRIVATE HELPER FUNCTIONS
# =============================================================================


def _verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against hash using hasher utility"""
    try:
        hasher = get_password_hasher()
        return hasher.verify_password(password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False


def _hash_password(password: str) -> str:
    """Hash password using hasher utility"""
    try:
        hasher = get_password_hasher()
        return hasher.hash_password(password)
    except Exception as e:
        logger.error(f"Password hashing error: {e}")
        raise
