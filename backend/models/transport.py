"""Pydantic v2 schemas for Transport entities."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, field_validator


TransportType = Literal["flight", "train", "bus", "ferry"]


class TransportBase(BaseModel):
    """Shared fields present on every transport representation."""

    type: TransportType
    provider: str
    duration_hours: float
    price: float
    departure_city: str
    arrival_city: str

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


class TransportCreate(TransportBase):
    """Payload accepted when creating a new transport option."""


class TransportResponse(TransportBase):
    """Transport data returned in API responses."""

    id: str

    @classmethod
    def from_node(cls, properties: dict[str, Any]) -> "TransportResponse":
        """Build a TransportResponse from a FalkorDB node's properties dict."""
        return cls(**{k: properties[k] for k in cls.model_fields})
