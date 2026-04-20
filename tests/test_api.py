from datetime import datetime

import pandas as pd
from fastapi.testclient import TestClient

from src.api.fastapi import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Weather Intelligence API. Go to /docs for more."
    }


def test_weather_endpoint_returns_records(monkeypatch):
    sample_df = pd.DataFrame(
        [
            {
                "city": "Brussels",
                "temp": 12.3,
                "humidity": 78,
                "description": "clear sky",
                "timestamp": datetime(2026, 4, 20, 10, 0, 0),
            }
        ]
    )

    monkeypatch.setattr("src.api.fastapi.get_engine", lambda: object())
    monkeypatch.setattr("src.api.fastapi.pd.read_sql", lambda query, engine: sample_df)

    response = client.get("/weather")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["city"] == "Brussels"
    assert body[0]["temp"] == 12.3


def test_weather_latest_endpoint_returns_single_record(monkeypatch):
    sample_df = pd.DataFrame(
        [
            {
                "city": "Brussels",
                "temp": 12.3,
                "humidity": 78,
                "description": "clear sky",
                "timestamp": datetime(2026, 4, 20, 10, 0, 0),
            }
        ]
    )

    monkeypatch.setattr("src.api.fastapi.get_engine", lambda: object())
    monkeypatch.setattr("src.api.fastapi.pd.read_sql", lambda query, engine: sample_df)

    response = client.get("/weather/latest")

    assert response.status_code == 200
    assert response.json()["city"] == "Brussels"
    assert response.json()["temp"] == 12.3


def test_weather_latest_endpoint_returns_message_when_empty(monkeypatch):
    empty_df = pd.DataFrame([])

    monkeypatch.setattr("src.api.fastapi.get_engine", lambda: object())
    monkeypatch.setattr("src.api.fastapi.pd.read_sql", lambda query, engine: empty_df)

    response = client.get("/weather/latest")

    assert response.status_code == 200
    assert response.json() == {"message": "No data found"}