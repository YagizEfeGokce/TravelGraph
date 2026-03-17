"""Authentication routes: register, login, token refresh, and current-user lookup."""

import time
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from core.dependencies import get_current_user
from core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from db.connection import get_db
from models.user import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

# ── In-memory login rate limiter ───────────────────────────────────────────────
# Maps email → list of failure timestamps (epoch seconds)
_failed_logins: dict[str, list[float]] = {}
_LOCKOUT_ATTEMPTS: int = 5
_LOCKOUT_SECONDS: int = 15 * 60


def _check_lockout(email: str) -> None:
    """Raise HTTP 429 if *email* has exceeded the failed-login threshold."""
    now = time.time()
    recent = [t for t in _failed_logins.get(email, []) if now - t < _LOCKOUT_SECONDS]
    _failed_logins[email] = recent
    if len(recent) >= _LOCKOUT_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed login attempts. Try again in 15 minutes.",
        )


def _record_failure(email: str) -> None:
    _failed_logins.setdefault(email, []).append(time.time())


def _clear_failures(email: str) -> None:
    _failed_logins.pop(email, None)


# ── Helper ─────────────────────────────────────────────────────────────────────

def _node_to_response(db: Any, user_id: str) -> UserResponse:
    """Fetch a User node by id and return a UserResponse."""
    result = db.query(
        "MATCH (u:User {id: $id}) RETURN u",
        {"id": user_id},
    )
    if not result.result_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse.from_node(result.result_set[0][0].properties)


# ── Pydantic request bodies ────────────────────────────────────────────────────

class RefreshRequest(BaseModel):
    """Body accepted by the token-refresh endpoint."""

    refresh_token: str


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(body: UserCreate, db: Any = Depends(get_db)) -> dict:
    """Register a new user.

    Returns the created user together with a fresh token pair.
    Raises HTTP 409 if the e-mail address is already taken.
    """
    # Email uniqueness check
    existing = db.query(
        "MATCH (u:User {email: $email}) RETURN u",
        {"email": body.email},
    )
    if existing.result_set:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )

    user_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    db.query(
        "CREATE (u:User {id: $id, email: $email, name: $name, "
        "password_hash: $ph, created_at: $ca}) RETURN u",
        {
            "id": user_id,
            "email": body.email,
            "name": body.name,
            "ph": hash_password(body.password),
            "ca": created_at,
        },
    )

    token_data = {"sub": user_id}
    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
        "token_type": "bearer",
        "user": _node_to_response(db, user_id).model_dump(),
    }


@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Any = Depends(get_db),
) -> dict:
    """Authenticate a user with email and password.

    ``form.username`` is treated as the email address.
    Raises HTTP 429 after 5 consecutive failures within 15 minutes.
    """
    email = form.username

    _check_lockout(email)

    result = db.query(
        "MATCH (u:User {email: $email}) RETURN u",
        {"email": email},
    )
    if not result.result_set:
        _record_failure(email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    user_props: dict = result.result_set[0][0].properties

    if not verify_password(form.password, user_props["password_hash"]):
        _record_failure(email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    _clear_failures(email)

    token_data = {"sub": user_props["id"]}
    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
        "token_type": "bearer",
        "user": UserResponse.from_node(user_props).model_dump(),
    }


@router.post("/refresh")
def refresh_token(body: RefreshRequest) -> dict:
    """Issue a new access token from a valid refresh token."""
    payload = decode_token(body.refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user_id: str | None = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is missing subject claim",
        )

    return {
        "access_token": create_access_token({"sub": user_id}),
        "token_type": "bearer",
    }


@router.get("/me")
def me(current_user: dict = Depends(get_current_user)) -> dict:
    """Return the authenticated user's profile."""
    return UserResponse.from_node(current_user).model_dump()
