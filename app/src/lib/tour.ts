import type { ScoreKey } from "./encoding";
import type { ViewMode } from "./types";

// Canonical map state a beat asks the atlas to enter. Any field left undefined
// is not changed, so beats can carry prior state forward (e.g. "Explore freely").
export type BeatState = {
  score?: ScoreKey;
  view?: ViewMode;
  outlook?: boolean;
  selected?: string | null;
};

// A guided story beat. The same beat list drives the desktop scroll rail, the
// mobile beat sheet, the keyboard stepper, and the progress rail.
export type Beat = {
  id: string;
  short: string; // progress-rail label
  title: string;
  claim: string;
  caveat: string;
  source: string;
  action: string;
  state: BeatState;
};

// Seven-beat spine (approved plan). Regional texture and outlook are kept OUT of
// the guided spine and remain available in free exploration.
export const BEATS: Beat[] = [
  {
    id: "gap",
    short: "Gap",
    title: "Open on the gap",
    claim: "Where does the adaptation gap look widest - and where does the official record go quiet?",
    caveat: "Comparative screen, not a ranking of need. Most ranks are fragile.",
    source: "adaptation_gap_index.csv",
    action: "Scroll to begin, or jump straight to Explore freely.",
    state: { score: "gap", view: "default", outlook: false, selected: null },
  },
  {
    id: "pillars",
    short: "Pressure / capacity",
    title: "Pull pressure and capacity apart",
    claim: "The gap is a mismatch between two imperfect sides, not a rank.",
    caveat: "Capacity is a proxy from official datasets, not full readiness.",
    source: "eda_country_drivers.csv",
    action: "Toggle the two sides of the gap.",
    state: { score: "pressure", view: "default", outlook: false, selected: null },
  },
  {
    id: "anchor",
    short: "Nauru / Tuvalu",
    title: "Anchor Nauru, contrast Tuvalu",
    claim: "A high gap does not always mean the same evidence story.",
    caveat: "Nauru's rank moves 1-7 under stress tests. High gap is not the same as data silence.",
    source: "eda_monitoring_gap.csv, eda_rank_volatility.csv",
    action: "Switch the anchor between Nauru and Tuvalu.",
    state: { score: "gap", view: "default", outlook: false, selected: "NR" },
  },
  {
    id: "quiet",
    short: "Data quiet",
    title: "Where the data goes quiet",
    claim: "Some high-gap places report zero monitoring rows; others have no rows at all.",
    caveat: "A reporting gap is not proof that infrastructure is absent.",
    source: "eda_monitoring_gap.csv",
    action: "Tap a marked point, or pick one below.",
    state: { view: "coverage", outlook: false, selected: null },
  },
  {
    id: "fragility",
    short: "Rank fragility",
    title: "Rank fragility",
    claim: "This is why the atlas refuses to become a leaderboard.",
    caveat: "Rank movement frames uncertainty and should not be read as definitive.",
    source: "eda_rank_volatility.csv",
    action: "See how far ranks move.",
    state: { view: "uncertainty", outlook: false, selected: "MH" },
  },
  {
    id: "fingerprint",
    short: "Fingerprint",
    title: "Evidence fingerprint preview",
    claim: "Similar gap scores can come from different evidence profiles.",
    caveat: "Similarity is official-data profile likeness, not shared risk, need, or responsibility.",
    source: "eda_similarity_neighbors.csv",
    action: "Read what similarity means here.",
    state: { score: "gap", view: "default", outlook: false, selected: "NR" },
  },
  {
    id: "explore",
    short: "Explore",
    title: "Explore freely",
    claim: "The guided path teaches the map. Now ask your own questions.",
    caveat: "The legend and methods stay visible throughout.",
    source: "",
    action: "Open the full atlas controls.",
    state: {},
  },
];
