from src.extract.weather_api import fetch_weather_data
from src.load.database import load_data_to_sql  # New import

def run_pipeline():
    print("Starting Weather Pipeline for Brussels...")
    
    # 1. EXTRACT
    raw_df = fetch_weather_data("Brussels")
    
    if raw_df is not None:
        # 2. TRANSFORM (Currently minimal, done inside extract)
        
        # 3. LOAD
        load_data_to_sql(raw_df, "weather_reports")
    else:
        print("Pipeline stopped.")

if __name__ == "__main__":
    run_pipeline()