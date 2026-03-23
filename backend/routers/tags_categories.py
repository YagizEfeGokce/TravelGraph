"""Tags and Categories routes: manage tags and categories, and their relations to activities."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from db.connection import get_db

router = APIRouter(tags=["tags_categories"])

class TagAddRequest(BaseModel):
    tag_id: str

@router.get("/tags")
def list_tags(db: Any = Depends(get_db)) -> list[dict]:
    """Retrieve all tags."""
    result = db.query("MATCH (t:Tag) RETURN t ORDER BY t.name ASC", {})
    return [dict(row[0].properties) for row in result.result_set]

@router.get("/categories")
def list_categories(db: Any = Depends(get_db)) -> list[dict]:
    """Retrieve all categories."""
    result = db.query("MATCH (c:Category) RETURN c ORDER BY c.name ASC", {})
    return [dict(row[0].properties) for row in result.result_set]

@router.post("/activities/{activity_id}/tags", status_code=status.HTTP_201_CREATED)
def add_tag_to_activity(
    activity_id: str,
    body: TagAddRequest,
    db: Any = Depends(get_db)
) -> dict:
    """Add a tag to an activity."""
    # Verify Activity exists
    act_check = db.query("MATCH (a:Activity {id: $id}) RETURN a", {"id": activity_id})
    if not act_check.result_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found.")
        
    # Verify Tag exists
    tag_check = db.query("MATCH (t:Tag {id: $id}) RETURN t", {"id": body.tag_id})
    if not tag_check.result_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found.")
        
    db.query(
        "MATCH (a:Activity {id: $aid}), (t:Tag {id: $tid}) "
        "MERGE (a)-[:HAS_TAG]->(t)",
        {"aid": activity_id, "tid": body.tag_id}
    )
    return {"message": "Tag added successfully."}

@router.get("/categories/{category_id}/activities")
def get_activities_by_category(category_id: str, db: Any = Depends(get_db)) -> list[dict]:
    """Retrieve all activities belonging to a specific category."""
    cat_check = db.query("MATCH (c:Category {id: $id}) RETURN c", {"id": category_id})
    if not cat_check.result_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
        
    result = db.query(
        "MATCH (a:Activity)-[:BELONGS_TO]->(c:Category {id: $cid}) "
        "RETURN a",
        {"cid": category_id}
    )
    return [dict(row[0].properties) for row in result.result_set]
