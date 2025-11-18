# ---------------------------------------------------------
# 03_descriptive_analysis.py
# Creates keyword frequency charts using YAKE
# ---------------------------------------------------------

import pandas as pd
import yake
import matplotlib.pyplot as plt
from pathlib import Path

print("📌 Loading extracted structured data...")
df = pd.read_csv("outputs/extracted.csv")

# ---------------------------------------------------------
# Step 1 — Load speech text
# ---------------------------------------------------------
texts = df["speech"].dropna().tolist()   # 🔥 FIXED: use "speech" not "text"

# Combine all speeches into one big text
full_text = " ".join(texts)

# ---------------------------------------------------------
# Step 2 — YAKE keyword extraction
# ---------------------------------------------------------
print("📌 Extracting keywords using YAKE...")

kw_extractor = yake.KeywordExtractor(
    lan="en",
    n=3,                # up to 3-word phrases
    dedupLim=0.1,       # reduce duplicates
    top=100             # extract top 100
)

keywords = kw_extractor.extract_keywords(full_text)

# Convert to DataFrame
kw_df = pd.DataFrame(keywords, columns=["keyword", "score"])

# Lower score = more important → sort ascending
kw_df = kw_df.sort_values("score").head(20)

# ---------------------------------------------------------
# Step 3 — Plot top keywords
# ---------------------------------------------------------
plt.figure(figsize=(10, 8))
plt.barh(kw_df["keyword"], kw_df["score"])
plt.xlabel("YAKE Score (lower = more important)")
plt.title("Top 20 Cleaned Keywords in EU Debates (YAKE)")
plt.gca().invert_yaxis()

Path("outputs").mkdir(exist_ok=True)
plt.tight_layout()
plt.savefig("outputs/top_keywords_clean.png")
plt.close()

print("✅ Keyword visualization saved to: outputs/top_keywords_clean.png")

