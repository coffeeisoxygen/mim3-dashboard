from __future__ import annotations

import os
from contextlib import contextmanager
from typing import TYPE_CHECKING, Generator

import streamlit as st
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if TYPE_CHECKING:
    from sqlalchemy import Engine
    from sqlalchemy.orm import Session


@st.cache_resource
def get_database_engine() -> Engine:
    """Get database engine - cached for application lifetime"""
    logger.info("Creating database engine")

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

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


@st.cache_resource
def get_session_factory() -> sessionmaker[Session]:
    """Get session factory - cached for application lifetime"""
    engine = get_database_engine()
    return sessionmaker(bind=engine, expire_on_commit=False)


def get_database_session() -> Session:
    """Get database session - NOT cached, create new each time"""
    SessionLocal = get_session_factory()
    return SessionLocal()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Context manager for database sessions - recommended approach"""
    session = get_database_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@st.cache_resource
def get_streamlit_connection():
    """Get Streamlit connection for queries"""
    return st.connection(
        "sales_db",
        type="sql",
        url="sqlite:///data/sales_dashboard.db",
        ttl=600,  # Cache query results for 10 minutes
    )


def create_all_tables() -> None:
    """Create all database tables"""
    from sales_dashboard.infrastructure.db_entities import Base

    engine = get_database_engine()
    Base.metadata.create_all(engine)
    logger.info("All database tables created")


def reset_database() -> None:
    """Reset database - useful for development"""
    if st.session_state.get("debug_mode", False):
        from sales_dashboard.infrastructure.db_entities import Base

        engine = get_database_engine()
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        logger.warning("Database reset completed")
