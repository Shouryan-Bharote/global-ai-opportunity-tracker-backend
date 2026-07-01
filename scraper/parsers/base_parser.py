from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from pydantic import BaseModel
from shared.logger import get_logger

T = TypeVar("T", bound=BaseModel)
logger = get_logger(__name__)


class BaseParser(ABC, Generic[T]):
    """Abstract base class for all parsers in the scraping pipeline.

    This class defines a consistent interface for converting raw data into
    structured Pydantic models. Subclasses are responsible for implementing
    the transformation logic.
    """

    @abstractmethod
    def parse(self, data: object) -> T:
        """Parses the input data into the target model type.

        Subclasses may invoke _validate() and _preprocess() before performing the parsing operation.

        Args:
            data: The raw input data to be parsed.

        Returns:
            The parsed data in the specified target model type.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses must implement the parse method.")

    def _validate(self, data: object) -> None:
        """Validate raw input before parsing.

        Args:
            data: The raw input data to be validated.
        """
        return None

    def _preprocess(self, data: object) -> object:
        """Preprocess raw input before parsing.

        Args:
            data: The raw input data to be preprocessed.

        Returns:
            The preprocessed input data.
        """
        return data
