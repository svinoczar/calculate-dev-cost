from pydantic import BaseModel
from typing import List

from data.domain.file_change import FileChange

class Commit(BaseModel):
    sha: str
    author_login: str | None
    message: str

    files: List[FileChange]

    commit_type: str | None = None
    commit_type_confidence: float | None = None