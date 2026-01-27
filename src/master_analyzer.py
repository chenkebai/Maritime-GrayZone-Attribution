import zipfile
import io
import csv
import os
from datetime import datetime, timedelta

# --- SETTINGS ---
ZIP_PATH = 'data/raw_ais/AIS_2024_01_31.zip'
OUTPUT_DIR = 'data'
CABLE_LAT_MIN, CABLE_LAT_MAX = 42.40, 42.50
CABLE_LON_MIN, CABLE_LON_MAX = -71.00, -70.80

SAR_TIMESTAMP = datetime.strptime("2024-01-31 22:43:47", "%Y-%m-%d %H:%M:%S")
SAR_WINDOW = timedelta(minutes=5)

def run_master_analysis():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    
    hits = []
    sar_sync_list = []

    print(f"[*] Streaming analysis of {ZIP_PATH}...")
    print("[*] Filtering for Cable Zone and SAR Synchronization window...")

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
                    
                    # 1. Spatial Filter: Is it near the cable?
                    if CABLE_LAT_MIN <= lat <= CABLE_LAT_MAX and CABLE_LON_MIN <= lon <= CABLE_LON_MAX:
                        hits.append(row)
                        
                        # 2. SAR Sync Filter: Was it there during the satellite pass?
                        # Format: 2024-01-31T22:43:47
                        ts_str = row['BaseDateTime'].replace('T', ' ')
                        vessel_time = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                        
                        if (SAR_TIMESTAMP - SAR_WINDOW) <= vessel_time <= (SAR_TIMESTAMP + SAR_WINDOW):
                            sar_sync_list.append(row)

                    if count % 1000000 == 0:
                        print(f"Scanned {count} million rows...")

        # --- PROCESS HITS FOR LOITERING ---
        if hits:
            # Save raw spatial hits
            with open(f"{OUTPUT_DIR}/jan31_spatial_hits.csv", 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(hits)

            # Save SAR Sync hits
            if sar_sync_list:
                with open(f"{OUTPUT_DIR}/jan31_sar_sync_list.csv", 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(sar_sync_list)

            print(f"\n[!] ANALYSIS COMPLETE")
            print(f"Total rows scanned: {count}")
            print(f"Pings in Cable Zone: {len(hits)}")
            print(f"Vessels active during SAR pass: {len(sar_sync_list)}")
            
            if sar_sync_list:
                print("\n[!] SAR-SYNCED VESSELS (Jan 31 22:43):")
                # Print unique vessels found during the pass
                seen = set()
                for v in sar_sync_list:
                    if v['MMSI'] not in seen:
                        print(f"- {v['VesselName']} (MMSI: {v['MMSI']}) at {v['LAT']}, {v['LON']}")
                        seen.add(v['MMSI'])
        else:
            print("\n[!] No vessels found in the landing zone for Jan 31.")

    except Exception as e:
        print(f"\n[!] Error during master analysis: {e}")

if __name__ == "__main__":
    run_master_analysis()