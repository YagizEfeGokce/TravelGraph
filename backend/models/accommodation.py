"""Pydantic v2 schemas for Accommodation entities."""

from typing import Any, Literal

from pydantic import BaseModel, field_validator


AccommodationType = Literal["hotel", "hostel", "apartment"]


class AccommodationBase(BaseModel):
    """Shared fields present on every accommodation representation."""

    name: str
    type: AccommodationType
    star_rating: int
    price_per_night: float
    address: str

    @field_validator("star_rating")
    @classmethod
    def validate_star_rating(cls, v: int) -> int:
        if not 1 <= v <= 5:
            raise ValueError("star_rating must be between 1 and 5")
        return v

    @field_validator("price_per_night")
    @classmethod
    def validate_price(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("price_per_night must be greater than 0")
        return v


class AccommodationCreate(AccommodationBase):
    """Payload accepted when creating a new accommodation."""

    destination_id: str


class AccommodationResponse(AccommodationBase):
    """Accommodation data returned in API responses."""

    id: str
    destination_id: str

    @classmethod
    def from_node(cls, properties: dict[str, Any]) -> "AccommodationResponse":
        """Build an AccommodationResponse from a FalkorDB node's properties dict."""
        return cls(**{k: properties[k] for k in cls.model_fields})
