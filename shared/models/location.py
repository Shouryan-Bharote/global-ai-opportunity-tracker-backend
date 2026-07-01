from pydantic import BaseModel, ConfigDict, Field

from shared.models.enums import LocationType


class Location(BaseModel):
    """Represents the location or mode of an opportunity."""

    model_config = ConfigDict(
        frozen=True,
        str_strip_whitespace=True,
    )

    type: LocationType = Field(
        ...,
        description="The mode of the opportunity (online, offline, hybrid, unknown).",
    )

    country: str | None = Field(
        default=None,
        min_length=1,
        description="The country where the opportunity takes place.",
    )

    state: str | None = Field(
        default=None,
        min_length=1,
        description="The state or province where the opportunity takes place.",
    )

    city: str | None = Field(
        default=None,
        min_length=1,
        description="The city where the opportunity takes place.",
    )

    venue: str | None = Field(
        default=None,
        min_length=1,
        description="The venue name or address for offline opportunities.",
    )

    timezone: str | None = Field(
        default=None,
        min_length=1,
        description="The IANA timezone of the opportunity.",
    )


__all__ = ["Location"]