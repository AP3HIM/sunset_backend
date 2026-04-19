import pandas as pd
import re

PATH = "sage/ml/data/captions.csv"

df = pd.read_csv(PATH)

def is_good_caption(title):
    if len(title) < 6:
        return False
    if title.isupper():
        return False
    if re.search(r"(full video|episode \d+|official trailer)", title.lower()):
        return False
    return True

df = df[df["caption"].apply(is_good_caption)]
df = df.drop_duplicates(subset=["caption"])

df.to_csv(PATH, index=False)
print(f"Cleaned captions → {len(df)} remain")
