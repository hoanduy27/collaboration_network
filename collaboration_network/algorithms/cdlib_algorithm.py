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
            name: str = None, 
            *args, **kwargs
        ):
        super(CDLibAlgorithm, self).__init__(name, *args, **kwargs)

        if isfunction(algorithm):
            self.algorithm = algorithm
        
        elif isinstance(algorithm, str):
            self.algorithm = getattr(cdalg, algorithm)

        else:
            raise ValueError("algorithm should be string (function name) or Callable of cdlib.evaluation")
        
        self.algorithm_params = algorithm_params
        if name is None:
            self.name = self.algorithm.__name__

    def __call__(self, G: nx.Graph):
        community = self.algorithm(G, **self.algorithm_params)
        partition = dict(community.to_node_community_map())
        partition = {k:partition[k][0] for k in G.nodes()}  
        
        return partition