# Pacific Adaptation Gap Atlas

An exploratory GIS-first data visualization project for the Pacific Dataviz Challenge 2026 climate-change theme.

The project investigates where Pacific island countries may face the largest mismatch between intensifying climate signals and the systems available to monitor, absorb, or respond to those changes.

## Current Shape

- `research/` contains the competition brief, official dataset inventory, and past-entry research.
- `context/` contains the project workflow, scope, task list, data card, assumptions, decisions, and handoff notes.
- `analysis/` contains Python modules for dataset ingestion, profiling, feature building, gap-index logic, outlook modeling, and script-first EDA.
- `scripts/` contains command-line entry points for reproducible data and validation work.
- `app/` contains the GIS atlas web app scaffold and current visual mockup.

Current analysis outputs include indicator forensics, country story labels, spatial typologies, trend/outlook display guidance, rank-volatility checks, monitoring-gap GIS priorities, and the final TASK-018 story/design briefs. A reviewable visual mockup is committed. `TASK-019` is planned for Evidence Fingerprint Divergence, a possible JSD-based similarity layer over official-data-derived profiles.

## Working Rule

Durable project context lives under `context/`. Root files should be runnable project entry points, package metadata, or repository-level configuration.

## First Commands

```powershell
python scripts/check_required_artifacts.py
python scripts/validate_task_statuses.py
python scripts/check_secrets.py
```

The app and analysis dependencies are declared but may need local installation before full app or analysis runs.
