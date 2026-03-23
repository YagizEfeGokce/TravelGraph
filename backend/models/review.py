"""Pydantic v2 schemas for Review entities."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, field_validator


TargetType = Literal["activity", "accommodation", "restaurant"]


class ReviewCreate(BaseModel):
    """Payload accepted when submitting a review."""

    target_id: str
    target_type: TargetType
    rating: int
    comment: str

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, v: int) -> int:
        if not 1 <= v <= 5:
            raise ValueError("rating must be between 1 and 5")
        return v

    @field_validator("comment")
    @classmethod
    def validate_comment(cls, v: str) -> str:
        if len(v) > 1000:
            raise ValueError("comment must not exceed 1000 characters")
        return v


class ReviewResponse(ReviewCreate):
    """Review data returned in API responses."""

    id: str
    user_name: str
    created_at: str

    @classmethod
    def from_node(
        cls,
        properties: dict[str, Any],
        user_name: str,
    ) -> "ReviewResponse":
        """Build a ReviewResponse from a FalkorDB node's properties dict."""
        return cls(
            id=properties["id"],
            target_id=properties["target_id"],
            target_type=properties["target_type"],
            rating=properties["rating"],
            comment=properties["comment"],
            user_name=user_name,
            created_at=properties["created_at"],
        )
