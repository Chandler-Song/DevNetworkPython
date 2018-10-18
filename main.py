import os
import shutil
import git

from aliasWorker import replaceAliases
from commitAnalysis import commitAnalysis
from centralityAnalysis import centralityAnalysis

# parse arguments
repoUrl = 'https://github.com/apache/gora'
destPath = r'C:\Users\denio\source\repos\gora'
outputDir = r'C:\Users\denio\source\repos\DeveloperNetwork\PythonSrc\analysisOutput'
aliasPath = r'C:\Users\denio\source\repos\DeveloperNetwork\PythonSrc\aliases\apachegora.yml'

try:    
    # get repository reference
    repo = None
    if not os.path.isdir(destPath):
        repo = git.Repo.clone_from(repoUrl, destPath, branch='master')
    else:
        repo = git.Repo(destPath)
        
    # delete any existing output files
    if os.path.exists(outputDir):
        shutil.rmtree(outputDir)
        
    os.makedirs(outputDir)
    
    # handle aliases
    commits = list(replaceAliases(repo, aliasPath))
        
    # run analysis
    commitAnalysis(commits, outputDir)
    centralityAnalysis(commits, outputDir)
    
finally:
    # close repo to avoid resource leaks
    del repo