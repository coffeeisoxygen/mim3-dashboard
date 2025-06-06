# services/interfaces/__init__.py
from __future__ import annotations

from typing import Protocol, Optional, Dict, Any, List
from sales_dashboard.domain.models.user import User
from sales_dashboard.domain.schemas.user import UserLogin, UserCreate, UserCreateByAdmin

class AuthServiceInterface(Protocol):
    """Authentication service contract"""

    def authenticate(self, login_data: UserLogin) -> Optional[User]: ...
    def verify_password(self, plain_password: str, hashed_password: str) -> bool: ...
    def hash_password(self, password: str) -> str: ...

class UserServiceInterface(Protocol):
    """User management service contract"""

    def create_user(self, user_data: UserCreate) -> User: ...
    def create_user_by_admin(self, user_data: UserCreateByAdmin, admin_user: User) -> User: ...
    def get_all_active_users(self) -> List[User]: ...  # ✅ Missing method
    def get_all_admins(self) -> List[User]: ...        # ✅ Missing method - used by bootstrap!
    def deactivate_user(self, user_id: int, admin_user: User) -> bool: ...
    def make_admin(self, user_id: int, admin_user: User) -> User: ...

class HealthServiceInterface(Protocol):
    """Health check service contract"""

    def check_database_health(self) -> Dict[str, Any]: ...
    def check_application_health(self) -> Dict[str, Any]: ...

class BootstrapServiceInterface(Protocol):
    """System bootstrap service contract"""

    def ensure_default_admin(self) -> Optional[User]: ...
    def reset_bootstrap_cache(self) -> None: ...

class SessionServiceInterface(Protocol):
    """Session management service contract"""

    def create_session(self, user: User) -> Dict[str, Any]: ...
    def get_current_user(self) -> Optional[User]: ...
    def destroy_session(self) -> None: ...
    def is_admin(self) -> bool: ...
    def require_login(self) -> User: ...
    def require_admin(self) -> User: ...
    def get_session_info(self) -> Dict[str, Any]: ...

class MetadataServiceInterface(Protocol):
    """Metadata service contract"""

    def get_metadata(self) -> Dict[str, Any]: ...
    def get_build_info(self) -> Dict[str, Any]: ...
    def show_app_info(self) -> None: ...

class AdvancedBootstrapService(BootstrapServiceInterface):
    def ensure_database_schema(self) -> bool:
        """Ensure database schema is up to date"""
        return True

    def ensure_default_settings(self) -> Dict[str, Any]:
        """Ensure default application settings"""
        return {}

    def ensure_sample_data(self) -> bool:
        """Create sample data for demo purposes"""
        return True

    def validate_environment(self) -> Dict[str, Any]:
        """Validate runtime environment for ETL operations"""
        return {}
