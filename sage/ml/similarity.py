from sentence_transformers import SentenceTransformer
import numpy as np

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def similarity_penalty(prompt, caption):
    p_emb, c_emb = embedder.encode([prompt, caption])
    sim = cosine_sim(p_emb, c_emb)

    # TOO similar = boring / copy
    if sim > 0.85:
        return -1.0 * (sim - 0.85) * 5

    # TOO dissimilar = irrelevant
    if sim < 0.45:
        return -1.5

    return 0.0
