from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON
from typing import Optional, List, Any, Dict
from datetime import datetime, timezone

from shared.models.enums import (
    OpportunityType, OpportunityStatus, OpportunitySource,
    DifficultyLevel, LocationType, PrizeType, Currency
)
from shared.models.organizer import Organizer
from shared.models.location import Location
from shared.models.timeline import Timeline
from shared.models.prize import Prize
from shared.models.metadata import Metadata


class OpportunityDB(SQLModel, table=True):
    __tablename__ = "opportunities"

    id: str = Field(primary_key=True, index=True)
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    type: str = Field(index=True)
    status: str = Field(index=True)
    difficulty: Optional[str] = Field(default=None)
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    eligibility: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    team_size_min: Optional[int] = Field(default=None)
    team_size_max: Optional[int] = Field(default=None)
    registration_fee: Optional[float] = Field(default=None)
    source: str = Field(index=True)
    source_url: str = Field(index=True, unique=True)
    registration_url: Optional[str] = Field(default=None)
    rules_url: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    is_featured: bool = Field(default=False)
    is_remote_friendly: bool = Field(default=False)
    notes: Optional[str] = Field(default=None)
    scraped_at: Optional[datetime] = Field(default=None)
    last_seen_at: Optional[datetime] = Field(default=None)
    # Nested objects stored as JSON
    organizer_json: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    location_json: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    timeline_json: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    prizes_json: List[dict] = Field(default_factory=list, sa_column=Column(JSON))
    metadata_json: Optional[Any] = Field(default=None, sa_column=Column(JSON))


from pydantic import BaseModel


class OpportunityCreate(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    type: str
    status: str
    difficulty: Optional[str] = None
    tags: List[str] = []
    eligibility: List[str] = []
    team_size_min: Optional[int] = None
    team_size_max: Optional[int] = None
    registration_fee: Optional[float] = None
    source: str
    source_url: str
    registration_url: Optional[str] = None
    rules_url: Optional[str] = None
    image_url: Optional[str] = None
    is_featured: bool = False
    is_remote_friendly: bool = False
    notes: Optional[str] = None
    scraped_at: Optional[datetime] = None
    last_seen_at: Optional[datetime] = None
    organizer: Optional[Organizer] = None
    location: Optional[Location] = None
    timeline: Optional[Timeline] = None
    prizes: List[Prize] = []
    metadata: Optional[Metadata] = None


class JobRun(SQLModel, table=True):
    __tablename__ = "job_runs"

    id: Optional[int] = Field(default=None, primary_key=True)
    scraper_name: str = Field(index=True)
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = Field(default=None)
    success: bool = Field(default=False)
    error: Optional[str] = Field(default=None)
    opportunities_count: int = Field(default=0)

