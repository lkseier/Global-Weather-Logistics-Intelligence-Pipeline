import pandas as pd
from src.load.database import get_engine

def view_stored_data():
    engine = get_engine()
    query = "SELECT * FROM weather_reports ORDER BY timestamp DESC LIMIT 10;"
    
    try:
        # Use Pandas to read the SQL query directly into a DataFrame
        df = pd.read_sql(query, engine)
        
        if df.empty:
            print("Ø The database table is empty.")
        else:
            print("pLatest Weather Records in Database:")
            print(df)
            
    except Exception as e:
        print(f"Error reading from database: {e}")

if __name__ == "__main__":
    view_stored_data()