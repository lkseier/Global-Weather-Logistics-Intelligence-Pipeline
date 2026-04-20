from src.extract.weather_api import fetch_weather_data

def run_pipeline():
    print("Starting Weather Pipeline...")
    
    # 1. EXTRACT
    raw_df = fetch_weather_data("Brussels")
    
    if raw_df is not None:
        print(f"Extracted data for: {raw_df['city'].iloc[0]}")
        print(raw_df)
        
        # Next up: 2. TRANSFORM & 3. LOAD (Coming soon!)
    else:
        print("Pipeline stopped due to extraction error.")

if __name__ == "__main__":
    run_pipeline()