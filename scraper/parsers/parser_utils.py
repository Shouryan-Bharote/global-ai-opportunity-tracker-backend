from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from enum import Enum
from typing import TypeVar

from pydantic import BaseModel

from scraper.parsers.normalizer import Normalizer

E = TypeVar("E", bound=Enum)
T = TypeVar("T", bound=BaseModel)


class ParserUtils:
    """A collection of generic utilities for parser implementations."""

    def __new__(cls) -> None:
        """Prevents instantiation of the ParserUtils class."""
        raise TypeError("ParserUtils cannot be instantiated.")

    @staticmethod
    def get_string(value: object) -> str | None:
        """Helper to get a normalized string."""
        return Normalizer.normalize_string(value)

    @staticmethod
    def get_list(value: object) -> list[str]:
        """Helper to get a normalized list of strings."""
        return Normalizer.normalize_list(value)

    @staticmethod
    def get_bool(value: object) -> bool | None:
        """Helper to get a normalized boolean."""
        return Normalizer.normalize_boolean(value)

    @staticmethod
    def get_int(value: object) -> int | None:
        """Helper to get a normalized integer."""
        return Normalizer.normalize_integer(value)

    @staticmethod
    def get_float(value: object) -> float | None:
        """Helper to get a normalized float."""
        return Normalizer.normalize_float(value)

    @staticmethod
    def get_url(value: object) -> str | None:
        """Helper to get a normalized URL."""
        return Normalizer.normalize_url(value)

    @staticmethod
    def get_datetime(value: object) -> datetime | None:
        """Helper to get a normalized datetime."""
        return Normalizer.normalize_datetime(value)

    @staticmethod
    def get_enum(
        value: object,
        enum_type: type[E],
        default: E | None = None,
    ) -> E | None:
        """Matches a value to an enum member by name or value.

        Normalization rules:
        - ignore case
        - ignore spaces/whitespace by converting them to underscores
        """
        raw_val = Normalizer.normalize_string(value)
        if not raw_val:
            return default

        normalized = "_".join(raw_val.split()).lower()

        for member in enum_type:
            member_name = "_".join(member.name.split()).lower()
            member_value = "_".join(str(member.value).split()).lower()

            if member_name == normalized:
                return member
            if member_value == normalized:
                return member

        return default

    @staticmethod
    def safe_get(
        data: object,
        key: str,
        default: object = None,
    ) -> object:
        """Mapping-safe getter for parser inputs.

        Equivalent to:
            data.get(key, default)
        but validates that the object is a Mapping.
        """
        if not isinstance(data, Mapping):
            return default
        return data.get(key, default)

    @staticmethod
    def build_model(data: object, model: type[T]) -> T | None:
        """Constructs a Pydantic model from a dictionary or existing instance."""
        if data is None:
            return None

        if isinstance(data, model):
            return data

        if isinstance(data, dict):
            return model(**data)

        raise TypeError(f"Data must be a dictionary or instance of {model.__name__}")

    @staticmethod
    def build_models(data: object, model: type[T]) -> list[T]:
        """Builds multiple Pydantic models using build_model().

        Behavior:
        - None -> []
        - list/tuple -> convert every element
        - existing model instance -> wrap in list
        - invalid element -> raise TypeError
        """
        if data is None:
            return []

        if isinstance(data, (list, tuple)):
            out: list[T] = []
            for item in data:
                built = ParserUtils.build_model(item, model)
                if built is None:
                    raise TypeError(
                        f"Invalid element type for {model.__name__}: {type(item).__name__}"
                    )
                out.append(built)
            return out

        if isinstance(data, model):
            return [data]

        # For single values, allow build_model() to raise TypeError for invalid elements.
        built = ParserUtils.build_model(data, model)
        if built is None:
            raise TypeError(
                f"Invalid element type for {model.__name__}: {type(data).__name__}"
            )
        return [built]


__all__ = ["ParserUtils"]
