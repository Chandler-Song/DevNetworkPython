import os
import shutil
import git

from aliasWorker import replaceAliases
from commitAnalysis import commitAnalysis
from centralityAnalysis import centralityAnalysis
from tagAnalysis import tagAnalysis

# parse arguments
repoUrl = 'https://github.com/apache/mahout'
destPath = r'C:\Users\denio\source\repos\apachemahout'
outputDir = r'C:\Users\denio\source\repos\analysisOutput'
aliasPath = None

def commitDate(tag):
    return tag.commit.committed_date

class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(self._cur_line)

try:    
    # get repository reference
    repo = None
    if not os.path.isdir(destPath):
        print("Downloading repository...")
        repo = git.Repo.clone_from(repoUrl, destPath, branch='master', progress=Progress(), odbt=git.GitCmdObjectDB)        
    else:
        repo = git.Repo(destPath, odbt=git.GitCmdObjectDB)
        
    # delete any existing output files
    if os.path.exists(outputDir):
        shutil.rmtree(outputDir)
        
    os.makedirs(outputDir)
    
    # handle aliases
    commits = list(replaceAliases(repo, aliasPath))
        
    # run analysis
    tagAnalysis(repo, outputDir)
    commitAnalysis(commits, outputDir)
    centralityAnalysis(repo, commits, outputDir)
    
finally:
    # close repo to avoid resource leaks
    del repo
    