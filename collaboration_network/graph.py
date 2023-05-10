import argparse
import glob
import logging
import functools as ft
import yaml

import networkx as nx
import numpy as np
import pandas as pd
import scipy.io
from tqdm import tqdm 

from collaboration_network import utils

DIRECT = 'direct'
INDIRECT = 'indirect'
INTERACT = 'interact'

class CollaborationGraph(nx.Graph):
    @classmethod 
    def from_config(cls, config_path):
        with open(config_path, 'r') as f:
            config = yaml.load(f, Loader=yaml.Loader)     
            args = argparse.Namespace(**config)

        
        # Read mat file to extract paper id, paper length, number of author/paper
        logging.info("Read paper info")
        mat = scipy.io.loadmat(args.matlab_raw_file)
        
        paper_ids = list(map(utils.path_to_paper_ids,  mat['docnames'].reshape(-1)))

        paper_lengths= mat['plengths'].reshape(-1)
        paper_num_authors = mat['panum'].reshape(-1)

        paper_info = {}
        for pid, plength, n_authors in zip(paper_ids, paper_lengths, paper_num_authors):
            paper_info[pid] = dict(length=plength, n_authors=n_authors)

        # Load author
        logging.info("Load author")
        if isinstance(args.idx_files, str):
            filepaths = glob.glob(args.idx_files)

        elif isinstance(args.idx_files, list):
            filepaths = ft.reduce(
                lambda cur, next: cur + glob.glob(next), 
                args.idx_files, []
            )   

        df = pd.concat([utils.read_author(fp) for fp in filepaths])

        # Map same author to one
        logging.info("Merge authors")
        if args.author_map is not None:
            df_author = pd.read_csv(args.author_map)
            df_author['final_group'] = (df_author.change_group.fillna(0) + df_author.change_more.fillna(0)) \
                                        .cumsum().astype(int)
            df = df.merge(df_author[['last_name', 'first_name', 'final_group']], on=['last_name', 'first_name'])

            df = df.groupby('final_group').apply(utils.merge_paper)
        else:
            df = df.groupby(['last_name', 'first_name']).apply(utils.merge_paper)

        df['full_name'] = df.apply(lambda x: x.last_name + ', ' + x.first_name, axis=1)

        # Create Graph
        logging.info("Create graph represents direct links")
        weight_type = args.weight_type
        alpha = args.weight_conf.get('alpha', 1.)
        beta = args.weight_conf.get('beta', 0.)

        # Create graph with direct edges
        G = nx.Graph()

        # Add nodes (node represents author) to the graph
        G.add_nodes_from(df.full_name)

        # Add edge with direct_weight, interact_weight
        for i in tqdm(range(len(df))):
            for j in range(i+1, len(df)):
                author_1 = df.iloc[i].full_name 
                papers_1 = set(df.iloc[i].paper_ids)

                author_2 = df.iloc[j].full_name 
                papers_2 = set(df.iloc[j].paper_ids)

                common_papers = papers_1.intersection(papers_2)
                if common_papers:
                    direct_weight = 1
                    interact_weight = sum(
                        [paper_info[paper]['n_authors']/np.sqrt(paper_info[paper]['length']) for paper in common_papers]
                    )/len(common_papers)

                    weight = direct_weight - beta * interact_weight
                    G.add_edge(author_1, author_2, direct_weight=direct_weight, interact_weight=interact_weight, weight = weight)
        
        if INDIRECT in weight_type and alpha != 1.:
            logging.info("Create graph represents indirect links")
            # Create a graph
            G_flex = nx.Graph()

            # Add nodes (node represents author) to the graph
            G_flex.add_nodes_from(df.full_name)
            for i in tqdm(range(G.number_of_nodes())):
                for j in range(i+1, G.number_of_nodes()):
                    u = list(G)[i]
                    v = list(G)[j]
                    # Error will raise if u and v does not have direct link, 
                    # in this case, we set the corresponding weight to 0
                    try:
                        direct_weight = G[u][v]['direct_weight']
                    except: 
                        direct_weight = 0 

                    try:
                        interact_weight = G[u][v]['interact_weight']
                    except:
                        interact_weight = 0

                    n_u_neighbors = G.degree(u)
                    n_v_neighbors = G.degree(v)
                    n_common_neighbors = len(list(nx.common_neighbors(G, u, v)))

                    indirect_weight = (
                        (2 * n_common_neighbors) 
                        / (n_u_neighbors + n_v_neighbors - 2 * direct_weight + 1e-7)
                    )

                    weight = (
                        alpha*direct_weight 
                        + (1-alpha) * indirect_weight 
                        - beta * interact_weight)

                    if weight > 0:
                        G_flex.add_edge(u, v, 
                            direct_weight=direct_weight, 
                            indirect_weight=indirect_weight, 
                            interact_weight=interact_weight,
                            weight = weight
                        )
            
            G = G_flex

        return G
    
