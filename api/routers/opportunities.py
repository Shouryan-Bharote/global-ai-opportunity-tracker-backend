from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status

from api.schemas import PaginatedResponse, StatsResponse
from shared.database.models import OpportunityDB, JobRun
from shared.database.repository import OpportunityRepository

router = APIRouter(prefix="/opportunities", tags=["Opportunities"])
repo = OpportunityRepository()


@router.get("", response_model=PaginatedResponse[OpportunityDB], summary="List opportunities")
def list_opportunities(
    q: Optional[str] = Query(None, description="Search keyword in title or description"),
    type: Optional[str] = Query(None, description="Opportunity category (hackathon, competition, etc.)"),
    status: Optional[str] = Query(None, description="Lifecycle status (open, upcoming, closed)"),
    source: Optional[str] = Query(None, description="Platform source (devpost, unstop)"),
    tag: Optional[str] = Query(None, description="Filter by tag keyword"),
    is_remote_friendly: Optional[bool] = Query(None, description="Filter remote-friendly events"),
    is_featured: Optional[bool] = Query(None, description="Filter featured events"),
    limit: int = Query(20, ge=1, le=100, description="Page limit (max 100)"),
    offset: int = Query(0, ge=0, description="Page offset"),
) -> PaginatedResponse[OpportunityDB]:
    """Retrieve filtered, paginated opportunities stored in the tracker database."""
    items, total = repo.list_opportunities(
        query=q,
        type_=type,
        status=status,
        source=source,
        tag=tag,
        is_remote_friendly=is_remote_friendly,
        is_featured=is_featured,
        limit=limit,
        offset=offset,
    )
    return PaginatedResponse(items=items, total=total, limit=limit, offset=offset)


@router.get("/stats", response_model=StatsResponse, summary="Get summary statistics")
def get_opportunity_stats() -> StatsResponse:
    """Retrieve summary counts broken down by source, type, and status."""
    stats = repo.get_stats()
    return StatsResponse(**stats)


@router.get("/{opportunity_id:path}", response_model=OpportunityDB, summary="Get opportunity details")
def get_opportunity_by_id(opportunity_id: str) -> OpportunityDB:
    """Fetch a single opportunity by its ID (typically its source URL)."""
    opp = repo.get_opportunity_by_id(opportunity_id)
    if not opp:
        # Fallback check by source_url
        opp = repo.get_opportunity_by_source_url(opportunity_id)
    if not opp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Opportunity with ID '{opportunity_id}' not found",
        )
    return opp
