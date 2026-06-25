"""Country-level driver decomposition for EDA."""

from __future__ import annotations

from typing import Any

import pandas as pd


def build_country_drivers(index: pd.DataFrame) -> pd.DataFrame:
    """Create country-level labels that explain the adaptation-gap score."""

    drivers = index.copy()
    for column in (
        "adaptation_gap_score",
        "climate_pressure_score",
        "capacity_score",
        "included_indicator_count",
    ):
        if column in drivers:
            drivers[column] = pd.to_numeric(drivers[column], errors="coerce")

    drivers["pressure_capacity_difference"] = (
        drivers["climate_pressure_score"] - drivers["capacity_score"]
    )
    drivers["adaptation_gap_rank"] = (
        drivers["adaptation_gap_score"].rank(method="min", ascending=False).astype("Int64")
    )
    drivers["driver_label"] = drivers.apply(_driver_label, axis=1)
    drivers["evidence_density_label"] = drivers["included_indicator_count"].apply(
        _evidence_density_label
    )

    columns = [
        "geo_code",
        "adaptation_gap_rank",
        "adaptation_gap_score",
        "climate_pressure_score",
        "capacity_score",
        "pressure_capacity_difference",
        "driver_label",
        "included_indicator_count",
        "evidence_density_label",
        "missingness_flag",
    ]
    return (
        drivers[columns]
        .sort_values(["adaptation_gap_rank", "geo_code"], kind="mergesort")
        .reset_index(drop=True)
    )


def _driver_label(row: pd.Series) -> str:
    if str(row.get("score_status", "")).lower() != "scored":
        return "insufficient data"

    gap = _float_value(row.get("adaptation_gap_score"))
    pressure = _float_value(row.get("climate_pressure_score"))
    capacity = _float_value(row.get("capacity_score"))
    if pressure >= 66 and capacity <= 33:
        return "high pressure + low visible capacity"
    if pressure >= 66:
        return "high pressure"
    if capacity <= 33:
        return "low visible capacity"
    if gap >= 66:
        return "elevated gap"
    if gap <= 33:
        return "lower relative gap"
    return "mixed signals"


def _evidence_density_label(value: Any) -> str:
    count = _float_value(value)
    if count >= 8:
        return "broad indicator evidence"
    if count >= 5:
        return "moderate indicator evidence"
    return "thin indicator evidence"


def _float_value(value: Any) -> float:
    if value is None or pd.isna(value):
        return 0.0
    return float(value)
