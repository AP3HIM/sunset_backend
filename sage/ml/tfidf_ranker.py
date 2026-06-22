import os
import pickle
import re

from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TFIDF_PATH = os.path.join(
    BASE_DIR,
    "data",
    "tfidf_data.pkl"
)

_df = None
_vectorizer = None
_matrix = None


def _load():
    global _df, _vectorizer, _matrix

    if _df is None:
        with open(TFIDF_PATH, "rb") as f:
            data = pickle.load(f)

        _df = data["captions"]
        _vectorizer = data["vectorizer"]
        _matrix = data["matrix"]


def suggest_captions(prompt, genre=None, top_k=5):
    _load()

    query = _vectorizer.transform([prompt])

    sims = cosine_similarity(
        query,
        _matrix
    )[0]

    df = _df.copy()

    df["score"] = sims

    df["boost"] = df["source"].apply(
        lambda x: 1.15 if x == "mostPopular" else 1.0
    )

    df["final_score"] = (
        df["score"] * df["boost"]
    )

    if genre:
        df = df[df["genre"] == genre]

    df = df[
        ~df["caption"].apply(is_bad_template)
    ]

    df = df.sort_values(
        "final_score",
        ascending=False
    )

    rows = df.head(top_k)

    return [
        {
            "caption": r["caption"],
            "genre": r.get("genre", ""),
            "platform": r.get("platform", ""),
            "score": r.get("final_score", 0)
        }
        for _, r in rows.iterrows()
    ]


def is_bad_template(caption):
    patterns = [
        r"vs\.",
        r"week \d+",
        r"season",
        r"highlights",
        r"full game",
        r"\d{4}",
    ]

    caption = caption.lower()

    return any(
        re.search(p, caption)
        for p in patterns
    )