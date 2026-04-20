-- scripts/init.sql
CREATE TABLE IF NOT EXISTS weather_reports (
    city VARCHAR(100),
    temp FLOAT,
    humidity INT,
    description TEXT,
    timestamp TIMESTAMP,
    CONSTRAINT unique_city_time UNIQUE (city, timestamp)
);