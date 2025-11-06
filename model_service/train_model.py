import os
import time
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

DATA_PATH = os.getenv("DATA_PATH", "/data/dataset.csv")
MODEL_PATH = os.getenv("MODEL_PATH", "/model/model.pkl")
MIN_ROWS = int(os.getenv("MIN_ROWS", "50"))

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

def wait_for_data(path: str, min_rows: int):
    while True:
        if os.path.exists(path):
            try:
                n = sum(1 for _ in open(path, "r")) - 1  # minus header
                if n >= min_rows:
                    return
            except Exception:
                pass
        time.sleep(1)

wait_for_data(DATA_PATH, MIN_ROWS)

df = pd.read_csv(DATA_PATH)
# Features & target
X = df[["temperature","pressure","flow"]]
y = df["yield"]

model = RandomForestRegressor(n_estimators=120, random_state=42)
model.fit(X, y)

joblib.dump(model, MODEL_PATH)
print(f"Model trained and saved to {MODEL_PATH}")
