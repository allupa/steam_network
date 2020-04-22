'''
This creates a random Erdös-Rényi network, a random Barabasi-Albert network, and a random gaussian random partition network 
that have the same number of nodes and about the same number of edges as the crawled data.

Also, it simulates spreading in generated networks
'''

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#Crawled data
G_crawled = nx.read_edgelist('network.csv')
G_crawled.graph['pos'] = nx.spring_layout(G_crawled)

N = 5989
p = 0
avg_k = 2.212

#Creating random ER data
def random_ER_network(N, avg_k):
    p = avg_k / (N-1)
    G = nx.fast_gnp_random_graph(N, p)
    G.graph['pos'] = nx.spring_layout(G)
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


G_ER = random_ER_network(N, avg_k)
nx.write_gexf(G_ER, 'random_ER.gexf')

'''
Arvot tähän alempaan heitetty päästä, tuli ainakin oikean kokoluokan nro of edges m = 1 arvolla
m_0 on ensimmäisen noden yhteydet ja m on jälkimmäisten nodejen yhteydet, yksinkertaistettuna
'''
G_BA = random_BA_network(N, m_0=10, m=1)
nx.write_gexf(G_BA, 'random_BA.gexf')

'''
Paljon tunkkausta, näillä ihan hyvä. Arvot: N nodet, klusterin keskiarvokoko, klustereiden määrä, klustereiden sisäisten linkkien todnäk,
klustereiden välisten linkkien todnäk, hieman yksinkertaistettuna
'''
G_gaussian = nx.generators.community.gaussian_random_partition_graph(N, 750, 8, 0.0015, 0.000005)
nx.write_gexf(G_gaussian, 'random_gauss.gexf')

'''
SIS/SIR -mallinnusta ja simulointia.
'''

def infect_node(G, n=1):
    G.graph['t'] = 0
    nx.set_node_attributes(G, False, 'Infected')
    nx.set_node_attributes(G, np.nan, 'Infection time')
    infect_list = np.random.choice(G.nodes, replace=False, size=n)
    for i_0 in infect_list:
        G.nodes[i_0]['Infected'] = True
        G.nodes[i_0]['Infection time'] = G.graph['t']

def plot(G, title=None):
    color = ['r' if G.nodes[node]['Infected'] else 'g' for node in G.nodes()]
    nx.draw(G, pos=G.graph['pos'], node_size=10, node_color=color)
    if title: plt.title(title)
    plt.show()


'''
infect_node(G_crawled, 2)
infect_node(G_gaussian, 2)
plot(G_crawled, G_gaussian)
'''