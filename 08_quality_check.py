# 07_quality_check.py
import pandas as pd

ex = pd.read_csv("outputs/extracted.csv")

# take a small random sample to inspect manually
sample = ex.sample(n=min(20, len(ex)), random_state=7).reset_index(drop=True)

# Show a neat table for manual review
cols = ["speech_id", "speaker", "topic", "keyword", "date"]
print(sample[cols].to_string(index=False))

print("\n👀 Manual check instructions:")
print("- Open data/eu_debates_sample.csv and locate speeches by approximate row index (speech_id order).")
print("- Mark each row's 'keyword' as Correct (TP) or Wrong (FP).")
print("- If a major obvious theme is missing, count it as a Miss (FN).")
print("- Then compute approx precision = TP/(TP+FP) and recall = TP/(TP+FN) and write in README.")
