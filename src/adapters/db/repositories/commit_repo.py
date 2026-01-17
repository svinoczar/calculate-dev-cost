# src/adapters/db/repositories/commit_repo.py
from sqlalchemy.orm import Session
from src.adapters.db.models.commit import CommitModel

class CommitRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        repository_id: int,
        contributor_id: int | None,
        sha: str,
        message: str
    ) -> CommitModel:
        commit = CommitModel(
            repository_id=repository_id,
            contributor_id=contributor_id,
            sha=sha,
            message=message
        )
        self.db.add(commit)
        self.db.commit()
        self.db.refresh(commit)
        return commit

    def get_by_repo_and_sha(
        self,
        repository_id: int,
        sha: str
    ) -> CommitModel | None:
        return (
            self.db.query(CommitModel)
            .filter_by(repository_id=repository_id, sha=sha)
            .first()
        )

    def get_or_create(
        self,
        repository_id: int,
        sha: str,
        message: str,
        contributor_id: int | None = None,
    ):
        commit = self.get_by_repo_and_sha(repository_id, sha)
        if commit:
            return commit

        return self.create(
            repository_id=repository_id,
            contributor_id=contributor_id,
            sha=sha,
            message=message,
        )
