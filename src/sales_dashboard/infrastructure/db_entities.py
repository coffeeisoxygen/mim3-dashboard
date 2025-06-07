from __future__ import annotations

from datetime import UTC, datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Modern SQLAlchemy declarative base"""

    pass


class AuditMixin:
    """Common audit fields for tracking CRUD operations"""

    # TODO: Consider adding batch_id for CSV import grouping
    # TODO: Add soft delete fields (deleted_by, deleted_at) for compliance
    # TODO: Evaluate if we need IP address tracking for security audit

    # Creation tracking
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), nullable=False
    )

    # Update tracking
    updated_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )


class UserEntity(Base):
    """User entity - core authentication"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nama: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Self-managed timestamps (no audit for users)
    created: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), nullable=False
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<UserEntity id={self.id} username={self.username}>"

    def __str__(self) -> str:
        return f"{self.username} ({self.email})"


# =============================================================================
# 🚧 FUTURE ENTITIES - TODO: Implement after user management refactoring
# =============================================================================

# TODO: Geographic hierarchy entities for MIM3 territory management
# class DesaEntity(Base, AuditMixin):
#     """Desa (village) entity with population and geographic data"""
#     __tablename__ = "desa"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(100), nullable=False)
#     population: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
#     # TODO: Add lat/lng fields for geospatial calculations
#     # TODO: Add kecamatan relationship
#     # TODO: Consider PostGIS for complex geographic queries

# TODO: BTS Tower/Site entity from Indosat data
# class SiteEntity(Base, AuditMixin):
#     """BTS tower sites with coverage data"""
#     __tablename__ = "sites"
#     # TODO: site_id from Indosat (external ID)
#     # TODO: lat/lng for Haversine distance calculations
#     # TODO: coverage_radius for overlap analysis
#     # TODO: Manual desa assignment override field

# TODO: Business outlet entity with geospatial relationships
# class OutletEntity(Base, AuditMixin):
#     """Business outlets with location and site assignment"""
#     __tablename__ = "outlets"
#     # TODO: Many columns from CSV import
#     # TODO: lat/lng for nearest site calculation
#     # TODO: Auto-assigned site_id via Haversine
#     # TODO: Manual assignment override

# TODO: Consider separate file for geospatial utilities
# - Haversine distance calculation functions
# - Coverage area intersection logic
# - Manual locator tools for admin users


# Event listener for audit updates
@event.listens_for(UserEntity, "before_update")
def update_user_timestamp(_mapper, _connection, target):
    """Update timestamp on user entity update"""
    target.updated = datetime.now(UTC)


# TODO: Remove after user management refactoring complete
class DesaEntity(Base, AuditMixin):
    """Desa (village) entity with audit tracking - PLACEHOLDER"""

    __tablename__ = "desa"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    population: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
