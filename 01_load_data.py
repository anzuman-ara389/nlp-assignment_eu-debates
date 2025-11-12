# 01_load_data.py
from datasets import load_dataset
import pandas as pd
from pathlib import Path

print("✅ Starting: loading EU debates dataset...")

# Ensure the 'data' folder exists
Path("data").mkdir(exist_ok=True)

# Load dataset
debates = load_dataset("RJuro/eu_debates", split="train")
df = debates.to_pandas()

print("✅ Dataset loaded with", len(df), "rows")

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# ✅ Filter for debates from 2019–2024
mask = df["date"].between("2019-01-01", "2024-12-31")

# ✅ Optionally filter for English speeches (if you want only one language)
mask = mask & (df["intervention_language"].str.lower() == "en")

# Select relevant columns
df_sub = df.loc[mask, ["speaker_name", "speaker_party", "debate_title", "date", "text"]].dropna(subset=["text"])

# Rename columns for consistency with later steps
df_sub = df_sub.rename(columns={
    "speaker_name": "speaker",
    "speaker_party": "party",
    "debate_title": "topic",
    "text": "speech"
})

# Take a small sample for easy testing
df_sample = df_sub.sample(n=min(400, len(df_sub)), random_state=42).reset_index(drop=True)

# Save to CSV
df_sample.to_csv("data/eu_debates_sample.csv", index=False)

print("✅ Saved filtered sample to data/eu_debates_sample.csv with", len(df_sample), "rows")
print(df_sample.head())

