from pydantic import BaseModel, ConfigDict, Field

from shared.models.enums import (
    DifficultyLevel,
    OpportunitySource,
    OpportunityStatus,
    OpportunityType,
)
from shared.models.location import Location
from shared.models.organizer import Organizer
from shared.models.prize import Prize
from shared.models.timeline import Timeline
from shared.models.metadata import Metadata

from datetime import datetime


class Opportunity(BaseModel):
    """Represents a generic AI/ML opportunity (hackathon, grant, internship, etc.)."""

    model_config = ConfigDict(
        frozen=True,
        str_strip_whitespace=True,
    )

    id: str = Field(
        ...,
        description="The unique identifier for the opportunity.",
    )

    title: str = Field(
        ...,
        min_length=1,
        description="The human-readable title of the opportunity.",
    )

    description: str | None = Field(
        None,
        description="The full description of the opportunity.",
    )

    type: OpportunityType = Field(
        ...,
        description="The category of the opportunity.",
    )

    status: OpportunityStatus = Field(
        ...,
        description="The current status of the opportunity.",
    )

    organizer: Organizer = Field(
        ...,
        description="The organization hosting the opportunity.",
    )

    location: Location = Field(
        ...,
        description="The physical or virtual location of the opportunity.",
    )

    timeline: Timeline = Field(
        ...,
        description="Key dates and deadlines for the opportunity.",
    )

    difficulty: DifficultyLevel | None = Field(
        None,
        description="The difficulty level of the opportunity.",
    )

    tags: list[str] = Field(
        default_factory=list,
        description="Relevant topics and technologies.",
    )

    prizes: list[Prize] = Field(
        default_factory=list,
        description="The prizes or rewards offered.",
    )

    eligibility: list[str] = Field(
        default_factory=list,
        description="Criteria for participant eligibility.",
    )

    team_size_min: int | None = Field(
        None,
        ge=1,
        description="The minimum required team size.",
    )

    team_size_max: int | None = Field(
        None,
        ge=1,
        description="The maximum allowed team size.",
    )

    registration_fee: float | None = Field(
        None,
        ge=0,
        description="The cost to register for the opportunity.",
    )

    source: OpportunitySource = Field(
        ...,
        description="The platform where the opportunity was found.",
    )

    source_url: str = Field(
        ...,
        min_length=1,
        description="The official URL of the opportunity page.",
    )

    registration_url: str | None = Field(
        None,
        description="The registration URL if different from the source URL.",
    )

    rules_url: str | None = Field(
        None,
        description="The URL of the rules or guidelines page.",
    )

    image_url: str | None = Field(
        None,
        description="The URL of the opportunity banner or thumbnail.",
    )

    is_featured: bool = Field(
        default=False,
        description="Whether the opportunity is marked as featured.",
    )

    is_remote_friendly: bool = Field(
        default=False,
        description="Whether the opportunity supports remote participation.",
    )

    notes: str | None = Field(
        None,
        description="Internal notes or additional information.",
    )

    scraped_at: datetime | None = Field(
        None,
        description="The timestamp when this opportunity was last scraped.",
    )

    last_seen_at: datetime | None = Field(
        None,
        description="The timestamp when this opportunity was last observed on the source platform.",
    )

    metadata: Metadata | None = Field(
        default=None,
        description="Additional metadata collected during scraping.",
    )


__all__ = ["Opportunity"]