from typing import Dict

# from community import community_louvain
import networkx as nx 

from .base import Algorithm
from .louvain_md_utils import best_partition

class LouvainMD(Algorithm):
    def __init__(self, 
                    weight='weight',
                    scale='auto',
                    randomize=None,
                    random_state=None,
                    *args, **kwargs
                ):
    
        super(LouvainMD, self).__init__(*args, **kwargs)
        self.weight = weight
        self.scale = scale
        self.randomize = randomize
        self.random_state = random_state

    def __call__(self, G: nx.Graph) -> Dict:
        if self.scale == 'auto':
            scale = max(G[u][v][self.weight] for u,v in G.edges())

        return best_partition(G, 
                              weight=self.weight, 
                              resolution=scale, 
                              randomize=self.randomize, 
                              random_state = self.random_state
                            )
    
    @property
    def default_name(self):
        return 'louvain_md'