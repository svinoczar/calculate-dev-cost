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

    def bulk_create(self, files: list[AnalysisSettingsModel]):
        self.db.add_all(files)
