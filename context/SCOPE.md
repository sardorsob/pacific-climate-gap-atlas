# Scope

## In Scope

- Build an exploratory GIS-first website for the Pacific Adaptation Gap Atlas.
- Use official Pacific Dataviz Challenge 2026 datasets as the core evidence base.
- Produce a reproducible Python pipeline for dataset profiling, normalization, index construction, and app-ready exports.
- Create a transparent Adaptation Gap Index with visible missingness and caveats.
- Add an optional Adaptation Gap Outlook layer if the baseline projection passes data and evaluation gates.
- Provide methodology, source notes, and handoff documentation.

## Out Of Scope For The Initial Sprint

- Operational disaster forecasting.
- Claims about household-level or community-level risk.
- Private, proprietary, or non-public datasets.
- Heavy supervised ML without a defensible target label and split strategy.
- Real-time data updates unless a simple cached static refresh is enough.
- User accounts, authentication, comments, or collaborative editing.

## Data Scope

Primary source inventory lives in `research/official_datasets_2026.csv`.

Priority datasets:

- mean sea surface temperature anomalies
- mean surface temperature anomalies
- rainfall anomalies
- sea level anomalies
- disaster-affected persons
- meteorological monitoring network
- power generation
- fisheries management measures
- greenhouse gas emissions per capita as responsibility context

## App Scope

The app should open on the map. A short intro can exist, but the first screen must be the exploratory atlas experience.

Core interactions:

- layer toggle for adaptation gap and pillar scores
- country/territory selection
- country detail panel
- source/methodology drawer
- mobile-friendly single-panel flow

## Verification Scope

Before delivery:

- data scripts run from a clean checkout
- generated app data has contracts and row counts
- app builds
- map and panels smoke-test on desktop and mobile viewport
- methodology and source notes are visible
- secret scan passes
