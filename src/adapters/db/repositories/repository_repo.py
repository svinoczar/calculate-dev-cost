from sqlalchemy.orm import Session

from src.adapters.db.base import Base
from src.adapters.db.models.repository import RepositoryModel


class RepositoryRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_by_owner_name(self, owner: str, name: str, vcs_provider: str = "github") -> RepositoryModel | None:
        return (
            self.db.query(RepositoryModel)
            .filter_by(owner=owner, name=name, vcs_provider=vcs_provider)
            .first()
        )

    def create(
        self,
        owner: str,
        name: str,
        vcs_provider: str,
        external_id: str | None,
        url: str,
    ) -> RepositoryModel:
        repo = RepositoryModel(
            owner=owner,
            name=name,
            vcs_provider=vcs_provider,
            external_id=external_id,
            url=url,
        )
        self.db.add(repo)
        try:
            self.db.commit()
        except:
            self.db.rollback()
            raise
        self.db.refresh(repo)
        return repo

    def get_or_create(
        self,
        owner: str,
        name: str,
        vcs_provider: str = "github",
        external_id: str | None = None,
        url: str | None = None,
    ) -> RepositoryModel:
        repo = self.get_by_owner_name(owner, name, vcs_provider)
        if repo:
            return repo

        if url is None:
            raise ValueError("url is required for repository creation")

        return self.create(owner, name, vcs_provider, external_id, url)
    
    def get_by_external_id(
        self,
        vcs_provider: str,
        external_id: str
    ) -> RepositoryModel | None:
        return (
            self.db.query(RepositoryModel)
            .filter_by(vcs_provider=vcs_provider, external_id=external_id)
            .first()
        )



