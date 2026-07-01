from __future__ import annotations

from collections.abc import Mapping
from enum import Enum
from typing import NoReturn, TypeVar
from pydantic import BaseModel

from shared.logger import get_logger
from shared.models.enums import DifficultyLevel, OpportunityStatus, OpportunityType
from shared.models.location import Location
from shared.models.metadata import Metadata
from shared.models.opportunity import Opportunity
from shared.models.organizer import Organizer
from shared.models.prize import Prize
from shared.models.timeline import Timeline
from scraper.parsers.base_parser import BaseParser
from scraper.parsers.parser_utils import ParserUtils

logger = get_logger(__name__)

T = TypeVar("T", bound=BaseModel)
E = TypeVar("E", bound=Enum)


class OpportunityParser(BaseParser[Opportunity]):
    """Canonical parser for converting raw scraped dictionaries into Opportunity models."""

    def parse(self, data: object) -> Opportunity:
        """Parses the input data into an Opportunity model.

        Args:
            data: Raw parsed input (expected to be a mapping).

        Returns:
            A validated Opportunity model instance.

        Raises:
            ValueError: If required fields are missing, null, or invalid.
            TypeError: If nested model parsing encounters invalid element types.
        """
        logger.debug("OpportunityParser: start parsing opportunity")
        self._validate(data)
        raw_data = self._preprocess(data)

        if not isinstance(raw_data, Mapping):
            raise TypeError("_preprocess() must return a Mapping[str, object]")

        raw_data_mapping: Mapping[str, object] = raw_data

        # Required nested models
        organizer = self._parse_required_model(
            raw_data_mapping,
            "organizer",
            Organizer,
        )
        location = self._parse_required_model(
            raw_data_mapping,
            "location",
            Location,
        )
        timeline = self._parse_required_model(
            raw_data_mapping,
            "timeline",
            Timeline,
        )

        # Enum fields
        opportunity_type = self._parse_enum(
            raw_data_mapping,
            "type",
            OpportunityType,
            required=True,
        )
        status = self._parse_enum(
            raw_data_mapping,
            "status",
            OpportunityStatus,
            required=True,
        )
        difficulty = self._parse_enum(
            raw_data_mapping,
            "difficulty",
            DifficultyLevel,
            required=False,
        )

        # Primitive string fields
        id_ = self._parse_string(raw_data_mapping, "id", required=True)
        title = self._parse_string(raw_data_mapping, "title", required=True)
        description = self._parse_string(
            raw_data_mapping,
            "description",
            required=False,
        )
        source = self._parse_string(raw_data_mapping, "source", required=True)
        notes = self._parse_string(raw_data_mapping, "notes", required=False)

        # URLs
        source_url = self._parse_url(raw_data_mapping, "source_url", required=True)
        registration_url = self._parse_url(
            raw_data_mapping,
            "registration_url",
            required=False,
        )
        rules_url = self._parse_url(
            raw_data_mapping,
            "rules_url",
            required=False,
        )
        image_url = self._parse_url(
            raw_data_mapping,
            "image_url",
            required=False,
        )

        # Numeric fields
        registration_fee = self._parse_float(raw_data_mapping, "registration_fee")
        team_size_min = self._parse_int(raw_data_mapping, "team_size_min")
        team_size_max = self._parse_int(raw_data_mapping, "team_size_max")

        # Boolean fields
        is_featured = self._parse_bool(raw_data_mapping, "is_featured")
        is_remote_friendly = self._parse_bool(raw_data_mapping, "is_remote_friendly")

        # Collections
        prizes = self._parse_prizes(raw_data_mapping)
        tags = self._parse_list(raw_data_mapping, "tags")
        eligibility = self._parse_list(raw_data_mapping, "eligibility")

        # Metadata
        metadata = self._parse_metadata(raw_data_mapping)

        # Construct Opportunity
        opportunity = Opportunity(
            id=id_,
            title=title,
            description=description,
            type=opportunity_type,
            status=status,
            organizer=organizer,
            location=location,
            timeline=timeline,
            difficulty=difficulty,
            tags=tags,
            prizes=prizes,
            eligibility=eligibility,
            team_size_min=team_size_min,
            team_size_max=team_size_max,
            registration_fee=registration_fee,
            source=source,
            source_url=source_url,
            registration_url=registration_url,
            rules_url=rules_url,
            image_url=image_url,
            is_featured=is_featured,
            is_remote_friendly=is_remote_friendly,
            notes=notes,
            **({"metadata": metadata} if metadata is not None else {}),
        )

        logger.debug(
            "OpportunityParser: successfully parsed opportunity id=%s",
            opportunity.id,
        )
        return self._postprocess(opportunity)

    def _validate(self, data: object) -> None:
        """Validates the input before parsing.

        Subclasses can override this method for stricter validation rules.
        """
        if not isinstance(data, Mapping):
            raise ValueError("Data must be a mapping.")

        required_fields = (
            "id",
            "title",
            "type",
            "status",
            "organizer",
            "location",
            "timeline",
            "source",
            "source_url",
        )

        missing_or_null: list[str] = []
        for field in required_fields:
            if field not in data or data[field] is None:
                missing_or_null.append(field)

        if missing_or_null:
            logger.warning(
                "OpportunityParser: validation failure: missing or null required fields=%s",
                missing_or_null,
            )
            raise ValueError(
                "Missing or null required field(s): " + ", ".join(missing_or_null)
            )

    def _preprocess(self, data: object) -> object:
        """Hook for lightweight preprocessing before parsing.

        Currently returns the input unchanged.

        TODO:
        Site-specific parsers may preprocess raw data before passing it to
        OpportunityParser rather than overriding this method.
        """
        return data

    # def _postprocess(self, opportunity: Opportunity) -> Opportunity:
    #     """Postprocess the parsed Opportunity.

    #     Canonical behavior returns the Opportunity unchanged.
    #     Subclasses may override to perform site-specific normalization steps.
    #     """
    #     return opportunity

    def _get(self, raw_data: Mapping[str, object], key: str) -> object:
        """Gets a value from the raw mapping using ParserUtils.safe_get()."""
        return ParserUtils.safe_get(raw_data, key)

    def _parse_bool(self, raw_data: Mapping[str, object], key: str) -> bool:
        """Parses a boolean field, defaulting to False."""
        return ParserUtils.get_bool(self._get(raw_data, key)) or False

    def _parse_int(self, raw_data: Mapping[str, object], key: str) -> int | None:
        """Parses an optional integer field."""
        return ParserUtils.get_int(self._get(raw_data, key))

    def _parse_float(self, raw_data: Mapping[str, object], key: str) -> float | None:
        """Parses an optional float field."""
        return ParserUtils.get_float(self._get(raw_data, key))

    def _parse_string(
        self,
        raw_data: Mapping[str, object],
        key: str,
        *,
        required: bool,
    ) -> str | None:
        """Parses a string field.

        Args:
            raw_data: Source mapping.
            key: Field key.
            required: Whether the field must be present and non-null/non-empty.

        Returns:
            The parsed string if present; otherwise None (when required=False).

        Raises:
            ValueError: If required=True and the value is missing/invalid.
        """
        value = ParserUtils.get_string(self._get(raw_data, key))

        if required:
            if value is None or value == "":
                self._raise_required_field_error(
                    field=key,
                    message=f"Missing or invalid required string field: {key}",
                )
            return value

        return value

    def _parse_url(
        self,
        raw_data: Mapping[str, object],
        key: str,
        *,
        required: bool,
    ) -> str | None:
        """Parses a URL field using ParserUtils.get_url().

        Args:
            raw_data: Source mapping.
            key: Field key.
            required: Whether the field must be present and non-null/non-empty.

        Returns:
            The parsed URL if present; otherwise None (when required=False).

        Raises:
            ValueError: If required=True and the URL is missing/invalid.
        """
        value = ParserUtils.get_url(self._get(raw_data, key))

        if required:
            if value is None or value == "":
                self._raise_required_field_error(
                    field=key,
                    message=f"Missing or invalid required URL field: {key}",
                )
            return value

        return value

    def _parse_enum(
        self,
        raw_data: Mapping[str, object],
        key: str,
        enum_type: type[E],
        *,
        required: bool,
    ) -> E | None:
        """Parses an enum value by name/value with normalization."""
        value = ParserUtils.get_enum(self._get(raw_data, key), enum_type)
        if required and value is None:
            self._raise_required_field_error(
                field=key,
                message=f"Missing or invalid required enum field: {key}",
            )
        return value

    def _raise_required_field_error(self, field: str, message: str) -> NoReturn:
        """Logs and raises a required-field validation error."""
        logger.warning(
            "OpportunityParser: validation failure: field=%s",
            field,
        )
        raise ValueError(message)

    def _parse_required_model(
        self,
        raw_data: Mapping[str, object],
        key: str,
        model: type[T],
    ) -> T:
        """Parses a required nested model via ParserUtils.build_model()."""
        data = self._get(raw_data, key)
        parsed = ParserUtils.build_model(data, model)
        if parsed is None:
            self._raise_required_field_error(
                field=key,
                message=f"Missing or invalid required field: {key}",
            )
        return parsed

    def _parse_list(self, raw_data: Mapping[str, object], key: str) -> list[str]:
        """Parses an optional list[str] field into a list (empty if missing)."""
        return ParserUtils.get_list(self._get(raw_data, key))

    def _parse_prizes(self, raw_data: Mapping[str, object]) -> list[Prize]:
        """Parses prizes list using nested model building."""
        prizes_data = self._get(raw_data, "prizes")
        if prizes_data is None:
            return []
        return ParserUtils.build_models(prizes_data, Prize)

    def _parse_metadata(self, raw_data: Mapping[str, object]) -> Metadata | None:
        """Parses Opportunity.metadata."""
        metadata_data = self._get(raw_data, "metadata")
        if metadata_data is None:
            return None

        metadata = ParserUtils.build_model(metadata_data, Metadata)
        if metadata is None:
            logger.warning(
                "OpportunityParser: validation failure: field=%s",
                "metadata",
            )
            raise ValueError("Invalid Opportunity.metadata: could not construct model")

        return metadata


__all__ = ["OpportunityParser"]
