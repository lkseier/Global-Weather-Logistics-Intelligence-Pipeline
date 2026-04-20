import os
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    """Creates a connection engine to the PostgreSQL database."""
    # In a real project, these would be in the .env file!
    user = "myuser"
    password = "mypassword"
    host = "localhost"
    port = "5432"
    db = "weather_data"
    
    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(url)
    return engine

def load_data_to_sql(df, table_name):
    """Loads a Pandas DataFrame into the SQL database."""
    engine = get_engine()
    try:
        # 'append' means it adds new rows each time the script runs
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Successfully loaded {len(df)} rows to table '{table_name}'")
    
    except IntegrityError:
        # This triggers if the UNIQUE constraint is violated
        print(f"Skipping Load: Data for this timestamp already exists in '{table_name}'.")

    except Exception as e:
        print(f"Database error: {e}")