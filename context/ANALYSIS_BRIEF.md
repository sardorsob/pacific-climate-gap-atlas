# Analysis Brief

## Status

The project has shifted into an analysis sprint before visual design resumes. `TASK-009` creates the first script-first EDA foundation. It does not finish the story, but it gives us reproducible tables that start separating strong signals from fragile ones.

## Current EDA Outputs

Run:

```powershell
python scripts/run_eda.py --config configs/eda.yml
```

The runner writes:

- `artifacts/tables/eda_data_coverage.csv`
- `artifacts/tables/eda_country_drivers.csv`
- `artifacts/tables/index_sensitivity.csv`
- `artifacts/tables/eda_trend_profiles.csv`
- `artifacts/tables/eda_monitoring_gap.csv`
- `artifacts/provenance/eda_summary.json`

## Early Signals

- The first coverage pass includes 22 geographies. Only one is flagged as thin coverage under the current threshold, so the next coverage task should inspect coverage by dataset and pillar rather than only geography-level totals.
- Country driver labels are currently descriptive. They identify low visible capacity, high pressure, lower relative gap, and mixed-signal geographies, but they should not be treated as causal explanations.
- Rank robustness is a major story risk. In the first weight-sensitivity table, 12 of 22 geographies are labeled fragile, 7 sensitive, and only 3 stable. The atlas should avoid presenting ranks as definitive until sensitivity analysis is deepened.
- The monitoring-gap table flags 4 high-gap plus low-monitoring candidates. This supports the monitoring-gap story lane, but monitoring counts still need normalization or stronger context before making infrastructure claims.
- Trend profiles classify some geographies as stronger and many as mixed. Outlook layers should remain secondary and visibly caveated unless later trend review raises confidence.

## Caveats

- This is descriptive EDA, not causal inference.
- Current GIS geometry is centroid fallback, not boundary polygons.
- Monitoring counts are proxy coverage and are not normalized by population, land area, coastline, station type, or hazard exposure.
- The first sensitivity scenarios are simple pressure-heavy and capacity-heavy stress tests. Later tasks should add leave-one-indicator-out and pillar-specific sensitivity.
- Driver labels are useful for exploration and app copy drafts, not final scientific claims.

## Next Analysis Priorities

1. Add GIS context enrichment so regional claims have a reviewed geography table.
2. Break coverage down by dataset and pillar to find true data deserts.
3. Run indicator-level forensics to identify leverage and outliers.
4. Deepen rank sensitivity with leave-one-indicator-out tests.
5. Decide whether monitoring gap, responsibility mismatch, or rank fragility is the strongest atlas story.
