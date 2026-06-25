# Analysis Backlog

## Purpose

The project is pausing visual design work until the atlas has a stronger evidence base. This backlog defines the in-depth EDA and GIS-oriented analysis needed before a final app story, layout, and Claude visual-design handoff.

## Current Status

Completed analysis lanes now cover the script-first EDA foundation, GIS context, official-data coverage, indicator forensics, country story labels, rank volatility, spatial typologies, trend/outlook interpretation, and monitoring-gap GIS priorities. Story synthesis and Claude visual handoff are next in `TASK-018`.

## Principles

- Start from analytical questions, not chart ideas.
- Use Python modules and scripts as the source of truth; notebooks are optional review surfaces only.
- Save reportable outputs under `artifacts/` with stable names.
- Preserve caveats when scores depend on sparse data, proxy indicators, or centroid geometry.
- Treat GIS claims carefully while current geometry is centroid fallback rather than boundaries.

## Analysis Lanes

### TASK-009: Script-First EDA Foundation

Question: Can we produce repeatable analysis tables from existing project artifacts without notebooks?

Outputs:
- `configs/eda.yml`
- `scripts/run_eda.py`
- `analysis/eda/*`
- `artifacts/tables/eda_data_coverage.csv`
- `artifacts/tables/eda_coverage_by_geography.csv`
- `artifacts/tables/eda_coverage_by_dataset.csv`
- `artifacts/tables/eda_indicator_forensics.csv`
- `artifacts/tables/eda_indicator_outliers.csv`
- `artifacts/tables/eda_country_drivers.csv`
- `artifacts/tables/eda_country_story_labels.csv`
- `artifacts/tables/index_sensitivity.csv`
- `artifacts/tables/eda_rank_volatility.csv`
- `artifacts/tables/eda_trend_profiles.csv`
- `artifacts/tables/eda_monitoring_gap.csv`
- `artifacts/provenance/eda_summary.json`
- `context/ANALYSIS_BRIEF.md`

### TASK-010: GIS Context Enrichment

Question: What spatial context is needed before we make regional or geographic claims?

Candidate enrichments:
- Pacific subregion labels: Melanesia, Micronesia, Polynesia
- Sovereignty or territory status
- Island group names where useful
- Optional population, land area, coastline, or boundary source if defensible

Outputs:
- `data/external/geography_context.csv`
- `artifacts/provenance/geography_context_sources.json`
- boundary-source decision in `context/DECISIONS.md`

### TASK-011: Data Coverage And Data Desert Atlas

Question: Where does the official data see the Pacific clearly, and where is the evidence thin?

Analyses:
- dataset count by geography
- row count by geography
- first and last observation year
- missing pillar flags
- per-dataset geography coverage
- monitoring-network coverage as its own layer

Outputs:
- `artifacts/tables/eda_coverage_by_geography.csv`
- `artifacts/tables/eda_coverage_by_dataset.csv`
- `artifacts/figures/eda_coverage_rankings.png`

### TASK-012: Indicator-Level Forensics

Question: Which indicators drive the scores, and where might indicator behavior mislead?

Analyses:
- top and bottom geographies per indicator
- latest-year differences
- outlier detection by indicator
- indicators with high leverage on pillar scores
- unit and grain caveats

Outputs:
- `artifacts/tables/eda_indicator_forensics.csv`
- `artifacts/tables/eda_indicator_outliers.csv`
- `context/ANALYSIS_BRIEF.md` update

### TASK-013: Country Driver Decomposition

Question: Why is each geography high, low, or middling on the adaptation gap?

Analyses:
- pressure versus capacity decomposition
- high-pressure plus low-capacity flags
- monitoring-thin and data-thin flags
- short reason labels for app side panels
- country exemplars for story sections

Outputs:
- `artifacts/tables/eda_country_drivers.csv`
- `artifacts/tables/eda_country_story_labels.csv`

### TASK-014: Rank Robustness And Sensitivity

Question: Which rankings are robust, and which are artifacts of weights or one indicator?

Analyses:
- equal-weight baseline ranking
- pressure-heavy and capacity-heavy alternatives
- leave-one-indicator-out rank volatility
- score spread under simple weighting scenarios
- robustness flag by geography

Outputs:
- `artifacts/tables/index_sensitivity.csv`
- `artifacts/tables/eda_rank_volatility.csv`
- `artifacts/figures/eda_rank_sensitivity.png`

### TASK-015: Spatial Typologies And Regional Patterns

Question: Do geographies form useful groups beyond rank order?

Analyses:
- quadrant typology: pressure high/low by capacity high/low
- data coverage typology
- optional clustering if the small sample behaves sensibly
- subregion comparison after GIS context enrichment
- centroid-distance similarity check, with ocean-space caveats

Outputs:
- `artifacts/tables/eda_spatial_typologies.csv`
- `artifacts/tables/eda_subregion_comparisons.csv`

### TASK-016: Trend And Outlook Interpretation

Question: Which trends are meaningful enough to show, and which should stay caveated?

Analyses:
- trend strength by geography and dataset
- trend diagnostics by indicator family
- current gap versus 2030/2050 outlook
- outlook change rankings
- fragile trend flags

Outputs:
- `artifacts/tables/eda_trend_profiles.csv`
- `artifacts/tables/eda_outlook_interpretation.csv`
- `context/MODEL_CARD.md` update

### TASK-017: Monitoring Gap Analysis

Question: Where is monitoring coverage weakest relative to climate pressure and adaptation need?

Analyses:
- monitoring count versus climate pressure
- monitoring count versus adaptation gap
- high-gap low-monitoring quadrants
- monitoring coverage as diagnostic rather than score-only input
- optional normalization after geography context enrichment

Outputs:
- `artifacts/tables/eda_monitoring_gap.csv`
- `artifacts/figures/eda_monitoring_gap_quadrants.png`

### TASK-018: Responsibility Context And Story Synthesis

Question: What is the strongest responsible, careful story the data can support?

Analyses:
- emissions context versus climate pressure
- emissions context versus adaptation gap
- strongest 2-3 narrative arcs
- country exemplars and caveats
- final app layer priority list

Outputs:
- `artifacts/tables/eda_responsibility_context.csv`
- `context/STORY_BRIEF.md`
- `context/CLAUDE_VISUAL_HANDOFF.md`

## Parallelization Plan

- Coverage/data desert and GIS enrichment can run in parallel.
- Indicator forensics and driver decomposition can run in parallel after the current score artifacts are available.
- Sensitivity analysis can run independently from trend/outlook interpretation.
- Story synthesis should wait until the other analysis lanes are reviewed.
