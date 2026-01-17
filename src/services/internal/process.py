from src.adapters.db.base import SessionLocal
from src.adapters.db.repositories.repository_repo import RepositoryRepository
from src.adapters.db.repositories.contributor_repo import ContributorRepository
from src.adapters.db.repositories.commit_repo import CommitRepository
from src.data.domain.commit import Commit
from src.data.github_api_response.commits_response_entity import SingleCommitEntity
from src.services.external.github_stats_manual import *
from src.services.internal.preprocessing.files_filter import FilesFilter
from src.services.internal.preprocessing.commit_enricher import CommitEnricher
from src.services.internal.preprocessing.file_language_enricher import FileLanguageEnricher
from src.services.internal.preprocessing.commit_type_detector import CommitTypeDetector
from src.adapters.db.models.commit import CommitModel
from src.util.mapper import (
    git_commit_authors_json_to_dto_list,
    single_commit_dto_to_domain_commit_dto,
    single_commit_json_to_dto,
)
from src.util.logger import logger
from src.services.internal.preprocessing.lang_detector import LanguageDetector

import json
import os
import re


lang_detector = LanguageDetector()

def process_repo(owner, repo, token=None):
    """
    Обрабатывает репозиторий:
    1) Проверяет, есть ли репо в БД
    2) Если нет, создаёт репо, контрибьюторов и все коммиты
    3) Если есть, добавляет только новые коммиты и новых контрибьюторов
    """

    commits = get_commits_list(owner, repo, token=token)
    contributors = get_contributors(owner, repo, token=token)

    dto_contributors = git_commit_authors_json_to_dto_list(contributors)

    with SessionLocal() as session:
        repo_repo = RepositoryRepository(session)
        contributor_repo = ContributorRepository(session)
        commit_repo = CommitRepository(session)

        # ----------------------
        # Репозиторий
        # ----------------------
        db_repo = repo_repo.get_by_owner_name(owner, repo)
        if not db_repo:
            db_repo = repo_repo.create(
                owner=owner,
                name=repo,
                vcs_provider="github",
                external_id=None,
                url=f"https://github.com/{owner}/{repo}"
            )
            logger.info("Created repo in DB: %s/%s", owner, repo)
        else:
            logger.info("Repo already exists in DB: %s/%s", owner, repo)

        # ----------------------
        # Контрибьюторы
        # ----------------------
        db_contributors = {}
        for c in dto_contributors:
            db_c = contributor_repo.get_or_create(
                vcs_provider="github",
                external_id=str(c.id) if hasattr(c, "id") else None,  # используем GitHub numeric ID
                login=c.login,
                profile_url=c.html_url
            )
            db_contributors[c.login] = db_c

        # ----------------------
        # Коммиты
        # ----------------------
        existing_shas = get_existing_commit_shas(session, db_repo.id)  # ← функция, вернёт set
        new_commits = []

        for commit_json in commits:
            if "author" not in commit_json or not commit_json["author"]:
                continue
            login = commit_json["author"]["login"]
            if commit_json["sha"] in existing_shas:
                continue  # Уже есть в БД

            # Преобразуем в domain commit
            commit_dto = single_commit_json_to_dto(commit_json)
            commit_obj = single_commit_dto_to_domain_commit_dto(commit_dto)

            # Можно сразу записывать файлы, язык, тип, и т.д.
            commit_obj = enrich_commit(commit_obj)  # ← функция, делает то, что у тебя раньше было через CommitEnricher

            # Добавляем в БД
            db_commit = commit_repo.create(
                repository_id=db_repo.id,
                contributor_id=db_contributors.get(login).id if login in db_contributors else None,
                sha=commit_obj.sha,
                message=commit_obj.message
            )
            new_commits.append(db_commit)

        logger.info("Added %d new commits for %s/%s", len(new_commits), owner, repo)

    return db_repo


def preprocess_commits(filename: str):
    logger.info("Processing commits . . .")

    files_filter = FilesFilter()
    commit_github_objects: list[SingleCommitEntity] = []
    commit_domain_objects: list[Commit] = []
    filtered_commit_domain_objects: list[Commit] = []

    file_enricher = FileLanguageEnricher(lang_detector)
    commit_type_detector = CommitTypeDetector()
    commit_enricher = CommitEnricher(
        file_enricher=file_enricher, commit_type_detector=commit_type_detector
    )

    with open(filename, "r", encoding="utf-8") as f:
        user_commits = json.load(f)

    for commit in user_commits:
        commit_github_objects.append(single_commit_json_to_dto(commit))

    for commit in commit_github_objects:
        commit_domain_objects.append(single_commit_dto_to_domain_commit_dto(commit))

    # print(len(commit_domain_objects))

    # print(f"GH: {commit_github_objects[0].model_dump().keys()}")
    # print(f"DOMAIN: {commit_domain_objects[0].model_dump().keys()}")

    for commit in commit_domain_objects:
        commit = files_filter.filter(commit)
        commit = commit_enricher.enrich(commit)
        filtered_commit_domain_objects.append(commit)

    with open("TEST_COMMIT_DIFF.diff", "w", encoding="utf-8") as out:
        c = 1

        for commit in filtered_commit_domain_objects:
            out.write(
                f"commit {c}\n"
                f"commit_type: {commit.commit_type}\n"
                f"confidence: {commit.commit_type_confidence:.3f}\n\n"
            )

            for file in commit.files:
                if not file.patch:
                    continue

                out.write(f"filename: {file.filename}\n")
                out.write(f"language: {file.language} \n")
                out.write("=" * 25 + "\n")
                out.write(file.patch + "\n")
                out.write("=" * 25 + "\n\n")

            c += 1

    print("Done processing. . .")






# ----------------------
# Получаем все sha коммитов для репо
# ----------------------
def get_existing_commit_shas(session, repo_id):
    shas = session.query(CommitModel.sha).filter(CommitModel.repository_id == repo_id).all()
    return set(s[0] for s in shas)

# ----------------------
# Энричим коммит: язык файлов, тип коммита и т.д.
# ----------------------
def enrich_commit(commit: Commit) -> Commit:
    lang_detector = LanguageDetector()
    file_enricher = FileLanguageEnricher(lang_detector)
    commit_type_detector = CommitTypeDetector()
    commit_enricher = CommitEnricher(file_enricher=file_enricher, commit_type_detector=commit_type_detector)
    files_filter = FilesFilter()

    commit = files_filter.filter(commit)
    commit = commit_enricher.enrich(commit)
    return commit
