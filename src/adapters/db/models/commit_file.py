from sqlalchemy import (
    String,
    Text,
    Integer,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column

from adapters.db.base import Base


class CommitFileModel(Base):
    __tablename__ = "commit_files"

    id: Mapped[int] = mapped_column(primary_key=True)

    commit_id: Mapped[int] = mapped_column(ForeignKey("commits.id"), nullable=False)

    file_path: Mapped[str] = mapped_column(Text, nullable=False)

    additions: Mapped[int | None] = mapped_column(Integer, nullable=True)
    deletions: Mapped[int | None] = mapped_column(Integer, nullable=True)
    changes: Mapped[int | None] = mapped_column(Integer, nullable=True)

    language: Mapped[str | None] = mapped_column(Text, nullable=True)
    language_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)

    patch: Mapped[str | None] = mapped_column(Text, nullable=True)
