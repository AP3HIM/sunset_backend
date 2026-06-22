import pandas as pd

df = pd.read_csv(
    "sage/ml/data/captions_csv.csv"
)

df = df.rename(
    columns={"Caption": "caption"}
)

df["platform"] = "instagram"
df["genre"] = "unknown"
df["source"] = "instagram"

df = df[
    ["caption", "platform", "genre", "source"]
]

df.dropna(inplace=True)
df.drop_duplicates(subset=["caption"], inplace=True)

df.to_csv(
    "sage/ml/data/instagram_clean.csv",
    index=False
)

print(len(df))