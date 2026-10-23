"""Dynamic LLM provider registry.

Supports any OpenAI-compatible provider through the CUSTOM slot.
New built-in providers (NVIDIA, etc.) are added here; the rest of the
codebase needs no changes.

Priority / fallback order is controlled by the ``LLM_PROVIDER_CHAIN``
env var (comma-separated, e.g. ``groq,nvidia,gemini``).  If that var is
empty the chain is auto-resolved from whichever API keys are present.
"""

from __future__ import annotations

from dataclasses import dataclass

from shared.config.settings import settings
from shared.llm.models import LLMProvider


@dataclass(frozen=True, slots=True)
class ProviderConfig:
    """Full runtime configuration for one LLM provider."""

    provider: LLMProvider
    provider_name: str         # LiteLLM ``custom_llm_provider`` identifier
    api_key: str
    default_model: str
    fallback_model: str | None = None
    base_url: str | None = None    # Only needed for non-standard endpoints


def _build_registry() -> dict[LLMProvider, ProviderConfig]:
    """Constructs the provider registry from current settings."""
    return {
        # ------------------------------------------------------------------ #
        #  Gemini                                                              #
        # ------------------------------------------------------------------ #
        LLMProvider.GEMINI: ProviderConfig(
            provider=LLMProvider.GEMINI,
            provider_name="gemini",
            api_key=settings.gemini_api_key,
            default_model="gemini/gemini-2.5-flash",
            fallback_model="gemini/gemini-2.0-flash",
        ),
        # ------------------------------------------------------------------ #
        #  Groq                                                                #
        # ------------------------------------------------------------------ #
        LLMProvider.GROQ: ProviderConfig(
            provider=LLMProvider.GROQ,
            provider_name="groq",
            api_key=settings.groq_api_key,
            default_model="groq/compound-beta-mini",
            fallback_model="groq/llama-3.3-70b-versatile",
        ),
        # ------------------------------------------------------------------ #
        #  OpenRouter                                                          #
        # ------------------------------------------------------------------ #
        LLMProvider.OPENROUTER: ProviderConfig(
            provider=LLMProvider.OPENROUTER,
            provider_name="openrouter",
            api_key=settings.openrouter_api_key,
            default_model="openrouter/google/gemini-2.5-flash",
            fallback_model="openrouter/deepseek/deepseek-chat-v3-0324",
        ),
        # ------------------------------------------------------------------ #
        #  NVIDIA NIM  (api.nvidia.com — OpenAI-compatible)                   #
        # ------------------------------------------------------------------ #
        LLMProvider.NVIDIA: ProviderConfig(
            provider=LLMProvider.NVIDIA,
            provider_name="openai",        # LiteLLM treats NVIDIA NIM as openai
            api_key=settings.nvidia_api_key,
            default_model=settings.nvidia_default_model,
            fallback_model=None,
            base_url=settings.nvidia_base_url,
        ),
        # ------------------------------------------------------------------ #
        #  Custom / Bring-Your-Own (any OpenAI-compatible endpoint)           #
        # ------------------------------------------------------------------ #
        LLMProvider.CUSTOM: ProviderConfig(
            provider=LLMProvider.CUSTOM,
            provider_name=settings.custom_provider_name or "openai",
            api_key=settings.custom_api_key,
            default_model=settings.custom_default_model,
            fallback_model=None,
            base_url=settings.custom_base_url or None,
        ),
    }


class Providers:
    """Central registry for supported LLM providers.

    Usage
    -----
    >>> config = Providers.get(LLMProvider.NVIDIA)
    >>> chain   = Providers.resolve_chain()   # ordered list of available providers
    """

    # Registry is lazily rebuilt on first access so tests can monkeypatch
    # settings before the module loads.
    _registry: dict[LLMProvider, ProviderConfig] | None = None

    def __new__(cls) -> "Providers":
        """Prevent instantiation — this is a pure namespace class."""
        raise TypeError("Providers cannot be instantiated.")

    # ------------------------------------------------------------------ #
    #  Internal helpers                                                    #
    # ------------------------------------------------------------------ #

    @classmethod
    def _get_registry(cls) -> dict[LLMProvider, ProviderConfig]:
        if cls._registry is None:
            cls._registry = _build_registry()
        return cls._registry

    @classmethod
    def _reload(cls) -> None:
        """Force-rebuild the registry (useful in tests / after settings change)."""
        cls._registry = _build_registry()

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    @classmethod
    def get(cls, provider: LLMProvider) -> ProviderConfig:
        """Returns the configuration for *provider*.

        Raises
        ------
        ValueError
            If the provider is not in the registry.
        """
        try:
            return cls._get_registry()[provider]
        except KeyError as exc:
            raise ValueError(f"Unsupported provider: {provider!r}") from exc

    @classmethod
    def has_api_key(cls, provider: LLMProvider) -> bool:
        """Returns ``True`` if an API key is configured for *provider*."""
        return bool(cls.get(provider).api_key.strip())

    @classmethod
    def resolve_chain(cls) -> list[LLMProvider]:
        """Returns an ordered list of *available* providers to use as fallback chain.

        Resolution order
        ----------------
        1. If ``LLM_PROVIDER_CHAIN`` is set in the environment, parse it as a
           comma-separated list of provider names (e.g. ``"groq,nvidia,gemini"``).
           Only providers that actually have an API key are kept.
        2. Otherwise auto-detect: return all providers that have an API key
           in a sensible default order (Groq → OpenRouter → NVIDIA → Gemini → Custom).

        Returns
        -------
        list[LLMProvider]
            Ordered list of ready-to-use providers, or an empty list if none
            have API keys configured.
        """
        raw_chain = settings.llm_provider_chain.strip()

        if raw_chain:
            # Parse user-specified chain
            chain: list[LLMProvider] = []
            for name in raw_chain.split(","):
                name = name.strip().lower()
                try:
                    p = LLMProvider(name)
                    if cls.has_api_key(p):
                        chain.append(p)
                except ValueError:
                    from shared.logger import logger  # local import to avoid circular
                    logger.warning(
                        "Unknown provider %r in LLM_PROVIDER_CHAIN — skipping.", name
                    )
            return chain

        # Auto-detect: sensible default priority order
        default_order: list[LLMProvider] = [
            LLMProvider.GROQ,
            LLMProvider.OPENROUTER,
            LLMProvider.NVIDIA,
            LLMProvider.GEMINI,
            LLMProvider.CUSTOM,
        ]
        return [p for p in default_order if cls.has_api_key(p)]

    # ------------------------------------------------------------------ #
    #  Convenience accessors (backwards-compatible with old callers)      #
    # ------------------------------------------------------------------ #

    @classmethod
    def provider_name(cls, provider: LLMProvider) -> str:
        """Returns the LiteLLM provider identifier string."""
        return cls.get(provider).provider_name

    @classmethod
    def api_key(cls, provider: LLMProvider) -> str:
        """Returns the configured API key for *provider*."""
        return cls.get(provider).api_key

    @classmethod
    def default_model(cls, provider: LLMProvider) -> str:
        """Returns the default model identifier for *provider*."""
        return cls.get(provider).default_model

    @classmethod
    def fallback_model(cls, provider: LLMProvider) -> str | None:
        """Returns the fallback model for *provider*, or ``None``."""
        return cls.get(provider).fallback_model