import git
import csv
from datetime import datetime

def tagAnalysis(repo: git.Repo, outputDir: str):

    tagInfo = []
    lastTag = None
    tags = sorted(repo.tags, key=lambda t: t.tag.tagged_date)
    
    print("Analyzing tags...")
    for tag in tags:
        commitCount = 0
        if (lastTag == None):
            commitCount = len(list(tag.commit.iter_items(repo, tag.tag)))
        else:
            sinceStr = datetime.fromtimestamp(lastTag.tag.tagged_date).strftime('%Y-%m-%d')
            commitCount = len(list(tag.commit.iter_items(repo, tag.tag, after=sinceStr)))
        
        tagDate = datetime.fromtimestamp(tag.tag.tagged_date).strftime('%Y-%m-%d')
        tagInfo.append(dict(
            name=tag.tag.tag,
            date= tagDate,
            commitCount= commitCount
        ))
        
        lastTag = tag
    
    # output non-tabular results
    with open(outputDir + '\\projectAnalysis.csv', 'a', newline='') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(['Tag Count', len(tagInfo)])
    
    # output tag info
    print("Outputting CSVs...")
    with open(outputDir + '\\tags.csv', 'a', newline='') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(['Name', 'Date', 'Commit Count'])
        for tag in sorted(tagInfo, key=lambda o: o['date']):
            w.writerow([tag['name'], tag['date'], tag['commitCount']])
    