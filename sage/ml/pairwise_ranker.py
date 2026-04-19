import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_PATH = "sage/ml/data/pairwise_model.pkl"

embedder = SentenceTransformer("all-MiniLM-L6-v2")

try:
    with open(MODEL_PATH, "rb") as f:
        clf = pickle.load(f)
except FileNotFoundError:
    clf = None


def pairwise_score(prompt, caption):
    """
    Returns a scalar preference score.
    Higher = better.
    Safe to call even if model doesn't exist yet.
    """
    if clf is None:
        return 0.0

    pe = embedder.encode(prompt)
    ce = embedder.encode(caption)

    x = np.concatenate([pe, ce, np.abs(pe - ce)]).reshape(1, -1)
    prob = clf.predict_proba(x)[0][1]

    # center around 0
    return (prob - 0.5) * 2.0
