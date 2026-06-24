"""Dataset profiling helpers for Pacific Data Hub SDMX CSV responses."""

from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
import re
import unicodedata

import pandas as pd


MISSING_TOKENS = {"", "nan", "none", "null", "na", "n/a"}


@dataclass(frozen=True)
class DatasetProfile:
    """Coverage and schema summary for one official dataset."""

    name: str
    slug: str
    pillar: str
    story_role: str
    status: str
    row_count: int
    geography_count: int
    year_start: int | None
    year_end: int | None
    value_count: int
    missing_value_count: int
    missing_value_pct: float | None
    geography_codes: list[str]
    geography_column: str | None
    time_column: str | None
    value_column: str | None
    columns: list[str]
    official_url: str
    sdmx_csv_api_url: str
    caveat_notes: str


def slugify(value: str) -> str:
    """Return a stable filename-safe slug."""

    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", normalized.lower()).strip("-")
    return slug or "dataset"


def profile_csv_text(
    *,
    name: str,
    pillar: str,
    story_role: str,
    official_url: str,
    sdmx_csv_api_url: str,
    csv_text: str,
) -> DatasetProfile:
    """Profile an SDMX CSV response body."""

    if not csv_text.strip():
        return error_profile(
            name=name,
            pillar=pillar,
            story_role=story_role,
            official_url=official_url,
            sdmx_csv_api_url=sdmx_csv_api_url,
            status="empty_response",
            caveat_notes="API response was empty.",
        )

    try:
        frame = pd.read_csv(StringIO(csv_text), dtype=str, keep_default_na=False)
    except Exception as exc:  # pragma: no cover - exact parser errors vary by pandas version
        return error_profile(
            name=name,
            pillar=pillar,
            story_role=story_role,
            official_url=official_url,
            sdmx_csv_api_url=sdmx_csv_api_url,
            status="parse_error",
            caveat_notes=f"Could not parse CSV response: {exc}",
        )

    return profile_frame(
        name=name,
        pillar=pillar,
        story_role=story_role,
        official_url=official_url,
        sdmx_csv_api_url=sdmx_csv_api_url,
        frame=frame,
    )


def profile_frame(
    *,
    name: str,
    pillar: str,
    story_role: str,
    official_url: str,
    sdmx_csv_api_url: str,
    frame: pd.DataFrame,
) -> DatasetProfile:
    """Profile an already-loaded dataframe."""

    columns = [str(column) for column in frame.columns]
    row_count = int(len(frame))
    geography_column = _pick_column(columns, preferred=["GEO_PICT"], contains=["GEO"])
    time_column = _pick_column(columns, preferred=["TIME_PERIOD", "TIME", "YEAR"], contains=["TIME", "YEAR"])
    value_column = _pick_column(columns, preferred=["OBS_VALUE", "VALUE"], contains=["VALUE"])

    geography_codes = _unique_non_missing(frame[geography_column]) if geography_column else []
    year_start, year_end = _year_range(frame[time_column]) if time_column else (None, None)
    value_count, missing_value_count, missing_value_pct = _value_coverage(frame, value_column)

    caveats = _build_caveats(
        row_count=row_count,
        geography_column=geography_column,
        time_column=time_column,
        value_column=value_column,
        missing_value_count=missing_value_count,
        missing_value_pct=missing_value_pct,
    )

    return DatasetProfile(
        name=name,
        slug=slugify(name),
        pillar=pillar,
        story_role=story_role,
        status="ok",
        row_count=row_count,
        geography_count=len(geography_codes),
        year_start=year_start,
        year_end=year_end,
        value_count=value_count,
        missing_value_count=missing_value_count,
        missing_value_pct=missing_value_pct,
        geography_codes=geography_codes,
        geography_column=geography_column,
        time_column=time_column,
        value_column=value_column,
        columns=columns,
        official_url=official_url,
        sdmx_csv_api_url=sdmx_csv_api_url,
        caveat_notes=" ".join(caveats),
    )


def error_profile(
    *,
    name: str,
    pillar: str,
    story_role: str,
    official_url: str,
    sdmx_csv_api_url: str,
    status: str,
    caveat_notes: str,
) -> DatasetProfile:
    """Build a profile row for missing or failed sources."""

    return DatasetProfile(
        name=name,
        slug=slugify(name),
        pillar=pillar,
        story_role=story_role,
        status=status,
        row_count=0,
        geography_count=0,
        year_start=None,
        year_end=None,
        value_count=0,
        missing_value_count=0,
        missing_value_pct=None,
        geography_codes=[],
        geography_column=None,
        time_column=None,
        value_column=None,
        columns=[],
        official_url=official_url,
        sdmx_csv_api_url=sdmx_csv_api_url,
        caveat_notes=caveat_notes,
    )


def profile_to_csv_row(profile: DatasetProfile, *, generated_at_utc: str) -> dict[str, object]:
    """Convert a profile to a flat CSV row."""

    return {
        "name": profile.name,
        "slug": profile.slug,
        "pillar": profile.pillar,
        "story_role": profile.story_role,
        "status": profile.status,
        "row_count": profile.row_count,
        "geography_count": profile.geography_count,
        "year_start": "" if profile.year_start is None else profile.year_start,
        "year_end": "" if profile.year_end is None else profile.year_end,
        "value_count": profile.value_count,
        "missing_value_count": profile.missing_value_count,
        "missing_value_pct": ""
        if profile.missing_value_pct is None
        else round(profile.missing_value_pct, 4),
        "geography_column": profile.geography_column or "",
        "time_column": profile.time_column or "",
        "value_column": profile.value_column or "",
        "geography_codes": " ".join(profile.geography_codes),
        "caveat_notes": profile.caveat_notes,
        "official_url": profile.official_url,
        "sdmx_csv_api_url": profile.sdmx_csv_api_url,
        "profiled_at_utc": generated_at_utc,
    }


def profile_to_contract(profile: DatasetProfile, *, generated_at_utc: str) -> dict[str, object]:
    """Convert a profile to a JSON-serializable data contract."""

    return {
        "name": profile.name,
        "slug": profile.slug,
        "pillar": profile.pillar,
        "story_role": profile.story_role,
        "status": profile.status,
        "generated_at_utc": generated_at_utc,
        "source": {
            "provider": "Pacific Data Hub / Pacific Community",
            "official_url": profile.official_url,
            "sdmx_csv_api_url": profile.sdmx_csv_api_url,
        },
        "coverage": {
            "row_count": profile.row_count,
            "geography_count": profile.geography_count,
            "geography_codes": profile.geography_codes,
            "year_range": {"start": profile.year_start, "end": profile.year_end},
            "value_count": profile.value_count,
            "missing_value_count": profile.missing_value_count,
            "missing_value_pct": profile.missing_value_pct,
        },
        "schema": {
            "columns": profile.columns,
            "geography_column": profile.geography_column,
            "time_column": profile.time_column,
            "value_column": profile.value_column,
        },
        "caveat_notes": profile.caveat_notes,
    }


def _pick_column(
    columns: list[str], *, preferred: list[str], contains: list[str]
) -> str | None:
    upper_lookup = {column.upper(): column for column in columns}
    for candidate in preferred:
        if candidate.upper() in upper_lookup:
            return upper_lookup[candidate.upper()]

    for token in contains:
        token_upper = token.upper()
        for column in columns:
            if token_upper in column.upper():
                return column

    return None


def _unique_non_missing(series: pd.Series) -> list[str]:
    values = {
        text
        for text in (str(value).strip() for value in series.tolist())
        if text and text.lower() not in MISSING_TOKENS
    }
    return sorted(values)


def _year_range(series: pd.Series) -> tuple[int | None, int | None]:
    years = pd.to_numeric(series, errors="coerce").dropna()
    if years.empty:
        return None, None

    return int(years.min()), int(years.max())


def _value_coverage(frame: pd.DataFrame, value_column: str | None) -> tuple[int, int, float | None]:
    row_count = int(len(frame))
    if not value_column:
        return 0, row_count, 1.0 if row_count else None

    numeric_values = pd.to_numeric(frame[value_column], errors="coerce")
    value_count = int(numeric_values.notna().sum())
    missing_value_count = row_count - value_count
    missing_value_pct = None if row_count == 0 else missing_value_count / row_count
    return value_count, missing_value_count, missing_value_pct


def _build_caveats(
    *,
    row_count: int,
    geography_column: str | None,
    time_column: str | None,
    value_column: str | None,
    missing_value_count: int,
    missing_value_pct: float | None,
) -> list[str]:
    caveats: list[str] = []

    if row_count == 0:
        caveats.append("No data rows were returned.")
    if not geography_column:
        caveats.append("No geography column was detected.")
    if not time_column:
        caveats.append("No time column was detected.")
    if not value_column:
        caveats.append("No observation value column was detected.")
    if missing_value_count == 1:
        caveats.append("One value is missing.")
    elif missing_value_count > 1 and missing_value_pct is not None:
        caveats.append(f"{missing_value_count} values are missing ({missing_value_pct:.1%}).")

    return caveats
