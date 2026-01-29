import csv

PATH = 'data/anomalies_flagged.csv'

print(f"\n{'Vessel Name':<20} | {'MMSI':<10} | {'Type':<5} | {'SOG':<5} | {'Avg':<5} | {'Z-Score'}")
print("-" * 72)

try:
    with open(PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"{row['VesselName']:<20} | {row['MMSI']:<10} | {row['VesselType']:<5} | {row['SOG']:<5} | {row['V_Mean']:<5} | {row['Z_Score']}")
except FileNotFoundError:
    print("Error: anomalies_flagged.csv not found. Run v_dev_engine.py first.")