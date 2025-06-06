from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Any

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import streamlit as st

if TYPE_CHECKING:
    from sqlalchemy import Engine
    from sqlalchemy.orm import Session


@st.cache_resource
def get_database_engine() -> Engine:
    """Get database engine - cached for application lifetime"""
    try:
        logger.info("Creating database engine")

        # Ensure data directory exists
        Path("data").mkdir(parents=True, exist_ok=True)

        # Create engine with proper SQLite settings
        engine = create_engine(
            "sqlite:///data/sales_dashboard.db",
            echo=False,  # Set True for SQL debugging
            pool_pre_ping=True,
            pool_recycle=3600,  # Recycle connections after 1 hour
            connect_args={
                "check_same_thread": False,  # Important for SQLite with multiple threads
                "timeout": 30,  # Connection timeout
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


@st.cache_resource
def get_streamlit_connection() -> Any:
    """Get Streamlit SQL connection with optimized settings"""
    try:
        # Ensure data directory exists
        Path("data").mkdir(parents=True, exist_ok=True)

        return st.connection(
            "sales_db",
            type="sql",
            url="sqlite:///data/sales_dashboard.db",
            # No default TTL - we'll control per query based on use case
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
