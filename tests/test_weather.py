import pytest
import pandas as pd
from src.extract.weather_api import fetch_weather_data

def test_fetch_weather_structure():
    """Test that the API returns the correct columns and data type."""
    df = fetch_weather_data("Brussels")
    
    # Check if it's a DataFrame
    assert isinstance(df, pd.DataFrame)
    
    # Check if essential columns are present
    expected_cols = ["city", "temp", "humidity", "timestamp"]
    for col in expected_cols:
        assert col in df.columns
        
    # Check if we actually got data
    assert len(df) > 0