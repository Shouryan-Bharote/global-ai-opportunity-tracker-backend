from __future__ import annotations

import asyncio
from typing import Optional
from fastapi import APIRouter, BackgroundTasks, Query
from pydantic import BaseModel

from api.schemas import PaginatedResponse
from shared.database.models import JobRun
from shared.database.repository import OpportunityRepository
from scraper.core.scheduler.job_scheduler import ScraperOrchestrator

router = APIRouter(prefix="/jobs", tags=["Scraper Jobs"])
repo = OpportunityRepository()
orchestrator = ScraperOrchestrator(headless=True)


class TriggerResponse(BaseModel):
    message: str
    target_scraper: str


@router.get("", response_model=PaginatedResponse[JobRun], summary="List job run history")
def list_job_runs(
    limit: int = Query(20, ge=1, le=100, description="Page limit"),
    offset: int = Query(0, ge=0, description="Page offset"),
) -> PaginatedResponse[JobRun]:
    """Retrieve execution history for all scrapers."""
    items, total = repo.list_job_runs(limit=limit, offset=offset)
    return PaginatedResponse(items=items, total=total, limit=limit, offset=offset)


async def _execute_scraper_background(scraper_name: Optional[str] = None) -> None:
    """Run scrapers asynchronously in the background."""
    if scraper_name == "devpost":
        await orchestrator._run_scraper_with_tracking_and_retry(
            "devpost", orchestrator.run_devpost_scraper
        )
    elif scraper_name == "unstop":
        await orchestrator._run_scraper_with_tracking_and_retry(
            "unstop", orchestrator.run_unstop_scraper
        )
    else:
        await orchestrator.run_all_scrapers()


@router.post("/trigger", response_model=TriggerResponse, summary="Trigger scraper run on-demand")
def trigger_scraper_run(
    scraper_name: Optional[str] = Query(None, description="Optional scraper name: 'devpost' or 'unstop'"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> TriggerResponse:
    """Manually initiate a scraping run in the background."""
    target = scraper_name.lower() if scraper_name else "all"
    background_tasks.add_task(_execute_scraper_background, scraper_name)
    return TriggerResponse(
        message=f"Scraper job '{target}' queued for background execution.",
        target_scraper=target,
    )
