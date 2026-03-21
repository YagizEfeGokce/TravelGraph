"""Pydantic v2 schemas for User entities."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, EmailStr, field_validator


class UserBase(BaseModel):
    """Shared fields present on every user representation."""

    email: EmailStr
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if len(v) < 2 or len(v) > 50:
            raise ValueError("Name must be between 2 and 50 characters")
        return v


class UserCreate(UserBase):
    """Payload accepted when registering a new user."""

    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(BaseModel):
    """Payload accepted when updating an existing user.  All fields are optional."""

    name: str | None = None
    password: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        if v is not None and (len(v) < 2 or len(v) > 50):
            raise ValueError("Name must be between 2 and 50 characters")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserResponse(UserBase):
    """User data safe to return in API responses — no password_hash field."""

    id: str
    created_at: str

    @classmethod
    def from_node(cls, properties: dict[str, Any]) -> "UserResponse":
        """Build a UserResponse from a FalkorDB node's properties dict."""
        return cls(
            id=properties["id"],
            email=properties["email"],
            name=properties["name"],
            created_at=properties["created_at"],
        )
