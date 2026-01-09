from fastapi import FastAPI
from core.config import settings
from services.commit_processor import process_commits
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)


@app.on_event("startup")
def startup():
    logger.info("Starting application")
    logger.info(f"Using commits file: {settings.commits_path}")


@app.post("/analyze/commits")
def analyze_commits():
    process_commits(settings.commits_path)
    return {"status": "ok"}