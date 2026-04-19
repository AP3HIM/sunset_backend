import pickle
from sentence_transformers import SentenceTransformer

MODEL_PATH = "sage/ml/data/feedback_model.pkl"

embedder = SentenceTransformer("all-MiniLM-L6-v2")

with open(MODEL_PATH, "rb") as f:
    clf = pickle.load(f)

def feedback_score(prompt, caption):
    text = f"Prompt: {prompt} || Caption: {caption}"
    emb = embedder.encode([text])
    prob_good = clf.predict_proba(emb)[0][1]
    return (prob_good - 0.5) * 1.0
