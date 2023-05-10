import os 
import argparse
import networkx as nx

from collaboration_network.graph import CollaborationGraph


def create_graph(args):
    G = CollaborationGraph.from_config(args.config_path)
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