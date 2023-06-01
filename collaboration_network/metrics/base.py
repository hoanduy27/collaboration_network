import networkx as nx
from collaboration_network import utils
from collections import Counter
from dataclasses import dataclass
from typing import List
import json

NONE = 'none'
COMMUNITY = 'community'
CONNECTED_COMPONENT = 'connected_component'

@dataclass
class MetricResult:
    
    min_size_type: str = NONE
    min_size: List[int] = None
    result: List[float] = None

    def to_dict(self):
        return dict(zip(self.min_size, self.result))
    
    def to_json(self):
        return json.dumps(dict(
            min_size_type = self.min_size_type,
            result = dict(zip(self.min_size, self.result))
        ))
    
    def score(self):
        if self.min_size_type == NONE:
            return self.result[0]
        else:
            return self.to_json()

class Metric:
    def __init__(
            self, 
            name, 
            min_size_partition=None, 
            min_size_connected_component=None
        ):
        self.name = name
        self.min_size_partition = min_size_partition
        self.min_size_connected_component = min_size_connected_component

    def call(self, G: nx.Graph, partition: dict):
        raise NotImplementedError
    
    def call_normal(
            self, 
            G:nx.Graph, 
            partition:dict, 
            min_size_partition, 
            min_size_connected_component
        ):
        G_sub = G.copy()
        if self.min_size_partition is not None:
            G_sub = utils.prune_graph_by_cluster_size(
                G_sub, 
                partition, 
                min_size_partition
            )
        if self.min_size_connected_component is not None:
            G_sub = utils.prune_graph_by_connected_components(
                G_sub, 
                min_size_connected_component
            )

        return self.call(G_sub, partition)

    def __call__(self, G: nx.Graph, partition:dict):
        metric_result = MetricResult(NONE, [], [])
        # print(metric_result.result)

        if self.min_size_partition != 'auto' and self.min_size_connected_component != 'auto':
            
            metric_result.min_size_type = NONE         
            metric_result.min_size.append(0)

            result = self.call_normal(
                G, 
                partition, 
                self.min_size_partition,
                self.min_size_connected_component 
            )

            metric_result.result.append(result)

        elif self.min_size_partition == 'auto':
            metric_result.min_size_type = COMMUNITY
            community_sizes = sorted(set(Counter(partition.values())))

            for com_size in community_sizes:
                result = self.call_normal(
                    G, 
                    partition,
                    com_size,
                    self.min_size_connected_component
                )
                metric_result.min_size.append(com_size)
                metric_result.result.append(result)

        elif self.min_size_connected_component == 'auto':
            metric_result.min_size_type = CONNECTED_COMPONENT
            cc_sizes = sorted(set(map(len, nx.connected_components(G))))
            for cc_size in cc_sizes:
                result = self.call_normal(
                    G, 
                    partition,
                    self.min_size_partition,
                    cc_size
                )
                metric_result.min_size.append(cc_size)
                metric_result.result.append(result)
        
        else:
            raise RuntimeError("Both `auto` in min_size_partition and min_size_connected_component not supported")
        
        return metric_result
