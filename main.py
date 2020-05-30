import sys, getopt, os, subprocess, shutil
import git
import yaml

from configuration import Configuration
from repoLoader import getRepo
from aliasWorker import replaceAliases
from commitAnalysis import commitAnalysis
from centralityAnalysis import centralityAnalysis
from tagAnalysis import tagAnalysis
from graphqlAnalysis import graphqlAnalysis
from devAnalysis import devAnalysis

FILEBROWSER_PATH = os.path.join(os.getenv("WINDIR"), "explorer.exe")


def main(argv):
    try:
        # parse args
        configFile = ""
        pat = ""

        try:
            opts, args = getopt.getopt(argv, "hc:p:", ["help", "config=", "pat="])
        except getopt.GetoptError:
            print(
                "ERROR: incorrect arguments!\nmain.py -c <config.yml> -p <GitHub PAT>"
            )
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print("main.py -c <config.yml> -p <GitHub PAT>")
                sys.exit()
            elif opt in ("-c", "--config"):
                configFile = arg
            elif opt in ("-p", "--pat"):
                pat = arg

        # validate file
        if not os.path.exists(configFile):
            sys.exit("ERROR: configuration file not found")

        # read configuration
        config = ...  # type: Configuration
        with open(configFile, "r", encoding="utf-8-sig") as file:
            content = file.read()
            config = yaml.load(content, Loader=yaml.FullLoader)

        # get repository reference
        repo = getRepo(config)

        # delete any existing output files for repo
        if os.path.exists(config.analysisOutputPath):
            shutil.rmtree(config.analysisOutputPath, False)

        os.makedirs(config.analysisOutputPath)

        # handle aliases
        commits = list(replaceAliases(repo.iter_commits(), config.aliasPath))

        # run analysis
        tagAnalysis(repo, config.analysisOutputPath)
        authorInfoDict = commitAnalysis(commits, config.analysisOutputPath)
        centralityAnalysis(repo, commits, config.analysisOutputPath)
        issueOrPrDevs = graphqlAnalysis(
            pat, config.repositoryShortname, config.analysisOutputPath
        )
        devAnalysis(authorInfoDict, issueOrPrDevs, config.analysisOutputPath)

        # open output directory
        explore(config.analysisOutputPath)

    finally:
        # close repo to avoid resource leaks
        if "repo" in locals():
            del repo


class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=""):
        print(self._cur_line, end="\r")


def commitDate(tag):
    return tag.commit.committed_date


# https://stackoverflow.com/a/50965628
def explore(path):
    # explorer would choke on forward slashes
    path = os.path.normpath(path)

    if os.path.isdir(path):
        subprocess.run([FILEBROWSER_PATH, path])
    elif os.path.isfile(path):
        subprocess.run([FILEBROWSER_PATH, "/select,", os.path.normpath(path)])


if __name__ == "__main__":
    main(sys.argv[1:])
