import datetime

from requests import Session
from src.adapters.db.models.commit_file import CommitFileModel
from src.adapters.db.repositories.commit_file_repo import CommitFileRepository 
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

def process_repo(
        owner,
        repo,
        token=None,
        since: datetime | None = None,
        max_commits: int | None = None):
    """
    Обрабатывает репозиторий:
    1) Проверяет, есть ли репо в БД
    2) Если нет, создаёт репо, контрибьюторов и все коммиты
    3) Если есть, добавляет только новые коммиты и новых контрибьюторов
    """

    commits = get_commits_list(
        owner,
        repo,
        token=token,
        since=since,
        max_commits=max_commits,
    )
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


def update_commits(
    db: Session,
    repository_id: int,
    token=None,
    limit: int = 100,
    since: datetime | None = None,
):
    logger.info("Updating commits...")

    commit_repo = CommitRepository(db)
    commit_file_repo = CommitFileRepository(db)
    repo_repo = RepositoryRepository(db)
    repo_object = repo_repo.get_by_id(repository_id)

    # 1. Берем коммиты, которые еще не обработаны
    commits = commit_repo.get_commits_for_update(
        repository_id=repository_id,
        limit=limit,
        since=since
        )

    if not commits:
        logger.info("No commits to update")
        return 0

    # 2. Инициализация всего пайплайна (1 в 1 как preprocess_commits)
    files_filter = FilesFilter()
    file_enricher = FileLanguageEnricher(lang_detector)
    commit_type_detector = CommitTypeDetector()
    commit_enricher = CommitEnricher(
        file_enricher=file_enricher,
        commit_type_detector=commit_type_detector
    )

    processed = 0

    # 3. Основной цикл
    for commit_model in commits:
        try:
            # 3.1 Получаем полный commit JSON из GitHub
            commit_json = get_commit(
                owner=repo_object.owner,
                repo=repo_object.name,
                ref=commit_model.sha,
                token=token  # если нужен токен
            )

            # 3.2 JSON -> DTO
            commit_dto = single_commit_json_to_dto(commit_json)

            # 3.3 DTO -> Domain
            domain_commit = single_commit_dto_to_domain_commit_dto(commit_dto)

            # 3.4 Фильтрация и обогащение (как раньше)
            domain_commit = files_filter.filter(domain_commit)
            domain_commit = commit_enricher.enrich(domain_commit)

            # 3.5 Запись результата в БД
            commit_repo.update_details(
                commit_id=commit_model.id,
                authored_at=commit_dto.commit.author.date,
                committed_at=commit_dto.commit.committer.date,
                author_name=commit_dto.commit.author.name,
                author_email=commit_dto.commit.author.email,
                additions=commit_dto.stats.additions if commit_dto.stats else None,
                deletions=commit_dto.stats.deletions if commit_dto.stats else None,
                changes=commit_dto.stats.total if commit_dto.stats else None,
                commit_type=domain_commit.commit_type,
                commit_type_confidence=domain_commit.commit_type_confidence,
            )
            
            # 3.6 Перезаписываем файлы коммита
            commit_file_repo.delete_by_commit_id(commit_model.id)

            files_models = []
            for f in domain_commit.files:
                files_models.append(
                    CommitFileModel(
                        commit_id=commit_model.id,
                        file_path=f.path,
                        additions=f.additions,
                        deletions=f.deletions,
                        changes=(
                            f.additions + f.deletions
                            if f.additions is not None and f.deletions is not None
                            else None
                        ),
                        language=f.language,
                        language_confidence=f.language_confidence,
                        patch=f.patch,
                    )
                )

            commit_file_repo.bulk_create(files_models)


            processed += 1

        except Exception as e:
            logger.exception(
                f"Failed to process commit {commit_model.sha}: {e}"
            )
            continue

    logger.info(f"Updated {processed} commits")
    return processed


# def preprocess_commits(filename: str):
#     logger.info("Processing commits . . .")

#     files_filter = FilesFilter()
#     commit_github_objects: list[SingleCommitEntity] = []
#     commit_domain_objects: list[Commit] = []
#     filtered_commit_domain_objects: list[Commit] = []

#     file_enricher = FileLanguageEnricher(lang_detector)
#     commit_type_detector = CommitTypeDetector()
#     commit_enricher = CommitEnricher(
#         file_enricher=file_enricher, commit_type_detector=commit_type_detector
#     )

#     with open(filename, "r", encoding="utf-8") as f:
#         user_commits = json.load(f)

#     for commit in user_commits:
#         commit_github_objects.append(single_commit_json_to_dto(commit))

#     for commit in commit_github_objects:
#         commit_domain_objects.append(single_commit_dto_to_domain_commit_dto(commit))

#     # print(len(commit_domain_objects))

#     # print(f"GH: {commit_github_objects[0].model_dump().keys()}")
#     # print(f"DOMAIN: {commit_domain_objects[0].model_dump().keys()}")

#     for commit in commit_domain_objects:
#         commit = files_filter.filter(commit)
#         commit = commit_enricher.enrich(commit)
#         filtered_commit_domain_objects.append(commit)

#     with open("TEST_COMMIT_DIFF.diff", "w", encoding="utf-8") as out:
#         c = 1

#         for commit in filtered_commit_domain_objects:
#             out.write(
#                 f"commit {c}\n"
#                 f"commit_type: {commit.commit_type}\n"
#                 f"confidence: {commit.commit_type_confidence:.3f}\n\n"
#             )

#             for file in commit.files:
#                 if not file.patch:
#                     continue

#                 out.write(f"filename: {file.filename}\n")
#                 out.write(f"language: {file.language} \n")
#                 out.write("=" * 25 + "\n")
#                 out.write(file.patch + "\n")
#                 out.write("=" * 25 + "\n\n")

#             c += 1

#     print("Done processing. . .")






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
