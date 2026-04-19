from sage.ml.feedback_scorer import feedback_score

def rerank_with_feedback(prompt, candidates, top_k=5):
    for c in candidates:
        c["feedback"] = feedback_score(prompt, c["caption"])

    candidates.sort(
        key=lambda x: x["feedback"],
        reverse=True
    )

    return candidates[:top_k]
