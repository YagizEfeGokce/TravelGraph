"""Itinerary routes: create, list, detail, delete, and stop management."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Body, Depends, HTTPException, Response, status

from core.dependencies import get_current_user, get_optional_user
from db.connection import get_db
from models.itinerary import ItineraryCreate, ItineraryResponse
from models.itinerary_stop import ItineraryStopCreate, ItineraryStopResponse

router = APIRouter(prefix="/itineraries", tags=["itineraries"])


# ── Helpers ────────────────────────────────────────────────────────────────────

def _get_itinerary_props(db: Any, itinerary_id: str) -> tuple[dict, str]:
    """Return (node_properties, owner_user_id) or raise HTTP 404."""
    result = db.query(
        "MATCH (u:User)-[:CREATED]->(i:Itinerary {id: $id}) RETURN i, u.id AS uid",
        {"id": itinerary_id},
    )
    if not result.result_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Itinerary '{itinerary_id}' not found",
        )
    row = result.result_set[0]
    return row[0].properties, row[1]


def _require_owner(owner_id: str, current_user: dict) -> None:
    """Raise HTTP 403 if *current_user* is not the itinerary owner."""
    if current_user["id"] != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify this itinerary",
        )


def _load_stops(db: Any, itinerary_id: str) -> list[dict]:
    """Return all stops for *itinerary_id* ordered by day_number then order."""
    result = db.query(
        "MATCH (i:Itinerary {id: $iid})-[:HAS_STOP]->(s:ItineraryStop)-[:AT]->(d:Destination)"
        "\nRETURN s, d.name AS dest_name"
        "\nORDER BY s.day_number ASC, s.order ASC",
        {"iid": itinerary_id},
    )
    return [
        ItineraryStopResponse.from_node(row[0].properties, row[1]).model_dump()
        for row in result.result_set
    ]


def _build_itinerary_response(
    props: dict, owner_id: str, db: Any
) -> ItineraryResponse:
    stops = _load_stops(db, props["id"])
    return ItineraryResponse.from_node(props, user_id=owner_id, stops=stops)


# ── Itinerary endpoints ────────────────────────────────────────────────────────

@router.post("", response_model=ItineraryResponse, status_code=status.HTTP_201_CREATED)
def create_itinerary(
    body: ItineraryCreate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> ItineraryResponse:
    """Create a new itinerary owned by the authenticated user."""
    itinerary_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    result = db.query(
        "MATCH (u:User {id: $uid})"
        "\nCREATE (i:Itinerary {"
        "id: $id, title: $title, start_date: $start_date, end_date: $end_date,"
        " is_public: $is_public, created_at: $ca"
        "})"
        "\nCREATE (u)-[:CREATED]->(i)"
        "\nRETURN i",
        {
            "uid": current_user["id"],
            "id": itinerary_id,
            "title": body.title,
            "start_date": body.start_date.isoformat(),
            "end_date": body.end_date.isoformat(),
            "is_public": body.is_public,
            "ca": created_at,
        },
    )
    props = result.result_set[0][0].properties
    return ItineraryResponse.from_node(props, user_id=current_user["id"])


@router.get("", response_model=list[ItineraryResponse])
def list_itineraries(
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> list[ItineraryResponse]:
    """Return all itineraries created by the authenticated user."""
    result = db.query(
        "MATCH (u:User {id: $uid})-[:CREATED]->(i:Itinerary)"
        "\nRETURN i ORDER BY i.start_date ASC",
        {"uid": current_user["id"]},
    )
    return [
        _build_itinerary_response(row[0].properties, current_user["id"], db)
        for row in result.result_set
    ]


@router.get("/{itinerary_id}", response_model=ItineraryResponse)
def get_itinerary(
    itinerary_id: str,
    db: Any = Depends(get_db),
    current_user: dict | None = Depends(get_optional_user),
) -> ItineraryResponse:
    """Return a single itinerary.

    - The owner always has access.
    - Other users (authenticated or not) may only see public itineraries.
    """
    props, owner_id = _get_itinerary_props(db, itinerary_id)

    is_owner = current_user is not None and current_user["id"] == owner_id
    if not is_owner and not props.get("is_public", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This itinerary is private",
        )

    return _build_itinerary_response(props, owner_id, db)


@router.delete("/{itinerary_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_itinerary(
    itinerary_id: str,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> Response:
    """Delete an itinerary and all its stops.  Only the owner may delete."""
    props, owner_id = _get_itinerary_props(db, itinerary_id)
    _require_owner(owner_id, current_user)

    db.query(
        "MATCH (i:Itinerary {id: $id})"
        "\nOPTIONAL MATCH (i)-[:HAS_STOP]->(s:ItineraryStop)"
        "\nDETACH DELETE i, s",
        {"id": itinerary_id},
    )
    return Response(status_code=204)


# ── Stop endpoints ─────────────────────────────────────────────────────────────

@router.post(
    "/{itinerary_id}/stops",
    response_model=ItineraryStopResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_stop(
    itinerary_id: str,
    body: ItineraryStopCreate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> ItineraryStopResponse:
    """Add a stop to an itinerary.  Only the owner may add stops."""
    props, owner_id = _get_itinerary_props(db, itinerary_id)
    _require_owner(owner_id, current_user)

    # Verify destination exists
    dest_result = db.query(
        "MATCH (d:Destination {id: $dest_id}) RETURN d.name AS name",
        {"dest_id": body.destination_id},
    )
    if not dest_result.result_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Destination '{body.destination_id}' not found",
        )
    dest_name: str = dest_result.result_set[0][0]

    stop_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    result = db.query(
        "MATCH (i:Itinerary {id: $iid}), (d:Destination {id: $dest_id})"
        "\nCREATE (s:ItineraryStop {"
        "id: $id, destination_id: $dest_id,"
        " day_number: $day_number, order: $order, notes: $notes, created_at: $ca"
        "})"
        "\nCREATE (i)-[:HAS_STOP]->(s)"
        "\nCREATE (s)-[:AT]->(d)"
        "\nRETURN s",
        {
            "iid": itinerary_id,
            "dest_id": body.destination_id,
            "id": stop_id,
            "day_number": body.day_number,
            "order": body.order,
            "notes": body.notes,
            "ca": created_at,
        },
    )
    stop_props = result.result_set[0][0].properties
    return ItineraryStopResponse.from_node(stop_props, destination_name=dest_name)


@router.get("/{itinerary_id}/stops", response_model=list[ItineraryStopResponse])
def list_stops(
    itinerary_id: str,
    db: Any = Depends(get_db),
    current_user: dict | None = Depends(get_optional_user),
) -> list[ItineraryStopResponse]:
    """Return all stops for an itinerary, ordered by day_number then order.

    Public itineraries are visible to everyone.  Private ones require ownership.
    """
    props, owner_id = _get_itinerary_props(db, itinerary_id)

    is_owner = current_user is not None and current_user["id"] == owner_id
    if not is_owner and not props.get("is_public", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This itinerary is private",
        )

    result = db.query(
        "MATCH (i:Itinerary {id: $iid})-[:HAS_STOP]->(s:ItineraryStop)-[:AT]->(d:Destination)"
        "\nRETURN s, d.name AS dest_name"
        "\nORDER BY s.day_number ASC, s.order ASC",
        {"iid": itinerary_id},
    )
    return [
        ItineraryStopResponse.from_node(row[0].properties, row[1])
        for row in result.result_set
    ]


@router.delete(
    "/{itinerary_id}/stops/{stop_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_stop(
    itinerary_id: str,
    stop_id: str,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> Response:
    """Delete a single stop from an itinerary.  Only the owner may delete."""
    _, owner_id = _get_itinerary_props(db, itinerary_id)
    _require_owner(owner_id, current_user)

    result = db.query(
        "MATCH (i:Itinerary {id: $iid})-[:HAS_STOP]->(s:ItineraryStop {id: $sid})"
        "\nRETURN s",
        {"iid": itinerary_id, "sid": stop_id},
    )
    if not result.result_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stop '{stop_id}' not found in itinerary '{itinerary_id}'",
        )

    db.query(
        "MATCH (i:Itinerary {id: $iid})-[:HAS_STOP]->(s:ItineraryStop {id: $sid})"
        "\nDETACH DELETE s",
        {"iid": itinerary_id, "sid": stop_id},
    )
    return Response(status_code=204)


@router.put("/{itinerary_id}/stops/{stop_id}/reorder")
def reorder_stop(
    itinerary_id: str,
    stop_id: str,
    new_order: int = Body(..., ge=1, embed=True),
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Update the ``order`` value of a stop within its day.  Only the owner may reorder."""
    _, owner_id = _get_itinerary_props(db, itinerary_id)
    _require_owner(owner_id, current_user)

    result = db.query(
        "MATCH (i:Itinerary {id: $iid})-[:HAS_STOP]->(s:ItineraryStop {id: $sid})"
        "\nSET s.order = $new_order"
        "\nRETURN s",
        {"iid": itinerary_id, "sid": stop_id, "new_order": new_order},
    )
    if not result.result_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stop '{stop_id}' not found in itinerary '{itinerary_id}'",
        )

    stop_props = result.result_set[0][0].properties

    # Fetch destination name for the response
    dest_result = db.query(
        "MATCH (s:ItineraryStop {id: $sid})-[:AT]->(d:Destination) RETURN d.name",
        {"sid": stop_id},
    )
    dest_name: str = dest_result.result_set[0][0] if dest_result.result_set else ""

    return ItineraryStopResponse.from_node(stop_props, destination_name=dest_name).model_dump()
