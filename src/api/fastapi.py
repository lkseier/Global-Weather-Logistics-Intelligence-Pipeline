from fastapi import FastAPI, HTTPException
from src.load.database import get_engine
import pandas as pd

app = FastAPI(title="Brussels Weather API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Weather Intelligence API. Go to /docs for more."}

@app.get("/weather")
def get_all_weather():
    """Fetch all stored weather records from the database."""
    engine = get_engine()
    query = "SELECT * FROM weather_reports ORDER BY timestamp DESC"
    
    try:
        df = pd.read_sql(query, engine)
        # Convert DataFrame to a list of dictionaries for JSON output
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather/latest")
def get_latest_weather():
    """Fetch only the most recent weather record."""
    engine = get_engine()
    query = "SELECT * FROM weather_reports ORDER BY timestamp DESC LIMIT 1"
    
    try:
        df = pd.read_sql(query, engine)
        if df.empty:
            return {"message": "No data found"}
        return df.to_dict(orient="records")[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))