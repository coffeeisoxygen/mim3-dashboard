from __future__ import annotations

import os
from typing import TYPE_CHECKING

import streamlit as st
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if TYPE_CHECKING:
    from sqlalchemy import Engine
    from sqlalchemy.orm import Session


@st.cache_resource
def get_database_engine() -> Engine:
    """Get database engine"""
    logger.info("Creating database engine")

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # Create engine
    engine = create_engine(
        "sqlite:///data/sales_dashboard.db",
        echo=False,  # Set True for SQL debugging
        pool_pre_ping=True,
    )

    return engine


@st.cache_resource
def get_session_factory() -> sessionmaker[Session]:
    """Get session factory"""
    engine = get_database_engine()
    return sessionmaker(bind=engine)


def get_database_session() -> Session:
    """Get database session"""
    SessionLocal = get_session_factory()
    return SessionLocal()


@st.cache_resource
def get_streamlit_connection():
    """Get Streamlit connection for queries"""
    return st.connection(
        "sales_db", type="sql", url="sqlite:///data/sales_dashboard.db"
    )


def create_all_tables():
    """Create all database tables"""
    from sales_dashboard.infrastructure.db_entities import Base

    engine = get_database_engine()
    Base.metadata.create_all(engine)
    logger.info("All database tables created")
