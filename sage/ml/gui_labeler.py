import tkinter as tk
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

class CaptionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pairwise Caption Labeler")

        self.prompt_idx = 0
        self.check_vars = []

        self.prompt_label = tk.Label(root, text="", font=("Arial", 14))
        self.prompt_label.pack(pady=10)

        self.caption_frame = tk.Frame(root)
        self.caption_frame.pack()

        self.submit_btn = tk.Button(root, text="Save + Next", command=self.save_and_next)
        self.submit_btn.pack(pady=10)

        self.load_prompt()

    def load_prompt(self):
        for w in self.caption_frame.winfo_children():
            w.destroy()

        self.check_vars = []

        prompt, genre = PROMPTS[self.prompt_idx]
        self.prompt_label.config(text=f"PROMPT: {prompt}")

        ranked = suggest_captions(prompt, genre=genre, top_k=10)
        self.results = generate_caption_v03(
            base_caption=prompt,
            ranked_captions=ranked,
            genre=genre,
            platform="youtube",
            n=5
        )

        for i, r in enumerate(self.results):
            var = tk.IntVar()
            cb = tk.Checkbutton(
                self.caption_frame,
                text=f"{i+1}. {r['caption']}",
                variable=var,
                wraplength=700,
                justify="left"
            )
            cb.pack(anchor="w")
            self.check_vars.append(var)

    def save_and_next(self):
        prompt, genre = PROMPTS[self.prompt_idx]

        entry = {
            "ts": time.time(),
            "prompt": prompt,
            "genre": genre,
            "candidates": []
        }

        for i, r in enumerate(self.results):
            entry["candidates"].append({
                "caption": r["caption"],
                "score": round(r["score"], 3),
                "label": int(self.check_vars[i].get())
            })

        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        self.prompt_idx = (self.prompt_idx + 1) % len(PROMPTS)
        self.load_prompt()

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptionGUI(root)
    root.mainloop()