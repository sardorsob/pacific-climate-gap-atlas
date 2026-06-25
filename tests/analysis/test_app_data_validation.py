from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from scripts import validate_data_contracts


class AppDataValidationTests(unittest.TestCase):
    def test_validate_root_accepts_complete_contracts_and_matching_public_copies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            processed = root / "data" / "processed" / "app"
            public = root / "app" / "public" / "data"
            processed.mkdir(parents=True)
            public.mkdir(parents=True)

            _write_json(processed / "geographies.json", _valid_geographies())
            _write_json(processed / "layers.json", _valid_layers())
            _write_auxiliary_app_files(processed)
            _copy_public_app_files(processed, public)

            errors = validate_data_contracts.validate_root(root)

            self.assertEqual(errors, [])

    def test_validate_root_reports_missing_required_fields_and_layer_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            processed = root / "data" / "processed" / "app"
            public = root / "app" / "public" / "data"
            processed.mkdir(parents=True)
            public.mkdir(parents=True)

            broken_geographies = _valid_geographies()
            del broken_geographies["geographies"][0]["centroid"]["lat"]
            del broken_geographies["geographies"][0]["source_refs"]["indicator_trace"]
            broken_layers = _valid_layers()
            broken_layers["layers"] = broken_layers["layers"][:-1]
            del broken_layers["layers"][0]["fields"]
            _write_json(processed / "geographies.json", broken_geographies)
            _write_json(processed / "layers.json", broken_layers)
            _write_auxiliary_app_files(processed)
            _copy_public_app_files(processed, public)

            errors = validate_data_contracts.validate_root(root)

            self.assertIn("geographies[0].centroid missing required field: lat", errors)
            self.assertIn("geographies[0].source_refs missing required field: indicator_trace", errors)
            self.assertIn("layers[0] missing required field: fields", errors)
            self.assertIn("layers missing required id: outlook_2050_flat", errors)

    def test_validate_root_checks_all_public_app_file_copies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            processed = root / "data" / "processed" / "app"
            public = root / "app" / "public" / "data"
            processed.mkdir(parents=True)
            public.mkdir(parents=True)

            _write_json(processed / "geographies.json", _valid_geographies())
            _write_json(processed / "layers.json", _valid_layers())
            _write_auxiliary_app_files(processed)
            _copy_public_app_files(processed, public)
            _write_json(public / "country_details.json", {"schema_version": 1, "stale": True})

            errors = validate_data_contracts.validate_root(root)

            self.assertIn(
                "app/public/data/country_details.json does not match "
                "data/processed/app/country_details.json byte-for-byte",
                errors,
            )

    def test_main_prints_fail_summary_and_returns_nonzero_for_missing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            stdout = io.StringIO()

            with contextlib.redirect_stdout(stdout):
                exit_code = validate_data_contracts.main(root=Path(tmp))

            self.assertEqual(exit_code, 1)
            self.assertIn("FAIL app data contracts", stdout.getvalue())
            self.assertIn("data/processed/app/geographies.json does not exist", stdout.getvalue())


def _valid_geographies() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "geographies": [
            {
                "geo_code": "FJ",
                "geography_code": "FJ",
                "name": "Fiji",
                "geography_name": "Fiji",
                "centroid": {"lon": 178.0, "lat": -18.0},
                "score_status": "scored",
                "adaptation_gap_score": 42.0,
                "climate_pressure_score": 67.0,
                "capacity_score": 25.0,
                "included_indicator_count": 3,
                "missingness_flag": False,
                "source_refs": {
                    "index": "data/processed/gap_index.csv",
                    "indicator_trace": "data/processed/indicator_trace.csv",
                },
            }
        ],
    }


def _valid_layers() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "layers": [
            _layer("adaptation_gap"),
            _layer("climate_pressure"),
            _layer("capacity"),
            _layer("outlook_2030_flat"),
            _layer("outlook_2050_flat"),
        ],
    }


def _layer(layer_id: str) -> dict[str, object]:
    return {
        "id": layer_id,
        "label": layer_id.replace("_", " ").title(),
        "type": "choropleth",
        "source_file": "geographies.json",
        "fields": ["geo_code", layer_id],
    }


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _write_auxiliary_app_files(processed: Path) -> None:
    for file_name in validate_data_contracts.PUBLIC_COPY_FILES:
        path = processed / file_name
        if not path.exists():
            _write_json(path, {"schema_version": 1})


def _copy_public_app_files(processed: Path, public: Path) -> None:
    for file_name in validate_data_contracts.PUBLIC_COPY_FILES:
        (public / file_name).write_bytes((processed / file_name).read_bytes())


if __name__ == "__main__":
    unittest.main()
