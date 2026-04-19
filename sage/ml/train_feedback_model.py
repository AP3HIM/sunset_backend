import json
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

DATA_PATH = "sage/ml/data/caption_feedback.json"
MODEL_OUT = "sage/ml/data/feedback_model.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")

# Load feedback
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

texts = []
labels = []

for row in data:
    text = f"Prompt: {row['prompt']} || Caption: {row['caption']}"
    texts.append(text)
    labels.append(row["label"])

X = model.encode(texts)
y = labels

clf = LogisticRegression(max_iter=1000)
clf.fit(X, y)

with open(MODEL_OUT, "wb") as f:
    pickle.dump(clf, f)

print(" Feedback model trained and saved")
