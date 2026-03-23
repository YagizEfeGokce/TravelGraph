"""Reviews routes: create and list reviews for activities, accommodations, restaurants."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel, Field

from core.dependencies import get_current_user, get_optional_user
from db.connection import get_db

router = APIRouter(tags=["reviews"])

class ReviewCreate(BaseModel):
    target_id: str
    target_type: str  # "activity" | "accommodation" | "restaurant"
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(default="", max_length=1000)

@router.get("/reviews")
def list_reviews(
    target_id: str = Query(...),
    target_type: str = Query(...),
    db: Any = Depends(get_db),
    _user: dict | None = Depends(get_optional_user),
) -> dict:
    """Return all reviews for a given target, plus the average rating."""
    result = db.query(
        "MATCH (u:User)-[:WROTE]->(r:Review)-[:ABOUT]->(t {id: $target_id}) "
        "RETURN r, u.name AS user_name "
        "ORDER BY r.created_at DESC",
        {"target_id": target_id},
    )
    reviews = []
    total_rating = 0
    for row in result.result_set:
        props = dict(row[0].properties)
        props["user_name"] = row[1]
        reviews.append(props)
        total_rating += props.get("rating", 0)
        
    avg_rating = total_rating / len(reviews) if reviews else 0.0
    
    return {
        "reviews": reviews,
        "average_rating": avg_rating
    }

@router.post("/reviews", status_code=status.HTTP_201_CREATED)
def create_review(
    body: ReviewCreate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Create a review for an activity, accommodation, or restaurant."""
    # Check if duplicate
    dup_check = db.query(
        "MATCH (u:User {id: $uid})-[:WROTE]->(r:Review)-[:ABOUT]->(t {id: $tid}) RETURN r",
        {"uid": current_user["id"], "tid": body.target_id}
    )
    if dup_check.result_set:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already reviewed this item.")
        
    # Verify the target exists
    target_check = db.query(
        "MATCH (t {id: $tid}) RETURN t",
        {"tid": body.target_id}
    )
    if not target_check.result_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target item not found.")

    review_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    db.query(
        "MATCH (u:User {id: $uid}), (t {id: $tid}) "
        "CREATE (r:Review {id: $id, target_id: $tid, target_type: $ttype, rating: $rating, comment: $comment, created_at: $ca}) "
        "CREATE (u)-[:WROTE]->(r) "
        "CREATE (r)-[:ABOUT]->(t)",
        {
            "uid": current_user["id"],
            "tid": body.target_id,
            "id": review_id,
            "ttype": body.target_type,
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

@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: str,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> Response:
    """Delete a review (only the author can delete it)."""
    res = db.query(
        "MATCH (u:User)-[:WROTE]->(r:Review {id: $id}) RETURN u.id",
        {"id": review_id}
    )
    if not res.result_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found.")
        
    author_id = res.result_set[0][0]
    if author_id != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own reviews.")
        
    db.query(
        "MATCH (r:Review {id: $id}) DETACH DELETE r",
        {"id": review_id}
    )
    return Response(status_code=204)
