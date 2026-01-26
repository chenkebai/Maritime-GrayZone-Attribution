import numpy as np

def calculate_v_dev(observed_sog, baseline_mu, baseline_sigma):
    """
    Implements Stage 2: V_dev = |Observed - Mean| / Std_Dev
    """
    if baseline_sigma <= 0:
        return 0
    return abs(observed_sog - baseline_mu) / baseline_sigma

# --- THIS IS THE PART THAT TRIGGER THE OUTPUT ---
if __name__ == "__main__":
    # Test Data
    cargo_mu = 15.0
    cargo_sigma = 1.2
    current_sog = 2.5 
    
    score = calculate_v_dev(current_sog, cargo_mu, cargo_sigma)
    
    print("\n" + "="*30)
    print("MARITIME GRAY-ZONE MONITOR")
    print("="*30)
    print(f"Observed Speed: {current_sog} knots")
    print(f"V_dev Anomaly Score: {score:.2f}")

    if score > 3.0:
        print("RESULT: [!] HIGH RISK ANOMALY DETECTED")
    else:
        print("RESULT: Normal Traffic.")
    print("="*30 + "\n")