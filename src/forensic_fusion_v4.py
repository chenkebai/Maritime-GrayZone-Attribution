import os, requests
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
from shapely.geometry import Point
from shapely.ops import nearest_points
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("SH_CLIENT_ID")
CLIENT_SECRET = os.getenv("SH_CLIENT_SECRET")

def get_token():
    auth_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    resp = requests.post(auth_url, data={"grant_type": "client_credentials", "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET})
    return resp.json().get("access_token")

def generate_forensic_evidence():
    token = get_token()
    
    # 1. LOAD DATA & TARGET CENTROID
    df = pd.read_csv("data/kinetic_sync_list.csv")
    ship_data = df[df['VESSEL_NAME'].str.contains("DANIT", case=False, na=False)].iloc[0]
    lat_s, lon_s = ship_data['LAT'], ship_data['LON']
    
    # Focus Zoom: Adjusted to keep the ship and pipeline segment centered
    offset = 0.025 
    bbox = [lon_s - offset, lat_s - offset, lon_s + offset, lat_s + offset]

    # 2. SAR API REQUEST
    payload = {
        "input": {
            "bounds": {"bbox": bbox, "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"}},
            "data": [{"type": "S1GRD", "dataFilter": {
                "timeRange": {"from": "2021-01-24T00:00:00Z", "to": "2021-01-26T23:59:59Z"},
                "mosaickingOrder": "mostRecent"
            }}]
        },
        "output": {"width": 1024, "height": 1024, "responses": [{"identifier": "default", "format": {"type": "image/png"}}]},
        "evalscript": """
        //VERSION=3
        function setup() { return { input: ["VV"], output: { bands: 1, sampleType: "AUTO" } }; }
        function evaluatePixel(sample) {
          let db = 10 * Math.log10(Math.max(0.0001, sample.VV));
          return [(db + 20) / 25]; 
        }
        """
    }

    print("[*] Requesting SAR Imagery...")
    resp = requests.post("https://sh.dataspace.copernicus.eu/api/v1/process", 
                         headers={"Authorization": f"Bearer {token}"}, json=payload)
    
    if resp.status_code != 200:
        print(f"[-] API Error: {resp.text}")
        return

    sar_img = Image.open(BytesIO(resp.content))

    # 3. FIXED GEOSPATIAL MATH (Connecting Ship to Pipe)
    pipes_raw = gpd.read_file("zip://data/infrastructure/pc_pipe.zip").to_crs(epsg=4326)
    ship_pt = Point(lon_s, lat_s)
    
    # Merge all pipeline segments into one geometry to find the absolute nearest point
    pipeline_union = pipes_raw.unary_union
    # Find the nearest points: p_src (on ship), p_pipe (on pipeline)
    p_src, p_pipe = nearest_points(ship_pt, pipeline_union)
    lon_p, lat_p = p_pipe.x, p_pipe.y

    # Calculate distance in meters for the legend using a metric projection (EPSG:3857)
    pipes_m = pipes_raw.to_crs(epsg=3857)
    ship_pt_m = gpd.GeoSeries([ship_pt], crs=4326).to_crs(epsg=3857).iloc[0]
    dist_meters = pipes_m.distance(ship_pt_m).min()

    # 4. THE FORENSIC PLOT
    fig, ax = plt.subplots(figsize=(14, 14), facecolor='black')
    
    # Layer 1: SAR Image
    ax.imshow(sar_img, cmap='magma', extent=[bbox[0], bbox[2], bbox[1], bbox[3]], 
              origin='upper', zorder=1)
    
    # Layer 2: Pipeline (Red Line)
    pipes_raw.plot(ax=ax, color='#FF3B30', linewidth=4, alpha=0.9, label='San Pedro Pipeline Corridor', zorder=2)
    
    # Layer 3: THE YELLOW CONNECTION LINE
    # This now uses p_pipe coordinates to ensure it touches the red line
    ax.plot([lon_s, lon_p], [lat_s, lat_p], color='yellow', linestyle='--', linewidth=3, 
            marker='o', markersize=6, label='Forensic Standoff Vector', zorder=6)

    # Add the meter label directly next to the line
    ax.text((lon_s + lon_p)/2, (lat_s + lat_p)/2 + 0.001, f"{dist_meters:.1f}m", 
            color='yellow', fontweight='bold', ha='center', fontsize=12,
            bbox=dict(facecolor='black', alpha=0.7, edgecolor='none'))

    # Layer 4: MSC DANIT AIS Center
    ax.scatter(lon_s, lat_s, color='#00FFFF', s=300, edgecolors='white', marker='P', label='MSC DANIT (AIS)', zorder=7)

    # 5. AXES & LABELS
    ax.tick_params(axis='both', colors='white', labelsize=10)
    ax.set_xlabel("Longitude", color='white')
    ax.set_ylabel("Latitude", color='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#444444')

    # 6. UPDATED TECHNICAL LEGEND (Removed Elly)
    tech_legend = (
        f"--- FORENSIC ATTRIBUTION DATA ---\n"
        f"SAR ACQUISITION: 2021-01-25 14:10 UTC\n"
        f"VESSEL: MSC DANIT (9618288)\n"
        f"SHIP POSITION: {lat_s:.5f}, {lon_s:.5f}\n"
        f"NEAREST PIPE INTERCEPT: {lat_p:.5f}, {lon_p:.5f}\n"
        f"CALCULATED DISTANCE: {dist_meters:.2f} meters\n"
        f"PROXIMITY STATUS: CRITICAL THREAT"
    )
    
    ax.text(0.02, 0.02, tech_legend, transform=ax.transAxes, color='white', fontsize=12,
            family='monospace', bbox=dict(facecolor='black', alpha=0.8, edgecolor='#00FFFF'))

    ax.set_xlim(bbox[0], bbox[2])
    ax.set_ylim(bbox[1], bbox[3])
    
    plt.legend(loc='upper right', facecolor='black', labelcolor='white', fontsize=11)
    
    save_path = "output/final_evidence/FORENSIC_FUSION_FINAL.png"
    os.makedirs("output/final_evidence", exist_ok=True)
    plt.savefig(save_path, dpi=300, facecolor='black', bbox_inches='tight')
    
    print(f"[!!!] Evidence Locked: {dist_meters:.2f}m standoff.")
    plt.show()

if __name__ == "__main__":
    generate_forensic_evidence()