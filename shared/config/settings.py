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

    # ======================
    # API Keys
    # ======================

    google_ai_api_key: str = ""
    groq_api_key: str = ""

    # ======================
    # Future Database
    # ======================

    database_url: str = ""

    # ======================
    # Browser
    # ======================

    headless: bool = True

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