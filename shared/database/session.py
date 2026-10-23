from contextlib import contextmanager
from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from shared.config.settings import settings


# ---------------------------------------------------------------------------
# Engine singleton — created once per process
# ---------------------------------------------------------------------------

_engine = None


def get_engine():
    """Return the SQLAlchemy engine, creating it on first call.

    The engine is cached as a module-level singleton so that connection pools
    are reused across calls. Switch from SQLite to PostgreSQL by changing
    ``SQLMODEL_DATABASE_URL`` in your ``.env`` file:

        postgresql+psycopg2://user:password@host:5432/dbname
    """
    global _engine
    if _engine is None:
        url = settings.sqlmodel_database_url
        connect_args = settings.sqlmodel_connect_args.copy() if settings.sqlmodel_connect_args else {}

        # SQLite requires check_same_thread=False for multi-threading,
        # but PostgreSQL / other SQL dialects reject check_same_thread with TypeError.
        if "sqlite" not in url:
            connect_args.pop("check_same_thread", None)

        _engine = create_engine(
            url,
            echo=settings.sqlmodel_echo,
            connect_args=connect_args,
        )
    return _engine


def init_db() -> None:
    """Create all SQLModel tables in the database if they do not already exist.

    Must be called once before any repository or session code runs — typically
    at application start-up or at the top of a scraper entry-point.

    This is idempotent: calling it multiple times is safe.
    """
    # Import all table models so SQLModel.metadata knows about them
    import shared.database.models  # noqa: F401  — registers OpportunityDB, JobRun

    SQLModel.metadata.create_all(get_engine())


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Context manager that provides a SQLModel Session scoped to the block.

    The session is committed on success and rolled back on any exception.
    Callers must not close the session manually.
    """
    session = Session(get_engine(), expire_on_commit=False)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
