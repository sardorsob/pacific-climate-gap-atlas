# Decisions

## 2026-06-24: Use A Context-First Repository Layout

All durable workflow documents, project state, task status, assumptions, and handoff notes live under `context/`.

Reason: the user wants one explicit context folder as the working memory center for both agents and humans.

## 2026-06-24: Use Adaptation Gap As The Main Frame

The headline is the broader adaptation gap, not only monitoring gaps.

Reason: monitoring is a strong diagnostic layer, but the broader adaptation frame better supports climate signal, stress, and capacity comparisons.

## 2026-06-24: Keep Outlook Modeling Transparent And Baseline-First

The future-facing layer will be framed as an outlook or scenario baseline, not an operational prediction.

Reason: there is unlikely to be enough target-labeled data for a defensible supervised prediction model, but a transparent trend/scenario layer can still add value.

## 2026-06-24: Keep Workflow Kits Local And Ignored

Reference workflow kits are copied under `context/agentic-workflow-kit/` and `context/data-science-agentic-workflow-kit/`, but ignored by Git.

Reason: they are useful local context but should not be pushed with this project.

## 2026-06-24: Parallelize Independent Work And Commit Task-By-Task

Independent tasks should run in parallel when dependencies and file ownership allow it. The orchestrator reviews parallel outputs before accepting them.

Commits should be task-oriented and must not include `Co-authored-by` trailers or assistant/agent authorship credit.

Reason: the user wants fast agentic execution without losing review discipline or clean authorship.

## 2026-06-24: Use PowerShell Fallback For Pacific SDMX CSV Profiling

The dataset profiler first tries Python standard-library HTTP, then falls back to Windows PowerShell `Invoke-WebRequest -UseBasicParsing` when the SDMX endpoint returns `422`.

Reason: the early repo does not have Python dependencies installed, and the official Pacific SDMX endpoint accepted the PowerShell request with the same SDMX CSV accept header.

## 2026-06-24: Prefer Local Raw Cache Before Live Fetching

The processed data pipeline checks `data/raw/official/*.csv` before calling live SDMX URLs. The raw cache is ignored by Git, and manual download filenames are documented in `data/raw/README.md`.

Reason: direct CSV downloads are a practical sprint backup when the official API is slow or client-sensitive, while the pipeline remains reproducible from either raw cache or live source URLs.

## 2026-06-24: Use Latest-Observation Percentile Ranks For Baseline Index

The first Adaptation Gap Index keeps the latest non-missing observation per geography and dataset, ranks each indicator within available Pacific geographies, averages climate/observed-stress ranks into pressure, averages adaptation-capacity ranks into capacity, and rescales pressure minus capacity to 0-100.

Anomaly datasets use absolute anomaly magnitude for scoring while preserving raw values in the trace table.

Reason: this gives us a transparent, auditable baseline quickly without imputation or opaque weighting, while leaving room for sensitivity analysis later.

## 2026-06-24: Treat Outlook As App-Optional Stress Test

The Adaptation Gap Outlook uses simple climate-signal linear trends and capacity scenarios for 2030 and 2050. It is methodology-ready but app-optional, and must not be described as an operational prediction.

Reason: aggregate linear holdout MAE beats naive, but fewer than half of individual trend series beat the naive baseline, so the result is useful for exploration only with visible caveats.

## 2026-06-24: Use Centroid GIS Exports Until Boundary Join Exists

TASK-005 exports app-ready GeoJSON as centroid features with explicit `geometry_status` and `geometry_policy` fields. The app should treat these as centroid or point layers until we add boundary data.

Reason: the official processed data has reliable geography codes and scores, but no tracked polygon boundary source yet. Centroids let the app shell move forward while keeping the geometry limitation visible.

## 2026-06-24: Pause App Design For Script-First EDA

The project will slow down before the visual design pass and run deeper exploratory analysis in Python modules and scripts rather than notebooks as the source of truth.

Reason: the atlas needs an evidence-backed story before Claude or any visual-design pass polishes the interface. Python files keep diffs smaller, artifacts reproducible, and parallel agent work easier to review.

## 2026-06-25: Keep GIS Context Descriptive And Boundary-Neutral

TASK-010 adds `data/external/geography_context.csv` and source notes for Pacific subregion, political status, administering or sovereign authority, and island-group context.

These fields are descriptive only and must not feed Adaptation Gap Index scoring unless a future reviewed methodology explicitly changes that.

Pacific subregions follow UN M49 statistical groupings and should not be framed as cultural or political boundaries. Boundary polygons remain undecided; keep centroid-first mapping until an authoritative boundary source is selected and documented.

Reason: the atlas needs spatial context for GIS exploration, but status labels and regional groupings are politically sensitive and should not be smuggled into the quantitative method.

## 2026-06-25: Treat EDA Story Labels As Descriptive Screens

TASK-012, TASK-013, TASK-014, and TASK-017 produce interpretation tables for story selection: indicator forensics, country story labels, rank volatility, and monitoring-gap priorities.

These outputs guide app copy, layer priority, and exemplar selection. They do not alter the baseline index and must not be described as causal explanations.

Monitoring-gap language should distinguish reported-zero monitoring rows from missing monitoring rows. Missing rows are reporting gaps unless an external source verifies infrastructure absence.

Reason: the current evidence base is strong enough for exploratory story selection but not for causal attribution, definitive rankings, or infrastructure-absence claims.

## 2026-06-25: Gate Outlook Layers With Diagnostic Quality

TASK-016 adds `eda_outlook_interpretation.csv` as display guidance for future-facing layers.

Supported diagnostics can appear as stress-test context. Mixed diagnostics require strong visible caveats. Weak or sparse diagnostics should be withheld from outlook layers.

Reason: the outlook is useful for exploratory contrast, but the diagnostics are too uneven for forecast language or automatic display across every geography.

## 2026-06-27: Add Evidence Fingerprint Divergence As A Planned Secondary Layer

The project will explore Jensen-Shannon divergence as a way to compare official-data evidence profiles across Pacific geographies. The public-facing idea is "evidence fingerprint similarity": which places have similar pressure, capacity, and data-visibility profiles behind their adaptation-gap scores.

JSD is preferred for the interface because it is symmetric, bounded, and easier to explain. KL divergence may be used only as an internal diagnostic after smoothing and missingness review.

The layer must be anchored on a selected geography and must not become a global leaderboard, causal cluster, vulnerability score, or policy-need grouping.

Reason: the idea strengthens the atlas by moving beyond "who ranks high" toward "what kind of gap profile is this," while staying inside the official-data evidence base and avoiding overclaimed modeling.
