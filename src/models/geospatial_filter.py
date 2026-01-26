from shapely.geometry import Point, LineString
import geopandas as gpd

def is_near_infrastructure(vessel_lat, vessel_lon, cable_coords, buffer_distance=0.1):
    """
    Stage 3: Determines if a vessel is within the 'Hot Zone'.
    buffer_distance: 0.1 decimal degrees is roughly 10-11km.
    """
    # 1. Create the Cable line
    cable_line = LineString(cable_coords)
    
    # 2. Create the Vessel point
    vessel_point = Point(vessel_lon, vessel_lat)
    
    # 3. Calculate distance
    distance = vessel_point.distance(cable_line)
    
    is_threat = distance <= buffer_distance
    return is_threat, distance

if __name__ == "__main__":
    # Real-world target: Svalbard Undersea Cable (Approx coordinates)
    # Line from Longyearbyen towards mainland Norway
    svalbard_cable = [(15.0, 78.0), (16.0, 78.5), (17.0, 79.0)]
    
    # TEST SCENARIO: A ship loitering at 78.48 N, 15.95 E
    ship_lat, ship_lon = 78.48, 15.95
    
    in_zone, dist = is_near_infrastructure(ship_lat, ship_lon, svalbard_cable)
    
    print(f"\n--- GEOSPATIAL ANALYSIS ---")
    print(f"Vessel Location: {ship_lat}, {ship_lon}")
    print(f"Distance to Cable: {dist:.4f} degrees")
    print(f"In 'Hot Zone' (Buffer 0.1): {in_zone}")
    print("="*27 + "\n")