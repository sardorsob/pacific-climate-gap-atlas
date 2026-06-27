# Experiments

## Run ID Format

```text
YYYY-MM-DD__HHMM__<short_tag>__<git_shortsha>
```

## Registry Template

```text
## <run_id>
- Task:
- Purpose:
- Config:
- Data version:
- Split:
- Method/model:
- Primary metric:
- Secondary metrics:
- Artifacts:
- Decision:
- Reason:
```

Do not delete failed or rejected runs. Mark them as rejected and explain why.

## 2026-06-24__task-004-outlook-baseline
- Task: TASK-004
- Purpose: Test whether a simple climate-signal trend outlook is defensible enough for a secondary exploratory layer.
- Config: `configs/outlook.yml`
- Data version: `data/processed/official_observations.csv` and `artifacts/tables/adaptation_gap_index.csv`
- Split: Last three observations held out per eligible climate-signal geography/dataset series.
- Method/model: Per-series linear trend for climate indicators; capacity flat or gradual-improvement scenarios.
- Primary metric: Holdout MAE versus latest-value naive baseline.
- Secondary metrics: trend series count, projection rows, residual spread, row caveats.
- Artifacts: `artifacts/tables/adaptation_gap_outlook.csv`, `artifacts/tables/climate_trend_diagnostics.csv`, `artifacts/provenance/outlook_summary.json`
- Decision: Accept as methodology-ready and app-optional.
- Reason: Aggregate linear MAE beats naive MAE, but only 39 of 86 individual series beat naive; use only with visible caveats.

## Planned: task-019-evidence-fingerprint-divergence
- Task: TASK-019
- Purpose: Test whether Jensen-Shannon divergence over official-data-derived evidence profiles adds useful explanatory comparison without becoming a new ranking.
- Config: `configs/eda.yml` plus any future divergence-specific settings.
- Data version: `artifacts/tables/adaptation_gap_indicator_trace.csv`, `artifacts/tables/eda_country_drivers.csv`, `artifacts/tables/eda_monitoring_gap.csv`, and related EDA tables.
- Split: Not applicable; descriptive similarity analysis, not prediction.
- Method/model: Normalize evidence vectors by geography; compute pairwise JSD; optionally compute KL as internal diagnostics after smoothing review.
- Primary metric: Interpretability and stability of nearest-neighbor evidence profiles.
- Secondary metrics: vector coverage, missingness sensitivity, pairwise JSD range, exemplar QA notes.
- Artifacts: planned `eda_evidence_fingerprints.csv`, `eda_pairwise_jsd.csv`, `eda_similarity_neighbors.csv`, `divergence_summary.json`.
- Decision: Pending.
- Reason: Needs implementation and manual QA before it can become an app layer.
