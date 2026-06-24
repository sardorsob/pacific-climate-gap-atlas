# Handover

## Current State

The repository is initialized as a context-first GIS/data-science project. `TASK-001` and `TASK-002` are complete: nine priority official datasets have been profiled, contracted, cached, normalized, and exported into processed app-ready metadata.

## How To Validate The Scaffold

```powershell
python scripts/check_required_artifacts.py
python scripts/validate_task_statuses.py
python scripts/check_secrets.py
```

## How To Rebuild The Dataset Profile

```powershell
python scripts/profile_datasets.py --config configs/datasets.yml
```

If `python` is not on PATH inside Codex Desktop, use the bundled runtime shown by `load_workspace_dependencies`.

## How To Rebuild Processed Data

```powershell
python scripts/make_dataset.py --config configs/datasets.yml
```

The script uses `data/raw/official/*.csv` first. If you manually download official SDMX CSV files, use the filenames listed in `data/raw/README.md`.

## Next Recommended Work

1. Complete `TASK-003`: implement the baseline Adaptation Gap Index.
2. Reassess whether `TASK-004` Outlook modeling is strong enough for the app.
3. Complete `TASK-005`: export GIS layer data for the web app after the index exists.

## Known Caveats

- App dependencies are declared but not installed.
- Python dependencies are declared but not installed.
- The SDMX fetch helper avoids undeclared runtime dependencies, but uses a Windows PowerShell fallback because the endpoint returned `422` to Python standard-library HTTP.
- Raw official CSV cache files under `data/raw/official/` are ignored by Git.
- The copied reference workflow kits are intentionally ignored under `context/`.
