from typing import Dict

from cdlib import algorithms as cdalg
import networkx as nx 

from community import community_louvain
from .base import Algorithm

class GirvanNewman(Algorithm):
    def __init__(self, level=3):
        self.level=level

    def call(self, G: nx.Graph) -> Dict:
        
        community = cdalg.girvan_newman(G, level=self.level)
        partition = dict(community.to_node_community_map())
        partition = {k:partition[k][0] for k in G.nodes()}  
        
        return partition
    
    @property
    def default_name(self):
        return 'girvan_newman'