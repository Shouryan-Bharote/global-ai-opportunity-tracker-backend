from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from shared.constants.logging import LogLevel

class Settings(BaseSettings):
    """
    Global application settings.
    Values are automatically loaded from the .env file.
    """

    # ======================
    # Application
    # ======================

    app_name: str = "TrackIT Backend"
    debug: bool = False
    log_level: LogLevel = LogLevel.INFO    
    environment: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list[str] = ["*"]

    # ======================
    # API Keys — Built-in Providers
    # ======================

    gemini_api_key: str = ""
    groq_api_key: str = ""
    openrouter_api_key: str = ""

    # NVIDIA NIM (api.nvidia.com) — OpenAI-compatible
    nvidia_api_key: str = ""
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"
    nvidia_default_model: str = "nvidia/llama-3.1-nemotron-ultra-253b-v1"

    # ======================
    # Custom / Bring-Your-Own Provider
    # Set these to use any OpenAI-compatible API endpoint
    # (e.g. Ollama, Together AI, Anyscale, OpenRouter custom org, etc.)
    # ======================

    custom_api_key: str = ""
    custom_base_url: str = ""          # e.g. http://localhost:11434/v1
    custom_provider_name: str = "openai"  # LiteLLM provider prefix
    custom_default_model: str = ""     # e.g. ollama/mistral or openai/gpt-4o

    # ======================
    # LLM Fallback Chain
    # Comma-separated ordered list of providers to try.
    # If empty, auto-detects from whichever keys are set.
    # Example: "groq,nvidia,gemini" or "openrouter,custom"
    # ======================

    llm_provider_chain: str = ""

    # ======================
    # Database (SQLModel)
    # ======================

    database_url: str = ""
    sqlmodel_database_url: str = "sqlite:///./opportunities.db"
    sqlmodel_echo: bool = False
    sqlmodel_connect_args: dict = {"check_same_thread": False}

    @model_validator(mode="after")
    def _normalize_database_url(self) -> "Settings":
        url = self.database_url or self.sqlmodel_database_url
        if url:
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql+psycopg2://", 1)
            elif url.startswith("postgresql://") and not url.startswith("postgresql+"):
                url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
            self.sqlmodel_database_url = url
        return self

    # ======================
    # Pydantic Configuration
    # ======================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
