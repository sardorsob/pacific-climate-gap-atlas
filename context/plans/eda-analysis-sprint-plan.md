# EDA Analysis Sprint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a script-first exploratory analysis sprint that turns the existing data spine into evidence, story candidates, and app-design requirements.

**Architecture:** Keep notebooks optional and non-authoritative. Put reusable logic in `analysis/eda/`, run it through `scripts/run_eda.py`, and save reportable outputs under `artifacts/tables/`, `artifacts/figures/`, and `artifacts/provenance/`. Keep durable interpretation and task status under `context/`.

**Tech Stack:** Python, pandas, existing project CSV/JSON artifacts, config files, and standard unittest coverage.

---

### Task 1: EDA Sprint Backlog And Scope

**Files:**
- Create: `context/ANALYSIS_BACKLOG.md`
- Modify: `context/TASKS.md`
- Modify: `context/PROJECT.md`

- [ ] Add the analysis backlog with GIS/data-science questions, expected artifacts, and dependency order.
- [ ] Add `TASK-009` as the first executable EDA scaffold task.
- [ ] Add later pending EDA tasks for coverage, driver decomposition, sensitivity, spatial context, trends, monitoring gap, and story synthesis.
- [ ] Mark the current phase as analysis sprint, with app implementation paused until story evidence is stronger.

### Task 2: Script-First EDA Helpers

**Files:**
- Create: `analysis/eda/__init__.py`
- Create: `analysis/eda/coverage.py`
- Create: `analysis/eda/drivers.py`
- Create: `analysis/eda/sensitivity.py`
- Create: `analysis/eda/trends.py`
- Create: `tests/analysis/test_eda.py`

- [ ] Write failing tests for coverage summaries, driver labels, sensitivity ranking, and trend-profile helpers.
- [ ] Implement minimal pandas helpers with small, focused functions.
- [ ] Use comments only for non-obvious blocks, formatted as `# comment`.
- [ ] Keep function outputs deterministic by sorting rows and columns explicitly.

### Task 3: EDA Runner And Artifacts

**Files:**
- Create: `configs/eda.yml`
- Create: `scripts/run_eda.py`
- Create: `artifacts/tables/eda_data_coverage.csv`
- Create: `artifacts/tables/eda_country_drivers.csv`
- Create: `artifacts/tables/index_sensitivity.csv`
- Create: `artifacts/tables/eda_trend_profiles.csv`
- Create: `artifacts/tables/eda_monitoring_gap.csv`
- Create: `artifacts/provenance/eda_summary.json`

- [ ] Write a CLI runner that reads generated project artifacts rather than notebooks.
- [ ] Save every table with a stable filename under `artifacts/tables/`.
- [ ] Save one provenance summary with inputs, outputs, row counts, and caveats.
- [ ] Print a short run summary.

### Task 4: Context Sync And QA

**Files:**
- Create: `context/ANALYSIS_BRIEF.md`
- Modify: `context/DATA_CARD.md`
- Modify: `context/STRUCTURE.md`
- Modify: `context/HANDOVER.md`
- Modify: `context/logs/Progress Log.md`

- [ ] Summarize what the first EDA pass does and does not prove.
- [ ] Index new artifacts and rerun commands in handoff docs.
- [ ] Run unit tests, EDA runner, task status validation, required artifact validation, secret scan, compile check, and diff check.
- [ ] Commit with a task-oriented message and no co-author trailer.
