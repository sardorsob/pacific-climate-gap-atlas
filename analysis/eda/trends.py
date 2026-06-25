"""Trend and outlook interpretation helpers."""

from __future__ import annotations

from typing import Any

import pandas as pd

OUTLOOK_INTERPRETATION_COLUMNS = [
    "geo_code",
    "target_year",
    "scenario",
    "reference_year",
    "current_score",
    "projected_score",
    "score_change",
    "movement_direction",
    "movement_magnitude_label",
    "outlook_movement_rank",
    "trend_series_count",
    "backtested_count",
    "linear_beats_naive_count",
    "beats_naive_share",
    "mean_abs_slope_per_decade",
    "mean_residual_std",
    "diagnostic_quality_label",
    "projection_fragility_label",
    "fragility_rank",
    "display_recommendation",
    "caveat",
]


def build_trend_profiles(diagnostics: pd.DataFrame, outlook: pd.DataFrame) -> pd.DataFrame:
    """Summarize climate trend diagnostics and flat-capacity outlook scores by geography."""

    trends = _diagnostic_summary(diagnostics)
    trends["trend_confidence"] = trends.apply(_trend_confidence, axis=1)
    trends["display_recommendation"] = trends["diagnostic_quality_label"].apply(
        _display_recommendation
    )
    trends["trend_profile_caveat"] = trends["diagnostic_quality_label"].apply(
        _trend_profile_caveat
    )
    trends = _add_trend_strength_rank(trends)

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
        "backtested_count",
        "mean_residual_std",
        "diagnostic_quality_label",
        "trend_strength_rank",
        "display_recommendation",
        "trend_profile_caveat",
    ]
    return merged[columns].sort_values("geo_code", kind="mergesort").reset_index(drop=True)


def build_outlook_interpretation(
    trend_diagnostics: pd.DataFrame,
    outlook: pd.DataFrame,
    current_index: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Interpret outlook rows as stress-test movement with diagnostic display guidance."""

    if outlook.empty:
        return pd.DataFrame(columns=OUTLOOK_INTERPRETATION_COLUMNS)

    diagnostics = _diagnostic_summary(trend_diagnostics)
    interpreted = outlook.copy()
    interpreted["target_year"] = pd.to_numeric(interpreted["horizon"], errors="coerce").astype(
        "Int64"
    )
    interpreted["projected_score"] = pd.to_numeric(
        interpreted["outlook_gap_score"], errors="coerce"
    )
    interpreted = interpreted.sort_values(
        ["geo_code", "scenario", "target_year"], kind="mergesort"
    ).reset_index(drop=True)

    references = _current_score_references(interpreted, current_index)
    interpreted = interpreted.merge(
        references,
        on=[column for column in ["geo_code", "scenario"] if column in references],
        how="left",
    )
    interpreted["score_change"] = (
        interpreted["projected_score"] - interpreted["current_score"]
    ).round(4)
    interpreted["movement_direction"] = interpreted["score_change"].apply(_movement_direction)
    interpreted["movement_magnitude_label"] = interpreted["score_change"].apply(
        _movement_magnitude_label
    )
    interpreted = interpreted.drop(
        columns=[
            "trend_series_count",
            "backtested_count",
            "linear_beats_naive_count",
            "beats_naive_share",
            "mean_abs_slope_per_decade",
            "mean_residual_std",
            "diagnostic_quality_label",
        ],
        errors="ignore",
    )
    interpreted = interpreted.merge(diagnostics, on="geo_code", how="left")
    interpreted["diagnostic_quality_label"] = interpreted["diagnostic_quality_label"].fillna(
        "sparse"
    )
    interpreted["display_recommendation"] = interpreted["diagnostic_quality_label"].apply(
        _display_recommendation
    )
    interpreted["projection_fragility_label"] = interpreted.apply(
        _projection_fragility_label, axis=1
    )
    interpreted["caveat"] = interpreted.apply(_outlook_caveat, axis=1)
    interpreted = _add_outlook_ranks(interpreted)

    return interpreted[OUTLOOK_INTERPRETATION_COLUMNS].sort_values(
        ["target_year", "scenario", "geo_code"], kind="mergesort"
    ).reset_index(drop=True)


def _diagnostic_summary(diagnostics: pd.DataFrame) -> pd.DataFrame:
    trend_input = diagnostics.copy()
    trend_input["slope_per_decade"] = pd.to_numeric(
        trend_input.get("slope_per_decade"), errors="coerce"
    )
    trend_input["residual_std"] = pd.to_numeric(trend_input.get("residual_std"), errors="coerce")
    trend_input["backtest_beats_naive_bool"] = trend_input.get(
        "backtest_beats_naive", pd.Series([False] * len(trend_input), index=trend_input.index)
    ).apply(_bool_value)
    trend_input["backtested_bool"] = _backtested_bool(trend_input)

    trends = (
        trend_input.groupby("geo_code", as_index=False)
        .agg(
            trend_series_count=("dataset_slug", "nunique"),
            linear_beats_naive_count=("backtest_beats_naive_bool", "sum"),
            backtested_count=("backtested_bool", "sum"),
            mean_abs_slope_per_decade=("slope_per_decade", lambda values: values.abs().mean()),
            mean_residual_std=("residual_std", "mean"),
        )
        .sort_values("geo_code", kind="mergesort")
    )
    trends["beats_naive_share"] = (
        trends["linear_beats_naive_count"] / trends["trend_series_count"].clip(lower=1)
    ).round(4)
    trends["diagnostic_quality_label"] = trends.apply(_diagnostic_quality_label, axis=1)
    return trends


def _current_score_references(
    outlook: pd.DataFrame,
    current_index: pd.DataFrame | None,
) -> pd.DataFrame:
    if (
        current_index is not None
        and not current_index.empty
        and {"geo_code", "adaptation_gap_score"}.issubset(current_index.columns)
    ):
        references = current_index[["geo_code", "adaptation_gap_score"]].copy()
        references["geo_code"] = references["geo_code"].fillna("").astype(str).str.strip()
        references["current_score"] = pd.to_numeric(
            references["adaptation_gap_score"], errors="coerce"
        )
        references["reference_year"] = pd.NA
        return references[["geo_code", "reference_year", "current_score"]]

    references = outlook.groupby(["geo_code", "scenario"], as_index=False).first()[
        ["geo_code", "scenario", "target_year", "projected_score"]
    ]
    return references.rename(
        columns={"target_year": "reference_year", "projected_score": "current_score"}
    )


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


def _diagnostic_quality_label(row: pd.Series) -> str:
    series_count = int(row.get("trend_series_count", 0))
    backtested_count = int(row.get("backtested_count", 0))
    share = float(row.get("beats_naive_share", 0.0))
    if series_count < 2 or backtested_count < 2:
        return "sparse"
    if series_count >= 3 and share >= 0.67:
        return "supported"
    if share > 0:
        return "mixed"
    return "weak"


def _display_recommendation(diagnostic_quality_label: str) -> str:
    if diagnostic_quality_label == "supported":
        return "show"
    if diagnostic_quality_label == "mixed":
        return "show_with_strong_caveat"
    return "withhold"


def _trend_profile_caveat(diagnostic_quality_label: str) -> str:
    if diagnostic_quality_label == "supported":
        return "show as stress-test context; not a forecast"
    if diagnostic_quality_label == "mixed":
        return "linear diagnostics are mixed; show only with a strong caveat"
    if diagnostic_quality_label == "sparse":
        return "withhold from outlook layer because diagnostics are sparse"
    return "withhold from outlook layer because diagnostics are weak"


def _movement_direction(score_change: float) -> str:
    if score_change >= 5:
        return "widening"
    if score_change <= -5:
        return "narrowing"
    return "little_change"


def _movement_magnitude_label(score_change: float) -> str:
    magnitude = abs(float(score_change))
    if magnitude >= 15:
        return "large"
    if magnitude >= 5:
        return "moderate"
    return "limited"


def _projection_fragility_label(row: pd.Series) -> str:
    quality = str(row.get("diagnostic_quality_label", "sparse"))
    movement = str(row.get("movement_magnitude_label", "limited"))
    if quality in {"sparse", "weak"}:
        return "fragile"
    if quality == "mixed" or movement == "large":
        return "caveated"
    return "lower"


def _outlook_caveat(row: pd.Series) -> str:
    caveats = ["stress-test interpretation; not a forecast"]
    quality = str(row.get("diagnostic_quality_label", "sparse"))
    if quality == "supported":
        caveats.append("diagnostics support cautious display")
    elif quality == "mixed":
        caveats.append("mixed diagnostics require visible caveat")
    elif quality == "sparse":
        caveats.append("withhold because sparse diagnostics do not support display")
    else:
        caveats.append("withhold because weak diagnostics do not support display")
    if str(row.get("projection_fragility_label")) == "fragile":
        caveats.append("fragile projection")
    return "; ".join(caveats)


def _add_trend_strength_rank(trends: pd.DataFrame) -> pd.DataFrame:
    ranked = trends.sort_values(
        ["beats_naive_share", "trend_series_count", "mean_abs_slope_per_decade", "geo_code"],
        ascending=[False, False, False, True],
        kind="mergesort",
    ).copy()
    ranked["trend_strength_rank"] = range(1, len(ranked) + 1)
    return ranked.sort_values("geo_code", kind="mergesort")


def _add_outlook_ranks(interpreted: pd.DataFrame) -> pd.DataFrame:
    movement_ranked = interpreted.assign(
        abs_score_change=interpreted["score_change"].abs()
    ).sort_values(
        ["abs_score_change", "target_year", "scenario", "geo_code"],
        ascending=[False, True, True, True],
        kind="mergesort",
    )
    interpreted.loc[movement_ranked.index, "outlook_movement_rank"] = range(
        1, len(movement_ranked) + 1
    )

    fragility_order = {"fragile": 3, "caveated": 2, "lower": 1}
    fragility_ranked = interpreted.assign(
        fragility_score=interpreted["projection_fragility_label"].map(fragility_order).fillna(3),
        abs_score_change=interpreted["score_change"].abs(),
    ).sort_values(
        ["fragility_score", "abs_score_change", "target_year", "scenario", "geo_code"],
        ascending=[False, False, True, True, True],
        kind="mergesort",
    )
    interpreted.loc[fragility_ranked.index, "fragility_rank"] = range(
        1, len(fragility_ranked) + 1
    )
    interpreted["outlook_movement_rank"] = interpreted["outlook_movement_rank"].astype(int)
    interpreted["fragility_rank"] = interpreted["fragility_rank"].astype(int)
    return interpreted


def _backtested_bool(frame: pd.DataFrame) -> pd.Series:
    if "holdout_linear_mae" in frame.columns:
        return pd.to_numeric(frame["holdout_linear_mae"], errors="coerce").notna()
    if "backtest_beats_naive" in frame.columns:
        return frame["backtest_beats_naive"].notna()
    return pd.Series([False] * len(frame), index=frame.index)


def _bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}
