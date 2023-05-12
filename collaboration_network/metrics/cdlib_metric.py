from inspect import isfunction
from typing import Dict, Union, Callable
import networkx as nx
from .base import Metric

from cdlib import evaluation as cdeval
from cdlib import NodeClustering


class CDLibMetric(Metric):
    def __init__(
            self, 
            metric: Union[str, Callable], 
            metric_params: Dict = {}, 
            name: str = None, 
            *args, **kwargs
        ):
        super(CDLibMetric, self).__init__(name, *args, **kwargs)

        if isfunction(metric):
            self.metric = metric
        
        elif isinstance(metric, str):
            self.metric = getattr(cdeval, metric)

        else:
            raise ValueError("metric should be string (function name) or Callable of cdlib.evaluation")
        
        self.metric_params = metric_params
        if name is None:
            self.name = self.metric.__name__

    def __call__(self, G: nx.Graph, partition:dict):
        communities = []
        for community in set(partition.values()):
            communities.append([
                node for node in partition if partition[node] == community
            ])

        nc = NodeClustering(communities, G)

        return self.metric(G, nc, **self.metric_params).score