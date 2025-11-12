# 02_extract_structured.py
import pandas as pd, json, re
from tqdm import tqdm
from pydantic import BaseModel, Field
from typing import Optional
from pathlib import Path

# Step 1: Load the sample data created in Step 1
print("✅ Loading sample data...")
df = pd.read_csv("data/eu_debates_sample.csv")
print("✅ Loaded", len(df), "rows")

# Step 2: Define a structured schema (like an LLM output)
class Record(BaseModel):
    speaker: Optional[str]
    party: Optional[str]
    topic: Optional[str]
    keyword: str
    sentiment: Optional[str] = Field(None, pattern="^(positive|negative|neutral)$")
    date: Optional[str]
    speech_id: str

# Step 3: Simple mock extraction function
def mock_extract(speech, speaker, party, topic, date, sid):
    # Grab 3–4 “keywords” from each speech
    toks = re.findall(r"[A-Za-z]{4,}", (speech or "")[:400])
    keyword = " ".join(toks[:3]).lower() if toks else "general policy"
    return {
        "speaker": speaker,
        "party": party,
        "topic": topic,
        "keyword": keyword,
        "sentiment": None,  # later we can estimate sentiment
        "date": str(date)[:10],
        "speech_id": sid
    }

# Step 4: Run the extraction
records = []
for i, r in tqdm(df.iterrows(), total=len(df)):
    sid = f"speech_{i:06d}"
    rec = mock_extract(r["speech"], r["speaker"], r["party"], r["topic"], r["date"], sid)
    records.append(rec)

# Step 5: Convert to DataFrame
extracted = pd.DataFrame(records)

# Step 6: Save to outputs/
Path("outputs").mkdir(exist_ok=True)
extracted.to_csv("outputs/extracted.csv", index=False)
print("✅ Done! Saved structured data to outputs/extracted.csv")

# Show preview
print(extracted.head())
