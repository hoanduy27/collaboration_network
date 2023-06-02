import os
import networkx as nx 
import logging
from collaboration_network import metrics
from collaboration_network import algorithms
from collaboration_network.benchmark import Benchmark

import glob 

logging.getLogger().setLevel(logging.DEBUG)
G_paths =  glob.glob('graphs/G_dir_alpha0.8_0*')

# G_paths = glob.glob('graphs/G_test.gml')

for G_path in G_paths:
    G = nx.read_gml(G_path)

    G_name = os.path.splitext(os.path.basename(G_path))[0]

    bm = Benchmark(
        G, 
        algorithms=[
            (algorithms.CDLibAlgorithm, dict(algorithm='girvan_newman', algorithm_params=dict(level=3))),
            (algorithms.CDLibAlgorithm, dict(algorithm='louvain', algorithm_params=dict(resolution=1))),
            (algorithms.CDLibAlgorithm, dict(algorithm='louvain', algorithm_params=dict(resolution=.2), name='louvain_res-0.2')),
            (algorithms.LouvainMD, dict())
        ],
        metrics=[
            (metrics.NumClusters, {}),
            (metrics.Modularity, {}),
            (metrics.Modularity, dict(name='modularity_by_min_size_cc', min_size_connected_component='auto' ) ),
            (metrics.ModularityDensity, {} ),
            (metrics.ModularityDensity, dict(name='modularity_density_by_min_size_cc', min_size_connected_component='auto') ),
            (metrics.CDLibMetric, dict(metric='internal_edge_density', name='intra_cluster_density')),
            (metrics.CDLibMetric, dict(metric='internal_edge_density', name='intra_cluster_density_by_min_size_cc',  min_size_connected_component='auto')),
            (metrics.CDLibMetric, dict(metric='cut_ratio', name='inter_cluster_density')),
            (metrics.CDLibMetric, dict(metric='cut_ratio', name='inter_cluster_density_by_min_size_cc',   min_size_connected_component='auto')),
            (metrics.Density, dict(min_size_connected_component='auto') ),
        ],
        n_iters=30,
        linkage=False,
        min_thres=0.0,
        max_thres='auto',
        num_thres=1
    )

    result = bm.run()

    os.makedirs(f'log/', exist_ok=True)

    result.to_csv(f'log/{G_name}_benchmark_full.csv', index=0)