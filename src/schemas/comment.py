from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from core import Platform


class CommentIn(BaseModel):
    """
    Dados brutos de um comentário vindos da API.
    Usado como contrato entre o Collector e o Repository.
    """

    platform_comment_id: str
    platform: Platform
    channel_id: int
    video_id: int
    parent_platform_comment_id: str | None = None

    author_id: str | None = None
    author_name: str | None = None
    text: str = Field(..., min_length=1)
    like_count: int = Field(default=0, ge=0)
    published_at: datetime | None = None


class CommentDB(CommentIn):
    """Comentário já persistido — inclui campos de controle do banco."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    deleted_at: datetime | None = None
    last_seen_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None


class DeletedCommentOut(BaseModel):
    """
    Shape exportado para o Power BI.
    Representa um comentário confirmado como deletado.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    platform: Platform
    channel_id: int
    video_id: int
    platform_comment_id: str
    author_name: str | None
    text: str
    like_count: int
    published_at: datetime | None
    deleted_at: datetime
    # Duração em segundos que o comentário ficou visível antes de ser apagado
    visible_for_seconds: float | None = None
