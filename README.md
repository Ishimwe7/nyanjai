# Local Air Quality Analytics and Environmental Exposure (PS0)

**Author:** Pacifique (Nyanja) Ishimwe  
**Andrew ID:** Nyanjai  
**Course:** 18-787: Data Analytics (Class of 2027)  
**Date:** February 8th, 2026

---

## 1. Project Objective
This report details a comprehensive six-month analysis (January – June 2023) of Fine Particulate Matter ($PM_{2.5}$) across Los Angeles County. The primary goal is to integrate high-resolution PurpleAir sensor data with socio-economic indicators from the American Community Survey (ACS) to identify "exposure hotspots" and audit environmental justice disparities.

## 2. Technical Methodology

### 2.1 Three-Tier Cleaning Logic
To ensure data integrity, all raw sensor data passed through a modular cleaning pipeline:
* **Tier 1: A/B Channel Agreement**: Discarded rows where internal laser counters disagreed by $>70\%$.
* **Tier 2: Stuck Sensor Audit**: Removed data strings with zero variance in $PM_{2.5}$ or Temperature over a 12-hour window.
* **Tier 3: Barkjohn Correction**: Applied the EPA-standardized correction formula to mitigate high-humidity interference.

### 2.2 Reference Validation (The Pivot)
The sensor network was validated against the **Reseda (AQS ID: 06-037-1201)** regulatory station.
* **Validation Points**: 4,313 Hourly Observations.
* **RMSE Improvement**: **1.44%** (Raw: 61.89 vs. Corrected: 61.00).
* **Decision**: The observed improvement justified the **"pivot"** to using the Corrected Dataset for all subsequent demographic joins.


## 3. Repository Structure
The project is organized into modular scripts to ensure reproducibility:

```text
NYANJAI/
├── data/                    # Raw and processed datasets
├── src/                     # Modular Python Source Code
│   ├── cleaning.py          # 3-tier QC and Barkjohn Logic
│   ├── ingestion.py         # API and CSV data loading
│   ├── analytics.py         # Exposure (X_g) and Statistics
│   └── generate_geocoding.py # Mapping sensors to GEOIDs
├── nyanjai_DA_PS1.ipynb     # Primary Analysis Notebook
├── README.md                # Project Documentation
└── requirements.txt         # Library Dependencies


## 4. Key Findings

* **Geographic Clustering**: Highest $PM_{2.5}$ intensities were found in inland basins like **San Fernando (8.25 μg/m³)** compared to coastal sites like **San Pedro (1.91 μg/m³)**.
* **The Equity Gap**: **Hispanic populations** face a significantly higher average exposure level (**6.68 μg/m³**) compared to other demographic subgroups.
* **Socioeconomic Correlation**: A nearly perfect **negative correlation (-1.00)** was identified between **Minority status and Poverty** within the study block groups.



## 5. Requirements & Installation

The following Python libraries are required to run the analysis:
* **Pandas, Numpy**: Data Wrangling and mathematical operations.
* **Matplotlib, Seaborn**: Data visualization and heatmap generation.
* **TimeZoneFinder, Pytz**: Temporal processing and UTC-to-Local conversion.

**To install all dependencies, run the following command:**

```bash
pip install pandas numpy matplotlib seaborn timezonefinder pytz