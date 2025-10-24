import os
import requests
import json
from dotenv import load_dotenv

from util.Mapper import JSONToSingleCommitEntity

load_dotenv()

token = os.getenv("GITHUB_TOKEN")


def get_commits_list(owner, repo):
    if not token:
        raise ValueError("GITHUB_TOKEN not found in .env file")

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {
        "Authorization": f"token {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    # return json.dumps(response.json(), indent=4)
    return response.json()


def get_commit(owner, repo, ref):

    if not token:
        raise ValueError("GITHUB_TOKEN not found in .env file")

    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{ref}"
    headers = {
        "Authorization": f"token {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def compare_commit(owner, repo, basehead):

    if not token:
        raise ValueError("GITHUB_TOKEN not found in .env file")

    url = f"https://api.github.com/repos/{owner}/{repo}/compare/{basehead}"
    headers = {
        "Authorization": f"token {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return json.loads(response.json())


def get_contributors(owner, repo):

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
commits = get_commits_list("Nerds-International", "nerd-code-frontend")
commit = get_commit("Nerds-International", "nerd-code-frontend", commits[0]["sha"])
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
