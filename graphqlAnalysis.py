import graphqlRequests as gql
import os
import csv


def graphqlAnalysis(pat: str, repoShortName: str, outputDir: str):

    # split repo by owner and name
    owner, name = splitRepoName(repoShortName)

    # run graphql requests
    issueCount = gql.countIssuesPerRepository(pat, owner, name)
    prCount = gql.countPullRequestsPerRepository(pat, owner, name)
    prCommitCount = gql.countCommitsPerPullRequest(pat, owner, name)

    # output
    with open(os.path.join(outputDir, "graphqlAnalysis.csv"), "a", newline="") as f:
        w = csv.writer(f, delimiter=",")
        w.writerow(["NumberIssues", issueCount])
        w.writerow(["NumberPRs", prCount])

    with open(os.path.join(outputDir, "commitsPerPR.csv"), "a", newline="") as f:
        w = csv.writer(f, delimiter=",")
        w.writerow(["PR Number", "Commit Count"])
        for prNumber in prCommitCount.keys():
            w.writerow([prNumber, prCommitCount[prNumber]])


def splitRepoName(repoShortName: str):
    split = repoShortName.split("/")
    return split[0], split[1]
