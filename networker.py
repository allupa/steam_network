import networkx as nx

def main():
    G = nx.read_edgelist('network.csv')
    nx.write_gexf(G, 'steam_graph.gexf')
    return 0

main()
