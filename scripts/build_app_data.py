"""Export app-ready JSON and GeoJSON files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.preprocessing.app_data import (  # noqa: E402
    build_atlas_geojson,
    build_geographies_payload,
    build_geography_records,
    build_layer_manifest,
    build_monitoring_geojson,
)


DEFAULT_CONFIG = ROOT / "configs" / "app_layers.yml"
DEFAULT_INDEX = ROOT / "artifacts" / "tables" / "adaptation_gap_index.csv"
DEFAULT_TRACE = ROOT / "artifacts" / "tables" / "adaptation_gap_indicator_trace.csv"
DEFAULT_LOOKUP = ROOT / "data" / "processed" / "geography_lookup.csv"
DEFAULT_OBSERVATIONS = ROOT / "data" / "processed" / "official_observations.csv"
DEFAULT_OUTLOOK = ROOT / "artifacts" / "tables" / "adaptation_gap_outlook.csv"
DEFAULT_PROCESSED_APP_DIR = ROOT / "data" / "processed" / "app"
DEFAULT_PUBLIC_DATA_DIR = ROOT / "app" / "public" / "data"
DEFAULT_SUMMARY_OUTPUT = ROOT / "artifacts" / "provenance" / "app_data_summary.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--indicator-trace", type=Path, default=DEFAULT_TRACE)
    parser.add_argument("--geography-lookup", type=Path, default=DEFAULT_LOOKUP)
    parser.add_argument("--observations", type=Path, default=DEFAULT_OBSERVATIONS)
    parser.add_argument("--outlook", type=Path, default=DEFAULT_OUTLOOK)
    parser.add_argument("--processed-app-dir", type=Path, default=DEFAULT_PROCESSED_APP_DIR)
    parser.add_argument("--public-data-dir", type=Path, default=DEFAULT_PUBLIC_DATA_DIR)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    return parser.parse_args()


def export_app_data(
    *,
    index_path: Path,
    trace_path: Path,
    lookup_path: Path,
    observations_path: Path,
    outlook_path: Path,
    config_path: Path,
    processed_app_dir: Path,
    public_data_dir: Path,
    summary_output: Path,
) -> dict[str, object]:
    if not config_path.exists():
        raise FileNotFoundError(f"App layer config not found: {config_path}")

    index = pd.read_csv(index_path)
    lookup = pd.read_csv(lookup_path)
    observations = pd.read_csv(observations_path)
    outlook = pd.read_csv(outlook_path)

    records = build_geography_records(index=index, lookup=lookup, outlook=outlook)
    geographies_payload = build_geographies_payload(records)
    atlas_geojson = build_atlas_geojson(records)
    monitoring_geojson = build_monitoring_geojson(observations)
    layers_payload = build_layer_manifest()
    country_details_payload = build_country_details_payload(records, trace_path=trace_path)

    processed_app_dir.mkdir(parents=True, exist_ok=True)
    public_data_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "geographies.json": geographies_payload,
        "atlas_geographies.geojson": atlas_geojson,
        "monitoring_network.geojson": monitoring_geojson,
        "layers.json": layers_payload,
        "country_details.json": country_details_payload,
    }

    for filename, payload in outputs.items():
        write_json(processed_app_dir / filename, payload)
        shutil.copyfile(processed_app_dir / filename, public_data_dir / filename)

    summary = {
        "schema_version": 1,
        "geography_count": len(records),
        "monitoring_feature_count": len(monitoring_geojson["features"]),
        "layer_count": len(layers_payload["layers"]),
        "processed_outputs": sorted(
            str((processed_app_dir / name).relative_to(ROOT)).replace("\\", "/")
            for name in outputs
        ),
        "public_outputs": sorted(
            str((public_data_dir / name).relative_to(ROOT)).replace("\\", "/") for name in outputs
        ),
        "source_refs": {
            "app_layer_config": config_path.relative_to(ROOT).as_posix(),
            "index": index_path.relative_to(ROOT).as_posix(),
            "indicator_trace": trace_path.relative_to(ROOT).as_posix(),
            "geography_lookup": lookup_path.relative_to(ROOT).as_posix(),
            "observations": observations_path.relative_to(ROOT).as_posix(),
            "outlook": outlook_path.relative_to(ROOT).as_posix(),
        },
        "geometry_policy": "centroid_fallback_until_boundary_join",
        "summary_output": summary_output.relative_to(ROOT).as_posix(),
    }
    write_json(summary_output, summary)
    return summary


def build_country_details_payload(records: list[dict[str, object]], *, trace_path: Path) -> dict[str, object]:
    trace = pd.read_csv(trace_path)
    details = {record["geo_code"]: dict(record) for record in records}
    for geo_code, group in trace.groupby("geo_code", sort=True):
        indicators = []
        for row in group.sort_values("dataset_slug", kind="mergesort").to_dict(orient="records"):
            indicators.append(
                {
                    "dataset_slug": row["dataset_slug"],
                    "dataset_name": row["dataset_name"],
                    "pillar": row["pillar"],
                    "latest_year": int(row["latest_year"]),
                    "latest_value": nullable_float(row["latest_value"]),
                    "scoring_value": nullable_float(row.get("scoring_value")),
                    "unit": nullable_text(row.get("unit")),
                    "indicator_score": nullable_float(row["indicator_score"]),
                    "source_row_hash": row["source_row_hash"],
                }
            )
        if geo_code in details:
            details[geo_code]["indicators"] = indicators

    return {
        "schema_version": 1,
        "details": details,
        "source_refs": {
            "indicator_trace": "artifacts/tables/adaptation_gap_indicator_trace.csv",
        },
    }


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def nullable_float(value: object) -> float | None:
    if value is None or pd.isna(value) or value == "":
        return None
    return round(float(value), 4)


def nullable_text(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value)


def main() -> int:
    args = parse_args()
    config_path = ROOT / args.config if not args.config.is_absolute() else args.config
    index_path = ROOT / args.index if not args.index.is_absolute() else args.index
    trace_path = ROOT / args.indicator_trace if not args.indicator_trace.is_absolute() else args.indicator_trace
    lookup_path = (
        ROOT / args.geography_lookup
        if not args.geography_lookup.is_absolute()
        else args.geography_lookup
    )
    observations_path = (
        ROOT / args.observations if not args.observations.is_absolute() else args.observations
    )
    outlook_path = ROOT / args.outlook if not args.outlook.is_absolute() else args.outlook
    processed_app_dir = (
        ROOT / args.processed_app_dir
        if not args.processed_app_dir.is_absolute()
        else args.processed_app_dir
    )
    public_data_dir = (
        ROOT / args.public_data_dir if not args.public_data_dir.is_absolute() else args.public_data_dir
    )
    summary_output = (
        ROOT / args.summary_output if not args.summary_output.is_absolute() else args.summary_output
    )

    summary = export_app_data(
        index_path=index_path,
        trace_path=trace_path,
        lookup_path=lookup_path,
        observations_path=observations_path,
        outlook_path=outlook_path,
        config_path=config_path,
        processed_app_dir=processed_app_dir,
        public_data_dir=public_data_dir,
        summary_output=summary_output,
    )

    print(
        f"Exported app data: geographies={summary['geography_count']}, "
        f"layers={summary['layer_count']}, "
        f"monitoring_features={summary['monitoring_feature_count']}"
    )
    print(f"Wrote processed app data: {processed_app_dir}")
    print(f"Wrote public app data: {public_data_dir}")
    print(f"Wrote summary: {summary_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
