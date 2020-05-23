import requests


def countIssuesPerRepository(pat: str, owner: str, name: str):
    query = """{{
        repository(owner:"{0}", name:"{1}") {{
            issues {{
                totalCount
            }}
        }}
    }}""".format(
        owner, name
    )

    result = runGraphqlRequest(pat, query)

    totalCount = result["repository"]["issues"]["totalCount"]
    return totalCount


def countPullRequestsPerRepository(pat: str, owner: str, name: str):
    query = """{{
        repository(owner: "{0}", name: "{1}") {{
            pullRequests{{
                totalCount
            }}
        }}
    }}""".format(
        owner, name
    )

    result = runGraphqlRequest(pat, query)

    totalCount = result["repository"]["pullRequests"]["totalCount"]
    return totalCount


def countCommitsPerPullRequest(pat: str, owner: str, name: str):
    query = buildCountCommitsPerPullRequestQuery(owner, name, None)

    prCommitCounts = {}
    while True:

        # get page of PRs
        result = runGraphqlRequest(pat, query)

        # extract nodes
        nodes = result["repository"]["pullRequests"]["nodes"]

        # add results to dict
        for pr in nodes:
            prNumber = pr["number"]
            commitCount = pr["commits"]["totalCount"]
            prCommitCounts[prNumber] = commitCount

        # check for next page
        pageInfo = result["repository"]["pullRequests"]["pageInfo"]
        if not pageInfo["hasNextPage"]:
            break

        cursor = pageInfo["endCursor"]
        query = buildCountCommitsPerPullRequestQuery(owner, name, cursor)

    return prCommitCounts


def buildCountCommitsPerPullRequestQuery(owner: str, name: str, cursor: str):
    return """{{
        repository(owner: "{0}", name: "{1}") {{
            pullRequests(first:100{2}){{
                nodes {{
                    number
                    commits {{
                        totalCount
                        }}
                }}
                pageInfo {{
                    hasNextPage
                    endCursor
                }}
            }}
        }}
    }}""".format(
        owner, name, buildNextPageQuery(cursor)
    )


def buildNextPageQuery(cursor: str):
    if cursor is None:
        return ""
    return ', after:"{0}"'.format(cursor)


def runGraphqlRequest(pat: str, query: str):
    headers = {"Authorization": "Bearer {0}".format(pat)}

    request = requests.post(
        "https://api.github.com/graphql", json={"query": query}, headers=headers
    )
    if request.status_code == 200:
        return request.json()["data"]
    raise "Query execution failed with code {0}: {1}".format(
        request.status_code, request.text
    )
