from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Any

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import streamlit as st

from sales_dashboard.utils.hasher import get_password_hasher

# =============================================================================
# 🔧 DATABASE CONFIGURATION
# =============================================================================
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
DATABASE_URL = f"sqlite:///{DATA_DIR}/sales_dashboard.db"

if TYPE_CHECKING:
    from sqlalchemy import Engine
    from sqlalchemy.orm import Session


# =============================================================================
# 🗄️ CORE DATABASE ENGINE & SESSIONS
# =============================================================================
@st.cache_resource
def get_database_engine() -> Engine:
    """Get database engine - cached for application lifetime"""
    try:
        logger.info("Creating database engine")

        # ✅ SIMPLE PATH - No complex settings
        db_path = Path(DATABASE_URL.replace("sqlite:///", ""))
        db_path.parent.mkdir(parents=True, exist_ok=True)

        # Create engine with simple configuration
        engine = create_engine(
            DATABASE_URL,
            echo=False,  # Set True for SQL debugging
            pool_pre_ping=True,
            pool_recycle=3600,  # 1 hour
            connect_args={
                "check_same_thread": False,  # SQLite threading
                "timeout": 30,
            },
        )

        return engine
    except Exception as e:
        logger.error(f"Failed to create database engine: {e}")
        raise


@st.cache_resource
def get_session_factory() -> sessionmaker[Session]:
    """Get session factory - cached for application lifetime"""
    try:
        engine = get_database_engine()
        return sessionmaker(bind=engine, expire_on_commit=False)
    except Exception as e:
        logger.error(f"Failed to create session factory: {e}")
        raise


def get_database_session() -> Session:
    """Get database session - NOT cached, create new each time"""
    try:
        SessionLocal = get_session_factory()
        return SessionLocal()
    except Exception as e:
        logger.error(f"Failed to create database session: {e}")
        raise


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Context manager for database sessions - recommended approach"""
    session = None
    try:
        session = get_database_session()
        yield session
        session.commit()
    except Exception as e:
        if session:
            session.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        if session:
            session.close()


# =============================================================================
# 🔗 STREAMLIT CONNECTIONS & CACHING
# =============================================================================
@st.cache_resource
def get_streamlit_connection() -> Any:
    """Get Streamlit SQL connection with configured settings"""
    try:
        # ✅ SIMPLE PATH - Direct database URL
        db_path = Path(DATABASE_URL.replace("sqlite:///", ""))
        db_path.parent.mkdir(parents=True, exist_ok=True)

        return st.connection(
            "sales_db",
            type="sql",
            url=DATABASE_URL,
        )
    except Exception as e:
        logger.error(f"Failed to create Streamlit connection: {e}")
        raise


def reset_connection_cache() -> None:
    """Reset Streamlit connection cache - call after data mutations"""
    try:
        conn = get_streamlit_connection()
        if hasattr(conn, "reset"):
            conn.reset()
            logger.debug("Streamlit connection cache reset")
        else:
            logger.warning("Connection does not support reset method")
    except Exception as e:
        logger.warning(f"Error resetting connection cache: {e}")


@contextmanager
def get_connection_session() -> Generator[Any, None, None]:
    """Context manager for Streamlit connection sessions (for writes)"""
    conn = None
    session = None
    try:
        conn = get_streamlit_connection()
        session = conn.session
        yield session
        session.commit()
    except Exception as e:
        if session:
            session.rollback()
        logger.error(f"Connection session error: {e}")
        raise


# =============================================================================
# 🏗️ DATABASE OPERATIONS (Tables, Schema Management)
# =============================================================================
def create_all_tables() -> None:
    """Create all database tables"""
    try:
        from sales_dashboard.infrastructure.db_entities import Base

        engine = get_database_engine()
        Base.metadata.create_all(engine)
        logger.info("All database tables created")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise


def reset_database() -> None:
    """Reset database - useful for development"""
    try:
        if st.session_state.get("debug_mode", False):
            from sales_dashboard.infrastructure.db_entities import Base

            engine = get_database_engine()
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)

            # Reset connection cache after schema changes
            reset_connection_cache()

            logger.warning("Database reset completed")
        else:
            logger.warning("Database reset attempted but debug_mode is not enabled")
    except Exception as e:
        logger.error(f"Failed to reset database: {e}")
        raise


# =============================================================================
# 🚀 DATABASE INITIALIZATION & BOOTSTRAP
# =============================================================================
@st.cache_resource
def ensure_database_ready() -> bool:
    """Initialize database - Streamlit native caching approach"""
    try:
        logger.info("Starting database initialization...")

        # App-level operations cached for app lifetime
        create_all_tables()
        create_default_admin()

        logger.info("Database initialized successfully")
        return True

    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


@st.cache_resource
def create_default_admin() -> bool:
    """Create default admin - cached to prevent duplicates"""
    try:
        from sales_dashboard.infrastructure.db_entities import UserEntity

        with get_db_session() as session:
            # Check if admin already exists
            admin = (
                session.query(UserEntity).filter(UserEntity.username == "admin").first()
            )

            if admin:
                logger.debug("Admin user already exists - skipping creation")
                return True

            # Create admin user
            hasher = get_password_hasher()
            hashed_password = hasher.hash_password("admin123")

            admin_user = UserEntity(
                nama="Administrator",
                email="admin@dashboard.com",
                username="admin",
                password=hashed_password,
                is_admin=True,
                is_active=True,
            )
            session.add(admin_user)
            logger.info("Default admin user created successfully")
            return True

    except Exception as e:
        logger.error(f"Failed to create default admin: {e}")
        raise


# DEVNOTE : this is just a reminder we we got a troble to check the streamlit docs
# =============================================================================
# - Current session state approach works but cache might be more Streamlit-native
# - Evaluate performance impact before switching
# - See Streamlit docs: https://docs.streamlit.io/develop/concepts/architecture/caching

# TODO: Remove Streamlit connection complexity after user operations migration
# - Once we fully migrate to simple user_operations.py functions
# - We can remove get_streamlit_connection() and related cache management
# - Simplify to just SQLAlchemy sessions via get_db_session()
