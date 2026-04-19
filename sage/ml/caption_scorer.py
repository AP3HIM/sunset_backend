import re
import numpy as np

def score_caption(caption):
    score = 0.0

    length = len(caption.split())
    if 4 <= length <= 12:
        score += 1.0
    else:
        score -= 0.5

    if caption.endswith(("!", "?", "…")):
        score += 0.3

    if re.search(r"\b(insane|crazy|wild|unreal|nobody)\b", caption.lower()):
        score += 0.5

    if caption.isupper():
        score -= 1.5
        
    if sum(1 for c in caption if c.isupper()) > len(caption) * 0.4:
        score -= 0.7


    if len(caption) > 80:
        score -= 0.5

    return score
