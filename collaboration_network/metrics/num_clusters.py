import networkx as nx
from .base import Metric

class NumClusters(Metric):
    def __init__(self, name="num_clusters", *args, **kwargs):
        super(NumClusters, self).__init__(name, *args, **kwargs)

    def __call__(self, G: nx.Graph, partition:dict):
        return len(set(partition.values()))
