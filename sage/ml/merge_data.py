# merge_data.py

import pandas as pd
import json
import os

rows = []

# tiktok trending.json
with open("sage/ml/data/trending.json", encoding="utf8") as f:
    data = json.load(f)

for item in data["collector"]:
    text = item.get("text")

    if text and len(text) > 5:
        rows.append({
            "caption": text,
            "genre": "general",
            "platform": "tiktok",
            "source": "tiktok"
        })
#tiktok train.csv
df = pd.read_csv("sage/ml/data/train.csv")

for text in df["description"].dropna():
    rows.append({
        "caption": text,
        "genre": "general",
        "platform": "tiktok",
        "source": "tiktok"
    })

# instagram captions_csv.csv
df = pd.read_csv("sage/ml/data/captions_csv.csv")

for text in df["Caption"].dropna():
    rows.append({
        "caption": text,
        "genre": "general",
        "platform": "instagram",
        "source": "instagram"
    })

# clickbait
df = pd.read_csv("sage/ml/data/clickbait.csv")

for text in df["headline"].dropna():
    rows.append({
        "caption": text,
        "genre": "viral",
        "platform": "youtube",
        "source": "clickbait"
    })

# reddit
reddit_files = [
    "AnimalsBeingBros.csv",
    "AskOuija.csv",
    "mildlyinteresting.csv",
    "questions.csv",
    "technology.csv"
]

for file in reddit_files:
    df = pd.read_csv(file)

    if "title" not in df.columns:
        continue

    for text in df["title"].dropna():
        rows.append({
            "caption": text,
            "genre": "reddit",
            "platform": "reddit",
            "source": "reddit"
        })

final = pd.DataFrame(rows)

final = final.drop_duplicates(
    subset=["caption"]
)

final = final[
    final["caption"].str.len() > 5
]

final.to_csv(
    "sage/ml/data/captions.csv",
    index=False
)

print(len(final))