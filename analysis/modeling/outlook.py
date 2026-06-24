"""Transparent baseline models for the Adaptation Gap Outlook."""

from __future__ import annotations

import pandas as pd


def latest_value_baseline(frame: pd.DataFrame, *, group_col: str, time_col: str, value_col: str) -> pd.DataFrame:
    """Return the latest observed value per group as a no-change baseline."""

    if frame.empty:
        return frame[[group_col, time_col, value_col]].copy()
    ordered = frame.sort_values([group_col, time_col])
    return ordered.groupby(group_col, as_index=False).tail(1)[[group_col, time_col, value_col]]
