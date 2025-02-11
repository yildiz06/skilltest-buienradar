import sqlite3

def create_stations_table():
    """Create the stations table with stationid as the primary key."""
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stations (
            stationid TEXT PRIMARY KEY,
            stationname TEXT,
            lat REAL,
            lon REAL,
            regio TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def create_measurements_table():
    """Create the measurements table with a foreign key to the stations table and an index on timestamp."""
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()

    # Enable foreign key support in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS measurements (
            measurementid INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL,
            groundtemperature REAL,
            feeltemperature REAL,
            windgusts REAL,
            windspeedBft REAL,
            humidity REAL,
            precipitation REAL,
            sunpower REAL,
            stationid TEXT,
            FOREIGN KEY (stationid) REFERENCES stations(stationid)
        )
    ''')
    
    # Create an index on the timestamp column to improve query performance
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_measurements_timestamp ON measurements (timestamp)
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_stations_table()
    print("Stations table created successfully!")
    
    create_measurements_table()
    print("Measurements table created successfully!")