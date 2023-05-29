import networkx as nx 
import os
from collaboration_network import metrics
from collaboration_network import algorithms
from collaboration_network.benchmark import Benchmark

import glob 
# G_paths =  glob.glob('graphs/G_dir_alpha0.8_0*')
G_paths = glob.glob('graphs/G_test.gml')

for G_path in G_paths:
    G = nx.read_gml(G_path)
    G_name = os.path.splitext(os.path.basename(G_path))[0]

    bm = Benchmark(
        G, 
        algorithms=[
            # (algorithms.GirvanNewman, dict(level=3)),
            # (algorithms.CDLibAlgorithm, dict(algorithm='lswl_plus')),
            (algorithms.CDLibAlgorithm, dict(algorithm='louvain', algorithm_params=dict(resolution=1.), name='louvain_res-1.0')),
            (algorithms.CDLibAlgorithm, dict(algorithm='louvain', algorithm_params=dict(resolution=.8), name='louvain_res-0.8')),
            (algorithms.CDLibAlgorithm, dict(algorithm='louvain', algorithm_params=dict(resolution=.6), name='louvain_res-0.6')),
            (algorithms.CDLibAlgorithm, dict(algorithm='louvain', algorithm_params=dict(resolution=.4), name='louvain_res-0.4')),
            (algorithms.CDLibAlgorithm, dict(algorithm='louvain', algorithm_params=dict(resolution=.2), name='louvain_res-0.2')),
            (algorithms.CDLibAlgorithm, dict(algorithm='girvan_newman', algorithm_params=dict(level=5), name='girvan_newman_lv-5')),
            (algorithms.CDLibAlgorithm, dict(algorithm='girvan_newman', algorithm_params=dict(level=4), name='girvan_newman_lv-4')),
            (algorithms.CDLibAlgorithm, dict(algorithm='girvan_newman', algorithm_params=dict(level=3), name='girvan_newman_lv-3')),
            (algorithms.CDLibAlgorithm, dict(algorithm='girvan_newman', algorithm_params=dict(level=2), name='girvan_newman_lv-2')),
        ],
        metrics=[
            (metrics.NumClusters, {}),
            (metrics.Modularity, {}),
            (metrics.CDLibMetric, dict(metric='internal_edge_density', name='intra_cluster_density')),
            (metrics.CDLibMetric, dict(metric='cut_ratio', name='inter_cluster_density')),
        ],
        n_iters=1,
        linkage=True,
        min_thres=0.0,
        max_thres='auto',
        num_thres=10
    )

    result = bm.run()

    os.makedirs(f'log/', exist_ok=True)

    result.to_csv(f'log/{G_name}_benchmark_full.csv', index=0)