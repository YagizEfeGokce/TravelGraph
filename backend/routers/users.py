"""User routes: profile management and user graph operations."""

from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])
