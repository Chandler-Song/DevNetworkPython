import graphqlRequests as gql


def graphqlAnalysis(pat: str, repoShortName: str):

    # split repo by owner and name
    owner, name = splitRepoName(repoShortName)

    # run graphql requests
    issueCount = gql.getIssuesPerRepository(pat, owner, name)
    prCount = gql.getPullRequestsPerRepository(pat, owner, name)


def splitRepoName(repoShortName: str):
    split = repoShortName.split("/")
    return split[0], split[1]
