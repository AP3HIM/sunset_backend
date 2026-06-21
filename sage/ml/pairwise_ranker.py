import pickle
import numpy as np
from sage.ml.embedder import get_embedder

MODEL_PATH = "sage/ml/data/pairwise_model.pkl"

try:
    with open(MODEL_PATH, "rb") as f:
        clf = pickle.load(f)
except FileNotFoundError:
    clf = None


def pairwise_score(prompt, caption):

    if clf is None:
        return 0.0

    embedder = get_embedder()

    pe, ce = embedder.encode(
        [prompt, caption],
        convert_to_numpy=True
    )

    x = np.concatenate(
        [pe, ce, np.abs(pe - ce)]
    ).reshape(1, -1)

    prob = clf.predict_proba(x)[0][1]

    return (prob - 0.5) * 2.0