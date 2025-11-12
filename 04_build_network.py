# 04_build_network.py
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

print("✅ Loading structured data...")
ex = pd.read_csv("outputs/extracted.csv")
print("✅ Loaded", len(ex), "rows")

# Step 1: Clean text for consistency
ex["keyword_norm"] = (
    ex["keyword"]
    .astype(str)
    .str.lower()
    .str.replace(r"[^a-z0-9\s\-]", "", regex=True)
    .str.strip()
)

# Step 2: Create an empty graph
G = nx.Graph()

# Step 3: Add edges (speaker ↔ keyword)
for _, row in ex.iterrows():
    speaker = row.get("speaker")
    keyword = row.get("keyword_norm")
    if not isinstance(speaker, str) or not isinstance(keyword, str):
        continue
    speaker_node = f"speaker::{speaker}"
    keyword_node = f"keyword::{keyword}"
    G.add_node(speaker_node, type="speaker")
    G.add_node(keyword_node, type="keyword")

    # Add edge or update weight
    if G.has_edge(speaker_node, keyword_node):
        G[speaker_node][keyword_node]["weight"] += 1
    else:
        G.add_edge(speaker_node, keyword_node, weight=1)

print(f"✅ Network created with {len(G.nodes())} nodes and {len(G.edges())} edges")

# Step 4: Analyze degree centrality
degree_dict = dict(G.degree())
top_nodes = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)[:10]
print("\n🏆 Top 10 most connected nodes:")
for name, deg in top_nodes:
    print(f"{name}: {deg}")

# Step 5: Visualization
Path("outputs").mkdir(exist_ok=True)
plt.figure(figsize=(10, 10))

# To make the graph readable, limit to smaller subgraph
if len(G.nodes()) > 300:
    top_keywords = [n for n, d in top_nodes if n.startswith("keyword::")]
    sub_nodes = set(top_keywords)
    for n in top_keywords:
        sub_nodes.update(G.neighbors(n))
    H = G.subgraph(sub_nodes).copy()
else:
    H = G.copy()

# Assign colors: 🔵 speakers, 🟠 keywords
colors = [
    "skyblue" if H.nodes[n]["type"] == "speaker" else "orange"
    for n in H.nodes()
]

# Draw the network (without labels)
pos = nx.spring_layout(H, seed=42)
nx.draw(
    H,
    pos,
    with_labels=False,
    node_color=colors,
    node_size=60,
    width=0.3,
    alpha=0.8
)

# Add a simple legend
plt.text(0.95, 0.05, "🔵 Speaker\n🟠 Keyword", transform=plt.gca().transAxes,
         fontsize=10, verticalalignment='bottom', horizontalalignment='right')

plt.title("Speaker–Keyword Network (Colored by Type)")
plt.tight_layout()
plt.savefig("outputs/network.png", dpi=300)
plt.close()

print("✅ Saved visualization → outputs/network.png")
print("\n🎯 Network analysis complete!")



