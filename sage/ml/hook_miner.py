import pandas as pd
import re
from collections import Counter

def extract_hooks(captions, min_words=3, max_words=6):
    hooks = []

    for cap in captions:
        parts = re.split(r"[:\-|]", cap)
        first = parts[0].strip()
        words = first.split()

        if min_words <= len(words) <= max_words:
            hooks.append(" ".join(words))

    return hooks

def build_hook_library(csv_path):
    df = pd.read_csv(csv_path)

    hooks_by_genre = {}

    for genre in df["genre"].unique():
        caps = df[df["genre"] == genre]["caption"].tolist()
        hooks = extract_hooks(caps)
        hooks_by_genre[genre] = Counter(hooks).most_common(50)

    return hooks_by_genre
