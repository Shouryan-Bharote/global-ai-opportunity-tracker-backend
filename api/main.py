from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select

from api.routers import opportunities, jobs
from api.schemas import HealthResponse
from shared.config.settings import settings
from shared.database.session import init_db, get_session
from shared.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle hook: initialize database tables and resources on startup."""
    logger.info("Initializing database schema on API startup...")
    init_db()
    logger.info("TrackIT FastAPI application initialized successfully.")
    yield
    logger.info("Shutting down TrackIT FastAPI application.")


def create_app() -> FastAPI:
    """Application factory for the TrackIT REST API."""
    app = FastAPI(
        title=settings.app_name,
        description="RESTful API for querying global AI hackathons, competitions, conferences, and opportunities.",
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS configuration for frontend clients
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount API routers
    app.include_router(opportunities.router, prefix="/api/v1")
    app.include_router(jobs.router, prefix="/api/v1")

    @app.get("/health", response_model=HealthResponse, tags=["Health"])
    def health_check() -> HealthResponse:
        """Health check endpoint for container probes and uptime monitoring."""
        db_ok = True
        try:
            with get_session() as session:
                session.exec(select(1)).first()
        except Exception as e:
            logger.error("Health check DB probe failed: %s", e)
            db_ok = False

        return HealthResponse(
            status="ok" if db_ok else "degraded",
            app_name=settings.app_name,
            environment=settings.environment,
            database_connected=db_ok,
        )

    return app


app = create_app()
