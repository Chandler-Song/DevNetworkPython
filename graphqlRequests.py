import requests


def getIssuesPerRepository(pat: str, owner: str, name: str):
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


def getPullRequestsPerRepository(pat: str, owner: str, name: str):
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
