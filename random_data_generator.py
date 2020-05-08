'''
This creates a random Erdös-Rényi network, a random Barabasi-Albert network, and possibly a random gaussian random partition network 
that have the same number of nodes and about the same number of edges as the crawled data.

Generated networks are infected (number of initially infected is 2) and infected networks are saved.
'''

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd

#Crawled data
G_crawled = nx.read_gexf('steam_graph_communities.gexf')
G_crawled.graph['pos'] = nx.spring_layout(G_crawled)

N = 7070
p = 0
avg_k = 54.043

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
    G.graph['pos'] = nx.spring_layout(G)
    return G


#Creating random network - ER
G_ER = random_ER_network(N, avg_k)
nx.write_gexf(G_ER, 'random_ER.gexf')

'''
Arvot tähän alempaan heitetty päästä, tuli ainakin oikean kokoluokan nro of edges (191 040) ja avg degree (54,042) m_0 = 60 ja m = 27 arvoilla
m_0 on ensimmäisen noden yhteydet ja m on jälkimmäisten nodejen yhteydet, yksinkertaistettuna
'''
#Creating random network - BA
G_BA = random_BA_network(N, m_0=60, m=27)
nx.write_gexf(G_BA, 'random_BA.gexf')

'''
Paljon tunkkausta, näillä ihan hyvä. Arvot: N nodet, klusterin keskiarvokoko, klustereiden määrä, klustereiden sisäisten linkkien todnäk,
klustereiden välisten linkkien todnäk, hieman yksinkertaistettuna
'''
#Creating random network - gaussian random partition
#G_gaussian = nx.generators.community.gaussian_random_partition_graph(1000, 75, 8, 0.015, 0.0005)
#G_gaussian.graph['pos'] = nx.spring_layout(G_gaussian)
#nx.write_gexf(G_gaussian, 'random_gauss.gexf')
#KORJAA 75 PAREMPAAN ARVOON JA KORVAA 1000 -> N
#ALUPERÄISET ARVOT N, 750, 8, 0.0015, 0.000005

'''
SIS/SIR -mallinnusta ja simulointia.
'''
#Ensimmäiset infektoidut
def infect_node(G, n=1):
    G.graph['t'] = 0
    nx.set_node_attributes(G, False, 'Infected')
    nx.set_node_attributes(G, np.nan, 'Infection time')
    infect_list = np.random.choice(G.nodes, replace=False, size=n)
    for i_0 in infect_list:
        G.nodes[i_0]['Infected'] = True
        G.nodes[i_0]['Infection time'] = G.graph['t']
    return G

#Tällä saat kirjoitettua halutuista tiedostoista gexf muotoisen, jolloin ne soveltuvat gephiin ja siellä näkee tartunnat. Poista kommentti functiosta infect_node
G_ER_inf = infect_node(G_ER, n=2)
G_BA_inf = infect_node(G_BA, n=2)
#G_gaussian_inf = infect_node(G_gaussian, n=2)
G_crawled_inf = infect_node(G_crawled, n=2)

nx.write_gexf(G_ER_inf, 'random_ER_inf.gexf')
nx.write_gexf(G_BA_inf, 'random_BA_inf.gexf')
#nx.write_gexf(G_gaussian_inf, 'random_gaussian_inf.gexf')
nx.write_gexf(G_crawled_inf, 'crawled_inf.gexf')
