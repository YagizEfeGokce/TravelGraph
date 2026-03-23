"""User routes: profile management and user graph operations."""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])
