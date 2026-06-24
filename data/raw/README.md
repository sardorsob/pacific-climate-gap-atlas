# Raw Data

Immutable official source pulls go here. This folder is ignored by Git except for this README and `.gitkeep`.

## Manual Download Cache

For sprint reliability, manually downloaded SDMX CSV files can be placed in `data/raw/official/`.
`scripts/make_dataset.py` will use matching local files before calling the live API.

In the Pacific Data Hub download menu, choose **Filtered data in tabular text (CSV)** for the currently selected indicator. Do not use unfiltered data unless the pipeline is intentionally being changed to ingest a full dataflow with multiple indicators.

| Dataset | Filename |
| --- | --- |
| Mean sea surface temperature anomalies | `mean-sea-surface-temperature-anomalies.csv` |
| Mean surface temperature anomalies | `mean-surface-temperature-anomalies.csv` |
| Rainfall anomalies | `rainfall-anomalies.csv` |
| Sea level anomalies | `sea-level-anomalies.csv` |
| Number of directly affected persons attributed to disasters | `number-of-directly-affected-persons-attributed-to-disasters.csv` |
| Meteorological monitoring network | `meteorological-monitoring-network.csv` |
| Power generation | `power-generation.csv` |
| Fisheries management measures in place and multilateral and bilateral fisheries management arrangements | `fisheries-management-measures-in-place-and-multilateral-and-bilateral-fisheries-management-arrangements.csv` |
| Greenhouse gas emissions per capita | `greenhouse-gas-emissions-per-capita.csv` |

Expected key columns: `GEO_PICT`, `TIME_PERIOD`, and `OBS_VALUE`.
