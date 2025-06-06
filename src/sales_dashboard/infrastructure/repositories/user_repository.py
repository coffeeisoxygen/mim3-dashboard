from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List
from loguru import logger

from sales_dashboard.domain.models.user import User
from sales_dashboard.domain.repository.user_repository import UserRepository
from sales_dashboard.infrastructure.db_engine import get_db_session, get_streamlit_connection
from sales_dashboard.infrastructure.db_entities import UserEntity

if TYPE_CHECKING:
    import pandas as pd


class SQLUserRepository(UserRepository):
    """SQLAlchemy implementation of UserRepository"""

    def get_by_username(self, username: str) -> Optional[User]:
        """Find user by username"""
        conn = get_streamlit_connection()
        result = conn.query(
            "SELECT * FROM users WHERE username = :username AND is_active = 1",
            params={"username": username},
        )

        if result.empty:
            return None

        row = result.iloc[0]
        return self._pandas_to_domain(row)

    def get_by_email(self, email: str) -> Optional[User]:
        """Find user by email"""
        conn = get_streamlit_connection()
        result = conn.query(
            "SELECT * FROM users WHERE email = :email AND is_active = 1",
            params={"email": email},
        )

        if result.empty:
            return None

        row = result.iloc[0]
        return self._pandas_to_domain(row)

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Find user by ID"""
        conn = get_streamlit_connection()
        result = conn.query(
            "SELECT * FROM users WHERE id = :user_id AND is_active = 1",
            params={"user_id": user_id},
        )

        if result.empty:
            return None

        row = result.iloc[0]
        return self._pandas_to_domain(row)

    def create(self, user: User) -> User:
        """Create new user"""
        logger.debug(f"Creating user: {user.username}")

        with get_db_session() as session:
            entity = UserEntity(
                nama=user.nama,
                email=user.email,
                username=user.username,
                password=user.password,
                is_admin=user.is_admin,
                is_active=user.is_active,
            )
            session.add(entity)
            session.flush()  # Get ID without committing yet
            user.id = entity.id
            # session.commit() handled by context manager

        logger.info(f"User created successfully with ID: {user.id}")
        return user

    def update(self, user: User) -> User:
        """Update existing user"""
        if user.id is None:
            raise ValueError("Cannot update user without ID")

        logger.debug(f"Updating user ID: {user.id}")

        with get_db_session() as session:
            entity = session.get(UserEntity, user.id)
            if not entity:
                raise ValueError(f"User with ID {user.id} not found")

            # Update entity fields
            entity.nama = user.nama
            entity.email = user.email
            entity.username = user.username
            entity.password = user.password
            entity.is_admin = user.is_admin
            entity.is_active = user.is_active
            # entity.updated will be auto-updated by event listener

        logger.info(f"User updated successfully: {user.username}")
        return user

    def delete(self, user_id: int) -> bool:
        """Soft delete user (set is_active=False)"""
        logger.debug(f"Soft deleting user ID: {user_id}")

        with get_db_session() as session:
            entity = session.get(UserEntity, user_id)
            if not entity:
                logger.warning(f"User with ID {user_id} not found for deletion")
                return False

            entity.is_active = False
            # entity.updated will be auto-updated by event listener

        logger.info(f"User soft deleted successfully: {user_id}")
        return True

    def get_all_active(self) -> List[User]:
        """Get all active users"""
        conn = get_streamlit_connection()
        result = conn.query("SELECT * FROM users WHERE is_active = 1 ORDER BY created DESC")

        if result.empty:
            return []

        return [self._pandas_to_domain(row) for _, row in result.iterrows()]

    def get_all_admins(self) -> List[User]:
        """Get all admin users with explicit boolean handling"""
        conn = get_streamlit_connection()
        result = conn.query(
            "SELECT * FROM users WHERE is_admin = ? AND is_active = ? ORDER BY created DESC",
            params=[True, True]  # Use explicit boolean values
        )

        if result.empty:
            logger.debug("No admin users found in database")
            return []

        admins = [self._pandas_to_domain(row) for _, row in result.iterrows()]
        logger.debug(f"Found {len(admins)} admin users")
        return admins

    def _pandas_to_domain(self, row: pd.Series) -> User:
        """Convert pandas Series to domain model"""
        return User(
            id=int(row["id"]),
            nama=str(row["nama"]),
            email=str(row["email"]),
            username=str(row["username"]),
            password=str(row["password"]),
            is_admin=bool(row["is_admin"]),
            is_active=bool(row["is_active"]),
            created=row["created"],
            updated=row["updated"],
        )
