# 06_export_triples.py
import pandas as pd
import networkx as nx
from pathlib import Path

# Load the structured extraction
ex = pd.read_csv("outputs/extracted.csv")
ex["keyword_norm"] = (
    ex["keyword"].astype(str).str.lower()
      .str.replace(r"[^a-z0-9\s\-]", "", regex=True).str.strip()
)

# Build graph (same as step 4)
G = nx.Graph()
for _, r in ex.iterrows():
    s = r.get("speaker")
    k = r.get("keyword_norm")
    if not isinstance(s, str) or not isinstance(k, str): 
        continue
    u, v = f"speaker::{s}", f"keyword::{k}"
    G.add_node(u, type="speaker"); G.add_node(v, type="keyword")
    if G.has_edge(u, v): G[u][v]["weight"] += 1
    else: G.add_edge(u, v, weight=1)

# Export triples
triples = []
for u, v, data in G.edges(data=True):
    if "speaker::" in u:
        subj, obj = u.replace("speaker::",""), v.replace("keyword::","")
    else:
        subj, obj = v.replace("speaker::",""), u.replace("keyword::","")
    triples.append({
        "subject": subj,
        "relation": "mentions",
        "object": obj,
        "weight": data.get("weight", 1)
    })

Path("outputs").mkdir(exist_ok=True)
pd.DataFrame(triples).to_csv("outputs/triples.csv", index=False)
print("✅ Saved → outputs/triples.csv with", len(triples), "rows")
