from inspect import isfunction
from typing import Dict, Union, Callable
import networkx as nx
from .base import Algorithm

from cdlib import algorithms as cdalg
from cdlib import NodeClustering


class CDLibAlgorithm(Algorithm):
    def __init__(
            self, 
            algorithm: Union[str, Callable], 
            algorithm_params: Dict = {}, 
            *args, **kwargs
        ):
        if isfunction(algorithm):
            self.algorithm = algorithm
        
        elif isinstance(algorithm, str):
            self.algorithm = getattr(cdalg, algorithm)

        else:
            raise ValueError("algorithm should be string (function name) or Callable of cdlib.evaluation")
        
        super(CDLibAlgorithm, self).__init__(*args, **kwargs)

        
        self.algorithm_params = algorithm_params

    def __call__(self, G: nx.Graph):
        community = self.algorithm(G, **self.algorithm_params)
        partition = dict(community.to_node_community_map())
        partition = {k:partition[k][0] for k in G.nodes()}  
        
        return partition
    
    @property
    def default_name(self):
        if isfunction(self.algorithm):
            return self.algorithm.__name__
        elif isinstance(self.algorithm, str):
            return self.algorithm
        else:
            raise RuntimeError("Algorithm type not valid. To fix, read code.")
        