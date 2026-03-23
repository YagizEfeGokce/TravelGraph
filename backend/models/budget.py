"""Pydantic v2 schemas for BudgetPlan entities."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, field_validator, model_validator


Currency = Literal["EUR", "USD", "TRY"]


class BudgetPlanCreate(BaseModel):
    """Payload accepted when creating a budget plan for an itinerary."""

    total_budget: float
    currency: Currency
    hotel_budget: float
    food_budget: float
    transport_budget: float
    activity_budget: float

    @field_validator("total_budget")
    @classmethod
    def validate_total(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("total_budget must be greater than 0")
        return v

    @model_validator(mode="after")
    def validate_line_items(self) -> "BudgetPlanCreate":
        items = {
            "hotel_budget": self.hotel_budget,
            "food_budget": self.food_budget,
            "transport_budget": self.transport_budget,
            "activity_budget": self.activity_budget,
        }
        for name, value in items.items():
            if value < 0:
                raise ValueError(f"{name} must be greater than or equal to 0")

        total_items = sum(items.values())
        if total_items > self.total_budget:
            raise ValueError(
                f"Sum of budget items ({total_items}) exceeds total_budget ({self.total_budget})"
            )
        return self


class BudgetPlanResponse(BudgetPlanCreate):
    """Budget plan data returned in API responses."""

    id: str
    itinerary_id: str

    @classmethod
    def from_node(cls, properties: dict[str, Any]) -> "BudgetPlanResponse":
        """Build a BudgetPlanResponse from a FalkorDB node's properties dict."""
        return cls(**{k: properties[k] for k in cls.model_fields})
