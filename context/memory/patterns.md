# Patterns Memory

## Context-First Documentation

When creating or updating project state, put the Markdown file under `context/` unless it is a public root entry point like `README.md`.

## Static App Data

The frontend should consume static JSON/GeoJSON exports from `app/public/data/`. Those files should be generated from Python scripts rather than edited manually.

## Script-First EDA

Use Python modules under `analysis/eda/` and `scripts/run_eda.py` for exploratory analysis that feeds the story. Save durable tables under `artifacts/tables/` and keep interpretation/caveats in `context/`.

## Dataviz Inspiration Audit

Use `context/DATAVIZ_INSPIRATION_AUDIT.md` before visual critique or mockup iteration.

Reusable patterns:

- full-bleed map as the primary evidence surface,
- compact edge controls for layers and source/method access,
- selected geography as the anchor for comparison,
- compact evidence strips in country panels,
- direct labels and leader lines for guided claims,
- motion only when it reveals, compares, focuses, or re-encodes evidence.

Avoid copying reference identities, palettes, layouts, or iconic stripe treatments.
