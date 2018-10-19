import os
import shutil
import git

from aliasWorker import replaceAliases
from commitAnalysis import commitAnalysis
from centralityAnalysis import centralityAnalysis

# parse arguments
repoUrl = 'https://github.com/qemu/qemu'
destPath = r'D:\Repos\qemu5'
outputDir = r'D:\Repos\DevNetworkPython\analysisOutput'
aliasPath = None

class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(self._cur_line)

try:    
    # get repository reference
    repo = None
    if not os.path.isdir(destPath):
        print("Downloading repository...")
        repo = git.Repo.clone_from(repoUrl, destPath, branch='master', progress=Progress())        
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
    