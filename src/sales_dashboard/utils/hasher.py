"""Password hashing utilities.

Simple password hasher with fallback options.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import hashlib

from sales_dashboard.config.constant import SIMPLE_HASH_SALT
from sales_dashboard.config.messages import ERROR_BCRYPT_NOT_AVAILABLE

try:
    import bcrypt

    BCRYPT_AVAILABLE = True
except ImportError:
    bcrypt = None
    BCRYPT_AVAILABLE = False


class PasswordHasher(ABC):
    """Abstract password hasher interface"""

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        pass

    @abstractmethod
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        pass


class SimpleHasher(PasswordHasher):
    """Simple SHA256 hasher for development/testing"""

    def hash_password(self, password: str) -> str:
        """Hash password using SHA256 with salt"""
        return hashlib.sha256(f"{password}{SIMPLE_HASH_SALT}".encode()).hexdigest()

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return self.hash_password(password) == hashed


class BcryptHasher(PasswordHasher):
    """Bcrypt hasher for production"""

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        if not BCRYPT_AVAILABLE or bcrypt is None:
            raise RuntimeError(ERROR_BCRYPT_NOT_AVAILABLE)
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against bcrypt hash"""
        if not BCRYPT_AVAILABLE or bcrypt is None:
            raise RuntimeError(ERROR_BCRYPT_NOT_AVAILABLE)
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def get_password_hasher(use_bcrypt: bool = True) -> PasswordHasher:
    """Get appropriate password hasher"""
    if use_bcrypt and BCRYPT_AVAILABLE:
        return BcryptHasher()
    return SimpleHasher()
