"""Telegram bot config"""

from pydantic import Field, HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Bot settings class."""

    bot_token: SecretStr
    service_uri: HttpUrl = Field(default="http://51.250.97.70:5000/")
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings()
