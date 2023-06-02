import os
import re
from typing import Union
import networkx as nx
import functools as ft

import pandas as pd 

def path_to_paper_ids(elem):
    path = elem[0]
    volume = path.split('/')[0][4:]

    paper_num = int(os.path.basename(os.path.splitext(path)[0]))
    return f"{volume}.{paper_num}"

def read_author(filepath):
    volume = os.path.basename(filepath)

    volume = os.path.splitext(volume)[0][1:]

    authors = []

    with open(filepath, 'r') as f: 
        for data in f.readlines():
            data = data.strip()
            author = re.sub(r"([^0-9]*),[ ,0-9]*$", r'\1', data)
            paper_ids = re.sub(r"[^0-9]*,([ ,0-9]*)$", r'\1', data)

            last_name, first_name = author.split(',')

            last_name = last_name.strip().upper()
            first_name = first_name.strip().upper()
            paper_ids = paper_ids.split(',') 
            paper_ids = list(map((lambda pid: '.'.join([volume, pid.strip()])), paper_ids))

            authors.append(dict(last_name=last_name, first_name=first_name, paper_ids=paper_ids))
    
    return pd.DataFrame(authors)

def merge_paper(x: pd.DataFrame):
    last_name = x.iloc[0].last_name
    first_name = x.iloc[0].first_name 
    paper_ids = ft.reduce(lambda cur, next: cur + next, x.paper_ids, [])

    return pd.Series(dict(last_name=last_name, first_name=first_name, paper_ids=paper_ids))

def prune_graph(G: nx.Graph, threshold: float, weight: str='weight'):
    G_sub = G.copy() 
    edge_to_removes = [(u,v) for u,v in G.edges() if G[u][v][weight] < threshold]

    G_sub.remove_edges_from(edge_to_removes)

    return G_sub

def prune_graph_by_cluster_size(G: nx.Graph, partition:dict, min_size: int = None):
    G_common = G.copy() 
    node_to_del = [] 
    
    for community in set(partition.values()):
        community_nodes = [node for node in partition.keys() if partition[node] == community]
        com_size = len(community_nodes)
        if com_size < min_size:
            node_to_del.extend(community_nodes)
    G_common.remove_nodes_from(node_to_del)
    partition_common = {node:partition[node] for node in G_common.nodes()}

    return G_common, partition_common

def prune_graph_by_connected_components(G: nx.Graph, min_size=None):
    G_common = G.copy() 
    node_to_del = [] 
    
    for node_set in nx.connected_components(G):
        if len(node_set) < min_size:
            node_to_del.extend(list(node_set))
        
    G_common.remove_nodes_from(node_to_del)

    # if partition is not None:
    #     partition_common = {node: partition[node] for node in G_common}

    #     return G_common, partition_common

    return G_common


    