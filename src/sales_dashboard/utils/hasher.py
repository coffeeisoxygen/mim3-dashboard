from __future__ import annotations

import hashlib
from typing import Protocol

class PasswordHasher(Protocol):
    """Protocol for password hashing implementations"""

    def hash_password(self, password: str) -> str:
        """Hash a password"""
        ...

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        ...

class SimpleHasher:
    """Simple SHA256 hasher for development - NOT for production"""

    def hash_password(self, password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return self.hash_password(password) == hashed

class BCryptHasher:
    """Production-ready bcrypt hasher"""

    def __init__(self):
        try:
            import bcrypt
            self.bcrypt = bcrypt
        except ImportError:
            raise ImportError(
                "bcrypt is required for BCryptHasher. Install with: uv add bcrypt"
            )

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = self.bcrypt.gensalt()
        return self.bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against bcrypt hash"""
        return self.bcrypt.checkpw(
            password.encode('utf-8'),
            hashed.encode('utf-8')
        )

# Factory function
def get_password_hasher(use_bcrypt: bool = False) -> PasswordHasher:
    """Get password hasher implementation"""
    if use_bcrypt:
        return BCryptHasher()
    return SimpleHasher()
