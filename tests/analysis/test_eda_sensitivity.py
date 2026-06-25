from __future__ import annotations

import unittest

import pandas as pd

from analysis.eda.sensitivity import (
    build_leave_one_indicator_sensitivity,
    build_rank_volatility,
)


class LeaveOneIndicatorSensitivityTests(unittest.TestCase):
    def test_leave_one_indicator_marks_required_pillar_drop_as_insufficient(self) -> None:
        index = pd.DataFrame(
            [
                _index_row("AA", 90.0, 80.0, 20.0),
                _index_row("BB", 50.0, 50.0, 50.0),
                _index_row("CC", 10.0, 20.0, 80.0),
            ]
        )
        trace = pd.DataFrame(
            [
                _trace_row("AA", "heat", "climate_signal", 90.0),
                _trace_row("BB", "heat", "climate_signal", 50.0),
                _trace_row("CC", "heat", "climate_signal", 10.0),
                _trace_row("AA", "capacity", "adaptation_capacity", 20.0),
                _trace_row("BB", "capacity", "adaptation_capacity", 50.0),
                _trace_row("CC", "capacity", "adaptation_capacity", 80.0),
            ]
        )

        sensitivity = build_leave_one_indicator_sensitivity(index, trace)

        dropped_capacity = sensitivity[sensitivity["scenario"] == "drop_capacity"]
        self.assertEqual(len(dropped_capacity), 3)
        self.assertTrue(dropped_capacity["scenario_rank"].isna().all())
        self.assertEqual(
            dropped_capacity["scenario_status"].unique().tolist(),
            ["insufficient_data"],
        )

    def test_rank_volatility_summarizes_weight_and_leave_one_indicator_scenarios(self) -> None:
        index = pd.DataFrame(
            [
                _index_row("AA", 90.0, 80.0, 20.0),
                _index_row("BB", 50.0, 50.0, 50.0),
                _index_row("CC", 10.0, 20.0, 80.0),
            ]
        )
        trace = pd.DataFrame(
            [
                _trace_row("AA", "heat", "climate_signal", 100.0),
                _trace_row("BB", "heat", "climate_signal", 60.0),
                _trace_row("CC", "heat", "climate_signal", 20.0),
                _trace_row("AA", "storm", "observed_stress", 10.0),
                _trace_row("BB", "storm", "observed_stress", 70.0),
                _trace_row("CC", "storm", "observed_stress", 20.0),
                _trace_row("AA", "finance", "adaptation_capacity", 20.0),
                _trace_row("BB", "finance", "adaptation_capacity", 50.0),
                _trace_row("CC", "finance", "adaptation_capacity", 80.0),
                _trace_row("AA", "monitoring", "adaptation_capacity", 80.0),
                _trace_row("BB", "monitoring", "adaptation_capacity", 50.0),
                _trace_row("CC", "monitoring", "adaptation_capacity", 20.0),
            ]
        )

        volatility = build_rank_volatility(index, trace)

        self.assertEqual(volatility["geo_code"].tolist(), ["AA", "BB", "CC"])
        self.assertIn("baseline_rank", volatility.columns)
        self.assertIn("scenario_rank_summary", volatility.columns)
        self.assertIn("rank_range", volatility.columns)
        self.assertIn("robustness_label", volatility.columns)
        self.assertEqual(volatility.loc[0, "baseline_rank"], 1)
        self.assertEqual(volatility.loc[0, "scenario_count"], 6)
        self.assertIn("drop_heat=", volatility.loc[0, "scenario_rank_summary"])
        self.assertIn("weight_pressure_heavy=", volatility.loc[0, "scenario_rank_summary"])
        self.assertGreaterEqual(volatility.loc[0, "rank_range"], 0)
        self.assertTrue(volatility["rank_caveat"].str.contains("Small sample").all())


def _index_row(
    geo_code: str,
    adaptation_gap_score: float,
    climate_pressure_score: float,
    capacity_score: float,
) -> dict[str, object]:
    return {
        "geo_code": geo_code,
        "adaptation_gap_score": adaptation_gap_score,
        "climate_pressure_score": climate_pressure_score,
        "capacity_score": capacity_score,
    }


def _trace_row(
    geo_code: str,
    dataset_slug: str,
    pillar: str,
    indicator_score: float,
) -> dict[str, object]:
    return {
        "geo_code": geo_code,
        "dataset_slug": dataset_slug,
        "dataset_name": dataset_slug.replace("-", " ").title(),
        "pillar": pillar,
        "indicator_score": indicator_score,
    }


if __name__ == "__main__":
    unittest.main()
