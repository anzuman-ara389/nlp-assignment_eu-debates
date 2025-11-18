# ---------------------------------------------------------
# 05_topic_modeling_bertopic.py
# Simple BERTopic on EU debates sample
# ---------------------------------------------------------

import pandas as pd
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from pathlib import Path

print("📌 Loading sample speeches...")
df = pd.read_csv("data/eu_debates_sample.csv")

# Use only the speech text
docs = df["speech"].dropna().astype(str).tolist()

# To keep it fast, limit to first 300–500 documents
MAX_DOCS = 400
docs = docs[:MAX_DOCS]

print(f"✅ Using {len(docs)} speeches for BERTopic")

# ---------------------------------------------------------
# STEP 1 — Define embedding model
# ---------------------------------------------------------
print("📌 Loading sentence-transformer model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------------------------------------------------
# STEP 2 — Fit BERTopic
# ---------------------------------------------------------
print("📌 Fitting BERTopic model (this may take a few minutes)...")
topic_model = BERTopic(embedding_model=embedding_model, language="english")

topics, probs = topic_model.fit_transform(docs)

# ---------------------------------------------------------
# STEP 3 — Inspect topics
# ---------------------------------------------------------
topic_info = topic_model.get_topic_info()
Path("outputs").mkdir(exist_ok=True)
topic_info.to_csv("outputs/bertopic_topics.csv", index=False)

print("\n🏆 Top 10 topics:")
print(topic_info.head(10))

# ---------------------------------------------------------
# STEP 4 — Save visualization (HTML)
# ---------------------------------------------------------
barchart = topic_model.visualize_barchart(top_n_topics=10)
barchart_path = "outputs/bertopic_barchart.html"
barchart.write_html(barchart_path)

print(f"\n✅ Saved topic summary to outputs/bertopic_topics.csv")
print(f"✅ Saved BERTopic bar chart to {barchart_path}")
print("\n🎯 BERTopic modeling complete!")
