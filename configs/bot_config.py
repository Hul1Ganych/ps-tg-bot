"""Telegram bot config"""

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Bot settings class."""

    bot_token: SecretStr
    service_uri: str = Field(default="http://0.0.0.0:5000/")
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings()
