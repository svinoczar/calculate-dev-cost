from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class GitUserEntity(BaseModel):
    name: str
    email: str
    date: datetime


class TreeEntity (BaseModel):
    url: str
    sha: str


class CommitVerificationEntity(BaseModel):
    verified: bool
    reason: str
    signature: Optional[str] = None
    payload: Optional[str] = None
    verified_at: Optional[datetime] = None


class CommitSignatureEntity(BaseModel):
    url: str
    author: GitUserEntity
    committer: GitUserEntity
    message: str
    tree: TreeEntity
    comment_count: int
    verification: CommitVerificationEntity


class GitCommitAuthorEntity(BaseModel):
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: Optional[str] = ""
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    site_admin: bool


class ParentEntity(BaseModel):
    url: str
    sha: str


class StatsEntity(BaseModel):
    additions: int
    deletions: int
    total: int


class FileEntity(BaseModel):
    filename: str
    additions: int
    deletions: int
    changes: int
    status: str
    raw_url: str
    blob_url: str
    patch: str


class SingleCommitEntity(BaseModel):
    url: str
    sha: str
    node_id: str
    html_url: str
    comments_url: str
    commit: CommitSignatureEntity
    author: GitCommitAuthorEntity
    committer: GitCommitAuthorEntity
    parents: List[ParentEntity]
    stats: Optional[StatsEntity]
    files: List[FileEntity]