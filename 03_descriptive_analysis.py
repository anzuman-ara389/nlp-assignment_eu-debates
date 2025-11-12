# 03_descriptive_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

print("✅ Loading structured data...")
ex = pd.read_csv("outputs/extracted.csv")
print("✅ Loaded", len(ex), "rows")

# Step 1: Clean up the keyword text
ex["keyword_norm"] = (
    ex["keyword"]
    .str.lower()
    .str.replace(r"[^a-z0-9\s\-]", "", regex=True)
    .str.strip()
)

# Step 2: Basic counts
top_keywords = ex["keyword_norm"].value_counts().head(20)
print("\n🔝 Top 20 keywords:\n", top_keywords)

# Step 3: Plot the top keywords
Path("outputs").mkdir(exist_ok=True)
plt.figure(figsize=(7,6))
top_keywords[::-1].plot(kind="barh")
plt.title("Top 20 Keywords in EU Debates")
plt.xlabel("Frequency")
plt.ylabel("Keyword")
plt.tight_layout()
plt.savefig("outputs/top_keywords.png")
print("✅ Saved bar chart → outputs/top_keywords.png")

# Step 4: Quick summary by party (if present)
if "party" in ex.columns:
    party_counts = ex["party"].value_counts().head(10)
    print("\n🏛️ Top 10 parties:\n", party_counts)
    plt.figure(figsize=(7,6))
    party_counts[::-1].plot(kind="barh", color="teal")
    plt.title("Top 10 Speaker Parties")
    plt.tight_layout()
    plt.savefig("outputs/top_parties.png")
    print("✅ Saved chart → outputs/top_parties.png")

print("\n🎉 Descriptive analysis complete!")
