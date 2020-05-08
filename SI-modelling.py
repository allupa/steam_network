'''
This simulates a spreading phenomenon in networks and plots figures of spreading related to time.
Infection has a chance of 5% to spread to a neigbouring node.
'''
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd

#Crawled data
G_crawled_inf = nx.read_gexf('crawled_inf.gexf')
G_crawled_inf.graph['pos'] = nx.spring_layout(G_crawled_inf)

print('crawled done')

#ER data
G_ER_inf = nx.read_gexf('random_ER_inf.gexf')
G_ER_inf.graph['pos'] = nx.spring_layout(G_ER_inf)

print('ER done')

#BA data
G_BA_inf = nx.read_gexf('random_BA_inf.gexf')
G_BA_inf.graph['pos'] = nx.spring_layout(G_BA_inf)

print('BA done, thus all read.')


def plot(G, title):
    color = ['r' if G.nodes[node]['Infected'] else 'g' for node in G.nodes()]
    nx.draw(G, pos=G.graph['pos'], node_size=5, node_color=color)
    #Jos ei toimi, niin poista nämä kommentit ja tuo pelkkä plt.title(title)
    #if title: plt.title(title)
    plt.title(title)
    
    plt.show()



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

print('moving to spreading...')

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
for b in range(5):
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
for b in range(5):
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
Crawled network spreading
'''

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
for b in range(5):
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
