import json
from datetime import datetime

LOG_PATH = "sage/ml/data/pairwise_log.jsonl"

def log_pairwise(prompt, a, b, winner):
    """
    winner: "a" or "b"
    """
    row = {
        "prompt": prompt,
        "a": a,
        "b": b,
        "winner": winner,
        "ts": datetime.utcnow().isoformat()
    }

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
