from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sales_dashboard.domain.models.user import User
from sales_dashboard.infrastructure.db_engine import (
    get_database_session,
    get_streamlit_connection,
)
from sales_dashboard.infrastructure.db_entities import UserEntity

if TYPE_CHECKING:
    import pandas as pd


class UserRepository:
    """User repository"""

    def find_by_username(self, username: str) -> Optional[User]:
        """Find user by username"""
        conn = get_streamlit_connection()
        result = conn.query(
            "SELECT * FROM users WHERE username = :username AND is_active = 1",
            params={"username": username},
        )

        if result.empty:
            return None

        row = result.iloc[0]
        return self._entity_to_domain(row)

    def save(self, user: User) -> User:
        """Save user to database"""
        session = get_database_session()
        try:
            if user.id is None:
                # Insert new
                entity = UserEntity(
                    nama=user.nama,
                    email=user.email,
                    username=user.username,
                    password=user.password,
                    is_admin=user.is_admin,
                    is_active=user.is_active,
                )
                session.add(entity)
                session.commit()
                session.refresh(entity)
                user.id = entity.id
            else:
                # Update existing
                session.query(UserEntity).filter(UserEntity.id == user.id).update({
                    "nama": user.nama,
                    "email": user.email,
                    "password": user.password,
                    "is_admin": user.is_admin,
                    "is_active": user.is_active,
                    "updated": user.updated,
                })
                session.commit()

            return user
        finally:
            session.close()

    def _entity_to_domain(self, row: pd.Series) -> User:
        """Convert database row to domain model"""
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
