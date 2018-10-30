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

def extractAliases(commits: typing.Iterable[git.Commit], aliasPath: str, maxDistance: int):
    
    # get set of all authors
    authors = set(list(commit.author.email.lower().strip() for commit in Bar('Processing').iter(list(commits))))
    
    # find all A>B aliases
    allAliases = set()
    lcs = MetricLCS()
    expr = r'(.+)@'
    
    for authorA in Bar('Processing').iter(authors):
        for authorB in authors:
            if (authorA == authorB):
                continue
                            
            localPartAMatches = re.findall(expr, authorA)
            localPartBMatches = re.findall(expr, authorB)
            
            if (len(localPartAMatches) == 0):
                localPartAMatches = [authorA]
                
            if (len(localPartBMatches) == 0):
                localPartBMatches = [authorB]
            
            distance = lcs.distance(localPartAMatches[0], localPartBMatches[0])
            
            if (distance > maxDistance):
                continue
                
            aliasKey = authorA + ">" + authorB
            allAliases.add(aliasKey)
                
    # normalize to one alias and its derivatives
    normalizedAliases = {}
    usedAsKeys = set()
    usedAsValues = {}
    
    for alias in Bar('Processing').iter(allAliases):
        split = alias.split('>')
        frm = split[0]
        to = split[1]
        
        if to in usedAsKeys:
            normalized = normalizedAliases.setdefault(to, set())
            normalized.add(frm)
            usedAsKeys.add(to)
            usedAsValues[frm] = to
            
        elif frm in usedAsValues:
            parent = usedAsValues[frm]
            normalized = normalizedAliases.setdefault(parent, set())
            normalized.add(to)
            usedAsValues[to] = parent
            
        elif to in usedAsValues:
            parent = usedAsValues[to]
            normalized = normalizedAliases.setdefault(parent, set())
            normalized.add(frm)
            usedAsValues[frm] = parent
            
        else: #if frm in usedAsKeys:
            normalized = normalizedAliases.setdefault(frm, set())
            normalized.add(to)
            usedAsKeys.add(frm)
            usedAsValues[to] = frm
            
    # make all sets lists for cleaner output
    for alias in normalizedAliases:
        normalizedAliases[alias] = list(normalizedAliases[alias])
    
    # output to yaml
    with open(aliasPath, 'a', newline='') as f:                
        yaml.dump(normalizedAliases, f)
        
main()