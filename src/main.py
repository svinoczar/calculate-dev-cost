import time
from services.external.github_stats_manual import *
from util.Mapper import JSONToGitCommitAuthorEntityList

if __name__ == '__main__':
    # Использование
    
    # print(commits)
    # sha = commits[0]['sha']
    # commit = get_commit("Nerds-International", "nerd-code-frontend", sha)
    # dto = JSONToSingleCommitEntity(commit)
    # print(commit['author'])
    contributors = [contributor.login for contributor in JSONToGitCommitAuthorEntityList(get_contributors("Nerds-International", "nerd-code-frontend"))]

    hashes = {}
    commits_dict = {}
    start_time = time.time()
    for author in contributors:
        print(f"author: {author}")
        # author = commit['author']['login']
        commits = get_commits_list("Nerds-International", "nerd-code-frontend", author)
        commit_hashes = [commit['sha'] for commit in commits]
        hashes[author] = commit_hashes
        print("hashes: OK")
        print(hashes)
        commits_list = [get_commit("Nerds-International", "nerd-code-frontend", sha) for sha in commit_hashes]
        commits_dict[author] = commits_list
        print("commits_list: OK")

    with open('author_to_hash.json', 'w') as f:
            json.dump(hashes, f)

    with open('commits.json', 'w') as f:
            json.dump(commits_dict, f)
        # print(commits)
        # print("\n")
        # exit(0)
    print(f"Programm time: {time.time()-start_time}")
    # print(contributors)
    
    
    # print('\n\n\n\n')
    # print(json.dumps(commits))
