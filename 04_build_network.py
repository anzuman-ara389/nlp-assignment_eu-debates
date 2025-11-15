# 04_build_network.py

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

print("✅ Loading structured data...")
df = pd.read_csv("outputs/extracted.csv")
print("✅ Loaded", len(df), "rows")

# ------------------------------------------------------
# STEP 1 — Build Bipartite Graph (Speaker ↔ Keyword)
# ------------------------------------------------------

G = nx.Graph()

for _, r in df.iterrows():
    speaker_node = f"speaker::{r['speaker']}"
    keyword_node = f"keyword::{r['keyword']}"

    G.add_node(speaker_node, type="speaker")
    G.add_node(keyword_node, type="keyword")

    G.add_edge(speaker_node, keyword_node)

print(f"🌐 Graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

# ------------------------------------------------------
# STEP 2 — Get top connected nodes
# ------------------------------------------------------

degree_sorted = sorted(G.degree(), key=lambda x: x[1], reverse=True)
top_nodes = degree_sorted[:15]   # Top 15 important nodes

print("\n🏆 Top 15 most connected nodes:")
for n, d in top_nodes:
    print(f"{n}: {d}")

# Create subgraph containing only top nodes + neighbors
important_nodes = set([n for n, _ in top_nodes])

for n, _ in top_nodes:
    important_nodes.update(G.neighbors(n))

H = G.subgraph(important_nodes).copy()

print(f"\n📌 Subgraph created → {H.number_of_nodes()} nodes, {H.number_of_edges()} edges")

# ------------------------------------------------------
# STEP 3 — Visualization
# ------------------------------------------------------

print("\n🎨 Drawing network graph...")

plt.figure(figsize=(14, 12))
pos = nx.spring_layout(H, seed=42)

node_colors = ["#1f77b4" if H.nodes[n]["type"] == "speaker" else "#ff7f0e" for n in H.nodes()]
node_sizes = [80 if H.nodes[n]["type"] == "speaker" else 140 for n in H.nodes()]

nx.draw(
    H,
    pos,
    with_labels=False,
    node_color=node_colors,
    node_size=node_sizes,
    edge_color="lightgray",
    width=0.8,
    alpha=0.9
)

# Label only top nodes
for n, _ in top_nodes:
    if n in H.nodes():
        x, y = pos[n]
        plt.text(
            x, y,
            n.replace("speaker::", "").replace("keyword::", ""),
            fontsize=10, fontweight="bold"
        )

plt.title("Bipartite Network Mapping Speaker–Topic Relations in EU Debates", fontsize=16)

legend_elements = [
    Patch(facecolor="#1f77b4", label="Speakers"),
    Patch(facecolor="#ff7f0e", label="Keywords")
]
plt.legend(handles=legend_elements, loc="upper left", fontsize=12)

plt.tight_layout()
plt.savefig("outputs/network_clean.png", dpi=300)
plt.show()

print("✅ Saved → outputs/network_clean.png")








