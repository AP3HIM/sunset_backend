import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

DATA_PATH = "sage/ml/data/gb_train.csv"
MODEL_PATH = "sage/ml/data/gb_caption_ranker.pkl"

def train():
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["label"])
    y = df["label"]

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = GradientBoostingClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=3,
        subsample=0.8,
        random_state=42,
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_val)
    acc = accuracy_score(y_val, preds)

    print("Validation accuracy:", acc)

    joblib.dump(model, MODEL_PATH)
    print("Saved model to", MODEL_PATH)


if __name__ == "__main__":
    train()
