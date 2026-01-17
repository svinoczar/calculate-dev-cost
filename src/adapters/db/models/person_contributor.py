from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from adapters.db.base import Base


class PersonContributorModel(Base):
    __tablename__ = "person_contributors"

    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), primary_key=True)
    contributor_id: Mapped[int] = mapped_column(
        ForeignKey("contributors.id"), primary_key=True
    )
