import networkx as nx 

from collaboration_network import metrics
from collaboration_network import algorithms
from collaboration_network.benchmark import Benchmark

G = nx.read_gml('graphs/G_dir_alpha0.8_beta1.0.gml')

bm = Benchmark(
    G, 
    algorithms=[
        (algorithms.GirvanNewman, dict(level=3)),
        (algorithms.Louvain, {}),
        (algorithms.Leiden, {}),
    ],
    metrics=[
        (metrics.NumClusters, {}),
        (metrics.Modularity, {}),
        (metrics.CDLibMetric, dict(metric='internal_edge_density')),
        (metrics.CDLibMetric, dict(metric='cut_ratio')),
    ],
    n_iters=5,
    linkage=True,
    num_thres=20
)

result = bm.run()

result.to_csv('log/benchmark_full.csv', index=0)