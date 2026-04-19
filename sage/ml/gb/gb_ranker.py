import joblib
import numpy as np
from sage.ml.features import extract_features

MODEL_PATH = "sage/ml/data/gb_caption_ranker.pkl"
_model = joblib.load(MODEL_PATH)

def gb_score(base, caption, platform="tiktok"):
    feats = extract_features(base, caption, platform)
    X = np.array([list(feats.values())])
    # probability caption is "good"
    return float(_model.predict_proba(X)[0][1])
