import networkx as nx
from .base import Metric

from cdlib import evaluation as cdeval
from cdlib import NodeClustering

class ModularityDensity(Metric):
    def __init__(self, name="modularity_density", *args, **kwargs):
        super(ModularityDensity, self).__init__(name, *args, **kwargs)

    def __call__(self, G: nx.Graph, partition:dict):
        communities = []
        for community in set(partition.values()):
            communities.append([
                node for node in partition if partition[node] == community
            ])

        nc = NodeClustering(communities, G)

        return cdeval.modularity_density(G, nc).score
    