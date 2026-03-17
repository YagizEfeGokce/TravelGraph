"""Pydantic v2 schemas for Tag entities."""

import re
from typing import Any

from pydantic import BaseModel, field_validator

_HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")


class TagBase(BaseModel):
    """Shared fields present on every tag representation."""

    name: str
    color: str

    @field_validator("color")
    @classmethod
    def validate_hex_color(cls, v: str) -> str:
        if not _HEX_COLOR_RE.match(v):
            raise ValueError("color must be a valid hex color code in #RRGGBB format")
        return v


class TagResponse(TagBase):
    """Tag data returned in API responses."""

    id: str

    @classmethod
    def from_node(cls, properties: dict[str, Any]) -> "TagResponse":
        """Build a TagResponse from a FalkorDB node's properties dict."""
        return cls(
            id=properties["id"],
            name=properties["name"],
            color=properties["color"],
        )
