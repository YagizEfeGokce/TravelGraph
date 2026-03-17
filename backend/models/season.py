"""Pydantic v2 schemas for Season entities."""

from typing import Any, Literal

from pydantic import BaseModel, field_validator


SeasonName = Literal["Spring", "Summer", "Autumn", "Winter"]


class SeasonBase(BaseModel):
    """Shared fields present on every season representation."""

    name: SeasonName
    months: list[int]
    avg_temp_c: float
    weather_description: str

    @field_validator("months")
    @classmethod
    def validate_months(cls, v: list[int]) -> list[int]:
        if not v:
            raise ValueError("months must not be empty")
        for month in v:
            if not 1 <= month <= 12:
                raise ValueError(f"Invalid month value {month}: must be between 1 and 12")
        return v


class SeasonResponse(SeasonBase):
    """Season data returned in API responses."""

    id: str

    @classmethod
    def from_node(cls, properties: dict[str, Any]) -> "SeasonResponse":
        """Build a SeasonResponse from a FalkorDB node's properties dict."""
        return cls(
            id=properties["id"],
            name=properties["name"],
            months=properties["months"],
            avg_temp_c=properties["avg_temp_c"],
            weather_description=properties["weather_description"],
        )
