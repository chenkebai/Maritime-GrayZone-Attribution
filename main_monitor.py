from src.models.v_dev_engine import calculate_v_dev
from src.models.geospatial_filter import is_near_infrastructure

def evaluate_gray_zone_risk(vessel_data, cable_coords):
    # 1. Check Speed Anomaly (Stage 2)
    v_score = calculate_v_dev(
        vessel_data['sog'], 
        vessel_data['type_avg_speed'], 
        vessel_data['type_std_dev']
    )
    
    # 2. Check Proximity (Stage 3)
    in_hot_zone, distance = is_near_infrastructure(
        vessel_data['lat'], 
        vessel_data['lon'], 
        cable_coords
    )
    
    # 3. Decision Logic (The Attribution Logic)
    is_suspicious = v_score > 3.0 and in_hot_zone
    
    return {
        "risk_detected": is_suspicious,
        "v_dev_score": round(v_score, 2),
        "distance_deg": round(distance, 4)
    }

if __name__ == "__main__":
    # Mock Scenario: Svalbard Cable
    svalbard_cable = [(15.0, 78.0), (16.0, 78.5), (17.0, 79.0)]
    
    # A ship that is slow AND near the cable
    test_ship = {
        'lat': 78.48, 'lon': 15.95, 'sog': 2.2, 
        'type_avg_speed': 14.5, 'type_std_dev': 1.1
    }
    
    report = evaluate_gray_zone_risk(test_ship, svalbard_cable)
    
    print("\n--- ATTRIBUTION REPORT ---")
    if report['risk_detected']:
        print(f"STATUS: [!] PRIORITY ALPHA - GRAY ZONE ACTIVITY DETECTED")
        print(f"REASON: Speed Anomaly ({report['v_dev_score']}) inside Critical Buffer.")
    else:
        print("STATUS: Low Risk.")