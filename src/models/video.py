from datetime import datetime

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Platform
from models import Base


class Video(Base):
    """Vídeo/post monitorado dentro de um canal."""

    __tablename__ = "videos"
    __table_args__ = (
        UniqueConstraint(
            "platform", "platform_video_id", name="uq_video_platform"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    channel_id: Mapped[int] = mapped_column(
        ForeignKey("channels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    platform_video_id: Mapped[str] = mapped_column(
        String(128), nullable=False, index=True
    )
    platform: Mapped[Platform] = mapped_column(String(32), nullable=False)

    title: Mapped[str | None] = mapped_column(String(512), nullable=True)
    url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(nullable=True)

    # Relacionamentos
    channel: Mapped["Channel"] = relationship(
        back_populates="videos"
    )  # noqa: F821
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="video", lazy="select"
    )  # noqa: F821

    def __repr__(self) -> str:
        return f"<Video {self.platform}:{self.platform_video_id} — {self.title!r}>"
