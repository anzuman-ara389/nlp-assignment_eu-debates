# 07_community_detection.py
import pandas as pd
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities

ex = pd.read_csv("outputs/extracted.csv")
ex["keyword_norm"] = (
    ex["keyword"].astype(str).str.lower()
      .str.replace(r"[^a-z0-9\s\-]", "", regex=True).str.strip()
)

G = nx.Graph()
for _, r in ex.iterrows():
    s = r.get("speaker"); k = r.get("keyword_norm")
    if not isinstance(s, str) or not isinstance(k, str): continue
    u, v = f"speaker::{s}", f"keyword::{k}"
    G.add_node(u, type="speaker"); G.add_node(v, type="keyword")
    if G.has_edge(u, v): G[u][v]["weight"] += 1
    else: G.add_edge(u, v, weight=1)

# focus on top 300 nodes by degree (readability/speed)
deg = dict(G.degree())
keep = set([n for n, d in sorted(deg.items(), key=lambda x: x[1], reverse=True)[:300]])
H = G.subgraph(keep).copy()

comms = list(greedy_modularity_communities(H))
print(f"✅ Found {len(comms)} communities")
for i, c in enumerate(comms[:5], 1):
    labels = [n.replace("speaker::","").replace("keyword::","") for n in list(c)[:5]]
    print(f"Community {i}: {', '.join(labels)}")
