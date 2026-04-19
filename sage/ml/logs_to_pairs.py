import json
from itertools import product

LOG_PATH = "sage/ml/data/pairwise_log.jsonl"
OUT_PATH = "sage/ml/data/caption_pairs.json"

pairs = []

with open(LOG_PATH, encoding="utf-8") as f:
    for line in f:
        row = json.loads(line)

        good = [c["caption"] for c in row["candidates"] if c["label"] == 1]
        bad = [c["caption"] for c in row["candidates"] if c["label"] == 0]

        for g, b in product(good, bad):
            pairs.append({
                "prompt": row["prompt"],
                "better": g,
                "worse": b
            })

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(pairs, f, indent=2, ensure_ascii=False)

print(f"Saved {len(pairs)} pairs")
