import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn, RedisDsn
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    """
    Advanced Configuration settings using Pydantic Settings.
    Environment variables are automatically mapped (e.g., APP_NAME -> app_name).
    """
    # --- Project Metadata ---
    APP_NAME: str = Field(default="WikiKisan Backend")
    DEBUG: bool = Field(default=False)
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = Field(..., description="Used for JWT and security hashing")

    # --- Database Settings ---
    # Using PostgresDsn ensures the URL is a valid database connection string
    DATABASE_URL: Optional[str] = Field(default="mongodb://localhost:27017/wikikisan")
    REDIS_URL: Optional[str] = None

    # --- External API Keys ---
    OPENWEATHER_API_KEY: Optional[str] = None
    AGMARKNET_API_KEY: Optional[str] = None

    # --- Pydantic Configuration ---
    # Tells Pydantic to read from a .env file if it exists
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,  # Keeps names strictly matching (e.g., DEBUG != debug)
        extra="ignore"        # Ignores extra variables in the .env file
    )

@lru_cache
def get_settings() -> Settings:
    """
    Using lru_cache ensures the settings are only loaded once.
    This improves performance significantly for high-traffic APIs.
    """
    return Settings()

# Global instance for easy access
settings = get_settings()
