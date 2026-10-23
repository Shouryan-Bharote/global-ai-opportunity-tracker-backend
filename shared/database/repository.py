import json
from typing import Any, Optional, Sequence
from datetime import datetime

from sqlmodel import Session, select, func, or_

from shared.database.models import OpportunityCreate, OpportunityDB, JobRun
from shared.database.session import get_session


class OpportunityRepository:
    """Repository for OpportunityDB and JobRun with UPSERT and advanced filtering."""

    def upsert_opportunity(self, opportunity_create: OpportunityCreate) -> OpportunityDB:
        """Insert or update an opportunity based on its ID or source URL.

        Returns the saved OpportunityDB instance.
        """
        with get_session() as session:
            db_opportunity = session.get(OpportunityDB, opportunity_create.id)

            if db_opportunity:
                # Update all non-PK fields on the existing record
                update_data = self._to_db_dict(opportunity_create)
                for field, value in update_data.items():
                    if field == "id":
                        continue
                    setattr(db_opportunity, field, value)
            else:
                # Fallback: check by source_url (unique constraint)
                statement = select(OpportunityDB).where(
                    OpportunityDB.source_url == opportunity_create.source_url
                )
                db_opportunity = session.exec(statement).first()

                if db_opportunity:
                    update_data = self._to_db_dict(opportunity_create)
                    for field, value in update_data.items():
                        if field == "id":
                            continue
                        setattr(db_opportunity, field, value)
                else:
                    # Brand new record — build directly from the flat dict
                    db_opportunity = OpportunityDB(**self._to_db_dict(opportunity_create))
                    session.add(db_opportunity)

            session.commit()
            session.refresh(db_opportunity)
            return db_opportunity

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def get_opportunity_by_id(self, opportunity_id: str) -> Optional[OpportunityDB]:
        """Return an opportunity by its primary key."""
        with get_session() as session:
            return session.get(OpportunityDB, opportunity_id)

    def get_opportunity_by_source_url(self, source_url: str) -> Optional[OpportunityDB]:
        """Return an opportunity by its unique source URL."""
        with get_session() as session:
            statement = select(OpportunityDB).where(
                OpportunityDB.source_url == source_url
            )
            return session.exec(statement).first()

    def list_opportunities(
        self,
        query: Optional[str] = None,
        type_: Optional[str] = None,
        status: Optional[str] = None,
        source: Optional[str] = None,
        tag: Optional[str] = None,
        is_remote_friendly: Optional[bool] = None,
        is_featured: Optional[bool] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[OpportunityDB], int]:
        """Return a filtered, paginated list of opportunities along with total count."""
        with get_session() as session:
            stmt = select(OpportunityDB)

            if query:
                search_term = f"%{query}%"
                stmt = stmt.where(
                    or_(
                        OpportunityDB.title.ilike(search_term),
                        OpportunityDB.description.ilike(search_term),
                    )
                )

            if type_:
                stmt = stmt.where(OpportunityDB.type == type_.lower())

            if status:
                stmt = stmt.where(OpportunityDB.status == status.lower())

            if source:
                stmt = stmt.where(OpportunityDB.source == source.lower())

            if is_remote_friendly is not None:
                stmt = stmt.where(OpportunityDB.is_remote_friendly == is_remote_friendly)

            if is_featured is not None:
                stmt = stmt.where(OpportunityDB.is_featured == is_featured)

            # Count total matching query before pagination
            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = session.exec(count_stmt).one()

            # Apply pagination and sorting (most recent first if available, else by title)
            stmt = stmt.order_by(OpportunityDB.scraped_at.desc(), OpportunityDB.title.asc())
            stmt = stmt.offset(offset).limit(limit)
            items = list(session.exec(stmt).all())

            # Optional in-memory tag filter if tag provided (since tags are stored in JSON array)
            if tag:
                normalized_tag = tag.lower()
                filtered_items = [
                    item for item in items if any(normalized_tag in t.lower() for t in (item.tags or []))
                ]
                return filtered_items, len(filtered_items)

            return items, total

    def list_job_runs(self, limit: int = 20, offset: int = 0) -> tuple[list[JobRun], int]:
        """Return job history records ordered from most recent to oldest."""
        with get_session() as session:
            count_stmt = select(func.count()).select_from(JobRun)
            total = session.exec(count_stmt).one()

            stmt = select(JobRun).order_by(JobRun.start_time.desc()).offset(offset).limit(limit)
            runs = list(session.exec(stmt).all())
            return runs, total

    def get_stats(self) -> dict[str, Any]:
        """Aggregate stats across opportunities and sources."""
        with get_session() as session:
            total_opps = session.exec(select(func.count()).select_from(OpportunityDB)).one()
            
            # Count by source
            source_stmt = select(OpportunityDB.source, func.count(OpportunityDB.id)).group_by(OpportunityDB.source)
            by_source = dict(session.exec(source_stmt).all())

            # Count by type
            type_stmt = select(OpportunityDB.type, func.count(OpportunityDB.id)).group_by(OpportunityDB.type)
            by_type = dict(session.exec(type_stmt).all())

            # Count by status
            status_stmt = select(OpportunityDB.status, func.count(OpportunityDB.id)).group_by(OpportunityDB.status)
            by_status = dict(session.exec(status_stmt).all())

            # Total jobs run
            total_jobs = session.exec(select(func.count()).select_from(JobRun)).one()

            return {
                "total_opportunities": total_opps,
                "by_source": by_source,
                "by_type": by_type,
                "by_status": by_status,
                "total_job_runs": total_jobs,
            }

    # ------------------------------------------------------------------
    # Private serialization
    # ------------------------------------------------------------------

    def _to_db_dict(self, opportunity_create: OpportunityCreate) -> dict[str, Any]:
        """Convert an OpportunityCreate into a flat dict suitable for OpportunityDB.

        Nested Pydantic models (Organizer, Location, Timeline, Prize, Metadata)
        are serialised to plain dicts and stored in the ``*_json`` JSON columns.
        """
        try:
            raw = opportunity_create.model_dump()
        except AttributeError:
            raw = opportunity_create.dict()

        organizer = raw.pop("organizer", None)
        location = raw.pop("location", None)
        timeline = raw.pop("timeline", None)
        prizes = raw.pop("prizes", None)
        metadata = raw.pop("metadata", None)

        raw["organizer_json"] = organizer
        raw["location_json"] = location
        raw["timeline_json"] = timeline
        raw["prizes_json"] = prizes if prizes is not None else []
        raw["metadata_json"] = metadata

        return raw