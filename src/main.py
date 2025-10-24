from services.external.github_stats_manual import *
from util.Mapper import JSONToGitCommitAuthorEntityList

if __name__ == '__main__':
    # Использование
    commits = get_commits_list("Nerds-International", "nerd-code-frontend")
    # print(commits)
    sha = commits[0]['sha']
    commit = get_commit("Nerds-International", "nerd-code-frontend", sha)
    dto = JSONToSingleCommitEntity(commit)
    # print(commit['author'])
    contributors = get_contributors("svinoczar", "contribution-analyzer")
    # print(contributors)
    dto_contributors = JSONToGitCommitAuthorEntityList(contributors)
    for contributor in dto_contributors:
        print(f"{contributor}\n")
    # print('\n\n\n\n')
    # print(json.dumps(commits))
