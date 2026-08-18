# shared/llm/parser.py

import json
import re
import time
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

from shared.llm.exceptions import (
    LLMResponseParseError,
    LLMValidationError,
)
from shared.llm.selector_profile import SelectorProfile
from shared.logger import logger

T = TypeVar("T", bound=BaseModel)


class ResponseParser:
    """Generic parser for converting raw LLM responses into validated Pydantic models."""

    @classmethod
    def parse(cls, raw_response: str, model: type[T]) -> T:
        """Parses a raw LLM response into the specified Pydantic model.

        Args:
            raw_response: Raw response returned by the LLM.
            model: Target Pydantic model.

        Returns:
            A validated instance of the requested model.

        Raises:
            LLMResponseParseError: If the response cannot be parsed as JSON.
            LLMValidationError: If the JSON does not satisfy the model schema.
        """
        logger.debug("Parsing LLM response into model=%s", model.__name__)

        start_time = time.perf_counter()

        stripped = cls._strip_thinking_tags(raw_response)
        
        # Try to find and extract a markdown code block first (e.g. ```json ... ```)
        json_str = cls._extract_markdown_code_block(stripped)
        if not json_str:
            cleaned = cls._strip_markdown(stripped)
            json_str = cls._extract_json(cleaned)

        data = cls._load_json(json_str)
        instance = cls._validate(data, model)

        elapsed = time.perf_counter() - start_time

        logger.debug(
            "Successfully parsed model=%s in %.3f seconds",
            model.__name__,
            elapsed,
        )

        return instance

    @classmethod
    def parse_selector_profile(cls, raw_response: str) -> SelectorProfile:
        """Convenience method for parsing a SelectorProfile."""
        return cls.parse(raw_response, SelectorProfile)

    @staticmethod
    def _extract_markdown_code_block(text: str) -> str | None:
        """Finds and extracts the first markdown code block content.

        Prioritizes ```json blocks over other code fences to prevent matching
        HTML snippets repeated by the LLM.
        """
        # First try explicit JSON blocks
        match = re.search(r"```json\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
            
        # Fall back to general blocks but avoid matching HTML blocks
        match = re.search(r"```(?!html|xml|css|javascript|typescript|python)[a-zA-Z]*\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
            
        return None

    @staticmethod
    def _strip_thinking_tags(text: str) -> str:
        """Removes <think>...</think> blocks emitted by reasoning models (e.g. Qwen, DeepSeek-R1).

        These blocks contain the model's chain-of-thought and must be removed
        before JSON extraction, as they often contain JSON-like fragments that
        confuse the extractor.
        """
        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

    @staticmethod
    def _strip_markdown(text: str) -> str:
        """Removes Markdown code fences from the response."""
        return re.sub(
            r"^```[a-zA-Z]*\n?|\n?```$",
            "",
            text.strip(),
            flags=re.MULTILINE,
        )

    @staticmethod
    def _extract_json(text: str) -> str:
        """Extracts the first complete JSON object or array."""

        object_start = text.find("{")
        array_start = text.find("[")

        if object_start == -1 and array_start == -1:
            raise LLMResponseParseError("No JSON object or array found in response.")

        if object_start == -1:
            start = array_start
            opening, closing = "[", "]"
        elif array_start == -1:
            start = object_start
            opening, closing = "{", "}"
        else:
            if object_start < array_start:
                start = object_start
                opening, closing = "{", "}"
            else:
                start = array_start
                opening, closing = "[", "]"

        depth = 0

        for index in range(start, len(text)):
            char = text[index]

            if char == opening:
                depth += 1
            elif char == closing:
                depth -= 1

                if depth == 0:
                    return text[start : index + 1]

        raise LLMResponseParseError("Incomplete JSON structure found in response.")

    @staticmethod
    def _load_json(json_str: str) -> Any:
        """Loads a JSON string into a Python object."""
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as exc:
            logger.error("Failed to decode JSON. json_str: %s", repr(json_str))
            logger.exception("Failed to decode JSON from LLM response.")
            raise LLMResponseParseError(
                f"Invalid JSON received: {exc}"
            ) from exc

    @staticmethod
    def _validate(data: Any, model: type[T]) -> T:
        """Validates parsed JSON against the specified Pydantic model."""
        try:
            return model.model_validate(data)
        except ValidationError as exc:
            logger.exception(
                "Validation failed for model=%s",
                model.__name__,
            )
            raise LLMValidationError(
                f"{model.__name__} validation failed:\n{exc}"
            ) from exc