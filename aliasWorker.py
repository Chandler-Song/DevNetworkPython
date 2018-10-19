import os
import git
import yaml

def replaceAliases(repo: git.Repo, aliasPath: str):
    
    # nothing to do if no alias file
    if aliasPath == None or not os.path.exists(aliasPath):
        return repo.iter_commits()
    
    # read aliases
    content = ""
    with open(aliasPath, 'r', encoding='utf-8-sig') as file:
        content = file.read()
        
    aliases = yaml.load(content)
    transposesAliases = {}
    for alias in aliases:
        for email in aliases[alias]:
            transposesAliases[email] = alias
            
    return replaceAll(repo.iter_commits(), transposesAliases)

def replaceAll(commits, aliases):
    for commit in commits:
        copy = commit
        author = commit.author.email
        
        if author in aliases:
            copy.author.email = aliases[author]
            yield copy
            
        yield commit