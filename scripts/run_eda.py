"""Run script-first exploratory analysis tables for the atlas story sprint."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.eda.coverage import build_data_coverage, build_monitoring_gap  # noqa: E402
from analysis.eda.drivers import build_country_drivers  # noqa: E402
from analysis.eda.sensitivity import build_rank_volatility, build_weight_sensitivity  # noqa: E402
from analysis.eda.trends import build_trend_profiles  # noqa: E402


DEFAULT_CONFIG = ROOT / "configs" / "eda.yml"
DEFAULT_LOOKUP = ROOT / "data" / "processed" / "geography_lookup.csv"
DEFAULT_OBSERVATIONS = ROOT / "data" / "processed" / "official_observations.csv"
DEFAULT_INDEX = ROOT / "artifacts" / "tables" / "adaptation_gap_index.csv"
DEFAULT_INDICATOR_TRACE = ROOT / "artifacts" / "tables" / "adaptation_gap_indicator_trace.csv"
DEFAULT_TREND_DIAGNOSTICS = ROOT / "artifacts" / "tables" / "climate_trend_diagnostics.csv"
DEFAULT_OUTLOOK = ROOT / "artifacts" / "tables" / "adaptation_gap_outlook.csv"
DEFAULT_TABLE_DIR = ROOT / "artifacts" / "tables"
DEFAULT_SUMMARY = ROOT / "artifacts" / "provenance" / "eda_summary.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--geography-lookup", type=Path, default=DEFAULT_LOOKUP)
    parser.add_argument("--observations", type=Path, default=DEFAULT_OBSERVATIONS)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--indicator-trace", type=Path, default=DEFAULT_INDICATOR_TRACE)
    parser.add_argument("--trend-diagnostics", type=Path, default=DEFAULT_TREND_DIAGNOSTICS)
    parser.add_argument("--outlook", type=Path, default=DEFAULT_OUTLOOK)
    parser.add_argument("--table-dir", type=Path, default=DEFAULT_TABLE_DIR)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY)
    return parser.parse_args()


def run_eda(
    *,
    config_path: Path,
    lookup_path: Path,
    observations_path: Path,
    index_path: Path,
    indicator_trace_path: Path,
    trend_diagnostics_path: Path,
    outlook_path: Path,
    table_dir: Path,
    summary_output: Path,
) -> dict[str, object]:
    if not config_path.exists():
        raise FileNotFoundError(f"EDA config not found: {config_path}")

    lookup = pd.read_csv(lookup_path)
    observations = pd.read_csv(observations_path)
    index = pd.read_csv(index_path)
    indicator_trace = pd.read_csv(indicator_trace_path)
    trend_diagnostics = pd.read_csv(trend_diagnostics_path)
    outlook = pd.read_csv(outlook_path)

    tables = {
        "eda_data_coverage.csv": build_data_coverage(lookup),
        "eda_country_drivers.csv": build_country_drivers(index),
        "index_sensitivity.csv": build_weight_sensitivity(index),
        "eda_rank_volatility.csv": build_rank_volatility(index, indicator_trace),
        "eda_trend_profiles.csv": build_trend_profiles(trend_diagnostics, outlook),
        "eda_monitoring_gap.csv": build_monitoring_gap(index, observations),
    }

    table_dir.mkdir(parents=True, exist_ok=True)
    for file_name, table in tables.items():
        table.to_csv(table_dir / file_name, index=False)

    summary = build_summary(
        config_path=config_path,
        lookup_path=lookup_path,
        observations_path=observations_path,
        index_path=index_path,
        indicator_trace_path=indicator_trace_path,
        trend_diagnostics_path=trend_diagnostics_path,
        outlook_path=outlook_path,
        table_dir=table_dir,
        tables=tables,
        summary_output=summary_output,
    )
    summary_output.parent.mkdir(parents=True, exist_ok=True)
    summary_output.write_text(
        json.dumps(summary, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    return summary


def build_summary(
    *,
    config_path: Path,
    lookup_path: Path,
    observations_path: Path,
    index_path: Path,
    indicator_trace_path: Path,
    trend_diagnostics_path: Path,
    outlook_path: Path,
    table_dir: Path,
    tables: dict[str, pd.DataFrame],
    summary_output: Path,
) -> dict[str, object]:
    coverage = tables["eda_data_coverage.csv"]
    drivers = tables["eda_country_drivers.csv"]
    monitoring = tables["eda_monitoring_gap.csv"]
    sensitivity = tables["index_sensitivity.csv"]
    rank_volatility = tables["eda_rank_volatility.csv"]

    return {
        "schema_version": 1,
        "pipeline_task": "TASK-009",
        "status": "eda_foundation_ready",
        "pipeline_tasks": ["TASK-009", "TASK-014"],
        "config": relative_path(config_path),
        "inputs": {
            "geography_lookup": relative_path(lookup_path),
            "observations": relative_path(observations_path),
            "gap_index": relative_path(index_path),
            "indicator_trace": relative_path(indicator_trace_path),
            "trend_diagnostics": relative_path(trend_diagnostics_path),
            "outlook": relative_path(outlook_path),
        },
        "outputs": {
            file_name: relative_path(table_dir / file_name) for file_name in sorted(tables)
        }
        | {"summary": relative_path(summary_output)},
        "row_counts": {file_name: int(len(table)) for file_name, table in sorted(tables.items())},
        "coverage": {
            "geography_count": int(coverage["geo_code"].nunique()),
            "thin_coverage_count": int((coverage["coverage_tier"] == "thin").sum()),
            "data_desert_count": int(coverage["data_desert_flag"].sum()),
        },
        "driver_labels": drivers["driver_label"].value_counts().sort_index().to_dict(),
        "monitoring_story_count": int(monitoring["monitoring_story_flag"].sum()),
        "rank_fragility": sensitivity["robustness_label"].value_counts().sort_index().to_dict(),
        "rank_volatility": (
            rank_volatility["robustness_label"].value_counts().sort_index().to_dict()
        ),
        "rank_volatility_max_range": int(rank_volatility["rank_range"].max()),
        "caveats": [
            "This is descriptive EDA, not causal inference.",
            "Current GIS geometry is centroid fallback until a boundary source is added.",
            (
                "Monitoring counts are proxy coverage and are not normalized by population "
                "or area yet."
            ),
            "Sensitivity scenarios are simple stress tests for narrative confidence.",
            "Leave-one-indicator rank volatility frames uncertainty, not a new ranking.",
        ],
    }


def relative_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def resolve_path(path: Path) -> Path:
    return ROOT / path if not path.is_absolute() else path


def main() -> int:
    args = parse_args()
    summary = run_eda(
        config_path=resolve_path(args.config),
        lookup_path=resolve_path(args.geography_lookup),
        observations_path=resolve_path(args.observations),
        index_path=resolve_path(args.index),
        indicator_trace_path=resolve_path(args.indicator_trace),
        trend_diagnostics_path=resolve_path(args.trend_diagnostics),
        outlook_path=resolve_path(args.outlook),
        table_dir=resolve_path(args.table_dir),
        summary_output=resolve_path(args.summary_output),
    )
    print(
        f"Built EDA tables: outputs={len(summary['row_counts'])}, "
        f"geographies={summary['coverage']['geography_count']}, "
        f"monitoring_story_count={summary['monitoring_story_count']}"
    )
    print(f"Wrote summary: {relative_path(resolve_path(args.summary_output))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
