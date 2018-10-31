import git
import yaml
import os
import requests
import sys

from configuration import Configuration
from repoLoader import getRepo
from progress.bar import Bar

def main():
    try:
        
        # read configuration
        config = ...  # type: Configuration
        with open('config.yml', 'r', encoding='utf-8-sig') as file:
            content = file.read()
            config = yaml.load(content)
        
        # get repository reference
        repo = getRepo(config)
        
        # get args
        repoShortname = 'apache/mahout'
        token = sys.argv[1]
        
        # delete existing alias file if present
        if os.path.exists(config.aliasPath):
            os.remove(config.aliasPath)
            
        # extract aliases
        extractAliases(repo, config.aliasPath, repoShortname, token)
        
    finally:
        
        # close repo to avoid resource leaks
        del repo

def extractAliases(repo: git.Repo, aliasPath: str, repoShortname: str, token: str):
    commits = list(repo.iter_commits());
    
    # get all distinct author emails
    emails = set(commit.author.email.lower()
                 for commit in Bar('Processing').iter(commits))
    
    # get a commit per email
    shasByEmail = {}
    for email in Bar('Processing').iter(emails):
        commit = next(commit
                   for commit in commits
                   if commit.author.email.lower() == email)
        
        shasByEmail[email] = commit.hexsha
    
    # query github for author logins by their commits
    loginsByEmail = dict()
    emailsWithoutLogins = []
    
    for email in Bar('Processing').iter(shasByEmail):
        sha = shasByEmail[email]
        url = 'https://api.github.com/repos/{}/commits/{}'.format(repoShortname, sha)
        request = requests.get(url, headers={'Authorization': 'token ' + token})
        commit = request.json()
        author = commit['author']
        
        if not author is None:
            loginsByEmail[email] = author['login']
        else:
            emailsWithoutLogins.append(email)
    
    uniqueLogins = len(set(loginsByEmail.values()))
        
    # output to yaml
    with open(aliasPath, 'a', newline='') as f:                
        yaml.dump(loginsByEmail, f)
        
main()