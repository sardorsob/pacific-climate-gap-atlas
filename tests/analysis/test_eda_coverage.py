from __future__ import annotations

import unittest

import pandas as pd

from analysis.eda import coverage as coverage_module


class Task011CoverageByGeographyTests(unittest.TestCase):
    def test_build_coverage_by_geography_includes_data_desert_flags_and_caveats(self) -> None:
        helper = getattr(coverage_module, "build_coverage_by_geography", None)
        self.assertIsNotNone(helper, "build_coverage_by_geography should be defined")

        observations = pd.DataFrame(
            [
                {
                    "dataset_slug": "climate-long-series",
                    "dataset_name": "Climate long series",
                    "pillar": "climate_signal",
                    "story_role": "climate_exposure",
                    "geo_code": "AA",
                    "year": 2000,
                    "value": 1.0,
                },
                {
                    "dataset_slug": "climate-long-series",
                    "dataset_name": "Climate long series",
                    "pillar": "climate_signal",
                    "story_role": "climate_exposure",
                    "geo_code": "AA",
                    "year": 2001,
                    "value": 1.1,
                },
                {
                    "dataset_slug": "climate-long-series",
                    "dataset_name": "Climate long series",
                    "pillar": "climate_signal",
                    "story_role": "climate_exposure",
                    "geo_code": "AA",
                    "year": 2002,
                    "value": 1.2,
                },
                {
                    "dataset_slug": "capacity-snapshot",
                    "dataset_name": "Capacity snapshot",
                    "pillar": "adaptation_capacity",
                    "story_role": "response_or_capacity",
                    "geo_code": "AA",
                    "year": 2020,
                    "value": 2.0,
                },
                {
                    "dataset_slug": "observed-stress",
                    "dataset_name": "Observed stress",
                    "pillar": "observed_stress",
                    "story_role": "impact",
                    "geo_code": "BB",
                    "year": 2021,
                    "value": 3.0,
                },
            ]
        )
        lookup = pd.DataFrame(
            [
                {"geo_code": "AA"},
                {"geo_code": "BB"},
                {"geo_code": "CC"},
            ]
        )

        table = helper(observations, lookup)

        self.assertEqual(table["geo_code"].tolist(), ["CC", "BB", "AA"])
        self.assertIn("row_count", table.columns)
        self.assertIn("dataset_count", table.columns)
        self.assertIn("first_observation_year", table.columns)
        self.assertIn("last_observation_year", table.columns)
        self.assertIn("data_desert_flag", table.columns)
        self.assertIn("missing_observed_stress_flag", table.columns)
        self.assertIn("coverage_caveat", table.columns)

        aa = table.loc[table["geo_code"] == "AA"].iloc[0]
        self.assertEqual(aa["row_count"], 4)
        self.assertEqual(aa["dataset_count"], 2)
        self.assertEqual(aa["first_observation_year"], 2000)
        self.assertEqual(aa["last_observation_year"], 2020)
        self.assertFalse(bool(aa["data_desert_flag"]))
        self.assertTrue(bool(aa["missing_observed_stress_flag"]))
        self.assertIn("long time series", aa["coverage_caveat"])

        cc = table.loc[table["geo_code"] == "CC"].iloc[0]
        self.assertEqual(cc["row_count"], 0)
        self.assertEqual(cc["dataset_count"], 0)
        self.assertTrue(bool(cc["data_desert_flag"]))
        self.assertTrue(bool(cc["missing_climate_signal_flag"]))


class Task011CoverageByDatasetTests(unittest.TestCase):
    def test_build_coverage_by_dataset_reports_missing_geographies_and_caveat(self) -> None:
        helper = getattr(coverage_module, "build_coverage_by_dataset", None)
        self.assertIsNotNone(helper, "build_coverage_by_dataset should be defined")

        observations = pd.DataFrame(
            [
                {
                    "dataset_slug": "climate-long-series",
                    "dataset_name": "Climate long series",
                    "pillar": "climate_signal",
                    "story_role": "climate_exposure",
                    "geo_code": "AA",
                    "year": 2000,
                    "value": 1.0,
                },
                {
                    "dataset_slug": "climate-long-series",
                    "dataset_name": "Climate long series",
                    "pillar": "climate_signal",
                    "story_role": "climate_exposure",
                    "geo_code": "AA",
                    "year": 2001,
                    "value": 1.1,
                },
                {
                    "dataset_slug": "climate-long-series",
                    "dataset_name": "Climate long series",
                    "pillar": "climate_signal",
                    "story_role": "climate_exposure",
                    "geo_code": "BB",
                    "year": 2000,
                    "value": 1.3,
                },
                {
                    "dataset_slug": "capacity-snapshot",
                    "dataset_name": "Capacity snapshot",
                    "pillar": "adaptation_capacity",
                    "story_role": "response_or_capacity",
                    "geo_code": "AA",
                    "year": 2020,
                    "value": 2.0,
                },
            ]
        )
        profile = pd.DataFrame(
            [
                {"slug": "climate-long-series", "name": "Climate long series"},
                {"slug": "capacity-snapshot", "name": "Capacity snapshot"},
            ]
        )
        lookup = pd.DataFrame(
            [
                {"geo_code": "AA"},
                {"geo_code": "BB"},
                {"geo_code": "CC"},
            ]
        )

        table = helper(observations, profile, lookup)

        self.assertEqual(
            table["dataset_slug"].tolist(),
            ["capacity-snapshot", "climate-long-series"],
        )
        self.assertIn("row_count", table.columns)
        self.assertIn("dataset_count", table.columns)
        self.assertIn("geography_count", table.columns)
        self.assertIn("first_observation_year", table.columns)
        self.assertIn("last_observation_year", table.columns)
        self.assertIn("partial_geography_coverage_flag", table.columns)
        self.assertIn("coverage_caveat", table.columns)

        climate = table.loc[table["dataset_slug"] == "climate-long-series"].iloc[0]
        self.assertEqual(climate["row_count"], 3)
        self.assertEqual(climate["dataset_count"], 1)
        self.assertEqual(climate["geography_count"], 2)
        self.assertEqual(climate["first_observation_year"], 2000)
        self.assertEqual(climate["last_observation_year"], 2001)
        self.assertEqual(climate["missing_geographies"], "CC")
        self.assertTrue(bool(climate["partial_geography_coverage_flag"]))
        self.assertIn("long time series", climate["coverage_caveat"])


if __name__ == "__main__":
    unittest.main()
