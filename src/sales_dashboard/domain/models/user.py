"""user model"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Optional

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr, Field


@dataclass
class User:
    """User domain model with modern type annotations"""

    id: Optional[int]
    nama: Annotated[str, MaxLen(100)]
    email: Annotated[str, MaxLen(100)]
    username: Annotated[str, MinLen(3), MaxLen(50)]
    password: Annotated[str, MinLen(6)]  # Will be hashed
    is_admin: bool = False
    is_active: bool = True
    created: Optional[datetime] = None
    updated: Optional[datetime] = None

    def __post_init__(self):
        if self.created is None:
            self.created = datetime.utcnow()
        if self.updated is None:
            self.updated = datetime.utcnow()

    def deactivate(self):
        """Deactivate user"""
        self.is_active = False
        self.updated = datetime.utcnow()

    def make_admin(self):
        """Make user admin"""
        self.is_admin = True
        self.updated = datetime.utcnow()


class UserCreate(BaseModel):
    """Schema for creating new user (by admin)"""
    nama: str = Field(..., max_length=100)
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    is_admin: bool = False


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """Schema for updating user info"""
    nama: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)


class UserStatusUpdate(BaseModel):
    """Schema for admin operations"""
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


class UserOut(BaseModel):
    """Schema for user output"""
    id: int
    nama: str
    email: EmailStr
    username: str
    is_admin: bool
    is_active: bool
    created: datetime
    updated: datetime

    class Config:
        from_attributes = True
