import requests


def getIssuesPerRepository(pat: str, repoShortName: str):
    split = splitRepoName(repoShortName)
    query = """{{
        repository(owner:"{0}", name:"{1}") {{
            issues {{
                totalCount
            }}
        }}
    }}""".format(
        split[0], split[1]
    )

    result = runGraphqlRequest(pat, query)

    totalCount = result["data"]["repository"]["issues"]["totalCount"]
    return totalCount


def splitRepoName(repoShortName: str):
    split = repoShortName.split("/")
    return (split[0], split[1])


def runGraphqlRequest(pat: str, query: str):
    headers = {"Authorization": "Bearer {0}".format(pat)}

    request = requests.post(
        "https://api.github.com/graphql", json={"query": query}, headers=headers
    )
    if request.status_code == 200:
        return request.json()
    raise "Query execution failed with code {0}: {1}".format(
        request.status_code, request.text
    )
