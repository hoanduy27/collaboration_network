import networkx as nx 

from collaboration_network import metrics
from collaboration_network import algorithms
from collaboration_network.benchmark import Benchmark

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

result.to_csv('log/benchmark.csv', index=0)