from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class Timeline(BaseModel):
    """Represents key dates for an opportunity."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    registration_open: datetime | None = Field(
        None,
        description="The date and time when registration opens.",
    )
    registration_close: datetime | None = Field(
        None,
        description="The date and time when registration closes.",
    )
    submission_deadline: datetime | None = Field(
        None,
        description="The date and time when submissions are due.",
    )
    event_start: datetime | None = Field(
        None,
        description="The date and time when the event starts.",
    )
    event_end: datetime | None = Field(
        None,
        description="The date and time when the event ends.",
    )
    result_date: datetime | None = Field(
        None,
        description="The date and time when results are announced.",
    )
    source_last_updated: datetime | None = Field(
        None,
        description="The timestamp when this information was last updated.",
    )


__all__ = ["Timeline"]
