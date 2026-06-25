from __future__ import annotations

import unittest

import pandas as pd

from analysis.eda.indicator_forensics import (
    build_indicator_forensics,
    build_indicator_forensics_tables,
    build_indicator_outliers,
)


class EdaIndicatorForensicsTests(unittest.TestCase):
    def test_forensics_preserves_trace_fields_and_adds_leverage_context(self) -> None:
        trace = pd.DataFrame(
            [
                _trace_row(
                    geo_code="AA",
                    dataset_slug="rainfall-anomalies",
                    pillar="climate_signal",
                    latest_value=-12.0,
                    scoring_value=12.0,
                    indicator_score=90.0,
                    source_row_hash="hash-aa",
                ),
                _trace_row(
                    geo_code="BB",
                    dataset_slug="rainfall-anomalies",
                    pillar="climate_signal",
                    latest_value=4.0,
                    scoring_value=4.0,
                    indicator_score=35.0,
                    source_row_hash="hash-bb",
                ),
                _trace_row(
                    geo_code="CC",
                    dataset_slug="rainfall-anomalies",
                    pillar="climate_signal",
                    latest_value=7.0,
                    scoring_value=7.0,
                    indicator_score=60.0,
                    source_row_hash="hash-cc",
                ),
                _trace_row(
                    geo_code="AA",
                    dataset_slug="greenhouse-gas-emissions-per-capita",
                    dataset_name="Greenhouse gas emissions per capita",
                    pillar="responsibility_context",
                    latest_value=100.0,
                    scoring_value=100.0,
                    unit="TON",
                    indicator_score=100.0,
                    source_row_hash="hash-ghg-aa",
                ),
            ]
        )

        forensics = build_indicator_forensics(trace)

        required_columns = {
            "geo_code",
            "dataset_slug",
            "dataset_name",
            "pillar",
            "latest_year",
            "latest_value",
            "scoring_value",
            "unit",
            "indicator_score",
            "source_row_hash",
            "rank_within_indicator",
            "score_percentile_group",
            "high_outlier_flag",
            "low_outlier_flag",
            "score_input_role",
        }
        self.assertTrue(required_columns.issubset(set(forensics.columns)))

        rainfall = forensics[forensics["dataset_slug"] == "rainfall-anomalies"]
        self.assertEqual(rainfall["geo_code"].tolist(), ["AA", "CC", "BB"])

        top_rainfall = rainfall.iloc[0]
        self.assertEqual(top_rainfall["latest_value"], -12.0)
        self.assertEqual(top_rainfall["scoring_value"], 12.0)
        self.assertEqual(top_rainfall["source_row_hash"], "hash-aa")
        self.assertEqual(top_rainfall["rank_within_indicator"], 1)
        self.assertEqual(top_rainfall["score_percentile_group"], "top_quartile")
        self.assertEqual(top_rainfall["score_input_role"], "score_input")

        ghg = forensics[forensics["dataset_slug"] == "greenhouse-gas-emissions-per-capita"]
        self.assertEqual(ghg.iloc[0]["score_input_role"], "context_only")

    def test_outliers_use_dataset_iqr_fences_and_include_method_caveats(self) -> None:
        scoring_values = [0.0, 10.0, 11.0, 12.0, 13.0, 14.0, 100.0]
        trace = pd.DataFrame(
            [
                _trace_row(
                    geo_code=f"G{index}",
                    dataset_slug="directly-affected",
                    dataset_name="Directly affected people",
                    pillar="observed_stress",
                    latest_value=value,
                    scoring_value=value,
                    indicator_score=float(index * 10),
                    source_row_hash=f"hash-{index}",
                )
                for index, value in enumerate(scoring_values, start=1)
            ]
        )

        outliers = build_indicator_outliers(trace)

        self.assertEqual(outliers["geo_code"].tolist(), ["G1", "G7"])
        self.assertEqual(outliers["outlier_direction"].tolist(), ["low", "high"])
        self.assertEqual(
            outliers["outlier_label"].tolist(),
            ["low scoring-value outlier", "high scoring-value outlier"],
        )
        self.assertEqual(
            set(outliers["outlier_method"]),
            {"dataset_iqr_1_5x_on_scoring_value"},
        )
        self.assertTrue(outliers["outlier_caveat"].str.contains("units and denominators").all())
        self.assertTrue(outliers["high_outlier_flag"].tolist()[1])
        self.assertTrue(outliers["low_outlier_flag"].tolist()[0])

    def test_forensics_tables_return_expected_artifact_names(self) -> None:
        trace = pd.DataFrame(
            [
                _trace_row(
                    geo_code="AA",
                    dataset_slug="capacity",
                    pillar="adaptation_capacity",
                    latest_value=1.0,
                    scoring_value=1.0,
                    indicator_score=25.0,
                    source_row_hash="hash-aa",
                ),
                _trace_row(
                    geo_code="BB",
                    dataset_slug="capacity",
                    pillar="adaptation_capacity",
                    latest_value=2.0,
                    scoring_value=2.0,
                    indicator_score=75.0,
                    source_row_hash="hash-bb",
                ),
            ]
        )

        tables = build_indicator_forensics_tables(trace)

        self.assertEqual(
            sorted(tables),
            ["eda_indicator_forensics.csv", "eda_indicator_outliers.csv"],
        )
        self.assertEqual(len(tables["eda_indicator_forensics.csv"]), 2)
        self.assertEqual(len(tables["eda_indicator_outliers.csv"]), 0)


def _trace_row(
    *,
    geo_code: str,
    dataset_slug: str,
    pillar: str,
    latest_value: float,
    scoring_value: float,
    indicator_score: float,
    source_row_hash: str,
    dataset_name: str = "Rainfall anomalies",
    latest_year: int = 2025,
    unit: str = "MM",
) -> dict[str, object]:
    return {
        "geo_code": geo_code,
        "dataset_slug": dataset_slug,
        "dataset_name": dataset_name,
        "pillar": pillar,
        "latest_year": latest_year,
        "latest_value": latest_value,
        "scoring_value": scoring_value,
        "unit": unit,
        "indicator_score": indicator_score,
        "indicator_weight": 1.0,
        "source_row_hash": source_row_hash,
    }


if __name__ == "__main__":
    unittest.main()
