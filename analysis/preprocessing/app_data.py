"""Build app-ready atlas data from processed analysis artifacts."""

from __future__ import annotations

from typing import Any

import pandas as pd


GEOGRAPHY_REFERENCE: dict[str, dict[str, float | str]] = {
    "AS": {"name": "American Samoa", "lon": -170.7, "lat": -14.3},
    "CK": {"name": "Cook Islands", "lon": -159.8, "lat": -21.2},
    "FJ": {"name": "Fiji", "lon": 178.1, "lat": -17.7},
    "FM": {"name": "Federated States of Micronesia", "lon": 158.2, "lat": 6.9},
    "GU": {"name": "Guam", "lon": 144.8, "lat": 13.4},
    "KI": {"name": "Kiribati", "lon": -157.4, "lat": 1.9},
    "MH": {"name": "Marshall Islands", "lon": 171.2, "lat": 7.1},
    "MP": {"name": "Northern Mariana Islands", "lon": 145.7, "lat": 15.1},
    "NC": {"name": "New Caledonia", "lon": 165.6, "lat": -21.3},
    "NR": {"name": "Nauru", "lon": 166.9, "lat": -0.5},
    "NU": {"name": "Niue", "lon": -169.9, "lat": -19.1},
    "PF": {"name": "French Polynesia", "lon": -149.4, "lat": -17.7},
    "PG": {"name": "Papua New Guinea", "lon": 145.0, "lat": -6.3},
    "PN": {"name": "Pitcairn", "lon": -128.3, "lat": -24.4},
    "PW": {"name": "Palau", "lon": 134.6, "lat": 7.5},
    "SB": {"name": "Solomon Islands", "lon": 160.2, "lat": -9.6},
    "TK": {"name": "Tokelau", "lon": -171.8, "lat": -9.2},
    "TO": {"name": "Tonga", "lon": -175.2, "lat": -21.2},
    "TV": {"name": "Tuvalu", "lon": 179.2, "lat": -8.5},
    "VU": {"name": "Vanuatu", "lon": 167.7, "lat": -16.2},
    "WF": {"name": "Wallis and Futuna", "lon": -176.2, "lat": -13.8},
    "WS": {"name": "Samoa", "lon": -172.1, "lat": -13.8},
}

SOURCE_REFS = {
    "index": "artifacts/tables/adaptation_gap_index.csv",
    "indicator_trace": "artifacts/tables/adaptation_gap_indicator_trace.csv",
    "outlook": "artifacts/tables/adaptation_gap_outlook.csv",
    "geography_lookup": "data/processed/geography_lookup.csv",
}


def build_geography_records(
    *,
    index: pd.DataFrame,
    lookup: pd.DataFrame,
    outlook: pd.DataFrame,
) -> list[dict[str, Any]]:
    """Join score, coverage, centroid, and outlook fields into app geography records."""

    lookup_by_geo = lookup.set_index("geo_code").to_dict(orient="index") if not lookup.empty else {}
    outlook_by_geo = _build_outlook_lookup(outlook)
    records: list[dict[str, Any]] = []

    for row in index.sort_values("geo_code", kind="mergesort").to_dict(orient="records"):
        geo_code = str(row["geo_code"])
        reference = GEOGRAPHY_REFERENCE.get(geo_code, {"name": geo_code, "lon": None, "lat": None})
        coverage = lookup_by_geo.get(geo_code, {})
        geo_outlook = outlook_by_geo.get(geo_code, {})
        record = {
            "geo_code": geo_code,
            "geography_code": geo_code,
            "name": reference["name"],
            "geography_name": reference["name"],
            "centroid": {"lon": reference["lon"], "lat": reference["lat"]},
            "geometry_status": "centroid_fallback",
            "score_status": _clean_text(row.get("score_status")),
            "adaptation_gap_score": _nullable_float(row.get("adaptation_gap_score")),
            "climate_pressure_score": _nullable_float(row.get("climate_pressure_score")),
            "capacity_score": _nullable_float(row.get("capacity_score")),
            "raw_gap_difference": _nullable_float(row.get("raw_gap_difference")),
            "outlook_2030_flat_gap_score": _lookup_outlook_gap(
                geo_outlook, horizon="2030", scenario="capacity_flat"
            ),
            "outlook_2050_flat_gap_score": _lookup_outlook_gap(
                geo_outlook, horizon="2050", scenario="capacity_flat"
            ),
            "available_pillars": _clean_text(row.get("available_pillars")),
            "missing_pillars": _clean_text(row.get("missing_pillars")),
            "included_indicator_count": _nullable_int(row.get("included_indicator_count")),
            "missingness_flag": _bool(row.get("missingness_flag")),
            "dataset_count": _nullable_int(coverage.get("dataset_count")),
            "row_count": _nullable_int(coverage.get("row_count")),
            "first_year": _nullable_int(coverage.get("first_year")),
            "last_year": _nullable_int(coverage.get("last_year")),
            "datasets": _clean_text(coverage.get("datasets")),
            "outlook": geo_outlook,
            "source_refs": SOURCE_REFS.copy(),
        }
        records.append(record)

    return records


def build_geographies_payload(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Build the app JSON geography payload."""

    return {
        "schema_version": 1,
        "geometry_policy": "centroid_fallback_until_boundary_join",
        "geographies": records,
        "source_refs": SOURCE_REFS.copy(),
    }


def build_atlas_geojson(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Build centroid-backed GeoJSON for immediate map rendering."""

    features = []
    for record in records:
        centroid = record["centroid"]
        if centroid["lon"] is None or centroid["lat"] is None:
            continue

        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [centroid["lon"], centroid["lat"]],
                },
                "properties": {
                    key: value
                    for key, value in record.items()
                    if key not in {"centroid", "source_refs"}
                },
            }
        )

    return {
        "type": "FeatureCollection",
        "schema_version": 1,
        "geometry_policy": "centroid_fallback_until_boundary_join",
        "features": features,
    }


def build_layer_manifest() -> dict[str, Any]:
    """Build layer metadata consumed by the web app."""

    layers = [
        {
            "id": "adaptation_gap",
            "label": "Adaptation gap",
            "type": "centroid_choropleth",
            "source_file": "data/atlas_geographies.geojson",
            "fields": ["adaptation_gap_score", "score_status", "missingness_flag"],
            "legend": "higher_score_means_larger_gap",
        },
        {
            "id": "climate_pressure",
            "label": "Climate pressure",
            "type": "centroid_choropleth",
            "source_file": "data/atlas_geographies.geojson",
            "fields": ["climate_pressure_score"],
            "legend": "higher_score_means_larger_pressure",
        },
        {
            "id": "capacity",
            "label": "Adaptation capacity",
            "type": "centroid_choropleth",
            "source_file": "data/atlas_geographies.geojson",
            "fields": ["capacity_score"],
            "legend": "higher_score_means_more_visible_capacity",
        },
        {
            "id": "outlook_2030_flat",
            "label": "2030 outlook, flat capacity",
            "type": "centroid_choropleth",
            "source_file": "data/atlas_geographies.geojson",
            "fields": ["outlook_2030_flat_gap_score"],
            "legend": "secondary_stress_test_not_prediction",
        },
        {
            "id": "outlook_2050_flat",
            "label": "2050 outlook, flat capacity",
            "type": "centroid_choropleth",
            "source_file": "data/atlas_geographies.geojson",
            "fields": ["outlook_2050_flat_gap_score"],
            "legend": "secondary_stress_test_not_prediction",
        },
        {
            "id": "monitoring_network",
            "label": "Meteorological monitoring",
            "type": "centroid_overlay",
            "source_file": "data/monitoring_network.geojson",
            "fields": ["latest_value", "latest_year"],
            "legend": "latest_station_or_monitoring_count",
        },
    ]
    return {"schema_version": 1, "layers": layers}


def build_monitoring_geojson(observations: pd.DataFrame) -> dict[str, Any]:
    """Build latest meteorological monitoring centroid overlay."""

    monitoring = observations[observations["dataset_slug"] == "meteorological-monitoring-network"].copy()
    if monitoring.empty:
        return {"type": "FeatureCollection", "schema_version": 1, "features": []}

    monitoring["year"] = pd.to_numeric(monitoring["year"], errors="coerce")
    monitoring["value"] = pd.to_numeric(monitoring["value"], errors="coerce")
    latest = (
        monitoring.dropna(subset=["year", "value"])
        .sort_values(["geo_code", "year"], ascending=[True, False], kind="mergesort")
        .drop_duplicates("geo_code", keep="first")
    )

    features = []
    for row in latest.to_dict(orient="records"):
        geo_code = str(row["geo_code"])
        reference = GEOGRAPHY_REFERENCE.get(geo_code)
        if reference is None:
            continue

        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [reference["lon"], reference["lat"]],
                },
                "properties": {
                    "geo_code": geo_code,
                    "geography_code": geo_code,
                    "name": reference["name"],
                    "geography_name": reference["name"],
                    "latest_year": _nullable_int(row.get("year")),
                    "latest_value": _nullable_float(row.get("value")),
                    "unit": _clean_text(row.get("unit")),
                    "geometry_status": "centroid_fallback",
                },
            }
        )

    return {
        "type": "FeatureCollection",
        "schema_version": 1,
        "geometry_policy": "centroid_fallback_until_boundary_join",
        "features": features,
    }


def _build_outlook_lookup(outlook: pd.DataFrame) -> dict[str, dict[str, dict[str, dict[str, Any]]]]:
    lookup: dict[str, dict[str, dict[str, dict[str, Any]]]] = {}
    if outlook.empty:
        return lookup

    for row in outlook.to_dict(orient="records"):
        geo_code = str(row["geo_code"])
        horizon = str(_nullable_int(row.get("horizon")))
        scenario = str(row["scenario"])
        lookup.setdefault(geo_code, {}).setdefault(horizon, {})[scenario] = {
            "outlook_gap_score": _nullable_float(row.get("outlook_gap_score")),
            "projected_climate_pressure_score": _nullable_float(
                row.get("projected_climate_pressure_score")
            ),
            "capacity_projection_score": _nullable_float(row.get("capacity_projection_score")),
            "trend_indicator_count": _nullable_int(row.get("trend_indicator_count")),
            "caveat_notes": _clean_text(row.get("caveat_notes")),
        }

    return lookup


def _clean_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value)


def _lookup_outlook_gap(
    outlook: dict[str, dict[str, dict[str, Any]]], *, horizon: str, scenario: str
) -> float | None:
    scenario_values = outlook.get(horizon, {}).get(scenario, {})
    return _nullable_float(scenario_values.get("outlook_gap_score"))


def _nullable_float(value: Any) -> float | None:
    if value is None or pd.isna(value) or value == "":
        return None
    return round(float(value), 4)


def _nullable_int(value: Any) -> int | None:
    if value is None or pd.isna(value) or value == "":
        return None
    return int(float(value))


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}
