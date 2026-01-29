import csv
from collections import Counter

INPUT_PATH = 'data/cable_suspects.csv'

# Dictionary for common AIS Vessel Types
SHIP_TYPES = {
    '30': 'Fishing',
    '31': 'Towing',
    '35': 'Military',
    '37': 'Pleasure Craft',
    '52': 'Tug',
    '60': 'Passenger',
    '70': 'Cargo',
    '80': 'Tanker',
    '90': 'Other'
}

print(f"--- Profiling Ships in the Cable Zone ---")

try:
    with open(INPUT_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        vessel_counts = Counter()
        mmsi_list = set()

        for row in reader:
            v_type = row['VesselType']
            vessel_counts[v_type] += 1
            mmsi_list.add(row['MMSI'])

        print(f"\nTotal Unique Vessels: {len(mmsi_list)}")
        print(f"{'Type ID':<10} | {'Count':<8} | {'Description'}")
        print("-" * 40)
        
        # Sort by count
        for v_type, count in vessel_counts.most_common():
            desc = SHIP_TYPES.get(v_type, "Unknown/Specialized")
            print(f"{v_type:<10} | {count:<8} | {desc}")

except Exception as e:
    print(f"Error: {e}")