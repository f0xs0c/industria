import os
import requests
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

DATA_PATH = os.getenv("DATA_PATH", "/data/dataset.csv")
MODEL_URL = os.getenv("MODEL_URL", "http://model_service:8001/predict")

app = FastAPI(title="Industria API Service", version="1.0.0")

# (CORS inutile côté prod grâce au reverse proxy Nginx du frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/stats")
def stats():
    try:
        df = pd.read_csv(DATA_PATH)
        if df.empty:
            raise HTTPException(status_code=503, detail="No data yet")
        tail = df.tail(300)  # fenêtre récente
        means = tail[["temperature","pressure","flow","yield"]].mean().round(3).to_dict()
        last = tail.iloc[-1][["temperature","pressure","flow","yield"]].round(3).to_dict()
        return {"means": means, "last": last, "count": int(len(df))}
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Dataset not found")

@app.get("/predict")
def predict_from_latest():
    try:
        df = pd.read_csv(DATA_PATH)
        row = df.iloc[-1]
        payload = {
            "temperature": float(row["temperature"]),
            "pressure": float(row["pressure"]),
            "flow": float(row["flow"]),
        }
        r = requests.post(MODEL_URL, json=payload, timeout=5)
        r.raise_for_status()
        return {"input": payload, "prediction": r.json()}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Model unavailable: {e}")
