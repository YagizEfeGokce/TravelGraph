"""Recommendation engine: graph-powered destination suggestions and route finding.

Three strategies are implemented:

1. **Budget + category match** — finds destinations whose activities share categories
   with a user's travel history, filtered by accommodation price.
2. **Collaborative filtering** — finds destinations visited by users with similar
   taste (shared visited destinations).
3. **Shortest path** — uses FalkorDB's ``shortestPath`` to find the fewest-hop
   connection between two destinations via ``CONNECTED_BY`` edges.
"""

from typing import Any

from models.destination import DestinationResponse

# ── Internal query helpers ─────────────────────────────────────────────────────


def _props(node: Any) -> dict:
    """Safely extract a property dict from a FalkorDB Node."""
    return node.properties if hasattr(node, "properties") else dict(node)


def _budget_category_query(
    db: Any,
    current_id: str,
    max_price: float,
    user_id: str | None,
    season: str | None,
) -> list[tuple[DestinationResponse, int]]:
    """Run the budget + category + (optional) season recommendation query.

    When *user_id* is provided the query anchors category matching through the
    user's visited destinations so only relevant categories are considered.
    When omitted it falls back to a simple category-diversity query.

    Returns:
        List of ``(DestinationResponse, category_match_score)`` tuples.
    """
    if user_id:
        # Category-match via user visit history
        cypher = (
            "MATCH (u:User {id: $user_id})-[:VISITED]->(visited:Destination)"
            "\nMATCH (visited)<-[:LOCATED_IN]-(a:Activity)-[:IN_CATEGORY]->(c:Category)"
            "\nMATCH (d:Destination)<-[:LOCATED_IN]-(a2:Activity)-[:IN_CATEGORY]->(c)"
            "\nMATCH (d)<-[:LOCATED_IN]-(acc:Accommodation)"
            "\nWHERE d.id <> $current_id"
            "\n  AND NOT (u)-[:VISITED]->(d)"
            "\n  AND acc.price_per_night <= $max_price"
        )
        params: dict[str, Any] = {
            "user_id": user_id,
            "current_id": current_id,
            "max_price": max_price,
        }
    else:
        # Fallback: category diversity without user context
        cypher = (
            "MATCH (d:Destination)<-[:LOCATED_IN]-(a:Activity)"
            "-[:IN_CATEGORY]->(c:Category)"
            "\nMATCH (d)<-[:LOCATED_IN]-(acc:Accommodation)"
            "\nWHERE d.id <> $current_id"
            "\n  AND acc.price_per_night <= $max_price"
        )
        params = {"current_id": current_id, "max_price": max_price}

    if season:
        cypher += "\n  AND EXISTS { MATCH (d)-[:BEST_IN]->(:Season {name: $season}) }"
        params["season"] = season

    cypher += (
        "\nWITH d, count(DISTINCT c) AS category_match, avg(acc.price_per_night) AS avg_price"
        "\nRETURN d, category_match, avg_price"
        "\nORDER BY category_match DESC LIMIT 5"
    )

    result = db.query(cypher, params)
    out: list[tuple[DestinationResponse, int]] = []
    for row in result.result_set:
        dest = DestinationResponse.from_node(_props(row[0]))
        category_match: int = int(row[1]) if row[1] is not None else 0
        out.append((dest, category_match))
    return out


def _collaborative_query(
    db: Any,
    user_id: str,
    current_id: str,
) -> list[tuple[DestinationResponse, int]]:
    """Run the collaborative-filtering recommendation query.

    Finds destinations visited by users who share at least one visited
    destination with *user_id*, ordered by the number of similar users.

    Returns:
        List of ``(DestinationResponse, overlap_score)`` tuples.
    """
    result = db.query(
        "MATCH (u:User {id: $user_id})-[:VISITED]->(d:Destination)"
        "\n      <-[:VISITED]-(similar:User)-[:VISITED]->(rec:Destination)"
        "\nWHERE NOT (u)-[:VISITED]->(rec)"
        "\n  AND rec.id <> $current_id"
        "\nRETURN rec, count(similar) AS overlap"
        "\nORDER BY overlap DESC LIMIT 5",
        {"user_id": user_id, "current_id": current_id},
    )
    out: list[tuple[DestinationResponse, int]] = []
    for row in result.result_set:
        dest = DestinationResponse.from_node(_props(row[0]))
        overlap: int = int(row[1]) if row[1] is not None else 0
        out.append((dest, overlap))
    return out


# ── Public API ────────────────────────────────────────────────────────────────


def recommend(
    db: Any,
    current_id: str,
    max_price: float = 500.0,
    user_id: str | None = None,
    season: str | None = None,
) -> list[DestinationResponse]:
    """Return up to 5 recommended destinations for *current_id*.

    Scoring strategy:
    - Each destination starts with its ``category_match`` score.
    - If *user_id* is provided, collaborative overlap adds ``overlap * 2`` bonus
      (weighted higher because it reflects real user behaviour).
    - Destinations that appear in both result sets get a combined score.
    - Final list is sorted descending by combined score.

    Args:
        db: FalkorDB graph instance (from ``get_db`` dependency).
        current_id: The destination the user is currently viewing.
        max_price: Upper bound for accommodation price per night.
        user_id: Optional — enables personalised recommendations.
        season: Optional — filters results to destinations best visited in this season.

    Returns:
        Up to 5 ``DestinationResponse`` objects ordered by relevance.
    """
    # id → (DestinationResponse, score)
    scored: dict[str, tuple[DestinationResponse, int]] = {}

    # 1. Budget + category (always executed)
    for dest, cat_score in _budget_category_query(db, current_id, max_price, user_id, season):
        scored[dest.id] = (dest, cat_score)

    # 2. Collaborative filtering (only when user_id is available)
    if user_id:
        for dest, overlap in _collaborative_query(db, user_id, current_id):
            if dest.id in scored:
                existing_dest, existing_score = scored[dest.id]
                scored[dest.id] = (existing_dest, existing_score + overlap * 2)
            else:
                scored[dest.id] = (dest, overlap * 2)

    sorted_results = sorted(scored.values(), key=lambda pair: pair[1], reverse=True)
    return [dest for dest, _ in sorted_results[:5]]


def find_route(
    db: Any,
    from_id: str,
    to_id: str,
) -> dict:
    """Find the shortest path between two destinations via CONNECTED_BY edges.

    Uses FalkorDB's built-in ``shortestPath`` function which explores
    ``CONNECTED_BY`` relationships (created when Transport nodes link cities).

    Returns a dict with:
    - ``hops``: number of relationship hops (-1 if no path exists).
    - ``nodes``: ordered list of ``{"id": ..., "name": ..., "type": ...}`` dicts
      representing every node in the path (Destination and Transport nodes).

    Args:
        db: FalkorDB graph instance.
        from_id: Source Destination node id.
        to_id: Target Destination node id.
    """
    result = db.query(
        "MATCH (a:Destination {id: $from_id}), (b:Destination {id: $to_id})"
        "\nRETURN shortestPath((a)-[:CONNECTED_BY*]->(b)) AS path",
        {"from_id": from_id, "to_id": to_id},
    )

    if not result.result_set:
        return {"hops": -1, "nodes": []}

    row = result.result_set[0]
    path = row[0]

    # path is None when no CONNECTED_BY edges exist between the two nodes
    if path is None:
        return {"hops": -1, "nodes": []}

    hops: int = -1

    # Extract nodes from the path object — FalkorDB Path API varies by version
    nodes: list[dict] = []
    try:
        path_nodes = path.nodes() if callable(getattr(path, "nodes", None)) else path.nodes
        for node in path_nodes:
            props = _props(node)
            nodes.append({
                "id": props.get("id", ""),
                "name": props.get("name", ""),
                "type": list(node.labels)[0] if hasattr(node, "labels") and node.labels else "Unknown",
            })
        hops = max(len(nodes) - 1, 0)
    except Exception:  # noqa: BLE001 — gracefully handle unexpected path shapes
        nodes = []

    return {"hops": hops, "nodes": nodes}
