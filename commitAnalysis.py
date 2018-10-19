from typing import List
import git
import csv
import os
from collections import Counter
from progress.bar import Bar
    
def commitAnalysis(commits: List[git.Commit], outputDir: str):
    
    authorInfoDict = {}
    
    # traverse all commits
    print("Analyzing commits...")
    for commit in Bar('Processing').iter(commits):
        
        # extract info
        author = commit.author.email
        timezone = commit.author_tz_offset
        time = commit.authored_datetime
        
        # save author
        authorInfo = authorInfoDict.setdefault(author, dict(
                timezones= {},
                commitCount= 0,
                sponsoredCommitCount= 0,
                earliestCommitDate=time,
                latestCommitDate=time
        ))
        
        # increase commit count
        authorInfo['commitCount'] += 1
        
        # validate earliest commit
        # by default GitPython orders commits from latest to earliest
        if (time < authorInfo['earliestCommitDate']):
            authorInfo['earliestCommitDate'] = time
        
        # ignore undtermined timezones
        if commit.author_tz_offset == 0:
            continue
        
        # increase timezone count
        timezoneCount = authorInfo['timezones'].setdefault(str(timezone), 0)
        timezoneCount += 1
        
        # check if commit was between 9 and 5
        if time.hour >= 9 and time.hour <= 17:
            authorInfo['sponsoredCommitCount'] += 1
        
    # save count of unique authors
    authorCount = len([*authorInfoDict])
    
    # get timezone count
    print("Analyzing timezones...")
    timezonesCounter = Counter(timezone 
                               for author in authorInfoDict 
                               for timezone in authorInfoDict[author]['timezones'])
    
    # calculate amount of sponsored devs
    print("Analyzing sponsored authors...")
    sponsoredAuthorCount = 0
    for author in authorInfoDict:
        info = authorInfoDict[author]
        commitCount = int(info['commitCount'])
        sponsoredCommitCount = int(info['sponsoredCommitCount'])
        diff = sponsoredCommitCount / commitCount
        if diff >= .95:
            sponsoredAuthorCount += 1
    
    print("Outputting CSVs...")
    
    # output author days on project
    with open(os.path.join(outputDir, 'authorDaysOnProject.csv'), 'a', newline='') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(['Author','# of Days'])
        for author in authorInfoDict:
            earliestDate = authorInfoDict[author]['earliestCommitDate']
            latestDate = authorInfoDict[author]['latestCommitDate']
            diff = latestDate - earliestDate
            w.writerow([author,diff.days + 1])
    
    with open(os.path.join(outputDir, 'timezones.csv'), 'a', newline='') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(['Timezone Offset','Commit Count'])
        for timezone in timezonesCounter:
            w.writerow([timezone,timezonesCounter[timezone]])
            
    # output commits per author
    with open(os.path.join(outputDir, 'commitsPerAuthor.csv'), 'a', newline='') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(['Author','Commit Count'])
        for author in authorInfoDict:
            w.writerow([author,authorInfoDict[author]['commitCount']])
        
    # output project info
    with open(os.path.join(outputDir, 'projectAnalysis.csv'), 'a', newline='') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(['AuthorCount',authorCount])
        w.writerow(['SponsoredAuthorCount',sponsoredAuthorCount])
        w.writerow(['TimezoneCount',len(timezonesCounter)])