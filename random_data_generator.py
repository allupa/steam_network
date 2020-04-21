'''
This creates a random Erdös-Rényi network and a random Barabasi-Albert network, that have the same number of nodes and about the same number of edges as the crawled data.
'''

import numpy as np
import networkx as nx

N = 5989
p = 0

#Creating random ER data
def random_ER_network(N, p=None, avg_k=None):
    if p is None and avg_k is None:
        raise Exception('Neither p nor avg_k defined.')
    if p is None:
        p = float(avg_k)/(N-1)
    nodes = range(N)
    G = nx.Graph()
    G.add_nodes_from(nodes)
    for i in range(N):
        for j in range(i+1, N):
            if np.random.rand() < p:
                G.add_edge(i, j)
    
    return G

#Creating random BA data
def random_BA_network(N, m_0, m):
    G = nx.complete_graph(m_0)
    for i in range(m_0, N):
        pk = np.array([degree for node, degree in G.degree()], dtype=float)
        pk /= pk.sum()

        targets = np.random.choice(range(i), size=m, replace=False, p=pk)
        for target in targets:
            G.add_edge(i, target)
    return G


G = random_ER_network(N, avg_k=2.212)
nx.write_gexf(G, 'random_ER.gexf')

'''
Arvot tähän alempaan heitetty päästä, tuli ainakin oikean kokoluokan nro of edges m = 1 arvolla
'''
G = random_BA_network(N, m_0=10, m=1)
nx.write_gexf(G, 'random_BA.gexf')