import pandas as pd
from config import *

# Restrict dtypes upfront to avoid memory blowup on 7.6M-row encounters
ENC_DTYPES = {
    "EncounterKey":          "int32",
    "PatientDurableKey":     "int32",
    "PrimaryDiagnosisKey":   "int32",
    "DepartmentKey":         "int32",
    "IsEdVisit":             "bool",
    "IsHospitalAdmission":   "bool",
    "IsInpatientAdmission":  "bool",
}

def load_patients():
    return pd.read_csv(PATIENTS, low_memory=False)

def load_encounters(cols=None, sample_frac=None, random_state=42):
    """
    cols        : list of column names to load; None loads all
    sample_frac : float 0–1; use 0.05 during development, 1.0 for final runs
    """
    df = pd.read_csv(ENCOUNTERS, dtype=ENC_DTYPES,
                     usecols=cols, low_memory=False)
    if sample_frac:
        df = df.sample(frac=sample_frac, random_state=random_state)
    return df

def load_diagnosis():
    return pd.read_csv(DIAGNOSIS, low_memory=False)

def load_departments():
    return pd.read_csv(DEPARTMENTS, low_memory=False)

def load_tiger():
    # GEOID must stay as string to preserve leading zeros in FIPS codes
    return pd.read_csv(TIGER, dtype={"GEOID": str})

def load_social_det(cols=None):
    return pd.read_csv(SOCIAL_DET, usecols=cols, low_memory=False)