# Evidence Fingerprint Divergence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans when implementing this plan. Do not implement this layer until the project owner confirms whether it ships in V1 or stays as a post-V1 enhancement.

**Goal:** Add a defensible information-theory layer that compares official-data-derived evidence profiles across Pacific geographies using Jensen-Shannon divergence.

**Status:** Planned. No analysis artifacts or app wiring exist yet.

**Architecture:** Keep divergence logic in `analysis/eda/divergence.py`, run it through `scripts/run_eda.py`, save tables under `artifacts/tables/`, record caveats in `artifacts/provenance/divergence_summary.json`, and expose app data only after the analysis outputs pass QA.

**Public Framing:** Evidence Fingerprint Divergence. Public metric is JSD or plain-language similarity bands. KL divergence stays internal unless smoothing and caveats are simple enough to explain.

---

### Task 1: Method Contract

**Files:**
- Modify: `context/INFORMATION_DIVERGENCE_PLAN.md`
- Modify: `configs/eda.yml`
- Modify: `context/ASSUMPTIONS.md`

- [ ] Decide whether V1 uses one combined fingerprint or separate pressure/capacity/visibility fingerprints.
- [ ] Define vector components and expected directionality.
- [ ] Define missingness treatment and smoothing policy.
- [ ] Decide whether public UI shows exact JSD values or similarity bands.

### Task 2: Divergence Helpers

**Files:**
- Create: `analysis/eda/divergence.py`
- Create: `tests/analysis/test_divergence.py`

- [ ] Add tests for vector normalization, zero/smoothing behavior, JSD symmetry, bounded output, and deterministic sorting.
- [ ] Implement JSD with documented base and bounds.
- [ ] Add optional KL helper only for internal diagnostics.
- [ ] Keep missingness visible in outputs rather than hiding it through smoothing.

### Task 3: EDA Runner Integration

**Files:**
- Modify: `scripts/run_eda.py`
- Create: `artifacts/tables/eda_evidence_fingerprints.csv`
- Create: `artifacts/tables/eda_pairwise_jsd.csv`
- Create: `artifacts/tables/eda_similarity_neighbors.csv`
- Create: `artifacts/provenance/divergence_summary.json`

- [ ] Generate a geography-level evidence fingerprint table.
- [ ] Generate pairwise JSD rows for all ordered or unordered geography pairs with a documented convention.
- [ ] Generate nearest-neighbor rows with caveat fields and reason labels.
- [ ] Add divergence output counts and caveats to provenance.

### Task 4: Story And App Decision

**Files:**
- Modify: `context/ANALYSIS_BRIEF.md`
- Modify: `context/STORY_BRIEF.md`
- Modify: `context/DESIGN_BRIEF.md`
- Modify: `context/TASKS.md`

- [ ] QA exemplar pairs: NR, TV, PN, AS, WF, MH.
- [ ] Decide whether the layer is strong enough for V1.
- [ ] If accepted, keep it as selected-geography comparison, not a global leaderboard.
- [ ] If rejected or deferred, document why and leave the core atlas unchanged.

### Task 5: App Data And Interface, If Accepted

**Files:**
- Modify: `analysis/preprocessing/app_data.py`
- Modify: `scripts/build_app_data.py`
- Modify: `app/public/data/*`
- Modify: `app/src/*`

- [ ] Export compact similarity data to app-ready JSON.
- [ ] Add a selected-geography fingerprint panel.
- [ ] Add a similarity comparison mode that preserves monitoring/missingness marks.
- [ ] Add method-drawer explanation and required caveat copy.
- [ ] Verify desktop and mobile screenshots before committing.
