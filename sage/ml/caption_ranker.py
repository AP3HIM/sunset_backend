import os
import pickle
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMBEDDINGS_PATH = os.path.join(BASE_DIR, "data", "caption_embeddings.pkl")

model = SentenceTransformer("all-MiniLM-L6-v2")

with open(EMBEDDINGS_PATH, "rb") as f:
    data = pickle.load(f)

captions_df = data["captions"]
caption_embeddings = data["embeddings"]

def suggest_captions(prompt, genre=None, top_k=5):
    prompt_embedding = model.encode([prompt])
    sims = cosine_similarity(prompt_embedding, caption_embeddings)[0]

    captions_df["score"] = sims
    captions_df["boost"] = captions_df["source"].apply(
        lambda x: 1.15 if x == "mostPopular" else 1.0
    )
    captions_df["final_score"] = captions_df["score"] * captions_df["boost"]

    filtered = captions_df
    if genre:
        filtered = filtered[filtered["genre"] == genre]

    sorted_df = filtered[
        ~filtered["caption"].apply(is_bad_template)
    ].sort_values("final_score", ascending=False)

    top_rows = diverse_top_k(
        sorted_df,
        caption_embeddings,
        top_k
    )

    return [{
        "caption": r["caption"],
        "genre": r["genre"],
        "platform": r["platform"],
        "score": r["final_score"]
    } for r in top_rows]

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
        emb = embeddings[idx]

        if not selected:
            selected.append(row)
            selected_embeddings.append(emb)
            continue

        sims = cosine_similarity(
            [emb], selected_embeddings
        )[0]

        if sims.max() < max_sim:
            selected.append(row)
            selected_embeddings.append(emb)

        if len(selected) >= k:
            break

    return selected