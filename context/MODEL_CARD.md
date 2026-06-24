# Model Card

## Model Name

Adaptation Gap Outlook

## Status

Draft concept. No accepted model has been trained or selected yet.

## Intended Use

Provide a transparent, caveated outlook layer showing where adaptation gaps may widen if recent climate-signal trends continue while capacity indicators remain flat or improve slowly.

## Not Intended For

- emergency management
- direct funding allocation
- claims about individual communities
- operational climate forecasting
- legal or policy determinations without local expert review

## Planned Baseline

- Current Adaptation Gap Index from official datasets.
- Per-geography climate-signal trend estimates where time series are long enough.
- Capacity baseline using latest observed values and simple scenario variants.
- Output bands: lower, moderate, higher gap-widening risk.

## Evaluation Requirements

Before the outlook appears in the app:

- compare against a naive latest-value or no-change baseline
- document split strategy for time-series evaluation
- inspect residuals or forecast errors where historical backtesting is possible
- show uncertainty or sensitivity bands
- record excluded geographies and sparse-series caveats

## Risk Statement

The outlook is a communication layer for data exploration, not a predictive climate model. If it cannot clear evaluation and caveat requirements, it should remain in methodology notes and not appear as a primary app layer.
