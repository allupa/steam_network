import networkx as nx
import json
import demon as d

# Read edgelist from csv
G = nx.read_edgelist(
    'C:\\Users\\asa.SOFIA\\Documents\\steam_network\\network.csv')

# Remove nodes with degree < 3 and score < 1
G.remove_nodes_from([n for n, degree in dict(G.degree()).items() if degree < 3])
with open('C:\\Users\\asa.SOFIA\\Documents\\steam_network\\review_scores.json') as f:
    scores = json.load(f)
for k, v in scores.items():
    if k in G.nodes:
        G.nodes[k][1] = v
removable_nodes = []
for n, v in G.nodes(data=True):
    if v:
        if v[1] < 1:
            removable_nodes.append(n)
    else:
        removable_nodes.append(n)
G.remove_nodes_from(removable_nodes)

dm = d.Demon(graph=G, epsilon=0.25, min_community_size=50, file_output="communities.txt")
coms = dm.execute()
