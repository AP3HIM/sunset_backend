import os
import pickle
import re
import numpy as np
from sage.ml.embedder import get_embedder
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMBEDDINGS_PATH = os.path.join(BASE_DIR, "data", "caption_embeddings.pkl")

_captions_df = None
_caption_embeddings = None

def _load():
    global _captions_df, _caption_embeddings

    if _captions_df is None:
        with open(EMBEDDINGS_PATH, "rb") as f:
            data = pickle.load(f)

        _captions_df = data["captions"]
        _caption_embeddings = data["embeddings"]

def suggest_captions(prompt, genre=None, top_k=5):
    _load()
    model = get_embedder()
    prompt_embedding = model.encode(
        [prompt],
        convert_to_numpy=True
    )

    sims = cosine_similarity(
        prompt_embedding,
        _caption_embeddings
    )[0]

    _captions_df["score"] = sims
    _captions_df["boost"] = _captions_df["source"].apply(
        lambda x: 1.15 if x == "mostPopular" else 1.0
    )
    _captions_df["final_score"] = _captions_df["score"] * _captions_df["boost"]

    filtered = _captions_df.copy()
    if genre:
        filtered = filtered[filtered["genre"] == genre]

    sorted_df = filtered[
        ~filtered["caption"].apply(is_bad_template)
    ].sort_values("final_score", ascending=False)

    top_rows = diverse_top_k(
        sorted_df,
        _caption_embeddings,
        top_k
    )

    return [{
        "caption": r.get("caption", ""),
        "genre": r.get("genre", ""),
        "platform": r.get("platform", ""),
        "score": r.get("final_score", 0.0)
    } for r in top_rows if r.get("caption")]

def is_bad_template(caption):
    bad_patterns = [
        r"vs\.",
        r"week \d+",
        r"season",
        r"highlights",
        r"full game",
        r"\d{4}",  # years
    ]
    caption = caption.lower()
    return any(re.search(p, caption) for p in bad_patterns)

def diverse_top_k(df, embeddings, k=5, max_sim=0.85):
    selected = []
    selected_embeddings = []

    for idx, row in df.iterrows():
        # Guard against index being out of bounds
        if idx >= len(embeddings):
            continue

        emb = embeddings[idx]

        if not selected:
            selected.append(row.to_dict())
            selected_embeddings.append(emb)
            continue

        sims = cosine_similarity([emb], selected_embeddings)[0]

        if sims.max() < max_sim:
            selected.append(row.to_dict())
            selected_embeddings.append(emb)

        if len(selected) >= k:
            break

    return selected