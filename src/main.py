from src.services.external.github_stats_manual import *
from src.util.mapper import JSONToGitCommitAuthorEntityList
from src.util.logger import logger


import json
import os


def process_repo(owner, repo):
    commits = get_commits_list(owner=owner, repo=repo)
    logger.info(f"Successfully retrieved {len(commits)} commits for {owner}/{repo}")
    
    contributors = get_contributors(owner=owner, repo=repo)
    dto_contributors = JSONToGitCommitAuthorEntityList(contributors)

    commits_dir = "user_commits"
    if not os.path.exists(commits_dir):
        os.makedirs(commits_dir)

    # Для каждого contributor'а собираем его коммиты
    for contributor in dto_contributors:
        contributor_login = contributor.login
        logger.info(f"Processing commits for: {contributor_login}")
        
        user_commits = []
        
        for commit in commits:
            if (commit.get('author') and 
                commit['author'].get('login') and 
                commit['author']['login'] == contributor_login):

                sha = commit['sha']
                try:
                    full_commit = get_commit(owner=owner, repo=repo, ref=sha)
                    # commit_dto = JSONToSingleCommitEntity(full_commit)
                    user_commits.append(full_commit)
                except Exception as e:
                    print(f"Error getting commit {sha}: {e}")
        
        if user_commits:
            filename = f"{commits_dir}/{contributor_login}_commits.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(user_commits, f, ensure_ascii=False, indent=4)
            logger.info(f"Saved {len(user_commits)} commits to {filename}")
        else:
            logger.warn(f"No commits found for {contributor_login}")

    with open('contributors.json', 'w', encoding='utf-8') as f:
        json.dump(contributors, f, ensure_ascii=False, indent=4)
        
    with open('all_commits_meta.json', 'w', encoding='utf-8') as f:
        json.dump(commits, f, ensure_ascii=False, indent=4)


def process_commits(fileneme: str):
    with open(fileneme, 'rt', encoding='utf-8') as f:
        user_commits = json.load(f)
    for 




if __name__ == '__main__':
    process_repo('Nerds-International', 'nerd-code-frontend')

    process_commits("Demid0_commits.json")