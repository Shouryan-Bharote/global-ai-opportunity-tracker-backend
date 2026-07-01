from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Generic, TypeVar

from shared.logger import get_logger
from shared.models.opportunity import Opportunity
from scraper.parsers.base_parser import BaseParser
from scraper.parsers.opportunity_parser import OpportunityParser

logger = get_logger(__name__)

T = TypeVar("T", bound=Opportunity)


class BaseSiteParser(BaseParser[Opportunity], ABC):
    """Generic base class for website-specific parsers.

    This class is responsible for converting raw website data into the canonical
    dictionary format expected by :class:`~scraper.parsers.opportunity_parser.OpportunityParser`.
    """

    def __init__(self) -> None:
        self._opportunity_parser = OpportunityParser()

    @abstractmethod
    def _transform(self, data: object) -> Mapping[str, object]:
        """Convert website-specific raw data into a canonical opportunity mapping.

        Args:
            data: Raw input produced by a website scraper.

        Returns:
            A mapping that matches the input schema expected by OpportunityParser.parse().
        """
        raise NotImplementedError

    def parse(self, data: object) -> Opportunity:
        """Parse raw website data into a canonical Opportunity model.

        Parsing flow:
          1) Validate using BaseParser hooks.
          2) Transform website-specific data into the canonical mapping.
          3) Parse the canonical mapping using OpportunityParser.
          4) Return the validated Opportunity model.

        Args:
            data: Raw input produced by a website scraper.

        Returns:
            A validated Opportunity model instance.
        """
        logger.debug("%s: start parsing site opportunity", self.__class__.__name__)

        self._validate(data)
        transformed = self._preprocess(data)
        # Note: _preprocess() is intentionally applied to preserve BaseParser hook semantics.
        canonical_mapping = self._transform(transformed)

        opportunity = self._opportunity_parser.parse(canonical_mapping)
        logger.debug("%s: successfully parsed opportunity id=%s", self.__class__.__name__, opportunity.id)
        return opportunity


__all__ = ["BaseSiteParser"]
