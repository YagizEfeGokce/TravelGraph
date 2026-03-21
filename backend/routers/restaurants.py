"""Restaurants routes."""
from __future__ import annotations

from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status

from db.connection import get_db
from models.restaurant import RestaurantCreate, RestaurantResponse

router = APIRouter(tags=["restaurants"])

@router.post("/restaurants", status_code=status.HTTP_201_CREATED)
def create_restaurant(body: RestaurantCreate, db: Any = Depends(get_db)) -> dict:
    """Create a new restaurant."""
    res = db.query("MATCH (d:Destination {id: $id}) RETURN d", {"id": body.destination_id})
    if not res.result_set:
        raise HTTPException(status_code=404, detail="Destination not found")
        
    restaurant_id = str(uuid4())
    
    db.query(
        "MATCH (d:Destination {id: $did}) "
        "CREATE (r:Restaurant {id: $id, name: $name, cuisine_type: $cuisine_type, price_range: $price_range, address: $address, rating: $rating}) "
        "CREATE (d)-[:HAS_RESTAURANT]->(r)",
        {
            "did": body.destination_id,
            "id": restaurant_id,
            "name": body.name,
            "cuisine_type": body.cuisine_type,
            "price_range": body.price_range,
            "address": body.address,
            "rating": body.rating
        }
    )
    response_data = body.model_dump()
    response_data["id"] = restaurant_id
    return response_data

@router.get("/restaurants", response_model=list[RestaurantResponse])
def get_restaurants(
    cuisine_type: str | None = Query(default=None),
    price_range: str | None = Query(default=None),
    db: Any = Depends(get_db),
) -> list[dict]:
    """Get all restaurants, optionally filtered."""
    query = "MATCH (d:Destination)-[:HAS_RESTAURANT]->(r:Restaurant) "
    conditions = []
    params: dict[str, Any] = {}
    
    if cuisine_type:
        conditions.append("toLower(r.cuisine_type) CONTAINS toLower($cuisine)")
        params["cuisine"] = cuisine_type
    if price_range:
        conditions.append("r.price_range = $price")
        params["price"] = price_range
        
    if conditions:
        query += "WHERE " + " AND ".join(conditions) + " "
        
    query += "RETURN r, d.id as destination_id"
    
    result = db.query(query, params)
    
    restaurants = []
    for row in result.result_set:
        props = dict(row[0].properties)
        props["destination_id"] = row[1]
        restaurants.append(props)
        
    return restaurants

@router.get("/destinations/{destination_id}/restaurants", response_model=list[RestaurantResponse])
def get_destination_restaurants(destination_id: str, db: Any = Depends(get_db)) -> list[dict]:
    """Get restaurants for a specific destination."""
    res = db.query("MATCH (d:Destination {id: $id}) RETURN d", {"id": destination_id})
    if not res.result_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destination not found")
        
    result = db.query(
        "MATCH (d:Destination {id: $id})-[:HAS_RESTAURANT]->(r:Restaurant) RETURN r, d.id as destination_id",
        {"id": destination_id}
    )
    
    restaurants = []
    for row in result.result_set:
        props = dict(row[0].properties)
        props["destination_id"] = row[1]
        restaurants.append(props)
        
    return restaurants
