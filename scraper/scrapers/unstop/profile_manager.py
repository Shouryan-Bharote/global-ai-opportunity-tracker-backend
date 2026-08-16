# scraper/scrapers/unstop/profile_manager.py
"""Manages persistence of the Unstop SelectorProfile to disk."""
from __future__ import annotations

import json
from pathlib import Path

from shared.llm.selector_profile import SelectorProfile
from shared.logger import get_logger

logger = get_logger(__name__)

# Profile is stored next to this file in profiles/hackathon_listing.json
_PROFILES_DIR = Path(__file__).parent / "profiles"
_PROFILE_PATH = _PROFILES_DIR / "hackathon_listing.json"


class UnstopProfileManager:
    """Loads and saves the Unstop SelectorProfile to a local JSON file.

    Keeping the profile on disk means the LLM is only called once (or when
    the profile is explicitly invalidated), making normal scrape runs fast
    and free of LLM costs.
    """

    def load(self) -> SelectorProfile | None:
        """Load the SelectorProfile from disk.

        Returns:
            The loaded profile, or None if no profile file exists.
        """
        if not _PROFILE_PATH.exists():
            logger.debug("No cached profile found at %s.", _PROFILE_PATH)
            return None

        try:
            raw = _PROFILE_PATH.read_text(encoding="utf-8")
            profile = SelectorProfile.model_validate_json(raw)
            logger.debug("Loaded SelectorProfile from %s.", _PROFILE_PATH)
            return profile
        except Exception:
            logger.warning(
                "Failed to load SelectorProfile from %s — will regenerate.",
                _PROFILE_PATH,
                exc_info=True,
            )
            return None

    def save(self, profile: SelectorProfile) -> None:
        """Save a SelectorProfile to disk.

        Args:
            profile: The profile to persist.
        """
        _PROFILES_DIR.mkdir(parents=True, exist_ok=True)
        try:
            _PROFILE_PATH.write_text(
                profile.model_dump_json(indent=2),
                encoding="utf-8",
            )
            logger.debug("Saved SelectorProfile to %s.", _PROFILE_PATH)
        except Exception:
            logger.warning(
                "Failed to save SelectorProfile to %s.",
                _PROFILE_PATH,
                exc_info=True,
            )

    def invalidate(self) -> None:
        """Delete the cached profile, forcing regeneration on the next run."""
        if _PROFILE_PATH.exists():
            _PROFILE_PATH.unlink()
            logger.info("Invalidated cached Unstop SelectorProfile.")
        else:
            logger.debug("No cached profile to invalidate.")
