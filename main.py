from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
import numpy as np
from sklearn.linear_model import LinearRegression
import os

app = FastAPI()

#pobieranie zmiennej środowiskowej
APP_ENV = os.getenv("APP_ENVIRONMENT", "local")
API_KEY = os.getenv("MY_SECRET_KEY", "not-set")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "mode": "online",
        "environment": APP_ENV,
        "key_status": "provided" if API_KEY != "not-set" else "missing"
    }

#model
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])
model = LinearRegression().fit(X, y)

#FastAPI sprawdza czy dane zostały wysłane zgodnie ze schematem (musi być pole value)
class PredictionInput(BaseModel):
    value: float

@app.post("/predict")
async def predict(data: PredictionInput):
    try:
        #wykonanie predykcji
        result = model.predict([[data.value]])
        return {
            "prediction": float(result[0]),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Wystąpił błąd")

#informacje o modelu
@app.get("/info")
def get_model_info():
    return {
        "model_type": type(model).__name__,
        "n_features": model.n_features_in_,
        "coefficients": model.coef_.tolist(),
        "intercept": float(model.intercept_),
        "description": "Model regresji liniowej"
    }

