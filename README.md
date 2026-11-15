# 🌍 AETHERRA — Field Shift

### From Space to Soil: Turning Earth Observations into Agricultural Intelligence

**NASA Space Apps Hackathon | Earth Observation × Agriculture × Machine Learning**

AETHERRA is a NASA-data-driven agricultural climate intelligence prototype designed to make historical vegetation and weather observations more accessible, understandable, and useful for regional exploration.

Our initial case study focuses on **Punjab, India**, where we combine NASA satellite-derived vegetation indices with historical climate measurements to explore environmental patterns and evaluate machine learning estimates of vegetation greenness.

**[GitHub Repository](https://github.com/GursharanSingh31/AETHERRA)** | **Live Demo: [https://aetherra-fieldshift.streamlit.app/]**

---

## 01. The Problem

Agriculture is influenced by changing environmental conditions, including temperature, rainfall, humidity, solar radiation, and vegetation dynamics.

NASA provides extensive Earth observation datasets, but transforming these scientific measurements into interpretable regional insights requires processing, integration, and analysis.

**The challenge:** How can we bridge the gap between Earth observation data and accessible agricultural climate intelligence?

## 02. Our Solution

**AETHERRA — Field Shift** is an interactive Streamlit dashboard that integrates historical NASA climate and vegetation datasets into one accessible analytical workspace.

The prototype allows users to:

- Explore regional climate observations over time.
- Visualize satellite-derived vegetation greenness using NDVI.
- Compare observations across selected districts in Punjab.
- Examine temperature, precipitation, humidity, and solar radiation.
- Review historical machine learning predictions alongside observed values.
- Understand exploratory climate insights through transparent, rule-based explanations.
- Download processed research data.

The goal is to make Earth observation data easier to explore and communicate—not to replace established agricultural forecasting or field-level assessment.

## 03. Study Area

Our initial prototype focuses on four locations in Punjab:

| District | Agricultural context |
|---|---|
| Amritsar | Wheat and paddy cultivation |
| Jalandhar | Regional agricultural landscapes |
| Ludhiana | Agricultural and environmental observation |
| Patiala | Climate and vegetation monitoring |

**Study period:** Historical observations from the 2010–2025 target period.

The application provides wheat and paddy as contextual selections. Its underlying satellite observations are not crop-specific measurements.

## 04. NASA Datasets

### NASA MODIS — MOD13Q1 Version 6.1

MODIS provides satellite-derived vegetation information through the Normalized Difference Vegetation Index (NDVI).

- Product: `MOD13Q1.061`
- Spatial resolution: Approximately 250 meters
- Temporal resolution: 16-day composites
- Data access: NASA AppEEARS
- Primary purpose: Historical vegetation greenness analysis

NDVI measures vegetation greenness using reflected light. Changes in NDVI may indicate vegetation dynamics but cannot independently establish crop yield, disease, or the causes of vegetation change.

### NASA POWER

NASA POWER provides historical meteorological information used in our integrated climate analysis.

| Variable | Application |
|---|---|
| Temperature | Thermal conditions |
| Rainfall | Precipitation patterns |
| Relative humidity | Atmospheric moisture |
| Solar radiation | Available solar energy |

These climate measurements are aggregated to align with the satellite observation periods.

**Official sources:**

- [NASA MODIS Vegetation Indices](https://lpdaac.usgs.gov/products/mod13q1v061/)
- [NASA AppEEARS](https://appeears.earthdatacloud.nasa.gov/)
- [NASA POWER](https://power.larc.nasa.gov/)

## 05. How AETHERRA Works

Our data processing and analytical workflow follows six stages.

**1. Data acquisition**

Collect historical MODIS NDVI observations and NASA POWER climate measurements for the selected Punjab locations.

**2. Quality filtering**

Clean and filter usable MODIS observations, including available pixel reliability information.

**3. Temporal alignment**

Aggregate daily weather measurements into periods aligned with usable MODIS NDVI observations.

**4. Data integration**

Combine vegetation and climate variables into a structured historical dataset.

**5. Machine learning evaluation**

Train a Random Forest regression model and compare its NDVI estimates against a persistence baseline using held-out chronological observations.

**6. Interactive visualization**

Present the processed information through a Streamlit dashboard with interactive charts, regional filters, machine learning evaluation, and explainable insights.

### System architecture

`NASA MODIS + NASA POWER`

↓

`Data Collection and Quality Filtering`

↓

`Temporal Alignment and Dataset Integration`

↓

`Historical Climate and Vegetation Analysis`

↓

`Random Forest Evaluation + Rule-Based Insights`

↓

`AETHERRA Streamlit Dashboard`

## 06. Key Features

### Climate Observatory

Explore historical meteorological measurements, including temperature, rainfall, humidity, and solar radiation, through interactive charts.

### Satellite Vegetation Analysis

Visualize MODIS NDVI observations and examine changes in vegetation greenness over the available historical periods.

### Regional Comparison

Compare the available vegetation observations for different Punjab study locations.

### AI Lab

Explore historical Random Forest predictions alongside observed NDVI values and a simple persistence baseline.

### Explainable Insights

Review transparent, threshold-based interpretations of selected climate and vegetation indicators.

These are exploratory analytical observations, not validated farm-level recommendations.

### Source Data Explorer

Inspect and download processed datasets used in the dashboard.

## 07. Machine Learning Experiment

AETHERRA includes a supervised learning experiment using **Random Forest Regression**.

**Objective:** Estimate the next vegetation observation from historical vegetation and climate-related predictors.

**Evaluation method:** Chronological held-out test data.

**Baseline:** Persistence prediction using the previous NDVI observation.

### Recorded evaluation results

| Metric | Result |
|---|---:|
| Random Forest MAE | 0.0397 |
| Persistence baseline MAE | 0.0407 |
| Random Forest R² | 0.3937 |

The Random Forest achieved a modest improvement in mean absolute error compared with the persistence baseline.

These results demonstrate an initial modeling experiment, not a validated operational forecast. The model requires broader validation, additional testing, and further development before agricultural decision-making applications can be considered.

## 08. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and application logic |
| Pandas | Data cleaning and integration |
| NumPy | Numerical operations |
| Scikit-learn | Random Forest regression and evaluation |
| Plotly | Interactive analytical charts |
| Streamlit | Web dashboard and user interface |
| Joblib | Model serialization |
| Matplotlib | Exploratory data visualization |
| NASA MODIS | Satellite vegetation observations |
| NASA POWER | Historical climate measurements |
| GitHub | Version control and collaboration |
| Streamlit Community Cloud | Web application deployment |

## 09. Project Structure

```text
AETHERRA/
├── .streamlit/
│   └── config.toml
├── app/
│   ├── assets/
│   ├── recommendations.py
│   ├── streamlit_app.py
│   └── styles.css
├── data/
│   └── processed/
│       ├── clean_modis.csv
│       ├── merged_dataset.csv
│       └── model_predictions.csv
├── docs/
├── models/
│   └── ndvi_model.joblib
├── src/
│   ├── clean_modis.py
│   ├── merge_datasets.py
│   ├── preprocess.py
│   └── train_model.py
├── .gitignore
├── README.md
└── requirements.txt
```

The repository also contains supporting scripts and research materials used during development.

## 10. Installation and Local Setup

### Prerequisites

- Python 3.12 or another compatible Python version
- Git
- Internet access for initial dependency installation

### Clone the repository

```bash
git clone https://github.com/GursharanSingh31/AETHERRA.git
cd AETHERRA
```

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Run the application

```bash
python -m streamlit run app/streamlit_app.py
```

The application should open locally at:

`http://localhost:8501`

The dashboard expects `data/processed/merged_dataset.csv`. The saved prediction dataset is used for the AI Lab evaluation view.

## 11. Limitations

AETHERRA is a research and demonstration prototype.

Its current limitations include:

- Historical observations rather than live Earth observation feeds.
- Selected geographic observation points rather than complete district-wide coverage.
- No field-level ground-truth validation.
- No operational crop-yield forecasting.
- No crop-specific disease detection.
- No validated agricultural treatment or irrigation recommendations.
- Limited model evaluation and generalization testing.

The prototype is intended for **educational, exploratory, and research-oriented use**.

## 12. Future Development

Potential extensions include:

- Additional NASA Earth observation products.
- Broader geographic and temporal coverage.
- Seasonal and crop-specific analysis with appropriate validation data.
- More sophisticated time-series models.
- Independent testing across locations and agricultural seasons.
- Agricultural expert collaboration.
- Improved accessibility for local communities.
- Expanded geospatial and interactive mapping capabilities.

These are proposed future directions, not completed features.

## 13. Team and Collaboration

**Project:** AETHERRA — Field Shift

**Event:** NASA Space Apps Hackathon

**Repository:** [GursharanSingh31/AETHERRA](https://github.com/GursharanSingh31/AETHERRA)

**Team members and contributions:**

Gursharan Singh - Data Engineering & AI/ML Lead
Maanya Jaiswal - UI/UX Designer 
Oorjit Gupta - Research, Testing and Documentation

## 14. Acknowledgements and Data Attribution

We acknowledge NASA and the scientific teams responsible for providing publicly accessible Earth observation datasets and services.

This project uses NASA MODIS vegetation products and NASA POWER historical meteorological data.

Visual illustrations used within the interface are decorative and should not be interpreted as actual NASA satellite measurements.

AETHERRA is an independent hackathon prototype and is not an official NASA forecasting or agricultural advisory product.

---

### AETHERRA — FIELD SHIFT

**Observe. Understand. Adapt.**

*Bringing Earth observation data closer to agricultural understanding.*
