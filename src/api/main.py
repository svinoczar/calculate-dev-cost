from datetime import datetime
from fastapi import FastAPI, HTTPException, Header
from fastapi.params import Depends
from pydantic import BaseModel
import logging

from src.services.internal.process import process_repo
from src.adapters.db.base import SessionLocal
from src.adapters.db.repositories.repository_repo import RepositoryRepository
from src.core.config import settings


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
    max_commits: int | None = None


class UpdateCommitsRequest(BaseModel):
    repository_id: int
    limit: int = 100
    since: datetime | None = None
    max_commits: int | None = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/repo/init")
def api_process_repo(
    req: RepoRequest,
    github_token: str = Header(None, alias="ght"),
    scope: str = Header(None, alias="acc-scope"), # username:id
    settings: str = Header(None, alias="analysis-settings"),
):
    if not github_token:
        raise HTTPException(status_code=400, detail="GitHub token header missing")
    try:
        print(scope.split(":"))
        scope_type, scope_id = scope.split(":")
        process_repo(
            req.owner,
            req.repo,
            token=github_token,
            scope_type=scope_type,
            scope_id=scope_id,
            settings=settings,
            since=req.since,
            max_commits=req.max_commits
        )
        return {"status": "success", "message": f"Processed {req.owner}/{req.repo}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @app.post("/commits/update")
# def api_update_commits(
#     req: UpdateCommitsRequest,
#     db: Session = Depends(get_db),
#     github_token: str = Header(None, alias='ght')
#     ):
#     try:
#         count = update_commits(
#             db=db,
#             repository_id=req.repository_id,
#             token=github_token,
#             limit=req.limit,
#             since=req.since
#             )
#         return {
#             "status": "success",
#             "updated_commits": count
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/repos")
# def list_repos():
#     with SessionLocal() as session:
#         repo_repo = RepositoryRepository(session)
#         repos = session.query(
#             repo_repo.db.query(
#                 repo_repo.db.query(repo_repo.db._decl_class_registry.values()).first()
#             )
#         ).all()
#         # проще пока просто отдавать owner+name
#         return [{"id": r.id, "owner": r.owner, "name": r.name} for r in repos]
