import os
import pandas as pd
import pickle
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "data", "captions.csv")
EMBEDDINGS_PATH = os.path.join(BASE_DIR, "data", "caption_embeddings.pkl")

def build_embeddings():
    df = pd.read_csv(DATA_PATH)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Embedding captions...")
    embeddings = model.encode(df["caption"].tolist(), show_progress_bar=True)

    with open(EMBEDDINGS_PATH, "wb") as f:
        pickle.dump({
            "captions": df,
            "embeddings": embeddings
        }, f)

    print(f"Saved embeddings to {EMBEDDINGS_PATH}")

if __name__ == "__main__":
    build_embeddings()
