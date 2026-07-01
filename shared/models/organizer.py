from pydantic import BaseModel, ConfigDict, Field


class Organizer(BaseModel):
    """Represents an organizer of an opportunity."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(
        ...,
        min_length=1,
        description="The name of the organizer or organization.",
    )
    website: str | None = Field(
        None,
        description="The official website URL of the organizer.",
    )
    email: str | None = Field(
        None,
        description="The public contact email of the organizer.",
    )
    logo_url: str | None = Field(
        None,
        description="The URL of the organizer's logo.",
    )
    description: str | None = Field(
        None,
        description="A short description of the organizer.",
    )


__all__ = ["Organizer"]
