# Patterns Memory

## Context-First Documentation

When creating or updating project state, put the Markdown file under `context/` unless it is a public root entry point like `README.md`.

## Static App Data

The frontend should consume static JSON/GeoJSON exports from `app/public/data/`. Those files should be generated from Python scripts rather than edited manually.
