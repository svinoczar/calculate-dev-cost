import os
from dotenv import load_dotenv
from github import Github, Auth

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
auth = Auth.Token(token)
g = Github(auth=auth)

# Then play with your Github objects:
for repo in g.get_user().get_repos():
    print(repo.name)

# To close connections after use
g.close()