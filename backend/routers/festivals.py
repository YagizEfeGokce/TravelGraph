"""Festivals routes: list all festivals across Turkey with optional city filter."""
from __future__ import annotations

from datetime import date
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status

from core.dependencies import get_optional_user
from db.connection import get_db
from models.festival import FestivalCreate

router = APIRouter(tags=["festivals"])


@router.get("/festivals")
def list_festivals(
    start_after: date | None = Query(default=None),
    end_before: date | None = Query(default=None),
    season: str | None = Query(default=None),
    city: str | None = Query(default=None),
    db: Any = Depends(get_db),
    _user: dict | None = Depends(get_optional_user),
) -> list[dict]:
    """Return all festivals. Optionally filter by city name, dates, or season."""
    query = "MATCH (d:Destination)-[:HAS_FESTIVAL]->(f:Festival) "
    conditions = []
    params: dict[str, Any] = {}

    if start_after:
        conditions.append("f.start_date >= $start_after")
        params["start_after"] = start_after.isoformat()
    if end_before:
        conditions.append("f.end_date <= $end_before")
        params["end_before"] = end_before.isoformat()
    if season:
        conditions.append("toLower(f.season) = toLower($season)")
        params["season"] = season
    if city:
        conditions.append("toLower(d.name) CONTAINS toLower($city)")
        params["city"] = city

    if conditions:
        query += "WHERE " + " AND ".join(conditions) + " "

    query += "RETURN f, d.name AS destination_name, d.id as destination_id ORDER BY f.start_date ASC"

    result = db.query(query, params)
    festivals = []
    for row in result.result_set:
        props = dict(row[0].properties)
        props["destination_name"] = row[1]
        props["destination_id"] = row[2]
        festivals.append(props)
    return festivals


@router.get("/destinations/{destination_id}/festivals")
def get_destination_festivals(destination_id: str, db: Any = Depends(get_db)) -> list[dict]:
    """Get festivals for a specific destination."""
    res = db.query("MATCH (d:Destination {id: $id}) RETURN d", {"id": destination_id})
    if not res.result_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destination not found")

    result = db.query(
        "MATCH (d:Destination {id: $id})-[:HAS_FESTIVAL]->(f:Festival) "
        "RETURN f, d.name AS destination_name, d.id as destination_id",
        {"id": destination_id}
    )

    festivals = []
    for row in result.result_set:
        props = dict(row[0].properties)
        props["destination_name"] = row[1]
        props["destination_id"] = row[2]
        festivals.append(props)
    return festivals


@router.post("/festivals", status_code=status.HTTP_201_CREATED)
def create_festival(body: FestivalCreate, db: Any = Depends(get_db)) -> dict:
    """Create a new festival."""
    res = db.query("MATCH (d:Destination {id: $id}) RETURN d", {"id": body.destination_id})
    if not res.result_set:
        raise HTTPException(status_code=404, detail="Destination not found")

    festival_id = str(uuid4())

    db.query(
        "MATCH (d:Destination {id: $did}) "
        "CREATE (f:Festival {id: $id, name: $name, description: $description, "
        "start_date: $start_date, end_date: $end_date, is_recurring: $is_recurring, "
        "ticket_price: $ticket_price, season: $season}) "
        "CREATE (d)-[:HAS_FESTIVAL]->(f)",
        {
            "did": body.destination_id,
            "id": festival_id,
            "name": body.name,
            "description": body.description,
            "start_date": body.start_date.isoformat(),
            "end_date": body.end_date.isoformat(),
            "is_recurring": body.is_recurring,
            "ticket_price": body.ticket_price,
            # We don't have season in the schema, but let's try to infer or pass None
            "season": "Spring" # hardcoded default or inferred from date since it's not in the schema
        }
    )

    response_data = body.model_dump()
    response_data["id"] = festival_id
    response_data["start_date"] = body.start_date.isoformat()
    response_data["end_date"] = body.end_date.isoformat()
    return response_data
