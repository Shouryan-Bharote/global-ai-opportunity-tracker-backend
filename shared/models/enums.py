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

class OpportunitySource(StrEnum):
    """Supported sources of opportunities."""

    UNSTOP = auto()
    DEVPOST = auto()
    KAGGLE = auto()
    HACK2SKILL = auto()
    DEVFOLIO = auto()
    MLH = auto()
    GOOGLE = auto()
    MICROSOFT = auto()
    GITHUB = auto()
    HUGGINGFACE = auto()
    AI_PLANET = auto()
    ZINDI = auto()
    DRIVEN_DATA = auto()
    TOPCODER = auto()
    OTHER = auto()


class OpportunityField(StrEnum):
    """Valid field names for selector profiles.

    Each member corresponds to a field on the Opportunity model.
    This enum constrains LLM-generated profiles so they can only
    reference fields that actually exist in the domain model.
    """

    TITLE = auto()
    DESCRIPTION = auto()
    TYPE = auto()
    STATUS = auto()
    ORGANIZER = auto()
    LOCATION = auto()
    TIMELINE = auto()
    DIFFICULTY = auto()
    TAGS = auto()
    PRIZES = auto()
    ELIGIBILITY = auto()
    TEAM_SIZE_MIN = auto()
    TEAM_SIZE_MAX = auto()
    REGISTRATION_FEE = auto()
    SOURCE = auto()
    SOURCE_URL = auto()
    REGISTRATION_URL = auto()
    RULES_URL = auto()
    IMAGE_URL = auto()
    IS_FEATURED = auto()
    IS_REMOTE_FRIENDLY = auto()
    NOTES = auto()


__all__ = [
    "OpportunityType",
    "OpportunityStatus",
    "LocationType",
    "DifficultyLevel",
    "PrizeType",
    "Currency",
    "OpportunitySource",
    "OpportunityField",
]