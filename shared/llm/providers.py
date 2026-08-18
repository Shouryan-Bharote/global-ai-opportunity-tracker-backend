from dataclasses import dataclass
from typing import ClassVar

from shared.config.settings import settings
from shared.llm.models import LLMProvider


@dataclass(frozen=True, slots=True)
class ProviderConfig:
    """Configuration for a specific LLM provider."""

    provider: LLMProvider
    provider_name: str
    api_key_field: str
    default_model: str
    fallback_model: str | None = None


class Providers:
    """Central registry for supported LLM providers."""

    _CONFIGS: ClassVar[dict[LLMProvider, ProviderConfig]] = {
        LLMProvider.GEMINI: ProviderConfig(
            provider=LLMProvider.GEMINI,
            provider_name="gemini",
            api_key_field="gemini_api_key",
            default_model="gemini/gemini-3.6-flash",
            fallback_model="gemini/gemini-3.5-flash",
        ),
        LLMProvider.GROQ: ProviderConfig(
            provider=LLMProvider.GROQ,
            provider_name="groq",
            api_key_field="groq_api_key",
            default_model="groq/groq/compound-mini",
            fallback_model="groq/openai/gpt-oss-120b",
        ),
        LLMProvider.OPENROUTER: ProviderConfig(
            provider=LLMProvider.OPENROUTER,
            provider_name="openrouter",
            api_key_field="openrouter_api_key",
            default_model="openrouter/google/gemini-2.5-flash",
            fallback_model="openrouter/deepseek/deepseek-chat-v3-0324",
        ),
    }

    def __new__(cls) -> "Providers":
        """Prevent instantiation."""
        raise TypeError("Providers cannot be instantiated.")

    @classmethod
    def get(cls, provider: LLMProvider) -> ProviderConfig:
        """Returns the configuration for a provider.

        Args:
            provider: The provider to retrieve.

        Returns:
            The provider configuration.

        Raises:
            ValueError: If the provider is unsupported.
        """
        try:
            return cls._CONFIGS[provider]
        except KeyError as exc:
            raise ValueError(f"Unsupported provider: {provider}") from exc

    @classmethod
    def provider_name(cls, provider: LLMProvider) -> str:
        """Returns the LiteLLM provider identifier."""
        return cls.get(provider).provider_name

    @classmethod
    def api_key(cls, provider: LLMProvider) -> str:
        """Returns the configured API key for a provider."""
        config = cls.get(provider)
        return getattr(settings, config.api_key_field)

    @classmethod
    def has_api_key(cls, provider: LLMProvider) -> bool:
        """Returns whether the provider has an API key configured."""
        return bool(cls.api_key(provider).strip())

    @classmethod
    def default_model(cls, provider: LLMProvider) -> str:
        """Returns the default model for a provider."""
        return cls.get(provider).default_model

    @classmethod
    def fallback_model(cls, provider: LLMProvider) -> str | None:
        """Returns the fallback model for a provider."""
        return cls.get(provider).fallback_model