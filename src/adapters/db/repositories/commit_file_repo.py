from sqlalchemy.orm import Session

from src.adapters.db.base import Base
from src.adapters.db.models.commit_file import CommitFileModel


class CommitFileRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def delete_by_commit_id(self, commit_id: int):
        self.db.query(CommitFileModel)\
            .filter(CommitFileModel.commit_id == commit_id)\
            .delete()

    def bulk_create(self, files: list[CommitFileModel]):
        self.db.add_all(files)
