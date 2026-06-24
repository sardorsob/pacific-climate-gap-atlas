# Pacific Dataviz Challenge 2026 Research Brief

Prepared: 2026-06-24

## Bottom Line

The 2026 theme is **climate change**. The strongest concept is not another generic climate dashboard; it is an **adaptation gap atlas** for Pacific islands: where climate signals are intensifying, where people/coasts/economies are exposed, and where response capacity or monitoring coverage is thin.

Working title: **The Pacific Adaptation Gap Atlas**

Core claim: Pacific islands did little to create the climate burden, but their exposure, data coverage, and response capacity vary sharply. A useful dataviz can help users move from "climate change is happening" to "what is at risk, what is being measured, and what action capacity exists."

## Deadline And Eligibility

- The website shows the 2026 challenge runs **1 June-31 August 2026** and the timeline lists **August 31, 2026** as applications closed.
- The rules PDF is more precise: the Challenge runs from **1 June 2026, 12:00 pm, to 31 August 2026, 11:00 pm, Fiji time**.
- Because the legal rule says Fiji time, treat the safe US Pacific deadline as **before Monday, August 31, 2026 at 4:00 am PDT**. Do not rely on the last hours.
- Main competition is open to individuals or teams, amateur or professional, any age, nationality, country, or territory.
- A submission must use **at least one official dataset**. Additional open datasets are allowed.
- All data sources must be listed.
- The dataviz must be public.
- Static entries must be high-quality PDF/JPEG/PNG and max 100 MB.
- Interactive entries must be publicly accessible by URL and remain accessible until at least **31 August 2029**.
- English or French is required for forms, dataviz, and explanations. Other languages can be added if the entry is still fully available in English and/or French.
- AI can support code, narrative, or visuals, but must not replace the core creative or analytical process.

Official sources:

- [Pacific Dataviz Challenge 2026 homepage](https://pacificdatavizchallenge.org/)
- [2026 complete rules PDF](https://pacificdatavizchallenge.org/sites/default/files/2026-05/Pacific-Dataviz-Challenge-2026-rules-reglement.pdf)
- [Application form](https://pacificdatavizchallenge.org/form/application-form)
- [Pacific Data Hub](https://pacificdata.org/)
- [Pacific Data Hub .Stat Explorer](https://stats.pacificdata.org/)
- [Pacific Data Hub .Stat API docs](https://docs.pacificdata.org/dotstat/api)

## Official 2026 Datasets

The scrape found **27 official datasets**. Full links and generated SDMX API CSV URLs are in `official_datasets_2026.csv`.

Climate exposure / observed change:

- Mean sea surface temperature anomalies
- Mean surface temperature anomalies
- Rainfall anomalies
- Sea level anomalies
- Climate altering land cover index
- Coastline
- Meteorological monitoring network
- Meteorological monitoring network - disaggregated

Pressure / context:

- Greenhouse gas emissions per capita
- Population growth

Impacts:

- Crop yield
- Crop yield - disaggregated
- Livestock yield
- Livestock yield - disaggregated
- Tourist arrivals
- Tourist arrivals - disaggregated
- Red List Index
- Number of directly affected persons attributed to disasters
- Direct disaster economic loss
- Tuberculosis incidence per 100,000 population
- Proportion of population using safely managed drinking water services

Response or capacity:

- Environmental taxes
- Environmental taxes - disaggregated
- Renewable energy share in the total final energy consumption
- Power generation
- Power generation - disaggregated
- Fisheries management measures in place and multilateral and bilateral fisheries management arrangements

Practical data access note:

- Explorer URLs can be mapped to the live SDMX v2 CSV API.
- Example that returned CSV:
  `https://stats-sdmx-disseminate.pacificdata.org/rest/v2/data/dataflow/SPC/DF_CLIMATE_CHANGE/1.0/A.SEA_LVL.?dimensionAtObservation=AllDimensions`
- Use request header: `Accept: application/vnd.sdmx.data+csv;version=2.0`
- The v2 API accepted `dimensionAtObservation`; it rejected the underscore version.

## Recommended Data Strategy

### Recommendation 1: The Pacific Adaptation Gap Atlas

Use this if the goal is maximum usefulness and novelty.

Official datasets to combine:

- Sea level anomalies
- Mean sea surface temperature anomalies
- Mean surface temperature anomalies
- Rainfall anomalies
- Coastline
- Population growth
- Directly affected persons attributed to disasters
- Direct disaster economic loss
- Meteorological monitoring network / disaggregated
- Renewable energy share
- Power generation / disaggregated
- Environmental taxes / disaggregated
- Fisheries management measures

Potential open-data additions:

- NASA/IPCC sea-level projections or NASA Sea Level Change data
- NOAA or IBTrACS tropical cyclone tracks
- OpenStreetMap critical infrastructure: hospitals, schools, ports, airports
- WorldPop or GHSL population grids
- Digital elevation or coastal low-elevation-zone data
- World Database on Protected Areas, if using marine/coastal protection

Why it can win:

- It satisfies the official dataset requirement many times over.
- It speaks to climate action, not just climate measurement.
- It can be useful to policymakers, journalists, students, and local advocates.
- It creates an original structure: **signal -> exposure -> monitoring -> response**.
- It gives you a defensible reason for every dataset included.

Artifact shape:

- Scrollytelling web app with a map-first opening.
- Country/island cards showing climate signals, exposure, monitoring coverage, and response indicators.
- A "where to look first" index that ranks countries/territories by adaptation-gap patterns, not by blame.
- Mobile path: one country card at a time, small-multiple sparklines, tap-to-expand methods/sources.

Risk:

- Data harmonization may be messy. The plan should start with a tight subset of countries with enough observations, then expand if coverage allows.

### Recommendation 2: Blue Economy Stress Test

Official datasets:

- Sea surface temperature anomalies
- Rainfall anomalies
- Sea level anomalies
- Tourist arrivals
- Fisheries management measures
- Red List Index
- Coastline
- Power generation / renewable energy

Potential open-data additions:

- NOAA Coral Reef Watch
- Global Fishing Watch
- Protected areas and EEZ boundaries
- Cruise/flight arrivals if available as open data

Why it is strong:

- Climate impacts become tangible through tourism, fisheries, biodiversity, and coastlines.
- The story can be visually distinctive without becoming decorative.

Risk:

- More dependent on external datasets; scope could drift.

### Recommendation 3: Climate-Smart Food, Water, And Health

Official datasets:

- Rainfall anomalies
- Surface temperature anomalies
- Crop yield
- Livestock yield
- Drinking water services
- Population growth
- Disaster affected persons / economic loss
- Tuberculosis incidence

Why it is useful:

- It tells a human story about climate stress on basics: food, water, and health.
- It can be built as a tight explanatory report if time gets short.

Risk:

- Past entries already covered food, health, water, and inequality themes heavily. It must avoid feeling like a familiar dashboard.

### Recommendation 4: The Observation Desert

Official datasets:

- Meteorological monitoring network / disaggregated
- Climate anomalies
- Disaster affected persons
- Direct disaster economic loss
- Population growth

Why it is novel:

- It asks: where are risks high but monitoring thin?
- It is a meta-story about climate knowledge infrastructure, which is useful and underused.

Risk:

- It needs careful framing so it does not imply absence of monitoring equals absence of local knowledge.

## Five-Day Catch-Up Sprint

Day 1: Pick one thesis and prove the data pipeline.

- Choose Recommendation 1 unless data coverage collapses.
- Download 4-6 official datasets through the SDMX API or Explorer CSV.
- Build a country/territory key and confirm which geographies overlap.
- Produce one ugly but honest table: country, years covered, latest values, missingness.

Day 2: Find the story shape.

- Make three rough views: map, time trend, and country card.
- Decide the primary ranking/index.
- Write the problem statement in 150 words.

Day 3: Build the main experience.

- Implement the opening map and country cards.
- Add direct labels and source notes.
- Make a mobile version early.

Day 4: Add novelty and usefulness.

- Add "what this means" annotations.
- Add methodology and caveats.
- Add one exportable/shareable static summary.

Day 5: Polish and submit-dry-run.

- Test every link, mobile viewport, contrast, keyboard/focus, and data source citation.
- Host the interactive version.
- Make sure the URL will remain accessible through **31 August 2029**.
- Fill the submission form draft before the final day.

## Past Winner Patterns

The scrape shows winners tend to do at least one of these:

- Use a strong human or civic question, not just a dataset tour.
- Use a memorable visual metaphor or narrative frame.
- Keep the subject Pacific-specific instead of globally generic.
- Make source/methodology visible.
- Avoid equal-weight dashboard clutter.
- Interactive winners often feel like guided stories or polished tools.
- Static winners often win through a single strong visual idea.

For 2026, a generic "climate dashboard" will likely blend in. A **diagnostic atlas** with a clear usefulness claim should stand out more.

## Past Winners And Highly Commended Links

| Year | Group | Prize/type | Title | Creator | Country | Link |
|---|---|---|---|---|---|---|
| 2025 | Open | Interactive | Paying the Heaviest of the Carbon Debt Never Incurred | Nur Adhyaksa Hamid | Indonesia | [work](https://hnuradhyaksa.github.io/post/pacific-dataviz-2025) |
| 2025 | Open | Static | Echoes of the unprotected sea | Eduardo España | Spain | [work](https://pacificdatavizchallenge.org/sites/default/files/Echoes%20Pacific%20Data%20-%20Eduardo%20Espana.pdf) |
| 2025 | Pacific | Interactive | Blue Paradigm | Eunice Rigo | Australia | [work](https://blue-paradigm.org/) |
| 2025 | Pacific | Static | when our waste suffocate the ocean | Sarah MOUNIAMA | New Caledonia | [work](https://pacificdatavizchallenge.org/sites/default/files/Dataviz%20-%20MOUNIAMA%20Sarah%202025.pdf) |
| 2025 | Pacific | Highly Commended | Visualising Digital Access Across the Blue Pacific | Crispin Laka | Solomon Islands | [work](https://2025-dataviz-challenge-harptreem.replit.app/) |
| 2025 | Pacific Youth | Interactive | The Silence of Mother Whale | Pélagie Sivitongo | New Caledonia | [work](https://ninapolodesign.wixsite.com/pelagiedataviz) |
| 2025 | Pacific Youth | Static | Education in the Pacific | Inès Reboul | New Caledonia | [work](https://pacificdatavizchallenge.org/sites/default/files/REBOUL%20INES-DATAVIZCHALLENGE.pdf) |
| 2025 | Pacific Youth | Highly Commended | Resource & Economic Development: Tourism in Fiji | Lusiana Boutu & Elia Komaitoga | Fiji | [work](https://arcg.is/1yeju91) |
| 2024 | Interactive Dataviz | 1st Prize | Women in the Pacific | Yan Holtz | France | [work](https://holtzy.github.io/pacific-challenge/) |
| 2024 | Interactive Dataviz | 2nd Prize | Blooming: Exploring Poverty in the Pacific Region | Kristin Baumann | Germany | [work](https://blooming-pacific.kristin-baumann.com/) |
| 2024 | Interactive Dataviz | 3rd Prize | A Tale of Two Futures: Gender Inequality in New Caledonia | Thalya Lim | United Kingdom | [work](https://public.tableau.com/views/ATaleofTwoFuturesGenderInequalityinNewCaledonia/ATaleOfTwoFutures?:language=en-GB&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) |
| 2024 | Static Dataviz | 1st Prize | Bruised petals, the frightening scars of violence against women | Alessia Musio | Italy | [work](https://pacificdatavizchallenge.org/sites/default/files/Pacific_Dataviz_Challenge_2024_300_6.jpg) |
| 2024 | Static Dataviz | 2nd Prize | De l'enfance à la vieillesse | Estibaliz Legarreta Gallo | France | [work](https://pacificdatavizchallenge.org/sites/default/files/De%20lenfance%20a%20la%20vieillesse_6.pdf) |
| 2024 | Static Dataviz | 3rd Prize | Trends in gender equality of the working population of Tonga | Ted du Bois | Netherlands | [work](https://pacificdatavizchallenge.org/sites/default/files/Trends%20in%20gender%20equality%20of%20the%20working%20population%20of%20Tonga_TdB_2024_vers.6.4.5_1.3_6.pdf) |
| 2024 | Special | Youth | Fighting Cancer in New Caledonia: Gender gap | Eliott Libner | Canada | [work](https://pacificdatavizchallenge.org/sites/default/files/LIBNER_Pacific_Dataviz_Challenge_2024_8.pdf) |
| 2024 | Special | Pacific | Briser le silence, libérer la parole | Fiona Umpa | New Caledonia | [work](https://app.powerbi.com/view?r=eyJrIjoiMDQxMDc4YzEtNzMyYS00NzUxLWFjMTctZmI0M2NhNDUzNjc3IiwidCI6IjlmOTQ5MTYzLTU0ZjAtNDZiNS04OTM2LTY2YzhmNTUwNGQyYyIsImMiOjEwfQ%3D%3D) |
| 2023 | Interactive Dataviz | 1st Prize | Food In Paradise | Ricardo Tranquilli Navarro | Spain | [work](https://app.powerbi.com/view?r=eyJrIjoiNmYzYmE2MGItZWRlOS00MGQwLWI4ZjEtYTJhOWM0ZTNiOGJhIiwidCI6IjA3N2I3NjZiLTYxZjAtNGU3Yy05MzczLTkyODgzMmFhOWZlZiIsImMiOjh9) |
| 2023 | Interactive Dataviz | 2nd Prize | Carbs on the Coast | Qingyue Li | United States | [work](https://public.tableau.com/app/profile/qingyue.li8346/viz/CarbsontheCoast/Dashboard2) |
| 2023 | Interactive Dataviz | 3rd Prize | Inflation, a health risk in New Caledonia | Julien Ayral | France | [work](https://app.powerbi.com/view?r=eyJrIjoiNzMzZTNhY2QtMzVmMC00MmIxLWE5MWYtM2U1Y2FiNWUxOWI5IiwidCI6ImVmODY2Y2IzLTVlZDktNDkwYy1hNzYxLTkwYzNkZGFlZTY0ZSIsImMiOjh9&pageName=ReportSection0810aec87a32558cd088) |
| 2023 | Static Dataviz | Unique Prize | 2022 assessment of the Caledonian fruit and vegetable market | Caroline Cailleton | New Caledonia | [work](https://pacific-community.gitlab.io/pacific-data-hub/pacific-data-viz/assets/img/2023/static_entries/Poster%20DataViz%20challenge%202023%20CC.PNG) |
| 2022 | Others | 3rd Prize | Cook Islands Terestrial Protected Areas | Pacific Standard Time Studio | Cook Islands | [work](https://earth.google.com/earth/d/1e8A3HlZgTZ4svjjfodEO1FomfFOwZYzS?usp=sharing) |
| 2022 | Others | 1st Prize | Republic of China Exports to Melanesian Spearhead Group | Artème Pointel | New Caledonia | [work](https://pacificdatavizchallenge.org/sites/default/files/POINTEL-Arteme_Pacific-DataViz-Challenge-2022.pdf) |
| 2022 | Others | Teamwork Prize | Kiribati Vanuatu Food Security | Enterprise DNA Challenge | United Kingdom | [work](https://app.powerbi.com/view?r=eyJrIjoiM2U1NmViMTktM2U5OC00NWEyLWFhNDYtYjY2OGMwNTdkYmQ5IiwidCI6ImJkM2ZjNmFlLWE0NTUtNGFlYS1hM2RiLTI4NzlkMjI1MzM4NiIsImMiOjEwfQ%3D%3D) |
| 2022 | Others | 2nd Prize | Pacific Countries Indicators Dashboard | Jonas Brouillon | New Caledonia | [work](https://jbrouillon.shinyapps.io/Pacific-Dashboard/) |

## Saved Files

- `official_datasets_2026.csv`: all 27 official datasets, source links, and generated SDMX API CSV URL patterns.
- `past_winners_links.csv`: curated winners/highly-commended list from 2022-2025.
- `past_entries_2022_2025.csv`: broader scrape of 285 past entries for later inspiration and pattern mining.
