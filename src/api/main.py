from datetime import datetime
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from src.services.internal.process import process_repo, preprocess_commits
from src.adapters.db.base import SessionLocal
from src.adapters.db.repositories.repository_repo import RepositoryRepository
import os

from src.core.config import settings
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(title=settings.app_name, debug=settings.debug)


# ---------------------------
# Pydantic модели для запроса
# ---------------------------
class RepoRequest(BaseModel):
    owner: str
    repo: str
    since: datetime | None = None
    max_commits: int


class CommitsFileRequest(BaseModel):
    filename: str


@app.post("/repo/init")
def api_process_repo(
    req: RepoRequest, 
    github_token: str = Header(None, alias='ght')
    ):
    if not github_token:
        raise HTTPException(status_code=400, detail="GitHub token header missing")
    try:
        process_repo(req.owner, req.repo, token=github_token, since=req.since, max_commits=req.max_commits)
        return {"status": "success", "message": f"Processed {req.owner}/{req.repo}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/preprocess_commits")
def api_preprocess_commits(req: CommitsFileRequest):
    if not os.path.exists(req.filename):
        raise HTTPException(status_code=404, detail="File not found")
    try:
        preprocess_commits.preprocess_commits(req.filename)
        return {
            "status": "success",
            "message": f"Processed commits from {req.filename}",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/repos")
def list_repos():
    with SessionLocal() as session:
        repo_repo = RepositoryRepository(session)
        repos = session.query(
            repo_repo.db.query(
                repo_repo.db.query(repo_repo.db._decl_class_registry.values()).first()
            )
        ).all()
        # проще пока просто отдавать owner+name
        return [{"id": r.id, "owner": r.owner, "name": r.name} for r in repos]
