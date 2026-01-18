# src/adapters/db/repositories/commit_repo.py
from datetime import datetime
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

    def get_commits_for_update(
        self,
        repository_id: int,
        limit: int,
        since: datetime | None = None,
    ) -> list[CommitModel]:
        query = self.db.query(CommitModel).filter(
            CommitModel.repository_id == repository_id,
            CommitModel.commit_type.is_(None)
        )
        if since:
            query = query.filter(CommitModel.authored_at >= since)
        return query.limit(limit).all()


    def update_details(
        self,
        commit_id: int,
        *,
        authored_at,
        committed_at,
        author_name: str | None,
        author_email: str | None,
        additions: int | None,
        deletions: int | None,
        changes: int | None,
        commit_type: str | None,
        commit_type_confidence: float | None,
    ):
        commit = self.db.get(CommitModel, commit_id)
        if not commit:
            return

        commit.authored_at = authored_at
        commit.committed_at = committed_at
        commit.author_name = author_name
        commit.author_email = author_email
        commit.additions = additions
        commit.deletions = deletions
        commit.changes = changes
        commit.commit_type = commit_type
        commit.commit_type_confidence = commit_type_confidence

        self.db.commit()
