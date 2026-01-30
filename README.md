# Maritime Gray-Zone Attribution Framework
### Minimizing Attribution Delay via AIS-SAR Data Fusion

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## 🎯 Research Objective
To minimize **Attribution Delay** in maritime gray-zone warfare. This project establishes a forensic "truth-source" by fusing **AIS (Signal)** and **SAR (Index)** data, aligning with the **NSS 2025** priorities for Critical Undersea Infrastructure (CUI) resilience.

## 🔬 Core Hypothesis (H1)
Automated detection of **Functional Indices**—specifically the **Kinetic Vector-Crossing** (Velocity Deviation $V_{dev}$ > 5.0 knots near CUI)—can identify subsea infrastructure strikes in real-time, bypassing the "Plausible Deniability" typical of gray-zone aggression.



## 🛠️ Tech Stack & Methodology
- **Logic:** Based on Jervis (1970) Signaling Theory & Gartzke (2015) Attribution Logic.
- **Engines:** - `kinetic_pipeline.py`: Implements $V_{dev}$ anomaly detection and Z-Score filtering.
    - `forensic_engine.py`: Performs SAR-AIS geospatial fusion and Euclidean Intercept calculations.
- **Geospatial:** GeoPandas, Shapely, PyProj (EPSG:3857 metric projection).
- **Data:** Sentinel-1 GRD (C-Band SAR), Terrestrial/Satellite AIS.

## 📊 Forensic Case Study: The San Pedro Bay Incident
The framework provides definitive attribution by generating a "Forensic Handshake" between electronic telemetry and physical radar returns.



### Key Metrics captured:
- **Detection Trigger:** Velocity anomaly detected ($Z > 4.0$).
- **Calculated Standoff:** 704.2m (accounting for ship catenary and 366m hull length).
- **Verification:** SAR backscatter confirmed the physical presence of a high-RCS vessel at the pipeline intercept coordinates during the AIS "dark" period.

## 📂 Repository Structure
- `/src`: Core attribution and fusion engines.
- `/utils`: API wrappers for Copernicus Data Space (STAC).
- `/docs`: Research paper and theory memos.
- `/data`: Sample infrastructure shapefiles (restricted/anonymized).

## 🚀 Getting Started
1. Clone the repository.
2. Configure `.env` with Sentinel Hub credentials.
3. Run `python src/forensic_engine.py` to generate the attribution visualization.

## 📜 License
Distributed under the **Apache License 2.0**. See `LICENSE` for more information.
