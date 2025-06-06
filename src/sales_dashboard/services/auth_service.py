"""Authentication service with modern type annotations"""

from __future__ import annotations

import hashlib
from typing import Optional

from loguru import logger

from sales_dashboard.domain.models.user import User
from sales_dashboard.infrastructure.repositories.user_repository import UserRepository


class AuthService:
    """Authentication service with proper typing"""

    def __init__(self) -> None:
        self._user_repo = UserRepository()

    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with proper password validation"""
        logger.debug(f"Authenticating user: {username}")

        user = self._user_repo.find_by_username(username)
        if not user:
            logger.warning(f"User not found: {username}")
            return None

        if not user.is_active:
            logger.warning(f"Inactive user tried to login: {username}")
            return None

        # Simple password check for now (TODO: Hash properly with bcrypt)
        if user.password == password:
            logger.info(f"Authentication successful: {username}")
            return user
        else:
            logger.warning(f"Authentication failed: {username}")
            return None

    def _hash_password(self, password: str) -> str:
        """Hash password - placeholder for now"""
        # TODO: Use bcrypt or argon2 for production
        return hashlib.sha256(password.encode()).hexdigest()

    def change_password(self, user: User, new_password: str) -> bool:
        """Change user password"""
        try:
            user.password = self._hash_password(new_password)
            self._user_repo.save(user)
            logger.info(f"Password changed for user: {user.username}")
            return True
        except Exception as e:
            logger.error(f"Failed to change password for {user.username}: {e}")
            return False
