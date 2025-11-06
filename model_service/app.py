import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

DATA_PATH = os.getenv("DATA_PATH", "/data/dataset.csv")
MODEL_PATH = os.getenv("MODEL_PATH", "/model/model.pkl")

app = FastAPI(title="Industria Model Service", version="1.0.0")

class Features(BaseModel):
    temperature: float = Field(..., description="Celsius")
    pressure: float = Field(..., description="bar")
    flow: float = Field(..., description="L/min")

# Charger ou entraîner si absent
if not os.path.exists(MODEL_PATH):
    # Entraînement de secours (petit set si data indispo)
    import subprocess
    subprocess.run(["python", "/app/train_model.py"], check=True)

model = joblib.load(MODEL_PATH)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/predict")
def predict(feat: Features):
    try:
        X = pd.DataFrame([
            {
                "temperature": feat.temperature,
                "pressure": feat.pressure,
                "flow": feat.flow,
            }
        ])
        y = model.predict(X)[0]
        return {"predicted_yield": float(round(y, 3))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
