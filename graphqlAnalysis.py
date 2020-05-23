import graphqlRequests as gql
import os
import csv


def graphqlAnalysis(pat: str, repoShortName: str, outputDir: str):

    # split repo by owner and name
    owner, name = splitRepoName(repoShortName)

    print("Querying number of issues")
    issueCount = gql.countIssuesPerRepository(pat, owner, name)

    print("Querying number of PRs")
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

    with open(os.path.join(outputDir, "numberCommitsPR.csv"), "a", newline="") as f:
        w = csv.writer(f, delimiter=",")
        w.writerow(["PR Number", "Commit Count"])
        for key in prCommitCount.keys():
            w.writerow([key, prCommitCount[key]])

    with open(
        os.path.join(outputDir, "numberDevelopersIssue.csv"), "a", newline=""
    ) as f:
        w = csv.writer(f, delimiter=",")
        w.writerow(["Issue Number", "Developer Count"])
        for key in issueParticipantCount.keys():
            w.writerow([key, issueParticipantCount[key]])

    with open(os.path.join(outputDir, "numberDevelopersPR.csv"), "a", newline="") as f:
        w = csv.writer(f, delimiter=",")
        w.writerow(["PR Number", "Developer Count"])
        for key in prParticipantCount.keys():
            w.writerow([key, prParticipantCount[key]])


def splitRepoName(repoShortName: str):
    split = repoShortName.split("/")
    return split[0], split[1]
