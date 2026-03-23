"""Pydantic v2 schemas for Restaurant entities."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, field_validator


PriceRange = Literal["budget", "mid", "luxury"]


class RestaurantBase(BaseModel):
    """Shared fields present on every restaurant representation."""

    name: str
    cuisine_type: str
    price_range: PriceRange
    address: str
    rating: float | None = None

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, v: float | None) -> float | None:
        if v is not None and not 1.0 <= v <= 5.0:
            raise ValueError("rating must be between 1 and 5")
        return v


class RestaurantCreate(RestaurantBase):
    """Payload accepted when creating a new restaurant."""

    destination_id: str


class RestaurantResponse(RestaurantBase):
    """Restaurant data returned in API responses."""

    id: str
    destination_id: str

    @classmethod
    def from_node(cls, properties: dict[str, Any]) -> "RestaurantResponse":
        """Build a RestaurantResponse from a FalkorDB node's properties dict."""
        return cls(**{k: properties[k] for k in cls.model_fields})
