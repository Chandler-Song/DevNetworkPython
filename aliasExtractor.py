import sys
import git
import re
import yaml
import typing
import os

from configuration import Configuration
from repoLoader import getRepo
from similarity.metric_lcs import MetricLCS
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
        
        # delete existing alias file if present
        if os.path.exists(config.aliasPath):
            os.remove(config.aliasPath)
            
        # extract aliases
        maxDistance = float(sys.argv[1])
        extractAliases(repo.iter_commits(), config.aliasPath, maxDistance)
        
    finally:
        # close repo to avoid resource leaks
        del repo

def extractAliases(commits: typing.Iterable[git.Commit], aliasPath: str, maxDistance: float):
    
    # get all distinct authors
    authors = list(set(list(commit.author.email.lower().strip() for commit in Bar('Processing').iter(list(commits)))))
    
    aliases = {}
    usedAsValues = {}
    
    for authorA in Bar('Processing').iter(authors):
        
        # go through used values
        if authorA in usedAsValues:
            continue
        
        # go through already extracted keys
        quickMatched = False
        for key in aliases:
            if authorA == key:
                quickMatched = True
                continue
            
            if (areSimilar(authorA, key, maxDistance)):
                aliases[key].append(authorA)
                usedAsValues[authorA] = key
                quickMatched = True
                break
            
        if quickMatched:
            continue
        
        # go through all authors
        for authorB in authors:
            if authorA == authorB:
                continue
            
            if (areSimilar(authorA, authorB, maxDistance)):
                aliasedAuthor = aliases.setdefault(authorA, [])
                aliasedAuthor.append(authorB)
                usedAsValues[authorB] = authorA
                break
    
    # output to yaml
    with open(aliasPath, 'a', newline='') as f:                
        yaml.dump(aliases, f)
        
def areSimilar(valueA: str, valueB: str, maxDistance: float):
    lcs = MetricLCS()
    expr = r'(.+)@'
    
    localPartAMatches = re.findall(expr, valueA)
    localPartBMatches = re.findall(expr, valueB)
    
    if (len(localPartAMatches) == 0):
        localPartAMatches = [valueA]
        
    if (len(localPartBMatches) == 0):
        localPartBMatches = [valueB]
    
    distance = lcs.distance(localPartAMatches[0], localPartBMatches[0])
    
    return distance <= maxDistance
        
main()