from __future__ import annotations

import unittest

import pandas as pd

from analysis.preprocessing.app_data import (
    build_geography_records,
    build_layer_manifest,
    build_monitoring_geojson,
)


class AppDataExportTests(unittest.TestCase):
    def test_build_geography_records_joins_scores_lookup_and_outlook(self) -> None:
        index = pd.DataFrame(
            [
                {
                    "geo_code": "FJ",
                    "score_status": "scored",
                    "adaptation_gap_score": 10.5,
                    "climate_pressure_score": 59.0,
                    "capacity_score": 86.0,
                    "raw_gap_difference": -27.0,
                    "available_pillars": "adaptation_capacity climate_signal",
                    "missing_pillars": None,
                    "included_indicator_count": 9,
                    "missingness_flag": False,
                }
            ]
        )
        lookup = pd.DataFrame(
            [
                {
                    "geo_code": "FJ",
                    "dataset_count": 9,
                    "row_count": 706,
                    "first_year": 1850,
                    "last_year": 2026,
                    "datasets": "sea-level-anomalies power-generation",
                }
            ]
        )
        outlook = pd.DataFrame(
            [
                {
                    "geo_code": "FJ",
                    "horizon": 2030,
                    "scenario": "capacity_flat",
                    "outlook_gap_score": 19.7,
                    "caveat_notes": "not an operational prediction",
                },
                {
                    "geo_code": "FJ",
                    "horizon": 2050,
                    "scenario": "capacity_flat",
                    "outlook_gap_score": 20.3,
                    "caveat_notes": "not an operational prediction",
                },
            ]
        )

        records = build_geography_records(index=index, lookup=lookup, outlook=outlook)

        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record["geo_code"], "FJ")
        self.assertEqual(record["geography_code"], "FJ")
        self.assertEqual(record["name"], "Fiji")
        self.assertEqual(record["geography_name"], "Fiji")
        self.assertEqual(record["centroid"], {"lon": 178.1, "lat": -17.7})
        self.assertEqual(record["geometry_status"], "centroid_fallback")
        self.assertEqual(record["outlook"]["2030"]["capacity_flat"]["outlook_gap_score"], 19.7)
        self.assertEqual(record["outlook_2030_flat_gap_score"], 19.7)
        self.assertEqual(record["outlook_2050_flat_gap_score"], 20.3)
        self.assertEqual(record["missing_pillars"], "")
        self.assertIn("indicator_trace", record["source_refs"])

    def test_build_layer_manifest_contains_required_layers(self) -> None:
        manifest = build_layer_manifest()
        layer_ids = {layer["id"] for layer in manifest["layers"]}

        self.assertTrue(
            {
                "adaptation_gap",
                "climate_pressure",
                "capacity",
                "outlook_2030_flat",
                "outlook_2050_flat",
            }.issubset(layer_ids)
        )

    def test_build_monitoring_geojson_exports_latest_monitoring_values(self) -> None:
        observations = pd.DataFrame(
            [
                {
                    "dataset_slug": "meteorological-monitoring-network",
                    "geo_code": "FJ",
                    "year": 2025,
                    "value": 7.0,
                    "unit": "N",
                },
                {
                    "dataset_slug": "meteorological-monitoring-network",
                    "geo_code": "FJ",
                    "year": 2026,
                    "value": 8.0,
                    "unit": "N",
                },
            ]
        )

        geojson = build_monitoring_geojson(observations)

        self.assertEqual(geojson["type"], "FeatureCollection")
        self.assertEqual(len(geojson["features"]), 1)
        feature = geojson["features"][0]
        self.assertEqual(feature["properties"]["geo_code"], "FJ")
        self.assertEqual(feature["properties"]["latest_year"], 2026)
        self.assertEqual(feature["properties"]["latest_value"], 8.0)
        self.assertEqual(feature["geometry"]["coordinates"], [178.1, -17.7])


if __name__ == "__main__":
    unittest.main()
