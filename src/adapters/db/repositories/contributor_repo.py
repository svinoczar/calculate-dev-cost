# src/adapters/db/repositories/contributor_repo.py
from sqlalchemy.orm import Session
from src.adapters.db.models.contributor import ContributorModel

class ContributorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create(
        self,
        vcs_provider: str,
        external_id: str,
        login: str | None = None,
        profile_url: str | None = None
    ) -> ContributorModel:
        contributor = (
            self.db.query(ContributorModel)
            .filter_by(vcs_provider=vcs_provider, external_id=external_id)
            .first()
        )
        if contributor:
            return contributor

        contributor = ContributorModel(
            vcs_provider=vcs_provider,
            external_id=external_id,
            login=login,
            profile_url=profile_url,
        )
        self.db.add(contributor)
        self.db.commit()
        self.db.refresh(contributor)
        return contributor
