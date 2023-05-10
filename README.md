# Scientific Collaboration Network
Community Detection in Scientific Collaboration Network with networkx.

## Algorithm:
- Girvan-Newman
- Louvan
- (tbu...)

## Dataset
NIPS conference paper volume 0-12 

## Frist step: Benchmarking
Currently, use this code snippet to run the benchmark (CLI will be added later). This code will load the graph and run Lovain algorithm for 10 times. Each time will record execution time and modularity. The result is saved to `log/benchmark.csv`

```python
# example_benchmark.py

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
```

You can benchmark using the **other graph**, or using **multiple algorithms**, or **multiple metrics**. 

## Create a graph
```
$ python -m collaboration_network.create_graph <path_to_config>
```

(TBU..., just skip this part now)

## Add new algorithm
- Create a new python file in `collaboration_network/algorithms`.
- Implement a new class inherited `Algorithm`, implement `__init__` (if requires extra parameters), `__call__` (the main part of the algorithm), `__name__` (string name for writing report when running benchmark).
- **Convention**: The `__call__` method MUST return a DICTIONARY, `key` is node, `value` is community number. 
- **Example**: `collaboration_network/algorithms/louvain.py`

## Add new metric
- Create a new python file in `collaboration_network/metrics`.
- Implement a new class inherited `Metric`, implement `__init__` (if requires extra parameters), `__call__(G, partition)` (the main part of the metric for evaluat), `__name__` (string name for writing report when running benchmark).
- The `__call__` method receives `G` as the graph and `partition` as the result of algorithm (described above)
- **Example**: `collaboration_network/metrics/modularity.py`