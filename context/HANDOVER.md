# Handover

## Current State

The repository is initialized as a context-first GIS/data-science project. `TASK-001` through `TASK-004` are complete: nine priority official datasets have been profiled, contracted, cached, normalized, scored into a baseline Adaptation Gap Index, and stress-tested with an app-optional outlook baseline.

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

## How To Rebuild The Gap Index

```powershell
python scripts/build_gap_index.py --config configs/gap_index.yml
```

## How To Rebuild The Outlook

```powershell
python scripts/run_outlook.py --config configs/outlook.yml
```

## Next Recommended Work

1. Complete `TASK-005`: export GIS layer data for the web app after the index exists.
2. Start `TASK-006`: build the GIS atlas app shell once app data exists.
3. Decide whether the outlook appears as a secondary app layer or only in methodology notes.

## Known Caveats

- App dependencies are declared but not installed.
- Python dependencies are declared but not installed.
- The SDMX fetch helper avoids undeclared runtime dependencies, but uses a Windows PowerShell fallback because the endpoint returned `422` to Python standard-library HTTP.
- Raw official CSV cache files under `data/raw/official/` are ignored by Git.
- The gap index is a draft comparative baseline. The app must show indicator counts, trace details, and methodology caveats near the score.
- The outlook baseline is app-optional. Only include it in the interface with visible caveats and row-level notes.
- The copied reference workflow kits are intentionally ignored under `context/`.
