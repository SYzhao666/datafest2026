# DataFest 2026 — Stormont Vail Health

**Analyzing patient journeys to understand how MyChart app engagement
affects emergency utilization and care continuity.**

---

## Research Question

Does MyChart app activation improve patient journey quality —
and does geographic distance compound or moderate this effect?

---

## Key Findings

| Group | ED Rate |
|---|---|
| App User | 0.6% |
| Non-App User | 1.3% |
| App User + Transport Hardship | 2.5% |
| Non-App User + Transport Hardship | 8.2% |
| Near + App User | 0.9% |
| Near + Non-App User | 2.3% |

- MyChart activation is associated with a **54% reduction** in ED visit rate (p < 0.0001)
- Non-app users with transport hardship show ED rates **13× higher** than
  app users without transport issues
- Distance alone does not strongly predict ED utilization —
  app status and transportation hardship are stronger predictors
- The app benefit is strongest for patients living **near SVH** —
  precisely the group most likely to default to the ER for non-urgent care

---

## Recommendation

SVH should prioritize MyChart outreach to patients who are:
1. Living within close proximity to SVH facilities
2. Flagged with transportation hardship in social determinants survey
3. Not yet activated on MyChart

This is a definable, reachable population that stands to benefit most
from digital engagement.

---

## Project Structure

```
datafest/
├── config.py                    # Centralized path configuration
├── requirements.txt             # Python dependencies
├── .gitignore
├── data/
│   ├── raw/                     # Original CSV files (not tracked by git)
│   ├── processed/               # Cleaned outputs used by visualization notebook
│   └── samples/                 # Development subsets
├── notebooks/
│   ├── 00_eda.ipynb             # Exploratory data analysis
│   ├── 01_mychart.ipynb         # Main analysis: app usage vs journey quality
│   ├── 02_distance.ipynb        # Supplementary: geographic distance analysis
│   └── 03_visualizations.ipynb  # All charts for final presentation
├── src/
│   ├── data_loader.py           # CSV loading with dtype optimization
│   ├── distance_utils.py        # Haversine distance + patient geocoding
│   ├── journey_builder.py       # Patient journey construction via DiagnosisValue
│   └── plot_utils.py            # Shared plotting style and save functions
└── outputs/
    ├── figures/                 # Saved charts (PNG + PDF)
    └── tables/                  # Saved result tables
```

---

## Setup

```bash
# Clone the repo
git clone https://github.com/SYzhao666/datafest2026.git
cd datafest2026

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Register Jupyter kernel
python -m ipykernel install --user --name=datafest
```

Place the raw CSV files in `data/raw/` before running any notebooks.

---

## Data

**Source:** Stormont Vail Health (SVH), Topeka, Kansas  
**Period:** January 2022 – December 2025  
**Scale:** 947,685 patients · 7,675,801 encounters

Key files used:

| File | Rows | Description |
|---|---|---|
| encounters.csv | 7,675,801 | All patient-system interactions |
| patients.csv | 947,685 | Patient demographics + MyChart status |
| diagnosis.csv | 1,531,262 | ICD-10 diagnosis codes |
| departments.csv | 11,597 | Department locations and specialties |
| social_determinants.csv | 3,977,901 | SDOH survey responses |
| tigercensuscodes.csv | 2,463 | Census block centroids (Kansas) |

Raw data is not tracked by git due to size and privacy constraints.

---

## Notebook Order

Run notebooks in sequence:

| Notebook | Purpose |
|---|---|
| `00_eda.ipynb` | Data structure, distributions, missing values |
| `01_mychart.ipynb` | Core app usage analysis + transport hardship cross-analysis |
| `02_distance.ipynb` | Geographic distance supplementary analysis |
| `03_visualizations.ipynb` | All 8 presentation charts |

---

## Technical Notes

- Encounters are sampled at **5%** during development for speed;
  set `sample_frac=1.0` for final runs
- Patient journeys are defined by **(PatientDurableKey, DiagnosisValue)** pairs —
  not PrimaryDiagnosisKey, which can change mid-journey due to federal coding updates
- Distance is calculated as straight-line (Haversine) from patient census block centroid
  to SVH main campus (39.0558, -95.6890)
- Patients with `*Unspecified` census blocks (~65%) are excluded from distance analysis

---

## Dependencies

- pandas >= 2.0
- numpy
- matplotlib
- seaborn
- scipy
- jupyter
- ipykernel
