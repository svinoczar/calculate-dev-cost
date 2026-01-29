from sqlalchemy.orm import Session

from src.adapters.db.base import Base
from src.adapters.db.models.analysis_settings import AnalysisSettingsModel


class AnalysisSettingsRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def delete_by_id(self, id: int):
        self.db.query(AnalysisSettingsModel)\
            .filter(AnalysisSettingsModel.id == id)\
            .delete()

    def create(
        self,
        scope_type: str,
        scope_id: int,
        settings: str,
    ) -> AnalysisSettingsModel:
        repo = AnalysisSettingsModel(
            scope_type=scope_type,
            scope_id=scope_id,
            settings=settings
        )
        self.db.add(repo)
        try:
            self.db.commit()
        except:
            self.db.rollback()
            raise
        self.db.refresh(repo)
        return repo

    def bulk_create(self, files: list[AnalysisSettingsModel]):
        self.db.add_all(files)

    def get_or_create(
        self,
        scope_type: str | None,
        scope_id: int | None,
        settings: str | None,
    ) -> AnalysisSettingsModel:
        repo = self.get_by_scope_id(scope_id)
        if repo:
            return repo

        if scope_type is None:
            raise ValueError("scope_type is required for analysis settings creation")
        if scope_id is None:
            raise ValueError("scope_id is required for analysis settings creation")
        if settings is None:
            raise ValueError("settings JSON is required for analysis settings creation")

        return self.create(scope_type, scope_id, settings)
    
    def get_by_scope_id(self, scope_id: int) -> AnalysisSettingsModel | None:
        return (
            self.db.query(AnalysisSettingsModel)
            .filter_by(scope_id=scope_id)
            .first()
        )