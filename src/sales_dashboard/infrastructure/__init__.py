"""Infrastructure layer - database connections and core setup.

Simple, direct database operations following Streamlit patterns.
No complex repository abstractions - keep it simple for internal tool.
"""

from .db_engine import (
    create_all_tables,
    ensure_database_ready,
    get_database_engine,
    get_db_session,
)
from .db_entities import Base, UserEntity

__all__ = [
    # Core database setup
    "ensure_database_ready",
    "get_db_session",
    "get_database_engine",
    "create_all_tables",
    # Cache management
    # Database entities
    "Base",
    "UserEntity",
]
