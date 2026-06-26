import type { ScoreKey } from "./encoding";

export type AtlasLayer = {
  id: ScoreKey;
  label: string;
  description: string;
  caveat: string;
};

// V1 score layers. The signature "Where the data goes quiet" coverage view and
// the uncertainty view are overlay MODES handled separately, not score layers.
export const atlasLayers: AtlasLayer[] = [
  {
    id: "gap",
    label: "Adaptation gap",
    description: "Climate pressure minus visible capacity, ranked within the Pacific.",
    caveat: "Comparative screen, not a ranking of need. Most ranks are fragile.",
  },
  {
    id: "pressure",
    label: "Climate pressure",
    description: "Climate-signal and observed-stress indicators combined.",
    caveat: "One side of the gap; combines several official indicators.",
  },
  {
    id: "capacity",
    label: "Visible capacity",
    description: "Monitoring, power, and fisheries-governance proxies.",
    caveat: "Capacity here is a proxy from official datasets, not a full measure of readiness.",
  },
];
