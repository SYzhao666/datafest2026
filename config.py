from pathlib import Path

ROOT         = Path(__file__).parent
DATA_RAW     = ROOT / "data" / "raw"
DATA_PROC    = ROOT / "data" / "processed"
DATA_SAMPLES = ROOT / "data" / "samples"
OUTPUTS_FIG  = ROOT / "outputs" / "figures"
OUTPUTS_TBL  = ROOT / "outputs" / "tables"

# Raw file paths — treat as read-only
ENCOUNTERS   = DATA_RAW / "encounters.csv"
PATIENTS     = DATA_RAW / "patients.csv"
DIAGNOSIS    = DATA_RAW / "diagnosis.csv"
DEPARTMENTS  = DATA_RAW / "departments.csv"
SOCIAL_DET   = DATA_RAW / "social_determinants.csv"
TIGER        = DATA_RAW / "tigercensuscodes.csv"