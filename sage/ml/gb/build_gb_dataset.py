# backend/sage/ml/gb/build_gb_dataset.py

import json
import pandas as pd
from sage.ml.features import extract_features

INPUT_PATH = "sage/ml/data/caption_pairs.json"
OUTPUT_PATH = "sage/ml/data/gb_train.csv"

def build_dataset():
    rows = []

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for row in data:
        base = row["prompt"]
        platform = row.get("platform", "tiktok")

        better = row["better"]
        worse = row["worse"]

        better_feats = extract_features(base, better, platform)
        worse_feats = extract_features(base, worse, platform)

        rows.append({**better_feats, "label": 1})
        rows.append({**worse_feats, "label": 0})

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved {len(df)} rows → {OUTPUT_PATH}")

if __name__ == "__main__":
    build_dataset()
