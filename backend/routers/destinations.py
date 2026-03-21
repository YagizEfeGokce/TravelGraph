"""Destination routes: listing, detail, sub-resources, recommendations, route, and creation."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status

from core.dependencies import get_current_user, get_optional_user
from db.connection import get_db
from models.destination import DestinationCreate, DestinationResponse
from services.recommendation import find_route, recommend

router = APIRouter(prefix="/destinations", tags=["destinations"])


# ── Helpers ────────────────────────────────────────────────────────────────────

def _get_destination_or_404(db: Any, destination_id: str) -> dict:
    """Return node properties for *destination_id*, raising HTTP 404 if not found."""
    result = db.query(
        "MATCH (d:Destination {id: $id}) RETURN d",
        {"id": destination_id},
    )
    if not result.result_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Destination '{destination_id}' not found",
        )
    return result.result_set[0][0].properties


def _build_list_query(
    country: str | None,
    category: str | None,
    season: str | None,
    min_rating: float | None,
    limit: int,
) -> tuple[str, dict]:
    """Construct a parameterised Cypher list query from optional filter values.

    Node values are always passed as parameters; only structural query parts
    (labels, relationship types) are concatenated as string literals.
    """
    params: dict[str, Any] = {"limit": limit}
    conditions: list[str] = []

    query = "MATCH (d:Destination)"

    if category:
        query += (
            "\nMATCH (d)<-[:LOCATED_IN]-(:Activity)"
            "-[:IN_CATEGORY]->(:Category {name: $category})"
        )
        params["category"] = category

    if country:
        conditions.append("d.country = $country")
        params["country"] = country

    if season:
        conditions.append(
            "EXISTS { MATCH (d)-[:BEST_IN]->(:Season {name: $season}) }"
        )
        params["season"] = season

    if min_rating is not None:
        conditions.append("d.avg_rating >= $min_rating")
        params["min_rating"] = min_rating

    if conditions:
        query += "\nWHERE " + " AND ".join(conditions)

    query += "\nRETURN DISTINCT d LIMIT $limit"
    return query, params


# ── Endpoints (fixed paths first, then parameterised) ─────────────────────────

@router.get("/route")
def destination_route(
    from_id: str = Query(alias="from"),
    to_id: str = Query(alias="to"),
    db: Any = Depends(get_db),
    _user: dict | None = Depends(get_optional_user),
) -> dict:
    """Find the shortest path between two destinations via CONNECTED_BY edges.

    Uses FalkorDB's ``shortestPath`` function traversing ``CONNECTED_BY``
    relationships (e.g. Transport nodes that link cities).

    Returns:
        ``hops``: number of relationship hops (-1 when no path exists).
        ``nodes``: ordered list of nodes (Destination + Transport) in the path.
    """
    _get_destination_or_404(db, from_id)
    _get_destination_or_404(db, to_id)
    return find_route(db, from_id, to_id)


@router.get("", response_model=list[DestinationResponse])
def list_destinations(
    country: str | None = Query(default=None),
    category: str | None = Query(default=None),
    season: str | None = Query(default=None),
    min_rating: float | None = Query(default=None, ge=0.0, le=5.0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Any = Depends(get_db),
    _user: dict | None = Depends(get_optional_user),
) -> list[DestinationResponse]:
    """Return a filtered list of destinations.

    All query parameters are optional.  Results are limited to *limit* (max 100).
    """
    query, params = _build_list_query(country, category, season, min_rating, limit)
    result = db.query(query, params)
    return [
        DestinationResponse.from_node(row[0].properties)
        for row in result.result_set
    ]


@router.post("", response_model=DestinationResponse, status_code=status.HTTP_201_CREATED)
def create_destination(
    body: DestinationCreate,
    db: Any = Depends(get_db),
    _user: dict = Depends(get_current_user),
) -> DestinationResponse:
    """Create a new destination node.  Requires authentication."""
    destination_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    result = db.query(
        "CREATE (d:Destination {"
        "id: $id, name: $name, country: $country, description: $description, "
        "lat: $lat, lng: $lng, created_at: $ca"
        "}) RETURN d",
        {
            "id": destination_id,
            "name": body.name,
            "country": body.country,
            "description": body.description,
            "lat": body.lat,
            "lng": body.lng,
            "ca": created_at,
        },
    )
    return DestinationResponse.from_node(result.result_set[0][0].properties)


@router.get("/{destination_id}", response_model=DestinationResponse)
def get_destination(
    destination_id: str,
    db: Any = Depends(get_db),
    _user: dict | None = Depends(get_optional_user),
) -> DestinationResponse:
    """Return a single destination with its computed average rating."""
    result = db.query(
        "MATCH (d:Destination {id: $id})"
        "\nOPTIONAL MATCH (d)<-[:RATES]-(r:Rating)"
        "\nRETURN d, avg(r.score) AS avg_rating",
        {"id": destination_id},
    )
    if not result.result_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Destination '{destination_id}' not found",
        )
    row = result.result_set[0]
    props = row[0].properties
    avg_rating: float | None = row[1] if row[1] is not None else None
    return DestinationResponse.from_node(props, avg_rating=avg_rating)


@router.get("/{destination_id}/activities")
def get_destination_activities(
    destination_id: str,
    db: Any = Depends(get_db),
    _user: dict | None = Depends(get_optional_user),
) -> list[dict]:
    """Return all activities belonging to the destination."""
    _get_destination_or_404(db, destination_id)

    result = db.query(
        "MATCH (d:Destination {id: $id})-[:HAS_ACTIVITY]->(a:Activity) RETURN a",
        {"id": destination_id},
    )
    return [row[0].properties for row in result.result_set]


@router.get("/{destination_id}/accommodations")
def get_destination_accommodations(
    destination_id: str,
    db: Any = Depends(get_db),
    _user: dict | None = Depends(get_optional_user),
) -> list[dict]:
    """Return all accommodations belonging to the destination."""
    _get_destination_or_404(db, destination_id)

    result = db.query(
        "MATCH (d:Destination {id: $id})-[:HAS_ACCOMMODATION]->(acc:Accommodation)"
        " RETURN acc",
        {"id": destination_id},
    )
    return [row[0].properties for row in result.result_set]


@router.get("/{destination_id}/restaurants")
def get_destination_restaurants(
    destination_id: str,
    db: Any = Depends(get_db),
    _user: dict | None = Depends(get_optional_user),
) -> list[dict]:
    """Return all restaurants belonging to the destination."""
    _get_destination_or_404(db, destination_id)

    result = db.query(
        "MATCH (d:Destination {id: $id})-[:HAS_RESTAURANT]->(r:Restaurant) RETURN r",
        {"id": destination_id},
    )
    return [row[0].properties for row in result.result_set]


@router.get("/{destination_id}/festivals")
def get_destination_festivals(
    destination_id: str,
    db: Any = Depends(get_db),
    _user: dict | None = Depends(get_optional_user),
) -> list[dict]:
    """Return all festivals belonging to the destination."""
    _get_destination_or_404(db, destination_id)

    result = db.query(
        "MATCH (d:Destination {id: $id})-[:HAS_FESTIVAL]->(f:Festival) RETURN f",
        {"id": destination_id},
    )
    return [row[0].properties for row in result.result_set]


@router.get("/{destination_id}/recommend", response_model=list[DestinationResponse])
def recommend_destinations(
    destination_id: str,
    user_id: str | None = Query(default=None),
    max_price: float = Query(default=500.0, ge=0.0),
    season: str | None = Query(default=None),
    db: Any = Depends(get_db),
    _user: dict | None = Depends(get_optional_user),
) -> list[DestinationResponse]:
    """Return up to 5 recommended destinations for *destination_id*.

    Recommendation strategy:
    - **Without** ``user_id``: budget + category diversity only.
    - **With** ``user_id``: personalised via user visit history (budget + category)
      merged with collaborative filtering (similar-user preferences).
      Results from both strategies are combined and scored, then the top 5 returned.

    Query params:
        user_id: Optional user id for personalised recommendations.
        max_price: Max accommodation price per night (default 500).
        season: Optional season name filter (Spring/Summer/Autumn/Winter).
    """
    _get_destination_or_404(db, destination_id)
    return recommend(
        db,
        current_id=destination_id,
        max_price=max_price,
        user_id=user_id,
        season=season,
    )
