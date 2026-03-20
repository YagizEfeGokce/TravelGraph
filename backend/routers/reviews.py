"""Reviews routes: create and list reviews for activities, accommodations, restaurants."""

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field

from core.dependencies import get_current_user, get_optional_user
from db.connection import get_db

router = APIRouter(prefix="/reviews", tags=["reviews"])


class ReviewCreate(BaseModel):
    target_id: str
    target_type: str  # "activity" | "accommodation" | "restaurant"
    rating: int = Field(..., ge=1, le=5)
    comment: str = ""


@router.get("")
def list_reviews(
    target_id: str = Query(...),
    target_type: str = Query(...),
    db: Any = Depends(get_db),
    _user: dict | None = Depends(get_optional_user),
) -> list[dict]:
    """Return all reviews for a given target (activity, accommodation, restaurant)."""
    result = db.query(
        "MATCH (u:User)-[:WROTE]->(r:Review {target_id: $target_id, target_type: $target_type})"
        " RETURN r, u.name AS user_name"
        " ORDER BY r.created_at DESC",
        {"target_id": target_id, "target_type": target_type},
    )
    reviews = []
    for row in result.result_set:
        props = dict(row[0].properties)
        props["user_name"] = row[1]
        reviews.append(props)
    return reviews


@router.post("", status_code=status.HTTP_201_CREATED)
def create_review(
    body: ReviewCreate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Create a review for an activity, accommodation, or restaurant."""
    review_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    db.query(
        "MATCH (u:User {id: $uid})"
        " CREATE (r:Review {id: $id, target_id: $target_id, target_type: $target_type,"
        " rating: $rating, comment: $comment, created_at: $ca})"
        " CREATE (u)-[:WROTE]->(r)",
        {
            "uid": current_user["id"],
            "id": review_id,
            "target_id": body.target_id,
            "target_type": body.target_type,
            "rating": body.rating,
            "comment": body.comment,
            "ca": created_at,
        },
    )
    return {
        "id": review_id,
        "target_id": body.target_id,
        "target_type": body.target_type,
        "rating": body.rating,
        "comment": body.comment,
        "created_at": created_at,
        "user_name": current_user.get("name", ""),
    }
