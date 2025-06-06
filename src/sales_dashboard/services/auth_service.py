from __future__ import annotations

from loguru import logger

from sales_dashboard.domain.models.user import User
from sales_dashboard.domain.repository.user_repository import UserRepository
from sales_dashboard.domain.schemas.user import UserCreate, UserCreateByAdmin, UserLogin
from sales_dashboard.utils.hasher import get_password_hasher


class AuthService:
    """Authentication and user management service"""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self.hasher = get_password_hasher(use_bcrypt=False)  # Configure as needed

    def authenticate(self, login_data: UserLogin) -> User | None:
        """Authenticate user login"""
        logger.debug(f"Authenticating user: {login_data.username}")

        user = self.user_repo.get_by_username(login_data.username)
        if not user or not user.is_active:
            logger.warning(f"User not found or inactive: {login_data.username}")
            return None

        if self.hasher.verify_password(login_data.password, user.password):
            logger.info(f"Authentication successful: {login_data.username}")
            return user

        logger.warning(f"Authentication failed: {login_data.username}")
        return None

    def create_user(self, user_data: UserCreate) -> User:
        """Create regular user (no admin privileges)"""
        # Check if username/email already exists
        if self.user_repo.get_by_username(user_data.username):
            raise ValueError("Username already exists")

        if self.user_repo.get_by_email(user_data.email):
            raise ValueError("Email already exists")

        # Create regular user
        user = User(
            id=None,
            nama=user_data.nama,
            email=user_data.email,
            username=user_data.username,
            password=self.hasher.hash_password(user_data.password),
            is_admin=False,
            is_active=True,
        )

        return self.user_repo.create(user)

    def create_user_by_admin(
        self, user_data: UserCreateByAdmin, admin_user: User
    ) -> User:
        """Create user with admin privileges (admin only)"""
        if not admin_user.is_admin:
            raise PermissionError("Only admin can create users with privileges")

        # Check if username/email already exists
        if self.user_repo.get_by_username(user_data.username):
            raise ValueError("Username already exists")

        if self.user_repo.get_by_email(user_data.email):
            raise ValueError("Email already exists")

        user = User(
            id=None,
            nama=user_data.nama,
            email=user_data.email,
            username=user_data.username,
            password=self.hasher.hash_password(user_data.password),
            is_admin=user_data.is_admin,
            is_active=True,
        )

        return self.user_repo.create(user)

    def deactivate_user(self, user_id: int, admin_user: User) -> bool:
        """Deactivate user (admin only)"""
        if not admin_user.is_admin:
            raise PermissionError("Only admin can deactivate users")

        return self.user_repo.delete(user_id)

    def make_admin(self, user_id: int, admin_user: User) -> User:
        """Make user admin (admin only)"""
        if not admin_user.is_admin:
            raise PermissionError("Only admin can grant admin privileges")

        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        user.make_admin()
        return self.user_repo.update(user)
