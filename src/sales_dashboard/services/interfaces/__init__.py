# services/interfaces/__init__.py
from __future__ import annotations

from typing import Any, Protocol

from sales_dashboard.domain.models.user import User
from sales_dashboard.domain.schemas.user import UserCreate, UserCreateByAdmin, UserLogin


class AuthServiceInterface(Protocol):
    """Authentication service contract"""

    def authenticate(self, login_data: UserLogin) -> User | None: ...
    def verify_password(self, plain_password: str, hashed_password: str) -> bool: ...
    def hash_password(self, password: str) -> str: ...


class UserServiceInterface(Protocol):
    """User management service contract"""

    def create_user(self, user_data: UserCreate) -> User: ...
    def create_user_by_admin(
        self, user_data: UserCreateByAdmin, admin_user: User
    ) -> User: ...
    def get_all_active_users(self) -> list[User]: ...  # ✅ Missing method
    def get_all_admins(
        self,
    ) -> list[User]: ...  # ✅ Missing method - used by bootstrap!
    def deactivate_user(self, user_id: int, admin_user: User) -> bool: ...
    def make_admin(self, user_id: int, admin_user: User) -> User: ...


class HealthServiceInterface(Protocol):
    """Health check service contract"""

    def check_database_health(self) -> dict[str, Any]: ...
    def check_application_health(self) -> dict[str, Any]: ...


class BootstrapServiceInterface(Protocol):
    """System bootstrap service contract"""

    def ensure_default_admin(self) -> User | None: ...
    def reset_bootstrap_cache(self) -> None: ...


class SessionServiceInterface(Protocol):
    """Session management service contract"""

    def create_session(self, user: User) -> dict[str, Any]: ...
    def get_current_user(self) -> User | None: ...
    def destroy_session(self) -> None: ...
    def is_admin(self) -> bool: ...
    def require_login(self) -> User: ...
    def require_admin(self) -> User: ...
    def get_session_info(self) -> dict[str, Any]: ...


class MetadataServiceInterface(Protocol):
    """Metadata service contract"""

    def get_metadata(self) -> dict[str, Any]: ...
    def get_build_info(self) -> dict[str, Any]: ...
    def show_app_info(self) -> None: ...


class AdvancedBootstrapServiceInterface(Protocol):
    """Advanced bootstrap service contract for ETL operations"""

    def ensure_database_schema(self) -> bool:
        """Ensure database schema is up to date"""
        ...

    def ensure_default_settings(self) -> dict[str, Any]:
        """Ensure default application settings"""
        ...

    def ensure_sample_data(self) -> bool:
        """Create sample data for demo purposes"""
        ...

    def validate_environment(self) -> dict[str, Any]:
        """Validate runtime environment for ETL operations"""
        ...
