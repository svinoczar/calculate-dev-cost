from src.adapters.db.base import SessionLocal
from src.adapters.db.repositories.repository_repo import RepositoryRepository
from src.data.domain.commit import Commit
from src.data.github_api_response.commits_response_entity import SingleCommitEntity
from src.services.external.github_stats_manual import *
from src.services.internal.preprocessing.files_filter import FilesFilter
from src.services.internal.preprocessing.commit_enricher import CommitEnricher
from src.services.internal.preprocessing.file_language_enricher import FileLanguageEnricher
from src.services.internal.preprocessing.commit_type_detector import CommitTypeDetector
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


def process_repo(owner, repo):
    commits = get_commits_list(owner=owner, repo=repo)
    logger.info(f"Successfully retrieved {len(commits)} commits for {owner}/{repo}")

    contributors = get_contributors(owner=owner, repo=repo)
    dto_contributors = git_commit_authors_json_to_dto_list(contributors)

    commits_dir = "user_commits"
    if not os.path.exists(commits_dir):
        os.makedirs(commits_dir)

    # Для каждого contributor'а собираем его коммиты
    for contributor in dto_contributors:
        contributor_login = contributor.login
        logger.info(f"Processing commits for: {contributor_login}")

        user_commits = []

        for commit in commits:
            if (
                commit.get("author")
                and commit["author"].get("login")
                and commit["author"]["login"] == contributor_login
            ):

                sha = commit["sha"]
                try:
                    full_commit = get_commit(owner=owner, repo=repo, ref=sha)
                    # commit_dto = JSONToSingleCommitEntity(full_commit)
                    user_commits.append(full_commit)
                except Exception as e:
                    print(f"Error getting commit {sha}: {e}")

        if user_commits:
            filename = f"{commits_dir}/{contributor_login}_commits.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(user_commits, f, ensure_ascii=False, indent=4)
            logger.info(f"Saved {len(user_commits)} commits to {filename}")
        else:
            logger.warn(f"No commits found for {contributor_login}")

    with open("contributors.json", "w", encoding="utf-8") as f:
        json.dump(contributors, f, ensure_ascii=False, indent=4)

    with open("all_commits_meta.json", "w", encoding="utf-8") as f:
        json.dump(commits, f, ensure_ascii=False, indent=4)


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


if __name__ == "__main__":
    process_repo('Nerds-International', 'nerd-code-frontend')

    # preprocess_commits("user_commits/Demid0_commits.json")