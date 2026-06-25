"""Trend and outlook interpretation helpers."""

from __future__ import annotations

from typing import Any

import pandas as pd


def build_trend_profiles(diagnostics: pd.DataFrame, outlook: pd.DataFrame) -> pd.DataFrame:
    """Summarize climate trend diagnostics and flat-capacity outlook scores by geography."""

    trend_input = diagnostics.copy()
    trend_input["slope_per_decade"] = pd.to_numeric(
        trend_input["slope_per_decade"], errors="coerce"
    )
    trend_input["backtest_beats_naive_bool"] = trend_input["backtest_beats_naive"].apply(
        _bool_value
    )

    trends = (
        trend_input.groupby("geo_code", as_index=False)
        .agg(
            trend_series_count=("dataset_slug", "nunique"),
            linear_beats_naive_count=("backtest_beats_naive_bool", "sum"),
            mean_abs_slope_per_decade=("slope_per_decade", lambda values: values.abs().mean()),
        )
        .sort_values("geo_code", kind="mergesort")
    )
    trends["beats_naive_share"] = (
        trends["linear_beats_naive_count"] / trends["trend_series_count"]
    ).round(4)
    trends["trend_confidence"] = trends.apply(_trend_confidence, axis=1)

    flat_outlook = outlook[outlook["scenario"] == "capacity_flat"].copy()
    flat_outlook["outlook_gap_score"] = pd.to_numeric(
        flat_outlook["outlook_gap_score"], errors="coerce"
    )
    outlook_summary = (
        flat_outlook.groupby("geo_code", as_index=False)
        .agg(max_flat_outlook_gap_score=("outlook_gap_score", "max"))
        .sort_values("geo_code", kind="mergesort")
    )

    merged = trends.merge(outlook_summary, on="geo_code", how="left")
    columns = [
        "geo_code",
        "trend_series_count",
        "linear_beats_naive_count",
        "beats_naive_share",
        "mean_abs_slope_per_decade",
        "trend_confidence",
        "max_flat_outlook_gap_score",
    ]
    return merged[columns].sort_values("geo_code", kind="mergesort").reset_index(drop=True)


def _trend_confidence(row: pd.Series) -> str:
    series_count = int(row.get("trend_series_count", 0))
    share = float(row.get("beats_naive_share", 0.0))
    if series_count < 2:
        return "sparse"
    if share >= 0.67:
        return "stronger"
    if share > 0:
        return "mixed"
    return "weak"


def _bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}
