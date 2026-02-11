from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    groq_api_key: str
    model_name: str
    openweather_api_key: str
    debug: bool


@lru_cache(maxsize=None)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()