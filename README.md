# Pacific Adaptation Gap Atlas

An exploratory GIS-first data visualization project for the Pacific Dataviz Challenge 2026 climate-change theme.

The project investigates where Pacific island countries may face the largest mismatch between intensifying climate signals and the systems available to monitor, absorb, or respond to those changes.

## Current Shape

- `research/` contains the competition brief, official dataset inventory, and past-entry research.
- `context/` contains the project workflow, scope, task list, data card, assumptions, decisions, and handoff notes.
- `analysis/` contains Python modules for dataset ingestion, profiling, feature building, gap-index logic, and outlook modeling.
- `scripts/` contains command-line entry points for reproducible data and validation work.
- `app/` contains the planned GIS atlas web app scaffold.

## Working Rule

Durable project context lives under `context/`. Root files should be runnable project entry points, package metadata, or repository-level configuration.

## First Commands

```powershell
python scripts/check_required_artifacts.py
python scripts/validate_task_statuses.py
python scripts/check_secrets.py
```

The app and analysis dependencies are declared but not installed in this scaffold commit.
