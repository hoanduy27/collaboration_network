import networkx as nx
from .base import Metric

class Modularity(Metric):
    def __init__(self):
        pass 

    def __call__(self, G: nx.Graph, partition:dict):
        communities = []
        for community in set(partition.values()):
            communities.append(set( 
                node for node in partition if partition[node] == community
            ))

        return nx.community.modularity(G, communities)
    
    @property
    def name(self):
        return 'modularity'