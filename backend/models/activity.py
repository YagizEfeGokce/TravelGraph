"""Pydantic v2 schemas for Activity entities."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, field_validator


class ActivityBase(BaseModel):
    """Shared fields present on every activity representation."""

    name: str
    description: str
    duration_hours: float
    price: float
    address: str

    @field_validator("duration_hours")
    @classmethod
    def validate_duration(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("duration_hours must be greater than 0")
        return v

    @field_validator("price")
    @classmethod
    def validate_price(cls, v: float) -> float:
        if v < 0:
            raise ValueError("price must be greater than or equal to 0")
        return v


class ActivityCreate(ActivityBase):
    """Payload accepted when creating a new activity.

    ``destination_id`` links the activity to an existing Destination node.
    """

    destination_id: str


class ActivityResponse(BaseModel):
    """Activity data returned in API responses."""

    id: str
    name: str
    description: str
    duration_hours: float
    price: float
    address: str
    destination_id: str
    categories: list[str] = []
    tags: list[str] = []

    @classmethod
    def from_node(cls, properties: dict[str, Any]) -> "ActivityResponse":
        """Build an ActivityResponse from a FalkorDB node's properties dict."""
        return cls(
            id=properties["id"],
            name=properties["name"],
            description=properties["description"],
            duration_hours=properties["duration_hours"],
            price=properties["price"],
            address=properties["address"],
            destination_id=properties["destination_id"],
            categories=properties.get("categories") or [],
            tags=properties.get("tags") or [],
        )
