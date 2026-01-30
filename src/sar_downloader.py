import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import os

def generate_fused_evidence(vessel_name, sar_img_path, sync_list_path, pipe_zip):
    print(f"[*] Starting Fusion Plot: {vessel_name}")
    
    # 1. Load Data
    df = pd.read_csv(sync_list_path)
    ship_data = df[df['VESSEL_NAME'] == vessel_name]
    pipes = gpd.read_file(f"zip://{pipe_zip}").to_crs(epsg=4326)
    sar_img = Image.open(sar_img_path)
    
    # 2. Reconstruct the Geographic Extent (Must match sar_downloader.py)
    # We find the center point used for the download
    target_hit = ship_data.sort_values('DIST_METERS').iloc[0]
    lat_c, lon_c = target_hit['LAT'], target_hit['LON']
    offset = 0.015 # The same offset used in your fixed downloader
    
    # [Left, Right, Bottom, Top]
    extent = [lon_c - offset, lon_c + offset, lat_c - offset, lat_c + offset]

    # 3. Setup the Plot
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # 4. Display SAR Imagery
    ax.imshow(sar_img, cmap='gray', extent=extent, zorder=1)
    
    # 5. Overlay Pipeline (Red Line)
    pipes.plot(ax=ax, color='#FF3B30', linewidth=3, alpha=0.8, label='Subsea Pipeline', zorder=2)
    
    # 6. Overlay AIS Pings (Cyan Dots)
    ax.scatter(ship_data['LON'], ship_data['LAT'], color='#00FFFF', s=30, 
               edgecolors='white', linewidth=0.5, label='AIS Telemetry', zorder=3)

    # 7. DRAW THE "TARGET BOX"
    # We box out the area where the ship showed the highest radar return
    # This is typically where the AIS cluster is densest
    box_width = 0.003  # Roughly 300 meters
    rect = patches.Rectangle((lon_c - box_width/2, lat_c - box_width/2), 
                             box_width, box_width, linewidth=2, 
                             edgecolor='#FFD60A', facecolor='none', 
                             label='Target ID: MSC DANIT', zorder=4)
    ax.add_patch(rect)

    # 8. Formatting for Academic Submission
    ax.set_title(f"SATELLITE SENSOR FUSION: {vessel_name}\nSentinel-1 SAR + AIS + Infrastructure Overlay", 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel("Longitude (WGS84)")
    ax.set_ylabel("Latitude (WGS84)")
    
    # Zoom in slightly more for the final "Money Shot"
    ax.set_xlim(extent[0] + 0.005, extent[1] - 0.005)
    ax.set_ylim(extent[2] + 0.005, extent[3] - 0.005)
    
    plt.legend(loc='upper right', facecolor='white', framealpha=0.9)
    plt.grid(True, linestyle='--', alpha=0.3)

    # Save the Final Proof
    os.makedirs("output/final_evidence", exist_ok=True)
    save_path = f"output/final_evidence/{vessel_name.replace(' ', '_')}_FUSED_FINAL.png"
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"[!!!] FINAL FUSED EVIDENCE SAVED: {save_path}")

if __name__ == "__main__":
    generate_fused_evidence(
        vessel_name="MSC DANIT",
        sar_img_path="output/sar_evidence/MSC_DANIT_SAR_FIXED.png",
        sync_list_path="data/kinetic_sync_list.csv",
        pipe_zip="data/infrastructure/pc_pipe.zip"
    )