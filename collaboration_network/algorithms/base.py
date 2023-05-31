import networkx as nx
from collaboration_network import utils

class Algorithm:
    def __init__(self, name=None):
        if name is None:
            self.name = self.default_name 
        else:
            self.name = name
        
    def preprocess_graph(self, G, w_min):
        G_sub = utils.prune_graph(G, threshold=w_min)

        return G_sub
    
    def call(self, G: nx.Graph):
        raise NotImplementedError
    
    def __call__(self, G, w_min=None):
        G_sub = G.copy()
        if w_min is not None:
            G_sub = self.preprocess_graph(G_sub, w_min) 

        partition = self.call(G_sub)
         
        return partition

    @property
    def default_name(self):
        raise NotImplementedError