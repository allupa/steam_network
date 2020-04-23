# steam_network
Project work for mapping out complex networks

# How it works
1. Using the crawler.py, the program collects a list of nodes using a random review from steam community as a starting point
2. The results.csv (or results.json) can be used in API.py to iterate over all nodes and collect edges
3. network.py writes the nodelist into a Gephi file - steam_graph.gexf
