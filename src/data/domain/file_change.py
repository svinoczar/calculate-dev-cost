from pydantic import BaseModel

class FileChange(BaseModel):
    path: str
    filename: str
    patch: str
    additions: int
    deletions: int

    language: str | None = None
    language_confidence: float | None = None