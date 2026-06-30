# Winner Scroll Tour Audit

## Status

Date: 2026-06-30

Purpose: test the project-owner hunch that recent interactive Pacific Dataviz winners lean toward guided scroll stories, then decide whether the atlas should pivot from a pure explorer to a scroll-led hybrid.

Method:

- Read the curated winner list in `research/past_winners_links.csv`.
- Opened the interactive winner and highly-commended URLs from 2022-2025 in the in-app browser.
- Scrolled through custom web entries and inspected embedded Tableau, Power BI, Earth, Wix, GitHub Pages, and standalone sites.
- Compared those patterns with the current local atlas mockup at `http://127.0.0.1:5173/`.
- Treated winners as principle studies only. Do not copy visual identity, palettes, layouts, illustrations, titles, or interaction branding.

Chrome was not available to this Codex thread during the audit, so the pass used the in-app browser. A few embedded dashboard pages exposed limited DOM text; findings for those entries are based on visible wrapper behavior and available text, not full internal dashboard extraction.

## Bottom Line

Yes, a scroll-tour pivot is worth exploring, but it should be a hybrid pivot rather than a full rebuild.

Recommended direction:

- Make the default experience a **guided scroll atlas** with a sticky full-bleed map and scroll beats that change map state.
- Preserve the existing explorer implementation as the "Explore freely" state after, or alongside, the guided spine.
- Keep the current map, layer controls, country panel, data-quiet overlay, legend, source drawer, and mock data structure as the reusable core.
- Replace the current control-heavy first impression with a short scroll-led reading path that earns attention before handing control to the user.

This gives the entry the editorial clarity of recent custom winners while keeping the GIS/exploratory tool identity that makes this project distinctive.

## Winner Interaction Pattern Summary

| Year | Entry | Observed family | Useful lesson |
| --- | --- | --- | --- |
| 2025 | Paying the Heaviest of the Carbon Debt Never Incurred | Custom long-form visual essay | Strong single moral question, long vertical reveal, little control burden. |
| 2025 | Blue Paradigm | Custom immersive scroll story | "Scroll to explore" framing, policy journey, canvas-backed atmosphere tied to a decision narrative. |
| 2025 | Visualising Digital Access Across the Blue Pacific | Unavailable Replit link | Link durability matters; avoid hosts that may disappear before the required 2029 access window. |
| 2025 | The Silence of Mother Whale | Custom long-form visual essay | Memorable metaphor and vertical pacing; simple scroll can beat complex controls when the story is emotionally clear. |
| 2024 | Women in the Pacific | Custom scroll story | Best direct precedent for our stack: scroll essay, claim-first sections, SVG visuals, annotations, and sources. |
| 2024 | Blooming | Custom scroll story | Strong visual metaphor, long vertical page, hover detail as secondary interaction. |
| 2024 | A Tale of Two Futures | Embedded Tableau report | Dashboard/report framing can place, but it feels less distinctive than custom scroll stories. |
| 2024 | Briser le silence, liberer la parole | Embedded Power BI story/report | Multi-page report can work when the human question is strong, but it does not solve attention by itself. |
| 2023 | Food In Paradise | Embedded Power BI story/report | Uses explicit "data story" framing inside a dashboard shell. |
| 2023 | Carbs on the Coast | Embedded Tableau dashboard | Analytical dashboard precedent, less useful for a distinctive 2026 climate atlas. |
| 2023 | Inflation, a health risk in New Caledonia | Embedded Power BI report | Report/dashboard mode, limited visible scroll behavior in audit. |
| 2022 | Cook Islands Terrestrial Protected Areas | Google Earth explorer | GIS explorer precedent; useful for place immersion, less useful for narrative pacing. |
| 2022 | Kiribati Vanuatu Food Security | Embedded Power BI report | Dashboard/report precedent. |

## Pattern Read

Recent custom winners, especially 2024-2025, tend to open with a concrete story frame and then use vertical progression to reveal evidence. Older or embedded winners often behave more like dashboards or BI reports. The competition does not require scrollytelling, but the stronger custom web winners show that guided pacing helps a reader understand why the visualization matters.

The current atlas mockup is a zero-scroll working surface. That is good for expert exploration, but it asks a first-time judge to parse controls immediately: score layer, overlays, legend, methods, tour, caveats, and selection all appear at once. The winners suggest that we should reduce first-load cognitive load by letting scroll reveal those controls one claim at a time.

## Recommended Scroll Spine

The scroll tour should not be a separate landing page. It should be the atlas in guided mode.

1. **Opening claim:** "Where does the adaptation gap look widest, and where does the official record go quiet?" The map is already visible.
2. **Gap surface:** Adaptation-gap points appear with a compact legend and no country detail panel yet.
3. **Pressure versus capacity:** Scroll changes the layer or splits the encoding so the gap becomes a mismatch, not a rank.
4. **Inspect a place:** Select NR first, then optionally contrast TV to show that high score is not the whole story.
5. **Where data goes quiet:** Activate reporting rings and labels for PN, NR, AS, and WF; explain reported zero versus missing rows beside the marks.
6. **Rank fragility:** Re-encode to uncertainty so the reader understands why the atlas avoids a leaderboard.
7. **Evidence fingerprints:** If app-wired, show nearest evidence profiles for the selected geography. If not app-wired, leave this as a disabled or methods-only preview.
8. **Explore freely:** Release into the current atlas controls with the same selected geography and layer state.

## Implementation Implication

This is not a throwaway redesign. It can preserve most of the current implementation:

- Keep `AtlasMap` as the sticky visual stage.
- Keep layer state, selected geography state, legend, country panel, data-quiet mode, and method drawer.
- Add a scroll-state controller that maps each beat to existing layer/overlay/panel states.
- Add a `ScrollTour` or `StoryRail` component for narrative steps.
- Make "Explore freely" a persistent escape hatch and final destination.
- Keep keyboard next/back controls and URL state for the active beat.
- Respect reduced motion by changing states instantly instead of animating through them.

## Design Rules For The Pivot

- The first viewport must still show evidence, not a decorative hero.
- The map remains the substrate; text should not push it below the fold on desktop or mobile.
- Each scroll beat gets one claim, one map state, one caveat, and one action.
- Do not use scroll animation as decoration. Scroll should reveal, focus, compare, or re-encode evidence.
- Keep essential values visible without hover.
- Do not hide the legend or caveat during guided mode.
- Do not turn the final experience into a leaderboard.
- The free-explore mode should remain credible as a GIS atlas, not an afterthought.

## Decision Recommendation

Move the next visual task toward a scroll-led hybrid:

- Default: guided scroll atlas.
- Secondary: free explorer.
- Do not build a long cinematic intro.
- Do not discard the current atlas shell.

This gives us the best chance to match winner-level narrative clarity while retaining the project-specific strength: a careful, caveated GIS adaptation-gap tool.
