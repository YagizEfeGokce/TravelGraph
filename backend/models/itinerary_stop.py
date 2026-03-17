"""Pydantic v2 schemas for ItineraryStop entities."""

from typing import Any

from pydantic import BaseModel, field_validator


class ItineraryStopCreate(BaseModel):
    """Payload accepted when adding a stop to an itinerary."""

    destination_id: str
    day_number: int
    order: int
    notes: str | None = None

    @field_validator("day_number")
    @classmethod
    def validate_day_number(cls, v: int) -> int:
        if v < 1:
            raise ValueError("day_number must be greater than or equal to 1")
        return v

    @field_validator("order")
    @classmethod
    def validate_order(cls, v: int) -> int:
        if v < 1:
            raise ValueError("order must be greater than or equal to 1")
        return v

    @field_validator("notes")
    @classmethod
    def validate_notes(cls, v: str | None) -> str | None:
        if v is not None and len(v) > 500:
            raise ValueError("notes must not exceed 500 characters")
        return v


class ItineraryStopResponse(ItineraryStopCreate):
    """Itinerary stop data returned in API responses."""

    id: str
    destination_name: str

    @classmethod
    def from_node(
        cls,
        properties: dict[str, Any],
        destination_name: str,
    ) -> "ItineraryStopResponse":
        """Build an ItineraryStopResponse from a FalkorDB node's properties dict."""
        return cls(
            id=properties["id"],
            destination_id=properties["destination_id"],
            day_number=properties["day_number"],
            order=properties["order"],
            notes=properties.get("notes"),
            destination_name=destination_name,
        )
