import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

conn = sqlite3.connect("weather.db")
cursor = conn.cursor()

query5 = """
SELECT s.stationname, m.temperature
FROM measurements m
JOIN stations s ON m.stationid = s.stationid
ORDER BY m.temperature DESC
LIMIT 1;
"""
cursor.execute(query5)
result5 = cursor.fetchone()
if result5:
    station_name, highest_temp = result5
    plt.figure(figsize=(15, 2))
    plt.barh(station_name, highest_temp, color="red")
    plt.xlabel("Temperatuur (°C)")
    plt.title(f"Hoogste temperatuur gemeten: {highest_temp}°C bij {station_name}")
    plt.show(block=True)

query6 = "SELECT AVG(temperature) FROM measurements;"
cursor.execute(query6)
result6 = cursor.fetchone()
if result6:
    avg_temp = result6[0]
    plt.figure(figsize=(20, 2))
    plt.bar(["Gemiddelde Temp"], [avg_temp], color="blue")
    plt.ylabel("Temperatuur (°C)")
    plt.title(f"Gemiddelde temperatuur: {round(avg_temp, 2)}°C")
    plt.show(block=True)

query7 = """
SELECT s.stationname, ABS(m.feeltemperature - m.temperature) AS temp_diff
FROM measurements m
JOIN stations s ON m.stationid = s.stationid
ORDER BY temp_diff DESC
LIMIT 1;
"""
cursor.execute(query7)
result7 = cursor.fetchone()
if result7:
    station_name, temp_diff = result7
    plt.figure(figsize=(10, 2))
    plt.barh(station_name, temp_diff, color="purple")
    plt.xlabel("Temperatuurverschil (°C)")
    plt.title(f"Grootste verschil: {temp_diff}°C bij {station_name}")
    plt.show(block=True)

query8 = """
SELECT stationname FROM stations WHERE regio LIKE '%Noordzee%' OR regio LIKE '%North Sea%';
"""
cursor.execute(query8)
result8 = cursor.fetchall()
if result8:
    station_names = [row[0] for row in result8]
    plt.figure(figsize=(10, 2))
    plt.barh(station_names, [1] * len(station_names), color="cyan")
    plt.xlabel("Noordzee Stations")
    plt.title("Weerstations in de Noordzee")
    plt.show(block=True)

conn.close()