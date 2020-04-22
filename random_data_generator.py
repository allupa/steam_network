'''
This creates a random Erdös-Rényi network, a random Barabasi-Albert network, and a random gaussian random partition network 
that have the same number of nodes and about the same number of edges as the crawled data.

Also, it simulates spreading in generated networks
'''

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd

#Crawled data
#G_crawled = nx.read_edgelist('network.csv')
#G_crawled.graph['pos'] = nx.spring_layout(G_crawled)

#N = 5989
N = 500
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
    G.graph['pos'] = nx.spring_layout(G)
    return G


#Creating random network - ER
G_ER = random_ER_network(N, avg_k)
#nx.write_gexf(G_ER, 'random_ER.gexf')

'''
Arvot tähän alempaan heitetty päästä, tuli ainakin oikean kokoluokan nro of edges m = 1 arvolla
m_0 on ensimmäisen noden yhteydet ja m on jälkimmäisten nodejen yhteydet, yksinkertaistettuna
'''
#Creating random network - BA
G_BA = random_BA_network(N, m_0=10, m=1)
#nx.write_gexf(G_BA, 'random_BA.gexf')

'''
Paljon tunkkausta, näillä ihan hyvä. Arvot: N nodet, klusterin keskiarvokoko, klustereiden määrä, klustereiden sisäisten linkkien todnäk,
klustereiden välisten linkkien todnäk, hieman yksinkertaistettuna
'''
#Creating random network - gaussian random partition
G_gaussian = nx.generators.community.gaussian_random_partition_graph(1000, 75, 8, 0.015, 0.0005)
G_gaussian.graph['pos'] = nx.spring_layout(G_gaussian)
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

def plot(G, title=None):
    color = ['r' if G.nodes[node]['Infected'] else 'g' for node in G.nodes()]
    nx.draw(G, pos=G.graph['pos'], node_size=10, node_color=color)
    if title: plt.title(title)
    plt.show()


#Tällä saat kirjoitettua halutuista tiedostoista gexf muotoisen, jolloin ne soveltuvat gephiin ja siellä näkee tartunnat. Poista kommentti functiosta infect_node
G_ER_inf = infect_node(G_ER, n=2)
G_BA_inf = infect_node(G_BA, n=2)
G_gaussian_inf = infect_node(G_gaussian, n=2)
#G_crawled_inf = infect_node(G_crawled, n=2)
'''
nx.write_gexf(G_ER_inf, 'random_ER_inf.gexf')
nx.write_gexf(G_BA_inf, 'random_BA_inf.gexf')
nx.write_gexf(G_gaussian_inf, 'random_gaussian_inf.gexf')
nx.write_gexf(G_crawled_inf, 'crawled_inf.gexf')
'''

#Infektion loppuvaiheen mallinnus
def spread(G, p):
    nx.set_node_attributes(G,
                            {node: True if t == 0 else False
                            for node, t in nx.get_node_attributes(G, 'Infection_time').items()},
                            'Infected')
    G.graph['t'] = 0
    while True:
        propagate = False
        G.graph['t'] += 1
        infected = [node for node in G.nodes() if G.nodes[node]['Infected']]
        for node in infected:
            susceptible_neighbors = [sn for sn in G.neighbors(node) if not G.nodes[sn]['Infected']]
            propagate += len(susceptible_neighbors) > 0
            for sn in susceptible_neighbors:
                if np.random.random_sample() < p:
                    G.nodes[sn]['Infected'] = True
                    G.nodes[sn]['Infection_time'] = G.graph['t']
        if not propagate:
            break
    infection_times = nx.get_node_attributes(G, 'Infection_time')
    it_counter = Counter(infection_times.values())
    return it_counter


'''
ER-network spreading
'''
it_counter = spread(G_ER_inf, p=0.05)
plot(G_ER_inf, title='ER-network Infection')

#Yhden datasetin kuvaajan piirtoa
it = pd.Series(it_counter)
it.sort_index().cumsum().plot(logy=False, marker='.')
plt.xlabel(r'$t$', fontsize=16)
plt.ylabel(r'$I(t)$', fontsize=16)
plt.title('ER-network, t={}'.format(G_ER_inf.graph['t']))
plt.show()

#Monen datasetin keskiarvoa
counter = Counter()
for b in range(20):
    counter += spread(G_ER_inf, p=0.05)
total = sum(counter.values())
for key in counter:
    counter[key] /= float(total)
it = pd.Series(counter)
it.sort_index().cumsum().plot(logy=False, marker='.')
plt.title('ER Infection Peak')
plt.xlabel(r'$t$', fontsize=16)
plt.ylabel(r'$I(t)$', fontsize=16)

plt.show()

'''
BA-network spreading
'''
it_counter = spread(G_BA_inf, p=0.05)
plot(G_BA_inf, title='BA-network Infection')

#Yhden datasetin kuvaajan piirtoa
it = pd.Series(it_counter)
it.sort_index().cumsum().plot(logy=False, marker='.')
plt.xlabel(r'$t$', fontsize=16)
plt.ylabel(r'$I(t)$', fontsize=16)
plt.title('BA-network, t={}'.format(G_BA_inf.graph['t']))
plt.show()

#Monen datasetin keskiarvoa
counter = Counter()
for b in range(20):
    counter += spread(G_BA_inf, p=0.05)
total = sum(counter.values())
for key in counter:
    counter[key] /= float(total)
it = pd.Series(counter)
it.sort_index().cumsum().plot(logy=False, marker='.')
plt.title('BA Infection Peak')
plt.xlabel(r'$t$', fontsize=16)
plt.ylabel(r'$I(t)$', fontsize=16)

plt.show()


'''
Gaussian network spreading
'''
it_counter = spread(G_gaussian_inf, p=0.05)
plot(G_gaussian_inf, title='Gaussian-network Infection')

#Yhden datasetin kuvaajan piirtoa
it = pd.Series(it_counter)
it.sort_index().cumsum().plot(logy=False, marker='.')
plt.xlabel(r'$t$', fontsize=16)
plt.ylabel(r'$I(t)$', fontsize=16)
plt.title('Gaussian-network, t={}'.format(G_gaussian_inf.graph['t']))
plt.show()

#Monen datasetin keskiarvoa
counter = Counter()
for b in range(20):
    counter += spread(G_gaussian_inf, p=0.05)
total = sum(counter.values())
for key in counter:
    counter[key] /= float(total)
it = pd.Series(counter)
it.sort_index().cumsum().plot(logy=False, marker='.')
plt.title('Gaussian Infection Peak')
plt.xlabel(r'$t$', fontsize=16)
plt.ylabel(r'$I(t)$', fontsize=16)

plt.show()


'''
Crawled network spreading


it_counter = spread(G_crawled_inf, p=0.05)
plot(G_crawled_inf, title='Crawled network Infection')


#Yhden datasetin kuvaajan piirtoa
it = pd.Series(it_counter)
it.sort_index().cumsum().plot(logy=False, marker='.')
plt.xlabel(r'$t$', fontsize=16)
plt.ylabel(r'$I(t)$', fontsize=16)
plt.title('Crawled network, t={}'.format(G_crawled_inf.graph['t']))
plt.show()

#Monen datasetin keskiarvoa
counter = Counter()
for b in range(20):
    counter += spread(G_crawled_inf, p=0.05)
total = sum(counter.values())
for key in counter:
    counter[key] /= float(total)
it = pd.Series(counter)
it.sort_index().cumsum().plot(logy=False, marker='.')
plt.title('Crawled Infection Peak')
plt.xlabel(r'$t$', fontsize=16)
plt.ylabel(r'$I(t)$', fontsize=16)

plt.show()
'''
