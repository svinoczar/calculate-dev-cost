from src.adapters.db.base import SessionLocal
from src.adapters.db.repositories.repository_repo import RepositoryRepository
from src.adapters.db.repositories.contributor_repo import ContributorRepository
from src.adapters.db.repositories.commit_repo import CommitRepository


def test_repository_repo():
    with SessionLocal() as session:
        repo_repo = RepositoryRepository(session)

        repo = repo_repo.get_or_create(
            owner="Nerds-International",
            name="nerd-code-frontend",
            vcs_provider="github",
            external_id="123456",
            url="https://github.com/Nerds-International/nerd-code-frontend",
        )

        assert repo.id is not None
        assert repo.owner == "Nerds-International"


def test_contributor_repo():
    with SessionLocal() as session:
        contributor_repo = ContributorRepository(session)

        contributor = contributor_repo.get_or_create(
            vcs_provider="github",
            external_id="999",
            login="octocat",
            profile_url="https://github.com/octocat",
        )

        assert contributor.id is not None


def test_commit_repo():
    with SessionLocal() as session:
        commit_repo = CommitRepository(session)

        commit = commit_repo.create(
            repo_id=1,
            contributor_id=None,
            sha="abc123",
            message="initial commit",
        )

        assert commit.id is not None


if __name__ == "__main__":
    test_repository_repo()
    test_contributor_repo()
    test_commit_repo()