from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from scraper.scrapers.devpost import DevpostScraper
from scraper.scrapers.unstop import UnstopScraper
from scraper.core.browser.models import BrowserLaunchOptions
from shared.database.models import OpportunityDB, JobRun
from shared.database.session import get_session
from shared.logger import get_logger

logger = get_logger(__name__)


class ScraperOrchestrator:
    """Orchestrates running of scrapers and stores results in the database."""

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.options = BrowserLaunchOptions(headless=headless)

    async def run_devpost_scraper(self) -> list[OpportunityDB]:
        """Run Devpost scraper and return opportunities."""
        logger.info("Starting Devpost scraper...")
        scraper = DevpostScraper(options=self.options)
        try:
            opportunities = await scraper.scrape()
            logger.info("Devpost scraper finished: %d opportunities", len(opportunities))
            return opportunities
        except Exception as e:
            logger.exception("Devpost scraper failed: %s", e)
            return []
        finally:
            await scraper.stop()

    async def run_unstop_scraper(self) -> list[OpportunityDB]:
        """Run Unstop scraper and return opportunities."""
        logger.info("Starting Unstop scraper...")
        scraper = UnstopScraper(options=self.options)
        try:
            opportunities = await scraper.scrape()
            logger.info("Unstop scraper finished: %d opportunities", len(opportunities))
            return opportunities
        except Exception as e:
            logger.exception("Unstop scraper failed: %s", e)
            return []
        finally:
            await scraper.stop()

    async def _save_opportunities(self, opportunities: list) -> int:
        """Save opportunities to the database using UPSERT."""
        from shared.database.models import OpportunityCreate
        from shared.database.repository import OpportunityRepository
        repository = OpportunityRepository()
        saved_count = 0
        for opp in opportunities:
            try:
                opp_create = OpportunityCreate.model_validate(opp, from_attributes=True)
                repository.upsert_opportunity(opp_create)
                saved_count += 1
            except Exception as e:
                logger.error("Failed to save opportunity %s: %s", getattr(opp, "id", "unknown"), e)
        return saved_count

    async def _run_scraper_with_tracking_and_retry(
        self, scraper_name: str, scraper_func, max_retries: int = 2, retry_delay: int = 5
    ) -> dict:
        """Run a scraper with retry logic and job tracking."""
        start_time = datetime.now(timezone.utc)
        opportunities = []
        success = False
        error = None

        for attempt in range(max_retries):
            try:
                logger.info(
                    "Running %s scraper (attempt %d/%d)", scraper_name, attempt + 1, max_retries
                )
                opportunities = await scraper_func()
                success = True
                break  # Success, exit retry loop
            except Exception as e:
                error = str(e)
                logger.warning(
                    "%s scraper attempt %d failed: %s", scraper_name, attempt + 1, e
                )
                if attempt < max_retries - 1:
                    logger.info(
                        "Retrying %s scraper in %d seconds...", scraper_name, retry_delay
                    )
                    await asyncio.sleep(retry_delay)
                else:
                    logger.error(
                        "%s scraper failed after %d attempts: %s",
                        scraper_name,
                        max_retries,
                        e,
                    )

        end_time = datetime.now(timezone.utc)
        opportunities_count = len(opportunities)

        # Save opportunities to database if any were scraped
        if opportunities:
            saved_count = await self._save_opportunities(opportunities)
            logger.info(
                "Saved %d/%d opportunities from %s scraper",
                saved_count,
                opportunities_count,
                scraper_name,
            )
            opportunities_count = saved_count  # Update count to reflect saved opportunities

        # Create job run record
        job_run = JobRun(
            scraper_name=scraper_name,
            start_time=start_time,
            end_time=end_time,
            success=success,
            error=error,
            opportunities_count=opportunities_count,
        )
        with get_session() as session:
            session.add(job_run)
            session.commit()

        return {
            "scraper": scraper_name,
            "count": opportunities_count,
            "start_time": start_time,
            "end_time": end_time,
            "success": success,
            "error": error,
        }

    async def run_all_scrapers(self) -> list[dict]:
        """Run all scrapers sequentially (for testing) and return a list of statistics."""
        logger.info("Starting orchestrator run of all scrapers (sequential)...")
        results = []
        # Run Devpost
        devpost_result = await self._run_scraper_with_tracking_and_retry(
            "devpost", self.run_devpost_scraper
        )
        results.append(devpost_result)
        # Run Unstop
        unstop_result = await self._run_scraper_with_tracking_and_retry(
            "unstop", self.run_unstop_scraper
        )
        results.append(unstop_result)
        logger.info("Orchestrator run completed: %s", results)
        return results

    async def start_scheduler_async(self, cron_expression: str = "0 2 * * *") -> None:
        """
        Start the asynchronous scheduler to run scrapers at the given cron expression.
        Default: every day at 2:00 AM.
        """
        scheduler = AsyncIOScheduler()
        trigger = CronTrigger.from_crontab(cron_expression)
        scheduler.add_job(self._run_orchestrator_job, trigger, id="scraper_orchestrator")
        scheduler.start()
        logger.info("Scheduler started with cron expression: %s", cron_expression)
        # Keep the scheduler running
        try:
            while True:
                await asyncio.sleep(3600)
        except KeyboardInterrupt:
            logger.info("Scheduler interrupted, shutting down...")
            scheduler.shutdown()

    def start_scheduler(self, cron_expression: str = "0 2 * * *") -> None:
        """Synchronous entrypoint that runs the async scheduler in an active event loop."""
        try:
            asyncio.run(self.start_scheduler_async(cron_expression=cron_expression))
        except KeyboardInterrupt:
            logger.info("Scheduler interrupted by user, exiting.")


    async def _run_orchestrator_job(self) -> None:
        """Job function to be called by the scheduler."""
        logger.info("Scheduler triggering orchestrator job...")
        # Run scrapers in parallel with concurrency control (max 2 parallel)
        semaphore = asyncio.Semaphore(2)

        async def run_scraper_with_semaphore(scraper_name: str, scraper_func):
            async with semaphore:
                return await self._run_scraper_with_tracking_and_retry(
                    scraper_name, scraper_func
                )

        # Create tasks for both scrapers
        devpost_task = run_scraper_with_semaphore("devpost", self.run_devpost_scraper)
        unstop_task = run_scraper_with_semaphore("unstop", self.run_unstop_scraper)

        # Wait for both to complete
        results = await asyncio.gather(devpost_task, unstop_task)
        logger.info("Orchestrator job completed: %s", results)


# For direct execution (e.g., poetry run python -m scraper.core.scheduler.job_scheduler)
def main() -> None:
    """Run the orchestrator either as a scheduled daemon or a one-off batch."""
    import os
    import sys

    headless_env = os.getenv("HEADLESS", "true").lower() in ("true", "1", "yes")
    cron_expr = os.getenv("SCRAPER_CRON_SCHEDULE", "0 2 * * *")
    orchestrator = ScraperOrchestrator(headless=headless_env)

    if "--scheduler" in sys.argv or os.getenv("RUN_MODE", "").lower() == "scheduler":
        logger.info("Running in continuous scheduler daemon mode (cron: %s)", cron_expr)
        orchestrator.start_scheduler(cron_expression=cron_expr)
    else:
        logger.info("Running one-off batch execution of all scrapers...")
        asyncio.run(orchestrator.run_all_scrapers())


if __name__ == "__main__":
    main()