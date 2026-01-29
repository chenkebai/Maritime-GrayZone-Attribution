import csv
import statistics
from collections import defaultdict

INPUT_PATH = 'data/cable_suspects.csv'
OUTPUT_PATH = 'data/anomalies_flagged.csv'

def calculate_v_dev():
    vessels = defaultdict(list)
    
    # 1. Group SOG by Vessel Type to find "Normal" behavior
    type_speeds = defaultdict(list)
    
    with open(INPUT_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)
        for row in data:
            sog = float(row['SOG'])
            v_type = row['VesselType']
            type_speeds[v_type].append(sog)
            vessels[row['MMSI']].append(row)

    # 2. Calculate Mean and StdDev for each type
    stats_map = {}
    for v_type, speeds in type_speeds.items():
        if len(speeds) > 1:
            stats_map[v_type] = {
                'mean': statistics.mean(speeds),
                'stdev': statistics.stdev(speeds)
            }
        else:
            stats_map[v_type] = {'mean': speeds[0], 'stdev': 0}

    # 3. Calculate Z-Score (V_dev) for each ping
    # Formula: Z = (SOG - Mean) / StDev
    anomalies = []
    for row in data:
        v_type = row['VesselType']
        sog = float(row['SOG'])
        mean = stats_map[v_type]['mean']
        stdev = stats_map[v_type]['stdev']
        
        # Avoid division by zero
        z_score = (sog - mean) / stdev if stdev > 0 else 0
        
        # We look for NEGATIVE Z-scores (meaning slower than average)
        # Specifically Z < -1.5 is a "Strong Loitering Signal"
        """In this framework, $V_{dev}$ (Velocity Deviation) serves as the primary kinematic indicator of loitering. 
            By selecting pings with a Z-score of less than -1.5, we filter for vessels operating at the bottom 6% of their peer-group's recorded speed. 
            This isolates vessels that are likely stationary or engaged in subsea operations, rather than those simply transitioning through the corridor."""
        if z_score < -1.5:
            row['Z_Score'] = round(z_score, 2)
            row['V_Mean'] = round(mean, 2)
            anomalies.append(row)

    # 4. Save High-Interest Anomalies
    if anomalies:
        headers = list(data[0].keys()) + ['Z_Score', 'V_Mean']
        with open(OUTPUT_PATH, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(anomalies)
        print(f"[!] Analysis Complete: Found {len(anomalies)} anomalous slow-speed pings.")
        print(f"Results saved to {OUTPUT_PATH}")
    else:
        print("No significant speed deviations found.")

if __name__ == "__main__":
    calculate_v_dev()