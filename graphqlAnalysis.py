import graphqlRequests as gql
import os
import csv


def graphqlAnalysis(pat: str, repoShortName: str, outputDir: str):

    # split repo by owner and name
    owner, name = splitRepoName(repoShortName)

    print("Querying number of issues per repository")
    issueCount = gql.countIssuesPerRepository(pat, owner, name)

    print("Querying number of PRs per repository")
    prCount = gql.countPullRequestsPerRepository(pat, owner, name)

    print("Querying number of commits per PR")
    prCommitCount = gql.countCommitsPerPullRequest(pat, owner, name)

    print("Querying issue participants")
    issueParticipants, issueParticipantCount = gql.getIssueParticipants(
        pat, owner, name
    )

    print("Querying PR participants")
    prParticipants, prParticipantCount = gql.getPullRequestParticipants(
        pat, owner, name
    )

    # join lists and clean memory
    participants = issueParticipants.update(prParticipants)
    del issueParticipants
    del prParticipants

    print("Writing GraphQL analysis results")
    with open(os.path.join(outputDir, "graphqlAnalysis.csv"), "a", newline="") as f:
        w = csv.writer(f, delimiter=",")
        w.writerow(["NumberIssues", issueCount])
        w.writerow(["NumberPRs", prCount])
        w.writerow(["NumberDevelopersIssue", issueParticipantCount])
        w.writerow(["NumberDevelopersPR", prParticipantCount])

    with open(
        os.path.join(outputDir, "commitsPerPullRequest.csv"), "a", newline=""
    ) as f:
        w = csv.writer(f, delimiter=",")
        w.writerow(["PR Number", "Commit Count"])
        for prNumber in prCommitCount.keys():
            w.writerow([prNumber, prCommitCount[prNumber]])


def splitRepoName(repoShortName: str):
    split = repoShortName.split("/")
    return split[0], split[1]
