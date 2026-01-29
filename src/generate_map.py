import csv

INPUT_PATH = 'data/anomalies_flagged.csv'
OUTPUT_PATH = 'data/cable_anomalies.kml'

def create_kml():
    kml_header = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <name>Maritime Gray-Zone Anomalies</name>
    <description>Vessels flagged for loitering near Lynn, MA Cable Landing</description>
"""
    kml_footer = """</Document>
</kml>"""

    placemarks = ""
    
    try:
        with open(INPUT_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['VesselName']
                lat = row['LAT']
                lon = row['LON']
                mmsi = row['MMSI']
                z = row['Z_Score']
                
                placemarks += f"""
    <Placemark>
        <name>{name}</name>
        <description>MMSI: {mmsi} | Z-Score: {z} | Status: {row['Status']}</description>
        <Point>
            <coordinates>{lon},{lat},0</coordinates>
        </Point>
    </Placemark>"""
        
        with open(OUTPUT_PATH, 'w') as f:
            f.write(kml_header + placemarks + kml_footer)
            
        print(f"[!] KML file generated: {OUTPUT_PATH}")
        print("You can now drag this file into Google Earth (Web or Desktop) to see the locations.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_kml()