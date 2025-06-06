from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    """Schema for creating regular users"""

    nama: str = Field(..., max_length=100, description="Nama lengkap pengguna")
    email: EmailStr = Field(..., description="Email valid pengguna")
    username: str = Field(
        ..., min_length=3, max_length=50, description="Username unik pengguna"
    )
    password: str = Field(..., min_length=6, description="Password minimal 6 karakter")
    # No is_admin field - security by design


class UserCreateByAdmin(BaseModel):
    """Schema for admin creating users with privileges"""

    nama: str = Field(..., max_length=100, description="Nama lengkap pengguna")
    email: EmailStr = Field(..., description="Email valid pengguna")
    username: str = Field(
        ..., min_length=3, max_length=50, description="Username unik pengguna"
    )
    password: str = Field(..., min_length=6, description="Password minimal 6 karakter")
    is_admin: bool = Field(
        default=False, description="Hak akses admin (hanya admin yang dapat mengatur)"
    )


class UserLogin(BaseModel):
    """Schema for user login with Pydantic v2 syntax"""

    model_config = ConfigDict(
        str_strip_whitespace=True,  # Auto strip whitespace
        validate_assignment=True,  # Validate on assignment
    )

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username harus antara 3-50 karakter",
        examples=["admin", "user123"],
    )
    password: str = Field(
        ...,
        min_length=6,
        description="Password minimal 6 karakter",
        examples=["password123"],
    )


class UserUpdate(BaseModel):
    """Schema for updating user information"""

    nama: str | None = Field(None, max_length=100, description="Nama lengkap pengguna")
    email: EmailStr | None = Field(None, description="Email valid pengguna")
    password: str | None = Field(
        None, min_length=6, description="Password baru minimal 6 karakter"
    )


class UserStatusUpdate(BaseModel):
    """Schema for admin user status operations"""

    is_active: bool | None = Field(None, description="Status aktif pengguna")
    is_admin: bool | None = Field(None, description="Hak akses admin")


class UserOut(BaseModel):
    """Schema for user output data"""

    model_config = ConfigDict(from_attributes=True)  # Pydantic v2 syntax

    id: int
    nama: str
    email: EmailStr
    username: str
    is_admin: bool
    is_active: bool
    created: str  # Will be converted to string for JSON serialization
    updated: str
