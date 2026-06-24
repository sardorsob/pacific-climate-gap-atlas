# Data Card

## Dataset Family

Pacific Dataviz Challenge 2026 official datasets, listed in `research/official_datasets_2026.csv`.

## Source Owner

Pacific Data Hub / Pacific Community data infrastructure, as referenced by the official challenge dataset inventory.

## Usage

At least one official dataset is required for the competition. This project targets a multi-dataset official-data spine and may add open external GIS reference files only when they improve map usability or boundary context.

## Initial Coverage Findings

Priority official datasets from the research pass:

| Dataset | Role | Rows | Geographies | Years | Notes |
| --- | --- | ---: | ---: | --- | --- |
| Mean sea surface temperature anomalies | climate signal | 3,696 | 21 | 1850-2025 | strong long time series |
| Mean surface temperature anomalies | climate signal | 3,872 | 22 | 1850-2025 | strong long time series |
| Rainfall anomalies | climate signal | 1,034 | 22 | 1979-2025 | useful climate variability layer |
| Sea level anomalies | climate signal | 651 | 21 | 1993-2023 | central coastal pressure layer |
| Directly affected persons attributed to disasters | observed stress | 174 | 21 | 2005-2023 | sparse but highly relevant |
| Meteorological monitoring network | adaptation capacity | 1,650 | 18 | 1889-2026 | core monitoring-gap layer |
| Power generation | adaptation capacity | 432 | 18 | 2000-2023 | proxy for infrastructure/energy context |
| Fisheries management measures | adaptation capacity | 1,563 | 22 | 1903-2026 | governance/blue-economy capacity signal |
| GHG emissions per capita | responsibility context | 935 | 17 | 1970-2024 | context, not a blame score |

Fourteen geographies appeared across all nine candidate datasets during the initial live API profile:

```text
FJ, FM, KI, MH, NC, NR, PF, PG, PW, SB, TO, TV, VU, WS
```

## Known API Caveats

Some generated SDMX URLs returned `422 Unprocessable Entity` during initial profiling. These should be recorded rather than silently removed. The data pipeline should keep per-dataset status and fallback links.

## Raw Data Policy

- `data/raw/` is immutable and ignored by Git except for documentation.
- `data/interim/` is ignored and can be regenerated.
- `data/processed/` can be selectively tracked when files are small and needed by the app.
- Every reusable processed dataset needs a contract under `data/contracts/`.

## PII / Sensitive Data

No personal-level data is expected. If any dataset contains sensitive or private fields, stop and update this card before continuing.
