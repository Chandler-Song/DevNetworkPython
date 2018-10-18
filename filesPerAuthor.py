import git
import re
import numpy as np
import datetime

fileMovePatten = "(\{.+ => (.+)\})"
fileMoveRegex = re.compile(fileMovePatten)

def time(repo: git.Repo):
    
    commits = repo.iter_commits()
    
    # get distinct author emails
    #authors = set(list(map(lambda c: c.author.email, commits)))
    
    # get distinct file names
    #files = [key for commit in commits for commit.stats.files.keys() in commit]
    
    print(datetime.datetime.now())
    
    files = set()
    for commitFiles in map(lambda c: c.stats.files, commits):
        files.update([*commitFiles])
        
    print(datetime.datetime.now())

def getFinalFileName(value: str):
    result = fileMoveRegex.findall(value)
    
    for match in result:
        value = value.replace(match[0], match[1])
        
    return value