# Handover

## Current State

The repository is initialized as a context-first GIS/data-science project. The workflow scaffold has passed required-artifact, task-status, and secret checks. No data pipeline, index, model, or app feature has been completed yet.

## How To Validate The Scaffold

```powershell
python scripts/check_required_artifacts.py
python scripts/validate_task_statuses.py
python scripts/check_secrets.py
```

## Next Recommended Work

1. Complete `TASK-001`: profile official datasets and create dataset contracts.
2. Complete `TASK-002`: build the reproducible processed dataset pipeline.
3. Complete `TASK-003`: implement the baseline Adaptation Gap Index.
4. Reassess whether `TASK-004` Outlook modeling is strong enough for the app.

## Known Caveats

- App dependencies are declared but not installed.
- Python dependencies are declared but not installed.
- Official dataset API profiling needs to be rerun through tracked scripts.
- The copied reference workflow kits are intentionally ignored under `context/`.
