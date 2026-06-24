"""Draft adaptation-gap index helpers.

The scoring implementation will be completed under TASK-003. This module keeps
the planned interface visible so downstream scripts can be wired deliberately.
"""

from __future__ import annotations

import pandas as pd


def percentile_rank(values: pd.Series, *, higher_is_more_pressure: bool = True) -> pd.Series:
    """Return 0-100 percentile ranks, preserving missing values."""

    ranked = values.rank(pct=True, na_option="keep") * 100
    if higher_is_more_pressure:
        return ranked
    return 100 - ranked
