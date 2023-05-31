from typing import Dict

from cdlib import algorithms as cdalg
import networkx as nx 

from community import community_louvain
from .base import Algorithm

class Leiden(Algorithm):
    def __init__(self):
        pass 

    def __call__(self, G: nx.Graph) -> Dict:
        
        community = cdalg.leiden(G)
        partition = dict(community.to_node_community_map())
        partition = {k:partition[k][0] for k in G.nodes()}  
        
        return partition
    
    @property
    def default_name(self):
        return 'leiden'