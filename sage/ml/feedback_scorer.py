import pickle
from sentence_transformers import SentenceTransformer

MODEL_PATH = "sage/ml/data/feedback_model.pkl"

_embedder = None
_clf = None

def _load():
    global _embedder, _clf

    if _embedder is None:
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")

    if _clf is None:
        with open(MODEL_PATH, "rb") as f:
            _clf = pickle.load(f)

def feedback_score(prompt, caption):
    _load()

    text = f"Prompt: {prompt} || Caption: {caption}"

    emb = _embedder.encode(
        [text],
        convert_to_numpy=True
    )

    prob_good = _clf.predict_proba(emb)[0][1]

    return (prob_good - 0.5) * 1.0