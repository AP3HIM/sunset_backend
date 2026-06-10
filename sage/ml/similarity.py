from sentence_transformers import SentenceTransformer
import numpy as np

_embedder = None

def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedder

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def similarity_penalty(prompt, caption):
    embedder = get_embedder()

    p_emb, c_emb = embedder.encode(
        [prompt, caption],
        convert_to_numpy=True
    )

    sim = cosine_sim(p_emb, c_emb)

    if sim > 0.85:
        return -1.0 * (sim - 0.85) * 5

    if sim < 0.45:
        return -1.5

    return 0.0