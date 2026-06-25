"""Coverage and monitoring-gap EDA tables."""

from __future__ import annotations

from typing import Any

import pandas as pd


MONITORING_DATASET_SLUG = "meteorological-monitoring-network"


def build_data_coverage(lookup: pd.DataFrame) -> pd.DataFrame:
    """Summarize geography-level data coverage from the processed lookup table."""

    coverage = lookup.copy()
    coverage["dataset_count"] = pd.to_numeric(coverage["dataset_count"], errors="coerce")
    coverage["row_count"] = pd.to_numeric(coverage["row_count"], errors="coerce")
    coverage["first_year"] = pd.to_numeric(coverage["first_year"], errors="coerce")
    coverage["last_year"] = pd.to_numeric(coverage["last_year"], errors="coerce")
    coverage["years_observed"] = coverage["last_year"] - coverage["first_year"] + 1
    coverage["coverage_tier"] = coverage.apply(_coverage_tier, axis=1)
    coverage["data_desert_flag"] = coverage.apply(_data_desert_flag, axis=1)

    columns = [
        "geo_code",
        "dataset_count",
        "row_count",
        "first_year",
        "last_year",
        "years_observed",
        "coverage_tier",
        "data_desert_flag",
        "datasets",
    ]
    return coverage[columns].sort_values("geo_code", kind="mergesort").reset_index(drop=True)


def build_monitoring_gap(index: pd.DataFrame, observations: pd.DataFrame) -> pd.DataFrame:
    """Compare adaptation-gap scores with latest monitoring-network coverage."""

    scored = index.copy()
    scored["adaptation_gap_score"] = pd.to_numeric(
        scored["adaptation_gap_score"], errors="coerce"
    )
    scored["climate_pressure_score"] = pd.to_numeric(
        scored["climate_pressure_score"], errors="coerce"
    )
    scored["capacity_score"] = pd.to_numeric(scored["capacity_score"], errors="coerce")

    monitoring = observations[observations["dataset_slug"] == MONITORING_DATASET_SLUG].copy()
    if monitoring.empty:
        latest = pd.DataFrame(columns=["geo_code", "latest_monitoring_year", "monitoring_count"])
    else:
        monitoring["year"] = pd.to_numeric(monitoring["year"], errors="coerce")
        monitoring["value"] = pd.to_numeric(monitoring["value"], errors="coerce")
        latest = (
            monitoring.dropna(subset=["year"])
            .sort_values(["geo_code", "year"], ascending=[True, False], kind="mergesort")
            .drop_duplicates("geo_code", keep="first")
            .rename(columns={"year": "latest_monitoring_year", "value": "monitoring_count"})
        )[["geo_code", "latest_monitoring_year", "monitoring_count"]]

    merged = scored.merge(latest, on="geo_code", how="left")
    merged["monitoring_count"] = merged["monitoring_count"].fillna(0)
    monitoring_median = merged["monitoring_count"].median()
    merged["monitoring_gap_label"] = merged.apply(
        lambda row: _monitoring_gap_label(row, monitoring_median), axis=1
    )
    merged["monitoring_story_flag"] = (
        merged["monitoring_gap_label"] == "high gap + low monitoring"
    )

    columns = [
        "geo_code",
        "adaptation_gap_score",
        "climate_pressure_score",
        "capacity_score",
        "latest_monitoring_year",
        "monitoring_count",
        "monitoring_gap_label",
        "monitoring_story_flag",
    ]
    return merged[columns].sort_values("geo_code", kind="mergesort").reset_index(drop=True)


def _coverage_tier(row: pd.Series) -> str:
    dataset_count = _float_value(row.get("dataset_count"))
    row_count = _float_value(row.get("row_count"))
    if dataset_count >= 8 and row_count >= 500:
        return "broad"
    if dataset_count >= 5:
        return "moderate"
    return "thin"


def _data_desert_flag(row: pd.Series) -> bool:
    dataset_count = _float_value(row.get("dataset_count"))
    row_count = _float_value(row.get("row_count"))
    return dataset_count < 5 or row_count < 100


def _monitoring_gap_label(row: pd.Series, monitoring_median: float) -> str:
    high_gap = _float_value(row.get("adaptation_gap_score")) >= 66
    low_monitoring = _float_value(row.get("monitoring_count")) <= monitoring_median
    if high_gap and low_monitoring:
        return "high gap + low monitoring"
    if high_gap:
        return "high gap + visible monitoring"
    if low_monitoring:
        return "low monitoring"
    return "monitoring less urgent"


def _float_value(value: Any) -> float:
    if value is None or pd.isna(value):
        return 0.0
    return float(value)
