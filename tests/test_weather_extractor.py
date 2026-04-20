from datetime import datetime

import pandas as pd

from src.extract.weather_api import fetch_weather_data


class DummyResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def test_fetch_weather_data_returns_dataframe(monkeypatch):
    payload = {
        "name": "Brussels",
        "main": {"temp": 12.3, "humidity": 78},
        "weather": [{"description": "clear sky"}],
        "dt": 1713607200,
    }

    monkeypatch.setenv("WEATHER_API_KEY", "test-key")
    monkeypatch.setattr("src.extract.weather_api.requests.get", lambda url: DummyResponse(payload))

    df = fetch_weather_data("Brussels")

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["city", "temp", "humidity", "description", "timestamp"]
    assert df.iloc[0]["city"] == "Brussels"
    assert df.iloc[0]["temp"] == 12.3
    assert df.iloc[0]["humidity"] == 78
    assert df.iloc[0]["description"] == "clear sky"
    assert pd.Timestamp(df.iloc[0]["timestamp"]) == pd.Timestamp(datetime(2024, 4, 20, 10, 0))


def test_fetch_weather_data_returns_none_on_request_error(monkeypatch):
    class FailingResponse:
        def raise_for_status(self):
            import requests; raise requests.exceptions.RequestException("boom")

    monkeypatch.setenv("WEATHER_API_KEY", "test-key")
    monkeypatch.setattr("src.extract.weather_api.requests.get", lambda url: FailingResponse())

    assert fetch_weather_data("Brussels") is None
