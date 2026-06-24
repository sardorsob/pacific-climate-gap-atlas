from __future__ import annotations

import unittest

import pandas as pd

from analysis.preprocessing.official_dataset import (
    build_geography_lookup,
    build_pipeline_summary,
    normalize_official_frame,
)


class OfficialDatasetPipelineTests(unittest.TestCase):
    def test_normalize_official_frame_builds_stable_long_rows(self) -> None:
        frame = pd.DataFrame(
            [
                {
                    "CLIMATE_CHANGE_INDICATORS": "SEA_LVL",
                    "GEO_PICT": "FJ",
                    "TIME_PERIOD": "2020",
                    "OBS_VALUE": "4.25",
                    "UNIT_MEASURE": "MM",
                    "OBS_STATUS": "A",
                    "REPORTING_TYPE": "G",
                },
                {
                    "CLIMATE_CHANGE_INDICATORS": "SEA_LVL",
                    "GEO_PICT": "WS",
                    "TIME_PERIOD": "2021",
                    "OBS_VALUE": "",
                    "UNIT_MEASURE": "MM",
                    "OBS_STATUS": "",
                    "REPORTING_TYPE": "G",
                },
            ]
        )

        normalized = normalize_official_frame(
            frame=frame,
            dataset_name="Sea level anomalies",
            dataset_slug="sea-level-anomalies",
            pillar="climate_signal",
            story_role="climate_exposure",
            official_url="https://example.test/view",
            sdmx_csv_api_url="https://example.test/api.csv",
        )

        self.assertEqual(len(normalized), 2)
        self.assertEqual(normalized.loc[0, "dataset_slug"], "sea-level-anomalies")
        self.assertEqual(normalized.loc[0, "indicator_code"], "SEA_LVL")
        self.assertEqual(normalized.loc[0, "geo_code"], "FJ")
        self.assertEqual(normalized.loc[0, "year"], 2020)
        self.assertEqual(normalized.loc[0, "value"], 4.25)
        self.assertTrue(pd.isna(normalized.loc[1, "value"]))
        self.assertEqual(len(normalized.loc[0, "source_row_hash"]), 64)

    def test_build_geography_lookup_counts_dataset_coverage(self) -> None:
        normalized = pd.DataFrame(
            [
                {"dataset_slug": "sea-level", "dataset_name": "Sea level", "geo_code": "FJ", "year": 2020},
                {"dataset_slug": "rainfall", "dataset_name": "Rainfall", "geo_code": "FJ", "year": 2021},
                {"dataset_slug": "rainfall", "dataset_name": "Rainfall", "geo_code": "WS", "year": 2021},
            ]
        )

        lookup = build_geography_lookup(normalized)

        fj = lookup[lookup["geo_code"] == "FJ"].iloc[0]
        self.assertEqual(fj["dataset_count"], 2)
        self.assertEqual(fj["row_count"], 2)
        self.assertEqual(fj["first_year"], 2020)
        self.assertEqual(fj["last_year"], 2021)
        self.assertEqual(fj["datasets"], "rainfall sea-level")

    def test_build_pipeline_summary_records_counts_and_sources(self) -> None:
        normalized = pd.DataFrame(
            [
                {
                    "dataset_slug": "sea-level",
                    "dataset_name": "Sea level",
                    "pillar": "climate_signal",
                    "geo_code": "FJ",
                    "year": 2020,
                    "source_content_sha256": "abc",
                    "official_url": "https://example.test/view",
                    "sdmx_csv_api_url": "https://example.test/api.csv",
                }
            ]
        )

        summary = build_pipeline_summary(normalized)

        self.assertEqual(summary["total_rows"], 1)
        self.assertEqual(summary["dataset_count"], 1)
        self.assertEqual(summary["geography_count"], 1)
        self.assertEqual(summary["datasets"][0]["source_content_sha256"], "abc")


if __name__ == "__main__":
    unittest.main()
