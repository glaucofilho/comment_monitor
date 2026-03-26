from enum import StrEnum
from functools import lru_cache

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Platform(StrEnum):
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Database ────────────────────────────────────────────────
    database_url: PostgresDsn = Field(
        default="postgresql+psycopg://sa:1234@localhost:5432/comment_monitor"
    )

    # ── YouTube ─────────────────────────────────────────────────
    youtube_api_key: str = Field(default="")
    # IDs dos canais a monitorar, separados por vírgula no .env
    # ex: YOUTUBE_CHANNEL_IDS=UCxxxx,UCyyyy
    youtube_channel_ids: list[str] = Field(default_factory=list)

    @field_validator("youtube_channel_ids", mode="before")
    @classmethod
    def split_channel_ids(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return [ch.strip() for ch in v.split(",") if ch.strip()]
        return v

    # ── Instagram ────────────────────────────────────────────────
    instagram_access_token: str = Field(default="")
    instagram_user_ids: list[str] = Field(default_factory=list)

    @field_validator("instagram_user_ids", mode="before")
    @classmethod
    def split_user_ids(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return [u.strip() for u in v.split(",") if u.strip()]
        return v

    # ── Scheduler ────────────────────────────────────────────────
    # Intervalo entre coletas (em minutos)
    poll_interval_minutes: int = Field(default=30, ge=5, le=1440)
    # Quantos dias para trás monitorar
    lookback_days: int = Field(default=30, ge=1, le=90)
    # Máximo de comentários por vídeo por chamada
    max_comments_per_video: int = Field(default=500, ge=50, le=2000)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
