from datetime import datetime
from sqlalchemy import (
    TIMESTAMP,
    String,
    Text,
    Integer,
    Float,
    ForeignKey,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.db.base import Base


class AnalysisSettingsModel(Base):
    __tablename__ = "analysis_settings"

    id: Mapped[int] = mapped_column(primary_key=True)

    scope_type: Mapped[str | None] = mapped_column(Text, nullable=False)

    scope_id: Mapped[int | None] = mapped_column(Integer, nullable=False)

    settings: Mapped[str | None] = mapped_column(Text, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )