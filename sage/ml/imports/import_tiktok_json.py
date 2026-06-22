import json
import pandas as pd

INPUT = "sage/ml/data/trending.json"
OUTPUT = "sage/ml/data/tiktok_trending.csv"

with open(INPUT, encoding="utf-8") as f:
    data = json.load(f)

rows = []

for item in data["collector"]:
    text = item.get("text", "").strip()

    if len(text) < 5:
        continue

    rows.append({
        "caption": text,
        "platform": "tiktok",
        "genre": "unknown",
        "source": "trending"
    })

df = pd.DataFrame(rows)
df.drop_duplicates(subset=["caption"], inplace=True)

df.to_csv(OUTPUT, index=False)

print(len(df))