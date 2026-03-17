"""Pydantic v2 schemas for Festival entities."""

from datetime import date
from typing import Any

from pydantic import BaseModel, field_validator, model_validator


class FestivalBase(BaseModel):
    """Shared fields present on every festival representation."""

    name: str
    description: str
    start_date: date
    end_date: date
    is_recurring: bool
    ticket_price: float | None = None

    @field_validator("ticket_price")
    @classmethod
    def validate_ticket_price(cls, v: float | None) -> float | None:
        if v is not None and v < 0:
            raise ValueError("ticket_price must be greater than or equal to 0")
        return v

    @model_validator(mode="after")
    def validate_date_range(self) -> "FestivalBase":
        if self.start_date >= self.end_date:
            raise ValueError("start_date must be before end_date")
        return self


class FestivalCreate(FestivalBase):
    """Payload accepted when creating a new festival."""

    destination_id: str


class FestivalResponse(FestivalBase):
    """Festival data returned in API responses."""

    id: str
    destination_id: str

    @classmethod
    def from_node(cls, properties: dict[str, Any]) -> "FestivalResponse":
        """Build a FestivalResponse from a FalkorDB node's properties dict.

        ``start_date`` and ``end_date`` are stored as ISO strings in FalkorDB
        and converted back to ``date`` objects here.
        """
        data = dict(properties)
        data["start_date"] = date.fromisoformat(data["start_date"])
        data["end_date"] = date.fromisoformat(data["end_date"])
        return cls(**{k: data[k] for k in cls.model_fields})
