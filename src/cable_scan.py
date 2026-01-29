import zipfile
import csv
import io

ZIP_PATH = 'data/raw_ais/AIS_2024_01_19.zip'
OUTPUT_PATH = 'data/cable_suspects.csv'

# Hibernia Atlantic Landing Zone (Lynn, MA)
# We define a "Bounding Box" around the cable landing

"""
The landing site at Lynn, MA (Zone 19) was selected due to its role as a primary transatlantic data artery.
2. Coordinate Derivation: The bounding box ($[42.40, 42.50], [-71.00, -70.80]$) centers on the landing station coordinates. This area encompasses the "Transition Zone" where the cable moves from the deep-sea armored state to the terrestrial landing.
3. Seasonal Context: January was selected to test detection efficacy during high sea-state conditions, testing the hypothesis that gray-zone actors use winter weather as environmental "noise" to mask loitering activity.
4. Analytical Objective: To identify "Type 31" (Towing/Tug) vessels—as seen in the GULF DAWN sample—operating at speeds below the fleet mean ($V_{avg}$) within the security perimeter.
"""

LAT_MIN, LAT_MAX = 42.40, 42.50
LON_MIN, LON_MAX = -71.00, -70.80

hits = []

print("Starting scan of 5+ million rows. This may take 2-3 minutes...")

try:
    with zipfile.ZipFile(ZIP_PATH, 'r') as z:
        csv_name = z.namelist()[0]
        with z.open(csv_name) as f:
            wrapper = io.TextIOWrapper(f, encoding='utf-8')
            reader = csv.DictReader(wrapper)
            
            headers = reader.fieldnames
            count = 0
            
            for row in reader:
                count += 1
                lat = float(row['LAT'])
                lon = float(row['LON'])
                
                # Check if the ship is in our "Cable Hot Zone"
                if LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX:
                    hits.append(row)
                
                if count % 1000000 == 0:
                    print(f"Scanned {count} rows...")

    # Save the results
    if hits:
        with open(OUTPUT_PATH, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(hits)
        print(f"\n[!] Success! Found {len(hits)} pings near the cable landing.")
        print(f"Results saved to: {OUTPUT_PATH}")
    else:
        print("\nNo ships found in the landing zone for this day.")

except Exception as e:
    print(f"Error during scan: {e}")