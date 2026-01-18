from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


from src.data.domain.file_change import FileChange

class Commit(BaseModel):
    sha: str
    author_login: str | None
    message: Optional[str] = None

    files: List[FileChange] | None = None

    commit_type: str | None = None
    commit_type_confidence: float | None = None

    authored_at: Optional[datetime] = None
    committed_at: Optional[datetime] = None

    author_name: Optional[str] = None
    author_email: Optional[str] = None

    additions: Optional[int] = None
    deletions: Optional[int] = None
    changes: Optional[int] = None