import networkx as nx 
from typing import List, Tuple, Dict
from collaboration_network import metrics 
from collaboration_network import algorithms
import pandas as pd 
from time import time

class Benchmark:
    def __init__(
            self, 
            G: nx.Graph, 
            algorithms: List[Tuple[algorithms.Algorithm, Dict]], 
            metrics: List[metrics.Metric], 
            n_iters=10
        ):
        self.G = G
        self.algorithms = algorithms
        self.metrics = metrics 
        self.n_iters = n_iters

    def run(self):
        results = []
        for algorithm_class , params in self.algorithms:
            algorithm = algorithm_class(**params)

            for rtime in range(self.n_iters):
                runtime_result = {}

                start_s = time()
                partition = algorithm(self.G)
                exec_time = time()-start_s 

                runtime_result.update(dict(
                    run_id=rtime,
                    method=algorithm.name,
                    execution_time=exec_time
                ))

                for metric_class in self.metrics:
                    metric = metric_class()
                    runtime_result[metric.name] = metric(self.G, partition)
                
                results.append(runtime_result)
        
        return pd.DataFrame(results)

if __name__ == '__main__':
    # SAMPLE CODE
    G = nx.read_gml('graphs/G_dir_alpha0.8_beta1.0.gml')

    bm = Benchmark(
        G, 
        algorithms=[
            (algorithms.Louvain, {})
        ],
        metrics=[metrics.Modularity],
        n_iters=10
    )

    result = bm.run()

    result.to_csv('benchmark.csv', index=0)