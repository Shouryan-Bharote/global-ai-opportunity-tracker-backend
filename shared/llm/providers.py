from dataclasses import dataclass
from typing import ClassVar

from shared.llm.models import LLMProvider


@dataclass(frozen=True)
class ProviderConfig:
    """Configuration for a specific LLM provider."""

    provider: LLMProvider
    default_model: str
    fallback_model: str | None = None


class Providers:
    """Central registry for supported LLM providers and their models."""

    _configs: ClassVar[dict[LLMProvider, ProviderConfig]] = {
        LLMProvider.GEMINI: ProviderConfig(
            provider=LLMProvider.GEMINI,
            default_model="gemini/gemini-2.5-flash",
            fallback_model="gemini/gemini-2.5-pro",
        ),
        LLMProvider.GROQ: ProviderConfig(
            provider=LLMProvider.GROQ,
            default_model="groq/llama-3.3-70b-versatile",
            fallback_model="groq/deepseek-r1-distill-llama-70b",
        ),
        LLMProvider.OPENROUTER: ProviderConfig(
            provider=LLMProvider.OPENROUTER,
            default_model="openrouter/google/gemini-2.5-flash",
            fallback_model="openrouter/deepseek/deepseek-chat-v3-0324",
        ),
    }

    def __new__(cls) -> "Providers":
        """Prevents instantiation of the Providers class."""
        raise TypeError("Providers cannot be instantiated.")

    @classmethod
    def get(cls, provider: LLMProvider) -> ProviderConfig:
        """Returns the configuration for the specified provider.

        Args:
            provider: The LLM provider.

        Returns:
            The provider configuration.

        Raises:
            ValueError: If the provider is not supported.
        """
        try:
            return cls._configs[provider]
        except KeyError as exc:
            raise ValueError(f"Unsupported provider: {provider}") from exc

    @classmethod
    def default_model(cls, provider: LLMProvider) -> str:
        """Returns the default model for a provider."""
        return cls.get(provider).default_model

    @classmethod
    def fallback_model(cls, provider: LLMProvider) -> str | None:
        """Returns the fallback model for a provider."""
        return cls.get(provider).fallback_model