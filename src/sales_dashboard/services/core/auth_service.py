# services/core/auth_service.py - Pure authentication
from __future__ import annotations

from typing import Optional
from loguru import logger

from sales_dashboard.domain.models.user import User
from sales_dashboard.domain.schemas.user import UserLogin
from sales_dashboard.domain.repository.user_repository import UserRepository
from sales_dashboard.utils.hasher import get_password_hasher
from sales_dashboard.services.interfaces import AuthServiceInterface

class AuthService(AuthServiceInterface):
    """Pure authentication service - single responsibility"""

    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo
        self.hasher = get_password_hasher(use_bcrypt=False)

    def authenticate(self, login_data: UserLogin) -> Optional[User]:
        """Authenticate user login"""
        logger.debug(f"Authenticating user: {login_data.username}")

        user = self.user_repo.get_by_username(login_data.username)
        if not user or not user.is_active:
            logger.warning(f"User not found or inactive: {login_data.username}")
            return None

        if self.verify_password(login_data.password, user.password):
            logger.info(f"Authentication successful: {login_data.username}")
            return user

        logger.warning(f"Authentication failed: {login_data.username}")
        return None

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.hasher.verify_password(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        """Hash password for storage"""
        return self.hasher.hash_password(password)
