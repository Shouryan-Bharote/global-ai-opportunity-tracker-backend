# scraper/scrapers/devpost/profile_manager.py
"""Manages persistence of the Devpost SelectorProfile to disk."""
from __future__ import annotations

import json
from pathlib import Path

from shared.llm.selector_profile import SelectorProfile
from shared.logger import get_logger

logger = get_logger(__name__)

_PROFILES_DIR = Path(__file__).parent / "profiles"
_DEFAULT_PROFILE_PATH = _PROFILES_DIR / "devpost_selectors.json"


class DevpostProfileManager:
    """Handles loading and saving the Devpost SelectorProfile to disk."""

    def __init__(self, file_path: Path = _DEFAULT_PROFILE_PATH) -> None:
        """Initialize DevpostProfileManager.

        Args:
            file_path: Path to the JSON file where profile is stored.
        """
        self._file_path = file_path

    def load(self) -> SelectorProfile | None:
        """Load the cached SelectorProfile from disk if it exists.

        Returns:
            SelectorProfile if valid JSON exists, None otherwise.
        """
        if not self._file_path.exists():
            logger.info("No cached Devpost SelectorProfile found at %s", self._file_path)
            return None

        try:
            raw_text = self._file_path.read_text(encoding="utf-8")
            profile = SelectorProfile.model_validate_json(raw_text)
            logger.info("Loaded cached Devpost SelectorProfile from %s", self._file_path)
            return profile
        except Exception:
            logger.warning(
                "Failed to parse cached Devpost profile at %s — will regenerate.",
                self._file_path,
                exc_info=True,
            )
            return None

    def save(self, profile: SelectorProfile) -> None:
        """Save a SelectorProfile to disk.

        Args:
            profile: The validated SelectorProfile to persist.
        """
        try:
            self._file_path.parent.mkdir(parents=True, exist_ok=True)
            json_data = profile.model_dump_json(indent=2)
            self._file_path.write_text(json_data, encoding="utf-8")
            logger.info("Saved Devpost SelectorProfile to %s", self._file_path)
        except Exception:
            logger.error("Failed to save Devpost profile to %s", self._file_path, exc_info=True)

    def invalidate(self) -> None:
        """Delete the cached profile file if it exists."""
        if self._file_path.exists():
            self._file_path.unlink()
            logger.info("Invalidated Devpost cached profile at %s", self._file_path)
