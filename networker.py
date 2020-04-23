import networkx as nx
import json
import util

'''
:param G: networkx graph
'''
def add_review_scores(G):
    config = util.load_config()
    with open(config['review_scores']['file'], 'r') as f:
        scores = json.load(f)
    for k, v in scores.items():
        G.nodes[k]['score'] = v
    print(G.nodes[:5])


def main():
    G = nx.read_edgelist('network.csv')
    add_review_scores(G)
    nx.write_gexf(G, 'steam_graph.gexf')
    return 0

main()
