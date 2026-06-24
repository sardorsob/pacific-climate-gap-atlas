from __future__ import annotations

import unittest

from analysis.io.dataset_profile import profile_csv_text, profile_to_contract, slugify


class DatasetProfileTests(unittest.TestCase):
    def test_slugify_makes_contract_safe_names(self) -> None:
        self.assertEqual(
            slugify(
                "Fisheries management measures in place and multilateral "
                "and bilateral fisheries management arrangements"
            ),
            "fisheries-management-measures-in-place-and-multilateral-and-bilateral-fisheries-management-arrangements",
        )

    def test_profile_csv_text_counts_rows_geographies_years_and_missingness(self) -> None:
        csv_text = "\n".join(
            [
                "STRUCTURE,GEO_PICT,TIME_PERIOD,OBS_VALUE,UNIT_MEASURE",
                "data,FJ,2020,1.5,C",
                "data,FJ,2021,,C",
                "data,WS,2021,2.25,C",
            ]
        )

        profile = profile_csv_text(
            name="Mean sea surface temperature anomalies",
            pillar="climate_signal",
            story_role="climate_exposure",
            official_url="https://example.test/view",
            sdmx_csv_api_url="https://example.test/api.csv",
            csv_text=csv_text,
        )

        self.assertEqual(profile.status, "ok")
        self.assertEqual(profile.row_count, 3)
        self.assertEqual(profile.geography_count, 2)
        self.assertEqual(profile.year_start, 2020)
        self.assertEqual(profile.year_end, 2021)
        self.assertEqual(profile.value_count, 2)
        self.assertEqual(profile.missing_value_count, 1)
        self.assertEqual(profile.geography_codes, ["FJ", "WS"])
        self.assertEqual(profile.caveat_notes, "One value is missing.")

    def test_profile_to_contract_preserves_source_and_schema_context(self) -> None:
        profile = profile_csv_text(
            name="Sea level anomalies",
            pillar="climate_signal",
            story_role="climate_exposure",
            official_url="https://example.test/view",
            sdmx_csv_api_url="https://example.test/api.csv",
            csv_text="GEO_PICT,TIME_PERIOD,OBS_VALUE\nFJ,1993,4.2\n",
        )

        contract = profile_to_contract(profile, generated_at_utc="2026-06-24T00:00:00Z")

        self.assertEqual(contract["slug"], "sea-level-anomalies")
        self.assertEqual(contract["source"]["official_url"], "https://example.test/view")
        self.assertEqual(contract["schema"]["geography_column"], "GEO_PICT")
        self.assertEqual(contract["coverage"]["year_range"], {"start": 1993, "end": 1993})


if __name__ == "__main__":
    unittest.main()
