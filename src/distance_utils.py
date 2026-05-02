import numpy as np
import pandas as pd

def haversine_km(lat1, lon1, lat2, lon2):
    """
    Vectorised Haversine formula.
    Inputs can be scalars, numpy arrays, or pandas Series.
    Returns straight-line distance in kilometres.
    """
    R = 6371  # Earth radius in km
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlam = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlam / 2)**2
    return 2 * R * np.arcsin(np.sqrt(a))

def assign_distance_group(km_series, labels=["Near", "Mid", "Far"]):
    """
    Bin continuous distance into tertiles.
    Tertiles are preferred over fixed thresholds because SVH's
    service area mixes dense urban and sparse rural blocks.
    """
    q33, q66 = km_series.quantile([0.33, 0.66])
    return pd.cut(km_series,
                  bins=[-np.inf, q33, q66, np.inf],
                  labels=labels)

def attach_patient_coords(patients_df, tiger_df):
    """
    Join patient census block to tiger centroid coordinates.
    Patients with '*Unspecified' block codes are dropped here
    because we cannot estimate their distance.
    """
    tiger_clean = tiger_df[["GEOID", "CENTLAT", "CENTLONG"]].copy()
    tiger_clean.columns = ["CensusBlockGroupFipsCode", "pat_lat", "pat_lon"]

    merged = patients_df.merge(tiger_clean,
                               on="CensusBlockGroupFipsCode",
                               how="left")
    n_missing = merged["pat_lat"].isna().sum()
    print(f"[attach_patient_coords] {n_missing} patients dropped "
          f"(no geocode match) out of {len(merged)}")
    return merged.dropna(subset=["pat_lat", "pat_lon"])