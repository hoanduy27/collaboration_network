import networkx as nx 
from typing import List, Tuple, Dict
import numpy as np 
from collaboration_network import metrics 
from collaboration_network import algorithms
import pandas as pd 
from time import time
from tqdm import tqdm
from collaboration_network import utils

class Benchmark:
    def __init__(
            self, 
            G: nx.Graph, 
            algorithms: List[Tuple[algorithms.Algorithm, Dict]], 
            metrics: List[Tuple[metrics.Metric, Dict]], 
            n_iters=10, 
            linkage=False,
            min_thres=0.0,
            max_thres='auto',
            num_thres=20,
            weight: str = "weight"
        ):
        self.G = G
        self.algorithms = algorithms
        self.metrics = metrics 
        self.n_iters = n_iters
        self.linkage = linkage
        self.weight = weight

        if self.linkage:
            if max_thres == 'auto':
                max_thres = max(G[u][v][weight] for u,v in G.edges())
            step = (max_thres - min_thres) / (num_thres - 1)
            self.linkage_threshold = np.arange(min_thres, max_thres+step, step)

    def run_one_step(self, G, algorithm):
        metric_result = {}

        start_s = time()
        partition = algorithm(G)
        metric_result['exec_time'] = time() - start_s

        for metric_class, params in self.metrics:
            metric = metric_class(**params)
            metric_result[metric.name] = metric(G, partition)

        return metric_result
        

    def run(self):
        results = []
        for algorithm_class , params in self.algorithms:
            algorithm = algorithm_class(**params)
            print(f'Running algorithm: {algorithm.name}')

            for rtime in tqdm(range(self.n_iters)):
                if not self.linkage:
                    runtime_result = dict(
                        run_id = rtime, 
                        method = algorithm.name,
                    )
                    try:
                        metric_result = self.run_one_step(self.G, algorithm)
                    except:
                        continue
                    runtime_result.update(metric_result)

                    results.append(runtime_result)
                else:
                    for thres in tqdm(self.linkage_threshold):
                        runtime_result = dict(
                            run_id = rtime, 
                            method = algorithm.name,
                            linkage_thres = thres
                        )

                        G_sub = utils.prune_graph(self.G, thres, self.weight)
                        try:
                            metric_result = self.run_one_step(G_sub, algorithm)
                        except Exception as e:
                            continue

                        runtime_result.update(metric_result)

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