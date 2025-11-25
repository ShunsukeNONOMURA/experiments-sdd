from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR.parent.parent / "docker" / ".env", override=False)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)

    app_name: str = Field(default="User Management API", alias="APP_NAME")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    database_url: str = Field(
        default="postgresql+psycopg://um_user:um_pass@localhost:5432/um_db",
        alias="DATABASE_URL",
    )
    pagination_default_limit: int = Field(default=20, alias="PAGINATION_DEFAULT_LIMIT")
    pagination_max_limit: int = Field(default=100, alias="PAGINATION_MAX_LIMIT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    enable_metrics: bool = Field(default=True, alias="ENABLE_METRICS")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()


settings = get_settings()
