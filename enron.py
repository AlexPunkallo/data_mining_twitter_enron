
# 1) Preparing Enron Dataset

import networkx as nx
from networkx import degree_centrality, closeness_centrality
import matplotlib.pyplot as plt
import operator

g = nx.Graph ()
file = 'Email-Enron.txt'
enron = nx.read_adjlist(file , delimiter = '\t', create_using = nx.DiGraph())

# 2) Use the NetworkX package to perform the following simple operations:

    # a) Compute and plot Degree Distribution

print "\n Loading Degree Distribution...\n"
def degree_distribution():
    dic = {}
    for n in enron.nodes():
        d = enron.degree(n)
        if d not in dic:
            dic[d] = 0
        dic[d] += 1
    items = sorted (dic.items())
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter([x for (x ,y) in items] ,[y for (x, y) in items])
    ax.set_xscale ('log')
    ax.set_yscale ('log')
    plt.title ("Enron Dataset Distribution")
    fig.savefig ("degree_distribution.png")
    plt.show()
degree_distribution()
print "\n Degree Distribution plotted\n"

# b) Compute the degree, closeness, betweeness, and PageRank centralities

    # Degree Centrality
    
print "\n Loading Degree Centrality...\n "
deg_cen=nx.degree_centrality(enron)
print "\n Degree Centrality done \n"

    # Closeness Centrality

cl_cen=nx.closeness_centrality(enron)
print "\n Loading Closeness Centrality...\n"
print bet_cen
print "\n Closeness Centrality done \n"

    # Betweeness Centrality

bet_cen=nx.betweenness_centrality(enron)
print "\n Loading Betweenness Centrality...\n"
print bet_cen
print "\n Betweenness Centrality done \n"

    # Page Rank Centrality

page_rank=nx.pagerank(enron, alpha=0.9)
print "\n Loading Page Rank Centrality...\n"
print page_rank
print "\n Page Rank Centrality done \n"

# c) Compute the clustering coefficient of some of the nodes, and the clustering coefficient of the graph

    # Adjust the graph

enron_und=enron.to_undirected()
print enron_und

    # Clustering coefficient of the graph

clust=nx.clustering(enron_und)
print "\n Loading Clustering Coefficient... \n"
print clust
print "\n Clustering Coefficient done \n"

# d) Compute the connected components of the graph

con_comp=nx.connected_components(enron_und)
print "\n Loading Connected components of the graph...\n"
print con_comp
print "\n Connected components done \n"

# e) Perform the k-core decomposition of the largest component

k_core=nx.k_core(enron_und)
print "\n K-core decomposition loading..."
print k_core
print "\n K-core decomposition done \n"

