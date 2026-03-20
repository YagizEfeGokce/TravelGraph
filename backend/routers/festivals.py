"""Festivals routes: list all festivals across Turkey with optional city filter."""

from typing import Any

from fastapi import APIRouter, Depends, Query

from core.dependencies import get_optional_user
from db.connection import get_db

router = APIRouter(prefix="/festivals", tags=["festivals"])


@router.get("")
def list_festivals(
    city: str | None = Query(default=None),
    db: Any = Depends(get_db),
    _user: dict | None = Depends(get_optional_user),
) -> list[dict]:
    """Return all festivals. Optionally filter by city name (case-insensitive contains)."""
    if city:
        result = db.query(
            "MATCH (d:Destination)-[:HAS_FESTIVAL]->(f:Festival)"
            " WHERE toLower(d.name) CONTAINS toLower($city)"
            " RETURN f, d.name AS city_name"
            " ORDER BY f.start_date ASC",
            {"city": city},
        )
    else:
        result = db.query(
            "MATCH (d:Destination)-[:HAS_FESTIVAL]->(f:Festival)"
            " RETURN f, d.name AS city_name"
            " ORDER BY f.start_date ASC",
            {},
        )
    festivals = []
    for row in result.result_set:
        props = dict(row[0].properties)
        props["city"] = row[1]
        festivals.append(props)
    return festivals
