"""Pydantic v2 schemas for Category entities."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class CategoryBase(BaseModel):
    """Shared fields present on every category representation."""

    name: str
    icon: str
    description: str | None = None


class CategoryResponse(CategoryBase):
    """Category data returned in API responses."""

    id: str

    @classmethod
    def from_node(cls, properties: dict[str, Any]) -> "CategoryResponse":
        """Build a CategoryResponse from a FalkorDB node's properties dict."""
        return cls(
            id=properties["id"],
            name=properties["name"],
            icon=properties["icon"],
            description=properties.get("description"),
        )
