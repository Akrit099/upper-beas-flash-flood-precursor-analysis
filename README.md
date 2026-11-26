# 🌊 DBSCAN-Based Flash Flood Precursor Analysis in the Upper Beas Basin

**A Multi-Source Environmental Data Clustering Study | 2015–2025**

<p align="center">
  <strong>Upper Beas Basin, Kullu District, Himachal Pradesh, India</strong>
</p>

---

## 📌 Project Overview

Flash floods are a major environmental hazard in mountainous regions, where rainfall, antecedent soil moisture, terrain characteristics, slope, and drainage conditions interact in complex ways.

This project investigates the integration of multi-source environmental datasets with **DBSCAN (Density-Based Spatial Clustering of Applications with Noise)** to identify dense environmental patterns that may be associated with flash-flood precursor conditions.

The study focuses on the Upper Beas Basin in Kullu district, Himachal Pradesh, India, covering the period **2015–2025**.

The project combines geospatial data processing, environmental feature engineering, unsupervised machine learning, historical flood-event comparison, and interactive visualization.

> **Research note:** This is an exploratory environmental clustering study. It is not a validated operational flood forecasting or early-warning system.

---

## 🎯 Research Objectives

1. Aggregate rainfall, soil moisture, terrain, slope, and drainage-related information across the Upper Beas Basin.
2. Develop a spatially and temporally aligned multi-source environmental dataset.
3. Apply DBSCAN to identify dense environmental patterns and noise observations.
4. Evaluate clustering behaviour through parameter sensitivity experiments.
5. Compare detected clusters with available historical flood-event records.
6. Develop an interactive geospatial dashboard for exploring environmental conditions and clustering results.

---

## 🗺️ Study Area

| Attribute | Description |
|---|---|
| Study Region | Upper Beas Basin |
| District | Kullu |
| State | Himachal Pradesh |
| Country | India |
| Study Period | 2015–2025 |
| Approximate Basin Area | 5,657 km² |
| Spatial Grid Cells | 325 |
| Boundary Status | Provisional |

---

## 📡 Data Sources

The research integrates multiple environmental and geospatial datasets.

| Dataset | Source | Application |
|---|---|---|
| CHIRPS Daily Rainfall | UCSB Climate Hazards Center | Daily and antecedent rainfall |
| SMAP Soil Moisture | NASA | Surface and root-zone soil moisture |
| SRTM DEM | USGS | Elevation and slope |
| HydroSHEDS | HydroSHEDS | Watershed and drainage context |
| Historical Flood Records | HiFlo-DAT | Historical event comparison |
| Google Earth Engine | Google | Geospatial data extraction and processing |

Dataset availability, spatial resolution, temporal coverage, and missing observations are considered during preprocessing.

---

## 🧪 Methodology

The project follows a multi-stage environmental data analysis workflow.

### 1. Data Collection

Environmental and geospatial datasets are collected for the Upper Beas Basin for the 2015–2025 study period.

### 2. Spatial Data Preparation

- Selection of a provisional watershed boundary.
- Preparation of 325 spatial grid cells.
- Extraction of geographic coordinates and terrain characteristics.
- Alignment of environmental observations with spatial locations.

### 3. Data Preprocessing

- Date and coordinate alignment.
- Missing-value assessment.
- Duplicate-record checks.
- Rainfall feature transformation.
- Soil-moisture availability handling.
- Temporal calibration and feature scaling.

### 4. Feature Engineering

The model uses environmental features including:

- Daily rainfall.
- Antecedent 3-day rainfall.
- Antecedent 7-day rainfall.
- Antecedent 15-day rainfall.
- Previous-day surface soil moisture.
- Previous-day root-zone soil moisture.
- Spatial coordinates.

Elevation and slope are also used for terrain analysis and interpretation.

### 5. DBSCAN Clustering

DBSCAN is applied to identify dense groups of environmental observations and classify sparse observations as noise.

The baseline configuration is:

| Parameter | Value |
|---|---:|
| Environmental Feature Weight | 0.3 |
| Epsilon (eps) | 2.0 |
| Minimum Samples | 4 |

Additional configurations are evaluated through parameter sensitivity experiments.

### 6. Historical Event Comparison

Detected environmental clusters are compared with available dated and geolocated historical flood records.

Historical event labels are kept separate from unsupervised model inputs.

### 7. Visualization

The project includes static research visualizations and an interactive Streamlit dashboard for exploring environmental conditions, spatial patterns, and historical records.

---

## 📊 Dataset Summary

| Component | Result |
|---|---:|
| Study Period | 2015–2025 |
| Daily CHIRPS Observations | 4,018 |
| Spatial Grid Cells | 325 |
| Integrated Dataset Records | 1,305,850 |
| Model Dataset Records | 1,276,275 |
| Coordinate-Bearing Historical Records | 128 |
| Date-Matched Historical Events | 13 |

**Data availability note:** SMAP soil-moisture observations are available from April 2015 onward. Missing observations are not treated as zero.

---

## 📈 Preliminary Experimental Results

The baseline DBSCAN configuration produced the following full-period average results:

| Metric | Result |
|---|---:|
| Mean Number of Clusters | 10.19 |
| Mean Noise Percentage | 4.94% |
| Mean Clustered Coverage | 95.06% |
| Mean Largest Cluster Size | 153.87 |

### Historical Event Comparison

The baseline configuration clustered all 13 date-matched historical event cells.

However, randomly selected control locations also showed a high clustering rate.

| Configuration | Event Detection | Control Detection | McNemar p-value |
|---|---:|---:|---:|
| Baseline: eps 2.0, min_samples 4 | 100% | 92.31% | 1.000 |
| Selective: eps 1.5, min_samples 6 | 69.23% | 46.15% | 0.375 |
| Strict: eps 1.5, min_samples 10 | 0% | 0% | 1.000 |

These results do not demonstrate statistically significant discrimination between historical event locations and controls.

The results should therefore be interpreted as exploratory environmental clustering patterns rather than predictive flood-risk indicators.

---

## 🖥️ Interactive Dashboard

The project includes a Streamlit-based research dashboard with the following modules:

- Command Center.
- Interactive Earth Explorer.
- Environmental Intelligence.
- DBSCAN Explorer.
- Historical Validation.
- Research and Methodology.

The Interactive Earth module includes satellite imagery, basin boundary visualization, research grid locations, historical event markers, and environmental layer exploration.

### 📸 Project Screenshots

#### 1. Historical Validation

![DBSCAN Historical Event and Matched-Control Comparison](visualizations/screenshots/Screenshot%202026-11-26%20120309.png)

#### 2. Interactive Earth — Local View

![Interactive Earth Local View](visualizations/screenshots/Screenshot%202026-11-26%20120216.png)

#### 3. Upper Beas Basin — Research Grid

![Upper Beas Basin Research Grid](visualizations/screenshots/Screenshot%202026-11-26%20120013.png)

### Run the Dashboard Locally

#### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/upper-beas-flash-flood-precursor-analysis.git
```

#### 2. Navigate to the project directory

```bash
cd upper-beas-flash-flood-precursor-analysis
```

#### 3. Create and activate a Python environment

```bash
conda create -n upperbeas python=3.11
conda activate upperbeas
```

#### 4. Install dependencies

```bash
pip install -r requirements.txt
```

#### 5. Launch the dashboard

```bash
streamlit run streamlit_app/app.py
```

The dashboard will open in your browser. If it does not open automatically, use the local URL displayed in the terminal, usually `http://localhost:8501`.

---

## 📓 Research Notebook

The main analytical notebook is:

```text
notebooks/Upper_Beas_Flood_Research.ipynb
```

An additional original notebook is retained as:

```text
notebooks/raw.ipynb
```

The main notebook uses the prepared datasets in `data/processed/`. Before running it, extract the integrated dataset ZIP archive into the same `data/processed/` folder so that the uncompressed CSV is available:

```text
data/processed/integrated_environmental_dataset_2015_2025.csv
```

The notebook also uses the other processed CSV files stored in that folder. The notebook is an analysis workflow based on prepared inputs; it does not automatically recreate every upstream data-acquisition and preparation step.

---

## 📁 Repository Structure

```text
upper-beas-flash-flood-precursor-analysis/
│
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
│
├── data/
│   └── processed/
│       ├── integrated_environmental_dataset_2015_2025.zip
│       ├── grid_master_325.csv
│       ├── historical_flood_events_final.csv
│       ├── historical_events_grid_matched.csv
│       └── spatially_matched_event_control_results.csv
│
├── notebooks/
│   ├── Upper_Beas_Flood_Research.ipynb
│   └── raw.ipynb
│
├── src/
│   ├── preprocessing/
│   ├── feature_engineering/
│   ├── clustering/
│   └── validation/
│
├── streamlit_app/
│   ├── app.py
│   └── upper_beas_interactive_map.html
│
└── visualizations/
    ├── screenshots/
    │   ├── Screenshot 2026-11-26 120013.png
    │   ├── Screenshot 2026-11-26 120216.png
    │   └── Screenshot 2026-11-26 120309.png
    ├── 01_upper_beas_study_area_map.png
    ├── 02_upper_beas_elevation_map.png
    ├── 03_upper_beas_slope_map.png
    ├── 04_upper_beas_rainfall_2015_09_22.png
    ├── 05_upper_beas_dbscan_clusters_2015_09_22.png
    ├── 06_dbscan_yearly_configuration_comparison.png
    └── 07_dbscan_event_control_comparison.png
```

---

## 🛠️ Technologies Used

- **Programming:** Python
- **Data Processing:** Pandas, NumPy
- **Machine Learning:** Scikit-learn, DBSCAN
- **Geospatial Analysis:** GeoPandas, Folium, Geemap
- **Remote Sensing:** Google Earth Engine
- **Visualization:** Matplotlib, Plotly
- **Dashboard:** Streamlit
- **Development Environment:** Jupyter Notebook, Anaconda

---

## ⚠️ Limitations

- The provisional study boundary requires further hydrological verification.
- The number of date-matched historical flood events is limited.
- SMAP soil-moisture observations have coarser spatial resolution than the research grid.
- Historical event records contain incomplete dates and varying location accuracy.
- DBSCAN results are sensitive to parameter selection and feature scaling.
- High clustering coverage does not necessarily indicate flood-related discrimination.
- The current research does not establish operational flood forecasting capability.

---

## 🚀 Future Scope

- Improve historical flood-event inventory and validation coverage.
- Incorporate additional hydrological and drainage characteristics.
- Evaluate alternative clustering algorithms such as OPTICS and HDBSCAN.
- Investigate physically meaningful spatial-temporal distance metrics.
- Improve settlement-level geospatial interpretation.
- Extend validation using independent event records.
- Explore real-time environmental monitoring as a future research direction.

---

## 👨‍💻 Project Information

**Project Title:** DBSCAN-Based Clustering of Multi-Source Flash Flood Precursor Data in Hilly Regions: A Preliminary Study of the Upper Beas Basin, Kullu District, Himachal Pradesh, India.

**Research Domain:** Geospatial Data Science | Environmental Analytics | Unsupervised Machine Learning | Hydrology

**Study Period:** 2015–2025

**Institution:** Lovely Professional University

---

## 📜 License

The project code is provided under the MIT License. Third-party datasets are subject to their respective providers' terms, licenses, and redistribution conditions. Refer to the `LICENSE` file and the original dataset providers before reusing or redistributing data.

---

## ⭐ Acknowledgements

We acknowledge the providers of CHIRPS, NASA SMAP, SRTM, HydroSHEDS, HiFlo-DAT, Google Earth Engine, and the open-source Python ecosystem for supporting this research.

---

<p align="center">
  <strong>Upper Beas Basin | Environmental Research | 2015–2025</strong>
</p>
