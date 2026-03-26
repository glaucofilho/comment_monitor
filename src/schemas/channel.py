from datetime import datetime

from pydantic import BaseModel, ConfigDict

from core import Platform


class ChannelIn(BaseModel):
    """Dados de um canal vindos da API da plataforma."""

    platform_channel_id: str
    platform: Platform
    name: str
    url: str | None = None
    description: str | None = None


class ChannelDB(ChannelIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
