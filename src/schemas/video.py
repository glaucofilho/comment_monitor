from datetime import datetime

from pydantic import BaseModel, ConfigDict

from core import Platform


class VideoIn(BaseModel):
    """Dados de um vídeo/post vindos da API da plataforma."""

    platform_video_id: str
    platform: Platform
    channel_id: int  # FK já resolvida antes de persistir
    title: str | None = None
    url: str | None = None
    published_at: datetime | None = None


class VideoDB(VideoIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
