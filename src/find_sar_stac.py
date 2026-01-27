import requests

# The modern CDSE STAC V1 Endpoint
URL = "https://stac.dataspace.copernicus.eu/v1/search"

# We want "Ground Range Detected" (GRD) for ship detection
COLLECTION = "SENTINEL-1-GRD" 

# Broadened to cover the entire coast of Massachusetts
BBOX = [-71.5, 41.5, -69.5, 43.5] 
# Search from Jan 1 to Feb 15
DATETIME = "2024-01-01T00:00:00Z/2024-02-15T23:59:59Z"

def find_sar_v1():
    print(f"[*] Querying {COLLECTION} via new V1 API...")
    
    payload = {
        "collections": [COLLECTION],
        "bbox": BBOX,
        "datetime": DATETIME,
        "limit": 50
    }

    try:
        response = requests.post(URL, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        features = data.get('features', [])
        
        if not features:
            print("[!] Still no results. Checking if S1A had an outage...")
            return

        print(f"\n[!] Success! Found {len(features)} SAR passes in January:")
        print(f"{'Date/Time (UTC)':<25} | {'Product ID'}")
        print("-" * 80)
        
        for feat in features:
            dt = feat['properties'].get('datetime', 'N/A')
            pid = feat['id']
            print(f"{dt:<25} | {pid}")
            
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    find_sar_v1