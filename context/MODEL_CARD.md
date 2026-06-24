# Model Card

## Model Name

Adaptation Gap Outlook

## Status

Draft baseline complete. The outlook is methodology-ready but app-optional because it is a transparent trend stress test, not an operational prediction.

## Intended Use

Provide a transparent, caveated outlook layer showing where adaptation gaps may widen if recent climate-signal trends continue while capacity indicators remain flat or improve slowly.

## Not Intended For

- emergency management
- direct funding allocation
- claims about individual communities
- operational climate forecasting
- legal or policy determinations without local expert review

## Implemented Baseline

- Input current Adaptation Gap Index from official datasets.
- Fit per-geography, per-indicator linear trends for climate-signal datasets with at least 8 observations.
- Score projected climate-signal values within peer geographies for 2030 and 2050.
- Carry current capacity score forward for `capacity_flat`.
- Move capacity partway toward 100 for `capacity_gradual_improvement`: 5% of the remaining capacity gap by 2030 and 15% by 2050.
- Output row-level caveats, residual spread, and holdout comparison against a naive latest-value baseline.

## Current Artifacts

- `artifacts/tables/adaptation_gap_outlook.csv`
- `artifacts/tables/climate_trend_diagnostics.csv`
- `artifacts/provenance/outlook_summary.json`
- Local ignored run bundle: `artifacts/logs/runs/task-004-outlook-baseline/`

## Evaluation Requirements

Before the outlook appears in the app:

- compare against a naive latest-value or no-change baseline: done
- document split strategy for time-series evaluation: done, last three observations are held out for eligible series
- inspect residuals or forecast errors where historical backtesting is possible: done in summary metrics
- show uncertainty or sensitivity bands: partial, residual spread and row caveats are present; visual bands are not designed yet
- record excluded geographies and sparse-series caveats

## Current Metrics

- Trend series: 86
- Trend geographies: 22
- Backtested series: 86
- Linear beats naive count: 39
- Mean linear holdout MAE: 1.7731
- Mean naive holdout MAE: 2.9953

## Risk Statement

The outlook is a communication layer for data exploration, not a predictive climate model. It can appear as a secondary exploratory layer only if the app makes caveats visible by default.
