"""user model"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Optional

from annotated_types import MaxLen, MinLen


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
