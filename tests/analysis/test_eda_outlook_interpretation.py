from __future__ import annotations

import unittest

import pandas as pd

from analysis.eda import trends
from analysis.eda.trends import build_trend_profiles


class EdaTrendProfileInterpretationTests(unittest.TestCase):
    def test_build_trend_profiles_adds_display_recommendations(self) -> None:
        diagnostics = pd.DataFrame(
            [
                _diagnostic("AA", "rainfall", 0.7, True),
                _diagnostic("AA", "temperature", 0.3, True),
                _diagnostic("AA", "sea-level", 0.2, True),
                _diagnostic("AA", "sea-surface", 0.1, False),
                _diagnostic("BB", "rainfall", 0.8, False),
            ]
        )
        outlook = pd.DataFrame(
            [
                _outlook("AA", 2030, "capacity_flat", 45.0),
                _outlook("AA", 2050, "capacity_flat", 55.0),
                _outlook("BB", 2030, "capacity_flat", 60.0),
            ]
        )

        profiles = build_trend_profiles(diagnostics, outlook)

        self.assertIn("display_recommendation", profiles.columns)
        self.assertIn("trend_strength_rank", profiles.columns)
        aa = profiles[profiles["geo_code"] == "AA"].iloc[0]
        bb = profiles[profiles["geo_code"] == "BB"].iloc[0]
        self.assertEqual(aa["trend_confidence"], "stronger")
        self.assertEqual(aa["display_recommendation"], "show")
        self.assertEqual(aa["trend_strength_rank"], 1)
        self.assertEqual(bb["trend_confidence"], "sparse")
        self.assertEqual(bb["display_recommendation"], "withhold")
        self.assertIn("sparse", bb["trend_profile_caveat"])

    def test_build_outlook_interpretation_caveats_weak_diagnostics(self) -> None:
        diagnostics = pd.DataFrame(
            [
                _diagnostic("AA", "rainfall", 0.7, True),
                _diagnostic("AA", "temperature", 0.3, True),
                _diagnostic("AA", "sea-level", 0.2, True),
                _diagnostic("AA", "sea-surface", 0.1, False),
                _diagnostic("BB", "rainfall", 0.8, False),
            ]
        )
        outlook = pd.DataFrame(
            [
                _outlook("AA", 2030, "capacity_flat", 40.0),
                _outlook("AA", 2050, "capacity_flat", 60.0),
                _outlook("BB", 2030, "capacity_flat", 30.0),
                _outlook("BB", 2050, "capacity_flat", 50.0),
            ]
        )

        self.assertTrue(hasattr(trends, "build_outlook_interpretation"))
        index = pd.DataFrame(
            [
                {"geo_code": "AA", "adaptation_gap_score": 35.0},
                {"geo_code": "BB", "adaptation_gap_score": 25.0},
            ]
        )

        interpretation = trends.build_outlook_interpretation(diagnostics, outlook, index)

        aa_2050 = interpretation[
            (interpretation["geo_code"] == "AA")
            & (interpretation["target_year"] == 2050)
            & (interpretation["scenario"] == "capacity_flat")
        ].iloc[0]
        bb_2050 = interpretation[
            (interpretation["geo_code"] == "BB")
            & (interpretation["target_year"] == 2050)
            & (interpretation["scenario"] == "capacity_flat")
        ].iloc[0]
        self.assertEqual(aa_2050["current_score"], 35.0)
        self.assertEqual(aa_2050["projected_score"], 60.0)
        self.assertEqual(aa_2050["score_change"], 25.0)
        self.assertEqual(aa_2050["movement_direction"], "widening")
        self.assertEqual(aa_2050["movement_magnitude_label"], "large")
        self.assertEqual(aa_2050["diagnostic_quality_label"], "supported")
        self.assertEqual(aa_2050["display_recommendation"], "show")
        self.assertIn("stress-test", aa_2050["caveat"])
        self.assertEqual(bb_2050["diagnostic_quality_label"], "sparse")
        self.assertEqual(bb_2050["display_recommendation"], "withhold")
        self.assertIn("sparse diagnostics", bb_2050["caveat"])


def _diagnostic(
    geo_code: str,
    dataset_slug: str,
    slope_per_decade: float,
    backtest_beats_naive: bool,
) -> dict[str, object]:
    return {
        "geo_code": geo_code,
        "dataset_slug": dataset_slug,
        "slope_per_decade": slope_per_decade,
        "residual_std": 1.0,
        "holdout_linear_mae": 1.0 if backtest_beats_naive else 3.0,
        "holdout_naive_mae": 2.0,
        "backtest_beats_naive": backtest_beats_naive,
    }


def _outlook(
    geo_code: str,
    horizon: int,
    scenario: str,
    outlook_gap_score: float,
) -> dict[str, object]:
    return {
        "geo_code": geo_code,
        "horizon": horizon,
        "scenario": scenario,
        "outlook_gap_score": outlook_gap_score,
        "trend_indicator_count": 4 if geo_code == "AA" else 1,
        "mean_residual_std": 1.0,
        "linear_beats_naive_count": 3 if geo_code == "AA" else 0,
        "linear_backtest_count": 4 if geo_code == "AA" else 1,
        "caveat_notes": "not an operational prediction",
    }


if __name__ == "__main__":
    unittest.main()
