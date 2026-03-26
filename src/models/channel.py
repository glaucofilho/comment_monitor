from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Platform
from models import Base


class Channel(Base):
    """Canal/perfil monitorado (YouTube channel ou Instagram user)."""

    __tablename__ = "channels"
    __table_args__ = (
        UniqueConstraint(
            "platform", "platform_channel_id", name="uq_channel_platform"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Identificador da plataforma (ex: UCxxxxxx no YouTube, "123456789" no Instagram)
    platform_channel_id: Mapped[str] = mapped_column(
        String(128), nullable=False, index=True
    )
    platform: Mapped[Platform] = mapped_column(String(32), nullable=False)

    # Metadados descritivos
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    description: Mapped[str | None] = mapped_column(
        String(2048), nullable=True
    )

    # Relacionamentos
    videos: Mapped[list["Video"]] = relationship(
        back_populates="channel", lazy="select"
    )  # noqa: F821

    def __repr__(self) -> str:
        return f"<Channel {self.platform}:{self.platform_channel_id} — {self.name!r}>"
