from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AudioFile(Base):
    __tablename__ = "audio_files"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    owner_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
    )

    object_name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
    )

    content_type: Mapped[str] = mapped_column(
        String(100),
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="uploaded",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
