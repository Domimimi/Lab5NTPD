from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_predictions_not_none():
    response = client.post("/predict", json={"value": 5.0})
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] is not None, "Predictions should not be None."


def test_predictions_length():
    response = client.post("/predict", json={"value": 10.0})
    data = response.json()

    assert "prediction" in data
    assert data["status"] == "success"
    assert isinstance(data["prediction"], float)


def test_predictions_value_range():
    test_val = 3.0
    response = client.post("/predict", json={"value": test_val})
    prediction = response.json()["prediction"]

    assert 5.9 <= prediction <= 6.1, f"Prediction for {test_val} should be around 6.0"


def test_model_accuracy():
    response = client.get("/info")
    assert response.status_code == 200
    info = response.json()

    coef = info["coefficients"][0]
    assert abs(coef - 2.0) < 0.01, f"Model accuracy/slope is wrong. Expected 2.0, got {coef}"