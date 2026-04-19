import json
import time
from sage.ml.caption_ranker import suggest_captions
from sage.ml.caption_generator import generate_caption_v03

LOG_PATH = "sage/ml/data/pairwise_log.jsonl"

PROMPTS = [
    ("crazy ending to the bears game", "sports"),
    ("insane fortnite clutch", "gaming"),
    ("ai explained in 30 seconds", "science_tech"),
]

def log_result(prompt, genre, results):
    print("\nEnter GOOD caption numbers (comma separated), e.g. 1,4")
    good_idxs = input(">> ").strip()
    good_set = set(int(i) for i in good_idxs.split(",") if i.strip().isdigit())

    entry = {
        "ts": time.time(),
        "prompt": prompt,
        "genre": genre,
        "candidates": []
    }

    for i, r in enumerate(results):
        entry["candidates"].append({
            "caption": r["caption"],
            "score": round(r["score"], 3),
            "label": 1 if (i + 1) in good_set else 0
        })

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


for prompt, genre in PROMPTS:
    print("\n" + "=" * 60)
    print("PROMPT:", prompt)

    ranked = suggest_captions(prompt, genre=genre, top_k=10)

    results = generate_caption_v03(
        base_caption=prompt,
        ranked_captions=ranked,
        genre=genre,
        platform="youtube",
        n=5
    )

    for i, r in enumerate(results, 1):
        print(f"{i}. {r['caption']}  | score={round(r['score'], 2)}")

    log_result(prompt, genre, results)
