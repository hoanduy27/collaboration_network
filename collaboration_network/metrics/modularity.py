import networkx as nx
from .base import Metric

class Modularity(Metric):
    def __init__(self, name="modularity", *args, **kwargs):
        super(Modularity, self).__init__(name, *args, **kwargs)

    def call(self, G: nx.Graph, partition:dict):
        sub_partition = {node:partition[node] for node in partition if node in G}
        communities = []
        for community in set(sub_partition.values()):
            communities.append(set( 
                node for node in sub_partition if sub_partition[node] == community
            ))

        return nx.community.modularity(G, communities)
