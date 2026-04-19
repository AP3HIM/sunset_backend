import json
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = "sage/ml/data/pairwise_model.pkl"
DATA_PATH = "sage/ml/data/caption_pairs.json"

model = SentenceTransformer("all-MiniLM-L6-v2")

with open(DATA_PATH, encoding="utf-8") as f:
    pairs = json.load(f)

X = []
y = []

for p in pairs:
    pe = model.encode(p["prompt"])
    be = model.encode(p["better"])
    we = model.encode(p["worse"])

    X.append(np.concatenate([pe, be, np.abs(pe - be)]))
    y.append(1)

    X.append(np.concatenate([pe, we, np.abs(pe - we)]))
    y.append(0)

clf = LogisticRegression(max_iter=1000)
clf.fit(X, y)

with open(MODEL_PATH, "wb") as f:
    pickle.dump(clf, f)

print("Pairwise model trained")
