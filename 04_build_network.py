import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------
# STEP 1 — Load Data
# ---------------------------------------------------
print("📥 Loading extracted CSV...")
df = pd.read_csv("outputs/extracted.csv")
print(f"Loaded {len(df)} rows")

df["keyword_norm"] = (
    df["keyword"]
    .astype(str)
    .str.lower()
    .str.replace(r"[^a-z0-9\s\-]", "", regex=True)
    .str.strip()
)

# ---------------------------------------------------
# STEP 2 — Build Graph
# ---------------------------------------------------
G = nx.Graph()

for _, row in df.iterrows():
    sp = row.get("speaker")
    kw = row.get("keyword_norm")

    if not isinstance(sp, str) or not isinstance(kw, str):
        continue

    sp_node = f"speaker::{sp}"
    kw_node = f"keyword::{kw}"

    G.add_node(sp_node, type="speaker")
    G.add_node(kw_node, type="keyword")

    # Edge combine (increase weight)
    if G.has_edge(sp_node, kw_node):
        G[sp_node][kw_node]["weight"] += 1
    else:
        G.add_edge(sp_node, kw_node, weight=1)

print(f"Graph created ✔ Nodes: {len(G.nodes())}, Edges: {len(G.edges())}")


# ---------------------------------------------------
# STEP 3 — Select subgraph (TOP 10 influential nodes)
# ---------------------------------------------------
degree_dict = dict(G.degree())
top_nodes = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)[:10]
top_node_names = [n for n, d in top_nodes]

# include neighbors of top nodes
sub_nodes = set(top_node_names)
for n in top_node_names:
    sub_nodes.update(G.neighbors(n))

H = G.subgraph(sub_nodes).copy()
print(f"Subgraph size ✔ Nodes: {len(H.nodes())}, Edges: {len(H.edges())}")


# ---------------------------------------------------
# STEP 4 — Visualization with colors + labels for top 10 only
# ---------------------------------------------------
pos = nx.spring_layout(H, seed=42)

node_colors = []
labels = {}

for n in H.nodes():
    node_type = H.nodes[n].get("type")
    if node_type == "speaker":
        node_colors.append("#1f77b4")  # blue
    else:
        node_colors.append("#ff7f0e")  # orange

    # label only top 10 nodes for readability
    labels[n] = n.split("::")[1] if n in top_node_names else ""


plt.figure(figsize=(14, 14))

nx.draw_networkx_nodes(
    H, pos,
    node_size=380,
    node_color=node_colors,
    alpha=0.9
)

nx.draw_networkx_edges(H, pos, width=0.8, alpha=0.5)

nx.draw_networkx_labels(
    H, pos,
    labels,
    font_size=8,
    font_color="black"
)

plt.title("Speaker–Keyword Network (Top Influential Nodes)", fontsize=14)
plt.axis("off")

Path("outputs").mkdir(exist_ok=True)
plt.savefig("outputs/network_clean.png", dpi=300, bbox_inches="tight")
print("📡 Clean network saved → outputs/network_clean.png")




