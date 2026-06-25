# Handover

## Current State

The repository is initialized as a context-first GIS/data-science project. `TASK-001` through `TASK-005` are complete: nine priority official datasets have been profiled, contracted, cached, normalized, scored into a baseline Adaptation Gap Index, stress-tested with an app-optional outlook baseline, and exported into static app-ready JSON/GeoJSON.

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

## How To Rebuild App Data

```powershell
python scripts/build_app_data.py --config configs/app_layers.yml
python scripts/validate_data_contracts.py
```

This writes app data under `data/processed/app/`, mirrors the website-facing files to `app/public/data/`, and records `artifacts/provenance/app_data_summary.json`.

## Next Recommended Work

1. Start `TASK-006`: build the GIS atlas app shell from `app/public/data/`.
2. Decide how visible the outlook caveats should be in the layer controls and side panel.
3. Prepare `TASK-007` source/methodology polish once the app shell exists.

## Known Caveats

- App dependencies are declared but not installed.
- Python dependencies are declared but not installed.
- The SDMX fetch helper avoids undeclared runtime dependencies, but uses a Windows PowerShell fallback because the endpoint returned `422` to Python standard-library HTTP.
- Raw official CSV cache files under `data/raw/official/` are ignored by Git.
- The gap index is a draft comparative baseline. The app must show indicator counts, trace details, and methodology caveats near the score.
- The outlook baseline is app-optional. Only include it in the interface with visible caveats and row-level notes.
- TASK-005 GIS exports use centroid fallback geometry, not island boundaries. Treat layers as centroid/point maps until boundary data is added.
- The copied reference workflow kits are intentionally ignored under `context/`.
