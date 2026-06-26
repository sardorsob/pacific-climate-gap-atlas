# Claude Storyboard Prompt

## How To Use This File

You are Claude, joining the Pacific Adaptation Gap Atlas project to help plan the narrative and visual storyboard for `TASK-018`.

Read this prompt first, then review the source files listed below. Your job is not to build the app yet. Your job is to help turn the completed EDA into an evidence-backed storyboard and design brief that a later design/build pass can use.

When you respond, write in a way that another agent and the project owner can critique. Prefer concrete narrative options, specific screen beats, and explicit caveats over generic dashboard advice.

## Project Frame

Project name: Pacific Adaptation Gap Atlas

Competition: Pacific Dataviz Challenge 2026

Deadline: August 31, 2026

Working artifact: public interactive GIS-first web visualization

Current thesis:

Pacific island countries face climate burdens they did little to create, but the size and shape of the adaptation gap varies by geography. The atlas should help readers explore where climate signals, observed stress, monitoring coverage, and response-capacity proxies appear most out of balance.

The desired product is not a marketing website. It should be a map-first exploratory atlas with a strong analytical spine. It should feel like a careful GIS tool and visual story, not a decorative landing page or a generic dashboard.

## Current Task

We are starting `TASK-018`: story synthesis and design brief.

Relevant task definition:

- Synthesize the EDA evidence into the strongest responsible story.
- Pick story arcs, layer priorities, country exemplars, and caveat placements.
- Label story confidence and unresolved uncertainty.
- Produce `context/STORY_BRIEF.md`.
- Produce `context/DESIGN_BRIEF.md`.
- Acceptance criterion: Claude receives a concrete, evidence-backed visual brief rather than abstract layout instructions.

This file is the first collaboration prompt for that process. Treat your output as a draft to be reviewed, challenged, and refined before anything becomes final.

## Files You Should Read First

Read these context files before proposing a storyboard:

- `context/PROJECT.md`
- `context/SCOPE.md`
- `context/ANALYSIS_BRIEF.md`
- `context/ANALYSIS_BACKLOG.md`
- `context/DATA_CARD.md`
- `context/MODEL_CARD.md`
- `context/docs/design.md`
- `context/docs/methodology.md`
- `context/TASKS.md`, especially `TASK-018`

Then inspect the main EDA artifacts:

- `artifacts/provenance/eda_summary.json`
- `artifacts/tables/eda_country_story_labels.csv`
- `artifacts/tables/eda_country_drivers.csv`
- `artifacts/tables/eda_monitoring_gap.csv`
- `artifacts/tables/eda_spatial_typologies.csv`
- `artifacts/tables/eda_subregion_comparisons.csv`
- `artifacts/tables/eda_rank_volatility.csv`
- `artifacts/tables/eda_outlook_interpretation.csv`
- `artifacts/tables/eda_indicator_forensics.csv`
- `artifacts/tables/eda_coverage_by_geography.csv`
- `artifacts/tables/eda_coverage_by_dataset.csv`

Use these as evidence. Do not invent findings that are not present in the files.

## Key Evidence Already Known

These are current project-level signals, but you should verify them against the artifacts before relying on them.

1. The EDA currently covers 22 Pacific geographies and 9 official datasets.
2. Primary high-gap story candidates are PN, NR, AS, WF, and TV.
3. Priority high-gap plus low-monitoring candidates are PN, NR, AS, and WF.
4. PN and NR have latest monitoring rows reporting zero.
5. AS and WF have no monitoring rows in the processed observations, so they must be described as reporting gaps unless externally verified.
6. Polynesia currently has the highest mean adaptation-gap score and the most high-gap/low-capacity cases.
7. Melanesia reads more as high-pressure with higher visible capacity.
8. Micronesia is mostly mixed-gap context with fragile ranks.
9. Rank robustness is weak. Leave-one-indicator sensitivity labels 19 geographies fragile and 3 sensitive. Avoid definitive leaderboard language.
10. The outlook table has 88 rows: 28 `show`, 48 `show_with_strong_caveat`, and 12 `withhold`.
11. Outlook should be framed as stress-test display guidance, not forecasting.
12. Current map geometry is centroid fallback, not authoritative boundary polygons.

## Analytical Guardrails

Use these rules in every narrative option.

- This is descriptive EDA, not causal inference.
- Do not frame the Adaptation Gap Index as a definitive measure of need, vulnerability, readiness, or funding priority.
- Do not imply missing monitoring rows prove infrastructure absence.
- Do not compare indicator outliers across incompatible units or datasets.
- Do not present country rank order as definitive.
- Do not treat Pacific subregions as cultural or political boundaries. They are descriptive statistical groupings.
- Do not turn emissions context into moral ranking. Use it only to explain responsibility mismatch.
- Do not present outlook layers as predictions.
- Do not design around polygon choropleths unless a boundary source has been selected and documented.
- Keep caveats near the claim they qualify, not hidden in a late methodology page.

## Product And Design Direction

The atlas should be:

- map-first
- exploratory
- GIS-flavored
- careful with uncertainty
- compact and useful rather than decorative
- visually strong enough for a dataviz competition
- Pacific-specific in language and framing

The first screen should be the actual atlas experience, not a landing page. The user should immediately see a Pacific map and a clear first layer.

The design can still have a narrative route. Think of it as an exploratory atlas with guided story beats, not a linear scrollytelling article that hides the map.

## Main User Flow

Use this existing flow unless you have a strong reason to propose a change:

1. User lands on the atlas map.
2. User selects an adaptation-gap, pillar, monitoring-gap, or story-priority layer.
3. User clicks a country or territory centroid.
4. Side panel explains climate signal, observed stress, capacity, missingness, rank uncertainty, and sources.
5. User opens methodology/source drawer for details.

## Candidate Narrative Arcs To Compare

Please compare at least these three arcs. You may add a fourth if the evidence suggests one.

### Arc A: The Adaptation Gap Atlas

Core question:

Where do climate pressure signals appear high relative to visible adaptation-capacity proxies?

Why it could work:

- It matches the project thesis.
- It gives the atlas a broad frame.
- It can contain monitoring, spatial typology, rank uncertainty, and outlook as supporting layers.

Risks:

- It can become abstract if the story is only an index.
- Rank fragility means the UI must avoid sounding too certain.

### Arc B: The Monitoring Gap Story

Core question:

Where might high adaptation gaps coincide with weaker visible monitoring coverage or official reporting gaps?

Why it could work:

- PN, NR, AS, and WF form a concrete GIS story set.
- It turns a vague adaptation concept into an inspectable map problem.
- It naturally supports caveats about what the official data sees and misses.

Risks:

- Monitoring is only one adaptation-capacity proxy.
- Counts are not normalized by population, land area, coastline, station type, or hazard exposure.
- Missing rows must be framed carefully as reporting gaps.

### Arc C: The Responsibility Context Story

Core question:

How do low responsibility-context signals sit alongside high climate pressure or adaptation gaps?

Why it could work:

- It speaks to the climate justice theme.
- It can make the atlas emotionally and politically legible without blame framing.
- It may help explain why "adaptation gap" matters.

Risks:

- Responsibility-context indicators are context-only and not score drivers.
- It can become morally simplistic if written badly.
- It needs careful source-backed language.

### Arc D: Optional Outlook Stress Test

Core question:

If recent climate-signal trends continue under simple capacity scenarios, which places deserve cautious future-facing attention?

Why it could work:

- It adds a future-facing competition hook.
- It can help users explore where the gap might widen or narrow.

Risks:

- The model is a stress test, not a forecast.
- Mixed diagnostics require strong visible caveats.
- Weak or sparse diagnostic rows should be withheld from the app outlook layer.

Treat this as a secondary layer unless you can justify making it central.

## What We Need From You

Please produce a structured draft with these sections.

### 1. Recommended Story Direction

Pick the strongest main arc and explain why it is stronger than the alternatives.

Do not just pick the prettiest story. Pick the story that is:

- most evidence-backed
- most visually communicable
- least likely to overclaim
- strongest for a GIS-first interactive atlas
- likely to stand out in a dataviz competition

### 2. Narrative Thesis

Write 2 to 4 candidate thesis statements.

Each thesis should be one or two sentences. They should be clear enough to guide design, but careful enough to survive methodology review.

Avoid slogans that hide uncertainty.

### 3. Storyboard

Draft a storyboard for the atlas experience.

Use 5 to 8 beats. For each beat, include:

- screen or interaction name
- user action
- map layer or visual layer
- side-panel content
- evidence source
- caveat placement
- intended reader takeaway

Example beat format:

```markdown
### Beat 1: Open On The Gap

- User action: lands on map
- Layer: adaptation gap score centroids
- Side panel: short explanation of pressure-minus-capacity framing
- Evidence: adaptation_gap_index.csv, eda_country_story_labels.csv
- Caveat placement: visible microcopy under layer title
- Takeaway: the map is an invitation to inspect mismatches, not a final ranking
```

### 4. Layer Priority

Recommend a layer hierarchy.

Include:

- default first layer
- primary comparison layer
- secondary diagnostic layers
- optional or hidden-by-default layers
- layers that should not be shown yet

For each layer, explain why.

### 5. Country Or Territory Exemplars

Recommend 4 to 7 geographies to use as story exemplars.

For each, include:

- geography code
- why it matters
- which table supports it
- confidence level: high, medium, or low
- caveat language needed

Do not force every primary high-gap geography into the story if it makes the narrative weaker.

### 6. Visual And Interaction Direction

Propose a visual grammar for the atlas.

Address:

- map-first layout
- point or centroid rendering
- color strategy
- layer controls
- side-panel structure
- uncertainty indicators
- source/method drawer
- how to avoid leaderboard vibes
- how to make caveats visible without making the app feel dead

Do not design a polished UI yet. Give enough direction that a visual designer can work from it.

### 7. Competition Hook

Explain what would make this entry memorable compared with a standard climate dashboard.

The answer should be specific to this dataset and project, not generic dataviz language.

### 8. Risks And Open Questions

List the top risks before design begins.

Include:

- analytical risks
- narrative risks
- visual risks
- data/source risks
- decisions the project owner should make

### 9. Proposed Contents For Final Files

Draft outlines for:

- `context/STORY_BRIEF.md`
- `context/DESIGN_BRIEF.md`

These outlines should be specific enough that another agent can turn them into final files after review.

## Response Style

Be decisive, but show your reasoning.

Use plain language. Avoid grandiose claims. Avoid vague phrases like "powerful narrative" unless you explain what makes it powerful.

When you make a claim, tie it to an artifact or context file.

If the evidence does not support a story, say so clearly.

## Collaboration Protocol

This is intended to become a back-and-forth between Claude, Codex, and the project owner.

After your first response:

1. Codex will review your draft against the local artifacts.
2. Codex may mark which claims are supported, uncertain, or unsupported.
3. The project owner will give preferences about narrative tone and visual direction.
4. We will converge on final `STORY_BRIEF.md` and `DESIGN_BRIEF.md`.

Do not treat your first response as final. Treat it as the first serious storyboard proposal.

## Things To Avoid

- A generic dashboard plan.
- A decorative landing page.
- A simple ranked list of countries.
- A choropleth-first plan that assumes boundaries we do not yet have.
- A climate doom story.
- A responsibility story that turns emissions context into blame scoring.
- A future forecast story.
- A narrative that hides missingness or uncertainty.

## Best Possible Outcome

The best output from you would make the project owner say:

"This finally tells me what the atlas is about, why the map matters, what a reader should do first, which places carry the story, and where the caveats belong."

---

# Claude Storyboard Draft v1 (TASK-018, first proposal)

Status: draft for critique by Codex and the project owner. Not final. All claims below were checked against the artifacts before relying on them.

## Verification Notes (before building on the brief)

All 12 listed key-evidence signals check out against the artifacts, with two sharpening details:

1. PN (Pitcairn) is rank #1 gap but also the only data desert, with just 4 indicators, `thin indicator evidence`, `sensitive` robustness, and a withheld outlook. Its capacity score of 10.1 is partly an artifact of missingness (no imputation, methodology.md), so PN cannot anchor a "worst place" claim.
2. The entire priority-1 monitoring set (PN, NR, AS, WF) is built on zero or missing monitoring rows — AS and WF have no rows at all. This is simultaneously the cleanest GIS story and the one most dependent on data absence.

## 1. Recommended Story Direction

Arc A (Adaptation Gap Atlas) as the spine, with Arc B (Monitoring Gap) as the signature diagnostic interaction, Arc C (responsibility) as panel-level context, and Arc D (outlook) as an optional governed toggle. This matches the already-approved headline ("broader adaptation gap, with monitoring as one diagnostic layer," PROJECT.md).

Proposed reframe (the actual winning idea, fully evidence-backed):

> The honest, distinctive story is not "these are the worst-off places." It is "the adaptation picture is uneven — and so is the official data that lets us see it. The places that score worst on the gap index are frequently the same places where the data goes quiet."

The evidence forces this:
- 19 of 22 geographies are `fragile` on leave-one-indicator volatility; only 3 are even `sensitive` and none are stable; max rank range is 15 (MH) — `eda_rank_volatility.csv`. A definitive leaderboard is not defensible.
- The #1 gap geography (PN) is the one data desert; the priority-1 monitoring-gap set (PN, NR, AS, WF) is defined by zero or missing reporting rows — `eda_monitoring_gap.csv`.
- Gap is computed as pressure-minus-capacity with no imputation (methodology.md), so thin coverage mechanically inflates apparent gap.

Why this beats the alternatives:
- Arc A alone becomes "an abstract index" and, given fragility, tempts an overclaiming leaderboard UI. It needs a concrete hook.
- Arc B alone is the most visually communicable (4 clean priority points, a 2x2 quadrant map) but is literally a story about missing data; as a standalone thesis it would imply "no monitoring = no infrastructure," which the guardrails forbid. It must live inside a broader frame that names the data-absence caveat as a feature.
- Arc C alone risks moral-ranking the emissions context, which the guardrails forbid and which the data can't carry (responsibility indicators are trace-only, not score drivers).
- Arc D alone is a forecast story we explicitly must not tell; 12 of 88 outlook rows are `withhold` and 48 need strong caveats.

The synthesis — gap map as the invitation, monitoring/data-coverage as the inspectable mechanism, uncertainty made visible as the integrity move — is the most evidence-backed, most communicable, least overclaiming, and most distinctive against a standard climate dashboard.

## 2. Narrative Thesis (candidates)

1. (Recommended) "Across 22 Pacific geographies, climate pressure and visible adaptation capacity are unevenly matched — and so is the official data that lets us measure them. This atlas maps where the gap looks widest, and is honest about where the data itself goes quiet."
2. "Pacific island countries carry climate burdens they did little to create. The size of the adaptation gap varies by place, but the rankings are fragile — so this atlas is a tool for inspecting mismatches, not a scoreboard."
3. "In several high-pressure Pacific places, the official monitoring record reports zero or nothing at all. This atlas treats those silences as findings worth seeing, not blanks to hide."
4. "Adaptation gaps in the Pacific are real but hard to rank with confidence. This atlas shows the signal, the capacity proxy, and the missingness side by side, so readers can judge for themselves."

Thesis 1 is the spine; 3 is the sharp sub-thesis for the monitoring layer.

## 3. Storyboard (7 beats)

### Beat 1: Open On The Gap
- User action: lands directly on the Pacific map (no landing page); a one-line intro overlays then fades
- Layer: adaptation-gap-score centroids, graduated point size + sequential color
- Side panel: collapsed/teaser — "Gap = climate pressure minus visible capacity, ranked within the Pacific. Not a measure of need or risk."
- Evidence: `adaptation_gap_index.csv`, `eda_country_story_labels.csv`
- Caveat placement: persistent microcopy under the layer title — "Comparative screen, not a ranking of need. Most ranks are fragile."
- Takeaway: the map is an invitation to inspect mismatches, not a verdict.

### Beat 2: Pressure vs Capacity, Pulled Apart
- User action: toggles between the two pillar layers (climate pressure / visible capacity)
- Layer: pillar-score centroids; a small linked split shows a place's pressure and capacity side by side
- Side panel: "Some places carry high pressure and high visible capacity (PG, SB). Others show moderate pressure but little visible capacity (PN, WF)."
- Evidence: story-label pressure/capacity summaries; `eda_subregion_comparisons.csv`
- Caveat: "Capacity here is a proxy from a few official datasets, not a full measure of readiness."
- Takeaway: the gap is a difference, and the two sides behave differently across the region.

### Beat 3: Click A Place (Country Detail)
- User action: clicks a centroid (default exemplar: NR/Nauru)
- Layer: selected point highlighted; others dim
- Side panel: full detail — climate signal, observed stress, capacity, indicator trace (so thin-evidence places are visibly thin), rank-uncertainty chip, sources
- Evidence: `country_details.json`, `eda_indicator_forensics.csv`
- Caveat: rank-uncertainty chip next to the rank, e.g. "Nauru's rank moves between 1 and 7 under stress tests."
- Takeaway: every score is inspectable down to the rows behind it.

### Beat 4: Where The Data Goes Quiet (signature beat)
- User action: switches to the monitoring / data-coverage layer; a quadrant legend (gap x monitoring) appears
- Layer: monitoring-gap quadrant styling; PN, NR, AS, WF surfaced as the high-gap / low-monitoring corner
- Side panel: distinguishes the two kinds of silence — "PN, NR: latest monitoring row reports zero. AS, WF: no monitoring rows at all in the processed official data."
- Evidence: `eda_monitoring_gap.csv`
- Caveat (load-bearing): inline, not in a drawer — "A reporting gap is not proof that infrastructure is absent. Counts are unnormalized proxy coverage."
- Takeaway: data absence is itself a mapped finding — and it clusters with high apparent gap.

### Beat 5: How Much Do The Ranks Move?
- User action: toggles an "uncertainty" view or hovers rank chips
- Layer: points re-encoded by rank-range / fragility instead of by score
- Side panel: "19 of 22 places are fragile to dropping a single indicator. MH alone can move 15 places."
- Evidence: `eda_rank_volatility.csv`, `index_sensitivity.csv`
- Caveat: "This view exists so the gap map can't be read as a fixed scoreboard."
- Takeaway: uncertainty is a first-class layer, not fine print.

### Beat 6: Regional Texture (subregions)
- User action: filters by subregion (Polynesia / Micronesia / Melanesia)
- Layer: subregion grouping with dominant-typology labels
- Side panel: "Polynesia: highest mean gap, most high-gap/low-capacity cases. Melanesia: high pressure but higher visible capacity. Micronesia: mixed and fragile."
- Evidence: `eda_subregion_comparisons.csv`, `eda_spatial_typologies.csv`
- Caveat: "UN M49 statistical groupings, not cultural or political boundaries. Small samples (5-10 each)."
- Takeaway: there's regional structure, described carefully and non-spatially.

### Beat 7: Outlook Stress Test (optional, off by default)
- User action: opts into the outlook toggle
- Layer: only `show`-flagged scenario rows render; `withhold` rows are absent and explained
- Side panel: "If recent climate-signal trends continued under simple capacity scenarios... This is a stress test, not a forecast."
- Evidence: `eda_outlook_interpretation.csv` (28 show / 48 strong-caveat / 12 withhold)
- Caveat: strong-caveat scenarios visibly marked; PN/PG/PW withheld with a one-line reason.
- Takeaway: a future-facing prompt for curiosity, fenced by its own diagnostics.

Plus a persistent Methodology / Sources drawer reachable from any beat.

## 4. Layer Priority

- Default first layer: adaptation-gap-score centroids. It is the thesis and the entry point.
- Primary comparison layer: the two pillar layers (climate pressure, visible capacity). Without seeing the two sides, "gap" is abstract.
- Signature diagnostic layer: monitoring / data-coverage quadrant. The memorable, inspectable hook; carries the strongest caveats.
- Secondary diagnostic layers: rank-fragility/uncertainty view; subregion filter; indicator-trace within the panel.
- Optional / hidden-by-default: outlook stress test, gated row-by-row by `display_recommendation`.
- Do NOT show yet: any polygon choropleth (geometry is centroid fallback); any responsibility/emissions layer as a map encoding (trace-only context, high blame-risk — keep it as panel text); any withheld outlook rows; any single "rank leaderboard" list view.

## 5. Country / Territory Exemplars

| Geo | Why it matters | Supporting table | Confidence | Caveat language needed |
|---|---|---|---|---|
| NR Nauru | Best-evidenced primary high-gap (9 indicators, broad evidence), reports zero monitoring | story_labels, monitoring_gap | Medium-high | "Rank moves 2->7 under stress tests; sovereign-status wording needs review" |
| TV Tuvalu | The honest high-gap case: high pressure with visible monitoring (3 stations) — shows gap isn't only a data artifact | story_labels, monitoring_gap | Medium | "Still fragile (range 7); high-pressure label is descriptive" |
| AS American Samoa | Reporting-gap exemplar: high gap but no monitoring rows at all | monitoring_gap, coverage_by_dataset | Medium-low | "Missing rows = reporting gap, not confirmed absence; US-territory wording review" |
| PN Pitcairn | Teaches the caveat: #1 gap and the lone data desert with thin evidence | story_labels, eda_data_coverage | Low (use as caveat teacher, not as 'worst') | "Score partly reflects missingness; outlook withheld; tiny territory" |
| MH Marshall Islands | Poster child for rank instability (range 15) | rank_volatility | Medium | "Use explicitly to show ranks move" |
| FJ Fiji | Lower-gap / high-capacity benchmark; Melanesia contrast | story_labels, subregion | Medium-high | "Lower relative gap != low risk; comparative only" |

Deliberately not forcing WF into the headline set — it has the thinnest capacity evidence (capacity 4.5, one indicator) and a rank range of 10, so it weakens rather than strengthens the spine. Keep it available as a second reporting-gap example behind AS.

## 6. Visual & Interaction Direction

- Map-first layout: map fills the viewport; a left/bottom collapsible panel; a compact top-left layer switcher. First paint = Pacific + gap layer + one line of microcopy.
- Point/centroid rendering: graduated circles (size = magnitude, color = score). Explicit point styling signals "this is a centroid, not a territory," which is honest given the geometry caveat. Consider a faint "centroid, not boundary" note in the legend.
- Color strategy: one sequential ramp for scores; a separate categorical/hatched treatment for missingness so "no data" never reads as "low value." Reserve a distinct desaturated/hatched token for `missing_reporting` and `reported_zero`.
- Layer controls: radio-style single active score layer + a couple of independent overlays (monitoring, uncertainty). Avoid a wall of toggles.
- Side-panel structure (fixed order): place name + status -> gap score with rank-uncertainty chip -> pressure vs capacity -> top signals -> missingness/coverage state -> indicator trace (expandable) -> sources. Caveats sit beside the number they qualify.
- Uncertainty indicators: a rank chip everywhere a rank appears ("moves N-M"); a fragility glyph; the dedicated re-encode view (Beat 5). Never show a bare rank.
- Source/method drawer: always reachable; holds full methodology, dataset cards, year spans, and the guardrails.
- Avoiding leaderboard vibes: no global 1-22 ranked list as a primary surface; lead with spatial pattern and quadrants; show ranges, not just positions; let stress-test re-encoding visibly scramble the order.
- Keeping caveats alive (not dead): make missingness interactive — clicking a hatched point opens "why is this blank?" That turns caveats into discoverable content rather than gray disclaimers.

## 7. Competition Hook

1. Missing data as a first-class, clickable map layer. Most climate dashboards hide blanks; this atlas styles "reports zero" and "no rows at all" as distinct, inspectable states — and shows they cluster with high apparent gap (PN, NR, AS, WF).
2. A scoreboard that visibly refuses to be a scoreboard. The uncertainty re-encoding (19/22 fragile, MH +-15) is shown, not buried — an integrity move a data-viz competition tends to reward.
3. Pacific-specific framing of "uneven on two axes" — uneven climate/capacity match and uneven official visibility — rather than a generic "climate is bad" doom map.

## 8. Risks & Open Questions

Analytical
- Gap is inflated by missingness (no imputation) -> thin-coverage places look worse. Must be stated wherever gap is shown.
- 19/22 fragile ranks -> any rank language is a liability.

Narrative
- Monitoring story can slide into "no data = no infrastructure" (forbidden). The reporting-gap framing must be in the primary panel, not a drawer.
- Responsibility/emissions context can tip into blame ranking. Keep it as sparse panel context only.

Visual
- Centroid points may read as authoritative locations/territories. Need explicit "centroid, not boundary" cue.
- Missingness color colliding with the score ramp would be a serious misread. Needs a separate visual channel.

Data / source
- AS/WF missing monitoring rows are unverified externally; sovereign/territory status labels flagged `needs_review` for NR, TV, NC, PF, etc. — wording review needed before publication.
- No boundary polygons yet.

Decisions for the project owner
1. Confirm the spine = "uneven gap + uneven data visibility" (Thesis 1) vs a cleaner gap-only frame.
2. Is the subregion filter a major interaction (Beat 6) or a minor toggle?
3. Ship outlook (Beat 7) in v1 at all, or defer?
4. Pursue a boundary source before launch, or commit to centroid-first for the competition?
5. Sign-off owner for the political-status wording review.

## 9. Proposed Contents For Final Files

`context/STORY_BRIEF.md` outline
1. One-paragraph thesis (Thesis 1) + the two-axis reframe
2. Story confidence statement (what's strong: pattern, missingness; what's weak: ranks)
3. Chosen arc + role of B/C/D as layers
4. Beat list (the 7 beats), each with takeaway + caveat
5. Exemplar table (section 5) with confidence + required caveat language
6. Guardrail register (the 11 analytical rules, each tied to the beat that enforces it)
7. Explicit "claims we will NOT make" list
8. Open decisions for owner (section 8)

`context/DESIGN_BRIEF.md` outline
1. Layout skeleton (map-first, panel, layer switcher, drawer)
2. Layer hierarchy (section 4) with default states and gating rules (incl. outlook row gating)
3. Encoding spec: score ramp vs missingness channel; centroid styling; quadrant legend
4. Side-panel field order (section 6) with caveat-adjacency rules
5. Uncertainty UI components (rank chip, fragility glyph, re-encode view)
6. Data bindings: which app JSON/CSV feeds each layer/panel field
7. Microcopy starter set (layer titles + the load-bearing caveats, verbatim)
8. "Do not build yet" list (polygons, emissions map layer, global ranked list, withheld outlook)
9. Acceptance check: every score surface shows trace access + uncertainty + missingness state

## Open Divergence For Review

The one substantive divergence from the prior brief: section 1/2 argues the spine should explicitly be "uneven gap and uneven data visibility," because the artifacts won't support a confident ranking, and that reframing turns the weakness into the hook.

---

# Concrete Design Plan v2 (TASK-018)

Status: proposed direction pending Codex/project-owner review. Revised to v2.1 after Codex Review Pass v1 (below); see the "v2.1 changelog" at the end of this section. Grounded against the artifacts, the `research/` winners + 2026 rules, and the real app data shapes and existing React/Vite/MapLibre scaffold. Supersedes draft v1 where they differ. Proposed decisions (owner to confirm): two-axis spine; outlook included but gated; missingness-as-a-layer as the signature edge. Boundaries / expanded datasets / open-data overlays are post-story scope options (section 7), not part of the TASK-018 storyboard itself.

## 1. Locked Spine + Thesis

Spine: the adaptation picture is uneven on two axes — climate pressure vs visible capacity, and the official data that lets us see it. The places that score worst are frequently the same places where the data goes quiet.

Primary thesis (app copy): "Across 22 Pacific geographies, climate pressure and visible adaptation capacity are unevenly matched — and so is the official data behind the comparison. This atlas maps where the gap looks widest and is honest about where the record falls silent."

Sub-thesis (signature layer): "In several high-pressure places the official monitoring record reports zero, or nothing at all. We treat those silences as findings, not blanks."

## 2. Display Methodology (concrete, real fields)

### 2.1 Single source of truth (parity verified)
- Parity check (Codex-confirmed): `data/processed/app/geographies.json` and `data/processed/app/atlas_geographies.geojson` both show NR gap = 88.9403 and centroid `[166.9, -0.5]`, matching `artifacts/tables/adaptation_gap_index.csv`. The earlier "NR = 73.28" note was a stale read and is withdrawn — no current bug.
- Rule (still adopt): `artifacts/tables/adaptation_gap_index.csv` is the single source of truth for scores/ranks; `eda_*` tables are the source for labels/quadrants/uncertainty. Add a standing parity assertion to `scripts/validate_data_contracts.py` (app-data score == index score per geo) as a guard against future drift, not a fix for a present bug.

### 2.2 Missingness taxonomy (drives the signature layer) — from `eda_monitoring_gap.csv`
Field-name correction (Codex): these are the categorical values of the single `monitoring_reporting_status` field (and the related `monitoring_coverage_tier`), not separate boolean columns.
- `monitoring_reporting_status` in (`reported_positive_latest_count`) with full/visible coverage -> filled point.
- partial / low proxy coverage (`monitoring_coverage_tier == low_proxy_coverage`) -> filled point, thin ring.
- `monitoring_reporting_status == "reported_zero_latest_count"` (PN, NR, NU) -> hollow ring, dashed outline. Copy: "latest official monitoring row reports 0 — verify before reading as no infrastructure."
- `monitoring_reporting_status == "missing_monitoring_dataset_row"` (AS, WF, MP, GU) -> hollow ring, dotted outline + diagonal hatch. Copy: "no monitoring rows in processed official data — a reporting gap, not confirmed absence."
- Data-desert (`data_desert_flag == True`, PN only) -> "thin evidence" badge in panel. Wording (Codex): thin evidence makes PN's score *less stable and harder to interpret*; its low capacity score comes from the available capacity proxies, not from imputing missing values as zero.

### 2.3 Gap x monitoring quadrant (signature legend) — `monitoring_quadrant`
Use precomputed `monitoring_quadrant` and `story_priority` (priority_1..5). Priority_1 set = PN, NR, AS, WF surfaced as the high-gap/low-monitoring corner. 2x2 legend: x = monitoring (low/visible), y = gap (lower/high).

### 2.4 Uncertainty encoding — from `eda_rank_volatility.csv`
- Every rank shown gets a chip: "rank moves {scenario_rank_min}-{scenario_rank_max}" using `rank_range`/`scenario_rank_min/max`.
- `robustness_label` (fragile/sensitive) -> a fragility glyph.
- "Uncertainty view" toggle re-encodes point color to `rank_range` (gray->purple) with a shuffle animation; caption "19 of 22 places are fragile to dropping one indicator; MH moves up to 15."

### 2.5 Outlook gating — from `eda_outlook_interpretation.csv` + nested `outlook` in geographies.json
Off by default. Gating rule (clarified per Codex, no contradiction): `display_recommendation == show` (28) -> render normally as map marks; `show_with_strong_caveat` (48) -> render only with visible caveat styling (badge + muted treatment); `withhold` (12, incl. PN/PG/PW) -> do NOT render as map marks, and explain the omission in the panel / method drawer.
Field note (Codex): the top-level `outlook_2030_flat_gap_score` / `outlook_2050_flat_gap_score` cover the flat-capacity scenario only. If the UI exposes the gradual-improvement scenario, read it from the nested `outlook` object in `geographies.json` (or from `eda_outlook_interpretation.csv`), not the top-level fields.

### 2.6 Honest triple-encoding of each centroid (core grammar)
- Fill color = active score (gap/pressure/capacity ramp).
- Radius = `included_indicator_count` (4->9): thin-evidence places render visibly smaller/lighter, so missingness is felt even on the score layer. Range ~7px (4 indicators) to 24px (9).
- Ring style = missingness state (2.2).
This makes "how much data backs this dot" a permanent, pre-attentive part of the map — the spine, encoded.

## 3. Visual System (how it will look)

### 3.1 Color tokens
- Gap (warm sequential, not doom-red): `#fdf3e7 -> #f4c98a -> #e8895a -> #b5462f` (sand->coral->maroon).
- Climate pressure (cool blue, distinct): `#eef3fb -> #9db9e3 -> #4f74c4 -> #27408b`.
- Capacity (cool green, distinct from pressure): `#eef7f0 -> #a4d4ae -> #4fa873 -> #1f6b46`.
- Uncertainty re-encode: `#e9e9ee -> #b9a8d6 -> #6b4fa3` (gray->purple).
- Neutrals: ocean basemap `#0c1f2e` / land `#16303f`; panel `#0f2231` dark or `#ffffff` light; text `#0b1620` / `#f4f7f9`.
- Missingness ring: stroke `#cdd6dc`, hatch `#7f9aa8`. Never on the score ramp.

### 3.2 Map + basemap
MapLibre GL (`maplibre-gl@4.7.1`, already a dep). Custom minimal ocean-forward style (no clutter labels), center `[172, -12]` zoom 3 (from `configs/app_layers.yml`). Ocean emphasized; subtle graticule for GIS feel; antimeridian handled (Pacific spans 180deg). Points only in V1 (centroid honesty); polygons in Phase V1.1.

### 3.3 Typography
- Display/titles: a characterful serif (Fraunces or Spectral) to avoid generic-dashboard feel.
- Body/data/UI: Inter (tabular numerals for scores).
- One claim per beat rendered large in the display face — borrowing Women in the Pacific's discipline.

### 3.4 Layout — desktop
Full-bleed map. Top-left: wordmark + one-line thesis. Left rail: radio group for the 3 score layers + separate toggles (monitoring overlay, missingness emphasis, uncertainty view, outlook). Right: detail panel (~380px, slides in on select, dims other points). Bottom-left: dual legend card (color ramp + size/ring "confidence & coverage" key). Bottom-right: "Methodology & sources" drawer button + "Take the tour" button.

### 3.5 Layout — mobile (single-panel flow)
Map top ~55vh; draggable bottom sheet holds layer switch (collapsed) and detail (expanded on tap). One column; legend collapses into an info chip.

### 3.6 Legend (does real work)
Color ramp for active score; size key ("bigger = more indicators behind the score"); ring key (filled / reported-zero dashed / no-rows dotted+hatch). The legend itself teaches the spine.

### 3.7 Visual QA before locking (Codex discussion notes)
- The 7px->24px radius range may overpower score color on mobile; test a tighter range plus ring/opacity first.
- The palette (warm gap + blue pressure + green capacity + purple uncertainty + dark ocean) is a lot at once. Produce a color-role ledger and test contrast + colorblind states before implementation.
- Missingness should be default-present but subtle on the everyday score map (ring + size already carry it); the dramatic grayscale "Data coverage" overlay is the opt-in, not the default.

## 4. Screen-by-Screen Beats -> Concrete Components

Existing scaffold lives in `app/src/components/...` (currently placeholders: `AtlasMap.tsx`, `LayerControls.tsx`, `CountryPanel.tsx`).

| Beat | Component | Behavior |
|---|---|---|
| 1 Open on the gap | `AtlasMap.tsx` (wire GeoJSON), `App.tsx` | Paints gap layer + fading thesis line + persistent "comparative screen, ranks fragile" microcopy |
| 2 Pressure vs capacity | `LayerControls.tsx` | Radio swaps fill ramp (250ms); optional mini split in panel |
| 3 Click a place | `CountryPanel.tsx` | Field order in 6; trace table from `country_details.json.indicators`; rank chip |
| 4 Where data goes quiet (SIGNATURE) | new `MissingnessLegend.tsx` + map ring styling | Quadrant legend; PN/NR/AS/WF surfaced; clicking a hollow ring opens panel "Why is this blank?" |
| 5 How much do ranks move | new `UncertaintyToggle.tsx` | Re-encode to `rank_range`, shuffle anim, caption |
| 6 Regional texture | new `SubregionFilter.tsx` | Filter by subregion; caption from `eda_subregion_comparisons.csv` |
| 7 Outlook (gated, off) | extend `LayerControls.tsx` | Row-gated render; withheld explained |
| (all) Method drawer + Tour | new `MethodDrawer.tsx`, `TourStepper.tsx` | Drawer always reachable; tour walks beats 1-7 with map staying visible. Make TV (high gap WITH visible monitoring) an early tour stop so "high gap" is never conflated with "data silence" (Codex note) |

## 5. Signature Edge in Depth — "Where the Data Goes Quiet"
- Default-on subtle cue: ring style + radius signal coverage even on the gap layer, so missingness is never hidden.
- Dedicated overlay: a "Data coverage" toggle dims the score ramp to grayscale and lights only ring/hatch states + quadrant legend, so the map briefly becomes a map of what we can and can't see. Priority_1 corner (PN, NR, AS, WF) glows.
- Two silences, never conflated: dashed (reported zero) vs dotted+hatch (no rows) are visually and verbally distinct; the load-bearing caveat sits in the panel, not a drawer.
- Interactive caveat: clicking a hollow point opens "Why is this blank?" with the exact `missing_reporting_caveat` / reported-zero text from `eda_monitoring_gap.csv`.
- Visual metaphor (internal art-direction only, not a public claim): the quiet coastline — silence rendered as absence of fill, so the eye reads the holes in the record.

## 6. Edge Over Past Winners

| Winner (year) | Their strength | How we match / beat it |
|---|---|---|
| Carbon Debt (2025) | Moral arc + scrollytelling | Keep responsibility as panel context, no blame; beat via an explorable GIS tool + guided tour, not a linear article |
| Women in the Pacific (2024) | One claim per chart | Adopt one-sentence-per-beat discipline in the display face |
| Blooming (2024) | Single memorable metaphor | Our metaphor = the quiet/blank coastline (missingness made visible) |
| Blue Paradigm (2025) | Experience design | Guided tour + honest stress-test interaction over chart density |
| Visualising Digital Access (2025) | Country-card usefulness | Detail panel = inspectable card with trace + sources + coverage |
| The field (generic dashboards) | — | We refuse the leaderboard and foreground absence/uncertainty — unoccupied white space |

The one-line edge (internal framing, not a public uniqueness claim unless the research review backs it): an entry whose subject is the unevenness of the evidence itself, executed as a careful GIS tool rather than a dashboard or a scrollytelling essay.

## 7. Scope (V1 storyboard) + Post-Story Options

The TASK-018 storyboard is V1 only. The other tiers are post-story scope options to evaluate after the story handoff — they should not distract the storyboard or the final brief.

- V1 — Baseline storyboard (competition floor, submittable alone): centroid points, 9 processed datasets, missingness layer (signature), uncertainty toggle, country panel w/ trace, gated outlook (only if cheap after core layers work), method drawer, tour, mobile. Language: English is required by the rules; French is optional polish, included only if the owner explicitly wants bilingual delivery. Targets TASK-006/007 acceptance (`npm --prefix app run build`, public deploy, visible sources).

Post-story scope options (each needs its own source + license review; mostly does NOT touch the score):
- Boundary polygons: source + document island/territory boundaries (candidates: Natural Earth 10m admin-0, Pacific Data Hub boundaries, marineregions.org EEZ). Swap centroid choropleth -> polygon where geometry exists; keep centroid fallback for micro-territories; resolve the geometry caveat. Does not change scores.
- Expanded datasets: add coastline, direct disaster economic loss, renewable energy share, population growth from the 27 official sets — as panel context / exposure overlays, NOT silently into the index (changing the index reshuffles every fragile rank). A richer index, if wanted, ships as a clearly labeled "v2 index" alongside the baseline.
- Open-data overlays: OSM critical infrastructure, low-elevation coastal zone / DEM exposure, IBTrACS cyclone tracks — clearly tagged non-official reference, sources listed, license-checked. Strictly additive; most scope risk.

## 8. Data Bindings (real fields)

| Surface | File | Field(s) |
|---|---|---|
| Gap layer | `atlas_geographies.geojson` | `adaptation_gap_score`, `score_status`, `missingness_flag`, `included_indicator_count` |
| Pressure / capacity | same | `climate_pressure_score`, `capacity_score` |
| Missingness ring/quadrant | `eda_monitoring_gap.csv` | `monitoring_reporting_status`, `monitoring_quadrant`, `story_priority`, `*_caveat` |
| Rank chip / uncertainty | `eda_rank_volatility.csv` | `rank_range`, `scenario_rank_min/max`, `robustness_label` |
| Panel detail + trace | `country_details.json` | record fields + `indicators[]` (`dataset_name`, `pillar`, `latest_value`, `scoring_value`, `unit`, `indicator_score`, `source_row_hash`) |
| Outlook | `eda_outlook_interpretation.csv` + `geographies.json.outlook` | `display_recommendation`, `outlook_2030_flat_gap_score`, `outlook_2050_flat_gap_score` |
| Subregion captions | `eda_subregion_comparisons.csv` | means, dominant typology, caveats |

## 9. Risks & Guardrail Enforcement
- App/EDA score drift -> reconcile to index + assertion (2.1).
- "No data = no infrastructure" -> reporting-gap caveat in primary panel (5).
- Fragile ranks -> no global 1-22 list; ranges everywhere; uncertainty view (2.4).
- Responsibility/emissions -> panel context only, never a map ramp or blame ranking.
- Centroid misread -> "centroid, not boundary" legend note until V1.1.
- Missingness color collision -> separate channel (ring/hatch), never the ramp.
- Status wording (`needs_review_*` on NR/TV/NC/PF...) -> owner sign-off before publish.
- Accessibility (competition value + WCAG): AA contrast on all ramps, keyboard focus states, non-color encoding (size+ring) so colorblind readers still get coverage.

## 10. Final-File Outlines (kept here; deferred as separate files)
- STORY_BRIEF.md outline: thesis + two-axis reframe; confidence statement (strong: pattern/missingness; weak: ranks); chosen arc + B/C/D as layers; 7 beats w/ takeaway+caveat; exemplar table w/ confidence; guardrail register (11 rules -> enforcing beat); "claims we will NOT make"; open owner decisions.
- DESIGN_BRIEF.md outline: layout skeleton; layer hierarchy + gating; encoding spec (ramps, size, ring/hatch, quadrant); panel field order + caveat adjacency; uncertainty components; data bindings (sec 8); microcopy starter set (verbatim caveats); "do not build yet" list; acceptance check (every score surface shows trace + uncertainty + coverage).

## 11. Verification
1. Claims source-backed (TASK-018 manual QA): read this section against the `eda_*` tables; every geography/number traces to a table (the Codex supported/uncertain/unsupported pass).
2. Score parity fix: run `python scripts/build_app_data.py` then `python scripts/validate_data_contracts.py`; add/confirm an assertion that app-data gap score == `adaptation_gap_index.csv` per geo (resolves NR 73.28 vs 88.94 drift).
3. Repo hygiene: `python scripts/check_secrets.py`, `python scripts/validate_task_statuses.py`.
4. When V1 is built: `npm --prefix app run build` (TASK-006); desktop + mobile viewport smoke; WCAG AA contrast on the three ramps; sources/methods visible (TASK-007).
5. Output scope check: only `context/storyboardbrainstorm.md` was modified by this step.

## v2.1 changelog (responses to Codex Review Pass v1)

All 9 required fixes applied, plus the discussion notes:
1. Stale NR bug claim removed; parity verified (NR = 88.9403, centroid `[166.9, -0.5]`) and the parity assertion kept as a standing guard (section 2.1).
2. Missingness/score wording softened: thin evidence raises uncertainty and interpretability, it does not lower the score (no zero-imputation) (section 2.2).
3. Monitoring states corrected to values of `monitoring_reporting_status`, not boolean fields (section 2.2).
4. Outlook gating de-contradicted: show renders, strong-caveat renders only with caveat styling, withhold does not render as marks (section 2.5).
5. Outlook field scope noted: top-level `outlook_*` = flat-capacity only; gradual-improvement comes from the nested `outlook` object / EDA table (sections 2.5, 8).
6. Status changed from "approved/locked" to "proposed, pending review" (section header).
7. "Quiet coastline" and the uniqueness line marked as internal art-direction, not public claims (sections 5, 6).
8. Language scope corrected: English required, French optional polish (section 7).
9. Boundaries / expanded datasets / open-data overlays moved to "post-story scope options," separated from the V1 storyboard (section 7).
Discussion notes adopted: TV added as an early tour stop (section 4); radius-range, color-ledger, and default-subtle-missingness QA flags added (section 3.7).

Open item for owner/Codex: confirm whether gated outlook stays in V1 or is deferred (Codex leans "bonus, not spine").

---

# Codex Review Pass v1

Status: strong direction with a few required corrections before this becomes `STORY_BRIEF.md` or `DESIGN_BRIEF.md`.

Overall verdict: the two-axis spine is the right move. "Uneven adaptation gap plus uneven official visibility" is more honest and more competition-distinctive than a simple gap ranking. It lets the atlas be exploratory without becoming mushy, and it turns uncertainty/missingness into a first-class visual feature instead of a disclaimer.

## What I Would Keep

- Lines 385-402: The arc hierarchy makes sense. Adaptation gap should be the spine, monitoring/data visibility should be the signature interaction, responsibility should stay contextual, and outlook should stay gated/off by default.
- Lines 406-409 and 573-577: Thesis 1 is the strongest. It is clear, careful, and app-buildable. The sub-thesis about official monitoring records reporting zero or nothing is a good hook as long as "reporting gap, not confirmed absence" stays adjacent.
- Lines 439-445 and 651-655: "Where the Data Goes Quiet" is the best storyboard beat. This is the part that feels like a real dataviz idea rather than another climate dashboard.
- Lines 447-453 and 595-598: Rank fragility as an interaction is a strong integrity move. Keep it visible and calm. It should feel like "inspect uncertainty," not like the app is apologizing for existing.
- Lines 486-492: The exemplar set is mostly smart. NR, TV, AS, PN, MH, and FJ give us high-gap, monitoring-gap, caveat, uncertainty, and benchmark roles without forcing every geography into the headline.
- Lines 633-634: The legend doing conceptual work is exactly right. The legend should teach score, evidence density, and reporting status at once.

## Required Fixes Before Finalizing

1. Lines 581-583 and 708: The NR app-data bug appears stale. Current `data/processed/app/geographies.json`, `data/processed/app/atlas_geographies.geojson`, and `app/public/data/atlas_geographies.geojson` all show NR `adaptation_gap_score = 88.9403` and centroid `[166.9, -0.5]`, matching the index. Keep the parity assertion idea, but remove the claim that this bug currently exists.
2. Lines 380, 394, and 515-516: The wording "thin coverage mechanically inflates apparent gap" is too strong. Missingness increases uncertainty and makes PN a caveat-teacher, but the score is not directly lowered by missing values because the current method does not impute absence as zero. Better wording: "thin evidence makes the score less stable and harder to interpret; PN's low capacity score comes from the available capacity proxies, not from imputed missingness."
3. Lines 588-589: `reported_zero_latest_count` and `missing_monitoring_dataset_row` are values of `monitoring_reporting_status`, not separate boolean fields in `eda_monitoring_gap.csv`. Rewrite as `monitoring_reporting_status == "reported_zero_latest_count"` for PN/NR/NU and `monitoring_reporting_status == "missing_monitoring_dataset_row"` for AS/WF/MP/GU.
4. Lines 600-601: The outlook rule contradicts itself. It says "render only show" and then also renders `show_with_strong_caveat`. Final rule should be: show rows render normally, strong-caveat rows render only with visible caveat styling, withhold rows do not render as map marks and are explained in the panel/method drawer.
5. Line 601 and 689: The top-level `outlook_2030_flat_gap_score` / `outlook_2050_flat_gap_score` fields cover flat-capacity outlook only. If the UI exposes gradual-improvement scenarios, it needs the nested `outlook` object or `eda_outlook_interpretation.csv` as the scenario source.
6. Line 569: "approved direction" and "locked decisions" is premature. This is a strong proposal, not an approved plan. Change to "proposed direction pending Codex/project-owner review."
7. Lines 656 and 669: "Quiet coastline" and "the only Pacific entry..." are useful internal art-direction phrases, but too grand as public claims. Keep the metaphor for design exploration; avoid publishing uniqueness claims unless the research review explicitly backs them.
8. Line 673: EN/FR copy expands V1 scope. The competition requires English or French, not necessarily bilingual. Treat French as optional polish unless the owner explicitly wants bilingual delivery.
9. Lines 674-676: Boundary polygons and open-data overlays are good later phases, but they should not distract TASK-018. For the final story handoff, phrase them as post-story scope options with source/license review, not as part of the core storyboard.

## Discussion Points

- NR as the default clicked exemplar is defensible because it is broad-evidence, high-gap, and reported-zero monitoring. I would still make TV an early tour stop so the reader sees a high-gap place with visible monitoring; otherwise the story may accidentally imply "high gap always means data silence."
- The radius-by-indicator-count idea at lines 603-607 is promising, but the 7px to 24px range may overpower the score color on mobile. In visual QA, test a tighter size range plus ring/opacity before locking it.
- The color system at lines 611-617 is directionally fine, but it risks becoming warm gap + blue pressure + green capacity + purple uncertainty + dark ocean. That is a lot. Claude should produce a color-role ledger and test contrast/colorblind states before implementation.
- The missingness layer should be default-present but subtle. A dedicated "Data coverage" overlay can be dramatic, but the everyday score map should already carry enough ring/size evidence that missingness is never hidden.
- Outlook belongs in V1 only if the implementation is cheap after the core layers work. The story does not need it to be compelling; it is a bonus layer, not a spine.

## Suggested Next Claude Revision

Ask Claude to revise v2 into a cleaner `TASK-018` storyboard draft with:

1. stale NR bug claim removed,
2. missingness/score wording softened,
3. monitoring status field names corrected,
4. outlook gating clarified,
5. "proposal, not approved" status,
6. V1 scope tightened to the actual storyboard,
7. post-V1 ideas separated from the final handoff.

After that revision, Codex can turn the accepted version into `context/STORY_BRIEF.md` and `context/DESIGN_BRIEF.md`.
