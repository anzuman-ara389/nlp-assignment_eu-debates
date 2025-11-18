import pandas as pd
import json
from pathlib import Path

print("Loading extracted.csv ...")
df = pd.read_csv("outputs/extracted.csv")

df = df.where(pd.notnull(df), None)
df = df.replace("NaN", None)

records = []

for _, row in df.iterrows():

    # ===== SENTIMENT FIX (SOLVES YOUR PROBLEM) =====
    raw_sent = row.get("sentiment")

    if raw_sent is None:
        sentiment_value = None
    else:
        raw_sent_str = str(raw_sent).strip().lower()
        if raw_sent_str in ["nan", "none", "", "null"]:
            sentiment_value = None
        else:
            sentiment_value = raw_sent
    # ================================================

    item = {
        "speaker": row.get("speaker"),
        "speech": row.get("speech", ""),
        "topic": row.get("topic"),
        "keyword": row.get("keyword"),
        "party": row.get("party"),
        "sentiment": sentiment_value,
        "date": row.get("date"),
        "id": row.get("speech_id"),

        "year": str(row.get("date"))[:4] if row.get("date") else None,
        "speaker_party": f"{row.get('speaker')} ({row.get('party')})"
    }

    records.append(item)

Path("outputs").mkdir(exist_ok=True)

with open("outputs/eu_debates_structured.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=4, ensure_ascii=False)

print("✅ ALL NaN FIXED SUCCESSFULLY!")


