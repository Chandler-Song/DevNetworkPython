import os
import git
import csv
from datetime import datetime

def tagAnalysis(repo: git.Repo, outputDir: str):
    print("Analyzing tags...")

    tagInfo = []
    tags = sorted(repo.tags, key=lambda t: t.tag.tagged_date)
    
    lastTag = None
    for tag in tags:
        commitCount = 0
        
        if (lastTag == None):
            commitCount = len(list(tag.commit.iter_items(repo, tag.tag)))
        else:
            sinceStr = formatDate(lastTag.tag.tagged_date)
            commitCount = len(list(tag.commit.iter_items(repo, tag.tag, after=sinceStr)))
        
        tagInfo.append(dict(
            name=tag.tag.tag,
            date= formatDate(tag.tag.tagged_date),
            commitCount= commitCount
        ))
        
        lastTag = tag
    
    # output non-tabular results
    with open(os.path.join(outputDir, 'project.csv'), 'a', newline='') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(['Tag Count', len(tagInfo)])
    
    # output tag info
    print("Outputting CSVs...")
    with open(os.path.join(outputDir, 'tags.csv'), 'a', newline='') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(['Name', 'Date', 'Commit Count'])
        for tag in sorted(tagInfo, key=lambda o: o['date']):
            w.writerow([tag['name'], tag['date'], tag['commitCount']])

def formatDate(value):
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d')