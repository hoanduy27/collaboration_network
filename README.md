# Scientific Collaboration Network
Community Detection in Scientific Collaboration Network with networkx.

## Algorithm:
- Girvan-Newman
- Louvain
- LouvainMD

We also write a wrapper for algorithms provided in [CDLib](https://cdlib.readthedocs.io/en/latest/) (bug is expected, though).

## Metric:
- Density
- Modularity
- Modularity density

We also write a wrapper for metrics provided in [CDLib](https://cdlib.readthedocs.io/en/latest/) (bug is also expected, though. But currently **intra-cluster density** and **inter-cluster density** are successfully wrapped from this library).

## Dataset
NIPS conference paper volume 0-12 

# Installation
```sh
pip install -r requirements.txt
```

# Reproduction instructions
## 1. Create a network
```sh
python -m collaboration_network.create_graph <path_to_config>
```
Network config can be found in [config/](config/).

To create all the network in [config/](config/) folder, run:
```sh
ls config | xargs -I {} python -m collaboration_network.create_graph {}
```

## 2. Benchmarking
You can benchmark using the **Benchmark** class in [collaboration_network/benchmark](collaboration_network/benchmark.py) for benchmarking **multiple algorithms** on a graph, using **multiple metrics**.

You can run this script for benchmarking all the networks created on previous step. This script will benchmark Girvan-Newman, Louvain and LouvainMD and log all metrics (execution time, number of clusters ,modularity, modularity density, inter-cluster density, intra-cluster density) to `log` folder.
```sh
python example_benchmark.py
```

You can write a benchmark script on your own, based on the example script provided. 

## 3. Evaluation
Currently, we provide this notebook [evaluate.ipynb](evaluate.py) for plotting benchmark result.

## 4. Visualization
Currently, we provide this notebook [graph_visualization.ipynb](evaluate.py) for visualizing Girvan-Newman, Louvain and LouvainMD on the constructed network.

# Add new algorithm
- Create a new python file in `collaboration_network/algorithms`.
- Implement a new class inherited `Algorithm`, implement `__init__` (if requires extra parameters), `__call__` (the main part of the algorithm), `__name__` (string name for writing report when running benchmark).
- **Convention**: The `__call__` method MUST return a DICTIONARY, `key` is node, `value` is community number. 
- **Example**: `collaboration_network/algorithms/louvain_md.py`

# Add new metric
- Create a new python file in `collaboration_network/metrics`.
- Implement a new class inherited `Metric`, implement `__init__` (if requires extra parameters), `__call__(G, partition)` (the main part of the metric for evaluat), `__name__` (string name for writing report when running benchmark).
- The `__call__` method receives `G` as the graph and `partition` as the result of algorithm (described above)
- **Example**: `collaboration_network/metrics/modularity.py`