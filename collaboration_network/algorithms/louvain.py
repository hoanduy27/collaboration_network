from typing import Dict

from community import community_louvain
import networkx as nx 

from .base import Algorithm

class Louvain(Algorithm):
    def __init__(self):
        pass 

    def __call__(self, G: nx.Graph) -> Dict:
        return community_louvain.best_partition(G)
    
    @property
    def name(self):
        return 'louvain'