import graphqlRequests as gql


def graphqlAnalysis(pat: str, repoShortName: str):
    issuesPerRepository = gql.getIssuesPerRepository(pat, repoShortName)
