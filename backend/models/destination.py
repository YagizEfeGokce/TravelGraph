"""Pydantic v2 schemas for Destination entities."""

from typing import Any

from pydantic import BaseModel, field_validator


class DestinationBase(BaseModel):
    """Shared fields present on every destination representation."""

    name: str
    country: str
    description: str
    lat: float
    lng: float

    @field_validator("lat")
    @classmethod
    def validate_lat(cls, v: float) -> float:
        if not -90.0 <= v <= 90.0:
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator("lng")
    @classmethod
    def validate_lng(cls, v: float) -> float:
        if not -180.0 <= v <= 180.0:
            raise ValueError("Longitude must be between -180 and 180")
        return v


class DestinationCreate(DestinationBase):
    """Payload accepted when creating a new destination."""


class DestinationUpdate(BaseModel):
    """Payload accepted when partially updating a destination.  All fields optional."""

    name: str | None = None
    country: str | None = None
    description: str | None = None
    lat: float | None = None
    lng: float | None = None

    @field_validator("lat")
    @classmethod
    def validate_lat(cls, v: float | None) -> float | None:
        if v is not None and not -90.0 <= v <= 90.0:
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator("lng")
    @classmethod
    def validate_lng(cls, v: float | None) -> float | None:
        if v is not None and not -180.0 <= v <= 180.0:
            raise ValueError("Longitude must be between -180 and 180")
        return v


class DestinationResponse(BaseModel):
    """Destination data returned in API responses."""

    id: str
    name: str
    country: str
    description: str
    lat: float
    lng: float
    avg_rating: float | None = None

    @classmethod
    def from_node(
        cls,
        properties: dict[str, Any],
        avg_rating: float | None = None,
    ) -> "DestinationResponse":
        """Build a DestinationResponse from a FalkorDB node's properties dict."""
        return cls(
            id=properties["id"],
            name=properties["name"],
            country=properties["country"],
            description=properties["description"],
            lat=properties["lat"],
            lng=properties["lng"],
            avg_rating=avg_rating,
        )
