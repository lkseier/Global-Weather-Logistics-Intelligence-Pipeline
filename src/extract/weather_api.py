import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load env from the root directory
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

def fetch_weather_data(city="Brussels"):
    """
    Extracts weather data for a specific city from OpenWeatherMap API.
    Returns: A Pandas DataFrame or None if error occurs.
    """
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status() # This raises an error for 4xx or 5xx responses
        data = response.json()
        
        # Initial minimal transformation (The 'T' in ETL)
        df = pd.DataFrame([{
            "city": data["name"],
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "timestamp": pd.to_datetime(data["dt"], unit='s')
        }])
        
        return df
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        return None