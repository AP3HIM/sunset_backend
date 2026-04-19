import pandas as pd
import joblib
from sage.ml.features import extract_features

MODEL_PATH = "sage/ml/data/gb_caption_ranker.pkl"

_model = None

def load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def gb_score(base, caption, platform):
    model = load_model()

    feats = extract_features(base, caption, platform)

    # IMPORTANT: DataFrame with SAME column names
    X = pd.DataFrame([feats])

    # probability caption is "good"
    prob = model.predict_proba(X)[0][1]
    return prob
