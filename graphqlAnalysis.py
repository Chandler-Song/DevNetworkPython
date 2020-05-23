import graphqlRequests as gql


def graphqlAnalysis(pat: str, repoShortName: str):

    # split repo by owner and name
    owner, name = splitRepoName(repoShortName)

    # run graphql requests
    issueCount = gql.countIssuesPerRepository(pat, owner, name)
    prCount = gql.countPullRequestsPerRepository(pat, owner, name)
    prCommitCount = gql.countCommitsPerPullRequest(pat, owner, name)


def splitRepoName(repoShortName: str):
    split = repoShortName.split("/")
    return split[0], split[1]
