# ---------------------------------------------------------
# 02_extract_structured.py
# Converts speeches into structured rows (LLM-style mock)
# ---------------------------------------------------------

import pandas as pd
import re
from tqdm import tqdm
from pathlib import Path

print("📌 Loading sample speeches...")
df = pd.read_csv("data/eu_debates_sample.csv")   # This file created in Step 1

# ---------------------------------------------------------
# Mock extractor (simulating LLM behavior)
# ---------------------------------------------------------
def mock_extract(speech, speaker, party, topic, date, sid):
    """
    A simple extractor that:
    - picks first 3 meaningful words as keyword
    - keeps original speech (important for later analysis)
    """
    # Extract tokens of length >= 4
    toks = re.findall(r"[A-Za-z]{4,}", (speech or "")[:400])

    # Take first 3 tokens as simple keyword
    keyword = " ".join(toks[:3]).lower() if toks else "general policy"

    return {
        "speech": speech,           # 🔥 ADDED (important for Step 3)
        "speaker": speaker,
        "party": party,
        "topic": topic,
        "keyword": keyword,
        "sentiment": None,          # placeholder for later
        "date": str(date)[:10],
        "speech_id": sid
    }

# ---------------------------------------------------------
# Run extraction for each speech
# ---------------------------------------------------------
print("📌 Extracting structured records...")

records = []

for i, r in tqdm(df.iterrows(), total=len(df)):
    sid = f"speech_{i:06d}"     # unique ID
    rec = mock_extract(
        r["speech"],
        r["speaker"],
        r["party"],
        r["topic"],
        r["date"],
        sid
    )
    records.append(rec)

# ---------------------------------------------------------
# Save output
# ---------------------------------------------------------
Path("outputs").mkdir(exist_ok=True)

out_df = pd.DataFrame(records)
out_path = "outputs/extracted.csv"

out_df.to_csv(out_path, index=False)

print(f"✅ Done! Saved structured dataset to: {out_path}")
print("🟢 Columns saved:", list(out_df.columns))
