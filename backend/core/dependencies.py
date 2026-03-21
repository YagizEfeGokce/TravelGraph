"""Reusable FastAPI dependencies for authentication."""
from __future__ import annotations

from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.security import decode_token
from db.connection import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
_optional_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login", auto_error=False
)


def _fetch_user_by_id(db: Any, user_id: str) -> dict | None:
    """Return node properties for the user with the given *user_id*, or ``None``."""
    result = db.query(
        "MATCH (u:User {id: $id}) RETURN u",
        {"id": user_id},
    )
    if not result.result_set:
        return None
    return result.result_set[0][0].properties


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Any = Depends(get_db),
) -> dict:
    """Resolve the currently authenticated user from the Bearer token.

    Raises:
        HTTPException(401): If the token is missing, invalid, or the user no longer exists.
    """
    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str | None = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing subject claim",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = _fetch_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_optional_user(
    token: str | None = Depends(_optional_oauth2_scheme),
    db: Any = Depends(get_db),
) -> dict | None:
    """Resolve the authenticated user if a valid token is present.

    Returns ``None`` instead of raising when the token is absent or invalid,
    making it suitable for endpoints that behave differently for guests.
    """
    if token is None:
        return None

    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        return None

    user_id: str | None = payload.get("sub")
    if not user_id:
        return None

    return _fetch_user_by_id(db, user_id)
