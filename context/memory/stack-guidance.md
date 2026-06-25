# Stack Guidance

## Python

- Use `analysis/` for reusable functions.
- Use `scripts/` for runnable workflows.
- Keep raw data immutable.
- Prefer config-driven runs.

## Web App

- Use React + TypeScript + Vite.
- Use MapLibre GL unless a simpler map library becomes clearly better.
- Keep the first screen map-first.
- Show missingness and caveats in the same interaction path as scores.

## GIS/Data

- Keep geography codes stable across all processed outputs.
- Use GeoJSON for app map layers.
- Keep source metadata attached to app-ready data.
- Treat current geometry as centroid fallback; use point/centroid map layers until a boundary source is chosen.
- Use `scripts/run_eda.py --config configs/eda.yml` to regenerate EDA story tables before visual synthesis.
