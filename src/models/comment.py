from datetime import datetime

from sqlalchemy import ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Platform
from models import Base


class Comment(Base):
    """
    Comentário coletado de um vídeo/post.

    Lógica de detecção de deleção:
      - deleted_at IS NULL  → comentário ainda visível na API
      - deleted_at NOT NULL → comentário não retornado pela API na última verificação
    """

    __tablename__ = "comments"
    __table_args__ = (
        UniqueConstraint(
            "platform", "platform_comment_id", name="uq_comment_platform"
        ),
        # Índice composto para a query de detecção de deleção:
        # WHERE video_id = ? AND deleted_at IS NULL
        Index("ix_comments_video_active", "video_id", "deleted_at"),
        # Índice para o PBI filtrar por canal + período
        Index("ix_comments_channel_deleted", "channel_id", "deleted_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # ── Chaves estrangeiras ───────────────────────────────────────
    channel_id: Mapped[int] = mapped_column(
        ForeignKey("channels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    video_id: Mapped[int] = mapped_column(
        ForeignKey("videos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Identificação na plataforma ───────────────────────────────
    platform_comment_id: Mapped[str] = mapped_column(
        String(128), nullable=False, index=True
    )
    platform: Mapped[Platform] = mapped_column(String(32), nullable=False)

    # ID do comentário pai (para respostas/replies)
    parent_platform_comment_id: Mapped[str | None] = mapped_column(
        String(128), nullable=True
    )

    # ── Conteúdo — preservado mesmo após deleção ──────────────────
    author_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    author_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    like_count: Mapped[int] = mapped_column(default=0, nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(nullable=True)

    # ── Controle de deleção ───────────────────────────────────────
    # Preenchido quando o comentário some da API
    deleted_at: Mapped[datetime | None] = mapped_column(
        nullable=True, default=None
    )
    # Snapshot do like_count e texto na última vez que foi visto na API
    last_seen_at: Mapped[datetime | None] = mapped_column(nullable=True)

    # ── Relacionamentos ───────────────────────────────────────────
    video: Mapped["Video"] = relationship(
        back_populates="comments"
    )  # noqa: F821

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def __repr__(self) -> str:
        status = "DELETED" if self.is_deleted else "active"
        return (
            f"<Comment {self.platform}:{self.platform_comment_id} "
            f"[{status}] by {self.author_name!r}>"
        )
