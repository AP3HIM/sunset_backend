import json
from itertools import product

INPUT = "sage/ml/data/pairwise_log.jsonl"
OUTPUT = "sage/ml/data/caption_pairs.json"

pairs = []

with open(INPUT, encoding="utf-8") as f:
    for line in f:
        row = json.loads(line)

        prompt = row["prompt"]
        candidates = row["candidates"]

        good = [c["caption"] for c in candidates if c.get("label") == 1]
        bad = [c["caption"] for c in candidates if c.get("label") == 0]

        for g, b in product(good, bad):
            pairs.append({
                "prompt": prompt,
                "better": g,
                "worse": b
            })

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(pairs, f, indent=2, ensure_ascii=False)

print(f"Saved {len(pairs)} pairs")