import requests
import sqlite3
import json
from datetime import datetime
import time
import schedule

API_URL = "https://data.buienradar.nl/2.0/feed/json"

def fetch_weather_data():
    """Haalt weerdata op van de Buienradar API en retourneert een JSON-object."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return data.get("actual", {}).get("stationmeasurements", [])
    except requests.exceptions.RequestException as e:
        print(f"Fout bij het ophalen van de API-data: {e}")
        return None

def insert_data_into_db(data):
    """
    Zet de opgehaalde JSON-data om in database records.
    - Stationinformatie wordt opgeslagen in de 'stations'-tabel (voorkomt duplicaten).
    - Metingen worden opgeslagen in de 'measurements'-tabel.
    """
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()

    for station in data:
        station_id = str(station.get("stationid"))
        station_name = station.get("stationname")
        lat = station.get("lat")
        lon = station.get("lon")
        region = station.get("regio")

        cursor.execute("""
            INSERT OR IGNORE INTO stations (stationid, stationname, lat, lon, regio)
            VALUES (?, ?, ?, ?, ?)
        """, (station_id, station_name, lat, lon, region))

        temperature = station.get("temperature")
        groundtemperature = station.get("groundtemperature")
        feeltemperature = station.get("feeltemperature")
        windgusts = station.get("windgusts")
        windspeedBft = station.get("windspeedBft")
        humidity = station.get("humidity")
        precipitation = station.get("precipitation")
        sunpower = station.get("sunpower")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO measurements (timestamp, temperature, groundtemperature, feeltemperature,
            windgusts, windspeedBft, humidity, precipitation, sunpower, stationid)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, temperature, groundtemperature, feeltemperature,
              windgusts, windspeedBft, humidity, precipitation, sunpower, station_id))

    conn.commit()
    conn.close()
    print(f"Data succesvol ingevoerd op {timestamp}")

def job():
    """Voert de extract, transform en load uit."""
    print(f"Data ophalen op: {datetime.now()}")
    data = fetch_weather_data()
    if data:
        insert_data_into_db(data)
        print("Nieuwe data toegevoegd aan database.\n")
    else:
        print("Geen data ontvangen.\n")

def main():
    job()

    schedule.every(20).minutes.do(job)

    start_time = datetime.now()
    while True:
        schedule.run_pending()
        time.sleep(1)
        if (datetime.now() - start_time).total_seconds() > 24 * 60 * 60:
            break

if __name__ == "__main__":
    main()
