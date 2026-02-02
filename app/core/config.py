from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment / .env file."""

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./todo.db"

    # Security / Auth
    SECRET_KEY: str = "CHANGE_ME_IN_ENV"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    OTP_EXPIRE_MINUTES: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings so we don't re-read env on every request."""

    return Settings()
