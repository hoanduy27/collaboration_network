from time import time
from typing import Dict, List, Tuple
import logging

import networkx as nx
import numpy as np
import pandas as pd
from tqdm import tqdm


from collaboration_network import algorithms, metrics, utils

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

    def run_one_step(self, algorithm, thres=None):
        metric_result = {}

        start_s = time()
        G_sub, partition = algorithm(self.G, w_min=thres, return_pruned_graph=True)
        metric_result['exec_time'] = time() - start_s

        for metric_class, params in self.metrics:
            try:
                metric = metric_class(**params)
                metric_result[metric.name] = metric(self.G, partition).score()
            except Exception as e:
                logging.exception(e)
                metric_result[metric.name] = None 
                continue

        return metric_result
        

    def run(self):
        results = []
        for algorithm_class , params in self.algorithms:
            algorithm = algorithm_class(**params)
            print(f'Running algorithm: {algorithm.name}')

            for rtime in tqdm(range(self.n_iters)):
                # Not use linkage threshold
                if not self.linkage:
                    runtime_result = dict(
                        run_id = rtime, 
                        method = algorithm.name,
                    )
                    try:
                        metric_result = self.run_one_step(algorithm)
                    except:
                        logging.exception(e)
                        continue
                    runtime_result.update(metric_result)

                    results.append(runtime_result)
                # Use linkage threshold
                else:
                    for thres in tqdm(self.linkage_threshold):
                        runtime_result = dict(
                            run_id = rtime, 
                            method = algorithm.name,
                            linkage_thres = thres
                        )

                        # G_sub = utils.prune_graph(self.G, thres, self.weight)
                        try:
                            metric_result = self.run_one_step(algorithm, thres)
                        except Exception as e:
                            logging.exception(e)
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