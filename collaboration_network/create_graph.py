import os
import argparse
import glob
import yaml
import networkx as nx

from collaboration_network.graph_new import CollaborationGraph


def create_graph(args):
    with open(args.config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)
        graph_args = argparse.Namespace(**config)

    G = CollaborationGraph.from_config(graph_args)
    graph_name = os.path.splitext(os.path.basename(args.config_path))[0]

    savepath = os.path.join('graphs', graph_name+'.gml')

    os.makedirs('graphs', exist_ok=True)

    nx.write_gml(G, savepath)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_path',
        help='Path to config to create graph'
    )
    parser.add_argument(
        '--graph_name',
        '-gn',
        help='Graph name, default to config name'
    )
    args = parser.parse_args()

    create_graph(args)

if __name__ == "__main__":
    main()