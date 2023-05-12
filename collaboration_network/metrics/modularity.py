import networkx as nx
from .base import Metric

class Modularity(Metric):
    def __init__(self, name="modularity", *args, **kwargs):
        super(Modularity, self).__init__(name, *args, **kwargs)

    def __call__(self, G: nx.Graph, partition:dict):
        communities = []
        for community in set(partition.values()):
            communities.append(set( 
                node for node in partition if partition[node] == community
            ))

        return nx.community.modularity(G, communities)
