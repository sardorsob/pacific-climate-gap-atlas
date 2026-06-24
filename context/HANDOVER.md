# Handover

## Current State

The repository is initialized as a context-first GIS/data-science project. `TASK-001` is complete: nine priority official datasets have been live-profiled, with a profile table under `artifacts/tables/` and JSON contracts under `data/contracts/`.

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

## Next Recommended Work

1. Complete `TASK-002`: build the reproducible processed dataset pipeline.
2. Complete `TASK-003`: implement the baseline Adaptation Gap Index.
3. Reassess whether `TASK-004` Outlook modeling is strong enough for the app.

## Known Caveats

- App dependencies are declared but not installed.
- Python dependencies are declared but not installed.
- The dataset profiler avoids undeclared runtime dependencies, but uses a Windows PowerShell fallback because the SDMX endpoint returned `422` to Python standard-library HTTP.
- The copied reference workflow kits are intentionally ignored under `context/`.
