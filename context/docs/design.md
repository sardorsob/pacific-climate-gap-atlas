# Design

## Product Frame

The Pacific Adaptation Gap Atlas is a map-first exploratory tool. It should feel like a GIS project with a strong analytical spine, not a dashboard pasted onto a map.

## Main User Flow

1. User lands on the atlas map.
2. User selects an adaptation-gap, pillar, monitoring-gap, or story-priority layer.
3. User clicks a country/territory centroid.
4. Side panel explains climate signal, observed stress, capacity, missingness, rank uncertainty, and sources.
5. User opens methodology/source drawer for details.

## Main Visual Pattern

- centroid-first point map layers for gap, pillar, monitoring, and story-priority scores until a boundary source is chosen
- direct country/territory selection
- compact trace, rank-volatility, monitoring, and optional trend snippets in the side panel
- visible missing-data state
- source/method caveats close to the score

## Current Story Inputs

- Primary high-gap story labels: PN, NR, AS, WF, and TV.
- Priority monitoring-gap candidates: PN, NR, AS, and WF.
- AS and WF have missing monitoring rows, so the design copy should frame them as reporting gaps unless externally verified.
- Rankings are fragile for most geographies; avoid interfaces that imply a definitive leaderboard.

## Tone

Useful, careful, and Pacific-specific. Avoid blame framing. Use emissions context to explain responsibility mismatch, not to rank moral worth.
