from __future__ import annotations

from typing import List

from sales_dashboard.domain.models.user import User
from sales_dashboard.domain.schemas.user import UserCreate, UserCreateByAdmin
from sales_dashboard.domain.repository.user_repository import UserRepository
from sales_dashboard.services.interfaces import (
    UserServiceInterface,
    AuthServiceInterface,
)


class UserService(UserServiceInterface):
    """User management service - focused on CRUD operations"""

    def __init__(
        self, user_repo: UserRepository, auth_service: AuthServiceInterface
    ) -> None:
        self.user_repo = user_repo
        self.auth_service = auth_service

    def create_user(self, user_data: UserCreate) -> User:
        """Create regular user (no admin privileges)"""
        # Validation
        if self.user_repo.get_by_username(user_data.username):
            raise ValueError("Username already exists")
        if self.user_repo.get_by_email(user_data.email):
            raise ValueError("Email already exists")

        # Create user
        user = User(
            id=None,
            nama=user_data.nama,
            email=user_data.email,
            username=user_data.username,
            password=self.auth_service.hash_password(user_data.password),
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

        # Validation
        if self.user_repo.get_by_username(user_data.username):
            raise ValueError("Username already exists")
        if self.user_repo.get_by_email(user_data.email):
            raise ValueError("Email already exists")

        user = User(
            id=None,
            nama=user_data.nama,
            email=user_data.email,
            username=user_data.username,
            password=self.auth_service.hash_password(user_data.password),
            is_admin=user_data.is_admin,
            is_active=True,
        )

        return self.user_repo.create(user)

    def get_all_active_users(self) -> List[User]:
        """Get all active users"""
        return self.user_repo.get_all_active()

    def get_all_admins(self) -> List[User]:
        """Get all admin users"""
        return self.user_repo.get_all_admins()

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
