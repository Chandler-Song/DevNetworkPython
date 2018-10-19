from typing import List
import git
from datetime import datetime
from dateutil.relativedelta import relativedelta
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
import csv
import matplotlib.pyplot as plt
from progress.bar import Bar

def centralityAnalysis(commits: List[git.Commit], outputDir: str):

    # define dictionary of authors and authors related to them
    allRelatedAuthors = {}
    
    # for all commits...
    print("Analyzing centrality...")
    for commit in Bar('Processing').iter(commits):
        author = commit.author.email
        
        # initialize dates for related author analysis
        commitDate = datetime.fromtimestamp(commit.committed_date)
        earliestDate = commitDate + relativedelta(months=-1)
        latestDate = commitDate + relativedelta(months=+1)
        
        # find authors related to this commit
        commitRelatedCommits = filter(lambda c:
            findRelatedCommits(author, earliestDate, latestDate, c), commits)
        
        commitRelatedAuthors = set(list(map(lambda c: c.author.email, commitRelatedCommits)))
        
        # get current related authors collection and update it
        authorRelatedAuthors = allRelatedAuthors.setdefault(author, set())
        authorRelatedAuthors.update(commitRelatedAuthors)

    # prepare graph
    print("Preparing NX graph...")
    G = nx.Graph()
    
    for author in allRelatedAuthors:
        for relatedAuthor in allRelatedAuthors[author]:
            G.add_edge(author.strip(), relatedAuthor.strip())
       
    # analyze graph
    closeness = dict(nx.closeness_centrality(G))
    betweenness = dict(nx.betweenness_centrality(G))
    centrality = dict(nx.degree_centrality(G))
    density = nx.density(G)
    modularity = list(greedy_modularity_communities(G))
    
    print("Outputting CSVs...")
    
    # output non-tabular results
    with open(outputDir + '\projectAnalysis.csv', 'a', newline='') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(['Density', density])
        w.writerow(['Community Count', len(modularity)])
        
    # output community information
    with open(outputDir + '\communityAuthors.csv', 'a', newline='') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(['Community Index', 'Author Count'])
        for idx, community in enumerate(modularity):
            w.writerow([idx+1, len(modularity[idx])])
    
    # combine centrality results
    combined = {}
    for key in closeness:
        single = {
                'Author': key,
                'Closeness': closeness[key],
                'Betweenness': betweenness[key],
                'Centrality': centrality[key]
                }
        
        combined[key] = single
    
    # output tabular results
    with open(outputDir + '\centralityAnalysis.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, ['Author','Closeness','Betweenness','Centrality'])
        w.writeheader()
        
        for key in combined:
            w.writerow(combined[key])
            
    # output graph to PNG
    print("Outputting graph to PNG...")
    graphFigure = plt.figure(5,figsize=(30,30))
    nx.draw(G, with_labels=True, node_color='orange', node_size=4000, edge_color='black', linewidths=2, font_size=20)
    graphFigure.savefig(outputDir + '\centralityGraph.png')

# helper functions
def findRelatedCommits(author, earliestDate, latestDate, commit):
    isDifferentAuthor = author != commit.author.email
    if not isDifferentAuthor:
        return False
        
    commitDate = datetime.fromtimestamp(commit.committed_date)
    isInRange = commitDate >= earliestDate and commitDate <= latestDate
    return isInRange