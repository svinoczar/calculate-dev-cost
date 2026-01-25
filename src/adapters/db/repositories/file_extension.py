from adapters.db.models.file_extension import FileExtensionModel


class FileExtensionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_language(self, extension: str) -> str | None:
        return (
            self.db.query(FileExtensionModel.language)
            .filter(FileExtensionModel.extension == extension)
            .scalar()
        )
