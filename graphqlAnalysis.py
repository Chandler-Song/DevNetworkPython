import graphqlRequests as gql
import os
import csv


def graphqlAnalysis(pat: str, repoShortName: str, outputDir: str):

    # split repo by owner and name
    owner, name = splitRepoName(repoShortName)

    # # number of issues per repository
    # issueCount = gql.countIssuesPerRepository(pat, owner, name)

    # # number of PRs per repository
    # prCount = gql.countPullRequestsPerRepository(pat, owner, name)

    # # number of commits per PR
    # prCommitCount = gql.countCommitsPerPullRequest(pat, owner, name)

    # select all issue participants
    issueParticipants = gql.getIssueParticipants(pat, owner, name)

    # select all PR participants

    # join lists

    # select distinct user logins

    # number of developers per issue

    # number of developers per PR

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
