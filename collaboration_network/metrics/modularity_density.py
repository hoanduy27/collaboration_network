import networkx as nx
from .base import Metric

from cdlib import evaluation as cdeval
from cdlib import NodeClustering

class ModularityDensity(Metric):
    def __init__(self, name="modularity_density", *args, **kwargs):
        super(ModularityDensity, self).__init__(name, *args, **kwargs)

    def call(self, G: nx.Graph, partition:dict):
        # communities = []
        # for community in set(partition.values()):
        #     communities.append([
        #         node for node in partition if partition[node] == community
        #     ])

        # nc = NodeClustering(communities, G)

        # return cdeval.modularity_density(G, nc).score
        return modularity_density(partition, G)


def modularity_density(partition, graph, weight='weight'):
    """Compute the modularity of a partition of a graph

    Parameters
    ----------
    partition : dict
       the partition of the nodes, i.e a dictionary where keys are their nodes
       and values the communities
    graph : networkx.Graph
       the networkx graph which is decomposed
    weight : str, optional
        the key in graph to use as weight. Default to 'weight'


    Returns
    -------
    modularity : float
       The modularity

    Raises
    ------
    KeyError
       If the partition is not a partition of all graph nodes
    ValueError
        If the graph has no link
    TypeError
        If graph is not a networkx.Graph

    References
    ----------
    .. 1. Newman, M.E.J. & Girvan, M. Finding and evaluating community
    structure in networks. Physical Review E 69, 26113(2004).

    Examples
    --------
    >>> import community as community_louvain
    >>> import networkx as nx
    >>> G = nx.erdos_renyi_graph(100, 0.01)
    >>> partition = community_louvain.best_partition(G)
    >>> modularity_density(partition, G)
    """
    if graph.is_directed():
        raise TypeError("Bad graph type, use only non directed graph")

    inc = dict([])
    deg = dict([])
    links = graph.size(weight=weight)
    if links == 0:
        raise ValueError("A graph without link has an undefined modularity")

    for node in graph:
        com = partition[node]
        deg[com] = deg.get(com, 0.) + graph.degree(node, weight=weight)
        for neighbor, datas in graph[node].items():
            edge_weight = datas.get(weight, 1)
            if partition[neighbor] == com:
                if neighbor == node:
                    inc[com] = inc.get(com, 0.) + float(edge_weight)
                else:
                    inc[com] = inc.get(com, 0.) + float(edge_weight) / 2.

    res = 0.
    scale = max(graph[u][v][weight] for u,v in graph.edges())
    for com in set(partition.values()):
        com_size = len([node for node in partition if partition[node] == com])
        ds = inc.get(com, 0.) / (scale * com_size * (com_size - 1) ) if com_size > 1 else 0

        res += (inc.get(com, 0.) *ds / links) - \
               (deg.get(com, 0.) *ds/ (2. * links)) ** 2
    return res
