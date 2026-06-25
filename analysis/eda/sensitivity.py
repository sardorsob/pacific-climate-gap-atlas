"""Simple rank-sensitivity checks for the draft Adaptation Gap Index."""

from __future__ import annotations

import pandas as pd


def build_weight_sensitivity(index: pd.DataFrame) -> pd.DataFrame:
    """Compare baseline ranks with pressure-heavy and capacity-heavy score variants."""

    scores = index.copy()
    for column in ("adaptation_gap_score", "climate_pressure_score", "capacity_score"):
        scores[column] = pd.to_numeric(scores[column], errors="coerce")

    scores["baseline_rank"] = _rank_desc(scores["adaptation_gap_score"])
    scores["pressure_heavy_score"] = (
        (0.7 * scores["climate_pressure_score"]) - (0.3 * scores["capacity_score"])
    )
    scores["capacity_heavy_score"] = (
        (0.3 * scores["climate_pressure_score"]) - (0.7 * scores["capacity_score"])
    )
    scores["pressure_heavy_rank"] = _rank_desc(scores["pressure_heavy_score"])
    scores["capacity_heavy_rank"] = _rank_desc(scores["capacity_heavy_score"])

    rank_columns = ["baseline_rank", "pressure_heavy_rank", "capacity_heavy_rank"]
    scores["rank_range"] = scores[rank_columns].max(axis=1) - scores[rank_columns].min(axis=1)
    scores["robustness_label"] = scores["rank_range"].apply(_robustness_label)

    columns = [
        "geo_code",
        "adaptation_gap_score",
        "baseline_rank",
        "pressure_heavy_score",
        "pressure_heavy_rank",
        "capacity_heavy_score",
        "capacity_heavy_rank",
        "rank_range",
        "robustness_label",
    ]
    return (
        scores[columns]
        .sort_values(["baseline_rank", "geo_code"], kind="mergesort")
        .reset_index(drop=True)
    )


def _rank_desc(series: pd.Series) -> pd.Series:
    return series.rank(method="min", ascending=False).astype("Int64")


def _robustness_label(rank_range: int | float) -> str:
    if rank_range <= 1:
        return "stable"
    if rank_range <= 3:
        return "sensitive"
    return "fragile"
