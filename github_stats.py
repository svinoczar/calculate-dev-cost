import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('GITHUB_TOKEN')

def get_commits_list(owner, repo):
    if not token:
        raise ValueError("GITHUB_TOKEN not found in .env file")
    
    url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    headers = {
        'Authorization': f'token {token}',
        'X-GitHub-Api-Version': '2022-11-28',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_commit(owner, repo, ref):
    
    if not token:
        raise ValueError("GITHUB_TOKEN not found in .env file")
    
    url = f'https://api.github.com/repos/{owner}/{repo}/commits/{ref}'
    headers = {
        'Authorization': f'token {token}',
        'X-GitHub-Api-Version': '2022-11-28',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


# Использование
# commits = get_commits_list('svinoczar', 'itmo')
# print(commits)

commits = get_commit('svinoczar', 'itmo', '2bf0de21d28e4ed24bb271c1d9e12ee7720c2cfe')
print(str(commits).replace('\'', '"'))
