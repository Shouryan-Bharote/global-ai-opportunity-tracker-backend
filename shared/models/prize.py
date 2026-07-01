from pydantic import BaseModel, ConfigDict, Field
from shared.models.enums import Currency, PrizeType


class Prize(BaseModel):
    """Represents a single prize or reward offered by an opportunity."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    type: PrizeType = Field(
        ...,
        description="The category or type of the prize.",
    )
    title: str | None = Field(
        None,
        min_length=1,
        description="A human-readable title for the prize (e.g., 'First Prize').",
    )
    amount: float | None = Field(
        None,
        ge=0,
        description="The numeric monetary value of the prize.",
    )
    currency: Currency | None = Field(
        None,
        description="The currency for the monetary prize amount.",
    )
    description: str | None = Field(
        None,
        min_length=1,
        description="Additional details about the prize (e.g., 'AWS Credits').",
    )


__all__ = ["Prize"]
