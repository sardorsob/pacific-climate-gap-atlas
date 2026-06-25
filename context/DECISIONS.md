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
