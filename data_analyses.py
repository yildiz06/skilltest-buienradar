"""
Gebruik de volgende commando's om specifieke vragen te beantwoorden:

Voor vraag 5 (hoogste temperatuur): py data_analyses.py --vraag 5

Voor vraag 6 (gemiddelde temperatuur): py data_analyses.py --vraag 6

Voor vraag 7 (grootste temperatuurverschil): py data_analyses.py --vraag 7

Voor vraag 8 (station in de Noordzee): py data_analyses.py --vraag 8
"""

import sqlite3
import argparse

def highest_temperature_station():
    """Vraag 5: Vindt het station met de hoogste gemeten temperatuur."""
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()

    query = """
    SELECT s.stationname, m.temperature, m.timestamp
    FROM measurements m
    JOIN stations s ON m.stationid = s.stationid
    ORDER BY m.temperature DESC
    LIMIT 1;
    """

    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    if result:
        print("\nVraag 5: Weerstation met de hoogste temperatuur:")
        print(f"Station: {result[0]}")
        print(f"Temperatuur: {result[1]}°C")
        print(f"Tijdstip: {result[2]}")
    else:
        print("Geen data beschikbaar.")

def average_temperature():
    """Vraag 6: Bereken de gemiddelde temperatuur."""
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()

    query = "SELECT AVG(temperature) FROM measurements;"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    if result and result[0] is not None:
        print("\nVraag 6: Gemiddelde temperatuur:")
        print(f"Gemiddelde temperatuur: {round(result[0], 2)}°C")
    else:
        print("Geen data beschikbaar.")

def biggest_temperature_difference():
    """Vraag 7: Vindt het station met het grootste verschil tussen gevoelstemperatuur en daadwerkelijke temperatuur."""
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()

    query = """
    SELECT s.stationname, ABS(m.feeltemperature - m.temperature) AS temp_diff
    FROM measurements m
    JOIN stations s ON m.stationid = s.stationid
    ORDER BY temp_diff DESC
    LIMIT 1;
    """

    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    if result:
        print("\nVraag 7: Grootste verschil tussen gevoelstemperatuur en temperatuur:")
        print(f"Station: {result[0]}")
        print(f"Temperatuurverschil: {round(result[1], 2)}°C")
    else:
        print("Geen data beschikbaar.")

def north_sea_station():
    """🔹 Vraag 8: Zoek het weerstation dat zich in de Noordzee bevindt."""
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()

    query = """
    SELECT stationname, regio
    FROM stations
    WHERE regio LIKE '%North Sea%' OR regio LIKE '%Noordzee%';
    """

    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    if result:
        print("\nVraag 8: Weerstation in de Noordzee:")
        print(f"Station: {result[0]}")
        print(f"Regio: {result[1]}")
    else:
        print("Geen weerstation gevonden in de Noordzee.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Voer data-analyse uit op Buienradar gegevens.")
    parser.add_argument("--vraag", type=int, choices=[5, 6, 7, 8], help="Welke vraag wil je beantwoorden? (5, 6, 7, of 8)")
    
    args = parser.parse_args()

    if args.vraag == 5:
        highest_temperature_station()
    elif args.vraag == 6:
        average_temperature()
    elif args.vraag == 7:
        biggest_temperature_difference()
    elif args.vraag == 8:
        north_sea_station()
    else:
        print("""\nGebruik de volgende commando's om specifieke vragen te beantwoorden:

Voor vraag 5 (hoogste temperatuur):             py data_analysis.py --vraag 5
Voor vraag 6 (gemiddelde temperatuur):          py data_analysis.py --vraag 6
Voor vraag 7 (grootste temperatuurverschil):    py data_analysis.py --vraag 7
Voor vraag 8 (station in de Noordzee):          py data_analysis.py --vraag 8
""")