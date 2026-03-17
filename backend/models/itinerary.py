"""Pydantic v2 schemas for Itinerary entities."""

from datetime import date
from typing import Any

from pydantic import BaseModel, model_validator

from models.budget import BudgetPlanResponse


class ItineraryBase(BaseModel):
    """Shared fields present on every itinerary representation."""

    title: str
    start_date: date
    end_date: date
    is_public: bool

    @model_validator(mode="after")
    def validate_date_range(self) -> "ItineraryBase":
        if self.start_date >= self.end_date:
            raise ValueError("start_date must be before end_date")
        return self


class ItineraryCreate(ItineraryBase):
    """Payload accepted when creating a new itinerary."""


class ItineraryResponse(ItineraryBase):
    """Itinerary data returned in API responses."""

    id: str
    user_id: str
    stops: list[dict] = []
    budget: BudgetPlanResponse | None = None

    @classmethod
    def from_node(
        cls,
        properties: dict[str, Any],
        user_id: str,
        stops: list[dict] | None = None,
        budget: BudgetPlanResponse | None = None,
    ) -> "ItineraryResponse":
        """Build an ItineraryResponse from a FalkorDB node's properties dict."""
        return cls(
            id=properties["id"],
            title=properties["title"],
            start_date=date.fromisoformat(properties["start_date"]),
            end_date=date.fromisoformat(properties["end_date"]),
            is_public=properties["is_public"],
            user_id=user_id,
            stops=stops or [],
            budget=budget,
        )
