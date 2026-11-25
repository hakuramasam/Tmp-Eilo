"""Application configuration."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_base_url: str = "https://api.openai.com/v1"
    api_key: str = ""
    model: str = ""
    timeout_seconds: float = Field(default=60.0, gt=0)
    max_tool_rounds: int = Field(default=8, ge=1, le=100)
    database_path: str = "./data/eilo-memory.sqlite3"
    system_prompt_path: str = ""

    model_config = SettingsConfigDict(
        env_prefix="EILO_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
