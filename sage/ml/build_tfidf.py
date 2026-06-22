import os
import pickle
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "captions.csv"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "tfidf_data.pkl"
)

df = pd.read_csv(DATA_PATH)

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2),
    max_features=20000
)

matrix = vectorizer.fit_transform(
    df["caption"].fillna("")
)

with open(OUTPUT_PATH, "wb") as f:
    pickle.dump(
        {
            "captions": df,
            "vectorizer": vectorizer,
            "matrix": matrix,
        },
        f
    )

print("Saved TF-IDF model.")