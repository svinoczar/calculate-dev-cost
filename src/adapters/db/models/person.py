from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text

from adapters.db.base import Base


class PersonModel(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str | None] = mapped_column(Text, nullable=True)
