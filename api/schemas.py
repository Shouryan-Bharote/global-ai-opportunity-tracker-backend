from __future__ import annotations

from typing import Any, Generic, Sequence, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard envelope for paginated collections."""

    items: list[T]
    total: int = Field(..., description="Total items matching filter")
    limit: int = Field(..., description="Page size requested")
    offset: int = Field(..., description="Offset requested")


class StatsResponse(BaseModel):
    """Aggregate dashboard metrics."""

    total_opportunities: int
    by_source: dict[str, int]
    by_type: dict[str, int]
    by_status: dict[str, int]
    total_job_runs: int


class HealthResponse(BaseModel):
    """System health check payload."""

    status: str = "ok"
    app_name: str
    environment: str
    database_connected: bool
