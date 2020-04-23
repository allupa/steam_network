import networkx as nx
import json
import util

'''
:param G: networkx graph
'''
def add_review_scores(G):
    print("Adding scores, this might take a while...")
    config = util.load_config()
    with open(config['review_scores']['file'], 'r') as f:
        scores = json.load(f)
    for k, v in scores.items():
        G.nodes[k][1] = v
    return G

def main():
    print("Reading csv...")
    G = nx.read_edgelist('network.csv')
    G_scored = add_review_scores(G)
    nx.write_gexf(G_scored, 'steam_graph.gexf')
    return 0

main()
