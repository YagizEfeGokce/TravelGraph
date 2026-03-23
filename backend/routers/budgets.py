"""Budgets routes: create, read, and update budget plans for itineraries."""
from __future__ import annotations

from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from core.dependencies import get_current_user
from db.connection import get_db
from models.budget import BudgetPlanCreate, BudgetPlanResponse

router = APIRouter(tags=["budgets"])

@router.post("/itineraries/{itinerary_id}/budget", status_code=status.HTTP_201_CREATED, response_model=BudgetPlanResponse)
def create_budget(
    itinerary_id: str,
    body: BudgetPlanCreate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> dict:
    """Create a budget plan for an itinerary. Only the owner can create it."""
    res = db.query(
        "MATCH (u:User {id: $uid})-[:CREATED]->(i:Itinerary {id: $iid}) RETURN i",
        {"uid": current_user["id"], "iid": itinerary_id}
    )
    if not res.result_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Itinerary not found or access denied")
        
    # Check if budget already exists
    res_b = db.query(
        "MATCH (i:Itinerary {id: $iid})-[:HAS_BUDGET]->(b:BudgetPlan) RETURN b",
        {"iid": itinerary_id}
    )
    if res_b.result_set:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Budget plan already exists for this itinerary")

    budget_id = str(uuid4())
    
    db.query(
        "MATCH (i:Itinerary {id: $iid}) "
        "CREATE (b:BudgetPlan {id: $id, total_budget: $tb, currency: $curr, hotel_budget: $hb, "
        "food_budget: $fb, transport_budget: $trb, activity_budget: $ab}) "
        "CREATE (i)-[:HAS_BUDGET]->(b)",
        {
            "iid": itinerary_id,
            "id": budget_id,
            "tb": body.total_budget,
            "curr": body.currency,
            "hb": body.hotel_budget,
            "fb": body.food_budget,
            "trb": body.transport_budget,
            "ab": body.activity_budget
        }
    )
    
    response_data = body.model_dump()
    response_data["id"] = budget_id
    response_data["itinerary_id"] = itinerary_id
    return response_data

@router.get("/itineraries/{itinerary_id}/budget", response_model=BudgetPlanResponse)
def get_budget(
    itinerary_id: str,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> dict:
    """Get the budget plan for an itinerary. Only the owner can view it."""
    res = db.query(
        "MATCH (u:User {id: $uid})-[:CREATED]->(i:Itinerary {id: $iid})-[:HAS_BUDGET]->(b:BudgetPlan) RETURN b",
        {"uid": current_user["id"], "iid": itinerary_id}
    )
    if not res.result_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget plan not found or access denied")
        
    props = dict(res.result_set[0][0].properties)
    props["itinerary_id"] = itinerary_id
    return props

@router.put("/itineraries/{itinerary_id}/budget", response_model=BudgetPlanResponse)
def update_budget(
    itinerary_id: str,
    body: BudgetPlanCreate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> dict:
    """Update the budget plan for an itinerary. Only the owner can update it."""
    res = db.query(
        "MATCH (u:User {id: $uid})-[:CREATED]->(i:Itinerary {id: $iid})-[:HAS_BUDGET]->(b:BudgetPlan) RETURN b",
        {"uid": current_user["id"], "iid": itinerary_id}
    )
    if not res.result_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget plan not found or access denied")
        
    budget_node = res.result_set[0][0]
    budget_id = budget_node.properties["id"]
    
    db.query(
        "MATCH (b:BudgetPlan {id: $id}) "
        "SET b.total_budget = $tb, b.currency = $curr, b.hotel_budget = $hb, "
        "b.food_budget = $fb, b.transport_budget = $trb, b.activity_budget = $ab",
        {
            "id": budget_id,
            "tb": body.total_budget,
            "curr": body.currency,
            "hb": body.hotel_budget,
            "fb": body.food_budget,
            "trb": body.transport_budget,
            "ab": body.activity_budget
        }
    )
    
    response_data = body.model_dump()
    response_data["id"] = budget_id
    response_data["itinerary_id"] = itinerary_id
    return response_data
