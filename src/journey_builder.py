import pandas as pd

def build_journeys(enc_df, diag_df):
    """
    Construct one row per (patient, DiagnosisValue) journey.

    Key design decision: we group by DiagnosisValue — NOT PrimaryDiagnosisKey —
    because federal code updates can change a patient's DiagnosisKey mid-journey
    while DiagnosisValue stays stable (see Read Me, diagnosis section).

    Required columns in enc_df:
        EncounterKey, PatientDurableKey, PrimaryDiagnosisKey,
        Date, IsEdVisit, IsHospitalAdmission
    Required columns in diag_df:
        DiagnosisKey, DiagnosisValue, GroupName
    """
    df = enc_df.merge(
        diag_df[["DiagnosisKey", "DiagnosisValue", "GroupName"]],
        left_on="PrimaryDiagnosisKey",
        right_on="DiagnosisKey",
        how="left"
    )
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(["PatientDurableKey", "DiagnosisValue", "Date"])

    journey_stats = df.groupby(
        ["PatientDurableKey", "DiagnosisValue"]
    ).agg(
        n_encounters    = ("EncounterKey",       "count"),
        first_visit     = ("Date",               "min"),
        last_visit      = ("Date",               "max"),
        ed_visits       = ("IsEdVisit",          "sum"),
        hosp_admits     = ("IsHospitalAdmission","sum"),
        diagnosis_group = ("GroupName",          "first"),
    ).reset_index()

    # Span of the journey in calendar days
    journey_stats["journey_days"] = (
        journey_stats["last_visit"] - journey_stats["first_visit"]
    ).dt.days

    # Proportion of encounters that were emergency visits
    journey_stats["ed_rate"] = (
        journey_stats["ed_visits"] / journey_stats["n_encounters"]
    )

    # Average gap between consecutive encounters (days) — proxy for follow-up regularity
    gaps = (
        df.groupby(["PatientDurableKey", "DiagnosisValue"])["Date"]
        .apply(lambda x: x.sort_values().diff().dt.days.mean())
        .reset_index(name="avg_gap_days")
    )
    journey_stats = journey_stats.merge(gaps, on=["PatientDurableKey", "DiagnosisValue"])

    return journey_stats


def filter_meaningful_journeys(journey_df, min_encounters=2):
    """
    Drop single-encounter journeys for the distance and app analyses.
    A one-visit journey has no follow-up pattern to measure.
    """
    return journey_df[journey_df["n_encounters"] >= min_encounters].copy()