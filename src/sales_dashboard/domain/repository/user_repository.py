from typing import Optional, List
from abc import ABC, abstractmethod
from sales_dashboard.domain.models.user import User

class UserRepository(ABC):
    """Abstract user repository interface"""

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Find user by username"""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Find user by email"""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Find user by ID"""
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        """Create new user"""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Update existing user"""
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Soft delete user (set is_active=False)"""
        pass

    @abstractmethod
    def get_all_active(self) -> List[User]:
        """Get all active users"""
        pass

    @abstractmethod
    def get_all_admins(self) -> List[User]:
        """Get all admin users"""
        pass
