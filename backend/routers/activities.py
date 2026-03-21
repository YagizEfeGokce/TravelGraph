"""Activity routes: listing with filters and creation."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status

from core.dependencies import get_current_user, get_optional_user
from db.connection import get_db
from models.activity import ActivityCreate, ActivityResponse

router = APIRouter(prefix="/activities", tags=["activities"])


# ── Helpers ────────────────────────────────────────────────────────────────────

def _build_activity_list_query(
    destination_id: str | None,
    category: str | None,
    tag: str | None,
) -> tuple[str, dict]:
    """Construct a parameterised Cypher query from optional activity filters.

    Structural query parts are string literals; all user-supplied values are
    passed as parameters.
    """
    params: dict[str, Any] = {}
    conditions: list[str] = []

    query = "MATCH (a:Activity)"

    if category:
        query += "\nMATCH (a)-[:IN_CATEGORY]->(:Category {name: $category})"
        params["category"] = category

    if destination_id:
        conditions.append("a.destination_id = $destination_id")
        params["destination_id"] = destination_id

    if tag:
        conditions.append("$tag IN a.tags")
        params["tag"] = tag

    if conditions:
        query += "\nWHERE " + " AND ".join(conditions)

    query += "\nRETURN DISTINCT a"
    return query, params


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.get("", response_model=list[ActivityResponse])
def list_activities(
    destination_id: str | None = Query(default=None),
    category: str | None = Query(default=None),
    tag: str | None = Query(default=None),
    db: Any = Depends(get_db),
    _user: dict | None = Depends(get_optional_user),
) -> list[ActivityResponse]:
    """Return activities, optionally filtered by destination, category, or tag."""
    query, params = _build_activity_list_query(destination_id, category, tag)
    result = db.query(query, params)
    return [ActivityResponse.from_node(row[0].properties) for row in result.result_set]


@router.post("", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
def create_activity(
    body: ActivityCreate,
    db: Any = Depends(get_db),
    _user: dict = Depends(get_current_user),
) -> ActivityResponse:
    """Create a new activity and link it to the given destination.

    Raises HTTP 404 if the destination does not exist.
    """
    dest_check = db.query(
        "MATCH (d:Destination {id: $id}) RETURN d",
        {"id": body.destination_id},
    )
    if not dest_check.result_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Destination '{body.destination_id}' not found",
        )

    activity_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    result = db.query(
        "MATCH (d:Destination {id: $destination_id})"
        "\nCREATE (a:Activity {"
        "id: $id, name: $name, description: $description, "
        "duration_hours: $duration_hours, price: $price, address: $address, "
        "destination_id: $destination_id, categories: [], tags: [], created_at: $ca"
        "})"
        "\nCREATE (d)-[:HAS_ACTIVITY]->(a)"
        "\nRETURN a",
        {
            "id": activity_id,
            "name": body.name,
            "description": body.description,
            "duration_hours": body.duration_hours,
            "price": body.price,
            "address": body.address,
            "destination_id": body.destination_id,
            "ca": created_at,
        },
    )
    return ActivityResponse.from_node(result.result_set[0][0].properties)
