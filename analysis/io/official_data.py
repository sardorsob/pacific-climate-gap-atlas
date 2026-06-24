"""Helpers for reading the official dataset inventory."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class OfficialDataset:
    """One row from the official 2026 dataset inventory."""

    name: str
    story_role: str
    official_url: str
    sdmx_csv_api_url: str


def read_official_inventory(path: Path) -> list[OfficialDataset]:
    """Read `research/official_datasets_2026.csv` into typed records."""

    frame = pd.read_csv(path)
    required = {"name", "story_role", "official_url", "sdmx_csv_api_url"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Official inventory is missing columns: {sorted(missing)}")

    return [
        OfficialDataset(
            name=str(row["name"]),
            story_role=str(row["story_role"]),
            official_url="" if pd.isna(row["official_url"]) else str(row["official_url"]),
            sdmx_csv_api_url=""
            if pd.isna(row["sdmx_csv_api_url"])
            else str(row["sdmx_csv_api_url"]),
        )
        for _, row in frame.iterrows()
    ]
