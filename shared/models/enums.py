from enum import StrEnum, auto

class OpportunityType(StrEnum):
    """Supported categories of opportunities."""

    HACKATHON = auto()
    COMPETITION = auto()
    CONFERENCE = auto()
    WORKSHOP = auto()
    FELLOWSHIP = auto()
    INTERNSHIP = auto()
    SCHOLARSHIP = auto()
    GRANT = auto()
    RESEARCH_PROGRAM = auto()
    BOOTCAMP = auto()
    COURSE = auto()
    CHALLENGE = auto()
    OTHER = auto()


class OpportunityStatus(StrEnum):
    """Supported lifecycle states of an opportunity."""

    UPCOMING = auto()
    OPEN = auto()
    CLOSED = auto()
    COMPLETED = auto()
    CANCELLED = auto()
    UNKNOWN = auto()


class LocationType(StrEnum):
    """Supported location modes for an opportunity."""

    ONLINE = auto()
    OFFLINE = auto()
    HYBRID = auto()
    UNKNOWN = auto()


class DifficultyLevel(StrEnum):
    """The difficulty level of the opportunity."""

    BEGINNER = auto()
    INTERMEDIATE = auto()
    ADVANCED = auto()
    EXPERT = auto()
    UNKNOWN = auto()


class PrizeType(StrEnum):
    """The type of prize offered."""

    CASH = auto()
    SCHOLARSHIP = auto()
    INTERNSHIP = auto()
    CERTIFICATE = auto()
    SWAG = auto()
    CREDITS = auto()
    OTHER = auto()


class Currency(StrEnum):
    """Supported currencies for prizes."""

    USD = auto()
    EUR = auto()
    GBP = auto()
    INR = auto()
    JPY = auto()
    CNY = auto()
    AUD = auto()
    CAD = auto()
    OTHER = auto()

__all__ = [
    "OpportunityType",
    "OpportunityStatus",
    "LocationType",
    "DifficultyLevel",
    "PrizeType",
    "Currency",
]