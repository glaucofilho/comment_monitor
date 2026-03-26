from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    """Base declarativa compartilhada por todos os models."""

    created_at: Mapped[datetime] = mapped_column(
        default=utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=utcnow,
        server_default=func.now(),
        onupdate=utcnow,
        nullable=False,
    )
