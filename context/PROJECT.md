# Project

## Current Phase

App-data complete; ready for app shell.

## Status

The repository has a committed workflow scaffold, official dataset contracts, a reproducible processed data pipeline, a draft Adaptation Gap Index baseline, an app-optional Adaptation Gap Outlook baseline, and static app-ready JSON/GeoJSON for the Pacific Dataviz Challenge 2026 interactive GIS atlas.

## Working Title

The Pacific Adaptation Gap Atlas

## Current Thesis

Pacific island countries face climate burdens they did little to create, but the size and shape of the adaptation gap varies by geography. The project should help readers explore where climate signals, observed stress, monitoring coverage, and response-capacity proxies appear most out of balance.

## Feature Table

| Area | Status | Notes |
| --- | --- | --- |
| Research source folder | present | `research/` includes brief, official dataset inventory, past winners, and review board |
| Workflow shell | done | all durable project Markdown lives under `context/` |
| Dataset profile | done | `artifacts/tables/dataset_profile.csv` and `data/contracts/*.json` cover nine priority official datasets |
| Data science pipeline | done | `scripts/make_dataset.py` produces normalized observations, geography lookup, app summary, and provenance |
| Adaptation Gap Index | done | `scripts/build_gap_index.py` produces geography scores plus indicator trace |
| Outlook model | done | trend stress-test baseline is methodology-ready and app-optional |
| Static app data | done | `scripts/build_app_data.py` produces public JSON/GeoJSON layer inputs |
| GIS atlas app | planned | React/Vite/MapLibre scaffold will consume static app-ready data |

## Last Session Notes

- Approved structure: context-first monorepo.
- Approved headline: broader adaptation gap, with monitoring as one diagnostic layer.
- Copied reference workflow kits into ignored local context paths.
- Completed `TASK-001` live dataset profiling and contracts for nine priority official datasets.
- Completed `TASK-002` processed data pipeline with local raw-cache support.
- Completed `TASK-003` baseline Adaptation Gap Index and methodology update.
- Completed `TASK-004` Adaptation Gap Outlook baseline and model-card update.
- Completed `TASK-005` app-data export with centroid GeoJSON, layer metadata, country details, and public app copies.
