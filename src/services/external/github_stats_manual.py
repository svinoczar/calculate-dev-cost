from datetime import datetime
import os
from time import time
import requests
import json

from dotenv import load_dotenv
from src.util.mapper import single_commit_json_to_dto


load_dotenv()


def get_commits_list(
    owner,
    repo,
    token=None,
    since: datetime | None = None,
    max_commits: int | None = None,
):
    if token is None:
        token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN not found")

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {
        "Authorization": f"token {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept": "application/vnd.github.v3+json",
    }

    all_commits = []
    page = 1
    per_page = 100

    while True:
        params = {
            "page": page,
            "per_page": per_page,
        }

        if since:
            params["since"] = since.isoformat()

        for attempt in range(3):
            try:
                response = requests.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=60,
                )
                response.raise_for_status()
                break
            except requests.RequestException as e:
                if attempt == 2:
                    raise
                time.sleep(5)

        commits = response.json()
        if not commits:
            break

        for commit in commits:
            all_commits.append(commit)
            if max_commits and len(all_commits) >= max_commits:
                return all_commits

        print(f"Retrieved page {page}: {len(commits)} commits")

        if "next" in response.links:
            page += 1
        else:
            break

    print(f"Total commits retrieved: {len(all_commits)}")
    return all_commits



def get_commit(owner, repo, ref, token=None):
    if token is None:
        token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN not found in .env file")

    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{ref}"
    headers = {
        "Authorization": f"token {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()
    return response.json()


def compare_commit(owner, repo, basehead, token=None):
    if token is None:
        token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN not found in .env file")

    url = f"https://api.github.com/repos/{owner}/{repo}/compare/{basehead}"
    headers = {
        "Authorization": f"token {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()
    return json.loads(response.json())


def get_contributors(owner, repo, token=None):

    if token is None:
        token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN not found in .env file")

    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()



# Использование
# commits = get_commits_list("Nerds-International", "nerd-code-frontend")
# commit = get_commit("Nerds-International", "nerd-code-frontend", commits[0]["sha"])
# print(commit)
# dto = JSONToSingleCommitEntity(commit)
# print(dto)
# print(get_collaborators("Nerds-International", "nerd-code-frontend"))
# print('\n\n\n\n')
# print(json.dumps(commits))

# commits = get_commit('svinoczar', 'itmo', '2bf0de21d28e4ed24bb271c1d9e12ee7720c2cfe')
# print(str(commits).replace('\'', '"'))

# commits = get_commit('svinoczar', 'contribution-analyzer', 'main...dev')
# print(str(commits).replace('\'', '"'))
