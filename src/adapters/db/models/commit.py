from datetime import datetime
from sqlalchemy import Boolean, Integer, String, Text, TIMESTAMP, Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.db.base import Base


class CommitModel(Base):
    __tablename__ = "commits"

    id: Mapped[int] = mapped_column(primary_key=True)

    repository_id: Mapped[int] = mapped_column(
        ForeignKey("repositories.id"), nullable=False
    )

    contributor_id: Mapped[int | None] = mapped_column(
        ForeignKey("contributors.id"), nullable=True
    )

    sha: Mapped[str] = mapped_column(Text, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)

    authored_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    committed_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )

    author_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    author_email: Mapped[str | None] = mapped_column(Text, nullable=True)

    additions: Mapped[int | None] = mapped_column(Integer, nullable=True)
    deletions: Mapped[int | None] = mapped_column(Integer, nullable=True)
    changes: Mapped[int | None] = mapped_column(Integer, nullable=True)

    commit_type: Mapped[str | None] = mapped_column(Text, nullable=True)
    commit_type_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)

    is_enriched: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )