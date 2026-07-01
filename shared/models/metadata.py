from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Metadata(BaseModel):
    """Additional metadata collected during scraping.

    This model is intentionally flexible to support varying sources and
    scraper-specific metadata without requiring frequent schema changes.
    """

    model_config = ConfigDict(
        frozen=True,
        str_strip_whitespace=True,
        extra="allow",
    )

    # Optional explicit payload field; additional keys are allowed via extra="allow".
    payload: dict[str, Any] = Field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        """Convenience accessor for metadata values."""
        if key == "payload":
            return self.payload
        return getattr(self, key, default)


__all__ = ["Metadata"]
