from data.github_api_response.CommitsResponseEntity import *


def JSONToSingleCommitEntity(json):
    return SingleCommitEntity(
        url=json["url"],
        sha=json["sha"],
        node_id=json["node_id"],
        html_url=json["html_url"],
        comments_url=json["comments_url"],
        commit=CommitSignatureEntity(
            url=json["commit"]["url"],
            author=GitUserEntity(
                name=json["commit"]["author"]["name"],
                email=json["commit"]["author"]["email"],
                date=json["commit"]["author"]["date"],
            ),
            committer=GitUserEntity(
                name=json["commit"]["committer"]["name"],
                email=json["commit"]["committer"]["email"],
                date=json["commit"]["committer"]["date"],
            ),
            message=json["commit"]["message"],
            tree=TreeEntity(
                url=json["commit"]["tree"]["url"], sha=json["commit"]["tree"]["sha"]
            ),
            comment_count=json["commit"]["comment_count"],
            verification=CommitVerificationEntity(
                verified=json["commit"]["verification"]["verified"],
                reason=json["commit"]["verification"]["reason"],
                signature=json["commit"]["verification"]["signature"],
                payload=json["commit"]["verification"]["payload"],
                verified_at=json["commit"]["verification"]["verified_at"],
            ),
        ),
        author=GitCommitAuthorEntity(
            login=json["author"]["login"],
            id=json["author"]["id"],
            node_id=json["author"]["node_id"],
            avatar_url=json["author"]["avatar_url"],
            gravatar_id=json["author"]["gravatar_id"],
            url=json["author"]["url"],
            html_url=json["author"]["html_url"],
            followers_url=json["author"]["followers_url"],
            following_url=json["author"]["following_url"],
            gists_url=json["author"]["gists_url"],
            starred_url=json["author"]["starred_url"],
            subscriptions_url=json["author"]["subscriptions_url"],
            organizations_url=json["author"]["organizations_url"],
            repos_url=json["author"]["repos_url"],
            events_url=json["author"]["events_url"],
            received_events_url=json["author"]["received_events_url"],
            type=json["author"]["type"],
            site_admin=json["author"]["site_admin"],
        ),
        committer=GitCommitAuthorEntity(
            login=json["committer"]["login"],
            id=json["committer"]["id"],
            node_id=json["committer"]["node_id"],
            avatar_url=json["committer"]["avatar_url"],
            gravatar_id=json["committer"]["gravatar_id"],
            url=json["committer"]["url"],
            html_url=json["committer"]["html_url"],
            followers_url=json["committer"]["followers_url"],
            following_url=json["committer"]["following_url"],
            gists_url=json["committer"]["gists_url"],
            starred_url=json["committer"]["starred_url"],
            subscriptions_url=json["committer"]["subscriptions_url"],
            organizations_url=json["committer"]["organizations_url"],
            repos_url=json["committer"]["repos_url"],
            events_url=json["committer"]["events_url"],
            received_events_url=json["committer"]["received_events_url"],
            type=json["committer"]["type"],
            site_admin=json["committer"]["site_admin"],
        ),
        parents=[
            ParentEntity(url=parent["url"], sha=parent["sha"])
            for parent in json["parents"]
        ],
        stats=StatsEntity(
            additions=json["stats"]["additions"],
            deletions=json["stats"]["deletions"],
            total=json["stats"]["total"],
        ),
        files=[
            FileEntity(
                filename=file["filename"],
                additions=file["additions"],
                deletions=file["deletions"],
                changes=file["changes"],
                status=file["status"],
                raw_url=file["raw_url"],
                blob_url=file["blob_url"],
                patch=file["patch"],
            )
            for file in json["files"]
        ],
    )


def JSONToGitCommitAuthorEntityList(json):
    return [
        GitCommitAuthorEntity(
            login=contributor["login"],
            id=contributor["id"],
            node_id=contributor["node_id"],
            avatar_url=contributor["avatar_url"],
            gravatar_id=contributor["gravatar_id"],
            url=contributor["url"],
            html_url=contributor["html_url"],
            followers_url=contributor["followers_url"],
            following_url=contributor["following_url"],
            gists_url=contributor["gists_url"],
            starred_url=contributor["starred_url"],
            subscriptions_url=contributor["subscriptions_url"],
            organizations_url=contributor["organizations_url"],
            repos_url=contributor["repos_url"],
            events_url=contributor["events_url"],
            received_events_url=contributor["received_events_url"],
            type=contributor["type"],
            site_admin=contributor["site_admin"],
        )
        for contributor in json
    ]
