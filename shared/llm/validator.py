from shared.llm.exceptions import LLMValidationError
from shared.llm.selector_profile import (
    ExtractionType,
    SelectorProfile,
)
from shared.logger import logger


class SelectorProfileValidator:
    """Validator for SelectorProfile models."""

    def __init__(self) -> None:
        raise TypeError("SelectorProfileValidator is not instantiable.")

    @staticmethod
    def validate(profile: SelectorProfile) -> None:
        """Validates a SelectorProfile.

        Args:
            profile: The SelectorProfile to validate.

        Raises:
            LLMValidationError: If validation fails.
        """
        logger.debug(
            "Validating selector profile for website=%s page_type=%s",
            profile.website,
            profile.page_type,
        )

        if not profile.website.strip():
            raise LLMValidationError("Website cannot be empty.")

        if not profile.page_type.strip():
            raise LLMValidationError("Page type cannot be empty.")

        if not profile.fields:
            raise LLMValidationError(
                "Selector profile must contain at least one extraction field."
            )

        field_names: set[str] = set()

        for field in profile.fields:
            field_name = field.name.strip()

            if not field_name:
                raise LLMValidationError("Field name cannot be empty.")

            if field_name in field_names:
                raise LLMValidationError(
                    f"Duplicate field name '{field_name}'."
                )

            field_names.add(field_name)

            if not field.selectors:
                raise LLMValidationError(
                    f"Field '{field_name}' must define at least one selector."
                )

            priorities = [selector.priority for selector in field.selectors]

            if len(priorities) != len(set(priorities)):
                raise LLMValidationError(
                    f"Duplicate selector priorities found in field '{field_name}'."
                )

            for selector in field.selectors:
                if not selector.value.strip():
                    raise LLMValidationError(
                        f"Empty selector value found in field '{field_name}'."
                    )

            if field.extraction_type == ExtractionType.ATTRIBUTE:
                if not field.attribute or not field.attribute.strip():
                    raise LLMValidationError(
                        f"Field '{field_name}' requires an attribute name."
                    )

            elif field.attribute:
                raise LLMValidationError(
                    f"Field '{field_name}' must not define an attribute for "
                    f"{field.extraction_type.value} extraction."
                )

        logger.debug(
            "Selector profile validation completed successfully."
        )