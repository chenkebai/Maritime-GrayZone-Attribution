import pandas as pd
import geopandas as gpd
import zipfile
import csv
import io
import pyproj
from shapely.geometry import Point
from shapely.ops import transform
import os

class MaritimeForensicPipeline:
    def __init__(self, pipe_zip, cable_zip):
        print("[*] Initializing Kinetic Infrastructure Engine...")
        self.pipes = gpd.read_file(f"zip://{pipe_zip}").to_crs(epsg=26911)
        self.cables = gpd.read_file(f"zip://{cable_zip}").to_crs(epsg=26911)
        print(f"[+] Infrastructure Loaded. Ready for Kinetic Analysis.")

    def analyze_ais_stream(self, ais_zip, distance_threshold_m=3000, speed_limit=5.0):
        anomalies = []
        # Expanded BBOX to catch the MSC DANIT's approach
        BBOX = [-118.4, 33.4, -117.7, 33.9] 
        
        project = pyproj.Transformer.from_crs("epsg:4326", "epsg:26911", always_xy=True).transform

        print(f"[*] Opening AIS Stream: {ais_zip}")
        with zipfile.ZipFile(ais_zip, 'r') as z:
            csv_name = [n for n in z.namelist() if n.endswith('.csv')][0]
            with z.open(csv_name) as f:
                reader = csv.DictReader(io.TextIOWrapper(f, encoding='utf-8'))
                
                for i, row in enumerate(reader):
                    try:
                        v_lat, v_lon = float(row['LAT']), float(row['LON'])

                        # 1. BBOX Filter
                        if (BBOX[1] <= v_lat <= BBOX[3]) and (BBOX[0] <= v_lon <= BBOX[2]):
                            v_speed = float(row.get('SOG', 0))
                            
                            # 2. KINETIC SPEED FILTER (Capturing 0-5 knots)
                            if v_speed <= speed_limit:
                                v_point_meters = transform(project, Point(v_lon, v_lat))
                                min_dist_pipe = self.pipes.distance(v_point_meters).min()
                                
                                # 3. EXPANDED PROXIMITY FILTER
                                if min_dist_pipe <= distance_threshold_m:
                                    anomalies.append({
                                        'VESSEL_NAME': row.get('VesselName', row['MMSI']),
                                        'MMSI': row['MMSI'],
                                        'LAT': v_lat, 'LON': v_lon,
                                        'TIMESTAMP': row['BaseDateTime'],
                                        'SPEED': v_speed,
                                        'DIST_METERS': round(min_dist_pipe, 2)
                                    })
                    except: continue
                    
                    if i % 1000000 == 0:
                        print(f"    ...scanned {i//1000000}M records (Hits: {len(anomalies)})")
        return anomalies

# Update these lines at the bottom of src/pipeline_v3_kinetic.py
if __name__ == "__main__":
    engine = MaritimeForensicPipeline(
        pipe_zip="data/infrastructure/pc_pipe.zip",
        cable_zip="data/infrastructure/SubmarineCable.zip" # Updated name
    )
    
    # Run analysis with Kinetic Parameters
    results = engine.analyze_ais_stream("data/raw_ais/AIS_2021_01_25.zip")
    
    if results:
        df = pd.DataFrame(results)
        df.to_csv("data/kinetic_sync_list.csv", index=False)
        print(f"\n[!] SUCCESS: Found {len(df)} kinetic proximity events.")
        
        # SEARCH FOR THE TARGET
        # MSC DANIT MMSI is 371716000
        target = df[(df['VESSEL_NAME'].str.contains("DANIT", na=False)) | (df['MMSI'] == "371716000")]
        
        if not target.empty:
            print(f"\n[!!!] TARGET IDENTIFIED: MSC DANIT")
            print(target[['TIMESTAMP', 'SPEED', 'DIST_METERS']].head(10))
        else:
            print("\n[?] MSC DANIT not found. Check if the speed or distance needs further adjustment.")
    else:
        print("[-] No events found with current parameters.")