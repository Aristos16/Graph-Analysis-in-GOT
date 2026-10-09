import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

Images_DIR = "ReportPics"

#upload my CSV files and making graph
nodes = pd.read_csv("data/got-all-seasons-nodes.csv")
edges = pd.read_csv("data/got-all-seasons-edges.csv")

G = nx.Graph()

strengths = []

for _, row in nodes.iterrows():

    G.add_node(row["Id"], label=row["Label"])

for _, row in edges.iterrows():

    G.add_edge(row["Source"], row["Target"], weight=row["Weight"])


#Basic stuff for report
NodesNumber = G.number_of_nodes()
EdgesNumber = G.number_of_edges()


density = nx.density(G)
components = nx.number_connected_components(G)



print("Nodes Number:", NodesNumber)
print("Edges Numbers:", EdgesNumber)
print("Density:", density)
print("Connected components:", components)

#Degree Distribution

degrees = [d for _, d in G.degree()]

#I make the graph and save it 
plt.figure(figsize=(8, 5))
plt.hist(degrees, bins=30)
plt.title("Degree Distribution")
plt.xlabel("Degree")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("ReportPics/degree_distribution.png", dpi=300)


#Strenght of all carachters 
for node in G.nodes():

    w = 0
    for _, _, data in G.edges(node, data=True):
        w += data["weight"]
    strengths.append(w)

plt.figure(figsize=(8, 5))
plt.hist(strengths, bins=30)
plt.title("Strength Distribution")
plt.xlabel("Weighted Degree (Strength)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("ReportPics/strength_distribution.png", dpi=300)
#plt.show()

#Find Characters with top 10 deggre

degree_dictionary = dict(G.degree())

CharactersWithMostDegree = sorted(degree_dictionary.items(), key=lambda x: x[1], reverse=True)[:10]

print("\n")
print("Characters with most degree:")
i=0
for char, deg in CharactersWithMostDegree:
    i=i+1
    print(i, G.nodes[char]["label"], deg)

# Bar chart for top 10 degree
names_deg = [G.nodes[n]["label"] for n, _ in CharactersWithMostDegree]
vals_deg = [d for _, d in CharactersWithMostDegree]

plt.figure(figsize=(10, 5))
plt.bar(names_deg, vals_deg)
plt.xticks(rotation=45, ha="right")
plt.title("Top 10 Characters by Degree")
plt.tight_layout()
plt.savefig("ReportPics/CharactersWithMostDegree.png", dpi=300)
#plt.show()

#Strength
strength_dictionary = {}
for node in G.nodes():

    total = sum(data["weight"] for _, _, data in G.edges(node, data=True))
    strength_dictionary[node] = total

top10_strength = sorted(strength_dictionary.items(), key=lambda x: x[1], reverse=True)[:10]

print("\n")
print("\nCharacters with most strenght: ")
i=0
for char, val in top10_strength:
    i=i+1
    print(i, G.nodes[char]["label"], val)

# Bar chart for top 10 strength
names_str = [G.nodes[n]["label"] for n, _ in top10_strength]
vals_str = [s for _, s in top10_strength]

plt.figure(figsize=(10, 5))
plt.bar(names_str, vals_str)
plt.xticks(rotation=45, ha="right")
plt.title("Top 10 Characters by Strength")
plt.tight_layout()
plt.savefig("ReportPics/CharactersWithMostStrength.png", dpi=300)
#plt.show()

#Making the Graph with the 40 characters with most connections

top_nodes = [node for node, _ in CharactersWithMostDegree]  
top_nodes = [node for node, _ in sorted(degree_dictionary.items(), key=lambda x: x[1], reverse=True)[:40]]

H = G.subgraph(top_nodes)

plt.figure(figsize=(14, 14))
pos = nx.spring_layout(H, seed=42)

nx.draw_networkx_nodes(H, pos, node_size=400, node_color="skyblue", alpha=0.9)
nx.draw_networkx_edges(H, pos, width=0.5, edge_color="gray")


labels = {node: G.nodes[node]["label"] for node in H.nodes()}
nx.draw_networkx_labels(H, pos, labels, font_size=8)

plt.title("Top 40 Characters Graph!")
plt.tight_layout()
plt.savefig("ReportPics/GraphWithTop40.png", dpi=300)




#Betweenness Centrality

for u, v, data in G.edges(data=True):
    data["distance"] = 1 / data["weight"]




print("\nBetweeness")

#NetworkX
betweenness = nx.betweenness_centrality(G, weight="distance", normalized=True)

top10_bet = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10] #reverse για να πάρω το μεγαλύτερο

print("\nTop 10 Characters by Betweenness:")

for i, (char, val) in enumerate(top10_bet, start=1):
    print(i, G.nodes[char]["label"], round(val, 6))

names_bet = [G.nodes[n]["label"] for n, _ in top10_bet]
vals_bet = [v for _, v in top10_bet]

plt.figure(figsize=(10, 5))
plt.bar(names_bet, vals_bet)
plt.xticks(rotation=45, ha="right")
plt.title("Top 10 Characters by Betweenness")
plt.tight_layout()
plt.savefig(os.path.join(Images_DIR, "Top10_betweenness_weighted.png"), dpi=300)

#PageRank


print("\nPageRank")

#NetworkX
pagerank = nx.pagerank(G, weight="weight")

top10_pr = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]

print("\nTop 10 Characters by PageRank:")

for i, (char, val) in enumerate(top10_pr, start=1):
    print(i, G.nodes[char]["label"], round(val, 6))

names_pr = [G.nodes[n]["label"] for n, _ in top10_pr]
vals_pr = [v for _, v in top10_pr]

plt.figure(figsize=(10, 5))
plt.bar(names_pr, vals_pr)
plt.xticks(rotation=45, ha="right")
plt.title("Top 10 Characters by PageRank")
plt.tight_layout()
plt.savefig(os.path.join(Images_DIR, "Top10_pagerank_weighted.png"), dpi=300)

#Save Tables
def save_top_table(filename, pairs, value_name):
    df = pd.DataFrame([
        {"rank": i+1, "Id": node, "Label": G.nodes[node]["label"], value_name: val}
        for i, (node, val) in enumerate(pairs)
    ])
    df.to_csv(os.path.join(Images_DIR, filename), index=False)

save_top_table("Top10_betweenness_weighted.csv", top10_bet, "betweenness")
save_top_table("Top10_pagerank_weighted.csv", top10_pr, "pagerank")


#plt.show()

#Compare tbls for report


degree_dict = dict(G.degree())
strength_dict = {n: sum(d["weight"] for _,_,d in G.edges(n, data=True)) for n in G.nodes()}
bet_dict = betweenness
pr_dict = pagerank

# παίρνουμε ένωση των top-10 από betweenness και pagerank
top_nodes = set([n for n,_ in top10_bet] + [n for n,_ in top10_pr])

rows = []
for n in top_nodes:
    rows.append({
        "Id": n,
        "Label": G.nodes[n]["label"],
        "Degree": degree_dict.get(n, 0),
        "Strength": strength_dict.get(n, 0),
        "Betweenness": bet_dict.get(n, 0),
        "PageRank": pr_dict.get(n, 0),
    })

df_compare = pd.DataFrame(rows)
df_compare = df_compare.sort_values(by="PageRank", ascending=False)

df_compare.to_csv(os.path.join(Images_DIR, "CompareMetrics_TopNodes.csv"), index=False)
print("\nSaved comparison table:", os.path.join(Images_DIR, "CompareMetrics_TopNodes.csv"))



#Louvain
print("\nComputing communities with Louvain...")
try:
    import community as community_louvain
except ImportError:
    raise SystemExit("Check louvain 248!!")

# partition: dict node -> community_id
partition = community_louvain.best_partition(G, weight="weight", random_state=42)

# Basic stats
num_comms = len(set(partition.values()))
print("Number of communities:", num_comms)

# Community sizes
comm_sizes = {}
for node, cid in partition.items():
    comm_sizes[cid] = comm_sizes.get(cid, 0) + 1

top_comms = sorted(comm_sizes.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 communities by size:")
for rank, (cid, size) in enumerate(top_comms, start=1):
    print(rank, "community", cid, "size", size)

# Leaders per community (by PageRank)
leaders = []
for cid, _ in top_comms:
    members = [n for n in G.nodes() if partition[n] == cid]
    members_sorted = sorted(members, key=lambda n: pagerank[n], reverse=True)[:3]
    for r, n in enumerate(members_sorted, start=1):
        leaders.append({
            "community": cid,
            "rank_in_community": r,
            "Id": n,
            "Label": G.nodes[n]["label"],
            "PageRank": pagerank[n],
            "Strength": sum(d["weight"] for _,_,d in G.edges(n, data=True))
        })

df_leaders = pd.DataFrame(leaders)
df_leaders.to_csv(os.path.join(Images_DIR, "CommunityLeaders_Top10Communities.csv"), index=False)
print("\nSaved:", os.path.join(Images_DIR, "CommunityLeaders_Top10Communities.csv"))

#Plot: Top-40 graph colored by community
top_nodes_40 = [node for node, _ in sorted(degree_dictionary.items(), key=lambda x: x[1], reverse=True)[:40]]
Hc = G.subgraph(top_nodes_40)

plt.figure(figsize=(14, 14))
pos = nx.spring_layout(Hc, seed=42)

# map each node -> community id (for coloring)
node_colors = [partition[n] for n in Hc.nodes()]

nx.draw_networkx_nodes(Hc, pos, node_size=420, node_color=node_colors, alpha=0.9)
nx.draw_networkx_edges(Hc, pos, width=0.6, alpha=0.5)

labels = {node: G.nodes[node]["label"] for node in Hc.nodes()}
nx.draw_networkx_labels(Hc, pos, labels, font_size=8)

plt.title("Top 40 Characters Colored by Louvain Communities")
plt.tight_layout()
plt.savefig(os.path.join(Images_DIR, "Graph_Top40_communities_louvain.png"), dpi=300)