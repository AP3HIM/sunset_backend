import pickle
from sage.ml.embedder import get_embedder

MODEL_PATH = "sage/ml/data/feedback_model.pkl"

_clf = None


def _load():
    global _clf

    if _clf is None:
        with open(MODEL_PATH, "rb") as f:
            _clf = pickle.load(f)


def feedback_score(prompt, caption):
    _load()

    embedder = get_embedder()

    text = f"Prompt: {prompt} || Caption: {caption}"

    emb = embedder.encode(
        [text],
        convert_to_numpy=True
    )

    prob_good = _clf.predict_proba(emb)[0][1]

    return (prob_good - 0.5)